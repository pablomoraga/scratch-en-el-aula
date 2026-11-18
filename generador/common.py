# -*- coding: utf-8 -*-
"""Registro de páginas y utilidades para escribir contenido."""
import html
from sb import r_block, render_project, Project, Sprite, used_categories
from dsl import *

PAGES = []      # cada página = dict(section, group, slug, title, body, kind, meta)
PROJECTS = {}   # nombre_archivo -> Project
RETOS = []      # datos estructurados de cada reto (para las tarjetas)
RESOURCES = {}
e = html.escape

def page(section, slug, title, body, group=None, kind='texto', meta=None):
    PAGES.append(dict(section=section, slug=slug, title=title, body=body, group=group, kind=kind, meta=meta or {}))

def dl(name, label='Descargar ayuda (.sb3)'):
    return ('<p class="dl"><a class="btn-dl" href="{{SB3}}%s.sb3" download>⬇ %s</a> '
            '<span class="dl-hint">Ábrelo en Scratch con <b>Archivo › Cargar desde tu ordenador</b>.</span></p>' % (name, e(label)))

def jugar(name):
    """Proyecto funcionando (reproductor de TurboWarp que lee el .sb3 publicado), plegado para no ocupar espacio."""
    return ('<details class="jugar"><summary>Ver el proyecto funcionando</summary>'
            '<div class="jugar-marco"><iframe data-src="{{PLAY}}%s.sb3" title="Proyecto de Scratch funcionando" '
            'allowfullscreen loading="lazy"></iframe></div>'
            '<p class="dl-hint">Pulsa la bandera verde para empezar. Se carga desde la web publicada.</p></details>' % name)

def code(project):
    return '<div class="sb-wrap">%s</div>' % render_project(project)

def ex(name, project, title, text):
    """Ejemplo corto: título, explicación, bloques y descarga."""
    PROJECTS[name] = project
    return ('<div class="ejemplo"><h3>▶ %s</h3><p>%s</p>%s%s%s</div>' % (e(title), text, code(project), dl(name, 'Descargar ejemplo (.sb3)'), jugar(name)))

def blocks_table(rows):
    out = ['<table class="tabla-bloques"><thead><tr><th>Bloque</th><th>¿Qué hace?</th></tr></thead><tbody>']
    for node, txt in rows:
        out.append('<tr><td><div class="sb-script sb-solo">%s</div></td><td>%s</td></tr>' % (r_block(node), txt))
    out.append('</tbody></table>')
    return ''.join(out)

def box(kind, title, inner):
    icon = {'idea': '💡', 'ojo': '⚠️', 'docente': '🍎', 'reto': '🚀', 'sabias': '🔎'}[kind]
    return '<div class="caja caja-%s"><p class="caja-t">%s %s</p>%s</div>' % (kind, icon, e(title), inner)

def ul(items): return '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def ol(items): return '<ol>' + ''.join('<li>%s</li>' % i for i in items) + '</ol>'
def P(*ps): return ''.join('<p>%s</p>' % p for p in ps)

NIVEL = {1: '★☆☆', 2: '★★☆', 3: '★★★'}

def reto(section, num, slug, title, nivel, tiempo, conceptos, objetivo, pasos, pistas, project, ampliar,
         group=None, materiales=None, nota=None, explica=None):
    name = slug
    PROJECTS[name] = project
    cats = used_categories(project)
    head = ('<div class="ficha"><span class="chip">Reto %s</span><span class="chip">Dificultad %s</span>'
            '<span class="chip">⏱ %s</span>%s</div>' % (num, NIVEL[nivel], e(tiempo),
                                                        ''.join('<span class="chip chip-c">%s</span>' % e(c) for c in conceptos)))
    body = head + '<p class="objetivo"><b>Objetivo:</b> %s</p>' % objetivo + jugar(name)
    if materiales:
        body += box('ojo', 'Necesitas', ul(materiales))
    body += '<h3>Paso a paso</h3>' + ol(pasos)
    if nota:
        body += nota
    body += '<details class="ayuda"><summary>🆘 Ayuda: pistas</summary>%s</details>' % ul(pistas)
    body += ('<details class="ayuda"><summary>✅ Ayuda: una solución posible</summary>%s%s%s</details>'
             % (code(project), ('<p>%s</p>' % explica) if explica else '', dl(name)))
    body += box('reto', '¿Y si…?', ul(ampliar))
    RETOS.append(dict(section=section, num=num, slug=slug, title=title, nivel=nivel, tiempo=tiempo, conceptos=conceptos,
                      objetivo=objetivo, pasos=pasos, pistas=pistas, ampliar=ampliar, materiales=materiales))
    page(section, slug, title, body, group=group, kind='reto', meta=dict(num=num, nivel=nivel, tiempo=tiempo))
