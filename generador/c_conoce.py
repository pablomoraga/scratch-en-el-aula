# -*- coding: utf-8 -*-
from common import *

SEC = 'conoce'
def captura(fich, alt, pie, clase='captura'):
    return ('<figure class="%s"><img src="../img/capturas/%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>' % (clase, fich, alt, pie))
R1 = lambda scripts, costumes=('robit1', 'robit2'), back=('blanco',), **kw: Project(list(back), [Sprite('Robit', list(costumes), scripts, **kw)])

# --- entorno -----------------------------------------------------------------
diagram = '''<div class="entorno">
 <div class="z z-menu"><b>1</b> Menú: Archivo, Editar, Tutoriales, idioma 🌐</div>
 <div class="z z-tabs"><b>2</b> Pestañas: Código · Disfraces · Sonidos</div>
 <div class="z z-stagebar"><b>6</b> ⚑ bandera verde · ⏹ detener · tamaño del escenario</div>
 <div class="z z-cat"><b>3</b> Categorías</div>
 <div class="z z-pal"><b>4</b> Paleta de bloques</div>
 <div class="z z-code"><b>5</b> Área de programación<br><small>aquí se arrastran y encajan los bloques</small></div>
 <div class="z z-stage"><b>7</b> Escenario<br><small>480 × 360</small></div>
 <div class="z z-sprites"><b>8</b> Objetos y sus propiedades</div>
 <div class="z z-back"><b>9</b> Fondos</div>
 <div class="z z-ext"><b>10</b> Añadir extensión</div>
</div>'''
page(SEC, 'entorno', 'El entorno de Scratch 3.0', P(
    'Cuando pulsas <b>Crear</b> en la web o abres la aplicación, aparece el editor. Así se ve, con sus partes numeradas:') + captura('editor-partes.jpg', 'Editor de Scratch 3.0 con Robit y sus partes numeradas del 1 al 10', 'El editor de Scratch 3.0 con el programa del reto «Robit camina». Los números corresponden a la tabla de abajo.', 'captura ancha') +
    '<table class="tabla"><tbody>'
    '<tr><td><b>1 Menú</b></td><td>El <b>engranaje</b> cambia el idioma y los colores; <b>Archivo</b> sirve para crear, cargar y guardar proyectos, y <b>Editar</b> para recuperar lo borrado o activar el modo turbo. Según la versión, aparecen como palabras o como iconos.</td></tr>'
    '<tr><td><b>2 Pestañas</b></td><td><b>Código</b> (bloques), <b>Disfraces</b> (o <b>Fondos</b> si está elegido el escenario) y <b>Sonidos</b>.</td></tr>'
    '<tr><td><b>3 Categorías</b></td><td>Cada color es un grupo de bloques: Movimiento, Apariencia, Sonido, Eventos, Control, Sensores, Operadores, Variables y Mis bloques.</td></tr>'
    '<tr><td><b>4 Paleta</b></td><td>Los bloques de la categoría elegida. Se arrastran al área de programación.</td></tr>'
    '<tr><td><b>5 Área de programación</b></td><td>Aquí se construyen los programas. Cada objeto tiene su propia área. Para borrar un bloque, arrástralo de vuelta a la paleta.</td></tr>'
    '<tr><td><b>6 Controles</b></td><td>La <b>bandera verde</b> inicia el proyecto y el <b>octógono rojo</b> lo detiene todo. Otros botones cambian el tamaño del escenario o lo ponen en pantalla completa.</td></tr>'
    '<tr><td><b>7 Escenario</b></td><td>Donde ocurre todo lo que programas.</td></tr>'
    '<tr><td><b>8 Objetos</b></td><td>Los personajes del proyecto. Debajo del escenario se ven y se cambian su nombre, posición (x, y), si se muestran, tamaño y dirección.</td></tr>'
    '<tr><td><b>9 Fondos</b></td><td>El escenario también puede tener programas y varios fondos.</td></tr>'
    '<tr><td><b>10 Extensiones</b></td><td>Botón azul de abajo a la izquierda: añade bloques de Música, Lápiz, Sensor de vídeo, micro:bit, Makey Makey…</td></tr>'
    '</tbody></table>' +
    box('idea', 'Truco', P('Haz clic sobre cualquier bloque (en la paleta o en el área) y se ejecutará al momento. '
                           'Es la forma más rápida de saber qué hace.')))

# --- coordenadas -------------------------------------------------------------
esquinas = R1([[flag(), gotoxy(0, 0), say('Estoy en el centro (0, 0)', 2), glide(1, 200, 140), say('Arriba a la derecha', 1),
                glide(1, -200, 140), say('Arriba a la izquierda', 1), glide(1, -200, -140), say('Abajo a la izquierda', 1),
                glide(1, 200, -140), say('Abajo a la derecha', 1), glide(1, 0, 0)]], back=('cuadricula',), size=60)
direcciones = R1([[flag(), gotoxy(0, 0), point(90), say('90: derecha', 1), point(0), say('0: arriba', 1), point(-90),
                   say('-90: izquierda', 1), point(180), say('180: abajo', 1), point(90)]], back=('cuadricula',), size=60)
page(SEC, 'coordenadas', 'El escenario y las coordenadas', P(
    'El escenario mide <b>480 pasos de ancho y 360 de alto</b>. Para decir dónde está un objeto se usan dos números, '
    'las <b>coordenadas</b>:') + ul([
        '<b>x</b>: posición horizontal. Va de <b>−240</b> (borde izquierdo) a <b>240</b> (borde derecho).',
        '<b>y</b>: posición vertical. Va de <b>−180</b> (abajo) a <b>180</b> (arriba).',
        'El centro del escenario es <b>(0, 0)</b>.']) +
    P('La <b>dirección</b> indica hacia dónde mira un objeto: <b>90</b> derecha, <b>0</b> arriba, <b>−90</b> izquierda y <b>180</b> abajo.') +
    ex('ej-coordenadas', esquinas, 'Viaje por las esquinas', 'Robit recorre el escenario usando coordenadas. El fondo es una cuadrícula con los ejes dibujados.') +
    ex('ej-direcciones', direcciones, 'Las cuatro direcciones', 'Robit apunta en cada una de las direcciones principales.') +
    box('idea', 'Truco', P('Al mover un objeto con el ratón por el escenario, sus coordenadas x e y cambian en el panel de objetos. '
                           'Úsalo para saber qué números poner en los bloques.')))

# --- objetos, disfraces, sonidos ---------------------------------------------
anima = R1([[flag(), forever(nextc(), wait(0.3))]])
page(SEC, 'objetos-disfraces-sonidos', 'Objetos, disfraces y sonidos', P(
    'Un <b>objeto</b> (en inglés <i>sprite</i>) es cualquier personaje o cosa del proyecto. Cada objeto tiene sus propios '
    '<b>programas</b>, <b>disfraces</b> y <b>sonidos</b>.') +
    '<h3>Añadir objetos y fondos</h3>' + P('Con el botón del gato (objetos) o el de la imagen (fondos), abajo a la derecha, puedes:') + ul([
        '<b>Elegir</b> uno de la biblioteca de Scratch.', '<b>Pintar</b> uno nuevo con el editor.',
        '<b>Sorpresa</b>: uno al azar.', '<b>Subir</b> una imagen desde tu ordenador (PNG, JPG, SVG, GIF).']) +
    '<h3>Disfraces</h3>' + P('Son las distintas apariencias de un objeto. Cambiándolos rápido se consigue una <b>animación</b>, como en los dibujos animados. '
                             'El editor permite dibujar en modo <b>vectorial</b> (formas que se pueden estirar sin perder calidad) o de <b>mapa de bits</b> (píxeles).') +
    captura('editor-disfraces.jpg', 'Pestaña Disfraces del editor con una estrella de píxeles', 'La pestaña <b>Disfraces</b>: a la izquierda, la lista de disfraces; en el centro, el editor de dibujo con sus herramientas.', 'captura ancha') +
    ex('ej-animacion', anima, 'Animación con disfraces', 'Robit tiene dos disfraces. Al cambiar de uno a otro cada 0,3 segundos parece que se mueve.') +
    '<h3>Sonidos</h3>' + P('En la pestaña <b>Sonidos</b> puedes elegir sonidos de la biblioteca, <b>grabar</b> con el micrófono o subir archivos. '
                           'El editor permite recortar y aplicar efectos: más rápido, más lento, eco, robot, al revés…') +
    box('docente', 'Derechos de autor', P('Si el alumnado sube imágenes o sonidos de internet, es buen momento para hablar de licencias y de usar '
                                          'recursos propios o con licencia libre, citando siempre su autoría.')))

# --- tipos de bloques ---------------------------------------------------------
tipos = '<table class="tabla-bloques"><thead><tr><th>Forma</th><th>Ejemplo</th><th>Para qué sirve</th></tr></thead><tbody>'
for nombre, node, txt in [
    ('Sombrero', flag(), 'Inicia un programa cuando ocurre algo. Siempre va arriba del todo.'),
    ('Apilable', move(10), 'Una orden. Se encaja encima y debajo de otras.'),
    ('Reportero (ovalado)', xpos(), 'Guarda un valor (número o texto) que se coloca dentro de otros bloques.'),
    ('Booleano (hexagonal)', touching('_edge_'), 'Responde verdadero o falso. Va en los huecos con puntas, como los de <i>si… entonces</i>.'),
    ('En forma de C', rep(10, move(10)), 'Envuelve a otros bloques para repetirlos o ejecutarlos solo si se cumple algo.'),
    ('Tapa', stop('all'), 'Termina un programa: no se puede encajar nada debajo.')]:
    tipos += '<tr><td><b>%s</b></td><td><div class="sb-script sb-solo">%s</div></td><td>%s</td></tr>' % (nombre, r_block(node), txt)
tipos += '</tbody></table>'
page(SEC, 'tipos-de-bloques', 'Tipos de bloques', P(
    'La <b>forma</b> de un bloque te dice dónde encaja, y su <b>color</b> a qué categoría pertenece. Las formas impiden montar programas sin sentido.') + tipos +
    P('Los huecos blancos se pueden escribir: los <b>ovalados</b> admiten números y los <b>rectangulares</b>, texto. Los que tienen una flecha ▾ son <b>menús desplegables</b>.') +
    box('idea', 'Leer un programa', P('Un programa se lee <b>de arriba abajo</b>: primero el bloque sombrero (cuándo empieza) y luego cada bloque en orden.')))

# --- categorías ---------------------------------------------------------------
def cat_page(slug, title, intro, rows, examples, extra=''):
    cap = captura('cat-%s.png' % slug, 'Paleta de bloques de %s en el editor de Scratch' % title,
                  'Así aparece la categoría en el editor. Baja por la paleta para ver el resto de bloques.', 'captura paleta')
    body = '<div class="con-paleta">' + cap + '<div>' + P(intro) + blocks_table(rows) + '</div></div>' + extra + ''.join(ex(*x) for x in examples)
    page(SEC, slug, title, body, group='Las categorías')

cat_page('movimiento', 'Movimiento', 'Bloques <b>azules</b> para mover y girar objetos por el escenario.', [
    (move(10), 'Avanza en la dirección en la que mira el objeto.'),
    (turn(15), 'Gira a la derecha (↺ gira a la izquierda) los grados indicados.'),
    (goto('_random_'), 'Salta a una posición aleatoria, al puntero del ratón o a otro objeto.'),
    (gotoxy(0, 0), 'Salta a unas coordenadas concretas.'),
    (glide(1, 100, 50), 'Se desliza poco a poco hasta un punto, en el tiempo indicado.'),
    (point(90), 'Apunta en una dirección (90 derecha, 0 arriba…).'),
    (towards('_mouse_'), 'Mira hacia el ratón o hacia otro objeto.'),
    (chx(10), 'Suma a x: valores positivos a la derecha, negativos a la izquierda.'),
    (sety(0), 'Coloca el objeto a una altura concreta.'),
    (bounce(), 'Si toca el borde, da la vuelta.'),
    (rot('left-right'), 'Evita que el objeto se ponga boca abajo al girar.'),
    (xpos(), 'Reportero con la posición x actual.')],
    [('ej-mov-pasear', R1([[flag(), rot('left-right'), forever(move(5), bounce(), nextc(), wait(0.1))]]), 'Paseo de lado a lado',
      'Robit camina, rebota en los bordes y no se pone boca abajo.'),
     ('ej-mov-raton', R1([[flag(), forever(towards('_mouse_'), if_(gt(dist('_mouse_'), 10), move(4)))]], size=60), 'Sigue al ratón',
      'Robit mira y se acerca al ratón, y se para cuando está muy cerca.')])

cat_page('apariencia', 'Apariencia', 'Bloques <b>morados</b> para cambiar el aspecto de los objetos y los fondos, y para mostrar mensajes.', [
    (say('¡Hola!', 2), 'Muestra un bocadillo con texto durante un tiempo.'),
    (think('Mmm...', 2), 'Igual, pero con un bocadillo de pensamiento.'),
    (costume('robit2'), 'Cambia a un disfraz concreto.'),
    (nextc(), 'Pasa al siguiente disfraz.'),
    (backdrop('cielo'), 'Cambia el fondo del escenario.'),
    (size(10), 'Agranda (o encoge, con números negativos) el objeto.'),
    (setsize(100), 'Fija el tamaño en porcentaje (100 % es el original).'),
    (effect('COLOR', 25), 'Aplica un efecto: color, ojo de pez, remolino, pixelar, mosaico, brillo o desvanecer.'),
    (cleareff(), 'Quita todos los efectos.'),
    (show(), 'Hace visible el objeto (<i>esconder</i> lo oculta).'),
    (front(), 'Pone el objeto por delante de los demás.')],
    [('ej-apa-presentacion', R1([[flag(), setsize(100), say('¡Hola! Soy Robit', 2), think('¿Qué hago ahora?', 2),
                                  rep(5, size(10), wait(0.1)), say('¡Soy más grande!', 2), setsize(100)]]), 'Robit se presenta',
      'Habla, piensa y crece poco a poco.'),
     ('ej-apa-efectos', R1([[flag(), cleareff(), rep(20, effect('COLOR', 10), wait(0.05)), rep(10, effect('GHOST', 10), wait(0.05)),
                             cleareff()]]), 'Efectos especiales', 'Cambia de color y después se desvanece hasta casi desaparecer.')])

snd = lambda scripts: Project(['blanco'], [Sprite('Robit', ['robit1'], scripts, sounds=['pop', 'ding', 'boing'])])
cat_page('sonido', 'Sonido', 'Bloques <b>fucsia</b> para reproducir y modificar sonidos.', [
    (playw('ding'), 'Reproduce un sonido y espera a que acabe para seguir.'),
    (play('pop'), 'Empieza un sonido y sigue con el programa a la vez.'),
    (stopsounds(), 'Para todos los sonidos.'),
    (pitch(10), 'Cambia el tono (más agudo o más grave).'),
    (vol(-10), 'Sube o baja el volumen.'),
    (setvol(100), 'Fija el volumen en porcentaje.')],
    [('ej-son-diferencia', snd([[key('1'), playw('ding'), say('Fin', 1)], [key('2'), play('ding'), say('Fin', 1)]]),
      'Esperar o no esperar', 'Pulsa 1 y luego 2: con <i>tocar sonido… hasta que termine</i> el «Fin» sale al acabar el sonido; con <i>iniciar sonido</i> sale a la vez.'),
     ('ej-son-escala', snd([[flag(), clearsnd(), rep(8, playw('pop'), pitch(20)), clearsnd()]]), 'Cada vez más agudo',
      'Repite un sonido subiendo el tono en cada vuelta.')])

cat_page('eventos', 'Eventos', 'Bloques <b>amarillos</b>. Casi todos son sombreros: deciden <b>cuándo</b> empieza un programa.', [
    (flag(), 'Al pulsar la bandera verde.'),
    (key('space'), 'Al pulsar una tecla.'),
    (clicked(), 'Al hacer clic sobre el objeto.'),
    (onbackdrop('cielo'), 'Cuando el escenario cambia a un fondo concreto.'),
    (whengt('TIMER', 10), 'Cuando el cronómetro o el volumen del micrófono superan un valor.'),
    (recv('empezar'), 'Al recibir un mensaje.'),
    (send('empezar'), 'Envía un mensaje a todos los objetos y sigue.'),
    (sendw('empezar'), 'Envía un mensaje y espera a que terminen los programas que lo reciben.')],
    [('ej-eve-teclas', R1([[key('right arrow'), point(90), move(10)], [key('left arrow'), point(-90), move(10)],
                           [clicked(), say('¡Me has hecho clic!', 1)]], rotation='left-right'), 'Teclas y clics',
      'Tres programas, tres eventos distintos.'),
     ('ej-eve-mensajes', Project(['blanco'], [
         Sprite('Robit', ['robit1'], [[flag(), say('Voy a avisar a la estrella', 2), send('brilla')]], x=-120),
         Sprite('Estrella', ['estrella'], [[recv('brilla'), rep(10, turn(36), size(5)), setsize(100)]], x=120)]),
      'Mensajes entre objetos', 'Robit envía el mensaje «brilla» y la estrella reacciona al recibirlo.')])

cat_page('control', 'Control', 'Bloques <b>naranjas</b> para repetir, esperar, decidir y crear clones.', [
    (wait(1), 'Hace una pausa.'),
    (rep(10), 'Repite lo de dentro un número de veces.'),
    (forever(), 'Repite lo de dentro sin parar.'),
    (if_(None), 'Hace lo de dentro solo si se cumple la condición.'),
    (ifelse(None, [], []), 'Si se cumple hace la primera parte; si no, la segunda.'),
    (until(None), 'Espera hasta que se cumpla la condición.'),
    (rep_until(None), 'Repite hasta que se cumpla la condición.'),
    (stop('all'), 'Detiene todo, este programa o los demás programas del objeto.'),
    (as_clone(), 'Programa que ejecutan los clones al nacer.'),
    (clone('_myself_'), 'Crea una copia (clon) de un objeto.'),
    (delclone(), 'Elimina el clon.')],
    [('ej-con-semaforo', Project(['blanco'], [Sprite('Boton', ['boton', 'boton_rojo'], [[flag(), forever(
        ifelse(touching('_mouse_'), [costume('boton_rojo')], [costume('boton')]))]])]), 'Condicional: semáforo',
      'El botón se pone rojo cuando el ratón está encima.'),
     ('ej-con-clones', Project(['espacio'], [Sprite('Estrella', ['estrella'], [[flag(), hide(), rep(15, clone(), wait(0.3))],
                                                                          [as_clone(), goto('_random_'), setsize(rnd(20, 80)), show(), wait(2), delclone()]])]),
      'Lluvia de clones', 'Se crean 15 estrellas en lugares al azar y cada una desaparece a los 2 segundos.')],
    box('ojo', 'Clones', P('Los clones aparecen ocultos si el original lo está, por eso se usa <i>mostrar</i> en el programa del clon. '
                           'Scratch permite un máximo de unos 300 clones a la vez.')))

cat_page('sensores', 'Sensores', 'Bloques <b>celestes</b> para detectar lo que pasa: toques, teclas, ratón, tiempo o preguntas.', [
    (touching('_edge_'), '¿Toca el borde, el ratón u otro objeto?'),
    (tcolor('#2e3a87'), '¿Toca un color concreto? Haz clic en el cuadrado y usa el cuentagotas.'),
    (dist('_mouse_'), 'Distancia hasta el ratón u otro objeto.'),
    (ask('¿Cómo te llamas?'), 'Hace una pregunta y espera a que se escriba la respuesta.'),
    (answer(), 'Guarda lo último que se ha contestado.'),
    (keyp('space'), '¿Está pulsada esa tecla ahora mismo?'),
    (mousedown(), '¿Está pulsado el botón del ratón?'),
    (mx(), 'Posición x del ratón.'),
    (timer(), 'Segundos desde que empezó (o se reinició) el cronómetro.'),
    (rtimer(), 'Pone el cronómetro a cero.')],
    [('ej-sen-pregunta', R1([[flag(), ask('¿Cómo te llamas?'), say(join('¡Encantado, ', join(answer(), '!')), 3)]]),
      'Preguntar y responder', 'Robit pregunta tu nombre y te saluda usando <i>respuesta</i>.'),
     ('ej-sen-teclas', R1([[flag(), forever(if_(keyp('right arrow'), chx(5)), if_(keyp('left arrow'), chx(-5)))]], size=60),
      'Movimiento suave', 'Con <i>¿tecla presionada?</i> dentro de un <i>por siempre</i>, el movimiento es mucho más fluido que con los eventos de tecla.')])

cat_page('operadores', 'Operadores', 'Bloques <b>verdes</b> para hacer cálculos, comparar y trabajar con textos.', [
    (add('', ''), 'Suma (también hay resta, multiplicación y división).'),
    (rnd(1, 10), 'Un número al azar entre dos valores.'),
    (gt('', 50), 'Mayor que (también menor que e igual a).'),
    (and_(None, None), 'Verdadero si se cumplen las dos condiciones.'),
    (or_(None, None), 'Verdadero si se cumple al menos una.'),
    (not_(None), 'Cambia verdadero por falso y al revés.'),
    (join('manzana ', 'plátano'), 'Junta dos textos.'),
    (letter(1, 'manzana'), 'Una letra de un texto.'),
    (length('manzana'), 'Cuántas letras tiene un texto.'),
    (round_(''), 'Redondea un número.')],
    [('ej-ope-dado', R1([[clicked(), say(join('Ha salido un ', rnd(1, 6)), 2)]]), 'Dado al azar',
      'Haz clic en Robit y te dirá un número del 1 al 6.'),
     ('ej-ope-calculo', R1([[flag(), ask('Dime un número'), setv('n', answer()), say(join('El doble es ', mul(v('n'), 2)), 3),
                             ifelse(gt(v('n'), 100), [say('¡Es mayor que 100!', 2)], [say('No llega a 100', 2)])]]),
      'Doble y comparación', 'Calcula el doble del número que escribas y lo compara con 100.')])

cat_page('variables', 'Variables y listas', 'Bloques <b>naranja oscuro</b>. Una <b>variable</b> es una caja con nombre que guarda un dato (puntos, vidas, tiempo…). '
         'Una <b>lista</b> guarda muchos datos en orden.', [
    (setv('puntos', 0), 'Pone un valor en la variable.'),
    (chv('puntos', 1), 'Suma (o resta, con negativo) a la variable.'),
    (v('puntos'), 'Reportero con el valor de la variable.'),
    (showv('puntos'), 'Muestra (o esconde) el marcador en el escenario.'),
    (ladd('cosa', 'compra'), 'Añade un elemento al final de la lista.'),
    (litem(1, 'compra'), 'Un elemento de la lista según su posición.'),
    (llen('compra'), 'Número de elementos de la lista.'),
    (lclear('compra'), 'Vacía la lista.')],
    [('ej-var-puntos', Project(['blanco'], [Sprite('Estrella', ['estrella'], [[flag(), setv('puntos', 0)],
                                                                         [clicked(), chv('puntos', 1), play('pop'), goto('_random_')]], sounds=['pop'])],
                               variables=['puntos'], shown=['puntos']), 'Marcador de puntos',
      'Cada clic en la estrella suma un punto y la estrella salta a otro sitio.'),
     ('ej-var-lista', Project(['blanco'], [Sprite('Robit', ['robit1'], [[flag(), lclear('compra'), ladd('pan', 'compra'), ladd('leche', 'compra'),
                                                                      ladd('fruta', 'compra'), say(join('Tengo apuntadas ', join(llen('compra'), ' cosas')), 2),
                                                                      say(join('La primera es: ', litem(1, 'compra')), 2)]])], lists=['compra']),
      'Lista de la compra', 'Robit apunta tres cosas en una lista y luego las consulta.')],
    box('idea', 'Para todos o solo para este objeto', P('Al crear una variable, Scratch pregunta si es <b>para todos los objetos</b> o '
                                                       '<b>solo para este objeto</b>. Las de «todos» las pueden leer y cambiar todos los objetos.')))

cat_page('mis-bloques', 'Mis bloques', 'Bloques <b>rosas</b>. Te permiten <b>inventar tus propios bloques</b>: das nombre a un grupo de instrucciones y '
         'luego lo usas como un solo bloque. Así los programas son más cortos y fáciles de leer.', [
    (define('saltar'), 'Define qué hace tu bloque nuevo.'),
    (call('saltar'), 'Usa tu bloque.')],
    [('ej-mis-saltar', Project(['cielo'], [Sprite('Robit', ['robit1'], [
        [define('saltar'), rep(10, chy(10)), rep(10, chy(-10))],
        [flag(), gotoxy(0, -100), say('Mira cómo salto', 1), call('saltar'), call('saltar'), say('¡Dos saltos!', 2)],
        [key('space'), call('saltar')]])]), 'El bloque «saltar»',
      'Creamos el bloque <i>saltar</i> una vez y lo usamos tres veces.')],
    box('idea', 'Cómo se crea', P('Categoría <b>Mis bloques › Crear un bloque</b>. Se pueden añadir entradas (números, textos o condiciones). '
                                  'Si marcas <i>Ejecutar sin actualizar la pantalla</i>, el bloque se ejecuta muy rápido, útil para dibujos con el lápiz.')))

# --- extensiones ------------------------------------------------------------------
ext_rows = '<table class="tabla"><thead><tr><th>Extensión</th><th>Para qué</th><th>Qué necesitas</th></tr></thead><tbody>' + ''.join(
    '<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % r for r in [
        ('Música', 'Tocar instrumentos, tambores y notas.', 'Nada.'),
        ('Lápiz', 'Dibujar con los objetos y sellar copias.', 'Nada.'),
        ('Sensor de vídeo', 'Detectar movimiento con la cámara (realidad aumentada).', 'Cámara web y dar permiso al navegador.'),
        ('Sensor de vídeo (caras)', 'Detectar caras y partes de la cara con la cámara.', 'Cámara web y dar permiso al navegador.'),
        ('Texto a voz', 'Que los objetos hablen en voz alta.', 'Conexión a internet.'),
        ('Traducir', 'Traducir textos a muchos idiomas.', 'Conexión a internet.'),
        ('Makey Makey', 'Usar objetos conductores (fruta, plastilina, papel de aluminio) como teclas.', 'Placa Makey Makey.'),
        ('micro:bit', 'Usar los botones, sensores y LED de la placa.', 'micro:bit, Bluetooth y Scratch Link.'),
        ('LEGO® (EV3, BOOST, WeDo 2.0)', 'Controlar motores y sensores de estos kits.', 'El kit, Bluetooth y Scratch Link.'),
        ('Go Direct Fuerza y Aceleración', 'Medir fuerza y aceleración.', 'Sensor de Vernier y Scratch Link.')]) + '</tbody></table>'
ext_body = P('Las extensiones añaden nuevas categorías de bloques. Se añaden con el botón azul de la esquina inferior izquierda. '
             'Al cargar un .sb3 que las usa, Scratch las añade solo.') + \
    captura('editor-extensiones.jpg', 'Ventana Elige una extensión del editor de Scratch', 'La ventana <b>Elige una extensión</b>. Baja para ver micro:bit, Makey Makey, LEGO y el resto.', 'captura ancha') + ext_rows
ext_body += ex('ej-ext-lapiz', Project(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), gotoxy(-50, -50), point(90),
                                                                             pcolor('#e85d2a'), psize(4), pdown(), rep(4, move(100), turn(90)), pup()]])]),
               'Lápiz: un cuadrado', 'El objeto deja rastro al moverse y dibuja un cuadrado.')
ext_body += ex('ej-ext-musica', Project(['blanco'], [Sprite('Tambor', ['tambor'], [[clicked(), rep(2, drum(2, 0.5), drum(1, 0.5)), drum(4, 1)]])]),
               'Música: un ritmo', 'Haz clic en el tambor para oír un ritmo con bombo, caja y platillo.')
ext_body += ex('ej-ext-voz', R1([[clicked(), lang('es'), speak('Hola, me llamo Robit'), speak(join('En inglés se dice: ', translate('hola', 'en')))]]),
               'Texto a voz y traducir', 'Robit habla en voz alta y traduce una palabra.')
ext_body += box('ojo', 'Scratch Link', P('micro:bit, LEGO y los sensores Vernier necesitan el programa gratuito <b>Scratch Link</b> instalado en el ordenador '
                                         '(Windows o macOS) y Bluetooth. Para la micro:bit hay que cargarle además un programa especial que se descarga desde la '
                                         'propia página de la extensión. Encontrarás los detalles en el apartado <b>Modo experto › micro:bit</b>.'))
page(SEC, 'extensiones', 'Las extensiones', ext_body)

# --- depurar y compartir ---------------------------------------------------------
page(SEC, 'depurar-compartir', 'Depurar, guardar y compartir', '<h3>Cuando algo no funciona</h3>' + ul([
    '¿Empieza el programa? Comprueba que tiene un <b>bloque sombrero</b> y que está en el <b>objeto correcto</b>.',
    '¿Los bloques están <b>encajados</b>? Un bloque suelto no se ejecuta.',
    '¿Va demasiado rápido para verlo? Añade un <i>esperar</i> para ir paso a paso.',
    '¿No sabes qué vale una variable? Marca su casilla para ver el marcador en el escenario.',
    '¿El objeto «desaparece»? Puede estar escondido, ser muy pequeño, estar fuera del escenario o tener el efecto desvanecer al 100.',
    'Al empezar, <b>coloca todo en su sitio</b>: posición, tamaño, disfraz, variables. Si no, el proyecto empieza como acabó la última vez.']) +
    '<h3>Guardar</h3>' + ul(['Con cuenta en línea: se guarda solo en la nube (<b>Archivo › Guardar ahora</b>).',
                             'Sin cuenta o en la aplicación: <b>Archivo › Guardar en tu ordenador</b> (crea un archivo .sb3).']) +
    '<h3>Compartir y remezclar</h3>' + P('Con cuenta, el botón <b>Compartir</b> publica el proyecto en la comunidad. Cualquiera puede verlo por dentro y '
                                       '<b>reinventarlo</b> (remezclarlo); Scratch guarda siempre el crédito del proyecto original. '
                                       'Todo lo compartido en Scratch tiene licencia Creative Commons BY-SA.') +
    box('docente', 'Buenas prácticas', ul(['Añadir instrucciones y créditos en la página del proyecto.',
                                           'Comentar con respeto y de forma constructiva.', 'No compartir datos personales.'])))
