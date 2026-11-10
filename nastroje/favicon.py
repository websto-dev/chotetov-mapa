"""Favicon Chotětova: izometrický čtverec trávy s kostelem sv. Prokopa (věž s cibulovou bání).
python nastroje/favicon.py  ->  web/favicon.svg, site/favicon.svg, site/favicon-32.png, site/apple-touch-icon.png, site/favicon.ico
"""
import os, shutil, subprocess, sys

K = 1.45            # měřítko izometrie
CX, CY = 32, 39.5   # obrazovková poloha bodu (0, 0, 0)
OUT = '#1b2233'     # obrys jako v mapě


def P(x, y, z=0.0):
    return (CX + (x - y) * K, CY + (x + y) * K / 2 - z * K * 0.95)


def poly(pts, fill, stroke=OUT, sw=0.9):
    s = ' '.join(f'{a:.2f},{b:.2f}' for a, b in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def box(x0, x1, y0, y1, z0, z1, top, left, right):
    """viditelné stěny kvádru: vršek, levá (y = y1) a pravá (x = x1)"""
    return [
        poly([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], left),
        poly([P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)], right),
        poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], top),
    ]


g = []
# zemní čtverec: tráva s hliněným bokem
T0, T1, D = -10.5, 10.5, 2.2
g += [poly([P(T0, T1, 0), P(T1, T1, 0), P(T1, T1, -D), P(T0, T1, -D)], '#7a5a3c'),
      poly([P(T1, T0, 0), P(T1, T1, 0), P(T1, T1, -D), P(T1, T0, -D)], '#5c4330'),
      poly([P(T0, T0, 0), P(T1, T0, 0), P(T1, T1, 0), P(T0, T1, 0)], '#6fae45')]
# cesta k průčelí
g.append(poly([P(-10.5, -0.9, 0), P(-6.6, -0.9, 0), P(-6.6, 0.9, 0), P(-10.5, 0.9, 0)], '#c9b48a', stroke='none'))

WALL_T, WALL_L, WALL_R = '#f6efdf', '#efe3c8', '#cdbd9c'
ROOF_L, ROOF_R = '#c8502f', '#9c3a22'
# loď: kvádr se sedlovou střechou po ose x
x0, x1, y0, y1, h, rz = -2.6, 8.2, -3.0, 3.0, 5.0, 8.4
g += box(x0, x1, y0, y1, 0, h, WALL_T, WALL_L, WALL_R)[:2]
g.append(poly([P(x1, y0, h), P(x1, y1, h), P(x1, 0, rz)], WALL_R))                         # štít
g.append(poly([P(x0, 0, rz), P(x1, 0, rz), P(x1, y1, h), P(x0, y1, h)], ROOF_L))           # střecha k divákovi
# okna lodi (levá stěna)
for wx in (0.8, 4.0):
    g.append(poly([P(wx, y1, 1.6), P(wx + 1.3, y1, 1.6), P(wx + 1.3, y1, 3.6), P(wx, y1, 3.6)], '#33465e', stroke='none'))
# presbytář vzadu je schovaný, věž vpředu (průčelí na západ = k levému hornímu rohu)
tx0, tx1, ty0, ty1, th = -6.6, -2.4, -2.1, 2.1, 12.2
g += box(tx0, tx1, ty0, ty1, 0, th, WALL_T, WALL_L, WALL_R)
# hodiny a okno věže
cxw, cyw = P(tx0 + 2.1, ty1, th - 2.0)
g.append(f'<circle cx="{cxw:.2f}" cy="{cyw:.2f}" r="1.55" fill="#f2c21a" stroke="{OUT}" stroke-width="0.6"/>')
g.append(poly([P(tx0 + 1.5, ty1, 4.2), P(tx0 + 2.7, ty1, 4.2), P(tx0 + 2.7, ty1, 7.0), P(tx0 + 1.5, ty1, 7.0)], '#33465e', stroke='none'))
# cibulová báně nad věží (2D silueta nad středem věže)
bx, by = P((tx0 + tx1) / 2, (ty0 + ty1) / 2, th)
dome = (f'M{bx - 5.2:.2f},{by:.2f} C{bx - 5.6:.2f},{by - 3.2:.2f} {bx - 1.2:.2f},{by - 4.2:.2f} {bx - 0.9:.2f},{by - 7.6:.2f} '
        f'L{bx + 0.9:.2f},{by - 7.6:.2f} C{bx + 1.2:.2f},{by - 4.2:.2f} {bx + 5.6:.2f},{by - 3.2:.2f} {bx + 5.2:.2f},{by:.2f} Z')
g.append(f'<path d="{dome}" fill="#3f6b5c" stroke="{OUT}" stroke-width="0.9" stroke-linejoin="round"/>')
g.append(f'<path d="M{bx - 3.6:.2f},{by - 1.2:.2f} C{bx - 3.4:.2f},{by - 3.0:.2f} {bx - 1.6:.2f},{by - 3.6:.2f} {bx - 1.1:.2f},{by - 5.4:.2f}" '
         f'fill="none" stroke="#7fb3a0" stroke-width="0.9" stroke-linecap="round"/>')
# zlatý kříž
g.append(f'<path d="M{bx:.2f},{by - 7.6:.2f} V{by - 13.2:.2f} M{bx - 1.6:.2f},{by - 11.4:.2f} H{bx + 1.6:.2f}" stroke="#f2c21a" stroke-width="1.3" stroke-linecap="round"/>')
# stromy
for (sx, sy), r in ((P(7.0, 7.5), 3.3), (P(-8.3, 6.0), 2.7), (P(8.3, -6.5), 2.6)):
    g.append(f'<ellipse cx="{sx:.2f}" cy="{sy + 0.6:.2f}" rx="{r:.2f}" ry="{r * 0.45:.2f}" fill="#2e5b2a" opacity="0.45"/>')
    g.append(f'<circle cx="{sx:.2f}" cy="{sy - r * 0.7:.2f}" r="{r:.2f}" fill="#3f8a3a" stroke="{OUT}" stroke-width="0.8"/>')
    g.append(f'<circle cx="{sx - r * 0.35:.2f}" cy="{sy - r * 1.0:.2f}" r="{r * 0.35:.2f}" fill="#6dbb55"/>')

svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' + ''.join(g) + '</svg>\n')
os.makedirs('site', exist_ok=True)
open('web/favicon.svg', 'w', encoding='utf-8').write(svg)
shutil.copy('web/favicon.svg', 'site/favicon.svg')

# PNG a ICO přes Chromium z Playwrightu (stejný jako pro render mapy)
js = r'''
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const svg = fs.readFileSync('web/favicon.svg', 'utf8');
  for (const [n, f, bg] of [[32, 'site/favicon-32.png', 'transparent'], [48, 'build/favicon-48.png', 'transparent'], [180, 'site/apple-touch-icon.png', '#1b2233'], [512, 'build/favicon-512.png', 'transparent']]) {
    await p.setViewportSize({ width: n, height: n });
    await p.setContent(`<html><body style="margin:0;background:${bg}"><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" width="${n}" height="${n}"></body></html>`);
    await p.screenshot({ path: f, omitBackground: bg === 'transparent' });
  }
  await b.close();
})();
'''
os.makedirs('build', exist_ok=True)
subprocess.run(['node', '-e', js], check=True)
from PIL import Image
Image.open('build/favicon-48.png').save('site/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
print('favicon hotová')
