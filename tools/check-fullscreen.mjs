/* Comprueba que la pantalla completa sobrevive al avance entre láminas.

   Era el fallo reportado: cada diapositiva es un documento distinto y la API
   de pantalla completa muere con el documento, así que pulsar «siguiente»
   devolvía a modo ventana. Esta prueba avanza varias láminas y verifica que
   el documento contenedor sigue en pantalla completa después de cada salto. */

import { readdirSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

// El puerto es 5174 y no el 5173 por omisión de Vite: en esta máquina el
// 5173 lo ocupa el servidor del curso anterior. Con el puerto compartido,
// este verificador cargaba las láminas de OTRO curso y las daba por buenas
// —un falso correcto, que es peor que no verificar—. Cada curso, su puerto.
// El puerto sale de IDIE_PORT si está definida y del 5174 si no. Estaba
// escrito a mano en cuatro archivos, y el día que otro curso del mismo
// equipo ocupó el 5174 no había forma de levantar este sin apagar aquel.
const BASE = `http://localhost:${Number(process.env.IDIE_PORT) || 5174}`;

// Las láminas se descubren en disco en vez de escribirse aquí. La versión
// original nombraba dos archivos concretos del curso anterior, y al cambiar
// de curso la prueba fallaba por no encontrarlos: acusaba a la pantalla
// completa de un problema que era suyo. Además, así el número de saltos se
// ajusta solo a las sesiones que existan hoy.
const RAIZ = path.resolve(import.meta.dirname, "..");
const SLIDES = path.join(RAIZ, "src", "slides");

// withFileTypes y no el nombre suelto: en src/slides puede haber archivos
// que no son sesiones (.gitignore, notas), y recorrerlos como si fueran
// carpetas rompe el verificador con un error que no dice nada del mazo.
const rutas = readdirSync(SLIDES, { withFileTypes: true })
	.filter((e) => e.isDirectory())
	.map((e) => e.name)
	.sort()
	.flatMap((clase) =>
		readdirSync(path.join(SLIDES, clase))
			.sort()
			.filter((f) => f.endsWith(".html"))
			.map((f) => `/src/slides/${clase}/${f}`),
	);

if (rutas.length < 2) {
	console.log(
		`Hacen falta al menos 2 láminas para probar el avance; hay ${rutas.length}.`,
	);
	process.exit(0);
}

// Tantos saltos como permitan las láminas existentes, con 5 de tope: pasado
// ese punto la prueba deja de aportar y solo alarga la ejecución.
const SALTOS = Math.min(5, rutas.length - 1);
const nav = await chromium.launch({ channel: "chrome" });
const pagina = await nav.newPage({ viewport: { width: 1280, height: 800 } });

const enPantallaCompleta = () =>
	pagina.evaluate(() => Boolean(document.fullscreenElement));
const rutaInterior = () =>
	pagina.evaluate(
		() => document.getElementById("marco").contentWindow.location.pathname,
	);

await pagina.goto(`${BASE}/presentar.html#${rutas[0]}`, {
	waitUntil: "networkidle",
});
await pagina.waitForTimeout(400);

console.log(
	"antes del gesto:",
	await enPantallaCompleta(),
	"|",
	await rutaInterior(),
);

// Primer gesto: debe entrar en pantalla completa.
await pagina.keyboard.press("ArrowRight");
await pagina.waitForTimeout(700);
console.log(
	"tras 1er gesto:",
	await enPantallaCompleta(),
	"|",
	await rutaInterior(),
);

const fallos = [];
for (let i = 2; i <= SALTOS; i++) {
	// Sin tocar el foco a mano: el marco debe devolverlo a la diapositiva por
	// su cuenta, que es lo que hace que las flechas funcionen de verdad.
	await pagina.keyboard.press("ArrowRight");
	await pagina.waitForTimeout(600);
	const fs = await enPantallaCompleta();
	const ruta = await rutaInterior();
	console.log(`salto ${i}: pantalla completa = ${fs} | ${ruta}`);
	if (!fs) fallos.push(`salto ${i}`);
}

await nav.close();

if (fallos.length) {
	console.log(`\n✗ se salió de pantalla completa en: ${fallos.join(", ")}`);
	process.exitCode = 1;
} else {
	console.log("\n✓ la pantalla completa se mantuvo en todos los saltos");
}

/* --------------------------------------------------------------------------
   Segundo escenario: el recorrido real del usuario. Se abre una diapositiva
   suelta, se pulsa su botón de pantalla completa y se comprueba que acaba en
   el modo presentación, que entra a pantalla completa y que avanzar con el
   ratón la conserva.
   -------------------------------------------------------------------------- */

const nav2 = await chromium.launch({ channel: "chrome" });
const p2 = await nav2.newPage({ viewport: { width: 1280, height: 800 } });

// Una lámina que NO es la portada: el recorrido real del usuario empieza en
// mitad del mazo, y la portada tiene su propia cadena de navegación truncada.
await p2.goto(`${BASE}${rutas[Math.min(1, rutas.length - 1)]}`, {
	waitUntil: "networkidle",
});
await p2.click('.deck-controls__btn[aria-label="Pantalla completa"]');
await p2.waitForURL(/presentar\.html/, { timeout: 5000 });
await p2.waitForTimeout(600);

const dentro = () =>
	p2.evaluate(
		() => document.getElementById("marco").contentWindow.location.pathname,
	);
const fs2 = () => p2.evaluate(() => Boolean(document.fullscreenElement));

console.log("\n--- desde el botón de una lámina suelta ---");
console.log(
	"marco cargado con:",
	await dentro(),
	"| pantalla completa:",
	await fs2(),
);

// Avanzar con el ratón, pulsando el enlace «siguiente» dentro del marco.
const errores = [];
for (let i = 1; i <= Math.min(3, rutas.length - 2); i++) {
	const marco = p2.frames()[1];
	await marco.click(".slide-nav a.slide-nav__link:last-of-type");
	await p2.waitForTimeout(700);
	const ok = await fs2();
	console.log(`clic ${i}: pantalla completa = ${ok} | ${await dentro()}`);
	if (!ok) errores.push(`clic ${i}`);
}

await nav2.close();

if (errores.length) {
	console.log(`\n✗ se salió de pantalla completa en: ${errores.join(", ")}`);
	process.exitCode = 1;
} else {
	console.log("✓ el botón lleva al modo presentación y el ratón lo conserva");
}
