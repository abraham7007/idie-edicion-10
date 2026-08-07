#!/usr/bin/env python3
"""Analizador de GIFT que reproduce question/format/gift/format.php.

No comprueba estilo: comprueba que Moodle vaya a leer lo mismo que se quiso
escribir. Cada paso replica el del importador —el troceado por línea en
blanco, el escapado previo, la extracción de la retroalimentación general con
`####`, y la decisión de tipo por el primer carácter del bloque de respuesta—
para que un fallo aquí sea un fallo allí.
"""
import re
import sys
import pathlib

RESERVADOS = {"\\\\": "&&092;", "\\:": "&&058;", "\\#": "&&035;",
              "\\=": "&&061;", "\\{": "&&123;", "\\}": "&&125;",
              "\\~": "&&126;", "\\n": "&&010;"}


def pre(s):
    for a, b in RESERVADOS.items():
        s = s.replace(a, b)
    return s


def post(s):
    for a, b in RESERVADOS.items():
        s = s.replace(b, a[-1])
    return s


def bloques(texto):
    """Trocea por línea en blanco, descartando comentarios."""
    actual, salida = [], []
    for linea in texto.splitlines():
        if linea.startswith("//"):
            continue
        if linea.strip() == "":
            if actual:
                salida.append("\n".join(actual))
                actual = []
            continue
        actual.append(linea)
    if actual:
        salida.append("\n".join(actual))
    return salida


def respuestas(cuerpo):
    """Trocea el bloque por ~ y = no escapados, conservando el signo."""
    partes = re.split(r"(?<!\\)([=~])", cuerpo)
    salida, signo = [], None
    for t in partes:
        if t in ("=", "~"):
            signo = t
        elif signo:
            salida.append((signo, t.strip()))
            signo = None
    return salida


def revisar(ruta):
    texto = ruta.read_text(encoding="utf-8")
    fallos, resumen = [], []
    # Dos defectos que no son de formato y que un banco entero puede tener sin
    # que ninguna pregunta suelta parezca mal: que todos los verdadero/falso
    # se resuelvan con la misma respuesta, y que la opción correcta caiga
    # siempre en la misma posición. Los dos se responden sin saber la materia.
    vf, posiciones = [], []

    if texto.startswith("﻿"):
        fallos.append("el archivo empieza con BOM; Moodle lo lee como basura")

    for bloque in bloques(texto):
        if bloque.startswith("$CATEGORY:"):
            resumen.append(("categoría", bloque.split(":", 1)[1].strip(), "", ""))
            continue

        crudo = pre(bloque)
        nombre = ""
        m = re.match(r"^::(.*?)::", crudo, re.S)
        if m:
            nombre = post(m.group(1))
            crudo = crudo[m.end():]
        else:
            fallos.append(f"pregunta sin nombre ::…:: → {bloque[:60]}")

        crudo = re.sub(r"^\s*\[(html|moodle|plain|markdown)\]", "", crudo.strip())

        ini, fin = crudo.find("{"), crudo.find("}")
        if ini < 0 or fin < 0:
            fallos.append(f"{nombre}: sin bloque de respuesta entre llaves")
            continue
        if crudo.count("{") - crudo.count("}") != 0:
            fallos.append(f"{nombre}: llaves desbalanceadas")
        cuerpo = crudo[ini + 1:fin].strip()
        cola = crudo[fin + 1:].strip()

        general = ""
        g = re.match(r"^([^}]*?)####(.*?)$", cuerpo, re.S)
        if g:
            cuerpo, general = g.group(1).strip(), g.group(2).strip()
        if not general:
            fallos.append(f"{nombre}: sin retroalimentación general (####)")

        # Tipo, por el mismo orden de comprobaciones que el importador.
        if cuerpo == "":
            tipo, detalle = "ensayo o descripción", "PROHIBIDA en este banco"
            fallos.append(f"{nombre}: bloque vacío, es un ensayo y el encargo lo excluye")
        elif re.match(r"^(TRUE|FALSE|T|F)\b", cuerpo, re.I):
            tipo = "verdadero/falso"
            trozos = re.split(r"(?<!\\)#", cuerpo)
            correcta = trozos[0].strip().upper()
            correcta = "verdadero" if correcta in ("T", "TRUE") else "falso"
            if len(trozos) < 3:
                fallos.append(f"{nombre}: V/F sin las dos retroalimentaciones")
            vf.append(correcta)
            detalle = f"correcta {correcta}, {len(trozos) - 1} retroalimentaciones"
        elif "->" in cuerpo:
            tipo = "emparejamiento"
            pares = [p for s, p in respuestas(cuerpo) if "->" in p]
            if len(pares) < 3:
                fallos.append(f"{nombre}: emparejamiento con menos de 3 pares")
            for s, p in respuestas(cuerpo):
                if s != "=":
                    fallos.append(f"{nombre}: par de emparejamiento con ~ en vez de =")
            detalle = f"{len(pares)} pares"
        elif cuerpo.startswith("#") and not cuerpo.startswith("####"):
            tipo, detalle = "numérica", "PROHIBIDA en este banco"
            fallos.append(f"{nombre}: pregunta numérica, se responde tecleando")
        else:
            rs = respuestas(cuerpo)
            if not rs:
                fallos.append(f"{nombre}: bloque de respuesta vacío")
                continue
            pesos = [re.match(r"^%(-?[\d.]+)%", t) for _, t in rs]
            if any(pesos):
                tipo = "respuesta múltiple"
                suma = sum(float(p.group(1)) for p in pesos if p)
                pos = sum(float(p.group(1)) for p in pesos if p and float(p.group(1)) > 0)
                if abs(pos - 100) > 0.05:
                    fallos.append(f"{nombre}: los pesos positivos suman {pos}, no 100")
                detalle = f"{sum(1 for p in pesos if p and float(p.group(1)) > 0)} correctas, suma {round(suma, 3)}"
            else:
                correctas = [t for s, t in rs if s == "="]
                if len(correctas) != 1:
                    fallos.append(f"{nombre}: {len(correctas)} respuestas con =, se esperaba 1")
                tipo = "opción múltiple"
                detalle = f"{len(rs)} opciones"
                if len(correctas) == 1:
                    posiciones.append([t for _, t in rs].index(correctas[0]))
                if not any(s == "~" for s, _ in rs):
                    tipo = "respuesta corta"
                    fallos.append(f"{nombre}: sin distractores, Moodle la importa "
                                  "como respuesta corta y se teclea")
                if cola:
                    tipo += " (palabra faltante)"

            # Toda opción incorrecta necesita su retroalimentación.
            for s, t in rs:
                incorrecta = s == "~" and not re.match(r"^%(?!-?0%)-?[1-9]", t)
                if incorrecta and "#" not in t:
                    fallos.append(f"{nombre}: distractor sin retroalimentación → {post(t)[:48]}")

        # Caracteres reservados sin escapar en el texto ya desescapado.
        visible = post(cuerpo) + post(general)
        for ch in ("::",):
            if ch in visible:
                fallos.append(f"{nombre}: «{ch}» sin escapar en el texto")

        resumen.append((nombre, tipo, detalle, "" if general else "sin ####"))

    if len(vf) > 1 and len(set(vf)) == 1:
        fallos.append(f"los {len(vf)} verdadero/falso se resuelven todos con "
                      f"«{vf[0]}»: se aciertan sin leer el enunciado")
    if len(posiciones) > 2 and len(set(posiciones)) == 1:
        fallos.append(f"la opción correcta está siempre en la posición "
                      f"{posiciones[0] + 1}: si el examen no baraja las "
                      "respuestas, se resuelve por posición")

    return resumen, fallos


RAIZ = pathlib.Path(__file__).resolve().parent.parent
rutas = ([pathlib.Path(a) for a in sys.argv[1:]]
         or sorted((RAIZ / "src/evaluacion").glob("*.gift")))
if not rutas:
    print("No hay bancos .gift en src/evaluacion")
    sys.exit(0)

total = 0
for ruta in rutas:
    resumen, fallos = revisar(ruta)
    preguntas = [r for r in resumen if r[0] != "categoría"]
    print(f"{ruta.name} · {len(preguntas)} preguntas\n")
    for nombre, tipo, detalle, aviso in resumen:
        print(f"  {nombre:52.52}  {tipo:28.28}  {detalle} {aviso}")
    tipos = sorted({t for n, t, _, _ in preguntas})
    print(f"\n  tipos distintos: {len(tipos)} → {', '.join(tipos)}")
    if fallos:
        print(f"\n  {len(fallos)} problema(s):")
        for f in fallos:
            print(f"   · {f}")
            total += len(fallos)
        continue
    print("\n  Sin problemas de formato.")

sys.exit(1 if total else 0)
