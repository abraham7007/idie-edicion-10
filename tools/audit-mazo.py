#!/usr/bin/env python3
# Reglas propias de este mazo, todas nacidas de un error encontrado en una
# revisión y documentado en METODOLOGIA.md §17. No sustituyen a los cuatro
# auditores derivados de skills —léxico, registro, editorial y cifras—, que
# vigilan lo que la norma académica exige en cualquier documento. Aquí solo
# está lo que se rompió en estas láminas y puede volver a romperse.
#
# Se corre sobre el HTML GENERADO y no sobre el guion de Python: lo que
# importa es lo que el aula lee. Un bloque declarado en el guion pero nunca
# montado en `LAMINAS` no existe, y ya pasó dos veces.
#
# Uso, desde src/slides:
#   python3 ../../tools/audit-mazo.py

from __future__ import annotations

import html
import pathlib
import re
import sys

# ── §17.17 · contraste sin información -------------------------------------
# El patrón «no es A sino B» y sus variantes. La marca NO es la forma
# negativa: es que la negación no añada nada. «Se sitúa cada actividad, no el
# proyecto entero» evita un error real de uso y se queda. Por eso esta lista
# recoge solo las construcciones cuya única función es el contraste retórico,
# y el veredicto final lo da quien escribe.
CONTRASTE = [
    (r"\bno\s+(?:es|son|se|basta|significa|mide|va|hay)\b[^.;]{0,90}?\bsino\b", "«no es A sino B»"),
    (r"\bno\s+s[oó]lo\b[^.;]{0,90}?\bsino\b", "«no solo A sino B»"),
    (r"\bno\s+como\b[^.;]{0,70}?\bsino\s+como\b", "«no como A sino como B»"),
    (r"\bno basta\b", "«no basta con»"),
    (r"\bno se trata de\b", "«no se trata de»"),
    (r"\blo que (?:decide|importa|cuenta) es\b", "«lo que decide es»"),
    (r"\bm[áa]s que\b[^.;]{0,60}?,\s*lo que\b", "«más que A, lo que»"),
    (r"\bno tanto\b[^.;]{0,80}?\bcomo\b", "«no tanto A como B»"),
    # Añadidos en la pasada de escritura de la sesión 2. Los tres primeros son
    # variantes del mismo giro; los dos últimos, cierres autoevaluativos.
    (r"\bes lo que\b", "«es lo que»"),
    (r"\bla clave (?:est[áa]|es)\b", "«la clave está en»"),
    (r"\bm[áa]s all[áa] de\b", "«más allá de»"),
    (r"\ben (?:resumen|conclusi[óo]n)\b", "cierre autoevaluativo"),
    (r"\besto (?:demuestra|evidencia) la importancia\b", "cierre autoevaluativo"),
]

# ── §9 · el mazo no se menciona a sí mismo ---------------------------------
# Lo explica el docente en voz alta. Escrito en la lámina sobra, y además
# envejece: «en la sesión 3» deja de ser cierto si el orden cambia.
AUTORREFERENCIA = [
    (r"\beste curso\b", "«este curso»"),
    (r"\bel estudiante\b", "«el estudiante»"),
    (r"\besta sesi[óo]n\b", "«esta sesión»"),
    (r"\ben la sesi[óo]n \d\b", "«en la sesión N»"),
    (r"\bqu[ée] te llevas\b", "«qué te llevas»"),
    (r"\bal terminar (?:sabr|podr|habr)", "«al terminar sabrás»"),
    (r"\bcomo vimos\b|\bcomo veremos\b", "«como vimos / veremos»"),
]

# ── §17.12 · el rótulo de un bloque no continúa dentro del párrafo ---------
# Los rótulos pasaron de ir en línea a ir encima, y diecinueve de veintidós
# textos se habían redactado como continuación suya: al subir el rótulo
# quedaron empezando en minúscula y en frase truncada.
ROTULOS_CON_CUERPO = (
    "conclusion", "warn-box", "keydata", "criterion", "avoid", "example",
    "practice", "def", "wk__sec--meta",
)

# ── §4.4 · tope de tablas por sesión ---------------------------------------
# El tope cuenta tablas de contenido, las que compiten por la atención del
# lector. La lámina de referencias queda fuera: su tabla es la bibliografía y
# nadie la lee en el aula, se consulta después.
MAX_TABLAS = 6
SIN_TOPE = ("referencias",)

# ── §3.2 · el icono referenciado tiene que existir en el juego -------------
# `<use href="#i-flag">` sin símbolo `i-flag` no rompe la página: el navegador
# no dibuja nada y el hueco pasa por diseño. Estuvo así en veinte láminas,
# porque ni el verificador de maqueta ni el ojo lo denuncian: la escuadra y el
# rótulo del bloque siguen ahí y solo falta el pictograma.
ICONOS = pathlib.Path(__file__).resolve().parent.parent / "public/course-icons.svg"


# ── §17.13 · longitud de entrada en las listas del taller ------------------
# Medido: a 615 px de columna enmarcada, una entrada de 81 caracteres se
# parte en dos líneas, y cada línea partida cuesta 24 px de alto.
MAX_CARACTERES_TALLER = 78

# ── §6.6 · el cuerpo de un bloque de recurso da la idea central ------------
# Tres líneas a su ancho de columna. Se mide en caracteres porque el ancho
# depende del reparto de la lámina: 240 es lo que caben en tres líneas en la
# columna estrecha, que es el caso más apretado.
MAX_CARACTERES_RECURSO = 240
BLOQUES_DE_RECURSO = ("keydata", "criterion", "avoid", "example", "practice")

# ── §6.5 · términos que en este curso significan otra cosa ----------------
# «figura» son las cuarenta y tantas figuras del mazo, así que usarla para la
# naturaleza jurídica del postulante confunde. Igual con «modelo» y «caso».
AMBIGUOS = (
    (r"\bla figura (?:decide|determina|define)\b", "«figura» sin precisar"),
    (r"^(?:El |La |Los |Las )?(?:figura|modelo|caso)s?\b(?!\s+(?:jur[íi]dica|de |lineal|del ))",
     "término ambiguo al abrir el título"),
)


def bloques_de(cuerpo: str, clase: str) -> list[str]:
    """Contenido de cada `<div class="clase">`, contando niveles.

    Con una expresión regular no se puede: `(.*?)</div>\\s*</div>` cierra en el
    primer par de cierres que encuentra y arrastra los bloques hermanos que
    vienen detrás, así que solo medía bien el último de cada columna. Un
    `en_la_practica` de 330 caracteres se contaba como 1 083.
    """
    salida = []
    for m in re.finditer(rf'<div class="{re.escape(clase)}"[^>]*>', cuerpo):
        i = m.end()
        nivel = 1
        for t in re.finditer(r"<div\b[^>]*>|</div>", cuerpo[i:]):
            nivel += 1 if t.group(0) != "</div>" else -1
            if nivel == 0:
                salida.append(cuerpo[i:i + t.start()])
                break
    return salida


def texto_de(nodo: str) -> str:
    """Texto que el aula lee, sin marcado.

    Los `<script>` se retiran antes: sus comentarios son prosa dirigida a quien
    edita el guion, y las reglas de registro no le aplican. Sin quitarlos, un
    comentario del simulador que dice «la cifra publicada, no una puntuación
    inventada» se contaba como contraste retórico de lámina.
    """
    limpio = re.sub(r"<script\b.*?</script>", " ", nodo, flags=re.S | re.I)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", limpio))).strip()


def revisar(carpeta: pathlib.Path) -> list[str]:
    fallos: list[str] = []
    disponibles = set(re.findall(r'<symbol id="([^"]+)"', ICONOS.read_text(encoding="utf-8")))
    reclamados: dict[str, set[str]] = {}

    # `rglob` y no `glob`: las láminas viven en src/slides/clase-NN/ y el
    # orquestador invoca esto desde src/slides. Con `glob` no encontraba ni un
    # fichero y el auditor informaba «sin observaciones» sobre cero láminas,
    # que es el mismo fallo silencioso que el verificador de maqueta tuvo con
    # el servidor apagado.
    ficheros = sorted(carpeta.rglob("*.html"))
    if not ficheros:
        fallos.append(f"no hay ninguna lámina bajo {carpeta}: nada que auditar")
    # El tope de tablas es POR SESIÓN, no por mazo: contándolas todas juntas, la
    # sesión 1 con seis y la sesión 2 con cuatro daban diez y saltaba la regla
    # con las dos dentro de norma.
    por_sesion: dict[str, int] = {}
    for f in ficheros:
        crudo = f.read_text(encoding="utf-8")
        # El <title> repite el título de la lámina y dispararía cada regla dos
        # veces; se recorta antes de medir.
        cuerpo = crudo.split("</head>", 1)[-1]
        plano = texto_de(cuerpo)
        nom = f.name

        for pat, rotulo in CONTRASTE + AUTORREFERENCIA:
            for m in re.finditer(pat, plano, re.I):
                cita = plano[max(0, m.start() - 40):m.end() + 25].strip()
                fallos.append(f"{nom}  {rotulo}  …{cita}…")

        # Rótulo arriba, texto debajo: el texto abre en mayúscula porque es una
        # oración completa. Se acepta que empiece por cifra, comilla o acrónimo.
        for clase in ROTULOS_CON_CUERPO:
            pat = (rf'class="[^"]*\b{re.escape(clase)}\b[^"]*"[^>]*>\s*'
                   rf'<(?:div|h3)[^>]*class="[^"]*__label[^"]*"[^>]*>.*?</(?:div|h3)>\s*<p[^>]*>(.{{0,40}})')
            for m in re.finditer(pat, cuerpo, re.S):
                primero = texto_de(m.group(1)).lstrip("«\"'¿¡ ")
                if primero and primero[0].isalpha() and primero[0].islower():
                    fallos.append(f"{nom}  cuerpo de .{clase} en minúscula  …{primero[:46]}…")

        for m in re.finditer(r'course-icons\.svg#([\w-]+)"', cuerpo):
            reclamados.setdefault(m.group(1), set()).add(nom)

        if not any(x in nom for x in SIN_TOPE):
            sesion = f.parent.name
            por_sesion[sesion] = por_sesion.get(sesion, 0) + len(re.findall(r"<table\b", cuerpo))

        # Iconos en línea con el texto: desplazan el párrafo entero y el bloque
        # deja de reconocerse. El pie de fuente es la excepción declarada.
        for m in re.finditer(r'<svg class="icon[^"]*"[^>]*>.*?</svg>\s*<(p|ul|ol)\b', cuerpo, re.S):
            contexto = cuerpo[max(0, m.start() - 220):m.start()]
            if "srcnote" not in contexto:
                fallos.append(f"{nom}  icono en línea con <{m.group(1)}>")

        for clase in BLOQUES_DE_RECURSO:
            for interior in bloques_de(cuerpo, clase):
                t = texto_de(interior)
                if len(t) > MAX_CARACTERES_RECURSO:
                    fallos.append(f"{nom}  .{clase} de {len(t)} caracteres, el tope es "
                                  f"{MAX_CARACTERES_RECURSO} (§6.6)  …{t[:44]}…")

        # El título vive en dos sitios que tienen que decir lo mismo: el h1 de
        # la lámina y el <title> del documento, que es lo que se lee en la
        # pestaña y en el índice del curso. Se escriben en dos llamadas
        # distintas —`cabecera()` y el segundo campo de `L()`— y al integrar
        # dos entregas se desincronizaron en dieciocho láminas sin que nada
        # fallara: el h1 llevaba el alcance y el año, y el <title> una versión
        # anterior más corta.
        h1 = re.search(r'<h1 class="slide__title[^>]*>(.*?)</h1>', cuerpo, re.S)
        doc = re.search(r"<title>(.*?)</title>", crudo, re.S)
        if h1 and doc:
            # Se normaliza el espacio antes de la puntuación: el h1 lleva
            # `<i>deep tech</i>, 2023` y al retirar la etiqueta queda un espacio
            # suelto delante de la coma que el <title>, sin marcado, no tiene.
            norm = lambda x: re.sub(r"\s+([,.;:])", r"\1", x).strip()
            a = norm(texto_de(h1.group(1)))
            b = norm(html.unescape(doc.group(1)).split(" · ")[-1])
            # La portada es la excepción: su <title> dice «Portada» a propósito.
            if a != b and b.lower() != "portada":
                fallos.append(f"{nom}  el <title> no coincide con el h1\n"
                              f"      h1      «{a[:64]}»\n"
                              f"      <title> «{b[:64]}»")

        titulo = re.search(r'<h1 class="slide__title[^>]*>(.*?)</h1>', cuerpo, re.S)
        if titulo:
            tt = texto_de(titulo.group(1))
            for pat, rotulo in AMBIGUOS:
                if re.search(pat, tt, re.I):
                    fallos.append(f"{nom}  {rotulo}  «{tt[:52]}»")

        if "wk__" in cuerpo:
            for m in re.finditer(r"<li[^>]*>(.*?)</li>", cuerpo, re.S):
                t = texto_de(m.group(1))
                if len(t) > MAX_CARACTERES_TALLER:
                    fallos.append(f"{nom}  entrada de taller de {len(t)} caracteres  …{t[:46]}…")

    for icono, donde in sorted(reclamados.items()):
        if icono not in disponibles:
            fallos.append(
                f"el icono «{icono}» no está en course-icons.svg y se usa en "
                f"{len(donde)} lámina(s), la primera {sorted(donde)[0]}")

    for sesion, n in sorted(por_sesion.items()):
        if n > MAX_TABLAS:
            fallos.append(f"{sesion} lleva {n} tablas y el máximo por sesión es {MAX_TABLAS} (§4.4)")

    return fallos


if __name__ == "__main__":
    raiz = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    problemas = revisar(raiz)
    if not problemas:
        print("audit-mazo · sin observaciones")
        sys.exit(0)
    print(f"audit-mazo · {len(problemas)} observación(es):")
    for p in problemas:
        print(f"  · {p}")
    sys.exit(1)
