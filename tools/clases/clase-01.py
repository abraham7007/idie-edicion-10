#!/usr/bin/env python3
"""Sesión 1 · Fundamentos y ecosistema I+D+i+e: Perú y el mundo.

Guion de la sesión. Contiene SOLO lo que distingue a cada lámina: la cabecera
repetida, la cadena de anterior/siguiente y el total los pone el generador
(METODOLOGIA.md §9). Se edita este archivo, nunca el HTML resultante.

Todas las cifras están verificadas contra la fuente que se cita al pie de la
lámina, y son las mismas que usan las figuras de `tools/figures/render.py`
(METODOLOGIA.md §1 y §3.2).

Uso:  python3 tools/clases/clase-01.py
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

SESION = "Sesión 1 · Fundamentos y ecosistema I+D+i+e"

# Los dos temas de la sesión. Frases nominales que nombran la materia, como
# la nombraría un temario: sin verbos y sin interrogaciones (METODOLOGIA.md §6).
TEMA_A = "Definiciones y madurez tecnológica"
TEMA_B = "Institucionalidad del sistema peruano de ciencia, tecnología e innovación"

# Fuentes citadas en esta sesión. Se escriben una vez y se reutilizan, para
# que dos láminas no puedan citar el mismo trabajo de dos formas distintas.
F_FRASCATI = "OCDE (2015), <i>Frascati Manual 2015</i> · lectura abierta en oecd.org"
F_OSLO = "OCDE y Eurostat (2018), <i>Oslo Manual 2018</i>, 4.ª ed. · lectura abierta en oecd.org"
F_GII = "OMPI (2025), <i>Global Innovation Index 2025</i>, versión ejecutiva · CC BY 4.0 IGO"
F_POLCTI_DIAG = "CONCYTEC (2024), <i>Política Nacional de CTI al 2030</i>, diagnóstico · documento público"
F_POLCTI = "CONCYTEC (2024), <i>Política Nacional de CTI al 2030</i>, Tabla 13 · documento público"
F_DS = "DS 093-2025-PCM, <i>El Peruano</i>, 15 de julio de 2025 · norma de dominio público"
F_ZAPATA = "Zapata-Cantu y González (2021), <i>Sustainability</i> 13(7):4077 · CC BY 4.0"
F_NOVILLO = "Novillo-Villegas et al. (2022), <i>Sustainability</i> 14(11):6686 · CC BY 4.0"
F_HELIYON = "Salvador-Carulla et al. (2024), <i>Heliyon</i> 10:e29930 · CC BY-NC 4.0"
F_TTO = "Hailu (2024), <i>Journal of Innovation and Entrepreneurship</i> 13 · CC BY 4.0"
F_RANTALA = "Rantala et al. (2021), <i>Triple Helix</i> 8(3):405 · CC BY 4.0"
F_UNESCO = "Instituto de Estadística de la UNESCO, vía Banco Mundial · dato de 2018"


def logro(icono, texto):
    return f'\t\t\t\t\t\t<p class="goal">{ico(icono)}<span>{texto}</span></p>'


# ==========================================================================
# 01 · PORTADA
# ==========================================================================

PORTADA = f"""			<div class="slide__content stagger">
				<div class="cover">
					<div class="cover__main">
						<span class="badge" data-animate="fade-up">{ico("i-network")}Sesión 1</span>

						<h1 class="slide__title" data-animate="fade-up">Fundamentos y ecosistema I+D+i+e</h1>

						<div class="cover__topics" data-animate="fade-up">
							<span class="topic"><span class="topic__n">01</span>{TEMA_A}</span>
							<span class="topic topic--b"><span class="topic__n">02</span>Institucionalidad del sistema peruano</span>
						</div>

{colofon()}
					</div>

{mapa_ecosistema(
    activos=("academia", "empresa", "mercado", "estado", "fondos"),
    aristas=("academia-empresa", "empresa-mercado", "mercado-estado",
             "estado-fondos", "fondos-academia"),
)}
				</div>
			</div>"""


# ==========================================================================
# 02 · AGENDA DE LA SESIÓN
# ==========================================================================

AGENDA = envolver(
    cabecera("Agenda", "Contenidos de los dos temas y las cuatro paradas de herramientas", "i-flow")
    + "\n"
    + """\t\t\t\t<div class="agenda" data-animate="fade-up">
\t\t\t\t\t<div class="agenda__block">
\t\t\t\t\t\t<span class="agenda__n">Tema 01</span>
\t\t\t\t\t\t<h3>Definiciones y madurez tecnológica</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Los cinco criterios de una actividad de I+D</li>
\t\t\t\t\t\t\t<li>El umbral entre desarrollo e innovación</li>
\t\t\t\t\t\t\t<li>Tipos de investigación y tipos de innovación</li>
\t\t\t\t\t\t\t<li>La escala TRL y sus dos cortes</li>
\t\t\t\t\t\t\t<li>Publicaciones, patentes y tasas de adjudicación</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 01</b>Buscadores académicos con DOI y licencia</li>
\t\t\t\t\t\t\t<li><b>Herramientas 02</b>Asistentes de chat generalistas</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__block agenda__block--b">
\t\t\t\t\t\t<span class="agenda__n">Tema 02</span>
\t\t\t\t\t\t<h3>Institucionalidad del sistema peruano</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Organismos del SINACTI y sus instrumentos</li>
\t\t\t\t\t\t\t<li>Arquitectura normativa vigente</li>
\t\t\t\t\t\t\t<li>Posición del país: inversión, índices y regiones</li>
\t\t\t\t\t\t\t<li>Capital humano, universidades y obstáculos</li>
\t\t\t\t\t\t\t<li>Modelos que explican el desempeño de un sistema</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t\t<ul class="agenda__wk">
\t\t\t\t\t\t\t<li><b>Herramientas 03</b>Dónde se comprueba qué norma está vigente</li>
\t\t\t\t\t\t\t<li><b>Herramientas 04</b>Registros de capacidades del país</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="agenda__map">
\t\t\t\t\t\t<span class="agenda__map-label">Las seis sesiones</span>
\t\t\t\t\t\t<ul class="agenda__steps">
\t\t\t\t\t\t\t<li class="is-on"><b>01</b>Fundamentos y ecosistema I+D+i+e</li>
\t\t\t\t\t\t\t<li><b>02</b><i>Startups</i>, <i>spin-offs</i> y transferencia</li>
\t\t\t\t\t\t\t<li><b>03</b>Mapa de financiamiento e inversión</li>
\t\t\t\t\t\t\t<li><b>04</b>Formulación de proyectos</li>
\t\t\t\t\t\t\t<li><b>05</b>Del proyecto ganado al resultado transferido</li>
\t\t\t\t\t\t\t<li><b>06</b><i>Pitch Elevator</i> y tendencias mundiales en I+D+i+e</li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)


# ==========================================================================
# (retiradas) MAPA DEL CURSO y DEFINICIONES CLAVE
# ==========================================================================
# Ambas abrían la sesión en la versión anterior. Se retiran por §4.1: una
# tabla de términos al principio obliga a memorizar sin contexto y gasta los
# mejores minutos de las tres horas. El vocabulario se introduce donde hace
# falta y se recoge en el glosario del cierre.
# ==========================================================================
# 03 · DEFINICIONES CLAVE
# ==========================================================================

DEFINICIONES = envolver(
    cabecera("Vocabulario", "Las cuatro letras de I+D+i+e", "i-book")
    + "\n"
    + tabla(
        ["Letra", "Qué es", "Pregunta que responde", "Resultado típico"],
        [
            ["I · Investigación", "Trabajo creativo y sistemático para aumentar el conocimiento", "¿Cómo funciona?", "Publicación, tesis, dato nuevo"],
            ["D · Desarrollo", "Uso de ese conocimiento para producir materiales, productos o procesos nuevos", "¿Se puede construir?", "Prototipo, planta piloto"],
            ["i · innovación", "Producto o proceso nuevo o mejorado, <b>puesto a disposición de otros</b>", "¿Alguien lo usa?", "Producto en el mercado, proceso adoptado"],
            ["e · emprendimiento", "Organización que captura valor de lo anterior", "¿Quién lo sostiene?", "Empresa, spin-off, unidad de negocio"],
        ],
    )
    + "\n"
    + aviso(
        "La frontera que más cuesta en una postulación es la de <b>D</b> a <b>i</b>: "
        "un prototipo que funciona en laboratorio y que nadie ha usado todavía es "
        "desarrollo, no innovación. Los fondos las financian con instrumentos distintos."
    )
    + "\n"
    + fuente_pie(F_FRASCATI, F_OSLO)
)


# ==========================================================================
# TEMA A
# ==========================================================================

PORTADILLA_A = seccion(
    "Tema 01",
    TEMA_A,
    "Qué cuenta como I+D, qué cuenta como innovación, y cómo se mide la madurez "
    "de una tecnología para saber quién puede financiarla.",
)

PARTIDA = envolver(
    cabecera("01 · Punto de partida", "Gasto en I+D como porcentaje del PBI: Perú y países seleccionados, 2018", "i-chart")
    + "\n"
    + figura(
        "s1-gasto-id-pbi",
        "Gasto en I+D sobre el producto bruto interno (PBI): Perú y ocho referencias, 2018",
        "<b>Israel y Corea invierten casi cinco por ciento de su economía; el Perú, trece centésimas.</b>",
    )
    + "\n"
    + conclusion(
        "Qué se sigue de esto:",
                "La referencia es la Organización para la Cooperación y el Desarrollo Económicos (OCDE); los datos son de 2018 y de 2017 para América Latina. Con un sistema de este tamaño, el dinero disponible se asigna por concurso y "
        "con rúbrica. No hay holgura para financiar una propuesta mal formulada aunque "
        "la idea sea buena.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_UNESCO)
)


CRITERIOS_ID = envolver(
    cabecera("01 · Qué cuenta como I+D", "Definición de I+D y los cinco criterios de Frascati 2015", "i-search")
    + "\n"
    + definicion(
        "Investigación y desarrollo",
        "Frascati 2015",
        "Trabajo creativo y sistemático realizado para aumentar el volumen de "
        "conocimiento y concebir nuevas aplicaciones a partir del conocimiento "
        "disponible <i>(research and experimental development)</i>.",
    )
    + "\n"
    + tabla(
        ["Criterio", "Qué exige", "Cómo se comprueba en una propuesta"],
        [
            ["Novedosa", "Busca conocimiento nuevo", "El estado del arte muestra que no existe"],
            ["Creativa", "Aporta conceptos o hipótesis originales", "Hay una hipótesis declarada, no solo una tarea"],
            ["Incierta", "El resultado no está garantizado", "El plan contempla que el experimento falle"],
            ["Sistemática", "Se planifica y se registra", "Hay protocolo, cronograma y registro"],
            ["Transferible", "Sus resultados pueden reproducirse", "Datos y método quedan disponibles"],
        ],
        titulo="Los cinco criterios de Frascati y su comprobación en una propuesta"
    )
    + "\n"
    + aviso(
        "Los cinco a la vez. Una actividad rutinaria de control de calidad es "
        "sistemática y transferible, pero ni novedosa ni incierta: <b>no es I+D</b>, y "
        "presentarla como tal es causa habitual de inadmisibilidad."
    )
    + "\n"
    + fuente_pie(F_FRASCATI)
)


TIPOS_INVESTIGACION = envolver(
    cabecera("01 · Qué cuenta como I+D", "Investigación básica, aplicada y desarrollo experimental: evidencia y financiador", "i-layers")
    + "\n"
    + tabla(
        ["Tipo", "Qué persigue", "Aplicación prevista", "Resultado que acredita el cierre", "Quién lo financia en el Perú"],
        [
            ["Básica", "Conocimiento nuevo sobre los fundamentos de un fenómeno", "Ninguna", "Publicación con datos y método abiertos", "PROCIENCIA: investigación y doctorados"],
            ["Aplicada", "Conocimiento nuevo dirigido a un objetivo práctico", "Declarada", "Prueba de concepto documentada", "PROCIENCIA e I+D con empresa"],
            ["Desarrollo experimental", "Producir productos o procesos nuevos", "Especificada", "Prototipo con su informe de ensayo", "ProInnóvate y Red CITE"],
        ],
        titulo="Los tres tipos de Frascati, la evidencia que cierra cada uno y quién lo financia"
    )
    + "\n"
    + ejemplo(
        "El mismo material da los tres tipos: estudiar por qué la fibra amazónica "
        "resiste la humedad es básica; buscar con ello un aislante altoandino, aplicada; "
        "ensayar paneles en campo, desarrollo experimental."
    )
    + "\n"
    + fuente_pie(F_FRASCATI, F_POLCTI_DIAG)
)


INNOVACION = envolver(
    cabecera("01 · Qué cuenta como I+D", "Definición de innovación de Oslo 2018 y sus dos condiciones", "i-bulb")
    + "\n"
    + definicion(
        "Innovación",
        "Oslo 2018",
        "Producto o proceso de negocio nuevo o mejorado, o una combinación de ambos, "
        "que <b>difiere significativamente</b> de los anteriores de la unidad y que ha "
        "sido <b>puesto a disposición de usuarios potenciales</b> o puesto en uso por "
        "la propia unidad.",
        "i-bulb",
    )
    + "\n"
    + duo(
        figura(
            "s1-umbral-innovacion",
            "Las dos condiciones de Oslo 2018 y los tres resultados posibles",
            "<b>Fallar la segunda condición no degrada a mejora: deja el proyecto en "
            "desarrollo experimental, que se financia por otra vía.</b>",
        ),
        evitar(
            "Declarar innovación un prototipo sin usuario. El mismo sensor de humedad es "
            "desarrollo experimental en el laboratorio e innovación en veinte parcelas de "
            "una cooperativa que decide con él cuándo regar."
        )
        + "\n"
        + conclusion(
        "La consecuencia práctica:",
                    "El evaluador busca la evidencia de uso. Si el proyecto todavía no la tiene, "
            "corresponde postular como desarrollo experimental.",
        ),
        invertir=False,
    )
    + "\n"
    + fuente_pie(F_OSLO)
)


TRL_TABLA = envolver(
    cabecera("01 · Medir la madurez", "Escala TRL: tramos de laboratorio, entorno relevante y entorno real", "i-ladder")
    + "\n"
    + tabla(
        ["Tramo y entorno de prueba", "Documento que acredita el tramo", "Instrumento que lo admite en el Perú"],
        [
            ["TRL 1-3 · laboratorio", "Publicación o informe con el principio verificado y el concepto formulado", "PROCIENCIA: investigación básica y aplicada"],
            ["TRL 4-6 · entorno relevante", "Informe de ensayo del prototipo, con las condiciones del entorno declaradas", "ProInnóvate: desarrollo tecnológico y proyectos de I+D con empresa"],
            ["TRL 7-9 · entorno real", "Acta de instalación u operación firmada por quien ya usa el sistema", "ProInnóvate: validación y escalamiento. Red CITE del ITP"],
        ],
        titulo="Tramos de la escala TRL, documento que acredita cada uno e instrumento que lo admite"
    )
    + "\n"
    + dato_clave(
        "La NASA formuló la escala en los años setenta con siete niveles, y la redefinición "
        "de 1995 añadió el 8 y el 9. La Comisión Europea la adaptó a la investigación en "
        "2014, para Horizonte 2020."
    )
    + "\n"
    + criterio(
        "Cada nivel declarado lleva el documento que lo acredita, con fecha y autor; sin "
        "ese documento el nivel es el anterior. Los ensayos se hacen en la Red CITE del "
        "ITP: 46 centros, dato de 2024."
    )
    + "\n"
    + fuente_pie(F_FRASCATI, F_HELIYON, F_POLCTI_DIAG)
)


TRL_SIM_JS = """\t\t<script type="module">
\t\t\t// Simulación: el nivel TRL gobierna qué instrumentos admiten el proyecto.
\t\t\t// Al recorrer el deslizador de extremo a extremo el veredicto cambia en
\t\t\t// los dos cortes reales de la escala (3-4 y 6-7). Una simulación que no
\t\t\t// cambia de conclusión no demuestra nada (METODOLOGIA.md §7.1).
\t\t\tconst TRAMOS = [
\t\t\t\t{ max: 3, tramo: "TRL 1-3", que: "Principio verificado, concepto formulado",
\t\t\t\t  admite: ["PROCIENCIA · investigación básica", "PROCIENCIA · investigación aplicada"],
\t\t\t\t  excluye: ["ProInnóvate · validación y escalamiento", "Capital semilla y de riesgo"],
\t\t\t\t  estado: "ok" },
\t\t\t\t{ max: 6, tramo: "TRL 4-6", que: "Prototipo validado en entorno relevante",
\t\t\t\t  admite: ["ProInnóvate · desarrollo tecnológico", "Proyectos de I+D con empresa asociada", "Red CITE · servicios de ensayo"],
\t\t\t\t  excluye: ["PROCIENCIA · investigación básica", "Capital semilla y de riesgo"],
\t\t\t\t  estado: "warn" },
\t\t\t\t{ max: 9, tramo: "TRL 7-9", que: "Sistema probado y operando en entorno real",
\t\t\t\t  admite: ["ProInnóvate · validación y escalamiento", "Capital semilla y de riesgo", "Red CITE · asistencia técnica"],
\t\t\t\t  excluye: ["PROCIENCIA · investigación básica", "PROCIENCIA · investigación aplicada"],
\t\t\t\t  estado: "danger" },
\t\t\t];

\t\t\tconst mando = document.getElementById("trl");
\t\t\tconst nivel = document.getElementById("trl-nivel");
\t\t\tconst tramo = document.getElementById("trl-tramo");
\t\t\tconst que = document.getElementById("trl-que");
\t\t\tconst admite = document.getElementById("trl-admite");
\t\t\tconst excluye = document.getElementById("trl-excluye");

\t\t\tfunction pintar() {
\t\t\t\tconst n = Number(mando.value);
\t\t\t\tconst t = TRAMOS.find((x) => n <= x.max);
\t\t\t\tnivel.textContent = "TRL " + n;
\t\t\t\ttramo.textContent = t.tramo;
\t\t\t\ttramo.dataset.estado = t.estado;
\t\t\t\tque.textContent = t.que;
\t\t\t\tadmite.innerHTML = t.admite.map((x) => "<li>" + x + "</li>").join("");
\t\t\t\texcluye.innerHTML = t.excluye.map((x) => "<li>" + x + "</li>").join("");
\t\t\t}
\t\t\tmando.addEventListener("input", pintar);
\t\t\tpintar();
\t\t</script>"""

TRL_SIM = envolver(
    cabecera("01 · Medir la madurez", "Instrumentos admisibles por nivel de la escala TRL", "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim" data-sim="trl" data-animate="fade-up">
\t\t\t\t\t<div class="sim__controls">
\t\t\t\t\t\t<label class="sim__label" for="trl">Nivel de madurez del proyecto</label>
\t\t\t\t\t\t<input class="sim__range" id="trl" type="range" min="1" max="9" step="1" value="2" />
\t\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t\t<span class="sim__value" id="trl-nivel">TRL 2</span>
\t\t\t\t\t\t\t<span class="sim__badge" id="trl-tramo" data-estado="ok">TRL 1-3</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="sim__what" id="trl-que">Principio verificado, concepto formulado</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Instrumentos que lo admiten</h3>
\t\t\t\t\t\t\t<ul id="trl-admite"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Instrumentos que lo declararían inadmisible</h3>
\t\t\t\t\t\t\t<ul id="trl-excluye"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">El conjunto admisible cambia en
\t\t\t\tdos puntos: entre TRL 3 y 4, y entre TRL 6 y 7. Ahí cambia la ventanilla.</p>"""
    + "\n"
    + criterio(
        "Casi ningún proyecto está entero en un tramo. Se declara el del componente que se "
        "va a ejecutar con el dinero solicitado, y lo ya alcanzado entra como antecedente, "
        "con el documento que lo acredita."
    )
    + "\n"
    + evitar(
        "Declarar el tramo por el equipamiento: un banco de ensayo recién comprado no sube "
        "ningún nivel mientras no exista un ensayo documentado."
    )
    + "\n"
    + fuente_pie(F_HELIYON)
)


TRL_LIMITES = envolver(
    cabecera("01 · Medir la madurez", "Los cuatro cuadrantes de madurez técnica y disposición a adoptar", "i-alert")
    + "\n"
    + duo(
        figura(
            "s1-trl-adopcion",
            "Madurez técnica frente a disposición de la organización a adoptar",
            "<b>La escala recorre un solo eje: un sistema en TRL 9 puede quedarse en el "
            "cuadrante donde nadie cambia su forma de trabajar.</b>",
        ),
        dato_clave(
            "La escala tiene <b>nueve niveles</b> y los nueve miden lo mismo: cuánta "
            "incertidumbre técnica queda. La revisión de <b>2024</b> de su uso fuera de la "
            "ingeniería concluye que no captura la dimensión organizativa del despliegue."
        )
        + "\n"
        + conclusion(
        "Cómo se usa entonces:",
                    "El TRL sirve para elegir el instrumento al que se postula, no para argumentar "
            "impacto. El impacto se sostiene con evidencia de adopción, que es otra cosa y "
            "se demuestra de otra manera.",
        ),
        invertir=False,
    )
    + "\n"
    + fuente_pie(F_HELIYON)
)


HERRAMIENTAS_01 = bloque_herramientas(
    ref="01", total="04",
    titulo="Buscadores académicos y su tipo de búsqueda",
    para_que=(
        "El primero de los cinco criterios de Frascati es la novedad, y la novedad se "
        "sostiene con el estado del arte. Un asistente de chat devuelve referencias "
        "plausibles; estos devuelven el DOI, y un evaluador puede abrirlo."
    ),
    herramientas=[
        ("Google Scholar", "Google", [
            "La cobertura más ancha: artículos, tesis, preprints y libros",
            "Alertas por término y por autor, que avisan de lo nuevo",
            "No filtra por calidad: la revista se juzga aparte",
        ], "scholar.google.com"),
        ("Semantic Scholar", "Allen Institute for AI", [
            "Base abierta con DOI y metadatos reutilizables sin permiso",
            "Muestra en qué contexto te cita cada trabajo posterior",
            "Interfaz de programación pública para automatizar la búsqueda",
        ], "semanticscholar.org"),
        ("Elicit", "Elicit Research", [
            "Extrae el mismo dato de muchos artículos a una sola tabla",
            "Pensado para revisión sistemática, no para una consulta suelta",
            "Enseña el pasaje del que sale cada celda, que es lo comprobable",
        ], "elicit.com"),
    ],
    como_elegir=[
        ("DOI", "Que el enlace abra el artículo y no una ficha ni un error."),
        ("Licencia", "Si declara la vía de acceso: lo que hay tras muro no sirve."),
        ("Salida", "Si exporta la lista sin volver a teclear ficha por ficha."),
    ],
)

HERRAMIENTAS_02 = bloque_herramientas(
    ref="02", total="04",
    titulo="Asistentes de chat generalistas y su especialidad",
    para_que=(
        "Redactar borradores, clasificar actividades y ordenar información suelta. Es la "
        "familia que todos van a usar y por fuera las tres se parecen; se eligen por lo "
        "que hacen con tus archivos y por dónde vive el trabajo."
    ),
    herramientas=[
        ("ChatGPT", "OpenAI", [
            "Ecosistema de asistentes configurables para tareas que se repiten",
            "Lee archivos y también imágenes dentro de la conversación",
            "La base instalada mayor, útil si el equipo ya trabaja con él",
        ], "chatgpt.com"),
        ("Claude", "Anthropic", [
            "Documentos largos y trabajo sostenido sobre varios archivos a la vez",
            "Sigue encargos escritos con muchas condiciones sin perder ninguna",
            "Trabaja sobre una carpeta entera desde su propia aplicación",
        ], "claude.ai"),
        ("Gemini", "Google", [
            "Integrado con Documentos, Hojas de cálculo, Drive y Gmail",
            "Lee lo que ya está en tu Drive sin volver a subirlo",
            "Devuelve el resultado directamente a un documento editable",
        ], "gemini.google.com"),
    ],
    como_elegir=[
        ("Contexto", "Qué le puedes dar a leer: un archivo, una carpeta, tu Drive."),
        ("Rastro", "Si dice de dónde saca lo que afirma o hay que creerle."),
        ("Datos", "Qué hace con lo que subes, antes de subir nada del proyecto."),
    ],
)



# ==========================================================================
# TEMA A · lo que el sistema produce (láminas de dato)
# ==========================================================================

PRODUCCION = envolver(
    cabecera("01 · Lo que el país produce", "Publicaciones en Scopus por cada 100 000 habitantes: Perú y América Latina, 2020", "i-chart")
    + "\n"
    + figura(
        "s1-scopus-100k",
        "Publicaciones en Scopus por 100 000 habitantes: siete países de la región y Canadá, 2020",
        "<b>El Perú cierra la tabla de la región en producción científica por habitante.</b> "
        "Chile publica casi seis veces más; Canadá, casi veinte. Dato de 2020.",
    )
    + "\n"
    + conclusion(
        "Por qué esto importa al formular:",
                "Un estado del arte que solo cite trabajo peruano se queda corto casi siempre. "
        "La revisión tiene que salir del país, y eso obliga a leer en inglés y a usar "
        "repositorios de acceso abierto.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "SCImago Journal &amp; Country Rank · dato de 2020")
)


PATENTES = envolver(
    cabecera("01 · Lo que el país produce", "Patentes registradas por millón de habitantes: Perú y diez países, 2010-2018", "i-patent")
    + "\n"
    + figura(
        "s1-coeficiente-invencion",
        "Patentes registradas por millón de habitantes en once países, promedio 2010-2018",
        "<b>2,1 registros por millón de habitantes: la décima parte de Chile.</b> Escala logarítmica.",
    )
    + "\n"
    + aviso(
        "La consecuencia para un proyecto universitario es directa: <b>casi ningún "
        "resultado peruano se protege antes de publicarse</b>. Publicar destruye la "
        "novedad y con ella la patentabilidad. El orden correcto es proteger y luego publicar."
    )
    + "\n"
    + fuente_pie(F_POLCTI, "OMPI y Banco Mundial, elaboración de INDECOPI")
)


ADJUDICACION = envolver(
    cabecera("01 · Lo que el país produce", "Solicitudes y aprobaciones del beneficio tributario de la Ley 30309, 2016-2022", "i-rubric")
    + "\n"
    + figura(
        "s1-ley-30309",
        "Proyectos presentados y aprobados en la Ley 30309, 2016-2022",
        "<b>352 presentados y 136 aprobados entre 2016 y 2022: 39 % acumulado.</b>",
    )
    + "\n"
    + conclusion(
        "Dato importante:",
                "El primer año aprobó el 11 %; los últimos, más de la mitad. La tasa subió sin que cambiara la ley. Lo que cambió fue el "
        "aprendizaje de los postulantes sobre qué exige la calificación. Esa destreza se "
        "adquiere presentando y leyendo los resultados de convocatorias anteriores.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "Base de datos institucional del CONCYTEC · Ley 30309")
)


# ==========================================================================
# TEMA B · capital humano
# ==========================================================================

RENACYT = envolver(
    cabecera("02 · Capital y capacidades", "Investigadores inscritos en el RENACYT por nivel y por sexo, 2023", "i-users")
    + "\n"
    + figura(
        "s1-renacyt-piramide",
        "Pirámide del RENACYT: ocho niveles y reparto por sexo, 2023",
        "<b>Cuatro de cada diez investigadores están en el nivel de entrada.</b> El 31,4 % son mujeres.",
    )
    + "\n"
    + conclusion(
        "Consecuencia práctica para un equipo:",
                "Las convocatorias puntúan la calificación del investigador principal, y el sistema "
        "tiene pocos investigadores de nivel alto. Un equipo mixto de docentes y estudiantes "
        "compite mejor si nombra con precisión quién aporta qué, en vez de listar a todo el "
        "laboratorio.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "RENACYT · Registro Nacional de Investigadores, dato de 2023")
)


UNIVERSIDADES = envolver(
    cabecera("02 · Capital y capacidades", "Puesto mundial y regional de seis universidades peruanas en SCImago, 2023", "i-building")
    + "\n"
    + duo(
        figura(
            "s1-universidades-sir",
            "Universidades peruanas en el ranking SCImago de instituciones, 2023",
            "<b>La primera peruana aparece en el puesto 4 558; la sexta, más de tres "
            "mil puestos por detrás.</b>",
        ),
        conclusion(
        "Lo que esto no significa:",
                "El puesto mide volumen y visibilidad de producción, no la calidad de un "
        "proyecto concreto. Un grupo pequeño con una pregunta bien acotada compite de "
        "igual a igual en una convocatoria, porque lo que se evalúa es la propuesta. "
        "El ranking sirve para elegir socios.",
        ),
        invertir=True,
    )
    + "\n"
    + fuente_pie(F_POLCTI, "SCImago Institutions Rankings SIR-IBER 2023")
)


TRL_FIGURA = envolver(
    cabecera("01 · Medir la madurez", "Los nueve niveles de madurez tecnológica y los cortes 3-4 y 6-7", "i-ladder")
    + "\n"
    + figura(
        "s1-trl-escalera",
        "Los nueve niveles de la escala TRL, con su entorno de prueba",
        "<b>Los dos cortes de la escala marcan el paso al entorno relevante y al entorno real.</b>",
    )
    + "\n"
    + conclusion(
        "Criterio para autoevaluarse:",
                "Los dos cortes no son administrativos: separan investigar, desarrollar y desplegar. "
        "El nivel se demuestra con el <b>entorno en el que ya se probó</b>, no con la "
        "sofisticación del prototipo. Un desarrollo muy elaborado que solo se ha probado "
        "en mesa sigue siendo TRL 4, y postularlo como TRL 7 se detecta en la primera "
        "lectura de los antecedentes.",
    )
    + "\n"
    + fuente_pie(F_FRASCATI, F_HELIYON)
)


# ==========================================================================
# TEMA B
# ==========================================================================

PORTADILLA_B = seccion(
    "Tema 02",
    TEMA_B,
    "Quién decide, quién financia y quién ejecuta la I+D+i+e en el Perú, y qué dicen "
    "los datos sobre lo que ese sistema produce.",
)

ACTORES = envolver(
    cabecera("02 · Quién decide", "Organismos del SINACTI y el instrumento de cada uno", "i-building")
    + "\n"
    + tabla(
        ["Organismo", "Papel en el sistema", "Qué opera", "Enlace oficial"],
        [
            ["CONCYTEC", "Rector de la política de ciencia, tecnología e innovación (CTI)", "SINACTI, RENACYT (registro de investigadores), ALICIA", '<a href="https://www.gob.pe/concytec">gob.pe/concytec</a>'],
            ["PROCIENCIA", "Financiador de investigación", "Concursos de investigación y becas", '<a href="https://prociencia.gob.pe/">prociencia.gob.pe</a>'],
            ["ProInnóvate", "Financiador de innovación empresarial", "Capital semilla, validación, desarrollo tecnológico", '<a href="https://www.proinnovate.gob.pe/">proinnovate.gob.pe</a>'],
            ["INDECOPI", "Autoridad de propiedad intelectual", "Patentes, modelos de utilidad, marcas", '<a href="https://www.indecopi.gob.pe/">indecopi.gob.pe</a>'],
            ["ITP · Red CITE", "Extensionismo tecnológico", "Servicios técnicos a cadenas productivas", '<a href="https://www.gob.pe/952-centros-de-innovacion-productiva-y-transferencia-tecnologica-cite">gob.pe · Red CITE</a>'],
            ["SUNEDU", "Supervisión universitaria", "Licenciamiento y RENATI", '<a href="https://www.gob.pe/sunedu">gob.pe/sunedu</a>'],
        ],
        titulo="Organismos del SINACTI, su papel y el instrumento que operan"
    )
    + "\n"
    + conclusion(
        "Regla para orientarse:",
        "PROCIENCIA financia <b>preguntas</b>; ProInnóvate financia <b>productos</b>. Si "
        "el proyecto todavía tiene una hipótesis abierta, el instrumento está del lado de "
        "PROCIENCIA; si ya tiene una solución que necesita llegar al mercado, del lado de "
        "ProInnóvate.",
    )
    + "\n"
    + fuente_pie(F_DS, F_POLCTI)
)


HITOS = envolver(
    cabecera("02 · Quién decide", "Seis hitos normativos del sistema peruano de CTI, 1968-2025", "i-calendar")
    + "\n"
    + figura(
        "s1-hitos-cti-peru",
        "Secuencia de los hitos normativos de la CTI peruana, de 1968 a 2025",
        "<b>La mitad de la arquitectura vigente es de la última década.</b> Intervalos iguales, no escala temporal.",
    )
    + "\n"
    + f"""\t\t\t\t<div class="bigfig-row" data-animate="fade-up">
{dato("1 % del PBI", "meta de gasto en I+D sobre el producto bruto interno al año 2030")}
{dato("6 objetivos", "prioritarios de esa política, desarrollados en 18 lineamientos", "navy")}
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_DS, F_POLCTI)
)


ALIANZA = envolver(
    cabecera("02 · Cuánto y dónde", "Gasto en I+D sobre el PBI en la Alianza del Pacífico, 2018", "i-chart")
    + "\n"
    + figura(
        "s1-alianza-pacifico",
        "Gasto en I+D sobre el PBI: México, Chile, Colombia y Perú, 2018",
        "<b>Último de los cuatro socios: México invierte cuatro veces y media más.</b>",
    )
    + "\n"
    + conclusion(
        "Lo que esto cambia para una propuesta:",
                "La competencia por fondos nacionales es alta y los montos son acotados. La "
        "cooperación internacional y los fondos regionales dejan de ser una alternativa "
        "exótica y pasan a formar parte del plan de financiamiento.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_UNESCO)
)


GII = envolver(
    cabecera("02 · Cuánto y dónde", "Puesto de nueve países de América Latina en el Global Innovation Index 2025", "i-globe")
    + "\n"
    + figura(
        "s1-gii-latam",
        "Posición de nueve economías latinoamericanas entre las 139 del Global Innovation Index 2025",
        "<b>Octavo en la región y 80 del mundo entre 139 economías.</b>",
    )
    + "\n"
    + aviso(
        "El índice se recompone cada año y ajusta su metodología con cierta frecuencia. "
        "Al citarlo en una propuesta se indica <b>la edición</b>: «puesto 80 de 139, "
        "Global Innovation Index 2025». Un puesto sin edición no es un dato."
    )
    + "\n"
    + fuente_pie(F_GII)
)


EVIDENCIA = envolver(
    cabecera("02 · Cómo funciona un sistema", "Triple, cuádruple y quíntuple hélice: los actores de cada modelo", "i-network")
    + "\n"
    + figura(
        "s1-helices",
        "Los tres modelos de hélice y el actor que añade cada uno",
        "<b>Cada modelo contiene al anterior: la quíntuple hélice sigue exigiendo la "
        "interacción entre universidad, empresa y Estado.</b>",
    )
    + "\n"
    + dato_clave(
        "En América Latina explican el desempeño innovador la <b>calidad institucional</b> "
        "y el <b>capital humano</b> antes que el gasto. El Perú cuenta 5 700 investigadores "
        "RENACYT en 2023."
    )
    + "\n"
    + criterio(
        "El convenio fija cuatro cosas antes de firmarse: qué resultado se transfiere, "
        "quién lo recibe, con qué indicador y en qué fecha se mide. Sin indicador, lo "
        "que se produce es un acto de firma."
    )
    + "\n"
    + fuente_pie(F_ZAPATA, F_TTO, F_RANTALA,
                 "RENACYT · Registro Nacional de Investigadores, dato de 2023")
)


CAPACIDAD = envolver(
    cabecera("02 · Cómo funciona un sistema", "Los tres determinantes de la capacidad de innovación de un sistema", "i-ladder")
    + "\n"
    + tabla(
        ["Determinante", "Qué aporta", "Qué pasa si falta"],
        [
            ["Capital humano formado", "Quien usa el equipamiento y formula el proyecto", "El equipo se compra y no se usa"],
            ["Infraestructura", "Laboratorio, equipamiento, acceso a datos", "La pregunta no se puede responder"],
            ["Vínculos con el sector productivo", "La demanda que orienta y cofinancia", "El resultado no encuentra usuario"],
        ],
        titulo="Determinantes de la capacidad de innovación y efecto de su ausencia",
    )
    + "\n"
    + criterio(
        "Cada determinante se acredita con su documento: el <b>capital humano</b> con el "
        "nivel RENACYT del investigador principal; la <b>infraestructura</b> con el "
        "inventario del laboratorio; el <b>vínculo productivo</b> con la carta de la empresa."
    )
    + "\n"
    + en_la_practica(
        "El estudio sobre países en desarrollo concluye que los tres determinantes <b>no "
        "son independientes</b>: invertir en infraestructura sin capital humano formado no "
        "produce capacidad, porque no hay quien la use."
    )
    + "\n"
    + fuente_pie(F_NOVILLO)
)


QUIEN_SIM_JS = """\t\t<script type="module">
\t\t\t// El tipo de entidad que postula decide a qué instrumentos puede acceder.
\t\t\t// Es la segunda decisión encadenada, después del TRL, y la que más
\t\t\t// veces se descubre tarde: se elige el fondo y luego se ve que la
\t\t\t// entidad no califica. Al recorrer las cinco figuras, el conjunto
\t\t\t// admisible cambia en las cinco (METODOLOGIA.md §3.3).
\t\t\tconst FIGURAS = {
\t\t\t\tuniversidad: {
\t\t\t\t\tque: "Universidad pública o privada licenciada, con su vicerrectorado de investigación",
\t\t\t\t\tpuede: ["Investigación básica y aplicada", "Proyectos con empresa asociada", "Equipamiento científico"],
\t\t\t\t\tno: ["Capital semilla para emprendimiento", "Validación y escalamiento comercial"],
\t\t\t\t\tnota: "Postula la institución, no el docente: el titular del proyecto es la universidad." },
\t\t\t\tempresa: {
\t\t\t\t\tque: "Empresa formal con ventas declaradas y RUC activo",
\t\t\t\t\tpuede: ["Desarrollo tecnológico", "Validación y escalamiento", "Proyectos de I+D con universidad"],
\t\t\t\t\tno: ["Investigación básica"],
\t\t\t\t\tnota: "Casi siempre exige contrapartida en efectivo, no solo valorizada." },
\t\t\t\temprendedor: {
\t\t\t\t\tque: "Persona natural o equipo sin empresa constituida todavía",
\t\t\t\t\tpuede: ["Capital semilla para emprendimiento innovador"],
\t\t\t\t\tno: ["Investigación básica", "Desarrollo tecnológico empresarial", "Equipamiento científico"],
\t\t\t\t\tnota: "La constitución de la empresa suele ser condición para el desembolso, no para postular." },
\t\t\t\tasociacion: {
\t\t\t\t\tque: "Asociación, cooperativa o comunidad productiva",
\t\t\t\t\tpuede: ["Extensionismo tecnológico y servicios CITE", "Proyectos asociativos con universidad"],
\t\t\t\t\tno: ["Capital semilla", "Investigación básica"],
\t\t\t\t\tnota: "Necesita casi siempre una entidad de investigación como asociada." },
\t\t\t\tinstituto: {
\t\t\t\t\tque: "Instituto público de investigación adscrito a un ministerio, con la I+D en su ley de creación",
\t\t\t\t\tpuede: ["Investigación aplicada de su sector", "Proyectos en consorcio con universidad o empresa", "Equipamiento científico"],
\t\t\t\t\tno: ["Capital semilla para emprendimiento"],
\t\t\t\t\tnota: "El régimen público fija su límite: el equipo se arma con el personal que ya tiene contratado." },
\t\t\t};

\t\t\tconst botones = document.querySelectorAll("[data-figura]");
\t\t\tconst que = document.getElementById("q-que");
\t\t\tconst puede = document.getElementById("q-puede");
\t\t\tconst no = document.getElementById("q-no");
\t\t\tconst nota = document.getElementById("q-nota");

\t\t\tfunction pintar(clave) {
\t\t\t\tconst f = FIGURAS[clave];
\t\t\t\tque.textContent = f.que;
\t\t\t\tpuede.innerHTML = f.puede.map((x) => "<li>" + x + "</li>").join("");
\t\t\t\tno.innerHTML = f.no.map((x) => "<li>" + x + "</li>").join("");
\t\t\t\tnota.textContent = f.nota;
\t\t\t\tfor (const b of botones) b.classList.toggle("is-on", b.dataset.figura === clave);
\t\t\t}
\t\t\tfor (const b of botones) b.addEventListener("click", () => pintar(b.dataset.figura));
\t\t\tpintar("universidad");
\t\t</script>"""

QUIEN_SIM = envolver(
    cabecera("02 · Quién decide", "Instrumentos admitidos por tipo de entidad postulante", "i-users")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="quien" data-animate="fade-up">
\t\t\t\t\t<div class="picker">
\t\t\t\t\t\t<button class="picker__btn is-on" type="button" data-figura="universidad">Universidad</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="empresa">Empresa formal</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="emprendedor">Persona o equipo</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="asociacion">Asociación o cooperativa</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-figura="instituto">Instituto público</button>
\t\t\t\t\t</div>
\t\t\t\t\t<p class="sim__what" id="q-que"></p>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-check")}Puede postular a</h3>
\t\t\t\t\t\t\t<ul id="q-puede"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel sim__panel--no">
\t\t\t\t\t\t\t<h3>{ico("i-alert")}Queda fuera de</h3>
\t\t\t\t\t\t\t<ul id="q-no"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + f"""\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<p><span class="conclusion__label">Detalle que decide la postulación:</span>
\t\t\t\t\t<span id="q-nota"></span></p>
\t\t\t\t</div>"""
    + "\n"
    + ejemplo(
        "Detrás de cada tipo de postulante hay una población acotada: 94 universidades "
        "licenciadas por la SUNEDU, y solo 47 con doctorado reconocido en marzo de 2020. "
        "Cifras del diagnóstico de la Política Nacional de CTI, 2024."
    )
    + "\n"
    + fuente_pie(F_DS, F_POLCTI_DIAG)
)


# ==========================================================================
# CIERRE
# ==========================================================================

HERRAMIENTAS_03 = bloque_herramientas(
    ref="03", total="04",
    titulo="Vías de consulta de la norma vigente y su versión",
    para_que=(
        "La arquitectura normativa cambia y media de ella es de la última década. Citar "
        "un decreto derogado o una versión anterior de un artículo invalida el apartado "
        "de marco legal de una propuesta."
    ),
    herramientas=[
        ("El Peruano", "Diario Oficial del Estado", [
            "Publica la norma el día en que empieza a existir",
            "La edición diaria se descarga completa y con fecha",
            "El número de la norma y su fecha son la cita que se escribe",
        ], "elperuano.pe"),
        ("SPIJ", "Ministerio de Justicia", [
            "Da el texto consolidado, con las modificaciones ya incorporadas",
            "Indica qué artículos siguen vigentes y cuáles se derogaron",
            "Evita citar la versión original de una norma ya modificada",
        ], "spij.minjus.gob.pe"),
        ("gob.pe", "Plataforma del Estado peruano", [
            "Reúne las normas por entidad que las emite",
            "Enlaza cada norma con el organismo que la aplica",
            "Punto de entrada cuando se sabe el tema pero no el número",
        ], "gob.pe"),
    ],
    como_elegir=[
        ("Vigencia", "Si el texto que lees es el consolidado o el del día de publicación."),
        ("Cita", "Número, fecha y el medio en que se publicó, siempre los tres."),
        ("Consulta", "La fecha en que lo miraste: la norma puede cambiar mañana."),
    ],
)

HERRAMIENTAS_04 = bloque_herramientas(
    ref="04", total="04",
    titulo="Registros de investigadores y producción del país",
    para_que=(
        "Las convocatorias puntúan la calificación del investigador principal y el "
        "párrafo de contexto se cae si una cifra no se puede seguir hasta su fuente. "
        "Los tres registros responden preguntas distintas y ninguno responde las otras."
    ),
    herramientas=[
        ("RENACYT", "CONCYTEC", [
            "Clasifica a los investigadores por nivel, y ese nivel puntúa",
            "Consulta pública por nombre y por institución",
            "Sirve para armar el equipo antes de escribir la propuesta",
        ], "renacyt.concytec.gob.pe"),
        ("ALICIA", "CONCYTEC", [
            "Repositorio nacional de tesis y artículos de entidades peruanas",
            "Búsqueda por institución y por área temática",
            "Dice si ya existe un grupo peruano trabajando el mismo tema",
        ], "alicia.concytec.gob.pe"),
        ("SCImago", "SCImago Lab", [
            "Producción y citas por país, área temática e institución",
            "Edición anual: el año forma parte del dato y se cita siempre",
            "Da la cifra de contexto y ayuda a elegir con quién asociarse",
        ], "scimagojr.com"),
    ],
    como_elegir=[
        ("Unidad", "Que publique el dato con su unidad y su año, no el número solo."),
        ("Fecha", "Cuándo se actualizó, o se cita la fecha en que se consultó."),
        ("Alcance", "Si el dato existe para tu región o solo a nivel nacional."),
    ],
)


PROBLEMAS = envolver(
    cabecera("Cierre", "Errores frecuentes en una postulación y su detección", "i-alert")
    + "\n"
    + '\t\t\t\t<div class="problem-grid" data-animate="fade-up">\n'
    + "\n".join([
        problema(
            "El TRL declarado no coincide con la evidencia",
            "La propuesta afirma TRL 6 y los antecedentes solo documentan ensayos de mesa.",
            "Se declara el nivel que se espera alcanzar al terminar, no el que ya está acreditado.",
            "Pedirle a cada nivel un documento fechado: informe de ensayo, acta de instalación o registro de campo. Si el único "
            "entorno probado es el laboratorio, el nivel baja a TRL 4 y con él cambia el instrumento.",
        ),
        problema(
            "Se declara innovación lo que todavía es desarrollo",
            "Entra a un fondo de escalamiento y cae en admisibilidad, sin llegar a la evaluación técnica.",
            "Oslo 2018 exige que el resultado esté puesto a disposición de terceros, y el prototipo no lo está.",
            "Buscar en el texto el nombre propio de quien ya lo usa. Si no aparece una empresa, una cooperativa o un "
            "establecimiento con nombre, el componente se reclasifica como desarrollo experimental.",
        ),
        problema(
            "Cifras de contexto sin unidad, año ni fuente",
            "El evaluador marca el diagnóstico como no verificable y el resto de la propuesta pierde crédito.",
            "Las cifras se toman de resúmenes de prensa o de presentaciones que citan sin referenciar.",
            "Seguir cada cifra hasta el documento que la publica y anotar edición y año. La que solo abre tras una "
            "suscripción se sustituye por otra de acceso abierto.",
        ),
        problema(
            "El fondo se elige por el monto y no por lo que financia",
            "Un proyecto con hipótesis abierta se presenta a un instrumento de escalamiento, o al revés.",
            "La búsqueda empieza por el importe de la convocatoria y no por lo que el organismo financia.",
            "PROCIENCIA financia preguntas; ProInnóvate financia productos. Y antes de cerrar la búsqueda, revisar el sector "
            "Producción, que opera 71 de los 164 instrumentos de CTI registrados entre 2012 y 2018.",
        ),
        problema(
            "La figura con la que se postula no califica",
            "La propuesta se descarta en admisibilidad sin que nadie llegue a leer la parte técnica.",
            "El instrumento se elige por la materia y la condición de postulante se comprueba al final.",
            "Leer las bases primero por el postulante. Un equipo sin empresa constituida queda fuera del desarrollo "
            "tecnológico empresarial; una empresa formal, fuera de la investigación básica.",
        ),
        problema(
            "El resultado se publica antes de protegerlo",
            "La propuesta compromete una patente y el trabajo ya está publicado o presentado en un congreso.",
            "La divulgación previa destruye la novedad, que es el primer requisito que examina INDECOPI.",
            "Fechar cada divulgación prevista y colocar la solicitud antes de la primera. El país registra 2,1 patentes por "
            "millón de habitantes en el promedio 2010-2018, la décima parte de Chile.",
        ),
    ])
    + "\n\t\t\t\t</div>"
    + "\n"
    + fuente_pie(
        F_OSLO,
        F_POLCTI,
        "Estudio de línea base del gasto público en CTI (Rogers, 2020)",
        "OMPI y Banco Mundial, elaboración de INDECOPI",
    )
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
    cabecera("Cierre", "Doce términos de los dos temas, con su equivalente en inglés", "i-book")
    + "\n"
    + '\t\t\t\t<div class="glossary glossary--grouped" data-animate="fade-up">\n'
    + _grupo_glosario("Tema 01 · Definiciones y madurez tecnológica", [
        termino("I+D", "R&amp;D",
                "Los cinco criterios de Frascati se cumplen a la vez o no se cumple ninguno. Con cuatro de cinco, la propuesta cae en admisibilidad."),
        termino("Desarrollo experimental", "experimental development",
                "La parte que produce el prototipo. Se financia con desarrollo tecnológico."),
        termino("Innovación", "innovation",
                "Exige un usuario nombrado que ya lo use. Sin nombre propio de empresa, cooperativa o establecimiento, lo que hay es desarrollo."),
        termino("TRL", "technology readiness level",
                "Mide la incertidumbre técnica que queda, no la calidad de la idea. El nivel se acredita con el entorno donde ya se probó."),
        termino("CRL", "commercial readiness level",
                "Usuario identificado, propuesta de valor contrastada y ventas repetidas."),
        termino("Estado del arte", "state of the art",
                "Lo ya publicado sobre el problema, que fija qué sería nuevo. Sostiene el criterio de novedad ante el evaluador y ante INDECOPI."),
    ])
    + "\n"
    + _grupo_glosario("Tema 02 · Institucionalidad del sistema peruano", [
        termino("SINACTI", "national STI system",
                "Los organismos que deciden, financian y ejecutan la política de CTI."),
        termino("Instrumento de CTI", "STI policy instrument",
                "Beca, concurso, subvención, servicio tecnológico o beneficio tributario."),
        termino("RENACYT", "national researchers register",
                "Registro que clasifica a los investigadores por nivel. Las convocatorias puntúan el nivel del investigador principal."),
        termino("Triple hélice", "triple helix",
                "Universidad, empresa y Estado. El vínculo transfiere tecnología solo cuando el convenio fija indicador y fecha de medición."),
        termino("Admisibilidad", "eligibility",
                "Filtro previo a la evaluación técnica: si no encaja, la propuesta no se lee."),
        termino("PBI", "gross domestic product",
                "El denominador con el que se compara el gasto en I+D entre países."),
        termino("Acceso abierto", "open access",
                "Descarga sin suscripción y con licencia declarada. Una fuente tras un muro de pago se da por no verificable."),
    ], "b")
    + "\n\t\t\t\t</div>"
    + "\n"
    + fuente_pie(F_FRASCATI, F_OSLO, F_HELIYON, F_DS)
)


RESUMEN = envolver(
    cabecera("Cierre", "Lo que queda establecido", "i-check")
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}Queda establecido</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Una actividad es I+D solo si cumple los cinco criterios de Frascati a la vez.</li>
\t\t\t\t\t\t\t<li>Un resultado es innovación solo si está en uso por terceros.</li>
\t\t\t\t\t\t\t<li>El nivel TRL determina qué instrumentos admiten el proyecto.</li>
\t\t\t\t\t\t\t<li>PROCIENCIA financia preguntas; ProInnóvate financia productos.</li>
\t\t\t\t\t\t\t<li>Toda cifra de contexto va con unidad, año y fuente descargable.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-arrow-right")}Lo que se lleva a la sesión 2</h3>
\t\t\t\t\t\t<p>La ficha del taller 01 y la ruta del taller 03. En la sesión 2 esa
\t\t\t\t\t\tficha adopta una <b>figura jurídica</b>: se decide si el proyecto es una
\t\t\t\t\t\t<i>spin-off</i> universitaria, una <i>startup</i> independiente o una licencia a un
\t\t\t\t\t\ttercero, y qué protección le corresponde.</p>
\t\t\t\t\t\t<p>La limitación que arrastramos: hoy sabemos <b>a quién</b> dirigirnos,
\t\t\t\t\t\tpero todavía no <b>desde qué figura</b> se postula. Eso es lo que decide
\t\t\t\t\t\tquién es el titular de los resultados.</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
)

REFERENCIAS = envolver(
    cabecera("Cierre", "Fuentes de la sesión y vía de acceso", "i-quote")
    + "\n"
    + tabla(
        ["Fuente", "Sirve a", "Acceso"],
        [
            ["OCDE (2015) <i>Frascati</i> y OCDE-Eurostat (2018) <i>Oslo</i>", "Definiciones, criterios, tipos y umbral de innovación", '<a href="https://www.oecd.org/en/publications/frascati-manual-2015_9789264239012-en.html">oecd.org</a> · lectura abierta'],
            ["OMPI (2025). <i>Global Innovation Index 2025</i>", "Posición del Perú y de la región", '<a href="https://www.wipo.int/en/web/global-innovation-index">wipo.int</a> · CC BY 4.0 IGO'],
            ["CONCYTEC (2024). <i>Política Nacional de CTI al 2030</i>", "Gasto en I+D, metas y objetivos", '<a href="https://www.gob.pe/institucion/pcm/normas-legales/6967622-093-2025-pcm">gob.pe</a> · documento público'],
            ["Zapata-Cantu y González (2021). <i>Sustainability</i> 13(7):4077", "Instituciones y capital humano en la región", '<a href="https://doi.org/10.3390/su13074077">doi.org/10.3390/su13074077</a> · CC BY 4.0'],
            ["Novillo-Villegas et al. (2022). <i>Sustainability</i> 14(11):6686", "Ruta de capacidad de innovación", '<a href="https://doi.org/10.3390/su14116686">doi.org/10.3390/su14116686</a> · CC BY 4.0'],
            ["Salvador-Carulla et al. (2024). <i>Heliyon</i> 10:e29930", "Alcance y límites del TRL", '<a href="https://doi.org/10.1016/j.heliyon.2024.e29930">Heliyon</a> · CC BY-NC 4.0'],
            ["Hailu (2024) y Rantala et al. (2021)", "Evidencia sobre triple hélice", '<a href="https://doi.org/10.1163/21971927-bja10011">Triple Helix</a> · CC BY 4.0'],
        ],
        titulo="Fuentes citadas en la sesión y su vía de acceso"
    )
) + "\n" + colofon_flotante()


# ==========================================================================
# LÁMINAS AÑADIDAS EN LA SEGUNDA PASADA
# ==========================================================================
# Los pies de figura se ajustan al límite de la skill paper-visuals: 25
# palabras o menos, interpretativos y no descriptivos. El contexto que antes
# iba en el pie pasa al cuerpo de la lámina, donde puede extenderse.

BRECHA = envolver(
    cabecera("01 · Punto de partida", "Perú frente a Chile en cuatro indicadores de innovación, 2010-2025", "i-scale")
    + "\n"
    + figura(
        "s1-brecha-chile",
        "Gasto, publicaciones, patentes y puesto en el índice de innovación: Perú y Chile, 2010-2025",
        "<b>Entre tres y diez veces por detrás de Chile, mida lo que se mida.</b>",
    )
    + "\n"
    + conclusion(
        "Lo que descarta esta figura:",
                "La brecha no se explica por un indicador mal construido ni por un año atípico. "
        "Cuatro medidas independientes apuntan en la misma dirección: dinero, "
        "publicaciones, patentes y posición compuesta. Cada indicador está normalizado "
        "contra su propio máximo porque sus unidades no son comparables entre sí.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_GII)
)


META = envolver(
    cabecera("02 · Cuánto y dónde", "Gasto en I+D vigente, media regional y meta nacional para 2030", "i-target")
    + "\n"
    + figura(
        "s1-meta-pbi",
        "Gasto vigente en I+D frente a la meta nacional para 2030",
        "<b>Del 0,13 % actual al 1 % comprometido hay siete veces de distancia.</b>",
    )
    + "\n"
    + conclusion(
        "Cómo se lee una meta así en una propuesta:",
        "La meta declara una dirección de política, no un presupuesto comprometido. Un "
        "proyecto alineado con los objetivos prioritarios compite mejor que uno que los "
        "ignora, aunque el gasto total no cambie.",
    )
    + "\n"
    + fuente_pie(F_DS, F_POLCTI)
)


CONCENTRACION = envolver(
    cabecera("02 · Quién decide", "Distribución del presupuesto público de CTI entre 164 instrumentos, 2012-2018", "i-fund")
    + "\n"
    + figura(
        "s1-concentracion-gasto",
        "Curva de concentración del presupuesto público de CTI, promedio anual 2012-2018",
        "<b>Cuarenta y cinco instrumentos de ciento sesenta y cuatro acumulan el 90 %.</b>",
    )
    + "\n"
    + definicion(
        "Instrumento de CTI",
        "Política Nacional de CTI 2024",
        "Mecanismo con presupuesto propio con el que un organismo del Estado financia "
        "o presta un servicio de ciencia, tecnología e innovación. Toma <b>cinco "
        "formas</b>: beca, concurso de investigación, subvención a la innovación "
        "empresarial, servicio tecnológico y beneficio tributario.",
        "i-fund",
    )
    + "\n"
    + criterio(
        "La forma decide a qué se postula y con qué. PROCIENCIA opera concursos de "
        "investigación; ProInnóvate, subvenciones; la Red CITE, servicios; la Ley "
        "30309, un beneficio tributario que se solicita después de gastar."
    )
    + "\n"
    + fuente_pie(F_POLCTI, "Estudio de línea base del gasto público en CTI (Rogers, 2020)")
)


SECTORES = envolver(
    cabecera("02 · Quién decide", "Instrumentos de financiamiento de CTI por sector del Estado, 2012-2018", "i-building")
    + "\n"
    + figura(
        "s1-instrumentos-sector",
        "Número de instrumentos de CTI por sector responsable, 2012-2018",
        "<b>Producción y CONCYTEC suman 109 de los 164 instrumentos existentes.</b>",
    )
    + "\n"
    + criterio(
        "Un proyecto de investigación aplicada con salida productiva tiene más puertas que "
        "CONCYTEC: el sector Producción opera setenta y un instrumentos, y conviene "
        "revisarlos antes de cerrar la búsqueda."
    )
    + "\n"
    + fuente_pie(F_POLCTI, "Estudio de línea base del gasto público en CTI (Rogers, 2020)")
)


APRENDIZAJE = envolver(
    cabecera("01 · Lo que el país produce", "Tasa de aprobación de la Ley 30309 entre 2016 y 2022", "i-milestone")
    + "\n"
    + figura(
        "s1-pendiente-30309",
        "Tasa de aprobación del beneficio tributario de la Ley 30309, 2016 y 2022",
        "<b>Del 11 % en 2016 al 53 % en 2022: lo que cambió fue cómo se presenta.</b>",
    )
    + "\n"
    + conclusion(
        "Por qué esta es la figura más importante de la sesión:",
                "La Ley 30309 no se modificó entre esos dos años, ni el presupuesto se amplió. "
        "Lo único que cambió fue el conocimiento de los postulantes sobre qué exige la "
        "calificación.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "Base de datos institucional del CONCYTEC · Ley 30309")
)


OBSTACULOS = envolver(
    cabecera("02 · Capital y capacidades", "Los tres obstáculos a la innovación más declarados por empresas manufactureras", "i-alert")
    + "\n"
    + figura(
        "s1-obstaculos",
        "Porcentaje de empresas manufactureras que declara cada obstáculo a la innovación",
        "<b>Un tercio de las empresas que sí innovaron señala la falta de personal calificado.</b>",
    )
    + "\n"
    + conclusion(
        "Dónde deja esto a un equipo universitario:",
        "Un equipo universitario está en el lado de la oferta. Un grupo con estudiantes formados y un docente que "
        "sabe formular resuelve exactamente la carencia que las empresas declaran. Es el "
        "argumento de valor de una propuesta conjunta.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "INEI · Encuesta Nacional de Innovación en la Industria Manufacturera")
)


TIPOS_INNOVACION = envolver(
    cabecera("01 · Qué cuenta como I+D", "Cinco tipos de innovación según el grado de cambio y el riesgo", "i-bulb")
    + "\n"
    + tabla(
        ["Tipo", "Qué cambia", "Novedad exigida", "Riesgo", "Ejemplo de proyecto universitario"],
        [
            ["Incremental", "Mejora un producto o proceso existente", "Para la unidad", "Bajo", "Bajar un 15 % el consumo de un equipo"],
            ["Radical", "Sustituye la tecnología de base", "Para el mundo", "Alto", "Cambiar el principio de medición de un sensor"],
            ["Arquitectural", "Recombina piezas conocidas de otra forma", "Para el mercado", "Medio", "Integrar tres instrumentos en una cadena"],
            ["De proceso", "Cambia cómo se produce, no qué se produce", "Para la unidad", "Bajo", "Automatizar el registro de un ensayo"],
            ["Organizativa", "Cambia cómo se trabaja o se vincula", "Para la unidad", "Bajo", "Consorcio universidad-cooperativa"],
        ],
        titulo="Tipos de innovación por grado de cambio, novedad exigida y ejemplo universitario"
    )
    + "\n"
    + dato_clave(
        "Oslo 2018 deja dos objetos, producto y proceso de negocio, y seis funciones donde "
        "cabe el segundo: producción, distribución, marketing, sistemas de información, "
        "administración y desarrollo de productos."
    )
    + "\n"
    + ejemplo(
        "La encuesta de innovación manufacturera de 2018 halló que el 55 % de las empresas "
        "encuestadas innovó, y que el 85 % de ellas no protegió lo que hizo."
    )
    + "\n"
    + fuente_pie(F_OSLO, F_POLCTI_DIAG)
)


MODELOS_FLUJO = envolver(
    cabecera("02 · Cómo funciona un sistema", "Lugar de la investigación en los modelos lineal y de eslabón en cadena", "i-flow")
    + "\n"
    + duo(
        figura(
            "s1-modelos-flujo",
            "Modelo lineal y modelo de eslabón en cadena de la innovación",
            "<b>El modelo de eslabón convoca a la investigación cuando un paso no resuelve "
            "con lo que sabe; el lineal la sitúa siempre al principio.</b>",
        ),
        criterio(
            "Las convocatorias de desarrollo tecnológico piden una <b>demanda "
            "identificada</b>, no un hallazgo en busca de aplicación. Los antecedentes "
            "empiezan por el eslabón donde apareció el problema, que casi nunca es el "
            "laboratorio."
        )
        + "\n"
        + conclusion(
        "Por qué importa al formular:",
                    "Presentar el proyecto en orden lineal ante un fondo que espera el modelo de "
            "eslabón se lee como desconexión con el sector productivo, y así lo puntúa la "
            "rúbrica.",
        ),
        invertir=False,
    )
    + "\n"
    + fuente_pie(F_OSLO)
)


# ==========================================================================
# TERCERA PASADA · láminas de figura y dos secciones interactivas
# ==========================================================================

RADAR = envolver(
    cabecera("02 · Cuánto y dónde", "Puesto del Perú en los doce pilares del Índice de Competitividad Global, 2019", "i-target")
    + "\n"
    + f"""\t\t\t\t<div class="split" data-animate="fade-up">
\t\t\t\t\t<div class="split__fig">
\t\t\t\t\t\t<div class="figure__frame figure__frame--tall" data-figure="s1-radar-pilares"></div>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="split__text">
\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t<span class="figure__num">Figura 18</span>
\t\t\t\t\t\t\t<span class="figure__name">Puesto del Perú en los doce pilares de competitividad, entre 141 economías, 2019</span>
\t\t\t\t\t\t\t<span class="figure__say"><b>El perfil no es plano: hay pilares de primer nivel y pilares de cola.</b> Puesto entre 141 economías.</span>
\t\t\t\t\t\t</p>
{dato("Puesto 1", "en estabilidad macroeconómica: la mejor del mundo", "navy")}
{dato("Puesto 90", "en capacidad de innovación, y 98 en adopción de tecnologías")}
\t\t\t\t\t\t<p>El problema peruano no es macroeconómico. La restricción está en los
\t\t\t\t\t\tpilares de <b>instituciones</b>, <b>habilidades</b> y <b>dinamismo
\t\t\t\t\t\tempresarial</b>, que son justamente sobre los que un proyecto de I+D+i+e
\t\t\t\t\t\tpuede actuar. Los vértices abrevian el nombre del pilar: «Macro» es
\t\t\t\t\t\testabilidad macroeconómica; «TIC», adopción de tecnologías de la
\t\t\t\t\t\tinformación; «Productos», mercado de productos.</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_POLCTI, "Foro Económico Mundial · Índice de Competitividad Global 2019")
)


TEMATICAS = envolver(
    cabecera("01 · Lo que el país produce", "Las seis áreas temáticas con más documentos publicados por el Perú, 2019", "i-layers")
    + "\n"
    + figura(
        "s1-treemap-tematicas",
        "Documentos publicados por el Perú según área temática, 2019",
        "<b>Seis áreas concentran la producción; la ingeniería no aparece entre ellas.</b>",
    )
    + "\n"
    + conclusion(
        "Cómo se usa este dato al elegir tema:",
                "Un proyecto en un área poco poblada compite con menos pares nacionales, pero "
        "también encuentra menos revisores y menos socios. La existencia de un grupo con "
        "el que asociarse pesa más que cualquiera de las dos, y se verifica en el "
        "buscador ALICIA antes de fijar el tema.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "SCImago Journal &amp; Country Rank · documentos de 2019")
)


REGIONES = envolver(
    cabecera("02 · Cuánto y dónde", "Índice de Competitividad Regional: primeras y últimas regiones del país, 2023", "i-globe")
    + "\n"
    + figura(
        "s1-regiones",
        "Índice de Competitividad Regional: cinco primeras y cuatro últimas regiones, 2023",
        "<b>La capacidad no está repartida: se concentra en Lima y en tres regiones del sur.</b> Índice de 2023.",
    )
    + "\n"
    + conclusion(
        "Por qué esto abre una puerta:",
                "Varias convocatorias reservan cuota o puntaje adicional a proyectos ejecutados "
        "fuera de Lima. Un equipo de una universidad regional no compite en desventaja: "
        "compite en una categoría distinta, y conviene comprobarlo en las bases antes "
        "de descartar un instrumento.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, "Índice de Competitividad Regional 2023")
)


CASCADA = envolver(
    cabecera("02 · Cuánto y dónde", "Reparto hipotético del salto hasta la meta del 1 % del PBI en 2030", "i-fund")
    + "\n"
    + figura(
        "s1-cascada-meta",
        "Composición del salto necesario hasta la meta del 1 % del PBI",
        "<b>El salto no lo cierra el Estado solo: el reparto intermedio es una hipótesis de trabajo.</b>",
    )
    + "\n"
    + conclusion(
        "Lo que se sigue para un proyecto universitario:",
                "El tramo que más tiene que crecer es el privado, y crece con proyectos "
        "conjuntos entre empresa y universidad. Un proyecto que incorpora una empresa "
        "asociada no solo suma contrapartida: se alinea con la dirección declarada de "
        "la política, y las rúbricas lo puntúan.",
    )
    + "\n"
    + fuente_pie(F_POLCTI, F_DS)
)


MATRIZ = envolver(
    cabecera("01 · Qué cuenta como I+D", "Incertidumbre y aplicación prevista: los cuatro cuadrantes de una actividad", "i-scale")
    + "\n"
    + figura(
        "s1-matriz-proyecto",
        "Clasificación de una actividad según incertidumbre y aplicación prevista",
        "<b>Incertidumbre y aplicación prevista: con esas dos preguntas se clasifica cualquier actividad.</b>",
    )
    + "\n"
    + conclusion(
        "Cómo se usa la matriz:",
                "Se sitúa cada actividad del proyecto, no el proyecto entero. Casi todos caen "
        "en dos casillas a la vez, y esa es la información útil: dice que hay dos "
        "componentes y que cada uno se financia por una vía distinta.",
    )
    + "\n"
    + fuente_pie(F_FRASCATI)
)


EMBUDO = envolver(
    cabecera("01 · Punto de partida", "Etapas entre la idea de proyecto y su uso por terceros", "i-flow")
    + "\n"
    + figura(
        "s1-embudo-idi",
        "Candidatos que superan cada etapa, de la idea al uso por un tercero",
        "<b>Cada etapa pierde candidatos, y la mayor caída ocurre antes de que nadie evalúe la idea.</b>",
    )
    + "\n"
    + aviso(
        "Las proporciones del embudo son de orden de magnitud, no una medición: "
        "ilustran dónde se pierde. La caída mayor está entre <b>idea</b> y "
        "<b>propuesta formulada</b>, que es la etapa que no depende de ningún fondo "
        "ni de ningún evaluador, solo de saber formular."
    )
    + "\n"
    + conclusion(
        "Dónde se puede intervenir:",
        "Las dos primeras caídas son las que un equipo puede reducir. Formular y pasar admisibilidad no dependen del "
        "presupuesto disponible ni del criterio de un evaluador, y juntas explican la "
        "mayor parte de la pérdida.",
    )
)


FRASCATI_JS = """\t\t<script type="module">
\t\t\t// Los cinco criterios se marcan uno a uno y el veredicto cambia. Es la
\t\t\t// forma de enseñar que NO son una lista de deseos: basta que falte uno
\t\t\t// para que la actividad deje de contar como I+D, y ese es exactamente
\t\t\t// el filtro de admisibilidad que aplica el evaluador.
\t\t\tconst casillas = [...document.querySelectorAll('.crit__box input')];
\t\t\tconst veredicto = document.getElementById("fr-veredicto");
\t\t\tconst detalle = document.getElementById("fr-detalle");

\t\t\tfunction pintar() {
\t\t\t\tconst faltan = casillas.filter((c) => !c.checked)
\t\t\t\t\t.map((c) => c.dataset.criterio);
\t\t\t\tif (faltan.length === 0) {
\t\t\t\t\tveredicto.textContent = "Es I+D";
\t\t\t\t\tveredicto.dataset.estado = "ok";
\t\t\t\t\tdetalle.textContent = "Los cinco criterios se cumplen. La actividad puede declararse como investigación y desarrollo ante cualquier fondo.";
\t\t\t\t} else {
\t\t\t\t\tveredicto.textContent = "No es I+D";
\t\t\t\t\tveredicto.dataset.estado = "danger";
\t\t\t\t\tdetalle.textContent = "Falta " + (faltan.length === 1 ? "el criterio" : "los criterios") +
\t\t\t\t\t\t" de " + faltan.join(", ") + ". Declararla como I+D expone la propuesta a caer en admisibilidad.";
\t\t\t\t}
\t\t\t}
\t\t\tfor (const c of casillas) c.addEventListener("change", pintar);
\t\t\tpintar();
\t\t</script>"""


def _crit(clave, rotulo, ayuda, marcado=True):
    ch = " checked" if marcado else ""
    return f"""\t\t\t\t\t\t<label class="crit__box">
\t\t\t\t\t\t\t<input type="checkbox" data-criterio="{clave}"{ch} />
\t\t\t\t\t\t\t<span><b>{rotulo}</b><span class="crit__help">{ayuda}</span></span>
\t\t\t\t\t\t</label>"""


FRASCATI_SIM = envolver(
    cabecera("01 · Qué cuenta como I+D", "Efecto de cada criterio de Frascati en el veredicto de una actividad", "i-rubric")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="frascati" data-animate="fade-up">
\t\t\t\t\t<div class="crit">
{_crit("novedad", "Novedosa", "Busca conocimiento que no existe todavía")}
{_crit("creatividad", "Creativa", "Parte de una hipótesis propia, no de una tarea")}
{_crit("incertidumbre", "Incierta", "El resultado puede no obtenerse")}
{_crit("sistematicidad", "Sistemática", "Hay protocolo, cronograma y registro")}
{_crit("transferibilidad", "Transferible", "Otro equipo podría reproducirla")}
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t<span class="sim__badge" id="fr-veredicto" data-estado="ok">Es I+D</span>
\t\t\t\t\t\t<span class="sim__what" id="fr-detalle"></span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + """\t\t\t\t<p class="sim-caption" data-animate="fade-up">Al desmarcar cualquiera de las
\t\t\t\tcinco casillas el veredicto cambia.</p>"""
    + "\n"
    + f"""\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-alert")}Rutina: queda fuera de la I+D</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Autopsia para determinar la causa de una muerte.</li>
\t\t\t\t\t\t\t<li>Registro diario de temperatura y presión.</li>
\t\t\t\t\t\t\t<li>Prototipo de preproducción para certificar.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>{ico("i-check")}La misma materia, ya como I+D</h3>
\t\t\t\t\t\t<ol>
\t\t\t\t\t\t\t<li>Estudio de una mortalidad para hallar el efecto de un tratamiento.</li>
\t\t\t\t\t\t\t<li>Métodos nuevos de medir la temperatura y de predecir el tiempo.</li>
\t\t\t\t\t\t\t<li>Prototipo para probar un concepto con riesgo alto de fallo.</li>
\t\t\t\t\t\t</ol>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + fuente_pie(F_FRASCATI)
)


INNOV_JS = """\t\t<script type="module">
\t\t\t// El tipo de innovación decide qué evidencia pide el evaluador. Es la
\t\t\t// tercera decisión encadenada de la sesión, después del TRL y de la
\t\t\t// figura del postulante, y la que más se declara por optimismo.
\t\t\tconst TIPOS = {
\t\t\t\tincremental: { riesgo: "Bajo", estado: "ok",
\t\t\t\t\tque: "Mejora medible sobre algo que ya funciona",
\t\t\t\t\tevidencia: ["Línea base del proceso actual, medida", "Magnitud de la mejora esperada, con su método de medición"],
\t\t\t\t\tfondo: "Instrumentos de mejora productiva y extensionismo" },
\t\t\t\tarquitectural: { riesgo: "Medio", estado: "warn",
\t\t\t\t\tque: "Recombinación de piezas conocidas en un orden nuevo",
\t\t\t\t\tevidencia: ["Prueba de que la combinación no está publicada", "Ensayo de integración de al menos dos componentes"],
\t\t\t\t\tfondo: "Desarrollo tecnológico y proyectos con empresa" },
\t\t\t\tradical: { riesgo: "Alto", estado: "danger",
\t\t\t\t\tque: "Sustitución del principio técnico de base",
\t\t\t\t\tevidencia: ["Prueba de concepto del principio nuevo", "Plan explícito de qué se hace si el principio no funciona"],
\t\t\t\t\tfondo: "Investigación aplicada y fondos de alto riesgo" },
\t\t\t\tproceso: { riesgo: "Bajo", estado: "ok",
\t\t\t\t\tque: "Cambio en cómo se produce, no en qué se produce",
\t\t\t\t\tevidencia: ["Tiempos o costos del proceso actual", "Compromiso de la unidad que adoptará el cambio"],
\t\t\t\t\tfondo: "Mejora de productividad y transferencia" },
\t\t\t};
\t\t\tconst botones = document.querySelectorAll("[data-tipo]");
\t\t\tconst riesgo = document.getElementById("in-riesgo");
\t\t\tconst que = document.getElementById("in-que");
\t\t\tconst ev = document.getElementById("in-evidencia");
\t\t\tconst fondo = document.getElementById("in-fondo");

\t\t\tfunction pintar(k) {
\t\t\t\tconst t = TIPOS[k];
\t\t\t\triesgo.textContent = "Riesgo " + t.riesgo.toLowerCase();
\t\t\t\triesgo.dataset.estado = t.estado;
\t\t\t\tque.textContent = t.que;
\t\t\t\tev.innerHTML = t.evidencia.map((x) => "<li>" + x + "</li>").join("");
\t\t\t\tfondo.textContent = t.fondo;
\t\t\t\tfor (const b of botones) b.classList.toggle("is-on", b.dataset.tipo === k);
\t\t\t}
\t\t\tfor (const b of botones) b.addEventListener("click", () => pintar(b.dataset.tipo));
\t\t\tpintar("incremental");
\t\t</script>"""

INNOV_SIM = envolver(
    cabecera("01 · Qué cuenta como I+D", "Cuatro tipos de innovación con su evidencia y su fondo aplicable", "i-sliders")
    + "\n"
    + f"""\t\t\t\t<div class="sim sim--stack" data-sim="innovacion" data-animate="fade-up">
\t\t\t\t\t<div class="picker">
\t\t\t\t\t\t<button class="picker__btn is-on" type="button" data-tipo="incremental">Incremental</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-tipo="arquitectural">Arquitectural</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-tipo="radical">Radical</button>
\t\t\t\t\t\t<button class="picker__btn" type="button" data-tipo="proceso">De proceso</button>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__readout">
\t\t\t\t\t\t<span class="sim__badge" id="in-riesgo" data-estado="ok">Riesgo bajo</span>
\t\t\t\t\t\t<span class="sim__what" id="in-que"></span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sim__panels sim__panels--pair">
\t\t\t\t\t\t<div class="sim__panel sim__panel--ok">
\t\t\t\t\t\t\t<h3>{ico("i-rubric")}Evidencia que pedirá el evaluador</h3>
\t\t\t\t\t\t\t<ul id="in-evidencia"></ul>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="sim__panel">
\t\t\t\t\t\t\t<h3>{ico("i-fund")}Dónde encaja</h3>
\t\t\t\t\t\t\t<p id="in-fondo"></p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""
    + "\n"
    + duo(
        figura(
            "s1-evidencia-por-tipo",
            "Evidencia que acredita cada tipo de innovación ante un evaluador",
            "<b>La evidencia migra al subir el riesgo: de medir lo que ya ocurre a "
            "demostrar el principio nuevo y prever su fallo.</b>",
        ),
        criterio(
            "El riesgo que se declara fija la evidencia que se pide. Declarar una "
            "innovación radical sin la prueba de concepto del principio nuevo es la forma "
            "más rápida de perder el punto de mérito innovador."
        ),
        invertir=True,
    )
    + "\n"
    + fuente_pie(F_OSLO, "Elaboración propia · correspondencia entre tipo declarado y evidencia exigida")
)


# ==========================================================================
# CUARTA PASADA · panorama de herramientas antes de los talleres
# ==========================================================================

HERRAMIENTAS = envolver(
    cabecera("01 · Herramientas de trabajo", "Seis categorías de herramientas de IA y su acceso a los archivos, 2026", "i-robot")
    + "\n"
    + figura(
        "s1-herramientas-ia",
        "Herramientas de IA disponibles en julio de 2026, por categoría de acceso",
        "<b>Las tres categorías del medio comparten motor y se distinguen por dónde "
        "corren: editor, terminal o aplicación propia.</b>",
    )
    + "\n"
    + criterio(
        "El editor con agente y el agente de terminal trabajan sobre un repositorio y "
        "piden manejo de consola. El agente de escritorio opera sobre una carpeta desde su "
        "propia aplicación, como Claude Cowork, publicado el 7 de julio de 2026."
    )
    + "\n"
    + en_la_practica(
        "Para redactar el estado del arte, la búsqueda con citación devuelve el DOI y la "
        "licencia de cada artículo, y el chat de navegador redacta el párrafo con esos "
        "documentos pegados en el contexto."
    )
    + "\n"
    + fuente_pie(
        "Anthropic (2026), <i>Claude Cowork</i> · anuncio de producto del 7 de julio",
        "Google (2025), <i>Antigravity</i> · vista previa pública, developers.googleblog.com",
        "Moonshot AI (2026), <i>Kimi Code CLI</i> · licencia MIT, github.com/MoonshotAI/kimi-code",
    )
)


EVOLUCION = envolver(
    cabecera("01 · Herramientas de trabajo", "Duración de la tarea que un modelo resuelve la mitad de las veces, 2019-2026", "i-flow")
    + "\n"
    + figura(
        "s1-evolucion-ia",
        "Horizonte temporal de tarea al 50 % de acierto en modelos de lenguaje, 2019-2026",
        "<b>De dos segundos en 2019 a más de dieciséis horas en 2026: cinco órdenes de "
        "magnitud en siete años.</b>",
    )
    + "\n"
    + dato_clave(
        "El horizonte temporal mide cuánto tarda una persona en la tarea más larga que el "
        "modelo resuelve la mitad de las veces. METR lo estimó sobre 170 tareas de "
        "programación: una duplicación cada 207 días."
    )
    + "\n"
    + criterio(
        "Un horizonte de una hora explica qué se le encarga hoy a un agente: redactar un "
        "apartado con las fuentes en el contexto. Una propuesta de veinte páginas dura "
        "semanas y queda cuatro órdenes de magnitud por encima."
    )
    + "\n"
    + fuente_pie(
        "METR (2025), <i>Measuring AI Ability to Complete Long Software Tasks</i>, "
        "arXiv:2503.14499 · acceso abierto",
    )
)


LIMITES_IA_LAMINA = envolver(
    cabecera("01 · Herramientas de trabajo", "Cuatro límites persistentes de los modelos de lenguaje, comprobados en 2026", "i-alert")
    + "\n"
    + figura(
        "s1-limites-ia",
        "Límites persistentes de los modelos de lenguaje en trabajo académico",
        "<b>Los cuatro se resuelven aportando contexto, no cambiando de modelo.</b>",
    )
    + "\n"
    + evitar(
        "Pedir referencias sin dar acceso a una fuente, y usar un detector de texto como "
        "prueba. Los detectores <b>estiman</b>: sus falsos positivos son altos y ninguna "
        "institución seria los admite como evidencia."
    )
    + "\n"
    + fuente_pie("Elaboración propia · comportamiento verificado en julio de 2026")
)


TRL_COMERCIAL = envolver(
    cabecera("01 · Medir la madurez", "Los tres tramos de madurez comercial frente a los tres tramos de TRL", "i-scale")
    + "\n"
    + duo(
        fig_desnuda("s1-madurez-doble",
                    "Correspondencia entre los tramos de madurez técnica y de madurez comercial",
                    "<b>Un proyecto puede estar en TRL 7 y en CRL 2: listo técnicamente y crudo comercialmente.</b>"),
        criterio(
            "El nivel de madurez comercial <i>(commercial readiness level)</i> mide otra "
            "cosa: si hay usuario identificado, si la propuesta de valor se contrastó y "
            "si hay ventas repetidas. Se declara aparte del TRL."
        )
        + "\n"
        + en_la_practica(
            "Un sensor validado en campo con veinte instalaciones alcanza TRL 7. Si "
            "ninguna de esas veinte pagó por él, la madurez comercial sigue en CRL 2, y "
            "un fondo de escalamiento lo devolverá pidiendo evidencia de demanda."
        ),
        invertir=True,
    )
    + "\n"
    + fuente_pie(F_FRASCATI, F_HELIYON)
)


# ==========================================================================
# MONTAJE
# ==========================================================================

def L(slug, titulo, nav, icono, contenido, clases="slide", scripts=""):
    return {"slug": slug, "titulo": f"{SESION} · {titulo}", "nav": nav,
            "icono": icono, "clases": clases, "contenido": contenido,
            "scripts": scripts}


LAMINAS = [
    # ── APERTURA ──
    L("portada", "Portada", "Portada", "i-network", PORTADA, "slide slide--start"),
    L("agenda", "Contenidos de los dos temas y las cuatro paradas de herramientas", "Agenda", "i-target", AGENDA),

    # ── 01 · PUNTO DE PARTIDA ──
    L("embudo", "Etapas entre la idea de proyecto y su uso por terceros", "El embudo", "i-flow", EMBUDO),
    L("situacion-de-partida", "Gasto en I+D como porcentaje del PBI: Perú y países seleccionados, 2018", "Gasto en I+D", "i-chart", PARTIDA),
    L("brecha-regional", "Perú frente a Chile en cuatro indicadores de innovación, 2010-2025", "Brecha regional", "i-scale", BRECHA),

    # ── 01 · QUÉ CUENTA COMO I+D ──
    L("criterios-de-id", "Definición de I+D y los cinco criterios de Frascati 2015", "Criterios", "i-search", CRITERIOS_ID),
    L("frascati-clasificador", "Efecto de cada criterio de Frascati en el veredicto de una actividad", "Clasificador", "i-rubric", FRASCATI_SIM, "slide", FRASCATI_JS),
    L("tipos-de-investigacion", "Investigación básica, aplicada y desarrollo experimental: evidencia y financiador", "Tipos", "i-layers", TIPOS_INVESTIGACION),
    L("matriz-proyecto", "Incertidumbre y aplicación prevista: los cuatro cuadrantes de una actividad", "Matriz", "i-scale", MATRIZ),
    L("innovacion", "Definición de innovación de Oslo 2018 y sus dos condiciones", "Umbral", "i-bulb", INNOVACION),
    L("tipos-de-innovacion", "Cinco tipos de innovación según el grado de cambio y el riesgo", "Tipos de innovación", "i-bulb", TIPOS_INNOVACION),
    L("innovacion-evidencia", "Cuatro tipos de innovación con su evidencia y su fondo aplicable", "Evidencia exigida", "i-sliders", INNOV_SIM, "slide", INNOV_JS),

    # ── 01 · MEDIR LA MADUREZ ──
    L("trl-escala", "Escala TRL: tramos de laboratorio, entorno relevante y entorno real", "Qué acredita el tramo", "i-ladder", TRL_TABLA),
    L("trl-figura", "Los nueve niveles de madurez tecnológica y los cortes 3-4 y 6-7", "Los dos cortes", "i-ladder", TRL_FIGURA),
    L("trl-instrumentos", "Instrumentos admisibles por nivel de la escala TRL", "TRL · simulación", "i-sliders", TRL_SIM, "slide", TRL_SIM_JS),
    L("trl-comercial", "Los tres tramos de madurez comercial frente a los tres tramos de TRL", "Madurez comercial", "i-scale", TRL_COMERCIAL),
    L("trl-limites", "Los cuatro cuadrantes de madurez técnica y disposición a adoptar", "Límites", "i-alert", TRL_LIMITES),

    # ── 01 · LO QUE EL PAÍS PRODUCE ──
    L("produccion-cientifica", "Publicaciones en Scopus por cada 100 000 habitantes: Perú y América Latina, 2020", "Publicaciones", "i-chart", PRODUCCION),
    L("tematicas", "Las seis áreas temáticas con más documentos publicados por el Perú, 2019", "Temáticas", "i-layers", TEMATICAS),
    L("patentes", "Patentes registradas por millón de habitantes: Perú y diez países, 2010-2018", "Patentes", "i-patent", PATENTES),
    L("tasa-de-adjudicacion", "Solicitudes y aprobaciones del beneficio tributario de la Ley 30309, 2016-2022", "Adjudicación", "i-rubric", ADJUDICACION),
    L("aprendizaje-30309", "Tasa de aprobación de la Ley 30309 entre 2016 y 2022", "Aprendizaje", "i-milestone", APRENDIZAJE),
    L("herramientas-01", "Herramientas 01 · Buscadores académicos", "Herramientas 01", "i-sliders", HERRAMIENTAS_01),

    # ── TALLERES DEL TEMA 01 ──
    L("herramientas-ia", "Seis categorías de herramientas de IA y su acceso a los archivos, 2026", "Herramientas", "i-robot", HERRAMIENTAS),
    L("evolucion-ia", "Duración de la tarea que un modelo resuelve la mitad de las veces, 2019-2026", "Evolución", "i-flow", EVOLUCION),
    L("limites-ia", "Cuatro límites persistentes de los modelos de lenguaje, comprobados en 2026", "Límites", "i-alert", LIMITES_IA_LAMINA),
    L("herramientas-02", "Herramientas 02 · Asistentes de chat generalistas", "Herramientas 02", "i-sliders", HERRAMIENTAS_02),

    # ── 02 · QUIÉN DECIDE ──
    L("actores-del-sinacti", "Organismos del SINACTI y el instrumento de cada uno", "Actores", "i-building", ACTORES),
    L("hitos-normativos", "Seis hitos normativos del sistema peruano de CTI, 1968-2025", "Hitos", "i-calendar", HITOS),
    L("herramientas-03", "Herramientas 03 · Consulta de la norma vigente", "Herramientas 03", "i-sliders", HERRAMIENTAS_03),
    L("concentracion-gasto", "Distribución del presupuesto público de CTI entre 164 instrumentos, 2012-2018", "Concentración", "i-fund", CONCENTRACION),
    L("instrumentos-sector", "Instrumentos de financiamiento de CTI por sector del Estado, 2012-2018", "Por sector", "i-building", SECTORES),
    L("quien-postula", "Instrumentos admitidos por tipo de entidad postulante", "Quién postula", "i-users", QUIEN_SIM, "slide", QUIEN_SIM_JS),

    # ── 02 · CUÁNTO Y DÓNDE ──
    L("alianza-del-pacifico", "Gasto en I+D sobre el PBI en la Alianza del Pacífico, 2018", "Alianza", "i-chart", ALIANZA),
    L("gii-2025", "Puesto de nueve países de América Latina en el Global Innovation Index 2025", "GII 2025", "i-globe", GII),
    L("radar-pilares", "Puesto del Perú en los doce pilares del Índice de Competitividad Global, 2019", "Perfil por pilares", "i-target", RADAR),
    L("regiones", "Índice de Competitividad Regional: primeras y últimas regiones del país, 2023", "Regiones", "i-globe", REGIONES),
    L("meta-2030", "Gasto en I+D vigente, media regional y meta nacional para 2030", "Meta 2030", "i-target", META),
    L("cascada-meta", "Reparto hipotético del salto hasta la meta del 1 % del PBI en 2030", "Cómo se cierra", "i-fund", CASCADA),

    # ── 02 · CAPITAL Y CAPACIDADES ──
    L("renacyt", "Investigadores inscritos en el RENACYT por nivel y por sexo, 2023", "Capital humano", "i-users", RENACYT),
    L("universidades", "Puesto mundial y regional de seis universidades peruanas en SCImago, 2023", "Universidades", "i-building", UNIVERSIDADES),
    L("herramientas-04", "Herramientas 04 · Registros de capacidades del país", "Herramientas 04", "i-sliders", HERRAMIENTAS_04),
    L("obstaculos", "Los tres obstáculos a la innovación más declarados por empresas manufactureras", "Obstáculos", "i-alert", OBSTACULOS),

    # ── 02 · CÓMO FUNCIONA UN SISTEMA ──
    L("modelos-de-flujo", "Lugar de la investigación en los modelos lineal y de eslabón en cadena", "Modelos", "i-flow", MODELOS_FLUJO),
    L("evidencia-de-sistemas", "Triple, cuádruple y quíntuple hélice: los actores de cada modelo", "Evidencia", "i-network", EVIDENCIA),
    L("capacidad-de-innovacion", "Los tres determinantes de la capacidad de innovación de un sistema", "Capacidad", "i-ladder", CAPACIDAD),

    # ── TALLERES DEL TEMA 02 ──

    # ── CIERRE ──
    L("problemas-frecuentes", "Errores frecuentes en una postulación y su detección", "Problemas", "i-alert", PROBLEMAS),
    L("glosario", "Doce términos de los dos temas, con su equivalente en inglés", "Glosario", "i-book", GLOSARIO),
    L("referencias", "Fuentes de la sesión y vía de acceso", "Referencias", "i-quote", REFERENCIAS),
]



if __name__ == "__main__":
    generar_desde({"clase": "clase-01", "sesion": SESION,
                   "laminas": renumerar(LAMINAS)})
