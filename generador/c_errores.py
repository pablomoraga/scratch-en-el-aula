# -*- coding: utf-8 -*-
"""Retos «Encuentra el error»: un proyecto con un fallo escondido y su solución."""
from common import *

SEC = 'errores'
ERRORES = []

def robit(scripts, back=('blanco',), **kw):
    return Project(list(back), [Sprite('Robit', ['robit1', 'robit2', 'robit3'], scripts, **kw)])

def E(slug, title, nivel, conceptos, sintoma, investiga, pistas, explicacion, mal, bien, ampliar):
    n = len(ERRORES) + 1
    num = 'D%02d' % n
    PROJECTS[slug + '-con-error'] = mal
    PROJECTS[slug + '-solucion'] = bien
    ERRORES.append(dict(num=num, slug=slug, title=title))
    head = ('<div class="ficha"><span class="chip">Error %s</span><span class="chip">Dificultad %s</span><span class="chip">⏱ 10-15 min</span>%s</div>'
            % (num, NIVEL[nivel], ''.join('<span class="chip chip-c">%s</span>' % e(c) for c in conceptos)))
    body = head + '<p class="objetivo"><b>¿Qué pasa?</b> %s</p>' % sintoma
    body += dl(slug + '-con-error', 'Descargar el proyecto con error (.sb3)') + jugar(slug + '-con-error')
    body += '<h3>El programa</h3>' + code(mal)
    body += '<h3>Investiga</h3>' + ol(investiga)
    body += '<details class="ayuda"><summary>🆘 Ayuda: pistas</summary>%s</details>' % ul(pistas)
    body += ('<details class="ayuda"><summary>✅ Ayuda: el error y su arreglo</summary><p>%s</p>%s%s</details>'
             % (explicacion, code(bien), dl(slug + '-solucion', 'Descargar el proyecto arreglado (.sb3)')))
    body += box('reto', '¿Y si…?', ul(ampliar))
    RETOS.append(dict(section=SEC, num=num, slug=slug, title=title, nivel=nivel, tiempo='10-15 min', conceptos=conceptos,
                      objetivo=sintoma, pasos=investiga, pistas=pistas, ampliar=ampliar, materiales=None))
    page(SEC, slug, title, body, kind='reto', meta=dict(num=num, nivel=nivel, tiempo='10-15 min'))

# 1 ---------------------------------------------------------------------
E('error-01', 'Robit no se entera', 1, ['eventos'],
  'Pulsamos la bandera verde y Robit no dice nada, aunque los bloques están ahí.',
  ['Mira el primer bloque del programa: ¿qué forma tiene?', '¿Qué tiene que pasar para que un programa empiece?'],
  ['Todo programa necesita un bloque de la categoría <b>Eventos</b> arriba del todo.'],
  'Faltaba el bloque sombrero <i>al hacer clic en ⚑</i>. Sin él, Scratch no sabe cuándo empezar.',
  robit([[say('¡Hola!', 2), say('Me llamo Robit', 2)]]),
  robit([[flag(), say('¡Hola!', 2), say('Me llamo Robit', 2)]]),
  ['Haz que también salude al hacer clic sobre él.'])

# 2 ---------------------------------------------------------------------
E('error-02', 'Robit se teletransporta', 1, ['bucles', 'animación'],
  'Robit debería cruzar el escenario andando, pero aparece al otro lado de golpe.',
  ['Cuenta cuántos pasos da y cuánto dura cada uno.', '¿Le da tiempo a tus ojos a ver cada movimiento?'],
  ['El ordenador ejecuta las repeticiones muchísimo más rápido de lo que podemos ver.', 'Busca en Control un bloque que haga una pausa.'],
  'Faltaba <i>esperar 0.1 segundos</i> dentro de la repetición. Sin pausas, las 30 vueltas ocurren en un instante.',
  robit([[flag(), gotoxy(-180, 0), rep(30, move(10), nextc())]]),
  robit([[flag(), gotoxy(-180, 0), rep(30, move(10), nextc(), wait(0.1))]]),
  ['Cambia el tiempo de espera: ¿cuál queda más natural?'])

# 3 ---------------------------------------------------------------------
E('error-03', 'La pelota pegada', 1, ['movimiento', 'bucles'],
  'La pelota sale disparada, llega al borde y se queda atascada allí para siempre.',
  ['¿Qué hace la pelota en cada vuelta del bucle?', '¿Hay algo que le diga qué hacer cuando llega al borde?'],
  ['En Movimiento hay un bloque pensado justo para los bordes.'],
  'Faltaba <i>si toca un borde, rebotar</i> dentro del <i>por siempre</i>.',
  Project(['blanco'], [Sprite('Pelota', ['pelota'], [[flag(), gotoxy(0, 0), point(45), forever(move(6))]])]),
  Project(['blanco'], [Sprite('Pelota', ['pelota'], [[flag(), gotoxy(0, 0), point(45), forever(move(6), bounce())]])]),
  ['Añade un sonido cada vez que rebote (pista: necesitarás <i>¿tocando borde?</i>).'])

# 4 ---------------------------------------------------------------------
E('error-04', 'Las flechas locas', 1, ['coordenadas', 'eventos'],
  'Al pulsar la flecha izquierda, Robit se va a la derecha.',
  ['Prueba cada flecha y anota hacia dónde va Robit.', 'Revisa los números de los bloques <i>sumar a x</i>.'],
  ['En el eje x, los números positivos van a la derecha y los negativos a la izquierda.'],
  'La flecha izquierda tenía <i>sumar a x 10</i>; debe ser <i>sumar a x −10</i>.',
  robit([[key('right arrow'), chx(10)], [key('left arrow'), chx(10)], [key('up arrow'), chy(10)], [key('down arrow'), chy(-10)]], size=60),
  robit([[key('right arrow'), chx(10)], [key('left arrow'), chx(-10)], [key('up arrow'), chy(10)], [key('down arrow'), chy(-10)]], size=60),
  ['Haz que Robit mire hacia donde camina.'])

# 5 ---------------------------------------------------------------------
E('error-05', 'El cuadrado que no cierra', 2, ['geometría', 'lápiz'],
  'Queríamos dibujar un cuadrado, pero sale una figura abierta y torcida.',
  ['¿Cuántos lados tiene un cuadrado? ¿Y cuánto mide cada esquina?', 'Compara esos números con los del programa.'],
  ['Una vuelta completa son 360 grados. Repartidos en 4 esquinas…'],
  'Giraba 80 grados en lugar de 90. Con 4 giros de 80 solo se completan 320 grados y la figura no se cierra.',
  Project(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), gotoxy(-50, -50), point(90), psize(3), pdown(), rep(4, move(100), turn(80)), pup()]])]),
  Project(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), gotoxy(-50, -50), point(90), psize(3), pdown(), rep(4, move(100), turn(90)), pup()]])]),
  ['¿Qué número hay que poner para un triángulo? ¿Y para un hexágono?'])

# 6 ---------------------------------------------------------------------
E('error-06', 'La cuenta atrás atascada', 2, ['variables', 'bucles'],
  'La nave debería contar 10, 9, 8… pero siempre dice 10.',
  ['Sigue el programa con el dedo, vuelta a vuelta. ¿Qué valor tiene <b>cuenta</b> en cada momento?', '¿Qué bloque se repite que no debería repetirse?'],
  ['Lo que va dentro del <i>repetir</i> ocurre en cada vuelta.'],
  'El bloque <i>dar a cuenta el valor 10</i> estaba dentro de la repetición, así que en cada vuelta volvía a valer 10. Debe ir antes del <i>repetir</i>.',
  Project(['espacio'], [Sprite('Nave', ['nave'], [[flag(), gotoxy(0, -130), rep(10, setv('cuenta', 10), say(v('cuenta'), 1), chv('cuenta', -1)), say('¡Despegue!', 1)]])],
          variables=['cuenta'], shown=['cuenta']),
  Project(['espacio'], [Sprite('Nave', ['nave'], [[flag(), gotoxy(0, -130), setv('cuenta', 10), rep(10, say(v('cuenta'), 1), chv('cuenta', -1)), say('¡Despegue!', 1)]])],
          variables=['cuenta'], shown=['cuenta']),
  ['Haz que la nave suba al terminar la cuenta.'])

# 7 ---------------------------------------------------------------------
E('error-07', 'Puntos de la partida anterior', 2, ['variables'],
  'Cada vez que empezamos una partida, el marcador sigue contando desde donde lo dejamos.',
  ['Juega dos partidas seguidas y mira el marcador al empezar.', '¿En algún momento se pone el marcador a cero?'],
  ['Las variables recuerdan su valor aunque pares el proyecto.'],
  'Faltaba <i>dar a puntos el valor 0</i> al pulsar la bandera verde.',
  Project(['blanco'], [Sprite('Estrella', ['estrella'], [[flag(), goto('_random_')], [clicked(), chv('puntos', 1), play('pop'), goto('_random_')]], sounds=['pop'])],
          variables=['puntos'], shown=['puntos']),
  Project(['blanco'], [Sprite('Estrella', ['estrella'], [[flag(), setv('puntos', 0), goto('_random_')], [clicked(), chv('puntos', 1), play('pop'), goto('_random_')]], sounds=['pop'])],
          variables=['puntos'], shown=['puntos']),
  ['Añade un récord que no se borre al empezar.'])

# 8 ---------------------------------------------------------------------
E('error-08', 'Robit boca abajo', 2, ['movimiento', 'dirección'],
  'Robit pasea de lado a lado, pero cuando rebota se pone boca abajo.',
  ['¿Hacia dónde apunta Robit después de rebotar?', 'Busca en Movimiento un bloque que controle cómo gira un objeto.'],
  ['Hay tres estilos: en todas direcciones, izquierda-derecha y no rotar.'],
  'Faltaba <i>fijar estilo de rotación a izquierda-derecha</i> antes del bucle.',
  robit([[flag(), forever(move(5), bounce(), nextc(), wait(0.1))]], size=70),
  robit([[flag(), rot('left-right'), forever(move(5), bounce(), nextc(), wait(0.1))]], size=70),
  ['¿Qué pasa con el estilo «no rotar»?'])

# 9 ---------------------------------------------------------------------
E('error-09', 'El mensaje perdido', 2, ['mensajes'],
  'Robit envía un mensaje a la estrella, pero la estrella nunca contesta.',
  ['Lee con atención el nombre del mensaje que se envía y el que se recibe.', '¿Son exactamente iguales?'],
  ['Para Scratch, una sola letra de diferencia ya es otro mensaje.'],
  'Robit enviaba «saludo» y la estrella esperaba «saludos». Los dos bloques deben usar el mismo mensaje.',
  Project(['noche'], [Sprite('Robit', ['robit1'], [[flag(), say('¡Hola, Estrella!', 2), send('saludo')]], x=-120, y=-60),
                      Sprite('Estrella', ['estrella'], [[recv('saludos'), say('¡Hola, Robit!', 2)]], x=120, y=80)]),
  Project(['noche'], [Sprite('Robit', ['robit1'], [[flag(), say('¡Hola, Estrella!', 2), send('saludo')]], x=-120, y=-60),
                      Sprite('Estrella', ['estrella'], [[recv('saludo'), say('¡Hola, Robit!', 2)]], x=120, y=80)]),
  ['Borra el mensaje que sobra desde el desplegable (Scratch lo quita solo al guardar si nadie lo usa).'])

# 10 --------------------------------------------------------------------
E('error-10', 'El juego que nunca acaba', 3, ['condicionales', 'operadores'],
  'Cada fallo resta 2 vidas. Empezamos con 3 y el juego debería acabar al quedarnos sin vidas… pero no acaba nunca.',
  ['Apunta el valor de <b>vidas</b> tras cada fallo: 3, …, …', '¿Llega a valer exactamente 0 alguna vez?'],
  ['Con <i>=</i> solo se cumple si el número es exactamente ese.', 'Prueba con <i>&lt;</i> (menor que).'],
  'Las vidas pasaban de 3 a 1 y de 1 a −1, sin pasar nunca por 0. La condición correcta es <i>vidas &lt; 1</i>.',
  robit([[flag(), setv('vidas', 3), say('Pulsa espacio para fallar', 2)],
         [key('space'), chv('vidas', -2), if_(eq(v('vidas'), 0), say('Fin del juego', 2), stop('all'))]]),
  robit([[flag(), setv('vidas', 3), say('Pulsa espacio para fallar', 2)],
         [key('space'), chv('vidas', -2), if_(lt(v('vidas'), 1), say('Fin del juego', 2), stop('all'))]]),
  ['¿Por qué es más seguro comprobar «menor que 1» que «igual a 0» en cualquier juego?'])
