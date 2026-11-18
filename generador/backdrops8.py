# -*- coding: utf-8 -*-
"""Fondos en pixel art: 120 x 90 píxeles grandes (x4 = 480 x 360, el escenario de Scratch)."""
import random, math
from pixart import Canvas
from pixel import PAL, text_rows

PAL.update({'Z': '#2e3a87', 'A': '#9fdcff', 'a': '#6cc0f5', 'I': '#4aa3e8', 'Q': '#241a52', 'q': '#130e30', 'T': '#3a3170',
            'E': '#5cb85c', 'e': '#3f9447', 'U': '#ecd8a0', 'u': '#cdb06e', 'D': '#2b8ccc', 'd': '#1b6aa3', 'X': '#14507e',
            'F': '#fff7e6', 'f': '#f3e7cc', 'J': '#c43c3c', 'j': '#8f2531', 'x': '#e9e9ef', 'z': '#dfe6ee', 't': '#7a4a24', 'i': '#a26a36'})

W, H = 120, 90

def bands(c, cols, y0=0, y1=H):
    n = len(cols); step = (y1 - y0) / n
    for i, col in enumerate(cols):
        c.rect(0, int(y0 + i * step), W - 1, int(y0 + (i + 1) * step) - 1, col)

def cloud(c, x, y):
    c.put(x, y, ['...WWWW....', '.WWWWWWWW..', 'WWWWWWWWWWW', '.wwwwwwwww.'])

def blanco():
    c = Canvas(W, H).rect(0, 0, W - 1, H - 1, 'W')
    for y in range(4, H, 10):
        for x in range(4, W, 10): c.px(x, y, 'z')
    return c.rows()

def cuadricula():
    c = Canvas(W, H).rect(0, 0, W - 1, H - 1, 'W')
    for x in range(0, W, 10): c.rect(x, 0, x, H - 1, 'z')
    for y in range(0, H, 10): c.rect(0, y, W - 1, y, 'z')
    c.rect(0, 45, W - 1, 45, 'B'); c.rect(60, 0, 60, H - 1, 'O')
    def lab(txt, x, y, col):
        rows = text_rows(txt, fg=col, shadow='.')
        c.put(x, y, rows)
    lab('X', 113, 37, 'B'); lab('Y', 63, 1, 'O')
    lab('240', 101, 47, 'k'); lab('-240', 1, 47, 'k'); lab('0', 62, 47, 'k'); lab('180', 70, 1, 'k'); lab('-180', 63, 82, 'k')
    return c.rows()

def laberinto():
    c = Canvas(W, H)
    for y in range(H):
        for x in range(W):
            c.px(x, y, 'F' if ((x // 4) + (y // 4)) % 2 == 0 else 'f')
    return c.rows()   # las paredes se dibujan aparte con su posición exacta (ver svg_laberinto)

def cielo():
    c = Canvas(W, H); bands(c, ['a', 'a', 'A', 'A', 'A', 'x'], 0, 70)
    c.circle(100, 14, 7, 'Y'); c.circle(100, 14, 5.5, 'H')
    cloud(c, 12, 12); cloud(c, 55, 6); cloud(c, 70, 24)
    c.shape(lambda x, y: y > 62 + 6 * math.sin(x / 9), 'e')
    c.shape(lambda x, y: y > 68 + 4 * math.sin(x / 6 + 1), 'E')
    rnd = random.Random(3)
    for _ in range(40): c.px(rnd.randrange(W), rnd.randrange(72, H), 'V')
    return c.rows()

def espacio():
    c = Canvas(W, H); bands(c, ['q', 'q', 'Q', 'Q', 'T'])
    rnd = random.Random(7)
    for _ in range(70): c.px(rnd.randrange(W), rnd.randrange(H), rnd.choice('WWwS'))
    for x, y in ((18, 14), (88, 9), (60, 40), (103, 66), (30, 70)):
        c.put(x - 1, y - 1, ['.W.', 'WWW', '.W.'])
    c.circle(96, 30, 8, 'M'); c.shade('M'); c.rect(86, 30, 106, 30, 'P')
    return c.rows()

def mar():
    c = Canvas(W, H); bands(c, ['I', 'D', 'D', 'd', 'X'], 0, 76)
    c.rect(0, 0, W - 1, 1, 'A')
    c.shape(lambda x, y: y > 76 + 2 * math.sin(x / 7), 'U')
    rnd = random.Random(5)
    for _ in range(25): c.px(rnd.randrange(W), rnd.randrange(78, H), 'u')
    for x in (8, 14, 104, 110):
        for y in range(56, 80):
            c.px(x + (1 if (y // 3) % 2 else 0), y, 'g')
    for x, y in ((30, 50), (32, 40), (29, 30), (90, 46), (92, 36)):
        c.put(x, y, ['.L.', 'L.L', '.L.'])
    return c.rows()

def noche():
    c = Canvas(W, H); bands(c, ['q', 'Q', 'Q', 'T'], 0, 72)
    rnd = random.Random(11)
    for _ in range(50): c.px(rnd.randrange(W), rnd.randrange(60), rnd.choice('WwS'))
    c.circle(95, 16, 7, 'x'); c.circle(98, 14, 6, 'Q')
    for i, (x0, w, h) in enumerate([(0, 14, 18), (14, 10, 26), (24, 16, 14), (40, 12, 30), (52, 18, 20), (70, 10, 34), (80, 16, 16), (96, 12, 24), (108, 12, 18)]):
        c.rect(x0, H - h, x0 + w - 1, H - 1, 'k')
        for wy in range(H - h + 3, H - 2, 4):
            for wx in range(x0 + 2, x0 + w - 2, 4):
                if rnd.random() < .45: c.rect(wx, wy, wx + 1, wy + 1, 'Y')
    return c.rows()

def teatro():
    c = Canvas(W, H).rect(0, 0, W - 1, H - 1, 'q')
    c.rect(14, 8, 105, 70, 'f')
    c.shape(lambda x, y: ((x - 60) / 34) ** 2 + ((y - 40) / 34) ** 2 <= 1 and 8 <= y <= 70, 'F')
    for x0, x1 in ((0, 22), (98, 119)):
        for x in range(x0, x1 + 1):
            c.rect(x, 0, x, 72, 'J' if (x // 3) % 2 else 'j')
    for x in range(0, W):
        c.rect(x, 0, x, 7, 'J' if (x // 3) % 2 else 'j')
    c.rect(0, 7, W - 1, 8, 'Y')
    c.rect(0, 71, W - 1, H - 1, 'i')
    for y in range(74, H, 5): c.rect(0, y, W - 1, y, 't')
    c.rect(0, 71, W - 1, 71, 'Y')
    return c.rows()

def campo():
    c = Canvas(W, H)
    for x in range(W):
        c.rect(x, 0, x, H - 1, 'E' if (x // 10) % 2 else 'e')
    c.rect(5, 5, 114, 5, 'W'); c.rect(5, 84, 114, 84, 'W'); c.rect(5, 5, 5, 84, 'W'); c.rect(114, 5, 114, 84, 'W')
    c.rect(60, 5, 60, 84, 'W')
    c.shape(lambda x, y: 11.5 ** 2 <= (x - 60.5) ** 2 + (y - 45) ** 2 <= 12.6 ** 2, 'W')
    c.rect(5, 30, 18, 30, 'W'); c.rect(5, 60, 18, 60, 'W'); c.rect(18, 30, 18, 60, 'W')
    c.rect(101, 30, 114, 30, 'W'); c.rect(101, 60, 114, 60, 'W'); c.rect(101, 30, 101, 60, 'W')
    return c.rows()

def porteria():
    c = Canvas(W, H); bands(c, ['a', 'A', 'A'], 0, 38)
    cloud(c, 8, 6); cloud(c, 96, 10)
    for y in range(38, H):
        c.rect(0, y, W - 1, y, 'E' if (y // 6) % 2 else 'e')
    for x in range(24, 97):
        for y in range(16, 56):
            if x % 4 == 0 or y % 4 == 0: c.px(x, y, 'x')
    c.rect(22, 14, 98, 15, 'W'); c.rect(22, 14, 23, 56, 'W'); c.rect(97, 14, 98, 56, 'W')
    c.rect(22, 16, 98, 16, 'w')
    return c.rows()

def fin():
    c = Canvas(W, H); bands(c, ['Y', 'H', 'Y'])
    t = text_rows('¡FIN!', fg='O', shadow='K')
    big = []
    for r in t:
        rr = ''.join(ch * 3 for ch in r)
        big += [rr] * 3
    c.put((W - len(big[0])) // 2, (H - len(big)) // 2, big)
    return c.rows()

def casa_encantada():
    c = Canvas(W, H); bands(c, ['q', 'q', 'Q', 'T'], 0, 70)
    rnd = random.Random(31)
    for _ in range(30): c.px(rnd.randrange(W), rnd.randrange(40), 'w')
    c.circle(20, 16, 8, 'Y'); c.circle(20, 16, 6.5, 'H')
    c.rect(0, 70, W - 1, H - 1, 'k')
    c.rect(52, 30, 92, 72, 'm'); c.poly([(48, 31), (72, 12), (96, 31)], 'K'); c.rect(80, 14, 85, 24, 'm')
    c.poly([(54, 30), (54, 14), (62, 6), (70, 14), (70, 30)], 'm'); c.poly([(52, 15), (62, 3), (72, 15)], 'K')
    for x, y in ((58, 18), (58, 40), (82, 40), (68, 40)):
        c.rect(x, y, x + 4, y + 5, 'Y')
    c.rect(68, 56, 75, 72, 'K')
    for x in (6, 104):
        c.rect(x, 50, x + 2, 72, 'K'); c.line(x + 1, 55, x - 5, 48, 'K'); c.line(x + 1, 58, x + 7, 50, 'K')
    return c.rows()

def nevado():
    c = Canvas(W, H); bands(c, ['T', 'Q', 'Q', 'b'], 0, 64)
    rnd = random.Random(17)
    for _ in range(80): c.px(rnd.randrange(W), rnd.randrange(64), 'W')
    c.shape(lambda x, y: y > 58 + 5 * math.sin(x / 11), 'W'); c.shape(lambda x, y: y > 72 + 3 * math.sin(x / 7 + 2), 'z')
    for x0 in (8, 96):
        c.rect(x0 + 5, 52, x0 + 7, 60, 'n'); c.poly([(x0 + 6, 30), (x0 + 13, 54), (x0 - 1, 54)], 'g'); c.poly([(x0 + 6, 30), (x0 + 10, 42), (x0 + 2, 42)], 'W')
    c.rect(44, 46, 74, 64, 'N'); c.poly([(40, 47), (59, 34), (78, 47)], 'W'); c.rect(56, 54, 61, 64, 'n'); c.rect(47, 51, 52, 56, 'Y'); c.rect(66, 51, 71, 56, 'Y')
    return c.rows()

def playa():
    c = Canvas(W, H); bands(c, ['a', 'A', 'A', 'x'], 0, 40)
    c.circle(98, 12, 8, 'Y'); c.circle(98, 12, 6, 'H'); cloud(c, 14, 8)
    bands(c, ['I', 'D', 'D', 'd'], 40, 72)
    for y in (46, 54, 62, 68):
        for x in range((y * 7) % 12, W, 12): c.rect(x, y, x + 4, y, 'L')
    c.shape(lambda x, y: y > 72 + 2 * math.sin(x / 8), 'U')
    rnd = random.Random(9)
    for _ in range(25): c.px(rnd.randrange(W), rnd.randrange(75, H), 'u')
    return c.rows()

def bosque():
    c = Canvas(W, H); bands(c, ['A', 'A', 'x'], 0, 50); c.rect(0, 50, W - 1, H - 1, 'E')
    rnd = random.Random(21)
    for x0 in range(-4, W, 14):
        h = rnd.randint(28, 40)
        c.rect(x0 + 5, 78 - 10, x0 + 7, 80, 'n')
        c.poly([(x0 + 6, 78 - h), (x0 + 14, 72), (x0 - 2, 72)], 'g' if (x0 // 14) % 2 else 'G')
    for _ in range(40): c.px(rnd.randrange(W), rnd.randrange(80, H), 'V')
    return c.rows()

def castillo():
    c = Canvas(W, H); bands(c, ['a', 'A', 'A', 'x'], 0, 70); cloud(c, 10, 10); cloud(c, 90, 6)
    c.rect(0, 70, W - 1, H - 1, 'E')
    c.rect(36, 32, 84, 72, 'S')
    for x in range(36, 85, 6): c.rect(x, 28, x + 2, 31, 'S')
    for x0 in (26, 82):
        c.rect(x0, 18, x0 + 12, 72, 'S'); c.poly([(x0 - 2, 19), (x0 + 6, 6), (x0 + 14, 19)], 'R')
    c.shade('S'); c.rect(54, 52, 66, 72, 'n'); c.rect(56, 54, 64, 72, 'N')
    c.rect(30, 30, 33, 35, 'K'); c.rect(86, 30, 89, 35, 'K'); c.rect(46, 40, 49, 45, 'K'); c.rect(71, 40, 74, 45, 'K')
    c.rect(32, 0, 32, 6, 'K'); c.rect(33, 1, 37, 3, 'Y')
    return c.rows()

BACKS = {'blanco': blanco(), 'cuadricula': cuadricula(), 'laberinto': laberinto(), 'cielo': cielo(), 'espacio': espacio(),
         'mar': mar(), 'casa_encantada': casa_encantada(), 'nevado': nevado(), 'playa': playa(), 'bosque': bosque(), 'castillo': castillo(), 'noche': noche(), 'teatro': teatro(), 'campo': campo(), 'porteria': porteria(), 'fin': fin()}

# Paredes del laberinto: mismas posiciones y color exacto que antes (el reto detecta el color #2e3a87)
MAZE_WALLS = [(0, 0, 480, 16), (0, 344, 480, 16), (0, 0, 16, 360), (464, 0, 16, 360),
              (90, 16, 16, 240), (190, 104, 16, 240), (290, 16, 16, 240), (380, 104, 16, 240)]
