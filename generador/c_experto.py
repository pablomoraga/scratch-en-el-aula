# -*- coding: utf-8 -*-
from common import *

SEC = 'experto'
GROUPS = [
    ('juegos', 'Juegos clásicos', 'Cinco juegos de siempre para aprender a usar puntos, vidas, colisiones y clones.', None),
    ('historias', 'Historias y animación', 'Cuentos, diálogos y tarjetas interactivas: programar también es contar.', None),
    ('arte', 'Arte con lápiz', 'Geometría, patrones y color con la extensión Lápiz.', None),
    ('musica', 'Música', 'Instrumentos, ritmos y melodías con la extensión Música.', None),
    ('makey', 'Makey Makey', 'Convierte fruta, plastilina o papel de aluminio en teclas.',
     ['Una placa <b>Makey Makey</b> conectada por USB (no necesita instalar nada: el ordenador la ve como un teclado).',
      'Pinzas de cocodrilo y objetos que conduzcan la electricidad: fruta, plastilina, papel de aluminio, grafito de lápiz blando…',
      'Que la persona que juega toque el cable de <b>tierra</b> (EARTH): sin ese contacto no se cierra el circuito.',
      'En Scratch, la extensión <b>Makey Makey</b>. También funcionan los bloques normales de tecla, porque la placa «pulsa» espacio y flechas.']),
    ('microbit', 'micro:bit', 'La placa micro:bit como mando: botones, inclinación, gestos y su pantalla de LED.',
     ['Una placa <b>micro:bit</b> (V1 o V2) con pilas o cable USB.',
      'El programa gratuito <b>Scratch Link</b> instalado en el ordenador (Windows o macOS) y el <b>Bluetooth</b> activado.',
      'Cargar en la micro:bit, una sola vez, el archivo <b>HEX de Scratch</b> que se descarga desde la página de la extensión (scratch.mit.edu/microbit).',
      'En Scratch: añadir la extensión <b>micro:bit</b> y pulsar <i>Conectar</i>. La placa muestra en su pantalla un nombre de cinco letras para reconocerla.']),
    ('ra', 'Realidad aumentada', 'Tu cuerpo como mando: la cámara detecta el movimiento sobre los objetos.',
     ['Una <b>cámara web</b> y dar permiso al navegador para usarla.',
      'La extensión <b>Sensor de vídeo</b>.',
      'Buena luz y un fondo que no se mueva detrás de quien juega. Si detecta demasiado, sube el número de las condiciones de movimiento.']),
    ('ciencia', 'Ciencia y matemáticas', 'Simulaciones, cálculo mental y traducción: Scratch como herramienta para otras materias.', None),
]
GROUP_TITLE = {g[0]: g[1] for g in GROUPS}
n = [0]
def R(group, *a, **k):
    n[0] += 1
    reto(SEC, 'E%02d' % n[0], 'experto-%02d' % n[0], *a, group=GROUP_TITLE[group], **k)
def P1(back, sprites, **kw): return Project(list(back), sprites, **kw)

# ============================ Juegos clásicos
R('juegos', 'Atrapa manzanas', 2, '30 min', ['variables', 'condicionales', 'sensores'],
  'Mover una cesta con el ratón para atrapar las manzanas que caen. Cada fallo cuesta una vida.',
  ['La cesta sigue la posición x del ratón, siempre abajo.', 'La manzana empieza arriba en una x aleatoria y baja sin parar.',
   'Si toca la cesta: suma un punto y vuelve arriba.', 'Si llega al suelo: resta una vida y vuelve arriba.', 'Con 0 vidas, fin del juego.'],
  ['<i>dar a x el valor (posición x del ratón)</i> dentro de un <i>por siempre</i> mueve la cesta.',
   'La manzana ha llegado al suelo cuando su <i>posición en y</i> es menor que −170.'],
  P1(['cielo'], [Sprite('Cesta', ['cesta'], [[flag(), gotoxy(0, -150), forever(setx(mx()))]]),
                 Sprite('Manzana', ['manzana'], [[flag(), setv('puntos', 0), setv('vidas', 3), gotoxy(rnd(-220, 220), 180),
                                                  forever(chy(-5),
                                                          if_(touching('Cesta'), chv('puntos', 1), play('pop'), gotoxy(rnd(-220, 220), 180)),
                                                          if_(lt(ypos(), -170), chv('vidas', -1), play('error'), gotoxy(rnd(-220, 220), 180)),
                                                          if_(eq(v('vidas'), 0), say('¡Fin del juego!', 2), stop('all')))]],
                        sounds=['pop', 'error'])], variables=['puntos', 'vidas'], shown=['puntos', 'vidas']),
  ['Que la manzana caiga cada vez más rápido (usa una variable <i>velocidad</i>).', 'Añade una roca que reste vidas si la atrapas.'])

R('juegos', 'Tenis de una pala', 2, '30 min', ['condicionales', 'ángulos', 'variables'],
  'Mantener la pelota en el aire con una pala.',
  ['La pala sigue al ratón en horizontal, abajo del todo.', 'La pelota se mueve y rebota en los bordes.',
   'Si toca la pala, rebota hacia arriba y suma un punto.', 'Si se cuela por abajo, pierdes una vida y vuelve al centro.'],
  ['Para rebotar en una superficie horizontal, la nueva dirección es <b>180 − dirección</b>.',
   'Tras rebotar en la pala, mueve la pelota unos pasos para que no se quede «pegada».'],
  P1(['blanco'], [Sprite('Pala', ['pala'], [[flag(), gotoxy(0, -160), forever(setx(mx()))]]),
                  Sprite('Pelota', ['pelota'], [[flag(), setv('puntos', 0), setv('vidas', 3), gotoxy(0, 100), point(rnd(140, 220)),
                                                 forever(move(6), bounce(),
                                                         if_(touching('Pala'), point(sub(180, direction())), move(10), chv('puntos', 1), play('pop')),
                                                         if_(lt(ypos(), -170), chv('vidas', -1), play('error'), gotoxy(0, 100), point(rnd(140, 220)), wait(1)),
                                                         if_(eq(v('vidas'), 0), say('¡Fin!', 2), stop('all')))]], sounds=['pop', 'error'])],
     variables=['puntos', 'vidas'], shown=['puntos', 'vidas']),
  ['Cada 5 puntos, que la pelota vaya más rápida.', 'Haz una versión para dos jugadores con palas verticales.'])

R('juegos', 'Laberinto de colores', 2, '35 min', ['sensores', 'color', 'condicionales'],
  'Llevar a Robit hasta la bandera sin tocar las paredes.',
  ['Dibuja (o usa) un fondo de laberinto con paredes de un solo color.', 'Robit, pequeño, se mueve con las flechas.',
   'Si toca el color de la pared, vuelve a la salida.', 'Si toca la bandera, ¡has ganado!'],
  ['En <i>¿tocando el color …?</i>, haz clic en el cuadrado de color y usa el cuentagotas sobre la pared.',
   'Mueve de 3 en 3 pasos: si vas muy rápido podrías «atravesar» paredes finas.'],
  P1(['laberinto'], [Sprite('Robit', ['robit1'], [[flag(), gotoxy(-190, 140), forever(
      if_(keyp('right arrow'), chx(3)), if_(keyp('left arrow'), chx(-3)), if_(keyp('up arrow'), chy(3)), if_(keyp('down arrow'), chy(-3)),
      if_(tcolor('#2e3a87'), play('error'), gotoxy(-190, 140)),
      if_(touching('Meta'), play('victoria'), say('¡Lo conseguí!', 2), stop('all')))]], size=25, sounds=['error', 'victoria']),
      Sprite('Meta', ['meta'], [], x=190, y=-130)]),
  ['Añade un cronómetro para saber cuánto tardas.', 'Crea un segundo nivel con otro fondo.'])

R('juegos', 'Esquiva meteoritos', 3, '40 min', ['clones', 'cronómetro', 'mensajes'],
  'Una nave que esquiva una lluvia de meteoritos. ¿Cuánto aguantas?',
  ['La nave se mueve a izquierda y derecha con las flechas.', 'El meteorito original se esconde y crea un clon cada medio segundo.',
   'Cada clon aparece arriba en una x aleatoria y baja girando; al llegar abajo se elimina.',
   'Si un clon toca la nave, envía el mensaje «choque».', 'La nave, al recibirlo, guarda el tiempo, cambia al fondo de fin y detiene todo.'],
  ['Los clones heredan la posición del original: colócalos en el programa <i>al comenzar como clon</i>.',
   'Al detener todo se borran los bocadillos; por eso el resultado se muestra en una variable.'],
  P1(['espacio', 'fin'], [
      Sprite('Nave', ['nave'], [[flag(), backdrop('espacio'), gotoxy(0, -140), rtimer(), forever(
          if_(keyp('right arrow'), chx(7)), if_(keyp('left arrow'), chx(-7)))],
          [recv('choque'), setv('segundos', round_(timer())), play('error'), backdrop('fin'), wait(0.5), stop('all')]], sounds=['error']),
      Sprite('Roca', ['roca'], [[flag(), hide(), forever(clone(), wait(0.5))],
                                [as_clone(), gotoxy(rnd(-220, 220), 180), setsize(rnd(50, 110)), show(),
                                 rep_until(lt(ypos(), -170), chy(-6), turn(5), if_(touching('Nave'), send('choque'))), delclone()]])],
     variables=['segundos'], shown=['segundos']),
  ['Añade monedas que den puntos extra.', 'Haz que los meteoritos caigan más rápido según pasa el tiempo.'])

R('juegos', 'Rompeladrillos', 3, '45 min', ['clones', 'bucles anidados', 'mensajes'],
  'Romper todos los ladrillos con la pelota sin dejar que caiga.',
  ['Con dos <i>repetir</i> (uno dentro de otro) crea 3 filas de 7 clones de ladrillo.',
   'Cada clon espera a que lo toque la pelota: suma un punto, avisa a la pelota y desaparece.',
   'La pelota rebota en bordes, pala y ladrillos.', 'Con 21 puntos has ganado; si la pelota cae, has perdido.'],
  ['Para crear las filas: repetir 3 { repetir 7 { crear clon, sumar a x 60 }, dar a x el valor −180, sumar a y −25 }.',
   'El ladrillo original está escondido, así que no estorba.'],
  P1(['blanco'], [
      Sprite('Ladrillo', ['ladrillo'], [[flag(), hide(), setv('puntos', 0), gotoxy(-180, 150),
                                         rep(3, rep(7, clone(), chx(60)), setx(-180), chy(-25))],
                                        [as_clone(), show(), until(touching('Pelota')), chv('puntos', 1), play('pop'), send('rebota'), delclone()]],
             sounds=['pop']),
      Sprite('Pala', ['pala'], [[flag(), gotoxy(0, -160), forever(setx(mx()))]]),
      Sprite('Pelota', ['pelota'], [[flag(), gotoxy(0, -100), point(30), wait(1), forever(move(6), bounce(),
          if_(touching('Pala'), point(sub(180, direction())), move(8)),
          if_(lt(ypos(), -170), say('¡Has perdido!', 2), stop('all')),
          if_(eq(v('puntos'), 21), say('¡Has ganado!', 2), stop('all')))],
          [recv('rebota'), point(sub(180, direction()))]], size=60)],
     variables=['puntos'], shown=['puntos']),
  ['Ladrillos que necesitan dos golpes (usa dos disfraces).', 'Una vida extra al romper cierto ladrillo.'])

# ============================ Historias y animación
R('historias', 'Cuento en tres escenas', 2, '35 min', ['mensajes', 'fondos', 'secuencia'],
  'Contar una pequeña historia con un protagonista que viaja por tres lugares y habla con otros personajes.',
  ['Escribe primero el guion en papel: qué pasa en cada escena.', 'El protagonista lleva la historia: cambia los fondos y habla.',
   'Los demás personajes se muestran solo en su escena (<i>cuando el fondo cambie a</i>).',
   'Para dar turno de palabra usa <i>enviar … y esperar</i>.'],
  ['<i>enviar … y esperar</i> hace que el protagonista espere a que el otro personaje termine de hablar.'],
  P1(['cielo', 'mar', 'espacio'], [
      Sprite('Robit', ['robit1', 'robit2'], [[flag(), gotoxy(-150, -80), backdrop('cielo'), say('Érase una vez un robot que quería conocer el mundo', 3),
                                           glide(2, 150, -80), backdrop('mar'), gotoxy(-150, -80), say('Primero llegó al mar...', 2), sendw('habla pez'),
                                           say('¡Gracias, pez! Me voy al espacio', 2), backdrop('espacio'), say('¡Qué silencio hay aquí!', 2),
                                           sendw('habla estrella'), say('Y así Robit conoció el mundo. FIN', 3)]], size=80),
      Sprite('Pez', ['pez'], [[flag(), hide()], [onbackdrop('mar'), show()], [onbackdrop('espacio'), hide()],
                              [recv('habla pez'), say('¡Hola, Robit! Si subes muy alto verás las estrellas', 3)]], x=120, y=40),
      Sprite('Estrella', ['estrella'], [[flag(), hide()], [onbackdrop('espacio'), show()],
                                        [recv('habla estrella'), say('Desde aquí se ve todo el planeta', 3)]], x=120, y=100)]),
  ['Añade sonidos o música en cada escena.', 'Deja que quien lo ve elija el final con una pregunta.'])

R('historias', 'Concurso de preguntas', 2, '30 min', ['sensores', 'condicionales', 'variables'],
  'Un presentador que hace preguntas, comprueba las respuestas y lleva la puntuación.',
  ['Pon los puntos a 0.', 'Para cada pregunta: preguntar, comprobar la respuesta con <i>si … si no</i> y sumar punto si acierta.',
   'Al final, decir la puntuación.'],
  ['Scratch no distingue mayúsculas de minúsculas al comparar, pero sí las tildes: acepta las dos formas con <i>o</i>.'],
  P1(['teatro'], [Sprite('Robit', ['robit1'], [[flag(), setv('puntos', 0), say('¡Bienvenido al concurso!', 2),
      ask('¿Cuántas patas tiene una araña?'),
      ifelse(eq(answer(), 8), [chv('puntos', 1), play('ding'), say('¡Correcto!', 1)], [play('error'), say('Son 8', 1)]),
      ask('¿Cuál es el planeta más grande del sistema solar?'),
      ifelse(or_(eq(answer(), 'Júpiter'), eq(answer(), 'Jupiter')), [chv('puntos', 1), play('ding'), say('¡Correcto!', 1)], [play('error'), say('Es Júpiter', 1)]),
      ask('¿Cuánto es 7 x 6?'),
      ifelse(eq(answer(), 42), [chv('puntos', 1), play('ding'), say('¡Correcto!', 1)], [play('error'), say('Es 42', 1)]),
      say(join('Has conseguido ', join(v('puntos'), ' de 3 puntos')), 3)]], sounds=['ding', 'error'])],
     variables=['puntos'], shown=['puntos']),
  ['Crea el bloque <i>acierto</i> en «Mis bloques» para no repetir código.', 'Guarda preguntas y respuestas en dos listas.'])

R('historias', 'Coreografía robótica', 2, '30 min', ['paralelismo', 'música', 'animación'],
  'Robit baila al ritmo de una base de percusión que suena a la vez.',
  ['Añade la extensión Música.', 'Un programa toca la base: bombo, caja, bombo, caja…', 'Otro programa, con el mismo evento, hace los pasos de baile.',
   'Los dos empiezan a la vez con la bandera verde: eso es <b>paralelismo</b>.'],
  ['A tempo 60, cada tiempo dura un segundo: ajusta las esperas del baile al ritmo.'],
  P1(['teatro'], [Sprite('Robit', ['robit1', 'robit2'], [[flag(), tempo(120), rep(8, drum(2, 0.5), drum(1, 0.5))],
                                                     [flag(), gotoxy(0, -60), rep(4, glide(0.5, -80, -60), nextc(), glide(0.5, 80, -60), nextc(),
                                                                                  rep(4, turn(90)), rep(2, size(20), wait(0.25), size(-20), wait(0.25)))]])]),
  ['Añade una pareja de baile que copie los pasos en espejo.', 'Cambia el fondo de color en cada compás.'])

R('historias', 'Tarjeta de felicitación interactiva', 1, '30 min', ['eventos', 'mensajes', 'efectos'],
  'Una tarjeta en la que cada personaje reacciona al hacer clic, y un botón que lanza una fiesta.',
  ['Cada objeto tiene su programa <i>al hacer clic en este objeto</i>.', 'El botón envía el mensaje «fiesta».',
   'Todos (también el escenario) reaccionan al recibir «fiesta».'],
  ['El escenario también puede cambiar efectos de color en su fondo.'],
  P1(['teatro'], [Sprite('Robit', ['robit1', 'robit2'], [[flag(), say('Haz clic en todo lo que veas', 3)], [clicked(), say('¡Feliz día!', 2)],
                                                     [recv('fiesta'), rep(10, nextc(), wait(0.1))]], x=-110, y=-40),
                  Sprite('Estrella', ['estrella'], [[clicked(), play('ding'), rep(36, turn(10))],
                                                    [recv('fiesta'), rep(10, effect('COLOR', 20), wait(0.1)), cleareff()]], x=110, y=80, sounds=['ding']),
                  Sprite('Boton', ['boton'], [[clicked(), play('victoria'), send('fiesta')]], x=130, y=-90, sounds=['victoria'])],
     stage_scripts=[[recv('fiesta'), rep(20, effect('COLOR', 10), wait(0.05)), cleareff()]]),
  ['Escribe un mensaje personal con el editor de fondos.', 'Graba tu voz felicitando.'])

R('historias', 'El narrador que habla', 2, '25 min', ['texto a voz', 'sensores'],
  'Robit cuenta una historia en voz alta y después lee lo que escribas.',
  ['Añade la extensión <b>Texto a voz</b> (necesita internet).', 'Fija el idioma a español y asigna una voz.',
   'Muestra cada frase en un bocadillo mientras la lee.', 'Al hacer clic, pide una frase y la lee.'],
  ['El <i>decir</i> de Texto a voz habla en voz alta; el <i>decir</i> de Apariencia muestra el bocadillo. Se pueden usar juntos.'],
  P1(['noche'], [Sprite('Robit', ['robit1', 'robit2'], [[flag(), lang('es'), voice('ALTO'),
      say('Había una vez una estrella que no sabía brillar'), speak('Había una vez una estrella que no sabía brillar'),
      say('Un robot le enseñó a encender su luz'), speak('Un robot le enseñó a encender su luz'),
      say('Y desde entonces ilumina las noches'), speak('Y desde entonces ilumina las noches'), say('Haz clic en mí')],
      [clicked(), ask('Escribe una frase y la leeré'), say(answer()), speak(answer()), say('')]])]),
  ['Prueba otras voces del menú <i>asignar voz a</i>.', 'Haz que dos personajes dialoguen con voces distintas.'])

# ============================ Arte con lápiz
R('arte', 'Polígonos a la carta', 2, '25 min', ['variables', 'operadores', 'geometría'],
  'Dibujar cualquier polígono regular indicando su número de lados.',
  ['Pregunta cuántos lados quieres y guarda la respuesta en <b>lados</b>.', 'Repite <b>lados</b> veces: avanzar y girar.',
   '¿Cuánto girar? 360 dividido entre el número de lados.'],
  ['Para que todos quepan, haz que el lado mida 400 / lados.'],
  P1(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), ask('¿Cuántos lados? (3 a 20)'), setv('lados', answer()),
                                              gotoxy(-60, -120), point(90), psize(3), pcolor('#9966ff'), pdown(),
                                              rep(v('lados'), move(div(400, v('lados'))), turn(div(360, v('lados'))), wait(0.1)), pup()]])]),
  ['¿Qué pasa con 100 lados? ¿Por qué?', 'Rellena el escenario de polígonos de colores.'])

R('arte', 'Flor de cuadrados', 2, '20 min', ['bucles anidados', 'geometría'],
  'Crear una flor girando un cuadrado alrededor de su esquina.',
  ['Haz que el objeto dibuje un cuadrado.', 'Repite 12 veces: dibujar el cuadrado y girar 30 grados.', 'Cambia el color del lápiz en cada vuelta.'],
  ['12 × 30 = 360: la flor da la vuelta completa.'],
  P1(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), gotoxy(0, 0), point(90), psize(2), pcolor('#e85d2a'), pdown(),
                                              rep(12, rep(4, move(90), turn(90)), turn(30), pchcolor(8)), pup()]])]),
  ['Prueba con triángulos o hexágonos.', 'Usa 36 vueltas de 10 grados.'])

R('arte', 'Pinta con el ratón', 2, '25 min', ['condicionales', 'eventos'],
  'Un programa de dibujo: pintas al mantener pulsado el ratón y cambias de color con el teclado.',
  ['Por siempre: ir al puntero del ratón.', 'Si el ratón está presionado, bajar lápiz; si no, subirlo.',
   'Teclas: <b>r</b> rojo, <b>a</b> azul, <b>v</b> verde, <b>b</b> borrar todo.'],
  ['El objeto lápiz conviene que sea muy pequeño, o escóndelo con el efecto desvanecer.'],
  P1(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), psize(6), pcolor('#222222'),
                                              forever(goto('_mouse_'), ifelse(mousedown(), [pdown()], [pup()]))],
                                             [key('r'), pcolor('#d7263d')], [key('a'), pcolor('#3d8bd6')], [key('v'), pcolor('#2f9e57')], [key('b'), pclear()]])]),
  ['Teclas para cambiar el grosor.', 'Un «pincel arcoíris» que cambie de color solo mientras pintas.'])

R('arte', 'Espiral de colores', 2, '20 min', ['variables', 'bucles'],
  'Dibujar una espiral que crece y cambia de color.',
  ['Crea la variable <b>lado</b>, empezando en 2.', 'Repite 120 veces: avanzar <b>lado</b> pasos, girar 91 grados, sumar 3 a lado y cambiar el color.'],
  ['Con 90 grados sale una espiral cuadrada; con 91 se va retorciendo.'],
  P1(['noche'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), gotoxy(0, 0), point(90), setv('lado', 2), psize(2), pcolor('#ff3366'), pdown(),
                                             rep(120, move(v('lado')), turn(91), chv('lado', 3), pchcolor(2)), pup()]])]),
  ['Prueba 121, 89 o 60 grados.', 'Pregunta el ángulo al empezar.'])

R('arte', 'Caleidoscopio de sellos', 3, '30 min', ['variables', 'bucles anidados', 'lápiz'],
  'Formar un mandala sellando estrellas en anillos alrededor del centro.',
  ['Un anillo: repetir 12 veces { ir al centro, girar 30, avanzar el radio, sellar }.',
   'Repite 4 anillos, aumentando el radio y cambiando color y tamaño.'],
  ['Guarda el radio en una variable para que cada anillo sea más grande.'],
  P1(['noche'], [Sprite('Estrella', ['estrella'], [[flag(), pclear(), show(), setv('radio', 40), setsize(40), point(0),
                                                   rep(4, rep(12, gotoxy(0, 0), turn(30), move(v('radio')), stamp()), chv('radio', 40), size(15),
                                                       effect('COLOR', 30)), hide()]])]),
  ['Haz que gire todo con una tecla y vuelva a sellar.', 'Usa otros objetos dibujados por ti.'])

# ============================ Música
R('musica', 'Batería con el teclado', 1, '20 min', ['eventos', 'música'],
  'Una batería completa: cada tecla, un instrumento de percusión.',
  ['Añade la extensión Música.', 'Asigna teclas: a bombo, s caja, d charles, f platillo, g palmada.', 'Que el tambor se haga un poco más grande al sonar.'],
  ['Duraciones cortas (0.25 tiempos) hacen que suene más seco.'],
  P1(['teatro'], [Sprite('Tambor', ['tambor'], [[key(k), setsize(115), drum(d, 0.25), setsize(100)] for k, d in
                                               [('a', 2), ('s', 1), ('d', 6), ('f', 4), ('g', 8)]], size=150)]),
  ['Graba un ritmo y repítelo con <i>repetir</i>.', 'Haz un objeto distinto para cada instrumento.'])

def piano():
    sprites = []
    for i, (k, nota, nombre) in enumerate(zip('asdfghjk', [60, 62, 64, 65, 67, 69, 71, 72], ['do', 're', 'mi', 'fa', 'sol', 'la', 'si', 'do2'])):
        sc = [costume('tecla_on'), note(nota, 0.5), costume('tecla')]
        sprites.append(Sprite('Tecla ' + nombre, ['tecla', 'tecla_on'], [[key(k)] + sc, [clicked()] + [costume('tecla_on'), note(nota, 0.5), costume('tecla')]],
                              x=-157 + i * 45, y=0))
    return P1(['blanco'], sprites)
R('musica', 'Piano de ocho teclas', 2, '30 min', ['eventos', 'música', 'objetos'],
  'Un piano con una escala de do mayor que se toca con el teclado o con el ratón.',
  ['Crea una tecla con dos disfraces (normal e iluminada).', 'Al pulsar su letra o al hacer clic: iluminarse, tocar su nota y apagarse.',
   'Duplica la tecla 7 veces y cambia letra y nota en cada una (60, 62, 64, 65, 67, 69, 71, 72).'],
  ['En la extensión Música, el 60 es el do central. Haz clic en el número de la nota para ver un teclado.',
   'Botón derecho sobre un objeto › <i>duplicar</i> copia también sus programas.'],
  piano(),
  ['Cambia el instrumento con una tecla.', 'Añade las teclas negras.'])

R('musica', 'Melodía guardada en una lista', 3, '30 min', ['listas', 'variables', 'bucles'],
  'Guardar las notas de una canción en una lista y que el programa las toque una a una.',
  ['Crea la lista <b>notas</b> y la variable <b>i</b>.', 'Al empezar, vacía la lista y añade las notas de «Estrellita, ¿dónde estás?».',
   'Recorre la lista: i empieza en 1 y, mientras no pase de la longitud, toca el elemento i y suma 1.'],
  ['<i>repetir (longitud de notas)</i> recorre toda la lista sin tener que contar.'],
  P1(['noche'], [Sprite('Estrella', ['estrella'], [[flag(), lclear('notas')] + [ladd(x, 'notas') for x in [60, 60, 67, 67, 69, 69, 67]] +
                                                  [setv('i', 1), instr(17), rep(llen('notas'), note(litem(v('i'), 'notas'), 0.5), turn(15), chv('i', 1))]])],
     lists=['notas']),
  ['Añade una segunda lista con la duración de cada nota.', 'Completa la canción entera.'])

R('musica', 'Ritmo en bucle con tempo variable', 2, '20 min', ['bucles', 'música', 'eventos'],
  'Una base de percusión que no para, cuya velocidad se cambia con las flechas.',
  ['Por siempre: bombo, charles, caja, charles.', 'Flecha arriba: sube el tempo 10. Flecha abajo: lo baja 10.', 'Que el tambor diga el tempo actual.'],
  ['El reportero <i>tempo</i> de la extensión Música da la velocidad en tiempos por minuto.'],
  P1(['teatro'], [Sprite('Tambor', ['tambor'], [[flag(), tempo(90), forever(drum(2, 0.5), drum(6, 0.5), drum(1, 0.5), drum(6, 0.5))],
                                               [key('up arrow'), chtempo(10), say(join('Tempo: ', gettempo()), 1)],
                                               [key('down arrow'), chtempo(-10), say(join('Tempo: ', gettempo()), 1)]], size=150)]),
  ['Añade una melodía que siga el mismo tempo.', 'Cambia de ritmo con la tecla espacio.'])

R('musica', 'Orquesta de dos', 3, '35 min', ['mensajes', 'paralelismo', 'música'],
  'Un director (botón) da la entrada y dos músicos tocan a la vez, cada uno su parte.',
  ['El botón, al hacer clic, envía «empieza».', 'Robit toca una línea de bajo con el instrumento bajo.', 'El tambor toca la percusión.',
   'Los dos empiezan al recibir el mensaje, así van sincronizados.'],
  ['Ambas partes deben durar lo mismo: cuenta los tiempos.'],
  P1(['teatro'], [Sprite('Boton', ['boton'], [[flag(), tempo(100)], [clicked(), send('empieza')]], x=0, y=-120),
                  Sprite('Robit', ['robit1', 'robit2'], [[recv('empieza'), instr(6), rep(2, note(48, 1), nextc(), note(55, 1), nextc(), note(53, 1), nextc(), note(55, 1), nextc())]], x=-120),
                  Sprite('Tambor', ['tambor'], [[recv('empieza'), rep(8, drum(2, 0.5), drum(1, 0.5))]], x=120)]),
  ['Añade un tercer músico con la melodía.', 'Un segundo botón que pare todo con <i>detener todos los sonidos</i>.'])

# ============================ Makey Makey
MK = ['Placa Makey Makey, pinzas de cocodrilo y objetos conductores.']
R('makey', 'Piano de frutas', 1, '30 min', ['eventos', 'música', 'circuitos'],
  'Tocar cinco notas tocando cinco piezas de fruta.',
  ['Conecta cada fruta a una entrada: espacio, izquierda, arriba, derecha, abajo.', 'Sujeta el cable de tierra (EARTH) con la otra mano.',
   'En Scratch, con la extensión Makey Makey, programa cada entrada para tocar una nota.'],
  ['Si no suena, comprueba que tocas la tierra y que la pinza está bien clavada en la fruta.'],
  P1(['blanco'], [Sprite('Robit', ['robit1', 'robit2'], [[makey(k), nextc(), note(nn, 0.5), say(nombre, 0.3)] for k, nn, nombre in
                                                    [('SPACE', 60, 'do'), ('LEFT', 62, 're'), ('UP', 64, 'mi'), ('RIGHT', 65, 'fa'), ('DOWN', 67, 'sol')]])]),
  ['Cambia el instrumento a marimba o guitarra.', 'Haz una batería de plastilina.'], materiales=MK)

def quiz_q(q, correcta_izq):
    ok = [chv('puntos', 1), play('ding'), say('¡Bien!', 1)]
    ko = [play('error'), say('¡Oh, no!', 1)]
    return [say(q), until(or_(keyp('left arrow'), keyp('right arrow'))),
            ifelse(keyp('left arrow'), ok if correcta_izq else ko, ko if correcta_izq else ok), wait(0.5)]
R('makey', 'Verdadero o falso con plátanos', 2, '30 min', ['condicionales', 'sensores'],
  'Un juego de preguntas en el que se responde tocando un plátano (verdadero) u otro (falso).',
  ['Conecta un plátano a la flecha izquierda (verdadero) y otro a la derecha (falso).', 'Robit muestra una afirmación y espera a que se toque uno.',
   'Comprueba cuál se ha tocado y suma puntos.'],
  ['Makey Makey se comporta como un teclado: <i>¿tecla flecha izquierda presionada?</i> detecta el plátano.'],
  P1(['teatro'], [Sprite('Robit', ['robit1'], [[flag(), setv('puntos', 0), say('Izquierda = verdadero · Derecha = falso', 3)] +
                                            quiz_q('El Sol es una estrella', True) + quiz_q('Las arañas tienen 6 patas', False) +
                                            quiz_q('El agua hierve a 100 grados al nivel del mar', True) +
                                            [say(join('Puntos: ', v('puntos')), 3)]], sounds=['ding', 'error'])],
     variables=['puntos'], shown=['puntos']),
  ['Usa plastilina verde y roja.', 'Añade un tiempo límite para responder.'], materiales=MK)

R('makey', 'No toques el cable', 2, '40 min', ['eventos', 'variables', 'circuitos'],
  'El clásico juego de pulso: recorrer un alambre con una anilla sin tocarlo.',
  ['Dobla un alambre (o una tira de papel de aluminio) y conéctalo a <b>espacio</b>.',
   'Haz una anilla de alambre, conéctala a <b>tierra</b>: será la varita.', 'Pon al final un trozo de aluminio conectado a la <b>flecha derecha</b>: es la meta.',
   'Cada toque resta una vida. Al llegar a la meta, se muestra el tiempo.'],
  ['Al tocar, el circuito se cierra y la placa «pulsa» espacio.', 'Pon una espera tras cada toque para no perder todas las vidas de golpe.'],
  P1(['blanco'], [Sprite('Robit', ['robit1'], [[flag(), setv('vidas', 3), rtimer(), say('¡Adelante! No toques el cable')],
                                            [makey('SPACE'), chv('vidas', -1), play('error'), say('¡Bzzz!', 1),
                                             if_(lt(v('vidas'), 1), say('¡Te has quedado sin vidas!', 2), stop('all'))],
                                            [makey('RIGHT'), play('victoria'), setv('tiempo', round_(timer())),
                                             say(join('¡Meta en ', join(v('tiempo'), ' segundos!')), 3), stop('all')]], sounds=['error', 'victoria'])],
     variables=['vidas', 'tiempo'], shown=['vidas', 'tiempo']),
  ['Lleva un récord con una variable.', 'Un alambre más difícil para el nivel 2.'],
  materiales=['Makey Makey, pinzas de cocodrilo, alambre o papel de aluminio sobre cartón, plastilina como soporte.'])

R('makey', 'Combinación secreta', 2, '25 min', ['eventos', 'secuencias'],
  'Una caja fuerte que solo se abre tocando tres objetos en el orden correcto.',
  ['Conecta tres objetos a izquierda, arriba y derecha.', 'Usa el bloque <i>al presionar … en orden</i>.',
   'Con la combinación correcta: sonido de victoria y Robit abre la caja. Con abajo: reiniciar.'],
  ['El bloque tiene varias combinaciones predefinidas en el desplegable.'],
  P1(['teatro'], [Sprite('Robit', ['robit1', 'robit2'], [[flag(), costume('robit1'), say('Introduce la combinación secreta')],
                                                     [makeycode('LEFT UP RIGHT'), play('victoria'), costume('robit2'), say('¡Caja abierta! Has encontrado el tesoro', 3)],
                                                     [makey('DOWN'), costume('robit1'), say('Caja cerrada. Inténtalo otra vez')]], sounds=['victoria'])]),
  ['Haz que la combinación incorrecta suene a error.', 'Inventa una historia de escape room.'], materiales=MK)

R('makey', 'Mando de carreras', 3, '40 min', ['sensores', 'condicionales', 'variables'],
  'Un coche visto desde arriba que se conduce con un mando de plastilina y recoge monedas. Espacio da turbo.',
  ['Haz un mando con cuatro bolas de plastilina: izquierda, derecha y espacio (turbo).', 'El coche avanza siempre y gira con izquierda y derecha.',
   'Al tocar espacio, hace un turbo.', 'La moneda suma un punto y salta a otro sitio.'],
  ['Para girar mientras se mantiene pulsado, usa <i>¿tecla … presionada?</i> dentro de <i>por siempre</i>.'],
  P1(['campo'], [Sprite('Coche', ['coche'], [[flag(), gotoxy(0, 0), setv('puntos', 0), forever(move(3), bounce(),
                                                                                         if_(keyp('left arrow'), turnl(5)), if_(keyp('right arrow'), turn(5)))],
                                           [makey('SPACE'), rep(10, move(8))]], size=60),
                 Sprite('Moneda', ['moneda'], [[flag(), goto('_random_'), forever(until(touching('Coche')), chv('puntos', 1), play('ding'), goto('_random_'))]],
                        sounds=['ding'])], variables=['puntos'], shown=['puntos']),
  ['Añade un cronómetro de 60 segundos.', 'Un segundo coche para jugar a dos.'], materiales=MK)

# ============================ micro:bit
MB = ['micro:bit con el HEX de Scratch, Scratch Link y Bluetooth.']
R('microbit', '¡Hola, micro:bit!', 1, '25 min', ['eventos', 'hardware'],
  'Comprobar la conexión: los botones muestran dibujos en los LED y al agitar la placa aparece un saludo.',
  ['Conecta la micro:bit siguiendo los pasos de la introducción.', 'Botón A: mostrar un corazón y que Robit lo diga.',
   'Botón B: mostrar una cara sonriente.', 'Al agitarla: mostrar el texto «Hola».'],
  ['El bloque <i>mostrar</i> tiene una cuadrícula: haz clic en los LED que quieras encender.'],
  P1(['blanco'], [Sprite('Robit', ['robit1'], [[mb_btn('A'), mb_show(HEART), say('Corazón', 1)], [mb_btn('B'), mb_show(SMILE), say('Sonrisa', 1)],
                                            [mb_gesture('shaken'), mb_text('Hola'), say('¡Me has agitado!', 1)]])]),
  ['Diseña tus propios iconos.', 'Al pulsar A y B a la vez, borrar la pantalla.'], materiales=MB)

R('microbit', 'Inclina para mover', 2, '25 min', ['sensores', 'operadores'],
  'Mover a Robit a izquierda y derecha inclinando la placa.',
  ['Usa el reportero <i>ángulo de inclinación hacia derecha</i>: da números positivos al inclinar a la derecha y negativos a la izquierda.',
   'Por siempre: sumar a x (ángulo de inclinación / 5).'],
  ['Dividir entre 5 hace que el movimiento sea más suave. Prueba otros valores.'],
  P1(['campo'], [Sprite('Robit', ['robit1'], [[flag(), gotoxy(0, 0), forever(chx(div(mb_angle('right'), 5)),
                                                                          if_(touching('_edge_'), say('¡Cuidado!', 0.5)))]], size=60)]),
  ['Añade el movimiento arriba y abajo con <i>ángulo de inclinación hacia delante</i>.', 'Convierte esto en el juego de atrapar del reto E01.'], materiales=MB)

R('microbit', 'El dado que se agita', 1, '20 min', ['operadores', 'hardware'],
  'Un dado electrónico: agitas la micro:bit y aparece un número del 1 al 6 en sus LED y en pantalla.',
  ['Evento: <i>al agitar</i>.', 'Guarda un número aleatorio entre 1 y 6 en <b>dado</b>.', 'Muéstralo en los LED y que Robit lo diga.'],
  ['<i>mostrar texto</i> puede mostrar números.'],
  P1(['blanco'], [Sprite('Robit', ['robit1'], [[mb_gesture('shaken'), setv('dado', rnd(1, 6)), mb_text(v('dado')), play('pop'),
                                            say(join('Ha salido un ', v('dado')), 2)]], sounds=['pop'])],
     variables=['dado'], shown=['dado']),
  ['Que al pulsar A muestre la suma de dos dados.', 'Cuenta cuántos seises salen.'], materiales=MB)

R('microbit', 'Atrapa manzanas inclinando', 2, '35 min', ['sensores', 'variables', 'hardware'],
  'El juego de atrapar manzanas, pero moviendo la cesta con la inclinación de la micro:bit.',
  ['La cesta: por siempre, dar a x el valor (ángulo de inclinación hacia derecha × 3).', 'La manzana cae como en el reto E01 y suma puntos al tocar la cesta.',
   'Cada 5 puntos, la micro:bit muestra un corazón.'],
  ['Si la cesta se sale del escenario, reduce el número por el que multiplicas.'],
  P1(['cielo'], [Sprite('Cesta', ['cesta'], [[flag(), gotoxy(0, -150), forever(setx(mul(mb_angle('right'), 3)))]]),
                 Sprite('Manzana', ['manzana'], [[flag(), setv('puntos', 0), gotoxy(rnd(-200, 200), 180), forever(chy(-4),
                     if_(touching('Cesta'), chv('puntos', 1), play('pop'), mb_text(v('puntos')), gotoxy(rnd(-200, 200), 180)),
                     if_(lt(ypos(), -170), gotoxy(rnd(-200, 200), 180)))]], sounds=['pop'])],
     variables=['puntos'], shown=['puntos']),
  ['Añade vidas y muestra una cara triste al perder.', 'Usa el botón A para pausar.'], materiales=MB)

R('microbit', 'Pulsador de concurso', 3, '40 min', ['variables', 'condicionales', 'hardware'],
  'Dos jugadores, uno con el botón A y otro con el B. Tras la señal, gana quien pulse primero. ¡Quien se adelante, pierde punto!',
  ['La variable <b>listo</b> vale 0 mientras se espera y 1 cuando se da la señal.', 'Robit espera un tiempo aleatorio y da la señal (listo = 1).',
   'Al pulsar A: si listo = 1, gana A (punto, listo = 0); si no, A pierde un punto.', 'Lo mismo con B. Pulsa la bandera para otra ronda.'],
  ['El tiempo aleatorio evita que se pueda adivinar cuándo saldrá la señal.'],
  P1(['teatro'], [Sprite('Robit', ['robit1'], [[flag(), setv('listo', 0), mb_clear(), say('Preparados...'), wait(rnd(2, 5)),
                                             setv('listo', 1), mb_show(HEART), play('ding'), say('¡YA!')],
                                            [mb_btn('A'), ifelse(eq(v('listo'), 1), [setv('listo', 0), chv('puntos A', 1), mb_show(ARROW_L), say('¡Gana A!')],
                                                                 [chv('puntos A', -1), say('A se ha adelantado', 1)])],
                                            [mb_btn('B'), ifelse(eq(v('listo'), 1), [setv('listo', 0), chv('puntos B', 1), mb_show(ARROW_R), say('¡Gana B!')],
                                                                 [chv('puntos B', -1), say('B se ha adelantado', 1)])]], sounds=['ding'])],
     variables=['puntos A', 'puntos B', 'listo'], shown=['puntos A', 'puntos B']),
  ['Que gane quien llegue antes a 5 puntos.', 'Úsalo para responder preguntas de clase.'], materiales=MB)

# ============================ Realidad aumentada
RA = ['Cámara web y extensión Sensor de vídeo.']
R('ra', 'Explota burbujas', 1, '25 min', ['sensor de vídeo', 'variables'],
  'Explotar burbujas moviendo las manos delante de la cámara.',
  ['Al empezar: activar vídeo y transparencia al 50.', 'Por siempre: si el movimiento de vídeo en el objeto es mayor que 30, sonar, sumar un punto y saltar a otro sitio.'],
  ['<i>movimiento de vídeo en objeto</i> solo mide el movimiento que hay justo detrás de la burbuja.'],
  P1(['blanco'], [Sprite('Burbuja', ['burbuja'], [[flag(), video('on'), vtransp(50), setv('puntos', 0), goto('_random_'),
                                                 forever(if_(gt(vmotion('sprite'), 30), play('pop'), chv('puntos', 1), goto('_random_'), wait(0.3)))]],
                        sounds=['pop'])], variables=['puntos'], shown=['puntos']),
  ['Juega solo 30 segundos con el cronómetro.', 'Burbujas «malas» que restan puntos.'], materiales=RA)

R('ra', 'Tambores en el aire', 2, '25 min', ['sensor de vídeo', 'música'],
  'Dos tambores invisibles: golpea el aire donde están para que suenen.',
  ['Crea dos objetos tambor, uno a cada lado.', 'Cada uno, por siempre: si detecta movimiento, toca su sonido y se agranda un momento.'],
  ['Añade una pequeña espera tras cada golpe para que no suene muchas veces seguidas.'],
  P1(['blanco'], [Sprite('Tambor', ['tambor'], [[flag(), video('on'), vtransp(60), forever(if_(gt(vmotion('sprite'), 40), setsize(130), drum(2, 0.25), setsize(100), wait(0.2)))]], x=-150, y=-80),
                  Sprite('Platillo', ['tambor'], [[flag(), forever(if_(gt(vmotion('sprite'), 40), setsize(130), drum(4, 0.25), setsize(100), wait(0.2)))]], x=150, y=-80)]),
  ['Añade más instrumentos.', 'Graba tu propio sonido para cada tambor.'], materiales=RA)

R('ra', 'Saluda a Robit', 1, '15 min', ['sensor de vídeo', 'eventos'],
  'Robit te devuelve el saludo cuando mueves la mano.',
  ['Activa el vídeo al empezar.', 'Usa el evento <i>cuando movimiento de vídeo &gt; 50</i>.', 'Robit saluda cambiando de disfraz y dice «¡Hola!».'],
  ['Este evento mide el movimiento de toda la imagen, no solo detrás de Robit.'],
  P1(['blanco'], [Sprite('Robit', ['robit1', 'robit2'], [[flag(), video('on'), vtransp(40)],
                                                     [vmotion_gt(50), say('¡Hola!'), rep(4, nextc(), wait(0.2)), say(''), wait(1)]])]),
  ['Que hable en voz alta con Texto a voz.', 'Que se asuste si el movimiento es muy grande.'], materiales=RA)

R('ra', 'Empuja la pelota', 2, '25 min', ['sensor de vídeo', 'dirección'],
  'Una pelota que se desplaza en la dirección en la que la empujas con la mano.',
  ['Por siempre: si hay movimiento sobre la pelota, apuntar en la <i>dirección de vídeo en objeto</i> y avanzar.', 'Que rebote en los bordes.'],
  ['El sensor de vídeo no solo mide cuánto movimiento hay: también hacia dónde va.'],
  P1(['blanco'], [Sprite('Balon', ['balon'], [[flag(), video('on'), vtransp(50), gotoxy(0, 0),
                                             forever(if_(gt(vmotion('sprite'), 20), point(vmotion('sprite', 'direction')), move(15)), bounce())]], size=150)]),
  ['Pon una portería y cuenta goles.', 'Que dos personas se pasen la pelota.'], materiales=RA)

R('ra', 'Lluvia de estrellas', 3, '35 min', ['sensor de vídeo', 'clones'],
  'Caen estrellas y hay que atraparlas con las manos antes de que lleguen al suelo.',
  ['El original crea un clon cada segundo.', 'Cada clon cae desde arriba.', 'Si detecta movimiento encima, suma un punto y desaparece.',
   'Si llega abajo, desaparece sin puntos.'],
  ['Cada clon mide el movimiento en su propia posición: así se puede atrapar cada estrella por separado.'],
  P1(['blanco'], [Sprite('Estrella', ['estrella'], [[flag(), video('on'), vtransp(40), setv('puntos', 0), hide(), forever(clone(), wait(1))],
                                                   [as_clone(), gotoxy(rnd(-200, 200), 180), show(),
                                                    rep_until(lt(ypos(), -170), chy(-3), if_(gt(vmotion('sprite'), 30), chv('puntos', 1), play('ding'), delclone())),
                                                    delclone()]], sounds=['ding'])], variables=['puntos'], shown=['puntos']),
  ['Estrellas doradas que valen el doble.', 'Que cada vez caigan más rápido.'], materiales=RA)

# ============================ Ciencia y matemáticas
R('ciencia', 'Tablas de multiplicar', 2, '25 min', ['variables', 'operadores', 'azar'],
  'Practicar las tablas con cinco multiplicaciones al azar.',
  ['Repite 5 veces: dos números al azar (2 a 9) en <b>a</b> y <b>b</b>.', 'Pregunta «a x b» con <i>unir</i>.',
   'Compara la respuesta con a × b y suma un punto si acierta.'],
  ['Para escribir la pregunta: unir(a, unir(" x ", b)).'],
  P1(['blanco'], [Sprite('Robit', ['robit1'], [[flag(), setv('puntos', 0), rep(5, setv('a', rnd(2, 9)), setv('b', rnd(2, 9)),
                                            ask(join(v('a'), join(' x ', join(v('b'), ' =')))),
                                            ifelse(eq(answer(), mul(v('a'), v('b'))), [chv('puntos', 1), play('ding'), say('¡Bien!', 1)],
                                                   [play('error'), say(join('Era ', mul(v('a'), v('b'))), 2)])),
                                            say(join('Has acertado ', join(v('puntos'), ' de 5')), 3)]], sounds=['ding', 'error'])],
     variables=['puntos'], shown=['puntos']),
  ['Elige qué tabla practicar al principio.', 'Cronometra cuánto tardas.'])

R('ciencia', 'Calculadora de áreas', 2, '25 min', ['variables', 'operadores', 'lápiz'],
  'Calcular el área de un rectángulo y de un triángulo y dibujar el rectángulo.',
  ['Pregunta la base y la altura (en centímetros) y guárdalas en variables.', 'Área del rectángulo = base × altura. Área del triángulo = base × altura / 2.',
   'Dibuja el rectángulo con el lápiz a escala (1 cm = 10 pasos).'],
  ['El dibujo empieza en el centro: con base hasta 20 y altura hasta 15 cabe en el escenario.'],
  P1(['cuadricula'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), ask('Base (1 a 20 cm)'), setv('base', answer()), ask('Altura (1 a 15 cm)'),
                                                  setv('altura', answer()), gotoxy(0, 0), point(90), psize(3), pcolor('#e85d2a'), pdown(),
                                                  rep(2, move(mul(v('base'), 10)), turnl(90), move(mul(v('altura'), 10)), turnl(90)), pup(),
                                                  say(join('Rectángulo: ', join(mul(v('base'), v('altura')), ' cm²')), 3),
                                                  say(join('Triángulo: ', join(div(mul(v('base'), v('altura')), 2), ' cm²')), 3)]])]),
  ['Añade el círculo (π × r × r, con π ≈ 3,14).', 'Calcula también el perímetro.'])

R('ciencia', 'Simulación de gravedad', 3, '30 min', ['variables', 'física'],
  'Una pelota que cae acelerando y rebota cada vez menos, como en la realidad.',
  ['La variable <b>velocidad</b> empieza en 0.', 'Por siempre: restar 1 a la velocidad (la gravedad) y sumar a y la velocidad.',
   'Al llegar al suelo: colocarla en el suelo y multiplicar la velocidad por −0,8 (rebota con menos fuerza).', 'Espacio: volver a lanzarla desde arriba.'],
  ['Multiplicar por un número negativo cambia el sentido; por 0,8 pierde un 20 % de energía en cada bote.'],
  P1(['cielo'], [Sprite('Pelota', ['pelota'], [[flag(), gotoxy(0, 150), setv('velocidad', 0), forever(chv('velocidad', -1), chy(v('velocidad')),
                                                if_(lt(ypos(), -160), sety(-160), setv('velocidad', mul(v('velocidad'), -0.8))))],
                                               [key('space'), gotoxy(rnd(-150, 150), 150), setv('velocidad', 0)]])],
     variables=['velocidad'], shown=['velocidad']),
  ['Prueba con 0,5 y con 1. ¿Qué pasaría en la Luna?', 'Añade movimiento horizontal.'])

R('ciencia', 'Sistema solar en miniatura', 3, '30 min', ['bucles', 'movimiento', 'astronomía'],
  'Un planeta que gira alrededor del Sol dejando su órbita dibujada, y una luna que gira a su alrededor.',
  ['Sol en el centro.', 'Planeta: avanzar un poco y girar un poco, por siempre (así recorre un círculo) con el lápiz bajado.',
   'Luna: por siempre, ir al planeta, girar 10 grados y avanzar 25 pasos.'],
  ['Si el planeta avanza 5 pasos y gira 2 grados, el radio de su órbita es de unos 143 pasos.'],
  P1(['espacio'], [Sprite('Sol', ['sol'], [[flag(), forever(turn(1))]]),
                   Sprite('Planeta', ['planeta'], [[flag(), pclear(), pup(), gotoxy(143, 0), point(0), pcolor('#5a6b8c'), psize(1), pdown(),
                                                    forever(move(5), turnl(2))]]),
                   Sprite('Luna', ['luna'], [[flag(), forever(goto('Planeta'), turn(10), move(25))]])]),
  ['Añade un segundo planeta más lejano y más lento.', 'Investiga las órbitas reales: ¿son círculos perfectos?'])

R('ciencia', 'Traductor parlante', 2, '20 min', ['traducir', 'texto a voz'],
  'Escribir una frase y escucharla en inglés, francés y alemán.',
  ['Añade las extensiones <b>Traducir</b> y <b>Texto a voz</b>.', 'Pregunta una frase.',
   'Para cada idioma: fijar idioma de la voz, mostrar la traducción y decirla en voz alta.'],
  ['Las dos extensiones necesitan conexión a internet.'],
  P1(['blanco'], [Sprite('Robit', ['robit1'], [[flag(), ask('Escribe una frase en español')] +
                                            sum([[lang(l), say(join(nom, translate(answer(), l))), speak(translate(answer(), l))]
                                                 for l, nom in [('en', 'Inglés: '), ('fr', 'Francés: '), ('de', 'Alemán: ')]], []) + [say('')]])]),
  ['Haz un juego de vocabulario en inglés.', 'Pregunta a qué idioma quiere traducir.'])
