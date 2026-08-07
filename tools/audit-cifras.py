#!/usr/bin/env python3
# Comprobación propia de este curso (METODOLOGIA.md §2 y §11): ninguna lámina
# que enuncie una magnitud puede quedarse sin pie de fuente. Una cifra sin
# atribución es una cifra que el estudiante no puede volver a usar.
#
# Las láminas de taller se excluyen: sus números son instrucciones —«tres
# cifras», «ocho líneas»— y no datos que haya que atribuir.
#
# Uso:  python3 tools/audit-cifras.py   (desde src/slides/)

# -*- coding: utf-8 -*-
import pathlib
import re

MAGNITUD = re.compile(r"\b\d+[.,]?\d*\s*(?:%|veces|puestos?|niveles?|millones?|USD|S/)")
faltan, revisadas = [], 0

for f in sorted(pathlib.Path(".").rglob("*.html")):
    if "taller" in f.name or "glosario" in f.name:
        continue
    revisadas += 1
    bruto = f.read_text(encoding="utf-8")
    cuerpo = re.sub(r"<nav.*?</nav>|<head>.*?</head>|<script.*?</script>", " ", bruto, flags=re.S)
    if MAGNITUD.search(re.sub(r"<[^>]+>", " ", cuerpo)) and 'class="srcnote"' not in bruto:
        faltan.append(str(f))

print(f"{revisadas} láminas revisadas (los talleres y el glosario se excluyen)")
if faltan:
    print(f"\n{len(faltan)} con magnitudes y sin pie de fuente:")
    for x in faltan:
        print(f"   {x}")
else:
    print("Todas las láminas con magnitudes llevan su pie de fuente.")
