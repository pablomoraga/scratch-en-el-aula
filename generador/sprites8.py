# -*- coding: utf-8 -*-
"""Objetos del proyecto en pixel art 8 bits (cada píxel = 4 px en Scratch salvo indicación)."""
from pixart import Canvas

def done(c, shade=True):
    if shade: c.shade()
    c.outline()
    return c.rows()

def pelota():
    c = Canvas(11, 11).circle(5.5, 5.5, 4.6, 'O')
    c.shade(); c.put(3, 3, ['WW', 'W.']); return done(c, False)

def balon():
    import math
    c = Canvas(15, 15)
    cols = ['R', 'W', 'B', 'W', 'Y', 'W']
    def seg(i):
        return lambda x, y: (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 6.6 ** 2 and int(((math.atan2(y - 7.5, x - 7.5) + math.pi) / (2 * math.pi) * 6 + 0.25) % 6) == i
    for i, col in enumerate(cols): c.shape(seg(i), col)
    c.shade(); c.circle(7.5, 7.5, 1.4, 'W'); c.put(4, 3, ['WW', 'W.'])
    return done(c, False)

def estrella():
    import math
    pts = []
    for i in range(10):
        r = 7.2 if i % 2 == 0 else 3.2
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((8 + r * math.cos(a), 8.3 + r * math.sin(a)))
    c = Canvas(16, 16).poly(pts, 'Y'); c.shade(); c.put(6, 6, ['K.K']); return done(c, False)

def nave(col='S', win='C'):
    c = Canvas(15, 17)
    c.poly([(7.5, 0.5), (11, 9), (11, 13), (4, 13), (4, 9)], col)
    c.poly([(4, 8), (0.5, 14), (4, 13)], 'R'); c.poly([(11, 8), (14.5, 14), (11, 13)], 'R')
    c.circle(7.5, 6.5, 1.8, win)
    c.shade()
    c.rect(6, 14, 8, 14, 'O'); c.rect(7, 15, 7, 15, 'Y')
    return done(c, False)

def roca():
    c = Canvas(13, 13).poly([(2, 3), (7, 1), (11.5, 4), (12, 9), (7, 12), (2, 10.5), (1, 6)], 'S')
    c.shade()
    c.put(4, 4, ['ss', 's.']); c.put(8, 7, ['ss', '.s']); c.put(4, 9, ['s'])
    return done(c, False)

def pez():
    c = Canvas(18, 12).ellipse(7.5, 6, 6.6, 4.4, 'O').poly([(12.5, 6), (17.5, 1.5), (17.5, 10.5)], 'Y')
    c.shade(); c.put(4, 4, ['W', 'K']); c.put(9, 3, ['Y', 'Y', 'Y', 'Y', 'Y'])
    return done(c, False)

def manzana():
    c = Canvas(12, 13).circle(5.5, 7.5, 4.8, 'R')
    c.shade(); c.put(5, 0, ['N', 'N']); c.put(6, 1, ['GG']); c.put(3, 5, ['W'])
    return done(c, False)

def cesta():
    c = Canvas(23, 13).poly([(0.5, 2), (22.5, 2), (19.5, 12.5), (3.5, 12.5)], 'N')
    for y in (5, 8, 11):
        c.rect(2, y, 20, y, 'n')
    for x in range(4, 20, 4): c.rect(x, 3, x, 12, 'n')
    c.rect(0, 1, 22, 2, 'O')
    return done(c)

def pala():
    c = Canvas(25, 5).rect(1, 1, 23, 3, 'B'); return done(c)

def ladrillo():
    c = Canvas(15, 5).rect(0, 0, 14, 4, 'R')
    c.rect(0, 2, 14, 2, 'r'); c.rect(7, 0, 7, 1, 'r'); c.rect(3, 3, 3, 4, 'r'); c.rect(11, 3, 11, 4, 'r')
    c.rect(0, 0, 14, 0, 'P')
    return c.rows()

def coche():
    c = Canvas(21, 12).rect(1, 4, 19, 8, 'R').poly([(5, 4.5), (7, 0.5), (14, 0.5), (16.5, 4.5)], 'R')
    c.shade(); c.rect(7, 1, 9, 3, 'C'); c.rect(11, 1, 14, 3, 'C')
    c.circle(5.5, 9, 2.4, 'K'); c.circle(15.5, 9, 2.4, 'K'); c.px(5, 9, 'S'); c.px(15, 9, 'S'); c.px(19, 5, 'Y')
    return done(c, False)

def punto():
    return ['.KK.', 'KKKK', 'KKKK', '.KK.']

def boton(col='G'):
    c = Canvas(18, 18).circle(9, 9, 7.6, col); c.shade(); c.circle(9, 9, 4.2, {'G': 'V', 'R': 'P'}[col])
    c.put(6, 6, ['WW', 'W.']); return done(c, False)

def meta():
    c = Canvas(11, 16).rect(1, 0, 1, 15, 'S')
    for y in range(0, 6):
        for x in range(2, 10):
            c.px(x, y, 'K' if (x // 2 + y // 2) % 2 else 'W')
    return done(c, False)

def burbuja():
    c = Canvas(16, 16).circle(8, 8, 6.6, 'L').circle(8, 8, 5.4, 'C')
    c.circle(8, 8, 4.4, 'L'); c.put(5, 4, ['WW', 'W.'])
    return done(c, False)

def tambor():
    c = Canvas(21, 18).ellipse(10.5, 4, 9.5, 3.4, 'W').rect(1, 4, 19, 13, 'R').ellipse(10.5, 13.5, 9.5, 3.4, 'R')
    c.ellipse(10.5, 4, 9.5, 3.4, 'W'); c.shade()
    for x in range(3, 19, 4): c.line(x, 7, x + 2, 13, 'Y')
    c.rect(1, 6, 19, 6, 'Y')
    return done(c, False)

def tecla(on=False):
    c = Canvas(10, 30).rect(1, 1, 8, 28, 'Y' if on else 'W'); return done(c)

def sol():
    c = Canvas(21, 21)
    for i in range(8):
        import math
        a = i * math.pi / 4
        c.line(10 + round(6 * math.cos(a)), 10 + round(6 * math.sin(a)), 10 + round(9.5 * math.cos(a)), 10 + round(9.5 * math.sin(a)), 'Y')
    c.circle(10.5, 10.5, 6.2, 'O'); c.circle(10.5, 10.5, 4.8, 'Y'); c.put(8, 7, ['HH', 'H.'])
    return done(c, False)

def planeta():
    c = Canvas(9, 9).circle(4.5, 4.5, 3.8, 'B'); c.put(2, 3, ['GG.', '.GGG']); c.put(5, 6, ['G'])
    return done(c.shade('B'))

def luna():
    c = Canvas(5, 5).circle(2.5, 2.5, 2, 'S'); return done(c)

def moneda():
    c = Canvas(10, 10).circle(5, 5, 4.2, 'Y'); c.shade(); c.rect(4, 3, 5, 6, 'y'); return done(c, False)

def fantasma():
    c = Canvas(16, 18).circle(8, 7, 6.5, 'W').rect(2, 7, 13, 14, 'W')
    for x in (2, 6, 10): c.rect(x, 15, x + 1, 15, 'W')
    c.shade(); c.put(5, 6, ['KK..KK', 'KK..KK']); c.put(7, 10, ['KK'])
    return done(c, False)

def mascota(mood):
    col = {'feliz': 'G', 'normal': 'V', 'triste': 'S'}[mood]
    c = Canvas(26, 23).ellipse(13, 13.5, 11.5, 8.8, col)
    c.poly([(4, 8), (3, 1), (8, 6)], col); c.poly([(22, 8), (23, 1), (18, 6)], col)
    c.shade()
    c.put(7, 9, ['WWW', 'WKW', 'WWW']); c.put(16, 9, ['WWW', 'WKW', 'WWW'])
    mouth = {'feliz': ['K......K', '.KKKKKK.'], 'normal': ['KKKKKKKK'], 'triste': ['.KKKKKK.', 'K......K']}[mood]
    c.put(9, 15, mouth); c.put(5, 13, ['P']); c.put(20, 13, ['P'])
    return done(c, False)

def comida():
    c = Canvas(13, 13).ellipse(6.5, 9, 5.8, 3.2, 'W').circle(4.5, 6, 2.3, 'R').circle(8.5, 5.5, 2.6, 'Y').circle(6.5, 3, 1.6, 'G')
    return done(c.shade())

def juguete():
    c = Canvas(13, 13).circle(6.5, 6.5, 5.6, 'B'); c.rect(1, 6, 11, 6, 'Y'); c.rect(6, 1, 6, 11, 'Y')
    return done(c.shade('B'))

def cama():
    c = Canvas(16, 11).rect(1, 4, 14, 7, 'M').rect(2, 2, 5, 4, 'W').rect(1, 8, 1, 9, 'N').rect(14, 8, 14, 9, 'N')
    return done(c.shade())

def flecha():
    c = Canvas(16, 9).rect(0, 3, 9, 5, 'O').poly([(9, 0), (15.5, 4.5), (9, 9)], 'O'); return done(c.shade())

SPRITES = {
    'pelota': pelota(), 'balon': balon(), 'estrella': estrella(), 'nave': nave(), 'nave2': nave('R', 'Y'),
    'roca': roca(), 'pez': pez(), 'manzana': manzana(), 'cesta': cesta(), 'pala': pala(), 'ladrillo': ladrillo(),
    'coche': coche(), 'punto': punto(), 'boton': boton('G'), 'boton_rojo': boton('R'), 'meta': meta(),
    'burbuja': burbuja(), 'tambor': tambor(), 'tecla': tecla(), 'tecla_on': tecla(True), 'sol': sol(),
    'planeta': planeta(), 'luna': luna(), 'moneda': moneda(), 'fantasma': fantasma(),
    'mascota_feliz': mascota('feliz'), 'mascota_normal': mascota('normal'), 'mascota_triste': mascota('triste'),
    'comida': comida(), 'juguete': juguete(), 'cama': cama(), 'flecha': flecha(),
}
PX = {'punto': 2}   # escala por objeto (por defecto 4)

# ------------------------------------------------------------------ efemérides
import math as _m
def calabaza():
    c = Canvas(18, 16).ellipse(9, 9.5, 8.2, 6.2, 'O')
    c.rect(8, 1, 9, 3, 'g'); c.shade('O')
    for x in (5, 12): c.rect(x, 5, x, 14, 'o')
    c.put(4, 6, ['..K', '.KK', 'KKK']); c.put(11, 6, ['K..', 'KK.', 'KKK'])
    c.put(5, 10, ['K.KK.KK.', 'KKKKKKKK', '.K..K..K'])
    return done(c, False)

def murcielago(up=True):
    c = Canvas(20, 10).ellipse(10, 5.5, 2.6, 3.4, 'k')
    if up: c.poly([(8, 5), (1, 0.5), (3, 4), (0.5, 6), (8, 7)], 'k'); c.poly([(12, 5), (19, 0.5), (17, 4), (19.5, 6), (12, 7)], 'k')
    else: c.poly([(8, 4), (0.5, 8), (3, 6), (2, 9.5), (8, 7)], 'k'); c.poly([(12, 4), (19.5, 8), (17, 6), (18, 9.5), (12, 7)], 'k')
    c.put(9, 4, ['R.R']); return done(c, False)

def arbol():
    c = Canvas(20, 26)
    for i, (y0, w) in enumerate(((3, 4), (8, 6), (13, 8), (18, 9))):
        c.poly([(10, y0 - 2), (10 + w, y0 + 5), (10 - w, y0 + 5)], 'G')
    c.rect(8, 23, 11, 25, 'N'); c.shade('GN')
    for x, y, col in ((9, 7, 'R'), (12, 11, 'Y'), (7, 13, 'C'), (11, 16, 'R'), (5, 19, 'Y'), (14, 20, 'M'), (9, 21, 'C')): c.px(x, y, col)
    c.put(9, 0, ['YY', 'YY']); return done(c, False)

def copo():
    c = Canvas(9, 9)
    for a in range(0, 180, 45):
        r = _m.radians(a); c.line(4 - round(4 * _m.cos(r)), 4 - round(4 * _m.sin(r)), 4 + round(4 * _m.cos(r)), 4 + round(4 * _m.sin(r)), 'W')
    return c.rows()

def regalo(col='R', lazo='Y'):
    c = Canvas(14, 14).rect(1, 4, 12, 12, col).rect(0, 3, 13, 5, col)
    c.shade(); c.rect(6, 3, 7, 12, lazo); c.rect(0, 4, 13, 4, lazo); c.put(3, 0, ['YYY..YYY', '.YYYYYY.', '..YYYY..'])
    return done(c, False)

def saco():
    c = Canvas(24, 18).ellipse(12, 11, 11, 6.6, 'R').poly([(8, 5), (16, 5), (14, 2), (10, 2)], 'R')
    c.shade(); c.rect(9, 4, 15, 5, 'Y'); c.put(5, 9, ['PP', 'P.'])
    return done(c, False)

def paloma(up=True):
    c = Canvas(20, 13).ellipse(9, 8, 6.5, 3.2, 'W').circle(15.5, 6, 2.4, 'W').poly([(17.5, 5.5), (20, 6.5), (17.5, 7.5)], 'O')
    c.poly([(3, 8), (0.5, 6), (0.5, 10)], 'W')
    if up: c.poly([(5, 7), (8, 0.5), (12, 1.5), (12, 7)], 'w')
    else: c.poly([(5, 8), (8, 12.5), (12, 11.5), (12, 8)], 'w')
    c.shade('W'); c.px(16, 5, 'K'); c.line(13, 9, 16, 11, 'g')
    return done(c, False)

def corazon():
    c = Canvas(13, 12).circle(4, 4, 3.4, 'R').circle(9, 4, 3.4, 'R').poly([(0.8, 5), (12.2, 5), (6.5, 11.5)], 'R')
    c.shade(); c.put(3, 2, ['W']); return done(c, False)

def gorro():
    c = Canvas(14, 16).poly([(7, 0.5), (12.5, 14), (1.5, 14)], 'M')
    for y in (5, 9, 13): c.rect(0, y, 13, y, '.')
    c.poly([(7, 0.5), (12.5, 14), (1.5, 14)], 'M'); c.shade()
    for x, y in ((6, 5), (8, 8), (5, 10), (9, 12)): c.px(x, y, 'Y')
    c.rect(1, 14, 12, 15, 'Y'); c.circle(7, 1.5, 1.5, 'Y')
    return done(c, False)

def gafas():
    c = Canvas(22, 8).rect(1, 1, 8, 6, 'M').rect(13, 1, 20, 6, 'M').rect(8, 2, 13, 3, 'K')
    c.rect(2, 2, 7, 5, 'C').rect(14, 2, 19, 5, 'C'); c.px(3, 2, 'W'); c.px(15, 2, 'W')
    return done(c, False)

def careta():
    c = Canvas(22, 9).ellipse(11, 4.5, 10.4, 4, 'Y'); c.shade()
    c.ellipse(6, 4.5, 2.6, 1.6, '.'); c.ellipse(16, 4.5, 2.6, 1.6, '.')
    for x in (2, 10, 18): c.px(x, 1, 'R')
    return done(c, False)

def libro(abierto=False):
    if abierto:
        c = Canvas(24, 14).poly([(1, 2), (11.5, 3), (11.5, 13), (1, 12)], 'W').poly([(12.5, 3), (23, 2), (23, 12), (12.5, 13)], 'W')
        for y in (5, 7, 9): c.rect(3, y, 9, y, 'w'); c.rect(14, y, 20, y, 'w')
        c.rect(11, 3, 12, 13, 'N')
    else:
        c = Canvas(16, 18).rect(1, 1, 14, 16, 'B').rect(2, 2, 2, 15, 'b'); c.shade('B'); c.rect(5, 5, 11, 7, 'Y')
    return done(c, False)

def contenedor(col):
    c = Canvas(22, 26).rect(1, 6, 20, 24, col).rect(0, 3, 21, 6, col); c.shade()
    c.rect(7, 1, 14, 3, 'k'); c.rect(4, 10, 17, 10, 'K')
    return done(c, False)

def botella():
    c = Canvas(8, 18).rect(2, 0, 4, 3, 'C').rect(1, 4, 5, 16, 'L').rect(1, 8, 5, 10, 'B'); return done(c.shade())

def lata():
    c = Canvas(9, 13).rect(1, 1, 7, 11, 'R').rect(1, 5, 7, 7, 'W'); return done(c.shade())

def periodico():
    c = Canvas(16, 12).rect(1, 1, 14, 10, 'W')
    for y in (3, 5, 7): c.rect(3, y, 12, y, 'S')
    c.rect(3, 1, 12, 1, 'K'); return done(c)

def caja():
    c = Canvas(14, 12).rect(1, 2, 12, 10, 'N').rect(0, 1, 13, 3, 'O'); c.shade(); c.rect(6, 1, 7, 10, 'u'); return done(c, False)

def tarro():
    c = Canvas(10, 14).rect(2, 0, 7, 2, 'S').rect(1, 3, 8, 12, 'V'); c.shade(); c.rect(2, 5, 2, 9, 'W'); return done(c, False)

def medusa():
    c = Canvas(14, 16).ellipse(7, 5, 6, 4.4, 'P').rect(1, 5, 12, 8, '.')
    c.ellipse(7, 5, 6, 4.4, 'P'); c.rect(1, 6, 12, 8, '.')
    for x in (2, 5, 8, 11): c.line(x, 8, x + (1 if x % 2 else -1), 15, 'M')
    c.rect(1, 5, 12, 6, 'P'); c.shade('P'); c.put(4, 3, ['K..K'])
    return done(c, False)

def concha():
    c = Canvas(15, 11).shape(lambda x, y: (x - 7.5) ** 2 + (y - 9) ** 2 <= 49 and y <= 9, 'P').rect(5, 9, 9, 10, 'P')
    c.shade('P')
    for x in (2, 5, 7, 9, 12): c.line(7, 9, x, 3 if x in (5, 7, 9) else 6, 'R')
    return done(c, False)

def tabla():
    c = Canvas(30, 6).ellipse(15, 3, 14, 2.4, 'Y'); c.shade(); c.rect(4, 3, 25, 3, 'R'); return done(c, False)

SPRITES.update({
    'calabaza': calabaza(), 'murcielago1': murcielago(True), 'murcielago2': murcielago(False), 'arbol': arbol(), 'copo': copo(),
    'regalo': regalo(), 'regalo2': regalo('B', 'W'), 'saco': saco(), 'paloma1': paloma(True), 'paloma2': paloma(False),
    'corazon': corazon(), 'gorro': gorro(), 'gafas': gafas(), 'careta': careta(), 'libro': libro(), 'libro_abierto': libro(True),
    'contenedor_amarillo': contenedor('Y'), 'contenedor_azul': contenedor('B'), 'contenedor_verde': contenedor('G'),
    'botella': botella(), 'lata': lata(), 'periodico': periodico(), 'caja': caja(), 'tarro': tarro(),
    'medusa': medusa(), 'concha': concha(), 'tabla': tabla(),
})
