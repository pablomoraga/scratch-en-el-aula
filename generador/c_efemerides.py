# -*- coding: utf-8 -*-
"""Talleres de una hora para fechas especiales del curso."""
from common import *
from c_talleres import taller

G = 'Efemérides'
PC = ['Un ordenador por pareja con Scratch (en línea o la aplicación).', 'Proyector para la demostración inicial.']
def T(n, *a, **k): taller(n, *a, group=G, label='Efeméride', **k)

# =========================================================== Halloween
T(1, 'efemeride-halloween', 'Halloween · Caza fantasmas en la casa encantada', '31 de octubre · desde 8 años',
  'Un juego de 30 segundos: los fantasmas aparecen y desaparecen por la casa encantada y hay que atraparlos con el ratón. Un murciélago cruza el cielo para dar ambiente.',
  PC,
  [('0-10', 'Demostración y reparto de papeles por pareja: quién programa la calabaza, quién los fantasmas.'),
   ('10-25', 'Fase 1: los fantasmas aparecen (clones) y se desvanecen.'),
   ('25-40', 'Fase 2: atraparlos con un clic y contar los puntos.'),
   ('40-50', 'Fase 3: la cuenta atrás de 30 segundos y el murciélago.'),
   ('50-60', 'Concurso: ¿quién caza más fantasmas?')],
  [('Fase 1 · Fantasmas que aparecen', ['El fantasma original se esconde y crea un clon cada medio segundo, más o menos.',
                                        'Cada clon va a un lugar al azar, aparece poco a poco (efecto desvanecer), flota un rato y se desvanece.']),
   ('Fase 2 · ¡Atrapado!', ['Al hacer clic en un clon: sumar 1 a <b>fantasmas</b>, sonar y eliminar el clon.']),
   ('Fase 3 · Tiempo y ambiente', ['La calabaza reinicia el cronómetro, avisa a los fantasmas con un mensaje y espera a que pasen 30 segundos.',
                                   'El murciélago cruza el cielo una y otra vez cambiando de disfraz para batir las alas.'])],
  Project(['casa_encantada'], [
      Sprite('Calabaza', ['calabaza'], [[flag(), setv('fantasmas', 0), gotoxy(-175, -135), say('¡Atrapa todos los fantasmas que puedas en 30 segundos!', 3),
                                         rtimer(), send('empieza'), until(gt(timer(), 30)), send('fin'), play('victoria'),
                                         say(join('¡Has cazado ', join(v('fantasmas'), ' fantasmas!')))]], size=150, sounds=['victoria']),
      Sprite('Fantasma', ['fantasma'], [[flag(), hide()], [recv('empieza'), rep_until(gt(timer(), 30), clone(), wait(rnd(0.4, 1)))],
                                        [as_clone(), goto('_random_'), seteffect('GHOST', 100), show(), rep(10, effect('GHOST', -8), wait(0.03)),
                                         rep(25, chx(rnd(-5, 5)), chy(rnd(-5, 5)), wait(0.05)), rep(10, effect('GHOST', 10), wait(0.03)), delclone()],
                                        [clicked(), chv('fantasmas', 1), play('pop'), delclone()], [recv('fin'), delclone()]], sounds=['pop']),
      Sprite('Murcielago', ['murcielago1', 'murcielago2'], [[flag(), forever(gotoxy(-235, rnd(60, 150)), rep(47, chx(10), chy(rnd(-3, 3)), nextc(), wait(0.06)), wait(rnd(1, 3)))]])],
      variables=['fantasmas'], shown=['fantasmas']),
  'Proyecta el juego y haz una ronda de «caza» con las parejas que quieran. Comentad qué hace que un juego sea más difícil: la velocidad, el tiempo, el tamaño de los fantasmas…',
  ['Primaria baja: sin clones; un solo fantasma que salta a otro sitio al atraparlo.',
   'ESO: fantasmas que se mueven más rápido según pasa el tiempo y una calabaza «trampa» que resta puntos.'])

# =========================================================== Navidad
T(2, 'efemeride-navidad', 'Navidad · Lluvia de regalos', 'Diciembre · desde 8 años',
  'Nieva sobre un pueblo de montaña, el árbol se ilumina y caen regalos que hay que recoger con el saco. Cada regalo atrapado toca una nota más aguda.',
  PC + ['Altavoces o auriculares (usa la extensión Música).'],
  [('0-10', 'Demostración. ¿Qué cosas se repiten en el proyecto? (la nieve, las luces, los regalos).'),
   ('10-25', 'Fase 1: la nieve con clones y las luces del árbol.'),
   ('25-40', 'Fase 2: el saco sigue al ratón y los regalos caen.'),
   ('40-50', 'Fase 3: puntos, música y tiempo.'),
   ('50-60', 'Personalización: tarjeta de felicitación con un mensaje propio.')],
  [('Fase 1 · Ambiente', ['El copo crea un clon cada 0,2 segundos; cada clon cae despacio desde arriba con un tamaño al azar y se elimina abajo.',
                          'El árbol cambia el efecto color cada medio segundo: parece que parpadean las luces.']),
   ('Fase 2 · El saco y los regalos', ['El saco, abajo, sigue la posición x del ratón.', 'El regalo cae desde una x al azar y vuelve arriba al tocar el suelo.']),
   ('Fase 3 · Puntos y música', ['Si el regalo toca el saco: sumar 1 a <b>regalos</b>, tocar la nota 60 + regalos y cambiar de disfraz.',
                                 'A los 30 segundos, el árbol felicita la Navidad y dice cuántos regalos hay.'])],
  Project(['nevado'], [
      Sprite('Arbol', ['arbol'], [[flag(), forever(effect('COLOR', 25), wait(0.5))], [recv('fin'), say(join('¡Feliz Navidad! Has recogido ', join(v('regalos'), ' regalos')))]],
             x=-170, y=-60, size=150),
      Sprite('Copo', ['copo'], [[flag(), hide(), forever(clone(), wait(0.2))],
                               [as_clone(), gotoxy(rnd(-240, 240), 180), setsize(rnd(60, 140)), show(), rep_until(lt(ypos(), -170), chy(-2), chx(rnd(-1, 1))), delclone()]]),
      Sprite('Saco', ['saco'], [[flag(), gotoxy(0, -140), front(), forever(setx(mx()))]]),
      Sprite('Regalo', ['regalo', 'regalo2'], [[flag(), setv('regalos', 0), instr(17), rtimer(), gotoxy(rnd(-200, 200), 180),
                                               rep_until(gt(timer(), 30), chy(-5),
                                                         if_(touching('Saco'), chv('regalos', 1), note(add(60, v('regalos')), 0.25), nextc(), gotoxy(rnd(-200, 200), 180)),
                                                         if_(lt(ypos(), -170), gotoxy(rnd(-200, 200), 180))),
                                               hide(), send('fin')]])],
      variables=['regalos'], shown=['regalos']),
  'Cada pareja cambia el mensaje del árbol por una felicitación propia y la presenta. Se puede exportar como tarjeta para las familias.',
  ['Primaria baja: dar hecha la nieve y trabajar solo el saco y los regalos.',
   'ESO: regalos de distinto valor (lista de puntos) y una melodía completa guardada en una lista.'])

# =========================================================== Día de la Paz
T(3, 'efemeride-paz', 'Día de la Paz · Palabras de paz por el mundo', '30 de enero · desde 9 años',
  'Robit dice la palabra «paz» en varios idiomas, en voz alta y por escrito, mientras las palomas cruzan el cielo. Cada paloma a la que haces clic deja un mensaje.',
  PC + ['Conexión a internet (extensiones Traducir y Texto a voz).', 'Altavoces.'],
  [('0-10', 'Conversación: ¿cómo se dice «paz» en las lenguas que conocemos en clase?'),
   ('10-25', 'Fase 1: las palomas vuelan (clones y dos disfraces).'),
   ('25-45', 'Fase 2: Robit traduce y lee «paz» en varios idiomas.'),
   ('45-55', 'Fase 3: cada paloma lleva un mensaje escrito por la pareja.'),
   ('55-60', 'Muestra conjunta en el proyector.')],
  [('Fase 1 · Palomas', ['La paloma original se esconde y crea un clon cada segundo.', 'Cada clon entra por la izquierda a una altura al azar y cruza batiendo las alas.']),
   ('Fase 2 · Paz en muchos idiomas', ['Con <i>fijar idioma a</i> elige la voz de cada idioma.', 'Con <i>traducir paz al …</i> obtén la palabra y muéstrala y léela.']),
   ('Fase 3 · Mensajes', ['Al hacer clic en una paloma, dice un mensaje de paz escrito por vosotros.'])],
  Project(['cielo'], [
      Sprite('Robit', ['robit1', 'robit2', 'robit3'], [[flag(), costume('robit2'), lang('es'), say('La palabra PAZ en muchos idiomas'), speak('paz')] +
                                                      sum([[lang(l), say(join(n, translate('paz', l))), speak(translate('paz', l)), wait(0.5)]
                                                           for l, n in [('en', 'Inglés: '), ('fr', 'Francés: '), ('de', 'Alemán: '), ('it', 'Italiano: ')]], []) +
                                                      [costume('robit3'), say('Haz clic en las palomas')]], x=-150, y=-90, size=70),
      Sprite('Paloma', ['paloma1', 'paloma2'], [[flag(), hide(), forever(clone(), wait(1))],
                                                [as_clone(), gotoxy(-235, rnd(-60, 150)), show(), rep_until(gt(xpos(), 230), chx(3), nextc(), wait(0.1)), delclone()],
                                                [clicked(), say('¡Convivir en paz es cosa de todos!', 2)]]),
      Sprite('Corazon', ['corazon'], [[flag(), forever(rep(5, size(4), wait(0.05)), rep(5, size(-4), wait(0.05)))]], x=170, y=-120, size=200)]),
  'Cada pareja lee en voz alta el mensaje de sus palomas. Se puede unir todo en un estudio de Scratch de la clase o del centro.',
  ['Primaria baja: sin traducción; Robit dice mensajes escritos por la clase.',
   'ESO: preguntar el idioma con <i>preguntar</i> y guardar los mensajes de toda la clase en una lista.'])

# =========================================================== Carnaval
def accesorio(nombre, cos, home, puesto, talla):
    hx, hy = home; px_, py_ = puesto
    return Sprite(nombre, [cos], [[flag(), gotoxy(hx, hy), setsize(80), front()],
                                  [clicked(), ifelse(lt(ypos(), -100), [setsize(talla), glide(0.4, px_, py_), front(), play('pop')],
                                                     [setsize(80), glide(0.4, hx, hy)])]], x=hx, y=hy, size=80, sounds=['pop'])
T(4, 'efemeride-carnaval', 'Carnaval · Disfraza a Robit', 'Febrero · desde 6 años',
  'Un probador de disfraces: haces clic en un gorro, unas gafas o un antifaz y se colocan sobre Robit. Con teclas cambia de color y baila.',
  PC,
  [('0-10', 'Demostración y lluvia de ideas de disfraces.'),
   ('10-25', 'Fase 1: cada accesorio va y vuelve con un clic.'),
   ('25-40', 'Fase 2: dibujar accesorios propios en el editor de disfraces.'),
   ('40-50', 'Fase 3: Robit cambia de color y baila.'),
   ('50-60', 'Desfile de carnaval en el proyector.')],
  [('Fase 1 · Probador', ['Cada accesorio empieza abajo, pequeño.', 'Al hacer clic: si está abajo, crece y se desliza hasta su sitio sobre Robit; si no, vuelve abajo.']),
   ('Fase 2 · Accesorios propios', ['Pinta un objeto nuevo (pelucas, narices, bigotes…) y copia el programa de otro accesorio.']),
   ('Fase 3 · Fiesta', ['Tecla <b>c</b>: Robit cambia de color. Tecla <b>espacio</b>: Robit baila cambiando de disfraz.'])],
  Project(['teatro'], [
      Sprite('Robit', ['robit1', 'robit2', 'robit3'], [[flag(), gotoxy(0, -20), cleareff(), costume('robit1'), say('Haz clic en los objetos para disfrazarme', 3)],
                                                      [key('c'), effect('COLOR', 25)], [key('space'), rep(6, nextc(), wait(0.2)), costume('robit1')]], x=0, y=-20, size=200),
      accesorio('Gorro', 'gorro', (-150, -145), (0, 100), 150),
      accesorio('Gafas', 'gafas', (0, -145), (0, 20), 150),
      accesorio('Antifaz', 'careta', (150, -145), (0, 20), 150)]),
  'Desfile: cada pareja enseña su Robit disfrazado y explica cómo ha programado un accesorio nuevo.',
  ['Primaria baja: dar los accesorios programados y que solo dibujen nuevos.',
   'ESO: guardar el disfraz elegido en variables y crear un botón de «foto» que use <i>sellar</i>.'])

# =========================================================== Día de Andalucía
PROV = ['Almería', 'Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla']
SIN = ['Almeria', 'Cadiz', 'Cordoba', 'Granada', 'Huelva', 'Jaen', 'Malaga', 'Sevilla']
def franja(color, y0):
    return [pcolor(color), setv('y', y0), rep(4, gotoxy(-150, v('y')), pdown(), setx(150), pup(), chv('y', -10))]
T(5, 'efemeride-andalucia', 'Día de Andalucía · Bandera y provincias', '28 de febrero · desde 8 años',
  'El lápiz dibuja la bandera de Andalucía (verde, blanca y verde) y después Robit propone un reto: escribir las ocho provincias andaluzas, con o sin tilde.',
  PC,
  [('0-10', '¿Qué sabemos de Andalucía? Colores de la bandera, provincias, capital.'),
   ('10-25', 'Fase 1: dibujar la bandera con el lápiz.'),
   ('25-45', 'Fase 2: el juego de las provincias con listas.'),
   ('45-55', 'Fase 3: evitar repeticiones y celebrar al completar las ocho.'),
   ('55-60', 'Ronda rápida: ¿quién completa las ocho antes?')],
  [('Fase 1 · La bandera', ['La bandera tiene tres franjas horizontales iguales: verde, blanca y verde.',
                            'Con tamaño de lápiz 10, cada franja son 4 líneas horizontales. Al final, un borde fino.']),
   ('Fase 2 · Las provincias', ['Crea la lista <b>provincias</b> con las ocho y la lista <b>sin tildes</b> con los mismos nombres sin tilde, en el mismo orden.',
                                'Pregunta una provincia y busca su número con <i># de elemento de … en …</i> en las dos listas.']),
   ('Fase 3 · Sin repetir', ['Si se encuentra, guarda el nombre correcto en la lista <b>encontradas</b>, solo si no estaba ya.',
                             'Al llegar a 8 puntos, Robit felicita el Día de Andalucía.'])],
  Project(['blanco'], [
      Sprite('Lapiz', ['punto'], [[flag(), hide(), pclear()], [recv('dibuja'), psize(10)] + franja('#007a33', 145) + franja('#ffffff', 105) + franja('#007a33', 65) +
                                  [psize(2), pcolor('#555555'), gotoxy(-155, 150), pdown(), setx(155), sety(30), setx(-155), sety(150), pup()]]),
      Sprite('Robit', ['robit1', 'robit2', 'robit3'], [[flag(), costume('robit1'), say('Vamos a dibujar la bandera de Andalucía', 2), sendw('dibuja'),
                                                      lclear('provincias'), lclear('sin tildes'), lclear('encontradas')] +
                                                     [ladd(p, 'provincias') for p in PROV] + [ladd(p, 'sin tildes') for p in SIN] +
                                                     [setv('puntos', 0), say('Ahora, ¿te sabes las 8 provincias?', 2),
                                                      rep_until(eq(v('puntos'), 8),
                                                                ask('Escribe una provincia de Andalucía'),
                                                                setv('n', litemnum(answer(), 'provincias')),
                                                                if_(eq(v('n'), 0), setv('n', litemnum(answer(), 'sin tildes'))),
                                                                ifelse(eq(v('n'), 0), [play('error'), say('Esa no es una provincia andaluza', 1)],
                                                                       [ifelse(lcontains('encontradas', litem(v('n'), 'provincias')), [say('¡Esa ya la has dicho!', 1)],
                                                                               [ladd(litem(v('n'), 'provincias'), 'encontradas'), chv('puntos', 1), play('ding'),
                                                                                say(join('¡Sí! ', litem(v('n'), 'provincias')), 1)])])),
                                                      costume('robit3'), play('victoria'), say('¡Las 8! Feliz Día de Andalucía, 28 de febrero', 4)]],
             x=0, y=-110, size=70, sounds=['ding', 'error', 'victoria'])],
      variables=['puntos', 'y', 'n'], lists=['provincias', 'sin tildes', 'encontradas'], shown=['puntos']),
  'Comprobad que la lista <b>encontradas</b> tiene las ocho provincias bien escritas, con sus tildes. Buen momento para hablar de por qué el ordenador necesita las dos listas.',
  ['Primaria baja: solo la bandera, y después un dibujo libre con el lápiz.',
   'ESO: añadir capitales o comarcas, o preguntar datos (el 28 de febrero se celebra el referéndum de autonomía de 1980).'])

# =========================================================== Día del Libro
T(6, 'efemeride-libro', 'Día del Libro · Elige tu propia aventura', '23 de abril · desde 8 años',
  'Robit encuentra un libro mágico que le lleva a otro mundo. Quien juega decide el camino escribiendo sus respuestas, y cada decisión cambia el escenario y el final.',
  PC,
  [('0-10', 'Lectura de un fragmento de un libro de aventuras y presentación del reto.'),
   ('10-20', 'Fase 1: el libro se abre y empieza la historia.'),
   ('20-40', 'Fase 2: decisiones con <i>preguntar</i> y <i>si… si no</i>.'),
   ('40-55', 'Fase 3: escribir un final propio.'),
   ('55-60', 'Intercambio: cada pareja juega la aventura de otra.')],
  [('Fase 1 · El libro mágico', ['El libro aparece cerrado, cambia al disfraz abierto y envía «empieza».']),
   ('Fase 2 · Decisiones', ['Robit pregunta «¿castillo o bosque?» y, según la respuesta, cambia el fondo y continúa la historia.',
                            'Dentro de cada camino hay otra pregunta con dos finales.']),
   ('Fase 3 · Tu final', ['Cambia los textos y añade un tercer camino con otro fondo.'])],
  Project(['blanco', 'castillo', 'bosque', 'noche', 'mar', 'espacio'], [
      Sprite('Libro', ['libro', 'libro_abierto'], [[flag(), show(), costume('libro'), gotoxy(0, 0), setsize(200), wait(1), costume('libro_abierto'),
                                                   play('ding'), wait(1), hide(), send('empieza')]], sounds=['ding']),
      Sprite('Robit', ['robit1', 'robit2', 'robit3'], [[flag(), hide(), backdrop('blanco')],
          [recv('empieza'), show(), gotoxy(0, -90), say('¡El libro me ha traído a otro mundo!', 2),
           ask('¿Voy al castillo o al bosque? (castillo / bosque)'),
           ifelse(eq(answer(), 'castillo'),
                  [backdrop('castillo'), say('Un castillo con dos puertas…', 2), ask('¿Abro la puerta grande o la pequeña? (grande / pequeña)'),
                   ifelse(eq(answer(), 'grande'), [backdrop('noche'), costume('robit3'), say('FINAL: una biblioteca infinita. Me quedo a leer para siempre.', 4)],
                          [backdrop('mar'), say('FINAL: un pasadizo secreto me lleva hasta el mar.', 4)])],
                  [backdrop('bosque'), say('El bosque tiene dos caminos…', 2), ask('¿Sigo las estrellas o el río? (estrellas / río)'),
                   ifelse(eq(answer(), 'estrellas'), [backdrop('espacio'), costume('robit3'), say('FINAL: ¡viajo al espacio en un cohete de papel!', 4)],
                          [backdrop('mar'), say('FINAL: el río me lleva a una playa llena de libros.', 4)])])]], size=70)]),
  'Cada pareja juega la aventura de otra y cuenta qué final le ha tocado. Se puede relacionar con un libro leído en clase.',
  ['Primaria baja: una sola decisión con dos finales.',
   'ESO: llevar la cuenta de decisiones en variables (valor, curiosidad) y que el final dependa de ellas.'])

# =========================================================== Medio ambiente
def residuo(nombre, cos, bueno, x, y):
    otros = [b for b in ('Amarillo', 'Azul', 'Verde') if b != bueno]
    return Sprite(nombre, [cos], [[flag(), show(), gotoxy(x, y), forever(
        until(and_(mousedown(), touching('_mouse_'))),
        rep_until(not_(mousedown()), goto('_mouse_')),
        ifelse(touching(bueno), [chv('reciclados', 1), play('ding'), hide(), stop('this script')],
               [if_(or_(touching(otros[0]), touching(otros[1])), play('error'), say('¡Ese no es su contenedor!', 1)), glide(0.3, x, y)]))]],
        x=x, y=y, size=150, sounds=['ding', 'error'])
T(7, 'efemeride-medio-ambiente', 'Día del Medio Ambiente · Recicla con Robit', '5 de junio · desde 6 años',
  'Hay que arrastrar cada residuo a su contenedor: amarillo para envases de plástico, latas y briks; azul para papel y cartón; verde para vidrio. Si te equivocas, el residuo vuelve a su sitio.',
  PC,
  [('0-10', '¿Qué va en cada contenedor? Repaso con objetos reales o fotos.'),
   ('10-25', 'Fase 1: arrastrar un residuo con el ratón.'),
   ('25-40', 'Fase 2: comprobar si cae en el contenedor correcto.'),
   ('40-50', 'Fase 3: contar los reciclados y celebrar al terminar.'),
   ('50-60', 'Ampliación: añadir residuos nuevos (y el contenedor marrón de orgánico).')],
  [('Fase 1 · Arrastrar', ['Por siempre: esperar a que se pulse el ratón sobre el residuo; mientras siga pulsado, ir al puntero del ratón.']),
   ('Fase 2 · ¿Contenedor correcto?', ['Al soltar: si toca su contenedor, suma 1 a <b>reciclados</b> y se esconde.',
                                       'Si toca otro contenedor, avisa del error y vuelve a su sitio.']),
   ('Fase 3 · ¡Todo reciclado!', ['Robit espera a que <b>reciclados</b> valga 5 y felicita.'])],
  Project(['cielo'], [
      Sprite('Amarillo', ['contenedor_amarillo'], [], x=-160, y=-110, size=130),
      Sprite('Azul', ['contenedor_azul'], [], x=0, y=-110, size=130),
      Sprite('Verde', ['contenedor_verde'], [], x=160, y=-110, size=130),
      residuo('Botella', 'botella', 'Amarillo', -190, 60), residuo('Lata', 'lata', 'Amarillo', -100, 100),
      residuo('Periodico', 'periodico', 'Azul', 0, 60), residuo('Caja', 'caja', 'Azul', 100, 110), residuo('Tarro', 'tarro', 'Verde', 190, 60),
      Sprite('Robit', ['robit1', 'robit2', 'robit3'], [[flag(), setv('reciclados', 0), costume('robit2'),
                                                      say('Amarillo: envases, latas y briks. Azul: papel y cartón. Verde: vidrio.', 4), say(''),
                                                      until(eq(v('reciclados'), 5)), costume('robit3'), play('victoria'), say('¡Todo reciclado! ¡Gracias por cuidar el planeta!')]],
             x=-215, y=150, size=45, sounds=['victoria'])],
      variables=['reciclados'], shown=['reciclados']),
  'Revisad entre todos en qué contenedor va cada residuo y por qué. Se puede añadir el contenedor marrón (orgánico) y el punto limpio como ampliación.',
  ['Primaria baja: solo dos contenedores y tres residuos.',
   'ESO: residuos que aparecen al azar desde una lista, cronómetro y récord.'])

# =========================================================== Verano
T(8, 'efemeride-verano', 'Fin de curso · Surf de verano', 'Junio · desde 8 años',
  'Robit hace surf: sube y baja con las flechas para recoger conchas y esquivar medusas durante 40 segundos. ¡Feliz verano!',
  PC,
  [('0-10', 'Demostración y repaso de clones (lo vimos en otros retos).'),
   ('10-25', 'Fase 1: la tabla se mueve con las flechas y Robit va encima.'),
   ('25-40', 'Fase 2: medusas y conchas que llegan desde la derecha (clones).'),
   ('40-50', 'Fase 3: puntos, vidas y tiempo.'),
   ('50-60', 'Campeonato de surf y despedida del curso.')],
  [('Fase 1 · Surfear', ['La tabla sube y baja con las flechas, sin salirse del mar (entre y = −100 e y = 0).', 'Robit va siempre a la tabla y un poco más arriba.']),
   ('Fase 2 · Olas de cosas', ['Medusas y conchas crean clones que aparecen por la derecha a una altura al azar y avanzan hacia la izquierda.']),
   ('Fase 3 · Puntos y vidas', ['Concha que toca la tabla: +1 punto. Medusa que toca la tabla: −1 vida.', 'Termina a los 40 segundos o al quedarse sin vidas.'])],
  Project(['playa'], [
      Sprite('Tabla', ['tabla'], [[flag(), gotoxy(-150, -50), setv('conchas', 0), setv('vidas', 3), rtimer(),
                                   rep_until(or_(gt(timer(), 40), lt(v('vidas'), 1)),
                                             if_(and_(keyp('up arrow'), lt(ypos(), 0)), chy(4)),
                                             if_(and_(keyp('down arrow'), gt(ypos(), -100)), chy(-4))),
                                   send('fin')]], x=-150, y=-50),
      Sprite('Robit', ['robit1', 'robit2', 'robit3'], [[flag(), costume('robit2'), forever(goto('Tabla'), chy(30))],
                                                      [recv('fin'), costume('robit3'), say(join('¡Feliz verano! Conchas: ', v('conchas')))]], size=45),
      Sprite('Medusa', ['medusa'], [[flag(), hide(), rep_until(gt(timer(), 38), wait(rnd(1, 2)), clone())],
                                    [as_clone(), gotoxy(235, rnd(-90, 10)), show(), rep_until(lt(xpos(), -235), chx(-5),
                                     if_(touching('Tabla'), chv('vidas', -1), play('error'), delclone())), delclone()], [recv('fin'), delclone()]], sounds=['error']),
      Sprite('Concha', ['concha'], [[flag(), hide(), rep_until(gt(timer(), 38), wait(rnd(0.8, 1.6)), clone())],
                                    [as_clone(), gotoxy(235, rnd(-90, 10)), show(), rep_until(lt(xpos(), -235), chx(-4),
                                     if_(touching('Tabla'), chv('conchas', 1), play('pop'), delclone())), delclone()], [recv('fin'), delclone()]], sounds=['pop'])],
      variables=['conchas', 'vidas'], shown=['conchas', 'vidas']),
  'Campeonato rápido en el proyector y foto de grupo con Robit celebrando el fin de curso.',
  ['Primaria baja: sin medusas; solo recoger conchas.',
   'ESO: velocidad creciente, vidas extra con un salvavidas y récord guardado.'])
