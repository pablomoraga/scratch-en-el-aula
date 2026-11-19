# -*- coding: utf-8 -*-
"""Tarjetas imprimibles A5 (dos por A4, anverso y reverso) a partir de los datos de los retos."""
import html, subprocess, os
from sb import Blk, S, r_block, walk
import pixel, robit

e = html.escape
NIV = {1: '★☆☆', 2: '★★☆', 3: '★★★'}

def palette(project, limit=10):
    seen, out = set(), []
    for n in walk(project):
        sp = S[n.op]
        if sp['kind'] in ('rep', 'bool') or n.op in seen: continue
        seen.add(n.op)
        a = {k: v for k, v in n.a.items() if not isinstance(v, list)}
        out.append(Blk(n.op, a))
    return out[:limit]

def card_front(r, img):
    pasos = ''.join('<li>%s</li>' % p for p in r['pasos'])
    return ('<div class="card front"><div class="band"><div class="robit">%s</div><div><div class="num">RETO %s</div>'
            '<div class="meta">%s · %s</div></div><div class="chips">%s</div></div>'
            '<h1>%s</h1><p class="obj"><b>Objetivo:</b> %s</p><h2>Paso a paso</h2><ol>%s</ol>'
            '<div class="foot">Scratch en el aula · Aprende Scratch con Robit</div></div>') % (
        img, e(r['num']), NIV[r['nivel']], e(r['tiempo']), ''.join('<span>%s</span>' % e(c) for c in r['conceptos']),
        e(r['title']), r['objetivo'], pasos)

def card_back(r, blocks_html):
    pistas = ''.join('<li>%s</li>' % p for p in r['pistas'])
    amp = ''.join('<li>%s</li>' % p for p in r['ampliar'])
    return ('<div class="card back"><div class="num small">RETO %s · %s</div><h2>Bloques que te ayudarán</h2><div class="pal">%s</div>'
            '<h2>Pistas</h2><ul>%s</ul><h2>¿Y si…?</h2><ul>%s</ul>'
            '<div class="foot">Ayuda y solución en la web del material · © Pablo Moraga · CC BY-NC-ND 4.0</div></div>') % (
        e(r['num']), e(r['title']), blocks_html, pistas, amp)

CSS = '''@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font:12.5pt/1.4 "DejaVu Sans",sans-serif;color:#1b1b2f}
.sheet{width:210mm;height:297mm;page-break-after:always;display:flex;flex-direction:column}
.card{width:210mm;height:148.5mm;padding:9mm 11mm;border-bottom:1px dashed #adb3bc;position:relative;overflow:hidden;background:#fdfdfe}
.band{display:flex;align-items:center;gap:5mm;background:#1b1b2f;color:#fff;margin:-9mm -11mm 5mm;padding:4mm 11mm}
.robit svg{width:15mm;height:auto;display:block}
.num{font:700 15pt "DejaVu Sans Mono",monospace;letter-spacing:.06em;color:#ffbe2e}.num.small{font-size:10pt;color:#e0861a;margin-bottom:2mm}
.meta{font:10pt "DejaVu Sans Mono",monospace;color:#c9cfe0}
.chips{margin-left:auto;display:flex;flex-wrap:wrap;gap:2mm;justify-content:flex-end;max-width:85mm}
.chips span{font:8.5pt "DejaVu Sans Mono",monospace;border:1px solid #ffbe2e;color:#ffbe2e;border-radius:4mm;padding:1mm 2.5mm}
h1{font-size:23pt;margin:0 0 3mm}h2{font-size:11pt;margin:4mm 0 1.5mm;color:#1d5aa6;text-transform:uppercase;letter-spacing:.04em}
.obj{background:#fff3b0;border:1.5px solid #1b1b2f;border-radius:3mm;padding:2.5mm 4mm;margin:0}
ol,ul{margin:0;padding-left:6mm}li{margin:.8mm 0}
.pal{display:flex;flex-wrap:wrap;gap:1.5mm 4mm;zoom:.85}
.foot{position:absolute;bottom:4mm;left:11mm;right:11mm;font:8pt "DejaVu Sans Mono",monospace;color:#8a8070;border-top:1px solid #e4dccb;padding-top:1.5mm}'''

def build_pdf(retos, projects, inline, out_pdf, tmpdir):
    img = pixel.svg(robit.ROBIT1, px=4)['data']
    sheets = []
    for i in range(0, len(retos), 2):
        pair = retos[i:i + 2]
        fronts = ''.join(card_front(r, img) for r in pair)
        backs = ''.join(card_back(r, ''.join('<div class="sb-script sb-solo">%s</div>' % r_block(b)
                                                for b in palette(projects[r['slug']]))) for r in pair)
        sheets.append('<div class="sheet">%s</div><div class="sheet">%s</div>' % (fronts, backs))
    doc = '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (CSS, inline(''.join(sheets)))
    os.makedirs(tmpdir, exist_ok=True)
    src = os.path.join(tmpdir, os.path.basename(out_pdf).replace('.pdf', '.html'))
    open(src, 'w', encoding='utf-8').write(doc)
    import shutil as _sh
    chrome = _sh.which('google-chrome') or _sh.which('google-chrome-stable') or _sh.which('chromium') or _sh.which('chromium-browser')
    subprocess.run([chrome, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + out_pdf, 'file://' + src], check=True, capture_output=True, timeout=180)
    return src
