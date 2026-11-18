# -*- coding: utf-8 -*-
"""Motor mínimo: describe programas Scratch 3 una sola vez y genera
   (a) archivos .sb3 que abre Scratch y (b) su dibujo en HTML."""
import json, hashlib, zipfile, html

# ---------------------------------------------------------------- especificación
# tipo de entrada: n num, p positivo, w entero>=0, i entero, a ángulo, c color, t texto,
# b booleano, s subpila, B mensaje, ('m', opcode_menu, campo) menú, note, matrix
# tipo de campo: ('f',) simple, ('v',) variable, ('l',) lista, ('bf',) mensaje
I = lambda name, t, d='': ('in', name, t, d)
F = lambda name, t='f', d='': ('fd', name, t, d)
M = lambda name, menu, field, d: ('in', name, ('m', menu, field), d)

S = {}
def spec(op, cat, kind, label, *params):
    S[op] = dict(cat=cat, kind=kind, label=label, params=params)

# Movimiento
spec('motion_movesteps', 'motion', 'stack', 'mover {STEPS} pasos', I('STEPS', 'n', 10))
spec('motion_turnright', 'motion', 'stack', 'girar ↻ {DEGREES} grados', I('DEGREES', 'n', 15))
spec('motion_turnleft', 'motion', 'stack', 'girar ↺ {DEGREES} grados', I('DEGREES', 'n', 15))
spec('motion_goto', 'motion', 'stack', 'ir a {TO}', M('TO', 'motion_goto_menu', 'TO', '_random_'))
spec('motion_gotoxy', 'motion', 'stack', 'ir a x: {X} y: {Y}', I('X', 'n', 0), I('Y', 'n', 0))
spec('motion_glidesecstoxy', 'motion', 'stack', 'deslizar en {SECS} segs a x: {X} y: {Y}', I('SECS', 'n', 1), I('X', 'n', 0), I('Y', 'n', 0))
spec('motion_glideto', 'motion', 'stack', 'deslizar en {SECS} segs a {TO}', I('SECS', 'n', 1), M('TO', 'motion_glideto_menu', 'TO', '_random_'))
spec('motion_pointindirection', 'motion', 'stack', 'apuntar en dirección {DIRECTION}', I('DIRECTION', 'a', 90))
spec('motion_pointtowards', 'motion', 'stack', 'apuntar hacia {TOWARDS}', M('TOWARDS', 'motion_pointtowards_menu', 'TOWARDS', '_mouse_'))
spec('motion_changexby', 'motion', 'stack', 'sumar a x {DX}', I('DX', 'n', 10))
spec('motion_setx', 'motion', 'stack', 'dar a x el valor {X}', I('X', 'n', 0))
spec('motion_changeyby', 'motion', 'stack', 'sumar a y {DY}', I('DY', 'n', 10))
spec('motion_sety', 'motion', 'stack', 'dar a y el valor {Y}', I('Y', 'n', 0))
spec('motion_ifonedgebounce', 'motion', 'stack', 'si toca un borde, rebotar')
spec('motion_setrotationstyle', 'motion', 'stack', 'fijar estilo de rotación a {STYLE}', F('STYLE', 'f', 'left-right'))
spec('motion_xposition', 'motion', 'rep', 'posición en x')
spec('motion_yposition', 'motion', 'rep', 'posición en y')
spec('motion_direction', 'motion', 'rep', 'dirección')
# Apariencia
spec('looks_sayforsecs', 'looks', 'stack', 'decir {MESSAGE} durante {SECS} segundos', I('MESSAGE', 't', '¡Hola!'), I('SECS', 'n', 2))
spec('looks_say', 'looks', 'stack', 'decir {MESSAGE}', I('MESSAGE', 't', '¡Hola!'))
spec('looks_thinkforsecs', 'looks', 'stack', 'pensar {MESSAGE} durante {SECS} segundos', I('MESSAGE', 't', 'Umm...'), I('SECS', 'n', 2))
spec('looks_think', 'looks', 'stack', 'pensar {MESSAGE}', I('MESSAGE', 't', 'Umm...'))
spec('looks_switchcostumeto', 'looks', 'stack', 'cambiar disfraz a {COSTUME}', M('COSTUME', 'looks_costume', 'COSTUME', ''))
spec('looks_nextcostume', 'looks', 'stack', 'siguiente disfraz')
spec('looks_switchbackdropto', 'looks', 'stack', 'cambiar fondo a {BACKDROP}', M('BACKDROP', 'looks_backdrops', 'BACKDROP', ''))
spec('looks_nextbackdrop', 'looks', 'stack', 'siguiente fondo')
spec('looks_changesizeby', 'looks', 'stack', 'cambiar tamaño por {CHANGE}', I('CHANGE', 'n', 10))
spec('looks_setsizeto', 'looks', 'stack', 'fijar tamaño al {SIZE} %', I('SIZE', 'n', 100))
spec('looks_changeeffectby', 'looks', 'stack', 'sumar al efecto {EFFECT} {CHANGE}', F('EFFECT', 'f', 'COLOR'), I('CHANGE', 'n', 25))
spec('looks_seteffectto', 'looks', 'stack', 'dar al efecto {EFFECT} el valor {VALUE}', F('EFFECT', 'f', 'COLOR'), I('VALUE', 'n', 0))
spec('looks_cleargraphiceffects', 'looks', 'stack', 'quitar efectos gráficos')
spec('looks_show', 'looks', 'stack', 'mostrar')
spec('looks_hide', 'looks', 'stack', 'esconder')
spec('looks_gotofrontback', 'looks', 'stack', 'ir a capa {FRONT_BACK}', F('FRONT_BACK', 'f', 'front'))
spec('looks_costumenumbername', 'looks', 'rep', '{NUMBER_NAME} de disfraz', F('NUMBER_NAME', 'f', 'number'))
spec('looks_size', 'looks', 'rep', 'tamaño')
# Sonido
spec('sound_playuntildone', 'sound', 'stack', 'tocar sonido {SOUND_MENU} hasta que termine', M('SOUND_MENU', 'sound_sounds_menu', 'SOUND_MENU', ''))
spec('sound_play', 'sound', 'stack', 'iniciar sonido {SOUND_MENU}', M('SOUND_MENU', 'sound_sounds_menu', 'SOUND_MENU', ''))
spec('sound_stopallsounds', 'sound', 'stack', 'detener todos los sonidos')
spec('sound_changevolumeby', 'sound', 'stack', 'cambiar volumen por {VOLUME}', I('VOLUME', 'n', -10))
spec('sound_setvolumeto', 'sound', 'stack', 'fijar volumen al {VOLUME} %', I('VOLUME', 'n', 100))
spec('sound_changeeffectby', 'sound', 'stack', 'sumar al efecto {EFFECT} {VALUE}', F('EFFECT', 'f', 'PITCH'), I('VALUE', 'n', 10))
spec('sound_cleareffects', 'sound', 'stack', 'quitar efectos de sonido')
# Eventos
spec('event_whenflagclicked', 'events', 'hat', 'al hacer clic en {FLAG}')
spec('event_whenkeypressed', 'events', 'hat', 'al presionar tecla {KEY_OPTION}', F('KEY_OPTION', 'f', 'space'))
spec('event_whenthisspriteclicked', 'events', 'hat', 'al hacer clic en este objeto')
spec('event_whenstageclicked', 'events', 'hat', 'al hacer clic en el escenario')
spec('event_whenbackdropswitchesto', 'events', 'hat', 'cuando el fondo cambie a {BACKDROP}', F('BACKDROP', 'f', ''))
spec('event_whenbroadcastreceived', 'events', 'hat', 'al recibir {BROADCAST_OPTION}', F('BROADCAST_OPTION', 'bf', 'mensaje1'))
spec('event_broadcast', 'events', 'stack', 'enviar {BROADCAST_INPUT}', I('BROADCAST_INPUT', 'B', 'mensaje1'))
spec('event_broadcastandwait', 'events', 'stack', 'enviar {BROADCAST_INPUT} y esperar', I('BROADCAST_INPUT', 'B', 'mensaje1'))
spec('event_whengreaterthan', 'events', 'hat', 'cuando {WHENGREATERTHANMENU} > {VALUE}', F('WHENGREATERTHANMENU', 'f', 'TIMER'), I('VALUE', 'n', 10))
# Control
spec('control_wait', 'control', 'stack', 'esperar {DURATION} segundos', I('DURATION', 'p', 1))
spec('control_repeat', 'control', 'c', 'repetir {TIMES}', I('TIMES', 'w', 10), I('SUBSTACK', 's'))
spec('control_forever', 'control', 'capc', 'por siempre', I('SUBSTACK', 's'))
spec('control_if', 'control', 'c', 'si {CONDITION} entonces', I('CONDITION', 'b'), I('SUBSTACK', 's'))
spec('control_if_else', 'control', 'e', 'si {CONDITION} entonces', I('CONDITION', 'b'), I('SUBSTACK', 's'), I('SUBSTACK2', 's'))
spec('control_wait_until', 'control', 'stack', 'esperar hasta que {CONDITION}', I('CONDITION', 'b'))
spec('control_repeat_until', 'control', 'c', 'repetir hasta que {CONDITION}', I('CONDITION', 'b'), I('SUBSTACK', 's'))
spec('control_stop', 'control', 'cap', 'detener {STOP_OPTION}', F('STOP_OPTION', 'f', 'all'))
spec('control_start_as_clone', 'control', 'hat', 'al comenzar como clon')
spec('control_create_clone_of', 'control', 'stack', 'crear clon de {CLONE_OPTION}', M('CLONE_OPTION', 'control_create_clone_of_menu', 'CLONE_OPTION', '_myself_'))
spec('control_delete_this_clone', 'control', 'cap', 'eliminar este clon')
# Sensores
spec('sensing_touchingobject', 'sensing', 'bool', '¿tocando {TOUCHINGOBJECTMENU}?', M('TOUCHINGOBJECTMENU', 'sensing_touchingobjectmenu', 'TOUCHINGOBJECTMENU', '_mouse_'))
spec('sensing_touchingcolor', 'sensing', 'bool', '¿tocando el color {COLOR}?', I('COLOR', 'c', '#000000'))
spec('sensing_distanceto', 'sensing', 'rep', 'distancia a {DISTANCETOMENU}', M('DISTANCETOMENU', 'sensing_distancetomenu', 'DISTANCETOMENU', '_mouse_'))
spec('sensing_askandwait', 'sensing', 'stack', 'preguntar {QUESTION} y esperar', I('QUESTION', 't', '¿Cómo te llamas?'))
spec('sensing_answer', 'sensing', 'rep', 'respuesta')
spec('sensing_keypressed', 'sensing', 'bool', '¿tecla {KEY_OPTION} presionada?', M('KEY_OPTION', 'sensing_keyoptions', 'KEY_OPTION', 'space'))
spec('sensing_mousedown', 'sensing', 'bool', '¿ratón presionado?')
spec('sensing_mousex', 'sensing', 'rep', 'posición x del ratón')
spec('sensing_mousey', 'sensing', 'rep', 'posición y del ratón')
spec('sensing_timer', 'sensing', 'rep', 'cronómetro')
spec('sensing_resettimer', 'sensing', 'stack', 'reiniciar cronómetro')
spec('sensing_loudness', 'sensing', 'rep', 'volumen del sonido')
# Operadores
for op, sym in [('add', '+'), ('subtract', '-'), ('multiply', '*'), ('divide', '/')]:
    spec('operator_' + op, 'operators', 'rep', '{NUM1} %s {NUM2}' % sym, I('NUM1', 'n', ''), I('NUM2', 'n', ''))
spec('operator_random', 'operators', 'rep', 'número aleatorio entre {FROM} y {TO}', I('FROM', 'n', 1), I('TO', 'n', 10))
for op, sym in [('gt', '>'), ('lt', '<'), ('equals', '=')]:
    spec('operator_' + op, 'operators', 'bool', '{OPERAND1} %s {OPERAND2}' % sym, I('OPERAND1', 't', ''), I('OPERAND2', 't', 50))
spec('operator_and', 'operators', 'bool', '{OPERAND1} y {OPERAND2}', I('OPERAND1', 'b'), I('OPERAND2', 'b'))
spec('operator_or', 'operators', 'bool', '{OPERAND1} o {OPERAND2}', I('OPERAND1', 'b'), I('OPERAND2', 'b'))
spec('operator_not', 'operators', 'bool', 'no {OPERAND}', I('OPERAND', 'b'))
spec('operator_join', 'operators', 'rep', 'unir {STRING1} {STRING2}', I('STRING1', 't', 'manzana '), I('STRING2', 't', 'plátano'))
spec('operator_letter_of', 'operators', 'rep', 'letra {LETTER} de {STRING}', I('LETTER', 'w', 1), I('STRING', 't', 'manzana'))
spec('operator_length', 'operators', 'rep', 'longitud de {STRING}', I('STRING', 't', 'manzana'))
spec('operator_round', 'operators', 'rep', 'redondear {NUM}', I('NUM', 'n', ''))
spec('operator_mathop', 'operators', 'rep', '{OPERATOR} de {NUM}', F('OPERATOR', 'f', 'abs'), I('NUM', 'n', ''))
# Variables y listas
spec('data_variable', 'variables', 'rep', '{VARIABLE}', F('VARIABLE', 'v', ''))
spec('data_setvariableto', 'variables', 'stack', 'dar a {VARIABLE} el valor {VALUE}', F('VARIABLE', 'v', ''), I('VALUE', 't', 0))
spec('data_changevariableby', 'variables', 'stack', 'sumar a {VARIABLE} {VALUE}', F('VARIABLE', 'v', ''), I('VALUE', 'n', 1))
spec('data_showvariable', 'variables', 'stack', 'mostrar variable {VARIABLE}', F('VARIABLE', 'v', ''))
spec('data_hidevariable', 'variables', 'stack', 'esconder variable {VARIABLE}', F('VARIABLE', 'v', ''))
spec('data_addtolist', 'lists', 'stack', 'añadir {ITEM} a {LIST}', I('ITEM', 't', 'cosa'), F('LIST', 'l', ''))
spec('data_deletealloflist', 'lists', 'stack', 'eliminar todos de {LIST}', F('LIST', 'l', ''))
spec('data_itemoflist', 'lists', 'rep', 'elemento {INDEX} de {LIST}', I('INDEX', 'i', 1), F('LIST', 'l', ''))
spec('data_listcontainsitem', 'lists', 'bool', '¿{ITEM} está en {LIST}?', I('ITEM', 't', 'cosa'), F('LIST', 'l', ''))
spec('data_itemnumoflist', 'lists', 'rep', '# de elemento de {ITEM} en {LIST}', I('ITEM', 't', 'cosa'), F('LIST', 'l', ''))
spec('data_lengthoflist', 'lists', 'rep', 'longitud de {LIST}', F('LIST', 'l', ''))
# Mis bloques (sin parámetros)
spec('procedures_definition', 'myblocks', 'hat', 'definir {PROC}')
spec('procedures_call', 'myblocks', 'stack', '{PROC}')
# Lápiz
spec('pen_clear', 'pen', 'stack', 'borrar todo')
spec('pen_stamp', 'pen', 'stack', 'sellar')
spec('pen_penDown', 'pen', 'stack', 'bajar lápiz')
spec('pen_penUp', 'pen', 'stack', 'subir lápiz')
spec('pen_setPenColorToColor', 'pen', 'stack', 'fijar color de lápiz a {COLOR}', I('COLOR', 'c', '#4c97ff'))
spec('pen_changePenColorParamBy', 'pen', 'stack', 'cambiar {COLOR_PARAM} de lápiz por {VALUE}', M('COLOR_PARAM', 'pen_menu_colorParam', 'colorParam', 'color'), I('VALUE', 'n', 10))
spec('pen_setPenColorParamTo', 'pen', 'stack', 'fijar {COLOR_PARAM} de lápiz a {VALUE}', M('COLOR_PARAM', 'pen_menu_colorParam', 'colorParam', 'color'), I('VALUE', 'n', 50))
spec('pen_setPenSizeTo', 'pen', 'stack', 'fijar tamaño de lápiz a {SIZE}', I('SIZE', 'n', 1))
spec('pen_changePenSizeBy', 'pen', 'stack', 'cambiar tamaño de lápiz por {SIZE}', I('SIZE', 'n', 1))
# Música
spec('music_playDrumForBeats', 'music', 'stack', 'tocar tambor {DRUM} durante {BEATS} tiempos', M('DRUM', 'music_menu_DRUM', 'DRUM', '1'), I('BEATS', 'n', 0.25))
spec('music_restForBeats', 'music', 'stack', 'silencio de {BEATS} tiempos', I('BEATS', 'n', 0.25))
spec('music_playNoteForBeats', 'music', 'stack', 'tocar nota {NOTE} durante {BEATS} tiempos', I('NOTE', 'note', 60), I('BEATS', 'n', 0.25))
spec('music_setInstrument', 'music', 'stack', 'fijar instrumento a {INSTRUMENT}', M('INSTRUMENT', 'music_menu_INSTRUMENT', 'INSTRUMENT', '1'))
spec('music_setTempo', 'music', 'stack', 'dar al tempo el valor {TEMPO}', I('TEMPO', 'n', 60))
spec('music_changeTempo', 'music', 'stack', 'cambiar tempo por {TEMPO}', I('TEMPO', 'n', 20))
spec('music_getTempo', 'music', 'rep', 'tempo')
# Sensor de vídeo
spec('videoSensing_whenMotionGreaterThan', 'video', 'hat', 'cuando movimiento de vídeo > {REFERENCE}', I('REFERENCE', 'n', 10))
spec('videoSensing_videoOn', 'video', 'rep', '{ATTRIBUTE} de vídeo en {SUBJECT}', M('ATTRIBUTE', 'videoSensing_menu_ATTRIBUTE', 'ATTRIBUTE', 'motion'), M('SUBJECT', 'videoSensing_menu_SUBJECT', 'SUBJECT', 'sprite'))
spec('videoSensing_videoToggle', 'video', 'stack', '{VIDEO_STATE} vídeo', M('VIDEO_STATE', 'videoSensing_menu_VIDEO_STATE', 'VIDEO_STATE', 'on'))
spec('videoSensing_setVideoTransparency', 'video', 'stack', 'fijar transparencia de vídeo a {TRANSPARENCY}', I('TRANSPARENCY', 'n', 50))
# Texto a voz y traducir
spec('text2speech_speakAndWait', 'tts', 'stack', 'decir {WORDS}', I('WORDS', 't', 'hola'))
spec('text2speech_setVoice', 'tts', 'stack', 'asignar voz a {VOICE}', M('VOICE', 'text2speech_menu_voices', 'voices', 'ALTO'))
spec('text2speech_setLanguage', 'tts', 'stack', 'fijar idioma a {LANGUAGE}', M('LANGUAGE', 'text2speech_menu_languages', 'languages', 'es'))
spec('translate_getTranslate', 'translate', 'rep', 'traducir {WORDS} al {LANGUAGE}', I('WORDS', 't', 'hola'), M('LANGUAGE', 'translate_menu_languages', 'languages', 'en'))
# Makey Makey
spec('makeymakey_whenMakeyKeyPressed', 'makey', 'hat', 'al presionar tecla {KEY}', M('KEY', 'makeymakey_menu_KEY', 'KEY', 'SPACE'))
spec('makeymakey_whenCodePressed', 'makey', 'hat', 'al presionar {SEQUENCE} en orden', M('SEQUENCE', 'makeymakey_menu_SEQUENCE', 'SEQUENCE', 'LEFT UP RIGHT'))
# micro:bit
spec('microbit_whenButtonPressed', 'microbit', 'hat', 'al presionar botón {BTN}', M('BTN', 'microbit_menu_buttons', 'buttons', 'A'))
spec('microbit_isButtonPressed', 'microbit', 'bool', '¿botón {BTN} presionado?', M('BTN', 'microbit_menu_buttons', 'buttons', 'A'))
spec('microbit_whenGesture', 'microbit', 'hat', 'al {GESTURE}', M('GESTURE', 'microbit_menu_gestures', 'gestures', 'moved'))
spec('microbit_displaySymbol', 'microbit', 'stack', 'mostrar {MATRIX}', I('MATRIX', 'matrix', '0101010101100010101000100'))
spec('microbit_displayText', 'microbit', 'stack', 'mostrar texto {TEXT}', I('TEXT', 't', 'Hola'))
spec('microbit_displayClear', 'microbit', 'stack', 'limpiar pantalla')
spec('microbit_whenTilted', 'microbit', 'hat', 'al inclinar hacia {DIRECTION}', M('DIRECTION', 'microbit_menu_tiltDirectionAny', 'tiltDirectionAny', 'any'))
spec('microbit_isTilted', 'microbit', 'bool', '¿inclinado hacia {DIRECTION}?', M('DIRECTION', 'microbit_menu_tiltDirectionAny', 'tiltDirectionAny', 'any'))
spec('microbit_getTiltAngle', 'microbit', 'rep', 'ángulo de inclinación hacia {DIRECTION}', M('DIRECTION', 'microbit_menu_tiltDirection', 'tiltDirection', 'front'))
spec('microbit_whenPinConnected', 'microbit', 'hat', 'al conectar pin {PIN}', M('PIN', 'microbit_menu_touchPins', 'touchPins', '0'))

EXT = {'pen': 'pen', 'music': 'music', 'videoSensing': 'videoSensing', 'text2speech': 'text2speech',
       'translate': 'translate', 'makeymakey': 'makeymakey', 'microbit': 'microbit'}

# Texto visible de opciones de menú (en español)
SHOW = {'_random_': 'posición aleatoria', '_mouse_': 'puntero del ratón', '_edge_': 'borde', '_myself_': 'mí mismo',
        'space': 'espacio', 'left arrow': 'flecha izquierda', 'right arrow': 'flecha derecha', 'up arrow': 'flecha arriba',
        'down arrow': 'flecha abajo', 'any': 'cualquiera', 'all': 'todos', 'this script': 'este programa',
        'other scripts in sprite': 'otros programas en el objeto', 'left-right': 'izquierda-derecha',
        'all around': 'en todas direcciones', "don't rotate": 'no rotar', 'COLOR': 'color', 'GHOST': 'desvanecer',
        'FISHEYE': 'ojo de pez', 'WHIRL': 'remolino', 'PIXELATE': 'pixelar', 'BRIGHTNESS': 'brillo', 'MOSAIC': 'mosaico',
        'PITCH': 'altura', 'front': 'delantera', 'back': 'trasera', 'on': 'encender', 'off': 'apagar',
        'on-flipped': 'invertir', 'motion': 'movimiento', 'direction': 'dirección', 'sprite': 'objeto',
        'stage': 'escenario', 'moved': 'mover', 'shaken': 'agitar', 'jumped': 'saltar', 'SPACE': 'espacio',
        'LEFT': 'flecha izquierda', 'RIGHT': 'flecha derecha', 'UP': 'flecha arriba', 'DOWN': 'flecha abajo',
        'LEFT UP RIGHT': 'izquierda arriba derecha', 'RIGHT UP LEFT': 'derecha arriba izquierda',
        'LEFT RIGHT': 'izquierda derecha', 'UP DOWN': 'arriba abajo', 'color': 'color', 'saturation': 'saturación',
        'brightness': 'brillo', 'transparency': 'transparencia', 'number': 'número', 'name': 'nombre',
        'TIMER': 'cronómetro', 'LOUDNESS': 'volumen del sonido', 'ALTO': 'contralto', 'TENOR': 'tenor', 'SQUEAK': 'chillido',
        'GIANT': 'gigante', 'KITTEN': 'gatito', 'es': 'Español', 'en': 'Inglés', 'fr': 'Francés', 'de': 'Alemán',
        'it': 'Italiano', 'abs': 'valor absoluto', 'sqrt': 'raíz cuadrada', 'sin': 'sen', 'cos': 'cos'}
DRUMS = {'1': '(1) Caja', '2': '(2) Bombo', '3': '(3) Baqueta', '4': '(4) Platillo crash', '5': '(5) Charles abierto',
         '6': '(6) Charles cerrado', '7': '(7) Pandereta', '8': '(8) Palmada', '9': '(9) Claves', '10': '(10) Bloque de madera',
         '11': '(11) Cencerro', '12': '(12) Triángulo', '13': '(13) Bongo', '14': '(14) Conga', '15': '(15) Cabasa',
         '16': '(16) Güiro', '17': '(17) Vibraslap', '18': '(18) Cuíca'}
INSTR = {'1': '(1) Piano', '2': '(2) Piano eléctrico', '3': '(3) Órgano', '4': '(4) Guitarra', '5': '(5) Guitarra eléctrica',
         '6': '(6) Bajo', '7': '(7) Pizzicato', '8': '(8) Violonchelo', '9': '(9) Trombón', '10': '(10) Clarinete',
         '11': '(11) Saxofón', '12': '(12) Flauta', '13': '(13) Flauta de madera', '14': '(14) Fagot', '15': '(15) Coro',
         '16': '(16) Vibráfono', '17': '(17) Caja de música', '18': '(18) Tambor metálico', '19': '(19) Marimba',
         '20': '(20) Sintetizador lead', '21': '(21) Sintetizador pad'}
TILT = {'any': 'cualquiera', 'front': 'delante', 'back': 'atrás', 'left': 'izquierda', 'right': 'derecha'}

# ---------------------------------------------------------------- construcción
class Blk:
    def __init__(self, op, a):
        self.op, self.a = op, a

def B(op, *args, **kw):
    """Crea un bloque; los argumentos posicionales siguen el orden de la especificación."""
    sp = S[op]
    names = [p[1] for p in sp['params']]
    a = {}
    for n, v in zip(names, args):
        a[n] = v
    a.update(kw)
    return Blk(op, a)

class Proc:  # «Mis bloques» sin parámetros
    def __init__(self, name): self.name = name

# ---------------------------------------------------------------- serializar a sb3
class Ctx:
    def __init__(self, proj, target_name):
        self.p, self.blocks, self.tname = proj, {}, target_name
    def nid(self):
        self.p.counter += 1
        return 'id%05d' % self.p.counter

PRIM = {'n': 4, 'p': 5, 'w': 6, 'i': 7, 'a': 8, 'c': 9, 't': 10}

def ser_stack(ctx, stack, parent, top=None):
    first = prev = None
    for node in stack:
        bid = ser_block(ctx, node, prev if prev else parent)
        if prev:
            ctx.blocks[prev]['next'] = bid
        else:
            first = bid
        prev = bid
    if top is not None and first:
        b = ctx.blocks[first]
        b['topLevel'] = True; b['parent'] = None; b['x'], b['y'] = top
    return first

def ser_value(ctx, val, typ, default, parent):
    if isinstance(typ, tuple):  # menú
        _, menu, field = typ
        sid = ctx.nid()
        ctx.blocks[sid] = dict(opcode=menu, next=None, parent=parent, inputs={},
                               fields={field: [str(val), None]}, shadow=True, topLevel=False)
        return [1, sid]
    if typ == 'b':
        return [2, ser_block(ctx, val, parent)] if val is not None else None
    if typ == 's':
        if not val: return None
        return [2, ser_stack(ctx, val, parent)]
    if typ == 'B':
        bid = ctx.p.bcast(val)
        return [1, [11, val, bid]]
    if typ in ('note', 'matrix'):
        sid = ctx.nid()
        op, fld = ('note', 'NOTE') if typ == 'note' else ('matrix', 'MATRIX')
        ctx.blocks[sid] = dict(opcode=op, next=None, parent=parent, inputs={}, fields={fld: [str(val) if not isinstance(val, Blk) else ('60' if typ == 'note' else '0' * 25), None]},
                               shadow=True, topLevel=False)
        if isinstance(val, Blk):
            if val.op == 'data_variable':
                return [3, [12, val.a['VARIABLE'], ctx.p.var(val.a['VARIABLE'])], sid]
            return [3, ser_block(ctx, val, parent), sid]
        return [1, sid]
    code = PRIM[typ]
    shadow = [code, str(default) if code != 9 else (default or '#ff0000')]
    if isinstance(val, Blk):
        if val.op == 'data_variable':
            name = val.a['VARIABLE']
            return [3, [12, name, ctx.p.var(name)], shadow]
        return [3, ser_block(ctx, val, parent), shadow]
    if code == 9:
        return [1, [9, str(val)]]
    return [1, [code, _fmt(val)]]

def _fmt(v):
    if isinstance(v, float) and v.is_integer(): v = int(v)
    return str(v)

def ser_block(ctx, node, parent):
    bid = ctx.nid()
    b = dict(opcode=node.op, next=None, parent=parent, inputs={}, fields={}, shadow=False, topLevel=False)
    ctx.blocks[bid] = b
    sp = S[node.op]
    if node.op == 'procedures_definition':
        pid = ctx.nid()
        ctx.blocks[pid] = dict(opcode='procedures_prototype', next=None, parent=bid, inputs={}, fields={},
                               shadow=True, topLevel=False,
                               mutation=dict(tagName='mutation', children=[], proccode=node.a['PROC'],
                                             argumentids='[]', argumentnames='[]', argumentdefaults='[]', warp='false'))
        b['inputs']['custom_block'] = [1, pid]
        return bid
    if node.op == 'procedures_call':
        b['mutation'] = dict(tagName='mutation', children=[], proccode=node.a['PROC'], argumentids='[]', warp='false')
        return bid
    for kind, name, typ, default in sp['params']:
        val = node.a.get(name, default if typ not in ('b', 's') else None)
        if kind == 'in':
            r = ser_value(ctx, val, typ, default if typ not in ('b', 's') else '', bid)
            if r is not None: b['inputs'][name] = r
        else:
            if typ == 'v':
                b['fields'][name] = [val, ctx.p.var(val)]
            elif typ == 'l':
                b['fields'][name] = [val, ctx.p.lst(val)]
            elif typ == 'bf':
                b['fields'][name] = [val, ctx.p.bcast(val)]
            else:
                b['fields'][name] = [str(val), None]
    if node.op == 'control_stop':
        opt = node.a.get('STOP_OPTION', 'all')
        b['mutation'] = dict(tagName='mutation', children=[], hasnext='true' if opt == 'other scripts in sprite' else 'false')
    return bid

class Sprite:
    def __init__(self, name, costumes, scripts=(), x=0, y=0, size=100, direction=90, visible=True,
                 sounds=(), rotation='all around'):
        self.name, self.costumes, self.scripts = name, list(costumes), list(scripts)
        self.x, self.y, self.size, self.direction, self.visible = x, y, size, direction, visible
        self.sounds, self.rotation = list(sounds), rotation

class Project:
    def __init__(self, backdrops=('blanco',), sprites=(), stage_scripts=(), variables=(), lists=(), shown=(),
                 stage_sounds=()):
        self.backdrops, self.sprites, self.stage_scripts = list(backdrops), list(sprites), list(stage_scripts)
        self.counter = 0
        self.vars, self.lists, self.bcasts = {}, {}, {}
        for v in variables: self.var(v)
        for l in lists: self.lst(l)
        self.shown = list(shown)
        self.stage_sounds = list(stage_sounds)
    def var(self, name):
        if name not in self.vars: self.vars[name] = 'var_%d' % (len(self.vars) + 1)
        return self.vars[name]
    def lst(self, name):
        if name not in self.lists: self.lists[name] = 'list_%d' % (len(self.lists) + 1)
        return self.lists[name]
    def bcast(self, name):
        if name not in self.bcasts: self.bcasts[name] = 'msg_%d' % (len(self.bcasts) + 1)
        return self.bcasts[name]

    def all_scripts(self):
        yield from self.stage_scripts
        for s in self.sprites: yield from s.scripts

    def to_sb3(self, path, assets):
        files = {}
        def costume(name, stage=False):
            return _costume_entry(name, assets, files)
        def sound(name):
            return _sound_entry(name, assets, files)
        def scripts_json(tname, scripts):
            ctx = Ctx(self, tname)
            for i, sc in enumerate(scripts):
                pos = (40 + (i % 2) * 380, 40 + (i // 2) * 320)
                head = sc[0]
                ser_stack(ctx, sc, None, top=pos)
            return ctx.blocks
        targets = []
        stage_blocks = scripts_json('Stage', self.stage_scripts)
        sprite_blocks = [scripts_json(s.name, s.scripts) for s in self.sprites]
        stage = dict(isStage=True, name='Stage',
                     variables={vid: [n, 0] for n, vid in self.vars.items()},
                     lists={lid: [n, []] for n, lid in self.lists.items()},
                     broadcasts={bid: n for n, bid in self.bcasts.items()},
                     blocks=stage_blocks, comments={}, currentCostume=0,
                     costumes=[costume(b, True) for b in self.backdrops],
                     sounds=[sound(s) for s in self.stage_sounds], volume=100, layerOrder=0, tempo=60,
                     videoTransparency=50, videoState='on', textToSpeechLanguage=None)
        targets.append(stage)
        for i, (s, blks) in enumerate(zip(self.sprites, sprite_blocks)):
            targets.append(dict(isStage=False, name=s.name, variables={}, lists={}, broadcasts={}, blocks=blks,
                                comments={}, currentCostume=0, costumes=[costume(c) for c in s.costumes],
                                sounds=[sound(x) for x in s.sounds], volume=100, layerOrder=i + 1,
                                visible=s.visible, x=s.x, y=s.y, size=s.size, direction=s.direction,
                                draggable=False, rotationStyle=s.rotation))
        ops = {b['opcode'] for t in targets for b in t['blocks'].values()}
        exts = sorted({EXT[o.split('_')[0]] for o in ops if o.split('_')[0] in EXT})
        monitors = []
        for k, name in enumerate(self.shown):
            monitors.append(dict(id=self.var(name), mode='default', opcode='data_variable',
                                 params={'VARIABLE': name}, spriteName=None, value=0, width=0, height=0,
                                 x=5, y=5 + k * 27, visible=True, sliderMin=0, sliderMax=100, isDiscrete=True))
        proj = dict(targets=targets, monitors=monitors, extensions=exts,
                    meta=dict(semver='3.0.0', vm='0.2.0', agent='Scratch en el aula'))
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('project.json', json.dumps(proj, ensure_ascii=False))
            for fn, data in files.items():
                z.writestr(fn, data)
        return proj

# ---------------------------------------------------------------- dibujar en HTML
FLAG = ('<svg class="flag" viewBox="0 0 16 16" width="16" height="16" aria-label="bandera verde">'
        '<path d="M3 1v14" stroke="#455a1f" stroke-width="1.6"/>'
        '<path d="M3.8 2.2c3-1.6 4.8 1.4 8.6-.2v7c-3.8 1.6-5.6-1.4-8.6.2z" fill="#4cbf56" stroke="#45993d" stroke-width=".8"/></svg>')
e = html.escape

def disp(v):
    s = str(v)
    if s in SHOW: return SHOW[s]
    return s

def r_val(val, typ):
    if isinstance(typ, tuple):
        menu = typ[1]
        txt = DRUMS.get(str(val)) if 'DRUM' in menu else INSTR.get(str(val)) if 'INSTRUMENT' in menu else TILT.get(str(val)) if 'tiltDirection' in menu else None
        return '<span class="sb-menu">%s ▾</span>' % e(txt or disp(val))
    if typ == 'B':
        return '<span class="sb-menu">%s ▾</span>' % e(str(val))
    if typ == 'b':
        return r_block(val) if val is not None else '<span class="sb-bool-empty"></span>'
    if typ == 'note':
        return r_block(val) if isinstance(val, Blk) else '<span class="sb-num">%s</span>' % e(_fmt(val))
    if typ == 'matrix':
        cells = ''.join('<i class="m%s"></i>' % ('1' if ch == '1' else '0') for ch in str(val))
        return '<span class="sb-matrix">%s</span>' % cells
    if isinstance(val, Blk):
        return r_block(val)
    if typ == 'c':
        return '<span class="sb-color" style="background:%s"></span>' % e(str(val))
    cls = 'sb-txt' if typ == 't' else 'sb-num'
    return '<span class="%s">%s</span>' % (cls, e(_fmt(val)))

def r_field(val, typ, op):
    if typ == 'v':
        return '<span class="sb-menu">%s ▾</span>' % e(val) if op != 'data_variable' else e(val)
    if typ in ('l', 'bf'):
        return '<span class="sb-menu">%s ▾</span>' % e(val)
    return '<span class="sb-menu">%s ▾</span>' % e(disp(val))

def r_label(node):
    sp = S[node.op]
    lab = e(sp['label'])
    if '{PROC}' in sp['label']:
        return lab.replace('{PROC}', e(node.a['PROC']))
    lab = lab.replace('{FLAG}', FLAG)
    for kind, name, typ, default in sp['params']:
        if typ == 's': continue
        token = '{%s}' % name
        if token not in lab: continue
        val = node.a.get(name, default if typ not in ('b',) else None)
        out = r_val(val, typ) if kind == 'in' else r_field(val, typ, node.op)
        lab = lab.replace(token, out)
    return lab

def r_block(node):
    sp = S[node.op]
    cat, kind = sp['cat'], sp['kind']
    lab = r_label(node)
    if kind == 'rep':
        return '<span class="sb-rep c-%s">%s</span>' % (cat, lab)
    if kind == 'bool':
        return '<span class="sb-boolb c-%s">%s</span>' % (cat, lab)
    if kind in ('c', 'capc', 'e'):
        inner = r_stack(node.a.get('SUBSTACK') or [])
        out = '<div class="sb-c c-%s%s"><div class="sb-line">%s</div><div class="sb-in">%s</div>' % (
            cat, ' sb-cap' if kind == 'capc' else '', lab, inner)
        if kind == 'e':
            out += '<div class="sb-line">si no</div><div class="sb-in">%s</div>' % r_stack(node.a.get('SUBSTACK2') or [])
        return out + '<div class="sb-cend"></div></div>'
    extra = ' sb-hat' if kind == 'hat' else ' sb-cap' if kind == 'cap' else ''
    if node.op == 'procedures_definition': extra += ' sb-def'
    return '<div class="sb-blk c-%s%s">%s</div>' % (cat, extra, lab)

def r_stack(stack):
    return ''.join(r_block(n) for n in stack)

def render_scripts(scripts, title=None):
    out = []
    for sc in scripts:
        out.append('<div class="sb-script">%s</div>' % r_stack(sc))
    t = '<div class="sb-owner">%s</div>' % e(title) if title else ''
    return '<div class="sb-group">%s<div class="sb-scripts">%s</div></div>' % (t, ''.join(out))

def render_project(p):
    parts = []
    if p.stage_scripts:
        parts.append(render_scripts(p.stage_scripts, 'Escenario'))
    for s in p.sprites:
        if s.scripts:
            parts.append(render_scripts(s.scripts, 'Objeto: ' + s.name))
    return ''.join(parts)

def used_categories(p):
    return sorted({S[n.op]['cat'] for n in walk(p)})

def walk(p):
    def w(stack):
        for n in stack:
            yield n
            for k, v in n.a.items():
                if isinstance(v, Blk): yield from w([v])
                elif isinstance(v, list) and v and isinstance(v[0], Blk): yield from w(v)
    for sc in p.all_scripts():
        yield from w(sc)

# ---------------------------------------------------------------- recursos sueltos
def _costume_entry(name, assets, files):
    data, ext, cx, cy = assets.image(name)
    md5 = hashlib.md5(data).hexdigest()
    files[md5 + '.' + ext] = data
    return dict(name=name, bitmapResolution=1, dataFormat=ext, assetId=md5, md5ext=md5 + '.' + ext,
                rotationCenterX=cx, rotationCenterY=cy)

def _sound_entry(name, assets, files):
    data, n, rate = assets.wav(name)
    md5 = hashlib.md5(data).hexdigest()
    files[md5 + '.wav'] = data
    return dict(name=name, assetId=md5, dataFormat='wav', format='', rate=rate, sampleCount=n, md5ext=md5 + '.wav')

def write_sprite3(path, name, costumes, sounds, assets):
    """Objeto suelto (.sprite3) sin programas, para importar con «Subir objeto»."""
    files = {}
    target = dict(isStage=False, name=name, variables={}, lists={}, broadcasts={}, blocks={}, comments={},
                  currentCostume=0, costumes=[_costume_entry(c, assets, files) for c in costumes],
                  sounds=[_sound_entry(s, assets, files) for s in sounds], volume=100, visible=True,
                  x=0, y=0, size=100, direction=90, draggable=False, rotationStyle='all around')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('sprite.json', json.dumps(target, ensure_ascii=False))
        for fn, data in files.items():
            z.writestr(fn, data)

def template_of(p):
    """Copia del proyecto con los mismos objetos y fondos pero sin programas ni variables."""
    sprites = [Sprite(s.name, s.costumes, [], x=s.x, y=s.y, size=s.size, direction=s.direction, visible=True,
                      sounds=s.sounds, rotation=s.rotation) for s in p.sprites]
    return Project(p.backdrops, sprites, stage_sounds=p.stage_sounds)
