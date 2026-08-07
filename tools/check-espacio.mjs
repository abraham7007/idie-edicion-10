/* Mide cuánto de la hoja usa cada lámina y exporta el mazo a PDF.

   El verificador de láminas responde a «¿cabe?». Esta herramienta responde a
   la pregunta contraria, que es la que quedaba sin medir: «¿sobra?». Una
   lámina que ocupa la mitad del panel se lee como una lámina sin terminar
   (METODOLOGIA.md §4.3), y a ojo no se distingue de una que ocupa el 80 %.

   Uso:  node tools/check-espacio.mjs [--pdf] */

import { existsSync, mkdirSync, readdirSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const RAIZ = path.resolve(import.meta.dirname, "..");
// El puerto sale de IDIE_PORT si está definida y del 5174 si no. Estaba
// escrito a mano en cuatro archivos, y el día que otro curso del mismo
// equipo ocupó el 5174 no había forma de levantar este sin apagar aquel.
const BASE = `http://localhost:${Number(process.env.IDIE_PORT) || 5174}`;
const SLIDES = path.join(RAIZ, "src", "slides");
// Los PDF van dentro de `src/` y no en una carpeta oculta: así los sirve el
// servidor de desarrollo y se abren desde el navegador en
// http://localhost:5174/src/pdf/clase-01.pdf, que es como se reparten.
const SALIDA = path.join(RAIZ, "src", "pdf");
const conPdf = process.argv.includes("--pdf");

const rutas = readdirSync(SLIDES, { withFileTypes: true })
	.filter((e) => e.isDirectory())
	.map((e) => e.name)
	.sort()
	.flatMap((clase) =>
		readdirSync(path.join(SLIDES, clase))
			.sort()
			.filter((f) => f.endsWith(".html"))
			.map((f) => ({ clase, archivo: f, rel: `${clase}/${f}` })),
	);

const nav = await chromium.launch({ channel: "chrome" });
const pagina = await nav.newPage({ viewport: { width: 1440, height: 900 } });
if (conPdf) mkdirSync(SALIDA, { recursive: true });

const medidas = [];
const pdfs = {};   // clase → rutas de sus PDF temporales, en orden

for (const d of rutas) {
	await pagina.goto(`${BASE}/src/slides/${d.rel}`, { waitUntil: "networkidle" });
	// Se desactivan las animaciones de entrada: con ellas a medias, la altura
	// del contenido se mide antes de que los bloques ocupen su sitio.
	await pagina.addStyleTag({
		content:
			"*,*::before,*::after{animation:none!important;transition:none!important}" +
			"[data-animate]{opacity:1!important;transform:none!important}",
	});
	await pagina.waitForTimeout(120);

	const m = await pagina.evaluate(() => {
		const panel = document.querySelector(".slide__content");
		if (!panel) return null;
		const est = getComputedStyle(panel);
		const util =
			panel.clientHeight -
			parseFloat(est.paddingTop) -
			parseFloat(est.paddingBlockEnd || est.paddingBottom);
		// Se mide la TINTA, no las cajas. Los contenedores llevan flex y se
		// estiran hasta el borde del panel, así que medir los hijos directos
		// daba 100 % en láminas que a ojo están a dos tercios. Se recorren las
		// hojas del árbol —lo que de verdad dibuja algo— y se toma la unión de
		// sus rectángulos.
		//
		// Con una excepción, y llegó midiendo mal seis láminas: una caja con
		// marco propio o fondo propio SÍ cubre su rectángulo entero. En la
		// lámina de problemas frecuentes, seis tarjetas con filo, cabecera de
		// color y relleno llenaban la hoja de arriba abajo y el medidor daba
		// 40 %, porque contaba solo el texto de dentro. Lo que el ojo ve
		// cubierto es la caja, no sus renglones.
		const conMarco = [...panel.querySelectorAll("*")].filter((x) => {
			const e = getComputedStyle(x);
			const tieneFilo = ["Top", "Right", "Bottom", "Left"]
				.some((l) => parseFloat(e[`border${l}Width`]) > 0);
			const tieneFondo = e.backgroundImage !== "none"
				|| !/^rgba?\(0, 0, 0, 0\)$|^transparent$/.test(e.backgroundColor);
			const r = x.getBoundingClientRect();
			return (tieneFilo || tieneFondo) && r.height > 12 && r.width > 12
				&& x.textContent.trim().length > 0;
		});
		const hojas = [...panel.querySelectorAll("*")].filter((x) => {
			if (x.children.length && !["svg", "TABLE"].includes(x.tagName)) {
				if (x.tagName !== "svg" && x.querySelector("*")) return false;
			}
			const r = x.getBoundingClientRect();
			return r.height > 2 && r.width > 2 && x.textContent.trim().length + (x.tagName === "svg" ? 1 : 0) > 0;
		});
		if (!hojas.length && !conMarco.length) return null;

		// No basta con medir de la primera tinta a la última: el pie de fuente
		// se ancla al canto inferior, así que ese tramo siempre da 100 % aunque
		// haya medio panel vacío en medio. Lo que se mide es el HUECO: se
		// proyectan los rectángulos sobre el eje vertical, se funden los que se
		// solapan y se busca el mayor tramo sin tinta.
		const bandas = [...hojas, ...conMarco]
			.map((x) => x.getBoundingClientRect())
			.map((r) => [r.top, r.bottom])
			.sort((a, b) => a[0] - b[0]);
		const fundidas = [];
		for (const [t, b] of bandas) {
			const ult = fundidas[fundidas.length - 1];
			if (ult && t <= ult[1] + 1) ult[1] = Math.max(ult[1], b);
			else fundidas.push([t, b]);
		}
		const cubierto = fundidas.reduce((s, [t, b]) => s + (b - t), 0);
		let hueco = 0;
		for (let k = 1; k < fundidas.length; k++) {
			hueco = Math.max(hueco, fundidas[k][0] - fundidas[k - 1][1]);
		}
		const arriba = fundidas[0][0];
		const abajo = fundidas[fundidas.length - 1][1];
		const titulo = document.querySelector(".slide__title, .wk__title");
		return {
			util: Math.round(util),
			usado: Math.round(abajo - arriba),
			cubierto: Math.round(cubierto),
			hueco: Math.round(hueco),
			cols: panel.querySelector(".duo") ? 2 : 1,
			titulo: titulo ? titulo.textContent.trim().slice(0, 50) : "—",
			// Las portadillas de tema son mínimas por norma (§4.1): un número,
			// un rótulo y un sumario de dos líneas centrados en la hoja. Medir
			// su aprovechamiento es medir contra un ideal que la norma prohíbe.
			exenta: Boolean(panel.querySelector(".sectioncard")),
		};
	});
	if (!m) continue;
	// La exención salta la MEDIDA, no la lámina: con el `continue` antes del
	// bloque del PDF, las dos portadillas de tema desaparecían del PDF y la
	// sesión 2 salía con 45 páginas de sus 47.
	if (!m.exenta) medidas.push({ ...d, ...m, pct: Math.round((m.cubierto / m.util) * 100) });

	if (conPdf) {
		// Un PDF por lámina, temporal: se unen al final en un solo archivo por
		// sesión. Playwright no sabe añadir páginas a un PDF existente.
		//
		// Los temporales se agrupan por sesión, no en una sola bolsa: al medir
		// dos sesiones de una vez, las noventa y cuatro láminas terminaban en un
		// único `clase-01.pdf`, que es justo lo contrario de la regla de un PDF
		// por clase.
		if (!pdfs[d.clase]) pdfs[d.clase] = [];
		const destino = path.join(SALIDA, "_tmp", d.clase,
			`${String(pdfs[d.clase].length).padStart(3, "0")}.pdf`);
		mkdirSync(path.dirname(destino), { recursive: true });
		await pagina.pdf({
			path: destino,
			width: "1440px",
			height: "900px",
			printBackground: true,
			pageRanges: "1",
		});
		pdfs[d.clase].push(destino);
	}
}
await nav.close();

medidas.sort((a, b) => a.pct - b.pct);
const media = Math.round(medidas.reduce((s, x) => s + x.pct, 0) / medidas.length);

console.log(`\n${medidas.length} láminas · aprovechamiento medio ${media} %\n`);
console.log("  %   hueco  col  lámina");
for (const m of medidas) {
	const marca = m.pct < 65 ? "!" : m.pct < 78 ? "·" : " ";
	console.log(
		`${marca} ${String(m.pct).padStart(3)}  ${String(m.hueco).padStart(4)}px   ${m.cols}   ` +
			`${m.archivo.replace(".html", "").padEnd(28)} ${m.titulo}`,
	);
}
const flojas = medidas.filter((m) => m.pct < 65);
console.log(`\n${flojas.length} láminas por debajo del 65 % de aprovechamiento.`);
if (conPdf) {
	const { execFileSync } = await import("node:child_process");
	const { rmSync } = await import("node:fs");
	console.log("");
	for (const [clase, paginas] of Object.entries(pdfs)) {
		const salida = path.join(SALIDA, `${clase}.pdf`);
		execFileSync("gs", [
			"-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite",
			"-dPDFSETTINGS=/prepress", `-sOutputFile=${salida}`, ...paginas,
		]);
		console.log(`PDF: ${path.relative(RAIZ, salida)}  (${paginas.length} páginas)`);
	}
	rmSync(path.join(SALIDA, "_tmp"), { recursive: true, force: true });
}
