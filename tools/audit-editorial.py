#!/usr/bin/env python3
# Control editorial sobre las láminas, derivado de las 18 dimensiones de la
# skill paper-review (references/control-calidad.md). Se aplican las que
# tienen equivalente en un mazo; las de manuscrito (ecuaciones numeradas,
# jerarquía de headings, voz por sección) no lo tienen.
#
# Dos familias de falso positivo conocidas, documentadas para no volver a
# investigarlas: los números que abren un .finding__value se leen como cifra
# a inicio de oración —son rótulos—, y las comillas rectas de las claves
# JSON son exigencia de la notación.
#
# Uso:  python3 tools/audit-editorial.py  (desde src/slides/)

# -*- coding: utf-8 -*-
import re, pathlib, collections

def visible(h):
    for pat in (r"<pre[^>]*>.*?</pre>", r'<div class="term">.*?</div>',
                r'<div class="prompt-box">.*?</div>', r"<script.*?</script>"):
        h = re.sub(pat, " ", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))

R = collections.defaultdict(list)
ACR = collections.defaultdict(set)

for f in sorted(pathlib.Path(".").rglob("*.html")):
    raw = f.read_text(encoding="utf-8")
    t = visible(raw)
    rel = str(f)

    # 9. Unidades SI: espacio fino entre cifra y unidad; nunca "10ms" pegado
    for m in re.finditer(r"\b\d+(?:[.,]\d+)?(ms|us|µs|kHz|MHz|Hz|mV|V|mA|kB|KB|MB|Ω|bits?|baudios)\b", t):
        R["9 · unidad pegada a la cifra"].append(f"{rel}: «{m.group(0)}»")

    # 7. Cifra al inicio de oración
    for m in re.finditer(r"(?:^|[.;] )(\d[\d.,]*)\s+[a-záéíóúñ]", t):
        R["7 · cifra al inicio de oración"].append(f"{rel}: «{m.group(0).strip()[:40]}»")

    # 14/8. Comillas rectas donde debería haber angulares o tipográficas
    n = len(re.findall(r'(?<![=<>/])"[A-Za-zÁÉÍÓÚÑáéíóúñ¿¡]', t))
    if n: R["8 · comillas rectas en texto visible"].append(f"{rel}: {n}")

    # 4. Acrónimos: se recogen para ver si alguno nunca se expande
    for m in re.finditer(r"\b([A-Z]{2,6})\b", t):
        ACR[m.group(1)].add(rel)

    # 16/18. Negrita: proporción de texto resaltado
    negrita = sum(len(x) for x in re.findall(r"<b>(.*?)</b>", raw, re.S))
    if len(t) > 400 and negrita / len(t) > 0.22:
        R["16 · exceso de negrita"].append(f"{rel}: {negrita*100//len(t)} % del texto")

    # 15. Espacio faltante alrededor de un elemento inline de código
    for m in re.finditer(r"[a-záéíóúñ]</?code>", raw):
        pass

    # 2. Referencias cruzadas: menciones a «Ejemplo NN» que no existan
    for m in re.finditer(r"Ejemplo (\d{2})", t):
        R["_ejemplos_citados"].append((rel, m.group(1)))

for k in sorted(R):
    if k.startswith("_"): continue
    print(f"\n### {k}  ({len(R[k])})")
    for x in R[k][:8]: print("   ", x)
    if len(R[k]) > 8: print(f"    … y {len(R[k])-8} más")

# 4. acrónimos usados en muchas láminas sin expansión en el glosario
glos = " ".join(visible(p.read_text(encoding="utf-8")) for p in pathlib.Path(".").rglob("*glosario*.html"))
sospechosos = {a: v for a, v in ACR.items()
               if len(v) >= 4 and a not in glos and a not in
               {
                   # ── SIGLAS QUE NO NECESITAN ENTRADA DE GLOSARIO ──
                   # Son nombres propios de institución, de programa o de
                   # norma, no términos técnicos que haya que definir. Un
                   # glosario que define «CONCYTEC» gasta una de sus once
                   # entradas en algo que la lámina ya nombró completo.

                   # notación, formatos y licencias
                   "DOI", "PDF", "CC", "BY", "NC", "ND", "SA", "JSON",
                   "URL", "OK", "KB", "MB", "USD", "PEN", "EUR", "IVA",

                   # organismos y programas peruanos
                   "CONCYTEC", "PROCIENCIA", "INDECOPI", "SINACTI", "ITP",
                   "CITE", "PNIPA", "PIE", "CTI", "UNI", "OTI", "DITT",
                   "CEPS", "CTIC", "VRI", "PIT", "MEF", "SUNAT", "MINEDU",
                   "SUNEDU", "PRONABEC", "MIPYME", "PYME",

                   # organismos y programas de la región y multilaterales
                   "ANID", "CORFO", "FAPESP", "EMBRAPII", "SECIHTI", "BID",
                   "GIZ", "AECID", "COSUDE", "GCF", "OCDE", "UE", "AICS",
                   "COOPI", "CAF", "PNUD", "UNESCO", "WIPO", "OMPI",

                   # becas, fondos y plataformas
                   "DAAD", "MSCA", "REPU", "ERC", "NSF", "NIH", "AWS",
                   "NVIDIA", "YC", "VC", "GII",

                   # bases de datos y ciencia abierta
                   "ALICIA", "RENATI", "ORCID", "OA", "PRISMA", "WOS",
                   "OPENAIRE", "SCOPUS",

                   # nombres de revista que aparecen en el pie de fuente. No
                   # gastan una entrada de glosario: quien los ve está leyendo
                   # una cita, no un término del curso.
                   "LBS", "SMJ", "JTT",

                   # instrumentos y notación de gestión ya nombrados en texto
                   "DS", "PCM", "MOU", "LOI", "NDA", "OKR", "IP", "PI", "TIC", "TT",
                   "ONG", "SAC", "SAFE", "KISS", "RBF",
               }}
print(f"\n### 4 · acrónimos en 4+ láminas sin entrada en el glosario ({len(sospechosos)})")
for a, v in sorted(sospechosos.items(), key=lambda x: -len(x[1]))[:12]:
    print(f"    {a}  en {len(v)} láminas")
