#!/usr/bin/env python3
"""Busca artículos de acceso abierto en OpenAlex y lista los descargables.

Filtra por acceso abierto y por existencia de PDF localizable, que son las
dos condiciones para que `get-paper.py` pueda traerlo. Sin ese filtro, la
mayoría de resultados relevantes no se pueden descargar y hay que
descartarlos uno a uno.

La consulta va contra TÍTULO Y RESUMEN, no contra el texto completo: es la
diferencia entre encontrar artículos del tema y encontrar artículos que
mencionan sus palabras de pasada.

Los resultados se limitan a los campos temáticos del curso (gestión,
economía, ciencias sociales y ciencias de la decisión). Pasar «todo» como
cuarto argumento levanta esa restricción.

Uso:
  python3 tools/buscar-oa.py "<consulta en inglés>" [n] [aaaa-mm-dd] [todo]
"""

from __future__ import annotations

import json
import subprocess
import sys
from urllib.parse import quote

CORREO = "infinity.witss@gmail.com"


# Campos temáticos de OpenAlex a los que pertenece este curso. Sin este
# filtro, consultas como «grant proposal funding success» devuelven ensayos
# clínicos y estudios de carga de enfermedad: la literatura biomédica domina
# el índice por volumen, y sus resúmenes usan las mismas palabras
# («funding», «project», «team», «outcome») con otro significado.
#   14 · Business, Management and Accounting
#   18 · Decision Sciences
#   20 · Economics, Econometrics and Finance
#   33 · Social Sciences
CAMPOS = "fields/14|fields/18|fields/20|fields/33"


def buscar(consulta: str, n: int = 12, desde: str = "2017-01-01",
           campos: str | None = CAMPOS) -> None:
    # title_and_abstract.search y no el parámetro `search` general: el general
    # indexa también el texto completo y la lista de referencias, así que una
    # consulta como «national innovation system Latin America» devolvía
    # estudios de carga de enfermedad que contienen esas palabras sueltas por
    # separado. Contra título y resumen, los resultados son del tema pedido.
    filtros = (
        "is_oa:true"
        f",from_publication_date:{desde}"
        f",title_and_abstract.search:{quote(consulta)}"
    )
    if campos:
        filtros += f",primary_topic.field.id:{campos}"
    url = (
        "https://api.openalex.org/works"
        f"?filter={filtros}"
        f"&per-page={n * 3}&mailto={CORREO}"
    )
    salida = subprocess.run(
        ["curl", "-sL", "--max-time", "60", url], capture_output=True, timeout=90
    )
    try:
        datos = json.loads(salida.stdout)
    except json.JSONDecodeError:
        print("  ! respuesta ilegible de OpenAlex")
        return

    mostrados = 0
    for w in datos.get("results", []):
        loc = w.get("best_oa_location") or {}
        # Sin url_for_pdf no hay descarga automática posible.
        if not loc.get("pdf_url"):
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if not doi:
            continue
        rev = (loc.get("source") or {}).get("display_name") or "—"
        print(f"\n{doi}   [{w.get('publication_year')}]  {w.get('cited_by_count')} cit.")
        print(f"  {(w.get('title') or '')[:110]}")
        print(f"  {rev[:70]}  ·  {loc.get('license') or 'sin licencia declarada'}")
        mostrados += 1
        if mostrados >= n:
            break
    if not mostrados:
        print("  (sin resultados descargables)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    buscar(
        sys.argv[1],
        int(sys.argv[2]) if len(sys.argv) > 2 else 12,
        sys.argv[3] if len(sys.argv) > 3 else "2017-01-01",
        None if len(sys.argv) > 4 and sys.argv[4] == "todo" else CAMPOS,
    )
