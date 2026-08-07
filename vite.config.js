import { readdirSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

const RAIZ = path.dirname(fileURLToPath(import.meta.url));

// Vite compila SOLO lo que se le declara como entrada. Con la configuración
// anterior `vite build` emitía index.html y nada más, así que en producción la
// portada cargaba y cualquier lámina devolvía 404: en desarrollo el servidor
// sirve los archivos tal cual y el fallo no se ve. Aquí se recorre el árbol y
// se declara cada documento HTML como su propia entrada.
function paginas(dir, acc = {}) {
	for (const nombre of readdirSync(dir)) {
		const ruta = path.join(dir, nombre);
		if (statSync(ruta).isDirectory()) {
			if (["node_modules", "dist", ".git"].includes(nombre)) continue;
			paginas(ruta, acc);
		} else if (nombre.endsWith(".html")) {
			acc[path.relative(RAIZ, ruta).replace(/[/\\.]/g, "_")] = ruta;
		}
	}
	return acc;
}

// El proyecto es multipágina por naturaleza: cada lámina es un documento HTML
// autónomo bajo src/slides/. No hay punto de entrada único ni enrutador; Vite
// sirve cada archivo tal cual y solo interviene para resolver el CSS.
//
// El puerto está fijado con strictPort porque tools/check-slides.mjs y
// tools/check-fullscreen.mjs apuntan a localhost:5174. Si Vite se desplazara a
// otro puerto al encontrarlo ocupado, el verificador cargaría lo que sirviera
// el puerto de al lado —en esta máquina, otro curso— y lo daría por bueno.
// El 5174 y no el 5173: el 5173 lo ocupa el proyecto del curso anterior.
export default defineConfig({
	plugins: [tailwindcss()],
	build: {
		rollupOptions: { input: paginas(RAIZ) },
	},
	server: {
		port: Number(process.env.IDIE_PORT) || 5174,
		strictPort: true,
	},
});
