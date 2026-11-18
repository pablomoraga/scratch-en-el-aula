# -*- coding: utf-8 -*-
"""Disfraces, fondos y sonidos propios (dibujados a mano en SVG y sintetizados en WAV)."""
import io, math, struct, wave, random
import pixel as _px, robit as _rb

def svg(w, h, body):
    return dict(data='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
                % (w, h, w, h, body), cx=w / 2, cy=h / 2)

def robi(arm):
    a = 'M14 52 L4 %d' % (40 if arm else 66)
    b = 'M76 52 L86 %d' % (66 if arm else 40)
    legs = ('<rect x="30" y="92" width="10" height="16" rx="3" fill="#4a4a4a"/>'
            '<rect x="50" y="%d" width="10" height="16" rx="3" fill="#4a4a4a"/>' % (90 if arm else 92))
    return svg(90, 110,
               '<path d="%s" stroke="#4a4a4a" stroke-width="6" stroke-linecap="round"/>'
               '<path d="%s" stroke="#4a4a4a" stroke-width="6" stroke-linecap="round"/>' % (a, b) + legs +
               '<line x1="45" y1="4" x2="45" y2="14" stroke="#4a4a4a" stroke-width="3"/><circle cx="45" cy="4" r="4" fill="#e85d2a"/>'
               '<rect x="18" y="14" width="54" height="40" rx="10" fill="#f2b134" stroke="#4a4a4a" stroke-width="3"/>'
               '<circle cx="34" cy="33" r="6" fill="#fff" stroke="#4a4a4a" stroke-width="2"/><circle cx="34" cy="33" r="2.5" fill="#222"/>'
               '<circle cx="56" cy="33" r="6" fill="#fff" stroke="#4a4a4a" stroke-width="2"/><circle cx="56" cy="33" r="2.5" fill="#222"/>'
               '<path d="M36 45 Q45 50 54 45" stroke="#4a4a4a" stroke-width="2.5" fill="none"/>'
               '<rect x="14" y="54" width="62" height="40" rx="8" fill="#3d8bd6" stroke="#4a4a4a" stroke-width="3"/>'
               '<circle cx="45" cy="74" r="7" fill="#7fd36b" stroke="#4a4a4a" stroke-width="2"/>')

def star(fill='#ffd23f'):
    pts = []
    for i in range(10):
        r = 28 if i % 2 == 0 else 12
        ang = -math.pi / 2 + i * math.pi / 5
        pts.append('%.1f,%.1f' % (30 + r * math.cos(ang), 30 + r * math.sin(ang)))
    return svg(60, 60, '<polygon points="%s" fill="%s" stroke="#b8860b" stroke-width="2"/>' % (' '.join(pts), fill))

def backdrop(body):
    return svg(480, 360, body)

def grid():
    b = '<rect width="480" height="360" fill="#ffffff"/>'
    for x in range(0, 481, 40):
        b += '<line x1="%d" y1="0" x2="%d" y2="360" stroke="%s" stroke-width="1"/>' % (x, x, '#c9c9c9')
    for y in range(0, 361, 40):
        b += '<line x1="0" y1="%d" x2="480" y2="%d" stroke="#c9c9c9" stroke-width="1"/>' % (y, y)
    b += '<line x1="240" y1="0" x2="240" y2="360" stroke="#e85d2a" stroke-width="2"/>'
    b += '<line x1="0" y1="180" x2="480" y2="180" stroke="#3d8bd6" stroke-width="2"/>'
    b += ('<text x="452" y="174" font-family="sans-serif" font-size="13" fill="#3d8bd6">x</text>'
          '<text x="246" y="16" font-family="sans-serif" font-size="13" fill="#e85d2a">y</text>'
          '<text x="244" y="196" font-family="sans-serif" font-size="11" fill="#555">(0,0)</text>'
          '<text x="4" y="196" font-family="sans-serif" font-size="11" fill="#555">-240</text>'
          '<text x="446" y="196" font-family="sans-serif" font-size="11" fill="#555">240</text>'
          '<text x="244" y="354" font-family="sans-serif" font-size="11" fill="#555">-180</text>'
          '<text x="244" y="30" font-family="sans-serif" font-size="11" fill="#555">180</text>')
    return backdrop(b)

def maze():
    W = '#2e3a87'
    walls = [(0, 0, 480, 16), (0, 344, 480, 16), (0, 0, 16, 360), (464, 0, 16, 360),
             (90, 16, 16, 240), (190, 104, 16, 240), (290, 16, 16, 240), (380, 104, 16, 240)]
    b = '<rect width="480" height="360" fill="#fff7e6"/>'
    b += ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, w, h, W) for x, y, w, h in walls)
    return backdrop(b)

def sky():
    return backdrop('<rect width="480" height="360" fill="#bfe6ff"/><rect y="300" width="480" height="60" fill="#7cc46b"/>'
                    '<circle cx="410" cy="60" r="34" fill="#ffd23f"/>'
                    '<ellipse cx="110" cy="80" rx="50" ry="18" fill="#fff"/><ellipse cx="250" cy="50" rx="40" ry="14" fill="#fff"/>')

def space():
    rnd = random.Random(7)
    b = '<rect width="480" height="360" fill="#14123a"/>'
    for _ in range(70):
        b += '<circle cx="%d" cy="%d" r="%.1f" fill="#fff" opacity="%.2f"/>' % (
            rnd.randint(0, 480), rnd.randint(0, 360), rnd.uniform(.6, 1.8), rnd.uniform(.4, 1))
    return backdrop(b)

def sea():
    return backdrop('<rect width="480" height="360" fill="#1d7fb8"/><rect y="300" width="480" height="60" fill="#e8d39a"/>'
                    '<path d="M40 300 q10-40 0-80 M60 300 q-10-30 0-60 M420 300 q12-50 0-100" stroke="#2f9e57" stroke-width="8" fill="none"/>')

def night():
    return backdrop('<rect width="480" height="360" fill="#25305e"/><circle cx="380" cy="70" r="30" fill="#f4f1c9"/>'
                    '<rect y="280" width="480" height="80" fill="#1b2a1d"/>')

def theatre():
    return backdrop('<rect width="480" height="360" fill="#3a1f2b"/><rect x="40" y="40" width="400" height="250" fill="#f6e7c8"/>'
                    '<path d="M40 40 h70 q-20 120 0 250 h-70z M440 40 h-70 q20 120 0 250 h70z" fill="#b3263a"/>'
                    '<rect y="290" width="480" height="70" fill="#6b3d1f"/>')

def field():
    return backdrop('<rect width="480" height="360" fill="#4fa64f"/><rect x="20" y="20" width="440" height="320" fill="none" stroke="#fff" stroke-width="4"/>'
                    '<line x1="240" y1="20" x2="240" y2="340" stroke="#fff" stroke-width="4"/><circle cx="240" cy="180" r="50" fill="none" stroke="#fff" stroke-width="4"/>')

def goal():
    b = '<rect width="480" height="360" fill="#5bb35b"/><rect width="480" height="150" fill="#bfe6ff"/>'
    b += '<rect x="90" y="60" width="300" height="160" fill="none" stroke="#fff" stroke-width="10"/>'
    for x in range(100, 390, 20):
        b += '<line x1="%d" y1="65" x2="%d" y2="215" stroke="#e8e8e8" stroke-width="1"/>' % (x, x)
    for y in range(70, 215, 20):
        b += '<line x1="95" y1="%d" x2="385" y2="%d" stroke="#e8e8e8" stroke-width="1"/>' % (y, y)
    return backdrop(b)

def finish():
    return backdrop('<rect width="480" height="360" fill="#ffe28a"/>'
                    '<text x="240" y="190" text-anchor="middle" font-family="sans-serif" font-size="54" font-weight="bold" fill="#e85d2a">¡FIN!</text>')

def shape(w, h, body): return svg(w, h, body)

COSTUMES = {
    'robit1': _px.svg(_rb.ROBIT1, px=4), 'robit2': _px.svg(_rb.ROBIT2, px=4), 'robit3': _px.svg(_rb.ROBIT3, px=4),
    'pelota': shape(40, 40, '<circle cx="20" cy="20" r="18" fill="#e85d2a" stroke="#8a2f0f" stroke-width="2"/><path d="M4 16 Q20 26 36 16" stroke="#fff" stroke-width="3" fill="none"/>'),
    'balon': shape(40, 40, '<circle cx="20" cy="20" r="18" fill="#fff" stroke="#222" stroke-width="2"/><polygon points="20,11 28,17 25,27 15,27 12,17" fill="#222"/>'),
    'estrella': star(),
    'nave': shape(60, 60, '<polygon points="30,2 46,44 30,36 14,44" fill="#d9e2ec" stroke="#3d4f63" stroke-width="2"/><circle cx="30" cy="22" r="6" fill="#3d8bd6"/><polygon points="22,42 30,58 38,42" fill="#f2b134"/>'),
    'nave2': shape(60, 60, '<polygon points="30,2 46,44 30,36 14,44" fill="#ffc9c9" stroke="#8a2f0f" stroke-width="2"/><circle cx="30" cy="22" r="6" fill="#e85d2a"/><polygon points="22,42 30,58 38,42" fill="#f2b134"/>'),
    'roca': shape(50, 50, '<polygon points="10,8 32,2 48,18 44,40 24,48 4,36" fill="#8d7b6a" stroke="#4d4238" stroke-width="2"/><circle cx="20" cy="20" r="4" fill="#6f5f51"/><circle cx="32" cy="32" r="5" fill="#6f5f51"/>'),
    'pez': shape(70, 44, '<ellipse cx="32" cy="22" rx="24" ry="15" fill="#f2b134" stroke="#9a6a0c" stroke-width="2"/><polygon points="54,22 68,8 68,36" fill="#e85d2a"/><circle cx="20" cy="18" r="3" fill="#222"/>'),
    'manzana': shape(40, 44, '<circle cx="20" cy="26" r="16" fill="#d7263d"/><path d="M20 10 q2-6 6-8" stroke="#5a3a1a" stroke-width="3" fill="none"/><ellipse cx="27" cy="9" rx="5" ry="3" fill="#4caf50"/>'),
    'cesta': shape(90, 50, '<path d="M4 12 h82 l-10 36 h-62z" fill="#c98a3d" stroke="#6b4518" stroke-width="3"/><path d="M14 22 h62 M18 34 h54" stroke="#6b4518" stroke-width="2"/>'),
    'pala': shape(100, 18, '<rect x="2" y="2" width="96" height="14" rx="7" fill="#3d8bd6" stroke="#1f4f80" stroke-width="2"/>'),
    'pala_v': shape(18, 90, '<rect x="2" y="2" width="14" height="86" rx="7" fill="#3d8bd6" stroke="#1f4f80" stroke-width="2"/>'),
    'ladrillo': shape(60, 22, '<rect x="1" y="1" width="58" height="20" rx="3" fill="#e85d2a" stroke="#8a2f0f" stroke-width="2"/>'),
    'coche': shape(80, 44, '<rect x="4" y="16" width="72" height="18" rx="6" fill="#d7263d"/><path d="M18 16 l8-12 h26 l10 12z" fill="#ffb3b3" stroke="#d7263d" stroke-width="2"/><circle cx="20" cy="36" r="7" fill="#222"/><circle cx="60" cy="36" r="7" fill="#222"/>'),
    'punto': shape(10, 10, '<circle cx="5" cy="5" r="4" fill="#222"/>'),
    'boton': shape(70, 70, '<circle cx="35" cy="35" r="32" fill="#7fd36b" stroke="#2f7a24" stroke-width="4"/><circle cx="35" cy="35" r="18" fill="#a6e696"/>'),
    'boton_rojo': shape(70, 70, '<circle cx="35" cy="35" r="32" fill="#ff6b6b" stroke="#a02626" stroke-width="4"/><circle cx="35" cy="35" r="18" fill="#ffa3a3"/>'),
    'meta': shape(40, 60, '<line x1="6" y1="4" x2="6" y2="58" stroke="#444" stroke-width="4"/><rect x="8" y="4" width="28" height="20" fill="#fff" stroke="#222"/><rect x="8" y="4" width="7" height="5" fill="#222"/><rect x="22" y="4" width="7" height="5" fill="#222"/><rect x="15" y="9" width="7" height="5" fill="#222"/><rect x="29" y="9" width="7" height="5" fill="#222"/><rect x="8" y="14" width="7" height="5" fill="#222"/><rect x="22" y="14" width="7" height="5" fill="#222"/><rect x="15" y="19" width="7" height="5" fill="#222"/><rect x="29" y="19" width="7" height="5" fill="#222"/>'),
    'burbuja': shape(60, 60, '<circle cx="30" cy="30" r="26" fill="#bfe6ff" fill-opacity=".6" stroke="#3d8bd6" stroke-width="3"/><circle cx="20" cy="20" r="6" fill="#fff"/>'),
    'tambor': shape(80, 70, '<ellipse cx="40" cy="20" rx="34" ry="12" fill="#f6e7c8" stroke="#6b4518" stroke-width="3"/><path d="M6 20 v30 q34 24 68 0 v-30" fill="#d7263d" stroke="#6b4518" stroke-width="3"/><path d="M10 26 l14 26 M30 32 l10 26 M70 26 l-14 26" stroke="#ffd23f" stroke-width="3"/>'),
    'tecla': shape(40, 120, '<rect x="2" y="2" width="36" height="116" rx="4" fill="#fff" stroke="#222" stroke-width="3"/>'),
    'tecla_on': shape(40, 120, '<rect x="2" y="2" width="36" height="116" rx="4" fill="#ffd23f" stroke="#222" stroke-width="3"/>'),
    'sol': shape(80, 80, '<circle cx="40" cy="40" r="26" fill="#ffb627"/><circle cx="40" cy="40" r="36" fill="none" stroke="#ffd23f" stroke-width="4" stroke-dasharray="6 6"/>'),
    'planeta': shape(30, 30, '<circle cx="15" cy="15" r="12" fill="#3d8bd6"/><path d="M6 12 q6-4 10 2 q4 6 9 2" stroke="#4caf50" stroke-width="3" fill="none"/>'),
    'luna': shape(16, 16, '<circle cx="8" cy="8" r="6" fill="#ccc"/>'),
    'flecha': shape(60, 30, '<polygon points="2,10 38,10 38,2 58,15 38,28 38,20 2,20" fill="#e85d2a"/>'),
    'moneda': shape(36, 36, '<circle cx="18" cy="18" r="16" fill="#ffd23f" stroke="#b8860b" stroke-width="3"/><text x="18" y="24" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="bold" fill="#b8860b">1</text>'),
    'fantasma': shape(60, 70, '<path d="M6 66 V30 a24 24 0 0 1 48 0 V66 l-8-8 l-8 8 l-8-8 l-8 8 l-8-8z" fill="#f4f4ff" stroke="#6b6b9a" stroke-width="3"/><circle cx="22" cy="30" r="5" fill="#222"/><circle cx="38" cy="30" r="5" fill="#222"/>'),
    'mascota_feliz': shape(100, 90, '<ellipse cx="50" cy="52" rx="44" ry="36" fill="#9be0c5" stroke="#2c7a5c" stroke-width="3"/><circle cx="34" cy="44" r="6" fill="#222"/><circle cx="66" cy="44" r="6" fill="#222"/><path d="M34 62 Q50 76 66 62" stroke="#222" stroke-width="4" fill="none"/><path d="M20 20 l8 14 M80 20 l-8 14" stroke="#2c7a5c" stroke-width="5" stroke-linecap="round"/>'),
    'mascota_normal': shape(100, 90, '<ellipse cx="50" cy="52" rx="44" ry="36" fill="#c7e6a3" stroke="#5c7a2c" stroke-width="3"/><circle cx="34" cy="44" r="6" fill="#222"/><circle cx="66" cy="44" r="6" fill="#222"/><path d="M36 66 H64" stroke="#222" stroke-width="4"/><path d="M20 20 l8 14 M80 20 l-8 14" stroke="#5c7a2c" stroke-width="5" stroke-linecap="round"/>'),
    'mascota_triste': shape(100, 90, '<ellipse cx="50" cy="52" rx="44" ry="36" fill="#e6c3a3" stroke="#7a542c" stroke-width="3"/><circle cx="34" cy="46" r="6" fill="#222"/><circle cx="66" cy="46" r="6" fill="#222"/><path d="M34 70 Q50 58 66 70" stroke="#222" stroke-width="4" fill="none"/><path d="M20 24 l10 10 M80 24 l-10 10" stroke="#7a542c" stroke-width="5" stroke-linecap="round"/>'),
    'comida': shape(50, 50, '<rect x="5" y="20" width="40" height="22" rx="6" fill="#c98a3d"/><circle cx="16" cy="18" r="8" fill="#d7263d"/><circle cx="32" cy="16" r="9" fill="#f2b134"/>'),
    'juguete': shape(50, 50, '<circle cx="25" cy="25" r="20" fill="#3d8bd6"/><path d="M5 25 h40 M25 5 v40" stroke="#ffd23f" stroke-width="5"/>'),
    'cama': shape(60, 40, '<rect x="4" y="18" width="52" height="14" rx="4" fill="#9966ff"/><rect x="6" y="10" width="16" height="10" rx="4" fill="#fff"/><path d="M4 32 v6 M56 32 v6" stroke="#444" stroke-width="4"/>'),
    'portero': shape(70, 60, '<ellipse cx="18" cy="30" rx="16" ry="22" fill="#ffd23f" stroke="#b8860b" stroke-width="3"/><ellipse cx="52" cy="30" rx="16" ry="22" fill="#ffd23f" stroke="#b8860b" stroke-width="3"/>'),
    'texto_go': shape(160, 60, '<rect x="2" y="2" width="156" height="56" rx="12" fill="#7fd36b" stroke="#2f7a24" stroke-width="3"/><text x="80" y="40" text-anchor="middle" font-family="sans-serif" font-size="26" font-weight="bold" fill="#1d4d16">¡JUGAR!</text>'),
}
BACKDROPS = {
    'blanco': backdrop('<rect width="480" height="360" fill="#ffffff"/>'),
    'cuadricula': grid(), 'laberinto': maze(), 'cielo': sky(), 'espacio': space(), 'mar': sea(),
    'noche': night(), 'teatro': theatre(), 'campo': field(), 'porteria': goal(), 'fin': finish(),
}
for i, col in enumerate(['#ffe8d6', '#d6f0ff', '#e8ffd6']):
    BACKDROPS['escena%d' % (i + 1)] = backdrop('<rect width="480" height="360" fill="%s"/>'
                                                '<text x="20" y="40" font-family="sans-serif" font-size="22" fill="#555">Escena %d</text>' % (col, i + 1))

# -------------------------------------------------------------- sonidos
RATE = 22050
def _tone(seq):
    frames = []
    for f0, f1, dur, kind in seq:
        n = int(RATE * dur)
        for i in range(n):
            t = i / RATE
            f = f0 + (f1 - f0) * i / max(n, 1)
            env = math.exp(-4 * t / dur)
            if kind == 'sin':
                v = math.sin(2 * math.pi * f * t)
            elif kind == 'sq':
                v = 1 if math.sin(2 * math.pi * f * t) > 0 else -1
                v *= .5
            else:
                v = random.Random(i).uniform(-1, 1)
            frames.append(int(v * env * 12000))
    return frames

SOUNDS = {
    'pop': [(900, 300, .12, 'sin')],
    'ding': [(1320, 1320, .5, 'sin')],
    'boing': [(200, 700, .35, 'sin')],
    'error': [(160, 120, .35, 'sq')],
    'victoria': [(523, 523, .15, 'sin'), (659, 659, .15, 'sin'), (784, 784, .15, 'sin'), (1046, 1046, .35, 'sin')],
    'golpe': [(0, 0, .15, 'noise')],
}

import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
PERSONAL = _os.path.join(HERE, 'personalizado')

class Assets:
    def svg(self, name):
        if name in COSTUMES: return COSTUMES[name]
        return BACKDROPS[name]
    def image(self, name):
        """Imagen de un disfraz o fondo: (bytes, extensión, centro x, centro y).
        Si existe personalizado/imagenes/<nombre>.svg o .png, se usa esa en lugar de la generada."""
        for ext in ('svg', 'png'):
            p = _os.path.join(PERSONAL, 'imagenes', name + '.' + ext)
            if _os.path.exists(p):
                data = open(p, 'rb').read()
                if ext == 'png':
                    from PIL import Image
                    w, h = Image.open(p).size
                else:
                    import re as _re
                    txt = data.decode('utf-8', 'ignore')
                    m = _re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', txt)
                    mw = _re.search(r'<svg[^>]*\swidth="([\d.]+)', txt); mh = _re.search(r'<svg[^>]*\sheight="([\d.]+)', txt)
                    w, h = (float(mw.group(1)), float(mh.group(1))) if mw and mh else (float(m.group(1)), float(m.group(2))) if m else (100, 100)
                return data, ext, w / 2, h / 2
        s = self.svg(name)
        return s['data'].encode('utf-8'), 'svg', s['cx'], s['cy']
    def wav(self, name):
        p = _os.path.join(PERSONAL, 'sonidos', name + '.wav')
        if _os.path.exists(p):
            with wave.open(p, 'rb') as w:
                n, rate = w.getnframes(), w.getframerate()
            return open(p, 'rb').read(), n, rate
        d, n = self._wav(name)
        return d, n, RATE
    def _wav(self, name):
        fr = _tone(SOUNDS[name])
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
            w.writeframes(b''.join(struct.pack('<h', max(-32767, min(32767, v))) for v in fr))
        return buf.getvalue(), len(fr)

# ------------------------------------------------------------------ estilo 8 bits
import sprites8 as _s8, backdrops8 as _b8
for _n, _g in _s8.SPRITES.items():
    COSTUMES[_n] = _px.svg(_g, px=_s8.PX.get(_n, 4))
for _n, _g in _b8.BACKS.items():
    _svg = _px.svg(_g, px=4)
    if _n == 'laberinto':
        _walls = ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="#2e3a87"/>' % w for w in _b8.MAZE_WALLS)
        _svg = dict(_svg, data=_svg['data'].replace('</svg>', _walls + '</svg>'))
    BACKDROPS[_n] = _svg
