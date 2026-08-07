"""Sesión 4 · Formulación de proyectos.

La sesión recorre el documento que hay que entregar, sección por sección, y en
cada una responde lo mismo: qué pide, con qué metodología se construye y un
ejemplo para discutir. Un solo caso atraviesa el mazo entero —un prototipo
electrónico para monitorear colmenas— para que el estudiante vea crecer la
misma propuesta en vez de un ejemplo suelto por sección.

No se formula contra ninguna convocatoria concreta: se enseña la estructura
canónica y la matriz del ILPES-CEPAL, que es lo que transfiere entre fondos.

Uso:  python3 tools/clases/clase-04.py
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

SESION = "Sesión 4 · Formulación de proyectos"

TEMA_A = "Del problema a la matriz: las secciones que sostienen la propuesta"
TEMA_B = "La evidencia y los resultados que el evaluador califica"

# ==========================================================================
# FUENTES
# ==========================================================================
F_ILPES = ("ILPES-CEPAL, <i>Metodología del marco lógico para la planificación, "
           "el seguimiento y la evaluación de proyectos</i> · serie manuales 42")
F_TOC = ("Breuer et al. (2018), <i>BMJ Global Health</i> · cómo se construye una "
         "teoría del cambio · CC BY-NC")
F_TOC_AGRI = ("Thornton et al. (2018), <i>Agricultural Systems</i> 165 · límites "
              "del marco lógico y de la teoría del cambio")
F_PRISMA = ("Page et al. (2021), <i>BMJ</i> 372:n71 · declaración PRISMA 2020 "
            "· CC BY")
F_VOS = ("Bibliometría con VOSviewer (2023), <i>Arab Gulf Journal of Scientific "
         "Research</i> · CC BY")
F_MIDAGRI = ("MIDAGRI · estadística apícola nacional, con datos del Censo "
             "Nacional Agropecuario · documento público")
F_CASO = ("Caso de clase · magnitudes didácticas del prototipo, no medidas en "
          "campo")

# ==========================================================================
# APERTURA
# ==========================================================================
PORTADA = envolver(
    f"""\t\t\t\t<p class="slide__eyebrow">Sesión 4</p>
\t\t\t\t<h1 class="slide__title">Formulación de proyectos</h1>
\t\t\t\t<ol class="topic">
\t\t\t\t\t<li><b>01</b>{TEMA_A}</li>
\t\t\t\t\t<li><b>02</b>{TEMA_B}</li>
\t\t\t\t</ol>"""
)

AGENDA = envolver(
    cabecera("Agenda", "Las once secciones de una propuesta y el orden en que se escriben", "i-flow")
    + "\n"
    + f"""\t\t\t\t<div class="agenda" data-animate="fade-up">
\t\t\t\t\t<div class="agenda__block">
\t\t\t\t\t\t<span class="agenda__n">Tema 01</span>
\t\t\t\t\t\t<h3>{TEMA_A}</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Datos generales y resumen: lo que se escribe al final</li>
\t\t\t\t\t\t\t<li>El problema, con su árbol y su magnitud</li>
\t\t\t\t\t\t\t<li>Objetivos con condición de logro</li>
\t\t\t\t\t\t\t<li>La matriz de marco lógico y sus dos lógicas</li>
\t\t\t\t\t\t\t<li>Metodología y plan de trabajo por objetivo</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 01</b>Gestores de referencias</li>
\t\t\t\t\t\t\t<li><b>Herramientas 02</b>Diagramación del árbol y la matriz</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--b">
\t\t\t\t\t\t<span class="agenda__n">Tema 02</span>
\t\t\t\t\t\t<h3>{TEMA_B}</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Estado del arte declarado y reproducible</li>
\t\t\t\t\t\t\t<li>Mapeo bibliométrico del campo</li>
\t\t\t\t\t\t\t<li>Producto, resultado e impacto: la cadena</li>
\t\t\t\t\t\t\t<li>Teoría del cambio y el límite del marco lógico</li>
\t\t\t\t\t\t\t<li>Revisar la propuesta con criterios de evaluación</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 03</b>Teoría del cambio y cadena de resultados</li>
\t\t\t\t\t\t\t<li><b>Herramientas 04</b>Revisión del documento antes de enviarlo</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__map">
\t\t\t\t\t\t<span class="agenda__map-label">Las seis sesiones</span>
\t\t\t\t\t\t<ul class="agenda__steps">
\t\t\t\t\t\t\t<li><b>01</b>Fundamentos y ecosistema I+D+i+e</li>
\t\t\t\t\t\t\t<li><b>02</b><i>Startups</i>, <i>spin-offs</i> y transferencia</li>
\t\t\t\t\t\t\t<li><b>03</b>Mapa de financiamiento e inversión</li>
\t\t\t\t\t\t\t<li class="is-on"><b>04</b>Formulación de proyectos</li>
\t\t\t\t\t\t\t<li><b>05</b>Presupuesto, ejecución y propiedad intelectual</li>
\t\t\t\t\t\t\t<li><b>06</b><i>Pitch Elevator</i> y tendencias mundiales en I+D+i+e</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)

ORDEN_ESCRITURA = envolver(
    cabecera("Punto de partida",
             "Las once secciones del documento y el orden real en que se escriben",
             "i-file")
    + "\n"
    + figura("s4-orden-secciones",
             "Secciones de una propuesta y orden de redacción",
             "El documento se lee de arriba abajo y se escribe en otro orden: el resumen es lo último.")
    + "\n"
    + criterio(
        "Escribir de la primera sección a la última obliga a resumir un proyecto "
        "que todavía no está definido. Se empieza por el problema y los objetivos, "
        "que fijan todo lo demás, y el resumen se redacta cuando ya hay algo que "
        "resumir."
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

CASO = envolver(
    cabecera("Punto de partida",
             "El proyecto que se formula en clase: monitoreo electrónico de colmenas",
             "i-target")
    + "\n"
    + duo(
        fig_desnuda("s4-caso-nodo",
                    "Componentes del nodo de monitoreo y variables que registra",
                    "Cuatro variables dentro de la colmena y un enlace de radio hasta el tablero del apicultor."),
        criterio(
            "El mismo proyecto atraviesa las cuarenta láminas. En cada sección se "
            "escribe su parte y se compara la versión que un evaluador rechaza con "
            "la que aprueba."
        )
        + "\n"
        + en_la_practica(
            "Tiene las tres cosas a la vez: caracterizar la señal acústica del "
            "enjambre es investigación, construir el nodo es desarrollo, y que el "
            "apicultor decida con él es innovación. La matriz se llena con las tres."
        )
    )
    + "\n"
    + fuente_pie(F_CASO)
)

SECCION_A = seccion("01", TEMA_A,
                    "Datos generales, resumen, problema, objetivos, matriz y plan de "
                    "trabajo. Seis secciones que se construyen en cadena: cada una "
                    "fija lo que la siguiente puede escribir.")

SECCION_B = seccion("02", TEMA_B,
                    "El estado del arte que sostiene la novedad y la cadena de "
                    "resultados que sostiene el impacto. El evaluador lo "
                    "califica cuando la parte técnica ya le parece correcta.")

# ==========================================================================
# §1 · DATOS GENERALES  ·  §2 · RESUMEN
# ==========================================================================
DATOS_GENERALES = envolver(
    cabecera("01 · §1 Datos generales",
             "Los cinco campos que deciden si la propuesta llega a leerse",
             "i-rubric")
    + "\n"
    + tabla(
        ["Campo", "Qué se declara", "Qué lo invalida"],
        [["Figura del postulante", "Quién firma: universidad, empresa, asociación o persona",
          "Una figura que la convocatoria no admite en esa línea"],
         ["Equipo", "Responsable técnico y dedicación de cada integrante",
          "Dedicación sin horas o un responsable sin credencial"],
         ["Duración", "Meses de ejecución, dentro del máximo de las bases",
          "Un plazo que excede el tope, aunque el plan sea bueno"],
         ["Monto", "Lo solicitado y la contrapartida comprometida",
          "Contrapartida calculada sobre lo solicitado y no sobre el costo total"],
         ["Entidades asociadas", "Quién aporta qué, con carta firmada y fechada",
          "Una firma posterior a la fecha de cierre"]],
        titulo="Campos de la primera sección y motivo de inadmisibilidad de cada uno")
    + "\n"
    + evitar(
        "Redactar la propuesta antes de comprobar estos cinco campos. La parte "
        "técnica puede ser impecable y la propuesta no llegar a la evaluación."
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

RESUMEN_SECCION = envolver(
    cabecera("01 · §2 Resumen",
             "Los cuatro movimientos del resumen y por qué se escribe el último",
             "i-quote")
    + "\n"
    + duo(
        fig_desnuda("s4-resumen-movimientos",
                    "Los cuatro movimientos de un resumen y su proporción",
                    "El problema y el resultado ocupan la mitad; las actividades no aparecen."),
        criterio(
            "Problema con su magnitud, solución propuesta, resultado medible e "
            "impacto esperado. En ese orden y sin actividades: lo que se hizo "
            "interesa en la metodología, no aquí."
        )
        + "\n"
        + ejemplo(
            "«Se desarrollará un sistema y se realizarán pruebas de campo» enumera "
            "actividades. «Un nodo de 40 g que avisa de la pérdida de peso de la "
            "colmena en menos de 24 horas» declara el resultado."
        )
    )
    + "\n"
    + fuente_pie(F_CASO)
)

# ==========================================================================
# §3 · PROBLEMA Y JUSTIFICACIÓN
# ==========================================================================
PROBLEMA_MAL = envolver(
    cabecera("01 · §3 Problema",
             "Un problema mal planteado no se corrige con una buena metodología",
             "i-alert")
    + "\n"
    + duo(
        fig_desnuda("s4-problema-vs",
                    "Dos formulaciones del mismo problema y qué permite hacer cada una",
                    "El problema difuso no se puede medir, ni acotar, ni cerrar: no hay método que lo salve."),
        criterio(
            "Un problema se puede evaluar cuando dice a quién afecta, en qué "
            "magnitud y en qué plazo. Sin esas tres cosas no hay indicador posible "
            "más adelante, y la matriz entera queda sin apoyo."
        )
        + "\n"
        + evitar(
            "«Falta de tecnología en el sector apícola». No nombra al afectado, no "
            "tiene magnitud y no se puede cerrar: cualquier resultado lo satisface."
        )
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

ARBOL_PROBLEMAS = envolver(
    cabecera("01 · §3 Problema",
             "El árbol de problemas del caso: causas, problema central y efectos",
             "i-diagram")
    + "\n"
    + figura("s4-arbol-problemas",
             "Árbol de problemas del monitoreo de colmenas",
             "Las causas de abajo son las que un proyecto puede atacar; los efectos de arriba son los que justifica.")
    + "\n"
    + criterio(
        "El árbol se construye de abajo arriba y se lee de arriba abajo. Solo las "
        "causas de la base entran en los componentes del proyecto: los efectos "
        "sirven para justificar, no para prometer."
    )
    + "\n"
    + fuente_pie(F_ILPES, F_CASO)
)

ARBOL_OBJETIVOS = envolver(
    cabecera("01 · §3 Problema",
             "Del árbol de problemas al árbol de objetivos, y dónde se rompe",
             "i-flow")
    + "\n"
    + figura("s4-arbol-objetivos",
             "Conversión del árbol de problemas en árbol de objetivos",
             "La conversión es mecánica salvo en las causas que el proyecto no controla: esas pasan a supuestos.")
    + "\n"
    + criterio(
        "Cada causa se reformula en positivo y se convierte en un medio. La "
        "conversión falla en las causas que están fuera del alcance del proyecto: "
        "no se convierten en objetivos, se declaran como supuestos."
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

BRECHA = envolver(
    cabecera("01 · §3 Problema",
             "Cuantificar la brecha: la apicultura peruana en cifras",
             "i-chart")
    + "\n"
    + figura("s4-brecha-apicola",
             "Colmenas instaladas, en producción y potencial estimado del país",
             "Entre lo que hay en producción y el potencial estimado hay más del doble de colmenas.")
    + "\n"
    + dato_clave(
        "El censo cuenta <b>252 329 colmenas instaladas</b> y <b>214 276</b> en "
        "producción, con <b>41 327 apicultores</b> y <b>10,8 kg por colmena y "
        "año</b>. El potencial se estima en 500 000 colmenas."
    )
    + "\n"
    + fuente_pie(F_MIDAGRI)
)

# ==========================================================================
# §5 · OBJETIVOS
# ==========================================================================
OBJETIVOS = envolver(
    cabecera("01 · §5 Objetivos",
             "Verbo, objeto y condición de logro: las tres partes de un objetivo",
             "i-target")
    + "\n"
    + duo(
        fig_desnuda("s4-objetivo-partes",
                    "Anatomía de un objetivo específico verificable",
                    "Sin condición de logro el objetivo no se puede cerrar, y el evaluador no tiene con qué puntuarlo."),
        criterio(
            "El verbo dice qué se hace, el objeto sobre qué, y la condición de "
            "logro cuándo se da por cumplido. La condición lleva magnitud, unidad "
            "y momento de medición."
        )
        + "\n"
        + ejemplo(
            "«Mejorar el monitoreo de las colmenas» no se cierra nunca. "
            "«Detectar la pérdida de peso de la colmena con un error menor a 200 g "
            "en pruebas de 90 días» sí."
        )
    )
    + "\n"
    + fuente_pie(F_ILPES, F_CASO)
)

OBJETIVOS_JERARQUIA = envolver(
    cabecera("01 · §5 Objetivos",
             "Objetivo general y específicos: qué relación tienen entre sí",
             "i-ladder")
    + "\n"
    + figura("s4-objetivos-jerarquia",
             "Objetivo general y los tres específicos del caso",
             "Los específicos suman el general: si se cumplen los tres y el general no, la jerarquía está mal escrita.")
    + "\n"
    + criterio(
        "Los objetivos específicos son resultados parciales, no etapas del trabajo. "
        "Un específico que empieza por «realizar» o «llevar a cabo» es una "
        "actividad disfrazada y no pertenece a esta sección."
    )
    + "\n"
    + fuente_pie(F_ILPES, F_CASO)
)

# ==========================================================================
# §6 · MARCO LÓGICO
# ==========================================================================
MATRIZ = envolver(
    cabecera("01 · §6 Marco lógico",
             "La matriz: cuatro filas de objetivos y cuatro columnas de prueba",
             "i-rubric")
    + "\n"
    + figura("s4-matriz-ml",
             "Matriz de marco lógico del caso, con sus dieciséis celdas",
             "Cada fila es un nivel de objetivo y cada columna, una prueba distinta sobre ese mismo objetivo.")
    + "\n"
    + criterio(
        "Fin, propósito, componentes y actividades en las filas. Resumen "
        "narrativo, indicadores, medios de verificación y supuestos en las "
        "columnas. La matriz no es un formulario: es el proyecto entero en una "
        "página."
    )
    + "\n"
    + fuente_pie(F_ILPES, F_CASO)
)

LOGICA_VERTICAL = envolver(
    cabecera("01 · §6 Marco lógico",
             "Lógica vertical: si las actividades, entonces los componentes",
             "i-ladder")
    + "\n"
    + duo(
        fig_desnuda("s4-logica-vertical",
                    "Encadenamiento de las cuatro filas de la matriz",
                    "Cada nivel se sostiene en el de abajo más su supuesto: si el supuesto falla, la cadena se corta ahí."),
        criterio(
            "Se lee de abajo arriba. Ejecutadas las actividades y cumplidos sus "
            "supuestos, se producen los componentes; con los componentes y sus "
            "supuestos, se logra el propósito."
        )
        + "\n"
        + evitar(
            "Saltar un nivel. Si del componente al propósito hace falta algo que no "
            "está escrito ni como actividad ni como supuesto, el evaluador lo ve al "
            "leer la columna de arriba abajo."
        )
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

LOGICA_HORIZONTAL = envolver(
    cabecera("01 · §6 Marco lógico",
             "Lógica horizontal: objetivo, indicador y medio tienen que cerrar",
             "i-arrow-right")
    + "\n"
    + figura("s4-logica-horizontal",
             "Las dos condiciones que debe cumplir cada fila de la matriz",
             "Los medios bastan para calcular el indicador, y el indicador basta para evaluar el objetivo.")
    + "\n"
    + criterio(
        "El ILPES lo define en dos condiciones: que los medios basten para obtener "
        "los datos que el indicador requiere, y que el indicador permita evaluar "
        "el logro del objetivo. Si una falla, la fila no cierra."
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

INDICADORES = envolver(
    cabecera("01 · §6 Marco lógico",
             "Qué distingue un indicador verificable de uno declarativo",
             "i-scale")
    + "\n"
    + tabla(
        ["Parte", "Qué aporta", "Declarativo", "Verificable"],
        [["Cantidad", "Cuánto", "«varias colmenas»", "«60 colmenas»"],
         ["Calidad", "De qué tipo", "«buen funcionamiento»", "«error menor a 200 g»"],
         ["Tiempo", "Para cuándo", "«al final del proyecto»", "«al mes 14»"],
         ["Lugar", "Dónde", "«en campo»", "«en dos apiarios de Junín»"],
         ["Línea base", "Desde dónde", "no se declara", "«desde 0 colmenas instrumentadas»"]],
        titulo="Las cinco partes de un indicador y su versión declarativa frente a la verificable")
    + "\n"
    + criterio(
        "Un indicador sin línea base no mide un cambio: mide un estado. Y sin "
        "cambio no hay nada que atribuir al proyecto."
    )
    + "\n"
    + fuente_pie(F_ILPES, F_CASO)
)

MEDIOS = envolver(
    cabecera("01 · §6 Marco lógico",
             "Medios de verificación: quién produce el dato y quién lo paga",
             "i-search")
    + "\n"
    + duo(
        fig_desnuda("s4-medios-verificacion",
                    "Origen del dato de cada indicador y su costo de obtención",
                    "El dato que nadie produce hoy hay que producirlo, y eso es una actividad con presupuesto."),
        criterio(
            "Es la columna peor llenada de la matriz. Un medio de verificación "
            "sirve si nombra el documento, quién lo emite y cada cuánto. «Informes "
            "del proyecto» no es un medio de verificación."
        )
        + "\n"
        + en_la_practica(
            "Si el dato del indicador no existe todavía, medirlo es una actividad "
            "del proyecto y aparece en el presupuesto. Descubrirlo al ejecutar es "
            "descubrir que falta dinero."
        )
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

SUPUESTOS = envolver(
    cabecera("01 · §6 Marco lógico",
             "Supuestos: lo que está fuera de control y aun así hay que declarar",
             "i-alert")
    + "\n"
    + figura("s4-supuestos",
             "Clasificación de un factor externo según probabilidad e impacto",
             "El factor improbable y grave no es un supuesto: es un riesgo que exige plan de mitigación.")
    + "\n"
    + criterio(
        "Un supuesto es una condición externa que se da por cumplida. Si su "
        "probabilidad es baja y su impacto alto, deja de ser supuesto y pasa a ser "
        "riesgo, con su medida de mitigación escrita."
    )
    + "\n"
    + evitar(
        "Usar los supuestos como excusa anticipada. «Que el clima sea favorable» "
        "no es un supuesto del proyecto: es una forma de no responder por el "
        "resultado."
    )
    + "\n"
    + fuente_pie(F_ILPES)
)

# ==========================================================================
# §7 · METODOLOGÍA Y PLAN DE TRABAJO
# ==========================================================================
METODO_POR_OBJETIVO = envolver(
    cabecera("01 · §7 Metodología",
             "Una metodología por objetivo específico, no una general",
             "i-layers")
    + "\n"
    + tabla(
        ["Objetivo específico", "Método", "Entregable", "Madurez"],
        [["Caracterizar la señal de la colmena",
          "Registro continuo y análisis espectral", "Informe con la firma acústica", "TRL 3"],
         ["Construir el nodo de medición",
          "Diseño iterativo y ensayo en banco", "Nodo con informe de ensayo", "TRL 4"],
         ["Validar en apiario",
          "Prueba comparada contra pesaje manual", "Acta de validación en campo", "TRL 6"]],
        titulo="Correspondencia entre objetivo específico, método, entregable y nivel de madurez")
    + "\n"
    + criterio(
        "Una metodología única para todo el proyecto delata que los objetivos "
        "específicos son etapas y no resultados. Cada objetivo necesita su diseño, "
        "su técnica y su entregable."
    )
    + "\n"
    + fuente_pie(F_ILPES, F_CASO)
)

CRONOGRAMA = envolver(
    cabecera("01 · §7 Metodología",
             "Actividades, hitos y la ruta que no admite retraso",
             "i-gantt")
    + "\n"
    + figura("s4-cronograma",
             "Cronograma del caso con sus hitos y su ruta crítica",
             "Tres actividades no admiten retraso: si una se mueve, la fecha final se mueve con ella.")
    + "\n"
    + criterio(
        "Un hito no es una fecha: es un documento con fecha y responsable. Si al "
        "llegar el mes no hay nada que enseñar, no había hito."
    )
    + "\n"
    + fuente_pie(F_CASO)
)

HITO_VERIFICABLE = envolver(
    cabecera("01 · §7 Metodología",
             "Qué convierte una actividad en un hito verificable",
             "i-milestone")
    + "\n"
    + duo(
        fig_desnuda("s4-hito",
                    "Actividad frente a hito, y qué acredita cada uno",
                    "La actividad consume tiempo y presupuesto; el hito produce un documento que alguien puede pedir."),
        ejemplo(
            "«Realizar pruebas de campo» consume cuatro meses y no acredita nada. "
            "«Acta de validación firmada por la asociación de apicultores, mes 14» "
            "es un hito: existe o no existe."
        )
        + "\n"
        + criterio(
            "El desembolso por tramos se libera contra hito verificado. Un plan sin "
            "hitos documentales deja al proyecto sin caja aunque el trabajo avance."
        )
    )
    + "\n"
    + fuente_pie(F_CASO)
)

# ==========================================================================
# §4 · ESTADO DEL ARTE  (tema 02)
# ==========================================================================
NOVEDAD = envolver(
    cabecera("02 · §4 Estado del arte",
             "Qué sostiene el criterio de novedad ante el evaluador",
             "i-book")
    + "\n"
    + duo(
        fig_desnuda("s4-novedad",
                    "Qué acredita cada afirmación de novedad de una propuesta",
                    "La novedad no se declara: se demuestra enseñando qué se buscó y qué no se encontró."),
        criterio(
            "El primero de los cinco criterios de Frascati es la novedad, y se "
            "acredita con el estado del arte. Una revisión que solo cite trabajo "
            "propio o nacional no sostiene nada."
        )
        + "\n"
        + evitar(
            "«No existen antecedentes en el país». El evaluador solo puede "
            "comprobarlo si dices dónde buscaste, con qué términos y qué "
            "descartaste."
        )
    )
    + "\n"
    + fuente_pie(F_PRISMA)
)

PRISMA_FLUJO = envolver(
    cabecera("02 · §4 Estado del arte",
             "El flujo de PRISMA 2020 aplicado a la revisión de una propuesta",
             "i-flow")
    + "\n"
    + figura("s4-prisma",
             "Identificación, cribado, elegibilidad e inclusión, con los descartes contados",
             "Lo que hace reproducible una búsqueda no es el número final: son los descartes contados en cada paso.")
    + "\n"
    + criterio(
        "PRISMA se diseñó para revisiones sistemáticas y una propuesta de I+D+i "
        "no lo es. Lo que se toma prestado es la disciplina de declarar: qué se "
        "buscó, dónde, con qué criterio y cuántos se cayeron en cada filtro."
    )
    + "\n"
    + fuente_pie(F_PRISMA)
)

MAPEO = envolver(
    cabecera("02 · §4 Estado del arte",
             "Mapeo bibliométrico: lo que la lectura no alcanza a mostrar",
             "i-network")
    + "\n"
    + figura("s4-mapeo",
             "Coocurrencia de términos en la literatura del monitoreo apícola",
             "Los grupos que aparecen dicen qué comunidades trabajan el tema y con qué vocabulario lo nombran.")
    + "\n"
    + en_la_practica(
        "El mapa sirve antes de leer: enseña qué términos usa cada comunidad y "
        "evita buscar durante semanas con la palabra equivocada."
    )
    + "\n"
    + fuente_pie(F_VOS)
)

# ==========================================================================
# §9 · RESULTADOS E IMPACTO
# ==========================================================================
CADENA = envolver(
    cabecera("02 · §9 Resultados",
             "Producto, resultado e impacto: tres cosas que se puntúan aparte",
             "i-ladder")
    + "\n"
    + figura("s4-cadena-resultados",
             "Cadena de resultados del caso, del producto al impacto",
             "El proyecto responde por el producto y por el resultado; del impacto solo puede responder en parte.")
    + "\n"
    + criterio(
        "El producto lo entrega el proyecto, el resultado es el cambio en "
        "quien lo usa, y el impacto es el efecto agregado. Prometer impacto con "
        "presupuesto de producto es el error que más credibilidad cuesta."
    )
    + "\n"
    + fuente_pie(F_TOC, F_CASO)
)

TEORIA_CAMBIO = envolver(
    cabecera("02 · §9 Resultados",
             "Teoría del cambio: qué añade sobre la matriz de marco lógico",
             "i-diagram")
    + "\n"
    + duo(
        fig_desnuda("s4-teoria-cambio",
                    "Supuestos causales entre cada eslabón de la cadena",
                    "La teoría del cambio hace explícito el «por qué creemos que esto lleva a aquello»."),
        criterio(
            "La matriz declara qué se logra; la teoría del cambio declara por qué "
            "se cree que una cosa lleva a la otra, y qué evidencia sostiene esa "
            "creencia. Es donde se ve si el proyecto está pensado o solo listado."
        )
    )
    + "\n"
    + fuente_pie(F_TOC)
)

LIMITE_ML = envolver(
    cabecera("02 · §9 Resultados",
             "El límite del marco lógico, dicho por la literatura que lo estudia",
             "i-alert")
    + "\n"
    + duo(
        fig_desnuda("s4-limite-ml",
                    "Avance previsto por la matriz frente al avance real de un proyecto temprano",
                    "La matriz supone avance lineal; un proyecto de I+D+i avanza a saltos y retrocede."),
        criterio(
            "La revisión de <i>Agricultural Systems</i> sostiene que el marco "
            "lógico induce una creencia equivocada en la previsibilidad y el "
            "control de lo que va a ocurrir, y que maneja mal el avance lento o "
            "negativo típico de las etapas tempranas."
        )
        + "\n"
        + en_la_practica(
            "La convocatoria va a pedir la matriz igualmente. Conocer su límite "
            "sirve para escribir supuestos honestos en vez de un plan que finge "
            "que nada puede salir mal."
        )
    )
    + "\n"
    + fuente_pie(F_TOC_AGRI)
)

TOC_TRAMITE = envolver(
    cabecera("02 · §9 Resultados",
             "Cuándo la teoría del cambio se convierte en un trámite",
             "i-alert")
    + "\n"
    + figura("s4-toc-tramite",
             "Señales de una teoría del cambio construida para cumplir",
             "Una teoría del cambio que nadie revisa durante la ejecución no era una teoría: era un anexo.")
    + "\n"
    + criterio(
        "Se vuelve trámite cuando se escribe una vez, al postular, y no se vuelve "
        "a mirar. Sirve cuando la evidencia recogida durante la ejecución valida o "
        "corrige sus supuestos y el proyecto se adapta."
    )
    + "\n"
    + fuente_pie(F_TOC, F_TOC_AGRI)
)

# ==========================================================================
# HERRAMIENTAS QUE DEBERÍAS CONOCER
# ==========================================================================
HERR_01 = bloque_herramientas(
    ref="01", total="04",
    titulo="Tres gestores de referencias y lo que decide la elección entre ellos",
    para_que=(
        "El estado del arte hay que citarlo aquí, en el presupuesto y en la "
        "sustentación. Lo decide una sola prueba: qué cuesta sacar la biblioteca "
        "el día que haga falta cambiar de gestor."
    ),
    herramientas=[
        ("Zotero", "programa libre", [
            "La biblioteca vive en tu equipo y no depende de ningún servicio",
            "Captura desde el navegador con un clic y trae el DOI",
            "Bibliotecas de grupo para trabajar con los coautores",
        ], "zotero.org"),
        ("Mendeley", "Elsevier", [
            "Capa gratuita con la biblioteca guardada en la nube",
            "Anotación de los PDF dentro del propio gestor",
            "Encaja con el ecosistema de Elsevier si ya publicas ahí",
        ], "mendeley.com"),
        ("EndNote", "Clarivate", [
            "De pago, y habitual por convenio de la universidad",
            "Integración profunda con el procesador de textos",
            "Miles de estilos de cita listos para la revista de destino",
        ], "endnote.com"),
    ],
    como_elegir=[
        ("Entrada", "Un clic desde el navegador, y que el DOI llegue solo."),
        ("Salida", "Que exporte a RIS o BibTeX sin perder campos."),
        ("Permanencia", "Qué queda de tu biblioteca si dejas de pagar."),
    ],
)

HERR_02 = bloque_herramientas(
    ref="02", total="04",
    titulo="Tres formas de dibujar el árbol, la matriz y el cronograma",
    para_que=(
        "El árbol de problemas y la matriz se discuten en equipo y cambian veinte "
        "veces antes de quedar. Lo que se necesita es rehacerlos rápido, no "
        "dibujarlos bonito una sola vez."
    ),
    herramientas=[
        ("draw.io", "aplicación libre", [
            "Diagramas de caja y flecha sin cuenta ni instalación",
            "Guarda en tu propio disco o en tu nube",
            "Exporta a imagen vectorial para la propuesta",
        ], "app.diagrams.net"),
        ("Mermaid", "texto que se vuelve diagrama", [
            "El diagrama se escribe como texto y se versiona con el proyecto",
            "Cambiar una rama es cambiar una línea, no rehacer el dibujo",
            "Se renderiza dentro de repositorios y editores",
        ], "mermaid.js.org"),
        ("Hojas de cálculo", "Sheets, Excel o Calc", [
            "La matriz de marco lógico es una tabla: vive bien en una hoja",
            "Varias personas sobre el mismo archivo y con historial",
            "Se exporta al formato que pida la convocatoria",
        ], "libreoffice.org"),
    ],
    como_elegir=[
        ("Rehacer", "Cuánto cuesta cambiar una rama del árbol."),
        ("Versionar", "Si se puede volver a la versión de la semana pasada."),
        ("Salida", "Si exporta en vectorial y en el formato que piden."),
    ],
)

HERR_03 = bloque_herramientas(
    ref="03", total="04",
    titulo="Tres apoyos para construir y validar la cadena de resultados",
    para_que=(
        "La cadena de resultados y la teoría del cambio se discuten con el socio y "
        "con el equipo. Lo que hace falta es una plantilla común y una guía que "
        "diga qué es evidencia y qué es deseo."
    ),
    herramientas=[
        ("Guía del BMJ", "Breuer et al., acceso abierto", [
            "Procedimiento paso a paso para construir una teoría del cambio",
            "Incluye los errores más frecuentes, que es su mayor aporte",
            "Pensada para intervenciones complejas, no para proyectos simples",
        ], "gh.bmj.com"),
        ("Plantillas de cadena de resultados", "agencias de cooperación", [
            "Formatos de insumo, producto, resultado e impacto ya separados",
            "Obligan a distinguir lo que el proyecto controla de lo que no",
            "Sirven de contraste contra la matriz que ya escribiste",
        ], "cepal.org"),
        ("Miro o pizarra compartida", "trabajo en equipo", [
            "La cadena se arma moviendo tarjetas con el socio delante",
            "Queda registro de qué se discutió y qué se descartó",
            "Se exporta como imagen para el anexo de la propuesta",
        ], "miro.com"),
    ],
    como_elegir=[
        ("Evidencia", "Si obliga a decir en qué se apoya cada eslabón."),
        ("Equipo", "Si el socio puede intervenir mientras se construye."),
        ("Registro", "Si queda constancia de lo descartado y por qué."),
    ],
)

HERR_04 = bloque_herramientas(
    ref="04", total="04",
    titulo="Tres revisiones que conviene hacer antes de enviar el documento",
    para_que=(
        "La propuesta se pierde por defectos que no son de fondo: una cifra sin "
        "fuente, un anexo sin firmar, un formato que no abre. Se revisan con "
        "lista, no con lectura."
    ),
    herramientas=[
        ("Lista de admisibilidad", "de las propias bases", [
            "Se recorre campo por campo antes de mirar el contenido",
            "La hace alguien que no escribió la propuesta",
            "Detecta lo que tumba la postulación sin llegar a evaluación",
        ], "gob.pe"),
        ("Comprobador de referencias", "el gestor que ya usas", [
            "Verifica que cada DOI resuelva y cada enlace abra",
            "Detecta la referencia citada en el texto y ausente de la lista",
            "Uniformiza el estilo de cita de una sola vez",
        ], "zotero.org"),
        ("Lectura por un tercero", "alguien ajeno al proyecto", [
            "Se le pide que resuma el proyecto tras leer solo el resumen",
            "Si no puede, el resumen está mal escrito",
            "Es la prueba más barata y la que más propuestas salva",
        ], "gob.pe"),
    ],
    como_elegir=[
        ("Orden", "Primero admisibilidad, después fondo: al revés se pierde tiempo."),
        ("Quién", "Que revise quien no escribió: el autor no ve sus huecos."),
        ("Plazo", "Con margen para corregir, no la víspera del cierre."),
    ],
)

# ==========================================================================
# CIERRE
# ==========================================================================
RESUMEN_FINAL = envolver(
    cabecera("Cierre",
             "Cinco puntos establecidos sobre cómo se formula una propuesta",
             "i-check")
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}Queda establecido</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>El documento se lee de arriba abajo y se escribe en otro orden: el problema primero y el resumen al final.</li>
\t\t\t\t\t\t\t<li>Un problema sin afectado, sin magnitud y sin plazo no admite indicador, y sin indicador no hay matriz.</li>
\t\t\t\t\t\t\t<li>La fila de la matriz cierra cuando el medio basta para calcular el indicador y el indicador para evaluar el objetivo.</li>
\t\t\t\t\t\t\t<li>Producto, resultado e impacto se puntúan por separado: prometer impacto con presupuesto de producto cuesta credibilidad.</li>
\t\t\t\t\t\t\t<li>El marco lógico induce una falsa sensación de previsibilidad, y por eso los supuestos se escriben en serio.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-arrow-right")}Lo que se lleva a la sesión 5</h3>
\t\t\t\t\t\t<p>La propuesta técnica escrita: problema, objetivos, matriz,
\t\t\t\t\t\tmetodología y cadena de resultados. Lo que falta es
\t\t\t\t\t\t<b>el dinero y los papeles</b>: presupuesto por partidas,
\t\t\t\t\t\tcronograma de desembolsos, propiedad intelectual y anexos.</p>
\t\t\t\t\t\t<p>La limitación que se arrastra: hay matriz y hay indicadores,
\t\t\t\t\t\ty todavía no está calculado cuánto cuesta producir cada medio de
\t\t\t\t\t\tverificación.</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_ILPES, F_TOC_AGRI)
)

def _grupo_glosario(rotulo, entradas, variante=""):
    """Un bloque del glosario por cada tema de la sesión."""
    v = f" gloss-group--{variante}" if variante else ""
    return (f'\t\t\t\t\t<section class="gloss-group{v}">\n'
            f'\t\t\t\t\t\t<h2 class="gloss-group__title">{rotulo}</h2>\n'
            + "\n".join(entradas)
            + "\n\t\t\t\t\t</section>")


GLOSARIO = envolver(
    cabecera("Cierre", "Doce términos para escribir y para leer una propuesta", "i-book")
    + "\n"
    + '\t\t\t\t<div class="glossary glossary--grouped" data-animate="fade-up">\n'
    + _grupo_glosario("Del problema a la matriz", [
        termino("Árbol de problemas", "problem tree",
                "Causas abajo, problema central en medio y efectos arriba. Solo las causas de la base entran en los componentes."),
        termino("Condición de logro", "success criterion",
                "La magnitud, la unidad y el momento con los que un objetivo se da por cumplido. Sin ella no se cierra."),
        termino("Marco lógico", "logical framework",
                "Matriz de cuatro filas de objetivos y cuatro columnas de prueba. El proyecto entero en una página."),
        termino("Lógica vertical", "vertical logic",
                "Cada nivel se sostiene en el de abajo más su supuesto. Se lee de abajo arriba."),
        termino("Lógica horizontal", "horizontal logic",
                "El medio basta para calcular el indicador y el indicador para evaluar el objetivo. Si una falla, la fila no cierra."),
        termino("Línea base", "baseline",
                "El valor del indicador antes de empezar. Sin ella se mide un estado y no un cambio."),
    ])
    + _grupo_glosario("De la evidencia al impacto", [
        termino("Medio de verificación", "means of verification",
                "El documento que prueba el indicador, con quién lo emite y cada cuánto. Producirlo cuesta dinero."),
        termino("Supuesto", "assumption",
                "Condición externa que se da por cumplida. Si es improbable y grave, deja de ser supuesto y pasa a riesgo."),
        termino("Hito verificable", "milestone",
                "Un documento con fecha y responsable. El desembolso por tramos se libera contra hito, no contra actividad."),
        termino("Cadena de resultados", "results chain",
                "Producto, resultado e impacto. El proyecto responde por los dos primeros y solo en parte por el tercero."),
        termino("Teoría del cambio", "theory of change",
                "Declara por qué se cree que un eslabón lleva al siguiente, y con qué evidencia. Se revisa durante la ejecución."),
        termino("Estado del arte declarado", "reported search",
                "Qué se buscó, dónde, con qué criterio y cuántos se descartaron en cada filtro. Eso lo hace comprobable."),
    ], variante="b")
    + '\t\t\t\t</div>'
    + "\n"
    + fuente_pie(F_ILPES, F_TOC, F_PRISMA)
)

REFERENCIAS = envolver(
    cabecera("Cierre", "Las seis fuentes de la sesión, con su enlace y su vía de acceso", "i-quote")
    + "\n"
    + tabla(
        ["Fuente", "Sirve a", "Dónde está"],
        [["ILPES-CEPAL. <i>Metodología del marco lógico</i>, serie manuales 42",
          "La matriz, la lógica vertical y la horizontal",
          '<a href="https://www.cepal.org/es/publicaciones/5607-metodologia-un-marco-logico-la-planificacion-seguimiento-la-evaluacion">cepal.org · serie manuales 42</a>'],
         ["Page et al. (2021). <i>BMJ</i> 372:n71",
          "Qué se declara para que una búsqueda sea reproducible",
          '<a href="https://doi.org/10.1136/bmj.n71">doi.org/10.1136/bmj.n71</a> · CC BY'],
         ["Breuer et al. (2018). <i>BMJ Global Health</i>",
          "Cómo se construye una teoría del cambio y sus errores",
          '<a href="https://gh.bmj.com">gh.bmj.com</a> · CC BY-NC'],
         ["Thornton et al. (2018). <i>Agricultural Systems</i> 165",
          "El límite del marco lógico y cuándo la teoría del cambio se vuelve trámite",
          '<a href="https://doi.org/10.1016/j.agsy.2018.05.009">doi.org/10.1016/j.agsy.2018.05.009</a>'],
         ["Bibliometría con VOSviewer (2023). <i>Arab Gulf J. Sci. Res.</i>",
          "Procedimiento de un mapeo bibliométrico",
          '<a href="https://www.emerald.com/insight/2536-0051.htm">emerald.com</a> · CC BY'],
         ["MIDAGRI · estadística apícola nacional",
          "Colmenas, apicultores y producción de miel del país",
          '<a href="https://www.gob.pe/midagri">gob.pe/midagri</a> · documento público'],
        ],
        titulo="Fuentes de la sesión y dirección en la que se consultan",
    )
)


# ==========================================================================
# SIMULACIONES
# ==========================================================================
MATRIZ_JS = """\t\t<script type="module">
\t\t\t// Tres condiciones deciden si una fila de la matriz cierra: que el
\t\t\t// indicador tenga sus cinco partes, que el medio de verificación exista
\t\t\t// y que el supuesto sea razonable. Cada control cambia el veredicto de
\t\t\t// extremo a extremo (METODOLOGIA.md §3.3).
\t\t\tconst raiz = document.querySelector('[data-sim="matriz"]');
\t\t\tconst mando = raiz.querySelector("#m-partes");
\t\t\tconst nivel = raiz.querySelector("#m-nivel");
\t\t\tconst veredicto = raiz.querySelector("#m-veredicto");
\t\t\tconst detalle = raiz.querySelector("#m-detalle");
\t\t\tconst ok = raiz.querySelector("#m-ok");
\t\t\tconst no = raiz.querySelector("#m-no");
\t\t\tconst medio = raiz.querySelector("#m-medio");
\t\t\tconst botones = [...raiz.querySelectorAll(".picker__btn")];
\t\t\tconst PARTES = ["cantidad", "calidad", "tiempo", "lugar", "línea base"];
\t\t\tconst NIVEL = { fin: "Fin", proposito: "Propósito",
\t\t\t\tcomponente: "Componente", actividad: "Actividad" };
\t\t\tlet fila = "proposito";

\t\t\tfunction pintar() {
\t\t\t\tconst n = Number(mando.value);
\t\t\t\tconst hay = medio.checked;
\t\t\t\tnivel.textContent = NIVEL[fila] + " · " + n + " de 5 partes";
\t\t\t\tconst tiene = PARTES.slice(0, n), falta = PARTES.slice(n);
\t\t\t\tok.innerHTML = tiene.map((x) => "<li>" + x + "</li>").join("")
\t\t\t\t\t|| "<li>El indicador no declara ninguna de las cinco partes.</li>";
\t\t\t\tno.innerHTML = falta.map((x) => "<li>falta " + x + "</li>").join("")
\t\t\t\t\t+ (hay ? "" : "<li>sin medio de verificación que produzca el dato</li>");
\t\t\t\tif (!hay) {
\t\t\t\t\tveredicto.textContent = "La fila no cierra";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "Sin medio de verificación no hay con qué calcular el indicador, aunque el indicador esté completo. La lógica horizontal exige las dos cosas.";
\t\t\t\t} else if (n < 3) {
\t\t\t\t\tveredicto.textContent = "Indicador declarativo";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "Con menos de tres partes el indicador no se puede verificar: el evaluador no sabe cuándo darlo por cumplido.";
\t\t\t\t} else if (n < 5) {
\t\t\t\t\tveredicto.textContent = "Verificable, con reparos";
\t\t\t\t\tveredicto.dataset.estado = "warn";
\t\t\t\t\tdetalle.textContent = "Se puede medir, pero sin línea base se mide un estado y no un cambio, y sin cambio no hay nada que atribuir al proyecto.";
\t\t\t\t} else {
\t\t\t\t\tveredicto.textContent = "La fila cierra";
\t\t\t\t\tveredicto.dataset.estado = "ok";
\t\t\t\t\tdetalle.textContent = "Indicador completo y medio que lo produce: la lógica horizontal de esta fila se sostiene.";
\t\t\t\t}
\t\t\t}
\t\t\tfor (const b of botones) {
\t\t\t\tb.addEventListener("click", () => {
\t\t\t\t\tfila = b.dataset.fila;
\t\t\t\t\tfor (const o of botones) o.classList.toggle("is-on", o === b);
\t\t\t\t\tpintar();
\t\t\t\t});
\t\t\t}
\t\t\tmando.addEventListener("input", pintar);
\t\t\tmedio.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


MATRIZ_SIM = envolver(
    cabecera("01 · §6 Marco lógico",
             "Cuándo cierra una fila de la matriz y cuándo deja de sostenerse",
             "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="matriz" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<label class="sim__label" for="m-partes">Partes declaradas del indicador</label>
\t\t\t\t\t\t<input class="sim__range" id="m-partes" type="range" min="0" max="5" step="1" value="2" />
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="m-nivel">Propósito</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="m-veredicto" data-estado="warn">La fila no cierra</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="picker">
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-fila="fin">Fin</button>
\t\t\t\t\t\t\t<button class="picker__btn is-on" type="button" data-fila="proposito">Propósito</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-fila="componente">Componente</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-fila="actividad">Actividad</button>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="m-medio" checked />
\t\t\t\t\t\t\t<span><b>Existe el medio de verificación</b><span class="crit__help">Documento, quién lo emite y cada cuánto</span></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<p class="sim__what" id="m-detalle"></p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Lo que el indicador declara</h3>
\t\t\t\t\t\t\t<ul id="m-ok"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Lo que le falta</h3>
\t\t\t\t\t\t\t<ul id="m-no"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Con el indicador completo,
\t\t\t\tdesmarcar el medio de verificación tumba la fila igual: la lógica horizontal
\t\t\t\texige las dos cosas.</p>"""
    + "\n"
    + fuente_pie(F_ILPES)
)


REVISION_JS = MATRIZ_JS.replace('data-sim="matriz"', 'data-sim="revision"').replace(
    "#m-", "#r-").replace("Partes declaradas", "Criterios cubiertos")


REVISION_SIM = envolver(
    cabecera("Cierre",
             "Revisar la propuesta con los criterios con que se va a evaluar",
             "i-rubric")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="revision" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<label class="sim__label" for="r-partes">Criterios de evaluación cubiertos</label>
\t\t\t\t\t\t<input class="sim__range" id="r-partes" type="range" min="0" max="5" step="1" value="3" />
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="r-nivel">Propuesta</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="r-veredicto" data-estado="warn">Revisión</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="picker">
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-fila="fin">Pertinencia</button>
\t\t\t\t\t\t\t<button class="picker__btn is-on" type="button" data-fila="proposito">Coherencia</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-fila="componente">Viabilidad</button>
\t\t\t\t\t\t\t<button class="picker__btn" type="button" data-fila="actividad">Impacto</button>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" id="r-medio" checked />
\t\t\t\t\t\t\t<span><b>Cada afirmación lleva su evidencia</b><span class="crit__help">Cifra con fuente, año y unidad</span></span>
\t\t\t\t\t\t</label>
\t\t\t\t\t\t<p class="sim__what" id="r-detalle"></p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Lo que la propuesta cubre</h3>
\t\t\t\t\t\t\t<ul id="r-ok"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Lo que le falta</h3>
\t\t\t\t\t\t\t<ul id="r-no"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Una propuesta puede cubrir
\t\t\t\ttodos los criterios y caerse igual si ninguna afirmación lleva evidencia
\t\t\t\tdetrás.</p>"""
    + "\n"
    + fuente_pie(F_ILPES)
)



ERRORES = envolver(
    cabecera("Cierre",
             "Cinco defectos que tumban una propuesta antes que el contenido",
             "i-alert")
    + "\n"
    + fichas([
        ("Problema sin magnitud", "§3", [
            "No dice a quién afecta ni cuánto",
            "Sin magnitud no hay indicador posible después",
        ]),
        ("Objetivo sin condición de logro", "§5", [
            "Empieza por «mejorar» o «fortalecer» y no se cierra nunca",
            "El evaluador no tiene con qué puntuarlo",
        ]),
        ("Indicador sin línea base", "§6", [
            "Mide un estado y no un cambio",
            "Sin cambio no hay nada que atribuir al proyecto",
        ]),
        ("Medio de verificación inventado", "§6", [
            "«Informes del proyecto» no es un medio de verificación",
            "Si el dato no existe hoy, producirlo cuesta dinero",
        ]),
        ("Impacto prometido de más", "§9", [
            "Se promete el efecto agregado con presupuesto de producto",
            "El defecto que más credibilidad cuesta ante el comité",
        ]),
        ("Cifra sin fuente", "todo el documento", [
            "El diagnóstico se marca como no verificable",
            "Y con él pierde crédito el resto de la propuesta",
        ]),
    ])
    + "\n"
    + fuente_pie(F_ILPES, F_TOC_AGRI)
)


def L(slug, titulo, nav, icono, contenido, clases="slide", scripts=""):
    return {"slug": slug, "titulo": f"{SESION} · {titulo}", "nav": nav,
            "icono": icono, "clases": clases, "contenido": contenido,
            "scripts": scripts}


LAMINAS = [
    L("portada", "Portada", "Portada", "i-project", PORTADA, "slide slide--start"),
    L("agenda", "Las once secciones de una propuesta y el orden en que se escriben", "Agenda", "i-flow", AGENDA),
    L("orden-secciones", "Las once secciones del documento y el orden real en que se escriben", "Orden", "i-file", ORDEN_ESCRITURA),
    L("caso", "El proyecto que se formula en clase: monitoreo electrónico de colmenas", "El caso", "i-target", CASO),

    L("tema-01", TEMA_A, "Tema 01", "i-project", SECCION_A),
    L("datos-generales", "Los cinco campos que deciden si la propuesta llega a leerse", "Datos generales", "i-rubric", DATOS_GENERALES),
    L("resumen-seccion", "Los cuatro movimientos del resumen y por qué se escribe el último", "Resumen", "i-quote", RESUMEN_SECCION),
    L("problema-mal", "Un problema mal planteado no se corrige con una buena metodología", "Problema", "i-alert", PROBLEMA_MAL),
    L("arbol-problemas", "El árbol de problemas del caso: causas, problema central y efectos", "Árbol", "i-diagram", ARBOL_PROBLEMAS),
    L("arbol-objetivos", "Del árbol de problemas al árbol de objetivos, y dónde se rompe", "Objetivos del árbol", "i-flow", ARBOL_OBJETIVOS),
    L("brecha", "Cuantificar la brecha: la apicultura peruana en cifras", "La brecha", "i-chart", BRECHA),
    L("herramientas-01", "Herramientas 01 · Gestores de referencias", "Herramientas 01", "i-sliders", HERR_01),
    L("objetivos", "Verbo, objeto y condición de logro: las tres partes de un objetivo", "Objetivos", "i-target", OBJETIVOS),
    L("objetivos-jerarquia", "Objetivo general y específicos: qué relación tienen entre sí", "Jerarquía", "i-ladder", OBJETIVOS_JERARQUIA),
    L("matriz", "La matriz: cuatro filas de objetivos y cuatro columnas de prueba", "La matriz", "i-rubric", MATRIZ),
    L("logica-vertical", "Lógica vertical: si las actividades, entonces los componentes", "Lógica vertical", "i-ladder", LOGICA_VERTICAL),
    L("logica-horizontal", "Lógica horizontal: objetivo, indicador y medio tienen que cerrar", "Lógica horizontal", "i-arrow-right", LOGICA_HORIZONTAL),
    L("indicadores", "Qué distingue un indicador verificable de uno declarativo", "Indicadores", "i-scale", INDICADORES),
    L("medios", "Medios de verificación: quién produce el dato y quién lo paga", "Medios", "i-search", MEDIOS),
    L("supuestos", "Supuestos: lo que está fuera de control y aun así hay que declarar", "Supuestos", "i-alert", SUPUESTOS),
    L("matriz-simulador", "Cuándo cierra una fila de la matriz y cuándo deja de sostenerse", "Simular la matriz", "i-sliders", MATRIZ_SIM, "slide", MATRIZ_JS),
    L("herramientas-02", "Herramientas 02 · Diagramación del árbol y la matriz", "Herramientas 02", "i-sliders", HERR_02),
    L("metodo-por-objetivo", "Una metodología por objetivo específico, no una general", "Metodología", "i-layers", METODO_POR_OBJETIVO),
    L("cronograma", "Actividades, hitos y la ruta que no admite retraso", "Cronograma", "i-gantt", CRONOGRAMA),
    L("hito-verificable", "Qué convierte una actividad en un hito verificable", "Hitos", "i-milestone", HITO_VERIFICABLE),

    L("tema-02", TEMA_B, "Tema 02", "i-book", SECCION_B),
    L("novedad", "Qué sostiene el criterio de novedad ante el evaluador", "Novedad", "i-book", NOVEDAD),
    L("prisma", "El flujo de PRISMA 2020 aplicado a la revisión de una propuesta", "PRISMA", "i-flow", PRISMA_FLUJO),
    L("mapeo", "Mapeo bibliométrico: lo que la lectura no alcanza a mostrar", "Mapeo", "i-network", MAPEO),
    L("herramientas-03", "Herramientas 03 · Teoría del cambio y cadena de resultados", "Herramientas 03", "i-sliders", HERR_03),
    L("cadena", "Producto, resultado e impacto: tres cosas que se puntúan aparte", "Cadena", "i-ladder", CADENA),
    L("teoria-cambio", "Teoría del cambio: qué añade sobre la matriz de marco lógico", "Teoría del cambio", "i-diagram", TEORIA_CAMBIO),
    L("limite-ml", "El límite del marco lógico, dicho por la literatura que lo estudia", "El límite", "i-alert", LIMITE_ML),
    L("toc-tramite", "Cuándo la teoría del cambio se convierte en un trámite", "Cuándo es trámite", "i-alert", TOC_TRAMITE),
    L("herramientas-04", "Herramientas 04 · Revisión del documento antes de enviarlo", "Herramientas 04", "i-sliders", HERR_04),
    L("revision-simulador", "Revisar la propuesta con los criterios con que se va a evaluar", "Revisar", "i-rubric", REVISION_SIM, "slide", REVISION_JS),
    L("errores", "Cinco defectos que tumban una propuesta antes que el contenido", "Errores", "i-alert", ERRORES),

    L("queda-establecido", "Cinco puntos establecidos sobre cómo se formula una propuesta", "Resumen", "i-check", RESUMEN_FINAL),
    L("glosario", "Doce términos para escribir y para leer una propuesta", "Glosario", "i-book", GLOSARIO),
    L("referencias", "Las seis fuentes de la sesión, con su enlace y su vía de acceso", "Referencias", "i-quote", REFERENCIAS),
]

generar_desde({
    "clase": "clase-04",
    "sesion": SESION,
    "laminas": renumerar(LAMINAS),
})
