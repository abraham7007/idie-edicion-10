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
             "Costo de los medios de verificación de la matriz",
             "i-scale")
    + "\n"
    + figura("s5-costo-medios",
             "Costo de obtención de cada medio de verificación del caso",
             "La matriz llegó con sus medios de verificación y sin precio. Ponerles precio es el primer renglón del presupuesto.")
    + "\n"
    + criterio(
        "Un indicador cuyo medio de verificación nadie paga no se mide, y una "
        "fila que no se mide no se rinde. Ponerle precio a la columna de medios "
        "es el primer renglón del presupuesto."
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
             "Obligaciones que impone cada forma de instrumento",
             "i-rubric")
    + "\n"
    + figura("s5-instrumento-obligacion",
             "Seis formas de instrumento frente a seis obligaciones del proyecto financiado",
             "La subvención es la única que exige las seis. El premio no exige ninguna: se gana y se cobra.")
    + "\n"
    + criterio(
        "Antes de escribir una sola partida hay que saber en qué fila está el "
        "proyecto. La fila decide qué documentos existirán, quién los firma y "
        "cuándo terminan las obligaciones."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA, F_TUPA)
)

ACTIVIDAD_PARTIDA = envolver(
    cabecera("01 · Estructura del presupuesto",
             "Cadena de la actividad al monto presupuestado",
             "i-flow")
    + "\n"
    + figura("s5-actividad-partida",
             "Recorrido de una actividad de la matriz hasta su monto en el presupuesto",
             "El presupuesto sale de la matriz hacia abajo. Nunca del monto máximo de la convocatoria hacia arriba.")
    + "\n"
    + evitar(
        "Partir del tope de la convocatoria y repartirlo. El evaluador reconoce "
        "un presupuesto construido al revés porque las partidas son redondas y "
        "ninguna se puede seguir hasta una actividad de la matriz."
    )
    + "\n"
    + fuente_pie(F_CASO, F_STARTUP)
)

PARTIDAS_ADMISIBLES = envolver(
    cabecera("01 · Partidas",
             "Partidas presupuestales admisibles y su tope",
             "i-layers")
    + "\n"
    + fichas([
        ("Honorarios e incentivos", "Equipo del proyecto", [
            "Honorarios del líder y del equipo emprendedor",
            "Incentivo al responsable técnico y a los coinvestigadores",
            "<b>Tope de 40 % del capital semilla en StartUp Perú; 20 % del monto en PROCIENCIA</b>",
        ]),
        ("Materiales e insumos", "Sin tope declarado", [
            "Materia prima para el producto mínimo viable",
            "Insumos de ensayo y suscripción a bases de datos, por el plazo del proyecto",
        ]),
        ("Consultorías especializadas", "Terceros, a suma alzada", [
            "Asesoría de expertos o empresas, nacionales o extranjeras",
            "A todo costo: honorario, pasaje y viático dentro del precio",
        ]),
        ("Servicios tecnológicos", "Terceros y proveedores", [
            "Prototipado, validación, certificación y ensayo",
            "Licencias de terceros y acompañamiento de incubadora",
        ]),
        ("Pasajes y viáticos", "Escala oficial", [
            "Trabajo de campo, capacitación y programas en el extranjero",
            "Por escala oficial y no por gasto real · <b>tope de 8 % en PROCIENCIA</b>",
        ]),
        ("Equipos y bienes duraderos", "Cuando la convocatoria los admite", [
            "Solo los vinculados a la naturaleza del proyecto",
            "No todo concurso abre esta partida, y el destino del bien lo fija el convenio",
        ]),
    ])
    + "\n"
    + criterio(
        "Las partidas y los topes cambian de una convocatoria a otra, y cambian "
        "incluso entre las bases iniciales y las integradas. Lo que no cambia es "
        "que cada gasto tiene que caber en una partida nombrada por las bases."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

PARTIDAS_NO_ADMISIBLES = envolver(
    cabecera("01 · Partidas",
             "Gastos no elegibles en una convocatoria pública",
             "i-alert")
    + "\n"
    + fichas([
        ("Lo que sostiene a la entidad", "No al proyecto", [
            "Personal administrativo y gastos administrativos en general",
            "Luz, agua, telefonía fija y celular, internet",
            "Son gastos que existirían igual sin el proyecto",
        ]),
        ("Lo financiero", "Nunca", [
            "Mantenimiento de cuenta corriente y comisiones",
            "Intereses y deuda previa",
            "Multas y penalidades",
        ]),
        ("Lo patrimonial", "Nunca", [
            "Adquisición o alquiler de inmuebles",
            "Adquisición o alquiler de vehículos",
            "Equipos y bienes no vinculados a la ejecución",
        ]),
    ])
    + "\n"
    + aviso(
        "Un gasto no elegible no se descuenta del cuadro: obliga a rehacerlo "
        "entero en plena evaluación, con el reloj de la convocatoria corriendo."
    )
    + "\n"
    + criterio(
        "La regla que ordena la lista: el fondo paga lo que el proyecto añade, "
        "no lo que la entidad ya sostiene. El sueldo del administrador y la "
        "factura de la luz existirían igual sin el proyecto, y por eso no entran."
    )
    + "\n"
    + en_la_practica(
        "El alquiler de un vehículo no es elegible; el pasaje de campo sí, por "
        "escala. El sensor de peso del prototipo es elegible; un equipo sin "
        "vínculo con el proyecto, no. La frontera es la vinculación."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

TOPES_RUBRO = envolver(
    cabecera("01 · Partidas",
             "Topes porcentuales por rubro y su base de cálculo",
             "i-scale")
    + "\n"
    + figura("s5-topes-rubro",
             "Topes declarados por rubro en dos convocatorias del Estado",
             "El tope no dice nada sin su base: el 40 % es sobre el capital semilla y el 20 % sobre el monto financiado.")
    + "\n"
    + en_la_practica(
        "El 40 % sobre un capital semilla de S/ 60 000 son S/ 24 000 para todo "
        "el equipo y todo el proyecto. Con dos personas a tiempo completo doce "
        "meses el presupuesto no cuadra, y eso se decide antes de postular."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

HERR_01 = bloque_herramientas(
    "01", "05",
    "Costeo y presupuesto del proyecto",
    "Para que el presupuesto salga de la matriz y siga cuadrando cuando el "
    "plan de trabajo cambie. El objetivo no es la plantilla: es que cada monto "
    "quede trazado a una actividad y a una partida.",
    [
        ("LibreOffice Calc", "The Document Foundation", [
            "Hoja de cálculo abierta, sin licencia que renovar ni cuenta que crear",
            "Referencias entre hojas: las actividades alimentan el cuadro de partidas",
            "Guarda en formato abierto, el que exige un anexo verificable",
        ], "libreoffice.org"),
        ("Google Sheets", "Google", [
            "Edición simultánea del equipo sobre el mismo cuadro, con historial de cambios",
            "El historial sirve de prueba de quién cambió qué monto y cuándo",
            "Exporta al formato cerrado que piden casi todas las bases",
        ], "sheets.google.com"),
        ("GanttProject", "Comunidad libre", [
            "Cronograma con dependencias, hitos y ruta crítica",
            "Asigna recurso y costo por tarea, que es la unión entre plan y presupuesto",
            "Exporta el cronograma como anexo, sin rehacerlo a mano",
        ], "ganttproject.biz"),
    ],
    [
        ("Trazabilidad", "que de un monto se llegue a la actividad que lo produce"),
        ("Formato de salida", "que exporte al que piden las bases, sin copiar a mano"),
        ("Historial", "que registre quién cambió qué, y no solo la hoja final"),
    ],
)

PARTIDA_PI_DIFUSION = envolver(
    cabecera("01 · Partidas",
             "Partida de propiedad intelectual y difusión",
             "i-target")
    + "\n"
    + figura("s5-cabe-en-la-partida",
             "Composición de la partida de propiedad intelectual y difusión del caso",
             "Con el tope del 5 % caben una solicitud de patente y el evento de cierre, y poco más.")
    + "\n"
    + fichas([
        ("Registro", "Tasas del TUPA", [
            "Solicitud y examen de fondo de la figura elegida",
            "Búsqueda de antecedentes, si se contrata",
        ]),
        ("Publicación", "Acceso abierto", [
            "Cargo por procesamiento de artículo, si la revista lo cobra",
            "Depósito de datos con identificador",
        ]),
        ("Difusión", "Obligatoria en varias bases", [
            "Evento público de cierre y su material",
            "Inscripción a congreso y material audiovisual",
        ]),
    ])
    + "\n"
    + evitar(
        "Dejar la propiedad intelectual y la difusión fuera del presupuesto. "
        "Después no hay de dónde pagarlas, y el proyecto termina con resultados "
        "sin registrar porque la tasa no estaba en ninguna partida."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_TUPA)
)

CONTRAPARTIDA_FIGURA = envolver(
    cabecera("01 · Contrapartida",
             "Reparto del costo según la figura del postulante",
             "i-chart")
    + "\n"
    + figura("s5-contrapartida-figura",
             "Cofinanciamiento y contrapartida por tipo de entidad postulante",
             "La misma propuesta pide 0 % en efectivo a una entidad pública y 30 % a una universidad privada societaria.")
    + "\n"
    + criterio(
        "Qué es la contrapartida y quién la aporta ya está dado. Aquí solo "
        "queda llenar la tabla: cada aporte comprometido lleva partida, monto y "
        "documento que lo acredita, firmado antes del cierre de la convocatoria."
    )
    + "\n"
    + fuente_pie(F_PROCIENCIA, F_STARTUP)
)

DOS_INSTRUMENTOS = envolver(
    cabecera("01 · Dos instrumentos",
             "Cifras comparadas de dos subvenciones del Estado",
             "i-rubric")
    + "\n"
    + figura("s5-dos-instrumentos",
             "Seis condiciones económicas de StartUp Perú 12G y de PROCIENCIA E072",
             "Ambas son subvenciones y ninguna cifra coincide: el monto varía por un factor de cuarenta y cinco.")
    + "\n"
    + dato_clave(
        "Las bases citadas son las <b>integradas y modificadas</b>: el tope de "
        "recursos humanos subió del 15 % al 20 % y el de viáticos del 5 % al 8 % "
        "respecto de las iniciales. Presupuestar con la primera versión "
        "publicada sale mal."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

DESEMBOLSO_HITOS = envolver(
    cabecera("01 · Desembolso",
             "Cronograma de desembolsos frente a cronograma de actividades",
             "i-gantt")
    + "\n"
    + tabla(
        ["Instrumento", "Cómo entra el dinero", "Qué lo dispara"],
        [
            ["StartUp Perú 12G", "Por hitos negociados en la reunión previa",
             "Hito verificado y aprobado por el ejecutivo del proyecto"],
            ["PROCIENCIA E072", "Hasta 20 % referencial y el saldo en un segundo desembolso",
             "Firma del contrato y avance verificado"],
            ["Beca", "Por armadas, mientras dura el programa",
             "Matrícula vigente y permanencia acreditada"],
            ["Beneficio tributario", "No hay desembolso: se deduce del impuesto",
             "Declaración anual, sobre gasto ya ejecutado"],
        ],
        "Tabla 1 · Momento del desembolso según la forma del instrumento",
    )
    + "\n"
    + criterio(
        "El cronograma de actividades dice cuándo se trabaja y el de desembolsos "
        "cuándo entra el dinero. No coinciden nunca, y la diferencia entre ambos "
        "hay que financiarla por otra vía."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

FLUJO_CAJA = envolver(
    cabecera("01 · Desembolso",
             "Hueco de caja entre el gasto y el desembolso",
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
             "Simulación: efecto de un cambio de actividad en el presupuesto",
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
             "Etapas del proyecto y momento de cada obligación",
             "i-gantt")
    + "\n"
    + figura("s5-ciclo-de-vida",
             "Ciclo de vida del proyecto financiado, con la obligación que entra en cada etapa",
             "Cada cosa tiene su mes. La propiedad intelectual va antes de divulgar y la documentación empieza el primer día.")
    + "\n"
    + criterio(
        "Casi todo lo que se hace tarde se hace tarde por no tener el calendario "
        "delante. Los dos retrasos más caros: documentar cuando hay que rendir, "
        "y pensar en proteger cuando el resultado ya se presentó en un congreso."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_D486, F_CASO)
)

CONVENIO = envolver(
    cabecera("02 · El convenio",
             "Cláusulas del convenio que se leen antes de firmar",
             "i-file")
    + "\n"
    + fichas([
        ("Objeto y entregables", "Qué se comprometió", [
            "El hito comprometido queda fijado aquí, no en la propuesta",
            "Cambiarlo después exige adenda y vuelve a evaluación",
        ]),
        ("Desembolsos y condiciones", "Cuándo entra el dinero", [
            "Qué documento dispara cada tramo",
            "Qué ocurre si un hito se retrasa",
        ]),
        ("Propiedad de los resultados", "Quién será titular", [
            "Titularidad de la propiedad intelectual generada",
            "Reservas del Estado sobre uso y publicación",
        ]),
        ("Destino de los bienes", "Al cerrar", [
            "Qué pasa con el equipo comprado con el fondo",
            "Si se transfiere, a quién y con qué acta",
        ]),
        ("Causales de resolución", "Cuándo se corta", [
            "Incumplimiento de hitos y de rendición",
            "Consecuencia: devolución de lo desembolsado",
        ]),
        ("Confidencialidad", "Qué no se cuenta", [
            "Alcance y plazo de la reserva",
            "Compatibilidad con la obligación de difusión de resultados",
        ]),
    ])
    + "\n"
    + aviso(
        "El convenio no repite la propuesta: la reemplaza. Lo que quedó bien "
        "escrito en el proyecto y mal escrito en el convenio, vale como está en "
        "el convenio."
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
        "En StartUp Perú la <b>reunión previa es obligatoria</b>: sin ella no hay "
        "desembolso. Ahí se ajusta la propuesta y se fija el plan de trabajo con "
        "sus hitos, y después se rinde contra ese plan y no contra la propuesta."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

HERR_02 = bloque_herramientas(
    "02", "05",
    "Seguimiento de hitos y evidencia documental",
    "Para que en el mes catorce se pueda demostrar qué se hizo en el mes tres. "
    "El objetivo no es gestionar el proyecto entero: es que cada hito tenga su "
    "evidencia fechada y localizable.",
    [
        ("Nextcloud", "Comunidad libre", [
            "Almacenamiento propio con historial de versiones por archivo",
            "El historial fecha cada versión, como pide una rendición",
            "Se puede alojar en el servidor de la propia universidad",
        ], "nextcloud.com"),
        ("Zotero", "Corporation for Digital Scholarship", [
            "Guarda la fuente y el documento juntos, con su fecha de consulta",
            "Grupos compartidos: el equipo entero ve el mismo acervo",
            "Exporta la bibliografía en el formato que pida la convocatoria",
        ], "zotero.org"),
        ("Obsidian", "Obsidian.md", [
            "Notas en archivos de texto plano, legibles sin la aplicación",
            "Enlaces entre notas: el hito apunta a la evidencia y al ensayo",
            "Los archivos viven en el disco, así que entran en el control de versiones",
        ], "obsidian.md"),
    ],
    [
        ("Fecha verificable", "que registre cuándo se creó cada cosa, no solo qué dice"),
        ("Salida sin la herramienta", "que el archivo se lea sin el programa"),
        ("Quién más entra", "que el equipo y la entidad accedan sin depender de una persona"),
    ],
)

INFORMES = envolver(
    cabecera("02 · Rendición",
             "Contenido del informe técnico y del informe financiero",
             "i-rubric")
    + "\n"
    + figura("s5-informes",
             "Piezas que exige cada uno de los dos informes de un tramo",
             "No comparten ninguna pieza y se entregan juntos. Uno prueba el resultado, el otro prueba el gasto.")
    + "\n"
    + criterio(
        "El informe técnico se escribe contra hitos, no contra actividades. "
        "«Se realizaron doce visitas» no es un hito: el hito es el documento, el "
        "ensayo o el prototipo que esas visitas produjeron."
    )
    + "\n"
    + fuente_pie(F_STARTUP, F_PROCIENCIA)
)

SUSTENTO = envolver(
    cabecera("02 · Rendición",
             "Requisitos del comprobante que sustenta un gasto",
             "i-file")
    + "\n"
    + tabla(
        ["Qué se presenta", "Qué debe decir", "Por qué se observa"],
        [
            ["Comprobante de pago", "Razón social de la entidad ejecutora, no de una persona",
             "A nombre de un integrante, el gasto no es del proyecto"],
            ["Detalle del bien o servicio", "Concepto que se pueda reconocer en una partida",
             "«Servicios varios» no se puede clasificar ni verificar"],
            ["Fecha", "Posterior al acta de inicio y anterior al cierre del tramo",
             "El gasto previo a la firma no es elegible"],
            ["Constancia de pago", "Transferencia o depósito desde la cuenta del proyecto",
             "El pago en efectivo sin trazabilidad se observa"],
            ["Entregable asociado", "Informe, acta o producto que el gasto produjo",
             "Un servicio pagado sin producto no acredita ejecución"],
        ],
        "Tabla 2 · Qué mira quien revisa un comprobante",
    )
    + "\n"
    + evitar(
        "Guardar los comprobantes para el final del tramo. La factura que falta "
        "aparece siempre, y aparece cuando el proveedor ya no responde."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

MODIFICACIONES = envolver(
    cabecera("02 · Modificaciones",
             "Cambios que se comunican y cambios que se autorizan",
             "i-flow")
    + "\n"
    + figura("s5-modificaciones",
             "Trámite que exige cada tipo de modificación durante la ejecución",
             "El umbral del 5 % separa lo que se comunica de lo que espera autorización antes de gastarse.")
    + "\n"
    + dato_clave(
        "En StartUp Perú, una variación de los recursos no reembolsables "
        "<b>superior al 5 %</b> deja de ser un ajuste y se deriva a la unidad de "
        "evaluación. El umbral se busca en el manual operativo del propio fondo."
    )
    + "\n"
    + fuente_pie(F_STARTUP)
)

CIERRE_DOBLE = envolver(
    cabecera("02 · Cierre",
             "Cierre técnico y cierre administrativo del proyecto",
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
             "Simulación: admisión de un gasto en la rendición",
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
             "Funciones de la documentación en un proyecto financiado",
             "i-book")
    + "\n"
    + fichas([
        ("Probar quién lo hizo", "Frente a una disputa", [
            "Un registro fechado sostiene la autoría cuando alguien la discute",
            "Sin fecha verificable, la palabra de las partes vale lo mismo",
        ]),
        ("Permitir reproducirlo", "Frente a un evaluador", [
            "Un resultado que nadie puede repetir no acredita nada",
            "La documentación técnica convierte un prototipo en producto transferible",
        ]),
        ("Sostener la rendición", "Frente al fondo", [
            "El informe técnico se arma con lo que ya está documentado",
            "Reconstruir el mes tres en el mes catorce cuesta más que anotarlo",
        ]),
        ("Contar la historia", "Frente al siguiente fondo", [
            "La evolución del proyecto es el material del <i>pitch</i>",
            "No se puede fabricar al final: o se recogió durante, o no existe",
        ]),
    ], columnas=2)
    + "\n"
    + criterio(
        "Documentar no es un trámite añadido al trabajo: es parte del método. "
        "Un ensayo sin bitácora es un ensayo que hay que volver a hacer."
    )
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_CASO)
)

CAPAS_DOCUMENTACION = envolver(
    cabecera("03 · Las capas",
             "Capas de la documentación de un proyecto",
             "i-layers")
    + "\n"
    + figura("s5-capas-documentacion",
             "Seis capas de documentación, con la pregunta que responde cada una",
             "Publicar en un repositorio es la quinta capa. Sin las cuatro anteriores no hay nada que publicar.")
    + "\n"
    + evitar(
        "Confundir documentar con subir al repositorio. Un repositorio con el "
        "código final y sin historia no dice qué se probó, qué se descartó ni "
        "cuándo, que es justo lo que se necesita para rendir y para proteger."
    )
    + "\n"
    + fuente_pie(F_CONCYTEC_TT)
)

BITACORA = envolver(
    cabecera("03 · Bitácora",
             "Valor probatorio de cada forma de registro",
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
             "Artefactos de un prototipo electrónico que se versionan",
             "i-layers")
    + "\n"
    + figura("s5-versiones-artefacto",
             "Cinco artefactos del prototipo y la forma de versionar cada uno",
             "El código es uno de los cinco. La placa, la lista de materiales y los ensayos también cambian de versión.")
    + "\n"
    + en_la_practica(
        "La versión 3 del firmware solo tiene sentido junto a la revisión B de la "
        "placa y a la lista de materiales que cambió el sensor de peso. Las tres "
        "por separado y sin referencia cruzada valen lo mismo que ninguna."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

HERR_03 = bloque_herramientas(
    "03", "05",
    "Documentación, trazabilidad y repositorios",
    "Para que el desarrollo quede registrado mientras ocurre y el depósito "
    "final sea citable. Tres herramientas cubren las seis capas: control de "
    "versiones, documento técnico y depósito con identificador.",
    [
        ("Git con GitLab o GitHub", "Comunidad y proveedores", [
            "Cada cambio queda con autor, fecha y motivo, sin esfuerzo adicional",
            "Sirve para firmware, esquemáticos en formato de texto y documentos en Markdown",
            "Las etiquetas de versión marcan qué estado del código corresponde a cada hito",
        ], "about.gitlab.com"),
        ("Zenodo", "CERN y Comisión Europea", [
            "Deposita datos, código y documentos y devuelve un DOI permanente",
            "El DOI hace citable el conjunto y fija su contenido en una fecha",
            "Se enlaza con un repositorio de código para archivar cada versión publicada",
        ], "zenodo.org"),
        ("ALICIA", "CONCYTEC", [
            "Repositorio nacional que recolecta la producción de las instituciones peruanas",
            "Es el destino que varias convocatorias exigen para tesis y artículos",
            "Da visibilidad nacional a lo que en un repositorio propio no se encuentra",
        ], "alicia.concytec.gob.pe"),
    ],
    [
        ("Identificador permanente", "que lo depositado se cite dentro de diez años"),
        ("Qué admite", "que acepte el tipo de archivo real del proyecto, no solo texto"),
        ("Qué exige el financiador", "que el destino sea uno de los que las bases reconocen"),
    ],
)

DATOS_Y_METADATOS = envolver(
    cabecera("03 · Datos",
             "Componentes del plan de gestión de datos",
             "i-diagram")
    + "\n"
    + tabla(
        ["Componente", "Qué declara", "Cuándo se decide"],
        [
            ["Qué datos se producen", "Tipo, volumen y formato de cada conjunto",
             "Al formular, no al terminar"],
            ["Cómo se nombran", "Convención de nombres y estructura de carpetas",
             "Antes del primer ensayo"],
            ["Qué metadatos llevan", "Variables, unidades, instrumento y condiciones",
             "Al cerrar cada ensayo"],
            ["Dónde se depositan", "Repositorio y momento del depósito",
             "Antes de publicar el artículo"],
            ["Con qué licencia", "Qué puede hacer un tercero con ellos",
             "Al depositar, y compatible con el convenio"],
            ["Qué no se abre", "Datos personales o comprometidos por confidencialidad",
             "Al firmar el convenio"],
        ],
        "Tabla 3 · Las seis decisiones de un plan de gestión de datos",
    )
    + "\n"
    + criterio(
        "Un dato sin unidad, sin instrumento y sin condiciones de medida no es "
        "un dato: es una columna de números. La diferencia se decide al "
        "registrarlo, no al depositarlo."
    )
    + "\n"
    + fuente_pie(F_DATOS_FIN, F_CASO)
)

DONDE_VA_CADA_COSA = envolver(
    cabecera("03 · Depósito",
             "Destino de cada clase de material producido",
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
             "Construcción de la historia del proyecto",
             "i-quote")
    + "\n"
    + fichas([
        ("Qué se recoge", "Durante, no al final", [
            "La decisión que cambió el rumbo, con su fecha y su motivo",
            "El ensayo que salió mal y lo que enseñó",
            "La versión del prototipo antes y después de cada hito",
        ]),
        ("De dónde sale", "De la bitácora", [
            "La bitácora ya tiene las fechas y los motivos",
            "El control de versiones ya tiene el antes y el después",
            "No hay que escribir nada nuevo: hay que seleccionar",
        ]),
        ("Para qué sirve", "Después del cierre", [
            "Es el material del <i>pitch</i> ante un comité",
            "Distingue la propuesta siguiente de un formulario",
            "Convence a un socio de que el equipo ejecuta",
        ]),
    ])
    + "\n"
    + evitar(
        "Escribir la historia el último mes. Lo que queda entonces es el "
        "cronograma cumplido, que no es una historia: es un calendario."
    )
    + "\n"
    + criterio(
        "Una historia de proyecto tiene tres piezas: dónde estaba el equipo al "
        "empezar, qué decisión cambió el rumbo y qué quedó demostrado al final. "
        "Las tres salen de la bitácora si la bitácora existe."
    )
    + "\n"
    + ejemplo(
        "«En el mes cuatro el sensor de peso derivaba con la temperatura. Se "
        "cambió el montaje y se añadió compensación por firmware, y el error "
        "bajó de 180 a 25 gramos.» Eso es historia: hay antes, decisión y "
        "después, con número."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

DATOS_ABIERTOS = envolver(
    cabecera("03 · Datos abiertos",
             "Distancia entre declarar y compartir datos",
             "i-chart")
    + "\n"
    + figura("s5-datos-compartidos",
             "Disponibilidad declarada y disponibilidad real de datos y código, 2016-2021",
             "Ocho de cada cien artículos declaran datos disponibles y dos los tienen de verdad.")
    + "\n"
    + dato_clave(
        "La revisión reúne <b>105 estudios sobre 2 121 580 artículos</b> de 31 "
        "especialidades. La disponibilidad declarada es del 8 % y la real del "
        "2 %; el código llega a menos del 0,5 % desde 2016."
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
             "Orden entre la solicitud de registro y la divulgación",
             "i-flow")
    + "\n"
    + figura("s5-proteger-antes-publicar",
             "Actividades admisibles antes y después de presentar la solicitud",
             "La fecha de solicitud parte el proyecto en dos. Antes se documenta; después se cuenta.")
    + "\n"
    + criterio(
        "Por qué la divulgación previa destruye la novedad ya está dado. Aquí se "
        "decide <b>cuándo</b>, y la respuesta cabe en una fecha: la de la "
        "solicitud, que entra en el cronograma como un hito más."
    )
    + "\n"
    + fuente_pie(F_D486, F_CASO)
)

MAPA_REGISTROS = envolver(
    cabecera("04 · Registros",
             "Figuras de protección disponibles y su vigencia",
             "i-rubric")
    + "\n"
    + figura("s5-mapa-registros",
             "Seis figuras de protección, qué protege cada una y cuánto dura",
             "Cinco se registran ante INDECOPI. El secreto empresarial no se registra y dura mientras se guarde.")
    + "\n"
    + en_la_practica(
        "El prototipo admite varias figuras a la vez: circuito y método de medida "
        "a patente o modelo de utilidad, carcasa a diseño industrial, firmware a "
        "derecho de autor y algoritmo de alerta como secreto."
    )
    + "\n"
    + fuente_pie(F_D486, F_INDECOPI)
)

TASAS_INDECOPI = envolver(
    cabecera("04 · Costo",
             "Tasas de registro de propiedad industrial",
             "i-fund")
    + "\n"
    + figura("s5-tasas-indecopi",
             "Tasa de solicitud y de examen de fondo por tipo de registro, en soles",
             "El modelo de utilidad cuesta la mitad que la patente y protege diez años en lugar de veinte.")
    + "\n"
    + dato_clave(
        "El TUPA del <b>Decreto Supremo 088-2025-PCM</b>, vigente desde el 1 de "
        "julio de 2025, redujo la solicitud de patente un 45 % y su examen de "
        "fondo un 41 %; en modelo de utilidad, un 30 % y un 65 %."
    )
    + "\n"
    + aviso(
        "Las tasas no son el costo total. A ellas se suman la redacción de la "
        "memoria descriptiva y las reivindicaciones, que es donde se decide si la "
        "patente sirve, y las anualidades de mantenimiento durante toda la vigencia."
    )
    + "\n"
    + fuente_pie(F_TUPA)
)

PLAZOS_PATENTE = envolver(
    cabecera("04 · Plazos",
             "Plazos del procedimiento de patente en el Perú",
             "i-gantt")
    + "\n"
    + figura("s5-plazos-patente",
             "Etapas del procedimiento de patente y su plazo según la Decisión 486",
             "Dieciocho meses de confidencialidad, sesenta días para oponerse y seis meses para pedir el examen.")
    + "\n"
    + criterio(
        "Los plazos los fija la Decisión 486 de la Comunidad Andina, que rige "
        "igual en Perú, Colombia, Ecuador y Bolivia. Dos guías comerciales daban "
        "plazos de oposición distintos; el artículo 42 dice sesenta días."
    )
    + "\n"
    + fuente_pie(F_D486)
)

HERR_04 = bloque_herramientas(
    "04", "05",
    "Búsqueda de antecedentes de patente",
    "Para comprobar la novedad antes de pagar la tasa. Una búsqueda que "
    "encuentra el antecedente ahorra el trámite entero; hecha después, solo "
    "sirve para entender por qué se denegó.",
    [
        ("Espacenet", "Oficina Europea de Patentes", [
            "Más de cien millones de documentos de patente de todo el mundo",
            "Búsqueda por clasificación internacional, que es como buscan los examinadores",
            "Muestra en qué países está protegida la misma invención",
        ], "worldwide.espacenet.com"),
        ("Patentscope", "OMPI", [
            "Cubre las solicitudes internacionales del PCT y las colecciones nacionales",
            "Busca en el texto completo, no solo en título y resumen",
            "Traduce la consulta a varios idiomas, útil cuando el antecedente es asiático",
        ], "patentscope.wipo.int"),
        ("Buscador de INDECOPI", "INDECOPI", [
            "Consulta las solicitudes y los títulos concedidos en el Perú",
            "Muestra el estado del expediente, no solo el documento final",
            "Es la fuente que hay que citar cuando el antecedente es peruano",
        ], "servicio.indecopi.gob.pe"),
    ],
    [
        ("Cobertura", "que incluya la jurisdicción donde se quiere proteger"),
        ("Qué campo busca", "que llegue al texto completo, no solo al título"),
        ("Estado del expediente", "que diga si la solicitud sigue viva o está abandonada"),
    ],
)

TRAMITE_VS_PROYECTO = envolver(
    cabecera("04 · El desfase",
             "Duración del trámite frente a la duración del proyecto",
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
             "Títulos de propiedad industrial otorgados en el Perú",
             "i-chart")
    + "\n"
    + figura("s5-titulos-indecopi",
             "Títulos otorgados en 2025 y sectores donde se concentran",
             "Mil cuarenta y siete títulos, máximo histórico, concentrados en cuatro sectores.")
    + "\n"
    + criterio(
        "La cifra calibra en dos direcciones. Hacia arriba: el sistema concede "
        "más que nunca. Hacia abajo: mil títulos al año en un país de treinta y "
        "tres millones deja poco antecedente nacional con el que chocar."
    )
    + "\n"
    + fuente_pie(F_INDECOPI)
)

TITULARIDAD_Y_CLAUSULAS = envolver(
    cabecera("04 · Titularidad",
             "Titularidad de los resultados en un proyecto con fondo público",
             "i-file")
    + "\n"
    + fichas([
        ("Las bases del concurso", "Antes de postular", [
            "Quién queda como titular y qué se reserva el Estado",
            "Qué obligación de explotación aparece, y en qué plazo",
        ]),
        ("El convenio", "Antes de firmar", [
            "El reparto entre entidad ejecutora y entidad asociada",
            "Quién decide sobre solicitar, licenciar o abandonar",
        ]),
        ("Lo que se pacta de verdad", "<i>Research Policy</i>, 2025", [
            "Titularidad y libertad de divulgar se negocian juntas",
            "El plazo de reserva de publicación es la cláusula que más afecta a una tesis",
        ]),
    ])
    + "\n"
    + criterio(
        "Antes de firmar hay que saber quién podrá publicar y cuándo. Un plazo "
        "de reserva de dieciocho meses no impide la tesis, pero decide en qué "
        "año se sustenta, y eso no se negocia después."
    )
    + "\n"
    + aviso(
        "Dónde se fija la titularidad ya está dado: reglamento, convenio o "
        "acuerdo de cesión. Con fondo público hay un cuarto documento por encima "
        "de los tres, y son las bases del concurso."
    )
    + "\n"
    + fuente_pie(F_PI_CONVENIOS, F_STARTUP, F_PROCIENCIA)
)

ARTICULOS = envolver(
    cabecera("04 · Publicación",
             "Requisitos de publicación de un proyecto financiado",
             "i-book")
    + "\n"
    + tabla(
        ["Qué exige", "Quién lo exige", "Qué implica en el presupuesto"],
        [
            ["Publicar en acceso abierto", "Varias agencias financiadoras",
             "Cargo por procesamiento del artículo, si la revista lo cobra"],
            ["Depositar en el repositorio nacional", "Normativa peruana de acceso libre",
             "Sin costo, pero exige la versión y los metadatos correctos"],
            ["Reconocer al financiador", "Todas las bases",
             "Ninguno: una línea de agradecimiento con el código del proyecto"],
            ["Depositar los datos asociados", "Cada vez más revistas y agencias",
             "Depósito con identificador persistente y curaduría de metadatos"],
        ],
        "Tabla 4 · Obligaciones de publicación y su reflejo en el presupuesto",
    )
    + "\n"
    + en_la_practica(
        "El artículo se escribe después de la solicitud de registro y antes del "
        "cierre administrativo. Publicado después del cierre, el informe final "
        "ya no lo puede recoger, aunque sea el mismo trabajo."
    )
    + "\n"
    + fuente_pie(F_ALICIA, F_DATOS_FIN)
)

CONGRESOS = envolver(
    cabecera("04 · Difusión",
             "Foro de difusión según la madurez del resultado",
             "i-network")
    + "\n"
    + figura("s5-congresos-momento",
             "Momento del proyecto en que cabe cada foro de difusión",
             "El póster, la ponencia y la demostración exigen madurez distinta, y ninguno va antes de la solicitud.")
    + "\n"
    + evitar(
        "Llevar el prototipo a una feria antes de presentar la solicitud. Una "
        "demostración pública con el dispositivo funcionando es divulgación "
        "habilitante: pone la invención a disposición del público y con eso "
        "termina la novedad."
    )
    + "\n"
    + fuente_pie(F_D486, F_CASO)
)

OTROS_RESULTADOS = envolver(
    cabecera("04 · Resultados",
             "Resultados acreditables de un proyecto y su prueba",
             "i-layers")
    + "\n"
    + figura("s5-resultados-tipos",
             "Ocho clases de resultado y el documento que acredita cada una",
             "Un proyecto produce más de un resultado, y cada uno se prueba con un documento distinto.")
    + "\n"
    + criterio(
        "La alianza formada durante el proyecto también es un resultado y se "
        "acredita igual: con un convenio firmado que declare objeto y plazo. Sin "
        "documento no entra en el informe final ni sirve para la propuesta siguiente."
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
             "Condiciones que hacen posible una transferencia",
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
        "Las tres condiciones son acumulativas y la que más falla es la tercera. "
        "Un resultado protegido y bien documentado sin receptor capaz de "
        "absorberlo se queda en el expediente, que es exactamente lo que "
        "describe el embudo peruano."
    )
    + "\n"
    + fichas([
        ("Resultado protegido", "O deliberadamente abierto", [
            "Sin titularidad clara no hay nada que licenciar",
            "Abrir también es una decisión, y hay que tomarla, no omitirla",
        ]),
        ("Documentación suficiente", "Lo de la capa tres", [
            "El receptor tiene que poder reproducirlo sin el equipo original",
            "Un prototipo sin documentación se transfiere con las personas o no se transfiere",
        ]),
        ("Receptor con capacidad", "De absorberlo", [
            "Alguien que pueda fabricar, operar o comercializar lo recibido",
            "Sin capacidad de absorción, la licencia se firma y no pasa nada",
        ]),
    ])
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_BM)
)

ABANICO = envolver(
    cabecera("05 · Alternativas",
             "Formas de transferencia y de intercambio de conocimiento",
             "i-diagram")
    + "\n"
    + figura("s5-abanico-transferencia",
             "Espectro de nueve formas de transferencia, de menor a mayor control cedido",
             "La licencia y la <i>spin-off</i> son dos de nueve. Las otras siete también transfieren y ceden menos.")
    + "\n"
    + criterio(
        "Licencia, <i>spin-off</i> y empresa independiente ocupan su lugar en el "
        "espectro. La figura añade las formas que casi nadie cuenta como "
        "transferencia: consultoría, uso de equipos, investigación por encargo "
        "y apertura deliberada."
    )
    + "\n"
    + fuente_pie(F_BM, F_CONCYTEC_TT)
)

MADUREZ_VIA = envolver(
    cabecera("05 · Madurez",
             "Madurez mínima que exige cada vía de transferencia",
             "i-ladder")
    + "\n"
    + figura("s5-madurez-via",
             "Nivel de madurez tecnológica desde el que admite cada vía de transferencia",
             "Por debajo del nivel cuatro casi nadie licencia: lo que se transfiere entonces es trabajo, no tecnología.")
    + "\n"
    + en_la_practica(
        "El prototipo, validado en campo con una asociación de productores, entra "
        "en el tramo donde la licencia no exclusiva empieza a ser posible. La "
        "cesión y la <i>spin-off</i> piden un nivel más y un receptor identificado."
    )
    + "\n"
    + fuente_pie(F_BM, F_CASO)
)

HERR_05 = bloque_herramientas(
    "05", "05",
    "Vigilancia tecnológica y búsqueda de comparables",
    "Para poner un número antes de negociar. El método de mercado necesita "
    "operaciones comparables y el de ingresos necesita tamaño de mercado: sin "
    "una fuente para cada cosa, la valorización es una opinión.",
    [
        ("Espacenet y Patentscope", "EPO y OMPI", [
            "Vigilancia de quién patenta en el campo y con qué frecuencia",
            "Los titulares que más solicitan son los primeros candidatos a licenciatario",
            "La familia de patentes indica en qué mercados se juega la tecnología",
        ], "worldwide.espacenet.com"),
        ("OpenAlex", "OurResearch", [
            "Base abierta de producción científica, con instituciones y financiadores",
            "Permite ver qué grupos trabajan el mismo problema y con quién colaboran",
            "Acceso libre y descargable, sin suscripción institucional",
        ], "openalex.org"),
        ("Datos abiertos de INEI y de gremios", "Fuentes nacionales", [
            "Tamaño del mercado peruano, el dato que pide el método de ingresos",
            "Series oficiales con año y unidad, citables en la propuesta",
            "Los gremios publican precios y volúmenes que la estadística general omite",
        ], "inei.gob.pe"),
    ],
    [
        ("Qué comparable devuelve", "que dé operaciones o magnitudes, no solo documentos"),
        ("Acceso sostenido", "que se vuelva a consultar sin suscripción, para actualizar"),
        ("Trazabilidad del dato", "que cada cifra tenga año, unidad y fuente citable"),
    ],
)

METODOS_VALORIZACION = envolver(
    cabecera("05 · Valorización",
             "Métodos de valorización de un activo intangible",
             "i-scale")
    + "\n"
    + figura("s5-metodos-valorizacion",
             "Los tres métodos de valorización, sus datos y su punto débil",
             "Ninguno da el valor: cada uno da un número distinto, y el rango entre ellos es la posición de negociación.")
    + "\n"
    + dato_clave(
        "El método de costo <b>ignora el valor futuro</b>. El de mercado necesita "
        "comparables que casi nunca existen. El de ingresos depende de una tasa "
        "de descuento que para una <i>spin-off</i> universitaria no es la de una "
        "empresa cotizada."
    )
    + "\n"
    + fuente_pie(F_OMPI)
)

VALORIZACION_POR_ACTIVO = envolver(
    cabecera("05 · Valorización",
             "Método aplicable según el tipo de activo",
             "i-rubric")
    + "\n"
    + figura("s5-valorizacion-por-activo",
             "Aplicabilidad de cada método de valorización según el tipo de activo",
             "El secreto empresarial y la base de datos no tienen comparables: el método de mercado no aplica.")
    + "\n"
    + criterio(
        "Una solicitud en trámite se valoriza casi siempre por costo: no hay "
        "concesión que comparar ni flujo que descontar con confianza. Una patente "
        "concedida en sector activo admite mercado e ingresos."
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
            ["Costo", "Horas de desarrollo, materiales, ensayos y tasas de registro ya ejecutados",
             "Un piso: nadie lo cede por menos de lo que costó"],
            ["Mercado", "Regalía habitual del sector sobre el precio del dispositivo, si se encuentra comparable",
             "Un rango, y una fuente que citar en la negociación"],
            ["Ingresos", "Colmenas en producción × tasa de adopción × margen, descontado y ajustado por riesgo",
             "Un techo optimista, con toda la incertidumbre de la cadena"],
        ],
        "Tabla 5 · Los tres métodos aplicados al mismo activo",
    )
    + "\n"
    + conclusion(
        "Tres números, una posición",
        "Los tres métodos no compiten por acertar: acotan. El de costo pone el "
        "piso, el de ingresos el techo y el de mercado dice qué se ha pagado por "
        "algo parecido. Negociar sin ninguno de los tres es aceptar lo que "
        "proponga la otra parte.",
    )
    + "\n"
    + fuente_pie(F_OMPI, F_CASO)
)

BRECHA_PERUANA = envolver(
    cabecera("05 · El contexto",
             "Embudo de la transferencia en la universidad peruana",
             "i-chart")
    + "\n"
    + figura("s5-brecha-peruana",
             "Universidades peruanas con política de propiedad intelectual, procedimiento y licencias",
             "El cuello de botella no está en patentar: está en el paso siguiente, que casi nadie da.")
    + "\n"
    + dato_clave(
        "De las <b>142 universidades</b> del país, unas <b>10</b> tenían política "
        "de propiedad intelectual y solo <b>4</b> procedimiento para transferir. "
        "<b>Ninguna patente había llegado a licenciarse</b>. Datos de 2016."
    )
    + "\n"
    + conclusion(
        "El hueco está después del registro",
        "Registrar es el paso que el sistema ya sabe dar y que las tasas "
        "reducidas favorecen. Falta el siguiente: valorizar, encontrar receptor "
        "y negociar. Ninguna estadística nacional lo mide todavía.",
    )
    + "\n"
    + fuente_pie(F_CONCYTEC_TT, F_INDECOPI)
)

# ==========================================================================
# CIERRE
# ==========================================================================
VIDEO_RESUMEN = envolver(
    cabecera("Cierre",
             "Estructura del video de resumen del proyecto",
             "i-quote")
    + "\n"
    + fichas([
        ("Qué cuenta", "Tres minutos, cuatro movimientos", [
            "El problema con su magnitud y su afectado nombrado",
            "Qué se construyó y cómo funciona, con el prototipo a la vista",
            "Qué se midió, con el número y su unidad",
            "Qué sigue, y qué hace falta para que siga",
        ]),
        ("Qué material exige", "Grabado durante, no al final", [
            "Prototipo funcionando, en cada versión",
            "Trabajo de campo con el beneficiario real",
            "El equipo trabajando, no posando",
            "Pantallas y datos en movimiento, no capturas fijas",
        ]),
        ("Qué lo arruina", "Errores frecuentes", [
            "Empezar por la institución y no por el problema",
            "Locución sobre imágenes de archivo que no son del proyecto",
            "Prometer impacto donde solo hubo producto",
        ]),
    ])
    + "\n"
    + evitar(
        "Dejar el video para el último mes. En el mes dieciocho el prototipo ya "
        "está desmontado, el campo terminó y lo único grabable es una persona "
        "hablando frente a una pared."
    )
    + "\n"
    + criterio(
        "El video no es difusión decorativa: en varias convocatorias el evento "
        "público de cierre es obligatorio y sale de una partida con tope. "
        "Grabarlo entra en el cronograma como cualquier otro hito."
    )
    + "\n"
    + dato_clave(
        "Tres minutos es el formato que aguantan tanto un comité como una feria. "
        "De esos tres minutos, el problema ocupa treinta segundos y el resto se "
        "reparte entre lo que se construyó y lo que se midió."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

DOSSIER = envolver(
    cabecera("Cierre",
             "Piezas del dossier final del proyecto",
             "i-file")
    + "\n"
    + figura("s5-dossier",
             "Piezas del dossier y mes del proyecto en que empieza a construirse cada una",
             "Ninguna pieza se puede fabricar el último mes: todas se recogen mientras el proyecto ocurre.")
    + "\n"
    + criterio(
        "El dossier no lo pide el fondo: queda del proyecto cuando el expediente "
        "se cierra, y es la materia prima del <i>Pitch Elevator</i> y de la "
        "propuesta siguiente."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

ERRORES = envolver(
    cabecera("Cierre",
             "Errores frecuentes en la ejecución de un proyecto financiado",
             "i-alert")
    + "\n"
    + fichas([
        ("Presupuesto sin flujo de caja", "Tema 01", [
            "El gasto va delante del desembolso y nadie declaró quién cubre el hueco",
            "El primer hito se retrasa y con él todo el cronograma",
        ]),
        ("Gasto sin entregable", "Tema 02", [
            "El comprobante acredita el pago y no la ejecución",
            "El tramo se observa y con él se detiene el desembolso siguiente",
        ]),
        ("Documentar al rendir", "Tema 03", [
            "Reconstruir el mes tres en el mes catorce cuesta más y prueba menos",
            "Sin bitácora no hay historia del proyecto ni fecha que oponer",
        ]),
        ("Publicar antes de solicitar", "Tema 04", [
            "La divulgación previa destruye la novedad y no admite reparación",
            "Una demostración en feria cuenta como divulgación",
        ]),
        ("Tasas fuera del presupuesto", "Tema 04", [
            "El trámite sobrevive al proyecto y las anualidades siguen corriendo",
            "La solicitud entra en abandono por una tasa que nadie previó",
        ]),
        ("Negociar sin número", "Tema 05", [
            "Sin valorización se acepta lo que la otra parte proponga",
            "Los tres métodos acotan: piso, techo y precedente",
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
\t\t\t\t\t\t<p>El <b>dossier del proyecto</b>: expediente, documentación,
\t\t\t\t\t\tregistros, publicaciones, historia y video. Aquí se produce
\t\t\t\t\t\ty en la siguiente se defiende ante un comité.</p>
\t\t\t\t\t\t<p>La limitación que se arrastra: hay un número de valorización y
\t\t\t\t\t\tno hay contraparte. Encontrar receptor y negociar con él no lo mide
\t\t\t\t\t\ttodavía ninguna estadística peruana.</p>
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
    L("costo-medios", "Costo de los medios de verificación de la matriz", "Costo de los medios", "i-scale", COSTO_MEDIOS),

    L("tema-01", TEMA_A, "Tema 01", "i-fund", SECCION_A),
    L("instrumento-obligacion", "Obligaciones que impone cada forma de instrumento", "Instrumento y obligación", "i-rubric", INSTRUMENTO_OBLIGACION),
    L("actividad-partida", "Cadena de la actividad al monto presupuestado", "De la actividad al monto", "i-flow", ACTIVIDAD_PARTIDA),
    L("partidas-admisibles", "Partidas presupuestales admisibles y su tope", "Partidas admisibles", "i-layers", PARTIDAS_ADMISIBLES),
    L("partidas-no-admisibles", "Gastos no elegibles en una convocatoria pública", "Gastos no elegibles", "i-alert", PARTIDAS_NO_ADMISIBLES),
    L("topes-rubro", "Topes porcentuales por rubro y su base de cálculo", "Topes por rubro", "i-scale", TOPES_RUBRO),
    L("herramientas-01", "Herramientas 01 · Costeo y presupuesto del proyecto", "Herramientas 01", "i-sliders", HERR_01),
    L("partida-pi-difusion", "Partida de propiedad intelectual y difusión", "Partida de PI", "i-target", PARTIDA_PI_DIFUSION),
    L("contrapartida-figura", "Reparto del costo según la figura del postulante", "Contrapartida", "i-chart", CONTRAPARTIDA_FIGURA),
    L("dos-instrumentos", "Cifras comparadas de dos subvenciones del Estado", "Dos instrumentos", "i-rubric", DOS_INSTRUMENTOS),
    L("desembolso-hitos", "Cronograma de desembolsos frente a cronograma de actividades", "Desembolso", "i-gantt", DESEMBOLSO_HITOS),
    L("flujo-caja", "Hueco de caja entre el gasto y el desembolso", "Flujo de caja", "i-chart", FLUJO_CAJA),
    L("presupuesto-simulador", "Simulación: efecto de un cambio de actividad en el presupuesto", "Simular el presupuesto", "i-sliders", PRESUPUESTO_SIM, "slide", PRESUPUESTO_JS),

    L("tema-02", TEMA_B, "Tema 02", "i-file", SECCION_B),
    L("ciclo-de-vida", "Etapas del proyecto y momento de cada obligación", "Ciclo de vida", "i-gantt", CICLO_DE_VIDA),
    L("convenio", "Cláusulas del convenio que se leen antes de firmar", "El convenio", "i-file", CONVENIO),
    L("antes-del-desembolso", "Condiciones previas al primer desembolso de un fondo público", "Antes de cobrar", "i-milestone", ANTES_DEL_DESEMBOLSO),
    L("herramientas-02", "Herramientas 02 · Seguimiento de hitos y evidencia documental", "Herramientas 02", "i-sliders", HERR_02),
    L("informes", "Contenido del informe técnico y del informe financiero", "Los dos informes", "i-rubric", INFORMES),
    L("sustento", "Requisitos del comprobante que sustenta un gasto", "El comprobante", "i-file", SUSTENTO),
    L("modificaciones", "Cambios que se comunican y cambios que se autorizan", "Modificaciones", "i-flow", MODIFICACIONES),
    L("cierre-doble", "Cierre técnico y cierre administrativo del proyecto", "Los dos cierres", "i-milestone", CIERRE_DOBLE),
    L("rendicion-simulador", "Simulación: admisión de un gasto en la rendición", "Simular la rendición", "i-sliders", RENDICION_SIM, "slide", RENDICION_JS),

    L("tema-03", TEMA_C, "Tema 03", "i-book", SECCION_C),
    L("documentar-es-metodo", "Funciones de la documentación en un proyecto financiado", "Por qué documentar", "i-book", DOCUMENTAR_ES_METODO),
    L("capas-documentacion", "Capas de la documentación de un proyecto", "Las seis capas", "i-layers", CAPAS_DOCUMENTACION),
    L("bitacora", "Valor probatorio de cada forma de registro", "La bitácora", "i-scale", BITACORA),
    L("versiones-artefacto", "Artefactos de un prototipo electrónico que se versionan", "Versiones", "i-layers", VERSIONES_ARTEFACTO),
    L("herramientas-03", "Herramientas 03 · Documentación, trazabilidad y repositorios", "Herramientas 03", "i-sliders", HERR_03),
    L("datos-y-metadatos", "Componentes del plan de gestión de datos", "Plan de datos", "i-diagram", DATOS_Y_METADATOS),
    L("donde-va-cada-cosa", "Destino de cada clase de material producido", "Dónde se deposita", "i-network", DONDE_VA_CADA_COSA),
    L("historia-del-proyecto", "Construcción de la historia del proyecto", "La historia", "i-quote", HISTORIA_DEL_PROYECTO),
    L("datos-abiertos", "Distancia entre declarar y compartir datos", "Datos abiertos", "i-chart", DATOS_ABIERTOS),

    L("tema-04", TEMA_D, "Tema 04", "i-target", SECCION_D),
    L("proteger-antes-publicar", "Orden entre la solicitud de registro y la divulgación", "Proteger y publicar", "i-flow", PROTEGER_ANTES_PUBLICAR),
    L("mapa-registros", "Figuras de protección disponibles y su vigencia", "Mapa de registros", "i-rubric", MAPA_REGISTROS),
    L("tasas-indecopi", "Tasas de registro de propiedad industrial", "Cuánto cuesta", "i-fund", TASAS_INDECOPI),
    L("plazos-patente", "Plazos del procedimiento de patente en el Perú", "Plazos del trámite", "i-gantt", PLAZOS_PATENTE),
    L("herramientas-04", "Herramientas 04 · Búsqueda de antecedentes de patente", "Herramientas 04", "i-sliders", HERR_04),
    L("tramite-vs-proyecto", "Duración del trámite frente a la duración del proyecto", "El desfase", "i-alert", TRAMITE_VS_PROYECTO),
    L("titulos-indecopi", "Títulos de propiedad industrial otorgados en el Perú", "Títulos otorgados", "i-chart", TITULOS_INDECOPI),
    L("titularidad-clausulas", "Titularidad de los resultados en un proyecto con fondo público", "Titularidad", "i-file", TITULARIDAD_Y_CLAUSULAS),
    L("articulos", "Requisitos de publicación de un proyecto financiado", "Publicación", "i-book", ARTICULOS),
    L("congresos", "Foro de difusión según la madurez del resultado", "Congresos", "i-network", CONGRESOS),
    L("otros-resultados", "Resultados acreditables de un proyecto y su prueba", "Otros resultados", "i-layers", OTROS_RESULTADOS),

    L("tema-05", TEMA_E, "Tema 05", "i-diagram", SECCION_E),
    L("que-es-transferir", "Condiciones que hacen posible una transferencia", "Qué es transferir", "i-target", QUE_ES_TRANSFERIR),
    L("abanico-transferencia", "Formas de transferencia y de intercambio de conocimiento", "El abanico", "i-diagram", ABANICO),
    L("madurez-via", "Madurez mínima que exige cada vía de transferencia", "Madurez y vía", "i-ladder", MADUREZ_VIA),
    L("herramientas-05", "Herramientas 05 · Vigilancia tecnológica y búsqueda de comparables", "Herramientas 05", "i-sliders", HERR_05),
    L("metodos-valorizacion", "Métodos de valorización de un activo intangible", "Los tres métodos", "i-scale", METODOS_VALORIZACION),
    L("valorizacion-por-activo", "Método aplicable según el tipo de activo", "Método por activo", "i-rubric", VALORIZACION_POR_ACTIVO),
    L("valorizar-el-caso", "Valorización del prototipo de colmenas por los tres métodos", "Valorizar el caso", "i-target", VALORIZAR_EL_CASO),
    L("brecha-peruana", "Embudo de la transferencia en la universidad peruana", "El embudo peruano", "i-chart", BRECHA_PERUANA),

    L("video-resumen", "Estructura del video de resumen del proyecto", "El video", "i-quote", VIDEO_RESUMEN),
    L("dossier", "Piezas del dossier final del proyecto", "El dossier", "i-file", DOSSIER),
    L("errores", "Errores frecuentes en la ejecución de un proyecto financiado", "Errores", "i-alert", ERRORES),
    L("queda-establecido", "Cinco puntos establecidos sobre presupuesto, ejecución y transferencia", "Resumen", "i-check", RESUMEN_FINAL),
    L("glosario", "Glosario de presupuesto, ejecución y transferencia", "Glosario", "i-book", GLOSARIO),
    L("referencias", "Fuentes citadas y vía de acceso a cada una", "Referencias", "i-quote", REFERENCIAS),
]

generar_desde({
    "clase": "clase-05",
    "sesion": SESION,
    "laminas": renumerar(LAMINAS),
})
