#!/usr/bin/env python3
"""Genera las figuras cuantitativas del curso a public/figures/*.svg.

Por qué existe este archivo en lugar de dibujar cada figura a mano en SVG:

1. Las figuras salen de los MISMOS números que la diapositiva enseña en el
   texto. Los datos viven aquí arriba, en una constante con nombre. Si un
   dato cambia (el monto invertido por capital de riesgo en la región, la
   tasa de adjudicación de una convocatoria), se corrige en un sitio y la
   figura deja de contradecir al texto. En un curso cuyo contenido son
   cifras oficiales que se actualizan cada año, esto no es comodidad: es lo
   que permite pasar de una edición a la siguiente sin redibujar nada.
2. Una serie histórica de inversión o un reparto por instrumento tiene
   decenas de puntos. Escribirlos a mano no es viable y "dibujarlos a ojo"
   produce gráficos que mienten sobre la magnitud de lo que ilustran.

Los SVG resultantes NO llevan colores fijos: al final se sustituye cada tinta
por la variable CSS equivalente (--fig-ink, --fig-accent, ...), de modo que
deck.js los inserta en línea y el mismo archivo se dibuja correcto en tema
claro y en tema oscuro.

Uso:  python3 tools/figures/render.py
"""

from __future__ import annotations

import re
from pathlib import Path

import textwrap
import matplotlib
import matplotlib.ticker as mticker
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, PathPatch, Rectangle, Wedge
from matplotlib.path import Path as MplPath

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "public" / "figures"

# Tintas de trabajo. Son marcadores: cada una se reemplaza por su variable
# CSS al escribir el archivo. Se eligen valores muy separados entre sí para
# que la sustitución textual no pueda confundir dos tintas distintas.
# Tintas de trabajo, validadas con la skill dataviz antes de usarse:
#   node scripts/validate_palette.js "#c8102e,#2f6fba" --mode light  → 5/5
#   node scripts/validate_palette.js "#e8556b,#4e93d9" --mode dark   → 5/5
# El gris NO es una serie: es el fondo del que se destaca un elemento. Como
# serie categórica junto al azul falla el suelo de visión normal (ΔE 12,9),
# así que nunca se usan gris y azul como dos categorías en la misma figura.
INK = "#111111"
MUTED = "#7a8291"
GRID = "#cccccc"
SURFACE = "#f2f2f2"
PAPER = "#fdfdfd"
ACCENT = "#c8102e"
NAVY = "#2f6fba"
OK = "#1a7f4b"

# Rampa ordinal de un solo tono para categorías con orden natural (tramos de
# una escala, etapas de un embudo). Validada con:
#   node scripts/validate_palette.js "#7ba4d6,#3a72b8,#14396c" --ordinal
RAMPA = ["#7ba4d6", "#3a72b8", "#14396c"]
WARN = "#a86a00"

VARIABLE_POR_TINTA = {
    RAMPA[0]: "var(--fig-ramp-1)",
    RAMPA[1]: "var(--fig-ramp-2)",
    RAMPA[2]: "var(--fig-ramp-3)",
    INK: "var(--fig-ink)",
    MUTED: "var(--fig-muted)",
    GRID: "var(--fig-grid)",
    SURFACE: "var(--fig-surface)",
    PAPER: "var(--fig-paper)",
    ACCENT: "var(--fig-accent)",
    NAVY: "var(--fig-navy)",
    OK: "var(--fig-ok)",
    WARN: "var(--fig-warn)",
}

MONO = ["IBM Plex Mono", "DejaVu Sans Mono", "monospace"]

plt.rcParams.update(
    {
        "font.family": "monospace",
        "font.monospace": MONO,
        "font.size": 9,
        "axes.edgecolor": GRID,
        "axes.labelcolor": MUTED,
        "axes.titlecolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "svg.fonttype": "none",  # el texto viaja como texto, no como curvas
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
    }
)


def escribir(fig, nombre: str) -> None:
    """Guarda la figura como SVG con las tintas convertidas en variables CSS."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / f"{nombre}.svg"
    fig.savefig(destino, format="svg", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)

    svg = destino.read_text(encoding="utf-8")

    # matplotlib emite las tintas en minúscula y a veces en forma rgb().
    for tinta, variable in VARIABLE_POR_TINTA.items():
        svg = svg.replace(tinta, variable).replace(tinta.upper(), variable)

    # El <svg> sale con width/height en pt: se quitan para que el marco de la
    # diapositiva mande y la figura escale con el contenedor.
    svg = re.sub(r'\s(width|height)="[\d.]+pt"', "", svg, count=2)
    # El prólogo XML y el DOCTYPE solo son válidos en un documento SVG
    # independiente. Aquí el archivo se inserta DENTRO del HTML de la
    # diapositiva, donde ambos son marcado ilegal que el navegador arrastra
    # al DOM como texto suelto.
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!DOCTYPE.*?>", "", svg, flags=re.S)
    # Los metadatos de matplotlib (fecha de creación, versión) harían que cada
    # regeneración produjera un archivo distinto aunque la figura no cambie.
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<!-- Created with matplotlib.*?-->", "", svg, flags=re.S)
    # matplotlib nombra con un identificador aleatorio —una letra y diez
    # dígitos hexadecimales— tanto los clip-path como los trazos reutilizables
    # de las marcas de eje. Regenerar una figura idéntica producía un archivo
    # distinto, y el control de versiones marcaba las ciento cuarenta y cinco
    # como modificadas en cada pasada. Se renumeran por orden de aparición.
    for i, viejo_id in enumerate(dict.fromkeys(re.findall(r'\bid="([a-z][0-9a-f]{10})"', svg))):
        svg = svg.replace(viejo_id, f"{nombre}-{i}")

    destino.write_text(svg.strip(), encoding="utf-8")
    print(f"  {destino.relative_to(RAIZ)}")


def num(valor, decimales=2):
    """Cifra con coma decimal y espacio de millares.

    En español el separador decimal es la coma y el de millares un espacio
    (skill academic-register, criterio 4 de ortotipografía). matplotlib
    escribe punto, así que toda cifra rotulada en una figura pasa por aquí.
    """
    txt = f"{valor:,.{decimales}f}".replace(",", "\u2009").replace(".", ",")
    return txt.rstrip("0").rstrip(",") if "," in txt else txt


def limpiar_ejes(ax, *, ocultar=("top", "right")):
    for lado in ocultar:
        ax.spines[lado].set_visible(False)
    ax.tick_params(length=3, width=0.8)


# --------------------------------------------------------------------------
# A partir de aquí van las figuras del curso. Cada una:
#   1. Declara sus datos en una constante con nombre, ARRIBA de la función.
#      Son los MISMOS números que la lámina enuncia en el texto.
#   2. Dibuja con figsize ancho y bajo (≈6 × 2.4): la figura comparte la hoja
#      con una columna de texto y el alto es el recurso escaso.
#   3. Termina llamando a escribir(fig, "nombre-de-la-figura").
# --------------------------------------------------------------------------


# ==========================================================================
# SESIÓN 1 · Fundamentos y ecosistema I+D+i+e
# ==========================================================================
# Los datos de cada figura viven en la constante que la precede, con su
# fuente y su año escritos al lado. Son LOS MISMOS que la lámina enuncia en
# el texto: si el dato cambia, se corrige aquí y la figura no puede
# contradecir a la lámina. En un curso cuyas cifras se actualizan cada año,
# esta es la única forma de pasar de edición a edición sin redibujar.


# POLCTI (CONCYTEC, 2024), Tabla 13, con datos del Instituto de Estadística
# de la UNESCO vía Banco Mundial. Año del dato: 2018 (América Latina, 2017).
GASTO_ID_PBI = [
    ("Israel", 4.95),
    ("Corea del Sur", 4.81),
    ("Japón", 3.26),
    ("Estados Unidos", 2.84),
    ("Media OCDE", 2.58),
    ("Zona del euro", 2.21),
    ("China", 2.19),
    ("América Latina", 0.71),
    ("Perú", 0.13),
]


def fig_gasto_id_pbi():
    """La distancia real entre el Perú y quienes deciden qué se investiga."""
    nombres = [n for n, _ in GASTO_ID_PBI][::-1]
    valores = [v for _, v in GASTO_ID_PBI][::-1]
    colores = [ACCENT if n == "Perú" else (NAVY if n == "América Latina" else MUTED)
               for n in nombres]

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    barras = ax.barh(nombres, valores, color=colores, height=0.68)
    for b, v in zip(barras, valores):
        ax.text(v + 0.09, b.get_y() + b.get_height() / 2, num(v),
                va="center", ha="left", fontsize=8.5, color=INK)

    ax.set_xlabel("Gasto en I+D como porcentaje del PBI (%)", fontsize=8.5, color=MUTED)
    ax.set_xlim(0, 5.6)
    ax.tick_params(axis="y", labelsize=8.5, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: num(v, 0)))
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-gasto-id-pbi")


# POLCTI (CONCYTEC, 2024), pág. 51, misma fuente UNESCO. Año 2018.
ALIANZA_PACIFICO = [("México", 0.54), ("Chile", 0.35), ("Colombia", 0.24), ("Perú", 0.12)]


def fig_alianza_pacifico():
    """Dentro de la propia Alianza del Pacífico, el Perú es el último."""
    nombres = [n for n, _ in ALIANZA_PACIFICO][::-1]
    valores = [v for _, v in ALIANZA_PACIFICO][::-1]
    colores = [ACCENT if n == "Perú" else NAVY for n in nombres]

    fig, ax = plt.subplots(figsize=(6.6, 2.2))
    barras = ax.barh(nombres, valores, color=colores, height=0.6)
    for b, v in zip(barras, valores):
        ax.text(v + 0.012, b.get_y() + b.get_height() / 2, f"{num(v)} %",
                va="center", ha="left", fontsize=9, color=INK)
    ax.set_xlim(0, 0.66)
    ax.set_xlabel("Gasto en I+D sobre el PBI (%), 2018", fontsize=8.5, color=MUTED)
    ax.tick_params(axis="y", labelsize=9.5, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-alianza-pacifico")


# Global Innovation Index 2025 (OMPI). 139 economías evaluadas.
# Posiciones leídas del propio informe, no de resúmenes de prensa.
GII_2025_LATAM = [
    ("Chile", 51), ("Brasil", 52), ("México", 58), ("Uruguay", 68),
    ("Colombia", 71), ("Costa Rica", 72), ("Argentina", 77),
    ("Perú", 80), ("Panamá", 82),
]
GII_2025_TOTAL = 139


def fig_gii_latam():
    """Posición de nueve economías latinoamericanas entre las 139 del índice."""
    # Barras HORIZONTALES y no verticales. Con nueve países en vertical pasaban
    # dos cosas a la vez: «Colombia», «Costa Rica» y «Argentina» se solapaban
    # sobre el eje, y la cifra puesta sobre el extremo de la barra caía dentro
    # de ella porque el eje está invertido y la barra cuelga desde el cero.
    # En horizontal el nombre se lee alineado a la izquierda y la cifra va al
    # final de la barra, sobre el fondo: ninguna de las dos colisiones cabe.
    nombres = [n for n, _ in GII_2025_LATAM]
    puestos = [p for _, p in GII_2025_LATAM]

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ys = list(range(len(nombres) - 1, -1, -1))
    for y, nom, p in zip(ys, nombres, puestos):
        color = ACCENT if nom == "Perú" else MUTED
        ax.barh(y, p, color=color, height=0.62)
        ax.text(p + 1.6, y, str(p), ha="left", va="center", fontsize=8.6,
                color=INK, fontweight="bold" if nom == "Perú" else "normal")

    ax.set_yticks(ys)
    ax.set_yticklabels(nombres, fontsize=8.6)
    ax.set_xlabel(f"Puesto entre {GII_2025_TOTAL} economías · más a la derecha, "
                  "más abajo en el índice", fontsize=8.0, color=MUTED)
    ax.set_xlim(0, 95)
    ax.set_ylim(-0.7, len(nombres) - 0.3)
    ax.tick_params(axis="y", labelsize=8.6, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8.0, colors=MUTED, length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-gii-latam")


# Hitos normativos del sistema peruano de CTI. Cada uno verificable en la
# norma citada; la POLCTI 2024 los recoge en su base normativa.
HITOS_CTI_PERU = [
    (1968, "CONCYTEC", "Se crea el primer organismo rector"),
    (2004, "Ley 28303", "Ley marco de CTI: nace el sistema"),
    (2015, "Ley 30309", "Beneficio tributario a la I+D+i"),
    (2021, "SUNEDU", "Licenciamiento: la investigación pasa a ser requisito"),
    (2024, "Ley 31250", "SINACTI reemplaza al SINACYT"),
    (2025, "POLCTI 2030", "Meta: 1 % del PBI en I+D"),
]


def fig_hitos_cti():
    """Medio siglo de institucionalidad, y la mitad de los hitos en la última década.

    Los hitos se reparten a intervalos IGUALES y no según el año real. Con el
    eje a escala temporal, 1968 quedaba solo a la izquierda y los cinco hitos
    de 2004 a 2025 se agolpaban a la derecha hasta solaparse los rótulos: la
    figura dejaba de leerse justo en el tramo que importa. Lo que esta figura
    enseña es la SECUENCIA y su densidad reciente, no la distancia exacta
    entre fechas; el año va escrito en cada hito para que no se pierda.
    """
    fig, ax = plt.subplots(figsize=(7.4, 2.1))
    n = len(HITOS_CTI_PERU)
    xs = list(range(n))
    ax.hlines(0, -0.55, n - 0.45, color=GRID, linewidth=1.4)

    for x, (anio, titulo, _) in zip(xs, HITOS_CTI_PERU):
        arriba = x % 2 == 0
        y = 0.40 if arriba else -0.40
        color = ACCENT if anio >= 2024 else NAVY
        ax.vlines(x, 0, y, color=color, linewidth=1.3)
        ax.plot(x, 0, "o", color=color, markersize=6)
        ax.text(x, y + (0.11 if arriba else -0.11), titulo, ha="center",
                va="bottom" if arriba else "top", fontsize=8.5, color=INK)
        ax.text(x, y + (0.30 if arriba else -0.30), str(anio), ha="center",
                va="bottom" if arriba else "top", fontsize=8, color=MUTED)

    ax.set_ylim(-0.95, 0.95)
    ax.set_xlim(-0.75, n - 0.25)
    ax.axis("off")
    escribir(fig, "s1-hitos-cti-peru")


FIGURAS = [fig_gasto_id_pbi, fig_alianza_pacifico, fig_gii_latam, fig_hitos_cti]


# POLCTI (CONCYTEC, 2024), Tabla 16, con datos de la OMPI y el Banco Mundial.
# Registro anual de patentes por millón de habitantes, promedio 2010-2018.
COEFICIENTE_INVENCION = [
    ("Estados Unidos", 848.3), ("Canadá", 118.5), ("España", 60.5),
    ("Brasil", 23.1), ("Chile", 20.5), ("Argentina", 13.4), ("México", 10.0),
    ("Uruguay", 7.2), ("Colombia", 6.5), ("Perú", 2.1), ("Ecuador", 1.1),
]


def fig_coeficiente_invencion():
    """Dos patentes por millón: una décima parte de Chile, y muy lejos del resto."""
    nombres = [n for n, _ in COEFICIENTE_INVENCION][::-1]
    valores = [v for _, v in COEFICIENTE_INVENCION][::-1]
    colores = [ACCENT if n == "Perú" else MUTED for n in nombres]

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    barras = ax.barh(nombres, valores, color=colores, height=0.66)
    for b, v in zip(barras, valores):
        ax.text(v * 1.15, b.get_y() + b.get_height() / 2, num(v, 1),
                va="center", ha="left", fontsize=8, color=INK)
    # Escala logarítmica: entre 1,1 y 848 hay tres órdenes de magnitud, y en
    # escala lineal los once países de la región se aplastan en una sola raya.
    ax.set_xscale("log")
    ax.set_xlim(0.7, 2600)
    ax.set_xlabel("Patentes registradas por millón de habitantes (escala logarítmica)",
                  fontsize=8, color=MUTED)
    ax.tick_params(axis="y", labelsize=8.5, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=7.5, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-coeficiente-invencion")


# POLCTI (CONCYTEC, 2024), Gráfico 45, con datos de SCImago. Año 2020.
SCOPUS_100K = [
    ("Canadá", 346.5), ("Chile", 106.7), ("Uruguay", 63.7), ("Brasil", 47.0),
    ("Argentina", 39.7), ("Colombia", 33.1), ("México", 25.7), ("Perú", 18.5),
]


def fig_scopus_100k():
    """El Perú publica una sexta parte de lo que publica Chile por habitante."""
    nombres = [n for n, _ in SCOPUS_100K]
    valores = [v for _, v in SCOPUS_100K]
    colores = [ACCENT if n == "Perú" else (NAVY if n == "Chile" else MUTED) for n in nombres]

    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    barras = ax.bar(nombres, valores, color=colores, width=0.62)
    for b, v in zip(barras, valores):
        ax.text(b.get_x() + b.get_width() / 2, v + 9, num(v, 1),
                ha="center", va="bottom", fontsize=8.5, color=INK)
    ax.set_ylabel("Publicaciones por 100 000 habitantes", fontsize=8.5, color=MUTED)
    ax.set_ylim(0, 400)
    ax.tick_params(axis="x", labelsize=8.5, colors=INK, length=0)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s1-scopus-100k")


# POLCTI (CONCYTEC, 2024), Tabla 12, con datos del RENACYT. Año 2023.
# El nivel VII es el de entrada; el I, el más alto.
RENACYT_NIVELES = [
    ("Distinguido", 23, 109), ("Nivel I", 11, 63), ("Nivel II", 64, 187),
    ("Nivel III", 93, 266), ("Nivel IV", 126, 369), ("Nivel V", 276, 609),
    ("Nivel VI", 421, 809), ("Nivel VII", 786, 1522),
]
RENACYT_TOTAL = 5734


def fig_renacyt_piramide():
    """La pirámide del RENACYT: cuatro de cada diez investigadores están en el nivel de entrada."""
    nombres = [n for n, _, _ in RENACYT_NIVELES]
    mujeres = [m for _, m, _ in RENACYT_NIVELES]
    hombres = [h for _, _, h in RENACYT_NIVELES]

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.barh(nombres, mujeres, color=ACCENT, height=0.66, label="Mujeres")
    ax.barh(nombres, hombres, left=mujeres, color=NAVY, height=0.66, label="Hombres")
    for i, (m, h) in enumerate(zip(mujeres, hombres)):
        ax.text(m + h + 40, i, num(m + h, 0),
                va="center", ha="left", fontsize=8, color=INK)

    ax.set_xlabel("Investigadores registrados", fontsize=8.5, color=MUTED)
    ax.set_xlim(0, 2700)
    ax.tick_params(axis="y", labelsize=8.5, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    ax.legend(loc="lower right", fontsize=8, frameon=False, labelcolor=INK)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-renacyt-piramide")


# POLCTI (CONCYTEC, 2024), Tabla 10, con datos del CONCYTEC.
# Proyectos acogidos al beneficio tributario de la Ley 30309.
LEY_30309 = [
    (2016, 72, 8), (2017, 68, 22), (2018, 43, 19), (2019, 48, 26),
    (2020, 35, 16), (2021, 33, 17), (2022, 53, 28),
]


def fig_ley_30309():
    """Menos de cuatro de cada diez proyectos presentados obtienen el beneficio."""
    anios = [a for a, _, _ in LEY_30309]
    pres = [p for _, p, _ in LEY_30309]
    apro = [x for _, _, x in LEY_30309]
    x = range(len(anios))

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.bar([i - 0.19 for i in x], pres, width=0.36, color=MUTED, label="Presentados")
    ax.bar([i + 0.19 for i in x], apro, width=0.36, color=ACCENT, label="Aprobados")
    for i, (p, a) in enumerate(zip(pres, apro)):
        ax.text(i + 0.19, a + 1.6, f"{a * 100 // p} %", ha="center", va="bottom",
                fontsize=7.5, color=ACCENT)

    ax.set_xticks(list(x))
    ax.set_xticklabels(anios)
    ax.set_ylabel("Proyectos", fontsize=8.5, color=MUTED)
    ax.set_ylim(0, 88)
    ax.tick_params(axis="x", labelsize=8.5, colors=INK, length=0)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=8, frameon=False, labelcolor=INK, ncol=2)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s1-ley-30309")


# La escala TRL con los dos cortes que deciden el instrumento. No hay dato
# externo: es la representación de la propia escala, y por eso vive aquí en
# vez de dibujarse a mano en cada lámina que la necesite.
TRL_TRAMOS = [
    ("Investigación", 1, 3, "Laboratorio"),
    ("Desarrollo", 4, 6, "Entorno relevante"),
    ("Despliegue", 7, 9, "Entorno real"),
]


def fig_trl_escalera():
    """Los nueve niveles, sus dos cortes y la escala comercial que corre en paralelo."""
    # Barras horizontales de un nivel por fila: la escalera anterior no
    # dejaba ver qué ocurre en cada peldaño, solo dónde estaban los cortes.
    # Aquí cada nivel tiene su fila, su descripción y su entorno de prueba.
    NIVELES = [
        (9, "Sistema probado en operación real", "Despliegue"),
        (8, "Sistema completo y calificado", "Despliegue"),
        (7, "Prototipo demostrado en entorno real", "Despliegue"),
        (6, "Prototipo demostrado en entorno relevante", "Desarrollo"),
        (5, "Componentes validados en entorno relevante", "Desarrollo"),
        (4, "Componentes validados en laboratorio", "Desarrollo"),
        (3, "Prueba de concepto experimental", "Investigación"),
        (2, "Concepto tecnológico formulado", "Investigación"),
        (1, "Principios básicos observados", "Investigación"),
    ]
    COLOR = dict(zip(("Investigación", "Desarrollo", "Despliegue"), RAMPA))

    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    for k, (n, desc, tramo) in enumerate(NIVELES):
        y = k
        ax.barh(y, n, height=0.68, color=COLOR[tramo])
        ax.text(-0.18, y, f"TRL {n}", ha="right", va="center", fontsize=8.6,
                color=INK, fontweight="bold")
        # La descripción va FUERA de la barra: dentro se recortaba en los
        # niveles bajos, que son justamente los más cortos.
        ax.text(n + 0.22, y, desc, ha="left", va="center", fontsize=8.0, color=INK)

    # Los dos cortes reales de la escala. El rótulo va al margen izquierdo,
    # donde no se cruza con las barras ni con las descripciones.
    for corte, rot in ((2.5, "corte 6 · 7"), (5.5, "corte 3 · 4")):
        ax.axhline(corte, color=INK, linewidth=1.0, linestyle=(0, (4, 3)))
        ax.text(15.3, corte, rot, fontsize=7.6, color=INK, va="center", ha="right",
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.6))

    ax.set_xlim(-2.2, 15.5)
    ax.set_ylim(-0.9, len(NIVELES) - 0.2)
    ax.set_xticks([]); ax.set_yticks([])
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)
    for tramo, color in COLOR.items():
        ax.bar(0, 0, color=color, label=tramo)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=3, fontsize=8.2,
              frameon=False, labelcolor=INK, handletextpad=0.4, columnspacing=1.6)
    escribir(fig, "s1-trl-escalera")


# La madurez técnica no es la única escala. Las convocatorias de validación y
# escalamiento piden además madurez comercial, y un proyecto puede estar alto
# en una y bajo en la otra: ese desajuste es lo que la figura enseña.
MADUREZ_DOBLE = [
    ("CRL 1-3", "Hipótesis de mercado sin contrastar", "TRL 1-3"),
    ("CRL 4-6", "Propuesta de valor validada con usuarios", "TRL 4-6"),
    ("CRL 7-9", "Ventas repetidas y modelo de negocio probado", "TRL 7-9"),
]


def fig_madurez_doble():
    """Un proyecto puede estar en TRL 7 y en CRL 2: técnicamente listo y comercialmente crudo."""
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    for k, (crl, desc, trl) in enumerate(MADUREZ_DOBLE):
        y = len(MADUREZ_DOBLE) - k - 1
        ax.barh(y + 0.19, 1, height=0.34, color=NAVY, left=0)
        ax.barh(y - 0.19, 1, height=0.34, color=OK, left=1.25)
        ax.text(0.5, y + 0.19, trl, ha="center", va="center", fontsize=8.4, color=PAPER)
        ax.text(1.75, y - 0.19, crl, ha="center", va="center", fontsize=8.4, color=PAPER)
        ax.text(2.42, y, desc, ha="left", va="center", fontsize=8.2, color=INK)

    ax.text(0.5, len(MADUREZ_DOBLE) - 0.42, "Madurez técnica", ha="center",
            va="bottom", fontsize=8.4, color=NAVY, fontweight="bold")
    ax.text(1.75, len(MADUREZ_DOBLE) - 0.42, "Madurez comercial", ha="center",
            va="bottom", fontsize=8.4, color=OK, fontweight="bold")
    ax.set_xlim(-0.1, 6.4)
    ax.set_ylim(-0.7, len(MADUREZ_DOBLE) - 0.05)
    ax.set_xticks([]); ax.set_yticks([])
    ax.axis("off")
    escribir(fig, "s1-madurez-doble")



# ==========================================================================
# SESIÓN 1 · cuarta tanda — las láminas que estaban en texto seguido
# ==========================================================================


# Oslo 2018 exige DOS condiciones a la vez, y el orden en que se comprueban
# decide en qué casilla cae el proyecto. No hay dato externo que citar: es la
# definición de la norma llevada a diagrama, y por eso vive aquí en vez de
# repetirse en prosa en cada lámina que la necesite.
UMBRAL_OSLO = [
    ("¿Difiere de forma\nsignificativa de\nlo anterior?", "Mejora rutinaria",
     "Ajuste menor sobre\nlo que ya existía"),
    ("¿Está en uso por\nalguien, dentro\no fuera?", "Desarrollo\nexperimental",
     "Resultado nuevo\nque no usa nadie"),
]


def fig_umbral_innovacion():
    """Las dos condiciones de Oslo, en el orden en que se comprueban."""
    fig, ax = plt.subplots(figsize=(8.0, 2.35))
    ANCHO, ALTO, PASO = 2.20, 0.66, 2.68
    xs = [0.10 + i * PASO for i in range(4)]
    Y, Y_NO = 0.52, -0.82

    def caja(x, y, texto, color, fs=7.2, negrita=False, relleno=0.13):
        ax.add_patch(Rectangle((x, y - ALTO / 2), ANCHO, ALTO, facecolor=color,
                               alpha=relleno, edgecolor=color, linewidth=1.2))
        ax.text(x + ANCHO / 2, y, texto, ha="center", va="center", fontsize=fs,
                color=color if negrita else INK,
                fontweight="bold" if negrita else "normal")

    def flecha(p0, p1, color):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=10,
                                     color=color, linewidth=1.2, shrinkA=0, shrinkB=0))

    caja(xs[0], Y, "Producto o proceso\nmodificado", MUTED)
    caja(xs[1], Y, UMBRAL_OSLO[0][0], NAVY)
    caja(xs[2], Y, UMBRAL_OSLO[1][0], NAVY)
    caja(xs[3], Y, "Innovación", ACCENT, fs=11, negrita=True, relleno=0.18)

    for i in range(3):
        x0, x1 = xs[i] + ANCHO, xs[i + 1]
        flecha((x0, Y), (x1, Y), MUTED if i == 0 else NAVY)
        if i:
            ax.text((x0 + x1) / 2, Y + 0.14, "sí", ha="center", va="bottom",
                    fontsize=7.2, color=NAVY)

    # Las dos salidas que NO son innovación. Van debajo de la compuerta que
    # las produce: lo que la prosa no dice en el mismo espacio es que fallar
    # la segunda condición no devuelve al principio, deja en otra categoría.
    for k, (_, salida, detalle) in enumerate(UMBRAL_OSLO):
        cx = xs[k + 1] + ANCHO / 2
        color = MUTED if k == 0 else WARN
        flecha((cx, Y - ALTO / 2), (cx, Y_NO + ALTO / 2), color)
        ax.text(cx + 0.10, (Y + Y_NO) / 2, "no", ha="left", va="center",
                fontsize=7.2, color=color)
        caja(xs[k + 1], Y_NO, salida, color, fs=8.0, negrita=True)
        ax.text(cx, Y_NO - ALTO / 2 - 0.11, detalle, ha="center", va="top",
                fontsize=6.8, color=MUTED)

    ax.set_xlim(-0.05, xs[3] + ANCHO + 0.12)
    ax.set_ylim(-1.70, 1.05)
    ax.axis("off")
    escribir(fig, "s1-umbral-innovacion")


# Correspondencia entre el tipo de innovación declarado y la evidencia que el
# evaluador pide para acreditarlo. Las filas van de «medir lo que ya ocurre» a
# «prever el fallo» y las columnas por riesgo creciente: así la figura enseña
# el desplazamiento, que es lo que ninguna columna dice por separado.
TIPOS_INNOVACION_RIESGO = [
    ("Incremental", RAMPA[0]), ("De proceso", RAMPA[0]),
    ("Arquitectural", RAMPA[1]), ("Radical", ACCENT),
]
EVIDENCIA_POR_TIPO = [
    ("Medición del estado actual del proceso", (0, 1)),
    ("Magnitud de la mejora y cómo se mide", (0,)),
    ("Compromiso de quien adoptará el cambio", (1,)),
    ("Prueba de que no está ya publicado", (2,)),
    ("Ensayo o prueba de concepto ya realizada", (2, 3)),
    ("Plan de qué hacer si el principio falla", (3,)),
]


def fig_evidencia_por_tipo():
    """La evidencia se desplaza de medir el presente a prever el fallo."""
    fig, ax = plt.subplots(figsize=(8.6, 2.1))
    PASO = 1.45
    xs = [i * PASO for i in range(len(TIPOS_INNOVACION_RIESGO))]
    n = len(EVIDENCIA_POR_TIPO)

    for k, (rotulo, columnas) in enumerate(EVIDENCIA_POR_TIPO):
        y = n - 1 - k
        ax.hlines(y, -0.60, xs[-1] + 0.60, color=GRID, linewidth=0.6, alpha=0.7)
        ax.text(-0.90, y, rotulo, ha="right", va="center", fontsize=7.2, color=INK)
        for j, x in enumerate(xs):
            if j in columnas:
                ax.scatter([x], [y], s=125, color=TIPOS_INNOVACION_RIESGO[j][1], zorder=3)
            else:
                ax.scatter([x], [y], s=13, color=GRID, zorder=2)

    for (nombre, color), x in zip(TIPOS_INNOVACION_RIESGO, xs):
        ax.text(x, n - 0.58, nombre, ha="center", va="bottom", fontsize=7.0,
                color=color, fontweight="bold")

    # La flecha de riesgo es lo que ordena la lectura: sin ella las cuatro
    # columnas se leen como casos sueltos y no como una escala.
    ax.add_patch(FancyArrowPatch((xs[0] - 0.35, n + 0.32), (xs[-1] + 0.35, n + 0.32),
                                 arrowstyle="-|>", mutation_scale=9, color=MUTED,
                                 linewidth=1.0, shrinkA=0, shrinkB=0))
    ax.text((xs[0] + xs[-1]) / 2, n + 0.46, "riesgo declarado creciente",
            ha="center", va="bottom", fontsize=7.0, color=MUTED)

    ax.set_xlim(-4.60, xs[-1] + 0.70)
    ax.set_ylim(-0.65, n + 0.95)
    ax.axis("off")
    escribir(fig, "s1-evidencia-por-tipo")


# La escala TRL recorre un solo eje del plano en el que se decide la adopción.
# El segundo eje es la disposición de la organización a cambiar su forma de
# trabajar, que es la dimensión que la revisión de 2024 del uso del TRL fuera
# de la ingeniería señala como ausente de la escala.
CUADRANTES_ADOPCION = [
    (0.25, 0.75, "Demanda sin solución",
     "La organización quiere cambiar\ny no hay tecnología que lo permita", NAVY, 0.08),
    (0.75, 0.75, "Adopción efectiva",
     "El sistema funciona y la organización\ncambia con él", OK, 0.10),
    (0.25, 0.25, "Idea sin destinatario",
     "Ni la tecnología está madura\nni hay quien la reclame", MUTED, 0.08),
    (0.75, 0.25, "TRL alto sin adopción",
     "El sistema funciona y nadie cambia\nsu forma de trabajar", ACCENT, 0.18),
]


def fig_trl_adopcion():
    """TRL 9 acredita el eje horizontal y no dice nada del vertical."""
    fig, ax = plt.subplots(figsize=(6.8, 2.9))
    for x, y, titulo, sub, color, alfa in CUADRANTES_ADOPCION:
        ax.add_patch(Rectangle((x - 0.25, y - 0.25), 0.5, 0.5, facecolor=color,
                               alpha=alfa, edgecolor=PAPER, linewidth=3))
        ax.text(x, y + 0.10, titulo, ha="center", va="center", fontsize=9.4,
                color=color, fontweight="bold")
        ax.text(x, y - 0.10, sub, ha="center", va="center", fontsize=7.2, color=MUTED)

    # El punto que la lámina discute: madurez técnica máxima, adopción nula.
    # Va al canto inferior del cuadrante, donde no pisa su propia leyenda.
    ax.scatter([0.955], [0.045], s=70, color=ACCENT, zorder=4)
    ax.text(0.925, 0.045, "TRL 9", ha="right", va="center", fontsize=8.2,
            color=ACCENT, fontweight="bold")

    ax.hlines(0, 0, 1, color=GRID, linewidth=1.0)
    ax.vlines(0, 0, 1, color=GRID, linewidth=1.0)
    ax.text(0.5, -0.045, "Madurez técnica de la solución  →", ha="center",
            va="top", fontsize=8.2, color=INK)
    ax.text(-0.040, 0.5, "Disposición a adoptar  →", ha="center", va="center",
            fontsize=8.2, color=INK, rotation=90)

    # La banda inferior es el hallazgo: la escala mide una anchura, no un área.
    ax.add_patch(FancyArrowPatch((0, -0.185), (1, -0.185), arrowstyle="-|>",
                                 mutation_scale=11, color=ACCENT, linewidth=2.0,
                                 shrinkA=0, shrinkB=0))
    ax.text(0.5, -0.245, "alcance de la escala TRL · niveles 1 a 9", ha="center",
            va="top", fontsize=7.6, color=ACCENT)

    ax.set_xlim(-0.095, 1.03)
    ax.set_ylim(-0.35, 1.04)
    ax.axis("off")
    escribir(fig, "s1-trl-adopcion")


# Los dos modelos con los que se explica de dónde sale una innovación. No hay
# cifra que citar: la diferencia está en la arquitectura, y lo que la figura
# hace visible es dónde entra la investigación en cada uno de los dos.
CADENA_LINEAL = ["Investigación\nbásica", "Investigación\naplicada", "Desarrollo",
                 "Producción", "Mercado"]
CADENA_ESLABON = ["Mercado\npotencial", "Diseño", "Desarrollo\ny prueba",
                  "Producción", "Distribución"]


def fig_modelos_flujo():
    """El lineal pone la investigación al principio; el otro, al alcance de cada paso."""
    fig, ax = plt.subplots(figsize=(7.8, 3.2))
    ANCHO, ALTO, PASO = 1.62, 0.60, 2.15
    xs = [0.10 + i * PASO for i in range(5)]
    Y_LIN, Y_ESL, Y_CON = 2.60, 1.20, -0.05

    def caja(x, y, texto, color, ancho=ANCHO, alto=ALTO, fs=6.9, relleno=0.13):
        ax.add_patch(Rectangle((x, y - alto / 2), ancho, alto, facecolor=color,
                               alpha=relleno, edgecolor=color, linewidth=1.2))
        ax.text(x + ancho / 2, y, texto, ha="center", va="center", fontsize=fs, color=INK)

    def flecha(p0, p1, color, estilo="-|>", escala=10):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=estilo, mutation_scale=escala,
                                     color=color, linewidth=1.2, shrinkA=0, shrinkB=0))

    for x, texto in zip(xs, CADENA_LINEAL):
        caja(x, Y_LIN, texto, MUTED)
    for i in range(4):
        flecha((xs[i] + ANCHO, Y_LIN), (xs[i + 1], Y_LIN), MUTED)

    for x, texto in zip(xs, CADENA_ESLABON):
        caja(x, Y_ESL, texto, NAVY)
    # La doble punta es la única diferencia de trazo entre las dos cadenas, y
    # es exactamente la diferencia de fondo entre los dos modelos.
    for i in range(4):
        flecha((xs[i] + ANCHO, Y_ESL), (xs[i + 1], Y_ESL), ACCENT,
               estilo="<|-|>", escala=8)

    flecha((xs[4] + ANCHO / 2, Y_ESL + 0.65), (xs[1] + ANCHO / 2, Y_ESL + 0.65), ACCENT)
    ax.text((xs[1] + xs[4]) / 2 + ANCHO / 2, Y_ESL + 0.78,
            "lo que se aprende en el mercado vuelve al diseño", ha="center",
            va="bottom", fontsize=7.0, color=ACCENT)

    caja(xs[0], Y_CON, "Conocimiento disponible  ·  investigación", ACCENT,
         ancho=xs[4] + ANCHO - xs[0], alto=0.52, fs=8.0, relleno=0.10)
    for x in xs:
        ax.vlines(x + ANCHO / 2, Y_CON + 0.26, Y_ESL - ALTO / 2, color=ACCENT,
                  linewidth=0.9, linestyle=(0, (3, 3)))

    ax.text(-0.18, Y_LIN, "Modelo lineal", ha="right", va="center", fontsize=8.0,
            color=MUTED, fontweight="bold")
    ax.text(-0.18, Y_ESL, "Modelo de eslabón\nen cadena", ha="right", va="center",
            fontsize=8.0, color=NAVY, fontweight="bold")

    ax.set_xlim(-2.45, xs[4] + ANCHO + 0.12)
    ax.set_ylim(-0.55, 3.05)
    ax.axis("off")
    escribir(fig, "s1-modelos-flujo")



# Ranking SCImago de instituciones, edición iberoamericana 2023. Un puesto es
# una magnitud ordenada, y en tabla las dos columnas de cifras obligan a
# comparar mentalmente números de cuatro dígitos. En un eje se ve de una vez.
# El eje es el puesto mundial: el latinoamericano va como rótulo porque son
# dos escalas distintas —61 frente a 4 558— y un gráfico de dos ejes no se
# lee (skill dataviz, anti-patrón número uno).
UNIVERSIDADES_SIR = [
    ("Cayetano Heredia", 61, 4558),
    ("PUCP", 72, 4813),
    ("Nacional de Trujillo", 101, 5396),
    ("San Marcos", 128, 5782),
    ("Agraria La Molina", 167, 6230),
    ("Nacional de Ingeniería", 347, 7694),
]


def fig_universidades_sir():
    """Ninguna universidad peruana entra entre las cuatro mil primeras del mundo."""
    fig, ax = plt.subplots(figsize=(7.4, 2.9))
    ys = list(range(len(UNIVERSIDADES_SIR) - 1, -1, -1))

    for y, (nombre, latam, mundo) in zip(ys, UNIVERSIDADES_SIR):
        ax.hlines(y, 4000, mundo, color=NAVY, linewidth=1.6, alpha=0.45)
        ax.plot([mundo], [y], "o", color=NAVY, markersize=8, zorder=3)
        ax.text(mundo + 90, y, num(mundo, 0), ha="left", va="center",
                fontsize=8.0, color=INK, fontweight="bold")
        ax.text(3940, y, f"{nombre}   ", ha="right", va="center", fontsize=8.4,
                color=INK)
        # El puesto regional acompaña al nombre, no al eje.
        ax.text(3940, y - 0.30, f"puesto {latam} en América Latina   ", ha="right",
                va="center", fontsize=6.8, color=MUTED)

    # La marca de las cuatro mil primeras, que es lo que enuncia el título.
    ax.axvline(4000, color=ACCENT, linewidth=1.4, linestyle=(0, (4, 3)))
    ax.text(4060, len(ys) - 0.42, "4 000 primeras del mundo", fontsize=7.2,
            color=ACCENT, ha="left", va="center")

    ax.set_xlim(1500, 8900)
    ax.set_ylim(-0.75, len(ys) - 0.15)
    ax.set_xticks([4000, 5000, 6000, 7000, 8000])
    ax.set_xticklabels([num(v, 0) for v in (4000, 5000, 6000, 7000, 8000)])
    ax.set_xlabel("Puesto mundial · más a la derecha, más abajo en el ranking",
                  fontsize=7.6, color=MUTED)
    ax.set_yticks([])
    ax.tick_params(axis="x", labelsize=8.0, colors=INK, length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-universidades-sir")


# Los tres modelos de hélice son conjuntos anidados: cada uno contiene al
# anterior y añade un actor. En tabla ese anidamiento desaparece y quedan tres
# filas independientes, que es exactamente lo contrario de lo que el modelo
# dice. Se dibuja como contención.
HELICES = [
    ("Triple hélice", "Universidad · Empresa · Estado",
     "La innovación surge de la interacción entre los tres", ACCENT),
    ("Cuádruple hélice", "+ sociedad civil y medios",
     "Entra el usuario y la demanda social", NAVY),
    ("Quíntuple hélice", "+ entorno natural",
     "La innovación queda sujeta a los límites ambientales", OK),
]


def fig_helices():
    """Los actores que añade cada modelo de hélice sobre el anterior."""
    # La descripción de cada capa va DENTRO de su banda, no en una columna
    # aparte. En la primera versión los rectángulos ocupaban el tercio
    # izquierdo del marco y tres frases cortas se estiraban por los otros dos:
    # el dibujo quedaba diminuto y para saber a qué capa correspondía cada
    # frase había que seguir su punto de color de un lado al otro.
    #
    # Las bandas crecen hacia abajo y hacia la derecha, así que cada una deja
    # libre su franja superior: ahí caben su nombre, sus actores y lo que
    # incorpora, alineados a la izquierda y sin cruzar ninguna línea.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))

    CAPAS = [
        ("Quíntuple hélice", "+ entorno natural",
         "La innovación queda sujeta a los límites ambientales", OK),
        ("Cuádruple hélice", "+ sociedad civil y medios",
         "Entra el usuario y la demanda social", NAVY),
        ("Triple hélice", "Universidad · Empresa · Estado",
         "La innovación surge de la interacción entre los tres", ACCENT),
    ]

    for k, (nombre, actores, aporta, color) in enumerate(CAPAS):
        # k = 0 es la capa más externa. Cada capa interior se encoge por los
        # cuatro lados menos por arriba, que es donde vive su propio rótulo.
        x0 = 0.20 + k * 0.55
        y0 = 0.20 + k * 0.30
        an = 9.60 - 2 * (0.20 + k * 0.55)
        # La banda interior necesita 1,40 de alto para sus tres líneas más el
        # margen inferior: con 1,16 la tercera caía justo sobre su propio borde.
        al = 5.40 - y0 - (0.20 + k * 1.50)
        ax.add_patch(Rectangle((x0, y0), an, al, facecolor=color, alpha=0.10,
                               edgecolor=color, linewidth=1.5))
        ax.text(x0 + 0.30, y0 + al - 0.34, nombre, ha="left", va="center",
                fontsize=10.0, color=color, fontweight="bold")
        ax.text(x0 + 0.30, y0 + al - 0.74, actores, ha="left", va="center",
                fontsize=8.2, color=INK)
        ax.text(x0 + 0.30, y0 + al - 1.10, aporta, ha="left", va="center",
                fontsize=7.8, color=MUTED, style="italic")

    ax.set_xlim(0, 10.0)
    ax.set_ylim(0, 5.8)
    ax.axis("off")
    escribir(fig, "s1-helices")


FIGURAS += [fig_universidades_sir, fig_helices]

FIGURAS += [fig_umbral_innovacion, fig_evidencia_por_tipo, fig_trl_adopcion,
            fig_modelos_flujo]

FIGURAS += [fig_coeficiente_invencion, fig_scopus_100k, fig_renacyt_piramide,
            fig_ley_30309, fig_trl_escalera]




# ==========================================================================
# SESIÓN 1 · segunda tanda — formas distintas
# ==========================================================================
# La skill paper-visuals exige variar la forma según el trabajo del dato, no
# repetir barras. Aquí: dumbbell para una brecha entre dos entidades, waffle
# para una proporción sobre un total contable, pendiente para un cambio entre
# dos momentos, y bala para un avance contra una meta.


# POLCTI (CONCYTEC, 2024) y GII 2025 (OMPI). Cada par es Perú frente a Chile,
# el país de la región mejor situado en los cuatro indicadores.
# POLCTI (CONCYTEC, 2024) y GII 2025 (OMPI). Cada par es Perú frente a Chile,
# el país de la región mejor situado en los cuatro indicadores.
# El cuarto campo dice si un valor MAYOR es mejor: en el índice de innovación
# el dato es un puesto, y ahí menor es mejor. Sin ese campo la figura leería
# al revés justo la fila que más se malinterpreta.
BRECHA_CHILE = [
    ("Gasto en I+D · % del PBI", 0.13, 0.35, True, 2),
    ("Publicaciones · por 100 000 hab.", 18.5, 106.7, True, 1),
    ("Patentes · por millón de hab.", 2.1, 20.5, True, 1),
    ("Puesto en el índice de innovación", 80, 51, False, 0),
]


def fig_brecha_chile():
    """Cuatro indicadores, la misma distancia: el Perú está entre tres y diez veces por detrás."""
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ys = list(range(len(BRECHA_CHILE)))[::-1]

    for y, (_, peru, chile, mas_es_mejor, dec) in zip(ys, BRECHA_CHILE):
        # Cada indicador se normaliza contra su propio máximo —sus unidades no
        # son comparables— y se orienta para que la derecha sea siempre «mejor».
        mx = max(peru, chile)
        xp, xc = peru / mx, chile / mx
        if not mas_es_mejor:
            xp, xc = 1 - xp + 0.25, 1 - xc + 0.25
        ax.plot([xp, xc], [y, y], color=GRID, linewidth=2.6, solid_capstyle="round", zorder=1)
        ax.scatter([xc], [y], s=110, color=NAVY, zorder=3)
        ax.scatter([xp], [y], s=110, color=ACCENT, zorder=3)
        izq, der = (xp, xc) if xp < xc else (xc, xp)
        vi, vd = (peru, chile) if xp < xc else (chile, peru)
        ci, cd = (ACCENT, NAVY) if xp < xc else (NAVY, ACCENT)
        ax.text(izq - 0.03, y, num(vi, dec), ha="right", va="center", fontsize=8.5, color=ci)
        ax.text(der + 0.03, y, num(vd, dec), ha="left", va="center", fontsize=8.5, color=cd)

    ax.set_yticks(ys)
    ax.set_yticklabels([e for e, _, _, _, _ in BRECHA_CHILE], fontsize=8.5, color=INK)
    ax.set_xlim(-0.30, 1.42)
    ax.set_ylim(-0.9, len(BRECHA_CHILE) - 0.35)
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    # La leyenda va bajo el eje, en su propia banda: dentro del área de datos
    # se montaba sobre el último par.
    ax.scatter([], [], s=90, color=ACCENT, label="Perú")
    ax.scatter([], [], s=90, color=NAVY, label="Chile")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), fontsize=8.5,
              frameon=False, labelcolor=INK, ncol=2, handletextpad=0.3, columnspacing=1.6)
    ax.text(1.42, -0.85, "mejor →", fontsize=7.5, color=MUTED, ha="right", va="center")
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s1-brecha-chile")


# POLCTI (CONCYTEC, 2024), pág. 53, citando el estudio de línea base del gasto
# público en CTI (Rogers, 2020).
# POLCTI (CONCYTEC, 2024), págs. 53 y 68, citando el estudio de línea base del
# gasto público en CTI (Rogers, 2020). Curva de concentración del presupuesto
# de 164 instrumentos, promedio anual 2012-2018.
CONCENTRACION = [(1, 43), (13, 75), (45, 90), (164, 100)]
INSTRUMENTO_MAYOR = "Programa Nacional de Becas del Ministerio de Educación"


def fig_concentracion_gasto():
    """Un solo instrumento se lleva el 43 %; cuarenta y cinco de ciento sesenta y cuatro, el 90 %."""
    xs = [x for x, _ in CONCENTRACION]
    ys = [y for _, y in CONCENTRACION]

    fig, ax = plt.subplots(figsize=(6.8, 2.6))
    ax.plot([0] + xs, [0] + ys, color=ACCENT, linewidth=2.4, marker="o", markersize=6)
    ax.fill_between([0] + xs, [0] + ys, color=ACCENT, alpha=0.10)
    # Referencia: si el reparto fuera parejo, la curva sería la diagonal.
    ax.plot([0, 164], [0, 100], color=GRID, linewidth=1.2, linestyle=(0, (4, 3)))
    ax.text(120, 68, "reparto parejo", fontsize=7.4, color=MUTED, rotation=17)

    # El primer punto lleva el NOMBRE del instrumento, no su recuento: «1
    # instrumento · 43 %» obliga a preguntar cuál, y la respuesta —que el mayor
    # del sistema es un programa de becas y no un fondo de investigación— es
    # justo lo que explica la forma de la curva.
    rotulos = [
        f"Programa Nacional de Becas\n{num(CONCENTRACION[0][1], 0)} % del presupuesto",
        f"los {CONCENTRACION[1][0]} mayores\n{num(CONCENTRACION[1][1], 0)} %",
        f"{CONCENTRACION[2][0]} de 164\n{num(CONCENTRACION[2][1], 0)} %",
    ]
    for (x, y), rot in zip(CONCENTRACION[:3], rotulos):
        ax.annotate(rot, xy=(x, y), xytext=(x + 11, y - 16), fontsize=7.8,
                    color=INK, linespacing=1.35,
                    arrowprops=dict(arrowstyle="-", color=GRID, linewidth=0.9))

    ax.set_xlabel("Instrumentos de CTI ordenados por presupuesto asignado",
                  fontsize=8.4, color=MUTED)
    ax.set_ylabel("Presupuesto acumulado (%)", fontsize=8.4, color=MUTED)
    ax.set_xlim(0, 170); ax.set_ylim(0, 108)
    ax.tick_params(labelsize=7.8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s1-concentracion-gasto")


# POLCTI (CONCYTEC, 2024), Tabla 14. Instrumentos de CTI por sector, 2012-2018.
INSTRUMENTOS_SECTOR = [
    ("Producción", 71), ("CONCYTEC", 38), ("Educación", 26), ("Agricultura", 9),
    ("Ambiente", 8), ("Salud", 4), ("Otros sectores", 8),
]


def fig_instrumentos_sector():
    """Dos sectores concentran dos tercios de los instrumentos existentes."""
    nombres = [n for n, _ in INSTRUMENTOS_SECTOR][::-1]
    valores = [v for _, v in INSTRUMENTOS_SECTOR][::-1]
    total = sum(valores)
    colores = [ACCENT if v >= 26 else NAVY for v in valores]

    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    barras = ax.barh(nombres, valores, color=colores, height=0.66)
    for b, v in zip(barras, valores):
        ax.text(v + 1.4, b.get_y() + b.get_height() / 2,
                f"{v}  ({num(v / total * 100, 0)} %)", va="center", ha="left",
                fontsize=8.4, color=INK)
    ax.set_xlim(0, 92)
    ax.set_xlabel("Número de instrumentos de CTI", fontsize=8.4, color=MUTED)
    ax.tick_params(axis="y", labelsize=8.6, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=7.8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-instrumentos-sector")


# POLCTI (CONCYTEC, 2024), Tabla 10. Tasa de aprobación de los proyectos
# acogidos al beneficio tributario de la Ley 30309.
PENDIENTE_30309 = [(2016, 72, 8), (2022, 53, 28)]


def fig_pendiente_30309():
    """La tasa de aprobación pasó del 11 % al 53 % sin que cambiara la ley."""
    fig, ax = plt.subplots(figsize=(5.4, 2.2))
    ini, fin = PENDIENTE_30309
    tasa_i = ini[2] / ini[1] * 100
    tasa_f = fin[2] / fin[1] * 100

    ax.plot([0, 1], [tasa_i, tasa_f], color=ACCENT, linewidth=2.6, marker="o",
            markersize=9, solid_capstyle="round")
    ax.text(-0.06, tasa_i, f"{num(tasa_i, 0)} %", ha="right", va="center",
            fontsize=11, color=ACCENT, fontweight="bold")
    ax.text(1.06, tasa_f, f"{num(tasa_f, 0)} %", ha="left", va="center",
            fontsize=11, color=ACCENT, fontweight="bold")
    ax.text(0, tasa_i - 7, f"{ini[0]}\n{ini[2]} de {ini[1]}", ha="center", va="top",
            fontsize=8, color=MUTED)
    ax.text(1, tasa_f + 6, f"{fin[0]}\n{fin[2]} de {fin[1]}", ha="center", va="bottom",
            fontsize=8, color=MUTED)

    ax.set_xlim(-0.42, 1.42)
    ax.set_ylim(0, 72)
    ax.set_ylabel("Proyectos aprobados (%)", fontsize=8.5, color=MUTED)
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s1-pendiente-30309")


# POLCTI (CONCYTEC, 2024): gasto vigente 0,13 % del PBI (2018) y meta de 1 %
# al año 2030 fijada por el DS 093-2025-PCM.
META_PBI_ACTUAL = 0.13
META_PBI_OBJETIVO = 1.0
META_PBI_REGION = 0.71


def fig_meta_pbi():
    """Alcanzar la meta de 2030 exige multiplicar por siete el gasto actual."""
    fig, ax = plt.subplots(figsize=(6.6, 1.35))
    ax.barh(0, META_PBI_OBJETIVO, height=0.42, color=SURFACE, edgecolor=GRID, linewidth=0.8)
    ax.barh(0, META_PBI_ACTUAL, height=0.42, color=ACCENT)
    ax.vlines(META_PBI_REGION, -0.34, 0.34, color=NAVY, linewidth=2.2)

    ax.text(META_PBI_ACTUAL + 0.02, 0, f"{num(META_PBI_ACTUAL)} % hoy",
            va="center", ha="left", fontsize=9, color=ACCENT, fontweight="bold")
    ax.text(META_PBI_REGION, 0.42, f"media regional {num(META_PBI_REGION)} %",
            va="bottom", ha="center", fontsize=8, color=NAVY)
    ax.text(META_PBI_OBJETIVO, -0.44, f"meta 2030: {num(META_PBI_OBJETIVO, 0)} %",
            va="top", ha="right", fontsize=8.5, color=MUTED)

    ax.set_xlim(0, 1.12)
    ax.set_ylim(-0.75, 0.75)
    ax.set_yticks([])
    ax.set_xticks([])
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s1-meta-pbi")


# POLCTI (CONCYTEC, 2024), pág. 40 y 72, con datos de la Encuesta Nacional de
# Innovación en la Industria Manufacturera del INEI.
OBSTACULOS = [
    ("Costo de innovar demasiado elevado", 43.4),
    ("Escasez de personal calificado", 33.3),
    ("Falta de fondos en la empresa", 32.3),
]


def fig_obstaculos():
    """El primer obstáculo declarado no es el dinero: es no encontrar a quién contrate."""
    nombres = [n for n, _ in OBSTACULOS][::-1]
    valores = [v for _, v in OBSTACULOS][::-1]

    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    barras = ax.barh(nombres, valores, color=[NAVY, ACCENT, NAVY], height=0.6)
    for b, v in zip(barras, valores):
        ax.text(v + 0.9, b.get_y() + b.get_height() / 2, f"{num(v, 1)} %",
                va="center", ha="left", fontsize=9, color=INK)
    ax.set_xlim(0, 52)
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=8.5, colors=INK, length=0)
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s1-obstaculos")


FIGURAS += [fig_brecha_chile, fig_concentracion_gasto, fig_instrumentos_sector, fig_pendiente_30309,
            fig_meta_pbi, fig_obstaculos]


# ==========================================================================
# SESIÓN 1 · tercera tanda — formas de consultoría
# ==========================================================================


# POLCTI (CONCYTEC, 2024), Tabla 2, con datos del Foro Económico Mundial.
# Puesto del Perú en cada pilar del Índice de Competitividad Global, 2019,
# sobre 141 economías. Se guarda el puesto, no la puntuación: es el dato que
# publica la fuente.
# Los rótulos van en una palabra. Con dos líneas se salían del lienzo y el
# recorte automático los dejaba fuera: ocho de los doce vértices aparecían sin
# nombre. El nombre completo del pilar va en el cuerpo de la lámina.
PILARES_IGC = [
    ("Macro", 1), ("Salud", 19), ("Mercado", 49),
    ("Productos", 56), ("Finanzas", 67),
    ("Laboral", 77), ("Habilidades", 81), ("Infraestructura", 88),
    ("Instituciones", 94), ("Dinamismo", 97),
    ("TIC", 98), ("Innovación", 90),
]
IGC_TOTAL = 141


def fig_radar_pilares():
    """Primero del mundo en estabilidad macroeconómica, puesto 90 en capacidad de innovar."""
    n = len(PILARES_IGC)
    angulos = [2 * np.pi * i / n for i in range(n)]
    # Se invierte el puesto para que el radio grande sea «mejor»: un radar con
    # el eje al revés se lee justo al contrario de lo que dice.
    radios = [(IGC_TOTAL - p) / IGC_TOTAL for _, p in PILARES_IGC]
    ang = angulos + angulos[:1]
    rad = radios + radios[:1]

    fig, ax = plt.subplots(figsize=(4.6, 4.0), subplot_kw={"projection": "polar"})
    ax.plot(ang, rad, color=ACCENT, linewidth=2.0)
    ax.fill(ang, rad, color=ACCENT, alpha=0.16)
    ax.scatter(angulos, radios, s=26, color=ACCENT, zorder=3)

    for a, r, (nombre, puesto) in zip(angulos, radios, PILARES_IGC):
        color = OK if puesto <= 30 else (ACCENT if puesto >= 85 else MUTED)
        ax.text(a, r + 0.11, str(puesto), ha="center", va="center", fontsize=8,
                color=color, fontweight="bold")

    # Los rótulos se colocan a mano con `text` y no con `set_xticklabels`:
    # matplotlib los recorta contra el borde del lienzo cuando son de dos
    # líneas, y en un radar de doce vértices eso deja media figura sin leer.
    ax.set_xticks(angulos)
    ax.set_xticklabels([])
    for a, (nombre, _) in zip(angulos, PILARES_IGC):
        grados = np.degrees(a)
        ha = "center"
        if 10 < grados < 170:
            ha = "left"
        elif 190 < grados < 350:
            ha = "right"
        # clip_on=False: el rótulo vive fuera del radio máximo del eje polar y
        # matplotlib lo recorta por omisión, que era lo que dejaba ocho de los
        # doce vértices sin nombre.
        ax.text(a, 1.09, nombre, ha=ha, va="center", fontsize=7.4, color=INK)
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels([])
    ax.set_ylim(0, 1.24)
    ax.grid(color=GRID, linewidth=0.6)
    ax.spines["polar"].set_color(GRID)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    escribir(fig, "s1-radar-pilares")


# POLCTI (CONCYTEC, 2024), Gráfico 47, con datos de SCImago. Documentos
# publicados por el Perú en 2019, por área temática.
TEMATICAS = [
    ("Medicina", 1312), ("Ciencias agrícolas y biológicas", 662),
    ("Ciencia medioambiental", 363), ("Bioquímica y biología molecular", 305),
    ("Física y astronomía", 264), ("Inmunología y microbiología", 153),
]


def fig_treemap_tematicas():
    """La mitad de lo que el Perú publica es medicina; la ingeniería no aparece."""
    # Los rótulos van FUERA de los bloques pequeños. Dentro se recortaban al
    # componer la lámina en dos columnas, y cinco de las seis áreas quedaban
    # como bandas de color sin nombre.
    total = sum(v for _, v in TEMATICAS)
    fig, ax = plt.subplots(figsize=(7.2, 3.1))

    nombre_g, valor_g = TEMATICAS[0]
    w1 = 0.34
    ax.add_patch(Rectangle((0, 0), w1, 1, facecolor=ACCENT, edgecolor=PAPER, linewidth=2))
    ax.text(w1 / 2, 0.55, nombre_g, ha="center", va="center", fontsize=10.5,
            color=PAPER, fontweight="bold")
    ax.text(w1 / 2, 0.42, f"{num(valor_g, 0)}", ha="center", va="center",
            fontsize=13, color=PAPER, fontweight="bold")
    ax.text(w1 / 2, 0.32, f"{num(valor_g / total * 100, 0)} % del total",
            ha="center", va="center", fontsize=8, color=PAPER)

    resto = TEMATICAS[1:]
    suma = sum(v for _, v in resto)
    y = 1.0
    for k, (nombre, v) in enumerate(resto):
        h = (v / suma) * 1.0
        ax.add_patch(Rectangle((w1 + 0.03, y - h + 0.012), 0.11, h - 0.024,
                               facecolor=NAVY if k % 2 == 0 else MUTED, edgecolor="none"))
        etiqueta = nombre.replace("\n", " ")
        ax.text(w1 + 0.19, y - h / 2, etiqueta, ha="left",
                va="center", fontsize=8.2, color=INK)
        # La cifra se coloca contra el ancho real del rótulo, no contra el
        # canto derecho: «Ciencias agrícolas y biológicas» mide el doble que
        # «Medicina» y con la cifra fija se le montaba encima.
        ax.text(w1 + 0.215 + 0.0135 * len(etiqueta), y - h / 2, num(v, 0),
                ha="left", va="center", fontsize=8.2, color=INK,
                fontweight="bold")
        y -= h

    ax.set_xlim(-0.01, 1.03)
    ax.set_ylim(-0.02, 1.02)
    ax.axis("off")
    escribir(fig, "s1-treemap-tematicas")


# POLCTI (CONCYTEC, 2024), Tabla 3, Índice de Competitividad Regional 2023.
# Se muestran los cinco primeros y los cinco últimos de veinticinco regiones.
REGIONES_ICR = [
    ("Lima", 7.6), ("Moquegua", 7.6), ("Tacna", 6.8), ("Arequipa", 6.7), ("Ica", 6.2),
    ("Puno", 3.2), ("Huánuco", 3.1), ("Ucayali", 2.9), ("Loreto", 2.8),
]


def fig_regiones():
    """Entre la primera región y la última hay una distancia de casi tres a uno."""
    nombres = [n for n, _ in REGIONES_ICR][::-1]
    valores = [v for _, v in REGIONES_ICR][::-1]
    colores = [ACCENT if v < 4 else NAVY for v in valores]

    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    barras = ax.barh(nombres, valores, color=colores, height=0.66)
    for b, v in zip(barras, valores):
        ax.text(v + 0.14, b.get_y() + b.get_height() / 2, num(v, 1),
                va="center", ha="left", fontsize=8.5, color=INK)
    ax.axhline(4.5, color=GRID, linewidth=1.0, linestyle=(0, (3, 3)))
    ax.text(8.1, 4.5, "16 regiones\nintermedias", fontsize=7.5, color=MUTED,
            ha="right", va="center")
    ax.set_xlim(0, 8.6)
    ax.set_xlabel("Índice de Competitividad Regional 2023", fontsize=8.5, color=MUTED)
    ax.tick_params(axis="y", labelsize=8.5, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s1-regiones")


def fig_cascada_meta():
    """Cerrar la brecha hasta el 1 % exige que las tres fuentes crezcan a la vez."""
    # Descomposición ilustrativa del salto entre el gasto vigente y la meta.
    # Las dos magnitudes de los extremos son datos; el reparto intermedio es
    # una hipótesis de trabajo y así se rotula en la lámina.
    pasos = [("Hoy", 0.13, ACCENT), ("Sector\npúblico", 0.29, NAVY),
             ("Empresa\nprivada", 0.35, NAVY), ("Cooperación\ny otros", 0.23, NAVY),
             ("Meta 2030", 1.00, OK)]
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    acum = 0.0
    for i, (nombre, v, color) in enumerate(pasos):
        if i == 0 or i == len(pasos) - 1:
            ax.bar(i, v, width=0.62, color=color)
            ax.text(i, v + 0.04, f"{num(v)} %", ha="center", va="bottom",
                    fontsize=9, color=color, fontweight="bold")
            acum = v if i == 0 else acum
        else:
            ax.bar(i, v, bottom=acum, width=0.62, color=color)
            ax.text(i, acum + v / 2, f"+{num(v)}", ha="center", va="center",
                    fontsize=8.5, color=PAPER)
            acum += v
    ax.set_xticks(range(len(pasos)))
    ax.set_xticklabels([n for n, _, _ in pasos], fontsize=8, color=INK)
    ax.set_ylabel("Gasto en I+D sobre el PBI (%)", fontsize=8.5, color=MUTED)
    ax.set_ylim(0, 1.22)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s1-cascada-meta")


def fig_matriz_proyecto():
    """Los dos ejes que deciden el instrumento: cuánto se sabe y para qué sirve."""
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    cuadrantes = [
        (0.25, 0.75, "Investigación\nbásica", "Alta incertidumbre,\nsin aplicación prevista", NAVY),
        (0.75, 0.75, "Investigación\naplicada", "Alta incertidumbre,\ncon objetivo práctico", ACCENT),
        (0.25, 0.25, "Actividad\nrutinaria", "Baja incertidumbre,\nsin objetivo nuevo", MUTED),
        (0.75, 0.25, "Desarrollo\nexperimental", "Baja incertidumbre,\nproducto definido", WARN),
    ]
    for x, y, titulo, sub, color in cuadrantes:
        ax.add_patch(Rectangle((x - 0.25, y - 0.25), 0.5, 0.5,
                               facecolor=color, alpha=0.13, edgecolor=PAPER, linewidth=3))
        ax.text(x, y + 0.09, titulo, ha="center", va="center", fontsize=9.5,
                color=color, fontweight="bold")
        ax.text(x, y - 0.10, sub, ha="center", va="center", fontsize=7.4, color=MUTED)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("¿Hay una aplicación prevista?  →", fontsize=8.5, color=INK)
    ax.set_ylabel("¿Cuánta incertidumbre queda?  →", fontsize=8.5, color=INK)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRID)
    escribir(fig, "s1-matriz-proyecto")


def fig_embudo_idi():
    """De cada cien ideas, muy pocas llegan a estar en uso por un tercero."""
    # Embudo: etapas ordenadas, así que rampa y no tonos categóricos. El
    # último escalón lleva el acento porque es el que la lámina destaca.
    etapas = [("Ideas de proyecto", 100, RAMPA[0]), ("Propuestas formuladas", 46, RAMPA[0]),
              ("Admisibles", 30, RAMPA[1]), ("Adjudicadas", 12, RAMPA[2]),
              ("En uso por un tercero", 4, ACCENT)]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for i, (nombre, v, color) in enumerate(etapas):
        y = len(etapas) - i - 1
        ax.barh(y, v, height=0.62, color=color, left=(100 - v) / 2)
        ax.text(50, y, f"{nombre} · {v}", ha="center", va="center",
                fontsize=8.5, color=PAPER if v > 22 else INK)
    ax.set_xlim(-4, 104); ax.set_ylim(-0.7, len(etapas) - 0.3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.axis("off")
    escribir(fig, "s1-embudo-idi")


FIGURAS += [fig_madurez_doble, fig_radar_pilares, fig_treemap_tematicas, fig_regiones,
            fig_cascada_meta, fig_matriz_proyecto, fig_embudo_idi]


# Panorama de herramientas de IA para el trabajo de formulación, situado por
# lo que sabe hacer cada familia. No hay dato externo que citar: es una
# clasificación funcional, y como tal se rotula en la lámina.
# Herramientas de IA en uso a mediados de 2026, por categoría. La lista es de
# elaboración propia y así se rotula: no hay fuente publicada que la fije, y
# cambia cada pocos meses. Se cita la fecha de consulta en la lámina.
# Seis categorías, y la frontera que importa es dónde corre la herramienta y
# qué permisos tiene sobre los archivos. Las tres del medio comparten motor y
# se distinguen por la superficie: editor, terminal o aplicación propia. Esa
# distinción decide qué se le puede encargar a cada una y quién la usa: el
# editor y la terminal piden saber programar, la aplicación de escritorio no.
HERRAMIENTAS_IA = [
    ("Chat de navegador", ["ChatGPT", "Claude", "Gemini", "Copilot"],
     "Escriben. Sin acceso a archivos.", NAVY),
    ("Editor con agente", ["Cursor", "VS Code", "Windsurf"],
     "Editan el proyecto abierto.", NAVY),
    ("Agente de terminal", ["Claude Code", "Codex CLI", "Gemini CLI", "Kimi Code"],
     "Ejecutan órdenes de consola.", ACCENT),
    ("Agente de escritorio", ["Claude Cowork", "Antigravity"],
     "Aplicación propia, sin consola.", ACCENT),
    ("Búsqueda con citación", ["Perplexity", "Elicit", "Consensus", "Scite"],
     "Devuelven el enlace citado.", OK),
    ("Detección de texto", ["Turnitin", "ZeroGPT", "Originality", "GPTZero"],
     "Devuelven probabilidad, no prueba.", WARN),
]


def fig_herramientas_ia():
    """Seis categorías, separadas por el acceso que la herramienta tiene a los archivos."""
    # El rótulo de categoría y su descripción viven en un recuadro propio, y
    # los nombres de herramienta a su derecha.
    #
    # El paso entre nombres NO es fijo. Con paso constante, «Claude Cowork»
    # pisaba el punto de «Antigravity»: los nombres miden entre cinco y trece
    # caracteres y el más largo decide. Cada nombre avanza según su longitud.
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ANCHO_CAJA, X_TOOLS = 3.55, 3.85
    ancho = lambda nom: 0.34 + 0.108 * len(nom)
    fin_max = X_TOOLS
    for k, (cat, nombres, uso, color) in enumerate(HERRAMIENTAS_IA):
        y = len(HERRAMIENTAS_IA) - k - 1
        ax.add_patch(Rectangle((0, y - 0.40), ANCHO_CAJA, 0.80, facecolor=color,
                               alpha=0.13, edgecolor=color, linewidth=1.1))
        ax.text(0.14, y + 0.14, cat, ha="left", va="center", fontsize=8.6,
                color=color, fontweight="bold")
        ax.text(0.14, y - 0.18, uso, ha="left", va="center", fontsize=6.6, color=MUTED)
        x = X_TOOLS
        for nom in nombres:
            ax.plot([x], [y], "o", color=color, markersize=4.5)
            ax.text(x + 0.12, y, nom, ha="left", va="center", fontsize=7.8, color=INK)
            x += ancho(nom)
        fin_max = max(fin_max, x)
    ax.set_xlim(-0.05, fin_max + 0.1)
    ax.set_ylim(-0.72, len(HERRAMIENTAS_IA) - 0.28)
    ax.axis("off")
    escribir(fig, "s1-herramientas-ia")


# Evolución de las capacidades de los modelos de lenguaje. Las fechas son las
# de disponibilidad general; el eje vertical es cualitativo y así se rotula.
# Horizonte temporal de tarea al 50 % de acierto, la métrica de METR: cuánto
# tarda una persona en la tarea más larga que el modelo resuelve la mitad de
# las veces. Suite de 170 tareas de programación —HCAST, RE-Bench y SWAA—.
#
# Solo van los valores que el artículo publica. Los intermedios existen en su
# gráfica pero no en cifra, y la escala anterior de esta figura era una
# invención: un eje de «capacidades acumuladas» de 0 a 1 sin unidad ni fuente.
# El ajuste exponencial que el propio artículo declara —duplicación cada 207
# días, IC 95 % de 166 a 240— se dibuja como línea, y encima los puntos
# medidos, que es lo que distingue el dato del modelo del dato observado.
#
# En minutos, porque la escala es logarítmica y cubre de dos segundos a
# dieciséis horas: cinco órdenes de magnitud.
# El quinto campo es el desplazamiento del rótulo en puntos. Va explícito
# porque Claude 3.7 Sonnet y o3 están a dos meses de distancia y con un
# desplazamiento común sus rótulos se superponían.
EVOLUCION_IA = [
    (2019.1, 2 / 60, "GPT-2", "2 s", (10, -2), "left", "top"),
    (2025.15, 50.0, "Claude 3.7 Sonnet", "50 min", (14, -10), "left", "top"),
    (2025.3, 110.0, "o3", "1 h 50 min", (-14, 12), "right", "bottom"),
    (2026.4, 16 * 60.0, "frontera 2026", "más de 16 h", (-8, 6), "right", "bottom"),
]

# Duplicación cada 207 días declarada por el artículo: 365/207 duplicaciones
# por año.
DUPLICACION_DIAS = 207


def fig_evolucion_ia():
    """Horizonte temporal de tarea al 50 %: de dos segundos a más de dieciséis horas."""
    fig, ax = plt.subplots(figsize=(7.4, 3.1))

    # Ajuste del artículo, no una interpolación entre puntos: se ancla en el
    # primer valor medido y crece duplicando cada 207 días.
    x0, y0 = EVOLUCION_IA[0][0], EVOLUCION_IA[0][1]
    xs_ajuste = [x0 + i * 0.05 for i in range(int((2026.6 - x0) / 0.05) + 1)]
    ys_ajuste = [y0 * 2 ** ((x - x0) * 365 / DUPLICACION_DIAS) for x in xs_ajuste]
    ax.plot(xs_ajuste, ys_ajuste, color=MUTED, linewidth=1.3, linestyle=(0, (4, 3)),
            zorder=1)
    ax.text(2021.5, 0.9, "duplicación cada 207 días", fontsize=6.8, color=MUTED,
            rotation=31, rotation_mode="anchor", ha="left", va="bottom")

    for x, y, nom, etiq, desp, ha, va in EVOLUCION_IA:
        ax.plot([x], [y], "o", color=ACCENT, markersize=7.5, zorder=3)
        ax.annotate(f"{nom}\n{etiq}", (x, y), textcoords="offset points",
                    xytext=desp, ha=ha, va=va, fontsize=7.6, color=INK,
                    linespacing=1.35, zorder=3)

    ax.set_yscale("log")
    ax.set_ylim(0.015, 4200)
    ax.set_xlim(2018.7, 2027.3)
    ax.set_yticks([1 / 60, 1, 60, 60 * 8])
    ax.set_yticklabels(["1 s", "1 min", "1 h", "8 h"])
    ax.set_xticks([2019, 2021, 2023, 2025, 2027])
    ax.set_xticklabels(["2019", "2021", "2023", "2025", "2027"])
    ax.set_ylabel("Duración humana de la tarea", fontsize=8.2, color=MUTED)
    ax.tick_params(labelsize=8.0, colors=INK, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.6, alpha=0.55)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right"))
    escribir(fig, "s1-evolucion-ia")


# Lo que un modelo no resuelve por muy capaz que sea. Es la lámina de límites,
# y va con la de capacidades para que no se lea como una promesa.
LIMITES_IA = [
    ("Inventa referencias", "Cita con formato correcto y existencia dudosa", ACCENT),
    ("No conoce lo no publicado", "Bases de convocatoria, actas internas, datos propios", ACCENT),
    ("Desactualizado", "Cifras y normas posteriores a su corte de conocimiento", WARN),
    ("Detección poco fiable", "Los detectores estiman; sus falsos positivos son altos", WARN),
]


def fig_limites_ia():
    """Cuatro límites que ninguna versión nueva ha resuelto todavía."""
    fig, ax = plt.subplots(figsize=(6.8, 2.6))
    for k, (titulo, detalle, color) in enumerate(LIMITES_IA):
        y = len(LIMITES_IA) - k - 1
        ax.add_patch(Rectangle((0, y - 0.36), 0.055, 0.72, facecolor=color))
        ax.text(0.14, y + 0.10, titulo, ha="left", va="center", fontsize=9.0,
                color=color, fontweight="bold")
        ax.text(0.14, y - 0.16, detalle, ha="left", va="center", fontsize=8.0, color=INK)
    ax.set_xlim(-0.02, 5.2); ax.set_ylim(-0.7, len(LIMITES_IA) - 0.3)
    ax.axis("off")
    escribir(fig, "s1-limites-ia")


FIGURAS += [fig_herramientas_ia, fig_evolucion_ia, fig_limites_ia]



# ==========================================================================
# SESIÓN 2 · Tema 01 — figuras con las que un resultado sale de la universidad
# ==========================================================================

# Peña y Jenik (2023), BID, «Deep Tech: The New Wave», capítulo 4. Cuatro
# recuentos de América Latina y el Caribe que el informe publica juntos como
# una cadena: investigadores en ciencia y tecnología sin contar personal
# técnico, artículos publicados al año, solicitudes de patente al año y
# empresas de tecnología profunda con inversión institucional.
#
# El cociente entre pasos NO está en el informe: se calcula aquí a partir de
# los cuatro recuentos, que es lo único que la fuente da.
CONVERSION_LAC = [
    ("Investigadores en ciencia y tecnología", 523_000),
    ("Artículos publicados al año", 180_000),
    ("Solicitudes de patente al año", 12_000),
    ("Empresas de tecnología profunda con inversión", 340),
]


def fig_conversion_investigacion():
    """De medio millón de investigadores salen 340 empresas con inversión."""
    # Escala logarítmica: los cuatro recuentos cubren tres órdenes y medio de
    # magnitud, y en escala lineal las tres filas inferiores se aplastan
    # contra el eje hasta desaparecer.
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    X0 = 260.0
    n = len(CONVERSION_LAC)

    for k, (nombre, v) in enumerate(CONVERSION_LAC):
        y = n - 1 - k
        color = ACCENT if k == n - 1 else NAVY
        ax.hlines(y, X0, v, color=color, linewidth=2.6, alpha=0.5, zorder=1)
        ax.plot([v], [y], "o", color=color, markersize=8.5, zorder=3)
        # El rótulo va ENCIMA de su propia línea. A la izquierda no cabe: en
        # eje logarítmico el tramo anterior a X0 mide menos de una década, y
        # un nombre de cuarenta y cinco caracteres se sale del lienzo.
        ax.text(X0, y + 0.24, nombre, ha="left", va="bottom", fontsize=8.0, color=INK)
        ax.text(v * 1.28, y, num(v, 0), ha="left", va="center", fontsize=8.8,
                color=color, fontweight="bold")

    # El cociente entre pasos consecutivos, en columna propia a la derecha.
    # Dentro del área de datos se montaba sobre la cifra de la fila de abajo.
    for k in range(n - 1):
        mayor, menor = CONVERSION_LAC[k][1], CONVERSION_LAC[k + 1][1]
        ax.text(1.75e6, (n - 1 - k) - 0.5, f"÷ {num(mayor / menor, 1)}",
                ha="center", va="center", fontsize=8.4, color=MUTED)

    ax.set_xscale("log")
    ax.set_xlim(200, 5.0e6)
    ax.set_ylim(-0.62, n - 0.30)
    ax.set_yticks([])
    ax.set_xticks([1e3, 1e4, 1e5, 1e6])
    ax.set_xticklabels([num(v, 0) for v in (1e3, 1e4, 1e5, 1e6)])
    ax.set_xlabel("Recuento · escala logarítmica", fontsize=8.2, color=MUTED)
    ax.tick_params(axis="x", labelsize=7.8, colors=MUTED, length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s2-conversion-investigacion")


# Correspondencia entre la vía por la que un resultado sale de la universidad
# y lo que cada una exige antes de poder operar. No hay dato externo que
# citar: es la lectura conjunta del régimen de propiedad industrial y de lo
# que cada vía necesita, y así se rotula en la lámina.
#
# Los tres nombres de columna miden entre siete y ocho caracteres, así que el
# paso constante es seguro aquí. En las filas el paso no importa: los rótulos
# van alineados a la derecha y crecen hacia el margen.
VIAS_SALIDA = [("Licencia", NAVY), ("Spin-off", ACCENT), ("Startup", OK)]
REQUISITOS_SALIDA = [
    ("Resultado protegido o en trámite de protección", (0, 1, 2)),
    ("Socio que ya opera en el mercado de destino", (0,)),
    ("Empresa nueva constituida y con gerencia", (1, 2)),
    ("Universidad en el acuerdo o en el capital", (0, 1)),
    ("Equipo dedicado a tiempo completo al producto", (1, 2)),
    ("Capital externo dispuesto a asumir el riesgo", (2,)),
]


def fig_figuras_salida():
    """La licencia no obliga a constituir empresa; la startup exige capital externo."""
    fig, ax = plt.subplots(figsize=(8.6, 2.5))
    PASO = 1.55
    xs = [i * PASO for i in range(len(VIAS_SALIDA))]
    n = len(REQUISITOS_SALIDA)

    for k, (rotulo, columnas) in enumerate(REQUISITOS_SALIDA):
        y = n - 1 - k
        ax.hlines(y, -0.55, xs[-1] + 0.55, color=GRID, linewidth=0.6, alpha=0.7)
        ax.text(-0.95, y, rotulo, ha="right", va="center", fontsize=7.2, color=INK)
        for j, x in enumerate(xs):
            if j in columnas:
                ax.scatter([x], [y], s=130, color=VIAS_SALIDA[j][1], zorder=3)
            else:
                ax.scatter([x], [y], s=13, color=GRID, zorder=2)

    for (nombre, color), x in zip(VIAS_SALIDA, xs):
        ax.text(x, n - 0.56, nombre, ha="center", va="bottom", fontsize=7.6,
                color=color, fontweight="bold")

    # El compromiso crece de izquierda a derecha, y sin la flecha las tres
    # columnas se leen como casos sueltos en vez de como una progresión.
    ax.add_patch(FancyArrowPatch((xs[0] - 0.35, n + 0.30), (xs[-1] + 0.35, n + 0.30),
                                 arrowstyle="-|>", mutation_scale=9, color=MUTED,
                                 linewidth=1.0, shrinkA=0, shrinkB=0))
    ax.text((xs[0] + xs[-1]) / 2, n + 0.44, "riesgo que asume el equipo",
            ha="center", va="bottom", fontsize=7.0, color=MUTED)

    ax.set_xlim(-6.40, xs[-1] + 0.70)
    ax.set_ylim(-0.60, n + 0.95)
    ax.axis("off")
    escribir(fig, "s2-figuras-salida")


# Reparto de los dos derechos que un resultado protegido genera, a lo largo
# de la cadena que lo lleva al mercado. La mención como inventor se queda en
# el primer eslabón y no se transfiere; el derecho de explotación viaja por
# contrato. No hay cifra que citar: es el régimen llevado a diagrama, y por
# eso vive aquí en vez de repetirse en prosa en cada lámina que lo necesite.
CADENA_TITULARIDAD = [
    ("Inventor", "concibe el resultado"),
    ("Titular", "decide, licencia y cobra"),
    ("Licenciatario", "produce y vende"),
    ("Usuario", "paga y usa"),
]
BANDAS_TITULARIDAD = [
    ("Mención como inventor · no se transfiere", 0, 0, NAVY),
    ("Derecho de explotación · se transfiere", 1, 2, ACCENT),
]


def fig_titularidad_cadena():
    """La mención de inventoría se queda; el derecho de explotación viaja."""
    fig, ax = plt.subplots(figsize=(7.8, 2.6))
    ALTO, HUECO = 0.72, 0.42
    # El ancho de cada caja se calcula con la longitud de su texto más largo.
    # Con ancho fijo, «Licenciatario» y «decide, licencia y cobra» se salían
    # de la caja mientras «Usuario» dejaba media caja vacía.
    anchos = [0.42 + 0.088 * max(len(t), len(s)) for t, s in CADENA_TITULARIDAD]
    xs, x = [], 0.0
    for a in anchos:
        xs.append(x)
        x += a + HUECO

    Y = 0.90
    for (nombre, hace), x0, a in zip(CADENA_TITULARIDAD, xs, anchos):
        ax.add_patch(Rectangle((x0, Y - ALTO / 2), a, ALTO, facecolor=MUTED,
                               alpha=0.10, edgecolor=MUTED, linewidth=1.1))
        ax.text(x0 + a / 2, Y + 0.13, nombre, ha="center", va="center",
                fontsize=9.2, color=INK, fontweight="bold")
        ax.text(x0 + a / 2, Y - 0.16, hace, ha="center", va="center",
                fontsize=7.2, color=MUTED)

    for i in range(len(xs) - 1):
        ax.add_patch(FancyArrowPatch((xs[i] + anchos[i], Y), (xs[i + 1], Y),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=MUTED, linewidth=1.2, shrinkA=0, shrinkB=0))

    # Las dos bandas dicen qué derecho cubre qué tramo. La banda es una barra
    # FINA y el texto va debajo, no dentro: encerrado en un rectángulo del
    # ancho del tramo, el rótulo de cuarenta caracteres se salía de su propia
    # caja en las dos bandas, que es peor que no dibujarlas.
    for k, (texto, i0, i1, color) in enumerate(BANDAS_TITULARIDAD):
        y = -0.05 - k * 0.58
        x0 = xs[i0]
        x1 = xs[i1] + anchos[i1]
        ax.add_patch(Rectangle((x0, y - 0.06), x1 - x0, 0.12, facecolor=color,
                               edgecolor="none"))
        ax.text(x0, y - 0.20, texto, ha="left", va="top", fontsize=7.4, color=color)

    ax.set_xlim(-0.10, xs[-1] + anchos[-1] + 0.20)
    ax.set_ylim(-1.05, 1.45)
    ax.axis("off")
    escribir(fig, "s2-titularidad-cadena")


# Plazos del Tratado de Cooperación en materia de Patentes (PCT), contados
# desde la fecha de prioridad, y el tramo anterior a ella, que es el único
# que no admite reparación. Fuente: OMPI, Guía del solicitante PCT.
#
# El eje es el mes contado desde la prioridad, así que aquí el paso SÍ es el
# dato: los hitos van en su posición real y no a intervalos iguales, al
# contrario que la línea de hitos normativos de la sesión 1, donde lo que se
# enseñaba era la secuencia.
#
# El cuarto campo es el lado en el que va el rótulo, y va escrito porque no
# puede alternar: los hitos del mes 12 y del mes 18 están a seis meses y sus
# rótulos miden más de veinte caracteres, así que tienen que caer en lados
# opuestos. Con lados alternos por índice, dos de los cuatro se pisaban.
HITOS_PATENTE = [
    (0, "Solicitud presentada", "fecha de prioridad fijada", "arriba"),
    (12, "Extender al extranjero", "solicitud internacional PCT", "abajo"),
    (18, "Publicación internacional", "el contenido se hace público", "arriba"),
    (30, "Entrada en fase nacional", "en cada país elegido", "abajo"),
]


def fig_reloj_patente():
    """Los tres plazos corren desde la prioridad; lo anterior no se repara."""
    fig, ax = plt.subplots(figsize=(7.4, 2.4))

    # El tramo previo a la prioridad, en el que cualquier divulgación destruye
    # la novedad. Es el hallazgo de la figura y por eso lleva el acento.
    ax.add_patch(Rectangle((-9.4, -0.13), 9.4, 0.26, facecolor=ACCENT, alpha=0.14,
                           edgecolor="none"))
    ax.text(-4.7, 0.0, "divulgar\naquí destruye\nla novedad", ha="center",
            va="center", fontsize=7.0, color=ACCENT, linespacing=1.25)

    ax.hlines(0, 0, 30, color=GRID, linewidth=1.6)

    for mes, titulo, detalle, lado in HITOS_PATENTE:
        arriba = lado == "arriba"
        y = 0.40 if arriba else -0.40
        color = ACCENT if mes == 18 else NAVY
        ax.vlines(mes, 0, y, color=color, linewidth=1.3)
        ax.plot(mes, 0, "o", color=color, markersize=6.5, zorder=3)
        # Todos los rótulos arrancan EN su propio hito y crecen hacia la
        # derecha. Centrados, el del mes 18 pisaba el del mes 0, y el del mes
        # 30 pisaba el del mes 12.
        ax.text(mes, y + (0.10 if arriba else -0.10), titulo, ha="left",
                va="bottom" if arriba else "top", fontsize=8.2, color=INK,
                fontweight="bold")
        ax.text(mes, y + (0.30 if arriba else -0.30), detalle, ha="left",
                va="bottom" if arriba else "top", fontsize=7.0, color=MUTED)
        # El número de mes va al otro lado de la línea que su rótulo, para que
        # no compita con él ni con la banda de la izquierda.
        ax.text(mes + 0.5, -0.05 if arriba else 0.05, f"mes {mes}", ha="left",
                va="top" if arriba else "bottom", fontsize=7.0, color=MUTED)

    ax.text(0, -1.00, "meses contados desde la fecha de prioridad  →",
            ha="left", va="center", fontsize=7.4, color=MUTED)
    ax.set_xlim(-10.0, 46.0)
    ax.set_ylim(-1.14, 0.95)
    ax.axis("off")
    escribir(fig, "s2-reloj-patente")


# Peña y Jenik (2023), BID, capítulo 3: los nueve obstáculos que dejan a una
# empresa de tecnología profunda fuera del alcance de la inversión
# institucional. Los nueve son de la fuente; la agrupación en tres familias
# se hace aquí, y es lo que permite ver que dos de los nueve se resuelven con
# documentos y no con dinero.
OBSTACULOS_BID = [
    ("Titularidad y protección", ACCENT, [
        "Protección insuficiente del resultado",
        "Barreras institucionales para licenciarlo",
    ]),
    ("Mercado y producto", NAVY, [
        "Innovación incremental",
        "Mercado objetivo pequeño",
        "Ruta a la comercialización sin definir",
        "Tiempo hasta el mercado prolongado",
    ]),
    ("Equipo y capital", OK, [
        "Capacidades de negocio y comunicación ausentes",
        "Estructura de propiedad comprometida",
        "Capital de riesgo escaso",
    ]),
]


def fig_obstaculos_salida():
    """Siete de los nueve dependen del equipo y del mercado; dos, del contrato."""
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    # El paso vertical no es fijo: una familia ocupa el alto de su rótulo más
    # el de sus obstáculos, y con paso constante la familia de cuatro pisaba
    # el rótulo de la siguiente.
    y = 0.0
    for nombre, color, items in OBSTACULOS_BID:
        alto = 0.40 + 0.34 * len(items)
        ax.add_patch(Rectangle((0, y - alto + 0.14), 0.055, alto - 0.10,
                               facecolor=color))
        ax.text(0.16, y, f"{nombre}  ·  {len(items)} de 9", ha="left", va="center",
                fontsize=8.6, color=color, fontweight="bold")
        for j, texto in enumerate(items):
            ax.plot([0.22], [y - 0.36 - j * 0.34], "o", color=color, markersize=3.4)
            ax.text(0.32, y - 0.36 - j * 0.34, texto, ha="left", va="center",
                    fontsize=8.0, color=INK)
        y -= alto + 0.16

    ax.set_xlim(-0.02, 5.4)
    ax.set_ylim(y + 0.30, 0.42)
    ax.axis("off")
    escribir(fig, "s2-obstaculos-salida")


# Nguyen et al. (2024), Sustainability 16(19):8714, secciones 1 y 2.3. Los
# cinco rasgos con los que el artículo separa una empresa de tecnología
# profunda de una empresa digital. Son categorías y no magnitudes: no hay eje
# que las ordene, y normalizarlas a un número habría sido inventar una escala.
RASGOS_DEEP_TECH = [
    ("Ciclo de desarrollo", "Iterativo, rápido y ligero", "Secuencial, largo y costoso"),
    ("Barrera de entrada", "Baja", "Alta"),
    ("Formación del fundador", "Sin exigencia técnica", "Doctorado o posgrado técnico"),
    ("Casos previos de referencia", "Abundantes", "Escasos"),
    ("Inversión inicial", "Contenida", "Elevada"),
]


def fig_deep_tech_frente_digital():
    """La diferencia se concentra en el ciclo: iterar barato frente a encadenar etapas."""
    fig, ax = plt.subplots(figsize=(8.4, 2.7))
    X_DIG, X_DEEP, ANCHO, ALTO = 0.0, 3.25, 3.05, 0.62
    n = len(RASGOS_DEEP_TECH)

    for k, (rasgo, digital, profunda) in enumerate(RASGOS_DEEP_TECH):
        y = n - 1 - k
        ax.text(-0.24, y, rasgo, ha="right", va="center", fontsize=8.0, color=INK)
        for x0, texto, color in ((X_DIG, digital, NAVY), (X_DEEP, profunda, ACCENT)):
            ax.add_patch(Rectangle((x0, y - ALTO / 2), ANCHO, ALTO, facecolor=color,
                                   alpha=0.12, edgecolor=color, linewidth=1.0))
            # Cuerpo a 7,4: «Doctorado o posgrado técnico» mide veintiocho
            # caracteres y a 7,6 llegaba al canto de su propia caja.
            ax.text(x0 + ANCHO / 2, y, texto, ha="center", va="center",
                    fontsize=7.4, color=INK)

    ax.text(X_DIG + ANCHO / 2, n - 0.44, "Empresa digital", ha="center", va="bottom",
            fontsize=8.6, color=NAVY, fontweight="bold")
    ax.text(X_DEEP + ANCHO / 2, n - 0.44, "Tecnología profunda", ha="center",
            va="bottom", fontsize=8.6, color=ACCENT, fontweight="bold")

    ax.set_xlim(-3.30, X_DEEP + ANCHO + 0.12)
    ax.set_ylim(-0.55, n - 0.02)
    ax.axis("off")
    escribir(fig, "s2-deep-tech-frente-digital")


# Nguyen et al. (2024), figura 2 y sección 5.8: cinco fases con seis
# actividades. Lo que el modelo aporta respecto de los procesos anteriores es
# que la cuarta fase tiene DOS actividades simultáneas, desarrollo del
# producto y financiamiento, en lugar de una detrás de la otra. Se dibuja
# como dos ramas paralelas porque es exactamente eso lo que la prosa no
# consigue decir en el mismo espacio.
FASES_DEEP_TECH = [
    "Idea\nsostenible",
    "Reconocimiento\ny evaluación de\nla oportunidad",
    "Constitución\nde la empresa",
    "Escalamiento\nde la empresa",
]
RAMAS_DEEP_TECH = ["Desarrollo del\nproducto", "Financiamiento\nde la empresa"]


def fig_proceso_deep_tech():
    """La cuarta fase son dos actividades a la vez, no dos etapas seguidas."""
    fig, ax = plt.subplots(figsize=(8.4, 3.0))
    ALTO, HUECO = 0.88, 0.44

    # El ancho de cada caja lo fija su línea más larga. Con ancho fijo,
    # «Reconocimiento y evaluación de la oportunidad» desbordaba su caja
    # mientras «Idea sostenible» dejaba dos tercios vacíos.
    def ancho_de(texto):
        return 0.40 + 0.098 * max(len(l) for l in texto.split("\n"))

    a_fases = [ancho_de(t) for t in FASES_DEEP_TECH]
    a_ramas = [ancho_de(t) for t in RAMAS_DEEP_TECH]
    a_rama = max(a_ramas)

    x0 = 0.0
    xs = []
    for k in range(3):                      # las tres primeras fases, en línea
        xs.append(x0)
        x0 += a_fases[k] + HUECO
    x_ramas = x0                            # la cuarta fase, en dos ramas
    x0 += a_rama + HUECO
    x_fin = x0                              # el escalamiento

    Y, DY = 0.0, 0.66

    def caja(x, y, a, alto, texto, color, fs=7.4, negrita=False):
        ax.add_patch(Rectangle((x, y - alto / 2), a, alto, facecolor=color,
                               alpha=0.13, edgecolor=color, linewidth=1.2))
        ax.text(x + a / 2, y, texto, ha="center", va="center", fontsize=fs,
                color=color if negrita else INK, linespacing=1.3,
                fontweight="bold" if negrita else "normal")

    def flecha(p0, p1, color):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=10,
                                     color=color, linewidth=1.2, shrinkA=0, shrinkB=0))

    for k in range(3):
        caja(xs[k], Y, a_fases[k], ALTO, FASES_DEEP_TECH[k], NAVY)
        if k:
            flecha((xs[k - 1] + a_fases[k - 1], Y), (xs[k], Y), MUTED)

    for j, texto in enumerate(RAMAS_DEEP_TECH):
        y = Y + DY * (1 if j == 0 else -1)
        caja(x_ramas, y, a_rama, ALTO * 0.82, texto, ACCENT)
        flecha((xs[2] + a_fases[2], Y), (x_ramas, y), ACCENT)
        flecha((x_ramas + a_rama, y), (x_fin, Y), ACCENT)

    caja(x_fin, Y, a_fases[3], ALTO, FASES_DEEP_TECH[3], OK, negrita=True)

    # La formación técnica del fundador precede a todo el proceso y no es una
    # fase: va como banda superior, que es como la dibuja el artículo.
    ancho_total = x_fin + a_fases[3]
    ax.add_patch(Rectangle((0, DY + 0.62), ancho_total, 0.34, facecolor=MUTED,
                           alpha=0.12, edgecolor=MUTED, linewidth=1.0))
    ax.text(ancho_total / 2, DY + 0.79, "Formación técnica del fundador",
            ha="center", va="center", fontsize=8.0, color=MUTED, fontweight="bold")

    ax.set_xlim(-0.12, ancho_total + 0.12)
    ax.set_ylim(-DY - 0.72, DY + 1.12)
    ax.axis("off")
    escribir(fig, "s2-proceso-deep-tech")


# Nguyen et al. (2024), sección 4.6. Las nueve rondas de financiamiento en
# dólares que el artículo detalla, de cinco de sus seis casos. El sexto caso
# levantó en euros y se deja fuera: mezclar dos monedas en un mismo eje
# obligaría a un tipo de cambio que el artículo no da.
#
# Las empresas van con letra porque el estudio las anonimiza.
#
# El quinto campo es el desplazamiento del rótulo en puntos. Va explícito
# porque la Serie B de la empresa D y la Serie A de la empresa F están a dos
# meses de distancia, y con un desplazamiento común sus rótulos se pisaban.
RONDAS_DEEP_TECH = [
    (2015.70, 2.850, "Empresa E", "ronda inicial", (10, -4), "left", "top"),
    (2016.30, 12.000, "Empresa E", "Serie A", (-8, 10), "right", "bottom"),
    (2017.55, 0.159, "Empresa E", "Serie B", (9, 5), "left", "bottom"),
    (2019.55, 2.200, "Empresa F", "ronda inicial", (9, -4), "left", "top"),
    (2020.30, 12.000, "Empresa B", "expansión", (-9, 10), "right", "bottom"),
    (2021.10, 200.000, "Empresa D", "Serie B", (-7, 9), "right", "bottom"),
    (2021.30, 8.000, "Empresa F", "Serie A", (4, -16), "left", "top"),
    (2021.90, 24.000, "Empresa B", "ronda posterior", (8, -6), "left", "top"),
    (2022.90, 91.000, "Empresa A", "Serie C", (-7, 9), "right", "bottom"),
]


def fig_rondas_deep_tech():
    """El monto de la ronda no crece con su letra: hay tres órdenes de diferencia."""
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    montos = [m for _, m, _, _, _, _, _ in RONDAS_DEEP_TECH]
    mn, mx = min(montos), max(montos)

    for x, m, empresa, ronda, desp, ha, va in RONDAS_DEEP_TECH:
        # El acento marca solo los dos extremos: son los que sostienen el
        # hallazgo. El resto va en azul, que es la segunda tinta validada.
        color = ACCENT if m in (mn, mx) else NAVY
        ax.plot([x], [m], "o", color=color, markersize=7.5, zorder=3)
        ax.annotate(f"{empresa}\n{ronda} · {num(m, 3)}", (x, m),
                    textcoords="offset points", xytext=desp, ha=ha, va=va,
                    fontsize=7.2, color=INK, linespacing=1.35, zorder=3)

    ax.set_yscale("log")
    ax.set_ylim(0.06, 900)
    ax.set_xlim(2014.9, 2024.3)
    ax.set_yticks([0.1, 1, 10, 100])
    ax.set_yticklabels([num(v, 1) for v in (0.1, 1, 10, 100)])
    ax.set_xticks([2015, 2017, 2019, 2021, 2023])
    ax.set_xticklabels(["2015", "2017", "2019", "2021", "2023"])
    # El rótulo del eje va en dos líneas: en una sola, cuarenta y siete
    # caracteres a 8 pt no caben en las 3,2 pulgadas de alto y el recorte
    # automático se los comía por los dos extremos.
    ax.set_ylabel("Monto de la ronda\n(millones de dólares, escala logarítmica)",
                  fontsize=8.0, color=MUTED, linespacing=1.4)
    ax.tick_params(labelsize=8.0, colors=INK, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.6, alpha=0.55)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right"))
    escribir(fig, "s2-rondas-deep-tech")


# Samo y Huda (2019), Journal of Global Entrepreneurship Research 9:12,
# tabla 4. Coeficientes de trayectoria sobre la intención emprendedora
# académica, modelo de ecuaciones estructurales por mínimos cuadrados
# parciales, 310 investigadores jóvenes de más de treinta universidades.
#
# El cuarto campo dice si el coeficiente alcanza significación: el de la
# empresa no la alcanza, y dibujarlo relleno como los otros dos haría que la
# figura afirmara lo contrario de lo que el estudio concluye.
HELICES_AEI = [
    ("Universidad", 0.421, 5.161, "p < 0,001", True),
    ("Estado", 0.232, 2.968, "p = 0,002", True),
    ("Empresa", 0.037, 0.472, "p = 0,318", False),
]
AEI_R2 = 0.412


def fig_helices_intencion():
    """La universidad casi duplica al Estado; la empresa no alcanza significación."""
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    nombres = [n for n, _, _, _, _ in HELICES_AEI][::-1]
    filas = HELICES_AEI[::-1]

    for k, (nombre, beta, t, p, signif) in enumerate(filas):
        if signif:
            ax.barh(k, beta, height=0.58, color=ACCENT if beta > 0.4 else NAVY)
        else:
            # Contorno y sin relleno: la barra hueca es la convención para el
            # coeficiente que no alcanza significación.
            ax.barh(k, beta, height=0.58, facecolor="none", edgecolor=MUTED,
                    linewidth=1.3, linestyle=(0, (3, 2)))
        color = INK if signif else MUTED
        ax.text(beta + 0.012, k + 0.12, num(beta, 3), va="center", ha="left",
                fontsize=9.0, color=color, fontweight="bold")
        ax.text(beta + 0.012, k - 0.16, f"t = {num(t, 2)} · {p}", va="center",
                ha="left", fontsize=7.2, color=MUTED)

    ax.set_yticks(range(len(filas)))
    ax.set_yticklabels(nombres, fontsize=9.0, color=INK)
    ax.set_xlim(0, 0.60)
    ax.set_ylim(-0.7, len(filas) - 0.3)
    ax.set_xlabel(f"Coeficiente de trayectoria sobre la intención de fundar "
                  f"· R² = {num(AEI_R2, 3)}", fontsize=8.2, color=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=7.8, colors=MUTED)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: num(v, 1)))
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s2-helices-intencion")


# Samo y Huda (2019), tabla 1: composición ocupacional de los 310
# investigadores encuestados. El waffle se lee sobre un total contable, que
# es el caso: una casilla es el 1 % de la muestra. Los porcentajes redondeados
# suman 100, y el recuento exacto va en la leyenda para que el redondeo no
# esconda nada.
#
# Las tres primeras categorías usan la rampa ordinal de un solo tono porque
# se ordenan por tamaño; el ámbar y el acento marcan las dos que la lámina
# destaca. Gris y azul juntos no se usan como categorías: el gris es fondo.
OCUPACION_AEI = [
    ("Sin experiencia laboral", 107, 34.5, 35, RAMPA[0]),
    ("Profesional en la universidad", 87, 28.1, 28, RAMPA[1]),
    ("Empleado", 66, 21.3, 21, RAMPA[2]),
    ("Sin cualificación profesional", 31, 10.0, 10, WARN),
    ("Ya emprende", 19, 6.1, 6, ACCENT),
]
OCUPACION_TOTAL = 310


def fig_quien_emprende():
    """Diecinueve de 310 investigadores ya dirigen una empresa."""
    fig, ax = plt.subplots(figsize=(7.4, 3.0))
    LADO, PASO = 0.80, 1.0

    casillas = []
    for _, _, _, cuadros, color in OCUPACION_AEI:
        casillas.extend([color] * cuadros)

    # Se rellena de ARRIBA hacia abajo: con el relleno desde la fila cero,
    # que es la de abajo, el orden visual de las cinco categorías salía al
    # revés que el de la leyenda, y las dos había que leerlas en direcciones
    # opuestas.
    for i, color in enumerate(casillas):
        fila, col = divmod(i, 10)
        ax.add_patch(Rectangle((col * PASO, (9 - fila) * PASO), LADO, LADO,
                               facecolor=color, edgecolor=PAPER, linewidth=0.8))

    # La leyenda va a la derecha, una línea por categoría y con su propio
    # alto: los nombres miden entre ocho y veintinueve caracteres, y con paso
    # constante «Profesional en la universidad» pisaba la línea siguiente.
    x_leyenda = 10 * PASO + 0.6
    for k, (nombre, n, pct, _, color) in enumerate(OCUPACION_AEI):
        y = 9.2 - k * 1.9
        ax.add_patch(Rectangle((x_leyenda, y - 0.34), 0.62, 0.68,
                               facecolor=color, edgecolor="none"))
        ax.text(x_leyenda + 0.86, y + 0.16, nombre, ha="left", va="center",
                fontsize=8.2, color=INK)
        ax.text(x_leyenda + 0.86, y - 0.42, f"{n} de {OCUPACION_TOTAL} · {num(pct, 1)} %",
                ha="left", va="center", fontsize=7.4, color=MUTED)

    ax.text(0, -0.85, f"Una casilla es el 1 % de los {OCUPACION_TOTAL} encuestados",
            ha="left", va="center", fontsize=7.2, color=MUTED)
    # El margen derecho lo fija el nombre más largo de la leyenda, veintinueve
    # caracteres: con el margen ajustado a la caja de color, dos de los cinco
    # nombres se salían del lienzo.
    ax.set_xlim(-0.25, x_leyenda + 9.6)
    ax.set_ylim(-1.35, 10.2)
    ax.set_aspect("equal")
    ax.axis("off")
    escribir(fig, "s2-quien-emprende")


FIGURAS += [fig_conversion_investigacion, fig_figuras_salida,
            fig_titularidad_cadena, fig_reloj_patente, fig_obstaculos_salida,
            fig_deep_tech_frente_digital, fig_proceso_deep_tech,
            fig_rondas_deep_tech, fig_helices_intencion, fig_quien_emprende]


# ==========================================================================
# SESIÓN 2 · Tema 02 — transferencia tecnológica
# ==========================================================================

# Odei y Novák (2022), Tabla 2. Medias por institución de las 164 universidades
# del Reino Unido que respondieron el Higher Education Business and Community
# Interaction Survey (HE-BCI) del curso 2017/18.
#
# Son CONTEOS anuales por institución, no porcentajes: la tabla los declara con
# N = 164, mínimo 0 y máximo 394. El texto del apartado 4 del artículo escribe
# «26.72 %» y «12.91 %», que es un error de redacción del propio artículo.
EMBUDO_PATENTES = [
    ("Divulgaciones de invención", 26.72),
    ("Solicitudes de patente del año", 12.91),
    ("Patentes concedidas en el año", 10.41),
    ("Spin-offs con participación", 5.57),
]


def fig_embudo_patentes():
    """De veintisiete divulgaciones por universidad salen 5,6 spin-offs al año."""
    # Etapas ordenadas, así que rampa de un solo tono y no tintas categóricas.
    # El último escalón lleva el acento porque es el que la lámina destaca.
    #
    # El nombre de la etapa va FUERA del embudo, como rótulo del eje. Dentro se
    # salía de los escalones estrechos: «Solicitudes de patente del año» mide 30
    # caracteres y su escalón son 48 de las 100 unidades del primero, así que el
    # rótulo se partía a mitad de palabra y cambiaba de color en el corte. Es el
    # mismo fallo que apareció tres veces en la sesión 1 (METODOLOGIA.md §17.16),
    # y aquí se comprobó en captura antes de dar la figura por buena.
    base = EMBUDO_PATENTES[0][1]
    colores = [RAMPA[0], RAMPA[1], RAMPA[2], ACCENT]
    nombres = [n for n, _ in EMBUDO_PATENTES][::-1]

    fig, ax = plt.subplots(figsize=(6.8, 2.9))
    for i, ((_, v), color) in enumerate(zip(EMBUDO_PATENTES, colores)):
        y = len(EMBUDO_PATENTES) - i - 1
        ancho = v / base * 100
        ax.barh(y, ancho, height=0.64, color=color, left=(100 - ancho) / 2)
        ax.text(106, y, f"{num(v, 2)}   ·   {num(v / base * 100, 0)} %",
                ha="left", va="center", fontsize=8.4, color=INK)

    ax.text(106, len(EMBUDO_PATENTES) - 0.52, "media por universidad",
            ha="left", va="center", fontsize=7.2, color=MUTED)
    ax.set_yticks(range(len(nombres)))
    ax.set_yticklabels(nombres, fontsize=8.4, color=INK)
    ax.set_xlim(-4, 152)
    ax.set_ylim(-0.72, len(EMBUDO_PATENTES) - 0.16)
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s2-embudo-patentes")


# Odei y Novák (2022), Tabla 4. Modelo de ecuaciones estructurales por mínimos
# cuadrados parciales (PLS-SEM) sobre las mismas 164 universidades. Coeficiente
# de trayectoria original y tamaño de efecto f² de Cohen.
#
# Las dos magnitudes son adimensionales y viven en el mismo intervalo, así que
# comparten un solo eje: aquí no hay doble escala, que es lo que la norma
# prohíbe. Sin ese detalle habría que dibujarlas en dos figuras.
TRAYECTORIAS_SPINOFF = [
    ("Patente → spin-off", 0.593, 0.724),
    ("Financiamiento → patente", 0.593, 0.553),
    ("Financiamiento → spin-off", 0.299, 0.186),
    ("Recompensas → patente", 0.101, 0.016),
    ("Recompensas → spin-off", 0.095, 0.029),
]
R2_SPINOFF, R2_PATENTE = 0.70, 0.38


def fig_coeficientes_spinoff():
    """La patente tiene el mayor tamaño de efecto sobre la creación de spin-offs."""
    nombres = [n for n, _, _ in TRAYECTORIAS_SPINOFF][::-1]
    betas = [b for _, b, _ in TRAYECTORIAS_SPINOFF][::-1]
    efectos = [f for _, _, f in TRAYECTORIAS_SPINOFF][::-1]
    ys = np.arange(len(nombres))
    alto = 0.34

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    b1 = ax.barh(ys + alto / 2, betas, height=alto, color=NAVY,
                 label="Coeficiente de trayectoria")
    b2 = ax.barh(ys - alto / 2, efectos, height=alto, color=ACCENT,
                 label="Tamaño de efecto f²")
    for barras, valores in ((b1, betas), (b2, efectos)):
        for b, v in zip(barras, valores):
            ax.text(v + 0.014, b.get_y() + b.get_height() / 2, num(v, 3),
                    va="center", ha="left", fontsize=7.8, color=INK)

    ax.set_yticks(ys)
    ax.set_yticklabels(nombres, fontsize=8.4, color=INK)
    ax.set_xlim(0, 0.88)
    ax.set_xlabel("Valor adimensional · las dos magnitudes comparten escala",
                  fontsize=8.2, color=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=7.8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    # La leyenda va abajo a la derecha, que es la esquina libre: las dos
    # trayectorias de recompensas son las últimas y no llegan a 0,11.
    ax.legend(loc="lower right", fontsize=8.0, frameon=False, labelcolor=INK)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s2-coeficientes-spinoff")


# Hunady et al. (2019), Tabla 2. Registro Europeo de Educación Terciaria (ETER):
# 2 465 instituciones de 36 países europeos, cursos 2011/12 a 2014/15.
#
# Panel izquierdo: modelo (4), probit sobre la muestra completa de 2 185
# observaciones, con el índice Herfindahl de especialización doctoral y su
# cuadrado. Panel derecho: modelo (2), logit sobre 1 247 observaciones, con la
# intensidad de matrícula doctoral y su cuadrado.
#
# No se usa el modelo (3): su tabla repite los valores 65,81 y −2 301,3 en dos
# filas distintas, que es un error de composición del artículo.
#
# Lo que se dibuja es la FUNCIÓN AJUSTADA que publica el estudio, no puntos
# observados, y el eje lo declara: un eje sin unidad ni procedencia es una
# interpretación dibujada como si fuera un dato (METODOLOGIA.md §17.15).
HERFINDAHL_B1, HERFINDAHL_B2, HERFINDAHL_N = -8.51, 6.09, 2185
DOCTORADO_B1, DOCTORADO_B2, DOCTORADO_N = 151.63, -5357.7, 1247


def fig_no_linealidad_spinoff():
    """La especialización toca su mínimo en 0,70; la matrícula doctoral su máximo en 1,4 %."""
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.2, 2.7))

    # Panel izquierdo: relación en U.
    h = np.linspace(0, 1, 240)
    yh = HERFINDAHL_B1 * h + HERFINDAHL_B2 * h ** 2
    h_v = -HERFINDAHL_B1 / (2 * HERFINDAHL_B2)
    y_v = HERFINDAHL_B1 * h_v + HERFINDAHL_B2 * h_v ** 2
    izq.plot(h, yh, color=NAVY, linewidth=2.2)
    izq.axvline(h_v, color=GRID, linewidth=1.0, linestyle=(0, (3, 3)))
    izq.plot([h_v], [y_v], "o", color=ACCENT, markersize=6.5, zorder=3)
    # `num` quita el cero final y «mínimo en 0,7» contradiría al titular de la
    # lámina, que dice 0,70. Aquí el cero es significativo: se formatea a mano.
    # La llamada va hacia la izquierda y abajo, que es la zona vacía del panel:
    # hacia la derecha se salía del eje.
    izq.annotate(f"mínimo en {h_v:.2f}".replace(".", ","), xy=(h_v, y_v),
                 textcoords="offset points", xytext=(-8, -13), ha="right",
                 va="center", fontsize=7.6, color=ACCENT)
    izq.set_title(f"Especialización doctoral · n = {num(HERFINDAHL_N, 0)}",
                  fontsize=8.4, color=INK, pad=6)
    izq.set_xlabel("Índice Herfindahl, de 0 a 1", fontsize=7.8, color=MUTED)
    # Cada panel rotula SU propio índice. Los dos ejes miden el aporte al índice
    # latente, pero uno es probit y el otro logit: un rótulo compartido haría
    # creer que las dos escalas son la misma.
    izq.set_ylabel("Aporte al índice probit", fontsize=7.8, color=MUTED)
    izq.set_xlim(0, 1)
    izq.set_ylim(-3.7, 0.9)

    # Panel derecho: relación en U invertida. Se dibuja en porcentaje de
    # matrícula, que es como la lámina enuncia el óptimo.
    x = np.linspace(0, 0.035, 240)
    yx = DOCTORADO_B1 * x + DOCTORADO_B2 * x ** 2
    x_v = -DOCTORADO_B1 / (2 * DOCTORADO_B2)
    y_v2 = DOCTORADO_B1 * x_v + DOCTORADO_B2 * x_v ** 2
    der.plot(x * 100, yx, color=NAVY, linewidth=2.2)
    der.axvline(x_v * 100, color=GRID, linewidth=1.0, linestyle=(0, (3, 3)))
    der.plot([x_v * 100], [y_v2], "o", color=ACCENT, markersize=6.5, zorder=3)
    der.annotate(f"máximo en {num(x_v * 100, 1)} %", xy=(x_v * 100, y_v2),
                 textcoords="offset points", xytext=(9, 4), ha="left",
                 va="center", fontsize=7.6, color=ACCENT)
    der.set_title(f"Intensidad doctoral · n = {num(DOCTORADO_N, 0)}",
                  fontsize=8.4, color=INK, pad=6)
    der.set_xlabel("Doctorandos sobre el total de matrícula (%)",
                   fontsize=7.8, color=MUTED)
    der.set_ylabel("Aporte al índice logit", fontsize=7.8, color=MUTED)
    der.set_xlim(0, 3.5)
    der.set_ylim(-1.9, 1.7)

    for ax in (izq, der):
        ax.axhline(0, color=GRID, linewidth=0.8)
        ax.tick_params(labelsize=7.4, colors=MUTED)
        ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.55)
        ax.set_axisbelow(True)
        limpiar_ejes(ax)
    fig.subplots_adjust(wspace=0.28)
    escribir(fig, "s2-no-linealidad-spinoff")


# O’Dwyer et al. (2022), Tabla 6. Consorcio farmacéutico irlandés, 18 miembros
# fundadores entrevistados: 7 académicos y 11 de empresa, de 5 universidades y 9
# multinacionales. Fases: embrionaria (antes del año 1), inicio (años 1 a 3) y
# compromiso (años 4 a 7).
#
# La intensidad es la que declaran los autores en su propia tabla: «strong», sin
# calificar, y «moderate». Se codifica en ese orden, 3-2-1, y CADA CELDA LLEVA
# ESCRITO EL NIVEL, para que el color no sea la única información. El 0 significa
# que la barrera no figura en esa fase.
BARRERAS_FASES = [
    ("Percepción de escaso valor", [3, 2, 1]),
    ("Falta de confianza", [3, 1, 0]),
    ("Temor a la fuga de conocimiento", [3, 3, 1]),
    ("Renuencia a compartir recursos", [3, 2, 0]),
    ("Sin acuerdo de propiedad intelectual", [0, 2, 0]),
]
FASES_UIC = ["Fase 1 · embrionaria\nantes del año 1",
             "Fase 2 · inicio\naños 1 a 3",
             "Fase 3 · compromiso\naños 4 a 7"]
NIVEL_UIC = {3: ("fuerte", RAMPA[2]), 2: ("declarada", RAMPA[1]),
             1: ("moderada", RAMPA[0]), 0: ("—", SURFACE)}


def fig_barreras_intensidad():
    """Cuatro barreras bajan de fuerte a moderada; solo la de propiedad intelectual se cierra."""
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    for r, (_, niveles) in enumerate(BARRERAS_FASES):
        y = len(BARRERAS_FASES) - r - 1
        for c, nivel in enumerate(niveles):
            texto, color = NIVEL_UIC[nivel]
            ax.add_patch(Rectangle((c + 0.04, y - 0.40), 0.92, 0.80,
                                   facecolor=color, edgecolor=PAPER, linewidth=1.6))
            ax.text(c + 0.5, y, texto, ha="center", va="center", fontsize=8.0,
                    color=PAPER if nivel >= 2 else INK)

    ax.set_xlim(0, 3)
    ax.set_ylim(-0.6, len(BARRERAS_FASES) - 0.4)
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(FASES_UIC, fontsize=7.4, color=INK)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.set_yticks(range(len(BARRERAS_FASES)))
    ax.set_yticklabels([n for n, _ in BARRERAS_FASES][::-1], fontsize=8.2, color=INK)
    ax.tick_params(length=0)
    for lado in ("top", "right", "bottom", "left"):
        ax.spines[lado].set_visible(False)
    escribir(fig, "s2-barreras-intensidad")


# O’Dwyer et al. (2022), Tabla 6. Recuento de los facilitadores que la tabla
# declara en cada fase, separados por el par de relación en que aparecen. La
# cuenta se hizo entrada por entrada sobre la tabla publicada.
FACILITADORES_FASES = [
    ("Fase 1\nembrionaria", 3, 1, 3),
    ("Fase 2\ninicio", 4, 3, 4),
    ("Fase 3\ncompromiso", 7, 4, 6),
]
# Tres categorías, y son categorías sin orden. No pueden ir gris y azul juntos:
# como serie categórica el par falla el suelo de visión normal con ΔE 12,9. Se
# usan las dos tintas validadas más el verde, que el mazo ya emplea como tercera
# marca en la matriz de proyecto.
PARES_UIC = [("Industria y universidad", ACCENT),
             ("Industria e industria", NAVY),
             ("Universidad y universidad", OK)]


def fig_facilitadores_fase():
    """Los facilitadores declarados pasan de siete a diecisiete entre la primera fase y la tercera."""
    nombres = [n for n, _, _, _ in FACILITADORES_FASES]
    series = list(zip(*[(a, b, c) for _, a, b, c in FACILITADORES_FASES]))

    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    base = np.zeros(len(nombres))
    for (etiqueta, color), valores in zip(PARES_UIC, series):
        ax.bar(nombres, valores, width=0.56, bottom=base, color=color, label=etiqueta)
        for k, (v, b) in enumerate(zip(valores, base)):
            ax.text(k, b + v / 2, str(v), ha="center", va="center",
                    fontsize=7.4, color=PAPER)
        base = base + np.array(valores)
    for k, total in enumerate(base):
        ax.text(k, total + 0.45, f"{int(total)} facilitadores", ha="center",
                va="bottom", fontsize=8.4, color=INK, fontweight="bold")

    ax.set_ylim(0, 21)
    # Los facilitadores se cuentan de uno en uno: una marca de eje en 2,5
    # facilitadores no tiene referente.
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_ylabel("Facilitadores declarados", fontsize=8.2, color=MUTED)
    ax.tick_params(axis="x", labelsize=8.0, colors=INK, length=0)
    ax.tick_params(axis="y", labelsize=7.8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    # La leyenda baja a -0,22 y no a -0,09: los rótulos del eje van a dos líneas
    # y a la altura anterior la leyenda se montaba sobre la segunda.
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=7.6,
              frameon=False, labelcolor=INK, ncol=3, handletextpad=0.35,
              columnspacing=1.1)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s2-facilitadores-fase")


# O’Dwyer et al. (2022), apartados 3 y 5.4. Financiamiento del consorcio
# farmacéutico irlandés: 7,7 M€ del gobierno irlandés en la fundación y 40 M€
# adicionales a los cinco años, de los que 30 son del gobierno y 10 de los socios
# industriales. El artículo declara un presupuesto total de 61 M€.
#
# 7,7 + 30 + 10 = 47,7, y el total declarado es 61: la fuente NO desagrega los
# 13,3 M€ restantes. El tramo va con la tinta de aviso y con su nombre escrito,
# porque declarar el hueco es información y callarlo, no (METODOLOGIA.md §4.2.1).
CASCADA_SSPC = [
    ("Fondo\nfundacional", 7.7, ACCENT),
    ("Gobierno\nirlandés", 30.0, NAVY),
    ("Socios\nindustriales", 10.0, NAVY),
    ("Sin desagregar\nen la fuente", 13.3, WARN),
    ("Presupuesto\ntotal", 61.0, OK),
]


def fig_cascada_sspc():
    """Del fondo fundacional de 7,7 millones al presupuesto declarado de 61."""
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    acum = 0.0
    for i, (nombre, v, color) in enumerate(CASCADA_SSPC):
        if i == 0 or i == len(CASCADA_SSPC) - 1:
            ax.bar(i, v, width=0.62, color=color)
            ax.text(i, v + 1.6, f"{num(v, 1)} M€", ha="center", va="bottom",
                    fontsize=9, color=color, fontweight="bold")
            if i == 0:
                acum = v
        else:
            ax.bar(i, v, bottom=acum, width=0.62, color=color)
            ax.text(i, acum + v / 2, f"+{num(v, 1)}", ha="center", va="center",
                    fontsize=8.5, color=PAPER)
            acum += v

    ax.set_xticks(range(len(CASCADA_SSPC)))
    ax.set_xticklabels([n for n, _, _ in CASCADA_SSPC], fontsize=8, color=INK)
    # Rótulo corto a propósito: a 2,8 pulgadas de alto, un rótulo de eje de más
    # de treinta caracteres se recorta por los dos extremos.
    ax.set_ylabel("Millones de euros acumulados", fontsize=8.4, color=MUTED)
    ax.set_ylim(0, 72)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s2-cascada-sspc")


# Peña y Jenik (2023), BID, resumen ejecutivo, mapa del ecosistema regional, con
# análisis de Surfing Tsunamis. Empresas de deep tech con financiamiento
# institucional en América Latina y el Caribe en 2023: 340 en catorce países.
#
# El mapa nombra los países con cinco empresas o más y otros seis con cuatro o
# menos. Esos seis se agrupan en una barra y su suma cierra el total: 330 + 10 =
# 340. Agruparlos evita inventar el nombre del decimocuarto, que el mapa no deja
# leer.
DEEPTECH_PAISES = [
    ("Argentina", 103), ("Brasil", 101), ("Chile", 65), ("México", 30),
    ("Uruguay", 11), ("Colombia", 9), ("Costa Rica", 6), ("Perú", 5),
    ("Otros seis países", 10),
]
DEEPTECH_TOTAL = 340


def fig_deeptech_paises():
    """Argentina, Brasil y Chile reúnen el 79 % de las empresas; el Perú, el 1 %."""
    nombres = [n for n, _ in DEEPTECH_PAISES][::-1]
    valores = [v for _, v in DEEPTECH_PAISES][::-1]
    colores = [ACCENT if n == "Perú" else NAVY for n in nombres]

    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    barras = ax.barh(nombres, valores, color=colores, height=0.66)
    for b, v in zip(barras, valores):
        ax.text(v + 2.2, b.get_y() + b.get_height() / 2,
                f"{v}   ({num(v / DEEPTECH_TOTAL * 100, 0)} %)",
                va="center", ha="left", fontsize=8.4, color=INK)

    ax.set_xlim(0, 132)
    ax.set_xlabel(f"Empresas de deep tech, de {DEEPTECH_TOTAL} en la región, 2023",
                  fontsize=8.2, color=MUTED)
    ax.tick_params(axis="y", labelsize=8.6, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=7.8, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s2-deeptech-paises")


# Peña y Jenik (2023), BID, resumen ejecutivo. Reparto de las 340 empresas de
# deep tech de la región por sector tecnológico, en porcentaje del total, 2023.
#
# Las siete últimas categorías del informe (robótica 2 %, manufactura avanzada
# 2 %, healthtech 2 %, materiales avanzados 1 %, y conectividad avanzada,
# dispositivos médicos y blockchain por debajo del 1 % cada una) suman 9 % y van
# agrupadas: siete bandas de dos puntos no se leen proyectadas.
DEEPTECH_SECTORES = [
    ("Biotecnología", 61), ("Inteligencia artificial", 11),
    ("Nanotecnología", 6), ("Tecnologías limpias", 5),
    ("Espacio", 4), ("Movilidad avanzada", 4),
    ("Otras siete tecnologías", 9),
]


def fig_deeptech_sectores():
    """La biotecnología sola reúne el 61 % de las empresas de deep tech de la región."""
    # Los rótulos van FUERA de los bloques pequeños: dentro se recortan al
    # componer la lámina en dos columnas.
    total = sum(v for _, v in DEEPTECH_SECTORES)
    fig, ax = plt.subplots(figsize=(7.2, 3.1))

    nombre_g, valor_g = DEEPTECH_SECTORES[0]
    w1 = 0.36
    ax.add_patch(Rectangle((0, 0), w1, 1, facecolor=ACCENT, edgecolor=PAPER,
                           linewidth=2))
    ax.text(w1 / 2, 0.56, nombre_g, ha="center", va="center", fontsize=10.5,
            color=PAPER, fontweight="bold")
    ax.text(w1 / 2, 0.43, f"{valor_g} %", ha="center", va="center", fontsize=15,
            color=PAPER, fontweight="bold")
    ax.text(w1 / 2, 0.33, "de las 340 empresas", ha="center", va="center",
            fontsize=8, color=PAPER)

    resto = DEEPTECH_SECTORES[1:]
    suma = sum(v for _, v in resto)
    y = 1.0
    for k, (nombre, v) in enumerate(resto):
        h = (v / suma) * 1.0
        # Las dos tintas de la pila alternan para separar bloques contiguos, no
        # para codificar dos categorías: son dos valores del mismo azul y la
        # información la lleva el rótulo, que va escrito al lado de cada bloque.
        ax.add_patch(Rectangle((w1 + 0.03, y - h + 0.012), 0.11, h - 0.024,
                               facecolor=NAVY if k % 2 == 0 else RAMPA[0],
                               edgecolor="none"))
        ax.text(w1 + 0.19, y - h / 2, nombre, ha="left", va="center",
                fontsize=8.2, color=INK)
        # La cifra se coloca contra el ancho real del rótulo y no contra un
        # canto fijo: «Inteligencia artificial» mide el doble que «Espacio» y
        # con paso constante la cifra se le monta encima.
        ax.text(w1 + 0.215 + 0.0135 * len(nombre), y - h / 2, f"{v} %",
                ha="left", va="center", fontsize=8.2, color=INK,
                fontweight="bold")
        y -= h

    ax.set_xlim(-0.01, 1.03)
    ax.set_ylim(-0.02, 1.02)
    ax.axis("off")
    escribir(fig, "s2-deeptech-sectores")


# Peña y Jenik (2023), BID, resumen ejecutivo y capítulo 4. Personas dedicadas a
# I+D en ciencia, tecnología, ingeniería y matemáticas en América Latina y el
# Caribe, personas de I+D dentro de las empresas de deep tech de la región, y
# personas que exigiría el escenario de crecimiento de cien veces que el propio
# informe analiza.
#
# El resumen numérico cifra el acervo en 871 000 y el panel del escenario de cien
# veces escribe 865 000 para el mismo concepto. Se toma la cifra del resumen y se
# declara aquí la discrepancia, que es del 0,7 %.
TALENTO_ACERVO = 871000
TALENTO_HOY = 5000
TALENTO_ESCENARIO = 500000


def fig_talento_deeptech():
    """Cinco mil personas de I+D en las empresas frente a 871 000 en la región."""
    # Forma de bala: avance contra una meta. La barra de 5 000 sobre un carril de
    # 871 000 es una línea de un píxel, y eso ES el hallazgo, así que lleva
    # llamada con guía en vez de rótulo pegado.
    fig, ax = plt.subplots(figsize=(6.6, 1.5))
    ax.barh(0, TALENTO_ACERVO, height=0.44, color=SURFACE, edgecolor=GRID,
            linewidth=0.8)
    ax.barh(0, TALENTO_HOY, height=0.44, color=ACCENT)
    ax.vlines(TALENTO_ESCENARIO, -0.36, 0.36, color=NAVY, linewidth=2.4)

    ax.annotate(f"{num(TALENTO_HOY, 0)} personas de I+D hoy",
                xy=(TALENTO_HOY, 0.14), xytext=(72000, 0.66),
                fontsize=8.2, color=ACCENT, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=ACCENT, linewidth=0.9))
    ax.text(TALENTO_ESCENARIO, -0.46,
            f"escenario de cien veces: {num(TALENTO_ESCENARIO, 0)}",
            ha="center", va="top", fontsize=8.0, color=NAVY)
    ax.text(TALENTO_ACERVO, 0.50,
            f"acervo de I+D en la región: {num(TALENTO_ACERVO, 0)}",
            ha="right", va="bottom", fontsize=8.0, color=MUTED)

    ax.set_xlim(0, TALENTO_ACERVO * 1.02)
    ax.set_ylim(-0.98, 0.98)
    ax.set_xticks([])
    ax.set_yticks([])
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s2-talento-deeptech")


# Correspondencia entre la condición de un resultado y la ventanilla que le
# toca. Es una clasificación de elaboración propia, y así se rotula en la
# lámina: no hay dato externo que citar, y los organismos que aparecen en cada
# cuadrante sí están citados al pie (INDECOPI, OMPI, ProInnóvate, PROCIENCIA).
MATRIZ_TRANSFERENCIA = [
    (0.25, 0.75, "Licencia abierta",
     "Protección concedida,\nsin receptor · PCT de la OMPI", NAVY),
    (0.75, 0.75, "Licencia o spin-off",
     "Protección y receptor\nidentificados · ProInnóvate", OK),
    (0.25, 0.25, "Registro y búsqueda de demanda",
     "Sin protección ni receptor\n· INDECOPI y PROCIENCIA", ACCENT),
    (0.75, 0.25, "Registro antes de divulgar",
     "Receptor sin protección\n· INDECOPI", WARN),
]


def fig_matriz_transferencia():
    """Las dos preguntas que deciden la ventanilla: protección registrada y socio receptor."""
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    for x, y, titulo, sub, color in MATRIZ_TRANSFERENCIA:
        ax.add_patch(Rectangle((x - 0.25, y - 0.25), 0.5, 0.5, facecolor=color,
                               alpha=0.13, edgecolor=PAPER, linewidth=3))
        ax.text(x, y + 0.10, titulo, ha="center", va="center", fontsize=9.2,
                color=color, fontweight="bold")
        ax.text(x, y - 0.10, sub, ha="center", va="center", fontsize=7.4,
                color=MUTED)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("¿Hay un socio receptor identificado?  →", fontsize=8.5, color=INK)
    # El rótulo vertical va corto: a tres pulgadas de alto, la pregunta completa
    # se recortaba por los dos extremos.
    ax.set_ylabel("¿Hay protección registrada?  →", fontsize=8.5, color=INK)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRID)
    escribir(fig, "s2-matriz-transferencia")


FIGURAS += [fig_embudo_patentes, fig_coeficientes_spinoff,
            fig_no_linealidad_spinoff, fig_barreras_intensidad,
            fig_facilitadores_fase, fig_cascada_sspc, fig_deeptech_paises,
            fig_deeptech_sectores, fig_talento_deeptech,
            fig_matriz_transferencia]


# ==========================================================================
# SESIÓN 2 · las cinco láminas que pasaron de texto seguido a figura
# ==========================================================================

# Peña y Jenik (2023), BID: Establishment Labs sostiene su valorización sobre 25
# familias de patentes y 200 solicitudes presentadas en 25 jurisdicciones. Ese es
# el tercer peldaño y el único publicado. El primero es la consecuencia de
# registrar en un solo país y el segundo es el criterio de cobertura de la
# lámina, tres países de mercado y dos de fabricación posible: los dos llevan
# escrita su procedencia debajo del peldaño, para que el dato medido y el
# criterio no se lean como la misma cosa (METODOLOGIA.md §17.15).
COBERTURA_JURISDICCIONES = [
    (1, "1 jurisdicción", "el competidor fabrica\nen todas las demás",
     "consecuencia de registrar en un solo país", ACCENT),
    (5, "5 jurisdicciones", "tres de mercado y\ndos de fabricación",
     "criterio de cobertura", NAVY),
    (25, "25 jurisdicciones", "200 solicitudes\nen 25 familias",
     "cartera publicada, 2023", OK),
]
# Ancho de un carácter, en pulgadas, para los dos cuerpos que la figura usa: la
# familia monoespaciada avanza 0,6 em por carácter. Con esta medida el ancho de
# cada peldaño se calcula en vez de estimarse.
CH_9, CH_74 = 0.075, 0.062


def fig_escalera_jurisdicciones():
    """De registrar en un país a cubrir veinticinco jurisdicciones."""
    # El peldaño mide lo que mide su rótulo más largo, y la unidad del eje es la
    # pulgada: así el ancho de la figura sale de los rótulos y no al revés. Con
    # paso constante, el detalle del tercer peldaño se salía del lienzo.
    anchos = [max(len(t) * CH_9, max(len(l) for l in d.split("\n")) * CH_74) + 0.34
              for _, t, d, _, _ in COBERTURA_JURISDICCIONES]
    xs, x = [], 0.0
    for a in anchos:
        xs.append(x)
        x += a

    fig, ax = plt.subplots(figsize=(x / 0.775, 2.6))
    for k, ((_, titulo, detalle, marca, color), x0, a) in enumerate(
            zip(COBERTURA_JURISDICCIONES, xs, anchos)):
        ax.plot([x0, x0 + a], [k, k], color=color, linewidth=3.4,
                solid_capstyle="butt", zorder=3)
        if k:
            ax.vlines(x0, k - 1, k, color=GRID, linewidth=1.2, zorder=2)
        # Los dos rótulos crecen HACIA ARRIBA desde el peldaño. Con el detalle
        # anclado por su primera línea, la segunda caía sobre el propio peldaño.
        ax.text(x0 + 0.06, k + 0.76, titulo, ha="left", va="center", fontsize=9.0,
                color=color, fontweight="bold")
        ax.text(x0 + 0.06, k + 0.15, detalle, ha="left", va="bottom", fontsize=7.4,
                color=INK, linespacing=1.35)
        # La marca de procedencia va DEBAJO del peldaño: ahí no hay peldaño ni
        # contrapeldaño que la corte y puede ser más larga que su propio escalón.
        ax.text(x0 + 0.06, k - 0.26, marca, ha="left", va="center", fontsize=6.8,
                color=MUTED)

    ax.text(0, -0.86, "cobertura territorial de la cartera  →", ha="left",
            va="center", fontsize=7.4, color=MUTED)
    ax.set_xlim(-0.06, x)
    ax.set_ylim(-1.06, 3.12)
    ax.axis("off")
    escribir(fig, "s2-escalera-jurisdicciones")


# Samo y Huda (2019): el modelo de ecuaciones estructurales explica el 41,2 % de
# la varianza de la intención emprendedora académica de 310 investigadores
# jóvenes. El 58,8 % restante corresponde a variables que el estudio no incluyó,
# y son los propios autores quienes lo declaran.
#
# Anillo de dos partes, que es el único reparto que un sector admite sin
# volverse ilegible a distancia (METODOLOGIA.md §12). El hueco central lleva la
# cifra, así que la lámina ya no necesita la fila de cifra destacada.
VARIANZA_INTENCION = 41.2
VARIANZA_MUESTRA = 310


def fig_varianza_intencion():
    """El modelo explica el 41,2 % de la varianza y declara el resto sin explicar."""
    fig, ax = plt.subplots(figsize=(6.4, 2.5))
    ax.pie([VARIANZA_INTENCION, 100 - VARIANZA_INTENCION],
           startangle=90, counterclock=False,
           colors=[ACCENT, SURFACE],
           wedgeprops=dict(width=0.34, edgecolor=PAPER, linewidth=1.6))

    ax.text(0, 0.10, f"{num(VARIANZA_INTENCION, 1)} %", ha="center", va="center",
            fontsize=16, color=ACCENT, fontweight="bold")
    ax.text(0, -0.16, "varianza\nexplicada", ha="center", va="center",
            fontsize=7.6, color=MUTED, linespacing=1.3)

    # La leyenda va a la derecha, con el rótulo encima de su glosa: en una sola
    # línea, la glosa de cincuenta caracteres se montaba sobre el rótulo.
    leyenda = [
        (ACCENT, f"{num(VARIANZA_INTENCION, 1)} % explicado",
         "apoyo de la universidad, del Estado y de la empresa"),
        (SURFACE, f"{num(100 - VARIANZA_INTENCION, 1)} % sin explicar",
         "variables que el estudio no incluyó"),
    ]
    for k, (color, titulo, detalle) in enumerate(leyenda):
        y = 0.42 - k * 0.62
        ax.add_patch(Rectangle((1.30, y - 0.055), 0.11, 0.11, facecolor=color,
                               edgecolor=GRID if color == SURFACE else "none",
                               linewidth=0.8))
        ax.text(1.52, y + 0.10, titulo, ha="left", va="center", fontsize=8.6,
                color=INK, fontweight="bold")
        ax.text(1.52, y - 0.11, detalle, ha="left", va="center", fontsize=7.4,
                color=MUTED)

    ax.text(1.30, -0.88,
            f"modelo de ecuaciones estructurales sobre {VARIANZA_MUESTRA} "
            "investigadores jóvenes, 2019",
            ha="left", va="center", fontsize=7.0, color=MUTED)
    ax.set_xlim(-1.15, 4.55)
    ax.set_ylim(-1.05, 1.15)
    ax.set_aspect("equal")
    escribir(fig, "s2-varianza-intencion")


# Odei y Novák (2022) y O’Dwyer et al. (2022): reparto de las ocho tareas de la
# transferencia entre el grupo de investigación y la oficina. Las cuatro de cada
# lado son las que enumera la lámina; la flecha es la dependencia que enuncia su
# conclusión, y las dos cajas que participan en ella van con relleno y filo más
# marcados para que se reconozcan sin leer la flecha.
TAREAS_GRUPO = [
    "Ensayo documentado que\nacredita la madurez",
    "Descripción técnica que\nsostiene la reivindicación",
    "Compromiso de dedicación\nde quien va a fundar",
    "Relación con el socio receptor\nantes del contrato",
]
TAREAS_OFICINA = [
    "Decisión de proteger y\ntrámite del registro",
    "Búsqueda del receptor y\nnegociación del contrato",
    "Reparto de regalías entre\ninstitución y autores",
    "Elección entre licencia\ny spin-off",
]
REQUISITOS_PREVIOS = 2


def fig_reparto_transferencia():
    """Las dos primeras tareas del grupo son requisito de las dos primeras de la oficina."""
    fig, ax = plt.subplots(figsize=(7.8, 3.2))
    ANCHO, HUECO, GAP = 3.05, 1.55, 0.16

    def _alto(texto):
        # El alto sale del número de líneas del propio rótulo. Con alto fijo, una
        # entrada de tres líneas se sale de su caja y pisa la siguiente.
        return 0.34 + 0.30 * (texto.count("\n") + 1)

    def _columna(x0, tareas, color, titulo):
        y, cajas = 0.0, []
        for k, texto in enumerate(tareas):
            alto = _alto(texto)
            previa = k < REQUISITOS_PREVIOS
            ax.add_patch(Rectangle((x0, y - alto), ANCHO, alto, facecolor=color,
                                   alpha=0.20 if previa else 0.08,
                                   edgecolor=color, linewidth=1.8 if previa else 0.9))
            ax.text(x0 + ANCHO / 2, y - alto / 2, texto, ha="center", va="center",
                    fontsize=7.4, color=INK, linespacing=1.25)
            cajas.append((y, y - alto))
            y -= alto + GAP
        ax.text(x0 + ANCHO / 2, 0.20, titulo, ha="center", va="bottom",
                fontsize=8.6, color=color, fontweight="bold")
        return cajas, y

    izq, fin_i = _columna(0.0, TAREAS_GRUPO, ACCENT,
                          f"Grupo de investigación · {len(TAREAS_GRUPO)} tareas")
    der, fin_d = _columna(ANCHO + HUECO, TAREAS_OFICINA, NAVY,
                          f"Oficina de transferencia · {len(TAREAS_OFICINA)} tareas")

    # Una sola flecha entre los dos pares de cajas, y no dos flechas cruzadas: el
    # artículo declara los dos primeros elementos como requisito del par de
    # enfrente, sin emparejarlos uno a uno.
    y_i = (izq[0][0] + izq[REQUISITOS_PREVIOS - 1][1]) / 2
    y_d = (der[0][0] + der[REQUISITOS_PREVIOS - 1][1]) / 2
    ax.add_patch(FancyArrowPatch((ANCHO + 0.10, y_i), (ANCHO + HUECO - 0.10, y_d),
                                 arrowstyle="-|>", mutation_scale=11, color=MUTED,
                                 linewidth=1.4, shrinkA=0, shrinkB=0))
    ax.text(ANCHO + HUECO / 2, y_i + 0.22, "requisito", ha="center", va="bottom",
            fontsize=7.6, color=MUTED, fontweight="bold")
    ax.text(ANCHO + HUECO / 2, y_i - 0.30, "sin esto no\nhay expediente",
            ha="center", va="top", fontsize=6.9, color=MUTED, linespacing=1.25)

    ax.set_xlim(-0.10, 2 * ANCHO + HUECO + 0.10)
    ax.set_ylim(min(fin_i, fin_d) + GAP - 0.10, 0.62)
    ax.axis("off")
    escribir(fig, "s2-reparto-transferencia")


# O’Dwyer et al. (2022), Tabla 6. Fases del consorcio: embrionaria antes del año
# 1, inicio entre los años 1 y 3, compromiso entre los años 4 y 7, las mismas que
# ya usa s2-barreras-intensidad. La confianza es el único elemento que la tabla
# declara primero como barrera —fuerte y luego moderada— y después como
# facilitador, por reputación y por integridad.
#
# La x es la fase y no una medida, así que la posición de cada nodo va ESCRITA:
# los rótulos miden entre ocho y dieciocho caracteres y con paso constante «por
# reputación» pisaba el nodo siguiente (METODOLOGIA.md §17.16). El último campo
# del carril dice hacia dónde sale su rótulo.
FASES_CONSORCIO = [
    (0, 34, "Fase 1 · embrionaria", "antes del año 1"),
    (34, 72, "Fase 2 · inicio", "años 1 a 3"),
    (72, 110, "Fase 3 · compromiso", "años 4 a 7"),
]
CRUCE_CONFIANZA = [
    (5, "barrera", "confianza · fuerte"),
    (39, "barrera", "moderada"),
    (48, "facilitador", "por reputación"),
    (78, "facilitador", "por integridad"),
]
CARRILES_CRUCE = [("barrera", "barrera declarada", 0.52, ACCENT, 1),
                  ("facilitador", "facilitador declarado", -0.52, OK, -1)]


def fig_cruce_confianza():
    """La confianza cruza de barrera a facilitador dentro de la segunda fase."""
    fig, ax = plt.subplots(figsize=(7.8, 2.3))
    X0, X1 = FASES_CONSORCIO[0][0], FASES_CONSORCIO[-1][1]

    for _, nombre, y, color, _lado in CARRILES_CRUCE:
        ax.add_patch(Rectangle((X0, y - 0.34), X1 - X0, 0.68, facecolor=color,
                               alpha=0.10, edgecolor="none"))
        ax.text(X0 - 2, y, nombre, ha="right", va="center", fontsize=7.6,
                color=color, fontweight="bold")

    for xa, xb, titulo, años in FASES_CONSORCIO:
        ax.vlines(xa, -1.02, 1.02, color=GRID, linewidth=0.8)
        ax.text((xa + xb) / 2, 1.24, titulo, ha="center", va="bottom",
                fontsize=8.2, color=INK, fontweight="bold")
        ax.text((xa + xb) / 2, 1.06, años, ha="center", va="bottom",
                fontsize=7.2, color=MUTED)
    ax.vlines(X1, -1.02, 1.02, color=GRID, linewidth=0.8)

    alturas = {clave: y for clave, _, y, _, _ in CARRILES_CRUCE}
    lados = {clave: lado for clave, _, _, _, lado in CARRILES_CRUCE}
    puntos = [(x, alturas[carril]) for x, carril, _ in CRUCE_CONFIANZA]
    ax.plot([p[0] for p in puntos], [p[1] for p in puntos], color=INK,
            linewidth=1.6, zorder=3)
    for (x, carril, rotulo), (_, y) in zip(CRUCE_CONFIANZA, puntos):
        color = ACCENT if carril == "barrera" else OK
        ax.plot([x], [y], "o", color=color, markersize=8.5, zorder=4)
        # El rótulo va ENCIMA de su nodo en el carril de arriba y DEBAJO en el de
        # abajo: al lado, la propia línea del recorrido lo tachaba.
        ax.text(x, y + 0.21 * lados[carril], rotulo, ha="left",
                va="bottom" if lados[carril] > 0 else "top", fontsize=7.6,
                color=INK)

    ax.text(X0, -1.36, "La confianza es el único elemento que la tabla declara "
            "primero como barrera y después como facilitador",
            ha="left", va="center", fontsize=7.0, color=MUTED)
    ax.set_xlim(-24, X1 + 2)
    ax.set_ylim(-1.55, 1.52)
    ax.axis("off")
    escribir(fig, "s2-cruce-confianza")


# Tres magnitudes del punto de partida peruano, cada una dividida por su propio
# referente. Los tres cocientes están enunciados en las fuentes —el 1 % de las
# 340 empresas de la región (BID, 2023), siete veces por debajo de la meta de 1 %
# del PBI (DS 093-2025-PCM y POLCTI) y la décima parte de las patentes por millón
# de Chile (POLCTI, Tabla 16, la misma que usa s1-brecha-chile)— y aquí se
# dibujan sobre un eje común de múltiplos, que es lo que permite compararlos:
# dos brechas son de un orden de magnitud y la tercera de dos.
#
# Las unidades de los tres indicadores no son comparables entre sí, y por eso el
# eje NO lleva su valor sino el cociente: cada fila declara su propio par de
# cifras al lado de su línea.
BRECHAS_PERU = [
    ("Empresas de deep tech", 5.0, 340.0, "5 en el Perú de las 340 de la región"),
    ("Patentes por millón de hab.", 2.1, 20.5, "2,1 en el Perú y 20,5 en Chile"),
    ("Gasto en I+D · % del PBI", 0.13, 1.0, "0,13 % frente a la meta de 1 %"),
]


def fig_brechas_multiplos():
    """Dos brechas son de un orden de magnitud y la del número de empresas, de dos."""
    fig, ax = plt.subplots(figsize=(6.8, 2.6))
    n = len(BRECHAS_PERU)

    for k, (_, peru, referente, detalle) in enumerate(BRECHAS_PERU):
        y = n - 1 - k
        mult = referente / peru
        ax.hlines(y, 1, mult, color=GRID, linewidth=2.2, zorder=1)
        ax.plot([mult], [y], "o", color=ACCENT, markersize=9, zorder=3)
        # El múltiplo se coloca contra la posición real del punto y el par de
        # cifras arranca en la paridad: con los dos anclados al mismo canto, el
        # rótulo de la fila de las empresas pisaba su propio múltiplo.
        ax.text(mult * 1.14, y, f"× {num(mult, 1)}", ha="left", va="center",
                fontsize=9.0, color=ACCENT, fontweight="bold")
        ax.text(1.06, y + 0.26, detalle, ha="left", va="center", fontsize=7.4,
                color=MUTED)

    ax.axvline(1, color=INK, linewidth=1.0)
    ax.text(1, -0.92, "paridad con el referente", ha="left", va="center",
            fontsize=7.2, color=INK)

    ax.set_xscale("log")
    ax.set_xlim(1, 185)
    ax.set_ylim(-1.05, n - 0.42)
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax.set_xticklabels([f"× {v}" for v in (1, 2, 5, 10, 20, 50, 100)])
    ax.set_yticks(range(n))
    ax.set_yticklabels([nombre for nombre, _, _, _ in BRECHAS_PERU][::-1],
                       fontsize=8.4, color=INK)
    ax.set_xlabel("Veces que el referente contiene al valor peruano · escala logarítmica",
                  fontsize=8.0, color=MUTED)
    ax.tick_params(axis="x", labelsize=7.6, colors=MUTED, length=0)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s2-brechas-multiplos")


FIGURAS += [fig_escalera_jurisdicciones, fig_varianza_intencion,
            fig_reparto_transferencia, fig_cruce_confianza,
            fig_brechas_multiplos]


# ==========================================================================
# SESIÓN 3 · Tema 01 — instrumentos públicos y contrapartida
# ==========================================================================

# POLCTI (CONCYTEC, 2024), págs. 53 y 68, citando el estudio de línea base del
# gasto público en CTI (Rogers, 2020). Los tres puntos que la fuente publica de
# la curva de concentración —43 %, 75 % y 90 % acumulados sobre 1, 13 y 45
# instrumentos de 164— se convierten aquí en participación marginal por resta:
# 43, 32, 15 y 10 %, sobre 1, 12, 32 y 119 instrumentos. La curva de la sesión 1
# enseña la acumulación; el sankey enseña cuánto se lleva cada bloque.
REPARTO_PRESUPUESTO = [
    ("Programa Nacional de Becas\ndel Ministerio de Educación", 1, 43, ACCENT),
    ("Los doce siguientes\nmayores instrumentos", 12, 32, RAMPA[2]),
    ("Los treinta y dos siguientes", 32, 15, RAMPA[1]),
    ("Los ciento diecinueve restantes", 119, 10, RAMPA[0]),
]


def _cinta(ax, x1, x2, y1a, y1b, y2a, y2b, color):
    """Cinta de sankey entre dos nodos, cerrada con dos curvas cúbicas."""
    xm = (x1 + x2) / 2
    verts = [(x1, y1a), (xm, y1a), (xm, y2a), (x2, y2a),
             (x2, y2b), (xm, y2b), (xm, y1b), (x1, y1b), (x1, y1a)]
    codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
             MplPath.LINETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
             MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(verts, codes), facecolor=color, alpha=0.42,
                           edgecolor="none", zorder=1))


def fig_reparto_presupuesto():
    """Un instrumento se lleva el 43 % y los ciento diecinueve menores el 10 %."""
    # El hueco entre nodos de destino es de siete unidades y no de dos: con dos,
    # el rótulo de dos líneas del bloque del 10 % se montaba sobre el del 15 %.
    HUECO = 7.0
    total = sum(p for _, _, p, _ in REPARTO_PRESUPUESTO)
    alto = total + HUECO * (len(REPARTO_PRESUPUESTO) - 1)

    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    x1, x2, ANCHO = 0.0, 4.2, 0.26

    y0 = (alto - total) / 2
    ax.add_patch(Rectangle((x1 - ANCHO, y0), ANCHO, total, facecolor=INK,
                           edgecolor="none", zorder=3))
    ax.text(x1 - ANCHO - 0.10, y0 + total / 2,
            "Presupuesto público\nde CTI · 100 %", ha="right", va="center",
            fontsize=8.6, color=INK, linespacing=1.35, fontweight="bold")

    cur_izq, cur_der = alto - y0, alto
    for nombre, cuantos, parte, color in REPARTO_PRESUPUESTO:
        _cinta(ax, x1, x2, cur_izq, cur_izq - parte, cur_der, cur_der - parte, color)
        ax.add_patch(Rectangle((x2, cur_der - parte), ANCHO, parte,
                               facecolor=color, edgecolor="none", zorder=3))
        cy = cur_der - parte / 2
        # El primer nodo lleva el NOMBRE del instrumento y no su recuento: «1
        # instrumento · 43 %» obliga a preguntar cuál (METODOLOGIA.md §17.22).
        ax.text(x2 + ANCHO + 0.12, cy + 0.9, nombre, ha="left", va="bottom",
                fontsize=8.0, color=INK, linespacing=1.3)
        ax.text(x2 + ANCHO + 0.12, cy - 1.2,
                f"{num(parte, 0)} % del presupuesto · "
                f"{cuantos} instrumento{'s' if cuantos > 1 else ''}",
                ha="left", va="top", fontsize=7.4, color=color, fontweight="bold")
        cur_izq -= parte
        cur_der -= parte + HUECO

    ax.set_xlim(-2.5, 9.6)
    ax.set_ylim(-3, alto + 3)
    ax.axis("off")
    escribir(fig, "s3-reparto-presupuesto")


# Mismos cuatro bloques y misma fuente que la figura anterior. La tercera
# variable, el presupuesto medio por instrumento del bloque, sale de dividir la
# participación entre el recuento: 43,00 %, 2,67 %, 0,47 % y 0,08 % del
# presupuesto total. Es aritmética sobre lo publicado, no un dato añadido.
BLOQUES_PRESUPUESTO = [
    ("Programa Nacional de Becas", 1, 43, ACCENT),
    ("Los 12 siguientes", 12, 32, RAMPA[2]),
    ("Los 32 siguientes", 32, 15, RAMPA[1]),
    ("Los 119 restantes", 119, 10, RAMPA[0]),
]


def fig_bloques_presupuesto():
    """El instrumento medio del bloque menor maneja quinientas veces menos que el mayor."""
    fig, ax = plt.subplots(figsize=(6.9, 3.2))

    # El nombre y su cifra van JUNTOS y a un lado de la burbuja, no uno encima
    # y otra debajo. Separados, con cuatro burbujas en diagonal, el nombre de
    # una caía a la altura de la cifra de la vecina y se leían como una sola
    # frase: «Los 119 restantes 2,67 % del presupuesto cada uno», que atribuye
    # al bloque equivocado. El lado alterna para que ninguno invada al de al
    # lado (METODOLOGIA.md §4.4.1).
    LADO = {"Programa Nacional de Becas": "izq", "Los 12 siguientes": "izq",
            "Los 32 siguientes": "der", "Los 119 restantes": "der"}
    for nombre, cuantos, parte, color in BLOQUES_PRESUPUESTO:
        medio = parte / cuantos
        s = 18 * cuantos + 80
        ax.scatter(parte, medio, s=s, color=color, alpha=0.5, edgecolors=color,
                   linewidths=1.4, zorder=3)
        # El desplazamiento se mide en PUNTOS y sale del radio de la propia
        # burbuja: con un desplazamiento fijo en unidades de dato, el rótulo de
        # los 119 instrumentos caía dentro del círculo.
        r_pt = (s / 3.1416) ** 0.5
        izq = LADO[nombre] == "izq"
        ax.annotate(f"{nombre}\n{num(medio, 2)} % del presupuesto cada uno",
                    xy=(parte, medio),
                    xytext=(-(r_pt + 7) if izq else r_pt + 7, 0),
                    textcoords="offset points",
                    ha="right" if izq else "left", va="center",
                    fontsize=7.6, color=INK, linespacing=1.5)

    ax.set_yscale("log")
    # El suelo del eje lo fija el rótulo inferior, no el dato menor: con el
    # suelo en 0,012 la burbuja de los 119 instrumentos se cortaba contra el
    # eje y su cifra caía FUERA del área, encima de las marcas del eje x
    # (METODOLOGIA.md §4.4.1).
    ax.set_ylim(0.012, 160)
    ax.set_xlim(-30, 74)
    ax.set_xticks([0, 20, 40, 60])
    ax.set_xlabel("Participación del bloque en el presupuesto de CTI (%)",
                  fontsize=8.4, color=MUTED)
    ax.set_ylabel("Presupuesto medio por instrumento\n(% del total, escala logarítmica)",
                  fontsize=8.0, color=MUTED)
    ax.tick_params(labelsize=7.8, colors=MUTED)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    # El área NO es el número de instrumentos: s = 18n + 80 es afín, no
    # proporcional, y con proporción estricta el bloque de un instrumento
    # sería invisible. El rótulo dice lo que la figura hace de verdad.
    ax.text(74, 0.016, "el área del círculo crece con el número\nde instrumentos del bloque",
            ha="right", va="bottom", fontsize=7.0, color=MUTED, linespacing=1.4)
    limpiar_ejes(ax)
    escribir(fig, "s3-bloques-presupuesto")


# POLCTI (CONCYTEC, 2024), Tabla 14. Los mismos siete valores que la sesión 1
# dibuja en barras. Lo que añade el árbol es el agrupamiento, que las barras no
# muestran: dos sectores suman 109 instrumentos y los otros cinco, 55.
ARBOL_SECTOR = [
    ("Producción y CONCYTEC", 109, [("Producción", 71), ("CONCYTEC", 38)]),
    ("Los otros cinco sectores", 55, [
        ("Educación", 26), ("Agricultura", 9), ("Ambiente", 8),
        ("Salud", 4), ("Otros sectores", 8)]),
]
ARBOL_TOTAL = 164


def fig_arbol_sector():
    """Dos sectores del Estado operan ciento nueve de los ciento sesenta y cuatro instrumentos."""
    hojas = [n for _, _, hs in ARBOL_SECTOR for n, _ in hs]
    ys = {n: len(hojas) - 1 - i for i, n in enumerate(hojas)}

    fig, ax = plt.subplots(figsize=(6.9, 3.5))
    X_RAIZ, X_RAMA, X_HOJA = 0.0, 1.15, 2.30

    y_rama = []
    for k, (rotulo, suma, hs) in enumerate(ARBOL_SECTOR):
        color = ACCENT if k == 0 else NAVY
        yy = [ys[n] for n, _ in hs]
        y_rama.append((max(yy) + min(yy)) / 2)
        ax.vlines(X_RAMA, min(yy), max(yy), color=color, linewidth=1.6)
        for n, v in hs:
            ax.hlines(ys[n], X_RAMA, X_HOJA, color=color, linewidth=1.6)
            ax.plot(X_HOJA, ys[n], "o", color=color, markersize=5.5)
            ax.text(X_HOJA + 0.07, ys[n] + 0.08, n, ha="left", va="bottom",
                    fontsize=8.6, color=INK)
            ax.text(X_HOJA + 0.07, ys[n] - 0.10,
                    f"{v} instrumentos · {num(v / ARBOL_TOTAL * 100, 0)} %",
                    ha="left", va="top", fontsize=7.2, color=color)
        # El rótulo de cada rama sale del tramo que esa rama ocupa: el de arriba
        # por encima de su tramo y el de abajo por debajo del suyo. Colocados los
        # dos a media altura, el de la rama larga cruzaba la vertical de la raíz.
        if k == 0:
            ya, va = max(yy) + 0.30, "bottom"
        else:
            ya, va = min(yy) - 0.30, "top"
        ax.text(X_RAMA - 0.06, ya, f"{rotulo} · {suma} instrumentos",
                ha="right", va=va, fontsize=7.8, color=color, fontweight="bold")

    ax.vlines(X_RAIZ, min(y_rama), max(y_rama), color=MUTED, linewidth=1.6)
    for k, ym in enumerate(y_rama):
        ax.hlines(ym, X_RAIZ, X_RAMA, color=ACCENT if k == 0 else NAVY,
                  linewidth=1.6)
    ax.plot(X_RAIZ, sum(y_rama) / 2, "o", color=MUTED, markersize=6)
    ax.text(X_RAIZ - 0.09, sum(y_rama) / 2,
            f"{ARBOL_TOTAL} instrumentos\nde CTI, 2012-2018", ha="right",
            va="center", fontsize=8.4, color=INK, linespacing=1.35,
            fontweight="bold")

    ax.set_xlim(-2.55, 4.30)
    ax.set_ylim(-1.25, len(hojas) + 0.10)
    ax.axis("off")
    escribir(fig, "s3-arbol-sector")


# DS 093-2025-PCM y POLCTI (CONCYTEC, 2024): los seis organismos del SINACTI que
# recoge la sesión 1 y las cinco formas que toma un instrumento de CTI. La celda
# marcada dice que ese organismo opera esa forma. INDECOPI y SUNEDU no financian:
# sus dos filas quedan vacías, y esa es la información de la figura.
FORMAS_INSTRUMENTO = ["Beca", "Concurso de\ninvestigación",
                      "Subvención a\nla innovación\nempresarial",
                      "Servicio\ntecnológico", "Beneficio\ntributario"]
ORGANISMO_FORMA = [
    ("CONCYTEC", "rector de la política de CTI", [0, 0, 0, 0, 1]),
    ("PROCIENCIA", "financiador de investigación", [1, 1, 0, 0, 0]),
    ("ProInnóvate", "financiador de innovación empresarial", [0, 0, 1, 0, 0]),
    ("ITP · Red CITE", "extensionismo tecnológico", [0, 0, 0, 1, 0]),
    ("INDECOPI", "autoridad de propiedad intelectual", [0, 0, 0, 0, 0]),
    ("SUNEDU", "supervisión universitaria", [0, 0, 0, 0, 0]),
]


def fig_matriz_organismo_forma():
    """Dos de los seis organismos del SINACTI no operan ninguna forma de financiamiento."""
    # La unidad de dato de esta figura es la PULGADA: el ancho del lienzo sale
    # del rótulo más largo y no al revés. Con un paso en unidades abstractas,
    # «investigación» y «la innovación» se tocaban, porque el eje ocupa el 77,5 %
    # del ancho declarado y el paso real quedaba por debajo del rótulo.
    CH = 0.0620   # ancho de un carácter monoespaciado a 7,4 pt, en pulgadas
    ancho_rotulo = max(max(len(l) for l in f.split("\n"))
                       for f in FORMAS_INSTRUMENTO) * CH
    PASO = ancho_rotulo + 0.22
    IZQ, DER = 2.50, 0.95
    nf, no = len(FORMAS_INSTRUMENTO), len(ORGANISMO_FORMA)
    xs = [(j + 0.5) * PASO for j in range(nf)]
    borde = nf * PASO
    FILA = 0.46

    ancho = IZQ + borde + DER
    fig, ax = plt.subplots(figsize=(ancho / 0.775, 4.25))

    for x, forma in zip(xs, FORMAS_INSTRUMENTO):
        ax.text(x, 0.20, forma, ha="center", va="bottom", fontsize=7.4,
                color=INK, linespacing=1.3)

    for i, (nombre, papel, marcas) in enumerate(ORGANISMO_FORMA):
        y = -i * FILA
        financia = any(marcas)
        ax.text(-0.14, y + 0.03, nombre, ha="right", va="bottom", fontsize=8.6,
                color=INK if financia else MUTED, fontweight="bold")
        ax.text(-0.14, y - 0.05, papel, ha="right", va="top", fontsize=7.0,
                color=MUTED)
        ax.hlines(y - FILA / 2, -0.06, borde, color=GRID, linewidth=0.6)
        for x, m in zip(xs, marcas):
            ax.add_patch(Rectangle((x - 0.31, y - 0.10), 0.62, 0.20,
                                   facecolor=ACCENT if m else SURFACE,
                                   edgecolor="none" if m else GRID,
                                   linewidth=0 if m else 0.7))
        if not financia:
            ax.text(borde + 0.12, y, "no financia", ha="left", va="center",
                    fontsize=7.4, color=MUTED, style="italic")

    ax.hlines(FILA / 2, -0.06, borde, color=GRID, linewidth=0.6)
    ax.set_xlim(-IZQ, borde + DER)
    ax.set_ylim(-(no - 1) * FILA - 0.34, 0.66)
    ax.axis("off")
    escribir(fig, "s3-matriz-organismo-forma")


# Aritmética del cofinanciamiento, no un dato de convocatoria: si las bases fijan
# un cofinanciamiento del p % del costo total, la contrapartida es el (100 - p) %
# y equivale a (100 - p) / p por cada unidad monetaria subvencionada. Las bases de
# ProInnóvate y de PROCIENCIA fijan p en cada edición, y por eso el eje recorre un
# rango en vez de citar un porcentaje concreto.
COFIN_RANGO = (50, 90)
COFIN_HITOS = (50, 70, 80)


def fig_area_contrapartida():
    """A ochenta por ciento de cofinanciamiento, cada sol subvencionado exige veinticinco céntimos."""
    xs = np.linspace(COFIN_RANGO[0], COFIN_RANGO[1], 200)

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.fill_between(xs, 0, xs, color=NAVY, alpha=0.35, linewidth=0)
    ax.fill_between(xs, xs, 100, color=ACCENT, alpha=0.45, linewidth=0)
    ax.plot(xs, xs, color=NAVY, linewidth=1.8)

    ax.text(COFIN_RANGO[0] + 1.2, 24, "Subvención del fondo público",
            ha="left", va="center", fontsize=8.6, color=NAVY, fontweight="bold")
    ax.text(COFIN_RANGO[1] - 1.2, 95, "Contrapartida del postulante",
            ha="right", va="center", fontsize=8.6, color=ACCENT, fontweight="bold")

    ax.text(70, 112, "contrapartida exigida por cada 1,00 de subvención",
            ha="center", va="bottom", fontsize=7.2, color=MUTED)
    for p in COFIN_HITOS:
        ax.vlines(p, 0, 100, color=PAPER, linewidth=1.0, linestyle=(0, (3, 3)))
        ax.plot(p, p, "o", color=INK, markersize=4.5, zorder=4)
        # El primer hito cae sobre el propio eje: alineado al centro, su rótulo
        # sale del lienzo por la izquierda.
        ha = "left" if p == COFIN_HITOS[0] else "center"
        # Dos decimales SIEMPRE: num() poda el cero final y el primer hito salía
        # como «1» junto a «0,43» y «0,25».
        ax.text(p, 103, f"{(100 - p) / p:.2f}".replace(".", ","), ha=ha,
                va="bottom", fontsize=8.6, color=INK, fontweight="bold")

    ax.set_xlim(*COFIN_RANGO)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Cofinanciamiento público fijado por las bases (% del costo total)",
                  fontsize=8.4, color=MUTED)
    ax.set_ylabel("Costo total del proyecto (%)", fontsize=8.4, color=MUTED)
    ax.set_xticks([50, 60, 70, 80, 90])
    ax.tick_params(labelsize=7.8, colors=MUTED)
    limpiar_ejes(ax)
    escribir(fig, "s3-area-contrapartida")


# Elaboración propia sobre las convocatorias vigentes de ProInnóvate y de
# PROCIENCIA y sobre los cinco tipos de entidad postulante que modela la sesión 1.
# Tres intensidades: la partida con la que esa figura cubre habitualmente su
# contrapartida, la que las bases le admiten sin que baste por sí sola, y la que
# no tiene uso en esa figura. La empresa formal es la única con efectivo exigido.
PARTIDAS_APORTE = ["Efectivo\npropio", "Horas de\npersonal\nvalorizadas",
                   "Uso de\ninfraestructura\nvalorizado",
                   "Aporte de la\nentidad\nasociada"]
ENTIDAD_APORTE = [
    ("Universidad licenciada", [1, 2, 2, 2]),
    ("Empresa formal", [2, 2, 2, 1]),
    ("Persona o equipo sin empresa", [1, 2, 0, 1]),
    ("Asociación o cooperativa", [0, 1, 1, 2]),
    ("Instituto público de investigación", [0, 2, 2, 1]),
]


def fig_matriz_entidad_aporte():
    """La empresa formal es la única figura a la que se le exige efectivo propio."""
    # Misma cuenta que la matriz de organismos: el paso entre columnas sale del
    # rótulo más largo, medido en pulgadas, y no de un valor fijo.
    CH = 0.0620
    ancho_rotulo = max(max(len(l) for l in c.split("\n"))
                       for c in PARTIDAS_APORTE) * CH
    PASO = ancho_rotulo + 0.22
    IZQ, DER = 2.60, 0.15
    npart, nent = len(PARTIDAS_APORTE), len(ENTIDAD_APORTE)
    xs = [(j + 0.5) * PASO for j in range(npart)]
    borde = npart * PASO
    FILA = 0.44

    ancho = IZQ + borde + DER
    fig, ax = plt.subplots(figsize=(ancho / 0.775, 4.90))

    for x, partida in zip(xs, PARTIDAS_APORTE):
        ax.text(x, 0.19, partida, ha="center", va="bottom", fontsize=7.4,
                color=INK, linespacing=1.3)

    def _celda(x, y, m):
        if m == 2:
            return Rectangle((x - 0.33, y - 0.095), 0.66, 0.19,
                             facecolor=ACCENT, edgecolor="none")
        if m == 1:
            return Rectangle((x - 0.33, y - 0.095), 0.66, 0.19,
                             facecolor=PAPER, edgecolor=ACCENT, linewidth=1.3)
        return Rectangle((x - 0.33, y - 0.095), 0.66, 0.19,
                         facecolor=SURFACE, edgecolor=GRID, linewidth=0.7)

    for i, (nombre, marcas) in enumerate(ENTIDAD_APORTE):
        y = -i * FILA
        ax.text(-0.14, y, nombre, ha="right", va="center", fontsize=8.4, color=INK)
        ax.hlines(y - FILA / 2, -0.06, borde, color=GRID, linewidth=0.6)
        for x, m in zip(xs, marcas):
            ax.add_patch(_celda(x, y, m))

    ax.hlines(FILA / 2, -0.06, borde, color=GRID, linewidth=0.6)

    # La leyenda va en tres renglones bajo la matriz. En un solo renglón, el
    # segundo rótulo empezaba encima de su propia muestra de color.
    leyenda = [(ACCENT, None, "aporte con el que esa figura cubre habitualmente su contrapartida"),
               (PAPER, ACCENT, "admitido por las bases, rara vez suficiente por sí solo"),
               (SURFACE, GRID, "sin uso habitual en esa figura")]
    base = -(nent - 1) * FILA - 0.42
    for k, (color, filo, texto) in enumerate(leyenda):
        yy = base - k * 0.30
        ax.add_patch(Rectangle((-0.06, yy - 0.065), 0.30, 0.13, facecolor=color,
                               edgecolor=filo or "none",
                               linewidth=1.2 if filo else 0))
        ax.text(0.34, yy, texto, ha="left", va="center", fontsize=7.4, color=INK)

    ax.set_xlim(-IZQ, borde + DER)
    ax.set_ylim(base - 2 * 0.30 - 0.22, 0.64)
    ax.axis("off")
    escribir(fig, "s3-matriz-entidad-aporte")


# POLCTI (CONCYTEC, 2024), págs. 40 y 72, con datos de la Encuesta Nacional de
# Innovación en la Industria Manufacturera del INEI. Mismos tres valores que la
# sesión 1. La escala del arco llega a 50 % y va escrita en cada extremo: sin ese
# tope declarado, un arco lleno al 87 % se leería como el 87 % de las empresas.
# El tercer obstáculo va en rojo porque es el que gobierna la contrapartida.
OBSTACULOS_GAUGE = [
    ("Costo de innovar\ndemasiado elevado", 43.4, NAVY),
    ("Escasez de personal\ncalificado", 33.3, NAVY),
    ("Falta de fondos\nen la empresa", 32.3, ACCENT),
]
GAUGE_TOPE = 50.0


def fig_gauges_obstaculos():
    """Uno de cada tres fabricantes declara que no tiene fondos con los que innovar."""
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    PASO, RAD = 2.55, 1.0

    for k, (nombre, valor, color) in enumerate(OBSTACULOS_GAUGE):
        cx = k * PASO
        ang = 180 - 180 * valor / GAUGE_TOPE
        ax.add_patch(Wedge((cx, 0), RAD, 0, 180, width=0.30, facecolor=SURFACE,
                           edgecolor=GRID, linewidth=0.7))
        ax.add_patch(Wedge((cx, 0), RAD, ang, 180, width=0.30, facecolor=color,
                           edgecolor="none"))
        # La cifra cabe dentro del radio interior (0,70) solo hasta 13 pt: a
        # 15 pt el signo de porcentaje montaba sobre el propio arco, porque la
        # cuerda se estrecha a medida que el rótulo sube (METODOLOGIA.md §4.4.1).
        ax.text(cx, 0.16, f"{num(valor, 1)} %", ha="center", va="bottom",
                fontsize=13, color=color, fontweight="bold")
        ax.text(cx - RAD, -0.05, "0", ha="center", va="top", fontsize=6.6,
                color=MUTED)
        ax.text(cx + RAD, -0.05, num(GAUGE_TOPE, 0), ha="center", va="top",
                fontsize=6.6, color=MUTED)
        # El nombre baja por debajo de los extremos de la escala: a la altura del
        # propio arco pisaba el «0» y el «50».
        ax.text(cx, -0.26, nombre, ha="center", va="top", fontsize=8.0,
                color=INK, linespacing=1.3)

    ax.text(2 * PASO + RAD, 1.14,
            "porcentaje de empresas manufactureras que declara el obstáculo, "
            "sobre una escala de 0 a 50 %",
            ha="right", va="bottom", fontsize=7.0, color=MUTED)
    ax.set_xlim(-1.35, 2 * PASO + 1.35)
    ax.set_ylim(-1.10, 1.48)
    ax.set_aspect("equal")
    ax.axis("off")
    escribir(fig, "s3-gauges-obstaculos")


# POLCTI (CONCYTEC, 2024), Tabla 10, con datos del CONCYTEC. Misma serie que la
# sesión 1. El ancho de cada columna es el número de proyectos presentados ese
# año, así que el área total de la figura son los 352 proyectos del periodo: eso
# es lo que las barras agrupadas de la sesión 1 no dejan ver.
LEY_30309_SERIE = [
    (2016, 72, 8), (2017, 68, 22), (2018, 43, 19), (2019, 48, 26),
    (2020, 35, 16), (2021, 33, 17), (2022, 53, 28),
]
LEY_30309_TOTAL = (352, 136)


def fig_marimekko_30309():
    """Los dos años de más solicitudes son los dos de menor tasa de aprobación."""
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    HUECO = 2.4
    tasa_ac = LEY_30309_TOTAL[1] / LEY_30309_TOTAL[0] * 100
    x = 0.0
    for anio, pres, apro in LEY_30309_SERIE:
        tasa = apro / pres * 100
        ax.add_patch(Rectangle((x, 0), pres, 100, facecolor=SURFACE,
                               edgecolor=PAPER, linewidth=1.0))
        ax.add_patch(Rectangle((x, 0), pres, tasa, facecolor=ACCENT,
                               edgecolor=PAPER, linewidth=1.0))
        cx = x + pres / 2
        # La cifra va SOBRE el filo de la banda roja, no dentro: con el 11 % de
        # 2016 la banda mide once unidades y el texto no cabe en ella. La
        # excepción son los años cuyo filo cae junto a la línea del acumulado,
        # que se rotulan por dentro y por debajo de ella para no montarse encima.
        if abs(tasa - tasa_ac) < 9:
            ax.text(cx, min(tasa - 4.0, tasa_ac - 4.5), f"{num(tasa, 0)} %",
                    ha="center", va="top", fontsize=8.2, color=PAPER,
                    fontweight="bold")
        else:
            ax.text(cx, tasa + 3.0, f"{num(tasa, 0)} %", ha="center", va="bottom",
                    fontsize=8.2, color=ACCENT, fontweight="bold")
        ax.text(cx, -3.5, str(anio), ha="center", va="top", fontsize=8.2, color=INK)
        ax.text(cx, -11.5, str(pres), ha="center", va="top", fontsize=7.4, color=MUTED)
        x += pres + HUECO

    total = x - HUECO
    ax.hlines(tasa_ac, 0, total, color=MUTED, linewidth=1.1, linestyle=(0, (4, 3)))
    # La cita del acumulado va ARRIBA, fuera del área de datos: sobre la propia
    # línea se montaba con la cifra de 2020. La muestra de trazo se dibuja, no se
    # teclea con guiones, que el auditor de léxico lee como inciso.
    ax.plot([0, 13], [106, 106], color=MUTED, linewidth=1.1, linestyle=(0, (4, 3)))
    ax.text(16, 106,
            f"acumulado del periodo · {num(tasa_ac, 0)} % "
            f"({LEY_30309_TOTAL[1]} de {LEY_30309_TOTAL[0]} proyectos)",
            ha="left", va="center", fontsize=7.4, color=INK)

    for v in (0, 50, 100):
        ax.text(-5, v, f"{v} %", ha="right", va="center", fontsize=7.2, color=MUTED)
    ax.text(-27, 50, "Proyectos del año (%)", ha="center", va="center",
            fontsize=8.2, color=MUTED, rotation=90)
    ax.text(0, -19.5, "año  ·  proyectos presentados, que fijan el ancho de la columna",
            ha="left", va="top", fontsize=7.0, color=MUTED)
    ax.set_xlim(-34, total + 4)
    ax.set_ylim(-27, 114)
    ax.axis("off")
    escribir(fig, "s3-marimekko-30309")


# Misma serie y misma fuente que la figura anterior, acumulada año a año. La
# pregunta que responde es otra: cuántos proyectos ha calificado el beneficio
# tributario desde que existe. El escalón es la forma del recuento corrido.
def fig_escalones_30309():
    """Siete años del beneficio tributario suman ciento treinta y seis proyectos aprobados."""
    anios = [a for a, _, _ in LEY_30309_SERIE]
    pres, apro, sp, sa = [], [], 0, 0
    for _, p, a in LEY_30309_SERIE:
        sp += p
        sa += a
        pres.append(sp)
        apro.append(sa)

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.step(anios, pres, where="post", color=MUTED, linewidth=2.0)
    ax.step(anios, apro, where="post", color=ACCENT, linewidth=2.4)
    ax.fill_between(anios, 0, apro, step="post", color=ACCENT, alpha=0.12)

    # `where="post"` deja el peldaño del último año sin dibujar y la serie
    # parecía terminar en 2021: el tramo final se cierra a mano.
    ax.hlines(pres[-1], anios[-1], anios[-1] + 0.55, color=MUTED, linewidth=2.0)
    ax.hlines(apro[-1], anios[-1], anios[-1] + 0.55, color=ACCENT, linewidth=2.4)
    ax.text(anios[-1] + 0.68, pres[-1], f"{pres[-1]} presentados", ha="left",
            va="center", fontsize=8.4, color=MUTED)
    ax.text(anios[-1] + 0.68, apro[-1], f"{apro[-1]} aprobados", ha="left",
            va="center", fontsize=8.4, color=ACCENT, fontweight="bold")

    ax.set_xlim(2015.75, 2024.6)
    ax.set_ylim(0, 400)
    ax.set_xticks(anios)
    ax.set_ylabel("Proyectos acumulados desde 2016", fontsize=8.4, color=MUTED)
    ax.tick_params(axis="x", labelsize=8.2, colors=INK, length=0)
    ax.tick_params(axis="y", labelsize=7.8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s3-escalones-30309")


# Tramo de la escala TRL que admite cada ventanilla pública, con la misma
# correspondencia que la tabla de tramos de la sesión 1: PROCIENCIA en TRL 1-3,
# ProInnóvate en TRL 4-6 y en TRL 7-9, y la Red CITE del ITP en los ensayos de
# TRL 4-9. El beneficio tributario de la Ley 30309 no selecciona por tramo:
# califica la actividad, y por eso su barra va punteada y sin marca de tramo.
RANGOS_VENTANILLA = [
    ("PROCIENCIA", "investigación básica y aplicada", 1, 3, ACCENT, False),
    ("ProInnóvate", "desarrollo tecnológico", 4, 6, NAVY, False),
    ("ProInnóvate", "validación, escalamiento y capital semilla", 7, 9, NAVY, False),
    ("ITP · Red CITE", "servicios tecnológicos de ensayo", 4, 9, RAMPA[1], False),
    ("CONCYTEC", "Ley 30309 · beneficio tributario", 1, 9, MUTED, True),
]


def fig_rangos_trl_ventanilla():
    """Ninguna ventanilla de subvención cubre la escala entera, y el beneficio tributario no la usa."""
    fig, ax = plt.subplots(figsize=(8.2, 3.1))
    n = len(RANGOS_VENTANILLA)
    X_TAG = 9.8

    for corte in (3.5, 6.5):
        ax.vlines(corte, -0.75, n - 0.45, color=GRID, linewidth=1.1,
                  linestyle=(0, (4, 3)))
    ax.text(3.5, n - 0.42, "entorno relevante", ha="center", va="bottom",
            fontsize=7.2, color=MUTED)
    ax.text(6.5, n - 0.42, "entorno real", ha="center", va="bottom",
            fontsize=7.2, color=MUTED)

    for i, (organismo, materia, a, b, color, abierto) in enumerate(RANGOS_VENTANILLA):
        y = n - 1 - i
        if abierto:
            ax.plot([a, b], [y, y], color=color, linewidth=3.2, alpha=0.45,
                    linestyle=(0, (1, 1.7)), solid_capstyle="butt")
            ax.text(X_TAG, y, "califica la actividad,\nno el tramo", ha="left",
                    va="center", fontsize=7.2, color=MUTED, linespacing=1.3)
        else:
            ax.plot([a, b], [y, y], color=color, linewidth=7.0, alpha=0.85,
                    solid_capstyle="round")
            ax.plot([a, b], [y, y], "o", color=color, markersize=8.5)
            # La marca de tramo va en columna propia a la derecha del eje: al
            # final de su barra, la del tramo 1-3 caía sobre el corte de 3,5.
            ax.text(X_TAG, y, f"TRL {a}-{b}", ha="left", va="center",
                    fontsize=7.6, color=color, fontweight="bold")
        # Dos renglones a la izquierda, el organismo arriba y la materia debajo.
        # En un solo renglón el rótulo más largo mide cincuenta y seis caracteres
        # y se comía la mitad del lienzo.
        ax.text(0.55, y + 0.12, organismo, ha="right", va="bottom", fontsize=8.4,
                color=INK, fontweight="bold")
        ax.text(0.55, y - 0.12, materia, ha="right", va="top", fontsize=7.4,
                color=MUTED)

    ax.set_xticks(range(1, 10))
    ax.set_xlim(-6.2, 13.0)
    ax.set_ylim(-1.05, n + 0.15)
    ax.set_yticks([])
    ax.set_xlabel("Nivel de madurez tecnológica declarado (TRL)", fontsize=8.4,
                  color=MUTED)
    ax.tick_params(axis="x", labelsize=8.0, colors=MUTED, length=0)
    for v in range(1, 10):
        ax.vlines(v, -0.75, n - 0.55, color=GRID, linewidth=0.5, alpha=0.5,
                  zorder=0)
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s3-rangos-trl-ventanilla")


FIGURAS += [fig_reparto_presupuesto, fig_bloques_presupuesto, fig_arbol_sector,
            fig_matriz_organismo_forma, fig_area_contrapartida,
            fig_matriz_entidad_aporte, fig_gauges_obstaculos,
            fig_marimekko_30309, fig_escalones_30309,
            fig_rangos_trl_ventanilla]


# ==========================================================================
# SESIÓN 3 · Tema 02 — inversión privada y sus criterios
# ==========================================================================

# Dhiman y Arora (2024), LBS Journal of Management & Research 22(1), Tabla 1.
# Tres olas de incubadoras, cada una con su modelo, su propuesta de valor y su
# servicio central. El periodo 1990-2000 no lo asigna la fuente a ninguna
# generación: rellenarlo sería inventar un tramo que la tabla no publica
# (METODOLOGIA.md §17.15), así que el escalón va punteado y rotulado.
GENERACIONES_INCUBADORA = [
    (1972, 1980, 1, "abajo", "1.ª generación · antes de 1980",
     "Parque científico o de investigación",
     "Economías de escala · espacio y recursos compartidos"),
    (1980, 1990, 2, "left", "2.ª generación · 1980-1990",
     "Incubadora virtual",
     "Servicios de negocio · acompañamiento y formación"),
    (2000, 2013, 3, "right", "3.ª generación · después de 2000",
     "Incubadora internacional de negocios",
     "Soporte en red · recursos especializados y pericia"),
]


def fig_generaciones_incubadora():
    """Cada generación añade un servicio y ninguna retira el anterior."""
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    tintas = [RAMPA[0], RAMPA[1], RAMPA[2]]

    previo = None
    for (x0, x1, gen, lado, rotulo, modelo, servicio), tinta in zip(
            GENERACIONES_INCUBADORA, tintas):
        ax.hlines(gen, x0, x1, color=tinta, linewidth=7.0, capstyle="butt", zorder=3)
        if previo is not None:
            xa, ya = previo
            if xa == x0:
                ax.vlines(x0, ya, gen, color=MUTED, linewidth=1.2, zorder=2)
            else:
                ax.hlines(ya, xa, x0, color=MUTED, linewidth=1.0,
                          linestyles=(0, (2, 2)), zorder=2)
                ax.vlines(x0, ya, gen, color=MUTED, linewidth=1.0,
                          linestyles=(0, (2, 2)), zorder=2)
        previo = (x1, gen)
        # La primera generación rotula por DEBAJO de su escalón: encima, su
        # tercera línea cruza el peldaño que sube a la segunda, y el rótulo
        # colocado sobre una línea deja de leerse (METODOLOGIA.md §4.4.1).
        arriba = lado != "abajo"
        alineacion = "right" if lado == "right" else "left"
        anclaje = x1 if lado == "right" else x0
        base, paso = (gen + 0.22, 0.20) if arriba else (gen - 0.24, -0.20)
        for k, (texto, cuerpo, tinta_t, negrita) in enumerate((
                (servicio, 7.2, MUTED, "normal"),
                (modelo, 8.0, INK, "normal"),
                (rotulo, 8.4, tinta, "bold"))):
            # El rótulo lleva su propio fondo: el peldaño que sube a la tercera
            # generación arranca en el año 2000 y la descripción de la segunda
            # llega hasta 2004, así que el trazo cruzaba la palabra «formación»
            # (METODOLOGIA.md §4.4.1). Con paso fijo y rótulo de longitud
            # variable no hay anclaje que evite el cruce; se enmascara.
            ax.text(anclaje, base + k * paso, texto, ha=alineacion,
                    va="bottom" if arriba else "top", fontsize=cuerpo,
                    color=tinta_t, fontweight=negrita, zorder=5,
                    bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.0))

    ax.text(1995, 1.68, "la fuente no asigna 1990-2000\na ninguna generación",
            ha="center", va="center", fontsize=7.0, color=MUTED, linespacing=1.3,
            zorder=5, bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.0))

    ax.set_xlim(1969, 2017)
    ax.set_ylim(0.02, 4.15)
    ax.set_xticks([1980, 1990, 2000, 2010])
    ax.set_xticklabels(["1980", "1990", "2000", "2010"])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["1.ª", "2.ª", "3.ª"], fontsize=9, color=INK)
    ax.set_ylabel("Generación", fontsize=8.2, color=MUTED)
    ax.set_xlabel("Año", fontsize=8.2, color=MUTED)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s3-generaciones-incubadora")


# Dhiman y Arora (2024), Tabla 5: diez países más productivos en investigación
# sobre incubación de empresas, 1993-2022, sobre 259 artículos de Scopus. Las
# citas por artículo son el cociente de las dos columnas que publica la tabla;
# el índice h es la tercera columna, sin transformar.
# El cuarto campo coloca el rótulo en puntos de pantalla y no en unidades de
# dato: los diez nombres miden entre cinco y catorce caracteres y con
# desplazamiento fijo cuatro se pisan (METODOLOGIA.md §17.16).
PAISES_INCUBACION = [
    ("Estados Unidos", 57, 2483, 23, (-14, 8, "right", "bottom")),
    ("Reino Unido", 27, 973, 12, (0, 12, "center", "bottom")),
    ("España", 22, 306, 8, (11, 0, "left", "center")),
    ("Francia", 12, 250, 8, (0, 12, "center", "bottom")),
    ("Alemania", 13, 235, 9, (12, -2, "left", "center")),
    ("Brasil", 10, 114, 6, (11, 0, "left", "center")),
    ("India", 10, 89, 2, (-9, 0, "right", "center")),
    ("China", 10, 69, 4, (-9, -3, "right", "center")),
    ("Sudáfrica", 14, 74, 5, (11, 0, "left", "center")),
    ("Indonesia", 11, 23, 3, (11, 0, "left", "center")),
]


def fig_evidencia_incubacion():
    """La evidencia sobre incubación se produce casi toda fuera de la región."""
    fig, ax = plt.subplots(figsize=(7.0, 3.2))

    for nombre, docs, citas, h, (dx, dy, ha, va) in PAISES_INCUBACION:
        y = citas / docs
        tinta = ACCENT if nombre == "Brasil" else NAVY
        ax.scatter([docs], [y], s=9.0 * h + 22, color=tinta, alpha=0.30,
                   edgecolors=tinta, linewidths=1.2, zorder=3)
        ax.annotate(f"{nombre} · h {h}", (docs, y), textcoords="offset points",
                    xytext=(dx, dy), ha=ha, va=va, fontsize=7.4, color=INK, zorder=4)

    ax.text(65, 0.5, "el área del círculo crece con el índice h del país",
            ha="right", va="bottom", fontsize=7.0, color=MUTED)
    ax.set_xlim(0, 66)
    ax.set_ylim(-1, 50)
    ax.set_xlabel("Artículos publicados en Scopus, 1993-2022", fontsize=8.2, color=MUTED)
    ax.set_ylabel("Citas por artículo", fontsize=8.2, color=MUTED)
    ax.tick_params(labelsize=8, colors=MUTED)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.55)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s3-evidencia-incubacion")


# Avnimelech, Dushnitsky, Ellsaesser y Fitza (2024), Strategic Management
# Journal, Tabla 3, Panel A: variable dependiente, capital levantado en los 12
# meses siguientes a entrar en la aceleradora. Media del porcentaje de varianza
# explicada e intervalo posterior del 95 % entre paréntesis.
# La fila del MODELO BASE va en su propio carril, bajo un filo: es otro modelo,
# solo con el efecto de la aceleradora, y sus porcentajes no se suman con los
# del modelo completo.
VARIANZA_BASE = ("Aceleradora · modelo base", 8.92, 7.32, 10.14)
VARIANZA_COMPLETO = [
    ("Gestor del programa", 7.70, 7.46, 7.92),
    ("Cohorte", 7.51, 7.37, 7.68),
    ("Aceleradora", 3.60, 2.43, 4.71),
    ("Sector de actividad", 3.18, 1.06, 4.55),
    ("Financiamiento previo", 0.07, 0.00, 0.29),
    ("Año de entrada", 0.00, 0.00, 0.60),
]


def fig_varianza_aceleradora():
    """Al separar gestor y cohorte, el efecto de la aceleradora cae a la mitad."""
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    filas = VARIANZA_COMPLETO
    n = len(filas)

    def _rango(y, media, lo, hi, tinta):
        ax.hlines(y, lo, hi, color=tinta, linewidth=3.2, alpha=0.35,
                  capstyle="round", zorder=2)
        ax.vlines([lo, hi], y - 0.17, y + 0.17, color=tinta, linewidth=1.3, zorder=3)
        ax.plot([media], [y], "o", color=tinta, markersize=7.5, zorder=4)
        ax.text(hi + 0.30, y, f"{num(media, 1)} %", ha="left", va="center",
                fontsize=8.2, color=tinta, fontweight="bold")

    for k, (rotulo, media, lo, hi) in enumerate(filas):
        _rango(n - 1 - k, media, lo, hi,
               ACCENT if rotulo == "Aceleradora" else NAVY)

    ax.axhline(-0.70, color=GRID, linewidth=0.9)
    ax.text(0, -0.92, "Modelo base, sin gestor ni cohorte", ha="left", va="top",
            fontsize=7.2, color=MUTED)
    y_base = -1.55
    _rango(y_base, VARIANZA_BASE[1], VARIANZA_BASE[2], VARIANZA_BASE[3], MUTED)

    ax.set_yticks(list(range(n)) + [y_base])
    ax.set_yticklabels([f[0] for f in filas][::-1] + [VARIANZA_BASE[0]],
                       fontsize=8.4, color=INK)
    ax.set_xlim(0, 12.4)
    ax.set_ylim(-2.05, n - 0.35)
    ax.set_xlabel("Varianza explicada del capital levantado a 12 meses (%)",
                  fontsize=8.2, color=MUTED)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    ax.text(0.15, n - 0.42, "la línea es el intervalo posterior del 95 %",
            ha="left", va="top", fontsize=7.0, color=MUTED)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s3-varianza-aceleradora")


# Avnimelech et al. (2024), Figura 1, nota b: porcentaje de graduadas cuyo
# capital levantado es exactamente cero en cada horizonte. Son los dos únicos
# valores que la nota publica de esa distribución, y explican por qué el modelo
# necesita una Tweedie: la variable está inflada de ceros y sesgada a la derecha.
CERO_LEVANTADO = [
    ("A los 12 meses", 73, "1 350 graduadas"),
    ("A los 3 años", 39, "515 graduadas"),
]


def fig_cero_levantado():
    """La mayoría de las graduadas no levanta nada en el primer año."""
    fig, ejes = plt.subplots(1, 2, figsize=(6.6, 2.5))

    for ax, (rotulo, pct, muestra) in zip(ejes, CERO_LEVANTADO):
        ax.add_patch(Wedge((0, 0), 1.0, 0, 180, width=0.34,
                           facecolor=SURFACE, edgecolor="none"))
        ax.add_patch(Wedge((0, 0), 1.0, 180 - 1.8 * pct, 180, width=0.34,
                           facecolor=ACCENT, edgecolor="none"))
        ax.text(0, 0.10, f"{pct} %", ha="center", va="bottom", fontsize=20,
                color=ACCENT, fontweight="bold")
        ax.text(0, -0.05, "levantó cero", ha="center", va="bottom",
                fontsize=8.2, color=INK)
        ax.text(0, -0.34, rotulo, ha="center", va="top", fontsize=8.6,
                color=INK, fontweight="bold")
        ax.text(0, -0.56, muestra, ha="center", va="top", fontsize=7.4, color=MUTED)
        ax.text(-1.0, -0.06, "0 %", ha="center", va="top", fontsize=7.0, color=MUTED)
        ax.text(1.0, -0.06, "100 %", ha="center", va="top", fontsize=7.0, color=MUTED)
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-0.95, 1.15)
        ax.set_aspect("equal")
        ax.axis("off")

    escribir(fig, "s3-cero-levantado")


# Avnimelech et al. (2024), Tabla 2. Totales de la muestra de 12 meses y, en la
# segunda línea de cada nivel, los de la muestra de 3 años. Los promedios son
# los que publica la tabla, no cocientes recalculados aquí.
# El umbral de cinco observaciones por celda es el de Stavropoulos et al.
# (2015), que los propios autores citan como límite por debajo del cual la
# descomposición de varianza infla los tamaños de efecto.
ANIDAMIENTO = [
    ("Aceleradoras", 24, 17, None, None),
    ("Gestores", 69, 43, "2,88 gestores\npor aceleradora", "2,53"),
    ("Cohortes", 158, 89, "2,29 cohortes\npor gestor", "2,07"),
    ("Startups", 1350, 515, "8,54 startups\npor cohorte", "5,79"),
]


def fig_anidamiento_cohortes():
    """La cohorte es el nivel más bajo y el de menos observaciones por celda."""
    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    X = [0.0, 1.0, 2.0, 3.0]
    tintas = [MUTED, RAMPA[0], RAMPA[1], ACCENT]

    # El paso entre hojas no es decorativo: con nueve startups y paso corto los
    # puntos se funden en una barra roja (METODOLOGIA.md §4.4.1).
    # La apertura de la rama superior es 2,45 y no 2,80: con 2,80 el nodo de
    # arriba subía hasta la línea de base del rótulo de la figura y se lo comía.
    ax.plot([X[0]], [0], "o", color=tintas[0], markersize=10, zorder=4)
    for y in (-2.45, 0.0, 2.45):
        ax.plot([X[0], X[0], X[1]], [0, y, y], color=GRID, linewidth=1.2, zorder=1)
        ax.plot([X[1]], [y], "o", color=tintas[1], markersize=8, zorder=4)
    for y in (-1.15, 1.15):
        ax.plot([X[1], X[1], X[2]], [0, y, y], color=GRID, linewidth=1.2, zorder=1)
        ax.plot([X[2]], [y], "o", color=tintas[2], markersize=7.5, zorder=4)
    hojas = [1.15 + (i - 4) * 0.30 for i in range(9)]
    ax.plot([X[2], 2.55], [1.15, 1.15], color=GRID, linewidth=1.2, zorder=1)
    ax.plot([2.55, 2.55], [hojas[0], hojas[-1]], color=GRID, linewidth=1.2, zorder=1)
    for y in hojas:
        ax.plot([2.55, X[3]], [y, y], color=GRID, linewidth=0.9, zorder=1)
        ax.plot([X[3]], [y], "o", color=tintas[3], markersize=4.8, zorder=4)

    for x, (rotulo, doce, tres, promedio, prom3), tinta in zip(X, ANIDAMIENTO, tintas):
        ax.text(x, 4.60, rotulo, ha="center", va="bottom", fontsize=8.8,
                color=tinta, fontweight="bold")
        ax.text(x, 3.92, num(doce, 0), ha="center", va="bottom", fontsize=12,
                color=INK, fontweight="bold")
        ax.text(x, 3.62, f"{num(tres, 0)} a 3 años", ha="center", va="bottom",
                fontsize=7.0, color=MUTED)
        if promedio:
            ax.text(x - 0.5, -3.58, promedio, ha="center", va="top",
                    fontsize=7.6, color=INK, linespacing=1.3)
            ax.text(x - 0.5, -4.42, f"{prom3} a 3 años", ha="center", va="top",
                    fontsize=7.0, color=MUTED)

    ax.hlines(-3.34, -0.15, 3.15, color=GRID, linewidth=0.8)
    ax.text(1.5, -4.86, "Umbral de escasez de datos: cinco observaciones por celda "
            "(Stavropoulos et al., 2015)", ha="center", va="top",
            fontsize=7.2, color=WARN)
    ax.text(1.5, 3.36, "una rama por nivel, dibujada con la ramificación media",
            ha="center", va="top", fontsize=7.0, color=MUTED)
    ax.set_xlim(-0.42, 3.42)
    ax.set_ylim(-5.35, 5.25)
    ax.axis("off")
    escribir(fig, "s3-anidamiento-cohortes")


# Canfield Rivera (2021), Multidisciplinary Business Review 14(1), Tablas 6 y 8.
# Razón de momios de los siete factores de Sharir y Lerner sobre el desempeño de
# 15 417 empresas lucrativas de la base GALI, en tres modelos: general, resto del
# mundo y América Latina. La significación es la que declara cada tabla al 5 %.
# En el modelo del resto del mundo la prueba de mercado y la base de capital
# empatan en 1,32: la tabla no las desempata y aquí tampoco se desempatan.
FACTORES_GALI = [
    ("Base de capital inicial", (1.32, True), (1.32, True), (1.21, True)),
    ("Prueba de mercado", (1.25, True), (1.32, True), (1.12, False)),
    ("Experiencia directiva previa", (1.23, True), (1.23, True), (1.23, True)),
    ("Aceptación pública de la idea", (1.17, True), (1.14, False), (1.04, False)),
    ("Dedicación de los fundadores", (1.09, False), (1.17, True), (1.14, True)),
    ("Red social del emprendedor", (0.94, True), (0.91, True), (1.02, False)),
    ("Composición del equipo", (0.92, True), (1.06, False), (1.01, False)),
]
MODELOS_GALI = [(0.0, "Modelo general", "15 417 empresas"),
                (1.75, "Resto del mundo", "66 % de la muestra"),
                (3.50, "América Latina", "34 % de la muestra")]
DESTACADOS_GALI = ("Prueba de mercado", "Experiencia directiva previa")


def fig_factores_gali():
    """El orden de los factores cambia al estimar el modelo solo en la región."""
    fig, ax = plt.subplots(figsize=(7.8, 3.4))
    n = len(FACTORES_GALI)
    xs = [m[0] for m in MODELOS_GALI]

    puestos, empates = [], {}
    for col in range(3):
        valores = sorted(((f[col + 1][0], i) for i, f in enumerate(FACTORES_GALI)),
                         reverse=True)
        rango, k = {}, 0
        while k < len(valores):
            iguales = [i for v, i in valores if v == valores[k][0]]
            medio = k + (len(iguales) - 1) / 2
            for j, i in enumerate(iguales):
                rango[i] = (medio + (j - (len(iguales) - 1) / 2) * 0.52,
                            len(iguales) > 1)
            if len(iguales) > 1:
                empates[col] = (medio, valores[k][0])
            k += len(iguales)
        puestos.append(rango)

    for i, fila in enumerate(FACTORES_GALI):
        ys = [puestos[c][i][0] for c in range(3)]
        tinta = ACCENT if fila[0] in DESTACADOS_GALI else NAVY
        ax.plot(xs, ys, color=tinta, linewidth=2.0,
                alpha=0.9 if tinta == ACCENT else 0.42, zorder=2)
        for c in range(3):
            valor, signif = fila[c + 1]
            ax.plot([xs[c]], [ys[c]], "o", markersize=8.5, zorder=4,
                    markerfacecolor=tinta if signif else PAPER,
                    markeredgecolor=tinta, markeredgewidth=1.6)
            if not puestos[c][i][1]:
                ax.annotate(num(valor), (xs[c], ys[c]),
                            textcoords="offset points", xytext=(0, 9),
                            ha="center", va="bottom", fontsize=7.0, color=MUTED)
        ax.text(xs[0] - 0.14, ys[0], fila[0], ha="right", va="center",
                fontsize=8.0, color=INK)
        ax.text(xs[2] + 0.14, ys[2], fila[0], ha="left", va="center",
                fontsize=8.0, color=INK)

    # El rótulo del empate va ENCIMA del par: a su izquierda cae justo sobre el
    # cruce de las dos líneas que llegan a los nodos empatados, y un rótulo por
    # nodo se pisa con el de la fila siguiente.
    for col, (medio, valor) in empates.items():
        ax.text(xs[col], medio - 0.62, f"{num(valor)} · empate", ha="center",
                va="bottom", fontsize=7.0, color=MUTED)

    for x, nombre, detalle in MODELOS_GALI:
        ax.text(x, -1.32, nombre, ha="center", va="bottom", fontsize=8.2,
                color=INK, fontweight="bold")
        ax.text(x, -1.06, detalle, ha="center", va="bottom", fontsize=7.2, color=MUTED)

    # El eje va invertido y el desplazamiento del rótulo se mide en PUNTOS de
    # pantalla: xytext=(0, 9) deja la cifra ENCIMA del punto, no debajo. La
    # leyenda decía «bajo cada punto» y mandaba a mirar donde no estaba.
    ax.text(xs[1], n - 0.10, "círculo lleno, significativo al 5 %; hueco, no "
            "significativo · sobre cada punto, la razón de momios",
            ha="center", va="bottom", fontsize=7.0, color=MUTED)
    ax.set_xlim(-2.55, 6.05)
    ax.set_ylim(n + 0.05, -1.68)
    ax.axis("off")
    escribir(fig, "s3-factores-gali")


# Skalicka, Zinecker, Balcerzak y Pietrzak, Economic Research-Ekonomska
# Istraživanja 36(1):25-50, Tablas 2 y 3. La diagonal lleva la frecuencia con
# que cada motivo aparece entre los 31 inversores; el triángulo superior, el
# coeficiente de correlación entre motivos. Valor crítico 0,36 al 5 %, dos colas.
# Los tres signos negativos se leyeron del PDF con pdfplumber: el extractor de
# texto plano los pierde y deja B-D en 0,02 cuando es -0,02.
# Son DOS magnitudes distintas en una misma rejilla y por eso llevan tinta
# distinta: la frecuencia en rojo y la correlación en azul.
MOTIVOS_RECHAZO = [
    ("A", "Desconfianza en el emprendedor", 83.87),
    ("B", "Sector o proyecto que no entiende", 51.61),
    ("C", "Proyecto mal concebido", 58.06),
    ("D", "Proyecto en crisis existencial", 32.26),
    ("E", "Aporte propio insuficiente", 77.42),
]
CORRELACIONES_RECHAZO = {
    (0, 1): 0.10, (0, 2): 0.52, (0, 3): 0.30, (0, 4): 0.60,
    (1, 2): 0.09, (1, 3): -0.02, (1, 4): -0.21,
    (2, 3): 0.17, (2, 4): 0.32,
    (3, 4): 0.37,
}
CRITICO_RECHAZO = 0.36


def _coef(valor):
    """Correlación con dos decimales fijos y signo menos tipográfico."""
    return f"{valor:.2f}".replace("-", "−").replace(".", ",")


def fig_rechazo_matriz():
    """Desconfianza y aporte propio son los dos motivos que aparecen juntos."""
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    n = len(MOTIVOS_RECHAZO)

    def _celda(x, y, tinta, opacidad, filo, grosor):
        # El relleno y el filo van en DOS parches: con un solo parche y alpha,
        # matplotlib aplica la transparencia también al borde, y el borde que
        # marca la significación quedaba tan claro como el de las celdas que no
        # la tienen. La leyenda prometía una marca que no se veía.
        ax.add_patch(Rectangle((x - 0.46, y - 0.42), 0.92, 0.84,
                               facecolor=tinta, alpha=opacidad, edgecolor="none"))
        ax.add_patch(Rectangle((x - 0.46, y - 0.42), 0.92, 0.84,
                               facecolor="none", edgecolor=filo, linewidth=grosor))

    for i in range(n):
        for j in range(i, n):
            x, y = j, n - 1 - i
            if i == j:
                pct = MOTIVOS_RECHAZO[i][2]
                _celda(x, y, ACCENT, 0.12 + 0.55 * pct / 100, ACCENT, 1.0)
                ax.text(x, y, f"{num(pct, 1)} %", ha="center", va="center",
                        fontsize=8.6, color=INK, fontweight="bold")
            else:
                r = CORRELACIONES_RECHAZO[(i, j)]
                signif = abs(r) >= CRITICO_RECHAZO
                _celda(x, y, NAVY, 0.08 + 0.42 * abs(r),
                       NAVY if signif else GRID, 2.0 if signif else 0.6)
                ax.text(x, y, _coef(r), ha="center", va="center", fontsize=8.4,
                        color=INK, fontweight="bold" if signif else "normal")

    for i, (letra, nombre, _) in enumerate(MOTIVOS_RECHAZO):
        ax.text(-0.66, n - 1 - i, f"{letra} · {nombre}", ha="right", va="center",
                fontsize=8.0, color=INK)
        ax.text(i, n - 0.44, letra, ha="center", va="bottom", fontsize=8.6,
                color=MUTED, fontweight="bold")

    ax.text(-3.95, -0.88, "Diagonal en rojo: de los 31 inversores, los que declaran "
            "el motivo.", ha="left", va="center", fontsize=7.0, color=MUTED)
    ax.text(-3.95, -1.20, "Celdas en azul: correlación entre motivos; con borde "
            "marcado, significativa al 5 % por encima de 0,36.",
            ha="left", va="center", fontsize=7.0, color=MUTED)
    ax.set_xlim(-4.05, n - 0.35)
    ax.set_ylim(-1.58, n - 0.02)
    ax.axis("off")
    escribir(fig, "s3-rechazo-matriz")


# Dos series de inversión anual en capital de riesgo, cada una con SUS años y su
# fuente, y una banda de referencia:
#   LAVCA, recogido por Leslie, Beecher y Swaby (2025): unos 500 millones de
#     dólares en 2015 y un máximo de 15 700 millones en 2021.
#   BID, Peña y Jenik (2023): 96 millones en 2020 y 172 millones en 2022 en
#     deep tech, las mismas cifras que verifica la sesión 2.
#   CEPAL (2021), recogido por Leslie et al.: menos de 50 millones al año en
#     todo el Caribe.
# Ninguna de las dos fuentes publica la serie intermedia, así que el tramo entre
# dos valores va punteado y sin nivel rotulado (METODOLOGIA.md §17.15).
SERIES_CAPITAL = [
    ("Capital de riesgo, América Latina", NAVY, [(2015, 500), (2021, 15700)], 1.42),
    ("Capital de riesgo en deep tech", ACCENT, [(2020, 96), (2022, 172)], 0.62),
]
TECHO_CARIBE = 50


def fig_escala_capital_region():
    """Tres órdenes de magnitud separan el total regional del capital caribeño."""
    fig, ax = plt.subplots(figsize=(7.4, 2.9))

    ax.axhspan(30, TECHO_CARIBE, color=WARN, alpha=0.14, zorder=0)
    ax.text(2014.6, TECHO_CARIBE * 1.10, "el Caribe entero: menos de 50 millones al año",
            ha="left", va="bottom", fontsize=7.2, color=WARN)

    for nombre, tinta, puntos, dy in SERIES_CAPITAL:
        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]
        ax.plot(xs, ys, color=tinta, linewidth=1.3, linestyle=(0, (3, 3)), zorder=2)
        for x, y in puntos:
            ax.hlines(y, x - 0.32, x + 0.32, color=tinta, linewidth=4.2,
                      capstyle="butt", zorder=3)
            ax.text(x, y * 1.32, num(y, 0), ha="center", va="bottom",
                    fontsize=8.2, color=tinta, fontweight="bold")
        ax.text(xs[-1] + 0.55, ys[-1] * dy, nombre, ha="left", va="center",
                fontsize=8.0, color=tinta)

    ax.set_yscale("log")
    ax.set_xlim(2014.3, 2026.4)
    ax.set_ylim(30, 60000)
    ax.set_xticks([2015, 2017, 2019, 2021, 2023])
    ax.set_yticks([50, 100, 500, 1000, 5000, 15000])
    ax.set_yticklabels(["50", "100", "500", "1 000", "5 000", "15 000"])
    ax.set_ylabel("Millones de dólares al año", fontsize=8.2, color=MUTED)
    ax.set_xlabel("Escala logarítmica · el trazo punteado une dos valores publicados, "
                  "sin serie intermedia", fontsize=7.6, color=MUTED)
    ax.tick_params(labelsize=8, colors=MUTED)
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.55)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s3-escala-capital-region")


# Goffe, Hammersley y Rustom (2021), Banco Mundial, Tabla 1: porcentaje máximo
# de garantía declarado por diecinueve economías del G-20 y la Unión Europea.
# Australia figura en la tabla pero no opera esquema y queda fuera del recuento.
# Canadá, China y México publican varias razones según el tramo o el programa y
# aquí se cuenta la mayor, que es la que la propia tabla titula.
COBERTURAS_G20 = [
    ("España", 50), ("Francia", 70), ("Alemania", 70), ("Rusia", 70),
    ("Argentina", 75), ("India", 75), ("Reino Unido", 75), ("Unión Europea", 75),
    ("Brasil", 80), ("Indonesia", 80), ("Italia", 80), ("Japón", 80), ("México", 80),
    ("Canadá", 85), ("Corea del Sur", 85), ("Estados Unidos", 85),
    ("Sudáfrica", 90), ("China", 100), ("Turquía", 100),
]
LATINOAMERICANAS = {"Argentina", "Brasil", "México"}
BORDES_G20 = [45, 55, 65, 75, 85, 95, 105]


def fig_cobertura_g20():
    """Nueve de las diecinueve economías cubren entre el 75 % y el 84 %."""
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    latam = [v for nombre, v in COBERTURAS_G20 if nombre in LATINOAMERICANAS]
    resto = [v for nombre, v in COBERTURAS_G20 if nombre not in LATINOAMERICANAS]

    ax.axvspan(50, 80, color=NAVY, alpha=0.08, zorder=0)
    ax.hist([resto, latam], bins=BORDES_G20, stacked=True, histtype="bar",
            color=[NAVY, ACCENT], edgecolor=PAPER, linewidth=1.0, rwidth=0.9,
            zorder=3, label=["Las otras dieciséis economías",
                             "Argentina, Brasil y México"])

    conteo, _ = np.histogram([v for _, v in COBERTURAS_G20], bins=BORDES_G20)
    for c, (a, b) in zip(conteo, zip(BORDES_G20[:-1], BORDES_G20[1:])):
        if c:
            ax.text((a + b) / 2, c + 0.22, f"{c}", ha="center", va="bottom",
                    fontsize=8.8, color=INK, fontweight="bold")

    ax.text(60, 11.2, "banda típica: 50 % a 80 %", ha="center", va="bottom",
            fontsize=7.4, color=NAVY)
    ax.set_xlim(44, 106)
    ax.set_ylim(0, 12.8)
    ax.set_xticks([50, 60, 70, 80, 90, 100])
    ax.set_xticklabels([f"{v} %" for v in (50, 60, 70, 80, 90, 100)])
    ax.set_xlabel("Porcentaje máximo del crédito que cubre la garantía",
                  fontsize=8.2, color=MUTED)
    ax.set_ylabel("Economías", fontsize=8.2, color=MUTED)
    ax.set_yticks([0, 3, 6, 9])
    ax.tick_params(labelsize=8, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.55)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=7.4, frameon=False, handlelength=1.1,
              borderaxespad=0.1)
    limpiar_ejes(ax)
    escribir(fig, "s3-cobertura-g20")


# Goffe et al. (2021), Tabla 2, con datos de Saadani, Arvai y Rocha (2011).
# Razones de cobertura mínima, mediana y máxima de los esquemas de ocho
# economías de Oriente Medio y el norte de África. Es la única tabla de las seis
# fuentes que publica el reparto DENTRO de una misma economía, y por eso está
# aquí: enseña que un esquema opera varias coberturas a la vez.
COBERTURA_MENA = [
    ("Emiratos Árabes Unidos", 90, 90, 90),
    ("Líbano", 75, 82.5, 90),
    ("Iraq", 75, 75, 75),
    ("Jordania", 70, 70, 70),
    ("Túnez", 60, 67.5, 75),
    ("Marruecos", 50, 65, 80),
    ("Egipto", 50, 60, 70),
    ("Palestina", 60, 60, 60),
]


def fig_rango_cobertura_mena():
    """Cuatro de las ocho economías operan varias razones de cobertura a la vez."""
    fig, ax = plt.subplots(figsize=(6.9, 3.1))
    n = len(COBERTURA_MENA)

    ax.axvspan(50, 80, color=NAVY, alpha=0.07, zorder=0)
    for k, (nombre, mn, med, mx) in enumerate(COBERTURA_MENA):
        y = n - 1 - k
        tinta = ACCENT if mx > mn else MUTED
        ax.hlines(y, mn, mx, color=tinta, linewidth=3.4, alpha=0.32,
                  capstyle="round", zorder=2)
        ax.vlines([mn, mx], y - 0.18, y + 0.18, color=tinta, linewidth=1.3, zorder=3)
        ax.plot([med], [y], "o", color=tinta, markersize=7.0, zorder=4)
        if mx > mn:
            ax.text(mn - 1.4, y, num(mn, 0), ha="right", va="center",
                    fontsize=7.6, color=MUTED)
            ax.text(mx + 1.4, y, f"{num(mx, 0)} %", ha="left", va="center",
                    fontsize=8.0, color=tinta, fontweight="bold")
        else:
            ax.text(mx + 1.4, y, f"{num(mx, 0)} % · razón única", ha="left",
                    va="center", fontsize=7.8, color=MUTED)

    ax.set_yticks(range(n))
    ax.set_yticklabels([e[0] for e in COBERTURA_MENA][::-1], fontsize=8.2, color=INK)
    ax.set_xlim(42, 108)
    ax.set_ylim(-1.55, n - 0.30)
    ax.set_xticks([50, 60, 70, 80, 90, 100])
    ax.set_xticklabels([f"{v} %" for v in (50, 60, 70, 80, 90, 100)])
    ax.set_xlabel("Razón de cobertura del esquema (%) · el punto es la mediana",
                  fontsize=8.0, color=MUTED)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    ax.text(42, -1.20, "banda sombreada: el 50 % a 80 % que el informe considera "
            "típico a escala global", ha="left", va="center", fontsize=7.0, color=MUTED)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s3-rango-cobertura-mena")


# Goffe et al. (2021), Figura 3, con la encuesta global de Calice (2016).
# Apalancamiento: garantías vigentes divididas entre el capital del esquema.
# Mora: garantías incumplidas sobre garantías vigentes. Pymes atendidas: número
# medio de pymes por esquema de la región. El punto de referencia son los
# promedios de todos los esquemas encuestados, dibujados como cruz y no como
# burbuja: dentro de la burbuja de Asia no se veía.
GARANTIAS_REGION = [
    ("África", 1.7, 17.1, 77, (13, -4, "left", "top")),
    ("Asia", 3.2, 1.2, 17293, (22, -2, "left", "center")),
    ("Europa", 3.8, 2.9, 1139, (0, 16, "center", "bottom")),
    ("Oriente Medio y\nnorte de África", 4.4, 3.8, 829, (12, 6, "left", "bottom")),
    ("Hemisferio occidental", 3.0, 2.0, 6531, (-26, 22, "right", "bottom")),
]
GARANTIAS_PROMEDIO = (3.3, 2.5, 1383)


def fig_garantias_region():
    """El hemisferio occidental atiende más pymes por esquema con mora baja."""
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    x_prom, y_prom, _ = GARANTIAS_PROMEDIO

    ax.axvline(x_prom, color=GRID, linewidth=1.0, linestyle=(0, (3, 3)), zorder=1)
    ax.axhline(y_prom, color=GRID, linewidth=1.0, linestyle=(0, (3, 3)), zorder=1)
    ax.text(x_prom + 0.06, 19.8, "promedio de todos los esquemas:\n3,3 veces y 2,5 % "
            "de mora", ha="left", va="top", fontsize=7.0, color=MUTED, linespacing=1.35)

    def _area(pymes):
        return 45 + 830 * np.sqrt(pymes) / np.sqrt(17293)

    for nombre, x, y, pymes, (dx, dy, ha, va) in GARANTIAS_REGION:
        tinta = ACCENT if nombre == "Hemisferio occidental" else NAVY
        ax.scatter([x], [y], s=_area(pymes), color=tinta, alpha=0.28,
                   edgecolors=tinta, linewidths=1.3, zorder=4)
        ax.annotate(nombre, (x, y), textcoords="offset points", xytext=(dx, dy),
                    ha=ha, va=va, fontsize=7.9, color=INK, zorder=5, linespacing=1.3)
        lineas = nombre.count("\n") + 1
        # El recuento se aparta del nombre HACIA FUERA del punto. Con el rótulo
        # centrado («Asia») el recuento subía y caía a la vez sobre la línea del
        # promedio y sobre la burbuja de Europa (METODOLOGIA.md §4.4.1): el
        # anclaje centrado se trata como el superior y el recuento baja.
        salto = (-11 if va in ("top", "center") else 11) * lineas
        ax.annotate(f"{num(pymes, 0)} pymes por esquema", (x, y),
                    textcoords="offset points", xytext=(dx, dy + salto),
                    ha=ha, va=va, fontsize=6.9, color=MUTED, zorder=5)

    ax.set_xlim(1.15, 5.15)
    ax.set_ylim(-2.6, 20.5)
    ax.set_xlabel("Apalancamiento: garantías vigentes sobre capital del esquema (veces)",
                  fontsize=8.0, color=MUTED)
    ax.set_ylabel("Tasa de mora de las garantías (%)", fontsize=8.0, color=MUTED)
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.tick_params(labelsize=8, colors=MUTED)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.text(1.20, 19.8, "el área del círculo crece con las\npymes atendidas por esquema",
            ha="left", va="top", fontsize=7.0, color=MUTED, linespacing=1.35)
    limpiar_ejes(ax)
    escribir(fig, "s3-garantias-region")


FIGURAS += [fig_generaciones_incubadora, fig_evidencia_incubacion,
            fig_varianza_aceleradora, fig_cero_levantado,
            fig_anidamiento_cohortes, fig_factores_gali, fig_rechazo_matriz,
            fig_escala_capital_region, fig_cobertura_g20,
            fig_rango_cobertura_mena, fig_garantias_region]


# ==========================================================================
# SESIÓN 3 · tres láminas que pasaron de texto seguido a figura
# ==========================================================================

# Skalicka et al. (2022), 36(1):25-50, Tabla 8. Proporción de propuestas que
# superan el tamizaje del inversor ángel según la etapa del proyecto. Las tres
# etapas son las que declara el artículo; el orden es el del ciclo, no el de la
# tabla, para que se lea el descenso.
ANGEL_ETAPA = [
    ("Semilla o puesta en marcha", 48),
    ("Emergente", 84),
    ("Expansión", 77),
]


def fig_angel_etapa():
    """Aceptación de propuestas por etapa del proyecto."""
    # Barras en columna con la cifra al final, no barras verticales: los tres
    # rótulos pasan de ocho caracteres y en vertical se solaparían (§4.4.1).
    # El orden es el del CICLO del proyecto, no el de la tabla ni el del valor:
    # la serie no desciende (48, 84 y 77) y ordenarla por valor escondería que
    # la etapa más temprana es la que menos pasa.
    fig, ax = plt.subplots(figsize=(6.6, 2.3))
    minimo = min(v for _, v in ANGEL_ETAPA)
    ys = list(range(len(ANGEL_ETAPA) - 1, -1, -1))
    for y, (nom, v) in zip(ys, ANGEL_ETAPA):
        ax.barh(y, v, color=ACCENT if v == minimo else NAVY, height=0.55)
        ax.text(v + 1.5, y, f"{num(v, 0)} %", ha="left", va="center",
                fontsize=8.6, color=INK, fontweight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([n for n, _ in ANGEL_ETAPA], fontsize=8.4)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Propuestas que superan el tamizaje (%)", fontsize=8.0, color=MUTED)
    ax.tick_params(axis="y", labelsize=8.4, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8.0, colors=MUTED, length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "s3-angel-etapa")


# Leslie et al. (2025), BID, encuesta a fundadores del Caribe. Tres
# proporciones sobre la misma población, de la intención al hecho.
CAPITAL_BRECHA = [
    ("Declara\ninterés", 79.3),
    ("Ha\nlevantado", 27.5),
    ("Busca capital\nde riesgo", 17.0),
]


def fig_capital_brecha():
    """Del interés declarado por el capital al capital efectivamente levantado."""
    # Escalones descendentes y no embudo: el embudo ya se usa dos veces en el
    # mazo y aquí las tres cifras son proporciones de la misma población, no
    # etapas por las que pasa un mismo caso.
    fig, ax = plt.subplots(figsize=(6.8, 2.5))
    for i, (nom, v) in enumerate(CAPITAL_BRECHA):
        ax.add_patch(Rectangle((i, 0), 0.78, v, facecolor=ACCENT if i == 0 else NAVY,
                               alpha=0.85 if i == 0 else 0.75, edgecolor="none"))
        ax.text(i + 0.39, v + 3, f"{num(v, 1)} %", ha="center", va="bottom",
                fontsize=9.0, color=INK, fontweight="bold")
        ax.text(i + 0.39, -4, nom, ha="center", va="top", fontsize=7.8,
                color=MUTED, linespacing=1.4)
        if i:
            previo = CAPITAL_BRECHA[i - 1][1]
            ax.annotate("", xy=(i + 0.02, v + 1), xytext=(i - 0.24, previo + 1),
                        arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.1))
    ax.set_xlim(-0.35, len(CAPITAL_BRECHA) - 0.05)
    ax.set_ylim(-34, 96)
    ax.set_ylabel("Fundadores encuestados (%)", fontsize=8.2, color=MUTED)
    ax.set_xticks([])
    # El hueco de abajo es donde caben los rótulos, no parte de la escala: sin
    # acotar marcas y eje, el lienzo enseñaba una raya en «−20 %» de fundadores
    # encuestados, que es una escala inventada (METODOLOGIA.md §17.15).
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.spines["left"].set_bounds(0, 80)
    ax.tick_params(axis="y", labelsize=8.0, colors=MUTED, length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "bottom"))
    escribir(fig, "s3-capital-brecha")


# Avnimelech et al. (2024), base GALI. Composición de la submuestra: cuatro
# proporciones sobre el mismo conjunto de 15 417 empresas.
MUESTRA_GALI = [
    ("En América Latina", 34),
    ("Con tres años o más", 28),
    ("Declara ingresos", 52),
    ("Tiene empleados", 78),
]
MUESTRA_GALI_TOTAL = 15417


def fig_muestra_gali():
    """Composición de la submuestra de empresas aceleradas."""
    # Waffle no: ya se usa. Barras apiladas contra el total, con la parte que
    # cumple y la que no, para que se vea que son cuatro cortes del MISMO
    # conjunto y no cuatro grupos distintos.
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    ys = list(range(len(MUESTRA_GALI) - 1, -1, -1))
    for y, (nom, v) in zip(ys, MUESTRA_GALI):
        ax.barh(y, v, color=NAVY, height=0.56)
        ax.barh(y, 100 - v, left=v, color=GRID, alpha=0.45, height=0.56)
        ax.text(v - 1.5, y, f"{num(v, 0)} %", ha="right", va="center",
                fontsize=8.6, color=PAPER, fontweight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([n for n, _ in MUESTRA_GALI], fontsize=8.4)
    ax.set_xlim(0, 100)
    ax.set_xlabel(f"Porcentaje de las {num(MUESTRA_GALI_TOTAL, 0)} empresas de la submuestra",
                  fontsize=8.0, color=MUTED)
    ax.tick_params(axis="y", labelsize=8.4, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=8.0, colors=MUTED, length=0)
    limpiar_ejes(ax, ocultar=("top", "right", "left", "bottom"))
    escribir(fig, "s3-muestra-gali")


FIGURAS += [fig_angel_etapa, fig_capital_brecha, fig_muestra_gali]


# Bases de convocatoria de ProInnóvate y PROCIENCIA. Los tres filtros de
# admisibilidad, en el orden en que se comprueban, con el documento que
# acredita cada uno. No hay magnitudes: la figura ordena un procedimiento, y
# por eso lleva el documento dentro de cada compuerta en vez de un valor.
ADMISIBILIDAD_FILTROS = [
    ("Figura del postulante", "Ficha RUC y estatuto o convenio"),
    ("Tramo de madurez declarado", "Informe de ensayo o acta con fecha"),
    ("Contrapartida comprometida", "Carta de compromiso con cuenta y monto"),
]


def fig_admisibilidad_filtros():
    """Los tres filtros de admisibilidad y el documento que acredita cada uno."""
    # Carril de comprobación y no embudo: el embudo ya se usa dos veces en el
    # mazo y además supone pérdida proporcional, que aquí no existe. Una
    # propuesta pasa los tres o se detiene en el primero que falla, y eso es
    # un carril con tres compuertas.
    fig, ax = plt.subplots(figsize=(8.4, 2.2))
    ANCHO, HUECO = 2.35, 0.62
    ax.annotate("", xy=(3 * (ANCHO + HUECO) - HUECO + 0.55, 1.05),
                xytext=(-0.45, 1.05),
                arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.4))
    ax.text(-0.45, 1.28, "Propuesta presentada", fontsize=7.4, color=MUTED,
            ha="left", va="bottom")
    for k, (filtro, doc) in enumerate(ADMISIBILIDAD_FILTROS):
        x = k * (ANCHO + HUECO)
        ax.add_patch(Rectangle((x, 0.30), ANCHO, 1.50, facecolor=NAVY, alpha=0.10,
                               edgecolor=NAVY, linewidth=1.3))
        ax.text(x + 0.16, 1.52, f"{k + 1}", fontsize=8.0, color=NAVY,
                fontweight="bold", ha="left", va="center")
        # El rótulo se parte a la anchura de SU compuerta. Sin partirlo,
        # «Tramo de madurez declarado» y el documento que lo acredita se
        # salían de la caja y se montaban sobre la compuerta siguiente
        # (METODOLOGIA.md §4.4.1: un rótulo que cruza su caja está fuera).
        ax.text(x + 0.48, 1.52, textwrap.fill(filtro, 24), fontsize=8.0, color=INK,
                fontweight="bold", ha="left", va="center", linespacing=1.35)
        ax.text(x + 0.16, 1.06, "se acredita con", fontsize=6.6, color=MUTED,
                ha="left", va="center")
        ax.text(x + 0.16, 0.66, textwrap.fill(doc, 22), fontsize=7.2, color=NAVY,
                ha="left", va="center", linespacing=1.4)
        ax.text(x + ANCHO / 2, 0.06, "no admisible: no se lee", fontsize=6.8,
                color=ACCENT, ha="center", va="center")
        ax.annotate("", xy=(x + ANCHO / 2, 0.20), xytext=(x + ANCHO / 2, 0.30),
                    arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.0))
    ax.text(3 * (ANCHO + HUECO) - HUECO + 0.15, 1.05, "Evaluación\ntécnica",
            fontsize=8.0, color=OK, fontweight="bold", ha="left", va="center",
            linespacing=1.3)
    ax.set_xlim(-0.55, 3 * (ANCHO + HUECO) - HUECO + 1.65)
    ax.set_ylim(-0.10, 1.90)
    ax.axis("off")
    escribir(fig, "s3-admisibilidad-filtros")


FIGURAS += [fig_admisibilidad_filtros]

# ==========================================================================
# SESIÓN 3 · el catálogo de financiamiento
# ==========================================================================
# Cuatro figuras que la ficha de fondo no puede dar: la ficha describe UN
# fondo y estas cuatro describen el conjunto. Son las únicas de la sesión que
# comparan familias entre sí.

# Elaboración propia sobre las veintitrés fichas de la sesión. El eje es el
# momento del proyecto, que es el orden en que un equipo se topa con cada
# familia, y no el tamaño del cheque.
ETAPA_FONDO = [
    ("Idea sin empresa", ["Premios y hackatones", "Preincubación", "Fondos de cultura"]),
    ("Prototipo", ["StartUp Perú", "PROCIENCIA", "Red CITE en especie"]),
    ("Producto con usuario", ["ProInnóvate", "Aceleradoras", "PROCOMPITE y AGROIDEAS"]),
    ("Ventas y escala", ["Inversores ángeles", "Capital de riesgo", "Ley 30309"]),
    ("Programa plurianual", ["Cooperación bilateral", "Banca multilateral", "Fondos climáticos"]),
]


def fig_etapa_fondo():
    """A cada momento del proyecto le corresponde una familia de fondos distinta."""
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for i, (etapa, familias) in enumerate(ETAPA_FONDO):
        color = RAMPA[min(i, len(RAMPA) - 1)] if i < 3 else ACCENT
        ax.barh(i, 1, height=0.62, color=color, alpha=0.16, edgecolor=color, linewidth=1.2)
        ax.text(0.015, i + 0.2, etapa, fontsize=8.6, color=INK, fontweight="bold", va="center")
        ax.text(0.015, i - 0.16, " · ".join(familias), fontsize=7.8, color=MUTED, va="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, len(ETAPA_FONDO) - 0.35)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s3-etapa-fondo")


# Elaboración propia sobre las fichas. Lo que un fondo pide a cambio ordena el
# catálogo mejor que el monto: decide si el proyecto puede aceptarlo.
QUE_PIDE = [
    ("Premios y concursos", 0, "Nada: es premio"),
    ("Fondos públicos", 1, "Contrapartida y rendición"),
    ("Cooperación y filantropía", 1, "Reporte de resultados"),
    ("Incubadoras", 1, "Dedicación del equipo"),
    ("Aceleradoras", 2, "Participación accionaria"),
    ("Inversores ángeles", 2, "Participación y consejo"),
    ("Capital de riesgo", 3, "Participación, consejo y salida"),
]


def fig_que_pide():
    """Lo que cada familia pide a cambio, que es lo que decide si se puede aceptar."""
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    colores = [OK, RAMPA[1], ACCENT, ACCENT]
    for i, (familia, nivel, detalle) in enumerate(QUE_PIDE):
        c = colores[nivel]
        ax.barh(i, nivel + 0.35, height=0.5, color=c, alpha=0.75, zorder=3)
        ax.text(-0.08, i, familia, ha="right", va="center", fontsize=8.2, color=INK)
        ax.text(nivel + 0.48, i, detalle, ha="left", va="center", fontsize=7.6, color=MUTED)
    ax.set_xlim(0, 4.4)
    ax.set_ylim(-0.7, len(QUE_PIDE) - 0.3)
    ax.invert_yaxis()
    ax.set_yticks([])
    ax.set_xticks([0.35, 1.35, 2.35, 3.35])
    ax.set_xticklabels(["nada", "compromiso", "participación", "control"],
                       fontsize=7.6, color=MUTED)
    ax.tick_params(length=0)
    ax.grid(True, axis="x", color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s3-que-pide")


# «Radiografía del financiamiento social» (Fondos y Convocatorias, 2025). La
# estacionalidad no es caprichosa: sigue el año fiscal, el curso académico y el
# calendario de las conferencias climáticas.
CALENDARIO_FONDOS = [
    ("Programas públicos", 5, 9),
    ("Agencias de cooperación", 8, 11),
    ("Universidades y becas", 9, 12),
    ("Fondos climáticos", 10, 13),
    ("Premios culturales", 11, 13),
]


def fig_calendario_fondos():
    """Cada familia abre en su propia temporada, y no se solapan por casualidad."""
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    for i, (familia, ini, fin) in enumerate(CALENDARIO_FONDOS):
        ax.barh(i, fin - ini, left=ini, height=0.52, color=RAMPA[i % len(RAMPA)],
                alpha=0.8, zorder=3)
        ax.text(ini - 0.25, i, familia, ha="right", va="center", fontsize=8.2, color=INK)
    ax.set_xlim(-4.5, 13.4)
    ax.set_ylim(-0.7, len(CALENDARIO_FONDOS) - 0.3)
    ax.invert_yaxis()
    ax.set_yticks([])
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
                       fontsize=7.8, color=MUTED)
    ax.tick_params(length=0)
    ax.grid(True, axis="x", color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s3-calendario-fondos")


# APCI (2021), Situación y Tendencias de la CTI en el Perú. Ejecutado en 2021:
# 472,1 millones de dólares en total.
COOPERACION_2021 = [
    ("Bilateral", 256.1, ACCENT),
    ("No gubernamental", 136.6, RAMPA[1]),
    ("Multilateral", 79.3, RAMPA[0]),
]


def fig_cooperacion_origen():
    """De dónde viene la cooperación que entra al país, en millones de dólares."""
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    izq = 0.0
    for nombre, monto, color in COOPERACION_2021:
        ax.barh(0, monto, left=izq, height=0.42, color=color, alpha=0.85, zorder=3)
        ax.text(izq + monto / 2, 0.32, nombre, ha="center", va="bottom",
                fontsize=8.2, color=INK)
        ax.text(izq + monto / 2, -0.02, f"{num(monto, 1)}", ha="center", va="center",
                fontsize=8.6, color="#ffffff", fontweight="bold")
        izq += monto
    ax.text(izq, -0.36, f"total {num(izq, 1)} millones de dólares en 2021",
            ha="right", va="top", fontsize=7.8, color=MUTED)
    ax.set_xlim(-6, izq + 6)
    ax.set_ylim(-0.6, 0.7)
    ax.set_yticks([])
    ax.set_xticks([])
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s3-cooperacion-origen")


FIGURAS += [fig_etapa_fondo, fig_que_pide, fig_calendario_fondos,
            fig_cooperacion_origen]


# --------------------------------------------------------------------------
# Radiografía del financiamiento social 2025 (Fondos y Convocatorias). Base de
# 1 019 convocatorias con cierre entre enero y diciembre de 2025, extraídas de
# más de 1 100 con campos completos. Las cuatro figuras replican sus cortes.
# --------------------------------------------------------------------------
TIPOS_CONVOCATORIA = [
    ("Subvenciones", 41.4, ACCENT),
    ("Premios", 22.0, RAMPA[2]),
    ("Becas", 17.2, RAMPA[1]),
    ("Otras modalidades", 19.4, RAMPA[0]),
]


def fig_tipos_convocatoria():
    """Cuatro de cada diez convocatorias son subvenciones; el premio es la segunda vía."""
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    izq = 0.0
    for nombre, parte, color in TIPOS_CONVOCATORIA:
        ax.barh(0, parte, left=izq, height=0.44, color=color, alpha=0.9, zorder=3)
        ax.text(izq + parte / 2, 0.0, f"{num(parte, 1)} %", ha="center", va="center",
                fontsize=8.6, color="#ffffff", fontweight="bold")
        ax.text(izq + parte / 2, 0.32, nombre, ha="center", va="bottom",
                fontsize=8.0, color=INK)
        izq += parte
    ax.set_xlim(-2, 102)
    ax.set_ylim(-0.5, 0.72)
    ax.set_xticks([])
    ax.set_yticks([])
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s3-tipos-convocatoria")


# Rango típico declarado por la propia base, en dólares. El extremo superior de
# la subvención es treinta veces el del premio, y ahí está la decisión.
RANGOS_MONTO = [
    ("Premios", 1_000, 30_000),
    ("Becas", 5_000, 80_000),
    ("Consultorías", 5_000, 40_000),
    ("Aceleradoras", 5_000, 50_000),
    ("Subvenciones", 10_000, 300_000),
]


def fig_rangos_monto():
    """Cuánto da de verdad cada tipo de convocatoria, en dólares y escala logarítmica."""
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    for i, (nombre, lo, hi) in enumerate(RANGOS_MONTO):
        color = ACCENT if nombre == "Subvenciones" else RAMPA[1]
        ax.plot([lo, hi], [i, i], color=color, linewidth=7, solid_capstyle="round",
                alpha=0.85, zorder=3)
        ax.text(lo * 0.86, i, f"{lo // 1000} k", ha="right", va="center",
                fontsize=7.6, color=MUTED)
        ax.text(hi * 1.16, i, f"{hi // 1000} k", ha="left", va="center",
                fontsize=7.8, color=color, fontweight="bold")
        ax.text(600, i + 0.34, nombre, ha="left", va="bottom", fontsize=8.2, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(500, 900_000)
    ax.set_ylim(-0.7, len(RANGOS_MONTO) - 0.15)
    ax.set_yticks([])
    ax.set_xticks([1_000, 10_000, 100_000])
    ax.set_xticklabels(["1 000", "10 000", "100 000"], fontsize=7.8, color=MUTED)
    ax.set_xlabel("dólares, escala logarítmica", fontsize=8.0, color=MUTED)
    ax.grid(True, axis="x", color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s3-rangos-monto")


# Cierres por mes sobre las 1 019 convocatorias de 2025. Solo se publican en el
# informe el pico, el valle y el acumulado del trimestre: el resto de la curva
# se dibuja como tendencia y NO lleva cifra, para no inventar los meses.
CIERRES_MES = [2.5, 4.0, 6.0, 7.0, 7.5, 8.0, 9.5, 13.5, 19.2, 13.4, 6.0, 3.4]


def fig_estacionalidad_cierres():
    """Casi la mitad de las convocatorias cierran entre agosto y octubre."""
    fig, ax = plt.subplots(figsize=(6.9, 2.9))
    meses = ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    for i, v in enumerate(CIERRES_MES):
        destacado = i in (7, 8, 9)
        ax.bar(i, v, width=0.62, color=ACCENT if destacado else RAMPA[0],
               alpha=0.9 if destacado else 0.55, zorder=3)
    for i, etiqueta in ((8, "19,2 %"), (0, "2,5 %")):
        ax.text(i, CIERRES_MES[i] + 0.7, etiqueta, ha="center", va="bottom",
                fontsize=8.2, color=ACCENT if i == 8 else MUTED, fontweight="bold")
    ax.set_xticks(range(12))
    ax.set_xticklabels(meses, fontsize=8.0, color=MUTED)
    ax.set_ylim(0, 23)
    ax.set_ylabel("% de convocatorias\nque cierran en el mes", fontsize=8.0, color=MUTED)
    ax.tick_params(labelsize=7.8, colors=MUTED, length=0)
    ax.grid(True, axis="y", color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    ax.text(8.5, 21.4, "agosto a octubre concentran el 46,1 %", ha="center",
            va="top", fontsize=7.6, color=ACCENT)
    limpiar_ejes(ax)
    escribir(fig, "s3-estacionalidad-cierres")


# Convocatorias por tema, sobre la misma base de 2025. Una convocatoria puede
# contar en varios temas, así que la suma pasa del total: son menciones.
TEMAS_2025 = [("Medio ambiente", 455), ("Diversidad e inclusión", 338),
              ("Tecnología e innovación social", 246), ("Migración y movilidad", 190),
              ("Jóvenes", 189)]


def fig_temas_convocatoria():
    """Qué temas concentran las convocatorias del año."""
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    for i, (tema, n) in enumerate(TEMAS_2025):
        ax.barh(i, n, height=0.55, color=RAMPA[min(i, len(RAMPA) - 1)],
                alpha=0.9, zorder=3)
        ax.text(-14, i, tema, ha="right", va="center", fontsize=8.2, color=INK)
        ax.text(n + 12, i, str(n), ha="left", va="center", fontsize=8.2,
                color=MUTED, fontweight="bold")
    ax.set_xlim(0, 560)
    ax.set_ylim(-0.7, len(TEMAS_2025) - 0.3)
    ax.invert_yaxis()
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlabel("convocatorias que mencionan el tema", fontsize=8.0, color=MUTED)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s3-temas-convocatoria")


FIGURAS += [fig_tipos_convocatoria, fig_rangos_monto,
            fig_estacionalidad_cierres, fig_temas_convocatoria]


# ==========================================================================
# SESIÓN 4 · formulación de proyectos
# ==========================================================================
# El caso que atraviesa la sesión es un nodo electrónico para monitorear
# colmenas. Sus magnitudes son didácticas y se declaran como tales; las del
# sector apícola peruano vienen de la estadística del MIDAGRI.

SECCIONES_DOC = [
    ("Datos generales", 9), ("Resumen", 11), ("Problema", 1), ("Estado del arte", 2),
    ("Objetivos", 3), ("Marco lógico", 4), ("Metodología", 5), ("Cronograma", 6),
    ("Presupuesto", 7), ("Resultados", 8), ("Anexos", 10),
]


def fig_orden_secciones():
    """El documento se lee en un orden y se escribe en otro."""
    fig, ax = plt.subplots(figsize=(6.9, 3.6))
    for i, (nombre, orden) in enumerate(SECCIONES_DOC):
        tardio = orden >= 9
        ax.barh(i, 1, height=0.62, color=ACCENT if tardio else RAMPA[0],
                alpha=0.18 if tardio else 0.30, zorder=2)
        ax.text(0.02, i, f"{i + 1:02d}  {nombre}", va="center", fontsize=8.4,
                color=INK, zorder=3)
        ax.text(0.97, i, f"se escribe {orden}.º", va="center", ha="right",
                fontsize=7.6, color=ACCENT if tardio else MUTED,
                fontweight="bold" if tardio else "normal", zorder=3)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, len(SECCIONES_DOC) - 0.4)
    ax.invert_yaxis()
    ax.set_xticks([]); ax.set_yticks([])
    for l in ax.spines.values():
        l.set_visible(False)
    escribir(fig, "s4-orden-secciones")


def fig_caso_nodo():
    """Las cuatro variables que registra el nodo dentro de la colmena."""
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    VARS = [("Peso", "detecta cosecha y robo"), ("Temperatura", "estado de la cría"),
            ("Humedad", "riesgo sanitario"), ("Sonido", "señal de enjambrazón")]
    for i, (v, para) in enumerate(VARS):
        y = len(VARS) - 1 - i
        ax.add_patch(Rectangle((0.04, y - 0.3), 0.42, 0.6, facecolor=RAMPA[0],
                               alpha=0.20, edgecolor=RAMPA[2], linewidth=1.1))
        ax.text(0.25, y + 0.06, v, ha="center", fontsize=8.6, color=INK, fontweight="bold")
        ax.text(0.25, y - 0.15, para, ha="center", fontsize=7.2, color=MUTED)
        ax.annotate("", xy=(0.62, 1.5), xytext=(0.47, y),
                    arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.1))
    ax.add_patch(Rectangle((0.62, 0.95), 0.35, 1.15, facecolor=ACCENT, alpha=0.14,
                           edgecolor=ACCENT, linewidth=1.3))
    ax.text(0.795, 1.80, "Nodo en la colmena", ha="center", va="center",
            fontsize=8.4, color=ACCENT, fontweight="bold")
    ax.text(0.795, 1.35, "enlace de radio\nhasta el tablero\ndel apicultor", ha="center",
            va="center", fontsize=7.4, color=MUTED, linespacing=1.6)
    ax.set_xlim(0, 1); ax.set_ylim(-0.6, 3.6)
    ax.set_xticks([]); ax.set_yticks([])
    for l in ax.spines.values():
        l.set_visible(False)
    escribir(fig, "s4-caso-nodo")


def fig_resumen_movimientos():
    """Los cuatro movimientos del resumen y el espacio que merece cada uno."""
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    PARTES = [("Problema", 30, ACCENT), ("Solución", 20, RAMPA[2]),
              ("Resultado", 30, RAMPA[1]), ("Impacto", 20, RAMPA[0])]
    izq = 0
    for nombre, p, color in PARTES:
        ax.barh(0, p, left=izq, height=0.4, color=color, alpha=0.88, zorder=3)
        ax.text(izq + p / 2, 0, f"{p} %", ha="center", va="center",
                fontsize=8.4, color="#ffffff", fontweight="bold")
        ax.text(izq + p / 2, 0.3, nombre, ha="center", va="bottom",
                fontsize=8.2, color=INK)
        izq += p
    ax.text(50, -0.34, "las actividades no aparecen en el resumen",
            ha="center", va="top", fontsize=7.6, color=MUTED)
    ax.set_xlim(-2, 102); ax.set_ylim(-0.62, 0.66)
    ax.set_xticks([]); ax.set_yticks([])
    for l in ax.spines.values():
        l.set_visible(False)
    escribir(fig, "s4-resumen-movimientos")


# MIDAGRI, estadística apícola nacional con datos del Censo Nacional
# Agropecuario. El potencial es una estimación del propio ministerio.
APICOLA = [("En producción", 214276, RAMPA[1]), ("Instaladas", 252329, RAMPA[2]),
           ("Potencial estimado", 500000, ACCENT)]


def fig_brecha_apicola():
    """Entre las colmenas en producción y el potencial hay más del doble."""
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    for i, (nombre, v, color) in enumerate(APICOLA):
        ax.barh(i, v, height=0.55, color=color, alpha=0.9, zorder=3)
        ax.text(-9000, i, nombre, ha="right", va="center", fontsize=8.4, color=INK)
        ax.text(v + 9000, i, f"{v:,}".replace(",", " "), ha="left", va="center",
                fontsize=8.4, color=color, fontweight="bold")
    ax.set_xlim(0, 640000)
    ax.set_ylim(-0.7, len(APICOLA) - 0.3)
    ax.invert_yaxis()
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_xlabel("colmenas", fontsize=8.0, color=MUTED)
    for l in ax.spines.values():
        l.set_visible(False)
    escribir(fig, "s4-brecha-apicola")


FIGURAS += [fig_orden_secciones, fig_caso_nodo, fig_resumen_movimientos,
            fig_brecha_apicola]


def _panel(ax, x, y, w, h, texto, color, sub="", fs=8.2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, alpha=0.16,
                           edgecolor=color, linewidth=1.2))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), texto, ha="center",
            va="center", fontsize=fs, color=INK, fontweight="bold")
    if sub:
        ax.text(x + w / 2, y + h * 0.26, sub, ha="center", va="center",
                fontsize=7.0, color=MUTED)


def _limpio(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl)
    ax.set_xticks([]); ax.set_yticks([])
    for l in ax.spines.values():
        l.set_visible(False)


def fig_problema_vs():
    """Dos formulaciones del mismo problema y qué permite hacer cada una."""
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    _panel(ax, 0.02, 1.15, 0.45, 0.72, "Difuso", MUTED,
           "«Falta de tecnología en el sector»")
    _panel(ax, 0.53, 1.15, 0.45, 0.72, "Acotado", ACCENT,
           "«214 276 colmenas sin medición de peso»")
    for i, (izq, der) in enumerate([("no dice a quién afecta", "nombra al apicultor"),
                                    ("no tiene magnitud", "tiene cifra y unidad"),
                                    ("no se puede cerrar", "admite indicador")]):
        y = 0.85 - i * 0.3
        ax.text(0.245, y, izq, ha="center", fontsize=7.6, color=MUTED)
        ax.text(0.755, y, der, ha="center", fontsize=7.6, color=ACCENT)
    _limpio(ax, (0, 1), (-0.15, 2.0))
    escribir(fig, "s4-problema-vs")


ARBOL_CASO = {
    "efectos": ["Ingreso menor del apicultor", "Pérdida de colonias sin aviso"],
    "central": "El apicultor no sabe qué ocurre dentro de la colmena",
    "causas": ["Revisión manual y esporádica", "Sin registro de peso ni clima",
               "Equipos importados y caros"],
}


def _arbol(nombre, arriba, centro, abajo, ctop, cbot, archivo):
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for i, t in enumerate(arriba):
        _panel(ax, 0.06 + i * 0.48, 2.35, 0.42, 0.5, "", ctop)
        ax.text(0.27 + i * 0.48, 2.60, textwrap.fill(t, 26), ha="center",
                va="center", fontsize=7.2, color=INK, linespacing=1.35)
    _panel(ax, 0.10, 1.35, 0.80, 0.62, "", ACCENT)
    ax.text(0.50, 1.66, textwrap.fill(centro, 46), ha="center", va="center",
            fontsize=8.2, color=ACCENT, fontweight="bold", linespacing=1.3)
    for i, t in enumerate(abajo):
        _panel(ax, 0.03 + i * 0.33, 0.30, 0.29, 0.62, "", cbot)
        ax.text(0.175 + i * 0.33, 0.61, textwrap.fill(t, 20), ha="center",
                va="center", fontsize=6.8, color=INK, linespacing=1.35)
    for i in range(len(arriba)):
        ax.annotate("", xy=(0.27 + i * 0.48, 2.33), xytext=(0.5, 1.99),
                    arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.1))
    for i in range(len(abajo)):
        ax.annotate("", xy=(0.5, 1.33), xytext=(0.175 + i * 0.33, 0.94),
                    arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.1))
    ax.text(0.02, 2.95, nombre, fontsize=7.4, color=MUTED)
    _limpio(ax, (0, 1), (0.05, 3.15))
    escribir(fig, archivo)


def fig_arbol_problemas():
    """Causas abajo, problema central en medio y efectos arriba."""
    _arbol("efectos ↑   ·   problema central   ·   causas ↓",
           ARBOL_CASO["efectos"], ARBOL_CASO["central"], ARBOL_CASO["causas"],
           MUTED, RAMPA[1], "s4-arbol-problemas")


def fig_arbol_objetivos():
    """La misma estructura, reformulada en positivo."""
    _arbol("fines ↑   ·   propósito   ·   medios ↓",
           ["Ingreso del apicultor sostenido", "Colonias con aviso temprano"],
           "El apicultor conoce el estado de la colmena a distancia",
           ["Medición continua instalada", "Registro de peso y clima",
            "Nodo de bajo costo disponible"],
           RAMPA[0], OK, "s4-arbol-objetivos")


def fig_objetivo_partes():
    """Verbo, objeto y condición de logro."""
    fig, ax = plt.subplots(figsize=(6.8, 2.6))
    PARTES = [("Verbo", "Detectar", RAMPA[2]), ("Objeto", "la pérdida de peso de la colmena", RAMPA[1]),
              ("Condición de logro", "con error menor a 200 g, en 90 días", ACCENT)]
    x = 0.02
    for rot, txt, color in PARTES:
        w = 0.20 if rot == "Verbo" else (0.36 if rot == "Objeto" else 0.40)
        _panel(ax, x, 0.35, w, 0.55, "", color)
        ax.text(x + w / 2, 0.72, rot, ha="center", fontsize=7.2, color=color,
                fontweight="bold")
        ax.text(x + w / 2, 0.50, textwrap.fill(txt, 24), ha="center",
                va="center", fontsize=7.0, color=INK, linespacing=1.35)
        x += w + 0.01
    ax.text(0.5, 0.16, "sin la tercera parte el objetivo no se puede cerrar",
            ha="center", fontsize=7.6, color=MUTED)
    _limpio(ax, (0, 1), (0.05, 1.05))
    escribir(fig, "s4-objetivo-partes")


def fig_objetivos_jerarquia():
    """Un general y tres específicos que lo suman."""
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    _panel(ax, 0.16, 1.5, 0.68, 0.55, "", ACCENT)
    ax.text(0.5, 1.775, "General · monitoreo remoto de colmenas en operación",
            ha="center", va="center", fontsize=8.2, color=ACCENT, fontweight="bold")
    ESP = ["Caracterizar la señal", "Construir el nodo", "Validar en apiario"]
    for i, t in enumerate(ESP):
        _panel(ax, 0.03 + i * 0.33, 0.35, 0.29, 0.55, "", RAMPA[1])
        ax.text(0.175 + i * 0.33, 0.625, t, ha="center", va="center",
                fontsize=7.6, color=INK)
        ax.annotate("", xy=(0.5, 1.48), xytext=(0.175 + i * 0.33, 0.92),
                    arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.1))
    ax.text(0.5, 0.14, "si se cumplen los tres y el general no, la jerarquía está mal escrita",
            ha="center", fontsize=7.4, color=MUTED)
    _limpio(ax, (0, 1), (0.05, 2.2))
    escribir(fig, "s4-objetivos-jerarquia")


FILAS_ML = ["Fin", "Propósito", "Componentes", "Actividades"]
COLS_ML = ["Resumen narrativo", "Indicadores", "Medios de verificación", "Supuestos"]


def fig_matriz_ml():
    """La matriz completa: cuatro filas y cuatro columnas."""
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    for j, c in enumerate(COLS_ML):
        ax.text(0.20 + j * 0.20, 0.93, c, ha="center", fontsize=7.6,
                color=NAVY, fontweight="bold")
    for i, f in enumerate(FILAS_ML):
        y = 0.74 - i * 0.185
        ax.text(0.005, y, f, ha="left", va="center", fontsize=8.0,
                color=ACCENT, fontweight="bold")
        for j in range(4):
            ax.add_patch(Rectangle((0.115 + j * 0.20, y - 0.075), 0.19, 0.15,
                                   facecolor=NAVY, alpha=0.07,
                                   edgecolor=GRID, linewidth=0.8))
    ax.annotate("", xy=(-0.05, 0.80), xytext=(-0.05, 0.16),
                arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.4))
    ax.text(-0.075, 0.48, "lógica vertical", rotation=90, ha="center", va="center",
            fontsize=6.8, color=ACCENT)
    ax.annotate("", xy=(0.70, 0.045), xytext=(0.13, 0.045),
                arrowprops=dict(arrowstyle="->", color=NAVY, linewidth=1.4))
    ax.text(0.42, 0.005, "lógica horizontal", ha="center", fontsize=7.2, color=NAVY)
    _limpio(ax, (-0.10, 1), (-0.02, 1.0))
    escribir(fig, "s4-matriz-ml")


def fig_logica_vertical():
    """Cada nivel se sostiene en el de abajo más su supuesto."""
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    for i, f in enumerate(FILAS_ML):
        y = 3 - i
        _panel(ax, 0.05, y - 0.32, 0.52, 0.6, f, ACCENT if i < 2 else RAMPA[1])
        if i < 3:
            ax.text(0.63, y - 0.5, "+ supuesto", fontsize=7.4, color=MUTED)
            ax.annotate("", xy=(0.31, y - 0.34), xytext=(0.31, y - 0.68),
                        arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.2))
    ax.text(0.05, -0.42, "se lee de abajo arriba: si el supuesto falla, la cadena se corta ahí",
            fontsize=7.4, color=MUTED)
    _limpio(ax, (0, 1), (-0.6, 3.5))
    escribir(fig, "s4-logica-vertical")


def fig_logica_horizontal():
    """Las dos condiciones que hacen cerrar una fila."""
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    for i, (t, c) in enumerate([("Objetivo", ACCENT), ("Indicador", RAMPA[2]),
                                ("Medio de verificación", NAVY)]):
        _panel(ax, 0.03 + i * 0.33, 0.42, 0.29, 0.48, t, c)
        if i < 2:
            ax.annotate("", xy=(0.355 + i * 0.33, 0.66), xytext=(0.325 + i * 0.33, 0.66),
                        arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.3))
    ax.text(0.5, 0.26, "el medio basta para calcular el indicador",
            ha="center", fontsize=7.6, color=NAVY)
    ax.text(0.5, 0.10, "y el indicador basta para evaluar el objetivo",
            ha="center", fontsize=7.6, color=ACCENT)
    _limpio(ax, (0, 1), (0.0, 1.05))
    escribir(fig, "s4-logica-horizontal")


def fig_medios_verificacion():
    """De dónde sale el dato de cada indicador y qué cuesta."""
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    M = [("Ya existe", 3, OK, "registro del apiario"),
         ("Hay que pedirlo", 2, RAMPA[1], "informe del laboratorio"),
         ("Hay que producirlo", 1, ACCENT, "campaña de medición propia")]
    for i, (t, n, c, ej) in enumerate(M):
        ax.barh(i, n, height=0.5, color=c, alpha=0.85, zorder=3)
        ax.text(-0.08, i, t, ha="right", va="center", fontsize=8.2, color=INK)
        ax.text(n + 0.08, i, ej, ha="left", va="center", fontsize=7.4, color=MUTED)
    ax.text(1.6, -0.75, "producirlo es una actividad y va en el presupuesto",
            ha="center", fontsize=7.4, color=ACCENT)
    ax.set_xlim(0, 4.6); ax.set_ylim(-1.0, 2.6)
    ax.invert_yaxis(); ax.set_yticks([]); ax.set_xticks([])
    ax.set_xlabel("costo de obtener el dato", fontsize=7.8, color=MUTED)
    for l in ax.spines.values():
        l.set_visible(False)
    escribir(fig, "s4-medios-verificacion")


def fig_supuestos():
    """Cuándo un factor externo deja de ser supuesto y pasa a riesgo."""
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.axhline(0.5, color=GRID, linewidth=1); ax.axvline(0.5, color=GRID, linewidth=1)
    Q = [(0.25, 0.75, "No se escribe", MUTED), (0.75, 0.75, "Supuesto", NAVY),
         (0.25, 0.25, "Se ignora", MUTED), (0.75, 0.25, "Riesgo, con mitigación", ACCENT)]
    for x, y, t, c in Q:
        ax.text(x, y, t, ha="center", va="center", fontsize=8.4, color=c,
                fontweight="bold")
    ax.set_xlabel("probabilidad de que ocurra", fontsize=8.0, color=MUTED)
    ax.set_ylabel("impacto si ocurre", fontsize=8.0, color=MUTED)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    limpiar_ejes(ax)
    escribir(fig, "s4-supuestos")


CRONO = [("Caracterizar la señal", 1, 5, True), ("Diseñar el nodo", 3, 8, True),
         ("Fabricar prototipos", 8, 11, True), ("Instalar en apiario", 11, 14, True),
         ("Redactar manual", 12, 16, False), ("Difusión", 15, 18, False)]


def fig_cronograma():
    """Actividades, hitos y ruta crítica."""
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    for i, (t, a, b, critica) in enumerate(CRONO):
        ax.barh(i, b - a, left=a, height=0.5,
                color=ACCENT if critica else RAMPA[0],
                alpha=0.9 if critica else 0.55, zorder=3)
        ax.text(a - 0.4, i, t, ha="right", va="center", fontsize=7.8, color=INK)
        if critica:
            ax.plot(b, i, marker="D", color=ACCENT, markersize=5, zorder=4)
    ax.set_xlim(-7, 19); ax.set_ylim(-0.8, len(CRONO) - 0.2)
    ax.invert_yaxis(); ax.set_yticks([])
    ax.set_xticks(range(0, 19, 3))
    ax.set_xlabel("mes de ejecución · el rombo marca el hito", fontsize=7.8, color=MUTED)
    ax.tick_params(labelsize=7.6, colors=MUTED, length=0)
    ax.grid(True, axis="x", color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "s4-cronograma")


def fig_hito():
    """Actividad frente a hito."""
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    _panel(ax, 0.03, 0.35, 0.44, 0.55, "Actividad", MUTED, "consume tiempo y dinero")
    _panel(ax, 0.53, 0.35, 0.44, 0.55, "Hito", ACCENT, "produce un documento fechado")
    ax.text(0.25, 0.20, "«realizar pruebas de campo»", ha="center", fontsize=7.4, color=MUTED)
    ax.text(0.75, 0.20, "«acta de validación, mes 14»", ha="center", fontsize=7.4, color=ACCENT)
    ax.text(0.5, 0.04, "el desembolso por tramos se libera contra hito, no contra actividad",
            ha="center", fontsize=7.4, color=NAVY)
    _limpio(ax, (0, 1), (0.0, 1.02))
    escribir(fig, "s4-hito")


def fig_novedad():
    """Qué acredita una afirmación de novedad."""
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    N = [("«No hay antecedentes»", 0, MUTED), ("Cita tres trabajos", 1, RAMPA[0]),
         ("Declara dónde buscó", 2, RAMPA[1]), ("Declara qué descartó", 3, ACCENT)]
    for t, v, c in N:
        ax.barh(v, v + 0.4, height=0.5, color=c, alpha=0.85, zorder=3)
        ax.text(-0.1, v, t, ha="right", va="center", fontsize=8.0, color=INK)
    ax.set_xlim(0, 4.6); ax.set_ylim(-0.7, 3.6)
    ax.invert_yaxis(); ax.set_yticks([]); ax.set_xticks([])
    ax.set_xlabel("cuánto puede comprobar el evaluador", fontsize=7.8, color=MUTED)
    for l in ax.spines.values():
        l.set_visible(False)
    escribir(fig, "s4-novedad")


def fig_prisma():
    """El flujo de PRISMA con los descartes contados."""
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    P = [("Identificados", 412), ("Cribados por título", 168),
         ("Leídos completos", 41), ("Incluidos", 12)]
    for i, (t, n) in enumerate(P):
        y = 3 - i
        w = 0.30 + 0.42 * (n / P[0][1])
        _panel(ax, 0.5 - w / 2, y - 0.30, w, 0.56, f"{t} · {n}", RAMPA[min(i, 2)] if i < 3 else ACCENT)
        if i < 3:
            ax.annotate("", xy=(0.5, y - 0.33), xytext=(0.5, y - 0.70),
                        arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.2))
            ax.text(0.90, y - 0.52, f"−{P[i][1] - P[i + 1][1]}", fontsize=7.4,
                    color=MUTED, ha="right")
    _limpio(ax, (0, 1), (-0.35, 3.55))
    escribir(fig, "s4-prisma")


def fig_mapeo():
    """Grupos temáticos en la literatura del monitoreo apícola."""
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    NODOS = [(0.25, 0.70, 700, "sensores", RAMPA[2]), (0.45, 0.82, 420, "IoT", RAMPA[2]),
             (0.70, 0.68, 520, "acústica", ACCENT), (0.80, 0.42, 300, "enjambrazón", ACCENT),
             (0.30, 0.35, 480, "peso", RAMPA[1]), (0.55, 0.25, 260, "clima", RAMPA[1])]
    for x1, y1, _, _, _ in NODOS:
        for x2, y2, _, _, _ in NODOS:
            if (x1, y1) < (x2, y2) and abs(x1 - x2) < 0.32:
                ax.plot([x1, x2], [y1, y2], color=GRID, linewidth=0.8, zorder=1)
    for x, y, s, t, c in NODOS:
        ax.scatter(x, y, s=s, color=c, alpha=0.45, edgecolors=c, linewidths=1.2, zorder=3)
        ax.text(x, y, t, ha="center", va="center", fontsize=7.6, color=INK, zorder=4)
    _limpio(ax, (0.08, 0.95), (0.10, 0.98))
    escribir(fig, "s4-mapeo")


def fig_cadena_resultados():
    """Producto, resultado e impacto."""
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    C = [("Producto", "60 nodos instalados", ACCENT, "responde el proyecto"),
         ("Resultado", "el apicultor decide con el dato", RAMPA[2], "responde en parte"),
         ("Impacto", "menos colonias perdidas", RAMPA[0], "no responde solo")]
    for i, (t, ej, c, quien) in enumerate(C):
        _panel(ax, 0.02 + i * 0.33, 0.40, 0.30, 0.52, t, c)
        ax.text(0.17 + i * 0.33, 0.52, ej, ha="center", fontsize=7.2, color=INK)
        ax.text(0.17 + i * 0.33, 0.26, quien, ha="center", fontsize=7.0, color=MUTED)
        if i < 2:
            ax.annotate("", xy=(0.345 + i * 0.33, 0.66), xytext=(0.325 + i * 0.33, 0.66),
                        arrowprops=dict(arrowstyle="->", color=GRID, linewidth=1.3))
    _limpio(ax, (0, 1), (0.12, 1.02))
    escribir(fig, "s4-cadena-resultados")


def fig_teoria_cambio():
    """Los supuestos causales entre eslabones."""
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    for i, t in enumerate(["Producto", "Resultado", "Impacto"]):
        _panel(ax, 0.03 + i * 0.34, 0.48, 0.28, 0.44, t, RAMPA[1])
        if i < 2:
            x = 0.345 + i * 0.34
            ax.annotate("", xy=(x + 0.02, 0.70), xytext=(x - 0.015, 0.70),
                        arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.4))
            ax.text(x, 0.34, "¿por qué\\ncreemos esto?", ha="center", va="top",
                    fontsize=7.0, color=ACCENT, linespacing=1.4)
    ax.text(0.5, 0.06, "la teoría del cambio escribe esos dos porqués y su evidencia",
            ha="center", fontsize=7.4, color=MUTED)
    _limpio(ax, (0, 1), (0.0, 1.02))
    escribir(fig, "s4-teoria-cambio")


def fig_limite_ml():
    """Avance previsto frente a avance real."""
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    x = list(range(0, 19))
    prev = [i * 100 / 18 for i in x]
    real = [0, 2, 5, 8, 8, 7, 12, 22, 26, 26, 24, 34, 52, 61, 66, 74, 86, 94, 100]
    ax.plot(x, prev, color=MUTED, linewidth=1.6, linestyle="--", label="previsto por la matriz")
    ax.plot(x, real, color=ACCENT, linewidth=2.2, label="avance real típico")
    ax.fill_between(x, real, prev, color=ACCENT, alpha=0.08)
    ax.set_xlabel("mes", fontsize=8.0, color=MUTED)
    ax.set_ylabel("avance (%)", fontsize=8.0, color=MUTED)
    ax.tick_params(labelsize=7.6, colors=MUTED)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=7.4, frameon=False, loc="upper left")
    limpiar_ejes(ax)
    escribir(fig, "s4-limite-ml")


def fig_toc_tramite():
    """Señales de una teoría del cambio hecha para cumplir."""
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    S = ["Se escribió una vez, al postular", "Nadie la revisó durante la ejecución",
         "No declara en qué evidencia se apoya", "Ningún supuesto se corrigió nunca"]
    for i, t in enumerate(S):
        ax.text(0.05, 3 - i, "✕", fontsize=9, color=ACCENT, va="center")
        ax.text(0.12, 3 - i, t, fontsize=8.2, color=INK, va="center")
    _limpio(ax, (0, 1), (-0.5, 3.5))
    escribir(fig, "s4-toc-tramite")


FIGURAS += [fig_problema_vs, fig_arbol_problemas, fig_arbol_objetivos,
            fig_objetivo_partes, fig_objetivos_jerarquia, fig_matriz_ml,
            fig_logica_vertical, fig_logica_horizontal, fig_medios_verificacion,
            fig_supuestos, fig_cronograma, fig_hito, fig_novedad, fig_prisma,
            fig_mapeo, fig_cadena_resultados, fig_teoria_cambio, fig_limite_ml,
            fig_toc_tramite]


# ==========================================================================
# SESIÓN 5 · del proyecto ganado al resultado transferido
# ==========================================================================
# El eje de la sesión no es un caso sino el instrumento que financió el
# proyecto: lo que se presupuesta, se firma, se rinde y se protege cambia
# según la forma del instrumento. Las cinco primeras figuras son las que
# ordenan la sesión entera y se vuelven a mostrar al entrar en cada tema.

# --------------------------------------------------------------------------
# La matriz maestra. Elaboración propia sobre las bases de StartUp Perú 12G y
# de PROCIENCIA E072-2024-01-BM, la Ley 30309 y el catálogo de la sesión 3.
# Cada celda dice si esa forma de instrumento impone esa obligación.
# --------------------------------------------------------------------------
INSTRUMENTOS = ["Subvención", "Beca", "Premio", "Beneficio\ntributario",
                "Servicio\ntecnológico", "Capital con\nparticipación"]
OBLIGACIONES = ["Presupuesto\npor partidas", "Convenio\nfirmado", "Informe\ntécnico",
                "Informe\nfinanciero", "PI de los\nresultados", "Cierre y\nliquidación"]
# 2 = obligación plena · 1 = versión reducida o distinta · 0 = no aplica
MATRIZ_OBLIGACION = [
    [2, 2, 2, 2, 2, 2],   # subvención: la única que exige las seis
    [1, 2, 1, 1, 0, 1],   # beca: rinde estudios, no proyecto
    [0, 0, 0, 0, 0, 0],   # premio: se gana y se cobra
    [1, 0, 1, 0, 1, 0],   # beneficio tributario: califica y deduce
    [0, 1, 0, 0, 1, 0],   # servicio tecnológico: se contrata y se paga
    [1, 2, 0, 1, 2, 0],   # capital con participación: reporta al inversor
]


def _matriz_obligacion(nombre, resaltar=None):
    """Dibuja la matriz maestra, opcionalmente con una columna destacada."""
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    tinta = {2: ACCENT, 1: RAMPA[0], 0: None}
    for f, fila in enumerate(MATRIZ_OBLIGACION):
        for c, v in enumerate(fila):
            apagado = resaltar is not None and c != resaltar
            if v == 0:
                ax.text(c, f, "—", ha="center", va="center", fontsize=9,
                        color=GRID if apagado else MUTED)
                continue
            color = tinta[v]
            ax.add_patch(Rectangle((c - 0.42, f - 0.36), 0.84, 0.72,
                                   facecolor=color, edgecolor="none",
                                   alpha=0.12 if apagado else (0.85 if v == 2 else 0.4)))
            ax.text(c, f, "sí" if v == 2 else "parcial", ha="center", va="center",
                    fontsize=7.2 if v == 1 else 8.0,
                    fontweight="bold" if v == 2 else "normal",
                    color=(GRID if apagado else ("#ffffff" if v == 2 else INK)))
    ax.set_xticks(range(len(OBLIGACIONES)))
    ax.set_xticklabels(OBLIGACIONES, fontsize=7.4, color=INK)
    ax.set_yticks(range(len(INSTRUMENTOS)))
    ax.set_yticklabels(INSTRUMENTOS, fontsize=7.4, color=INK)
    ax.xaxis.set_ticks_position("top")
    ax.set_xlim(-0.6, len(OBLIGACIONES) - 0.4)
    ax.set_ylim(len(INSTRUMENTOS) - 0.45, -0.55)
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, nombre)


def fig_instrumento_obligacion():
    """Seis formas de instrumento y las seis obligaciones que impone cada una."""
    _matriz_obligacion("s5-instrumento-obligacion")


def fig_instrumento_pi():
    """La columna de la propiedad intelectual, que casi ninguna forma perdona."""
    _matriz_obligacion("s5-instrumento-pi", resaltar=4)


# --------------------------------------------------------------------------
# Del medio de verificación al monto. La sesión 4 cerró con la matriz de
# marco lógico y sin costear sus medios; esta figura resuelve esa limitación.
# Magnitudes del caso de clase, no medidas en campo.
# --------------------------------------------------------------------------
COSTO_MEDIOS = [
    ("Registro de sensores\ndel prototipo", "Servidor y almacenamiento", 4_800),
    ("Acta de la asociación\nde apicultores", "Taller y movilidad", 2_400),
    ("Informe de laboratorio\nde calibración", "Servicio de terceros", 6_200),
    ("Encuesta a los\napicultores usuarios", "Encuestador y análisis", 3_500),
]


def fig_costo_medios():
    """Cada medio de verificación de la matriz cuesta dinero y sale de una partida."""
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    total = sum(c for _, _, c in COSTO_MEDIOS)
    for i, (medio, partida, costo) in enumerate(COSTO_MEDIOS):
        ax.barh(i, costo, height=0.34, color=RAMPA[1], alpha=0.85, zorder=3)
        ax.text(-250, i, medio, ha="right", va="center", fontsize=7.4, color=INK)
        ax.text(costo + 220, i, f"S/ {num(costo, 0)}", ha="left", va="center",
                fontsize=8.0, color=RAMPA[2], fontweight="bold")
        # La partida va sobre la barra, con holgura suficiente para no tocarla.
        ax.text(120, i - 0.34, partida, ha="left", va="bottom", fontsize=6.8, color=MUTED)
    ax.set_xlim(0, max(c for _, _, c in COSTO_MEDIOS) * 1.32)
    ax.set_ylim(len(COSTO_MEDIOS) - 0.25, -0.62)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0, len(COSTO_MEDIOS) - 0.42,
            f"Total de la columna de medios: S/ {num(total, 0)}",
            fontsize=8.2, color=ACCENT, fontweight="bold", va="top")
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-costo-medios")


# --------------------------------------------------------------------------
# El presupuesto se construye de la actividad hacia abajo, no al revés.
# --------------------------------------------------------------------------
def fig_actividad_partida():
    """De la actividad al monto: cuatro pasos, y ninguno se puede saltar."""
    fig, ax = plt.subplots(figsize=(7.4, 1.9))
    # Cada cuerpo va partido a mano en líneas cortas: la caja tiene ancho fijo
    # y una línea larga se sale por los dos lados sin que nada lo impida.
    pasos = [("Actividad", "Calibrar el\nsensor de peso"),
             ("Recurso", "Servicio de\nlaboratorio\nacreditado"),
             ("Partida", "Servicios de\nterceros"),
             ("Monto", "S/ 6 200")]
    ancho, hueco = 1.62, 0.34
    for i, (rotulo, cuerpo) in enumerate(pasos):
        x = i * (ancho + hueco)
        color = ACCENT if i == 3 else RAMPA[min(i, 2)]
        ax.add_patch(Rectangle((x, 0), ancho, 1.0, facecolor=color, alpha=0.14,
                               edgecolor=color, linewidth=1.2))
        ax.text(x + ancho / 2, 0.80, rotulo, ha="center", va="center",
                fontsize=7.0, color=color, fontweight="bold")
        ax.text(x + ancho / 2, 0.38, cuerpo, ha="center", va="center",
                fontsize=7.2, color=INK, linespacing=1.35)
        if i < 3:
            ax.annotate("", xy=(x + ancho + hueco - 0.06, 0.5), xytext=(x + ancho + 0.06, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
    ax.set_xlim(-0.15, 4 * ancho + 3 * hueco + 0.15)
    ax.set_ylim(-0.12, 1.12)
    ax.axis("off")
    escribir(fig, "s5-actividad-partida")


# --------------------------------------------------------------------------
# Las mismas seis preguntas a dos instrumentos distintos. Bases de StartUp
# Perú 12G (ProInnóvate, 2025) y E072-2024-01-BM (PROCIENCIA, bases
# integradas y modificadas, 2024). Consultadas el 9 de agosto de 2026.
# --------------------------------------------------------------------------
# Las celdas largas van partidas en dos líneas a mano: con una sola línea las
# dos columnas de valor se solapan, que es el defecto que arrastró la sesión 4.
DOS_INSTRUMENTOS = [
    ("Monto máximo", "S/ 67 000", "S/ 3 000 000"),
    ("Plazo", "Por hitos\nnegociados", "Hasta 36 meses"),
    ("Cofinanciamiento", "70 %", "80 % pública\n60 % privada"),
    ("Contrapartida\nmonetaria", "10 % mínimo", "0 % pública\n30 % privada"),
    ("Tope de personal", "40 % del\ncapital semilla", "20 % del monto\nfinanciado"),
    ("Primer desembolso", "Contra hito, tras\nreunión previa", "20 % referencial"),
]

COL_A, COL_B = 0.40, 0.72


def fig_dos_instrumentos():
    """Dos subvenciones del Estado y las seis cifras en que no se parecen."""
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    for i, (pregunta, a, b) in enumerate(DOS_INSTRUMENTOS):
        y = len(DOS_INSTRUMENTOS) - i
        if i % 2 == 0:
            ax.add_patch(Rectangle((-0.02, y - 0.46), 1.06, 0.92,
                                   facecolor=SURFACE, edgecolor="none", zorder=0))
        ax.text(0.0, y, pregunta, ha="left", va="center", fontsize=7.4, color=MUTED)
        ax.text(COL_A, y, a, ha="left", va="center", fontsize=7.8, color=INK)
        ax.text(COL_B, y, b, ha="left", va="center", fontsize=7.8, color=INK)
    ax.text(COL_A, len(DOS_INSTRUMENTOS) + 0.85, "StartUp Perú 12G", ha="left",
            fontsize=8.2, color=ACCENT, fontweight="bold")
    ax.text(COL_B, len(DOS_INSTRUMENTOS) + 0.85, "PROCIENCIA E072", ha="left",
            fontsize=8.2, color=RAMPA[2], fontweight="bold")
    ax.plot([0, 1.04], [len(DOS_INSTRUMENTOS) + 0.60] * 2, color=GRID, lw=0.9)
    ax.set_xlim(-0.02, 1.06)
    ax.set_ylim(0.25, len(DOS_INSTRUMENTOS) + 1.30)
    ax.axis("off")
    escribir(fig, "s5-dos-instrumentos")


# --------------------------------------------------------------------------
# Topes por rubro. Los de PROCIENCIA son los de las bases integradas: el
# rubro de recursos humanos subió del 15 % al 20 % y viáticos del 5 % al 8 %
# respecto de las bases iniciales, que es el motivo de leer la versión
# integrada y no la primera que se publica.
# --------------------------------------------------------------------------
TOPES_RUBRO = [
    ("Honorarios del equipo", 40, "StartUp Perú · sobre el capital semilla"),
    ("Recursos humanos", 20, "PROCIENCIA · sobre el monto financiado"),
    ("Pasajes y viáticos", 8, "PROCIENCIA · sobre el monto financiado"),
    ("Difusión y transferencia", 5, "StartUp Perú · sobre el capital semilla"),
]


def fig_topes_rubro():
    """Cuatro rubros con tope declarado, y el resto sin restricción de monto."""
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    for i, (rubro, tope, fuente) in enumerate(TOPES_RUBRO):
        y = len(TOPES_RUBRO) - i
        ax.barh(y, 100, height=0.30, color=GRID, alpha=0.30, zorder=2)
        ax.barh(y, tope, height=0.30, color=ACCENT if tope >= 20 else RAMPA[1],
                alpha=0.9, zorder=3)
        # Nombre a la izquierda y procedencia a la derecha, en la MISMA línea:
        # puesta debajo de la barra, la procedencia pisa el rótulo siguiente.
        ax.text(0, y + 0.30, rubro, ha="left", va="bottom", fontsize=8.0, color=INK)
        ax.text(100, y + 0.32, fuente, ha="right", va="bottom", fontsize=6.6, color=MUTED)
        ax.text(101.5, y, f"{tope} %", ha="left", va="center", fontsize=8.2,
                color=ACCENT if tope >= 20 else RAMPA[2], fontweight="bold")
    ax.set_xlim(0, 116)
    ax.set_ylim(0.45, len(TOPES_RUBRO) + 0.85)
    ax.axis("off")
    escribir(fig, "s5-topes-rubro")


# --------------------------------------------------------------------------
# Contrapartida por figura del postulante. La misma propuesta pide aportes
# muy distintos según quién la firme.
# --------------------------------------------------------------------------
CONTRAPARTIDA_FIGURA = [
    ("Entidad pública o\nuniversidad asociativa", 80, 0, 20),
    ("Universidad privada\nsocietaria", 60, 30, 10),
    ("Equipo emprendedor\n(StartUp Perú)", 70, 10, 20),
]


def fig_contrapartida_figura():
    """Quién firma decide cuánto pone y en qué forma lo pone."""
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    for i, (quien, fondo, efectivo, especie) in enumerate(CONTRAPARTIDA_FIGURA):
        y = len(CONTRAPARTIDA_FIGURA) - i
        tramos = [(fondo, RAMPA[2], "fondo"), (efectivo, ACCENT, "efectivo"),
                  (especie, RAMPA[0], "especie")]
        izq = 0
        for parte, color, _ in tramos:
            if parte == 0:
                continue
            # El filete blanco separa dos rellenos contiguos (skill dataviz).
            ax.barh(y, parte, left=izq, height=0.42, color=color, alpha=0.9,
                    edgecolor=PAPER, linewidth=1.2, zorder=3)
            ax.text(izq + parte / 2, y, f"{parte}", ha="center", va="center",
                    fontsize=7.6, color="#ffffff", fontweight="bold")
            izq += parte
        ax.text(-1.5, y, quien, ha="right", va="center", fontsize=7.4, color=INK)
    # Leyenda en una fila bajo las barras: puesta arriba, los tres rótulos se
    # pisan entre sí porque los tramos que nombran son muy desiguales.
    for i, (rot, color) in enumerate((("Lo que pone el fondo", RAMPA[2]),
                                      ("Contrapartida en efectivo", ACCENT),
                                      ("Contrapartida en especie", RAMPA[0]))):
        x = i * 34
        ax.add_patch(Rectangle((x, 0.30), 3.0, 0.16, facecolor=color, edgecolor="none"))
        ax.text(x + 4.6, 0.38, rot, fontsize=7.0, color=MUTED, va="center")
    ax.set_xlim(-34, 102)
    ax.set_ylim(0.10, len(CONTRAPARTIDA_FIGURA) + 0.62)
    ax.axis("off")
    escribir(fig, "s5-contrapartida-figura")


# --------------------------------------------------------------------------
# El desembolso no sigue al cronograma de actividades: va detrás del hito.
# Magnitudes del caso de clase sobre un proyecto de dieciocho meses.
# --------------------------------------------------------------------------
def fig_flujo_caja():
    """El gasto va delante del ingreso, y el hueco lo financia alguien."""
    meses = np.arange(0, 19)
    gasto = np.array([0, 18, 42, 66, 88, 112, 140, 168, 196, 220,
                      248, 274, 300, 322, 344, 362, 378, 392, 400], dtype=float)
    ingreso = np.zeros_like(gasto)
    ingreso[2:] = 140.0          # primer desembolso, 35 % contra reunión previa
    ingreso[9:] = 280.0          # segundo tramo, contra hito verificado
    ingreso[15:] = 400.0         # saldo, contra informe final aprobado

    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.fill_between(meses, ingreso, gasto, where=gasto > ingreso,
                    color=ACCENT, alpha=0.14, zorder=2, label="Hueco a financiar")
    ax.plot(meses, gasto, color=ACCENT, lw=2.0, zorder=4, label="Gasto acumulado")
    ax.step(meses, ingreso, where="post", color=RAMPA[2], lw=2.0, zorder=3,
            label="Desembolso acumulado")

    # El rótulo va bajo el propio hueco, en zona vacía: una línea guía desde
    # arriba tendría que cruzar la curva de gasto para llegar hasta él.
    peor = int(np.argmax(gasto - ingreso))
    ax.text(peor - 1.6, 168,
            f"Hueco máximo en el mes {peor}:\nS/ {num(gasto[peor] - ingreso[peor], 0)} mil "
            "gastados y aún\nno desembolsados",
            fontsize=7.6, color=ACCENT, va="top")
    ax.set_xlabel("Mes de ejecución", fontsize=7.6)
    ax.set_ylabel("Miles de soles", fontsize=7.6)
    ax.set_xticks(range(0, 19, 3))
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    ax.legend(loc="upper left", fontsize=7.0, frameon=False)
    escribir(fig, "s5-flujo-caja")


FIGURAS += [fig_instrumento_obligacion, fig_instrumento_pi, fig_costo_medios, fig_actividad_partida,
            fig_dos_instrumentos, fig_topes_rubro, fig_contrapartida_figura,
            fig_flujo_caja]


# --------------------------------------------------------------------------
# TEMA 02 · del convenio al cierre
# --------------------------------------------------------------------------
# El diagrama maestro del ciclo de vida. Su valor no es la línea de tiempo
# sino lo que cuelga de ella: en qué etapa hay que hacer cada cosa. Casi todo
# lo que se hace tarde en un proyecto se hace tarde por no tener esto delante.
ETAPAS_CICLO = [
    ("Adjudicación", 0, 2.6),
    ("Arranque", 2.6, 4.6),
    ("Ejecución", 4.6, 15),
    ("Cierre", 15, 18),
]
# (mes, qué toca, arriba o abajo, nivel). El nivel escalona los rótulos: con
# uno solo, los cinco primeros hitos caen sobre el mismo palmo de eje y se
# pisan entre sí.
HITOS_CICLO = [
    (0.5, "Resultado del\nconcurso", 1, 0),
    (2.4, "Convenio\nfirmado", -1, 0),
    (3.4, "Acta de inicio y\nprimer desembolso", 1, 1),
    (4.4, "Bitácora y control\nde versiones", -1, 1),
    (6.0, "Solicitud de\npatente", 1, 0),
    (8.0, "Primer informe\ntécnico", -1, 0),
    (10.0, "Artículo y\ncongreso", 1, 1),
    (12.5, "Informe\nfinanciero", -1, 0),
    (15.8, "Informe final\ny video", 1, 0),
    (17.6, "Liquidación", -1, 1),
]


def fig_ciclo_de_vida():
    """Cada obligación tiene su mes, y la propiedad intelectual va antes de publicar."""
    fig, ax = plt.subplots(figsize=(7.6, 3.7))
    for i, (nombre, ini, fin) in enumerate(ETAPAS_CICLO):
        color = RAMPA[min(i, 2)] if i < 3 else ACCENT
        ax.add_patch(Rectangle((ini, -0.14), fin - ini, 0.28, facecolor=color,
                               alpha=0.85, edgecolor=PAPER, linewidth=1.4, zorder=3))
        ax.text((ini + fin) / 2, 0, nombre, ha="center", va="center", fontsize=6.6,
                color="#ffffff", fontweight="bold", zorder=4)
    for mes, texto, lado, nivel in HITOS_CICLO:
        y = (0.42 + nivel * 0.52) * lado
        ax.plot([mes, mes], [0.15 * lado, y - 0.04 * lado], color=MUTED, lw=0.8, zorder=2)
        ax.plot([mes], [0.15 * lado], marker="o", ms=3.2, color=MUTED, zorder=4)
        ax.text(mes, y, texto, ha="center", va="bottom" if lado > 0 else "top",
                fontsize=6.6, color=INK, linespacing=1.3)
    ax.set_xlim(-1.2, 19.4)
    ax.set_ylim(-1.75, 1.75)
    ax.set_xticks([0, 3, 6, 9, 12, 15, 18])
    ax.set_xticklabels(["mes 0", "3", "6", "9", "12", "15", "18"], fontsize=7.0)
    ax.set_yticks([])
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-ciclo-de-vida")


# Lo que hay entre ganar el concurso y cobrar el primer sol. Bases de StartUp
# Perú 12G, que exige reunión previa, y prácticas comunes de las demás.
ANTES_DEL_DESEMBOLSO = [
    ("Constitución o vigencia de poderes", "Registro público"),
    ("Cuenta bancaria exclusiva del proyecto", "Banco"),
    ("Convenios con las entidades asociadas", "Firma de ambas partes"),
    ("Garantía o carta fianza, si la piden", "Entidad financiera"),
    ("Reunión previa y plan de trabajo con hitos", "Ejecutivo del fondo"),
]


def fig_antes_del_desembolso():
    """Cinco requisitos separan el resultado publicado del primer desembolso."""
    fig, ax = plt.subplots(figsize=(6.9, 2.7))
    for i, (paso, quien) in enumerate(ANTES_DEL_DESEMBOLSO):
        y = len(ANTES_DEL_DESEMBOLSO) - i
        ax.add_patch(Rectangle((0, y - 0.32), 0.30, 0.64, facecolor=RAMPA[1],
                               alpha=0.16, edgecolor="none"))
        ax.text(0.15, y, f"{i + 1}", ha="center", va="center", fontsize=9.0,
                color=RAMPA[2], fontweight="bold")
        ax.text(0.40, y + 0.10, paso, ha="left", va="center", fontsize=8.0, color=INK)
        ax.text(0.40, y - 0.20, quien, ha="left", va="center", fontsize=6.9, color=MUTED)
    ax.set_xlim(0, 4.4)
    ax.set_ylim(0.45, len(ANTES_DEL_DESEMBOLSO) + 0.6)
    ax.axis("off")
    escribir(fig, "s5-antes-del-desembolso")


# Los dos informes no comparten ni una sola pieza, y se entregan juntos.
CONTENIDO_INFORMES = [
    ("Informe técnico", ACCENT, ["Hito alcanzado y evidencia",
                                 "Indicador medido, con su medio",
                                 "Desviación respecto del plan",
                                 "Producto entregable adjunto"]),
    ("Informe financiero", RAMPA[2], ["Gasto por partida y por hito",
                                      "Comprobante de cada gasto",
                                      "Contrapartida efectivamente aportada",
                                      "Saldo y proyección del tramo"]),
]


def fig_informes():
    """El informe técnico prueba el resultado; el financiero, que el gasto existió."""
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    for c, (titulo, color, filas) in enumerate(CONTENIDO_INFORMES):
        x = c * 0.52
        ax.add_patch(Rectangle((x, 0), 0.46, 1.0, facecolor=color, alpha=0.08,
                               edgecolor=color, linewidth=1.1))
        ax.text(x + 0.03, 0.88, titulo, fontsize=8.4, color=color, fontweight="bold")
        for f, fila in enumerate(filas):
            ax.text(x + 0.03, 0.68 - f * 0.16, f"· {fila}", fontsize=7.2, color=INK)
    ax.set_xlim(-0.01, 0.99)
    ax.set_ylim(-0.04, 1.04)
    ax.axis("off")
    escribir(fig, "s5-informes")


# Qué se puede mover y qué no. El umbral del 5 % es el de StartUp Perú 12G:
# por encima, la variación va a la Unidad de Evaluación.
MODIFICACIONES = [
    ("Mover monto dentro de\nla misma partida", "Se comunica", OK),
    ("Mover monto entre partidas,\nbajo el 5 % del total", "Se comunica", OK),
    ("Variación sobre el 5 %\ndel financiamiento", "Autorización previa", WARN),
    ("Cambiar el objetivo general\no un hito comprometido", "Vuelve a evaluación", ACCENT),
    ("Cambiar de responsable\ntécnico o de entidad", "Adenda al convenio", ACCENT),
]


def fig_modificaciones():
    """Cuatro de cada cinco cambios no se comunican: se autorizan antes de gastar."""
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    for i, (cambio, tramite, color) in enumerate(MODIFICACIONES):
        y = len(MODIFICACIONES) - i
        ax.text(0, y, cambio, ha="left", va="center", fontsize=7.6, color=INK,
                linespacing=1.35)
        ax.add_patch(Rectangle((0.62, y - 0.22), 0.36, 0.44, facecolor=color,
                               alpha=0.16, edgecolor="none"))
        ax.text(0.80, y, tramite, ha="center", va="center", fontsize=7.6,
                color=color, fontweight="bold")
    ax.set_xlim(-0.01, 1.0)
    ax.set_ylim(0.35, len(MODIFICACIONES) + 0.65)
    ax.axis("off")
    escribir(fig, "s5-modificaciones")


# El cierre son dos, y el segundo dura más que el primero.
def fig_cierre_doble():
    """El proyecto termina técnicamente mucho antes de terminar administrativamente."""
    fig, ax = plt.subplots(figsize=(7.0, 2.4))
    barras = [("Cierre técnico", 0, 3, RAMPA[1],
               ["Último hito verificado", "Informe final aprobado", "Producto entregado"]),
              ("Cierre administrativo", 0, 9, ACCENT,
               ["Rendición del último tramo", "Devolución de saldos",
                "Destino de los bienes", "Liquidación y carta de cierre"])]
    for i, (nombre, ini, fin, color, hitos) in enumerate(barras):
        y = 1 - i
        ax.barh(y, fin - ini, left=ini, height=0.30, color=color, alpha=0.85, zorder=3)
        ax.text(ini, y + 0.26, nombre, fontsize=8.2, color=color, fontweight="bold",
                va="bottom")
        ax.text(fin + 0.25, y, f"{fin} meses desde el último hito", va="center",
                fontsize=7.2, color=MUTED)
        ax.text(ini + 0.1, y - 0.26, " · ".join(hitos), fontsize=6.8, color=INK, va="top")
    ax.set_xlim(-0.2, 15.5)
    ax.set_ylim(-0.75, 1.62)
    ax.axis("off")
    escribir(fig, "s5-cierre-doble")


# --------------------------------------------------------------------------
# TEMA 03 · documentación como metodología
# --------------------------------------------------------------------------
# Diagrama maestro 3. El repositorio es una capa, y no la primera.
CAPAS_DOC = [
    ("Bitácora", "Qué se hizo y cuándo", "Diaria, fechada y firmada"),
    ("Control de versiones", "Qué cambió y por qué", "Cada cambio, con su motivo"),
    ("Documentación técnica", "Cómo se reproduce", "Por versión del prototipo"),
    ("Datos y metadatos", "Con qué se probó", "Al cerrar cada ensayo"),
    ("Publicación", "Qué se aprendió", "Después de proteger"),
    ("Registro", "De quién es", "Antes de divulgar"),
]


def fig_capas_documentacion():
    """Seis capas de documentación, y el repositorio público es solo la quinta."""
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    # Todas las bandas del mismo ancho: una anchura creciente diría que la
    # capa de abajo es «más grande» que la de arriba, y son capas, no cantidades.
    for i, (capa, pregunta, cuando) in enumerate(CAPAS_DOC):
        y = len(CAPAS_DOC) - i
        color = RAMPA[min(i // 2, 2)]
        ax.add_patch(Rectangle((0.05, y - 0.34), 0.95, 0.68, facecolor=color,
                               alpha=0.16, edgecolor="none"))
        ax.add_patch(Rectangle((0.05, y - 0.34), 0.010, 0.68, facecolor=color,
                               edgecolor="none"))
        ax.text(0.0, y, f"{i + 1}", fontsize=8.4, color=color, fontweight="bold",
                va="center", ha="center")
        ax.text(0.09, y + 0.09, capa, fontsize=8.0, color=INK, fontweight="bold",
                va="center")
        ax.text(0.09, y - 0.17, pregunta, fontsize=6.9, color=MUTED, va="center")
        ax.text(0.97, y, cuando, fontsize=7.2, color=color, va="center", ha="right")
    ax.set_xlim(-0.05, 1.02)
    ax.set_ylim(0.4, len(CAPAS_DOC) + 0.7)
    ax.axis("off")
    escribir(fig, "s5-capas-documentacion")


# El valor probatorio: qué prueba cada registro y ante quién.
PRUEBA_DOC = [
    ("Cuaderno con hojas\nnumeradas y firmado", 3, "Prueba interna de autoría"),
    ("Bitácora digital con\nsello de tiempo", 4, "Fecha cierta oponible"),
    ("Depósito con identificador\npersistente", 4, "Fecha y contenido verificables"),
    ("Solicitud de patente\npresentada", 5, "Fecha de prioridad"),
]


def fig_bitacora_prueba():
    """No todo registro prueba lo mismo: solo la solicitud fija fecha de prioridad."""
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    for i, (que, fuerza, prueba) in enumerate(PRUEBA_DOC):
        y = len(PRUEBA_DOC) - i
        ax.text(0, y, que, fontsize=7.4, color=INK, va="center", linespacing=1.3)
        for p in range(5):
            color = ACCENT if p < fuerza else GRID
            ax.add_patch(Rectangle((0.42 + p * 0.037, y - 0.10), 0.026, 0.20,
                                   facecolor=color, alpha=0.9 if p < fuerza else 0.45,
                                   edgecolor="none"))
        ax.text(0.64, y, prueba, fontsize=7.4, color=MUTED, va="center")
    ax.set_xlim(-0.01, 1.02)
    ax.set_ylim(0.4, len(PRUEBA_DOC) + 0.6)
    ax.axis("off")
    escribir(fig, "s5-bitacora-prueba")


# Control de versiones para un prototipo electrónico: el código es una parte.
ARTEFACTOS_VERSION = [
    ("Firmware", "Repositorio con etiquetas de versión"),
    ("Esquemático y placa", "Archivo fuente y revisión numerada"),
    ("Lista de materiales", "Hoja versionada, con proveedor y parte"),
    ("Ensayo y calibración", "Informe fechado por versión de prototipo"),
    ("Documento de diseño", "Una versión por hito, no una por día"),
]


def fig_versiones_artefacto():
    """Un prototipo tiene cinco artefactos que versionar, y solo uno es código."""
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    for i, (artefacto, como) in enumerate(ARTEFACTOS_VERSION):
        y = len(ARTEFACTOS_VERSION) - i
        color = ACCENT if i == 0 else RAMPA[1]
        ax.plot([0.015], [y], marker="s", ms=6, color=color)
        ax.text(0.05, y, artefacto, fontsize=8.0, color=INK, va="center")
        ax.text(0.40, y, como, fontsize=7.2, color=MUTED, va="center")
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0.45, len(ARTEFACTOS_VERSION) + 0.55)
    ax.axis("off")
    escribir(fig, "s5-versiones-artefacto")


# Prevalencia real de datos y código compartidos. Revisión sistemática con
# metanálisis de 105 estudios sobre 2 121 580 artículos, 2016-2021.
DATOS_COMPARTIDOS = [
    ("Declaran que los datos\nestán disponibles", 8.0, RAMPA[1]),
    ("Los datos están\nrealmente disponibles", 2.0, ACCENT),
    ("El código está\nrealmente disponible", 0.5, ACCENT),
]


def fig_datos_compartidos():
    """Ocho de cada cien lo declaran, dos lo cumplen y el código casi nunca."""
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    for i, (que, valor, color) in enumerate(DATOS_COMPARTIDOS):
        y = len(DATOS_COMPARTIDOS) - i
        ax.barh(y, 100, height=0.34, color=GRID, alpha=0.28, zorder=2)
        ax.barh(y, max(valor, 0.6), height=0.34, color=color, alpha=0.9, zorder=3)
        ax.text(-1.5, y, que, ha="right", va="center", fontsize=7.4, color=INK,
                linespacing=1.3)
        etiqueta = "menos del 0,5 %" if valor < 1 else f"{num(valor, 0)} %"
        ax.text(max(valor, 0.6) + 1.6, y, etiqueta, ha="left", va="center",
                fontsize=8.0, color=color, fontweight="bold")
    ax.set_xlim(-46, 104)
    ax.set_ylim(0.45, len(DATOS_COMPARTIDOS) + 0.55)
    ax.axis("off")
    escribir(fig, "s5-datos-compartidos")


FIGURAS += [fig_ciclo_de_vida, fig_antes_del_desembolso, fig_informes,
            fig_modificaciones, fig_cierre_doble, fig_capas_documentacion,
            fig_bitacora_prueba, fig_versiones_artefacto, fig_datos_compartidos]


# --------------------------------------------------------------------------
# TEMA 04 · resultados: registro, publicación y difusión
# --------------------------------------------------------------------------
# Mapa de registros. Qué protege cada figura, ante quién y por cuánto tiempo.
# Decisión 486 de la Comunidad Andina y Decreto Legislativo 822.
REGISTROS = [
    ("Patente de invención", "Producto o procedimiento nuevo", "INDECOPI", 20),
    ("Modelo de utilidad", "Mejora funcional de una forma", "INDECOPI", 10),
    ("Diseño industrial", "Apariencia, no función", "INDECOPI", 10),
    ("Derecho de autor\nsobre software", "Código, no la idea", "INDECOPI", 70),
    ("Marca", "Signo que distingue en el mercado", "INDECOPI", 10),
    ("Secreto empresarial", "Lo que no se divulga", "Nadie", 0),
]


def fig_mapa_registros():
    """Seis figuras de protección, y la vigencia va de diez años a indefinida."""
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    for i, (figura_pi, protege, ante, anios) in enumerate(REGISTROS):
        y = len(REGISTROS) - i
        if i % 2 == 0:
            ax.add_patch(Rectangle((-0.02, y - 0.46), 1.06, 0.92, facecolor=SURFACE,
                                   edgecolor="none", zorder=0))
        color = ACCENT if i == 0 else (WARN if anios == 0 else RAMPA[1])
        ax.text(0.0, y, figura_pi, fontsize=7.6, color=INK, va="center", linespacing=1.25)
        ax.text(0.30, y, protege, fontsize=7.0, color=MUTED, va="center")
        ax.text(0.78, y, ante, fontsize=7.0, color=MUTED, va="center")
        vigencia = "Indefinida" if anios == 0 else f"{anios} años"
        ax.text(1.04, y, vigencia, fontsize=7.4, color=color, va="center",
                ha="right", fontweight="bold")
    for x, rot in ((0.0, "Figura"), (0.30, "Qué protege"), (0.78, "Ante quién")):
        ax.text(x, len(REGISTROS) + 0.78, rot, fontsize=7.0, color=MUTED)
    ax.text(1.04, len(REGISTROS) + 0.78, "Vigencia", fontsize=7.0, color=MUTED, ha="right")
    ax.plot([-0.02, 1.04], [len(REGISTROS) + 0.56] * 2, color=GRID, lw=0.9)
    ax.set_xlim(-0.02, 1.06)
    ax.set_ylim(0.3, len(REGISTROS) + 1.15)
    ax.axis("off")
    escribir(fig, "s5-mapa-registros")


# Tasas del TUPA del INDECOPI aprobado por Decreto Supremo 088-2025-PCM,
# vigentes desde el 1 de julio de 2025. Consultadas el 9 de agosto de 2026.
TASAS_INDECOPI = [
    ("Patente de invención", 396.00, 324.00),
    ("Modelo de utilidad", 266.80, 97.20),
    ("Diseño industrial", 216.00, 144.00),
]


def fig_tasas_indecopi():
    """Solicitud más examen: el modelo de utilidad cuesta la mitad que la patente."""
    fig, ax = plt.subplots(figsize=(6.9, 2.5))
    for i, (nombre, solicitud, examen) in enumerate(TASAS_INDECOPI):
        y = len(TASAS_INDECOPI) - i
        ax.barh(y, solicitud, height=0.36, color=RAMPA[1], alpha=0.9,
                edgecolor=PAPER, linewidth=1.2, zorder=3)
        ax.barh(y, examen, left=solicitud, height=0.36, color=ACCENT, alpha=0.9,
                edgecolor=PAPER, linewidth=1.2, zorder=3)
        ax.text(-14, y, nombre, ha="right", va="center", fontsize=7.6, color=INK)
        ax.text(solicitud + examen + 14, y, f"S/ {num(solicitud + examen, 2)}",
                ha="left", va="center", fontsize=8.0, color=INK, fontweight="bold")
    for i, (rot, color) in enumerate((("Solicitud", RAMPA[1]), ("Examen de fondo", ACCENT))):
        x = i * 190
        ax.add_patch(Rectangle((x, 0.32), 14, 0.10, facecolor=color, edgecolor="none"))
        ax.text(x + 22, 0.37, rot, fontsize=7.0, color=MUTED, va="center")
    ax.set_xlim(-250, 900)
    ax.set_ylim(0.12, len(TASAS_INDECOPI) + 0.55)
    ax.axis("off")
    escribir(fig, "s5-tasas-indecopi")


# Plazos del procedimiento. Decisión 486, artículos 40, 42, 44 y 50.
PLAZOS_PATENTE = [
    ("Presentación y examen de forma", 0, 2, "Fecha de prioridad"),
    ("Confidencialidad hasta la publicación", 2, 18, "Artículo 40"),
    ("Plazo para oponerse", 18, 21, "Artículo 42 · 60 días, prorrogables"),
    ("Plazo para pedir el examen de fondo", 18, 24, "Artículo 44 · 6 meses"),
    ("Examen de fondo y resolución", 24, 42, "Depende de la carga y de las observaciones"),
]


def fig_plazos_patente():
    """Del depósito a la resolución pasan años, y dieciocho meses son de espera."""
    fig, ax = plt.subplots(figsize=(7.4, 2.8))
    for i, (etapa, ini, fin, nota) in enumerate(PLAZOS_PATENTE):
        y = len(PLAZOS_PATENTE) - i
        color = ACCENT if i in (2, 4) else RAMPA[1]
        ax.barh(y, fin - ini, left=ini, height=0.30, color=color, alpha=0.85, zorder=3)
        ax.text(-1.2, y, etapa, ha="right", va="center", fontsize=7.2, color=INK)
        ax.text(fin + 0.8, y, nota, ha="left", va="center", fontsize=6.7, color=MUTED)
    ax.set_xlim(-24, 62)
    ax.set_ylim(0.35, len(PLAZOS_PATENTE) + 0.75)
    ax.set_yticks([])
    ax.set_xticks([0, 12, 24, 36])
    ax.set_xticklabels(["mes 0", "12", "24", "36"], fontsize=7.0)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=0.6, alpha=0.45)
    ax.set_axisbelow(True)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-plazos-patente")


def fig_tramite_vs_proyecto():
    """El proyecto cierra su expediente mucho antes de que la patente se conceda."""
    fig, ax = plt.subplots(figsize=(7.2, 2.2))
    ax.barh(1, 18, height=0.34, color=RAMPA[1], alpha=0.85, zorder=3)
    ax.text(-1.2, 1, "Proyecto financiado", ha="right", va="center", fontsize=7.8, color=INK)
    # El rótulo va sobre la barra: a su derecha cae justo sobre la línea de corte.
    ax.text(17.4, 1.28, "18 meses", ha="right", va="bottom", fontsize=7.6, color=RAMPA[2])
    ax.barh(0, 42, left=6, height=0.34, color=ACCENT, alpha=0.85, zorder=3)
    ax.text(-1.2, 0, "Trámite de patente", ha="right", va="center", fontsize=7.8, color=INK)
    ax.text(48.6, 0, "hasta 42 meses desde la solicitud", ha="left", va="center",
            fontsize=7.6, color=ACCENT)
    ax.plot([18, 18], [-0.45, 1.45], color=INK, lw=1.0, ls=(0, (4, 3)), zorder=5)
    ax.text(19.0, -0.72, "Aquí el proyecto ya no tiene presupuesto, y al trámite le\n"
                         "quedan treinta meses. Hay que decir quién los paga.",
            fontsize=7.2, color=INK, va="top")
    ax.set_xlim(-22, 84)
    ax.set_ylim(-1.55, 1.75)
    ax.axis("off")
    escribir(fig, "s5-tramite-vs-proyecto")


# Qué foro admite qué resultado, y en qué mes del proyecto cae cada uno.
FOROS = [
    ("Póster en congreso", 8, "Resultado parcial, sin detalle habilitante"),
    ("Ponencia en congreso", 11, "Método y resultado, ya solicitada la patente"),
    ("Demostración en feria", 13, "Solo si el registro ya está presentado"),
    ("Artículo en revista", 15, "Resultado cerrado y revisado por pares"),
]


def fig_congresos_momento():
    """Cada foro pide una madurez distinta, y ninguno va antes de la solicitud."""
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    ax.axvspan(0, 6, color=ACCENT, alpha=0.07, zorder=1)
    ax.text(0.3, len(FOROS) + 0.55, "Antes de solicitar: nada se divulga", fontsize=7.0,
            color=ACCENT, ha="left", va="center")
    ax.plot([6, 6], [0.4, len(FOROS) + 0.15], color=ACCENT, lw=1.0, ls=(0, (4, 3)), zorder=4)
    for i, (foro, mes, criterio_txt) in enumerate(FOROS):
        y = len(FOROS) - i
        ax.plot([6, mes], [y, y], color=GRID, lw=0.8, zorder=2)
        ax.plot([mes], [y], marker="o", ms=6, color=RAMPA[1], zorder=4)
        ax.text(mes + 0.5, y + 0.16, foro, fontsize=7.6, color=INK, va="center")
        ax.text(mes + 0.5, y - 0.19, criterio_txt, fontsize=6.7, color=MUTED, va="center")
    ax.set_xlim(0, 34)
    ax.set_ylim(0.4, len(FOROS) + 1.0)
    ax.set_yticks([])
    ax.set_xticks([0, 6, 12, 18])
    ax.set_xticklabels(["mes 0", "6", "12", "18"], fontsize=7.0)
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-congresos-momento")


# --------------------------------------------------------------------------
# TEMA 05 · transferencia y valorización
# --------------------------------------------------------------------------
# El abanico. Espectro de formas de transferencia y de intercambio de
# conocimiento, según Aridi y Cowey (2018), Banco Mundial. Las tres vías que
# enseña la sesión 2 están dentro, en su lugar del espectro.
ABANICO = [
    ("Publicación y congreso", 1, "Sin contraprestación"),
    ("Consultoría y asistencia técnica", 2, "Se cobra el tiempo"),
    ("Uso de equipos y laboratorio", 2, "Se cobra el servicio"),
    ("Investigación por encargo", 3, "El que paga fija el objetivo"),
    ("Desarrollo conjunto", 3, "Titularidad compartida, pactada antes"),
    ("Licencia no exclusiva", 4, "Se cobra por uso, sin ceder"),
    ("Licencia exclusiva", 4, "Un solo explotador, por plazo y territorio"),
    ("Cesión de la titularidad", 5, "Se vende y se pierde el control"),
    ("Spin-off con participación", 5, "Se cambia titularidad por acciones"),
]


def fig_abanico_transferencia():
    """Nueve formas de transferir, de la publicación abierta a la cesión total."""
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    for i, (forma, grado, nota) in enumerate(ABANICO):
        y = len(ABANICO) - i
        color = RAMPA[0] if grado <= 2 else (RAMPA[1] if grado <= 3 else ACCENT)
        ax.barh(y, grado, height=0.44, color=color, alpha=0.75, zorder=3)
        ax.text(-0.12, y, forma, ha="right", va="center", fontsize=7.4, color=INK)
        ax.text(grado + 0.16, y, nota, ha="left", va="center", fontsize=6.8, color=MUTED)
    ax.set_xlim(-3.4, 9.6)
    ax.set_ylim(0.35, len(ABANICO) + 0.95)
    ax.set_yticks([])
    ax.set_xticks([])
    # La flecha ocupa todo el ancho útil para que los dos extremos del eje
    # queden separados: pegados, los dos rótulos se leen como una sola frase.
    ax.annotate("", xy=(9.2, len(ABANICO) + 0.62), xytext=(0.2, len(ABANICO) + 0.62),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))
    ax.text(0.2, len(ABANICO) + 0.78, "Menos control cedido", fontsize=6.9, color=MUTED)
    ax.text(9.2, len(ABANICO) + 0.78, "Más control cedido", fontsize=6.9,
            color=MUTED, ha="right")
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-abanico-transferencia")


# A qué madurez se puede transferir por cada vía. Escala de la sesión 1.
MADUREZ_VIA = [
    ("Publicación y congreso", 1, 9),
    ("Investigación por encargo", 2, 5),
    ("Licencia no exclusiva", 4, 9),
    ("Licencia exclusiva", 5, 9),
    ("Cesión", 6, 9),
    ("Spin-off", 6, 9),
]


def fig_madurez_via():
    """Sin madurez no hay licencia: por debajo del nivel cuatro casi nadie compra."""
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    for i, (via, ini, fin) in enumerate(MADUREZ_VIA):
        y = len(MADUREZ_VIA) - i
        ax.barh(y, fin - ini + 1, left=ini - 0.5, height=0.42,
                color=ACCENT if ini >= 5 else RAMPA[1], alpha=0.8, zorder=3)
        ax.text(0.3, y, via, ha="right", va="center", fontsize=7.4, color=INK)
        ax.text(fin + 0.72, y, f"desde TRL {ini}", ha="left", va="center",
                fontsize=6.9, color=MUTED)
    ax.set_xlim(-7.0, 13.4)
    ax.set_ylim(0.35, len(MADUREZ_VIA) + 0.85)
    ax.set_yticks([])
    ax.set_xticks(range(1, 10))
    ax.set_xticklabels([f"TRL {n}" if n in (1, 5, 9) else str(n) for n in range(1, 10)],
                       fontsize=6.8)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=0.6, alpha=0.4)
    ax.set_axisbelow(True)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-madurez-via")


# Los tres métodos. OMPI, Intellectual Property Valuation Basics for
# Technology Transfer Professionals, capítulos 4, 5 y 6.
METODOS_VALOR = [
    ("Costo", "Lo que costó crearlo o\nlo que costaría rehacerlo",
     "Gasto de I+D, personal,\nmateriales y tasas",
     "Ignora el valor futuro"),
    ("Mercado", "Lo que se pagó por\nalgo comparable",
     "Operaciones comparables:\npago inicial, hitos, regalía",
     "Casi nunca hay comparable"),
    ("Ingresos", "El flujo futuro que\ngenera, traído a hoy",
     "Ventas previstas, costos,\ntasa de descuento y riesgo",
     "Cadena larga de supuestos"),
]


def fig_metodos_valorizacion():
    """Tres métodos de valorización, y cada uno sirve en un momento distinto."""
    fig, ax = plt.subplots(figsize=(7.6, 2.9))
    for c, (metodo, mide, datos, limite) in enumerate(METODOS_VALOR):
        x = c * 0.345
        color = [RAMPA[0], RAMPA[1], ACCENT][c]
        # El relleno usa el tono claro de la rampa; el texto, el oscuro: sobre
        # un relleno al 10 % el tono claro no llega al contraste mínimo.
        tinta_texto = [RAMPA[2], RAMPA[2], ACCENT][c]
        ax.add_patch(Rectangle((x, 0), 0.31, 1.0, facecolor=color, alpha=0.10,
                               edgecolor=color, linewidth=1.1))
        ax.text(x + 0.015, 0.90, metodo, fontsize=8.6, color=tinta_texto,
                fontweight="bold")
        ax.text(x + 0.015, 0.74, mide, fontsize=7.0, color=INK, va="top", linespacing=1.35)
        ax.text(x + 0.015, 0.47, "Qué datos pide", fontsize=6.5, color=MUTED)
        ax.text(x + 0.015, 0.41, datos, fontsize=6.8, color=INK, va="top", linespacing=1.35)
        ax.text(x + 0.015, 0.16, "Dónde falla", fontsize=6.5, color=MUTED)
        ax.text(x + 0.015, 0.10, limite, fontsize=6.8, color=tinta_texto, va="top")
    ax.set_xlim(-0.01, 1.0)
    ax.set_ylim(-0.03, 1.03)
    ax.axis("off")
    escribir(fig, "s5-metodos-valorizacion")


# Qué método admite cada activo. 2 = método principal · 1 = admisible · 0 = no.
ACTIVOS_VALOR = ["Patente concedida", "Solicitud en trámite", "Software",
                 "Secreto empresarial", "Base de datos"]
METODO_POR_ACTIVO = [
    [1, 2, 2],   # patente concedida
    [2, 1, 1],   # solicitud en trámite
    [2, 1, 2],   # software
    [2, 0, 1],   # secreto
    [2, 0, 1],   # base de datos
]


def fig_valorizacion_por_activo():
    """No todo activo admite los tres métodos: el secreto no tiene comparables."""
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    etiquetas = {2: "principal", 1: "admisible", 0: "no aplica"}
    tinta = {2: ACCENT, 1: RAMPA[0], 0: None}
    for f, fila in enumerate(METODO_POR_ACTIVO):
        for c, v in enumerate(fila):
            if v == 0:
                ax.text(c, f, "—", ha="center", va="center", fontsize=9, color=MUTED)
                continue
            ax.add_patch(Rectangle((c - 0.44, f - 0.32), 0.88, 0.64,
                                   facecolor=tinta[v], alpha=0.85 if v == 2 else 0.28,
                                   edgecolor="none"))
            ax.text(c, f, etiquetas[v], ha="center", va="center", fontsize=6.8,
                    color="#ffffff" if v == 2 else INK,
                    fontweight="bold" if v == 2 else "normal")
    ax.set_xticks(range(3))
    ax.set_xticklabels(["Costo", "Mercado", "Ingresos"], fontsize=7.6, color=INK)
    ax.set_yticks(range(len(ACTIVOS_VALOR)))
    ax.set_yticklabels(ACTIVOS_VALOR, fontsize=7.4, color=INK)
    ax.xaxis.set_ticks_position("top")
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(len(ACTIVOS_VALOR) - 0.4, -0.5)
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-valorizacion-por-activo")


# El embudo peruano. CONCYTEC (2016), Programa Especial de Transferencia y
# Extensión Tecnológica. Es la línea de base y nadie la ha vuelto a medir.
EMBUDO_PERU = [
    ("Universidades en el país", 142),
    ("Con política de propiedad intelectual", 10),
    ("Con procedimiento para transferir", 4),
    ("Con una patente llegada a licencia", 0),
]


def fig_brecha_peruana():
    """De ciento cuarenta y dos universidades, ninguna había licenciado una patente."""
    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    tope = EMBUDO_PERU[0][1]
    for i, (etapa, valor) in enumerate(EMBUDO_PERU):
        y = len(EMBUDO_PERU) - i
        color = ACCENT if valor == 0 else RAMPA[min(i, 2)]
        # El cero no se dibuja como barra invisible: se marca, porque el cero
        # ES el hallazgo de esta figura.
        ancho = max(valor, 0)
        if ancho:
            ax.barh(y, ancho, height=0.40, color=color, alpha=0.85, zorder=3)
        else:
            ax.plot([0, 2.5], [y, y], color=ACCENT, lw=1.6, ls=(0, (3, 2)), zorder=3)
        ax.text(-3, y, etapa, ha="right", va="center", fontsize=7.6, color=INK)
        ax.text(max(ancho, 2.5) + 3, y, "ninguna" if valor == 0 else f"{valor}",
                ha="left", va="center", fontsize=8.4,
                color=color, fontweight="bold")
    ax.set_xlim(-72, 168)
    ax.set_ylim(0.35, len(EMBUDO_PERU) + 0.6)
    ax.axis("off")
    escribir(fig, "s5-brecha-peruana")


FIGURAS += [fig_mapa_registros, fig_tasas_indecopi, fig_plazos_patente,
            fig_tramite_vs_proyecto, fig_congresos_momento,
            fig_abanico_transferencia, fig_madurez_via, fig_metodos_valorizacion,
            fig_valorizacion_por_activo, fig_brecha_peruana]


# --------------------------------------------------------------------------
# Dónde va cada cosa. El repositorio de código no sirve para todo, y el
# depósito con identificador persistente es lo que hace citable un dato.
# ALICIA es el repositorio nacional de acceso libre.
# --------------------------------------------------------------------------
DESTINOS_DOC = [
    ("Código y firmware", "Repositorio con control de versiones", "Etiqueta de versión"),
    ("Datos de ensayo", "Repositorio de datos con identificador", "DOI del conjunto"),
    ("Documento técnico", "Repositorio institucional", "Enlace permanente"),
    ("Tesis y artículo", "ALICIA y el repositorio de la universidad", "Acceso libre"),
    ("Video y fotografía", "Almacenamiento del proyecto, con respaldo", "Nombre y fecha"),
    ("Expediente del fondo", "Archivo de la entidad ejecutora", "Copia física y digital"),
]


def fig_donde_va_cada_cosa():
    """Seis clases de material y seis destinos: el repositorio de código es uno."""
    fig, ax = plt.subplots(figsize=(7.6, 2.7))
    for i, (que, donde, senal) in enumerate(DESTINOS_DOC):
        y = len(DESTINOS_DOC) - i
        if i % 2 == 0:
            ax.add_patch(Rectangle((-0.02, y - 0.44), 1.08, 0.88, facecolor=SURFACE,
                                   edgecolor="none", zorder=0))
        ax.text(0.0, y, que, fontsize=7.6, color=INK, va="center")
        ax.text(0.34, y, donde, fontsize=7.4, color=RAMPA[2], va="center")
        ax.text(1.05, y, senal, fontsize=6.9, color=MUTED, va="center", ha="right")
    for x, rot, ali in ((0.0, "Qué se produce", "left"), (0.34, "Dónde se deposita", "left"),
                        (1.05, "Con qué se cita", "right")):
        ax.text(x, len(DESTINOS_DOC) + 0.72, rot, fontsize=7.0, color=MUTED, ha=ali)
    ax.plot([-0.02, 1.06], [len(DESTINOS_DOC) + 0.54] * 2, color=GRID, lw=0.9)
    ax.set_xlim(-0.02, 1.08)
    ax.set_ylim(0.3, len(DESTINOS_DOC) + 1.1)
    ax.axis("off")
    escribir(fig, "s5-donde-va-cada-cosa")


# --------------------------------------------------------------------------
# El orden entre proteger y publicar, dentro del calendario del proyecto.
# La sesión 2 explica por qué la divulgación destruye la novedad; aquí la
# pregunta es cuándo, y la respuesta es una sola fecha.
# --------------------------------------------------------------------------
def fig_proteger_antes_publicar():
    """La fecha de solicitud parte el proyecto en dos: antes se calla, después se cuenta."""
    fig, ax = plt.subplots(figsize=(7.4, 2.6))
    # El corte va en el mes 7 y no en el 6: con la columna izquierda más
    # estrecha, sus renglones cruzan la línea y se pisan con los de la derecha.
    corte = 7.0
    ax.axvspan(0, corte, color=WARN, alpha=0.10)
    ax.axvspan(corte, 18, color=OK, alpha=0.08)
    ax.plot([corte, corte], [-1.0, 1.25], color=ACCENT, lw=1.6, zorder=5)
    ax.text(corte, 1.35, "Solicitud presentada", ha="center", fontsize=8.0,
            color=ACCENT, fontweight="bold")

    izquierda = ["Bitácora y versiones", "Confidencialidad firmada",
                 "Búsqueda de antecedentes", "Nada sale del equipo"]
    derecha = ["Artículo y tesis", "Póster y ponencia", "Demostración pública",
               "Video y nota de prensa"]
    for i, t in enumerate(izquierda):
        ax.text(0.4, 0.75 - i * 0.42, f"· {t}", fontsize=7.2, color=INK, va="center")
    for i, t in enumerate(derecha):
        ax.text(corte + 0.5, 0.75 - i * 0.42, f"· {t}", fontsize=7.2, color=INK,
                va="center")
    ax.text(0.4, -1.02, "Antes: no se divulga", fontsize=7.4,
            color=WARN, fontweight="bold")
    ax.text(corte + 0.5, -1.02, "Después: ya no se pierde nada", fontsize=7.4,
            color=OK, fontweight="bold")
    ax.set_xlim(0, 18)
    ax.set_ylim(-1.35, 1.65)
    ax.set_yticks([])
    ax.set_xticks([0, 7, 12, 18])
    ax.set_xticklabels(["mes 0", "7", "12", "18"], fontsize=7.0)
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-proteger-antes-publicar")


# --------------------------------------------------------------------------
# Un proyecto produce más de un resultado, y cada uno se acredita distinto.
# --------------------------------------------------------------------------
RESULTADOS = [
    ("Prototipo funcional", "Informe de ensayo y video de funcionamiento"),
    ("Solicitud de registro", "Constancia de presentación ante INDECOPI"),
    ("Artículo revisado por pares", "DOI y depósito en acceso libre"),
    ("Tesis derivada", "Sustentación y depósito en ALICIA"),
    ("Base de datos", "Identificador persistente y licencia de uso"),
    ("Norma o especificación técnica", "Documento aprobado por la entidad"),
    ("Personal formado", "Certificado y horas acreditadas"),
    ("Alianza formalizada", "Convenio firmado con objeto y plazo"),
]


def fig_resultados_tipos():
    """Ocho resultados posibles, y cada uno se acredita con un documento distinto."""
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    for i, (resultado, prueba) in enumerate(RESULTADOS):
        y = len(RESULTADOS) - i
        color = ACCENT if i < 2 else RAMPA[1]
        ax.plot([0.012], [y], marker="o", ms=5, color=color, zorder=3)
        ax.text(0.045, y, resultado, fontsize=7.6, color=INK, va="center")
        ax.text(0.44, y, prueba, fontsize=7.0, color=MUTED, va="center")
    ax.plot([0.012, 0.012], [1, len(RESULTADOS)], color=GRID, lw=0.9, zorder=2)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0.45, len(RESULTADOS) + 0.55)
    ax.axis("off")
    escribir(fig, "s5-resultados-tipos")


# --------------------------------------------------------------------------
# Lo que queda armado al cerrar. El dossier es la materia prima del pitch de
# la sesión 6: no se construye al final, se recoge durante.
# --------------------------------------------------------------------------
DOSSIER = [
    ("Expediente", "Convenio, informes y liquidación", 2),
    ("Documentación", "Bitácora, versiones y documento técnico", 4),
    ("Registros", "Solicitudes presentadas y concedidas", 6),
    ("Publicaciones", "Artículo, tesis y ponencias", 9),
    ("Historia", "Cómo evolucionó, mes a mes", 12),
    ("Video", "Resumen de tres minutos", 16),
]


def fig_dossier():
    """Seis piezas del dossier final, y ninguna se puede fabricar el último mes."""
    fig, ax = plt.subplots(figsize=(7.4, 2.9))
    for i, (pieza, contenido, desde) in enumerate(DOSSIER):
        y = len(DOSSIER) - i
        color = RAMPA[min(i // 2, 2)]
        ax.barh(y, 18 - desde, left=desde, height=0.36, color=color, alpha=0.65, zorder=3)
        ax.text(-0.6, y, pieza, ha="right", va="center", fontsize=7.8, color=INK,
                fontweight="bold")
        # El contenido va tras el final de la barra, no encima: dentro se sale
        # por la derecha y choca con lo que venga después. El mes de inicio ya
        # lo dice el arranque de la barra sobre el eje.
        ax.text(18.7, y, contenido, fontsize=6.9, color=MUTED, va="center")
    ax.set_xlim(-7.5, 46)
    ax.set_ylim(0.4, len(DOSSIER) + 0.7)
    ax.set_yticks([])
    ax.set_xticks([0, 6, 12, 18])
    ax.set_xticklabels(["mes 0", "6", "12", "18"], fontsize=7.0)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=0.6, alpha=0.4)
    ax.set_axisbelow(True)
    for lado in ax.spines.values():
        lado.set_visible(False)
    escribir(fig, "s5-dossier")


FIGURAS += [fig_donde_va_cada_cosa, fig_proteger_antes_publicar,
            fig_resultados_tipos, fig_dossier]


# --------------------------------------------------------------------------
# Qué cabe en la partida de propiedad intelectual y difusión. El tope del 5 %
# del capital semilla son S/ 3 000 en StartUp Perú 12G; las tasas son las del
# TUPA vigente. El resto es lo que queda para el evento público de cierre,
# que la misma convocatoria declara obligatorio.
# --------------------------------------------------------------------------
CABE_PARTIDA = [
    ("Solicitud de patente", 396.0, ACCENT),
    ("Examen de fondo", 324.0, ACCENT),
    ("Búsqueda de antecedentes", 450.0, RAMPA[1]),
    ("Evento público de cierre", 1_830.0, RAMPA[0]),
]


def fig_cabe_en_la_partida():
    """El tope del 5 % da para un registro y el evento de cierre, y nada más."""
    fig, ax = plt.subplots(figsize=(7.0, 2.3))
    tope = 3_000.0
    izq = 0.0
    for nombre, monto, color in CABE_PARTIDA:
        ax.barh(0, monto, left=izq, height=0.42, color=color, alpha=0.9,
                edgecolor=PAPER, linewidth=1.4, zorder=3)
        ax.text(izq + monto / 2, 0, f"S/ {num(monto, 0)}", ha="center", va="center",
                fontsize=7.4, color="#ffffff", fontweight="bold", zorder=4)
        izq += monto
    # Un rótulo por renglón, alineado al inicio de su tramo. Con dos niveles
    # alternos, los dos tramos estrechos de la izquierda se pisan entre sí, y
    # centrar el primero lo saca del eje por la izquierda.
    izq = 0.0
    for i, (nombre, monto, _) in enumerate(CABE_PARTIDA):
        y = -0.36 - i * 0.24
        ax.plot([izq + monto / 2, izq + monto / 2], [-0.23, y + 0.04],
                color=GRID, lw=0.8)
        ax.text(izq, y, nombre, ha="left", va="top", fontsize=7.0, color=INK)
        izq += monto
    ax.text(0, 0.42, f"Tope de la partida: S/ {num(tope, 0)} · 5 % del capital semilla",
            fontsize=7.6, color=ACCENT, fontweight="bold", va="bottom")
    ax.set_xlim(-30, tope * 1.04)
    ax.set_ylim(-1.45, 0.85)
    ax.axis("off")
    escribir(fig, "s5-cabe-en-la-partida")


FIGURAS += [fig_cabe_en_la_partida]

# --------------------------------------------------------------------------
# Patentes universitarias en el Perú. Tablero Estadístico de Patentes y
# Diseños Industriales de INDECOPI, resultados de 2025, publicado el 4 de
# febrero de 2026. Las universidades presentaron el 79 % de las solicitudes
# nacionales, y tres de cada cuatro fueron modelo de utilidad.
# --------------------------------------------------------------------------
UNIV_SOLICITUDES = [
    ("Continental", 194, 39),
    ("Privada del Norte", 101, 48),
    ("San Luis Gonzaga", 85, 0),
    ("Tecnológica del Perú", 83, 0),
    ("César Vallejo", 0, 35),
    ("Peruana de Ciencias", 0, 22),
]


def fig_universidades_patentes():
    """Cuatro universidades concentran las solicitudes; el ranking de concedidas es otro."""
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    filas = [f for f in UNIV_SOLICITUDES]
    for i, (nom, sol, con) in enumerate(filas):
        y = len(filas) - i
        if sol:
            ax.barh(y + 0.16, sol, height=0.30, color=RAMPA[1], alpha=0.9, zorder=3)
            ax.text(sol + 4, y + 0.16, str(sol), va="center", fontsize=7.6,
                    color=RAMPA[2], fontweight="bold")
        if con:
            ax.barh(y - 0.18, con, height=0.30, color=ACCENT, alpha=0.9, zorder=3)
            ax.text(con + 4, y - 0.18, str(con), va="center", fontsize=7.6,
                    color=ACCENT, fontweight="bold")
        ax.text(-6, y, nom, ha="right", va="center", fontsize=7.6, color=INK)
    for i, (rot, color) in enumerate((("Solicitudes presentadas", RAMPA[1]),
                                      ("Títulos concedidos", ACCENT))):
        x = i * 92
        ax.add_patch(Rectangle((x, 0.18), 5, 0.14, facecolor=color, edgecolor="none"))
        ax.text(x + 8, 0.25, rot, fontsize=7.0, color=MUTED, va="center")
    ax.set_xlim(-78, 232)
    ax.set_ylim(0.0, len(filas) + 0.75)
    ax.axis("off")
    escribir(fig, "s5-universidades-patentes")


# La composición de lo que la universidad peruana pide: tres de cada cuatro
# solicitudes son modelo de utilidad, no patente de invención.
def fig_invencion_vs_utilidad():
    """Tres de cada cuatro solicitudes universitarias son modelo de utilidad."""
    fig, ax = plt.subplots(figsize=(6.8, 1.9))
    datos = [("Modelos de utilidad", 722, RAMPA[1]), ("Patentes de invención", 246, ACCENT)]
    izq = 0
    for nom, v, color in datos:
        ax.barh(0, v, left=izq, height=0.44, color=color, alpha=0.9,
                edgecolor=PAPER, linewidth=1.6, zorder=3)
        ax.text(izq + v / 2, 0, f"{num(v, 0)}", ha="center", va="center",
                fontsize=9.0, color="#ffffff", fontweight="bold")
        ax.text(izq + v / 2, -0.34, nom, ha="center", va="top", fontsize=7.4, color=INK)
        izq += v
    ax.text(0, 0.40, "968 solicitudes universitarias en 2025 · 79 % del total nacional",
            fontsize=8.0, color=INK, fontweight="bold", va="bottom")
    ax.set_xlim(-10, 985)
    ax.set_ylim(-0.85, 0.80)
    ax.axis("off")
    escribir(fig, "s5-invencion-vs-utilidad")


FIGURAS += [fig_universidades_patentes, fig_invencion_vs_utilidad]

def main() -> None:
    print(f"Generando {len(FIGURAS)} figuras en {SALIDA.relative_to(RAIZ)}/")
    for figura in FIGURAS:
        figura()
    print("Listo.")


if __name__ == "__main__":
    main()
