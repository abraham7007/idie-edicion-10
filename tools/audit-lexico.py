#!/usr/bin/env python3
# Barrido de léxico-bandera anti-IA sobre las láminas.
# Lista cerrada tomada de la skill human-academic-writing
# (references/anti-ia__LEXICO_BANDERA_ES.md). NO se amplía por intuición:
# la lista está construida sobre frecuencias medidas, y añadir términos
# "que suenan a IA" produce falsos positivos sobre prosa humana correcta.
#
# Uso:  python3 tools/audit-lexico.py     (desde src/slides/)

# -*- coding: utf-8 -*-
import re, pathlib, collections

TERMINOS = {
 "adjetivos": ["robusto","robusta","robustos","robustas","integral","holístic","multifacétic",
   "crucial","fundamental","exhaustiv","pivotal","novedos","disruptiv","meticulos",
   "comprehensiv","considerable","sustantiv"],
 "sustantivos": ["paradigma","panorama","ecosistema","sinergia","vislumbre","tapiz","tejido",
   "paisaje"],
 "iniciadoras": ["cabe destacar","cabe señalar","cabe mencionar","cabe resaltar",
   "es importante señalar","es importante mencionar","es importante destacar",
   "es preciso mencionar","vale la pena","es menester","resulta crucial",
   "resulta fundamental","es importante notar"],
 "conectores": ["en este sentido","en este contexto","en esa línea","en el marco de",
   "en el ámbito de","por consiguiente","adicionalmente","asimismo","en conclusión"],
 "aperturas": ["el presente apartado","el presente trabajo","a continuación se presenta",
   "a continuación se expone","a continuación se describe","en lo que sigue",
   "acto seguido","hoy en día","en la actualidad","en los últimos años",
   "como se ha mencionado"],
 "calcos": ["en base a","basado en","basada en","una de las principales razones",
   "por encima de todo","como resultado","más aún","en primer lugar","en segundo lugar"],
 "verbos": ["abordar","abordan","aborda","vislumbrar","dilucidar","profundizar",
   "sustentar","propiciar","dinamizar"],
 "antitesis": ["no se trata de","más que un","más que una","lejos de"],
 "locuciones": ["habida cuenta","en aras de","a tenor de","merced a","en el seno de"],
}

# Términos de la lista cerrada que en ESTE curso son vocabulario del campo y
# no marca de redacción automática. No se borran de TERMINOS —borrarlos haría
# perder el aviso cuando sí son relleno—: se separan en un informe aparte que
# hay que leer caso por caso. Cada entrada lleva la razón; sin razón escrita,
# no entra.
EXCEPCIONES = {
 "ecosistema": "objeto del curso: SINACTI, ecosistema peruano de CTI. La sesión 1 se llama así.",
 "panorama": "«panorama de inversión» es el rótulo del sector; comprobar que no abra un párrafo de relleno.",
 "en el marco de": "correcto ante una norma citada («en el marco de la Ley 30309»); incorrecto como muletilla.",
 "sustentar": "«sustentar el proyecto ante el jurado» es la acción que enseña la sesión 6.",
 "fundamental": "«investigación fundamental» es categoría de Frascati 2015, no un adjetivo enfático.",
 "novedos": "«novedosa» es el nombre literal de uno de los cinco criterios de Frascati 2015; fuera de esa lista, sí es relleno.",
}

def visible(html: str) -> str:
    html = re.sub(r"<pre[^>]*>.*?</pre>", " ", html, flags=re.S)
    html = re.sub(r'<div class="term">.*?</div>', " ", html, flags=re.S)
    html = re.sub(r'<div class="prompt-box">.*?</div>', " ", html, flags=re.S)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)

hallazgos = collections.defaultdict(list)
comprobar = collections.defaultdict(list)
for f in sorted(pathlib.Path(".").rglob("*.html")):
    txt = visible(f.read_text(encoding="utf-8")).lower()
    for cat, lista in TERMINOS.items():
        for t in lista:
            n = txt.count(t)
            if not n:
                continue
            destino = comprobar if t in EXCEPCIONES else hallazgos
            destino[cat].append((str(f), t, n))

total = 0
for cat in TERMINOS:
    if not hallazgos[cat]: continue
    print(f"\n### {cat}")
    for arch, t, n in sorted(hallazgos[cat], key=lambda x: -x[2]):
        print(f"   {n}×  «{t}»  → {arch}")
        total += n
print(f"\nTOTAL: {total} apariciones a corregir")

pendientes = sum(n for cat in comprobar for _, _, n in comprobar[cat])
if pendientes:
    print(f"\n\n### A COMPROBAR CASO POR CASO ({pendientes} apariciones)")
    print("    No son correcciones: son términos del campo que la lista marca")
    print("    igual. Se leen y se decide; no se sustituyen en bloque.\n")
    vistos = set()
    for cat in comprobar:
        for arch, t, n in sorted(comprobar[cat], key=lambda x: -x[2]):
            if t not in vistos:
                print(f"    «{t}» — {EXCEPCIONES[t]}")
                vistos.add(t)
            print(f"       {n}×  → {arch}")
