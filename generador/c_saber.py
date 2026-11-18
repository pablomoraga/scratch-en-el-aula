# -*- coding: utf-8 -*-
from common import *
import common
from sb import template_of
from assets import Assets
_A = Assets()
def _ext(n): return _A.image(n)[1]

SEC = 'saber'

# ----------------------------------------------------------------- recursos de Comenzamos
retos = [p for p in PAGES if p['section'] == 'comenzamos' and p['kind'] == 'reto']
RES = dict(plantillas={}, sprites={}, fondos=[], sonidos=[])
for p in retos:
    proj = PROJECTS[p['slug']]
    RES['plantillas']['plantilla-' + p['slug']] = template_of(proj)
    for b in proj.backdrops:
        if b not in RES['fondos']: RES['fondos'].append(b)
    for s in proj.sprites:
        cos, snd = RES['sprites'].setdefault(s.name, ([], []))
        for c in s.costumes:
            if c not in cos: cos.append(c)
        for x in s.sounds:
            if x not in snd: snd.append(x)
            if x not in RES['sonidos']: RES['sonidos'].append(x)
common.RESOURCES = RES

def btn(href, label):
    return '<a class="btn-dl" href="{{RES}}%s" download>⬇ %s</a>' % (href, e(label))

filas = ''.join('<tr><td><b>%s</b> · %s</td><td>%s</td></tr>' % (p['meta']['num'], e(p['title']),
                btn('plantillas/plantilla-%s.sb3' % p['slug'], 'Plantilla')) for p in retos)
obj = ''.join('<div class="recurso"><img src="{{RES}}objetos/%s.%s" alt="%s" width="70" height="70"><b>%s</b>'
              '<small>%d disfraz%s%s</small>%s</div>' % (
                  cos[0], _ext(cos[0]), e(nombre), e(nombre), len(cos), '' if len(cos) == 1 else 'es',
                  (' · %d sonido%s' % (len(snd), '' if len(snd) == 1 else 's')) if snd else '',
                  btn('objetos/%s.sprite3' % slug_name, '.sprite3'))
              for nombre, (cos, snd) in RES['sprites'].items() for slug_name in [nombre.lower()])
fon = ''.join('<div class="recurso recurso-fondo"><img src="{{RES}}fondos/%s.%s" alt="%s" width="120" height="90"><b>%s</b>%s</div>'
              % (f, _ext(f), e(f), e(f), btn('fondos/%s.%s' % (f, _ext(f)), _ext(f).upper())) for f in RES['fondos'])
son = ''.join('<div class="recurso"><b>%s</b>%s</div>' % (e(s), btn('sonidos/%s.wav' % s, 'WAV')) for s in RES['sonidos'])

page(SEC, 'recursos-comenzamos', 'Recursos de Comenzamos', P(
    'Todo lo necesario para que cada alumno o alumna empiece los retos de <b>Comenzamos</b> con los mismos personajes, fondos y sonidos, '
    'pero sin la programación hecha. Todos los recursos son originales y puedes repartirlos libremente en clase.') +
    '<p>%s</p>' % btn('recursos-comenzamos.zip', 'Descargar todo (.zip)') +
    '<h3>Tarjetas imprimibles</h3>' +
    P('Cada reto en una tarjeta A5 con Robit: en la cara, el objetivo y los pasos; en el dorso, los bloques que ayudan, las pistas y las ideas para ampliar. '
      'Imprime en A4 a doble cara (giro por el borde largo) y corta por la línea discontinua: cada hoja da dos tarjetas.') +
    '<p>%s %s</p>' % (btn('tarjetas-comenzamos.pdf', 'Tarjetas de Comenzamos (PDF)'), btn('tarjetas-encuentra-el-error.pdf', 'Tarjetas de Encuentra el error (PDF)')) +
    '<h3>Plantillas de cada reto</h3>' +
    P('Cada plantilla es un proyecto .sb3 con los objetos y fondos ya colocados y <b>sin ningún bloque</b>. Se abre con <b>Archivo › Cargar desde tu ordenador</b>.') +
    '<table class="tabla"><thead><tr><th>Reto</th><th>Plantilla</th></tr></thead><tbody>%s</tbody></table>' % filas +
    '<h3>Objetos</h3>' + P('Archivos <b>.sprite3</b>: cada uno incluye todos los disfraces y sonidos del objeto. En Scratch: pasa el ratón por el botón del gato '
                           '(abajo a la derecha) y elige <b>Subir un objeto</b>.') + '<div class="recursos">%s</div>' % obj +
    '<h3>Fondos</h3>' + P('Imágenes <b>SVG</b> de 480 × 360. En Scratch: botón de fondos (abajo a la derecha) › <b>Subir un fondo</b>.') +
    '<div class="recursos">%s</div>' % fon +
    '<h3>Sonidos</h3>' + P('Archivos <b>WAV</b> muy cortos. En la pestaña Sonidos: <b>Subir sonido</b>.') + '<div class="recursos">%s</div>' % son +
    box('docente', 'Ideas de uso', ul(['Reparte la plantilla del reto y deja que el alumnado programe desde cero.',
                                       'Comparte el .zip en el aula virtual para que cada cual monte sus propios proyectos.',
                                       'Invita a modificar los dibujos en el editor de disfraces: así el proyecto pasa a ser suyo.'])))

# ----------------------------------------------------------------- llavero
page(SEC, 'llavero-robit', 'Robit en 3D: llavero imprimible', P(
    'Robit también existe fuera de la pantalla. Este llavero reproduce su pixel art en relieve y es un buen premio para quien termine los retos, '
    'o una actividad de diseño e impresión 3D para el club de robótica.') +
    '<p><img src="{{RES}}llavero/robit-llavero-vista.png" alt="Vista del llavero de Robit impreso en dos colores" width="320"></p>' +
    '<p>%s</p>' % btn('llavero/robit-llavero.stl', 'Descargar el llavero (.stl)') +
    '<table class="tabla"><tbody>'
    '<tr><td><b>Tamaño</b></td><td>32 × 53 × 4,2 mm (cada píxel mide 1,6 mm).</td></tr>'
    '<tr><td><b>Anilla</b></td><td>Agujero de 4,8 mm sobre la antena, para una anilla de llavero normal.</td></tr>'
    '<tr><td><b>Material</b></td><td>PLA. Capa de 0,2 mm, 3 perímetros y 20 % de relleno. No necesita soportes: la base es plana.</td></tr>'
    '<tr><td><b>Dos colores</b></td><td>El contorno, los ojos y la boca sobresalen 1,2 mm. Programa en el laminador un cambio de filamento '
    '(o una pausa) a <b>3,0 mm</b> de altura: base amarilla y relieve negro.</td></tr>'
    '</tbody></table>' +
    box('docente', 'Idea para el aula', P('Diseña tu propio personaje en pixel art en una cuadrícula de papel y conviértelo en llavero: '
                                          'cada cuadrado coloreado es un cubo. Es una forma muy visual de entender las coordenadas y la impresión 3D.')))

# ----------------------------------------------------------------- glosario
GLOS = [
    ('Algoritmo', 'Lista ordenada de pasos para resolver un problema.'),
    ('Bloque', 'Pieza de Scratch que representa una instrucción. Su forma indica dónde encaja.'),
    ('Bucle', 'Repetición de un grupo de instrucciones: <i>repetir</i>, <i>por siempre</i>, <i>repetir hasta que</i>.'),
    ('Clon', 'Copia de un objeto creada mientras el programa funciona.'),
    ('Condicional', 'Instrucción que solo se ejecuta si se cumple algo: <i>si… entonces</i>.'),
    ('Coordenadas', 'Par de números (x, y) que indica una posición en el escenario.'),
    ('Depurar', 'Buscar y corregir los errores de un programa.'),
    ('Disfraz', 'Cada una de las apariencias de un objeto.'),
    ('Evento', 'Algo que ocurre y pone en marcha un programa: un clic, una tecla, un mensaje…'),
    ('Extensión', 'Grupo de bloques extra que se añade a Scratch: Lápiz, Música, micro:bit…'),
    ('Lista', 'Variable que guarda varios datos en orden.'),
    ('Mensaje', 'Aviso que un objeto envía a todos los demás para coordinarse.'),
    ('Objeto', 'Personaje o elemento del proyecto, con sus propios programas, disfraces y sonidos.'),
    ('Operador', 'Bloque que calcula, compara o une datos.'),
    ('Paralelismo', 'Varios programas funcionando a la vez.'),
    ('Programa', 'Conjunto de bloques encajados que empieza con un bloque sombrero.'),
    ('Reportero', 'Bloque ovalado que devuelve un valor.'),
    ('Variable', 'Espacio con nombre donde se guarda un dato que puede cambiar.'),
]
page(SEC, 'glosario', 'Glosario', '<table class="tabla"><tbody>%s</tbody></table>' % ''.join(
    '<tr><td><b>%s</b></td><td>%s</td></tr>' % g for g in GLOS))

# ----------------------------------------------------------------- evaluación
page(SEC, 'evaluacion', 'Evaluación', P(
    'Una rúbrica sencilla para valorar cualquier proyecto de este material. Cada criterio puntúa de 1 a 4.') +
    '<table class="tabla"><thead><tr><th>Criterio</th><th>1 · Empezando</th><th>2 · En camino</th><th>3 · Conseguido</th><th>4 · Experto</th></tr></thead><tbody>'
    '<tr><td><b>Funciona</b></td><td>No llega a funcionar.</td><td>Funciona a medias.</td><td>Hace lo que pide el reto.</td><td>Funciona y añade mejoras propias.</td></tr>'
    '<tr><td><b>Conceptos</b></td><td>Solo secuencias.</td><td>Usa eventos y bucles.</td><td>Usa condicionales y variables.</td><td>Combina mensajes, clones, listas o «Mis bloques».</td></tr>'
    '<tr><td><b>Orden</b></td><td>Bloques sueltos y repetidos.</td><td>Programas separados pero desordenados.</td><td>Programas claros y con nombres adecuados.</td><td>Evita repeticiones con bucles o bloques propios.</td></tr>'
    '<tr><td><b>Depuración</b></td><td>Necesita la solución.</td><td>Corrige con las pistas.</td><td>Encuentra y corrige sus errores.</td><td>Explica sus errores y ayuda a otras personas.</td></tr>'
    '<tr><td><b>Creatividad</b></td><td>Copia el ejemplo.</td><td>Cambia algún detalle.</td><td>Personaliza objetos, fondos o sonidos.</td><td>Crea una versión propia con ideas nuevas.</td></tr>'
    '</tbody></table>' +
    '<h3>Autoevaluación rápida al terminar un reto</h3>' + ul(['¿Qué conceptos he usado?', '¿Qué error he tenido y cómo lo he arreglado?',
                                                               '¿Qué mejora añadiría si tuviera más tiempo?']))

# ----------------------------------------------------------------- enlaces
def link(url, title, desc):
    return '<li><a href="%s" target="_blank" rel="noopener">%s</a>: %s</li>' % (url, e(title), desc)
page(SEC, 'enlaces', 'Enlaces y bibliografía',
     '<h3>Oficiales de Scratch</h3><ul>' +
     link('https://scratch.mit.edu', 'Scratch', 'editor en línea y comunidad.') +
     link('https://scratch.mit.edu/download', 'Aplicación de Scratch', 'para programar sin conexión.') +
     link('https://scratch.mit.edu/ideas', 'Ideas de Scratch', 'tutoriales y tarjetas de actividades oficiales.') +
     link('https://scratch.mit.edu/starter-projects', 'Proyectos de inicio', 'proyectos para remezclar.') +
     link('https://scratch.mit.edu/educators', 'Scratch para educadores', 'cuentas de profesorado y recursos para el aula.') +
     link('https://scratch.mit.edu/microbit', 'Scratch y micro:bit', 'instalación de Scratch Link y del programa para la placa.') +
     link('https://www.scratchjr.org', 'ScratchJr', 'versión para 5-7 años.') + '</ul>' +
     '<h3>Scratch Foundation</h3><ul>' +
     link('https://www.scratchfoundation.org/learn/', 'Aprender con Scratch', 'portada de recursos de la Fundación Scratch.') +
     link('https://www.scratchfoundation.org/learn/learning-library', 'Learning Library', 'biblioteca de actividades, planes de lección, tarjetas de programación y vídeos (en inglés).') +
     link('https://www.scratchfoundation.org/learn/for-educators', 'Scratch for Educators', 'recursos, cuentas de profesorado y red de docentes.') +
     link('https://www.scratchfoundation.org/learn/for-families', 'Scratch for Families', 'información para familias.') +
     link('https://scratch.mit.edu/projects/editor/?tutorial=getStarted', 'Tutorial «Primeros pasos»', 'se abre dentro del propio editor de Scratch.') + '</ul>' +
     '<h3>Hardware</h3><ul>' +
     link('https://microbit.org/es-es/', 'micro:bit', 'web oficial de la placa.') +
     link('https://makeymakey.com', 'Makey Makey', 'web oficial de la placa.') + '</ul>' +
     '<h3>Lecturas recomendadas</h3><ul>' +
     link('https://eduteka.icesi.edu.co/pdfdir/hgse-scratch-computacion-creativa.pdf', 'Computación creativa',
          'guía curricular de la Universidad de Harvard, en español (Eduteka).') +
     link('https://leer.es/wp-content/uploads/2021/06/guia_didactica_actualizacion_scratch3_0.pdf', 'Guía didáctica de Scratch 3.0', 'Leer.es.') +
     link('https://academypop.com/wp-content/uploads/2019/01/Gu%C3%ADa-para-conocer-sobre-el-entorno-de-Scratch-3.pdf',
          'Guía para conocer el entorno de Scratch 3', 'AcademyPop.') +
     link('https://miguelmejiac.wordpress.com/wp-content/uploads/2013/07/cuadernillo-de-ejercicios-parte-1.pdf',
          'Cuadernillo de ejercicios (parte 1)', 'Miguel Mejía. Hecho con una versión anterior de Scratch.') + '</ul>')
