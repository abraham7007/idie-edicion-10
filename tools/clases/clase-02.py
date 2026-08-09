#!/usr/bin/env python3
"""Sesión 2 · Startups, spin-offs y transferencia.

Guion de la sesión. Contiene SOLO lo que distingue a cada lámina: la cabecera
repetida, la cadena de anterior/siguiente y el total los pone el generador
(METODOLOGIA.md §9). Se edita este archivo, nunca el HTML resultante.

Todas las cifras están verificadas contra la fuente que se cita al pie de la
lámina, y son las mismas que usan las figuras de `tools/figures/render.py`
(METODOLOGIA.md §1 y §3.2).

Uso:  python3 tools/clases/clase-02.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tools"))

from clases.comun import (  # noqa: E402
    cabecera, colofon, colofon_flotante, ico, mapa_ecosistema, problema, termino,
)
from clases.comun_idie import (  # noqa: E402
    aviso, conclusion, criterio, dato, dato_clave, definicion, duo, ejemplo,
    en_la_practica, envolver_visual as envolver,
    evitar, fig_desnuda, figura, fuente_pie, reiniciar_alternancia, seccion,
    renumerar, tabla, bloque_herramientas,
)
from generar_clase import generar_desde  # noqa: E402

reiniciar_alternancia()

SESION = "Sesión 2 · Startups, spin-offs y transferencia"

# Los dos temas de la sesión. Frases nominales que nombran la materia, como la
# nombraría un temario: sin verbos y sin interrogaciones (METODOLOGIA.md §6).
TEMA_A = "Vías de explotación del resultado y titularidad de la invención"
TEMA_B = "Transferencia tecnológica y determinantes de la creación de spin-offs"

# El mismo nombre con el anglicismo en cursiva, para donde se pinta como HTML.
# En el <title> del documento el marcado se vería literal, así que ahí va el de
# arriba, sin etiquetas.
TEMA_B_HTML = ("Transferencia tecnológica y determinantes de la creación de "
               "<i>spin-offs</i>")


# --------------------------------------------------------------------------
# FUENTES
#
# Las seis primeras son los trabajos revisados por pares de esta sesión, todos
# descargados y verificados en src/paper/ (ficha en src/paper/fuentes.json,
# clave `clase-02`). Se escriben una vez y se reutilizan, para que dos láminas
# no puedan citar el mismo trabajo de dos formas distintas.
# --------------------------------------------------------------------------

F_ODWYER = ("O’Dwyer et al. (2022), <i>The Journal of Technology Transfer</i> "
            "· CC BY 4.0")
F_ODEI = ("Odei y Novák (2022), <i>Economic Research-Ekonomska Istraživanja</i> "
          "· CC BY 4.0")
F_HUNADY = ("Hunady et al. (2019), <i>Business Systems Research</i> 10(1) "
            "· CC BY-NC-ND 3.0")
F_SAMO = ("Samo y Huda (2019), <i>Journal of Global Entrepreneurship Research</i> "
          "9 · CC BY 4.0")
F_NGUYEN = "Nguyen et al. (2024), <i>Sustainability</i> 16(19):8714 · CC BY 4.0"
F_BID = ("Peña y Jenik (2023), <i>Deep Tech: The New Wave</i>, BID "
         "· doi 10.18235/0004947")

# Institucionales y normativas. La ficha de acceso de cada una está en
# src/paper/fuentes-externas.json.
F_LEY_31250 = ("Ley 31250, <i>Ley del Sistema Nacional de Ciencia, Tecnología e "
               "Innovación</i>, 2021 · norma de dominio público")
F_INDECOPI = ("INDECOPI, <i>Anuario de Propiedad Intelectual</i> "
              "· documento público")
F_OMPI_PCT = ("OMPI, <i>Guía del solicitante PCT</i> · lectura abierta en "
              "wipo.int")


def logro(icono, texto):
    return f'\t\t\t\t\t\t<p class="goal">{ico(icono)}<span>{texto}</span></p>'


# ==========================================================================
# PORTADA
#
# El objeto central de toda portada de sesión es el mapa del ecosistema
# (METODOLOGIA.md §0). En esta sesión el tramo iluminado es el que va de la
# academia a la empresa y de la empresa al mercado: es exactamente el recorrido
# del que trata la sesión.
# ==========================================================================

PORTADA = f"""			<div class="slide__content stagger">
				<div class="cover">
					<div class="cover__main">
						<span class="badge" data-animate="fade-up">{ico("i-rocket")}Sesión 2</span>

						<h1 class="slide__title" data-animate="fade-up"><i>Startups</i>, <i>spin-offs</i> y transferencia</h1>

						<div class="cover__topics" data-animate="fade-up">
							<span class="topic"><span class="topic__n">01</span>{TEMA_A}</span>
							<span class="topic topic--b"><span class="topic__n">02</span>{TEMA_B_HTML}</span>
						</div>

{colofon()}
					</div>

{mapa_ecosistema(
    activos=("academia", "empresa", "mercado"),
    aristas=("academia-empresa", "empresa-mercado"),
)}
				</div>
			</div>"""


# ==========================================================================
# AGENDA
# ==========================================================================

AGENDA = envolver(
    cabecera("Agenda", "Explotación del resultado, transferencia tecnológica y cuatro paradas de herramientas", "i-flow")
    + "\n"
    + """\t\t\t\t<div class="agenda" data-animate="fade-up">
\t\t\t\t\t<div class="agenda__block">
\t\t\t\t\t\t<span class="agenda__n">Tema 01</span>
\t\t\t\t\t\t<h3>Explotación del resultado y titularidad</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Licencia, <i>spin-off</i> y <i>startup</i>: qué exige cada una</li>
\t\t\t\t\t\t\t<li>Quién es el titular del resultado y quién lo explota</li>
\t\t\t\t\t\t\t<li>La patente como requisito y como activo</li>
\t\t\t\t\t\t\t<li><i>Deep tech</i> y en qué se aparta del emprendimiento corriente</li>
\t\t\t\t\t\t\t<li>Qué mueve a un investigador a fundar una empresa</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 01</b>Trabajar sin divulgar el resultado</li>
\t\t\t\t\t\t\t<li><b>Herramientas 02</b>Buscadores de patentes y su cobertura</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--b">
\t\t\t\t\t\t<span class="agenda__n">Tema 02</span>
\t\t\t\t\t\t<h3>Transferencia y creación de <i>spin-offs</i></h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Qué hace una oficina de transferencia y qué no</li>
\t\t\t\t\t\t\t<li>Determinantes medidos de la creación de <i>spin-offs</i></li>
\t\t\t\t\t\t\t<li>Barreras de la colaboración universidad-empresa</li>
\t\t\t\t\t\t\t<li>El <i>deep tech</i> en América Latina</li>
\t\t\t\t\t\t\t<li>De dónde parte el Perú y con qué instrumentos</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 03</b>Repositorios que dan DOI, fecha y enlace estable</li>
\t\t\t\t\t\t\t<li><b>Herramientas 04</b>Trámites en línea del expediente peruano</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="agenda__map" data-animate="fade-up">
\t\t\t\t\t\t<span class="agenda__map-label">Las seis sesiones</span>
\t\t\t\t\t\t<ul class="agenda__steps">
\t\t\t\t\t\t\t<li><b>01</b>Fundamentos y ecosistema I+D+i+e</li>
\t\t\t\t\t\t\t<li class="is-on"><b>02</b><i>Startups</i>, <i>spin-offs</i> y transferencia</li>
\t\t\t\t\t\t\t<li><b>03</b>Mapa de financiamiento e inversión</li>
\t\t\t\t\t\t\t<li><b>04</b>Formulación de proyectos</li>
\t\t\t\t\t\t\t<li><b>05</b>Del proyecto ganado al resultado transferido</li>
\t\t\t\t\t\t\t<li><b>06</b><i>Pitch Elevator</i> y tendencias mundiales en I+D+i+e</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)


# ==========================================================================
# 01 · FIGURAS CON LAS QUE UN RESULTADO SALE
#
# Los bloques de contenido de los dos temas se escriben en tandas y se montan
# al final, en LAMINAS. El montaje va SIEMPRE al final del archivo: un bloque
# declarado después de la lista nunca se ejecuta, y eso ya costó dos láminas
# perdidas en la sesión 1 (METODOLOGIA.md §17).
# ==========================================================================

SECCION_A = seccion(
    "01",
    TEMA_A,
    "Licencia, <i>spin-off</i> y <i>startup</i> son las tres vías por las que un "
    "resultado se explota, y cada una fija un titular distinto, un reparto de "
    "riesgo distinto y un instrumento de financiamiento distinto.",
)

SECCION_B = seccion(
    "02",
    TEMA_B_HTML,
    "Lo que el convenio fija decide si hay transferencia. Los determinantes que "
    "la literatura mide sobre 164 universidades se pueden comprobar en la propia "
    "institución antes de firmar.",
)


# ==========================================================================
# 01 · CONTENIDO DEL TEMA A
# ==========================================================================

CONVERSION = envolver(
    cabecera("01 · De la investigación a la empresa",
             "Cadena de conversión de investigación a empresa en América Latina, 2023", "i-chart")
    + "\n"
    + figura(
        "s2-conversion-investigacion",
        "Investigadores, artículos, solicitudes de patente y empresas de <i>deep tech</i> con inversión, América Latina y el Caribe, 2023",
        "<b>Cada paso divide el recuento anterior: por tres hasta el artículo, "
        "por quince hasta la patente y por treinta y cinco hasta la empresa.</b>",
    )
    + "\n"
    + dato_clave(
        "América Latina y el Caribe reúne <b>523 000 investigadores</b>, publica "
        "<b>180 000 artículos</b> al año y presenta <b>12 000 solicitudes de "
        "patente</b>. Las empresas de <i>deep tech</i> con inversión institucional son "
        "<b>340</b>. Informe del BID de 2023."
    )
    + "\n"
    + conclusion(
        "Dónde se estrecha la cadena",
        "El tramo más angosto va de la solicitud de patente a la empresa: treinta y "
        "cinco solicitudes por cada empresa que consigue inversión. Las tres vías "
        "de salida operan en ese tramo, y una vía mal elegida deja el resultado dentro "
        "de la universidad.",
    )
    + "\n"
    + fuente_pie(F_BID)
)


TRES_VIAS = envolver(
    cabecera("01 · Las tres vías de salida",
             "Vías de salida de un resultado y su requisito propio", "i-layers")
    + "\n"
    + definicion(
        "Vía de salida",
        "Elaboración propia sobre el régimen de propiedad industrial",
        "Mecanismo por el que un resultado de investigación pasa a ser usado por "
        "alguien distinto de quien lo obtuvo. Hay tres, y cada una decide quién "
        "queda como titular del resultado, quién asume el riesgo técnico y con qué "
        "capital se financia el paso siguiente.",
        "i-agreement",
    )
    + "\n"
    + figura(
        "s2-figuras-salida",
        "Cinco requisitos exigidos por cada una de las tres vías de salida",
        "<b>La licencia es la única que no obliga a constituir empresa; la "
        "<i>startup</i>, la única que exige capital externo de riesgo.</b>",
    )
    + "\n"
    + criterio(
        "La vía se elige por el requisito que falta. Sin socio que ya opere en el "
        "mercado de destino queda descartada la licencia; sin equipo a tiempo completo "
        "quedan descartadas la <i>spin-off</i> y la <i>startup</i>."
    )
    + "\n"
    + fuente_pie(F_INDECOPI, F_LEY_31250)
)


LICENCIA_SPINOFF = envolver(
    cabecera("01 · Las tres vías de salida",
             "Licencia y <i>spin-off</i>: titular, riesgo y retorno de cada vía", "i-scale")
    + "\n"
    + definicion(
        "Licencia de explotación",
        "Régimen de propiedad industrial",
        "Autorización que el titular de un derecho concede a un tercero para "
        "explotar el resultado durante un plazo y en un territorio determinados, a "
        "cambio de una contraprestación. El titular sigue siendo el mismo después "
        "de firmarla.",
        "i-agreement",
    )
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-agreement")}Licencia a una empresa que ya opera</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>La titularidad se queda en la universidad.</li>
\t\t\t\t\t\t\t<li>El riesgo de producción y de venta lo asume el licenciatario.</li>
\t\t\t\t\t\t\t<li>El ingreso llega como regalía sobre ventas o como pago fijo.</li>
\t\t\t\t\t\t\t<li>El resultado depende de la prioridad que le dé un tercero.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-rocket")}<i>Spin-off</i> creada desde el grupo</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>La titularidad se licencia o se aporta a la empresa nueva.</li>
\t\t\t\t\t\t\t<li>El riesgo técnico y comercial lo asume el propio equipo.</li>
\t\t\t\t\t\t\t<li>El ingreso llega como participación en el capital.</li>
\t\t\t\t\t\t\t<li>El resultado depende de la dedicación de sus fundadores.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + conclusion(
        "Cuál se elige",
        "Con un socio industrial identificado y un resultado que encaja en su línea "
        "de producto, la licencia entrega uso y evita constituir una empresa. "
        "Cuando el resultado exige desarrollo adicional que ninguna empresa quiere "
        "financiar, la <i>spin-off</i> es la única de las dos que lo mantiene vivo, "
        "y el precio es que el equipo pasa a asumir el riesgo.",
    )
    + "\n"
    + fuente_pie(F_INDECOPI, F_ODEI)
)


STARTUP_INDEPENDIENTE = envolver(
    cabecera("01 · Las tres vías de salida",
             "Constitución de una <i>startup</i> con resultado ajeno a la universidad", "i-rocket")
    + "\n"
    + definicion(
        "<i>Startup</i>",
        "Elaboración propia sobre Nguyen et al. (2024)",
        "Empresa nueva que busca un modelo de negocio repetible y escalable en "
        "condiciones de incertidumbre alta. Cuando el resultado que explota no "
        "pertenece a la universidad, la <i>startup</i> se constituye sin ella y sin "
        "acuerdo de licencia.",
        "i-rocket",
    )
    + "\n"
    + en_la_practica(
        "Un egresado que desarrolló el algoritmo con datos públicos y sin equipamiento "
        "del laboratorio constituye una <i>startup</i> sin deber nada a la "
        "universidad. Entrenado en el laboratorio, el mismo algoritmo exige acuerdo "
        "previo."
    )
    + "\n"
    + evitar(
        "Constituir la empresa antes de resolver la titularidad. Una reclamación "
        "pendiente de la universidad detiene la revisión previa del inversor, y el "
        "informe del BID de 2023 cuenta la propiedad comprometida entre los nueve "
        "obstáculos."
    )
    + "\n"
    + fuente_pie(F_NGUYEN, F_BID)
)


OBSTACULOS_SALIDA = envolver(
    cabecera("01 · Las tres vías de salida",
             "Nueve obstáculos al acceso a inversión institucional en <i>deep tech</i>, 2023", "i-alert")
    + "\n"
    + figura(
        "s2-obstaculos-salida",
        "Obstáculos que dejan a una empresa de <i>deep tech</i> fuera del alcance de la inversión institucional, 2023",
        "<b>Siete de los nueve dependen del equipo y del mercado elegido; dos se "
        "resuelven antes, en el acuerdo de titularidad.</b>",
    )
    + "\n"
    + dato_clave(
        "De las <b>340 empresas</b> de <i>deep tech</i> con inversión institucional en la "
        "región, <b>120</b> superaron el millón de dólares levantado y <b>220</b> "
        "quedaron por debajo. BID, 2023."
    )
    + "\n"
    + criterio(
        "Dos de los nueve se resuelven con documentos: la protección insuficiente y las "
        "barreras para licenciar. Ambos se leen en el reglamento de propiedad "
        "intelectual y en el convenio del fondo."
    )
    + "\n"
    + fuente_pie(F_BID)
)


INVENTOR_Y_TITULAR = envolver(
    cabecera("01 · Titular y explotador",
             "Titular, inventor y explotador de una invención en el régimen de propiedad industrial", "i-patent")
    + "\n"
    + definicion(
        "Titular",
        "Régimen de propiedad industrial",
        "Persona natural o jurídica a cuyo nombre se concede el derecho, y la única "
        "que puede autorizar la explotación, licenciarla, cederla o ejercerla ante "
        "un tercero. El inventor conserva el derecho a ser mencionado como tal en "
        "el documento, y ese derecho no se transfiere.",
        "i-patent",
    )
    + "\n"
    + figura(
        "s2-titularidad-cadena",
        "Mención de inventoría y derecho de explotación en la cadena de inventor a mercado",
        "<b>La mención como inventor se queda en el primer eslabón; el derecho a "
        "explotar y a cobrar viaja por contrato hasta el mercado.</b>",
    )
    + "\n"
    + criterio(
        "Cuatro preguntas ordenan la discusión de titularidad: quién concibió el "
        "resultado, con qué recursos se obtuvo, quién lo financió y quién va a "
        "explotarlo. Las cuatro respuestas se escriben antes de presentar la "
        "solicitud."
    )
    + "\n"
    + fuente_pie(F_INDECOPI, F_OMPI_PCT)
)


DONDE_SE_FIJA = envolver(
    cabecera("01 · Titular y explotador",
             "Titularidad según el origen del resultado: reglamento, convenio y acuerdo de cesión", "i-file")
    + "\n"
    + tabla(
        ["Origen del resultado", "Documento donde se fija la titularidad",
         "Qué hay que verificar antes de publicar"],
        [
            ["Trabajo con equipamiento y personal de la universidad",
             "Reglamento de propiedad intelectual de la universidad",
             "Si el reglamento reserva la titularidad a la institución y qué reparto de ingresos declara"],
            ["Proyecto con fondo público adjudicado",
             "Convenio de adjudicación, cláusula de propiedad intelectual",
             "Si el convenio obliga a poner el resultado a disposición y en qué plazo"],
            ["Proyecto con empresa asociada",
             "Convenio de colaboración entre las partes",
             "Si hay cotitularidad y quién puede licenciar sin permiso del otro"],
            ["Tesis o trabajo de un estudiante",
             "Acuerdo de cesión o de cotitularidad con el autor",
             "Si el autor firmó antes de que el resultado existiera, y con qué contraprestación"],
        ],
        titulo="Origen del resultado, documento que fija su titularidad y comprobación previa a la publicación",
    )
    + "\n"
    + criterio(
        "El documento manda sobre la costumbre. Un grupo puede llevar veinte años "
        "publicando sin conflicto y descubrir, al firmar la primera licencia, que el "
        "reglamento reservaba la titularidad a la institución."
    )
    + "\n"
    + aviso(
        "Ninguna de las cuatro situaciones se resuelve por defecto: la asignación "
        "la fija el documento correspondiente, y la Ley 31250 organiza el Sistema "
        "Nacional de Ciencia, Tecnología e Innovación dentro del que esos convenios "
        "se firman. Cuando el documento no existe, lo que hay no es una titularidad "
        "compartida: es una discusión pendiente."
    )
    + "\n"
    + fuente_pie(F_LEY_31250, F_INDECOPI)
)


CEDER_O_LICENCIAR = envolver(
    cabecera("01 · Titular y explotador",
             "Cesión y licencia: efecto sobre la titularidad", "i-agreement")
    + "\n"
    + definicion(
        "Cesión",
        "Régimen de propiedad industrial",
        "Transferencia de la titularidad del derecho a otra persona, que pasa a ser "
        "el nuevo titular y decide sola sobre él. Quien cede deja de poder "
        "licenciarlo, ejercerlo o negociarlo.",
        "i-agreement",
    )
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}Cuándo conviene licenciar</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Hay más de un mercado o más de un uso posible.</li>
\t\t\t\t\t\t\t<li>El grupo quiere seguir investigando sobre el resultado.</li>
\t\t\t\t\t\t\t<li>Interesa cobrar por volumen de uso y no una sola vez.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-alert")}Cuándo la cesión es la salida</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>El mantenimiento del derecho cuesta más de lo que rinde.</li>
\t\t\t\t\t\t\t<li>El comprador exige titularidad plena para invertir.</li>
\t\t\t\t\t\t\t<li>La universidad no tiene capacidad de vigilar la infracción.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + conclusion(
        "Cuál se elige",
        "La licencia es reversible y la cesión no. Con un solo comprador que exige "
        "titularidad plena y sin capacidad institucional de vigilar el derecho, la "
        "cesión resuelve; en cualquier otro escenario la licencia deja abiertas las "
        "opciones que la cesión cierra para siempre.",
    )
    + "\n"
    + fuente_pie(F_INDECOPI, F_OMPI_PCT)
)


PATENTE_REQUISITO = envolver(
    cabecera("01 · La patente",
             "Orden entre solicitud de patente y divulgación pública del resultado", "i-calendar")
    + "\n"
    + figura(
        "s2-reloj-patente",
        "Plazos del Tratado de Cooperación en materia de Patentes contados desde la fecha de prioridad",
        "<b>Los tres plazos corren desde la primera solicitud, y la divulgación "
        "anterior a ella no admite reparación.</b>",
    )
    + "\n"
    + aviso(
        "La novedad se pierde con cualquier divulgación previa que ponga el "
        "contenido a disposición del público: un artículo, una tesis en "
        "repositorio abierto, un póster de congreso o una demostración en feria. "
        "El orden correcto es solicitar y después publicar, y entre las dos cosas "
        "median días, no meses."
    )
    + "\n"
    + dato_clave(
        "El Tratado de Cooperación en materia de Patentes (PCT) permite pedir "
        "protección en varios países con una sola solicitud, y cuenta <b>157 estados "
        "contratantes</b> según el informe del BID de 2023."
    )
    + "\n"
    + fuente_pie(F_OMPI_PCT, F_BID)
)


TRES_PROTECCIONES = envolver(
    cabecera("01 · La patente",
             "Patente, modelo de utilidad y secreto empresarial: exigencia y vigencia de cada vía", "i-patent")
    + "\n"
    + tabla(
        ["Vía de protección", "Qué protege", "Qué exige", "Qué ocurre al publicar antes"],
        [
            ["Patente de invención",
             "Un producto o un procedimiento nuevo",
             "Novedad, nivel inventivo y aplicación industrial. Vigencia de 20 años desde la solicitud",
             "La divulgación previa destruye la novedad y con ella la patentabilidad"],
            ["Modelo de utilidad",
             "Una forma o configuración que mejora la función de un objeto",
             "Novedad y ventaja técnica, con exigencia inventiva menor. Vigencia de 10 años desde la solicitud",
             "El efecto es el mismo: la divulgación previa cierra la vía"],
            ["Secreto empresarial",
             "Información no divulgada con valor comercial",
             "Medidas efectivas para mantenerla reservada. No se registra y no caduca mientras se guarde",
             "Publicar lo extingue, y no queda derecho alguno que ejercer"],
        ],
        titulo="Tres vías de protección de un resultado, lo que exige cada una y el efecto de publicar antes de solicitarla",
    )
    + "\n"
    + criterio(
        "La vía se decide antes de escribir el artículo, con dos preguntas: si el "
        "resultado se reproduce leyendo la publicación y si alguien puede detectar su "
        "uso en un producto ajeno. La patente obliga a describirlo por completo."
    )
    + "\n"
    + fuente_pie(F_INDECOPI, F_OMPI_PCT)
)


PATENTE_ACTIVO = envolver(
    cabecera("01 · La patente",
             "Familias de patentes, solicitudes y jurisdicciones de la cartera de Establishment Labs, 2023", "i-fund")
    + "\n"
    + figura(
        "s2-escalera-jurisdicciones",
        "Cobertura territorial de una cartera de patentes, del país único a Establishment Labs, 2023",
        "<b>Veinticinco jurisdicciones sostienen 200 solicitudes agrupadas en 25 "
        "familias.</b> Los dos primeros escalones son criterio de cobertura.",
    )
    + "\n"
    + dato_clave(
        "Una familia de patentes reúne las solicitudes que protegen una misma "
        "invención en varios países. <b>Establishment Labs</b> sostiene <b>25 "
        "familias</b> y <b>200 solicitudes</b>, con una valorización de <b>1 800 "
        "millones de dólares</b>."
    )
    + "\n"
    + criterio(
        "El derecho vale donde está registrado. Antes de gastar en jurisdicciones se "
        "nombran los tres países del mercado y los dos donde el competidor puede "
        "fabricar: esas cinco se protegen primero."
    )
    + "\n"
    + fuente_pie(
        F_BID,
        "Elaboración propia · criterio de cobertura territorial",
    )
)


DEEP_TECH = envolver(
    cabecera("01 · <i>Deep tech</i>",
             "<i>Deep tech</i>: definición, rasgos distintivos y tasa de fracaso, revisión de 2024", "i-bolt")
    + "\n"
    + definicion(
        "<i>Deep tech</i>",
        "Nguyen et al. (2024)",
        "Empresa nueva impulsada por ciencia, cuyo producto nace de un avance "
        "científico o de ingeniería y no de la recombinación de tecnologías ya "
        "disponibles. Su desarrollo es secuencial, largo y costoso, y sus "
        "fundadores suelen tener doctorado o posgrado técnico.",
        "i-bolt",
    )
    + "\n"
    + figura(
        "s2-deep-tech-frente-digital",
        "Cinco rasgos que separan una empresa de <i>deep tech</i> de una empresa digital, 2024",
        "<b>La diferencia se concentra en el ciclo de desarrollo: donde la digital "
        "itera rápido y barato, la profunda avanza por etapas encadenadas.</b>",
    )
    + "\n"
    + dato_clave(
        "La tasa de fracaso de los emprendimientos de <i>deep tech</i> es del <b>90 % "
        "o más</b>, atribuida a la barrera de entrada alta, el desarrollo largo y la "
        "inversión inicial elevada. Revisión de seis casos, 2024."
    )
    + "\n"
    + fuente_pie(F_NGUYEN)
)


PROCESO_DEEP_TECH = envolver(
    cabecera("01 · <i>Deep tech</i>",
             "Fases y actividades del proceso emprendedor en <i>deep tech</i>, seis casos, 2024", "i-flow")
    + "\n"
    + figura(
        "s2-proceso-deep-tech",
        "Cinco fases y seis actividades del proceso emprendedor en <i>deep tech</i>, seis casos, 2024",
        "<b>Las dos actividades de la cuarta fase ocurren en paralelo: buscar "
        "dinero y desarrollar el producto son la misma etapa.</b>",
    )
    + "\n"
    + criterio(
        "El desarrollo del producto ocurre <b>después</b> de constituir la empresa y "
        "absorbe el mayor esfuerzo en los primeros uno a tres años. Un cronograma que "
        "sitúa la constitución al final contradice los seis casos de 2024."
    )
    + "\n"
    + en_la_practica(
        "En los seis casos los fundadores tenían formación técnica: control y sistemas "
        "dinámicos, ingeniería industrial o doctorado en ingeniería. El único sin ese "
        "perfil incorporó un socio con cuatro años en inteligencia artificial."
    )
    + "\n"
    + fuente_pie(F_NGUYEN)
)


RONDAS_DEEP_TECH = envolver(
    cabecera("01 · <i>Deep tech</i>",
             "Montos de nueve rondas de financiamiento en <i>deep tech</i>, 2015-2022", "i-fund")
    + "\n"
    + figura(
        "s2-rondas-deep-tech",
        "Nueve rondas de financiamiento de cinco empresas de <i>deep tech</i>, en millones de dólares, 2015-2022",
        "<b>El monto no crece con la letra de la ronda: una Serie B de 0,159 "
        "millones convive con otra de 200 millones el mismo año.</b>",
    )
    + "\n"
    + dato_clave(
        "Las nueve rondas van de <b>0,159 millones</b> a <b>200 millones de "
        "dólares</b>: un factor de mil doscientos entre la menor y la mayor. Las "
        "empresas aparecen con letra y sin nombre porque el estudio las anonimiza. "
        "Datos de 2015 a 2022."
    )
    + "\n"
    + criterio(
        "La etiqueta de la ronda describe el orden de llegada del inversor y no el "
        "tamaño del cheque. Al presentar un plan de financiamiento se declara el "
        "monto, el uso y el hito técnico que ese monto compra; la letra sobra."
    )
    + "\n"
    + fuente_pie(F_NGUYEN)
)


INTENCION_HELICES = envolver(
    cabecera("01 · Qué mueve a un investigador",
             "Apoyo de universidad, Estado y empresa sobre la intención emprendedora académica, 2019", "i-network")
    + "\n"
    + figura(
        "s2-helices-intencion",
        "Coeficientes de trayectoria de las tres hélices sobre la intención emprendedora académica, 310 investigadores, 2019",
        "<b>La universidad casi duplica al Estado, y el apoyo empresarial no "
        "alcanza significación estadística.</b>",
    )
    + "\n"
    + dato_clave(
        "Sobre <b>310 investigadores jóvenes</b>, el apoyo de la universidad pesa "
        "<b>0,421</b>; el del Estado, <b>0,232</b>; el de la empresa, <b>0,037</b> con "
        "p de 0,318. Mínimos cuadrados parciales, 2019."
    )
    + "\n"
    + conclusion(
        "Qué se sigue para un grupo universitario",
        "La palanca que más mueve la intención de fundar está dentro de la propia "
        "institución: reglamento claro, oficina que acompañe y programas que "
        "reconozcan el emprendimiento como trabajo académico. Los autores leen el "
        "coeficiente empresarial bajo como señal de vínculo débil entre academia e "
        "industria en el país estudiado.",
    )
    + "\n"
    + fuente_pie(F_SAMO)
)


QUIEN_EMPRENDE = envolver(
    cabecera("01 · Qué mueve a un investigador",
             "Perfil ocupacional y de sexo de los 310 investigadores encuestados, 2019", "i-users")
    + "\n"
    + figura(
        "s2-quien-emprende",
        "Composición ocupacional de 310 investigadores jóvenes encuestados, 2019",
        "<b>Un tercio de la muestra no tiene ninguna experiencia laboral, y solo "
        "diecinueve de los 310 ya dirigen una empresa.</b>",
    )
    + "\n"
    + dato_clave(
        "De los <b>310 encuestados</b>, <b>107</b> no tienen experiencia laboral (34,5 "
        "%), <b>87</b> son profesionales en la universidad (28,1 %) y <b>19</b> ya "
        "emprenden (6,1 %). El 64,5 % son mujeres. Encuesta de 2019."
    )
    + "\n"
    + conclusion(
        "Qué dice esta composición",
        "La intención de fundar se mide casi siempre en gente que todavía no ha "
        "fundado nada, y ese es el límite del dato. El grupo con experiencia "
        "empresarial es tan pequeño que ningún resultado del estudio se puede leer "
        "como el comportamiento de quien ya emprendió.",
    )
    + "\n"
    + fuente_pie(F_SAMO)
)


LO_QUE_NO_EXPLICA = envolver(
    cabecera("01 · Qué mueve a un investigador",
             "Alcance explicativo del modelo de las tres hélices y motivos declarados para fundar", "i-search")
    + "\n"
    + figura(
        "s2-varianza-intencion",
        "Varianza de la intención emprendedora académica explicada por el modelo de las tres hélices, 310 investigadores, 2019",
        "<b>El modelo declara su propio hueco: el 58,8 % corresponde a variables "
        "que el estudio no incluyó.</b> La muestra es de un solo país.",
    )
    + "\n"
    + criterio(
        "Tres motivos aparecen en los seis casos de <i>deep tech</i> de 2024 y se "
        "verifican antes de fundar: interés propio por la tecnología, competencia "
        "acreditada en el campo y una carencia concreta detectada en él."
    )
    + "\n"
    + conclusion(
        "Con qué se cierra el tema",
        "Un resultado sale de la universidad cuando alguien decide llevarlo, la "
        "titularidad está escrita y la protección se solicitó antes de publicar. "
        "Las tres condiciones se comprueban con documentos que existen o no "
        "existen, y ninguna depende de la calidad científica del resultado.",
    )
    + "\n"
    + fuente_pie(F_SAMO, F_NGUYEN)
)


def _cond(clave, rotulo, ayuda, marcado=False):
    """Casilla de una condición de origen del resultado.

    Arrancan todas desmarcadas: así el recorrido de extremo a extremo va del
    caso de un solo titular al de cuatro documentos que concordar, y el
    veredicto cambia dos veces por el camino (METODOLOGIA.md §3.3).
    """
    ch = " checked" if marcado else ""
    return f"""\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" data-origen="{clave}"{ch} />
\t\t\t\t\t\t\t<span><b>{rotulo}</b><span class="crit__help">{ayuda}</span></span>
\t\t\t\t\t\t</label>"""


TITULARIDAD_SIM = envolver(
    cabecera("01 · Titular y explotador",
             "Documentos de titularidad exigidos según las cuatro condiciones de origen del resultado", "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="titularidad" data-animate="fade-up">
\t\t\t\t\t<div class="crit">
{_cond("universidad", "Equipamiento o personal de la universidad", "El trabajo se hizo con recursos de la institución")}
{_cond("fondo", "Fondo público adjudicado", "PROCIENCIA, ProInnóvate u otro concurso del Estado")}
{_cond("empresa", "Empresa asociada en el proyecto", "Aporta contrapartida, personal o instalaciones")}
{_cond("estudiante", "Autoría de un estudiante o tesista", "El resultado nace de un trabajo conducente a grado")}
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t<span class="sim__badge" id="ti-veredicto" data-estado="ok">Un solo titular</span>
\t\t\t\t\t\t<span class="sim__what" id="ti-detalle"></span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-file")}Documentos que hay que tener firmados</h3>
\t\t\t\t\t\t\t<ul id="ti-docs"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Lo que queda sin resolver</h3>
\t\t\t\t\t\t\t<ul id="ti-riesgo"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">El veredicto cambia dos veces
\t\t\t\tal recorrer las cuatro casillas: con una condición la titularidad pasa a
\t\t\t\testar compartida, y con tres o más el reparto exige concordar documentos
\t\t\t\tque se firmaron en momentos distintos.</p>"""
    + "\n"
    + criterio(
        "Cada condición marcada añade un documento y un firmante. La cláusula de "
        "titularidad se negocia cuando el proyecto se formula, que es el momento en el "
        "que todas las partes todavía necesitan algo de las demás."
    )
    + "\n"
    + fuente_pie(F_LEY_31250, F_INDECOPI)
)


TITULARIDAD_JS = """\t\t<script type="module">
\t\t\t// Cada condición de origen del resultado añade un documento y un
\t\t\t// firmante. El veredicto cambia dos veces al recorrer las cuatro
\t\t\t// casillas: con una condición la titularidad pasa a estar compartida y
\t\t\t// con tres o más hay que concordar documentos firmados en momentos
\t\t\t// distintos. Una simulación que no cambia de conclusión no demuestra
\t\t\t// nada (METODOLOGIA.md §3.3).
\t\t\tconst ORIGENES = {
\t\t\t\tuniversidad: {
\t\t\t\t\tdoc: "Reglamento de propiedad intelectual de la universidad",
\t\t\t\t\triesgo: "Reparto de ingresos entre institución, grupo e inventores" },
\t\t\t\tfondo: {
\t\t\t\t\tdoc: "Convenio de adjudicación, cláusula de propiedad intelectual",
\t\t\t\t\triesgo: "Obligación de poner el resultado a disposición, y su plazo" },
\t\t\t\tempresa: {
\t\t\t\t\tdoc: "Convenio de colaboración con la empresa asociada",
\t\t\t\t\triesgo: "Quién puede licenciar sin permiso del cotitular" },
\t\t\t\testudiante: {
\t\t\t\t\tdoc: "Acuerdo de cesión o de cotitularidad con el autor",
\t\t\t\t\triesgo: "Firma del autor obtenida antes de que el resultado existiera" },
\t\t\t};

\t\t\tconst BASE_DOC = "Acuerdo entre los autores del resultado";

\t\t\tconst casillas = [...document.querySelectorAll('.crit__box input')];
\t\t\tconst veredicto = document.getElementById("ti-veredicto");
\t\t\tconst detalle = document.getElementById("ti-detalle");
\t\t\tconst docs = document.getElementById("ti-docs");
\t\t\tconst riesgo = document.getElementById("ti-riesgo");

\t\t\tconst lista = (nodo, xs) => {
\t\t\t\tnodo.innerHTML = xs.length
\t\t\t\t\t? xs.map((x) => "<li>" + x + "</li>").join("")
\t\t\t\t\t: "<li>Nada pendiente con esta combinación de origen.</li>";
\t\t\t};

\t\t\tfunction pintar() {
\t\t\t\tconst activos = casillas
\t\t\t\t\t.filter((c) => c.checked)
\t\t\t\t\t.map((c) => c.dataset.origen);

\t\t\t\tlista(docs, [BASE_DOC].concat(activos.map((k) => ORIGENES[k].doc)));
\t\t\t\tlista(riesgo, activos.map((k) => ORIGENES[k].riesgo));

\t\t\t\tif (activos.length === 0) {
\t\t\t\t\tveredicto.textContent = "Un solo titular";
\t\t\t\t\tveredicto.dataset.estado = "ok";
\t\t\t\t\tdetalle.textContent = "El resultado no toca recursos, fondos ni terceros: la titularidad se fija en el acuerdo entre sus autores y una sola firma la cierra.";
\t\t\t\t} else if (activos.length < 3) {
\t\t\t\t\tveredicto.textContent = "Titularidad compartida";
\t\t\t\t\tveredicto.dataset.estado = "warn";
\t\t\t\t\tdetalle.textContent = "Con " + activos.length + (activos.length === 1 ? " condición" : " condiciones") + " de origen hay " + (activos.length + 1) + " documentos que tienen que decir lo mismo. Se leen antes de solicitar protección.";
\t\t\t\t} else {
\t\t\t\t\tveredicto.textContent = "Reparto por concordar";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "Con " + activos.length + " condiciones de origen, los " + (activos.length + 1) + " documentos se firmaron en momentos distintos y pueden contradecirse. La contradicción aparece cuando el resultado empieza a valer algo.";
\t\t\t\t}
\t\t\t}
\t\t\tfor (const c of casillas) c.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


# ==========================================================================
# 02 · CONTENIDO DEL TEMA B
# ==========================================================================

def definicion(termino, fuente, cuerpo, icono="i-book"):
    """Bloque de definición. Nombra SIEMPRE el término que define."""
    return f"""\t\t\t\t<div class="def" data-animate="fade-up">
\t\t\t\t\t<div class="def__label">{ico(icono)}Definición
\t\t\t\t\t\t<span class="def__term">{termino}</span>
\t\t\t\t\t\t<span class="def__src">{fuente}</span>
\t\t\t\t\t</div>
\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t</div>"""


def conclusion(rotulo, cuerpo, icono="i-check"):
    """Cierre de la lámina. El rótulo va arriba, con su icono, y el texto debajo.

    `cuerpo` es una oración que se sostiene sola, con mayúscula inicial
    (METODOLOGIA.md §17.12).

    El icono por omisión es `i-check`, que es el que §7.2 asigna al bloque de
    conclusión. `clase-01.py` pone `i-flag`, que NO existe en
    public/course-icons.svg: `audit-mazo.py` lo detecta y el hueco se ve en las
    cinco láminas de esta tanda que cierran con conclusión. Conviene corregirlo
    también allí.
    """
    return f"""\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<div class="conclusion__label">{ico(icono)}{rotulo.rstrip(":")}</div>
\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t</div>"""


def aviso(cuerpo, rotulo="Atención"):
    return f"""\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t<div class="warn-box__label">{ico("i-alert")}{rotulo}</div>
\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t</div>"""


# Fuentes del tramo peruano. Son las MISMAS cifras verificadas en la sesión 1 y
# se citan con el mismo texto literal: dos sesiones que citen el mismo documento
# de dos formas distintas rompen la lámina de referencias del cierre.
F_POLCTI = ("CONCYTEC (2024), <i>Política Nacional de CTI al 2030</i>, Tabla 13 "
            "· documento público")
F_POLCTI_DIAG = ("CONCYTEC (2024), <i>Política Nacional de CTI al 2030</i>, "
                 "diagnóstico · documento público")
F_GII = ("OMPI (2025), <i>Global Innovation Index 2025</i>, versión ejecutiva "
         "· CC BY 4.0 IGO")
F_DS = ("DS 093-2025-PCM, <i>El Peruano</i>, 15 de julio de 2025 · norma de "
        "dominio público")
F_RENACYT = "RENACYT · Registro Nacional de Investigadores, dato de 2023"

# Referencia secundaria: los cinco factores organizativos de una oficina de
# transferencia son de Siegel, Waldman y Link, y se leen recogidos en el apartado
# 2.3 de Odei y Novák. Se declara así porque el artículo original no se descargó.
F_SIEGEL = ("Siegel, Waldman y Link (2003), <i>Research Policy</i> 32(1):27, "
            "recogidos por Odei y Novák · referencia secundaria")


def _det(clave, rotulo, ayuda, marcado=True):
    """Casilla de un determinante medido. Misma marca que el clasificador de la
    sesión 1: si las dos interactivas usan la misma casilla, el CSS ya existe y
    el control se reconoce sin volver a aprenderlo."""
    ch = " checked" if marcado else ""
    return f"""\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" data-det="{clave}"{ch} />
\t\t\t\t\t\t\t<span><b>{rotulo}</b><span class="crit__help">{ayuda}</span></span>
\t\t\t\t\t\t</label>"""


# ==========================================================================
# 02 · LA OFICINA DE TRANSFERENCIA
# ==========================================================================

OTT_RUTA = envolver(
    cabecera("02 · Oficina de transferencia", "Recorrido del resultado en la oficina de transferencia", "i-network")
    + "\n"
    + definicion(
        "Oficina de transferencia tecnológica",
        "Hunady et al. 2019",
        "Unidad que recibe el resultado ya protegido y elige la vía de explotación: "
        "licenciarlo a una empresa o constituir una <i>spin-off</i>.",
    )
    + "\n"
    + f"""\t\t\t\t<div class="blockdiagram" data-animate="fade-up">
\t\t\t\t\t<div class="bd-node">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-search")}Competencias</div>
\t\t\t\t\t\t<p class="bd-node__body">Identificación de las competencias clave de la institución.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Etapa 1</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow">→</span>
\t\t\t\t\t<div class="bd-node">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-fund")}Financiamiento</div>
\t\t\t\t\t\t<p class="bd-node__body">Fondos propios, de empresa o públicos para la investigación.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Etapa 2</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow">→</span>
\t\t\t\t\t<div class="bd-node">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-simulate")}Resultado</div>
\t\t\t\t\t\t<p class="bd-node__body">Investigación, resultados y ensayo de esos resultados.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Etapa 3</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow">→</span>
\t\t\t\t\t<div class="bd-node">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-bulb")}Invención</div>
\t\t\t\t\t\t<p class="bd-node__body">La invención o la innovación queda declarada ante la institución.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Etapa 4</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + f"""\t\t\t\t<div class="blockdiagram" data-animate="fade-up">
\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-patent")}Decisión de patentar</div>
\t\t\t\t\t\t<p class="bd-node__body">La institución resuelve si protege el resultado y con qué figura.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Etapa 5 · antes de divulgar</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow">→</span>
\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-building")}Oficina de transferencia</div>
\t\t\t\t\t\t<p class="bd-node__body">Elige la vía de explotación y negocia sus condiciones.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Etapa 6 · la decisión</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow">→</span>
\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-agreement")}Licencia</div>
\t\t\t\t\t\t<p class="bd-node__body">Alquiler de la tecnología a una empresa que ya existe.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Vía A</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t<div class="bd-node__title">{ico("i-rocket")}<i>Spin-off</i></div>
\t\t\t\t\t\t<p class="bd-node__body">Empresa nueva constituida para explotar el resultado.</p>
\t\t\t\t\t\t<span class="bd-node__meta">Vía B</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + criterio(
        "La decisión entre licencia y <i>spin-off</i> llega con la protección ya "
        "resuelta: en el modelo por etapas de Hunady et al. (2019) la decisión de "
        "patentar precede a la oficina. Divulgar antes cierra las dos vías."
    )
    + "\n"
    + fuente_pie(F_HUNADY)
)


OTT_FACTORES = envolver(
    cabecera("02 · Oficina de transferencia", "Factores organizativos de una oficina de transferencia", "i-rubric")
    + "\n"
    + tabla(
        ["Factor", "Qué exige de la oficina", "Cómo se comprueba desde fuera"],
        [
            ["Sistema de recompensas", "Retribuir a la oficina por el resultado transferido", "El reglamento publica el porcentaje"],
            ["Gestión del personal", "Dirigir el equipo con carga y metas propias", "Hay jefatura con dedicación declarada"],
            ["Política institucional", "Una norma interna que promueve la transferencia", "La norma está aprobada y fechada"],
            ["Personal calificado", "Elevar la calificación de quien atiende la oficina", "El perfil de puesto exige propiedad intelectual"],
            ["Barreras culturales", "Retirar los obstáculos culturales y de información", "Existe un canal de divulgación de invenciones"],
        ],
        titulo="Los cinco factores organizativos de una oficina de transferencia y su comprobación",
        clases="table--full",
    )
    + "\n"
    + criterio(
        "Ninguno de los cinco depende del volumen de investigación, y la ausencia de "
        "cualquiera se detecta leyendo el reglamento interno."
    )
    + "\n"
    + fuente_pie(F_ODEI, F_SIEGEL)
)


OTT_LIMITES = envolver(
    cabecera("02 · Oficina de transferencia",
             "Reparto de tareas entre el grupo y la oficina de transferencia", "i-users")
    + "\n"
    + figura(
        "s2-reparto-transferencia",
        "Reparto de ocho tareas entre el grupo de investigación y la oficina de transferencia tecnológica",
        "<b>Las dos primeras tareas del grupo son requisito de las dos primeras de "
        "la oficina.</b> Sin ellas el expediente no llega a existir.",
    )
    + "\n"
    + conclusion(
        "Dónde se detiene la transferencia",
        "Sin ensayo documentado y sin descripción técnica la oficina no tiene qué "
        "proteger ni qué ofrecer. Las otras dos tareas del grupo, la dedicación de "
        "quien va a fundar y la relación con el receptor, tampoco las puede aportar "
        "la oficina en su lugar.",
    )
    + "\n"
    + dato_clave(
        "En el consorcio farmacéutico irlandés de O’Dwyer et al. (2022), el gestor de "
        "proyecto y la oficina de transferencia aparecen como facilitadores solo en la "
        "tercera fase, entre los años cuatro y siete."
    )
    + "\n"
    + fuente_pie(F_ODWYER, F_ODEI)
)


# ==========================================================================
# 02 · DETERMINANTES MEDIDOS DE LA CREACIÓN DE SPIN-OFFS
# ==========================================================================

SPINOFF_EMBUDO = envolver(
    cabecera("02 · Determinantes medidos", "Creación de <i>spin-offs</i> por universidad y su dispersión, Reino Unido, curso 2017/18", "i-flow")
    + "\n"
    + figura(
        "s2-embudo-patentes",
        "Divulgaciones, patentes y <i>spin-offs</i> por universidad, media de 164 instituciones del Reino Unido, curso 2017/18",
        "<b>Cada etapa pierde cerca de la mitad de los casos, y la caída mayor está "
        "entre la divulgación y la solicitud.</b>",
    )
    + "\n"
    + dato_clave(
        "La encuesta cuenta por separado 5,57 <i>spin-offs</i> con participación de la "
        "universidad, 1,54 sin participación y 2,79 empresas creadas por el personal: "
        "9,90 empresas nuevas por institución y año, curso 2017/18."
    )
    + "\n"
    + aviso(
        "La media esconde el reparto. En esas mismas 164 universidades el mínimo de "
        "<i>spin-offs</i> es cero y el máximo, 70; en patentes concedidas, cero y "
        "321. La cartera acumulada tiene media de 125,29 patentes y desviación "
        "típica de 375,87. <b>Citar la media como descripción de una universidad "
        "cualquiera invierte el dato.</b>"
    )
    + "\n"
    + fuente_pie(F_ODEI)
)


SPINOFF_COEFICIENTES = envolver(
    cabecera("02 · Determinantes medidos", "Cinco determinantes de la creación de <i>spin-offs</i> y su tamaño de efecto, 164 universidades", "i-chart")
    + "\n"
    + figura(
        "s2-coeficientes-spinoff",
        "Coeficientes de trayectoria y tamaños de efecto del modelo de ecuaciones estructurales, 164 universidades, curso 2017/18",
        "<b>La patente encabeza las cinco trayectorias con un tamaño de efecto de "
        "0,724 y media además el efecto del financiamiento.</b>",
    )
    + "\n"
    + dato_clave(
        "El modelo por mínimos cuadrados parciales <i>(PLS-SEM)</i> explica el 70 % de "
        "la varianza en la creación de <i>spin-offs</i> y el 38 % en la cartera de "
        "patentes, con p entre 0,001 y 0,022 en las cinco trayectorias."
    )
    + "\n"
    + conclusion(
        "Qué se sigue de esto:",
        "El financiamiento actúa por dos caminos. Uno directo sobre la creación de "
        "<i>spin-offs</i>, con coeficiente de 0,299, y otro a través de la patente, "
        "con coeficiente de 0,593. El segundo pesa casi el triple que el primero en "
        "tamaño de efecto, 0,553 frente a 0,186.",
    )
    + "\n"
    + fuente_pie(F_ODEI)
)


SPINOFF_NO_LINEAL = envolver(
    cabecera("02 · Determinantes medidos", "Especialización e intensidad doctoral frente a la creación de <i>spin-offs</i>, Europa, 2011-2014", "i-scale")
    + "\n"
    + figura(
        "s2-no-linealidad-spinoff",
        "Funciones ajustadas de especialización y de intensidad doctoral sobre la probabilidad de crear una <i>spin-off</i>, instituciones europeas, 2011-2014",
        "<b>La especialización toca su mínimo en 0,70 y la matrícula doctoral su "
        "máximo en 1,4 %.</b> Ambas son la función ajustada publicada.",
    )
    + "\n"
    + dato_clave(
        "Hunady et al. (2019) estimaron modelos probit y logit sobre <b>2 465 "
        "instituciones</b> de educación superior de 36 países europeos, con datos del "
        "Registro Europeo de Educación Terciaria <i>(ETER)</i> de 2011/12 a 2014/15."
    )
    + "\n"
    + criterio(
        "Otros dos indicadores resultan significativos al 1 %: la proporción de "
        "estudiantes extranjeros, con coeficiente de 3,07, y la proporción de ingresos "
        "por matrícula, con coeficiente de −4,61."
    )
    + "\n"
    + fuente_pie(F_HUNADY)
)


DETERMINANTES_JS = """\t\t<script type="module">
\t\t\t// Los seis determinantes que las dos fuentes miden como significativos se
\t\t\t// marcan uno a uno y el veredicto cambia. Hay tres estados y la casilla de
\t\t\t// la patente decide por sí sola el paso al tercero: es la trayectoria con
\t\t\t// el mayor tamaño de efecto del modelo y además media el efecto del
\t\t\t// financiamiento, así que su ausencia no se compensa con las otras cinco.
\t\t\t//
\t\t\t// Cada entrada guarda la cifra PUBLICADA, no una puntuación inventada: los
\t\t\t// coeficientes de los dos estudios se estimaron en modelos distintos y
\t\t\t// sumarlos daría un número sin significado (METODOLOGIA.md §17.15).
\t\t\tconst DETERMINANTES = {
\t\t\t\tfinanciamiento: { rotulo: "Financiamiento de I+D", efecto: 0.186,
\t\t\t\t\tnota: "coeficiente de 0,299 hacia la <i>spin-off</i>" },
\t\t\t\tpatente: { rotulo: "Cartera de patentes", efecto: 0.724,
\t\t\t\t\tnota: "f² de 0,724, el mayor de las cinco vías" },
\t\t\t\trecompensa: { rotulo: "Recompensas", efecto: 0.029,
\t\t\t\t\tnota: "presente en el 79 % de 164 universidades" },
\t\t\t\tdoctorado: { rotulo: "Matrícula doctoral", efecto: 0,
\t\t\t\t\tnota: "el máximo del modelo cae en el 1,4 %" },
\t\t\t\tespecializacion: { rotulo: "Especialización", efecto: 0,
\t\t\t\t\tnota: "el mínimo cae en un índice de 0,70" },
\t\t\t\tmatriculas: { rotulo: "Ingresos por matrícula", efecto: 0,
\t\t\t\t\tnota: "coeficiente de \\u22124,61 al 1 %" },
\t\t\t};

\t\t\t// El recuento se escribe en palabra y no en cifra: la insignia dice «Cinco
\t\t\t// de seis» y no «5 de seis», que era la mezcla que quedaba al redactar el
\t\t\t// estado completo aparte del parcial.
\t\t\tconst PALABRAS = ["Ninguno", "Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis"];

\t\t\tconst casillas = [...document.querySelectorAll('.crit__box input[data-det]')];
\t\t\tconst veredicto = document.getElementById("dt-veredicto");
\t\t\tconst detalle = document.getElementById("dt-detalle");
\t\t\tconst reunidos = document.getElementById("dt-reunidos");
\t\t\tconst ausentes = document.getElementById("dt-ausentes");

\t\t\tfunction fila(clave) {
\t\t\t\tconst d = DETERMINANTES[clave];
\t\t\t\treturn "<li><b>" + d.rotulo + "</b> · " + d.nota + "</li>";
\t\t\t}

\t\t\tfunction pintar() {
\t\t\t\tconst si = casillas.filter((c) => c.checked).map((c) => c.dataset.det);
\t\t\t\tconst no = casillas.filter((c) => !c.checked).map((c) => c.dataset.det);
\t\t\t\treunidos.innerHTML = si.length ? si.map(fila).join("")
\t\t\t\t\t: "<li>Ninguno de los seis está acreditado.</li>";
\t\t\t\tausentes.innerHTML = no.length ? no.map(fila).join("")
\t\t\t\t\t: "<li>Ninguno: el perfil está completo.</li>";

\t\t\t\tif (no.length === 0) {
\t\t\t\t\tveredicto.textContent = "Seis de seis";
\t\t\t\t\tveredicto.dataset.estado = "ok";
\t\t\t\t\tdetalle.innerHTML = "El perfil reúne los seis determinantes que los dos estudios miden como significativos sobre la creación de <i>spin-offs</i>.";
\t\t\t\t} else if (no.includes("patente")) {
\t\t\t\t\tveredicto.textContent = "Falta la vía de mayor peso";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.innerHTML = "Sin cartera de patentes queda fuera la trayectoria de mayor tamaño de efecto del modelo, f² de 0,724, que además media el efecto del financiamiento sobre la creación de <i>spin-offs</i>.";
\t\t\t\t} else {
\t\t\t\t\t// Se nombra el ausente de mayor tamaño de efecto publicado. Los tres
\t\t\t\t\t// determinantes de Hunady et al. llevan efecto 0 porque su artículo no
\t\t\t\t\t// publica f²: van al final del orden, no al principio.
\t\t\t\t\tconst peor = no.slice().sort(
\t\t\t\t\t\t(a, b) => DETERMINANTES[b].efecto - DETERMINANTES[a].efecto)[0];
\t\t\t\t\t// Construcción con dos puntos y sin artículo: los seis rótulos tienen
\t\t\t\t\t// género distinto y «Falta el/la ...» obligaría a concordar en código.
\t\t\t\t\tveredicto.textContent = PALABRAS[si.length] + " de seis";
\t\t\t\t\tveredicto.dataset.estado = "warn";
\t\t\t\t\tdetalle.innerHTML = (no.length === 1
\t\t\t\t\t\t? "Determinante ausente: "
\t\t\t\t\t\t: "Faltan " + PALABRAS[no.length].toLowerCase() +
\t\t\t\t\t\t  " determinantes, y el de mayor efecto publicado es: ") +
\t\t\t\t\t\tDETERMINANTES[peor].rotulo + " · " + DETERMINANTES[peor].nota + ".";
\t\t\t\t}
\t\t\t}
\t\t\tfor (const c of casillas) c.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


DETERMINANTES_SIM = envolver(
    cabecera("02 · Determinantes medidos", "Perfil institucional según los seis determinantes medidos de la creación de <i>spin-offs</i>", "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="determinantes" data-animate="fade-up">
\t\t\t\t\t<div class="crit">
{_det("financiamiento", "Financiamiento de I+D adjudicado", "Convenio o resolución")}
{_det("patente", "Cartera de patentes propia", "Expediente o patente concedida")}
{_det("recompensa", "Esquema de recompensas al investigador", "Porcentaje en el reglamento")}
{_det("doctorado", "Matrícula doctoral en el tramo intermedio", "Proporción de doctorandos")}
{_det("especializacion", "Especialización alta o muy amplia", "Concentración por campo")}
{_det("matriculas", "Baja dependencia de los ingresos por matrícula", "Peso de las pensiones")}
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t<span class="sim__badge" id="dt-veredicto" data-estado="ok">Seis de seis</span>
\t\t\t\t\t\t<span class="sim__what" id="dt-detalle"></span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Determinantes reunidos, con su cifra publicada</h3>
\t\t\t\t\t\t\t<ul id="dt-reunidos"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Determinantes ausentes</h3>
\t\t\t\t\t\t\t<ul id="dt-ausentes"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Al desmarcar la cartera de
\t\t\t\tpatentes el veredicto pasa a rojo.</p>"""
    + "\n"
    + fuente_pie(F_ODEI, F_HUNADY)
)


# ==========================================================================
# 02 · BARRERAS DE LA COLABORACIÓN UNIVERSIDAD-EMPRESA
# ==========================================================================

BARRERAS_FASES_LAMINA = envolver(
    cabecera("02 · Barreras de la colaboración", "Cinco barreras de la colaboración universidad-empresa a lo largo de siete años", "i-alert")
    + "\n"
    + figura(
        "s2-barreras-intensidad",
        "Intensidad declarada de cinco barreras en las tres primeras fases del consorcio farmacéutico irlandés",
        "<b>Cuatro barreras bajan de fuerte a moderada y siguen presentes en la "
        "tercera fase.</b> Solo la de propiedad intelectual se resuelve.",
    )
    + "\n"
    + dato_clave(
        "El caso es un consorcio farmacéutico irlandés con dieciocho miembros "
        "fundadores, cinco universidades y nueve empresas multinacionales, con "
        "entrevistas de 50 a 105 minutos. La intensidad declarada tiene tres grados."
    )
    + "\n"
    + criterio(
        "La ausencia de acuerdo de propiedad intelectual se cierra firmándolo: consta "
        "como barrera en la segunda fase y como facilitador en la tercera. Las otras "
        "cuatro siguen presentes al año siete."
    )
    + "\n"
    + fuente_pie(F_ODWYER)
)


FACILITADORES_FASES_LAMINA = envolver(
    cabecera("02 · Barreras de la colaboración", "Facilitadores por fase en el consorcio farmacéutico irlandés", "i-network")
    + "\n"
    + figura(
        "s2-facilitadores-fase",
        "Facilitadores declarados por fase y por par de relación en el consorcio farmacéutico irlandés",
        "<b>De siete facilitadores en la fase embrionaria a diecisiete en la de "
        "compromiso.</b> Ninguno aparece en las tres fases.",
    )
    + "\n"
    + dato_clave(
        "Ningún facilitador aparece en las tres fases. En las dos primeras el común a "
        "los tres pares de relación es la experiencia previa en construir redes; en la "
        "tercera, la cohesión apoyada en la proximidad."
    )
    + "\n"
    + conclusion(
        "Cómo se lee la cuenta:",
        "El par universidad-universidad reúne seis facilitadores en la tercera fase, "
        "entre ellos la reciprocidad, la complementariedad de conocimiento y las "
        "recompensas extrínsecas, que no aparecen en los otros dos pares. La "
        "colaboración entre grupos académicos del mismo campo tiene su propio "
        "conjunto de condiciones.",
    )
    + "\n"
    + fuente_pie(F_ODWYER)
)


CONFIANZA_ACUERDO = envolver(
    cabecera("02 · Barreras de la colaboración",
             "Tipos de confianza por fase del consorcio farmacéutico irlandés", "i-agreement")
    + "\n"
    + definicion(
        "Confianza por reputación y confianza por integridad",
        "O’Dwyer et al. 2022",
        "Dos formas sucesivas de confianza entre socios. La primera se apoya en la "
        "trayectoria y la credibilidad declaradas del actor que convoca; la segunda, "
        "en el comportamiento observado durante el trabajo conjunto.",
        "i-agreement",
    )
    + "\n"
    + figura(
        "s2-cruce-confianza",
        "Recorrido de la confianza por las tres fases de un consorcio universidad-empresa, dieciocho miembros fundadores",
        "<b>El cruce de barrera a facilitador ocurre dentro de la segunda fase, "
        "entre los años uno y tres.</b> Es el único elemento que cambia de lado.",
    )
    + "\n"
    + criterio(
        "La confianza por integridad se produjo con actividades contables: reuniones "
        "trimestrales, doscientas jornadas de formación en tres sedes el primer año, "
        "y estancias de tres meses de doctorandos en las empresas."
    )
    + "\n"
    + evitar(
        "Convocar la primera reunión para negociar la propiedad intelectual. En el caso "
        "reconstruido el acuerdo aparece en la tercera fase, con la confianza por "
        "reputación ya establecida."
    )
    + "\n"
    + fuente_pie(F_ODWYER)
)


FINANCIAMIENTO_REPARTO = envolver(
    cabecera("02 · Barreras de la colaboración", "Reparto del fondo fundacional entre los cinco grupos académicos del consorcio irlandés", "i-fund")
    + "\n"
    + figura(
        "s2-cascada-sspc",
        "Financiamiento del consorcio farmacéutico irlandés, del fondo fundacional al presupuesto declarado, en millones de euros",
        "<b>El fondo fundacional de 7,7 millones atrajo cuarenta millones a los cinco "
        "años, tres cuartas partes de fuente pública.</b>",
    )
    + "\n"
    + dato_clave(
        "El reparto del fondo fundacional fue idéntico entre los cinco grupos "
        "académicos: mismo equipamiento y mismo número de personas contratadas. Los "
        "autores le atribuyen la condición de igualdad del consorcio."
    )
    + "\n"
    + en_la_practica(
        "El consorcio pasó de cinco universidades y nueve empresas multinacionales a "
        "diecisiete empresas farmacéuticas, treinta y seis investigadores principales, "
        "115 plazas de doctorado y 87 de posdoctorado."
    )
    + "\n"
    + fuente_pie(F_ODWYER)
)


# ==========================================================================
# 02 · EL DEEP TECH EN AMÉRICA LATINA
# ==========================================================================

DEEPTECH_REGION = envolver(
    cabecera("02 · <i>Deep tech</i> en la región", "Distribución y valor agregado del <i>deep tech</i> por país en América Latina, 2023", "i-globe")
    + "\n"
    + figura(
        "s2-deeptech-paises",
        "Empresas de <i>deep tech</i> con financiamiento institucional en América Latina y el Caribe, por país, 2023",
        "<b>Argentina, Brasil y Chile reúnen el 79 % de las empresas; el Perú tiene "
        "cinco, el 1 % del total.</b>",
    )
    + "\n"
    + dato_clave(
        "Chile concentra el 25 % del valor agregado, Brasil el 23 %, Argentina el 23 % "
        "y Costa Rica el 22 % con seis empresas. La más valiosa es <b>Establishment "
        "Labs</b>, costarricense, en 1 800 millones de dólares."
    )
    + "\n"
    + criterio(
        "El informe cuenta <b>24 empresas</b> valoradas por encima de 50 millones de "
        "dólares: tres sobre 500 millones, nueve entre 100 y 500 millones y doce entre "
        "50 y 100 millones. Auth0 queda fuera por estar ya adquirida."
    )
    + "\n"
    + fuente_pie(F_BID)
)


DEEPTECH_SECTORES = envolver(
    cabecera("02 · <i>Deep tech</i> en la región", "Biotecnología y los otros doce sectores del <i>deep tech</i> en América Latina, 2023", "i-layers")
    + "\n"
    + figura(
        "s2-deeptech-sectores",
        "Reparto de las empresas de <i>deep tech</i> de América Latina y el Caribe por sector tecnológico, 2023",
        "<b>La biotecnología sola reúne el 61 % de las 340 empresas; ninguna otra "
        "tecnología pasa del 11 %.</b>",
    )
    + "\n"
    + dato_clave(
        "La inteligencia artificial es el segundo sector con el 11 %, seguida de "
        "nanotecnología con el 6 %, tecnologías limpias con el 5 %, y espacio y "
        "movilidad avanzada con el 4 %. Las siete restantes suman el 9 %."
    )
    + "\n"
    + en_la_practica(
        "El informe atribuye el peso de la biotecnología al vínculo con la "
        "alimentación y la agricultura, a la biodiversidad disponible y al personal "
        "formado en el campo. Las siguientes en valor son NotCo y Bioceres."
    )
    + "\n"
    + fuente_pie(F_BID)
)


DEEPTECH_TALENTO = envolver(
    cabecera("02 · <i>Deep tech</i> en la región", "Personal de I+D y capital de riesgo por investigador, América Latina, 2023", "i-users")
    + "\n"
    + figura(
        "s2-talento-deeptech",
        "Personal de I+D en las empresas de <i>deep tech</i> frente al acervo de América Latina y el Caribe, 2023",
        "<b>Cinco mil personas de I+D en las empresas frente a 871 000 en la región: "
        "el acervo no es hoy la restricción.</b>",
    )
    + "\n"
    + dato_clave(
        "El capital de riesgo en <i>deep tech</i> por investigador y año es de <b>421 "
        "dólares</b> en la región y de <b>114 774</b> en Israel. La región tiene 968 "
        "investigadores por millón de habitantes; Israel, 8 342."
    )
    + "\n"
    + conclusion(
        "Cómo va cambiando:",
        "La inversión regional en <i>deep tech</i> pasó de 96 millones de dólares en "
        "2020, el 0,59 % de todo el capital de riesgo de la región, a 172 millones en "
        "2022, el 2,2 %. El informe proyecta veinte veces más en la década, hasta "
        "3 440 millones.",
    )
    + "\n"
    + fuente_pie(F_BID)
)


# ==========================================================================
# 02 · DE DÓNDE PARTE EL PERÚ Y CON QUÉ INSTRUMENTOS
# ==========================================================================
# Las cifras peruanas de este tramo son las MISMAS que verifica la sesión 1, con
# el mismo pie. Buscar cifras nuevas para repetir el argumento habría dejado dos
# valores distintos del mismo indicador en el mismo mazo.

PERU_PARTIDA = envolver(
    cabecera("02 · Punto de partida peruano",
             "Indicadores de partida del Perú frente a su referente en tres brechas, 2018-2023", "i-chart")
    + "\n"
    + figura(
        "s2-brechas-multiplos",
        "Razón entre el valor del referente y el valor peruano en tres indicadores de partida, 2018-2023",
        "<b>Dos brechas son de un orden de magnitud y la del número de empresas es "
        "de dos.</b> Cada indicador va con su propio referente.",
    )
    + "\n"
    + en_la_practica(
        "El BID cifra en menos de <b>20 millones de dólares</b> el valor del "
        "ecosistema peruano de <i>deep tech</i>. El país tiene <b>5 700 "
        "investigadores</b> en el RENACYT en 2023 y el <b>puesto 80 de 139</b> del "
        "<i>Global Innovation Index</i> 2025."
    )
    + "\n"
    + criterio(
        "Los tres determinantes se comprueban antes de proyectar una <i>spin-off</i>: "
        "financiamiento adjudicado con su resolución, expediente presentado ante "
        "INDECOPI y el porcentaje del inventor fijado en el reglamento."
    )
    + "\n"
    + fuente_pie(F_BID, F_POLCTI, F_DS, F_GII, F_RENACYT)
)


PERU_INSTRUMENTOS = envolver(
    cabecera("02 · Punto de partida peruano", "Cinco instrumentos peruanos de la transferencia", "i-building")
    + "\n"
    + tabla(
        ["Instrumento", "Qué tramo cubre", "Qué exige acreditar", "Enlace oficial"],
        [
            ["INDECOPI · patente de invención", "La protección previa a cualquier licencia", "Memoria descriptiva y reivindicaciones", '<a href="https://www.indecopi.gob.pe/">indecopi.gob.pe</a>'],
            ["INDECOPI · modelo de utilidad", "Protección de mejoras con menor exigencia de novedad", "Mejora funcional sobre un objeto conocido", '<a href="https://www.indecopi.gob.pe/">indecopi.gob.pe</a>'],
            ["OMPI · solicitud PCT", "La extensión de la protección a otros países", "Reivindicación de prioridad dentro de doce meses", '<a href="https://www.wipo.int/pct/es/">wipo.int/pct</a>'],
            ["ProInnóvate · desarrollo y validación", "El paso del prototipo al producto con empresa receptora", "Empresa formal y contrapartida en efectivo", '<a href="https://www.proinnovate.gob.pe/">proinnovate.gob.pe</a>'],
            ["ITP · Red CITE", "El ensayo que acredita la madurez del resultado", "Convenio con el centro y protocolo del ensayo", '<a href="https://www.gob.pe/952-centros-de-innovacion-productiva-y-transferencia-tecnologica-cite">gob.pe · Red CITE</a>'],
        ],
        titulo="Instrumentos peruanos que cubren tramos de la transferencia y lo que exige cada uno",
    )
    + "\n"
    + criterio(
        "Setenta y uno de los 164 instrumentos de ciencia, tecnología e innovación que "
        "operó el Estado peruano entre 2012 y 2018 pertenecían al sector Producción y "
        "38 al CONCYTEC. INDECOPI no opera instrumentos de financiamiento."
    )
    + "\n"
    + fuente_pie(F_LEY_31250, F_INDECOPI, F_OMPI_PCT, F_POLCTI)
)


PERU_MATRIZ = envolver(
    cabecera("02 · Punto de partida peruano", "Protección registrada y socio receptor: cuatro situaciones de un resultado peruano", "i-scale")
    + "\n"
    + figura(
        "s2-matriz-transferencia",
        "Ventanilla que corresponde a un resultado según su protección registrada y su socio receptor",
        "<b>Solo el cuadrante con protección registrada y receptor identificado "
        "admite un contrato de licencia o una <i>spin-off</i>.</b>",
    )
    + "\n"
    + criterio(
        "Cada cuadrante tiene su ventanilla y su orden. Con receptor identificado y "
        "sin protección, el registro va antes de cualquier reunión técnica: divulgar "
        "el resultado destruye la novedad y con ella la patentabilidad."
    )
    + "\n"
    + en_la_practica(
        "Un grupo con prototipo validado en campo y una cooperativa dispuesta a usarlo "
        "está en el cuadrante superior derecho si el expediente está presentado ante "
        "INDECOPI. Sin él, el primer producto es la memoria descriptiva."
    )
    + "\n"
    + fuente_pie(
        F_INDECOPI, F_OMPI_PCT,
        "Elaboración propia · correspondencia entre condición del resultado y ventanilla",
    )
)


PERU_PALANCAS = envolver(
    cabecera("02 · Punto de partida peruano", "Palancas públicas y universitarias de <i>deep tech</i> y sus casos regionales, 2023", "i-target")
    + "\n"
    + criterio(
        "El informe del BID documenta quince palancas públicas. Cuatro no tienen caso "
        "regional: fondos de contrapartida a la investigación aplicada, incentivos "
        "tributarios a la I+D privada, leyes de transferencia y desafíos tecnológicos."
    )
    + "\n"
    + en_la_practica(
        "Los casos regionales se concentran en cinco países: Chile en cinco palancas, "
        "Argentina en cuatro, Brasil en dos, Costa Rica en dos y Uruguay en una. Las "
        "cuatro sin caso regional citan Singapur, Corea, Israel y DARPA."
    )
    + "\n"
    + conclusion(
        "Qué queda del lado universitario:",
        "El Perú no aparece como caso regional en ninguna de las quince palancas "
        "públicas ni en las ocho universitarias. De estas últimas, dos ya tienen caso "
        "en la región y son las que una dirección de innovación puede montar sin "
        "cambio normativo: la unidad de aceleración e incubación, con la Universidad "
        "Nacional del Litoral, y la empresa de transferencia, con el Tecnológico de "
        "Monterrey.",
    )
    + "\n"
    + evitar(
        "Citar el informe como si el Perú figurara entre sus casos. El país aparece "
        "en el mapa de empresas, con cinco, y no aparece en la tabla de palancas: "
        "confundir las dos cosas convierte una ausencia documentada en un respaldo."
    )
    + "\n"
    + fuente_pie(F_BID)
)


# ==========================================================================
# HERRAMIENTAS 05 A 08
# ========================================================================

HERRAMIENTAS_05 = bloque_herramientas(
    ref="01", total="04",
    titulo="Modelos locales para trabajar sin divulgar el resultado",
    para_que=(
        "Subir un resultado sin expediente presentado a un servicio ajeno no es "
        "divulgación pública y no destruye la novedad por sí solo, pero sí compromete "
        "lo que se firmó con la empresa asociada. Estas tres lo mantienen dentro."
    ),
    herramientas=[
        ("Ollama", "proyecto libre", [
            "Descarga y ejecuta el modelo en tu propia máquina",
            "Nada de lo que escribes sale del equipo",
            "Se maneja desde la terminal, sin cuenta ni suscripción",
        ], "ollama.com"),
        ("LM Studio", "aplicación de escritorio", [
            "La misma idea con ventana y catálogo de modelos",
            "Funciona sin conexión una vez descargado el modelo",
            "Deja probar varios modelos sobre el mismo texto",
        ], "lmstudio.ai"),
        ("Modo sin retención", "en los asistentes de siempre", [
            "Algunos planes permiten desactivar el uso de tus datos",
            "Se comprueba en la configuración de la cuenta y en las condiciones",
            "Es la salida cuando el modelo local no alcanza para la tarea",
        ]),
    ],
    como_elegir=[
        ("Dónde corre", "Si el texto sale de tu equipo o se queda en él."),
        ("Qué se guarda", "Cuánto tiempo y para qué, según las condiciones del servicio."),
        ("Quién responde", "Qué dice el convenio que se firmó con la empresa asociada."),
    ],
)

HERRAMIENTAS_06 = bloque_herramientas(
    ref="02", total="04",
    titulo="Buscadores de patentes y su cobertura",
    para_que=(
        "El estado de la técnica decide si hay novedad y la novedad decide si hay "
        "patente. La búsqueda se hace antes de redactar el artículo, porque después "
        "de publicar ya no queda nada que proteger."
    ),
    herramientas=[
        ("Espacenet", "Oficina Europea de Patentes", [
            "Documentos de patente de todo el mundo en una sola búsqueda",
            "Filtra por clasificación internacional, no solo por palabras",
            "Muestra la familia: en qué países se pidió lo mismo",
        ], "worldwide.espacenet.com"),
        ("Patentscope", "OMPI", [
            "Incluye las solicitudes internacionales PCT desde que se publican",
            "Busca dentro del texto completo y en varios idiomas",
            "Traduce los resúmenes de forma automática",
        ], "patentscope.wipo.int"),
        ("Google Patents", "Google", [
            "Se busca en lenguaje corriente, como en la web",
            "Enlaza también la literatura que no es de patente",
            "Descarga el documento completo en PDF",
        ], "patents.google.com"),
    ],
    como_elegir=[
        ("Cobertura", "Qué oficinas nacionales incluye, y si está la peruana."),
        ("Familia", "Si dice en qué otros países se pidió la misma invención."),
        ("Salida", "Si la lista se exporta para adjuntarla al expediente."),
    ],
)

HERRAMIENTAS_07 = bloque_herramientas(
    ref="03", total="04",
    titulo="Repositorios con DOI, fecha y dirección estable",
    para_que=(
        "Con el expediente ya presentado toca publicar. Un repositorio con DOI deja "
        "constancia de autoría y fecha, y da la dirección estable que el convenio de "
        "transferencia puede citar sin que el enlace se rompa."
    ),
    herramientas=[
        ("Zenodo", "CERN", [
            "Da DOI a cualquier depósito, también a datos y a código",
            "Permite embargo: depositar ahora y abrir en una fecha",
            "Versiona sin invalidar el DOI de la versión anterior",
        ], "zenodo.org"),
        ("figshare", "Digital Science", [
            "DOI con previsualización de figuras y tablas",
            "Lo usan revistas para alojar el material suplementario",
            "Recuento público de descargas y de citas",
        ], "figshare.com"),
        ("OSF", "Center for Open Science", [
            "Registra el plan antes de ejecutarlo y lo sella con fecha",
            "Enlaza datos, código y manuscrito en un mismo proyecto",
            "Deja partes privadas y partes abiertas en el mismo depósito",
        ], "osf.io"),
    ],
    como_elegir=[
        ("DOI", "Que lo dé de verdad, y no un enlace que puede cambiar."),
        ("Embargo", "Si permite depositar hoy y abrir en la fecha que se decida."),
        ("Permanencia", "Quién garantiza que siga ahí dentro de diez años."),
    ],
)

HERRAMIENTAS_08 = bloque_herramientas(
    ref="04", total="04",
    titulo="Trámites en línea del expediente de propiedad industrial",
    para_que=(
        "Entre saber que hay algo que proteger y tener la solicitud presentada median "
        "pasos concretos. Los tres se hacen en línea y cada uno tiene su propio reloj."
    ),
    herramientas=[
        ("Búsqueda tecnológica", "INDECOPI", [
            "Servicio previo a la solicitud, para ver si ya existe",
            "Lo atiende la dirección de invenciones y devuelve informe",
            "Se pide antes de redactar la memoria descriptiva",
        ], "indecopi.gob.pe"),
        ("Gaceta Electrónica", "INDECOPI", [
            "Publica las solicitudes presentadas en el país",
            "Deja ver qué se está pidiendo en tu campo y quién lo pide",
            "Es donde corre el plazo para oponerse a una solicitud ajena",
        ], "indecopi.gob.pe"),
        ("ePCT", "OMPI", [
            "Gestiona en línea la solicitud internacional y sus plazos",
            "Avisa de cada vencimiento del procedimiento",
            "Da acceso al expediente desde cualquier oficina",
        ], "pct.wipo.int"),
    ],
    como_elegir=[
        ("Antes", "Qué hay que consultar antes de escribir una sola línea."),
        ("Plazo", "Qué reloj empieza a correr el día que se presenta."),
        ("Territorio", "Dónde vale el derecho que se está pidiendo, y dónde no."),
    ],
)



# ==========================================================================
# CIERRE
# ==========================================================================

RESUMEN = envolver(
    cabecera("Cierre", "Cinco puntos establecidos sobre explotación del resultado, titularidad y transferencia tecnológica", "i-check")
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}Queda establecido</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Licencia, <i>spin-off</i> y <i>startup</i> fijan cada una un titular, un riesgo y un capital distintos.</li>
\t\t\t\t\t\t\t<li>El inventor conserva la mención; el titular decide, licencia y cobra.</li>
\t\t\t\t\t\t\t<li>Cualquier divulgación anterior a la solicitud destruye la novedad, y esa pérdida no se repara.</li>
\t\t\t\t\t\t\t<li>La cartera de patentes es la vía de mayor tamaño de efecto sobre la creación de <i>spin-offs</i>, con f² de 0,724.</li>
\t\t\t\t\t\t\t<li>El acuerdo de propiedad intelectual se firma en la tercera fase, con la confianza por reputación ya construida.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-arrow-right")}Lo que se lleva a la sesión 3</h3>
\t\t\t\t\t\t<p>La vía de salida elegida, el titular escrito y la\n						protección solicitada antes de publicar. Esa figura jurídica busca\n						ahora <b>dinero</b>: qué instrumento admite a cada una y qué exige a
\t\t\t\t\t\tcambio.</p>
\t\t\t\t\t\t<p>La limitación que arrastramos: la vía de salida está elegida y el
\t\t\t\t\t\ttitular escrito, y todavía no está decidido <b>con qué capital</b> se
\t\t\t\t\t\tfinancia el primer tramo ni quién lo aporta.</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)


def _grupo_glosario(rotulo, entradas, variante=""):
    """Un bloque del glosario por cada tema de la sesión.

    Agrupar no es adorno: el glosario se consulta buscando un término que se
    oyó en un momento concreto de las tres horas, y el bloque temático es la
    única pista que el lector conserva de ese momento.
    """
    v = f" gloss-group--{variante}" if variante else ""
    return (f'\t\t\t\t\t<section class="gloss-group{v}">\n'
            f'\t\t\t\t\t\t<h2 class="gloss-group__title">{rotulo}</h2>\n'
            + "\n".join(entradas)
            + "\n\t\t\t\t\t</section>")


GLOSARIO = envolver(
    cabecera("Cierre", "Doce términos de explotación y transferencia", "i-book")
    + "\n"
    + '\t\t\t\t<div class="glossary glossary--grouped" data-animate="fade-up">\n'
    + _grupo_glosario("Tema 01 · Explotación del resultado y titularidad", [
        termino("Licencia de explotación", "licence",
                "Autoriza el uso por un plazo y un territorio sin mover la titularidad. El ingreso llega como regalía y el riesgo lo asume el receptor."),
        termino("Cesión", "assignment",
                "Transfiere la titularidad y no se recupera. Quien cede deja de poder licenciar el resultado, ejercerlo ante un tercero o negociarlo otra vez."),
        termino("Titular", "right holder",
                "El nombre a cuyo favor se concede el derecho. Es quien firma la licencia y cobra, y se decide antes de presentar la solicitud."),
        termino("<i>Spin-off</i>", "university spin-off",
                "Empresa creada para explotar un resultado de la universidad. Obliga a acordar qué aporta la institución y qué participación recibe."),
        termino("<i>Startup</i>", "startup",
                "Empresa nueva que busca un modelo repetible y escalable. Si el resultado no pertenece a la universidad se constituye sin ella y sin licencia."),
        termino("PCT", "patent cooperation treaty",
                "Una sola solicitud reserva la fecha de prioridad y abre treinta meses para decidir en qué países se entra en fase nacional."),
    ])
    + "\n"
    + _grupo_glosario("Tema 02 · Transferencia y creación de <i>spin-offs</i>", [
        termino("Transferencia tecnológica", "technology transfer",
                "El paso del resultado a quien lo va a usar. Ocurre cuando el convenio fija qué se entrega, quién lo explota y con qué indicador se mide."),
        termino("Oficina de transferencia", "technology transfer office",
                "Elige entre licencia y <i>spin-off</i> y negocia el contrato. Sin ensayo documentado ni descripción técnica no tiene qué proteger."),
        termino("Divulgación de invención", "invention disclosure",
                "El aviso interno que declara el resultado y abre el expediente. De 27 al año por universidad salen 5,6 <i>spin-offs</i>."),
        termino("Tamaño de efecto f²", "effect size",
                "Mide cuánto pesa cada trayectoria del modelo. El de la patente sobre la <i>spin-off</i> es 0,724, el mayor de las cinco medidas."),
        termino("Confianza por integridad", "integrity-based trust",
                "Se apoya en el comportamiento observado durante el trabajo conjunto. Llega en la tercera fase, que es cuando el acuerdo se firma."),
        termino("IGO", "intergovernmental organization",
                "Variante de licencia Creative Commons de los organismos intergubernamentales. Permite reproducir su tabla o su cifra citando la edición."),
    ], "b")
    + "\n\t\t\t\t</div>"
    + "\n"
    + fuente_pie(F_INDECOPI, F_OMPI_PCT, F_ODEI, F_ODWYER)
)


REFERENCIAS = envolver(
    cabecera("Cierre", "Fuentes citadas y vía de acceso a cada una", "i-quote")
    + "\n"
    + tabla(
        ["Fuente", "Sirve a", "Acceso"],
        [
            ["O’Dwyer, Filieri y O’Malley (2022). <i>The Journal of Technology Transfer</i>",
             "Barreras y facilitadores por fase de un consorcio universidad-empresa",
             '<a href="https://doi.org/10.1007/s10961-022-09932-2">doi.org/10.1007/s10961-022-09932-2</a> · CC BY 4.0'],
            ["Odei y Novák (2022) y Hunady, Orviska y Pisar (2019)",
             "Determinantes medidos de la creación de <i>spin-offs</i>",
             '<a href="https://doi.org/10.1080/1331677X.2022.2086148">Odei</a> · <a href="https://doi.org/10.2478/bsrj-2019-0010">Hunady</a> · CC BY 4.0 y CC BY-NC-ND 3.0'],
            ["Samo y Huda (2019). <i>Journal of Global Entrepreneurship Research</i> 9",
             "Intención emprendedora académica y peso de cada hélice",
             '<a href="https://doi.org/10.1186/s40497-018-0121-7">doi.org/10.1186/s40497-018-0121-7</a> · CC BY 4.0'],
            ["Nguyen, Kowalski y Dzienis (2024). <i>Sustainability</i> 16(19):8714",
             "Proceso emprendedor, rondas y rasgos del <i>deep tech</i>",
             '<a href="https://doi.org/10.3390/su16198714">doi.org/10.3390/su16198714</a> · CC BY 4.0'],
            ["Peña y Jenik (2023). <i>Deep Tech: The New Wave</i>, BID",
             "Mapa regional, obstáculos de salida y palancas públicas",
             '<a href="https://publications.iadb.org/publications/english/document/Deep-Tech-The-New-Wave.pdf">publications.iadb.org</a> · CC BY-NC-ND 3.0 IGO'],
            ["Ley 31250 (2021), INDECOPI y OMPI · <i>Guía del solicitante PCT</i>",
             "Titularidad, vías de protección y plazos del PCT",
             '<a href="https://busquedas.elperuano.pe/dispositivo/NL/1968664-1">Ley 31250</a> · <a href="https://www.indecopi.gob.pe/">INDECOPI</a> · <a href="https://www.wipo.int/pct/es/">OMPI</a>'],
            ["CONCYTEC (2024) <i>POLCTI al 2030</i>, DS 093-2025-PCM y OMPI (2025) <i>GII</i>",
             "Cifras del punto de partida peruano y su referente",
             '<a href="https://www.gob.pe/institucion/pcm/normas-legales/6967622-093-2025-pcm">gob.pe</a> · <a href="https://www.wipo.int/en/web/global-innovation-index">wipo.int</a> · CC BY 4.0 IGO'],
        ],
        titulo="Fuentes citadas en la sesión y su vía de acceso"
    )
) + "\n" + colofon_flotante()


# ==========================================================================
# MONTAJE
# ==========================================================================

def L(slug, titulo, nav, icono, contenido, clases="slide", scripts=""):
    return {"slug": slug, "titulo": f"{SESION} · {titulo}", "nav": nav,
            "icono": icono, "clases": clases, "contenido": contenido,
            "scripts": scripts}


LAMINAS = [
    # ── APERTURA ──
    L("portada", "Portada", "Portada", "i-rocket", PORTADA, "slide slide--start"),
    L("agenda", "Explotación del resultado, transferencia tecnológica y cuatro paradas de herramientas", "Agenda", "i-flow", AGENDA),

    # ── 01 · FIGURAS DE SALIDA ──
    L("tema-01", TEMA_A, "Tema 01", "i-layers", SECCION_A),

    # de la investigación a la empresa
    L("conversion-investigacion", "Cadena de conversión de investigación a empresa en América Latina, 2023", "De la investigación a la empresa", "i-chart", CONVERSION),

    # las tres vías de salida
    L("tres-vias-de-salida", "Vías de salida de un resultado y su requisito propio", "Las tres vías", "i-layers", TRES_VIAS),
    L("licencia-o-spinoff", "Licencia y spin-off: titular, riesgo y retorno de cada vía", "Licencia o spin-off", "i-scale", LICENCIA_SPINOFF),
    L("startup-independiente", "Constitución de una startup con resultado ajeno a la universidad", "La startup", "i-rocket", STARTUP_INDEPENDIENTE),
    L("obstaculos-de-salida", "Nueve obstáculos al acceso a inversión institucional en deep tech, 2023", "Obstáculos", "i-alert", OBSTACULOS_SALIDA),

    # titular y explotador
    L("inventor-y-titular", "Titular, inventor y explotador de una invención en el régimen de propiedad industrial", "Inventor y titular", "i-patent", INVENTOR_Y_TITULAR),
    L("donde-se-fija-la-titularidad", "Titularidad según el origen del resultado: reglamento, convenio y acuerdo de cesión", "Dónde se fija", "i-file", DONDE_SE_FIJA),
    L("titularidad-simulador", "Documentos de titularidad exigidos según las cuatro condiciones de origen del resultado", "Titularidad · simulación", "i-sliders", TITULARIDAD_SIM, "slide", TITULARIDAD_JS),
    L("herramientas-01", "Herramientas 01 · Trabajar sin divulgar el resultado", "Herramientas 01", "i-sliders", HERRAMIENTAS_05),
    L("ceder-o-licenciar", "Cesión y licencia: efecto sobre la titularidad", "Ceder o licenciar", "i-agreement", CEDER_O_LICENCIAR),

    # la patente
    L("patente-como-requisito", "Orden entre solicitud de patente y divulgación pública del resultado", "El reloj de la patente", "i-calendar", PATENTE_REQUISITO),
    L("tres-vias-de-proteccion", "Patente, modelo de utilidad y secreto empresarial: exigencia y vigencia de cada vía", "Qué protege cada vía", "i-patent", TRES_PROTECCIONES),
    L("patente-como-activo", "Familias de patentes, solicitudes y jurisdicciones de la cartera de Establishment Labs, 2023", "La patente como activo", "i-fund", PATENTE_ACTIVO),
    L("herramientas-02", "Herramientas 02 · Buscadores de patentes", "Herramientas 02", "i-sliders", HERRAMIENTAS_06),

    # deep tech
    L("deep-tech", "Deep tech: definición, rasgos distintivos y tasa de fracaso, revisión de 2024", "Deep tech", "i-bolt", DEEP_TECH),
    L("proceso-deep-tech", "Fases y actividades del proceso emprendedor en deep tech, seis casos, 2024", "El proceso", "i-flow", PROCESO_DEEP_TECH),
    L("rondas-deep-tech", "Montos de nueve rondas de financiamiento en deep tech, 2015-2022", "Las rondas", "i-fund", RONDAS_DEEP_TECH),

    # qué mueve a un investigador
    L("intencion-emprendedora", "Apoyo de universidad, Estado y empresa sobre la intención emprendedora académica, 2019", "Las tres hélices", "i-network", INTENCION_HELICES),
    L("quien-emprende", "Perfil ocupacional y de sexo de los 310 investigadores encuestados, 2019", "Quién emprende", "i-users", QUIEN_EMPRENDE),
    L("lo-que-no-explica", "Alcance explicativo del modelo de las tres hélices y motivos declarados para fundar", "El hueco del modelo", "i-search", LO_QUE_NO_EXPLICA),

    # ── 01 · TALLERES ──

    # ── 02 · TRANSFERENCIA ──
    L("tema-02", TEMA_B, "Tema 02", "i-network", SECCION_B),

    # ── 02 · LA OFICINA DE TRANSFERENCIA ──
    L("ott-ruta", "Recorrido del resultado en la oficina de transferencia", "La ruta", "i-network", OTT_RUTA),
    L("ott-factores", "Factores organizativos de una oficina de transferencia", "Cinco factores", "i-rubric", OTT_FACTORES),
    L("ott-limites", "Reparto de tareas entre el grupo y la oficina de transferencia", "Qué no resuelve", "i-users", OTT_LIMITES),
    L("herramientas-03", "Herramientas 03 · Repositorios con DOI y fecha", "Herramientas 03", "i-sliders", HERRAMIENTAS_07),

    # ── 02 · DETERMINANTES MEDIDOS ──
    L("spinoff-embudo", "Creación de spin-offs por universidad y su dispersión, Reino Unido, curso 2017/18", "El embudo", "i-flow", SPINOFF_EMBUDO),
    L("spinoff-coeficientes", "Cinco determinantes de la creación de spin-offs y su tamaño de efecto, 164 universidades", "Coeficientes", "i-chart", SPINOFF_COEFICIENTES),
    L("spinoff-no-lineal", "Especialización e intensidad doctoral frente a la creación de spin-offs, Europa, 2011-2014", "Relación en U", "i-scale", SPINOFF_NO_LINEAL),
    L("determinantes-simulador", "Perfil institucional según los seis determinantes medidos de la creación de spin-offs", "Determinantes", "i-sliders", DETERMINANTES_SIM, "slide", DETERMINANTES_JS),

    # ── 02 · BARRERAS DE LA COLABORACIÓN ──
    L("barreras-fases", "Cinco barreras de la colaboración universidad-empresa a lo largo de siete años", "Barreras", "i-alert", BARRERAS_FASES_LAMINA),
    L("facilitadores-fases", "Facilitadores por fase en el consorcio farmacéutico irlandés", "Facilitadores", "i-network", FACILITADORES_FASES_LAMINA),
    L("confianza-acuerdo", "Tipos de confianza por fase del consorcio farmacéutico irlandés", "Confianza", "i-agreement", CONFIANZA_ACUERDO),
    L("financiamiento-reparto", "Reparto del fondo fundacional entre los cinco grupos académicos del consorcio irlandés", "Reparto igual", "i-fund", FINANCIAMIENTO_REPARTO),

    # ── 02 · EL DEEP TECH EN AMÉRICA LATINA ──
    L("deeptech-region", "Distribución y valor agregado del deep tech por país en América Latina, 2023", "La región", "i-globe", DEEPTECH_REGION),
    L("deeptech-sectores", "Biotecnología y los otros doce sectores del deep tech en América Latina, 2023", "Sectores", "i-layers", DEEPTECH_SECTORES),
    L("deeptech-talento", "Personal de I+D y capital de riesgo por investigador, América Latina, 2023", "Talento", "i-users", DEEPTECH_TALENTO),

    # ── 02 · DE DÓNDE PARTE EL PERÚ ──
    L("peru-partida", "Indicadores de partida del Perú frente a su referente en tres brechas, 2018-2023", "Punto de partida", "i-chart", PERU_PARTIDA),
    L("peru-instrumentos", "Cinco instrumentos peruanos de la transferencia", "Instrumentos", "i-building", PERU_INSTRUMENTOS),
    L("herramientas-04", "Herramientas 04 · Trámites del expediente peruano", "Herramientas 04", "i-sliders", HERRAMIENTAS_08),
    L("peru-matriz", "Protección registrada y socio receptor: cuatro situaciones de un resultado peruano", "La matriz", "i-scale", PERU_MATRIZ),
    L("peru-palancas", "Palancas públicas y universitarias de deep tech y sus casos regionales, 2023", "Palancas", "i-target", PERU_PALANCAS),

    # ── CIERRE ──
    L("queda-establecido", "Cinco puntos establecidos sobre explotación del resultado, titularidad y transferencia tecnológica", "Resumen", "i-check", RESUMEN),
    L("glosario", "Doce términos de explotación y transferencia", "Glosario", "i-book", GLOSARIO),
    L("referencias", "Fuentes citadas y vía de acceso a cada una", "Referencias", "i-quote", REFERENCIAS),
]

if __name__ == "__main__":
    generar_desde({"clase": "clase-02", "sesion": SESION,
                   "laminas": renumerar(LAMINAS)})
