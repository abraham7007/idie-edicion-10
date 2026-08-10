"""Sesión 5 · Del proyecto ganado al resultado transferido.

La sesión recorre los tres tiempos del dinero y de los papeles: el
presupuesto que se presenta, lo que empieza el día que se gana, y lo que
queda cuando termina. El eje no es un caso sino **el instrumento que financió
el proyecto**: lo que se presupuesta, se firma, se rinde y se protege cambia
según la forma del instrumento, y por eso la matriz instrumento × obligación
abre la sesión y se vuelve a mostrar al entrar en cada tema.

El prototipo de monitoreo de colmenas de la sesión 4 se conserva como ejemplo
trabajado. Sus magnitudes internas son didácticas y se declaran como tales;
toda cifra de convocatoria, tasa o plazo lleva su fuente y su fecha.

Lo que la sesión NO repite: contrapartida y momento del desembolso son de la
sesión 3; titularidad, cesión, licencia, vías de protección y la ruta de la
oficina de transferencia son de la sesión 2. Aquí entran como enlace de una
línea, nunca como explicación.

Uso:  python3 tools/clases/clase-05.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tools"))

from clases.comun import (  # noqa: E402
    cabecera, colofon, ico, mapa_ecosistema, problema, termino,
)
from clases.comun_idie import (  # noqa: E402
    aviso, conclusion, criterio, dato, dato_clave, definicion, duo, ejemplo,
    en_la_practica, envolver_visual as envolver, evitar, fichas, figura,
    fuente_pie, reiniciar_alternancia, seccion, renumerar, tabla,
    bloque_herramientas,
)
from generar_clase import generar_desde  # noqa: E402

reiniciar_alternancia()

SESION = "Sesión 5 · Del proyecto ganado al resultado transferido"

TEMA_A = "Presupuesto según el instrumento"
TEMA_B = "Del convenio al cierre administrativo"
TEMA_C = "Documentación como metodología"
TEMA_D = "Resultados: registro, publicación y difusión"
TEMA_E = "Transferencia y valorización"

# ==========================================================================
# FUENTES
# ==========================================================================
F_STARTUP = ('ProInnóvate · bases del concurso <i>Emprendimientos Innovadores '
             '12G</i> de StartUp Perú, 2025 · '
             '<a href="https://startup.proinnovate.gob.pe">'
             'startup.proinnovate.gob.pe</a> · consultado el 9 de agosto de 2026')
F_PROCIENCIA = ('PROCIENCIA · bases integradas y modificadas del concurso '
                'E072-2024-01-BM, 2024 · '
                '<a href="https://prociencia.gob.pe">prociencia.gob.pe</a> · '
                'consultado el 9 de agosto de 2026')
F_TUPA = ('Decreto Supremo 088-2025-PCM · Texto Único de Procedimientos '
          'Administrativos del INDECOPI, vigente desde el 1 de julio de 2025 · '
          '<a href="https://busquedas.elperuano.pe/dispositivo/NL/2414225-1">'
          'busquedas.elperuano.pe</a>')
F_D486 = ('Comunidad Andina · Decisión 486, Régimen Común sobre Propiedad '
          'Industrial, artículos 40, 42, 44 y 50 · '
          '<a href="https://www.wipo.int/wipolex/es/legislation/details/9451">'
          'wipolex.wipo.int</a>')
F_INDECOPI = ('INDECOPI · Dirección de Invenciones y Nuevas Tecnologías, cifras '
              'del Día del Inventor Peruano, julio de 2026 · '
              '<a href="https://www.indecopi.gob.pe">indecopi.gob.pe</a>')
F_OMPI = ('OMPI (2024), <i>Intellectual Property Valuation Basics for Technology '
          'Transfer Professionals</i>, capítulos 4 a 6 · '
          '<a href="https://www.wipo.int/web-publications/'
          'intellectual-property-valuation-basics-for-technology-transfer-'
          'professionals/en/index.html">wipo.int</a>')
F_BM = ('Aridi, A. y Cowey, L. (2018), <i>Technology Transfer from Public '
        'Research Organizations: A Framework for Analysis</i>, Banco Mundial · '
        '<a href="https://documents.worldbank.org">documents.worldbank.org</a>')
F_CONCYTEC_TT = ('CONCYTEC (2016), <i>Programa Especial de Transferencia y '
                 'Extensión Tecnológica · Parte 1</i> · '
                 '<a href="https://portal.concytec.gob.pe">portal.concytec.gob.pe</a>')
F_PI_CONVENIOS = ('Cláusulas contractuales de propiedad intelectual y divulgación '
                  'en convenios público-privados (2025), <i>Research Policy</i>')
F_DATOS = ('Prevalencia de datos y código compartidos en investigación médica y '
           'de la salud (2023), <i>BMJ</i> · revisión sistemática de 105 estudios '
           'sobre 2 121 580 artículos · CC BY')
F_DATOS_FIN = ('Apertura de datos desde la perspectiva de las agencias '
               'financiadoras (2022), <i>Research Integrity and Peer Review</i> · CC BY')
F_GOBERNANZA = ('Gobernanza de la investigación y futuros de la evaluación (2019) · '
                'indicadores con que se rinde cuentas de lo financiado')
F_ALICIA = ('CONCYTEC · ALICIA, Acceso Libre a Información Científica para la '
            'Innovación · <a href="https://alicia.concytec.gob.pe">'
            'alicia.concytec.gob.pe</a>')
F_TABLERO = ('INDECOPI · Tablero Estadístico de Patentes y Diseños '
             'Industriales, resultados de 2025, publicado el 4 de febrero de '
             '2026 · <a href="https://www.gob.pe/institucion/indecopi/noticias/'
             '1355764-hito-en-la-innovacion-en-2025-se-protegieron-mas-de-mil-'
             'inventos-en-el-peru-a-traves-del-sistema-de-patentes">indecopi '
             'en gob.pe</a>')
F_OTT = ('PROCIENCIA · concurso <i>Fortalecimiento de Oficinas de Transferencia '
         'Tecnológica 2025-01</i> · '
         '<a href="https://prociencia.gob.pe">prociencia.gob.pe</a>')
F_CASO = ('Caso de clase · magnitudes didácticas del prototipo de monitoreo de '
          'colmenas, no medidas en campo')

# ==========================================================================
# APERTURA
# ==========================================================================
PORTADA = f"""			<div class="slide__content stagger">
				<div class="cover">
					<div class="cover__main">
						<span class="badge" data-animate="fade-up">{ico("i-project")}Sesión 5</span>

						<h1 class="slide__title" data-animate="fade-up">Del proyecto ganado al resultado transferido</h1>

						<div class="cover__topics" data-animate="fade-up">
							<span class="topic"><span class="topic__n">01</span>{TEMA_A}</span>
							<span class="topic topic--b"><span class="topic__n">02</span>{TEMA_B}</span>
							<span class="topic"><span class="topic__n">03</span>{TEMA_C}</span>
							<span class="topic topic--b"><span class="topic__n">04</span>{TEMA_D}</span>
							<span class="topic"><span class="topic__n">05</span>{TEMA_E}</span>
						</div>

{colofon()}
					</div>

{mapa_ecosistema(
    activos=("academia", "empresa", "estado"),
    aristas=("estado-fondos", "fondos-academia", "academia-empresa"),
)}
				</div>
			</div>"""

AGENDA = envolver(
    cabecera("Agenda", "Contenidos de los cinco temas y las cinco paradas de herramientas", "i-flow")
    + "\n"
    + f"""\t\t\t\t<div class="agenda agenda--cinco" data-animate="fade-up">
\t\t\t\t\t<div class="agenda__block">
\t\t\t\t\t\t<span class="agenda__n">Tema 01</span>
\t\t\t\t\t\t<h3>Presupuesto</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Qué exige cada forma de instrumento</li>
\t\t\t\t\t\t\t<li>Partidas, topes y gastos no elegibles</li>
\t\t\t\t\t\t\t<li>Desembolso por hitos y hueco de caja</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--b">
\t\t\t\t\t\t<span class="agenda__n">Tema 02</span>
\t\t\t\t\t\t<h3>Convenio y ejecución</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Convenio y condiciones previas</li>
\t\t\t\t\t\t\t<li>Informe técnico y financiero</li>
\t\t\t\t\t\t\t<li>Los dos cierres del proyecto</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block">
\t\t\t\t\t\t<span class="agenda__n">Tema 03</span>
\t\t\t\t\t\t<h3>Documentación</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Las seis capas</li>
\t\t\t\t\t\t\t<li>Bitácora y control de versiones</li>
\t\t\t\t\t\t\t<li>La historia del proyecto</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--b">
\t\t\t\t\t\t<span class="agenda__n">Tema 04</span>
\t\t\t\t\t\t<h3>Resultados y registro</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Registros, tasas y plazos</li>
\t\t\t\t\t\t\t<li>El trámite y el plazo del proyecto</li>
\t\t\t\t\t\t\t<li>Artículos, congresos y alianzas</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--ancho">
\t\t\t\t\t\t<span class="agenda__n">Tema 05</span>
\t\t\t\t\t\t<h3>Transferencia</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>El abanico de alternativas</li>
\t\t\t\t\t\t\t<li>Madurez mínima de cada vía</li>
\t\t\t\t\t\t\t<li>Los tres métodos de valorización</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__map">
\t\t\t\t\t\t<span class="agenda__map-label">Las seis sesiones</span>
\t\t\t\t\t\t<ul class="agenda__steps">
\t\t\t\t\t\t\t<li><b>01</b>Fundamentos y ecosistema I+D+i+e</li>
\t\t\t\t\t\t\t<li><b>02</b><i>Startups</i>, <i>spin-offs</i> y transferencia</li>
\t\t\t\t\t\t\t<li><b>03</b>Mapa de financiamiento e inversión</li>
\t\t\t\t\t\t\t<li><b>04</b>Formulación de proyectos</li>
\t\t\t\t\t\t\t<li class="is-on"><b>05</b>Del proyecto ganado al resultado transferido</li>
\t\t\t\t\t\t\t<li><b>06</b><i>Pitch Elevator</i> y tendencias mundiales en I+D+i+e</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)

COSTO_MEDIOS = envolver(
    cabecera("Punto de partida",
             "Costo de los cuatro medios de verificación del caso, en soles",
             "i-scale")
    + "\n"
    + figura("s5-costo-medios",
             "Costo de obtención de cada medio de verificación del caso",
             "La matriz llegó con sus medios de verificación y sin precio. Ponerles precio es el primer renglón del presupuesto.")
    + "\n"
    + criterio(
        "Un medio de verificación que nadie paga no se mide, y lo que no se mide "
        "no se rinde."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

# ==========================================================================
# TEMA 01 · PRESUPUESTO SEGÚN EL INSTRUMENTO
# ==========================================================================
SECCION_A = seccion(
    "01", TEMA_A,
    "Qué se escribe en el presupuesto depende de qué instrumento lo financia. "
    "Una subvención exige las seis obligaciones; un premio, ninguna."
)

INSTRUMENTO_OBLIGACION = envolver(
    cabecera("01 · El eje de la sesión",
             "Seis formas de instrumento y las seis obligaciones de cada una",
             "i-rubric")
    + "\n"
    + figura("s5-instrumento-obligacion",
             "Seis formas de instrumento frente a seis obligaciones del proyecto financiado",
             "La subvención es la única que exige las seis. El premio no exige ninguna: se gana y se cobra.")
    + "\n"
    + criterio(
        "La fila del instrumento decide qué documentos existirán y quién los firma."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA, F_TUPA)
)

ACTIVIDAD_PARTIDA = envolver(
    cabecera("01 · Estructura del presupuesto",
             "Los cuatro pasos del costeo, de la actividad al monto",
             "i-flow")
    + "\n"
    + figura("s5-actividad-partida",
             "Recorrido de una actividad de la matriz hasta su monto en el presupuesto",
             "El presupuesto sale de la matriz hacia abajo. Nunca del monto máximo de la convocatoria hacia arriba.")
    + "\n"
    + evitar(
        "Partir del tope y repartirlo. Se nota: las partidas salen redondas y "
        "ninguna se puede seguir hasta una actividad."
    )
    + "\n"
    + fuente_pie(F_CASO, F_STARTUP)
)

PARTIDAS_ADMISIBLES = envolver(
    cabecera("01 · Partidas",
             "Seis partidas admisibles y su tope en StartUp Perú y PROCIENCIA",
             "i-layers")
    + "\n"
    + fichas([
        ("Honorarios e incentivos", "<b>Tope 40 % · 20 %</b>", [
            "Líder, equipo, responsable técnico y coinvestigadores",
        ]),
        ("Materiales e insumos", "Sin tope", [
            "Materia prima, ensayo y bases de datos",
        ]),
        ("Consultorías", "A suma alzada", [
            "Honorario, pasaje y viático dentro del precio",
        ]),
        ("Servicios tecnológicos", "Terceros", [
            "Prototipado, ensayo, certificación y licencias",
        ]),
        ("Pasajes y viáticos", "<b>Tope 8 %</b>", [
            "Por escala oficial, no por gasto real",
        ]),
        ("Equipos y bienes duraderos", "Si la convocatoria los abre", [
            "Solo los vinculados al proyecto",
        ]),
    ])
    + "\n"
    + criterio(
        "Cada gasto tiene que caber en una partida nombrada por las bases. Los "
        "topes cambian entre convocatorias y hasta entre bases iniciales e "
        "integradas."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

PARTIDAS_NO_ADMISIBLES = envolver(
    cabecera("01 · Partidas",
             "Tres familias de gasto no elegible en un fondo público",
             "i-alert")
    + "\n"
    + fichas([
        ("Lo que sostiene a la entidad", "Existiría sin el proyecto", [
            "Personal administrativo",
            "Luz, agua, telefonía, internet",
        ]),
        ("Lo financiero", "Nunca", [
            "Comisiones bancarias e intereses",
            "Deuda previa, multas y penalidades",
        ]),
        ("Lo patrimonial", "Nunca", [
            "Inmuebles y vehículos",
            "Equipos sin vínculo con la ejecución",
        ]),
    ])
    + "\n"
    + aviso(
        "Un gasto no elegible no se descuenta del cuadro: obliga a rehacerlo "
        "entero en plena evaluación, con el reloj de la convocatoria corriendo."
    )
    + "\n"
    + criterio(
        "El fondo paga lo que el proyecto añade, no lo que la entidad ya sostiene."
    )
    + "\n"
    + en_la_practica(
        "El sensor de peso del prototipo entra; el alquiler de un vehículo, no. "
        "La frontera es la vinculación con el proyecto."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

TOPES_RUBRO = envolver(
    cabecera("01 · Partidas",
             "Cuatro topes por rubro y la base sobre la que se calculan",
             "i-scale")
    + "\n"
    + figura("s5-topes-rubro",
             "Topes declarados por rubro en dos convocatorias del Estado",
             "El tope no dice nada sin su base: el 40 % es sobre el capital semilla y el 20 % sobre el monto financiado.")
    + "\n"
    + en_la_practica(
        "El 40 % de S/ 60 000 son S/ 24 000 para todo el equipo y todo el "
        "proyecto. Dos personas a tiempo completo no caben."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

HERR_01 = bloque_herramientas(
    "01", "05",
    "Costeo y presupuesto del proyecto",
    "Que cada monto se pueda seguir hasta una actividad y una partida.",
    [
        ("LibreOffice Calc", "The Document Foundation", [
            "Abierta, sin licencia ni cuenta",
            "Las actividades alimentan el cuadro de partidas",
            "Formato abierto, el del anexo verificable",
        ], "libreoffice.org"),
        ("Google Sheets", "Google", [
            "Edición simultánea con historial",
            "El historial prueba quién cambió qué monto",
            "Exporta al formato que piden las bases",
        ], "sheets.google.com"),
        ("GanttProject", "Comunidad libre", [
            "Dependencias, hitos y ruta crítica",
            "Recurso y costo por tarea",
            "Exporta el cronograma como anexo",
        ], "ganttproject.biz"),
    ],
    [
        ("Trazabilidad", "del monto a la actividad que lo produce"),
        ("Formato de salida", "el que piden las bases, sin copiar a mano"),
        ("Historial", "quién cambió qué, no solo la hoja final"),
    ],
)

PARTIDA_PI_DIFUSION = envolver(
    cabecera("01 · Partidas",
             "La partida de propiedad intelectual y difusión: 5 % del capital semilla",
             "i-target")
    + "\n"
    + figura("s5-cabe-en-la-partida",
             "Composición de la partida de propiedad intelectual y difusión del caso",
             "Con el tope del 5 % caben una solicitud de patente y el evento de cierre, y poco más.")
    + "\n"
    + fichas([
        ("Registro", "Tasas del TUPA", [
            "Solicitud, examen y búsqueda de antecedentes",
        ]),
        ("Publicación", "Acceso abierto", [
            "Cargo de la revista y depósito de datos",
        ]),
        ("Difusión", "Obligatoria en varias bases", [
            "Evento de cierre, congreso y audiovisual",
        ]),
    ])
    + "\n"
    + evitar(
        "Dejarla fuera del presupuesto: después no hay de dónde pagar la tasa."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_TUPA)
)

CONTRAPARTIDA_FIGURA = envolver(
    cabecera("01 · Contrapartida",
             "Contrapartida exigida a tres figuras de postulante, en porcentaje",
             "i-chart")
    + "\n"
    + figura("s5-contrapartida-figura",
             "Cofinanciamiento y contrapartida por tipo de entidad postulante",
             "La misma propuesta pide 0 % en efectivo a una entidad pública y 30 % a una universidad privada societaria.")
    + "\n"
    + criterio(
        "Cada aporte lleva partida, monto y documento, firmado antes del cierre "
        "de la convocatoria."
    )
    + "\n"
    + fuente_pie(F_PROCIENCIA, F_STARTUP)
)

FICHA_STARTUP = envolver(
    cabecera("01 · El instrumento del caso",
             "Condiciones económicas de StartUp Perú 12G, convocatoria 2025",
             "i-fund")
    + "\n"
    + figura("s5-ficha-startup",
             "Montos y porcentajes que fijan el presupuesto de un capital semilla",
             "Seis cifras bastan para saber si el proyecto cabe en la convocatoria.")
    + "\n"
    + dato_clave(
        "Cada convocatoria fija las suyas y cambian entre la versión inicial de "
        "las bases y la integrada. Se leen antes de escribir el presupuesto, no "
        "después."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

DESEMBOLSO_HITOS = envolver(
    cabecera("01 · Desembolso",
             "Momento del desembolso en cuatro formas de instrumento",
             "i-gantt")
    + "\n"
    + tabla(
        ["Instrumento", "Cómo entra el dinero", "Qué lo dispara"],
        [
            ["Subvención a empresa", "Por hitos negociados", "Hito verificado y aprobado"],
            ["Subvención a investigación", "Un adelanto y el saldo", "Firma y avance verificado"],
            ["Beca", "Por armadas", "Matrícula y permanencia"],
            ["Beneficio tributario", "No hay desembolso", "Declaración anual del impuesto"],
        ],
        "Tabla 1 · Momento del desembolso según la forma del instrumento",
    )
    + "\n"
    + criterio(
        "Actividades y desembolsos no coinciden nunca, y la diferencia hay que "
        "financiarla por otra vía."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

FLUJO_CAJA = envolver(
    cabecera("01 · Desembolso",
             "Hueco de caja de un proyecto de dieciocho meses, en miles de soles",
             "i-chart")
    + "\n"
    + figura("s5-flujo-caja",
             "Gasto acumulado y desembolso acumulado de un proyecto de dieciocho meses",
             "El gasto va siempre delante. El área entre las dos curvas es dinero que alguien tiene que poner antes.")
    + "\n"
    + problema(
        "El proyecto se gana y no puede empezar",
        "El equipo tiene el resultado publicado y no tiene con qué comprar el primer lote de sensores.",
        "El primer desembolso llega contra hito, y el primer hito exige haber gastado.",
        "Quién financia el hueco, con qué documento y a qué costo. Si la respuesta es «ya veremos», el primer hito se retrasa entero.",
    )
    + "\n"
    + fuente_pie(F_CASO, F_STARTUP)
)

PRESUPUESTO_SIM = envolver(
    cabecera("01 · Simulación",
             "Simulación: honorarios, tope del 40 % y saldo del capital semilla",
             "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="presupuesto" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<label class="sim__label" for="p-meses">Meses de dedicación del equipo emprendedor</label>
\t\t\t\t\t\t<input class="sim__range" id="p-meses" type="range" min="3" max="18" step="1" value="9" />
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="p-honorarios">S/ 0</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="p-veredicto" data-estado="ok">Dentro del tope</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="p-ensayo" checked />
\t\t\t\t\t\t\t<span><b>Se contrata el ensayo de calibración</b><span class="crit__help">Laboratorio acreditado · S/ 6 200 en servicios tecnológicos</span></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<p class="sim__what" id="p-nota"></p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Lo que cubre el capital semilla</h3>
\t\t\t\t\t\t\t<ul id="p-ok"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Lo que sale de la contrapartida</h3>
\t\t\t\t\t\t\t<ul id="p-no"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_STARTUP, F_CASO)
)

PRESUPUESTO_JS = """\t\t<script type="module">
\t\t\t// El tope del 40 % sobre el capital semilla es el de las bases de
\t\t\t// StartUp Perú 12G. Al pasarlo, el exceso no desaparece: cambia de
\t\t\t// bolsillo y pasa a la contrapartida del equipo.
\t\t\tconst raiz = document.querySelector('[data-sim="presupuesto"]');
\t\t\tconst meses = raiz.querySelector("#p-meses");
\t\t\tconst ensayo = raiz.querySelector("#p-ensayo");
\t\t\tconst salida = raiz.querySelector("#p-honorarios");
\t\t\tconst veredicto = raiz.querySelector("#p-veredicto");
\t\t\tconst nota = raiz.querySelector("#p-nota");
\t\t\tconst ok = raiz.querySelector("#p-ok");
\t\t\tconst no = raiz.querySelector("#p-no");

\t\t\tconst SEMILLA = 60000;
\t\t\tconst TOPE = 0.4 * SEMILLA;
\t\t\tconst POR_MES = 3200;
\t\t\tconst ENSAYO = 6200;
\t\t\tconst DIFUSION = 3000;

\t\t\t// Separador de millares con espacio fino y coma decimal, como el resto
\t\t\t// del mazo: «51,200» se lee 51,2 en español.
\t\t\tconst soles = (n) =>
\t\t\t\t"S/ " + Math.round(n).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, "\\u2009");

\t\t\tfunction pintar() {
\t\t\t\tconst m = Number(meses.value);
\t\t\t\tconst honorarios = m * POR_MES;
\t\t\t\tconst servicios = ensayo.checked ? ENSAYO : 0;
\t\t\t\tconst cubierto = Math.min(honorarios, TOPE);
\t\t\t\tconst exceso = Math.max(honorarios - TOPE, 0);
\t\t\t\tconst resto = SEMILLA - cubierto - servicios - DIFUSION;

\t\t\t\tsalida.textContent = soles(honorarios) + " en honorarios · " + m + " meses";
\t\t\t\tveredicto.textContent = exceso
\t\t\t\t\t? "Sobre el tope del 40 %"
\t\t\t\t\t: "Dentro del tope del 40 %";
\t\t\t\tveredicto.dataset.estado = exceso ? "warn" : "ok";

\t\t\t\tok.innerHTML = [
\t\t\t\t\t"Honorarios hasta el tope: " + soles(cubierto),
\t\t\t\t\t"Servicios tecnológicos: " + soles(servicios),
\t\t\t\t\t"Difusión y transferencia: " + soles(DIFUSION),
\t\t\t\t\t"Queda para materiales y consultoría: " + soles(Math.max(resto, 0)),
\t\t\t\t].map((x) => "<li>" + x + "</li>").join("");

\t\t\t\tno.innerHTML = exceso
\t\t\t\t\t? "<li>Honorarios sobre el tope: " + soles(exceso) + "</li>"
\t\t\t\t\t\t+ "<li>Va como aporte del equipo, con su compromiso por escrito</li>"
\t\t\t\t\t: "<li>Nada: el reparto cabe entero en el capital semilla</li>";

\t\t\t\tif (exceso) {
\t\t\t\t\tnota.textContent = "El exceso no se pierde ni lo cubre el fondo: pasa a "
\t\t\t\t\t\t+ "la contrapartida, y esa parte se compromete por escrito antes del "
\t\t\t\t\t\t+ "cierre de la convocatoria.";
\t\t\t\t} else if (resto < 4000) {
\t\t\t\t\tnota.textContent = "Quedan menos de S/ 4\\u2009000 para materiales y "
\t\t\t\t\t\t+ "consultoría. El presupuesto cuadra en la hoja y no en la ejecución.";
\t\t\t\t} else {
\t\t\t\t\tnota.textContent = "El reparto cabe. Cada monto debe poder seguirse "
\t\t\t\t\t\t+ "hasta una actividad de la matriz.";
\t\t\t\t}
\t\t\t}

\t\t\tmeses.addEventListener("input", pintar);
\t\t\tensayo.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""

# ==========================================================================
# TEMA 02 · DEL CONVENIO AL CIERRE ADMINISTRATIVO
# ==========================================================================
SECCION_B = seccion(
    "02", TEMA_B,
    "Lo que empieza el día que el proyecto se gana. Es la parte que nadie "
    "prepara, y la que decide si el segundo desembolso llega."
)

CICLO_DE_VIDA = envolver(
    cabecera("02 · El calendario",
             "Cuatro etapas del proyecto y diez obligaciones con su mes",
             "i-gantt")
    + "\n"
    + figura("s5-ciclo-de-vida",
             "Ciclo de vida del proyecto financiado, con la obligación que entra en cada etapa",
             "Cada cosa tiene su mes. La propiedad intelectual va antes de divulgar y la documentación empieza el primer día.")
    + "\n"
    + criterio(
        "Los dos retrasos más caros: documentar cuando hay que rendir y proteger "
        "cuando el resultado ya se presentó."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_D486, F_CASO)
)

CONVENIO = envolver(
    cabecera("02 · El convenio",
             "Seis cláusulas del convenio que se leen antes de firmar",
             "i-file")
    + "\n"
    + fichas([
        ("Objeto y entregables", "Qué se comprometió", [
            "Cambiar un hito exige adenda y vuelve a evaluación",
        ]),
        ("Desembolsos", "Qué dispara cada tramo", [
            "Y qué ocurre si un hito se retrasa",
        ]),
        ("Propiedad de los resultados", "Quién será titular", [
            "Y qué se reserva el Estado sobre uso y publicación",
        ]),
        ("Destino de los bienes", "Al cerrar", [
            "A quién pasa el equipo y con qué acta",
        ]),
        ("Causales de resolución", "Cuándo se corta", [
            "Devolución de lo desembolsado",
        ]),
        ("Confidencialidad", "Alcance y plazo", [
            "Compatible con la difusión obligatoria",
        ]),
    ])
    + "\n"
    + aviso(
        "El convenio no repite la propuesta: la reemplaza. Lo mal escrito aquí "
        "vale como está aquí."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

ANTES_DEL_DESEMBOLSO = envolver(
    cabecera("02 · Arranque",
             "Condiciones previas al primer desembolso de un fondo público",
             "i-milestone")
    + "\n"
    + figura("s5-antes-del-desembolso",
             "Requisitos entre la publicación del resultado y el primer desembolso",
             "Cinco trámites separan ganar de cobrar, y ninguno se puede empezar antes de ganar.")
    + "\n"
    + en_la_practica(
        "Sin reunión previa no hay desembolso. Ahí se fija el plan de trabajo, y "
        "después se rinde contra ese plan."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

HERR_02 = bloque_herramientas(
    "02", "05",
    "Seguimiento de hitos y evidencia documental",
    "Que en el mes catorce se pueda demostrar qué se hizo en el mes tres.",
    [
        ("Nextcloud", "Comunidad libre", [
            "Historial de versiones por archivo",
            "Cada versión queda fechada",
            "Se aloja en el servidor de la universidad",
        ], "nextcloud.com"),
        ("Zotero", "Corp. for Digital Scholarship", [
            "Fuente y documento juntos, con fecha",
            "Grupos: el equipo ve el mismo acervo",
            "Exporta al formato de la convocatoria",
        ], "zotero.org"),
        ("Obsidian", "Obsidian.md", [
            "Texto plano, legible sin la aplicación",
            "El hito enlaza con su evidencia",
            "Los archivos entran en control de versiones",
        ], "obsidian.md"),
    ],
    [
        ("Fecha verificable", "cuándo se creó, no solo qué dice"),
        ("Salida sin la herramienta", "el archivo se lee sin el programa"),
        ("Quién más entra", "el equipo accede sin depender de una persona"),
    ],
)

INFORMES = envolver(
    cabecera("02 · Rendición",
             "Cuatro piezas del informe técnico y cuatro del financiero",
             "i-rubric")
    + "\n"
    + figura("s5-informes",
             "Piezas que exige cada uno de los dos informes de un tramo",
             "No comparten ninguna pieza y se entregan juntos. Uno prueba el resultado, el otro prueba el gasto.")
    + "\n"
    + criterio(
        "El hito no es «se realizaron doce visitas»: es el documento o el ensayo "
        "que esas visitas produjeron."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

SUSTENTO = envolver(
    cabecera("02 · Rendición",
             "Cinco requisitos del comprobante que sustenta un gasto",
             "i-file")
    + "\n"
    + tabla(
        ["Qué se presenta", "Qué debe decir", "Por qué se observa"],
        [
            ["Comprobante", "A nombre de la entidad ejecutora", "No de un integrante"],
            ["Detalle", "Concepto clasificable en una partida", "«Servicios varios» no vale"],
            ["Fecha", "Entre el acta de inicio y el cierre del tramo", "Antes de la firma no es elegible"],
            ["Constancia de pago", "Desde la cuenta del proyecto", "El efectivo sin rastro se observa"],
            ["Entregable", "Informe, acta o producto", "El pago solo prueba el pago"],
        ],
        "Tabla 2 · Qué mira quien revisa un comprobante",
    )
    + "\n"
    + evitar(
        "Guardarlos para el final del tramo: la factura que falta aparece cuando "
        "el proveedor ya no responde."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

MODIFICACIONES = envolver(
    cabecera("02 · Modificaciones",
             "Cinco modificaciones presupuestales y el trámite de cada una",
             "i-flow")
    + "\n"
    + figura("s5-modificaciones",
             "Trámite que exige cada tipo de modificación durante la ejecución",
             "El umbral del 5 % separa lo que se comunica de lo que espera autorización antes de gastarse.")
    + "\n"
    + dato_clave(
        "Una variación <b>superior al 5 %</b> deja de ser ajuste y vuelve a "
        "evaluación. El umbral está en el manual operativo del fondo."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

CIERRE_DOBLE = envolver(
    cabecera("02 · Cierre",
             "Duración del cierre técnico y del administrativo, en meses",
             "i-milestone")
    + "\n"
    + figura("s5-cierre-doble",
             "Duración del cierre técnico y del cierre administrativo desde el último hito",
             "El proyecto termina técnicamente mucho antes de terminar en el expediente.")
    + "\n"
    + problema(
        "El equipo se disuelve antes del cierre administrativo",
        "Nadie responde los requerimientos del fondo porque el proyecto «ya terminó».",
        "El cierre técnico y el administrativo se confunden, y el segundo dura meses más.",
        "Quién queda como responsable del expediente después del último hito, y con cargo a qué tiempo.",
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

RENDICION_SIM = envolver(
    cabecera("02 · Simulación",
             "Simulación: las cuatro condiciones que admiten un gasto",
             "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="rendicion" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<span class="sim__label">Un gasto de S/ 6 200 por un ensayo de calibración</span>
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="r-estado">Se observa</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="r-badge" data-estado="warn">3 de 4 condiciones</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="r-nombre" checked />
\t\t\t\t\t\t\t<span><b>Comprobante a nombre de la entidad ejecutora</b></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="r-fecha" checked />
\t\t\t\t\t\t\t<span><b>Fecha posterior al acta de inicio</b></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="r-partida" checked />
\t\t\t\t\t\t\t<span><b>Concepto reconocible en una partida del presupuesto</b></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="r-entregable" />
\t\t\t\t\t\t\t<span><b>Informe de ensayo adjunto</b><span class="crit__help">Prueba que el servicio se prestó, no solo que se pagó</span></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<p class="sim__what" id="r-nota"></p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Lo que el expediente acredita</h3>
\t\t\t\t\t\t\t<ul id="r-ok"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Lo que se va a observar</h3>
\t\t\t\t\t\t\t<ul id="r-no"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_STARTUP, F_CASO)
)

RENDICION_JS = """\t\t<script type="module">
\t\t\t// Las cuatro condiciones son acumulativas: basta que falle una para que
\t\t\t// el gasto se observe. La cuarta —el entregable— es la que más se olvida
\t\t\t// y por eso arranca desmarcada.
\t\t\tconst raiz = document.querySelector('[data-sim="rendicion"]');
\t\t\tconst CONDICIONES = [
\t\t\t\t["r-nombre",
\t\t\t\t\t"El comprobante es de la entidad ejecutora",
\t\t\t\t\t"A nombre de una persona: el gasto no es del proyecto"],
\t\t\t\t["r-fecha",
\t\t\t\t\t"El gasto cae dentro del plazo de ejecución",
\t\t\t\t\t"Anterior al acta de inicio: no es elegible"],
\t\t\t\t["r-partida",
\t\t\t\t\t"El concepto entra en servicios tecnológicos",
\t\t\t\t\t"Sin concepto clasificable no hay contraste con el presupuesto"],
\t\t\t\t["r-entregable",
\t\t\t\t\t"El informe de ensayo prueba que el servicio se prestó",
\t\t\t\t\t"Servicio pagado sin producto: acredita el pago, no la ejecución"],
\t\t\t];
\t\t\tconst estado = raiz.querySelector("#r-estado");
\t\t\tconst badge = raiz.querySelector("#r-badge");
\t\t\tconst ok = raiz.querySelector("#r-ok");
\t\t\tconst no = raiz.querySelector("#r-no");
\t\t\tconst nota = raiz.querySelector("#r-nota");

\t\t\tfunction pintar() {
\t\t\t\tconst cumplidas = [], fallidas = [];
\t\t\t\tCONDICIONES.forEach(([id, si, error]) => {
\t\t\t\t\t(raiz.querySelector("#" + id).checked ? cumplidas : fallidas)
\t\t\t\t\t\t.push(raiz.querySelector("#" + id).checked ? si : error);
\t\t\t\t});
\t\t\t\tok.innerHTML = cumplidas.map((x) => "<li>" + x + "</li>").join("")
\t\t\t\t\t|| "<li>Nada: el comprobante no acredita ninguna condición.</li>";
\t\t\t\tno.innerHTML = fallidas.map((x) => "<li>" + x + "</li>").join("")
\t\t\t\t\t|| "<li>Nada: las cuatro condiciones se cumplen.</li>";

\t\t\t\tconst admitido = fallidas.length === 0;
\t\t\t\testado.textContent = admitido ? "Se admite" : "Se observa";
\t\t\t\tbadge.textContent = cumplidas.length + " de " + CONDICIONES.length + " condiciones";
\t\t\t\tbadge.dataset.estado = admitido ? "ok" : "warn";
\t\t\t\tnota.textContent = admitido
\t\t\t\t\t? "El gasto entra en la rendición del tramo."
\t\t\t\t\t: "Un gasto observado se subsana, pero suspende el tramo entero "
\t\t\t\t\t\t+ "mientras tanto, y con él el desembolso siguiente.";
\t\t\t}

\t\t\tCONDICIONES.forEach(([id]) =>
\t\t\t\traiz.querySelector("#" + id).addEventListener("change", pintar));
\t\t\tpintar();
\t\t</script>"""

# ==========================================================================
# TEMA 03 · DOCUMENTACIÓN COMO METODOLOGÍA
# ==========================================================================
SECCION_C = seccion(
    "03", TEMA_C,
    "El repositorio público es una capa de la documentación, y es la quinta. "
    "Sin las cuatro anteriores no hay prueba de autoría ni historia que contar."
)

DOCUMENTAR_ES_METODO = envolver(
    cabecera("03 · Por qué",
             "Cuatro funciones de la documentación en un proyecto financiado",
             "i-book")
    + "\n"
    + fichas([
        ("Probar quién lo hizo", "Frente a una disputa", [
            "Sin fecha verificable, las dos palabras valen igual",
        ]),
        ("Permitir reproducirlo", "Frente a un evaluador", [
            "Lo que nadie repite no acredita nada",
        ]),
        ("Sostener la rendición", "Frente al fondo", [
            "El informe se arma con lo ya documentado",
        ]),
        ("Contar la historia", "Frente al siguiente fondo", [
            "O se recogió durante, o no existe",
        ]),
    ], columnas=2)
    + "\n"
    + criterio(
        "Un ensayo sin bitácora es un ensayo que hay que volver a hacer."
    )
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_CASO)
)

CAPAS_DOCUMENTACION = envolver(
    cabecera("03 · Las capas",
             "Las seis capas de documentación, de la bitácora al registro",
             "i-layers")
    + "\n"
    + figura("s5-capas-documentacion",
             "Seis capas de documentación, con la pregunta que responde cada una",
             "Publicar en un repositorio es la quinta capa. Sin las cuatro anteriores no hay nada que publicar.")
    + "\n"
    + evitar(
        "Confundir documentar con subir al repositorio. El código final sin "
        "historia no dice qué se probó ni qué se descartó."
    )
    + "\n"
    + fuente_pie(F_CONCYTEC_TT)
)

BITACORA = envolver(
    cabecera("03 · Bitácora",
             "Fuerza probatoria de cuatro formas de registrar el desarrollo",
             "i-scale")
    + "\n"
    + figura("s5-bitacora-prueba",
             "Fuerza probatoria de cuatro formas de registrar el desarrollo",
             "Solo la solicitud presentada fija fecha de prioridad. Las demás prueban autoría, no derecho.")
    + "\n"
    + definicion(
        "Fecha cierta",
        "Práctica registral y probatoria",
        "Momento a partir del cual la existencia de un documento no depende de "
        "la palabra de quien lo firma, porque un tercero o un mecanismo "
        "verificable la respalda. Separa una libreta de notas de una prueba "
        "utilizable.",
    )
    + "\n"
    + fuente_pie(F_D486, F_CONCYTEC_TT)
)

VERSIONES_ARTEFACTO = envolver(
    cabecera("03 · Versiones",
             "Cinco artefactos de un prototipo electrónico y cómo se versionan",
             "i-layers")
    + "\n"
    + figura("s5-versiones-artefacto",
             "Cinco artefactos del prototipo y la forma de versionar cada uno",
             "El código es uno de los cinco. La placa, la lista de materiales y los ensayos también cambian de versión.")
    + "\n"
    + en_la_practica(
        "La versión 3 del firmware solo tiene sentido con la revisión B de la "
        "placa y su lista de materiales."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

HERR_03 = bloque_herramientas(
    "03", "05",
    "Documentación, trazabilidad y repositorios",
    "Registrar el desarrollo mientras ocurre y dejar el depósito citable.",
    [
        ("Git con GitLab o GitHub", "Comunidad y proveedores", [
            "Cada cambio con autor, fecha y motivo",
            "Firmware, esquemáticos y documentos",
            "La etiqueta marca el estado de cada hito",
        ], "about.gitlab.com"),
        ("Zenodo", "CERN y Comisión Europea", [
            "Datos, código y documentos con DOI",
            "El DOI fija el contenido en una fecha",
            "Se enlaza con el repositorio de código",
        ], "zenodo.org"),
        ("ALICIA", "CONCYTEC", [
            "Repositorio nacional de acceso libre",
            "Destino exigido para tesis y artículos",
            "Da visibilidad que el repositorio propio no da",
        ], "alicia.concytec.gob.pe"),
    ],
    [
        ("Identificador permanente", "citable dentro de diez años"),
        ("Qué admite", "el tipo de archivo real, no solo texto"),
        ("Qué exige el financiador", "que las bases reconozcan el destino"),
    ],
)

DATOS_Y_METADATOS = envolver(
    cabecera("03 · Datos",
             "Las seis decisiones de un plan de gestión de datos",
             "i-diagram")
    + "\n"
    + tabla(
        ["Componente", "Qué declara", "Cuándo se decide"],
        [
            ["Qué se produce", "Tipo, volumen y formato", "Al formular"],
            ["Cómo se nombran", "Convención y estructura de carpetas", "Antes del primer ensayo"],
            ["Qué metadatos", "Variable, unidad, instrumento", "Al cerrar cada ensayo"],
            ["Dónde se depositan", "Repositorio y momento", "Antes de publicar"],
            ["Con qué licencia", "Qué puede hacer un tercero", "Al depositar"],
            ["Qué no se abre", "Datos personales y confidenciales", "Al firmar el convenio"],
        ],
        "Tabla 3 · Las seis decisiones de un plan de gestión de datos",
    )
    + "\n"
    + criterio(
        "Un dato sin unidad ni instrumento es una columna de números. Se decide "
        "al registrarlo, no al depositarlo."
    )
    + "\n"
    + fuente_pie(F_DATOS_FIN, F_CASO)
)

DONDE_VA_CADA_COSA = envolver(
    cabecera("03 · Depósito",
             "Seis clases de material y su repositorio de destino",
             "i-network")
    + "\n"
    + figura("s5-donde-va-cada-cosa",
             "Clase de material, repositorio de destino y forma de citarlo",
             "Seis clases de material y seis destinos distintos. El repositorio de código sirve para uno.")
    + "\n"
    + fuente_pie(F_ALICIA, F_DATOS_FIN)
)

HISTORIA_DEL_PROYECTO = envolver(
    cabecera("03 · Historia",
             "La historia del proyecto: qué se recoge, de dónde sale y para qué",
             "i-quote")
    + "\n"
    + fichas([
        ("Qué se recoge", "Durante, no al final", [
            "La decisión que cambió el rumbo, con fecha",
            "El ensayo que salió mal y lo que enseñó",
        ]),
        ("De dónde sale", "De la bitácora", [
            "Fechas, motivos, antes y después",
            "No se escribe nada nuevo: se selecciona",
        ]),
        ("Para qué sirve", "Después del cierre", [
            "Material del <i>pitch</i> ante un comité",
            "Convence de que el equipo ejecuta",
        ]),
    ])
    + "\n"
    + ejemplo(
        "«Mes cuatro: el sensor de peso derivaba con la temperatura. Se cambió "
        "el montaje y el error bajó de 180 a 25 gramos.» Antes, decisión y "
        "después, con número."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

DATOS_ABIERTOS = envolver(
    cabecera("03 · Datos abiertos",
             "Datos y código disponibles: 8 % declarado y 2 % real, 2016-2021",
             "i-chart")
    + "\n"
    + figura("s5-datos-compartidos",
             "Disponibilidad declarada y disponibilidad real de datos y código, 2016-2021",
             "Ocho de cada cien artículos declaran datos disponibles y dos los tienen de verdad.")
    + "\n"
    + dato_clave(
        "<b>105 estudios sobre 2 121 580 artículos.</b> Disponibilidad declarada "
        "8 %, real 2 %, y el código bajo el 0,5 %."
    )
    + "\n"
    + conclusion(
        "Declarar no es compartir",
        "La distancia entre la declaración y el archivo descargable es el "
        "hallazgo. Si el convenio obliga a abrir datos, el plan de gestión y la "
        "partida de depósito son lo que hace que la obligación se cumpla.",
    )
    + "\n"
    + fuente_pie(F_DATOS, F_DATOS_FIN, F_GOBERNANZA)
)

# ==========================================================================
# TEMA 04 · RESULTADOS: REGISTRO, PUBLICACIÓN Y DIFUSIÓN
# ==========================================================================
SECCION_D = seccion(
    "04", TEMA_D,
    "Qué produce el proyecto, cuánto cuesta protegerlo y en qué orden se "
    "protege y se cuenta. Qué es una patente ya está dado; aquí, en qué mes se "
    "solicita y con cargo a qué partida."
)

PROTEGER_ANTES_PUBLICAR = envolver(
    cabecera("04 · El orden",
             "Antes y después de la solicitud: qué se documenta y qué se divulga",
             "i-flow")
    + "\n"
    + figura("s5-proteger-antes-publicar",
             "Actividades admisibles antes y después de presentar la solicitud",
             "La fecha de solicitud parte el proyecto en dos. Antes se documenta; después se cuenta.")
    + "\n"
    + criterio(
        "El <b>cuándo</b> cabe en una fecha: la de la solicitud, que entra en el "
        "cronograma como un hito más."
    )
    + "\n"
    + fuente_pie(F_D486, F_CASO)
)

MAPA_REGISTROS = envolver(
    cabecera("04 · Registros",
             "Seis figuras de protección industrial y su vigencia en el Perú",
             "i-rubric")
    + "\n"
    + figura("s5-mapa-registros",
             "Seis figuras de protección, qué protege cada una y cuánto dura",
             "Cinco se registran ante INDECOPI. El secreto empresarial no se registra y dura mientras se guarde.")
    + "\n"
    + en_la_practica(
        "El prototipo admite varias a la vez: circuito a patente, carcasa a "
        "diseño, firmware a derecho de autor y algoritmo a secreto."
    )
    + "\n"
    + fuente_pie(F_D486, F_INDECOPI)
)

TASAS_INDECOPI = envolver(
    cabecera("04 · Costo",
             "Tasas de registro del TUPA de INDECOPI, vigentes desde julio de 2025",
             "i-fund")
    + "\n"
    + figura("s5-tasas-indecopi",
             "Tasa de solicitud y de examen de fondo por tipo de registro, en soles",
             "El modelo de utilidad cuesta la mitad que la patente y protege diez años en lugar de veinte.")
    + "\n"
    + dato_clave(
        "El <b>DS 088-2025-PCM</b> redujo la solicitud de patente un 45 % y su "
        "examen un 41 %; el modelo de utilidad, un 30 % y un 65 %."
    )
    + "\n"
    + aviso(
        "A la tasa se suman la redacción de las reivindicaciones, donde se decide "
        "si la patente sirve, y las anualidades."
    )
    + "\n"
    + fuente_pie(F_TUPA)
)

PLAZOS_PATENTE = envolver(
    cabecera("04 · Plazos",
             "Plazos del procedimiento de patente según la Decisión 486",
             "i-gantt")
    + "\n"
    + figura("s5-plazos-patente",
             "Etapas del procedimiento de patente y su plazo según la Decisión 486",
             "Dieciocho meses de confidencialidad, sesenta días para oponerse y seis meses para pedir el examen.")
    + "\n"
    + criterio(
        "Los fija la Decisión 486, que rige igual en Perú, Colombia, Ecuador y "
        "Bolivia. No los fija INDECOPI."
    )
    + "\n"
    + fuente_pie(F_D486)
)

HERR_04 = bloque_herramientas(
    "04", "05",
    "Búsqueda de antecedentes de patente",
    "Comprobar la novedad antes de pagar la tasa, no después de la denegación.",
    [
        ("Espacenet", "Oficina Europea de Patentes", [
            "Más de cien millones de documentos",
            "Búsqueda por clasificación internacional",
            "Muestra en qué países está protegida",
        ], "worldwide.espacenet.com"),
        ("Patentscope", "OMPI", [
            "PCT y colecciones nacionales",
            "Busca en el texto completo",
            "Traduce la consulta a varios idiomas",
        ], "patentscope.wipo.int"),
        ("Buscador de INDECOPI", "INDECOPI", [
            "Solicitudes y títulos concedidos en el Perú",
            "Muestra el estado del expediente",
            "La fuente que se cita si el antecedente es peruano",
        ], "servicio.indecopi.gob.pe"),
    ],
    [
        ("Cobertura", "la jurisdicción donde se quiere proteger"),
        ("Qué campo busca", "el texto completo, no solo el título"),
        ("Estado del expediente", "si la solicitud sigue viva o está abandonada"),
    ],
)

TRAMITE_VS_PROYECTO = envolver(
    cabecera("04 · El desfase",
             "Dieciocho meses de proyecto frente a cuarenta y dos de trámite",
             "i-alert")
    + "\n"
    + figura("s5-tramite-vs-proyecto",
             "Duración del proyecto financiado y del trámite de patente sobre la misma línea",
             "El proyecto cierra su expediente y al trámite le quedan treinta meses sin presupuesto detrás.")
    + "\n"
    + problema(
        "La solicitud se abandona por una tasa que nadie presupuestó",
        "El expediente entra en abandono porque no se pagó el examen de fondo a tiempo.",
        "El proyecto ya cerró, la cuenta se liquidó y el trámite seguía corriendo.",
        "Quién asume las tasas posteriores al cierre y con cargo a qué. Se decide al firmar el convenio, no cuando llega el requerimiento.",
    )
    + "\n"
    + fuente_pie(F_D486, F_TUPA, F_CASO)
)

TITULOS_INDECOPI = envolver(
    cabecera("04 · El contexto",
             "Universidades peruanas en el ranking de patentes de INDECOPI, 2025",
             "i-chart")
    + "\n"
    + figura("s5-universidades-patentes",
             "Solicitudes presentadas y títulos concedidos por universidad, 2025",
             "Quien más solicita no es quien más obtiene: Continental encabeza en solicitudes y Privada del Norte en concesiones.")
    + "\n"
    + dato_clave(
        "<b>968 solicitudes</b> universitarias en 2025, el <b>79 % del total "
        "nacional</b> y un 34 % más que en 2024. Se concedieron 513 títulos a "
        "nacionales, de un récord de 1 050 con extranjeros."
    )
    + "\n"
    + fuente_pie(F_TABLERO)
)

COMPOSICION_SOLICITUDES = envolver(
    cabecera("04 · El contexto",
             "Composición de la solicitud universitaria peruana, 2025",
             "i-layers")
    + "\n"
    + figura("s5-invencion-vs-utilidad",
             "Reparto de las 968 solicitudes universitarias entre las dos figuras, 2025",
             "Tres de cada cuatro solicitudes son modelo de utilidad, la figura de diez años y examen más barato.")
    + "\n"
    + criterio(
        "El modelo de utilidad protege una mejora funcional, cuesta la mitad y se "
        "resuelve antes. No es una patente de segunda."
    )
    + "\n"
    + fuente_pie(F_TABLERO, F_TUPA)
)

TITULARIDAD_Y_CLAUSULAS = envolver(
    cabecera("04 · Titularidad",
             "Titularidad de los resultados en un proyecto con fondo público",
             "i-file")
    + "\n"
    + fichas([
        ("Las bases del concurso", "Antes de postular", [
            "Quién es titular y qué se reserva el Estado",
        ]),
        ("El convenio", "Antes de firmar", [
            "Quién decide solicitar, licenciar o abandonar",
        ]),
        ("Lo que se pacta", "<i>Research Policy</i>, 2025", [
            "El plazo de reserva decide en qué año se sustenta la tesis",
        ]),
    ])
    + "\n"
    + aviso(
        "Con fondo público hay un documento por encima del reglamento y del "
        "convenio: las bases del concurso."
    )
    + "\n"
    + fuente_pie(F_PI_CONVENIOS, F_STARTUP, F_PROCIENCIA)
)

ARTICULOS = envolver(
    cabecera("04 · Publicación",
             "Cuatro obligaciones de publicación y su costo en el presupuesto",
             "i-book")
    + "\n"
    + tabla(
        ["Qué exige", "Quién lo exige", "Qué implica en el presupuesto"],
        [
            ["Acceso abierto", "Agencias financiadoras", "Cargo de la revista, si lo cobra"],
            ["Depósito en ALICIA", "Normativa peruana", "Sin costo, con metadatos correctos"],
            ["Reconocer al financiador", "Todas las bases", "Una línea con el código"],
            ["Depositar los datos", "Revistas y agencias", "Identificador y metadatos"],
        ],
        "Tabla 4 · Obligaciones de publicación y su reflejo en el presupuesto",
    )
    + "\n"
    + en_la_practica(
        "Después de la solicitud y antes del cierre. Publicado más tarde, el "
        "informe final ya no lo recoge."
    )
    + "\n"
    + fuente_pie(F_ALICIA, F_DATOS_FIN)
)

CONGRESOS = envolver(
    cabecera("04 · Difusión",
             "Cuatro foros de difusión y el mes del proyecto en que caben",
             "i-network")
    + "\n"
    + figura("s5-congresos-momento",
             "Momento del proyecto en que cabe cada foro de difusión",
             "El póster, la ponencia y la demostración exigen madurez distinta, y ninguno va antes de la solicitud.")
    + "\n"
    + evitar(
        "Llevar el prototipo a una feria antes de solicitar. Una demostración "
        "pública es divulgación habilitante."
    )
    + "\n"
    + fuente_pie(F_D486, F_CASO)
)

OTROS_RESULTADOS = envolver(
    cabecera("04 · Resultados",
             "Ocho resultados acreditables y el documento que prueba cada uno",
             "i-layers")
    + "\n"
    + figura("s5-resultados-tipos",
             "Ocho clases de resultado y el documento que acredita cada una",
             "Un proyecto produce más de un resultado, y cada uno se prueba con un documento distinto.")
    + "\n"
    + criterio(
        "La alianza también es resultado, y se acredita con un convenio firmado "
        "que declare objeto y plazo."
    )
    + "\n"
    + fuente_pie(F_CASO, F_BM)
)

# ==========================================================================
# TEMA 05 · TRANSFERENCIA Y VALORIZACIÓN
# ==========================================================================
SECCION_E = seccion(
    "05", TEMA_E,
    "Cómo sale el resultado del proyecto y cuánto vale. Las tres vías de salida "
    "ya están dadas; aquí está el abanico completo y la pregunta que ninguna de "
    "las tres responde."
)

QUE_ES_TRANSFERIR = envolver(
    cabecera("05 · Definición",
             "Las tres condiciones que hacen posible una transferencia",
             "i-target")
    + "\n"
    + definicion(
        "Transferencia tecnológica",
        "CONCYTEC (2016) y Aridi y Cowey (2018)",
        "Proceso por el que un resultado de investigación pasa a ser usado por "
        "alguien distinto de quien lo obtuvo, con una contraprestación pactada. "
        "Comprende desde el intercambio de conocimiento sin contraprestación "
        "hasta la cesión completa de la titularidad.",
        "i-flow",
    )
    + "\n"
    + criterio(
        "Las tres son acumulativas y la que más falla es la tercera."
    )
    + "\n"
    + fichas([
        ("Resultado protegido", "O abierto a propósito", [
            "Sin titularidad clara no hay nada que licenciar",
        ]),
        ("Documentación suficiente", "La capa tres", [
            "El receptor lo reproduce sin el equipo original",
        ]),
        ("Receptor con capacidad", "De absorberlo", [
            "Sin ella la licencia se firma y no pasa nada",
        ]),
    ])
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_BM)
)

ABANICO = envolver(
    cabecera("05 · Alternativas",
             "Nueve formas de transferencia, de la publicación a la cesión",
             "i-diagram")
    + "\n"
    + figura("s5-abanico-transferencia",
             "Espectro de nueve formas de transferencia, de menor a mayor control cedido",
             "La licencia y la <i>spin-off</i> son dos de nueve. Las otras siete también transfieren y ceden menos.")
    + "\n"
    + criterio(
        "La figura añade las formas que casi nadie cuenta como transferencia: "
        "consultoría, uso de equipos, encargo y apertura."
    )
    + "\n"
    + fuente_pie(F_BM, F_CONCYTEC_TT)
)

MADUREZ_VIA = envolver(
    cabecera("05 · Madurez",
             "Madurez mínima de seis vías de transferencia, en escala TRL",
             "i-ladder")
    + "\n"
    + figura("s5-madurez-via",
             "Nivel de madurez tecnológica desde el que admite cada vía de transferencia",
             "Por debajo del nivel cuatro casi nadie licencia: lo que se transfiere entonces es trabajo, no tecnología.")
    + "\n"
    + en_la_practica(
        "El prototipo, validado en campo, entra donde la licencia no exclusiva "
        "empieza a ser posible. La cesión pide un nivel más."
    )
    + "\n"
    + fuente_pie(F_BM, F_CASO)
)

HERR_05 = bloque_herramientas(
    "05", "05",
    "Vigilancia tecnológica y búsqueda de comparables",
    "Poner un número antes de negociar: comparables y tamaño de mercado.",
    [
        ("Espacenet y Patentscope", "EPO y OMPI", [
            "Quién patenta en el campo y con qué frecuencia",
            "Los que más solicitan son candidatos a licenciatario",
            "La familia indica en qué mercados se juega",
        ], "worldwide.espacenet.com"),
        ("OpenAlex", "OurResearch", [
            "Producción científica con institución y financiador",
            "Qué grupos trabajan el mismo problema",
            "Libre y descargable, sin suscripción",
        ], "openalex.org"),
        ("INEI y gremios sectoriales", "Fuentes nacionales", [
            "Tamaño del mercado peruano",
            "Series oficiales con año y unidad",
            "Precios y volúmenes que la estadística omite",
        ], "inei.gob.pe"),
    ],
    [
        ("Qué comparable devuelve", "operaciones o magnitudes, no documentos"),
        ("Acceso sostenido", "se vuelve a consultar sin suscripción"),
        ("Trazabilidad del dato", "año, unidad y fuente citable"),
    ],
)

METODOS_VALORIZACION = envolver(
    cabecera("05 · Valorización",
             "Costo, mercado e ingresos: los tres métodos de valorización",
             "i-scale")
    + "\n"
    + figura("s5-metodos-valorizacion",
             "Los tres métodos de valorización, sus datos y su punto débil",
             "Ninguno da el valor: cada uno da un número distinto, y el rango entre ellos es la posición de negociación.")
    + "\n"
    + dato_clave(
        "Costo ignora el valor futuro. Mercado necesita comparables que casi "
        "nunca existen. Ingresos depende de la tasa de descuento."
    )
    + "\n"
    + fuente_pie(F_OMPI)
)

VALORIZACION_POR_ACTIVO = envolver(
    cabecera("05 · Valorización",
             "Método de valorización aplicable a cinco tipos de activo",
             "i-rubric")
    + "\n"
    + figura("s5-valorizacion-por-activo",
             "Aplicabilidad de cada método de valorización según el tipo de activo",
             "El secreto empresarial y la base de datos no tienen comparables: el método de mercado no aplica.")
    + "\n"
    + criterio(
        "La solicitud en trámite se valoriza por costo: no hay concesión que "
        "comparar ni flujo que descontar."
    )
    + "\n"
    + fuente_pie(F_OMPI)
)

VALORIZAR_EL_CASO = envolver(
    cabecera("05 · Ejercicio",
             "Valorización del prototipo de colmenas por los tres métodos",
             "i-target")
    + "\n"
    + tabla(
        ["Método", "Cómo se arma el número", "Qué sale"],
        [
            ["Costo", "Horas, materiales, ensayos y tasas ya ejecutados", "El piso"],
            ["Mercado", "Regalía del sector sobre el precio del dispositivo", "Un rango citable"],
            ["Ingresos", "Colmenas × adopción × margen, descontado", "El techo optimista"],
        ],
        "Tabla 5 · Los tres métodos aplicados al mismo activo",
    )
    + "\n"
    + conclusion(
        "Tres números, una posición",
        "Los tres no compiten por acertar: acotan. Sin ninguno se acepta lo que "
        "proponga la otra parte.",
    )
    + "\n"
    + fuente_pie(F_OMPI, F_CASO)
)

BRECHA_PERUANA = envolver(
    cabecera("05 · El contexto",
             "Registro y licencia en la universidad peruana, 2016 y 2025",
             "i-chart")
    + "\n"
    + figura("s5-brecha-peruana",
             "Universidades con política de propiedad intelectual, procedimiento y licencias, 2016",
             "El cuello de botella no está en registrar: está en el paso siguiente, que nadie ha vuelto a medir.")
    + "\n"
    + dato_clave(
        "De las <b>142 universidades</b> del país, unas <b>10</b> tenían "
        "política de propiedad intelectual y solo <b>4</b> procedimiento para "
        "transferir. <b>Ninguna patente había llegado a licenciarse.</b>"
    )
    + "\n"
    + en_la_practica(
        "Una década después el registro se disparó, con 968 solicitudes "
        "universitarias en 2025, y PROCIENCIA financia cinco oficinas de "
        "transferencia. Cuántas patentes se licencian sigue sin publicarse."
    )
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_TABLERO, F_OTT)
)

# ==========================================================================
# CIERRE
# ==========================================================================
VIDEO_RESUMEN = envolver(
    cabecera("Cierre",
             "El video de resumen: tres minutos en cuatro movimientos",
             "i-quote")
    + "\n"
    + fichas([
        ("Cuatro movimientos", "Tres minutos", [
            "Problema con su magnitud · 30 segundos",
            "Qué se construyó, con el prototipo a la vista",
            "Qué se midió, con número y unidad",
            "Qué sigue y qué hace falta",
        ]),
        ("Material grabado durante", "No al final", [
            "Prototipo funcionando, en cada versión",
            "Campo con el beneficiario real",
            "Datos en movimiento, no capturas fijas",
        ]),
        ("Qué lo arruina", "Errores frecuentes", [
            "Empezar por la institución",
            "Imágenes de archivo ajenas al proyecto",
            "Prometer impacto donde hubo producto",
        ]),
    ])
    + "\n"
    + evitar(
        "Dejarlo para el mes dieciocho: el prototipo ya está desmontado y el "
        "campo terminó."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

DOSSIER = envolver(
    cabecera("Cierre",
             "Seis piezas del dossier y el mes en que empieza cada una",
             "i-file")
    + "\n"
    + figura("s5-dossier",
             "Piezas del dossier y mes del proyecto en que empieza a construirse cada una",
             "Ninguna pieza se puede fabricar el último mes: todas se recogen mientras el proyecto ocurre.")
    + "\n"
    + criterio(
        "El dossier no lo pide el fondo: queda del proyecto, y es la materia "
        "prima del <i>pitch</i>."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

ERRORES = envolver(
    cabecera("Cierre",
             "Seis errores frecuentes en la ejecución, uno por tema",
             "i-alert")
    + "\n"
    + fichas([
        ("Presupuesto sin flujo de caja", "Tema 01", [
            "Nadie declaró quién cubre el hueco",
        ]),
        ("Gasto sin entregable", "Tema 02", [
            "Acredita el pago, no la ejecución",
        ]),
        ("Documentar al rendir", "Tema 03", [
            "Sin bitácora no hay fecha que oponer",
        ]),
        ("Publicar antes de solicitar", "Tema 04", [
            "La novedad se pierde y no se repara",
        ]),
        ("Tasas fuera del presupuesto", "Tema 04", [
            "La solicitud entra en abandono",
        ]),
        ("Negociar sin número", "Tema 05", [
            "Se acepta lo que proponga la otra parte",
        ]),
    ])
    + "\n"
    + fuente_pie(F_STARTUP, F_D486, F_OMPI)
)

RESUMEN_FINAL = envolver(
    cabecera("Cierre", "Cinco puntos establecidos sobre presupuesto, ejecución y transferencia", "i-check")
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}Queda establecido</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>La forma del instrumento decide qué se presupuesta, qué se firma, qué se rinde y qué pasa con la propiedad intelectual.</li>
\t\t\t\t\t\t\t<li>El presupuesto se construye de la actividad hacia el monto, y el tope de un rubro no significa nada sin su base de cálculo.</li>
\t\t\t\t\t\t\t<li>El gasto va siempre delante del desembolso: el hueco de caja se declara y se financia, o el proyecto empieza tarde.</li>
\t\t\t\t\t\t\t<li>Documentar es método: sin bitácora, versiones y datos con metadatos no hay prueba de autoría ni historia que contar.</li>
\t\t\t\t\t\t\t<li>La solicitud de registro parte el proyecto en dos, y el trámite dura más que el financiamiento que lo pagó.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-arrow-right")}Lo que se lleva a la sesión 6</h3>
\t\t\t\t\t\t<p>El <b>dossier</b>: expediente, documentación, registros,
\t\t\t\t\t\tpublicaciones, historia y video.</p>
\t\t\t\t\t\t<p>La limitación: hay número de valorización y no hay contraparte.</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_OMPI)
)


def _grupo_glosario(rotulo, entradas, variante=""):
    """Un bloque del glosario por cada tema de la sesión."""
    v = f" gloss-group--{variante}" if variante else ""
    return (f'\t\t\t\t\t<section class="gloss-group{v}">\n'
            f'\t\t\t\t\t\t<h2 class="gloss-group__title">{rotulo}</h2>\n'
            + "\n".join(entradas)
            + "\n\t\t\t\t\t</section>")


GLOSARIO = envolver(
    cabecera("Cierre", "Glosario de presupuesto, ejecución y transferencia", "i-book")
    + "\n"
    + '\t\t\t\t<div class="glossary glossary--grouped" data-animate="fade-up">\n'
    + _grupo_glosario("Presupuesto y ejecución", [
        termino("Partida presupuestal", "budget line",
                "Categoría de gasto reconocida por las bases. Un gasto que no cabe en ninguna partida no es elegible."),
        termino("Hueco de caja", "cash gap",
                "Diferencia acumulada entre el gasto ejecutado y el desembolso recibido. Lo financia el ejecutor."),
    ])
    + "\n"
    + _grupo_glosario("Documentación", [
        termino("Bitácora", "logbook",
                "Registro fechado de lo que se hizo y por qué. Primera capa de la documentación y prueba de autoría."),
        termino("Fecha cierta", "verifiable date",
                "Momento cuya existencia respalda un tercero o un mecanismo verificable, no la palabra del firmante."),
    ], "b")
    + "\n"
    + _grupo_glosario("Registro y transferencia", [
        termino("Examen de fondo", "substantive examination",
                "Revisión de novedad, nivel inventivo y aplicación industrial. Se pide dentro de los seis meses de la publicación."),
        termino("Fecha de prioridad", "priority date",
                "Fecha de la primera solicitud. Desde ella corren los plazos internacionales y contra ella se juzga la novedad."),
        termino("Divulgación habilitante", "enabling disclosure",
                "Comunicación que pone la invención a disposición del público con detalle suficiente para reproducirla."),
        termino("Valorización", "valuation",
                "Estimación del valor de un intangible por costo, mercado o ingresos descontados. Los tres dan números distintos."),
    ])
    + "\n\t\t\t\t</div>"
)

REFERENCIAS = envolver(
    cabecera("Cierre", "Fuentes citadas y vía de acceso a cada una", "i-quote")
    + "\n"
    # Dos tablas porque el constructor admite siete filas y la sesión cita once
    # fuentes. La lámina de referencias no cuenta para el tope de la anatomía.
    + tabla(
        ["Fuente", "Dónde se consulta"],
        [
            ["ProInnóvate · bases de StartUp Perú 12G, 2025",
             '<a href="https://startup.proinnovate.gob.pe">startup.proinnovate.gob.pe</a>'],
            ["PROCIENCIA · bases integradas E072-2024-01-BM, 2024",
             '<a href="https://prociencia.gob.pe">prociencia.gob.pe</a>'],
            ["Decreto Supremo 088-2025-PCM · TUPA del INDECOPI",
             '<a href="https://busquedas.elperuano.pe/dispositivo/NL/2414225-1">busquedas.elperuano.pe</a>'],
            ["Comunidad Andina · Decisión 486",
             '<a href="https://www.wipo.int/wipolex/es/legislation/details/9451">wipolex.wipo.int</a>'],
            ["INDECOPI · Dirección de Invenciones y Nuevas Tecnologías",
             '<a href="https://www.indecopi.gob.pe">indecopi.gob.pe</a>'],
            ["CONCYTEC · ALICIA, repositorio nacional",
             '<a href="https://alicia.concytec.gob.pe">alicia.concytec.gob.pe</a>'],
        ],
        "Tabla 6 · Normas, bases y portales oficiales",
    )
    + "\n"
    + tabla(
        ["Fuente", "Dónde se consulta"],
        [
            ["OMPI (2024) · <i>Intellectual Property Valuation Basics</i>",
             '<a href="https://www.wipo.int/web-publications/intellectual-property-valuation-basics-for-technology-transfer-professionals/en/index.html">wipo.int</a>'],
            ["Aridi, A. y Cowey, L. (2018) · Banco Mundial",
             '<a href="https://documents.worldbank.org">documents.worldbank.org</a>'],
            ["CONCYTEC (2016) · Transferencia y Extensión Tecnológica",
             '<a href="https://portal.concytec.gob.pe">portal.concytec.gob.pe</a>'],
            ["<i>Research Policy</i> (2025) · cláusulas de PI en convenios",
             '<a href="https://doi.org/10.1016/j.respol.2025.105182">doi.org · Research Policy</a>'],
            ["<i>BMJ</i> (2023) · datos y código compartidos · CC BY",
             '<a href="https://doi.org/10.1136/bmj-2023-075767">doi.org/10.1136/bmj-2023-075767</a>'],
        ],
        "Tabla 7 · Literatura y fuentes metodológicas",
    )
)


def L(slug, titulo, nav, icono, contenido, clases="slide", scripts=""):
    return {"slug": slug, "titulo": f"{SESION} · {titulo}", "nav": nav,
            "icono": icono, "clases": clases, "contenido": contenido,
            "scripts": scripts}


LAMINAS = [
    L("portada", "Portada", "Portada", "i-project", PORTADA, "slide slide--start"),
    L("agenda", "Contenidos de los cinco temas y las cinco paradas de herramientas", "Agenda", "i-flow", AGENDA),
    L("costo-medios", "Costo de los cuatro medios de verificación del caso, en soles", "Costo de los medios", "i-scale", COSTO_MEDIOS),

    L("tema-01", TEMA_A, "Tema 01", "i-fund", SECCION_A),
    L("instrumento-obligacion", "Seis formas de instrumento y las seis obligaciones de cada una", "Instrumento y obligación", "i-rubric", INSTRUMENTO_OBLIGACION),
    L("actividad-partida", "Los cuatro pasos del costeo, de la actividad al monto", "De la actividad al monto", "i-flow", ACTIVIDAD_PARTIDA),
    L("partidas-admisibles", "Seis partidas admisibles y su tope en StartUp Perú y PROCIENCIA", "Partidas admisibles", "i-layers", PARTIDAS_ADMISIBLES),
    L("partidas-no-admisibles", "Tres familias de gasto no elegible en un fondo público", "Gastos no elegibles", "i-alert", PARTIDAS_NO_ADMISIBLES),
    L("topes-rubro", "Cuatro topes por rubro y la base sobre la que se calculan", "Topes por rubro", "i-scale", TOPES_RUBRO),
    L("herramientas-01", "Herramientas 01 · Costeo y presupuesto del proyecto", "Herramientas 01", "i-sliders", HERR_01),
    L("partida-pi-difusion", "La partida de propiedad intelectual y difusión: 5 % del capital semilla", "Partida de PI", "i-target", PARTIDA_PI_DIFUSION),
    L("contrapartida-figura", "Contrapartida exigida a tres figuras de postulante, en porcentaje", "Contrapartida", "i-chart", CONTRAPARTIDA_FIGURA),
    L("ficha-startup", "Condiciones económicas de StartUp Perú 12G, convocatoria 2025", "El instrumento", "i-fund", FICHA_STARTUP),
    L("desembolso-hitos", "Momento del desembolso en cuatro formas de instrumento", "Desembolso", "i-gantt", DESEMBOLSO_HITOS),
    L("flujo-caja", "Hueco de caja de un proyecto de dieciocho meses, en miles de soles", "Flujo de caja", "i-chart", FLUJO_CAJA),
    L("presupuesto-simulador", "Simulación: honorarios, tope del 40 % y saldo del capital semilla", "Simular el presupuesto", "i-sliders", PRESUPUESTO_SIM, "slide", PRESUPUESTO_JS),

    L("tema-02", TEMA_B, "Tema 02", "i-file", SECCION_B),
    L("ciclo-de-vida", "Cuatro etapas del proyecto y diez obligaciones con su mes", "Ciclo de vida", "i-gantt", CICLO_DE_VIDA),
    L("convenio", "Seis cláusulas del convenio que se leen antes de firmar", "El convenio", "i-file", CONVENIO),
    L("antes-del-desembolso", "Condiciones previas al primer desembolso de un fondo público", "Antes de cobrar", "i-milestone", ANTES_DEL_DESEMBOLSO),
    L("herramientas-02", "Herramientas 02 · Seguimiento de hitos y evidencia documental", "Herramientas 02", "i-sliders", HERR_02),
    L("informes", "Cuatro piezas del informe técnico y cuatro del financiero", "Los dos informes", "i-rubric", INFORMES),
    L("sustento", "Cinco requisitos del comprobante que sustenta un gasto", "El comprobante", "i-file", SUSTENTO),
    L("modificaciones", "Cinco modificaciones presupuestales y el trámite de cada una", "Modificaciones", "i-flow", MODIFICACIONES),
    L("cierre-doble", "Duración del cierre técnico y del administrativo, en meses", "Los dos cierres", "i-milestone", CIERRE_DOBLE),
    L("rendicion-simulador", "Simulación: las cuatro condiciones que admiten un gasto", "Simular la rendición", "i-sliders", RENDICION_SIM, "slide", RENDICION_JS),

    L("tema-03", TEMA_C, "Tema 03", "i-book", SECCION_C),
    L("documentar-es-metodo", "Cuatro funciones de la documentación en un proyecto financiado", "Por qué documentar", "i-book", DOCUMENTAR_ES_METODO),
    L("capas-documentacion", "Las seis capas de documentación, de la bitácora al registro", "Las seis capas", "i-layers", CAPAS_DOCUMENTACION),
    L("bitacora", "Fuerza probatoria de cuatro formas de registrar el desarrollo", "La bitácora", "i-scale", BITACORA),
    L("versiones-artefacto", "Cinco artefactos de un prototipo electrónico y cómo se versionan", "Versiones", "i-layers", VERSIONES_ARTEFACTO),
    L("herramientas-03", "Herramientas 03 · Documentación, trazabilidad y repositorios", "Herramientas 03", "i-sliders", HERR_03),
    L("datos-y-metadatos", "Las seis decisiones de un plan de gestión de datos", "Plan de datos", "i-diagram", DATOS_Y_METADATOS),
    L("donde-va-cada-cosa", "Seis clases de material y su repositorio de destino", "Dónde se deposita", "i-network", DONDE_VA_CADA_COSA),
    L("historia-del-proyecto", "La historia del proyecto: qué se recoge, de dónde sale y para qué", "La historia", "i-quote", HISTORIA_DEL_PROYECTO),
    L("datos-abiertos", "Datos y código disponibles: 8 % declarado y 2 % real, 2016-2021", "Datos abiertos", "i-chart", DATOS_ABIERTOS),

    L("tema-04", TEMA_D, "Tema 04", "i-target", SECCION_D),
    L("proteger-antes-publicar", "Antes y después de la solicitud: qué se documenta y qué se divulga", "Proteger y publicar", "i-flow", PROTEGER_ANTES_PUBLICAR),
    L("mapa-registros", "Seis figuras de protección industrial y su vigencia en el Perú", "Mapa de registros", "i-rubric", MAPA_REGISTROS),
    L("tasas-indecopi", "Tasas de registro del TUPA de INDECOPI, vigentes desde julio de 2025", "Cuánto cuesta", "i-fund", TASAS_INDECOPI),
    L("plazos-patente", "Plazos del procedimiento de patente según la Decisión 486", "Plazos del trámite", "i-gantt", PLAZOS_PATENTE),
    L("herramientas-04", "Herramientas 04 · Búsqueda de antecedentes de patente", "Herramientas 04", "i-sliders", HERR_04),
    L("tramite-vs-proyecto", "Dieciocho meses de proyecto frente a cuarenta y dos de trámite", "El desfase", "i-alert", TRAMITE_VS_PROYECTO),
    L("titulos-indecopi", "Universidades peruanas en el ranking de patentes de INDECOPI, 2025", "Quién patenta", "i-chart", TITULOS_INDECOPI),
    L("composicion-solicitudes", "Composición de la solicitud universitaria peruana, 2025", "Invención o utilidad", "i-layers", COMPOSICION_SOLICITUDES),
    L("titularidad-clausulas", "Titularidad de los resultados en un proyecto con fondo público", "Titularidad", "i-file", TITULARIDAD_Y_CLAUSULAS),
    L("articulos", "Cuatro obligaciones de publicación y su costo en el presupuesto", "Publicación", "i-book", ARTICULOS),
    L("congresos", "Cuatro foros de difusión y el mes del proyecto en que caben", "Congresos", "i-network", CONGRESOS),
    L("otros-resultados", "Ocho resultados acreditables y el documento que prueba cada uno", "Otros resultados", "i-layers", OTROS_RESULTADOS),

    L("tema-05", TEMA_E, "Tema 05", "i-diagram", SECCION_E),
    L("que-es-transferir", "Las tres condiciones que hacen posible una transferencia", "Qué es transferir", "i-target", QUE_ES_TRANSFERIR),
    L("abanico-transferencia", "Nueve formas de transferencia, de la publicación a la cesión", "El abanico", "i-diagram", ABANICO),
    L("madurez-via", "Madurez mínima de seis vías de transferencia, en escala TRL", "Madurez y vía", "i-ladder", MADUREZ_VIA),
    L("herramientas-05", "Herramientas 05 · Vigilancia tecnológica y búsqueda de comparables", "Herramientas 05", "i-sliders", HERR_05),
    L("metodos-valorizacion", "Costo, mercado e ingresos: los tres métodos de valorización", "Los tres métodos", "i-scale", METODOS_VALORIZACION),
    L("valorizacion-por-activo", "Método de valorización aplicable a cinco tipos de activo", "Método por activo", "i-rubric", VALORIZACION_POR_ACTIVO),
    L("valorizar-el-caso", "Valorización del prototipo de colmenas por los tres métodos", "Valorizar el caso", "i-target", VALORIZAR_EL_CASO),
    L("brecha-peruana", "Registro y licencia en la universidad peruana, 2016 y 2025", "Registro y licencia", "i-chart", BRECHA_PERUANA),

    L("video-resumen", "El video de resumen: tres minutos en cuatro movimientos", "El video", "i-quote", VIDEO_RESUMEN),
    L("dossier", "Seis piezas del dossier y el mes en que empieza cada una", "El dossier", "i-file", DOSSIER),
    L("errores", "Seis errores frecuentes en la ejecución, uno por tema", "Errores", "i-alert", ERRORES),
    L("queda-establecido", "Cinco puntos establecidos sobre presupuesto, ejecución y transferencia", "Resumen", "i-check", RESUMEN_FINAL),
    L("glosario", "Glosario de presupuesto, ejecución y transferencia", "Glosario", "i-book", GLOSARIO),
    L("referencias", "Fuentes citadas y vía de acceso a cada una", "Referencias", "i-quote", REFERENCIAS),
]

generar_desde({
    "clase": "clase-05",
    "sesion": SESION,
    "laminas": renumerar(LAMINAS),
})
