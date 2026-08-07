import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

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
	server: {
		port: Number(process.env.IDIE_PORT) || 5174,
		strictPort: true,
	},
});
