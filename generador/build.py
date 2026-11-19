# -*- coding: utf-8 -*-
import os, re, shutil, json, html, zipfile, sys
sys.path.insert(0, os.path.dirname(__file__))
import common
from common import PAGES, PROJECTS, e, P, ul, box
import c_empezar, c_conoce, c_comenzamos, c_errores, c_experto, c_talleres, c_efemerides, c_saber
import tarjetas, pixel, robit
from sb import write_sprite3
from c_experto import GROUPS
from assets import Assets

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('SALIDA', os.path.join(HERE, '..', '_salida'))
SITE = OUT + '/web'
EXE = OUT + '/paquete-exe'
REPO = 'https://pablomoraga.github.io/scratch-en-el-aula/'
ASSETS = Assets()

SECTIONS = [
    ('empezar', '01', 'Para empezar', 'Qué es programar, lenguajes de texto y de bloques, qué es Scratch y cómo usar este material.'),
    ('conoce', '02', 'Conoce Scratch 3.0', 'El entorno, el escenario y todas las categorías de bloques con ejemplos cortos.'),
    ('comenzamos', '03', 'Comenzamos', '20 retos sencillos para hacer en clase o en casa.'),
    ('errores', '04', 'Encuentra el error', '10 proyectos con un fallo escondido para aprender a depurar como detectives.'),
    ('experto', '05', 'Modo experto', '40 retos en 8 bloques: juegos, historias, arte, música, Makey Makey, micro:bit, realidad aumentada y ciencia.'),
    ('talleres', '06', 'Talleres', '3 talleres de club y 8 de efemérides (Halloween, Navidad, Día de la Paz, Carnaval, Día de Andalucía, Día del Libro, Medio Ambiente y fin de curso), de una hora cada uno.'),
    ('saber', '07', 'Para saber más', 'Plantillas, objetos, fondos y sonidos para el alumnado, glosario, rúbrica de evaluación y enlaces.'),
]
SEC_TITLE = {s[0]: s[2] for s in SECTIONS}
SEC_INTRO = {
    'empezar': P('Antes de tocar un bloque, conviene saber qué es programar y por qué usamos Scratch. Este apartado está pensado tanto para el alumnado como para el profesorado.'),
    'conoce': P('Un recorrido por todo Scratch 3.0. Cada página tiene una tabla con los bloques más importantes y ejemplos muy cortos que puedes descargar y abrir.'),
    'comenzamos': P('Veinte retos ordenados de menos a más. Cada uno se hace en 10-20 minutos y tiene pistas y una solución descargable. '
                    'Están pensados para Primaria, pero sirven como calentamiento en ESO.'),
    'errores': P('Cada reto es un proyecto que <b>no funciona bien</b>. Descárgalo, descubre qué falla y arréglalo. '
                 'Encontrar y corregir errores (depurar) es una de las habilidades más importantes de la programación. '
                 'Se pueden hacer después de Comenzamos o intercalados con sus retos.'),
    'experto': P('Cuarenta retos organizados en ocho bloques temáticos. Algunos necesitan materiales (Makey Makey, micro:bit o cámara web): '
                 'lo encontrarás indicado en cada bloque.'),
    'saber': P('Recursos para trabajar en clase y para seguir aprendiendo: los materiales de los retos de Comenzamos listos para repartir, '
               'un glosario, una rúbrica de evaluación y enlaces recomendados.'),
    'talleres': P('Talleres cerrados de una hora, con guion por tiempos, fases y proyecto terminado. Los tres primeros están pensados para un club de robótica, '
                  'una jornada de puertas abiertas o una clase magistral en un museo de ciencia. En <b>Efemérides</b> tienes ocho más para celebrar fechas especiales del curso.'),
}
GROUP_INFO = {g[1]: g for g in GROUPS}

# ------------------------------------------------------------------ árbol de páginas
def slugify(t):
    t = t.lower()
    for a, b in zip('áéíóúñü', 'aeiounu'): t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

tree = []   # (section, [items]) item = page or ('group', title, slug, [pages])
for sid, num, title, _ in SECTIONS:
    items = []
    groups = {}
    for p in [p for p in PAGES if p['section'] == sid]:
        if p['group']:
            if p['group'] not in groups:
                g = dict(kind='group', title=p['group'], slug=slugify(p['group']), pages=[], section=sid)
                groups[p['group']] = g
                items.append(g)
            groups[p['group']]['pages'].append(p)
        else:
            items.append(p)
    tree.append((sid, items))

# orden plano para anterior/siguiente
flat = []
for sid, items in tree:
    flat.append(dict(kind='section', section=sid, slug='index', title=SEC_TITLE[sid]))
    for it in items:
        if it.get('kind') == 'group':
            flat.append(dict(kind='groupidx', section=sid, slug=it['slug'], title=it['title'], group=it))
            flat.extend(it['pages'])
        else:
            flat.append(it)

def href(p, frm_root=False):
    pre = '' if frm_root else '../'
    return '%s%s/%s.html' % (pre, p['section'], p['slug'])

# ------------------------------------------------------------------ estilos
CAT = {'motion': '#4C97FF', 'looks': '#9966FF', 'sound': '#CF63CF', 'events': '#FFBF00', 'control': '#FFAB19', 'sensing': '#5CB1D6',
       'operators': '#59C059', 'variables': '#FF8C1A', 'lists': '#FF661A', 'myblocks': '#FF6680', 'pen': '#0FBD8C', 'music': '#0FBD8C',
       'video': '#0FBD8C', 'tts': '#0FBD8C', 'translate': '#0FBD8C', 'makey': '#0FBD8C', 'microbit': '#0FBD8C'}
HEX = 'clip-path:polygon(9px 0,calc(100% - 9px) 0,100% 50%,calc(100% - 9px) 100%,9px 100%,0 50%);'
STY = {
    'sb-wrap': 'margin:12px 0;',
    'sb-group': 'border:1px dashed #b9ad97;border-radius:8px;padding:8px 10px 4px;margin:8px 0;background:#fffdf8;',
    'sb-owner': 'font:700 11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:#7a6f5c;margin-bottom:4px;',
    'sb-scripts': 'display:flex;flex-wrap:wrap;align-items:flex-start;gap:4px 18px;',
    'sb-script': 'display:inline-flex;flex-direction:column;align-items:flex-start;margin:4px 0 8px;font:700 13px/1.25 Helvetica,Arial,sans-serif;color:#fff;',
    'sb-solo': 'margin:2px 0;',
    'sb-blk': 'display:inline-flex;flex-wrap:wrap;align-items:center;gap:5px;padding:6px 10px;border-radius:5px;margin:0 0 1px;min-height:20px;border:1px solid rgba(0,0,0,.18);color:#fff;',
    'sb-hat': 'border-radius:18px 18px 5px 5px;padding-top:11px;',
    'sb-cap': 'border-bottom-left-radius:10px;border-bottom-right-radius:10px;',
    'sb-def': 'border-radius:18px 18px 5px 5px;',
    'sb-c': 'display:flex;flex-direction:column;align-items:stretch;border-radius:5px;margin:0 0 1px;border:1px solid rgba(0,0,0,.18);color:#fff;',
    'sb-line': 'display:flex;flex-wrap:wrap;align-items:center;gap:5px;padding:6px 10px;',
    'sb-in': 'display:flex;flex-direction:column;align-items:flex-start;margin-left:14px;min-height:14px;padding:1px 0;background:#fffdf8;',
    'sb-cend': 'height:10px;',
    'sb-num': 'display:inline-block;background:#fff;color:#575e75;border-radius:10px;padding:2px 8px;font-weight:500;',
    'sb-txt': 'display:inline-block;background:#fff;color:#575e75;border-radius:3px;padding:2px 6px;font-weight:500;',
    'sb-menu': 'display:inline-block;background:rgba(0,0,0,.16);border-radius:10px;padding:2px 8px;',
    'sb-rep': 'display:inline-flex;align-items:center;gap:4px;border-radius:12px;padding:3px 8px;border:1px solid rgba(0,0,0,.2);color:#fff;',
    'sb-boolb': 'display:inline-flex;align-items:center;gap:4px;padding:3px 14px;color:#fff;' + HEX,
    'sb-bool-empty': 'display:inline-block;width:34px;height:18px;background:rgba(0,0,0,.2);' + HEX,
    'sb-color': 'display:inline-block;width:20px;height:14px;border:2px solid #fff;border-radius:3px;',
    'sb-matrix': 'display:inline-grid;grid-template-columns:repeat(5,6px);gap:1px;background:#fff;padding:2px;border-radius:3px;',
    'm0': 'display:block;width:6px;height:6px;background:#ddd;', 'm1': 'display:block;width:6px;height:6px;background:#e33;',
    'flag': 'vertical-align:middle;',
    # contenido
    'caja': 'border-left:5px solid #e85d2a;background:#fff6ec;border-radius:6px;padding:10px 14px;margin:16px 0;',
    'caja-idea': 'border-left-color:#f2b134;background:#fffaeb;', 'caja-ojo': 'border-left-color:#d7263d;background:#fff1f1;',
    'caja-docente': 'border-left-color:#2f9e57;background:#effaf2;', 'caja-reto': 'border-left-color:#3d8bd6;background:#eef6ff;',
    'caja-sabias': 'border-left-color:#9966ff;background:#f5f0ff;',
    'caja-t': 'font-weight:700;margin:0 0 6px;',
    'tabla': 'border-collapse:collapse;width:100%;margin:12px 0;font-size:.95em;',
    'tabla-bloques': 'border-collapse:collapse;width:100%;margin:12px 0;font-size:.95em;',
    'ficha': 'display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px;',
    'chip': 'display:inline-block;font:600 12px/1 ui-monospace,Menlo,Consolas,monospace;padding:6px 9px;border:1.5px solid #1f1b16;border-radius:20px;background:#fff;',
    'chip-c': 'border-color:#b9ad97;background:#f3ecdf;',
    'objetivo': 'font-size:1.05em;background:#fff;border:1.5px solid #1f1b16;border-radius:8px;padding:10px 14px;box-shadow:3px 3px 0 #1f1b16;',
    'ayuda': 'border:1.5px solid #1f1b16;border-radius:8px;padding:8px 12px;margin:12px 0;background:#fff;',
    'btn-dl': 'display:inline-block;background:#e85d2a;color:#fff;font-weight:700;text-decoration:none;padding:8px 14px;border-radius:6px;border:1.5px solid #1f1b16;box-shadow:2px 2px 0 #1f1b16;',
    'dl-hint': 'font-size:.85em;color:#6a604f;margin-left:6px;',
    'dl': 'margin:10px 0;',
    'ejemplo': 'border-top:1px solid #d9cfbd;padding-top:6px;margin-top:18px;',
    'comparar': 'display:flex;flex-wrap:wrap;gap:20px;', 'comparar-t': 'font:700 12px/1 ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.06em;color:#7a6f5c;margin:10px 0 4px;',
    'recursos': 'display:flex;flex-wrap:wrap;gap:12px;margin:10px 0;',
    'recurso': 'display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;background:#fff;border:1.5px solid #1f1b16;border-radius:10px;padding:10px;min-width:120px;',
    'codigo': 'background:#1f1b16;color:#f3ecdf;padding:12px 14px;border-radius:8px;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;overflow:auto;',
}
for c, col in CAT.items():
    STY['c-' + c] = 'background:%s;' % col

ENT = '''.entorno{display:grid;grid-template-columns:70px 150px 1fr 240px;grid-template-rows:34px 30px 34px 150px 90px 40px;gap:4px;font:600 12px/1.25 system-ui,sans-serif;margin:14px 0;max-width:760px}
.entorno .z{border:1.5px solid #1f1b16;border-radius:6px;padding:6px;background:#fff}
.entorno b{display:inline-block;background:#e85d2a;color:#fff;border-radius:50%;width:18px;height:18px;text-align:center;line-height:18px;margin-right:4px}
.z-menu{grid-column:1/5;background:#855cd6!important;color:#fff}.z-tabs{grid-column:1/4}.z-stagebar{grid-column:4}
.z-cat{grid-row:3/7;grid-column:1}.z-pal{grid-row:3/7;grid-column:2;background:#f9f9f9!important}.z-code{grid-row:3/7;grid-column:3;background:#f9f9f9!important}
.z-stage{grid-row:3/5;grid-column:4;background:#e8f4ff!important}.z-sprites{grid-row:5;grid-column:4}.z-back{grid-row:6;grid-column:4}
.z-ext{grid-row:7;grid-column:1/3;background:#4c97ff!important;color:#fff}'''
ENT_INLINE = {}  # el esquema del entorno se convierte en tabla en el paquete eXe

def inline(htmltxt):
    def rep(m):
        classes = m.group(1).split()
        st = ''.join(STY.get(c, '') for c in classes)
        return 'class="%s"%s' % (m.group(1), (' style="%s"' % st) if st else '')
    from sb import FLAG
    htmltxt = htmltxt.replace(FLAG, '<span style="color:#3f9e47;font-weight:900;">⚑</span>')
    out = re.sub(r'class="([^"]*)"', rep, htmltxt)
    out = out.replace('<td>', '<td style="border:1px solid #d9cfbd;padding:6px 8px;vertical-align:top;">')
    out = out.replace('<th>', '<th style="border:1px solid #d9cfbd;padding:6px 8px;background:#f3ecdf;text-align:left;">')
    out = out.replace('<summary>', '<summary style="cursor:pointer;font-weight:700;">')
    return out

ENTORNO_TABLE = ('<table class="tabla"><tbody>'
                 '<tr><td colspan="3" style="background:#855cd6;color:#fff">1 · Menú (Archivo, Editar, Tutoriales, idioma)</td></tr>'
                 '<tr><td colspan="2">2 · Pestañas Código / Disfraces / Sonidos</td><td>6 · Bandera verde, detener, tamaño</td></tr>'
                 '<tr><td>3 · Categorías<br><br>4 · Paleta de bloques</td><td style="background:#f9f9f9">5 · Área de programación</td>'
                 '<td style="background:#e8f4ff">7 · Escenario (480 × 360)<br><br>8 · Objetos<br>9 · Fondos</td></tr>'
                 '<tr><td colspan="3" style="background:#4c97ff;color:#fff">10 · Botón de extensiones (abajo a la izquierda)</td></tr></tbody></table>')

# ------------------------------------------------------------------ cuerpo de páginas especiales
def card_list(pages, pre):
    out = '<div class="cards">'
    for p in pages:
        m = p.get('meta', {})
        tag = ('Reto %s · %s · %s' % (m['num'], common.NIVEL[m['nivel']], m['tiempo'])) if p.get('kind') == 'reto' else (
            'Taller · 60 min' if p.get('kind') == 'taller' else SEC_TITLE[p['section']])
        out += '<a class="card" href="%s%s.html"><span class="card-tag">%s</span><span class="card-t">%s</span></a>' % (pre, p['slug'], e(tag), e(p['title']))
    return out + '</div>'

def section_body(sid, items, for_exe=False):
    body = SEC_INTRO[sid]
    if for_exe: return body + ul([e(it['title']) for it in items])
    pages = []
    for it in items:
        if it.get('kind') == 'group':
            pages.append(dict(slug=it['slug'], title=it['title'], kind='grupo', section=sid, meta={}))
        else:
            pages.append(it)
    out = body + '<div class="cards">'
    for p in pages:
        if p['kind'] == 'grupo':
            g = [x for x in items if x.get('kind') == 'group' and x['slug'] == p['slug']][0]
            tag = '%d %s' % (len(g['pages']), {'experto': 'retos', 'talleres': 'talleres'}.get(sid, 'páginas'))
        elif p.get('kind') == 'reto':
            m = p['meta']; tag = 'Reto %s · %s · %s' % (m['num'], common.NIVEL[m['nivel']], m['tiempo'])
        elif p.get('kind') == 'taller':
            tag = 'Taller · 60 min'
        else:
            tag = 'Lectura'
        out += '<a class="card" href="%s.html"><span class="card-tag">%s</span><span class="card-t">%s</span></a>' % (p['slug'], e(tag), e(p['title']))
    return out + '</div>'

def group_body(g, for_exe=False):
    info = GROUP_INFO.get(g['title'])
    body = ''
    if info:
        body += P(info[2])
        if info[3]: body += box('ojo', 'Antes de empezar necesitas', ul(info[3]))
    elif g['title'] == 'Efemérides':
        body += P('Ocho talleres de una hora para celebrar fechas del curso con un proyecto de Scratch vistoso: Halloween, Navidad, Día de la Paz, '
                  'Carnaval, Día de Andalucía, Día del Libro, Día del Medio Ambiente y fin de curso. Cada uno trae guion por tiempos, fases, '
                  'proyecto terminado y adaptaciones para Primaria y ESO.')
    else:
        body += P('Una página por cada categoría de bloques, con su color, sus bloques principales y ejemplos.')
    if for_exe: return body + ul([e(p['title']) for p in g['pages']])
    return body + card_list(g['pages'], '')

# ------------------------------------------------------------------ plantilla web
def nav_html(cur):
    out = '<nav class="side"><a class="side-home" href="../index.html">Inicio</a>'
    for sid, num, title, _ in SECTIONS:
        open_ = cur and cur['section'] == sid
        out += '<details%s><summary><span class="num">%s</span> %s</summary><ul>' % (' open' if open_ else '', num, e(title))
        out += '<li><a href="../%s/index.html"%s>Presentación</a></li>' % (sid, ' class="on"' if cur and cur['section'] == sid and cur['slug'] == 'index' else '')
        for it in dict(tree)[sid]:
            if it.get('kind') == 'group':
                gopen = cur and (cur.get('group') == it['title'] or cur.get('group') is it)
                out += '<li><details%s><summary>%s</summary><ul><li><a href="../%s/%s.html">Introducción</a></li>' % (
                    ' open' if gopen else '', e(it['title']), sid, it['slug'])
                for p in it['pages']:
                    out += '<li><a href="../%s/%s.html"%s>%s</a></li>' % (sid, p['slug'], ' class="on"' if cur is p else '', e(label(p)))
                out += '</ul></details></li>'
            else:
                out += '<li><a href="../%s/%s.html"%s>%s</a></li>' % (sid, it['slug'], ' class="on"' if cur is it else '', e(label(it)))
        out += '</ul></details>'
    return out + '</nav>'

def label(p):
    if p.get('kind') == 'reto': return '%s · %s' % (p['meta']['num'], p['title'])
    return p['title']

HEADER = '''<header class="top"><a class="brand" href="{root}index.html"><img src="{root}img/robit-icono.svg" alt="" width="22" height="22"> Pablo Moraga <span>· Scratch en el aula</span></a>
<nav class="topnav">{links}</nav></header>'''
FOOTER = '''<footer class="foot"><p>© Pablo Moraga · Contenidos con licencia <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es" target="_blank" rel="noopener">CC BY-NC-ND 4.0</a> · <a href="https://github.com/pablomoraga" target="_blank" rel="noopener">github.com/pablomoraga</a></p>
<p class="small">Puedes compartir este material, sus proyectos y sus recursos tal cual, sin modificarlos, sin fines comerciales y citando siempre a su autor, Pablo Moraga.</p>
<p class="small">Scratch es un proyecto de la Fundación Scratch en colaboración con el grupo Lifelong Kindergarten del MIT Media Lab. Está disponible gratis en <a href="https://scratch.mit.edu" target="_blank" rel="noopener">scratch.mit.edu</a>. Este material es independiente y no está vinculado a la Fundación Scratch.</p></footer>'''

def doc(title, body, root, cur=None, prevnext=''):
    links = ''.join('<a href="%s%s/index.html">%s</a>' % (root, sid, e(t)) for sid, _, t, _ in SECTIONS)
    side = nav_html(cur) if cur is not None else ''
    main_cls = 'with-side' if side else 'home'
    return ('<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s · Scratch en el aula</title><link rel="icon" href="%simg/robit-icono.svg"><link rel="stylesheet" href="%scss/estilo.css"></head><body>%s'
            '<div class="layout %s">%s<main>%s%s</main></div>%s<script src="%sjs/app.js"></script></body></html>') % (
        e(title), root, root, HEADER.format(root=root, links=links), main_cls, side, body, prevnext, FOOTER, root)

def crumbs(p):
    out = '<p class="crumbs"><a href="../index.html">Inicio</a> › <a href="index.html">%s</a>' % e(SEC_TITLE[p['section']])
    if isinstance(p.get('group'), str):
        out += ' › <a href="%s.html">%s</a>' % (slugify(p['group']), e(p['group']))
    return out + '</p>'

def prevnext(i):
    out = '<div class="pn">'
    if i > 0:
        q = flat[i - 1]; out += '<a class="pn-prev" href="../%s/%s.html">← %s</a>' % (q['section'], q['slug'], e(q['title']))
    else: out += '<span></span>'
    if i < len(flat) - 1:
        q = flat[i + 1]; out += '<a class="pn-next" href="../%s/%s.html">%s →</a>' % (q['section'], q['slug'], e(q['title']))
    return out + '</div>'

def sb3url(for_exe): return (REPO + 'sb3/') if for_exe else '../sb3/'
def resurl(for_exe): return (REPO + 'recursos/') if for_exe else '../recursos/'

def page_body(p, for_exe=False):
    if p['kind'] == 'section':
        return section_body(p['section'], dict(tree)[p['section']], for_exe)
    if p['kind'] == 'groupidx':
        return group_body(p['group'], for_exe)
    b = p['body']
    if for_exe:
        b = re.sub(r'<div class="entorno">.*?</div>\n</div>', ENTORNO_TABLE, b, flags=re.S)
    import urllib.parse
    b = re.sub(r'data-src="\{\{PLAY\}\}([^"]+)"', lambda m: 'data-src="https://turbowarp.org/embed?project_url=%s"' % urllib.parse.quote(REPO + 'sb3/' + m.group(1), safe=''), b)
    return b.replace('{{SB3}}', sb3url(for_exe)).replace('{{RES}}', resurl(for_exe))

# ------------------------------------------------------------------ construir
def build():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(SITE + '/sb3'); os.makedirs(SITE + '/css'); os.makedirs(SITE + '/js')
    # sb3
    for name, proj in PROJECTS.items():
        proj.to_sb3('%s/sb3/%s.sb3' % (SITE, name), ASSETS)
    build_resources()
    # css
    css = open(os.path.join(os.path.dirname(__file__), 'estilo.css'), encoding='utf-8').read()
    css += '\n' + ENT + '\n' + ''.join('.%s{%s}\n' % (k, v) for k, v in STY.items())
    open(SITE + '/css/estilo.css', 'w', encoding='utf-8').write(css)
    shutil.copy(os.path.join(os.path.dirname(__file__), 'app.js'), SITE + '/js/app.js')
    # imagen del proyecto
    os.makedirs(SITE + '/img')
    open(SITE + '/img/robit.svg', 'w').write(pixel.svg(robit.ROBIT2, px=4)['data'])
    open(SITE + '/img/robit-icono.svg', 'w').write(pixel.svg(robit.ROBIT1[:17], px=4)['data'])
    l1 = pixel.text_rows('APRENDE SCRATCH', fg='Y', shadow='K'); l2 = pixel.text_rows('CON ROBIT', fg='B', shadow='K')
    g = ['.' * (29 + len(l1[0]) + 1) for _ in range(30)]
    g = pixel.put(g, 0, 0, robit.ROBIT2); g = pixel.put(g, 28, 8, l1); g = pixel.put(g, 28, 19, l2)
    open(SITE + '/img/logo.svg', 'w').write(pixel.svg(g, px=4)['data'])
    pixel.png(g, SITE + '/img/logo.png', px=6)
    # portada
    cards = ''.join('<a class="card big" href="%s/index.html"><span class="card-tag">%s</span><span class="card-t">%s</span><span class="card-d">%s</span></a>'
                    % (sid, num, e(t), e(d)) for sid, num, t, d in SECTIONS)
    nret = sum(1 for p in PAGES if p['kind'] == 'reto')
    home = ('<section class="hero"><div class="hero-txt"><p class="kicker">Programación creativa · Primaria y ESO</p><h1>Scratch <em>en el aula</em></h1>'
            '<p class="tagline">Aprende Scratch con Robit</p>'
            '<p class="lead">Un manual propio y sintético para aprender a programar con Scratch 3.0: del primer bloque a juegos, música, '
            'Makey Makey, micro:bit y realidad aumentada.</p><p><a class="btn" href="empezar/index.html">Empezar ↓</a> '
            '<a class="btn btn2" href="comenzamos/index.html">Ir a los retos</a></p>'
            '<div class="stats"><span><b>%d</b> retos</span><span><b>11</b> talleres</span><span><b>%d</b> archivos .sb3</span></div></div>'
            '<img class="hero-robit" src="img/robit.svg" alt="Robit, la mascota del proyecto, saludando" width="192" height="240"></section>'
            '<section class="home-sec"><h2><span class="num">00</span> Contenidos</h2><div class="cards">%s</div></section>'
            '<section class="home-sec"><h2><span class="num">→</span> Para el profesorado</h2>%s</section>') % (
        nret, len(PROJECTS), cards,
        P('Todos los retos incluyen pistas y un archivo <b>.sb3</b> de ayuda que se abre en Scratch con <b>Archivo › Cargar desde tu ordenador</b>. '
          'Robit y el resto de personajes, fondos y sonidos son originales: se pueden usar libremente en clase y cambiar por los del alumnado.'))
    open(SITE + '/index.html', 'w', encoding='utf-8').write(doc('Inicio', home, '', None))
    # páginas
    for i, p in enumerate(flat):
        d = SITE + '/' + p['section']
        os.makedirs(d, exist_ok=True)
        head = ('<p class="crumbs"><a href="../index.html">Inicio</a></p>' if p['kind'] == 'section' else crumbs(p))
        title = p['title']
        body = head + '<h1>%s</h1>' % e(title) + page_body(p)
        open('%s/%s.html' % (d, p['slug']), 'w', encoding='utf-8').write(doc(title, body, '../', p, prevnext(i)))
    est = os.path.join(HERE, 'estaticos')          # archivos propios (fotos, PDF...) que se copian tal cual
    if os.path.isdir(est):
        shutil.copytree(est, SITE, dirs_exist_ok=True)
    open(SITE + '/.nojekyll', 'w').close()
    if os.environ.get('EXE'): build_exe()

def build_resources():
    R = common.RESOURCES
    base = SITE + '/recursos'
    for d in ('plantillas', 'objetos', 'fondos', 'sonidos'):
        os.makedirs(base + '/' + d)
    for name, proj in R['plantillas'].items():
        proj.to_sb3('%s/plantillas/%s.sb3' % (base, name), ASSETS)
    for name, (cos, snd) in R['sprites'].items():
        write_sprite3('%s/objetos/%s.sprite3' % (base, name.lower()), name, cos, snd, ASSETS)
        for c in cos:
            data, ext, _, _ = ASSETS.image(c)
            open('%s/objetos/%s.%s' % (base, c, ext), 'wb').write(data)
    for f in R['fondos']:
        data, ext, _, _ = ASSETS.image(f)
        open('%s/fondos/%s.%s' % (base, f, ext), 'wb').write(data)
    for snd in R['sonidos']:
        open('%s/sonidos/%s.wav' % (base, snd), 'wb').write(ASSETS.wav(snd)[0])
    # llavero
    os.makedirs(base + '/llavero')
    shutil.copy(os.path.join(HERE, 'llavero', 'robit-llavero.stl'), base + '/llavero/robit-llavero.stl')
    shutil.copy(os.path.join(HERE, 'llavero', 'robit-llavero-vista.png'), base + '/llavero/robit-llavero-vista.png')
    # tarjetas
    projs = dict(PROJECTS)
    for r in common.RETOS:
        if r['section'] == 'errores': projs[r['slug']] = PROJECTS[r['slug'] + '-solucion']
    for sec, name in (('comenzamos', 'tarjetas-comenzamos'), ('errores', 'tarjetas-encuentra-el-error')):
        tarjetas.build_pdf([r for r in common.RETOS if r['section'] == sec], projs, inline, base + '/' + name + '.pdf', '/tmp/tarjetas')
    with zipfile.ZipFile(base + '/recursos-comenzamos.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(base):
            for fn in files:
                if fn.endswith('.zip') or 'llavero' in root or 'encuentra' in fn: continue
                full = os.path.join(root, fn)
                z.write(full, 'recursos-comenzamos/' + os.path.relpath(full, base))

def build_exe():
    os.makedirs(EXE, exist_ok=True)
    lines = ['# Estructura para eXeLearning', '',
             'Cada carpeta es una página del árbol de eXe (el número indica el orden y la sangría, el nivel).',
             'En cada página: añade un iDevice de **Texto**, pulsa el botón **Código fuente** (<>) del editor y pega el contenido de `contenido.html`.',
             'Los enlaces a los .sb3 apuntan a %ssb3/ : sube la carpeta `sb3` a la raíz de ese repositorio.' % REPO, '']
    def write(path, title, body, depth):
        os.makedirs(path, exist_ok=True)
        open(path + '/contenido.html', 'w', encoding='utf-8').write('<!-- Página eXe: %s -->\n%s\n' % (title, inline(body)))
        lines.append('%s- %s  →  `%s/contenido.html`' % ('  ' * depth, title, os.path.relpath(path, EXE)))
    for si, (sid, num, title, _) in enumerate(SECTIONS):
        sdir = '%s/%s-%s' % (EXE, num, slugify(title))
        write(sdir, title, page_body(dict(kind='section', section=sid, slug='index', title=title), True), 0)
        for j, it in enumerate(dict(tree)[sid], 1):
            if it.get('kind') == 'group':
                gdir = '%s/%02d-%s' % (sdir, j, it['slug'])
                write(gdir, it['title'], group_body(it, True), 1)
                for k, p in enumerate(it['pages'], 1):
                    write('%s/%02d-%s' % (gdir, k, p['slug']), label(p), page_body(p, True), 2)
            else:
                write('%s/%02d-%s' % (sdir, j, it['slug']), label(it), page_body(it, True), 1)
    shutil.copytree(SITE + '/sb3', EXE + '/sb3')
    shutil.copytree(SITE + '/recursos', EXE + '/recursos')
    open(EXE + '/LEEME.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    build()
    print('páginas', len(flat), 'proyectos', len(PROJECTS))
