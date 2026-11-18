# -*- coding: utf-8 -*-
"""Pixel art de 8 bits: cuadrículas de caracteres -> SVG nítido, PNG y STL (llavero)."""
import struct

PAL = {
    'K': '#1b1b2f', 'k': '#3b3b5c',                     # contorno / sombra oscura
    'W': '#f4f4f4', 'w': '#c9cfe0',                     # blanco / gris claro
    'Y': '#ffbe2e', 'y': '#e0861a', 'H': '#fff3b0',     # amarillo, sombra, brillo
    'B': '#2f8fdd', 'b': '#1d5aa6', 'L': '#7cc8ff',     # azules
    'R': '#ef4136', 'r': '#a8202f', 'P': '#ff9db0',     # rojos / rosa
    'G': '#5bd65a', 'g': '#2b9a45', 'V': '#b6f26b',     # verdes
    'S': '#9aa3b8', 's': '#5d6680',                     # grises metálicos
    'O': '#ff7a1a', 'o': '#b8500f',                     # naranjas
    'M': '#8b5cf6', 'm': '#5b34b8',                     # morados
    'C': '#45e0e0', 'c': '#1d9aa8',                     # cian
    'N': '#8a5a2b', 'n': '#5c3a1a',                     # marrones
}

def norm(rows):
    w = max(len(r) for r in rows)
    return [r.ljust(w, '.') for r in rows]

def svg(rows, px=4, pal=PAL, bg=None):
    rows = norm(rows)
    h, w = len(rows), len(rows[0])
    out = []
    if bg: out.append('<rect width="%d" height="%d" fill="%s"/>' % (w * px, h * px, bg))
    for y, r in enumerate(rows):
        x = 0
        while x < w:
            c = r[x]
            if c in pal:
                x2 = x
                while x2 + 1 < w and r[x2 + 1] == c: x2 += 1
                out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x * px, y * px, (x2 - x + 1) * px, px, pal[c]))
                x = x2 + 1
            else:
                x += 1
    W, H = w * px, h * px
    return dict(data='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" shape-rendering="crispEdges">%s</svg>'
                % (W, H, W, H, ''.join(out)), cx=W / 2, cy=H / 2)

def png(rows, path, px=8, pal=PAL, bg=None):
    from PIL import Image
    rows = norm(rows)
    h, w = len(rows), len(rows[0])
    im = Image.new('RGBA', (w * px, h * px), bg or (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in pal:
                col = pal[c]
                rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
                for dy in range(px):
                    for dx in range(px):
                        im.putpixel((x * px + dx, y * px + dy), rgb)
    im.save(path)

def put(rows, x, y, patch):
    """Copia un parche (lista de cadenas) sobre la cuadrícula; '.' en el parche no pinta y '_' borra."""
    rows = [list(r) for r in norm(rows)]
    for dy, pr in enumerate(patch):
        for dx, c in enumerate(pr):
            if c == '.': continue
            yy, xx = y + dy, x + dx
            while yy >= len(rows): rows.append(['.'] * len(rows[0]))
            while xx >= len(rows[yy]):
                for rr in rows: rr.append('.')
            rows[yy][xx] = '.' if c == '_' else c
    return [''.join(r) for r in rows]

def flip(rows):
    return [r[::-1] for r in norm(rows)]

# ------------------------------------------------------------------ fuente de píxeles 5x7
FONT = {
    'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
    'B': ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
    'C': ['01111', '10000', '10000', '10000', '10000', '10000', '01111'],
    'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
    'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
    'H': ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
    'I': ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
    'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
    'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
    'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
    'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
    'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
    'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
    'G': ['01111', '10000', '10000', '10111', '10001', '10001', '01111'],
    'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
    'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
    'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
    'F': ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
    'J': ['00111', '00010', '00010', '00010', '00010', '10010', '01100'],
    'V': ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
    'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
    '!': ['00100', '00100', '00100', '00100', '00100', '00000', '00100'],
    '¡': ['00100', '00000', '00100', '00100', '00100', '00100', '00100'],
    ' ': ['000', '000', '000', '000', '000', '000', '000'],
    'X': ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
    '0': ['01110', '10011', '10101', '10101', '11001', '10001', '01110'],
    '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
    '2': ['01110', '10001', '00001', '00110', '01000', '10000', '11111'],
    '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
    '5': ['11111', '10000', '11110', '00001', '00001', '10001', '01110'],
    '6': ['00110', '01000', '10000', '11110', '10001', '10001', '01110'],
    '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
    '9': ['01110', '10001', '10001', '01111', '00001', '00010', '01100'],
    '-': ['000', '000', '000', '111', '000', '000', '000'],
}
def text_rows(txt, fg='W', shadow='K'):
    """Texto en píxeles con sombra desplazada (1,1)."""
    h = 7
    cols = []
    for ch in txt.upper():
        g = FONT[ch]
        for x in range(len(g[0])):
            cols.append([g[y][x] for y in range(h)])
        cols.append(['0'] * h)
    w = len(cols)
    rows = [['.'] * (w + 1) for _ in range(h + 1)]
    for x, col in enumerate(cols):
        for y, v in enumerate(col):
            if v == '1':
                if rows[y + 1][x + 1] == '.': rows[y + 1][x + 1] = shadow
    for x, col in enumerate(cols):
        for y, v in enumerate(col):
            if v == '1': rows[y][x] = fg
    return [''.join(r) for r in rows]

# ------------------------------------------------------------------ STL (llavero)
def stl_from_heights(H, px, path, name='robit'):
    """H[y][x] = altura en mm (0 = vacío). Genera una malla cerrada (estanca) en STL binario."""
    hh, ww = len(H), len(H[0])
    tris = []
    def quad(a, b, c, d):          # a,b,c,d en sentido antihorario visto desde fuera
        tris.append((a, b, c)); tris.append((a, c, d))
    def X(x): return x * px
    def Y(y): return (hh - y) * px   # fila 0 arriba -> y grande
    for y in range(hh):
        for x in range(ww):
            h = H[y][x]
            if h <= 0: continue
            x0, x1, y1, y0 = X(x), X(x + 1), Y(y), Y(y + 1)
            quad((x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h))        # arriba
            quad((x0, y0, 0), (x0, y1, 0), (x1, y1, 0), (x1, y0, 0))        # abajo
            def nb(xx, yy): return H[yy][xx] if 0 <= xx < ww and 0 <= yy < hh else 0
            # izquierda (x-)
            n = nb(x - 1, y)
            if n < h: quad((x0, y0, n), (x0, y0, h), (x0, y1, h), (x0, y1, n))
            n = nb(x + 1, y)
            if n < h: quad((x1, y0, n), (x1, y1, n), (x1, y1, h), (x1, y0, h))
            n = nb(x, y - 1)   # fila de arriba (y mayor en el espacio)
            if n < h: quad((x0, y1, n), (x0, y1, h), (x1, y1, h), (x1, y1, n))
            n = nb(x, y + 1)
            if n < h: quad((x0, y0, n), (x1, y0, n), (x1, y0, h), (x0, y0, h))
    with open(path, 'wb') as f:
        f.write(name.encode().ljust(80, b' ')[:80])
        f.write(struct.pack('<I', len(tris)))
        for a, b, c in tris:
            ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
            vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            l = (nx * nx + ny * ny + nz * nz) ** .5 or 1
            f.write(struct.pack('<12fH', nx / l, ny / l, nz / l, *a, *b, *c, 0))
    return tris
