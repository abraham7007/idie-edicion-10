// Construye y verifica una sesión completa, en el orden que METODOLOGIA.md §14
// fija y §18 justifica. Existe porque el orden no es indiferente y hasta ahora
// vivía solo en la cabeza de quien lo ejecutaba: las figuras antes que las
// láminas, porque el generador de láminas cita nombres de SVG que tienen que
// existir; la verificación de maqueta antes que las auditorías de texto,
// porque reescribir prosa sobre una lámina que va a cambiar de composición
// obliga a repetir la pasada; y el PDF al final, cuando ya no queda nada que
// pueda moverse.
//
// Se detiene en el primer fallo de las etapas duras —figuras, láminas y
// maqueta—, y acumula las de auditoría, que son observaciones sobre el texto y
// se corrigen todas juntas.
//
// Uso:
//   node tools/construir.mjs 01           una sesión
//   node tools/construir.mjs 01 --pdf     y su PDF
//   node tools/construir.mjs --todas      todas las que existan

import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, rmSync } from "node:fs";
import path from "node:path";

const RAIZ = path.resolve(import.meta.dirname, "..");
// El puerto sale de IDIE_PORT si está definida y del 5174 si no. Estaba
// escrito a mano en cuatro archivos, y el día que otro curso del mismo
// equipo ocupó el 5174 no había forma de levantar este sin apagar aquel.
const PUERTO = Number(process.env.IDIE_PORT) || 5174;

const args = process.argv.slice(2);
const conPdf = args.includes("--pdf");
const todas = args.includes("--todas");
const sesiones = todas
	? readdirSync(path.join(RAIZ, "tools/clases"))
		.filter((f) => /^clase-\d\d\.py$/.test(f))
		.map((f) => f.slice(6, 8))
	: args.filter((a) => /^\d\d$/.test(a));

if (!sesiones.length) {
	console.error("Falta el número de sesión. Ejemplo: node tools/construir.mjs 01 --pdf");
	process.exit(1);
}

// El verificador de maqueta mide en un navegador contra el servidor de
// desarrollo. Sin él, mide una página vacía y da todo por bueno, que es peor
// que fallar: en una ocasión informó «sin problemas» sobre cero láminas.
function servidorVivo() {
	// Basta con que el puerto conteste algo. Exigir un 2xx en la raíz era un
	// error: este sitio es multipágina y no tiene índice en `/`, así que Vite
	// devuelve 404 con el servidor perfectamente en pie. Lo que distingue
	// «apagado» de «en pie» es el código 000, que curl da cuando no hay
	// conexión.
	const r = spawnSync("curl", ["-s", "-o", "/dev/null", "-w", "%{http_code}",
		"--max-time", "5", `http://localhost:${PUERTO}/`], { encoding: "utf8" });
	const codigo = r.stdout.trim();
	return codigo !== "" && codigo !== "000";
}

function etapa(rotulo, ejecutar, { duro = true } = {}) {
	process.stdout.write(`\n▸ ${rotulo}\n`);
	try {
		const salida = ejecutar();
		if (salida?.trim()) console.log(salida.trimEnd().split("\n").map((l) => `  ${l}`).join("\n"));
		return { ok: true };
	} catch (e) {
		const texto = [e.stdout, e.stderr].filter(Boolean).map(String).join("\n").trimEnd();
		if (texto) console.log(texto.split("\n").map((l) => `  ${l}`).join("\n"));
		if (duro) {
			console.error(`\n✗ ${rotulo}: la construcción se detiene aquí.`);
			process.exit(1);
		}
		return { ok: false, rotulo };
	}
}

const py = (script, args = [], cwd = RAIZ) =>
	execFileSync("python3", [script, ...args], { cwd, encoding: "utf8" });
const node = (script, args = []) =>
	execFileSync("node", [script, ...args], { cwd: RAIZ, encoding: "utf8" });

console.log(`Construyendo ${sesiones.length === 1 ? "la sesión" : "las sesiones"} ${sesiones.join(", ")}`);

// 1 · Figuras. Van primero: el guion de la sesión nombra los SVG y un nombre
//     que no existe deja un marco vacío que la maqueta no detecta como error.
etapa("Figuras", () => py("tools/figures/render.py").split("\n").slice(-1)[0]);

const observaciones = [];

for (const s of sesiones) {
	const guion = path.join("clases", `clase-${s}.py`);
	if (!existsSync(path.join(RAIZ, "tools", guion))) {
		console.error(`No existe tools/${guion}`);
		process.exit(1);
	}
	const laminas = path.join(RAIZ, "src/slides", `clase-${s}`);

	// 2 · Láminas. Se borra la carpeta antes: si una lámina desaparece del
	//     montaje, su HTML se queda y los verificadores siguen midiéndola.
	//
	//     Ojo con el otro lado del mismo problema: borrar y regenerar una
	//     carpeta deja al servidor de desarrollo sirviendo el HTML que tenía
	//     en memoria. Al montar la sesión 2 sobre lo que quedaba del andamio,
	//     el fichero en disco decía `02-agenda.html` y el servidor mandaba
	//     `02-estructura-proyecto.html`, una lámina que ya no existía. Eso lo
	//     denuncia la comprobación de coherencia de más abajo.
	etapa(`Láminas · sesión ${s}`, () => {
		rmSync(laminas, { recursive: true, force: true });
		return py(guion, [], path.join(RAIZ, "tools"));
	});
}

if (!servidorVivo()) {
	console.error(`\n✗ No responde el servidor en el puerto ${PUERTO}.`);
	console.error("  Arráncalo en otra terminal con `npm run dev` y repite.");
	process.exit(1);
}

// 2.b · Coherencia entre el disco y el servidor. Se compara el enlace de
//       navegación de la primera lámina con el que sirve Vite: si difieren, lo
//       que se está verificando no es lo que se acaba de generar, y todo lo que
//       venga después es ruido.
for (const s of sesiones) {
	const rel = `src/slides/clase-${s}`;
	const primera = readdirSync(path.join(RAIZ, rel)).filter((f) => f.endsWith(".html")).sort()[0];
	etapa(`Coherencia · sesión ${s}`, () => {
		const enDisco = readFileSync(path.join(RAIZ, rel, primera), "utf8");
		const servido = execFileSync("curl", ["-s", "--max-time", "10",
			`http://localhost:${PUERTO}/${rel}/${primera}`], { encoding: "utf8" });
		const saca = (t) => (t.match(/slide-nav__link" href="([^"]+)"/) || [])[1] || "";
		if (saca(enDisco) !== saca(servido)) {
			throw Object.assign(new Error("desajuste"), {
				stdout: `el disco dice «${saca(enDisco)}» y el servidor sirve «${saca(servido)}».\n`
					+ "Reinicia el servidor y borra node_modules/.vite antes de repetir.",
			});
		}
		return "el servidor sirve lo que hay en disco";
	});
}

// 3 · Maqueta. Desbordes, recortes, errores de consola y navegación rota.
//     Antes que el texto: una lámina que va a cambiar de composición no merece
//     una pasada de prosa todavía.
etapa("Maqueta", () => node("tools/check-slides.mjs"));

// 4 · Texto. Cuatro auditorías derivadas de skills y una propia del mazo. Son
//     observaciones, así que se acumulan y se corrigen juntas.
for (const [rotulo, script] of [
	["Cifras con fuente", "tools/audit-cifras.py"],
	["Léxico anti-IA", "tools/audit-lexico.py"],
	["Registro académico", "tools/audit-registro.py"],
	["Control editorial", "tools/audit-editorial.py"],
	["Reglas del mazo", "tools/audit-mazo.py"],
]) {
	const r = etapa(rotulo, () => py(path.join("..", "..", script), [], path.join(RAIZ, "src/slides")),
		{ duro: false });
	if (!r.ok) observaciones.push(rotulo);
}

// 4.b · Anatomía de la sesión. §4.5 la dejaba como seis órdenes sueltas que
//       había que recordar ejecutar; aquí se comprueban de una vez y contra los
//       números de §4.4. Es aviso y no parada: una sesión a medio construir
//       tiene que poder verificarse.
for (const s of sesiones) {
	etapa(`Anatomía · sesión ${s}`, () => {
		const dir = path.join(RAIZ, "src/slides", `clase-${s}`);
		const html = readdirSync(dir).filter((f) => f.endsWith(".html"));
		const leer = (f) => readFileSync(path.join(dir, f), "utf8");
		const cuenta = (re) => html.filter((f) => re.test(leer(f))).length;
		const figuras = new Set(
			html.flatMap((f) => [...leer(f).matchAll(/data-figure="([^"]+)"/g)].map((m) => m[1])),
		).size;
		const tablas = html.filter((f) => !f.includes("referencias") && /<table\b/.test(leer(f))).length;
		const filas = [
			// La sesión 3 es un catálogo y una ficha de fondo se consulta, no se
			// expone: no consume los tres minutos y medio que consume una lámina
			// de contenido. Por eso admite más láminas que las demás, y por eso
			// la excepción va por sesión y no para todo el mazo (§4.6).
			["láminas", html.length, 40, s === "03" ? 62 : 50],
			// Sin techo de figuras: lo tuvo y marcaba fuera de norma a la
			// sesión 1 con 31, que es justo la densidad que se pedía (§4.4).
			// La sesión 3 inventaría fondos con una ficha por lámina, y una
			// ficha no lleva figura. Bajar el mínimo para todo el mazo dejaría
			// pasar sesiones planas, así que la excepción se declara por
			// sesión (METODOLOGIA.md §4.6).
			["figuras", figuras, s === "03" ? 8 : 20, 999],
			["figuras por lámina", (figuras / html.length).toFixed(2),
				s === "03" ? 0.15 : 0.5, 9],
			["tablas de contenido", tablas, 0, 6],
			["secciones interactivas", cuenta(/data-sim/), 2, 99],
			["bloques de práctica", html.filter((f) => /(taller|herramientas)-\d/.test(f)).length,
				4, 4],
		];
		return filas
			.map(([q, v, min, max]) => {
				const ok = v >= min && v <= max;
				const rango = min === max ? `${min}` : `${min}-${max}`;
				return `${ok ? " " : "!"} ${String(v).padStart(3)}  ${q.padEnd(24)} norma ${rango}`;
			})
			.join("\n");
	}, { duro: false });
}

// 5 · Aprovechamiento del alto. Informativo: el medidor cuenta tinta, así que
//     una rejilla de tarjetas puntúa bajo con la hoja llena. Se mira en
//     captura antes de tocar nada (METODOLOGIA.md §17.8).
etapa("Aprovechamiento", () => node("tools/check-espacio.mjs"), { duro: false });

// 6 · Portada del curso. Al final porque cuenta láminas y figuras de lo que
//     acaba de generarse; escrita antes, contaría lo anterior.
etapa("Portada del curso", () => py("indice.py", [], path.join(RAIZ, "tools")));

if (conPdf) etapa("PDF", () => node("tools/check-espacio.mjs", ["--pdf"]));

console.log("");
if (observaciones.length) {
	console.log(`Maqueta correcta. Pendiente de texto en: ${observaciones.join(", ")}.`);
	process.exit(1);
}
console.log("Sesión construida y verificada. Sin observaciones.");
