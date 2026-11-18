# -*- coding: utf-8 -*-
from common import *

SEC = 'comenzamos'
def robi(scripts, back=('blanco',), **kw):
    return Project(list(back), [Sprite('Robit', ['robit1', 'robit2'], scripts, **kw)])
n = [0]
def R(*a, **k):
    n[0] += 1
    reto(SEC, '%02d' % n[0], 'reto-%02d' % n[0], *a, **k)

R('¡Hola, Robit!', 1, '10 min', ['secuencia', 'eventos'],
  'Que Robit se presente al pulsar la bandera verde.',
  ['Empieza con el bloque <i>al hacer clic en ⚑</i> (Eventos).', 'Añade un bloque para que Robit diga «¡Hola!» durante 2 segundos.',
   'Después, que piense algo y que diga cómo se llama.', 'Pulsa la bandera verde para probarlo.'],
  ['Los bloques de hablar y pensar están en <b>Apariencia</b>.', 'Usa los que llevan «durante … segundos»: si no, los mensajes se pisan.'],
  robi([[flag(), say('¡Hola!', 2), think('¿Qué digo ahora?', 2), say('Me llamo Robit', 2)]]),
  ['Haz que Robit cuente un chiste en tres partes.', 'Añade un segundo personaje que le conteste (usa <i>esperar</i> para dar turnos).'])

R('Robit camina', 1, '15 min', ['bucles', 'animación'],
  'Hacer que Robit cruce el escenario moviendo las piernas.',
  ['Al pulsar la bandera, coloca a Robit a la izquierda (x: −180, y: 0).', 'Repite 30 veces: mover 10 pasos, cambiar al siguiente disfraz y esperar un poco.',
   'Prueba con distintos tiempos de espera.'],
  ['El bloque <i>repetir</i> está en Control.', 'Con <i>esperar 0.1 segundos</i> la animación queda natural.'],
  robi([[flag(), gotoxy(-180, 0), rep(30, move(10), nextc(), wait(0.1))]]),
  ['Haz que al llegar diga «¡Llegué!».', '¿Puedes hacer que vuelva andando hacia atrás?'])

R('Rebota sin parar', 1, '10 min', ['bucles', 'movimiento'],
  'Que una pelota se mueva sola y rebote en los bordes para siempre.',
  ['Usa <i>por siempre</i> con <i>mover</i> y <i>si toca un borde, rebotar</i>.', 'Al empezar, haz que apunte en una dirección inclinada (por ejemplo, 45).',
   'Cambia el número de pasos para ir más rápido o más lento.'],
  ['Si apunta a 90 solo irá de lado a lado: prueba otros ángulos.'],
  Project(['blanco'], [Sprite('Pelota', ['pelota'], [[flag(), gotoxy(0, 0), point(45), forever(move(6), bounce())]])]),
  ['Añade una segunda pelota con otra velocidad.', 'Haz que la pelota cambie de color en cada rebote… ¡o siempre!'])

R('Muévete con las flechas', 1, '15 min', ['eventos', 'coordenadas'],
  'Mover a Robit por el escenario con las cuatro flechas del teclado.',
  ['Crea cuatro programas, uno por flecha, con <i>al presionar tecla</i>.', 'Derecha e izquierda cambian x; arriba y abajo cambian y.',
   'Usa 10 para avanzar y −10 para retroceder.'],
  ['<i>sumar a x 10</i> mueve a la derecha; <i>sumar a x −10</i>, a la izquierda.'],
  robi([[key('right arrow'), chx(10)], [key('left arrow'), chx(-10)], [key('up arrow'), chy(10)], [key('down arrow'), chy(-10)]], size=60),
  ['Que cambie de disfraz con cada paso.', 'Pon un fondo y un objetivo al que llegar.'])

R('Dibuja un cuadrado', 1, '15 min', ['bucles', 'lápiz', 'geometría'],
  'Dibujar un cuadrado con la extensión Lápiz.',
  ['Añade la extensión <b>Lápiz</b>.', 'Al empezar: borra todo, coloca el objeto y baja el lápiz.',
   'Un cuadrado es: avanzar y girar 90 grados, cuatro veces.', 'Sube el lápiz al terminar.'],
  ['Mete <i>mover 100 pasos</i> y <i>girar 90 grados</i> dentro de <i>repetir 4</i>.'],
  Project(['blanco'], [Sprite('Lapiz', ['punto'], [[flag(), pclear(), gotoxy(-50, -50), point(90), psize(3), pdown(), rep(4, move(100), turn(90)), pup()]])]),
  ['¿Y un triángulo? (pista: gira 120).', '¿Y un hexágono? ¿Qué relación hay entre los lados y los grados?'])

R('Cambia de escenario', 1, '10 min', ['eventos', 'fondos'],
  'Hacer un pequeño viaje por tres fondos distintos con un clic.',
  ['Añade varios fondos al escenario.', 'Programa a Robit: al hacer clic en él, siguiente fondo.',
   'Haz que diga algo distinto cuando el fondo cambie a cada uno.'],
  ['El bloque <i>cuando el fondo cambie a</i> está en Eventos.'],
  Project(['cielo', 'mar', 'espacio'], [Sprite('Robit', ['robit1'], [[flag(), backdrop('cielo'), say('Haz clic en mí para viajar')],
                                                                 [clicked(), nextb()],
                                                                 [onbackdrop('cielo'), say('¡Qué buen día!', 2)],
                                                                 [onbackdrop('mar'), say('¡Cuánta agua!', 2)],
                                                                 [onbackdrop('espacio'), say('¡Estoy en el espacio!', 2)]])]),
  ['Dibuja tu propio fondo.', 'Haz que el tamaño de Robit cambie en cada lugar.'])

R('Teletransporte', 1, '10 min', ['eventos', 'azar'],
  'Que una estrella salte a un lugar al azar cada vez que la toques.',
  ['Al hacer clic en la estrella: ir a posición aleatoria.', 'Añade un sonido para que sea más divertido.'],
  ['<i>ir a posición aleatoria</i> está en Movimiento.'],
  Project(['espacio'], [Sprite('Estrella', ['estrella'], [[clicked(), play('pop'), goto('_random_')]], sounds=['pop'])]),
  ['Que diga «¡Atrápame!» al saltar.', 'Que salte sola cada segundo y tú intentes tocarla.'])

R('Persigue al ratón', 1, '10 min', ['bucles', 'sensores'],
  'Un pez que sigue al puntero del ratón por el mar.',
  ['Por siempre: apuntar hacia el puntero del ratón y mover unos pasos.', 'Fija el estilo de rotación para que no se ponga boca abajo.'],
  ['Si tiembla al llegar al ratón, añade una condición: mover solo si la distancia al ratón es mayor que 10.'],
  Project(['mar'], [Sprite('Pez', ['pez'], [[flag(), rot('left-right'), forever(towards('_mouse_'), if_(gt(dist('_mouse_'), 10), move(4)))]], direction=-90)]),
  ['Añade otro pez más lento.', 'Haz que el pez diga «¡Ñam!» cuando toque el ratón.'])

R('Colores locos', 1, '10 min', ['bucles', 'efectos'],
  'Que un objeto cambie de color sin parar y vuelva a la normalidad al hacer clic.',
  ['Por siempre: sumar al efecto color 5 y esperar un poquito.', 'Al hacer clic en el objeto: quitar efectos gráficos.'],
  ['Los efectos están en Apariencia. Desde el desplegable puedes elegir otros.'],
  robi([[flag(), cleareff(), forever(effect('COLOR', 5), wait(0.05))], [clicked(), cleareff()]]),
  ['Prueba los efectos remolino y ojo de pez.', 'Usa una tecla para cada efecto.'])

R('Crece y encoge', 1, '10 min', ['eventos', 'tamaño'],
  'Agrandar y encoger a Robit con dos teclas, y volver a su tamaño con otra.',
  ['Tecla <b>a</b>: cambiar tamaño por 10. Tecla <b>z</b>: cambiar tamaño por −10.', 'Tecla <b>espacio</b>: fijar tamaño al 100 %.'],
  ['Hay un límite: Scratch no deja que un objeto sea infinitamente grande o pequeño.'],
  robi([[key('a'), size(10)], [key('z'), size(-10)], [key('space'), setsize(100)]]),
  ['Que diga su tamaño (bloque reportero <i>tamaño</i>).', 'Que crezca poco a poco con una repetición.'])

R('Una conversación', 2, '20 min', ['mensajes', 'paralelismo'],
  'Dos personajes que hablan por turnos usando mensajes.',
  ['Crea dos objetos: Robit y la Estrella.', 'Robit saluda y <b>envía</b> un mensaje «turno estrella».',
   'La Estrella, <b>al recibir</b> ese mensaje, contesta y envía «turno robi».', 'Robit responde al recibirlo.'],
  ['Crea los mensajes desde el desplegable de <i>enviar</i> › <i>Nuevo mensaje</i>.'],
  Project(['noche'], [Sprite('Robit', ['robit1'], [[flag(), say('Hola, Estrella. ¿Qué haces?', 2), send('turno estrella')],
                                                  [recv('turno robi'), say('¡Qué bonito! Yo también quiero brillar', 2)]], x=-120, y=-60),
                      Sprite('Estrella', ['estrella'], [[recv('turno estrella'), say('Estoy brillando para ti', 2), send('turno robi')]], x=120, y=80)]),
  ['Alarga la conversación con más mensajes.', 'Que la estrella gire cuando habla.'])

R('El preguntón', 2, '15 min', ['sensores', 'operadores'],
  'Que Robit te pregunte el nombre y te salude.',
  ['Usa <i>preguntar … y esperar</i>.', 'Con <i>unir</i> forma la frase «Hola, » + respuesta.', 'Pregunta también la edad y comenta algo.'],
  ['Puedes meter un <i>unir</i> dentro de otro para juntar tres textos.'],
  robi([[flag(), ask('¿Cómo te llamas?'), say(join('¡Hola, ', join(answer(), '!')), 2), ask('¿Cuál es tu color favorito?'),
         say(join('El ', join(answer(), ' es precioso')), 2)]]),
  ['Haz una entrevista con 5 preguntas.', 'Guarda el nombre en una variable para usarlo al final.'])

R('Cuenta atrás', 2, '15 min', ['variables', 'bucles'],
  'Una cuenta atrás del 10 al 0 para lanzar un cohete.',
  ['Crea la variable <b>cuenta</b>.', 'Al empezar, dale el valor 10.', 'Repite 10 veces: decir la cuenta 1 segundo y sumarle −1.',
   'Al final, que la nave despegue hacia arriba.'],
  ['Mete el reportero <i>cuenta</i> dentro del bloque <i>decir</i>.'],
  Project(['espacio'], [Sprite('Nave', ['nave'], [[flag(), gotoxy(0, -130), setv('cuenta', 10), rep(10, say(v('cuenta'), 1), chv('cuenta', -1)),
                                                   say('¡Despegue!', 1), rep(40, chy(8))]])], variables=['cuenta'], shown=['cuenta']),
  ['Usa <i>repetir hasta que cuenta = 0</i> en vez de repetir 10.', 'Añade sonido en cada número.'])

R('Contador de clics', 2, '10 min', ['variables', 'eventos'],
  '¿Cuántas veces eres capaz de hacer clic en el botón?',
  ['Crea la variable <b>clics</b> y ponla a 0 al empezar.', 'Al hacer clic en el botón: sumar 1 y hacer un pequeño efecto.'],
  ['Para el efecto: encoge un poco el botón y vuelve a su tamaño.'],
  Project(['blanco'], [Sprite('Boton', ['boton'], [[flag(), setv('clics', 0), setsize(100)],
                                                   [clicked(), chv('clics', 1), play('pop'), setsize(90), wait(0.05), setsize(100)]], sounds=['pop'])],
          variables=['clics'], shown=['clics']),
  ['Añade el cronómetro y para el juego a los 10 segundos.', 'Que el botón felicite al llegar a 50 clics.'])

R('Lanza el dado', 2, '10 min', ['operadores', 'azar'],
  'Un dado que da un número del 1 al 6 al hacer clic.',
  ['Al hacer clic en Robit: guarda en la variable <b>dado</b> un número aleatorio entre 1 y 6.', 'Haz que lo diga.', 'Si sale 6, que lo celebre.'],
  ['Para comparar usa el bloque verde <i>=</i> dentro de <i>si … entonces</i>.'],
  robi([[clicked(), think('Lanzando...', 1), setv('dado', rnd(1, 6)), say(join('Ha salido un ', v('dado')), 2),
         if_(eq(v('dado'), 6), say('¡Un seis!', 1), rep(2, turn(180)))]]),
  ['Haz un dado de 20 caras.', 'Lanza dos dados y suma.'])

R('Cielo de estrellas', 2, '15 min', ['lápiz', 'azar'],
  'Llenar el cielo de estrellas de distintos tamaños usando el bloque <i>sellar</i>.',
  ['Añade la extensión Lápiz.', 'Al empezar, borra todo.', 'Repite 30 veces: ir a una posición aleatoria, tamaño aleatorio y sellar.'],
  ['<i>sellar</i> deja una copia del objeto dibujada en el fondo.'],
  Project(['noche'], [Sprite('Estrella', ['estrella'], [[flag(), pclear(), rep(30, goto('_random_'), setsize(rnd(20, 80)),
                                                                                  seteffect('COLOR', rnd(0, 100)), stamp())]])]),
  ['Haz que cada estrella aparezca con un sonido.', 'Sella en forma de círculo usando <i>mover</i> y <i>girar</i>.'])

R('Mi instrumento', 2, '15 min', ['eventos', 'sonido'],
  'Convertir el teclado en un instrumento con tres sonidos.',
  ['Programa las teclas 1, 2 y 3 para que suene un sonido distinto.', 'Que el tambor «salte» un poco cada vez que suena.'],
  ['Usa <i>iniciar sonido</i> para poder tocar rápido.'],
  Project(['blanco'], [Sprite('Tambor', ['tambor'], [[key('1'), play('pop'), chy(10), wait(0.1), chy(-10)],
                                                     [key('2'), play('ding'), chy(10), wait(0.1), chy(-10)],
                                                     [key('3'), play('boing'), chy(10), wait(0.1), chy(-10)]], sounds=['pop', 'ding', 'boing'])]),
  ['Graba tus propios sonidos con el micrófono.', 'Usa la extensión Música para tocar notas de verdad.'])

R('¡Ay, el borde!', 2, '15 min', ['condicionales', 'sensores'],
  'Mover a Robit con las flechas y que se queje si toca el borde.',
  ['Mueve con las flechas, como en el reto 4, pero dentro de un <i>por siempre</i> con <i>¿tecla presionada?</i>.',
   'Añade: si toca el borde, decir «¡Ay!» y volver al centro.'],
  ['<i>¿tocando borde?</i> está en Sensores; elige «borde» en el desplegable.'],
  robi([[flag(), gotoxy(0, 0), forever(if_(keyp('right arrow'), chx(5)), if_(keyp('left arrow'), chx(-5)),
                                        if_(keyp('up arrow'), chy(5)), if_(keyp('down arrow'), chy(-5)),
                                        if_(touching('_edge_'), say('¡Ay!', 1), gotoxy(0, 0)))]], size=50),
  ['Pon un objeto peligroso en medio.', 'Cuenta las veces que tocas el borde.'])

R('Carrera de caracoles', 2, '15 min', ['paralelismo', 'azar'],
  'Dos corredores que deslizan hasta la meta a velocidades al azar.',
  ['Crea dos objetos, uno arriba y otro abajo, a la izquierda.', 'Al pulsar la bandera, cada uno se desliza hasta x: 200 en un tiempo aleatorio.',
   'El que llegue diga «¡Llegué!».'],
  ['El tiempo del bloque <i>deslizar</i> puede ser un <i>número aleatorio entre 2 y 6</i>.'],
  Project(['campo'], [Sprite('Robit', ['robit1'], [[flag(), gotoxy(-200, 80), glide(rnd(2, 6), 200, 80), say('¡Llegué!', 2)]], size=60),
                      Sprite('Coche', ['coche'], [[flag(), gotoxy(-200, -80), glide(rnd(2, 6), 200, -80), say('¡Llegué!', 2)]])]),
  ['Añade una cuenta atrás antes de salir.', 'Usa el cronómetro para saber cuánto tarda cada uno.'])

R('El fantasma', 2, '15 min', ['efectos', 'bucles'],
  'Un fantasma que aparece y desaparece poco a poco, y se esconde si lo tocas.',
  ['Repite 10 veces: sumar al efecto desvanecer 10 (desaparece).', 'Ve a otro sitio y repite con −10 (aparece).',
   'Mete todo en un <i>por siempre</i>.', 'Al hacer clic en él: decir «¡Buuu!».'],
  ['El efecto desvanecer a 100 lo hace invisible; a 0, totalmente visible.'],
  Project(['noche'], [Sprite('Fantasma', ['fantasma'], [[flag(), cleareff(), forever(rep(10, effect('GHOST', 10), wait(0.05)), goto('_random_'),
                                                                                 rep(10, effect('GHOST', -10), wait(0.05)), wait(1))],
                                                        [clicked(), say('¡Buuu!', 1)]])]),
  ['Cuenta cuántas veces consigues tocarlo.', 'Que aparezcan varios fantasmas con clones.'])
