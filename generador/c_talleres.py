# -*- coding: utf-8 -*-
from common import *

SEC = 'talleres'

def guion(rows):
    return ('<table class="tabla"><thead><tr><th>Tiempo</th><th>Qué se hace</th></tr></thead><tbody>' +
            ''.join('<tr><td><b>%s</b></td><td>%s</td></tr>' % r for r in rows) + '</tbody></table>')

def taller(num, slug, title, publico, gancho, materiales, rows, fases, project, cierre, adaptar, group=None, label='Taller'):
    PROJECTS[slug] = project
    body = ('<div class="ficha"><span class="chip">%s %d</span><span class="chip">⏱ 60 min</span><span class="chip">%s</span></div>' % (label, num, e(publico)) +
            '<p class="objetivo">%s</p>' % gancho + jugar(slug) + box('ojo', 'Material', ul(materiales)) + '<h3>Guion de la sesión</h3>' + guion(rows))
    for t, items in fases:
        body += '<h3>%s</h3>' % e(t) + ol(items)
    body += ('<details class="ayuda" open><summary>✅ Proyecto terminado</summary>%s%s</details>' % (code(project), dl(slug, 'Descargar proyecto del taller (.sb3)')))
    body += box('docente', 'Cierre y exposición', P(cierre)) + box('reto', 'Adaptaciones', ul(adaptar))
    page(SEC, slug, title, body, kind='taller', group=group, meta=dict(num=num))

# --------------------------------------------------------------------------- 1
def lim(var):  # mantener la variable entre 0 y 100
    return if_(gt(v(var), 100), setv(var, 100))
taller(1, 'taller-1-mascota', 'Taller 1 · Mi mascota virtual', 'A partir de 8 años',
       'Crear una mascota que tiene hambre, ganas de jugar y sueño. Si no la cuidas, se pone triste. '
       'Funciona muy bien en exposiciones porque cualquiera puede jugar y entender cómo funciona por dentro.',
       ['Un ordenador por pareja con Scratch.', 'Proyector para la demostración.', 'Opcional: tarjetas impresas con los bloques clave.'],
       [('0-10', 'Demostración del proyecto terminado. Pregunta: «¿qué tiene que «saber» el ordenador sobre la mascota?» → aparecen las variables.'),
        ('10-25', 'Fase 1: variables hambre, alegría y energía, que bajan con el tiempo.'),
        ('25-40', 'Fase 2: botones de comida, juego y cama que las suben.'),
        ('40-50', 'Fase 3: la cara de la mascota cambia según cómo esté.'),
        ('50-60', 'Personalización libre y paseo por los proyectos de otras parejas.')],
       [('Fase 1 · La mascota tiene necesidades', [
            'Crea tres variables: <b>hambre</b>, <b>alegría</b> y <b>energía</b> (100 = perfecto).',
            'Al empezar, todas valen 100.', 'Por siempre: esperar 1 segundo y restar un poco a cada una (2, 3 y 1).']),
        ('Fase 2 · Cuidarla', [
            'Objeto comida: al hacer clic suma 15 a hambre; si pasa de 100, la deja en 100. Avisa con el mensaje «come».',
            'Haz lo mismo con el juguete (alegría) y la cama (energía).', 'La mascota, al recibir cada mensaje, dice algo.']),
        ('Fase 3 · Emociones', [
            'Si alguna necesidad baja de 30: disfraz triste.', 'Si no, si alguna baja de 60: disfraz normal. Si no: feliz.',
            'Si alguna llega a 0: la mascota se duerme y se acaba el juego.'])],
       Project(['cielo'], [
           Sprite('Mascota', ['mascota_feliz', 'mascota_normal', 'mascota_triste'], [
               [flag(), setv('hambre', 100), setv('alegría', 100), setv('energía', 100), rtimer(), costume('mascota_feliz'),
                forever(wait(1), chv('hambre', -2), chv('alegría', -3), chv('energía', -1),
                        ifelse(or_(lt(v('hambre'), 30), or_(lt(v('alegría'), 30), lt(v('energía'), 30))),
                               [costume('mascota_triste')],
                               [ifelse(or_(lt(v('hambre'), 60), or_(lt(v('alegría'), 60), lt(v('energía'), 60))),
                                       [costume('mascota_normal')], [costume('mascota_feliz')])]),
                        if_(or_(lt(v('hambre'), 1), or_(lt(v('alegría'), 1), lt(v('energía'), 1))),
                            say(join('Me has cuidado ', join(round_(timer()), ' segundos. Zzz...')), 3), stop('all')))],
               [recv('come'), say('¡Ñam, ñam!', 1)], [recv('juega'), rep(2, chy(20), wait(0.1), chy(-20), wait(0.1)), say('¡Qué divertido!', 1)],
               [recv('duerme'), say('Zzz...', 1)]], y=20, size=150),
           Sprite('Comida', ['comida'], [[clicked(), chv('hambre', 15), lim('hambre'), play('pop'), send('come')]], x=-150, y=-130, sounds=['pop']),
           Sprite('Juguete', ['juguete'], [[clicked(), chv('alegría', 15), lim('alegría'), play('boing'), send('juega')]], x=0, y=-130, sounds=['boing']),
           Sprite('Cama', ['cama'], [[clicked(), chv('energía', 15), lim('energía'), play('ding'), send('duerme')]], x=150, y=-130, sounds=['ding'])],
           variables=['hambre', 'alegría', 'energía'], shown=['hambre', 'alegría', 'energía']),
       'Cada pareja cuenta en un minuto qué ha añadido a su mascota. En exposición, deja el proyecto abierto en un ordenador con un cartel: '
       '«¿Cuánto tiempo eres capaz de cuidarla?» y un récord apuntado en una pizarra.',
       ['Primaria baja: dar el proyecto con las variables ya creadas y trabajar solo las fases 2 y 3.',
        'ESO: añadir una lista con el registro de lo que hace la mascota o que «crezca» con el tiempo (más disfraces).'])

# --------------------------------------------------------------------------- 2
naves = []
for nombre, cos, x, teclas in [('Nave', 'nave', -200, ('d', 'a', 'w', 's')), ('Nave2', 'nave2', 200, ('right arrow', 'left arrow', 'up arrow', 'down arrow'))]:
    der, izq, arr, aba = teclas
    naves.append(Sprite(nombre, [cos], [[flag(), gotoxy(x, -140), point(0), forever(
        if_(keyp(der), chx(6)), if_(keyp(izq), chx(-6)), if_(keyp(arr), chy(6)), if_(keyp(aba), chy(-6)),
        if_(touching('Roca'), play('error'), gotoxy(x, -140)))]], size=70, sounds=['error']))
taller(2, 'taller-2-carrera-espacial', 'Taller 2 · Carrera espacial a dos jugadores', 'A partir de 10 años',
       'Dos naves compiten por recoger 10 estrellas mientras esquivan meteoritos. Juego rápido, competitivo y perfecto para que el público se enganche.',
       ['Un ordenador por pareja (cada persona maneja una nave con el mismo teclado).', 'Proyector.'],
       [('0-10', 'Demostración: dos voluntarios juegan una partida. ¿Qué objetos hay? ¿Qué hace cada uno?'),
        ('10-25', 'Fase 1: dos naves que se mueven con W A S D y con las flechas.'),
        ('25-40', 'Fase 2: la estrella da puntos al jugador que la toca. Gana quien llegue a 10.'),
        ('40-50', 'Fase 3: meteoritos (clones) que cruzan el escenario y devuelven la nave a la salida.'),
        ('50-60', 'Torneo rápido entre parejas.')],
       [('Fase 1 · Dos naves', ['Nave azul: teclas W, A, S, D. Nave roja: flechas.', 'Usa <i>por siempre</i> y <i>¿tecla presionada?</i> para que el movimiento sea suave.']),
        ('Fase 2 · Recoger estrellas', ['La estrella comprueba por siempre si la toca una nave u otra.', 'Suma punto al jugador correspondiente y salta a otro sitio.',
                                        'Si alguien llega a 10, anuncia el ganador y detiene todo.']),
        ('Fase 3 · Peligro', ['El meteorito original se esconde y crea un clon cada segundo y medio.', 'Cada clon entra por la derecha a una altura al azar y cruza hacia la izquierda.',
                              'Las naves, si tocan un meteorito, vuelven a su salida.'])],
       Project(['espacio'], naves + [
           Sprite('Estrella', ['estrella'], [[flag(), setv('azul', 0), setv('roja', 0), goto('_random_'), forever(
               if_(touching('Nave'), chv('azul', 1), play('ding'), goto('_random_')),
               if_(touching('Nave2'), chv('roja', 1), play('ding'), goto('_random_')),
               if_(eq(v('azul'), 10), say('¡Gana la nave azul!', 3), stop('all')),
               if_(eq(v('roja'), 10), say('¡Gana la nave roja!', 3), stop('all')))]], sounds=['ding']),
           Sprite('Roca', ['roca'], [[flag(), hide(), forever(wait(1.5), clone())],
                                     [as_clone(), gotoxy(235, rnd(-150, 150)), show(), rep_until(lt(xpos(), -235), chx(-4), turn(3)), delclone()]])],
           variables=['azul', 'roja'], shown=['azul', 'roja']),
       'Organiza un minitorneo: las parejas ganadoras se enfrentan en el proyector. Antes de cada partida, la pareja explica un cambio que ha hecho al juego.',
       ['Primaria: sin la fase 3, o con un solo meteorito sin clones.',
        'ESO: añadir disparos con clones, vidas y velocidad que aumenta con el tiempo.'])

# --------------------------------------------------------------------------- 3
taller(3, 'taller-3-portero-ra', 'Taller 3 · Portero de realidad aumentada', 'A partir de 9 años · ideal para exposiciones',
       'Balones que «vienen hacia ti» haciéndose cada vez más grandes. Tienes 60 segundos para pararlos con las manos delante de la cámara. '
       'Muy vistoso en una pantalla grande en un Parque de las Ciencias o en una feria.',
       ['Ordenador con cámara web (o cámara USB) y proyector o pantalla grande.', 'Espacio despejado delante de la cámara y buena iluminación.'],
       [('0-10', 'Demostración con público. ¿Cómo «ve» el ordenador? Explicación sencilla de cómo detecta el movimiento comparando imágenes.'),
        ('10-25', 'Fase 1: activar la cámara y crear balones (clones) en la portería.'),
        ('25-40', 'Fase 2: el balón crece para dar sensación de que se acerca. Si detecta movimiento, es parada; si llega a ser grande, es gol.'),
        ('40-50', 'Fase 3: tiempo de 60 segundos y marcador final.'),
        ('50-60', 'Ronda de penaltis con el público.')],
       [('Fase 1 · Cámara y balones', ['Activa el vídeo con transparencia 30 para ver el fondo y a la vez a la persona.',
                                       'El balón original se esconde y crea un clon cada 1 o 2 segundos.',
                                       'Cada clon aparece en un punto al azar dentro de la portería y pequeño (tamaño 20).']),
        ('Fase 2 · Parada o gol', ['El clon repite 40 veces: crecer un poco.', 'Mientras crece, si hay movimiento sobre él: parada, sonido y desaparece.',
                                   'Si termina de crecer sin ser parado: gol y desaparece.']),
        ('Fase 3 · Tiempo y marcador', ['Reinicia el cronómetro al empezar.', 'Crea balones solo mientras el cronómetro sea menor que 60.',
                                        'Al acabar, envía «fin» y Robit anuncia el resultado.'])],
       Project(['porteria'], [
           Sprite('Balon', ['balon'], [[flag(), video('on'), vtransp(30), setv('paradas', 0), setv('goles', 0), hide(), rtimer(),
                                        rep_until(gt(timer(), 60), clone(), wait(rnd(1, 2))), wait(3), send('fin')],
                                       [as_clone(), gotoxy(rnd(-120, 120), rnd(20, 100)), setsize(20), show(),
                                        rep(40, size(4), if_(gt(vmotion('sprite'), 30), chv('paradas', 1), play('golpe'), delclone()), wait(0.05)),
                                        chv('goles', 1), play('error'), delclone()]], sounds=['golpe', 'error']),
           Sprite('Robit', ['robit1', 'robit2'], [[flag(), hide()],
                                               [recv('fin'), show(), say(join('¡Fin! Paradas: ', join(v('paradas'), join(' · Goles: ', v('goles')))))]], x=180, y=-110, size=70)],
           variables=['paradas', 'goles'], shown=['paradas', 'goles']),
       'En exposición, apunta en una pizarra el récord de paradas del día. Mientras el público juega, enseña en la pantalla del ordenador el programa del clon: '
       'es el mejor momento para explicar qué es un clon y qué es una condición.',
       ['Primaria: sin tiempo límite y con balones que crecen más despacio.',
        'ESO: niveles de dificultad (balones más rápidos), récord guardado en una variable y balones «trampa» que no hay que tocar.'])
