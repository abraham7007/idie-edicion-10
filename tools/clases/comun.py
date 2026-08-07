#!/usr/bin/env python3
"""Bloques comunes a todas las sesiones del curso.

Las láminas de concepto, de fuente y de «Taller de formulación» tienen una
estructura fija que el proyecto ya ha decidido. Vive aquí una sola vez para
que un cambio de criterio no haya que replicarlo en cada sesión.
"""

import math


def ico(nombre, clase="icon"):
    return f'<svg class="{clase}" aria-hidden="true"><use href="/course-icons.svg#{nombre}" /></svg>'


def cabecera(badge, titulo, icono="i-flow", pequeno=True):
    """Insignia de tema + título, el arranque común de una lámina de concepto."""
    t = "slide__title slide__title--sm" if pequeno else "slide__title"
    return f"""\t\t\t\t<span class="badge" data-animate="fade-up">
\t\t\t\t\t{ico(icono)}
\t\t\t\t\t{badge}
\t\t\t\t</span>

\t\t\t\t<h1 class="{t}" data-animate="fade-up">{titulo}</h1>"""


def envolver(interior, clases="slide__content stagger"):
    return f'\t\t\t<div class="{clases}">\n{interior}\n\t\t\t</div>'


# ============================================================
# COLOFÓN — autoría y licencia
# ============================================================
# Va solo en la portada y en el cierre de cada sesión, nunca en las láminas
# de contenido: es una firma legal, no un elemento decorativo que deba
# repetirse en las 49 láminas (METODOLOGIA.md §7, aprovechamiento de espacio).

AUTOR = "Abraham Caso-Torres"
LICENCIA_TEXTO = "CC BY-SA 4.0"
LICENCIA_HREF = "https://creativecommons.org/licenses/by-sa/4.0/deed.es"


def colofon():
    """Crédito de autoría y licencia abierta, en flujo normal.

    Para la portada: hay hueco de sobra en la columna de texto de `.cover`.
    """
    return (f'\t\t\t\t<p class="colofon">© {AUTOR} · '
            f'<a href="{LICENCIA_HREF}" target="_blank" rel="license noopener">{LICENCIA_TEXTO}</a></p>')


def colofon_flotante():
    """Crédito de autoría y licencia, para el cierre de la sesión.

    La lámina de referencias ya lleva una tabla de siete filas al límite de
    alto (comun_idie.tabla, §5): cualquier línea añadida al flujo desborda.
    Se ancla fuera de `.slide__content`, en la esquina que la tira de
    navegación deja vacía en la última lámina (no hay «siguiente»), y no en
    el flujo — por eso va fuera de `envolver(...)`, como hermano del bloque
    de contenido y no dentro de él.
    """
    return (f'\t\t\t<p class="colofon colofon-flotante">© {AUTOR} · '
            f'<a href="{LICENCIA_HREF}" target="_blank" rel="license noopener">{LICENCIA_TEXTO}</a></p>')


# ============================================================
# EL MAPA DEL ECOSISTEMA — objeto central del curso (METODOLOGIA.md §1.1)
# ============================================================
# Cinco actores institucionales alrededor del proyecto. Las coordenadas se
# calculan aquí y no se escriben a mano: si se cambia el radio o se añade un
# actor, la figura se recoloca sola y ninguna arista queda descolgada.

CX, CY = 115.0, 105.0  # centro del dibujo
R_ANILLO = 72.0  # distancia del centro a cada actor
R_NODO = 25.0
R_NUCLEO = 30.0

# En orden horario desde arriba. El orden importa: las aristas del perímetro
# unen vecinos, y son las que cuentan la historia del curso (academia →
# empresa es transferencia; estado → fondos es la convocatoria).
ACTORES = [
    ("academia", "ACADEMIA"),
    ("empresa", "EMPRESA"),
    ("mercado", "MERCADO"),
    ("estado", "ESTADO"),
    ("fondos", "FONDOS"),
]

_POS = {}
for _i, (_clave, _) in enumerate(ACTORES):
    _ang = math.radians(-90 + _i * 360 / len(ACTORES))
    _POS[_clave] = (CX + R_ANILLO * math.cos(_ang), CY + R_ANILLO * math.sin(_ang))


def _aristas():
    """Perímetro entre vecinos + radios al núcleo. Devuelve (clave, x1,y1,x2,y2)."""
    fuera = []
    n = len(ACTORES)
    for i, (clave, _) in enumerate(ACTORES):
        siguiente = ACTORES[(i + 1) % n][0]
        x1, y1 = _POS[clave]
        x2, y2 = _POS[siguiente]
        fuera.append((f"{clave}-{siguiente}", x1, y1, x2, y2))
        fuera.append((f"{clave}-nucleo", x1, y1, CX, CY))
    return fuera


def mapa_ecosistema(activos=(), aristas=(), pie="", subpie=""):
    """Mapa del ecosistema para la portada de una sesión.

    `activos` son las claves de actor iluminadas y `aristas` las de los
    enlaces. Sin argumentos sale el mapa completo en tono apagado, que es lo
    correcto cuando la lámina no habla de un tramo concreto.
    """
    activos, aristas = set(activos), set(aristas)

    lineas = []
    for clave, x1, y1, x2, y2 in _aristas():
        on = " hero-map__edge--on" if clave in aristas else ""
        lineas.append(
            f'\t\t\t\t\t\t<line class="hero-map__edge{on}" '
            f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" />'
        )

    nodos = [
        f'\t\t\t\t\t\t<g class="hero-map__core">\n'
        f'\t\t\t\t\t\t\t<circle cx="{CX}" cy="{CY}" r="{R_NUCLEO}" />\n'
        f'\t\t\t\t\t\t\t<text x="{CX}" y="{CY - 5.5}">PROYECTO</text>\n'
        f'\t\t\t\t\t\t\t<text x="{CX}" y="{CY + 6.5}">I+D+i+e</text>\n'
        f"\t\t\t\t\t\t</g>"
    ]
    for clave, etiqueta in ACTORES:
        x, y = _POS[clave]
        on = " hero-map__node--on" if clave in activos else ""
        nodos.append(
            f'\t\t\t\t\t\t<g class="hero-map__node{on}">\n'
            f'\t\t\t\t\t\t\t<circle cx="{x:.1f}" cy="{y:.1f}" r="{R_NODO}" />\n'
            f'\t\t\t\t\t\t\t<text x="{x:.1f}" y="{y:.1f}">{etiqueta}</text>\n'
            f"\t\t\t\t\t\t</g>"
        )

    leyenda = ""
    if pie or subpie:
        b = f"<b>{subpie}</b>" if subpie else ""
        leyenda = f'\n\t\t\t\t\t<p class="hero-map__caption">{pie}{b}</p>'

    cuerpo = "\n".join(lineas + nodos)
    return f"""\t\t\t\t<div class="hero-map" data-animate="fade-up">
\t\t\t\t\t<svg class="hero-map__svg" viewBox="14 2 202 192" role="img"
\t\t\t\t\t\taria-label="Mapa del ecosistema I+D+i+e: academia, empresa, mercado, estado y fondos alrededor del proyecto">
{cuerpo}
\t\t\t\t\t</svg>{leyenda}
\t\t\t\t</div>"""


def taller(
    ref,
    titulo,
    ficha,
    borrador,
    diagrama,
    que_produce,
    insumos,
    resultado,
    prompt,
    nota,
    concepto,
    fuentes="",
):
    """Estructura canónica del «Taller de formulación asistida».

    Es el bloque práctico del curso, adaptado de «La hora del código» de la
    metodología (§4). El esqueleto no cambia —y no debe cambiar—: los tres
    entregables van ANTES del prompt, porque el prompt es solo la forma de
    pedirlos, y «por qué se pide así» es lo que enseña a especificar.

    Lo que cambia respecto del original es únicamente la naturaleza de los
    entregables: aquí no se compila firmware, se redacta una propuesta.
    """
    src = f'\n\t\t\t\t\t\t\t\t\t<div class="hw-set">{fuentes}</div>' if fuentes else ""
    return envolver(
        f"""\t\t\t\t<div class="code-hour" data-animate="fade-up">
\t\t\t\t\t<div class="code-hour__header">
\t\t\t\t\t\t{ico("i-workshop")}
\t\t\t\t\t\t<span class="code-hour__label">Taller de formulación</span>
\t\t\t\t\t\t<span class="code-hour__ref">Taller {ref}</span>
\t\t\t\t\t</div>

\t\t\t\t\t<h2 class="code-hour__title">{titulo}</h2>

\t\t\t\t\t<div class="deliverables">
\t\t\t\t\t\t<div class="deliverable">
\t\t\t\t\t\t\t{ico("i-project")}
\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t<span class="deliverable__name">Ficha</span>
\t\t\t\t\t\t\t\t<span class="deliverable__what">{ficha}</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="deliverable deliverable--sim">
\t\t\t\t\t\t\t{ico("i-paper")}
\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t<span class="deliverable__name">Borrador</span>
\t\t\t\t\t\t\t\t<span class="deliverable__what">{borrador}</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="deliverable deliverable--diagram">
\t\t\t\t\t\t\t{ico("i-diagram")}
\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t<span class="deliverable__name">Diagrama</span>
\t\t\t\t\t\t\t\t<span class="deliverable__what">{diagrama}</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="code-hour__body code-hour__body--pair">
\t\t\t\t\t\t<div class="code-hour__stack">
\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-target")}Qué debe producir</h4>
\t\t\t\t\t\t\t\t<p>{que_produce}</p>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-folder")}Insumos</h4>
\t\t\t\t\t\t\t\t<p>{insumos}</p>{src}
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-rubric")}Resultado esperado</h4>
\t\t\t\t\t\t\t\t<div class="term">{resultado}</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t<h4>{ico("i-robot")}Prompt para el asistente</h4>
\t\t\t\t\t\t\t<div class="prompt-box">{prompt}</div>
\t\t\t\t\t\t\t<p class="prompt-note"><b>Por qué se pide así.</b> {nota}</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="code-hour__why">
\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t<p><b>Concepto que se verifica.</b> {concepto}</p>
\t\t\t\t\t</div>
\t\t\t\t</div>""",
        "slide__content slide__content--flush stagger",
    )


def fuente(
    etiqueta,
    licencia,
    cita,
    titulo,
    objetivo,
    metodologia,
    discusion,
    figura,
    hallazgos,
    relevancia,
    icono_cab="i-paper",
    rotulo_metodo="Metodología o base normativa",
):
    """Lámina de fuente: sigue el recorrido que hace un lector por el texto.

    Adaptación de la «lámina de artículo» de la metodología (§5). Aquí las
    fuentes autorizadas no son solo artículos revisados por pares: son también
    manuales metodológicos (Frascati, Oslo), informes de organismos (GII,
    BID Lab, OCDE) y bases legales de convocatoria. Por eso la sección central
    no puede llamarse siempre «procedimiento experimental»: un manual no
    experimenta, fija una definición. El rótulo se pasa por argumento y se
    elige según lo que la fuente sea de verdad.
    """
    return envolver(
        f"""\t\t\t\t<div class="paper" data-animate="fade-up">
\t\t\t\t\t<div class="paper__header">
\t\t\t\t\t\t{ico(icono_cab)}
\t\t\t\t\t\t<span class="paper__label">{etiqueta}</span>
\t\t\t\t\t\t<span class="paper__license">{licencia}</span>
\t\t\t\t\t</div>

\t\t\t\t\t<p class="paper__cite">{cita}</p>

\t\t\t\t\t<h2 class="paper__title">{titulo}</h2>

\t\t\t\t\t<div class="paper__body">
\t\t\t\t\t\t<div class="paper__notes">
\t\t\t\t\t\t\t<div class="paper__section">
\t\t\t\t\t\t\t\t<div class="paper__section-label">{ico("i-target")}Objetivo del estudio</div>
\t\t\t\t\t\t\t\t<p>{objetivo}</p>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="paper__section">
\t\t\t\t\t\t\t\t<div class="paper__section-label">{ico("i-sliders")}{rotulo_metodo}</div>
\t\t\t\t\t\t\t\t<p>{metodologia}</p>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="paper__section">
\t\t\t\t\t\t\t\t<div class="paper__section-label">{ico("i-book")}Discusión y conclusiones</div>
\t\t\t\t\t\t\t\t<p>{discusion}</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="figure">
{figura}
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="findings">
{hallazgos}
\t\t\t\t\t</div>

\t\t\t\t\t<div class="paper__relevance">
\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t<span class="paper__relevance-label">Para esta sesión:</span>
\t\t\t\t\t\t\t{relevancia}
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>""",
        "slide__content slide__content--flush stagger",
    )


def hallazgo(valor, texto, variante=""):
    v = f" finding--{variante}" if variante else ""
    return (
        f'\t\t\t\t\t\t<div class="finding{v}">\n'
        f'\t\t\t\t\t\t\t<span class="finding__value">{valor}</span>\n'
        f'\t\t\t\t\t\t\t<span class="finding__what">{texto}</span>\n'
        f"\t\t\t\t\t\t</div>"
    )


def problema(titulo, sintoma, porque, comprobar, icono="i-alert"):
    return f"""\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">{ico(icono)}{titulo}</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>{sintoma}</p>
\t\t\t\t\t\t\t<p><b>Por qué ocurre.</b> {porque}</p>
\t\t\t\t\t\t\t<p><b>Cómo comprobarlo.</b> {comprobar}</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>"""


def termino(es, en, definicion):
    return f"""\t\t\t\t\t<div class="glossary-item">
\t\t\t\t\t\t<h3>{es} <span class="glossary-item__en">{en}</span></h3>
\t\t\t\t\t\t<p class="glossary-item__body">{definicion}</p>
\t\t\t\t\t</div>"""


