/* Portada del curso (index.html). Hace dos cosas y ninguna más.

   1. Respeta el tema que el mazo dejó guardado. La clave de almacenamiento es
      la misma que usa deck.js: entrar al índice con el modo oscuro puesto y
      verlo en claro delata que son dos páginas distintas, y no lo son.
   2. Deja elegir la sesión con el teclado. Del 1 al 6 abre la sesión
      correspondiente, que es el gesto natural cuando la proyección ya está en
      marcha y el ratón está lejos.

   No monta la lista de sesiones: eso lo escribe tools/indice.py leyendo las
   carpetas de láminas, porque el recuento cambia con cada construcción. */

const CLAVE_TEMA = "idie-theme";

const guardado = localStorage.getItem(CLAVE_TEMA);
if (guardado === "dark" || guardado === "light") {
	document.documentElement.dataset.theme = guardado;
}

/* El atajo se limita a las sesiones ya construidas. Las pendientes se pintan
   como <article> y sin enlace, así que aquí no aparecen: pulsar su número no
   hace nada, que es lo correcto. */
const tarjetas = [...document.querySelectorAll(".idx__card:has(.idx__go)")];

document.addEventListener("keydown", (e) => {
	if (e.metaKey || e.ctrlKey || e.altKey) return;
	const n = Number.parseInt(e.key, 10);
	if (!Number.isInteger(n)) return;
	const destino = tarjetas.find(
		(c) => c.querySelector(".idx__n")?.textContent.trim() === String(n).padStart(2, "0"),
	);
	if (destino) {
		e.preventDefault();
		window.location.href = destino.querySelector(".idx__go").getAttribute("href");
	}
});
