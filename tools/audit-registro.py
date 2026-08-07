#!/usr/bin/env python3
# Registro académico en español, derivado de la skill `academic-register`
# (references/registro-es.md). Comprueba lo que esa skill vigila y que aquí
# aplica: ortotipografía de cifras, anglicismos sin cursiva, acrónimos sin
# expansión en primera mención y persona verbal prohibida.
#
# Uso:  python3 tools/audit-registro.py   (desde src/slides/)

# -*- coding: utf-8 -*-
import collections
import pathlib
import re

# Anglicismos no castellanizados: la skill exige cursiva. Se buscan fuera de
# <i> y de los bloques de código y prompt, donde son notación.
ANGLICISMOS = ["startup", "startups", "spin-off", "spin-offs", "spin-out",
               "stakeholder", "cluster", "hub", "know-how", "framework",
               "benchmarking", "pitch", "venture capital", "deep tech"]

# Acrónimos que la lámina debe expandir en su primera mención del mazo.
# Los nombres propios de institución no entran: no son términos que definir.
EXIGEN_EXPANSION = {
    "TRL": "madurez tecnológica",
    "PBI": "producto bruto interno",
    "SINACTI": "Sistema Nacional de Ciencia, Tecnología e Innovación",
    "RENACYT": "Registro Nacional de Investigadores",
    "OCDE": "Organización para la Cooperación y el Desarrollo Económicos",
    "CTI": "ciencia, tecnología",
    "GII": "Global Innovation Index",
}

PERSONA_PROHIBIDA = [r"\byo\b", r"\bconsidero\b", r"\bcreo que\b",
                     r"\busted\b", r"\bdebes\b", r"\btienes que\b", r"\btu proyecto\b"]


def visible(bruto):
    h = re.sub(r"<head>.*?</head>|<script.*?</script>|<nav.*?</nav>", " ", bruto, flags=re.S)
    h = re.sub(r'<div class="prompt-box">.*?</div>', " ", h, flags=re.S)
    # La ranura del equivalente en inglés del glosario es inglés por
    # construcción, y se distingue por su tipografía monoespaciada y su color
    # apagado. Exigirle cursiva dentro convertiría la marca en redundancia:
    # marcaba «startup» y «spin-off» justo en la lámina que los define.
    h = re.sub(r'<span class="glossary-item__en">.*?</span>', " ", h, flags=re.S)
    h = re.sub(r"<i>.*?</i>", " ", h, flags=re.S)          # ya va en cursiva
    h = re.sub(r'<div class="term">.*?</div>', " ", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


R = collections.defaultdict(list)
vistos = set()

for f in sorted(pathlib.Path(".").rglob("*.html")):
    bruto = f.read_text(encoding="utf-8")
    t = visible(bruto)
    rel = str(f)

    # 4 · coma decimal: en español el separador decimal es la coma
    # «CC BY 4.0», «Oslo 2018, 4.ª ed.», los DOI y los identificadores de
    # arXiv son notación, no cifras. El de arXiv se añadió al citar
    # arXiv:2503.14499 en la lámina del horizonte temporal: su punto separa
    # el mes del número de orden y cambiarlo por una coma rompe el enlace.
    sin_notacion = re.sub(
        r"CC BY[^,·]*|10\.\d{4,}/\S+|arXiv:\s*\d{4}\.\d{4,}|\d+\.ª", " ", t)
    for m in re.finditer(r"\b\d+\.\d+\b", sin_notacion):
        R["4 · punto decimal (debe ser coma)"].append(f"{rel}: {m.group(0)}")

    # 4 · millares: 5734 debe escribirse 5 734
    # Los DOI dentro de un enlace llegan aquí partidos —«10961», «09932»— porque
    # el marcado ya se retiró. Se limpian del texto antes de buscar millares.
    # También el número de una norma —«Ley 30309», «DS 093-2025-PCM»— y los
    # tramos numéricos de una dirección web: ninguno es un millar y separarlos
    # con espacio los rompería.
    sin_doi = re.sub(r"10\.\d{4,}\S*|s\d{5,}|doi\.org\S*", " ", t)
    sin_doi = re.sub(r"\b(Ley|Decreto|DS|RM|RS)\s+N?º?\s*[\d.\-]+", " ", sin_doi)
    sin_doi = re.sub(r"\b[\w.\-]+\.(pe|org|com|gob|edu|net|int|gov)\b\S*", " ", sin_doi)
    for m in re.finditer(r"(?<![\d.,])\d{4,}(?![\d.,\s])", sin_doi):
        if not re.match(r"(19|20)\d\d$", m.group(0)):       # los años van juntos
            R["4 · millares sin espacio"].append(f"{rel}: {m.group(0)}")

    # 4 · espacio entre cifra y unidad
    for m in re.finditer(r"\b\d+(%|ha|km|kg)\b", t):
        R["4 · unidad pegada a la cifra"].append(f"{rel}: {m.group(0)}")

    # 1 · anglicismos sin cursiva
    # Un anglicismo dentro de una dirección web no es un anglicismo: es parte
    # del nombre del dominio y ponerlo en cursiva rompería el enlace.
    sin_url = re.sub(r"\b[\w.\-]+\.(pe|org|com|gob|edu|net|int|gov)\b\S*", " ", t)
    # Tampoco lo es cuando forma parte del nombre propio de un programa: el
    # concurso se llama StartUp Perú y en cursiva dejaría de ser su nombre.
    for propio in ("StartUp Perú", "Startup Perú", "Start-Up Perú"):
        sin_url = sin_url.replace(propio, " ")
    for a in ANGLICISMOS:
        if re.search(rf"\b{re.escape(a)}\b", sin_url, re.I):
            R["1 · anglicismo sin cursiva"].append(f"{rel}: «{a}»")

    # 5 · acrónimo sin expansión en su primera aparición del mazo
    for sig in EXIGEN_EXPANSION:
        if re.search(rf"\b{sig}\b", t) and sig not in vistos:
            vistos.add(sig)
            if EXIGEN_EXPANSION[sig].split()[0].lower() not in t.lower():
                R["5 · acrónimo sin expandir en su primera mención"].append(
                    f"{rel}: {sig} → «{EXIGEN_EXPANSION[sig]}»")

    # Inciso entre guiones largos: es la marca tipográfica más reconocible de
    # un texto generado (METODOLOGIA.md §8). Se resuelve con coma, con
    # paréntesis, o partiendo la frase.
    for m in re.finditer(r"—[^—]{4,90}—", t):
        R["8 · inciso entre guiones largos"].append(f"{rel}: {m.group(0)[:60]}")

    # 3 · persona verbal prohibida
    for pat in PERSONA_PROHIBIDA:
        if re.search(pat, t, re.I):
            R["3 · persona verbal prohibida"].append(f"{rel}: {pat}")

total = 0
for k in sorted(R):
    print(f"\n### {k}  ({len(R[k])})")
    for x in R[k][:10]:
        print("   ", x)
    if len(R[k]) > 10:
        print(f"    … y {len(R[k]) - 10} más")
    total += len(R[k])
print(f"\nTOTAL: {total} observaciones de registro" if total else "\nSin observaciones de registro.")
