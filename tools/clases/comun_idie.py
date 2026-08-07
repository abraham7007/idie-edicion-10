#!/usr/bin/env python3
"""Bloques propios de este curso, añadidos a los de `clases/comun.py`.

Existen porque METODOLOGIA.md §2 cambia la regla de origen: aquí las
fuentes NO ocupan lámina propia, se integran en el contenido. Eso obliga a
tener un pie de fuente reutilizable, y a que ninguna lámina con cifras pueda
escribirse sin él.
"""

from clases.comun import envolver, ico


def fuente_pie(*citas):
    """Pie de fuente de una lámina. Obligatorio en toda lámina con cifras.

    El formato es fijo —autor (año), publicación · licencia— para que el
    estudiante lo pueda copiar tal cual. Cuando la copia abierta vive en un
    repositorio y no en el editor, la cita debe apuntar al repositorio: un
    enlace que lleva a un muro de pago se da por inaccesible y no se vuelve
    a intentar (METODOLOGIA.md §2).
    """
    filas = "\n".join(f"\t\t\t\t\t\t<li>{c}</li>" for c in citas)
    return f"""\t\t\t\t<div class="srcnote">
\t\t\t\t\t<div class="srcnote__label">{ico("i-book")}Fuentes</div>
\t\t\t\t\t<ul>
{filas}
\t\t\t\t\t</ul>
\t\t\t\t</div>"""


def figura(nombre, titulo, pie, ancho=""):
    """Figura generada por programa, insertada en línea.

    Lleva SIEMPRE dos cosas debajo, y en este orden:

      Figura N · <título>      qué representa el dibujo, en frase nominal
      <pie>                    la conclusión que hay que sacar de él

    Separarlos importa: el título permite citar la figura desde el texto y
    desde el pie de fuente; el pie enuncia el hallazgo. Mezclarlos deja la
    figura sin nombre y obliga a describirla cada vez que se menciona.
    """
    _NUM["fig"] += 1
    cl = f" figure--{ancho}" if ancho else ""
    return f"""\t\t\t\t<figure class="figure{cl}" data-animate="fade-up">
\t\t\t\t\t<div class="figure__frame" data-figure="{nombre}"></div>
\t\t\t\t\t<figcaption class="figure__caption">
\t\t\t\t\t\t<span class="figure__num">Figura {_NUM["fig"]}</span>
\t\t\t\t\t\t<span class="figure__name">{titulo}</span>
\t\t\t\t\t\t<span class="figure__say">{pie}</span>
\t\t\t\t\t</figcaption>
\t\t\t\t</figure>"""


def dato(valor, texto, variante=""):
    """Cifra destacada. Lleva SIEMPRE unidad y año dentro del texto."""
    v = f" bigfig--{variante}" if variante else ""
    return f"""\t\t\t\t<div class="bigfig{v}" data-animate="fade-up">
\t\t\t\t\t<span class="bigfig__value">{valor}</span>
\t\t\t\t\t<span class="bigfig__what">{texto}</span>
\t\t\t\t</div>"""


def tabla(cabeceras, filas, titulo="", clases=""):
    """Tabla comparativa. Primera columna destacada (guía de estilo, §5).

    El título va ENCIMA, que es donde lo pone la norma editorial para tablas
    —al revés que en las figuras, cuyo pie va debajo—. Máximo 7 filas: con 9
    desborda y no hay recorte que lo arregle, porque la altura la fija la
    columna más alta.
    """
    if len(filas) > 7:
        raise ValueError(f"{len(filas)} filas: el máximo por lámina es 7")
    cap = ""
    if titulo:
        _NUM["tab"] += 1
        cap = (f'\t\t\t\t\t<p class="table__caption">'
               f'<span class="figure__num">Tabla {_NUM["tab"]}</span>'
               f'<span class="figure__name">{titulo}</span></p>\n')
    th = "".join(f"<th>{c}</th>" for c in cabeceras)
    tr = "\n".join(
        "\t\t\t\t\t\t\t<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>"
        for f in filas
    )
    return f"""\t\t\t\t<div class="table-scroll{' ' + clases if clases else ''}" data-animate="fade-up">
{cap}\t\t\t\t\t<table class="table--keyfirst">
\t\t\t\t\t\t<thead><tr>{th}</tr></thead>
\t\t\t\t\t\t<tbody>
{tr}
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>"""


def seccion(numero, rotulo, sumario):
    """Portadilla de tema. Frase nominal, sin verbos ni interrogaciones."""
    # Sin `--narrow`: esa variante acota el contenido a 56 rem y, como el marco
    # de la lámina se dibuja sobre el propio contenido, encogía la diapositiva
    # entera y la portadilla se veía casi cuadrada sobre una pantalla 16:9. El
    # marco se queda completo y lo que se acota es la medida del texto.
    return f"""\t\t\t<div class="slide__content slide__content--seccion stagger">
\t\t\t\t<div class="sectioncard" data-animate="fade-up">
\t\t\t\t\t<span class="sectioncard__n">{numero}</span>
\t\t\t\t\t<h1 class="sectioncard__title">{rotulo}</h1>
\t\t\t\t\t<p class="sectioncard__lede">{sumario}</p>
\t\t\t\t</div>
\t\t\t</div>"""


def definicion(termino, fuente, cuerpo, icono="i-book"):
    """Bloque de definición. Nombra SIEMPRE el término que define.

    Antes el rótulo decía solo «Definición · Frascati 2015» y había que leer
    el párrafo entero para saber qué se estaba definiendo.
    """
    return f"""\t\t\t\t<div class="def" data-animate="fade-up">
\t\t\t\t\t<div class="def__label">{ico(icono)}Definición
\t\t\t\t\t\t<span class="def__term">{termino}</span>
\t\t\t\t\t\t<span class="def__src">{fuente}</span>
\t\t\t\t\t</div>
\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t</div>"""


def ejemplo(cuerpo):
    return f"""\t\t\t\t<div class="example" data-animate="fade-up">
\t\t\t\t\t<div class="example__label">{ico("i-target")}En la práctica</div>
\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t</div>"""


def conclusion(rotulo, cuerpo, icono="i-milestone"):
    """Cierre de la lámina. El rótulo va arriba, con su icono, y el texto debajo.

    Estuvo dentro del párrafo, en negrita y seguido del texto. Con el icono o
    el rótulo en línea, la sangría del bloque desplaza todo el párrafo y la
    primera línea arranca donde termina el rótulo: se pierde ancho útil en
    cada línea y el bloque deja de reconocerse de un vistazo. Todos los
    bloques de recurso del mazo siguen ahora el mismo patrón.

    Consecuencia para quien escribe: `cuerpo` es una oración que se sostiene
    sola, con mayúscula inicial. Cuando el rótulo iba en línea los textos se
    redactaron como continuación suya —«Dónde deja esto a un equipo: en el
    lado de la oferta»— y al subir el rótulo diecinueve de veintidós cierres
    quedaron empezando en minúscula y en frase truncada.
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


def taller_idie(ref, titulo, campo, objetivo, caso, viene_de, alimenta, prompt):
    """Taller de formulación, versión de este curso (METODOLOGIA.md §5).

    Cuatro cosas y ninguna más: el título, el objetivo, el caso y el prompt.
    Llevó también criterios de evaluación, pasos numerados y pares de
    comparación; con los cuatro bloques la lámina se leía como un formulario
    y repetía en forma de lista lo que el prompt ya pide en forma de encargo.

    El prompt se escribe sobre este caso y con sus magnitudes dentro, no como
    plantilla con huecos por rellenar.
    """
    return envolver_taller(f"""				<div class="wk" data-animate="fade-up">
					<div class="wk__head">
						{ico("i-workshop")}
						<span class="wk__label">Taller de formulación</span>
						<span class="wk__chain">{viene_de} → <b>Taller {ref}</b> → {alimenta}</span>
						<span class="wk__ref">Taller {ref}</span>
					</div>

					<h2 class="wk__title">{titulo}</h2>

					<div class="wk__body">
						<div class="wk__col">
							<div class="wk__sec wk__sec--meta">
								<h3>{ico("i-target")}Objetivo</h3>
								<p>{objetivo}</p>
							</div>
							<div class="wk__caso">
								<h3>{ico("i-flow")}El caso · {campo}</h3>
								<p>{caso}</p>
							</div>
						</div>

						<div class="wk__col">
							<div class="wk__sec wk__sec--prompt">
								<h3>{ico("i-robot")}Prompt</h3>
								<div class="prompt-box">{prompt}</div>
							</div>
						</div>
					</div>
				</div>""")


def bloque_herramientas(ref, total, titulo, para_que, herramientas, como_elegir):
    """«Herramientas que deberías conocer»: la lámina que sustituye al taller.

    No hay encargo ni prompt. La lámina recomienda, para una función concreta
    del proyecto, las pocas herramientas que de verdad hay que conocer y dice
    en qué destaca cada una. El estudiante sale sabiendo con qué trabajar, no
    con un ejercicio resuelto.

    Tres reglas que sostienen el bloque:

    1. **Tres herramientas, nunca más.** El propósito no es inventariar el
       mercado sino dejar elegida la que se va a usar, y una lista de siete no
       se decide, se hojea.
    2. **Cada una con sus competencias**, no con un adjetivo. «Potente» no
       ayuda a elegir; «lee archivos del propio Drive sin subirlos», sí.
    3. **Ningún dato perecedero.** Ni precio, ni límite de contexto, ni
       política de retención: eso caduca en semanas y obligaría a rehacer el
       mazo cada edición. Va lo estructural, que es lo que dura, y el cierre
       dice con qué criterio elegir cuando estas tres cambien.

    `herramientas` es una lista de (nombre, quién la hace, [competencias]) y
    `como_elegir`, una lista de (criterio, qué mirar).
    """
    def _tarjeta(t):
        # La ficha admite (nombre, quién, competencias) y, cuando existe,
        # (nombre, quién, competencias, sitio). Nombrar una herramienta sin
        # decir dónde está obliga a buscarla, y en una lámina proyectada eso
        # equivale a no darla.
        nom, quien, comps = t[0], t[1], t[2]
        sitio = t[3] if len(t) > 3 else ""
        pie = (f'\n\t\t\t\t\t\t\t<a class="tools__sitio" '
               f'href="https://{sitio}">{sitio}</a>' if sitio else "")
        return ('\t\t\t\t\t\t<article class="tools__card">\n'
                f'\t\t\t\t\t\t\t<h3><b>{nom}</b><span>{quien}</span></h3>\n'
                '\t\t\t\t\t\t\t<ul>\n'
                + "\n".join(f'\t\t\t\t\t\t\t\t<li>{c}</li>' for c in comps) + "\n"
                '\t\t\t\t\t\t\t</ul>' + pie + '\n'
                '\t\t\t\t\t\t</article>')

    tarjetas = "\n".join(_tarjeta(t) for t in herramientas)

    criterios = "\n".join(
        f'\t\t\t\t\t\t\t<li><b>{c}</b>{e}</li>' for c, e in como_elegir)

    return envolver_taller(f"""\t\t\t\t<div class="wk wk--tools" data-animate="fade-up">
\t\t\t\t\t<div class="wk__head">
\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t<span class="wk__label">Herramientas que deberías conocer</span>
\t\t\t\t\t\t<span class="wk__ref">{ref} / {total}</span>
\t\t\t\t\t</div>

\t\t\t\t\t<h2 class="wk__title">{titulo}</h2>
\t\t\t\t\t<p class="tools__lede">{para_que}</p>

\t\t\t\t\t<div class="tools__grid">
{tarjetas}
\t\t\t\t\t</div>

\t\t\t\t\t<div class="tools__pick">
\t\t\t\t\t\t<h4>{ico("i-rubric")}Con qué criterio se elige, hoy y cuando estas tres cambien</h4>
\t\t\t\t\t\t<ul>
{criterios}
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>""")


def fichas(items, columnas=3):
    """Rejilla de fichas cortas, para inventariar sin gastar una tabla.

    El mazo tiene un tope de seis tablas por sesión (§4.4) y una tabla de seis
    filas por cuatro columnas es además la forma más lenta de leer un
    inventario desde el fondo del aula: obliga a recorrer la fila entera para
    saber de qué habla la primera celda. La ficha agrupa por entidad, que es
    la unidad con la que se decide.

    `items` es una lista de (nombre, quién lo opera, [líneas]).
    """
    def _ficha(t):
        nom, quien, ls = t[0], t[1], t[2]
        sitio = t[3] if len(t) > 3 else ""
        pie = (f'\n\t\t\t\t\t\t<a class="tools__sitio" '
               f'href="https://{sitio}">{sitio}</a>' if sitio else "")
        return ('\t\t\t\t\t<article class="tools__card">\n'
                f'\t\t\t\t\t\t<h3><b>{nom}</b><span>{quien}</span></h3>\n'
                '\t\t\t\t\t\t<ul>\n'
                + "\n".join(f'\t\t\t\t\t\t\t<li>{c}</li>' for c in ls) + "\n"
                '\t\t\t\t\t\t</ul>' + pie + '\n'
                '\t\t\t\t\t</article>')

    tarjetas = "\n".join(_ficha(t) for t in items)
    return (f'\t\t\t\t<div class="tools__grid tools__grid--suelta cols-{columnas}"'
            f' data-animate="fade-up">\n{tarjetas}\n\t\t\t\t</div>')


def ficha_fondo(operador, financia, quien, datos, sitio, nota=""):
    """Una lámina, un fondo. La unidad de la sesión 3 desde la décima edición.

    La sesión no explica qué dice la literatura sobre el financiamiento: dice
    a qué se puede postular. Por eso la unidad dejó de ser el hallazgo y pasó
    a ser el fondo, y la lámina responde siempre las mismas seis preguntas en
    el mismo sitio —quién lo opera, qué financia, a quién admite, cuánto da,
    en qué plazo y dónde está—, que es lo que permite comparar dos fondos sin
    volver a leerlos enteros.

    `datos` es una lista de (rótulo, valor) para el panel de la derecha: monto,
    plazo, contrapartida, periodicidad. El monto SIEMPRE lleva su fecha de
    consulta, porque cambia en cada edición y sin fecha caduca sin avisar.
    """
    campos = "\n".join(
        f'\t\t\t\t\t\t<div class="fondo__dato">\n'
        f'\t\t\t\t\t\t\t<dt>{r}</dt>\n\t\t\t\t\t\t\t<dd>{v}</dd>\n'
        f'\t\t\t\t\t\t</div>' for r, v in datos)
    puntos = "\n".join(f'\t\t\t\t\t\t\t<li>{x}</li>' for x in financia)
    pie = (f'\n\t\t\t\t\t<p class="fondo__nota">{ico("i-alert")}{nota}</p>'
           if nota else "")
    return f"""\t\t\t\t<div class="fondo" data-animate="fade-up">
\t\t\t\t\t<p class="fondo__operador">{ico("i-building")}{operador}</p>

\t\t\t\t\t<div class="fondo__cuerpo">
\t\t\t\t\t\t<div class="fondo__col">
\t\t\t\t\t\t\t<h3>{ico("i-fund")}Qué financia</h3>
\t\t\t\t\t\t\t<ul>
{puntos}
\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t<h3 class="fondo__quien">{ico("i-users")}Quién puede postular</h3>
\t\t\t\t\t\t\t<p>{quien}</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<dl class="fondo__panel">
{campos}
\t\t\t\t\t\t</dl>
\t\t\t\t\t</div>

\t\t\t\t\t<a class="fondo__sitio" href="https://{sitio}">{ico("i-link")}{sitio}</a>{pie}
\t\t\t\t</div>"""


def envolver_taller(interior):
    return f'\t\t\t<div class="slide__content slide__content--flush stagger">\n{interior}\n\t\t\t</div>'


def duo(figura_html, lado_html, invertir=False, ancha=False, tabla=False):
    """Lámina en dos columnas, con el lado de la figura alternando.

    `invertir` lo pasa el guion de la sesión a partir del índice de la
    lámina, no lo elige el autor: con la figura siempre del mismo lado el
    mazo se lee como una plantilla (METODOLOGIA.md §7).
    """
    flip = " duo--flip" if invertir else ""
    ancho = " duo--table" if tabla else (" duo--wide" if ancha else "")
    return f"""\t\t\t\t<div class="duo{flip}{ancho}" data-animate="fade-up">
\t\t\t\t\t<div class="duo__fig">
{figura_html}
\t\t\t\t\t</div>
\t\t\t\t\t<div class="duo__side">
{lado_html}
\t\t\t\t\t</div>
\t\t\t\t</div>"""


def fig_desnuda(nombre, titulo="", pie=""):
    """Figura sin marco de <figure>, para meterla dentro de una columna."""
    if not titulo:
        return f'\t\t\t\t\t\t<div class="figure__frame" data-figure="{nombre}"></div>'
    _NUM["fig"] += 1
    return (f'\t\t\t\t\t\t<div class="figure__frame" data-figure="{nombre}"></div>\n'
            f'\t\t\t\t\t\t<p class="figure__caption">'
            f'<span class="figure__num">Figura {_NUM["fig"]}</span>'
            f'<span class="figure__name">{titulo}</span>'
            f'<span class="figure__say">{pie}</span></p>')


def _recurso(clase, rotulo, icono, cuerpo):
    return f"""\t\t\t\t\t\t<div class="{clase}">
\t\t\t\t\t\t\t<div class="{clase}__label">{ico(icono)}{rotulo}</div>
\t\t\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t\t\t</div>"""


def dato_clave(cuerpo):
    """La cifra que hay que retener. Rótulo fijo y su icono."""
    return _recurso("keydata", "Dato importante", "i-chart", cuerpo)


def criterio(cuerpo):
    """La regla con la que se decide."""
    return _recurso("criterion", "Criterio", "i-rubric", cuerpo)


def evitar(cuerpo):
    """El error que descalifica."""
    return _recurso("avoid", "Evitar", "i-alert", cuerpo)


def en_la_practica(cuerpo):
    """El caso concreto, con nombres y magnitudes."""
    return f"""\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">{ico("i-target")}En la práctica</div>
\t\t\t\t\t\t\t<p>{cuerpo}</p>
\t\t\t\t\t\t</div>"""


# Contador de láminas visuales de la sesión. La alternancia del lado la lleva
# el generador y no el autor: con la figura siempre del mismo lado el mazo se
# lee como una plantilla (METODOLOGIA.md §7). Se reinicia al empezar cada
# sesión con `reiniciar_alternancia()`.
_ALTERNA = {"n": 0}

# Numeración correlativa de figuras y tablas dentro de la sesión. Es norma
# editorial: todo elemento visual se nombra y se numera para poder citarlo
# —«como muestra la figura 4»— sin ambigüedad (skill paper-visuals).
_NUM = {"fig": 0, "tab": 0}


def reiniciar_alternancia():
    _ALTERNA["n"] = 0
    _NUM["fig"] = 0
    _NUM["tab"] = 0


def visual(cabecera_html, visual_html, lado_html, pie_html="", pie_fig=""):
    """Lámina de figura o tabla, compuesta en dos columnas y alternando lado.

    `visual_html` es la figura o la tabla; `lado_html`, la lectura que la
    acompaña. El lado en el que cae la figura lo decide el orden de llamada,
    no quien escribe la lámina.
    """
    _ALTERNA["n"] += 1
    invertir = _ALTERNA["n"] % 2 == 0
    cap = f'\n\t\t\t\t\t\t<p class="figure__caption">{pie_fig}</p>' if pie_fig else ""
    bloque = duo(f"{visual_html}{cap}", lado_html, invertir=invertir)
    return envolver(cabecera_html + "\n" + bloque + ("\n" + pie_html if pie_html else ""))


def envolver_visual(interior, clases="slide__content stagger"):
    """Envoltorio que compone en dos columnas toda lámina con figura o tabla.

    Sustituye a `envolver` en los guiones de sesión. Detecta el bloque visual
    dentro del contenido y lo separa de la lectura que lo acompaña, dejando la
    cabecera arriba y el pie de fuente abajo:

        cabecera
        ┌──────────────┬──────────────┐
        │   figura     │   lectura    │   ← el lado alterna por lámina
        └──────────────┴──────────────┘
        pie de fuente

    Se hace aquí y no en cada lámina porque son casi treinta y el reparto no
    es una decisión de contenido: es composición, y la composición se decide
    una vez (METODOLOGIA.md §7).
    """
    import re as _re

    if 'class="duo' in interior:
        return envolver(interior, clases)

    m = (_re.search(r'\t*<figure class="figure[^"]*"[\s\S]*?</figure>', interior)
         or _re.search(r'\t*<div class="table-scroll[^"]*"[\s\S]*?\n\t*</div>', interior))
    if not m:
        return envolver(interior, clases)

    # Una tabla de cuatro o más columnas no cabe en media hoja: al estrecharla
    # las celdas se parten en tres líneas y la lámina desborda. Esas se quedan
    # a lo ancho, que es la excepción que la regla de dos columnas admite.
    if interior.count("<th>", m.start(), m.end()) >= 4:
        return envolver(interior, clases)

    visual_html = m.group(0)
    antes, despues = interior[:m.start()], interior[m.end():]

    # El pie de fuente se queda abajo, fuera de las dos columnas.
    pie = ""
    mp = _re.search(r'\t*<div class="srcnote">[\s\S]*?</div>\s*$', despues)
    if mp:
        pie = mp.group(0)
        despues = despues[:mp.start()]

    # La cabecera es lo que va antes del visual: insignia y titular.
    cabecera_html = antes.rstrip().rstrip("+ ").rstrip()
    lado = despues.strip("\n").strip()
    if not lado:
        return envolver(interior, clases)

    # El ancho de la figura lo decide cuánto texto la acompaña: con una
    # lectura corta no hay razón para reservarle un tercio de la hoja.
    texto = _re.sub(r"<[^>]+>", " ", lado)
    ancha = len(" ".join(texto.split())) < 260
    es_tabla = "table-scroll" in visual_html

    _ALTERNA["n"] += 1
    bloque = duo(visual_html, lado, invertir=_ALTERNA["n"] % 2 == 0,
                 ancha=ancha, tabla=es_tabla)
    partes = [p for p in (cabecera_html, bloque, pie.rstrip()) if p]
    return envolver("\n".join(partes), clases)


def renumerar(laminas):
    """Renumera figuras y tablas siguiendo el orden de las láminas.

    Los bloques se construyen en el orden del archivo, que no es el del mazo:
    una figura definida arriba puede acabar en la lámina cuarenta. Numerar al
    construir daba «Figura 3» en la lámina veinte. Aquí se reasigna al final,
    cuando el orden real ya está decidido.
    """
    import re as _re

    n = {"Figura": 0, "Tabla": 0}

    def _uno(m):
        clase = m.group(1)
        n[clase] += 1
        return f'{m.group(0)[:m.start(2) - m.start(0)]}{clase} {n[clase]}'

    for lam in laminas:
        lam["contenido"] = _re.sub(
            r'(?<=class="figure__num">)(Figura|Tabla) (\d+)',
            lambda m: f"{m.group(1)} {n.__setitem__(m.group(1), n[m.group(1)] + 1) or n[m.group(1)]}",
            lam["contenido"])
    return laminas
