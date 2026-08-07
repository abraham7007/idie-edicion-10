#!/usr/bin/env python3
"""Genera index.html, la portada del curso desde la que se elige la sesión.

Se genera y no se escribe a mano por la misma razón que las láminas: el
recuento de diapositivas y qué sesiones existen cambia con cada construcción,
y una lista escrita a mano queda desfasada al día siguiente. Aquí se leen las
carpetas de `src/slides/` y el propio HTML de cada portada.

El modo presentación ya contempla esta dirección: `src/js/presenter.js` acepta
`/index.html` dentro de su marco, así que cambiar de sesión no obliga a salir
de pantalla completa y volver a entrar.

Uso, desde tools/:
  python3 indice.py
"""

from __future__ import annotations

import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# El temario de las seis sesiones. Vive aquí porque el índice tiene que poder
# anunciar una sesión que todavía no está construida: sin esto, la sesión 5 no
# existiría en el índice hasta el día en que se genere, y quien abra el curso
# no sabría que va a haberla.
SESIONES = [
    ("01", "Fundamentos y ecosistema I+D+i+e",
     "Qué cuenta como I+D, la escala de madurez tecnológica y el mapa del "
     "sistema peruano de ciencia, tecnología e innovación."),
    ("02", "<i>Startups</i>, <i>spin-offs</i> y transferencia",
     "Las figuras con las que un resultado de investigación sale de la "
     "universidad, y qué exige cada una."),
    ("03", "Mapa de financiamiento e inversión",
     "Los instrumentos disponibles, quién los opera y con qué contrapartida "
     "se accede a cada uno."),
    ("04", "Formulación de proyectos",
     "Del problema al marco lógico: objetivos, indicadores, supuestos y la "
     "evidencia que sostiene cada uno."),
    ("05", "Presupuesto, ejecución y propiedad intelectual",
     "Partidas admisibles, cronograma de desembolsos, las obligaciones que "
     "empiezan cuando el proyecto se gana, y la propiedad intelectual de la "
     "ejecución: patentes, licencias comerciales y parques tecnológicos."),
    ("06", "<i>Pitch Elevator</i> y tendencias mundiales en I+D+i+e",
     "Defensa ante un comité y hacia dónde va el ecosistema global, con cuánta "
     "de la cooperación internacional acaba llegando al Perú y por qué vía."),
]


def sesion_construida(numero: str) -> dict | None:
    """Devuelve el recuento y la primera lámina, o None si no existe."""
    carpeta = RAIZ / "src/slides" / f"clase-{numero}"
    laminas = sorted(carpeta.glob("*.html")) if carpeta.is_dir() else []
    if not laminas:
        return None
    # El total se lee del atributo que el generador escribe en <body>, no del
    # número de ficheros: si sobra un HTML de una lámina retirada, el atributo
    # sigue diciendo la verdad y el recuento de ficheros no.
    crudo = laminas[0].read_text(encoding="utf-8")
    m = re.search(r'data-deck-total="(\d+)"', crudo)
    figuras = sum(
        len(re.findall(r'data-figure="', f.read_text(encoding="utf-8")))
        for f in laminas
    )
    pdf = RAIZ / "src/pdf" / f"clase-{numero}.pdf"
    return {
        "total": int(m.group(1)) if m else len(laminas),
        "figuras": figuras,
        "primera": f"/src/slides/clase-{numero}/{laminas[0].name}",
        # El PDF se exporta a src/ para que lo sirva el servidor: desde aquí se
        # descarga sin salir del navegador.
        "pdf": f"/src/pdf/clase-{numero}.pdf" if pdf.is_file() else "",
    }


def tarjeta(numero: str, titulo: str, sumario: str, estado: dict | None) -> str:
    if estado is None:
        return f"""\t\t\t\t<article class="idx__card idx__card--pendiente">
\t\t\t\t\t<span class="idx__n">{numero}</span>
\t\t\t\t\t<h2 class="idx__title">{titulo}</h2>
\t\t\t\t\t<p class="idx__lede">{sumario}</p>
\t\t\t\t\t<span class="idx__estado">En preparación</span>
\t\t\t\t</article>"""
    # La tarjeta es un <div> y no un <a>: lleva dentro el enlace al PDF, y un
    # ancla dentro de otra no es HTML válido. El enlace principal cubre la
    # tarjeta con un seudoelemento y el del PDF se pone por encima.
    # El enlace al PDF se retiró al publicar el curso: el repositorio lleva la
    # presentación interactiva y no los PDF, y un botón que apunta a un archivo
    # ausente es peor que no tenerlo.
    pdf = ""
    return f"""\t\t\t\t<div class="idx__card">
\t\t\t\t\t<span class="idx__n">{numero}</span>
\t\t\t\t\t<h2 class="idx__title">
\t\t\t\t\t\t<a class="idx__go" href="{estado['primera']}">{titulo}</a>
\t\t\t\t\t</h2>
\t\t\t\t\t<p class="idx__lede">{sumario}</p>
\t\t\t\t\t<span class="idx__estado idx__estado--lista">
\t\t\t\t\t\tDisponible
\t\t\t\t\t</span>{pdf}
\t\t\t\t</div>"""


def main() -> None:
    estados = {n: sesion_construida(n) for n, _, _ in SESIONES}
    listas = [n for n, e in estados.items() if e]
    tarjetas = "\n".join(tarjeta(n, t, s, estados[n]) for n, t, s in SESIONES)
    primera_lista = estados[listas[0]]["primera"] if listas else ""

    presentar = ""
    if primera_lista:
        presentar = (
            f'\t\t\t\t<a class="idx__present" href="/presentar.html#{primera_lista}">'
            f'\n\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#i-play" /></svg>'
            f'\n\t\t\t\t\tModo presentación'
            f'\n\t\t\t\t</a>'
        )

    salida = f"""<!doctype html>
<html lang="es">
\t<head>
\t\t<meta charset="UTF-8" />
\t\t<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0" />
\t\t<title>Diseño y Gestión de Proyectos I+D+i+e · OTI-UNI</title>

\t\t<link rel="preconnect" href="https://fonts.googleapis.com" />
\t\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
\t\t<link
\t\t\thref="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600;700&amp;family=IBM+Plex+Sans:wght@400;500;600;700&amp;display=swap"
\t\t\trel="stylesheet"
\t\t/>
\t\t<link rel="stylesheet" href="/src/css/base.css" />
\t</head>
\t<body class="idx">
\t\t<main class="idx__wrap">
\t\t\t<header class="idx__head">
\t\t\t\t<span class="idx__eyebrow">Programa de Iniciación Tecnológica · OTI-UNI</span>
\t\t\t\t<h1 class="idx__h1">Diseño y Gestión de Proyectos I+D+i+e</h1>
\t\t\t\t<p class="idx__sub">
\t\t\t\t\tDécima edición · seis sesiones de tres horas · fondos, instrumentos
\t\t\t\t\ty herramientas para formular un proyecto
\t\t\t\t</p>
{presentar}
\t\t\t</header>

\t\t\t<div class="idx__grid">
{tarjetas}
\t\t\t</div>
\t\t</main>

\t\t<script type="module" src="/src/js/indice.js"></script>
\t</body>
</html>
"""
    (RAIZ / "index.html").write_text(salida, encoding="utf-8")
    hechas = ", ".join(listas) if listas else "ninguna"
    print(f"index.html · sesiones construidas: {hechas}")


if __name__ == "__main__":
    main()
