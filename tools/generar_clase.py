#!/usr/bin/env python3
"""Genera las láminas de una sesión a partir de un manifiesto JSON.

Emite archivos HTML autónomos, idénticos en forma a los escritos a mano: el
generador no deja rastro en el resultado ni se necesita para servirlo. Lo que
automatiza es exactamente lo que se hace mal a mano —la cabecera repetida, la
cadena de anterior/siguiente y el total de láminas—, no el contenido.

El manifiesto es una lista de láminas:

  {
    "clase": "clase-05",
    "sesion": "Sesión 5 · Máquinas de estados finitos",
    "laminas": [
      {"slug": "portada", "titulo": "…", "nav": "…", "icono": "i-flow",
       "clases": "slide", "contenido": "…html…", "scripts": "…"}
    ]
  }

`nav` es el rótulo corto que aparece en la tira de navegación; `titulo` es el
del <title> del documento. Se separan porque el rótulo debe caber en la tira y
el título debe ser completo.

El nombre lleva guion bajo y no guion medio para que los guiones de sesión
puedan importar generar_desde() directamente; sigue funcionando como orden
suelta sobre un manifiesto JSON.

Uso:
  python3 tools/generar_clase.py manifiesto.json [--dry]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

CABECERA = """<!doctype html>
<html lang="es">
\t<head>
\t\t<meta charset="UTF-8" />
\t\t<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0" />
\t\t<title>{titulo}</title>

\t\t<link rel="preconnect" href="https://fonts.googleapis.com" />
\t\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
\t\t<link
\t\t\thref="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"
\t\t\trel="stylesheet"
\t\t/>
\t\t<link rel="stylesheet" href="../../css/base.css" />
\t</head>
\t<body data-deck-total="{total}">
\t\t<main class="{clases}">
{contenido}
{nav}
\t\t</main>
{scripts}
\t\t<script type="module" src="../../js/deck.js"></script>
\t</body>
</html>
"""

ENLACE_ANT = """\t\t\t\t<a class="slide-nav__link" href="{href}">
\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#{icono}" /></svg>
\t\t\t\t\t<span>{rotulo}</span>
\t\t\t\t</a>"""

ENLACE_SIG = """\t\t\t\t<a class="slide-nav__link" href="{href}">
\t\t\t\t\t<span>{rotulo}</span>
\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#{icono}" /></svg>
\t\t\t\t</a>"""


def nombre(indice: int, slug: str) -> str:
    return f"{indice + 1:02d}-{slug}.html"


def bloque_nav(laminas: list[dict], i: int) -> str:
    partes = ['\t\t\t<nav class="slide-nav" aria-label="Navegación de la diapositiva">']
    if i > 0:
        prev = laminas[i - 1]
        partes.append(
            ENLACE_ANT.format(
                href=nombre(i - 1, prev["slug"]),
                rotulo=prev.get("nav", prev["titulo"]),
                icono=prev.get("icono", "i-flow"),
            )
        )
    else:
        # La portada no tiene lámina anterior; el hueco mantiene la
        # distribución de la tira, que es un grid de dos columnas.
        partes.append("\t\t\t\t<span></span>")
    if i < len(laminas) - 1:
        sig = laminas[i + 1]
        partes.append(
            ENLACE_SIG.format(
                href=nombre(i + 1, sig["slug"]),
                rotulo=sig.get("nav", sig["titulo"]),
                icono=sig.get("icono", "i-flow"),
            )
        )
    else:
        partes.append("\t\t\t\t<span></span>")
    partes.append("\t\t\t</nav>")
    return "\n".join(partes)


def generar_desde(m: dict, seco: bool = False) -> int:
    """Emite las láminas de un manifiesto ya cargado en memoria.

    Los guiones de cada sesión llaman aquí en vez de escribir un JSON
    intermedio: el contenido es HTML, y en Python cabe en cadenas triples
    legibles, mientras que en JSON habría que escapar cada comilla.
    """
    laminas = m["laminas"]
    total = len(laminas)
    destino = RAIZ / "src" / "slides" / m["clase"]
    destino.mkdir(parents=True, exist_ok=True)

    for i, lam in enumerate(laminas):
        html = CABECERA.format(
            titulo=lam["titulo"],
            total=total,
            clases=lam.get("clases", "slide slide--start"),
            contenido=lam["contenido"].rstrip("\n"),
            nav=bloque_nav(laminas, i),
            scripts=lam.get("scripts", ""),
        )
        archivo = destino / nombre(i, lam["slug"])
        if seco:
            print(f"  · {archivo.relative_to(RAIZ)}")
        else:
            archivo.write_text(html)
    print(f"{'(simulado) ' if seco else ''}{total} láminas en {destino.relative_to(RAIZ)}")
    return total


def generar(ruta_manifiesto: Path, seco: bool) -> int:
    return generar_desde(json.loads(ruta_manifiesto.read_text()), seco)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    generar(Path(sys.argv[1]), "--dry" in sys.argv)
