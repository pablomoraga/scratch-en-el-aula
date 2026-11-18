# -*- coding: utf-8 -*-
"""Herramientas para dibujar pixel art por formas: relleno, contorno y sombreado automáticos."""
import math

DARK = {'Y': 'y', 'B': 'b', 'L': 'B', 'R': 'r', 'P': 'R', 'G': 'g', 'V': 'G', 'S': 's', 'W': 'w', 'w': 'S', 'O': 'o',
        'M': 'm', 'C': 'c', 'N': 'n', 'H': 'Y', 'y': 'o', 'b': 'K', 'g': 'K', 'r': 'K', 's': 'k', 'o': 'n', 'n': 'K', 'c': 'b', 'm': 'K'}
LIGHT = {'Y': 'H', 'B': 'L', 'R': 'P', 'G': 'V', 'S': 'W', 'O': 'Y', 'C': 'W', 'N': 'O', 'M': 'P', 'w': 'W', 's': 'S', 'b': 'B',
         'g': 'G', 'r': 'R', 'y': 'Y', 'L': 'W', 'V': 'W', 'n': 'N', 'c': 'C', 'm': 'M', 'o': 'O'}

class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [['.'] * w for _ in range(h)]
    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h: self.g[y][x] = c
    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else '.'
    def shape(self, inside, c):
        for y in range(self.h):
            for x in range(self.w):
                if inside(x + .5, y + .5): self.g[y][x] = c
        return self
    def rect(self, x0, y0, x1, y1, c):            # incluye x1,y1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): self.px(x, y, c)
        return self
    def ellipse(self, cx, cy, rx, ry, c):
        return self.shape(lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1, c)
    def circle(self, cx, cy, r, c): return self.ellipse(cx, cy, r, r, c)
    def poly(self, pts, c):
        def inside(x, y):
            n, ins = len(pts), False
            for i in range(n):
                x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: ins = not ins
            return ins
        return self.shape(inside, c)
    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)
        return self
    def shade(self, only=None):
        """Brillo arriba-izquierda y sombra abajo-derecha en el borde de cada zona de color."""
        src = [r[:] for r in self.g]
        for y in range(self.h):
            for x in range(self.w):
                c = src[y][x]
                if c in '.K' or (only and c not in only): continue
                def other(dx, dy):
                    yy, xx = y + dy, x + dx
                    return not (0 <= xx < self.w and 0 <= yy < self.h) or src[yy][xx] != c
                if (other(1, 0) or other(0, 1)) and c in DARK: self.g[y][x] = DARK[c]
                elif (other(-1, 0) or other(0, -1)) and c in LIGHT: self.g[y][x] = LIGHT[c]
        return self
    def outline(self, c='K'):
        src = [r[:] for r in self.g]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != '.': continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < self.w and 0 <= yy < self.h and src[yy][xx] not in '.':
                        self.g[y][x] = c; break
        return self
    def put(self, x, y, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch != '.': self.px(x + dx, y + dy, ch)
        return self
    def rows(self): return [''.join(r) for r in self.g]
