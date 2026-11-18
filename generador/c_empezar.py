# -*- coding: utf-8 -*-
from common import *

SEC = 'empezar'

# 1 ---------------------------------------------------------------------------
page(SEC, 'que-es-programar', '¿Qué es programar?', P(
    'Programar es <b>dar instrucciones a una máquina</b> para que haga lo que queremos. Esas instrucciones tienen que ser '
    '<b>claras, ordenadas y sin dudas</b>, porque el ordenador no adivina: hace exactamente lo que le decimos, ni más ni menos.',
    'A una lista de pasos ordenados que resuelve un problema la llamamos <b>algoritmo</b>. Usamos algoritmos todos los días '
    'sin darnos cuenta: una receta, las instrucciones para montar un mueble o el camino de casa al cole.') +
    '<h3>Un algoritmo de la vida diaria: lavarse los dientes</h3>' +
    ol(['Coger el cepillo.', 'Poner pasta.', 'Repetir: cepillar arriba y abajo durante dos minutos.', 'Enjuagar la boca.',
        'Si el cepillo está sucio, lavarlo.', 'Guardar el cepillo.']) +
    P('En esta lista ya aparecen tres ideas muy importantes de la programación: <b>secuencia</b> (el orden de los pasos), '
      '<b>repetición</b> (hacer algo varias veces) y <b>condición</b> (hacer algo solo si se cumple algo).') +
    box('docente', 'Actividad desenchufada: el robot humano (10 min)', P(
        'Por parejas: una persona es el «robot» y la otra la «programadora». El robot solo entiende tres órdenes: '
        '<i>avanza un paso</i>, <i>gira a la derecha</i> y <i>gira a la izquierda</i>. La programadora escribe en un papel '
        'las órdenes para llegar hasta un objeto del aula. Después se prueba el programa y, si falla, se corrige. '
        'Acabáis de <b>programar</b> y de <b>depurar</b> sin ordenador.')) +
    box('sabias', '¿Sabías que…?', P('A los fallos de un programa se les llama <i>bugs</i> («bichos» en inglés), '
                                      'y a buscarlos y arreglarlos se le llama <b>depurar</b>.')))

# 2 ---------------------------------------------------------------------------
cuenta = Project(['blanco'], [Sprite('Robit', ['robit1'], [[flag(), setv('cuenta', 10),
    rep(10, say(v('cuenta'), 1), chv('cuenta', -1)), say('¡Despegue!', 2)]])], variables=['cuenta'], shown=['cuenta'])
PROJECTS['ej-cuenta-atras'] = cuenta
page(SEC, 'lenguajes', 'Lenguajes de programación: texto y bloques', P(
    'Para hablar con un ordenador usamos un <b>lenguaje de programación</b>: un idioma con palabras y reglas muy estrictas. '
    'Hay muchos: Python, JavaScript, C++, Java… La mayoría se escriben con <b>texto</b>, y un punto o una coma mal puestos '
    'hacen que el programa no funcione. A esas reglas de escritura se les llama <b>sintaxis</b>.',
    'Los lenguajes <b>por bloques</b>, como Scratch, cambian el teclado por piezas que encajan como un puzle. '
    'Cada pieza es una instrucción y solo encaja donde tiene sentido, así que es imposible cometer errores de escritura '
    'y podemos centrarnos en lo importante: <b>pensar la solución</b>.') +
    '<h3>El mismo programa en tres lenguajes</h3>' +
    P('Una cuenta atrás del 10 al 1 que termina diciendo «¡Despegue!»:') +
    '<div class="comparar"><div><p class="comparar-t">Scratch (bloques)</p>%s%s</div>' % (code(cuenta), dl('ej-cuenta-atras', 'Descargar ejemplo (.sb3)')) +
    '<div><p class="comparar-t">Python (texto)</p><pre class="codigo">cuenta = 10\nfor i in range(10):\n    print(cuenta)\n    cuenta = cuenta - 1\nprint("¡Despegue!")</pre>'
    '<p class="comparar-t">JavaScript (texto)</p><pre class="codigo">let cuenta = 10;\nfor (let i = 0; i &lt; 10; i++) {\n  console.log(cuenta);\n  cuenta = cuenta - 1;\n}\nconsole.log("¡Despegue!");</pre></div></div>' +
    P('Fíjate en que los tres hacen lo mismo y tienen la misma estructura: una variable, una repetición de 10 veces y un mensaje final. '
      'Lo que cambia es <b>cómo se escribe</b>. Por eso, quien aprende a pensar con bloques tiene ya mucho camino recorrido para '
      'pasar después a un lenguaje de texto.') +
    '<h3>Bloques frente a texto</h3><table class="tabla"><thead><tr><th></th><th>Bloques</th><th>Texto</th></tr></thead><tbody>'
    '<tr><td>Cómo se escribe</td><td>Arrastrando y encajando piezas</td><td>Tecleando palabras y símbolos</td></tr>'
    '<tr><td>Errores de escritura</td><td>No hay: las piezas solo encajan donde deben</td><td>Frecuentes (comas, paréntesis, mayúsculas)</td></tr>'
    '<tr><td>Qué hay disponible</td><td>Se ve todo en la paleta de bloques</td><td>Hay que conocer o buscar las instrucciones</td></tr>'
    '<tr><td>Ideal para</td><td>Empezar, aprender conceptos, prototipos rápidos</td><td>Programas grandes y uso profesional</td></tr>'
    '</tbody></table>' +
    box('sabias', 'Otros entornos de bloques que te sonarán', ul([
        '<b>ScratchJr</b>: versión para tablet pensada para 5-7 años.',
        '<b>MakeCode</b>: de Microsoft, para micro:bit y otras placas; permite pasar de bloques a JavaScript o Python.',
        '<b>MicroBlocks</b>, <b>mBlock</b> o <b>Snap!</b>: bloques para robótica y para programación más avanzada.'])))

# 3 ---------------------------------------------------------------------------
page(SEC, 'que-es-scratch', '¿Qué es Scratch?', P(
    '<b>Scratch</b> es un lenguaje de programación por bloques y una comunidad en línea, <b>gratuitos</b>, creados por el grupo '
    '<i>Lifelong Kindergarten</i> del MIT Media Lab. Hoy lo mantiene la <b>Fundación Scratch</b>. Con Scratch se pueden crear '
    'historias interactivas, juegos, animaciones, música y arte, y compartirlos con personas de todo el mundo.',
    'Está pensado sobre todo para personas de <b>8 a 16 años</b>, pero lo usan desde Primaria hasta la universidad. '
    'Para edades más tempranas existe <b>ScratchJr</b>.') +
    '<h3>Un poco de historia</h3><table class="tabla"><tbody>'
    '<tr><td><b>2007</b></td><td>Se publica Scratch 1.0, un programa que se instalaba en el ordenador.</td></tr>'
    '<tr><td><b>2013</b></td><td>Llega Scratch 2.0 y se puede programar directamente en el navegador.</td></tr>'
    '<tr><td><b>2019</b></td><td>Se lanza Scratch 3.0 (enero): funciona en tablets, añade nuevas extensiones y un editor de sonidos y disfraces renovado.</td></tr>'
    '</tbody></table>' +
    '<h3>¿Dónde lo uso?</h3>' + ul([
        '<b>En línea</b>: en <a href="https://scratch.mit.edu" target="_blank" rel="noopener">scratch.mit.edu</a>, pulsando <b>Crear</b>. '
        'No hace falta cuenta para programar, pero sí para guardar en la nube y compartir.',
        '<b>Sin conexión</b>: con la aplicación de Scratch, que se descarga gratis desde '
        '<a href="https://scratch.mit.edu/download" target="_blank" rel="noopener">scratch.mit.edu/download</a>. Los proyectos se guardan en el ordenador como archivos <b>.sb3</b>.']) +
    box('docente', 'Para el profesorado', P(
        'Con una <b>cuenta de educador/a</b> de Scratch puedes crear clases y cuentas de alumnado sin necesidad de correo electrónico, '
        'y reunir sus proyectos en estudios. Recuerda al alumnado que no ponga datos personales (nombre completo, dirección, fotos) '
        'en los proyectos que comparta.')))

# 4 ---------------------------------------------------------------------------
page(SEC, 'pensamiento-computacional', 'Pensamiento computacional', P(
    'Programar con Scratch no es solo aprender a usar bloques: es aprender a <b>pensar de una manera ordenada para resolver problemas</b>. '
    'A esa forma de pensar se le llama <b>pensamiento computacional</b>. Un marco muy usado con Scratch (Brennan y Resnick, MIT) '
    'lo organiza en tres dimensiones:') +
    '<h3>1. Conceptos: lo que se aprende</h3><table class="tabla"><thead><tr><th>Concepto</th><th>Idea</th><th>En Scratch</th></tr></thead><tbody>'
    '<tr><td>Secuencia</td><td>Los pasos tienen un orden.</td><td>Bloques apilados de arriba abajo.</td></tr>'
    '<tr><td>Bucles</td><td>Repetir sin tener que escribir lo mismo muchas veces.</td><td><i>repetir</i>, <i>por siempre</i>.</td></tr>'
    '<tr><td>Eventos</td><td>Algo hace que otra cosa ocurra.</td><td><i>al hacer clic en la bandera</i>, <i>al presionar tecla</i>.</td></tr>'
    '<tr><td>Paralelismo</td><td>Varias cosas pasan a la vez.</td><td>Varios programas que empiezan con el mismo evento.</td></tr>'
    '<tr><td>Condicionales</td><td>Tomar decisiones.</td><td><i>si… entonces</i>, <i>si… si no</i>.</td></tr>'
    '<tr><td>Operadores</td><td>Cálculos y comparaciones.</td><td>+, −, &gt;, =, <i>número aleatorio</i>, <i>unir</i>.</td></tr>'
    '<tr><td>Datos</td><td>Guardar y usar información.</td><td>Variables y listas.</td></tr>'
    '</tbody></table>'
    '<h3>2. Prácticas: cómo se trabaja</h3>' + ul([
        '<b>Probar poco a poco</b>: construir un trozo, probarlo y seguir.',
        '<b>Depurar</b>: encontrar por qué algo no funciona y arreglarlo.',
        '<b>Reutilizar y remezclar</b>: partir de proyectos propios o ajenos (citando a quien los hizo).',
        '<b>Dividir en partes</b>: separar un proyecto grande en piezas pequeñas.']) +
    '<h3>3. Perspectivas: cómo cambia la mirada</h3>' + ul([
        '<b>Expresarse</b>: la tecnología sirve para crear, no solo para consumir.',
        '<b>Conectar</b>: se crea mejor con y para otras personas.',
        '<b>Preguntarse</b>: «¿cómo funcionará esto?» y «¿podría hacerlo yo?».']) +
    box('docente', 'En el aula', P('En cada reto de este material verás unas etiquetas con los conceptos que se trabajan. '
                                   'Te ayudarán a programar las sesiones y a evaluar.')))

# 5 ---------------------------------------------------------------------------
page(SEC, 'como-usar', 'Cómo usar este material', P(
    'El material está ordenado de menos a más. Puedes seguirlo de principio a fin o saltar al apartado que necesites.') +
    '<table class="tabla"><tbody>'
    '<tr><td><b>Para empezar</b></td><td>Qué es programar y qué es Scratch.</td></tr>'
    '<tr><td><b>Conoce Scratch 3.0</b></td><td>El entorno y todos los bloques, con ejemplos cortos.</td></tr>'
    '<tr><td><b>Comenzamos</b></td><td>20 retos sencillos para clase o casa.</td></tr>'
    '<tr><td><b>Encuentra el error</b></td><td>10 proyectos con un fallo escondido para aprender a depurar.</td></tr>'
    '<tr><td><b>Modo experto</b></td><td>40 retos en 8 bloques temáticos: juegos, historias, arte, música, Makey Makey, micro:bit, realidad aumentada y ciencia.</td></tr>'
    '<tr><td><b>Talleres</b></td><td>3 proyectos para hacer en una hora en un club o en una exposición.</td></tr>'
    '<tr><td><b>Para saber más</b></td><td>Plantillas, objetos y fondos para el alumnado, tarjetas imprimibles, el llavero 3D de Robit, glosario, evaluación y enlaces.</td></tr>'
    '</tbody></table>'
    '<h3>Cómo es cada reto</h3>' + ul([
        '<b>Ficha</b>: número, dificultad (★☆☆ a ★★★), tiempo aproximado y conceptos.',
        '<b>Paso a paso</b>: lo que hay que conseguir, sin dar los bloques.',
        '<b>Ayuda</b>: primero pistas y, si hace falta, una solución posible con su archivo <b>.sb3</b> descargable.',
        '<b>¿Y si…?</b>: ideas para ir más allá.']) +
    '<h3>Abrir un archivo .sb3</h3>' + ol([
        'Descarga el archivo desde el botón <b>⬇ Descargar</b>.',
        'Abre Scratch (en línea o la aplicación).',
        'Ve al menú <b>Archivo › Cargar desde tu ordenador</b> y elige el archivo.',
        'Para guardar tus cambios: <b>Archivo › Guardar en tu ordenador</b>.']) +
    box('ojo', 'Una solución, no la solución', P('En programación casi siempre hay varias formas correctas de resolver un problema. '
                                                 'Las soluciones que se ofrecen son solo un ejemplo.')) +
    box('docente', 'Consejos para dinamizar', ul([
        'Trabajo por parejas: una persona maneja el ratón y la otra «navega»; se cambian cada reto.',
        'Antes de pedir ayuda, «pregunta a tres»: a tu pareja, a otra pareja y a las pistas.',
        'Al terminar, una pareja enseña su proyecto y cuenta un error que tuvo y cómo lo arregló.',
        'Los recursos gráficos y sonidos de los archivos de ayuda son originales y sencillos; anima al alumnado a cambiarlos por los suyos.'])))
