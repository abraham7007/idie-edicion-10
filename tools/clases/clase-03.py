#!/usr/bin/env python3
"""Sesión 3 · Mapa de financiamiento e inversión.

Guion de la sesión. Contiene SOLO lo que distingue a cada lámina: la cabecera
repetida, la cadena de anterior/siguiente y el total los pone el generador
(METODOLOGIA.md §9). Se edita este archivo, nunca el HTML resultante.

Todas las cifras están verificadas contra la fuente que se cita al pie de la
lámina, y son las mismas que usan las figuras de `tools/figures/render.py`
(METODOLOGIA.md §1 y §3.2).

Las cifras peruanas de esta sesión son LAS MISMAS que verifican las sesiones 1
y 2, con el mismo pie. Buscar cifras nuevas para repetir el argumento dejaría
dos valores distintos del mismo indicador en el mismo mazo.

Uso:  python3 tools/clases/clase-03.py
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
    en_la_practica, envolver_visual as envolver, evitar, fig_desnuda, figura,
    fichas, ficha_fondo, fuente_pie, reiniciar_alternancia, seccion, renumerar, tabla,
    bloque_herramientas,
)
from generar_clase import generar_desde  # noqa: E402

reiniciar_alternancia()

SESION = "Sesión 3 · Mapa de financiamiento e inversión"

# Los dos temas. Frases nominales que nombran la materia como la nombraría un
# temario oficial: es la prueba de §17.19, que va más allá de §6 porque el
# nombre de tema aparece en la portada, la agenda, la portadilla y el índice del
# curso, y en tres de esos cuatro sitios se lee sin contexto.
TEMA_A = "Fondos públicos: a cuál se postula, qué financia y qué exige"
TEMA_B = "Inversión privada en etapa temprana y sus criterios de decisión"


# --------------------------------------------------------------------------
# FUENTES
#
# Copiadas de src/paper/fuentes.json, clave `clase-03`, NUNCA tecleadas de
# memoria: tres pies de la sesión 1 atribuían mal el trabajo por escribirlos a
# mano (METODOLOGIA.md §17.9). Los seis trabajos revisados por pares están
# descargados en src/paper/clase-03/.
# --------------------------------------------------------------------------

F_AVNIMELECH = ("Avnimelech et al. (2024), <i>Strategic Management Journal</i>, 1 350 "
                "<i>startups</i> aceleradas en Israel · CC BY 4.0")
F_CANFIELD = ("Canfield Rivera (2021), <i>Multidisciplinary Business Review</i> "
              "· CC BY-NC-ND 4.0")
# Crossref devuelve para este DOI la política genérica del editor, no la
# licencia del artículo: el propio PDF declara CC BY 4.0 en su página 66.
F_DHIMAN = ("Dhiman y Arora (2024), <i>LBS Journal of Management &amp; Research</i> "
            "22(1):66-92 · CC BY 4.0")
F_LESLIE = ("Leslie et al. (2025), <i>Venture Capital in the Caribbean</i>, BID "
            "· CC BY 3.0 IGO")
F_GOFFE = ("Goffe et al. (2021), <i>Best Practices in the Operation of Partial "
           "Credit Guarantee Schemes</i>, Banco Mundial · CC BY 3.0 IGO")
F_SKALICKA = ("Skalicka et al. (2022), <i>Economic Research-Ekonomska "
              "Istraživanja</i> 36(1):25-50, 31 inversores checos · CC BY 4.0")

# Versiones cortas para los pies que reúnen muchas citas —el glosario y el
# cierre—, donde el alcance ya lo declara la lámina que usa cada dato.
F_AVNIMELECH_C = "Avnimelech et al. (2024), <i>Strategic Management Journal</i> · CC BY 4.0"
F_SKALICKA_C = ("Skalicka et al. (2022), <i>Economic Research</i> 36(1):25-50 "
                "· CC BY 4.0")

# Reutilizadas de las sesiones 1 y 2, con el pie idéntico.
F_POLCTI = ("CONCYTEC (2024), <i>Política Nacional de CTI al 2030</i>, Tabla 13 "
            "· documento público")
F_POLCTI_DIAG = ("CONCYTEC (2024), <i>Política Nacional de CTI al 2030</i>, "
                 "diagnóstico · documento público")
F_ROGERS = "Estudio de línea base del gasto público en CTI (Rogers, 2020)"
F_LEY_30309 = ("Base de datos institucional del CONCYTEC · Ley 30309, "
               "2016-2022")
F_DS = ("DS 093-2025-PCM, <i>El Peruano</i>, 15 de julio de 2025 · norma de "
        "dominio público")
F_INEI = "INEI · Encuesta Nacional de Innovación en la Industria Manufacturera"
F_BID = ("Peña y Jenik (2023), <i>Deep Tech: The New Wave</i>, BID "
         "· doi 10.18235/0004947")

# Portales sin PDF estable: las bases cambian en cada edición, así que la
# lámina cita el portal y el mes de consulta, nunca un importe de convocatoria.
F_PROINNOVATE = ("ProInnóvate · convocatorias en proinnovate.gob.pe, agosto de 2026")
F_PROCIENCIA = ("PROCIENCIA · convocatorias en prociencia.gob.pe, agosto de 2026")
F_RADIO = ("Fondos y Convocatorias (2025), <i>Radiografía del financiamiento "
           "social</i> · base de 1 019 convocatorias con cierre en 2025")
F_MAPEO = ("Informe de mapeo sobre fondos concursables, programa Ágora Perú "
           "(FOAL, 2024) · documento público")
F_APCI = ("APCI (2021), <i>Situación y Tendencias de la Cooperación Técnica "
          "Internacional en el Perú</i> · documento público")


# ==========================================================================
# PORTADA
#
# El objeto central de toda portada es el mapa del ecosistema (§0). Aquí se
# ilumina el tramo del dinero: del Estado a los fondos, de los fondos a la
# academia, y de la empresa al mercado, que es de donde vuelve el capital
# privado.
# ==========================================================================

PORTADA = f"""			<div class="slide__content stagger">
				<div class="cover">
					<div class="cover__main">
						<span class="badge" data-animate="fade-up">{ico("i-fund")}Sesión 3</span>

						<h1 class="slide__title" data-animate="fade-up">Mapa de financiamiento e inversión</h1>

						<div class="cover__topics" data-animate="fade-up">
							<span class="topic"><span class="topic__n">01</span>{TEMA_A}</span>
							<span class="topic topic--b"><span class="topic__n">02</span>{TEMA_B}</span>
						</div>

{colofon()}
					</div>

{mapa_ecosistema(
    activos=("estado", "fondos", "academia", "empresa"),
    aristas=("estado-fondos", "fondos-academia", "academia-empresa"),
)}
				</div>
			</div>"""


# ==========================================================================
# AGENDA
# ==========================================================================

AGENDA = envolver(
    cabecera("Agenda", "Financiamiento público, inversión privada y cuatro paradas de herramientas", "i-flow")
    + "\n"
    + """\t\t\t\t<div class="agenda" data-animate="fade-up">
\t\t\t\t\t<div class="agenda__block">
\t\t\t\t\t\t<span class="agenda__n">Tema 01</span>
\t\t\t\t\t\t<h3>Instrumentos públicos y contrapartida</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Once fondos del Estado, uno por lámina, con su ficha</li>
\t\t\t\t\t\t\t<li>Qué financia cada uno y a quién admite</li>
\t\t\t\t\t\t\t<li>La contrapartida: efectivo, especie y quién la aporta</li>
\t\t\t\t\t\t\t<li>Cuándo entra el dinero y quién financia entretanto</li>
\t\t\t\t\t\t\t<li>Qué ventanilla admite el proyecto</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 01</b>Portales donde se ve qué convocatoria está abierta</li>
\t\t\t\t\t\t\t<li><b>Herramientas 02</b>Buscadores de convocatorias no oficiales</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--b">
\t\t\t\t\t\t<span class="agenda__n">Tema 02</span>
\t\t\t\t\t\t<h3>Inversión privada y sus criterios</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Incubadora y aceleradora: qué añade cada una</li>
\t\t\t\t\t\t\t<li>Cuánto del desempeño es atribuible a la aceleradora</li>
\t\t\t\t\t\t\t<li>Los criterios con que decide un inversor ángel</li>
\t\t\t\t\t\t\t<li>Capital de riesgo en la región y sus magnitudes</li>
\t\t\t\t\t\t\t<li>Garantías parciales de crédito</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 03</b>Bases de datos de inversión y sus vacíos</li>
\t\t\t\t\t\t\t<li><b>Herramientas 04</b>Fondos de cooperación fuera del presupuesto nacional</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="agenda__map" data-animate="fade-up">
\t\t\t\t\t\t<span class="agenda__map-label">Las seis sesiones</span>
\t\t\t\t\t\t<ul class="agenda__steps">
\t\t\t\t\t\t\t<li><b>01</b>Fundamentos y ecosistema I+D+i+e</li>
\t\t\t\t\t\t\t<li><b>02</b><i>Startups</i>, <i>spin-offs</i> y transferencia</li>
\t\t\t\t\t\t\t<li class="is-on"><b>03</b>Mapa de financiamiento e inversión</li>
\t\t\t\t\t\t\t<li><b>04</b>Formulación de proyectos</li>
\t\t\t\t\t\t\t<li><b>05</b>Presupuesto, ejecución y propiedad intelectual</li>
\t\t\t\t\t\t\t<li><b>06</b><i>Pitch Elevator</i> y tendencias mundiales en I+D+i+e</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)


# ==========================================================================
# PORTADILLAS DE TEMA
# ==========================================================================

SECCION_A = seccion(
    "01",
    TEMA_A,
    "El Estado peruano opera ciento sesenta y cuatro instrumentos de "
    "financiamiento de ciencia, tecnología e innovación. Cada uno admite un "
    "tipo de entidad, cubre un tramo de madurez y exige una contrapartida "
    "distinta.",
)

SECCION_B = seccion(
    "02",
    TEMA_B,
    "Incubadoras, aceleradoras, inversores ángeles y fondos de capital de "
    "riesgo aportan capital con criterios propios, medidos en la literatura "
    "sobre etapa temprana.",
)


# ==========================================================================
# 01 · CONTENIDO DEL TEMA A
# ==========================================================================

PRESUPUESTO_CTI = envolver(
    cabecera("01 · Presupuesto público de CTI",
             "Bloques de concentración del presupuesto público de CTI, 2012-2018",
             "i-fund")
    + "\n"
    + definicion(
        "Instrumento de financiamiento de CTI",
        "Política Nacional de CTI 2024",
        "Mecanismo con presupuesto propio con el que un organismo del Estado "
        "financia o presta un servicio de ciencia, tecnología e innovación. "
        "Toma <b>cinco formas</b>: beca, concurso de investigación, subvención "
        "a la innovación empresarial, servicio tecnológico y beneficio "
        "tributario.",
        "i-fund",
    )
    + "\n"
    + figura(
        "s3-reparto-presupuesto",
        "Reparto del presupuesto público de CTI en cuatro bloques por tamaño, 2012-2018",
        "<b>El mayor gasto público en ciencia y tecnología del país es un "
        "programa de becas, y se lleva 43 de cada 100 soles.</b>",
    )
    + "\n"
    + dato_clave(
        "Los <b>119 instrumentos menores</b> comparten el <b>10 %</b> del "
        "presupuesto de CTI del periodo 2012-2018. Los <b>45 mayores</b> "
        "acumulan el <b>90 %</b>."
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_ROGERS)
)


BLOQUES_DE_PRESUPUESTO = envolver(
    cabecera("01 · Presupuesto público de CTI",
             "Presupuesto medio por instrumento de CTI según su bloque, 2012-2018",
             "i-chart")
    + "\n"
    + figura(
        "s3-bloques-presupuesto",
        "Participación y presupuesto medio por instrumento en los cuatro bloques, 2012-2018",
        "<b>Entre el instrumento mayor y el instrumento medio del último bloque "
        "hay un factor de quinientos.</b>",
    )
    + "\n"
    + criterio(
        "El bloque decide la estrategia de búsqueda. Un instrumento del último "
        "bloque maneja el 0,08 % del presupuesto de CTI: financia una actividad "
        "acotada y no un proyecto completo."
    )
    + "\n"
    + en_la_practica(
        "Un proyecto de dieciocho meses con equipamiento se formula contra uno "
        "de los 45 mayores, o se parte en etapas con un financiador distinto "
        "para cada una."
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_ROGERS)
)


INSTRUMENTOS_POR_SECTOR = envolver(
    cabecera("01 · Presupuesto público de CTI",
             "Agrupamiento de los 164 instrumentos de CTI por sector del Estado, 2012-2018",
             "i-building")
    + "\n"
    + figura(
        "s3-arbol-sector",
        "Los 164 instrumentos de CTI agrupados por sector responsable, 2012-2018",
        "<b>El rector del sistema no es su mayor operador: Producción opera "
        "setenta y uno, y CONCYTEC treinta y ocho.</b>",
    )
    + "\n"
    + criterio(
        "La búsqueda empieza por el sector cuya materia cubre el proyecto. "
        "Producción opera 71 instrumentos de los 164 y CONCYTEC opera 38, según "
        "la Tabla 14 de la Política Nacional de CTI."
    )
    + "\n"
    + evitar(
        "Dar por cerrada la búsqueda con dos portales. Cinco sectores del Estado "
        "operan otros 55 instrumentos, y cada sector convoca los suyos por su "
        "cuenta."
    )
    + "\n"
    + fuente_pie(F_POLCTI)
)


DESAGREGACION_INVENTARIO = envolver(
    cabecera("01 · Presupuesto público de CTI",
             "Nivel de desagregación del inventario público de instrumentos de CTI",
             "i-search")
    + "\n"
    + dato_clave(
        "El inventario cubre <b>164 instrumentos</b> de siete sectores del "
        "Estado, con el presupuesto promedio anual del periodo <b>2012-2018</b>. "
        "Es un promedio del periodo y no la cifra de un año."
    )
    + "\n"
    + aviso(
        "La fuente publica el recuento por sector y la curva de concentración "
        "del presupuesto. No publica el reparto de los 164 instrumentos por "
        "forma, ni el presupuesto de cada uno, ni el calendario de sus "
        "convocatorias."
    )
    + "\n"
    + criterio(
        "Lo que la fuente no desagrega se consulta en el portal del organismo "
        "que opera el instrumento, y se cita con el mes de consulta: las bases "
        "cambian en cada edición."
    )
    + "\n"
    + en_la_practica(
        "Un importe de convocatoria citado sin edición ni fecha de consulta "
        "caduca antes de que la propuesta llegue a presentarse."
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_ROGERS, F_PROINNOVATE, F_PROCIENCIA)
)


FONDO_PROCOMPITE = envolver(
    cabecera("01 · Fondos del Estado",
             "PROCOMPITE: cofinanciamiento de planes de negocio de cadenas productivas",
             "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Gobiernos regionales y locales · Ley 29337",
        financia=[
            "Equipamiento, maquinaria e infraestructura productiva de uso colectivo",
            "Insumos, material genético y capital de trabajo del plan de negocio",
            "Asistencia técnica y capacitación asociadas al mismo plan",
        ],
        quien=("Agentes económicos organizados: asociaciones, cooperativas y grupos de "
               "productores formalizados. No admite empresas individuales ni personas "
               "naturales sueltas."),
        datos=[
            ("Monto", "De S/ 80 000 a 350 000 según la categoría"),
            ("Modalidad", "No reembolsable, por concurso del gobierno regional o local"),
            ("Categorías", "A para grupos pequeños y B para propuestas de mayor monto"),
            ("Contrapartida", "Aporte del agente organizado, en efectivo o valorizado"),
            ("Cuándo abre", "Cada gobierno convoca por su cuenta y con su propio calendario"),
        ],
        sitio="gob.pe/38839-postular-a-las-convocatorias-para-fondos-concursables-de-procompite",
        nota=("Cada gobierno convoca por su cuenta: el calendario y el tope exacto se "
              "leen en sus propias bases."),
    )
    + "\n"
    + fuente_pie(F_POLCTI)
)

CINCO_FORMAS = envolver(
    cabecera("01 · Formas de instrumento",
             "Las cinco formas del instrumento de CTI peruano",
             "i-layers")
    + "\n"
    + tabla(
        ["Forma", "Qué financia", "Cuándo llega el dinero",
         "Qué exige del postulante"],
        [
            ["Beca",
             "Estudios de posgrado o estancias de un investigador",
             "Por armadas, mientras dura el programa",
             "Admisión acreditada en el programa de posgrado"],
            ["Concurso de investigación",
             "Un proyecto con pregunta abierta y resultado publicable",
             "Por tramos, contra informe técnico aprobado",
             "Entidad de investigación titular y equipo inscrito en el Registro Nacional de Investigadores"],
            ["Subvención a la innovación empresarial",
             "Desarrollo, validación o escalamiento de una solución",
             "Por tramos, contra hito verificado",
             "Contrapartida, con una parte de ella en efectivo"],
            ["Servicio tecnológico",
             "Un ensayo, una caracterización o una asistencia técnica",
             "No hay desembolso: el centro presta el servicio",
             "Pago del servicio y una muestra o un prototipo que ensayar"],
            ["Beneficio tributario",
             "Gasto ya ejecutado en I+D+i que el CONCYTEC califica",
             "Después del gasto, con la declaración del impuesto a la renta",
             "Ser contribuyente del impuesto a la renta"],
        ],
        titulo="Las cinco formas del instrumento de financiamiento de CTI, su desembolso y su requisito",
    )
    + "\n"
    + criterio(
        "La forma decide dos cosas antes que el monto: si el dinero llega antes o "
        "después del gasto, y si hace falta contrapartida."
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROCIENCIA, F_PROINNOVATE, F_LEY_30309)
)


ORGANISMO_Y_FORMA = envolver(
    cabecera("01 · Formas de instrumento",
             "Correspondencia entre organismo del SINACTI y forma de instrumento operada",
             "i-network")
    + "\n"
    + figura(
        "s3-matriz-organismo-forma",
        "Formas de instrumento de financiamiento de CTI que opera cada organismo del SINACTI",
        "<b>Dos de los seis organismos no mueven dinero: INDECOPI protege "
        "derechos y SUNEDU supervisa universidades.</b>",
    )
    + "\n"
    + criterio(
        "Cada forma tiene un operador único dentro del Sistema Nacional de "
        "Ciencia, Tecnología e Innovación. Localizada la forma que corresponde "
        "al proyecto, el organismo queda determinado y con él las bases que hay "
        "que leer."
    )
    + "\n"
    + evitar(
        "Dirigir a INDECOPI o a SUNEDU una solicitud de financiamiento. "
        "Ninguno de los dos opera instrumentos con presupuesto."
    )
    + "\n"
    + fuente_pie(F_DS, F_POLCTI)
)


PROCIENCIA_Y_PROINNOVATE = envolver(
    cabecera("01 · Formas de instrumento",
             "PROCIENCIA y ProInnóvate: materia financiada y evidencia de cierre",
             "i-scale")
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-book")}PROCIENCIA · concurso de investigación</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Financia un proyecto cuya pregunta sigue abierta.</li>
\t\t\t\t\t\t\t<li>El titular es una entidad de investigación registrada.</li>
\t\t\t\t\t\t\t<li>Se puntúa el nivel del investigador principal en el Registro Nacional de Investigadores.</li>
\t\t\t\t\t\t\t<li>Cierra con publicación, tesis o prueba de concepto documentada.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-rocket")}ProInnóvate · subvención a la innovación</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Financia una solución con destinatario ya identificado.</li>
\t\t\t\t\t\t\t<li>El titular es una empresa formal, sola o con entidad asociada.</li>
\t\t\t\t\t\t\t<li>El equipo se puntúa por su experiencia en el mercado de destino.</li>
\t\t\t\t\t\t\t<li>Cierra con prototipo validado, producto o venta acreditada.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + conclusion(
        "Cuál corresponde",
        "La pregunta abierta prevalece sobre el sector de destino. Un proyecto con "
        "hipótesis sin resolver corresponde a PROCIENCIA aunque su salida sea "
        "comercial, y uno con la solución ya definida corresponde a ProInnóvate "
        "aunque nazca en un laboratorio.",
    )
    + "\n"
    + en_la_practica(
        "El mismo material da los dos casos: caracterizar una fibra amazónica "
        "sigue siendo pregunta abierta; ensayar paneles con esa fibra en veinte "
        "viviendas ya tiene destinatario."
    )
    + "\n"
    + fuente_pie(F_PROCIENCIA, F_PROINNOVATE, F_POLCTI_DIAG)
)


CONTRAPARTIDA = envolver(
    cabecera("01 · La contrapartida",
             "Contrapartida en un instrumento de cofinanciamiento: efectivo y especie",
             "i-agreement")
    + "\n"
    + definicion(
        "Contrapartida (<i>counterpart contribution</i>)",
        "Bases de convocatoria de ProInnóvate y PROCIENCIA",
        "Parte del costo total del proyecto que no cubre el fondo público y que "
        "aporta quien postula, solo o con sus entidades asociadas. Se declara en "
        "el presupuesto de la propuesta y se rinde con comprobante, igual que el "
        "dinero subvencionado.",
        "i-agreement",
    )
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-budget")}Aporte en efectivo</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Dinero propio depositado en la cuenta del proyecto.</li>
\t\t\t\t\t\t\t<li>Se acredita con el estado de cuenta y el comprobante de cada gasto.</li>
\t\t\t\t\t\t\t<li>Cubre las partidas que el fondo excluye y los sobrecostos.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-building")}Aporte en especie</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Horas de personal propio, uso de equipamiento e instalaciones.</li>
\t\t\t\t\t\t\t<li>Se valoriza con la planilla o el tarifario, y se rinde igual.</li>
\t\t\t\t\t\t\t<li>No entra dinero en la cuenta del proyecto.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + conclusion(
        "Qué decide la mezcla",
        "El tipo de entidad que postula fija la proporción. A una empresa formal "
        "se le exige una parte en efectivo; una universidad cubre casi toda su "
        "contrapartida con horas de investigador y uso de laboratorio "
        "valorizados.",
    )
    + "\n"
    + fuente_pie(F_PROINNOVATE, F_PROCIENCIA)
)


ARITMETICA_CONTRAPARTIDA = envolver(
    cabecera("01 · La contrapartida",
             "Reparto del costo de un proyecto entre subvención y contrapartida",
             "i-budget")
    + "\n"
    + figura(
        "s3-area-contrapartida",
        "Subvención y contrapartida sobre el costo total, según el cofinanciamiento de las bases",
        "<b>La contrapartida crece más deprisa de lo que baja el "
        "cofinanciamiento: del 70 % al 50 %, el aporte se multiplica por más de "
        "dos.</b>",
    )
    + "\n"
    + dato_clave(
        "Con un cofinanciamiento del <b>70 %</b>, cada 1,00 de subvención exige "
        "<b>0,43</b> de contrapartida. El porcentaje de las bases se aplica al "
        "costo total del proyecto."
    )
    + "\n"
    + evitar(
        "Calcular la contrapartida sobre el monto solicitado. Aplicar a lo "
        "solicitado el porcentaje que corresponde al costo total deja el "
        "presupuesto corto desde la primera rendición."
    )
    + "\n"
    + fuente_pie(F_PROINNOVATE, F_PROCIENCIA)
)


QUIEN_APORTA = envolver(
    cabecera("01 · La contrapartida",
             "Partidas con las que cada tipo de entidad postulante aporta su contrapartida",
             "i-users")
    + "\n"
    + figura(
        "s3-matriz-entidad-aporte",
        "Partidas de contrapartida admitidas por tipo de entidad postulante",
        "<b>A la empresa formal se le pide efectivo; las demás figuras aportan "
        "trabajo e instalaciones valorizados.</b>",
    )
    + "\n"
    + criterio(
        "La figura del postulante decide qué partidas admite el fondo como "
        "aporte. Una persona sin empresa constituida no puede valorizar "
        "infraestructura propia, y esa partida sale de una entidad asociada."
    )
    + "\n"
    + en_la_practica(
        "Para el emprendedor sin empresa, la constitución suele ser condición "
        "para el desembolso y no para postular: la contrapartida se compromete "
        "antes de que exista el RUC."
    )
    + "\n"
    + fuente_pie(F_PROINNOVATE, F_PROCIENCIA, F_POLCTI_DIAG)
)


ENTIDAD_ASOCIADA = envolver(
    cabecera("01 · La contrapartida",
             "Entidad asociada: aporte que compromete y documento que lo acredita",
             "i-agreement")
    + "\n"
    + tabla(
        ["Quién aporta", "Forma del aporte", "Documento que lo acredita",
         "Qué lo invalida"],
        [
            ["Entidad solicitante",
             "Efectivo propio y horas de su personal",
             "Carta de compromiso con el monto desagregado por partida",
             "Un monto global, sin desagregar por partida"],
            ["Empresa asociada",
             "Efectivo, insumos y horas de su personal técnico",
             "Convenio de asociación firmado antes de la postulación",
             "Una firma posterior a la fecha de cierre de la convocatoria"],
            ["Universidad asociada",
             "Horas de investigador y uso de laboratorio valorizados",
             "Carta del vicerrectorado de investigación con el tarifario",
             "Horas de personal que el propio proyecto ya paga"],
            ["Entidad pública del ámbito de aplicación",
             "Uso de terreno, instalaciones o personal de campo",
             "Convenio interinstitucional vigente durante la ejecución",
             "Un compromiso verbal recogido en un acta de reunión"],
        ],
        titulo="Quién aporta la contrapartida, con qué documento se acredita y qué la invalida",
    )
    + "\n"
    + criterio(
        "Cada aporte comprometido lleva firma, fecha y monto desagregado. Un "
        "compromiso sin monto no se puede evaluar y se descuenta del presupuesto "
        "en la etapa de admisibilidad."
    )
    + "\n"
    + fuente_pie(F_PROINNOVATE, F_PROCIENCIA)
)


OBSTACULOS_Y_FONDOS = envolver(
    cabecera("01 · La contrapartida",
             "Obstáculos declarados por empresas manufactureras del Perú y la contrapartida",
             "i-alert")
    + "\n"
    + figura(
        "s3-gauges-obstaculos",
        "Los tres obstáculos a la innovación más declarados por empresas manufactureras del Perú",
        "<b>La contrapartida en efectivo se le pide a la figura que declara no "
        "tener fondos: una de cada tres empresas.</b>",
    )
    + "\n"
    + dato_clave(
        "El <b>43,4 %</b> de las empresas manufactureras declara el costo de "
        "innovar como obstáculo, el <b>33,3 %</b> la escasez de personal "
        "calificado y el <b>32,3 %</b> la falta de fondos propios."
    )
    + "\n"
    + conclusion(
        "Consecuencia para el plan de financiamiento",
        "La contrapartida en efectivo se compromete antes de postular, con la "
        "cuenta y el monto identificados. Una empresa que la declara sin tenerla "
        "lo descubre en el primer desembolso, cuando el fondo pide el depósito.",
    )
    + "\n"
    + fuente_pie(F_POLCTI_DIAG, F_INEI)
)


LEY_30309_POR_ANO = envolver(
    cabecera("01 · Adjudicación y beneficio",
             "Proyectos presentados y aprobados en la Ley 30309 por año, 2016-2022",
             "i-chart")
    + "\n"
    + definicion(
        "Beneficio tributario a la I+D+i (<i>tax credit</i>)",
        "Ley 30309",
        "Deducción adicional del impuesto a la renta sobre el gasto ya ejecutado "
        "en investigación, desarrollo tecnológico e innovación, cuando el "
        "CONCYTEC califica el proyecto. Se solicita después de gastar.",
        "i-budget",
    )
    + "\n"
    + figura(
        "s3-marimekko-30309",
        "Proyectos presentados y tasa de aprobación de la Ley 30309, por año, 2016-2022",
        "<b>La tasa de aprobación pasó del 11 % de 2016 al 53 % de 2022 sin que "
        "la ley cambiara.</b>",
    )
    + "\n"
    + dato_clave(
        "Entre 2016 y 2022 se presentaron <b>352 proyectos</b> y se aprobaron "
        "<b>136</b>, el <b>39 %</b> acumulado del periodo."
    )
    + "\n"
    + fuente_pie(F_LEY_30309, F_POLCTI)
)


LEY_30309_ACUMULADO = envolver(
    cabecera("01 · Adjudicación y beneficio",
             "Proyectos acumulados con beneficio tributario aprobado, 2016-2022",
             "i-milestone")
    + "\n"
    + figura(
        "s3-escalones-30309",
        "Proyectos presentados y aprobados acumulados en la Ley 30309, 2016-2022",
        "<b>Siete años de vigencia dejan 136 proyectos calificados en todo el "
        "país, unos veinte por año.</b>",
    )
    + "\n"
    + criterio(
        "El beneficio se pide sobre gasto ya ejecutado, así que exige caja propia "
        "durante toda la ejecución. Entra en el plan de financiamiento como "
        "recuperación posterior, no como fuente."
    )
    + "\n"
    + evitar(
        "Declarar el beneficio tributario como contrapartida. La contrapartida se "
        "aporta durante la ejecución y el beneficio llega después, con la "
        "declaración anual del impuesto."
    )
    + "\n"
    + fuente_pie(F_LEY_30309, F_POLCTI)
)


DESEMBOLSO_Y_CAJA = envolver(
    cabecera("01 · Adjudicación y beneficio",
             "Momento del desembolso de cada forma y efecto en la caja",
             "i-clock")
    + "\n"
    + tabla(
        ["Forma del instrumento", "Cuándo entra el dinero",
         "Quién financia el gasto entretanto", "Riesgo que hay que cubrir"],
        [
            ["Beca",
             "Por armadas, durante el programa",
             "El fondo, desde la primera armada",
             "El desfase entre la matrícula y la primera armada"],
            ["Concurso de investigación",
             "Por tramos, contra informe aprobado",
             "La entidad titular, hasta el tramo siguiente",
             "Un informe observado detiene el tramo siguiente"],
            ["Subvención a la innovación empresarial",
             "Por tramos, contra hito verificado",
             "La empresa, con su contrapartida en efectivo",
             "Un hito que se retrasa retrasa el desembolso"],
            ["Servicio tecnológico",
             "No hay desembolso al proyecto",
             "Quien contrata el servicio, por adelantado",
             "El costo del ensayo, que se paga antes del resultado"],
            ["Beneficio tributario",
             "Con la declaración anual del impuesto",
             "La empresa, durante todo el ejercicio",
             "El gasto no calificado, que ya se ejecutó"],
        ],
        titulo="Momento del desembolso de cada forma de instrumento y quién financia el gasto entretanto",
    )
    + "\n"
    + criterio(
        "Toda forma salvo la beca exige que alguien financie el gasto antes de "
        "cobrarlo, y ese alguien se nombra con su cuenta y su monto."
    )
    + "\n"
    + fuente_pie(F_PROCIENCIA, F_PROINNOVATE, F_LEY_30309)
)


TRAMO_Y_VENTANILLA = envolver(
    cabecera("01 · Tramo de madurez y ventanilla",
             "Tramo de madurez TRL que admite cada ventanilla pública de financiamiento",
             "i-ladder")
    + "\n"
    + figura(
        "s3-rangos-trl-ventanilla",
        "Tramo de la escala TRL admitido por cada ventanilla pública de financiamiento de CTI",
        "<b>Los dos cortes de la escala separan tres ventanillas distintas, y el "
        "beneficio tributario no usa ninguno de los dos.</b>",
    )
    + "\n"
    + criterio(
        "Se declara el tramo del componente que se va a ejecutar con el dinero "
        "solicitado. Lo ya alcanzado entra como antecedente, con el documento "
        "que lo acredita."
    )
    + "\n"
    + dato_clave(
        "Los ensayos que acreditan el paso al entorno relevante se hacen en la "
        "<b>Red CITE</b> del ITP: <b>46 centros</b>, dato de 2024. El servicio se "
        "contrata, y no se subvenciona."
    )
    + "\n"
    + fuente_pie(F_POLCTI_DIAG, F_PROCIENCIA, F_PROINNOVATE)
)


ADMISIBILIDAD = envolver(
    cabecera("01 · Tramo de madurez y ventanilla",
             "Filtros de admisibilidad previos a la evaluación técnica de una propuesta",
             "i-rubric")
    + "\n"
    + figura(
        "s3-admisibilidad-filtros",
        "Los tres filtros de admisibilidad y el documento que acredita cada uno",
        "<b>Una propuesta se detiene en el primer filtro que falla y no llega a "
        "la evaluación técnica.</b>",
    )
    + "\n"
    + definicion(
        "Admisibilidad (<i>eligibility</i>)",
        "Bases de convocatoria de ProInnóvate y PROCIENCIA",
        "Filtro que se aplica a una propuesta antes de la evaluación técnica y "
        "que comprueba tres cosas: la figura del postulante, el tramo de "
        "madurez declarado y la contrapartida comprometida. Una propuesta "
        "inadmisible no llega a leerse.",
        "i-rubric",
    )
    + "\n"
    + criterio(
        "Los tres filtros se comprueban contra las bases. Cada uno tiene un "
        "documento que lo acredita, y sin ese documento el filtro se da por "
        "incumplido."
    )
    + "\n"
    + fuente_pie(F_PROINNOVATE, F_PROCIENCIA)
)


VENTANILLA_JS = """\t\t<script type="module">
\t\t\t// Tres condiciones encadenadas deciden la ventanilla: el tramo de
\t\t\t// madurez, la figura del postulante y la contrapartida en efectivo
\t\t\t// disponible. Al recorrer cada control de extremo a extremo el veredicto
\t\t\t// cambia, que es lo que una simulación tiene que demostrar
\t\t\t// (METODOLOGIA.md §3.3):
\t\t\t//   TRL 1 a 9 con universidad y sin efectivo: de una ventanilla a ninguna.
\t\t\t//   Figura, en TRL 2 sin efectivo: universidad e instituto tienen una,
\t\t\t//   las otras tres no tienen ninguna.
\t\t\t//   Efectivo, en TRL 5 con empresa: de ninguna ventanilla a cuatro.
\t\t\tconst VENTANILLAS = [
\t\t\t\t{ nombre: "PROCIENCIA · investigación básica y aplicada",
\t\t\t\t  trl: [1, 3], efectivo: false,
\t\t\t\t  entidades: ["universidad", "instituto"],
\t\t\t\t  nota: "La contrapartida se cubre con horas de investigador y uso de laboratorio valorizados." },
\t\t\t\t{ nombre: "PROCIENCIA · proyecto asociativo con empresa",
\t\t\t\t  trl: [3, 6], efectivo: true,
\t\t\t\t  entidades: ["universidad", "instituto", "empresa", "asociacion"],
\t\t\t\t  nota: "La parte en efectivo la aporta la empresa asociada, con convenio firmado antes del cierre." },
\t\t\t\t{ nombre: "ProInnóvate · desarrollo tecnológico",
\t\t\t\t  trl: [4, 6], efectivo: true, entidades: ["empresa"],
\t\t\t\t  nota: "El desembolso llega por tramos, contra hito verificado: la empresa financia cada tramo antes de cobrarlo." },
\t\t\t\t{ nombre: "ProInnóvate · validación y escalamiento",
\t\t\t\t  trl: [7, 9], efectivo: true, entidades: ["empresa"],
\t\t\t\t  nota: "Exige un usuario que ya opere el sistema y un acta que lo acredite." },
\t\t\t\t{ nombre: "ProInnóvate · capital semilla para emprendimiento",
\t\t\t\t  trl: [6, 9], efectivo: true, entidades: ["emprendedor", "empresa"],
\t\t\t\t  nota: "La constitución de la empresa suele ser condición para el desembolso, no para postular." },
\t\t\t\t{ nombre: "ITP · Red CITE · servicio tecnológico de ensayo",
\t\t\t\t  trl: [4, 9], efectivo: true,
\t\t\t\t  entidades: ["universidad", "instituto", "empresa", "emprendedor", "asociacion"],
\t\t\t\t  nota: "El servicio se paga y no se subvenciona: el desembolso sale de la caja del proyecto." },
\t\t\t\t{ nombre: "CONCYTEC · Ley 30309 · beneficio tributario",
\t\t\t\t  trl: [1, 9], efectivo: true, entidades: ["empresa"],
\t\t\t\t  nota: "El gasto se ejecuta primero y se recupera con la declaración anual del impuesto." },
\t\t\t];

\t\t\tconst FIGURAS = {
\t\t\t\tuniversidad: "una universidad licenciada",
\t\t\t\tempresa: "una empresa formal",
\t\t\t\temprendedor: "una persona o un equipo sin empresa constituida",
\t\t\t\tasociacion: "una asociación o cooperativa",
\t\t\t\tinstituto: "un instituto público de investigación",
\t\t\t};

\t\t\tconst mando = document.getElementById("v-trl");
\t\t\tconst nivel = document.getElementById("v-nivel");
\t\t\tconst veredicto = document.getElementById("v-veredicto");
\t\t\tconst detalle = document.getElementById("v-detalle");
\t\t\tconst admite = document.getElementById("v-admite");
\t\t\tconst fuera = document.getElementById("v-fuera");
\t\t\tconst efectivo = document.getElementById("v-efectivo");
\t\t\tconst botones = document.querySelectorAll("[data-figura]");
\t\t\tlet figura = "universidad";

\t\t\tfunction razon(v, trl, fig, hay) {
\t\t\t\tif (trl < v.trl[0] || trl > v.trl[1]) {
\t\t\t\t\treturn "admite TRL " + v.trl[0] + "-" + v.trl[1];
\t\t\t\t}
\t\t\t\tif (!v.entidades.includes(fig)) return "no admite esa figura";
\t\t\t\tif (v.efectivo && !hay) return "exige contrapartida en efectivo";
\t\t\t\treturn "";
\t\t\t}

\t\t\tfunction pintar() {
\t\t\t\tconst trl = Number(mando.value);
\t\t\t\tconst hay = efectivo.checked;
\t\t\t\tnivel.textContent = "TRL " + trl;

\t\t\t\tconst ok = [];
\t\t\t\tconst no = [];
\t\t\t\tfor (const v of VENTANILLAS) {
\t\t\t\t\tconst r = razon(v, trl, figura, hay);
\t\t\t\t\tif (r) no.push({ v, r });
\t\t\t\t\telse ok.push(v);
\t\t\t\t}

\t\t\t\t// La lista de descartes se ordena por cercanía: primero la que solo
\t\t\t\t// falla por la contrapartida, después por la figura y al final por el
\t\t\t\t// tramo. Con siete descartes y orden de declaración, el panel mostraba
\t\t\t\t// las tres que nunca van a servir y escondía la que está a una firma.
\t\t\t\tconst peso = { "exige contrapartida en efectivo": 0, "no admite esa figura": 1 };
\t\t\t\tno.sort((a, b) => (peso[a.r] ?? 2) - (peso[b.r] ?? 2));

\t\t\t\tadmite.innerHTML = ok.length
\t\t\t\t\t? ok.map((v) => "<li>" + v.nombre + "</li>").join("")
\t\t\t\t\t: "<li>Ninguna de las siete ventanillas públicas con esta combinación.</li>";
\t\t\t\tfuera.innerHTML = no.slice(0, 4)
\t\t\t\t\t.map((x) => "<li>" + x.v.nombre + " · " + x.r + "</li>").join("");

\t\t\t\tif (ok.length === 0) {
\t\t\t\t\tveredicto.textContent = "Sin ventanilla admisible";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "Con " + FIGURAS[figura] + " en TRL " + trl
\t\t\t\t\t\t+ (hay ? " y contrapartida en efectivo disponible" : " y sin contrapartida en efectivo")
\t\t\t\t\t\t+ ", ninguna ventanilla pública admite el proyecto. La salida es cambiar de figura con una entidad asociada, o financiar antes el tramo que falta.";
\t\t\t\t} else if (ok.length === 1) {
\t\t\t\t\tveredicto.textContent = "Una ventanilla admisible";
\t\t\t\t\tveredicto.dataset.estado = "warn";
\t\t\t\t\tdetalle.textContent = ok[0].nota;
\t\t\t\t} else {
\t\t\t\t\tveredicto.textContent = ok.length + " ventanillas admisibles";
\t\t\t\t\tveredicto.dataset.estado = "ok";
\t\t\t\t\tdetalle.textContent = ok[0].nota;
\t\t\t\t}
\t\t\t}

\t\t\tfor (const b of botones) {
\t\t\t\tb.addEventListener("click", () => {
\t\t\t\t\tfigura = b.dataset.figura;
\t\t\t\t\tfor (const o of botones) o.classList.toggle("is-on", o === b);
\t\t\t\t\tpintar();
\t\t\t\t});
\t\t\t}
\t\t\tmando.addEventListener("input", pintar);
\t\t\tefectivo.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


VENTANILLA_SIM = envolver(
    cabecera("01 · Tramo de madurez y ventanilla",
             "Ventanillas admisibles según madurez, entidad y contrapartida",
             "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="ventanilla" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<label class="sim__label" for="v-trl">Tramo de madurez del componente</label>
\t\t\t\t\t\t<input class="sim__range" id="v-trl" type="range" min="1" max="9" step="1" value="2" />
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="v-nivel">TRL 2</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="v-veredicto" data-estado="warn">Una ventanilla admisible</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="picker">
\t\t\t\t\t\t\t<button class="picker__btn is-on" type="button" data-figura="universidad">Universidad</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="empresa">Empresa</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="emprendedor">Persona</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="asociacion">Asociación</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="instituto">Instituto</button>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="v-efectivo" />
\t\t\t\t\t\t\t<span><b>Contrapartida en efectivo disponible</b><span class="crit__help">Dinero propio con cuenta y monto</span></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<p class="sim__what" id="v-detalle"></p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Ventanillas que admiten</h3>
\t\t\t\t\t\t\t<ul id="v-admite"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Por qué queda fuera</h3>
\t\t\t\t\t\t\t<ul id="v-fuera"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Con empresa en TRL 5, marcar la
\t\t\t\tcontrapartida en efectivo pasa de ninguna ventanilla a cuatro.</p>"""
    + "\n"
    + fuente_pie(F_PROCIENCIA, F_PROINNOVATE, F_POLCTI_DIAG)
)


# ==========================================================================
# 02 · CONTENIDO DEL TEMA B
# ==========================================================================

INCUBACION_EVIDENCIA = envolver(
    cabecera("02 · Evidencia sobre incubación",
             "Producción de investigación sobre incubación de empresas por país, 1993-2022",
             "i-globe")
    + "\n"
    + figura(
        "s3-evidencia-incubacion",
        "Artículos, citas por artículo e índice h de los diez países más productivos en incubación, 1993-2022",
        "<b>Brasil es el único país latinoamericano entre los diez, con 10 artículos "
        "y 114 citas.</b> Estados Unidos publica 57 y reúne 2 483 citas.",
    )
    + "\n"
    + criterio(
        "Antes de citar una práctica de incubación conviene comprobar en qué país se "
        "midió. Estados Unidos y el Reino Unido reúnen 84 de los 186 artículos de los "
        "diez primeros y 3 456 de sus 4 616 citas."
    )
    + "\n"
    + aviso(
        "El artículo afirma que la mitad de la contribución procede de economías "
        "emergentes. Son cinco de los diez países del listado, pero 55 de los 186 "
        "artículos de la tabla, el 29,6 %.",
        "Discrepancia entre el texto y la tabla",
    )
    + "\n"
    + fuente_pie(F_DHIMAN)
)


INCUBADORA_ACELERADORA = envolver(
    cabecera("02 · Incubadora y aceleradora",
             "Incubadora y aceleradora: admisión, duración y servicio central de cada una",
             "i-scale")
    + "\n"
    + tabla(
        ["Rasgo", "Incubadora de empresas", "Aceleradora"],
        [
            ["Forma de admisión", "Ingreso continuo, empresa por empresa",
             "Cohorte con fecha de inicio y de cierre"],
            ["Duración del programa", "Sin plazo fijo en las definiciones recogidas",
             "Nueve meses o menos"],
            ["Servicio central", "Espacio, servicios compartidos y consultoría",
             "Componente formativo y mentoría"],
            ["Evidencia disponible", "259 artículos en Scopus, 1993-2022",
             "1 350 graduadas de 24 aceleradoras, 2010-2019"],
            ["Descomposición del desempeño", "La revisión no la descompone",
             "El gestor del programa explica el 7,7 % de la varianza"],
        ],
        "Rasgos con los que se distinguen la incubadora y la aceleradora",
    )
    + "\n"
    + definicion(
        "Aceleradora de empresas",
        "Avnimelech et al., criterios de selección de la muestra",
        "Programa de duración corta, nueve meses o menos, que admite a las empresas "
        "por cohortes y que incluye un componente formativo y de mentoría.",
    )
    + "\n"
    + conclusion(
        "Qué separa a las dos:",
        "La cohorte y el plazo. La incubadora admite empresa por empresa y sin plazo "
        "declarado; la aceleradora las agrupa en un grupo que entra y sale a la vez, "
        "en nueve meses o menos.",
    )
    + "\n"
    + fuente_pie(F_AVNIMELECH, F_DHIMAN)
)


ACELERADORA_COHORTE = envolver(
    cabecera("02 · La cohorte de aceleración",
             "Estructura anidada de las 1 350 <i>startups</i> aceleradas en Israel, 2010-2019",
             "i-layers")
    + "\n"
    + figura(
        "s3-anidamiento-cohortes",
        "Aceleradoras, gestores de programa, cohortes y <i>startups</i> de la muestra israelí, 2010-2019",
        "<b>Con 2,29 cohortes por gestor, y 2,07 en la muestra de tres años, la "
        "estructura queda por debajo del umbral de cinco observaciones por "
        "celda.</b>",
    )
    + "\n"
    + definicion(
        "Cohorte de aceleración",
        "Avnimelech et al., estructura del modelo jerárquico",
        "Grupo de <i>startups</i> que entra y termina el programa en las mismas "
        "fechas y bajo el mismo gestor. Es el nivel más bajo de la estructura.",
    )
    + "\n"
    + en_la_practica(
        "El conjunto reúne todas las graduadas de aceleradora de Israel entre 2010 y "
        "2019. Se excluyeron las cohortes de un solo miembro y las aceleradoras con "
        "menos de dos gestores."
    )
    + "\n"
    + fuente_pie(F_AVNIMELECH)
)


VARIANZA_CERO = envolver(
    cabecera("02 · Distribución del resultado",
             "Graduadas de aceleradora sin capital levantado, a doce meses y a tres años",
             "i-diagram")
    + "\n"
    + figura(
        "s3-cero-levantado",
        "Proporción de graduadas cuyo capital levantado es exactamente cero, por horizonte",
        "<b>Setenta y tres de cada cien no levantan nada en el primer año</b>; treinta "
        "y nueve siguen en cero a los tres.",
    )
    + "\n"
    + dato_clave(
        "A los tres años el reparto se mantiene: la cohorte explica el <b>5,64 %</b> y "
        "el gestor el 4,91 %, frente al 2,60 % de la aceleradora. El efecto del año de "
        "entrada es 0,00 % en los dos horizontes."
    )
    + "\n"
    + en_la_practica(
        "Los autores citan a Chan et al. (2020), que con datos de Estados Unidos, "
        "México, Kenia e India miden un efecto de aceleradora del 11,1 % y un efecto "
        "de sector del 0,0 %."
    )
    + "\n"
    + fuente_pie(F_AVNIMELECH)
)


DESEMPENO_LATAM = envolver(
    cabecera("02 · Desempeño posterior a la aceleración",
             "Factores de éxito de 15 417 empresas aceleradas: modelo general y América Latina",
             "i-users")
    + "\n"
    + figura(
        "s3-factores-gali",
        "Orden de los siete factores de éxito por razón de momios en tres modelos, base GALI",
        "<b>En la región solo tres de los siete factores resultan significativos al "
        "5 %</b>, y la experiencia directiva previa pasa al primer puesto.",
    )
    + "\n"
    + definicion(
        "Razón de momios",
        "Canfield Rivera, modelo logístico ordinal",
        "Cociente entre la probabilidad de que un resultado ocurra y la de que no "
        "ocurra, ante el aumento de una unidad del predictor. Un valor de uno indica "
        "ausencia de asociación.",
    )
    + "\n"
    + dato_clave(
        "La desigualdad de oportunidades cambia de signo: razón de momios de "
        "<b>0,73</b> en el resto del mundo y de <b>1,24</b> en América Latina, las dos "
        "significativas al 5 %."
    )
    + "\n"
    + fuente_pie(F_CANFIELD)
)


DESEMPENO_MUESTRA = envolver(
    cabecera("02 · Desempeño posterior a la aceleración",
             "Perfil de las empresas aceleradas de la base GALI y límites del modelo",
             "i-search")
    + "\n"
    + figura(
        "s3-muestra-gali",
        "Composición de la submuestra de 15 417 empresas aceleradas de la base GALI",
        "<b>Cuatro de cada cinco tienen empleados y solo la mitad declara ingresos.</b>",
    )
    + "\n"
    + dato_clave(
        "La submuestra reúne <b>15 417 empresas lucrativas</b> de 164 países, el 34 % "
        "en América Latina. El 28 % lleva tres años o más operando, el 52 % declara "
        "ingresos y el 78 % tiene empleados."
    )
    + "\n"
    + en_la_practica(
        "El 16 % había recibido capital externo antes del programa, el 14 % deuda y el "
        "25 % inversión filantrópica. Superar el tercer año multiplica por 1,95 la "
        "razón de momios en el modelo regional."
    )
    + "\n"
    + fuente_pie(F_CANFIELD)
)


ANGEL_CRITERIOS = envolver(
    cabecera("02 · El inversor ángel",
             "Seis categorías de criterios de tamizaje del inversor ángel en etapa temprana",
             "i-rubric")
    + "\n"
    + tabla(
        ["Categoría", "Criterio que más se declara", "Inversores de 31"],
        [
            ["Potencial de mercado", "Mercado en crecimiento rápido", "20 · 64,5 %"],
            ["Preferencias del inversor", "Proyectos de tecnologías de la información",
             "19 · 61,3 %"],
            ["Emprendedor y equipo", "Avance conseguido hasta la fecha", "25 · 80,6 %"],
            ["Producto", "Potencial de expansión del producto", "26 · 83,9 %"],
            ["Criterios financieros", "Aporte financiero del propio emprendedor",
             "28 · 90,3 %"],
            ["Control y seguimiento", "Papel directivo o de consultoría del inversor",
             "la fuente no publica la frecuencia"],
        ],
        "Criterios de tamizaje del inversor ángel por categoría y frecuencia declarada",
    )
    + "\n"
    + dato_clave(
        "La rentabilidad esperada no admite gradación: los <b>31 inversores</b> exigen "
        "una rentabilidad muy alta y ninguno acepta una rentabilidad nula o negativa."
    )
    + "\n"
    + aviso(
        "El texto describe el potencial de expansión del producto como un factor poco "
        "mencionado. Su tabla le asigna 26 de los 31 inversores, el 83,9 %, la "
        "frecuencia más alta de la categoría.",
        "Discrepancia entre el texto y la tabla",
    )
    + "\n"
    + fuente_pie(F_SKALICKA)
)


ANGEL_ETAPA = envolver(
    cabecera("02 · Etapa y rentabilidad exigida",
             "Aceptación de propuestas por etapa del proyecto y exigencia de rentabilidad",
             "i-ladder")
    + "\n"
    + figura(
        "s3-angel-etapa",
        "Propuestas que superan el tamizaje del inversor ángel según la etapa del proyecto",
        "<b>La etapa semilla pasa el tamizaje en el 48 % de los casos y la emergente en el 84 %.</b>",
    )
    + "\n"
    + dato_clave(
        "La propuesta pasa el tamizaje en el <b>84 %</b> de los casos si el proyecto "
        "está en etapa emergente, en el 77 % en expansión y en el <b>48 %</b> en "
        "semilla o puesta en marcha."
    )
    + "\n"
    + en_la_practica(
        "El 90,3 % de los inversores exige que el emprendedor ponga dinero propio. "
        "Solo el 9,7 % admite financiar sin aporte del iniciador del proyecto, y "
        "siempre bajo condiciones."
    )
    + "\n"
    + criterio(
        "Un proyecto en crisis existencial baja la aceptación al 19 % en semilla, al "
        "23 % en etapa emergente y al 13 % en expansión. En semilla, el financiamiento "
        "de crisis es el 40 % de los fondos invertidos."
    )
    + "\n"
    + fuente_pie(F_SKALICKA)
)


CAPITAL_VEHICULOS = envolver(
    cabecera("02 · Capital de riesgo en la región",
             "Vehículos de inversión temprana identificados en Jamaica y Trinidad y Tobago, 2025",
             "i-budget")
    + "\n"
    + tabla(
        ["Vehículo", "País", "Capital comprometido", "Tamaño objetivo"],
        [
            ["<i>Caribbean Venture Capital Fund</i> · MScale", "Jamaica",
             "15,4 millones USD en el primer cierre",
             "50 millones USD, con el 30 % reservado a capital de riesgo"],
            ["Stratus SME Private Equity Fund", "Jamaica",
             "la fuente no publica el cierre",
             "3 000 millones JMD, unos 19,5 millones USD"],
            ["JASMEF", "Jamaica", "la fuente no publica el cierre",
             "10 millones USD"],
            ["First Angels Jamaica", "Jamaica", "3 millones USD en una década",
             "unos 500 000 USD al año de capacidad estimada"],
            ["Tobago House of Assembly · VCEFL", "Trinidad y Tobago",
             "25 millones TTD, unos 3,7 millones USD",
             "100 millones TTD, unos 14,7 millones USD"],
            ["Aspire Fund Management", "Trinidad y Tobago",
             "50 millones USD de activos gestionados",
             "operaciones de 250 000 a 1 millón USD"],
        ],
        "Vehículos de inversión temprana identificados en dos mercados del Caribe, 2024-2025",
    )
    + "\n"
    + criterio(
        "La forma del vehículo decide el plazo de salida y el control del "
        "consejo. Las dos cosas se pactan antes de la primera transferencia."
    )
    + "\n"
    + fuente_pie(F_LESLIE)
)


CAPITAL_BRECHA = envolver(
    cabecera("02 · Brecha de financiamiento",
             "Brecha entre el interés por el capital y el capital levantado, Caribe 2025",
             "i-flow")
    + "\n"
    + figura(
        "s3-capital-brecha",
        "Interés declarado por levantar capital y capital efectivamente levantado, Caribe 2025",
        "<b>De cada tres fundadores que declaran interés, uno ha levantado capital.</b>",
    )
    + "\n"
    + dato_clave(
        "El <b>79,3 %</b> de los fundadores encuestados declara interés en levantar "
        "capital, el <b>27,5 %</b> lo ha levantado y el 17 % apunta específicamente a "
        "capital de riesgo."
    )
    + "\n"
    + en_la_practica(
        "La brecha total de financiamiento de las pymes del Caribe se estima entre "
        "<b>4 000 y 6 000 millones de dólares</b> al año. Menos del 1 % de las "
        "<i>startups</i> accede a capital de riesgo."
    )
    + "\n"
    + fuente_pie(F_LESLIE)
)


GARANTIA_RANGO = envolver(
    cabecera("02 · Garantía parcial de crédito",
             "Coberturas mínima, mediana y máxima de ocho esquemas de garantía, 2011",
             "i-file")
    + "\n"
    + figura(
        "s3-rango-cobertura-mena",
        "Recorrido de la razón de cobertura dentro de cada esquema nacional, ocho economías, 2011",
        "<b>Marruecos opera del 50 % al 80 % en el mismo esquema:</b> la cobertura "
        "depende del producto y del tamaño del prestatario.",
    )
    + "\n"
    + dato_clave(
        "Las comisiones anuales de los esquemas maduros van del <b>0,8 %</b> de "
        "Taiwán al <b>2,3 %</b> de Canadá, sobre el importe garantizado. Corea cobra "
        "el 1,2 % y Estados Unidos el 1,9 %."
    )
    + "\n"
    + criterio(
        "La cobertura y la comisión se leen juntas. En Hungría la comisión sube con la "
        "cobertura: 0,6 % anual con el 40 % cubierto y 0,9 % con el 70 %."
    )
    + "\n"
    + fuente_pie(F_GOFFE)
)


GARANTIA_DESEMPENO = envolver(
    cabecera("02 · Garantía parcial de crédito",
             "Apalancamiento, mora y alcance de los esquemas de garantía por región, 2016",
             "i-network")
    + "\n"
    + figura(
        "s3-garantias-region",
        "Apalancamiento, tasa de mora y pymes atendidas por esquema de garantía, cinco regiones",
        "<b>África apalanca 1,7 veces con un 17,1 % de mora; el hemisferio occidental "
        "apalanca 3,0 con un 2,0 %.</b>",
    )
    + "\n"
    + dato_clave(
        "Los esquemas del hemisferio occidental atienden <b>6 531 pymes</b> cada uno, "
        "el 3,4 % de las pymes del país, con un apalancamiento de 3,0 veces y una mora "
        "del 2,0 %."
    )
    + "\n"
    + en_la_practica(
        "Italia es el país europeo con más garantías vigentes: el <b>2,1 % del "
        "PBI</b> y 33 600 millones de euros, frente a 16 700 millones en Francia y "
        "5 600 millones en Alemania."
    )
    + "\n"
    + fuente_pie(F_GOFFE)
)


ANGEL_MERCADO_JS = """\t\t<script type="module">
\t\t\t// Las cuatro condiciones de mercado que el estudio identifica, y la
\t\t\t// probabilidad PUBLICADA de no quedar descartado con cada combinación.
\t\t\t// La tabla da un valor por combinación, no una fórmula: aquí no se
\t\t\t// interpola ni se promedia nada (METODOLOGIA.md §17.15). La combinación
\t\t\t// vacía no aparece en la tabla, y por eso el veredicto lo declara en vez
\t\t\t// de suponer un cero.
\t\t\tconst CONDICIONES = {
\t\t\t\tA: { rotulo: "Mercado internacional",
\t\t\t\t\tnota: "11 de los 31 inversores lo exigen · 35,5 %" },
\t\t\t\tB: { rotulo: "Mercado en crecimiento rápido",
\t\t\t\t\tnota: "20 de los 31 inversores lo exigen · 64,5 %" },
\t\t\t\tC: { rotulo: "Mercado objetivo identificable",
\t\t\t\t\tnota: "18 de los 31 inversores lo exigen · 58,1 %" },
\t\t\t\tD: { rotulo: "Sin competencia significativa",
\t\t\t\t\tnota: "10 de los 31 inversores lo exigen · 32,3 %" },
\t\t\t};

\t\t\t// Skalicka et al., Tabla 6, en porcentaje. La clave es la lista de
\t\t\t// condiciones acreditadas en orden alfabético.
\t\t\tconst PROBABILIDAD = {
\t\t\t\tA: 3, B: 16, C: 13, D: 3,
\t\t\t\tAB: 39, AC: 16, AD: 6, BC: 39, BD: 19, CD: 32,
\t\t\t\tABC: 68, ABD: 42, ACD: 35, BCD: 65,
\t\t\t\tABCD: 100,
\t\t\t};

\t\t\t// El recuento se escribe en palabra y no en cifra: la insignia ya lleva
\t\t\t// el porcentaje y mezclar dos números en la misma frase se lee mal.
\t\t\tconst PALABRAS = ["ninguna", "una", "dos", "tres", "cuatro"];

\t\t\tconst casillas = [...document.querySelectorAll('.crit__box input[data-cond]')];
\t\t\tconst veredicto = document.getElementById("am-veredicto");
\t\t\tconst detalle = document.getElementById("am-detalle");
\t\t\tconst acreditadas = document.getElementById("am-si");
\t\t\tconst ausentes = document.getElementById("am-no");

\t\t\tfunction fila(clave) {
\t\t\t\tconst c = CONDICIONES[clave];
\t\t\t\treturn "<li><b>" + c.rotulo + "</b> · " + c.nota + "</li>";
\t\t\t}

\t\t\tfunction pintar() {
\t\t\t\tconst si = casillas.filter((c) => c.checked)
\t\t\t\t\t.map((c) => c.dataset.cond).sort();
\t\t\t\tconst no = casillas.filter((c) => !c.checked)
\t\t\t\t\t.map((c) => c.dataset.cond).sort();
\t\t\t\tacreditadas.innerHTML = si.length ? si.map(fila).join("")
\t\t\t\t\t: "<li>Ninguna de las cuatro condiciones está acreditada.</li>";
\t\t\t\tausentes.innerHTML = no.length ? no.map(fila).join("")
\t\t\t\t\t: "<li>Ninguna: las cuatro condiciones se cumplen.</li>";

\t\t\t\tconst p = PROBABILIDAD[si.join("")];
\t\t\t\tif (p === undefined) {
\t\t\t\t\tveredicto.textContent = "Sin valor publicado";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "La tabla no publica la probabilidad cuando " +
\t\t\t\t\t\t"no se acredita ninguna de las cuatro condiciones de mercado.";
\t\t\t\t\treturn;
\t\t\t\t}

\t\t\t\tveredicto.textContent = p + " %";
\t\t\t\tveredicto.dataset.estado = p === 100 ? "ok" : (p >= 35 ? "warn" : "danger");
\t\t\t\tconst cuantas = si.length === 1
\t\t\t\t\t? "una condición" : PALABRAS[si.length] + " condiciones";
\t\t\t\tdetalle.textContent = p === 100
\t\t\t\t\t? "Con las cuatro condiciones acreditadas, ninguno de los 31 " +
\t\t\t\t\t  "inversores descarta la propuesta en el tamizaje inicial."
\t\t\t\t\t: "Probabilidad publicada de no quedar descartado de entrada con " +
\t\t\t\t\t  cuantas + " de mercado acreditadas.";
\t\t\t}
\t\t\tfor (const c of casillas) c.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


def _mercado(clave, rotulo, ayuda, marcado=True):
    """Casilla de una condición de mercado del tamizaje del inversor ángel.

    Misma marca que el clasificador de la sesión 1 y que los determinantes de
    la sesión 2: si las tres interactivas usan la misma casilla, el CSS ya
    existe y el control se reconoce sin volver a aprenderlo.

    Arrancan las cuatro marcadas: así el recorrido de extremo a extremo va del
    100 % publicado al 3 % de una sola condición, y el veredicto cambia tres
    veces por el camino (METODOLOGIA.md §3.3).
    """
    ch = " checked" if marcado else ""
    return f"""\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" data-cond="{clave}"{ch} />
\t\t\t\t\t\t\t<span><b>{rotulo}</b><span class="crit__help">{ayuda}</span></span>
\t\t\t\t\t\t</label>"""


ANGEL_MERCADO_SIM = envolver(
    cabecera("02 · Condiciones de mercado",
             "Probabilidad de superar el tamizaje según las condiciones de mercado acreditadas",
             "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="angel-mercado" data-animate="fade-up">
\t\t\t\t\t<div class="crit">
{_mercado("A", "Mercado internacional establecido o alcanzable", "Tamaño del mercado en unidades y países")}
{_mercado("B", "Mercado en crecimiento rápido", "Tasa de crecimiento anual con su fuente")}
{_mercado("C", "Mercado objetivo claramente identificable", "Cliente nombrado y demanda expresada")}
{_mercado("D", "Sin competencia significativa", "Competidores nombrados y ventaja sostenible")}
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t<span class="sim__badge" id="am-veredicto" data-estado="ok">100 %</span>
\t\t\t\t\t\t<span class="sim__what" id="am-detalle"></span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Condiciones acreditadas, con la frecuencia con que se exigen</h3>
\t\t\t\t\t\t\t<ul id="am-si"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Condiciones ausentes</h3>
\t\t\t\t\t\t\t<ul id="am-no"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Desmarcar el mercado en crecimiento
\t\t\t\trápido baja la probabilidad publicada del 100 % al 35 %.</p>"""
    + "\n"
    + fuente_pie(F_SKALICKA)
)


# ==========================================================================
# 02 · INCUBACIÓN DE EMPRESAS
# ==========================================================================

INCUBACION_DEFINICION = envolver(
    cabecera("02 · Incubación de empresas",
             "Incubación de empresas: definición y tres generaciones desde los años setenta",
             "i-building")
    + "\n"
    + figura(
        "s3-generaciones-incubadora",
        "Generaciones de incubadora de empresas y servicio central de cada una, 1970-2013",
        "<b>Cada generación añade un servicio y ninguna retira el anterior: primero "
        "el espacio, después la formación, después la red.</b>",
    )
    + "\n"
    + definicion(
        "Incubadora de empresas",
        "NBIA (2021), recogida por Dhiman y Arora",
        "Instalación que ofrece recursos compartidos a empresas jóvenes, como "
        "espacio de oficina, consultores y personal, y que puede dar además acceso "
        "a financiamiento y soporte técnico.",
    )
    + "\n"
    + dato_clave(
        "La revisión cubre <b>259 artículos</b> de 150 revistas indexados en Scopus "
        "entre 1993 y 2022, filtrados desde 447 documentos. Las tres generaciones "
        "conviven hoy en el mismo mercado."
    )
    + "\n"
    + fuente_pie(F_DHIMAN)
)


# ==========================================================================
# 02 · CUÁNTO DEL DESEMPEÑO ES ATRIBUIBLE A LA ACELERADORA
# ==========================================================================

VARIANZA_DESCOMPOSICION = envolver(
    cabecera("02 · Descomposición de varianza",
             "Varianza del capital levantado atribuible a cada nivel del programa de aceleración",
             "i-chart")
    + "\n"
    + figura(
        "s3-varianza-aceleradora",
        "Porcentaje de la varianza del capital levantado a 12 meses explicado por cada clase de efecto",
        "<b>Al añadir gestor y cohorte al modelo, el efecto de la aceleradora cae del "
        "8,9 % al 3,6 %.</b> La cohorte explica el 7,5 %.",
    )
    + "\n"
    + definicion(
        "Descomposición de varianza",
        "Avnimelech et al., método bayesiano jerárquico",
        "Reparto de la variación total de un resultado entre las clases de efecto "
        "que podrían explicarla. Cada clase recibe un porcentaje medio y un "
        "intervalo posterior.",
    )
    + "\n"
    + criterio(
        "El modelo base y el modelo completo son estimaciones distintas y sus "
        "porcentajes no se suman. Al añadir gestor y cohorte, parte de lo que se "
        "atribuía a la aceleradora se reasigna."
    )
    + "\n"
    + fuente_pie(F_AVNIMELECH)
)


# ==========================================================================
# 02 · LOS CRITERIOS DEL INVERSOR ÁNGEL
# ==========================================================================

ANGEL_RECHAZO = envolver(
    cabecera("02 · El inversor ángel",
             "Motivos de rechazo del inversor ángel en la etapa temprana, Chequia 2018-2019",
             "i-alert")
    + "\n"
    + figura(
        "s3-rechazo-matriz",
        "Frecuencia de cinco motivos de rechazo y correlación entre ellos, 31 inversores ángeles",
        "<b>La desconfianza en el emprendedor aparece en 26 de los 31</b> y va junto "
        "con el aporte propio insuficiente, con una correlación de 0,60.",
    )
    + "\n"
    + definicion(
        "Inversor ángel",
        "Skalicka et al., marco teórico",
        "Capitalista de riesgo no institucionalizado que invierte patrimonio propio "
        "en empresas de etapa temprana y espera tomar un papel directivo o de "
        "consultoría en la participada.",
    )
    + "\n"
    + criterio(
        "El tamizaje funciona por eliminación: basta un defecto fatal para descartar "
        "la propuesta. La correlación no dice cuál causa cuál, solo que los dos "
        "motivos aparecen juntos."
    )
    + "\n"
    + fuente_pie(F_SKALICKA)
)


# ==========================================================================
# 02 · CAPITAL DE RIESGO EN LA REGIÓN
# ==========================================================================

CAPITAL_ESCALA = envolver(
    cabecera("02 · Capital de riesgo en la región",
             "Magnitud anual del capital de riesgo en América Latina y el Caribe, 2015-2022",
             "i-fund")
    + "\n"
    + figura(
        "s3-escala-capital-region",
        "Inversión anual de capital de riesgo en América Latina y en su tramo de <i>deep tech</i>, 2015-2022",
        "<b>El Caribe entero invierte menos de 50 millones de dólares al año, por "
        "debajo del 1 % del volumen de operaciones de la región.</b>",
    )
    + "\n"
    + definicion(
        "Capital de riesgo",
        "Leslie et al. (2025), BID",
        "Financiamiento de capital con estrategia de riesgo y recompensa altos, "
        "dirigido a empresas tecnológicas de etapa semilla y temprana. Suele seguir a "
        "una ronda de inversores ángeles.",
    )
    + "\n"
    + dato_clave(
        "La inversión regional en <i>deep tech</i> pasó de <b>96 millones de dólares</b> "
        "en 2020 a <b>172 millones</b> en 2022. El informe los da como el 0,59 % y el "
        "2,2 % del capital regional, proporciones que no cuadran con la serie."
    )
    + "\n"
    + fuente_pie(F_LESLIE, F_BID)
)


# ==========================================================================
# 02 · GARANTÍAS PARCIALES DE CRÉDITO
# ==========================================================================

GARANTIA_COBERTURA = envolver(
    cabecera("02 · Garantía parcial de crédito",
             "Razón de cobertura máxima de los esquemas de garantía del G-20",
             "i-agreement")
    + "\n"
    + figura(
        "s3-cobertura-g20",
        "Distribución de la razón de cobertura máxima en diecinueve economías del G-20 y la Unión Europea",
        "<b>Nueve de las diecinueve cubren entre el 75 % y el 84 %</b>; solo China y "
        "Turquía llegan al 100 %.",
    )
    + "\n"
    + definicion(
        "Garantía parcial de crédito",
        "Goffe et al. (2021), Banco Mundial",
        "Compromiso por el que un fondo asume una fracción de la pérdida del "
        "prestamista si el crédito no se paga. El resto queda con el banco, para que "
        "mantenga el análisis de riesgo.",
    )
    + "\n"
    + criterio(
        "Bajar la cobertura del 90 % al 80 % duplica el riesgo del banco, de diez a "
        "veinte puntos, y duplica el capital que debe reservar. El informe considera "
        "típico el tramo del 50 % al 80 %."
    )
    + "\n"
    + fuente_pie(F_GOFFE)
)


# ==========================================================================
# HERRAMIENTAS 09 A 12
# ========================================================================

HERRAMIENTAS_09 = bloque_herramientas(
    ref="01", total="04",
    titulo="Tres portales donde se comprueba qué convocatoria está abierta hoy",
    para_que=(
        "Las bases cambian en cada edición y un monto citado sin fecha caduca antes de "
        "que la propuesta llegue a presentarse. Estos portales son la única fuente que "
        "dice qué está abierto, con qué plazo y con qué formatos."
    ),
    herramientas=[
        ("ProInnóvate", "Ministerio de la Producción", [
            "Bases, cronograma y formatos de cada concurso de innovación",
            "Publica las listas de adjudicados de ediciones anteriores",
            "Avisa de las charlas informativas de cada convocatoria",
        ], "proinnovate.gob.pe"),
        ("PROCIENCIA", "CONCYTEC", [
            "Concursos de investigación y programas de becas",
            "Publica los formatos y las guías de postulación",
            "Resultados por etapa: admisibilidad, evaluación y adjudicación",
        ], "prociencia.gob.pe"),
        ("gob.pe", "Plataforma del Estado peruano", [
            "Reúne convocatorias de todas las entidades, no solo las de CTI",
            "Sirve para los cinco sectores que operan los otros 55 instrumentos",
            "Punto de entrada cuando no se sabe qué organismo lo opera",
        ], "gob.pe"),
    ],
    como_elegir=[
        ("Actualización", "Qué fecha lleva la página, y si la declara."),
        ("Bases", "Si el documento se descarga entero o solo hay un resumen."),
        ("Historial", "Si publica resultados anteriores, que dicen qué se aprueba."),
    ],
)

HERRAMIENTAS_10 = bloque_herramientas(
    ref="02", total="04",
    titulo="Tres buscadores de convocatorias que no salen en los portales oficiales",
    para_que=(
        "Los portales del Estado publican lo suyo y nada más. Fundaciones, embajadas, "
        "cámaras de comercio y organismos internacionales convocan por su cuenta, y "
        "esos avisos solo aparecen reunidos en plataformas que los rastrean a diario."
    ),
    herramientas=[
        ("Fondos y Convocatorias", "plataforma privada", [
            "Reúne a diario convocatorias locales e internacionales",
            "Filtra por país, tema y tipo de postulante",
            "Publica su propia radiografía anual del financiamiento",
        ], "fondosyconvocatorias.com.mx"),
        ("Gestionándote", "plataforma del tercer sector", [
            "Subvenciones y donaciones para organizaciones de la región",
            "Avisa de becas, premios y residencias además de proyectos",
            "Acceso libre a la mayor parte del listado",
        ], "gestionandote.org"),
        ("Rossel Consultores", "consultora regional", [
            "Fondos no reembolsables de organismos internacionales",
            "Cobertura declarada de Perú y del resto de la región",
            "Clasificado por sector, no solo por país",
        ], "rosselconsultores.org"),
    ],
    como_elegir=[
        ("Vigencia", "Si la ficha declara la fecha de cierre y si sigue abierta."),
        ("Filtro", "Si deja acotar por país y por figura de postulante."),
        ("Origen", "Si enlaza la convocatoria oficial o solo la resume."),
    ],
)

HERRAMIENTAS_11 = bloque_herramientas(
    ref="03", total="04",
    titulo="Tres bases de datos donde se consulta qué se ha invertido y quién lo puso",
    para_que=(
        "Antes de sentarse con un inversor conviene saber qué se invirtió en el sector, "
        "en qué etapa y quién puso el dinero. Las tres publican operaciones y ninguna "
        "publica todas: lo que falta suele ser lo pequeño y lo local."
    ),
    herramientas=[
        ("Crunchbase", "Crunchbase Inc.", [
            "Rondas, montos e inversores empresa por empresa",
            "Capa gratuita con número limitado de consultas",
            "Sirve para saber quién invirtió antes en tu sector",
        ], "crunchbase.com"),
        ("Dealroom", "Dealroom.co", [
            "Cobertura por país y por sector, con informes descargables",
            "Fichas de ecosistema con series por año",
            "Buen detalle de Europa y creciente de América Latina",
        ], "dealroom.co"),
        ("LAVCA", "asociación de capital privado en América Latina", [
            "Publica el dato agregado de la región, no empresa por empresa",
            "Informes anuales con el reparto por país y por etapa",
            "Útil para el párrafo de contexto de una propuesta",
        ], "lavca.org"),
    ],
    como_elegir=[
        ("Cobertura", "Si el Perú y tu sector están de verdad, no solo el país grande."),
        ("Origen", "De dónde sale cada operación y si la empresa la confirmó."),
        ("Vacío", "Qué operaciones no aparecen, que suelen ser las pequeñas."),
    ],
)

HERRAMIENTAS_12 = bloque_herramientas(
    ref="04", total="04",
    titulo="Tres vías para localizar fondos de cooperación fuera del presupuesto nacional",
    para_que=(
        "El capital privado no agota lo que hay fuera del presupuesto público. La "
        "cooperación internacional entra al país por canales propios, con reglas de "
        "elegibilidad distintas y con su propia exigencia de contrapartida."
    ),
    herramientas=[
        ("APCI", "Agencia Peruana de Cooperación Internacional", [
            "Registro oficial de la cooperación que entra al país",
            "Informes anuales con montos por fuente y por sector",
            "Dice qué cooperante financia qué tipo de proyecto",
        ], "gob.pe/apci"),
        ("Funding & Tenders", "Comisión Europea", [
            "Convocatorias europeas y sus condiciones de participación",
            "Declara si un tercer país entra, y con qué figura",
            "Busca socios ya inscritos para formar consorcio",
        ], "ec.europa.eu/info/funding-tenders"),
        ("Convocatorias del BID", "Banco Interamericano de Desarrollo", [
            "Fondos, licitaciones y cooperación técnica del banco",
            "Operaciones por país y por sector, con su documentación",
            "Publica también los informes que sostienen sus prioridades",
        ], "iadb.org"),
    ],
    como_elegir=[
        ("Elegibilidad", "Si el Perú entra, y con qué figura de postulante."),
        ("Socio", "Si exige una entidad del país que aporta el dinero."),
        ("Contrapartida", "Qué pide a cambio, en qué moneda y en qué momento."),
    ],
)



# ==========================================================================
# CIERRE
# ==========================================================================

RESUMEN = envolver(
    cabecera("Cierre",
             "Cinco puntos establecidos sobre dónde buscar el dinero de un proyecto",
             "i-check")
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}Queda establecido</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>PROCIENCIA y ProInnóvate son dos de once ventanillas públicas; las otras nueve están en agro, pesca, empleo, turismo y cultura.</li>
\t\t\t\t\t\t\t<li>La forma del instrumento decide si el dinero llega antes o después del gasto, y eso decide quién financia la ejecución entretanto.</li>
\t\t\t\t\t\t\t<li>La contrapartida se calcula sobre el costo total y no sobre el monto solicitado, y se compromete por escrito antes de postular.</li>
\t\t\t\t\t\t\t<li>Fuera del Estado hay premios, filantropía, embajadas, banca multilateral y fondos climáticos, cada uno con su figura admitida.</li>
\t\t\t\t\t\t\t<li>No todo el financiamiento es caja: el ensayo, el laboratorio y las horas de personal se valorizan y cuentan como aporte.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-arrow-right")}Lo que se lleva a la sesión 4</h3>
\t\t\t\t\t\t<p>La ventanilla que admite el proyecto, la contrapartida con su
\t\t\t\t\t\taportante y la lista de fondos de respaldo. Con el dinero
\t\t\t\t\t\tlocalizado, lo que falta es <b>el documento</b>: objetivos,
\t\t\t\t\t\tindicadores y supuestos que el evaluador puntúa.</p>
\t\t\t\t\t\t<p>La limitación que se arrastra: hay fondos identificados y
\t\t\t\t\t\ttodavía no está escrito con qué indicadores se demostrará que el
\t\t\t\t\t\tproyecto cumplió.</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_POLCTI, F_MAPEO, F_APCI)
)


def _grupo_glosario(rotulo, entradas, variante=""):
    """Un bloque del glosario por cada tema de la sesión."""
    v = f" gloss-group--{variante}" if variante else ""
    return (f'\t\t\t\t\t<section class="gloss-group{v}">\n'
            f'\t\t\t\t\t\t<h2 class="gloss-group__title">{rotulo}</h2>\n'
            + "\n".join(entradas)
            + "\n\t\t\t\t\t</section>")


GLOSARIO = envolver(
    cabecera("Cierre", "Doce términos para leer una convocatoria y una hoja de términos", "i-book")
    + "\n"
    + '\t\t\t\t<div class="glossary glossary--grouped" data-animate="fade-up">\n'
    + _grupo_glosario("Fondos públicos y su contrapartida", [
        termino("Contrapartida", "matching funds",
                "La parte del gasto que no cubre el fondo. En efectivo obliga a tener caja; valorizada se acredita con planilla y tarifario."),
        termino("Cofinanciamiento", "co-funding",
                "El porcentaje que aporta el fondo. Cuanto más baja, más deprisa crece lo que el postulante tiene que poner."),
        termino("Ventanilla", "funding window",
                "El instrumento concreto al que se postula, con su entidad admitida, su tramo de madurez y su contrapartida."),
        termino("Admisibilidad", "eligibility",
                "Filtro previo a la evaluación técnica: si la entidad o el tramo no encajan, la propuesta no se lee."),
        termino("No reembolsable", "grant",
                "Dinero que no se devuelve. Se rinde con comprobante y se pierde si el gasto no corresponde a lo aprobado."),
        termino("Aporte en especie", "in-kind contribution",
                "Equipamiento, ensayos, horas y espacio valorizados. Cuenta como contrapartida si lleva su tarifario y su carta."),
    ])
    + _grupo_glosario("Dinero privado e internacional", [
        termino("Ticket", "ticket size",
                "El monto que un inversor pone en una sola operación. Ordena a quién tiene sentido acudir en cada etapa."),
        termino("Participación", "equity",
                "La parte de la empresa que se entrega a cambio del capital. Un premio no la pide; una aceleradora casi siempre sí."),
        termino("Cohorte", "cohort",
                "El grupo que entra junto a una aceleradora, con fecha de inicio y de cierre. Separa a la aceleradora de la incubadora."),
        termino("Entidad acreditada", "accredited entity",
                "La organización por la que un fondo internacional canaliza su dinero. Al Green Climate Fund no se postula directo."),
        termino("Elegibilidad de país", "country eligibility",
                "Si el Perú entra en esa convocatoria y con qué figura. Se comprueba antes de escribir una sola línea."),
        termino("Consorcio", "consortium",
                "Varias entidades postulando juntas. Es la vía habitual de entrada a los programas marco europeos."),
    ], variante="b")
    + '\t\t\t\t</div>'
    + "\n"
    + fuente_pie(F_POLCTI, F_MAPEO, F_APCI)
)


REFERENCIAS = envolver(
    cabecera("Cierre", "Las siete fuentes de la sesión, con su enlace y su vía de acceso", "i-quote")
    + "\n"
    + tabla(
        ["Fuente", "Sirve a", "Dónde está"],
        [
            ["CONCYTEC (2024). <i>Política Nacional de CTI al 2030</i>",
             "Presupuesto público de CTI, instrumentos por sector y Ley 30309",
             '<a href="https://www.gob.pe/institucion/pcm/normas-legales/6967622-093-2025-pcm">gob.pe/institucion/pcm/normas-legales/6967622</a>'],
            ["ProInnóvate y StartUp Perú",
             "Capital semilla, desarrollo tecnológico y validación con empresa",
             '<a href="https://startup.proinnovate.gob.pe">startup.proinnovate.gob.pe</a> · <a href="https://proinnovate.gob.pe">proinnovate.gob.pe</a>'],
            ["PROCIENCIA · CONCYTEC",
             "Concursos de investigación y programas de becas",
             '<a href="https://prociencia.gob.pe">prociencia.gob.pe</a>'],
            ["Informe de mapeo de fondos concursables, programa Ágora Perú (FOAL, 2024)",
             "Premios, filantropía y fondos de embajada que convocan en el país",
             '<a href="https://www.foal.es/sites/default/files/noticias/files/Informe_fondos_concursables.pdf">foal.es · informe en PDF</a>'],
            ["APCI (2021). <i>Situación y Tendencias de la Cooperación Técnica Internacional en el Perú</i>",
             "Cuánta cooperación entra al país, de dónde viene y a qué se destina",
             '<a href="https://www.gob.pe/institucion/apci/colecciones/859-situacion-y-tendencias-de-la-cti-en-el-peru">gob.pe/apci · colección de informes</a>'],
            ["Green Climate Fund · registro de entidades acreditadas",
             "Por qué puerta entra al Perú el dinero del principal fondo climático",
             '<a href="https://www.greenclimate.fund/partners/accredited-entities/profonanpe">greenclimate.fund · ficha de Profonanpe</a>'],
            ["Portales de los fondos sectoriales del Estado",
             "PROCOMPITE, AGROIDEAS, PNIPA, FONDOEMPLEO, Turismo Emprende y Cultura",
             '<a href="https://www.gob.pe/agroideas">gob.pe/agroideas</a> · <a href="https://pnipa.gob.pe">pnipa.gob.pe</a> · <a href="https://fondoempleo.com.pe">fondoempleo.com.pe</a>'],
        ],
        titulo="Fuentes de la sesión y dirección en la que se consultan",
    )
)

FONDO_PROCIENCIA = envolver(
    cabecera("01 · Fondos del Estado", "PROCIENCIA: concursos de investigación y programas de becas", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="CONCYTEC · Programa Nacional de Investigación Científica y Estudios Avanzados",
        financia=[
            "Proyectos de investigación básica y aplicada con pregunta abierta",
            "Becas de maestría y doctorado, y estancias de investigación",
            "Equipamiento científico y publicación de resultados",
        ],
        quien="Entidades de investigación registradas, con el investigador principal inscrito en el RENACYT. La persona natural postula solo a becas.",
        datos=[
            ("Modalidad", "No reembolsable, por concurso nacional"),
            ("Desembolso", "Por tramos, contra informe técnico aprobado"),
            ("Contrapartida", "Casi toda valorizada: horas de investigador y laboratorio"),
            ("Cierra con", "Publicación, tesis o prueba de concepto documentada"),
        ],
        sitio="prociencia.gob.pe",
        nota="Los montos y las líneas temáticas cambian en cada concurso: se leen en las bases vigentes.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_LEY_30309 = envolver(
    cabecera("01 · Fondos del Estado", "Ley 30309: deducción adicional del impuesto sobre el gasto en I+D+i", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="CONCYTEC califica · SUNAT aplica la deducción",
        financia=[
            "Gasto ya ejecutado en investigación, desarrollo tecnológico e innovación",
            "Personal, materiales, ensayos y servicios del proyecto calificado",
            "No adelanta dinero: devuelve parte por la vía tributaria",
        ],
        quien="Contribuyentes del impuesto a la renta de tercera categoría, es decir empresas formales con utilidad sobre la que deducir.",
        datos=[
            ("Modalidad", "Beneficio tributario sobre gasto ya realizado"),
            ("Cuándo llega", "Con la declaración anual del impuesto"),
            ("Serie 2016-2022", "352 proyectos presentados y 136 aprobados, 39 % acumulado"),
            ("Aprobación", "Del 11 % en 2016 al 53 % en 2022, sin que la ley cambiara"),
        ],
        sitio="gob.pe/concytec",
        nota="No sirve como contrapartida: la contrapartida se aporta durante la ejecución y esto llega después.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_STARTUP_PERU = envolver(
    cabecera("01 · Fondos del Estado", "StartUp Perú: capital semilla para emprendimientos innovadores", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="ProInnóvate · Ministerio de la Producción",
        financia=[
            "Validación temprana de un producto mínimo viable con tracción",
            "Escalamiento de emprendimientos dinámicos ya con ventas",
            "Acompañamiento obligatorio de una incubadora de la red del programa",
        ],
        quien="Empresas formales jóvenes. El líder emprendedor y al menos la mitad del equipo deben ser peruanos o residentes, y el mérito innovador se exige al menos a nivel de país.",
        datos=[
            ("Monto", "Hasta S/ 150 000 en la categoría de emprendimientos dinámicos"),
            ("Modalidad", "Recursos no reembolsables, por concurso"),
            ("Categorías", "Emprendimientos innovadores y emprendimientos dinámicos"),
            ("Ejecución", "Hasta ocho meses en la categoría de validación"),
            ("Incluye", "Un monto fijo destinado a la incubadora que acompaña"),
        ],
        sitio="startup.proinnovate.gob.pe",
        nota="El importe cambia en cada edición. Consultado en agosto de 2026, la convocatoria vigente es la 13G.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_PROINNOVATE_EMPRESA = envolver(
    cabecera("01 · Fondos del Estado", "ProInnóvate: desarrollo tecnológico y validación con empresa", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="ProInnóvate · Ministerio de la Producción",
        financia=[
            "Desarrollo de un prototipo hasta producto con destinatario identificado",
            "Validación en entorno real y escalamiento productivo",
            "Proyectos de I+D de empresa con entidad de investigación asociada",
        ],
        quien="Empresa formal, sola o con universidad o instituto asociado. Sin empresa constituida no hay postulación en esta línea.",
        datos=[
            ("Modalidad", "Subvención con cofinanciamiento, por concurso"),
            ("Desembolso", "Por tramos, contra hito verificado"),
            ("Contrapartida", "Obligatoria, con una parte en efectivo"),
            ("Cierra con", "Prototipo validado, producto o venta acreditada"),
        ],
        sitio="proinnovate.gob.pe",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_AGROIDEAS = envolver(
    cabecera("01 · Fondos del Estado", "AGROIDEAS: reconversión productiva y asociatividad agraria", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Programa de Compensaciones para la Competitividad · Midagri",
        financia=[
            "Adopción de tecnología agraria: maquinaria, riego y material genético",
            "Reconversión de cultivos hacia productos de mayor valor",
            "Gestión y fortalecimiento de la propia organización agraria",
        ],
        quien="Organizaciones agrarias con personería jurídica y productores asociados. No admite al productor individual.",
        datos=[
            ("Modalidad", "Incentivo no reembolsable, con plan de negocio aprobado"),
            ("Componentes", "Gestión empresarial, adopción de tecnología y reconversión"),
            ("Contrapartida", "Aporte de la organización, en efectivo o valorizado"),
            ("Cuándo abre", "Ventanilla del programa, con evaluación por etapas"),
        ],
        sitio="gob.pe/agroideas",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_PNIPA = envolver(
    cabecera("01 · Fondos del Estado", "PNIPA: innovación en pesca y acuicultura", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Programa Nacional de Innovación en Pesca y Acuicultura · Midagri",
        financia=[
            "Subproyectos de investigación adaptativa en pesca y acuicultura",
            "Adopción de tecnología en unidades productivas del sector",
            "Servicios de extensión y asesoría a productores",
        ],
        quien="Empresas, asociaciones de productores, universidades e institutos de investigación del sector pesquero y acuícola.",
        datos=[
            ("Modalidad", "Fondos concursables no reembolsables"),
            ("Líneas", "Investigación, desarrollo de mercado y servicios de extensión"),
            ("Contrapartida", "Exigida al postulante y a sus entidades asociadas"),
            ("Alcance", "Nacional, con énfasis en la Amazonía y la costa"),
        ],
        sitio="pnipa.gob.pe",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_FONDOEMPLEO = envolver(
    cabecera("01 · Fondos del Estado", "FONDOEMPLEO: proyectos de empleo y capacitación laboral", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Fondo Nacional de Capacitación Laboral y de Promoción del Empleo",
        financia=[
            "Proyectos que generan empleo sostenible en una zona determinada",
            "Capacitación laboral y formación técnica de trabajadores",
            "Emprendimientos productivos con acompañamiento",
        ],
        quien="Entidades públicas y privadas sin fines de lucro, gobiernos locales y organizaciones de productores.",
        datos=[
            ("Modalidad", "Concurso público de proyectos, no reembolsable"),
            ("Origen del dinero", "Aporte de empresas por utilidades no distribuidas"),
            ("Contrapartida", "Requerida a la entidad ejecutora"),
            ("Cuándo abre", "Concurso anual, con bases publicadas por convocatoria"),
        ],
        sitio="fondoempleo.com.pe",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_TURISMO_EMPRENDE = envolver(
    cabecera("01 · Fondos del Estado", "Turismo Emprende: emprendimientos de servicios turísticos", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Ministerio de Comercio Exterior y Turismo",
        financia=[
            "Creación de emprendimientos que prestan servicios turísticos",
            "Mejora y ampliación de un servicio turístico ya en marcha",
            "Equipamiento y acondicionamiento del establecimiento",
            "Promoción y difusión del servicio que se pone en marcha",
        ],
        quien="Personas naturales con negocio y personas jurídicas del rubro turístico, con actividad registrada.",
        datos=[
            ("Monto", "Hasta S/ 60 000 por unidad productiva y S/ 120 000 por organización comunitaria"),
            ("Modalidad", "Aporte no reembolsable por concurso"),
            ("Ámbito", "Nacional, con prioridad en destinos turísticos declarados"),
            ("Contrapartida", "Aporte del beneficiario sobre el costo total"),
            ("Cuándo abre", "Convocatoria del ministerio, por edición"),
            ("Qué no cubre", "Compra de terreno ni deuda anterior al proyecto"),
        ],
        sitio="gob.pe/mincetur",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_CULTURA = envolver(
    cabecera("01 · Fondos del Estado", "Estímulos económicos del Ministerio de Cultura", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Ministerio de Cultura · Dirección de Artes y Dirección del Libro",
        financia=[
            "Producción de artes escénicas, visuales, danza y música en vivo",
            "Festivales, ferias y circulación nacional de las artes",
            "Publicación de libros, bibliotecas comunales y fomento de la lectura",
        ],
        quien="Personas naturales y jurídicas del sector cultural, incluidos colectivos y organizaciones comunales.",
        datos=[
            ("Modalidad", "Estímulo económico no reembolsable, por concurso"),
            ("Convocatorias", "Varias líneas independientes, cada una con sus bases"),
            ("Contrapartida", "Según la línea; algunas no la exigen"),
            ("Cuándo abre", "Calendario anual publicado al inicio del año"),
        ],
        sitio="gob.pe/cultura",
        nota="Es la vía para el componente de difusión de un proyecto de I+D+i con salida cultural o educativa.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_RED_CITE = envolver(
    cabecera("01 · Fondos del Estado", "Red CITE del ITP: servicios tecnológicos que se contratan", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Instituto Tecnológico de la Producción",
        financia=[
            "No entrega dinero: presta el ensayo, la caracterización y la planta piloto",
            "Asistencia técnica y capacitación especializada por cadena productiva",
            "Uso de laboratorio y equipamiento que el proyecto no tiene",
        ],
        quien="Cualquier empresa, asociación o grupo de investigación que contrate el servicio. No hay concurso ni postulación.",
        datos=[
            ("Modalidad", "Servicio tecnológico pagado, no subvención"),
            ("Cobertura", "46 centros en el país, dato de 2024"),
            ("Para qué sirve", "Acredita el paso al entorno relevante de la escala TRL"),
            ("Cuándo", "Todo el año, según disponibilidad del centro"),
        ],
        sitio="gob.pe/itp",
        nota="Es financiamiento en especie: lo que se ahorra el proyecto por no comprar el equipo ni montar el laboratorio.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)

FONDO_LEY_30309 = envolver(
    cabecera("01 · Fondos del Estado", "Ley 30309: deducción adicional del impuesto sobre el gasto en I+D+i", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="CONCYTEC califica · SUNAT aplica la deducción",
        financia=[
            "Gasto ya ejecutado en investigación, desarrollo tecnológico e innovación",
            "Personal, materiales, ensayos y servicios del proyecto calificado",
            "No adelanta dinero: devuelve parte por la vía tributaria",
        ],
        quien="Contribuyentes del impuesto a la renta de tercera categoría, es decir empresas formales con utilidad sobre la que deducir.",
        datos=[
            ("Modalidad", "Beneficio tributario sobre gasto ya realizado"),
            ("Cuándo llega", "Con la declaración anual del impuesto"),
            ("Serie 2016-2022", "352 proyectos presentados y 136 aprobados, 39 % acumulado"),
            ("Aprobación", "Del 11 % en 2016 al 53 % en 2022, sin que la ley cambiara"),
        ],
        sitio="gob.pe/concytec",
        nota="No sirve como contrapartida: la contrapartida se aporta durante la ejecución y esto llega después.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_PROINNOVATE, F_PROCIENCIA)
)


F02_PREINCUBACION = envolver(
    cabecera("02 · Dónde más hay dinero", "Preincubación e incubación: acompañamiento antes que dinero", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Incubadoras universitarias y privadas de la red de ProInnóvate",
        financia=[
            "No entrega capital: da espacio, mentoría, formación y red de contactos",
            "Servicios compartidos que el emprendimiento no puede pagar solo",
            "En algunos programas, un monto pequeño de arranque",
        ],
        quien="Equipos con una idea validada o un prototipo, con o sin empresa constituida según el programa.",
        datos=[
            ("Qué pide a cambio", "Dedicación del equipo; algunas piden participación"),
            ("Duración", "Sin plazo fijo: se entra y se sale caso por caso"),
            ("Cuándo sirve", "Antes de tener ventas, para dejar el proyecto postulable"),
            ("Cómo se llega", "StartUp Perú paga la incubadora que acompaña al ganador"),
        ],
        sitio="startup.proinnovate.gob.pe",
        nota="Aquí el valor no es el dinero: es que el proyecto quede en condiciones de postular a lo que sí lo da.",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_ACELERADORA = envolver(
    cabecera("02 · Dónde más hay dinero", "Aceleradoras: cohorte cerrada, plazo corto y capital de entrada", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Programas privados, algunos con respaldo público",
        financia=[
            "Un capital de entrada a cambio de participación en la empresa",
            "Programa formativo intensivo con mentores y sesiones fijas",
            "Acceso a una rueda de inversores al cerrar la cohorte",
            "Servicios y créditos de proveedores negociados para toda la cohorte",
        ],
        quien="Empresas ya constituidas con producto en el mercado y algo de tracción. Se entra por cohorte, con fecha de inicio y de cierre.",
        datos=[
            ("Qué pide a cambio", "Participación accionaria, casi siempre"),
            ("Duración", "Nueve meses o menos, con fecha de salida fijada"),
            ("Diferencia con la incubadora", "La cohorte y el plazo, no el tipo de servicio"),
            ("Riesgo", "El programa no garantiza levantar capital después"),
            ("Cómo se entra", "Postulación abierta con fecha, no por presentación"),
        ],
        sitio="startup.proinnovate.gob.pe",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_ANGELES = envolver(
    cabecera("02 · Dónde más hay dinero", "Inversores ángeles: patrimonio propio en etapa temprana", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Personas naturales, solas o agrupadas en redes",
        financia=[
            "Capital propio a cambio de participación, en etapa temprana",
            "Suelen acompañar con contactos y con un papel de consejo",
            "Tickets pequeños comparados con un fondo, y decisión rápida",
            "A veces entran varios ángeles juntos en la misma ronda",
        ],
        quien="Empresas constituidas con producto y primeras ventas. El ángel decide sobre el emprendedor antes que sobre el producto.",
        datos=[
            ("Qué pide a cambio", "Participación y, con frecuencia, un puesto de consejo"),
            ("Aporte propio", "Casi siempre exige que el fundador ponga dinero suyo"),
            ("Cómo se llega", "Por presentación de alguien de su red, rara vez en frío"),
            ("Qué prepara antes", "Aporte propio acreditado y avance demostrable"),
            ("Motivo de rechazo", "La desconfianza en el emprendedor, antes que el producto"),
        ],
        sitio="lavca.org",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_CAPITAL_RIESGO = envolver(
    cabecera("02 · Dónde más hay dinero", "Capital de riesgo: fondo con tesis, plazo de salida y consejo", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Sociedades gestoras de fondos, con dinero de terceros",
        financia=[
            "Rondas de crecimiento a cambio de participación significativa",
            "Escalamiento comercial, no investigación ni prototipo",
            "Rondas sucesivas si la empresa cumple los hitos pactados",
        ],
        quien="Empresas con modelo repetible y crecimiento demostrable. La etapa semilla y temprana es la que suele seguir a una ronda de ángeles.",
        datos=[
            ("Qué pide a cambio", "Participación, puesto en el consejo y derechos de salida"),
            ("Plazo", "El fondo tiene fecha de cierre y necesita vender su parte"),
            ("Qué mira", "Tamaño del mercado y capacidad de crecer, no la tecnología sola"),
            ("Dónde se consulta", "Bases de datos de operaciones por país y sector"),
        ],
        sitio="dealroom.co",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_KUNAN = envolver(
    cabecera("02 · Dónde más hay dinero", "Desafío Kunan: el premio de emprendimiento social del país", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Asociación Kunan, con categorías impulsadas por empresas",
        financia=[
            "Premio en efectivo al emprendimiento social ganador de cada categoría",
            "Exposición pública y acceso a la red de aliados del premio",
            "Acompañamiento según la categoría y el auspiciador",
        ],
        quien="Emprendimientos sociales y ambientales del país. Algunas categorías exigen empresa constituida, tres años de operación y ventas mínimas.",
        datos=[
            ("Modalidad", "Premio anual por concurso, no reembolsable"),
            ("Categorías", "Varias, cada una con su auspiciador y sus requisitos"),
            ("Qué pide a cambio", "Nada de participación: es premio, no inversión"),
            ("Cuándo abre", "Convocatoria anual en su propio sitio"),
        ],
        sitio="desafio.kunan.org",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_WIESE = envolver(
    cabecera("02 · Dónde más hay dinero", "Fondo Emprendedor de la Fundación Wiese", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Fundación Wiese · filantropía empresarial peruana",
        financia=[
            "Financiamiento directo a la empresa social seleccionada",
            "Asesoría estratégica profesional durante todo el programa",
            "Capacitación diseñada a medida del portafolio",
        ],
        quien="Entidad privada con personería jurídica constituida en el Perú, con o sin fin de lucro, que reporte al menos S/ 25 000 de ingresos anuales.",
        datos=[
            ("Monto", "S/ 150 000 por empresa social seleccionada"),
            ("Duración", "18 meses de acompañamiento"),
            ("Periodicidad", "Convoca cada tres años, no todos los años"),
            ("Qué busca", "Autosostenibilidad por mecanismos de mercado"),
        ],
        sitio="fundacionwiese.org",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_DAP_AUSTRALIA = envolver(
    cabecera("02 · Dónde más hay dinero", "Direct Aid Program: fondos de la Embajada de Australia", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Gobierno de Australia · Embajada en Lima",
        financia=[
            "Proyectos de pequeña escala de desarrollo inclusivo en Perú y Bolivia",
            "Mejora de la calidad de vida de comunidades locales",
            "Áreas prioritarias declaradas cada año, entre ellas igualdad de género",
        ],
        quien="Organizaciones sin fines de lucro constituidas y activas con al menos dos años de operación: ONG, asociaciones, academia, cooperativas.",
        datos=[
            ("Monto", "Hasta 20 000 dólares australianos"),
            ("Modalidad", "Fondo concursable de embajada, no reembolsable"),
            ("Ámbito", "Perú y Bolivia, con sede u operación en alguno de los dos"),
            ("Cuándo abre", "Convocatoria anual de la embajada"),
        ],
        sitio="peru.embassy.gov.au",
        nota="Casi todas las embajadas tienen un programa equivalente: es la familia entera, no un caso suelto.",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_IAF = envolver(
    cabecera("02 · Dónde más hay dinero", "Inter American Foundation: donaciones a organizaciones de base", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Fundación Interamericana · organismo autónomo del gobierno de EE. UU.",
        financia=[
            "Soluciones de autoayuda propuestas por grupos de base",
            "Alianzas entre organizaciones comunitarias, empresas y gobiernos locales",
            "Proyectos dirigidos por la propia organización local, no por un intermediario",
        ],
        quien="Organizaciones de base y ONG de América Latina y el Caribe, con liderazgo local del proyecto.",
        datos=[
            ("Modalidad", "Donación por convocatoria anual"),
            ("Qué valora", "Que la idea y la ejecución nazcan de la propia comunidad"),
            ("Qué pide a cambio", "Reporte de resultados, sin participación"),
            ("Ámbito", "Toda la región, con concurso abierto"),
        ],
        sitio="iaf.gov",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_UNION_EUROPEA = envolver(
    cabecera("02 · Dónde más hay dinero", "Delegación de la Unión Europea y los programas marco", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Delegación de la UE en el Perú y Comisión Europea",
        financia=[
            "Ayudas de la Delegación a proyectos en el país, por licitación o subvención",
            "Participación peruana en programas marco de investigación europeos",
            "Consorcios con socios europeos, que es la vía habitual de entrada",
        ],
        quien="Entidades peruanas que cumplan las condiciones de elegibilidad de cada convocatoria; en los programas marco, casi siempre dentro de un consorcio.",
        datos=[
            ("Modalidad", "Subvención con cofinanciamiento y reporte exigente"),
            ("Requisito habitual", "Socio en un país miembro para formar consorcio"),
            ("Dónde se busca", "El portal único de convocatorias de la Comisión"),
            ("Qué revisar primero", "Si el Perú figura como país elegible en esa línea"),
        ],
        sitio="ec.europa.eu/info/funding-tenders",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_BID = envolver(
    cabecera("02 · Dónde más hay dinero", "Banca multilateral: BID y Banco Mundial", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Banco Interamericano de Desarrollo y Banco Mundial",
        financia=[
            "Cooperación técnica no reembolsable ligada a operaciones con el Estado",
            "Fondos temáticos y desafíos de innovación con convocatoria propia",
            "Estudios y asistencia técnica que preceden a un préstamo",
        ],
        quien="En general el Estado es el prestatario; a las convocatorias temáticas postulan empresas, universidades y organizaciones.",
        datos=[
            ("Modalidad", "Préstamo al Estado, o cooperación técnica no reembolsable"),
            ("Vía de acceso", "Casi siempre a través de una entidad pública ejecutora"),
            ("Qué publica", "Operaciones por país y sector, con su documentación"),
            ("Uso indirecto", "Sus informes sostienen el diagnóstico de una propuesta"),
        ],
        sitio="iadb.org",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_CLIMA = envolver(
    cabecera("02 · Dónde más hay dinero", "Green Climate Fund: se entra por una entidad acreditada", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Green Climate Fund · con Profonanpe como entidad peruana acreditada",
        financia=[
            "Adaptación y mitigación del cambio climático a escala de programa",
            "Conservación de áreas protegidas y ecosistemas, con horizonte largo",
            "Fortalecimiento de la entidad que ejecuta, además del proyecto",
        ],
        quien="El proyecto no postula al fondo: postula a través de una entidad acreditada, que es la que responde ante el fondo.",
        datos=[
            ("Acceso peruano", "Profonanpe, acceso directo nacional, categoría micro"),
            ("Acreditación", "Desde 2015, reacreditada en noviembre de 2022"),
            ("Instrumentos", "Habilitada para otorgar donaciones y gestionar proyectos"),
            ("Escala", "Programas plurianuales, no proyectos de un año"),
        ],
        sitio="greenclimate.fund/partners/accredited-entities/profonanpe",
        nota="No está comprobado que sea la única entidad peruana acreditada: eso lo dice una fuente secundaria.",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

F02_ESPECIE = envolver(
    cabecera("02 · Dónde más hay dinero", "Financiamiento en especie: lo que no llega como dinero", "i-fund")
    + "\n"
    + ficha_fondo(
        operador="Centros tecnológicos, universidades, empresas y programas de nube",
        financia=[
            "Uso de laboratorio, equipamiento y planta piloto que el proyecto no tiene",
            "Ensayos y caracterizaciones que acreditan el nivel de madurez",
            "Horas de personal técnico y crédito de cómputo en la nube",
        ],
        quien="Cualquier proyecto que sepa valorizar el aporte y documentarlo con el tarifario o la planilla que lo respalda.",
        datos=[
            ("Por qué cuenta", "Se declara como contrapartida valorizada en la propuesta"),
            ("Cómo se acredita", "Tarifario del centro, planilla o carta de compromiso"),
            ("Dónde se consigue", "Red CITE del ITP, laboratorios universitarios, convenios"),
            ("Error frecuente", "No pedirlo por escrito antes de presentar la propuesta"),
        ],
        sitio="gob.pe/itp",
        nota="Es la vía más accesible y la que menos se usa: no compite por caja, compite por convenio.",
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

MAPA_ETAPA_FONDO = envolver(
    cabecera("02 · Dónde más hay dinero",
             "Qué familia de fondos corresponde a cada momento del proyecto",
             "i-ladder")
    + "\n"
    + figura("s3-etapa-fondo",
             "Familias de financiamiento por momento del proyecto",
             "Ninguna familia sirve en todas las etapas: la que financia una idea no financia una escala.")
    + "\n"
    + criterio(
        "Postular fuera de etapa es la causa más común de descarte. Un premio no "
        "sostiene un programa plurianual y un fondo climático no financia un prototipo "
        "de laboratorio."
    )
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

QUE_PIDE_CADA_UNO = envolver(
    cabecera("02 · Dónde más hay dinero",
             "Qué pide a cambio cada familia, de no pedir nada a pedir control",
             "i-scale")
    + "\n"
    + figura("s3-que-pide",
             "Contraprestación exigida por familia de financiamiento",
             "El premio no pide nada y el capital de riesgo pide participación, consejo y una salida.")
    + "\n"
    + criterio(
        "Antes que el monto se mira la contraprestación: hay dinero que el proyecto no "
        "puede aceptar. Ceder participación con la titularidad del resultado sin "
        "resolver bloquea la operación entera."
    )
    + "\n"
    + fuente_pie(F_MAPEO)
)

CALENDARIO_CONVOCATORIAS = envolver(
    cabecera("02 · Dónde más hay dinero",
             "En qué meses del año abre cada familia de convocatorias",
             "i-calendar")
    + "\n"
    + figura("s3-calendario-fondos",
             "Temporada habitual de apertura por familia de convocante",
             "La estacionalidad sigue el año fiscal, el curso académico y el calendario de las cumbres climáticas.")
    + "\n"
    + en_la_practica(
        "El primer trimestre se dedica a preparar, no a postular: personería, estados "
        "financieros y cartas de compromiso. Después, con la convocatoria abierta, "
        "ya no da tiempo a conseguirlos."
    )
    + "\n"
    + fuente_pie(F_MAPEO)
)

COOPERACION_ORIGEN = envolver(
    cabecera("02 · Dónde más hay dinero",
             "De dónde viene la cooperación internacional que entra al Perú",
             "i-globe")
    + "\n"
    + figura("s3-cooperacion-origen",
             "Cooperación técnica internacional ejecutada en el Perú por modalidad, 2021",
             "Dos tercios llegan por acuerdo entre gobiernos; la vía multilateral es la más pequeña de las tres.")
    + "\n"
    + dato_clave(
        "En 2021 se ejecutaron <b>472,1 millones de dólares</b>, el pico de la década. "
        "El 71 % fue cooperación oficial y el 29 % no gubernamental."
    )
    + "\n"
    + fuente_pie(F_APCI)
)

# El segundo simulador de la sesión. Reemplaza al tamizaje del inversor ángel,
# que se retiró con la evidencia extranjera. Recorre el catálogo entero en vez
# de una sola familia, que es lo que la sesión enseña ahora.
CATALOGO_JS = """\t\t<script type="module">
\t\t\t// Tres condiciones deciden qué familias admiten el proyecto: la etapa,
\t\t\t// la figura con la que se postula y si el equipo puede ceder
\t\t\t// participación. Cada control cambia el veredicto de extremo a extremo
\t\t\t// (METODOLOGIA.md §3.3):
\t\t\t//   Etapa 1 a 5 con empresa y cediendo: de tres familias a cinco.
\t\t\t//   Figura, en etapa 3 cediendo: la empresa tiene seis y la persona dos.
\t\t\t//   Ceder participación, con empresa en etapa 4: de cuatro a siete.
\t\t\tconst FAMILIAS = [
\t\t\t\t{ n: "Premios y concursos", e: [1, 3], part: false,
\t\t\t\t  f: ["empresa", "persona", "asociacion"],
\t\t\t\t  nota: "El premio no pide participación ni contrapartida: es la puerta más accesible y la que menos se usa." },
\t\t\t\t{ n: "Preincubación e incubación", e: [1, 3], part: false,
\t\t\t\t  f: ["empresa", "persona", "asociacion"],
\t\t\t\t  nota: "No da capital: deja el proyecto en condiciones de postular a lo que sí lo da." },
\t\t\t\t{ n: "Fondos públicos sectoriales", e: [2, 4], part: false,
\t\t\t\t  f: ["empresa", "asociacion"],
\t\t\t\t  nota: "Agro, pesca, empleo, turismo y cultura tienen ventanilla propia, y casi nadie las mira." },
\t\t\t\t{ n: "StartUp Perú y ProInnóvate", e: [2, 4], part: false,
\t\t\t\t  f: ["empresa"],
\t\t\t\t  nota: "Exige empresa formal: sin RUC no hay postulación en esta vía." },
\t\t\t\t{ n: "Aceleradoras", e: [3, 4], part: true,
\t\t\t\t  f: ["empresa"],
\t\t\t\t  nota: "Cohorte cerrada y participación accionaria a cambio del capital de entrada." },
\t\t\t\t{ n: "Inversores ángeles", e: [3, 5], part: true,
\t\t\t\t  f: ["empresa"],
\t\t\t\t  nota: "Decide sobre el emprendedor antes que sobre el producto, y exige aporte propio." },
\t\t\t\t{ n: "Capital de riesgo", e: [4, 5], part: true,
\t\t\t\t  f: ["empresa"],
\t\t\t\t  nota: "Pide participación, puesto en el consejo y una salida con fecha." },
\t\t\t\t{ n: "Cooperación y filantropía", e: [2, 5], part: false,
\t\t\t\t  f: ["asociacion", "universidad"],
\t\t\t\t  nota: "Embajadas, fundaciones y organismos: piden reporte, no participación." },
\t\t\t\t{ n: "Fondos climáticos y multilaterales", e: [4, 5], part: false,
\t\t\t\t  f: ["asociacion", "universidad"],
\t\t\t\t  nota: "Se entra por una entidad acreditada y con horizonte plurianual." },
\t\t\t];
\t\t\tconst NOMBRES = { empresa: "una empresa formal", persona: "una persona sin empresa",
\t\t\t\tasociacion: "una asociación", universidad: "una universidad" };
\t\t\tconst ETAPAS = ["", "idea", "prototipo", "producto con usuario", "ventas", "escala"];

\t\t\tconst raiz = document.querySelector('[data-sim="catalogo"]');
\t\t\tconst mando = raiz.querySelector("#c-etapa");
\t\t\tconst nivel = raiz.querySelector("#c-nivel");
\t\t\tconst veredicto = raiz.querySelector("#c-veredicto");
\t\t\tconst detalle = raiz.querySelector("#c-detalle");
\t\t\tconst admite = raiz.querySelector("#c-admite");
\t\t\tconst fuera = raiz.querySelector("#c-fuera");
\t\t\tconst ceder = raiz.querySelector("#c-ceder");
\t\t\tconst botones = [...raiz.querySelectorAll(".picker__btn")];
\t\t\tlet figura = "empresa";

\t\t\tfunction pintar() {
\t\t\t\tconst e = Number(mando.value);
\t\t\t\tconst cede = ceder.checked;
\t\t\t\tnivel.textContent = "Etapa " + e + " · " + ETAPAS[e];
\t\t\t\tconst ok = [], no = [];
\t\t\t\tfor (const F of FAMILIAS) {
\t\t\t\t\tif (e < F.e[0] || e > F.e[1]) { no.push({ F, r: "fuera de etapa" }); continue; }
\t\t\t\t\tif (!F.f.includes(figura)) { no.push({ F, r: "no admite esa figura" }); continue; }
\t\t\t\t\tif (F.part && !cede) { no.push({ F, r: "exige ceder participación" }); continue; }
\t\t\t\t\tok.push(F);
\t\t\t\t}
\t\t\t\tconst peso = { "exige ceder participación": 0, "no admite esa figura": 1 };
\t\t\t\tno.sort((a, b) => (peso[a.r] ?? 2) - (peso[b.r] ?? 2));
\t\t\t\tadmite.innerHTML = ok.length
\t\t\t\t\t? ok.map((F) => "<li>" + F.n + "</li>").join("")
\t\t\t\t\t: "<li>Ninguna de las nueve familias con esta combinación.</li>";
\t\t\t\tfuera.innerHTML = no.slice(0, 4)
\t\t\t\t\t.map((x) => "<li>" + x.F.n + " · " + x.r + "</li>").join("");
\t\t\t\tif (ok.length === 0) {
\t\t\t\t\tveredicto.textContent = "Ninguna familia admite";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "Con " + NOMBRES[figura] + " en etapa de " + ETAPAS[e]
\t\t\t\t\t\t+ ", ninguna familia del catálogo encaja. La salida es cambiar de figura o buscar la etapa anterior.";
\t\t\t\t} else {
\t\t\t\t\tveredicto.textContent = ok.length === 1
\t\t\t\t\t\t? "Una familia admite" : ok.length + " familias admiten";
\t\t\t\t\tveredicto.dataset.estado = ok.length === 1 ? "warn" : "ok";
\t\t\t\t\tdetalle.textContent = ok[0].nota;
\t\t\t\t}
\t\t\t}
\t\t\tfor (const b of botones) {
\t\t\t\tb.addEventListener("click", () => {
\t\t\t\t\tfigura = b.dataset.figura;
\t\t\t\t\tfor (const o of botones) o.classList.toggle("is-on", o === b);
\t\t\t\t\tpintar();
\t\t\t\t});
\t\t\t}
\t\t\tmando.addEventListener("input", pintar);
\t\t\tceder.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


CATALOGO_SIM = envolver(
    cabecera("02 · Dónde más hay dinero",
             "Qué familias del catálogo admiten el proyecto según etapa y figura",
             "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="catalogo" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<label class="sim__label" for="c-etapa">Etapa del proyecto</label>
\t\t\t\t\t\t<input class="sim__range" id="c-etapa" type="range" min="1" max="5" step="1" value="3" />
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="c-nivel">Etapa 3</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="c-veredicto" data-estado="ok">Familias admisibles</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="picker">
\t\t\t\t\t\t\t<button class="picker__btn is-on" type="button" data-figura="empresa">Empresa</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="persona">Persona</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="asociacion">Asociación</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="universidad">Universidad</button>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="c-ceder" />
\t\t\t\t\t\t\t<span><b>El equipo puede ceder participación</b><span class="crit__help">Parte de la empresa a cambio del capital</span></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<p class="sim__what" id="c-detalle"></p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Familias que admiten</h3>
\t\t\t\t\t\t\t<ul id="c-admite"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Por qué quedan fuera</h3>
\t\t\t\t\t\t\t<ul id="c-fuera"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Con empresa en etapa de
\t\t\t\tventas, marcar que se puede ceder participación pasa de cuatro familias a siete.</p>"""
    + "\n"
    + fuente_pie(F_MAPEO, F_APCI)
)

RADIO_TIPOS = envolver(
    cabecera("02 · El mercado del financiamiento",
             "Qué tipo de oportunidad son las convocatorias que se publican en un año",
             "i-chart")
    + "\n"
    + figura("s3-tipos-convocatoria",
             "Reparto de 1 019 convocatorias por tipo de oportunidad, cierre en 2025",
             "La subvención es el formato dominante, pero el premio y la beca juntos igualan su peso.")
    + "\n"
    + dato_clave(
        "De más de <b>1 100 convocatorias</b> con campos completos, <b>1 019</b> "
        "cerraron entre enero y diciembre de 2025. El <b>75 %</b> declara un monto; "
        "el <b>25 %</b> restante no lo publica."
    )
    + "\n"
    + fuente_pie(F_RADIO)
)

RADIO_MONTOS = envolver(
    cabecera("02 · El mercado del financiamiento",
             "Cuánto dinero da de verdad cada tipo de convocatoria",
             "i-budget")
    + "\n"
    + figura("s3-rangos-monto",
             "Rango típico de monto por tipo de oportunidad, en dólares",
             "El techo de una subvención es diez veces el de un premio, y ahí está la decisión de a qué postular.")
    + "\n"
    + dato_clave(
        "Más del <b>60 %</b> de las oportunidades está en rangos pequeños y medianos "
        "y solo alrededor del <b>10 %</b> es de gran escala. Los montos altos vienen "
        "de organismos multilaterales, fondos europeos, embajadas y programas "
        "ambientales."
    )
    + "\n"
    + fuente_pie(F_RADIO)
)

RADIO_CALENDARIO = envolver(
    cabecera("02 · El mercado del financiamiento",
             "En qué meses del año se concentran los cierres de convocatoria",
             "i-calendar")
    + "\n"
    + figura("s3-estacionalidad-cierres",
             "Convocatorias que cierran en cada mes, sobre las 1 019 de 2025",
             "Septiembre concentra casi una de cada cinco; enero es el mes en que casi nada cierra.")
    + "\n"
    + en_la_practica(
        "El primer trimestre no se pierde: se dedica a reunir personería, estados "
        "financieros y cartas de compromiso. En septiembre ya no da tiempo a "
        "conseguirlos."
    )
    + "\n"
    + fuente_pie(F_RADIO)
)

RADIO_TEMAS = envolver(
    cabecera("02 · El mercado del financiamiento",
             "Qué temas concentran las convocatorias y cuáles emergen",
             "i-globe")
    + "\n"
    + figura("s3-temas-convocatoria",
             "Convocatorias que mencionan cada tema, cierre en 2025",
             "Una convocatoria cuenta en varios temas: el proyecto que cruza dos de ellos tiene más puertas.")
    + "\n"
    + criterio(
        "El impacto social aparece en casi siete de cada diez convocatorias. Un "
        "proyecto de ingeniería que no declara a quién beneficia queda fuera de la "
        "mayor parte de este mercado, aunque su tecnología sea buena."
    )
    + "\n"
    + fuente_pie(F_RADIO)
)


def L(slug, titulo, nav, icono, contenido, clases="slide", scripts=""):
    return {"slug": slug, "titulo": f"{SESION} · {titulo}", "nav": nav,
            "icono": icono, "clases": clases, "contenido": contenido,
            "scripts": scripts}


LAMINAS = [
    # ── APERTURA ──
    L("portada", "Portada", "Portada", "i-fund", PORTADA, "slide slide--start"),
    L("agenda", "Financiamiento público, inversión privada y cuatro paradas de herramientas", "Agenda", "i-flow", AGENDA),

    # ── 01 · INSTRUMENTOS PÚBLICOS ──
    L("tema-01", TEMA_A, "Tema 01", "i-fund", SECCION_A),
    L("bloques-de-presupuesto", "Presupuesto medio por instrumento de CTI según su bloque, 2012-2018", "Tamaño medio", "i-chart", BLOQUES_DE_PRESUPUESTO),
    L("desagregacion-inventario", "Nivel de desagregación del inventario público de instrumentos de CTI", "Qué publica la fuente", "i-search", DESAGREGACION_INVENTARIO),
    L("fondo-prociencia", "PROCIENCIA: concursos de investigación y programas de becas", "PROCIENCIA", "i-fund", FONDO_PROCIENCIA),
    L("fondo-startup-peru", "StartUp Perú: capital semilla para emprendimientos innovadores", "StartUp Perú", "i-fund", FONDO_STARTUP_PERU),
    L("fondo-proinnovate-empresa", "ProInnóvate: desarrollo tecnológico y validación con empresa", "ProInnóvate", "i-fund", FONDO_PROINNOVATE_EMPRESA),
    L("fondo-procompite", "PROCOMPITE: cofinanciamiento de planes de negocio de cadenas productivas", "PROCOMPITE", "i-fund", FONDO_PROCOMPITE),
    L("fondo-agroideas", "AGROIDEAS: reconversión productiva y asociatividad agraria", "AGROIDEAS", "i-fund", FONDO_AGROIDEAS),
    L("fondo-pnipa", "PNIPA: innovación en pesca y acuicultura", "PNIPA", "i-fund", FONDO_PNIPA),
    L("fondo-fondoempleo", "FONDOEMPLEO: proyectos de empleo y capacitación laboral", "FONDOEMPLEO", "i-fund", FONDO_FONDOEMPLEO),
    L("fondo-turismo-emprende", "Turismo Emprende: emprendimientos de servicios turísticos", "Turismo Emprende", "i-fund", FONDO_TURISMO_EMPRENDE),
    L("fondo-cultura", "Estímulos económicos del Ministerio de Cultura", "Cultura", "i-fund", FONDO_CULTURA),
    L("fondo-red-cite", "Red CITE del ITP: servicios tecnológicos que se contratan", "Red CITE", "i-fund", FONDO_RED_CITE),
    L("fondo-ley-30309", "Ley 30309: deducción adicional del impuesto sobre el gasto en I+D+i", "Ley 30309", "i-fund", FONDO_LEY_30309),
    L("herramientas-01", "Herramientas 01 · Portales de convocatoria", "Herramientas 01", "i-sliders", HERRAMIENTAS_09),
    L("contrapartida", "Contrapartida en un instrumento de cofinanciamiento: efectivo y especie", "Contrapartida", "i-agreement", CONTRAPARTIDA),
    L("aritmetica-contrapartida", "Reparto del costo de un proyecto entre subvención y contrapartida", "Cuánto se aporta", "i-budget", ARITMETICA_CONTRAPARTIDA),
    L("quien-aporta", "Partidas con las que cada tipo de entidad postulante aporta su contrapartida", "Quién aporta", "i-users", QUIEN_APORTA),
    L("entidad-asociada", "Entidad asociada: aporte que compromete y documento que lo acredita", "Entidad asociada", "i-agreement", ENTIDAD_ASOCIADA),
    L("herramientas-02", "Herramientas 02 · Buscadores de convocatorias", "Herramientas 02", "i-sliders", HERRAMIENTAS_10),
    L("desembolso-y-caja", "Momento del desembolso de cada forma y efecto en la caja", "Desembolso", "i-clock", DESEMBOLSO_Y_CAJA),
    L("admisibilidad", "Filtros de admisibilidad previos a la evaluación técnica de una propuesta", "Admisibilidad", "i-rubric", ADMISIBILIDAD),
    L("ventanilla-simulador", "Ventanillas admisibles según madurez, entidad y contrapartida", "Qué ventanilla admite", "i-sliders", VENTANILLA_SIM, "slide", VENTANILLA_JS),

    # ── 02 · INVERSIÓN PRIVADA ──

    L("tema-02", TEMA_B, "Tema 02", "i-rocket", SECCION_B),
    L("radio-tipos", "Qué tipo de oportunidad son las convocatorias que se publican en un año", "Tipos", "i-chart", RADIO_TIPOS),
    L("radio-montos", "Cuánto dinero da de verdad cada tipo de convocatoria", "Montos", "i-budget", RADIO_MONTOS),
    L("radio-calendario", "En qué meses del año se concentran los cierres de convocatoria", "Cierres", "i-calendar", RADIO_CALENDARIO),
    L("radio-temas", "Qué temas concentran las convocatorias y cuáles emergen", "Temas", "i-globe", RADIO_TEMAS),
    L("mapa-etapa-fondo", "Qué familia de fondos corresponde a cada momento del proyecto", "Etapa y fondo", "i-ladder", MAPA_ETAPA_FONDO),
    L("tipo-preincubacion", "Preincubación e incubación: acompañamiento antes que dinero", "Incubación", "i-fund", F02_PREINCUBACION),
    L("tipo-aceleradora", "Aceleradoras: cohorte cerrada, plazo corto y capital de entrada", "Aceleradoras", "i-fund", F02_ACELERADORA),
    L("tipo-angeles", "Inversores ángeles: patrimonio propio en etapa temprana", "Ángeles", "i-fund", F02_ANGELES),
    L("tipo-capital-riesgo", "Capital de riesgo: fondo con tesis, plazo de salida y consejo", "Capital de riesgo", "i-fund", F02_CAPITAL_RIESGO),
    L("que-pide-cada-uno", "Qué pide a cambio cada familia, de no pedir nada a pedir control", "Qué pide cada uno", "i-scale", QUE_PIDE_CADA_UNO),
    L("fondo-kunan", "Desafío Kunan: el premio de emprendimiento social del país", "Kunan", "i-fund", F02_KUNAN),
    L("fondo-wiese", "Fondo Emprendedor de la Fundación Wiese", "Fundación Wiese", "i-fund", F02_WIESE),
    L("fondo-dap-australia", "Direct Aid Program: fondos de la Embajada de Australia", "Embajada de Australia", "i-fund", F02_DAP_AUSTRALIA),
    # ── 02 · INCUBADORA Y ACELERADORA ──
    # ── 02 · EFECTO ATRIBUIBLE A LA ACELERADORA ──
    L("herramientas-03", "Herramientas 03 · Bases de datos de inversión", "Herramientas 03", "i-sliders", HERRAMIENTAS_11),
    L("fondo-iaf", "Inter American Foundation: donaciones a organizaciones de base", "IAF", "i-fund", F02_IAF),
    L("fondo-union-europea", "Delegación de la Unión Europea y los programas marco", "Unión Europea", "i-fund", F02_UNION_EUROPEA),
    L("fondo-bid", "Banca multilateral: BID y Banco Mundial", "BID", "i-fund", F02_BID),
    L("cooperacion-origen", "De dónde viene la cooperación internacional que entra al Perú", "Cooperación", "i-globe", COOPERACION_ORIGEN),
    L("fondo-clima", "Green Climate Fund: se entra por una entidad acreditada", "Fondos climáticos", "i-fund", F02_CLIMA),
    L("tipo-especie", "Financiamiento en especie: lo que no llega como dinero", "En especie", "i-fund", F02_ESPECIE),
    L("catalogo-simulador", "Qué familias del catálogo admiten el proyecto según etapa y figura", "Qué familia admite", "i-sliders", CATALOGO_SIM, "slide", CATALOGO_JS),
    L("calendario-convocatorias", "En qué meses del año abre cada familia de convocatorias", "Calendario", "i-calendar", CALENDARIO_CONVOCATORIAS),
    # ── 02 · CRITERIOS DEL INVERSOR ÁNGEL ──
    # ── 02 · CAPITAL DE RIESGO EN LA REGIÓN ──
    # ── 02 · GARANTÍAS PARCIALES DE CRÉDITO ──
    L("herramientas-04", "Herramientas 04 · Fondos de cooperación internacional", "Herramientas 04", "i-sliders", HERRAMIENTAS_12),

    # ── 02 · TALLERES ──

    # ── CIERRE ──
    L("queda-establecido", "Cinco puntos establecidos sobre dónde buscar el dinero de un proyecto", "Resumen", "i-check", RESUMEN),
    L("glosario", "Doce términos para leer una convocatoria y una hoja de términos", "Glosario", "i-book", GLOSARIO),
    L("referencias", "Las siete fuentes de la sesión, con su enlace y su vía de acceso", "Referencias", "i-quote", REFERENCIAS),
]

if __name__ == "__main__":
    generar_desde({"clase": "clase-03", "sesion": SESION,
                   "laminas": renumerar(LAMINAS)})
