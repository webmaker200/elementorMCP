"""Prepare AI Medical Coder (Sophus) page assets from the design bundle renders.
usage: venv-python prep_assets.py <scratch dir with cap/ and assets/>  -> writes ../assets/*
Rasters -> WebP (alpha kept where the card shadow needs it); SVG logo marks stripped of the C2PA <metadata>."""
import os, re, sys
from PIL import Image

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
os.makedirs(OUT, exist_ok=True)

def webp(src, name, width=None, crop=None, q=80):
    im = Image.open(src).convert('RGBA')
    if crop:
        im = im.crop(crop)
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    alpha = im.getchannel('A').getextrema()[0] < 255
    if not alpha:
        im = im.convert('RGB')
    p = os.path.join(OUT, name + '.webp')
    im.save(p, 'WEBP', quality=q, method=6)
    print(name, im.size, 'alpha' if alpha else '', os.path.getsize(p) // 1024, 'KB')

c = lambda n: os.path.join(SRC, 'cap', n + '.png')
webp(c('dash-coder'), 'sophus-coder-dashboard', 1800, q=82)
webp(c('dash-manager'), 'sophus-manager-dashboard', 1800, q=82)
im = Image.open(c('how-panel')); webp(c('how-panel'), 'sophus-claim-card-panel', 1130, crop=(80, 80, im.width - 80, im.height - 80))
for n in ('seat-coders', 'seat-managers', 'seat-billing'):
    webp(c(n), 'sophus-' + n, 1170)
for n in ('m-payer', 'm-status', 'm-kept', 'm-audit', 'm-phone'):
    webp(c(n), 'sophus-' + n.replace('m-', 'card-'), None, q=82)
for f, n in (('0404bb0e', 'assign'), ('2afa7346', 'review'), ('8f2484d8', 'returns'), ('a97d87d7', 'audit')):
    webp(os.path.join(SRC, 'assets', f + '.png'), 'sophus-icon-' + n, 96, q=90)
for f, n in (('9c7a99c8', 'sophus-mark'), ('38cafbef', 'sophus-mark-light'), ('fe0c6399', 'sophus-mark-white')):
    s = open(os.path.join(SRC, 'assets', f + '.svg')).read()
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    s = re.sub(r'\s*xmlns:c2pa="[^"]*"', '', s)
    open(os.path.join(OUT, n + '.svg'), 'w').write(s)
    print(n, len(s), 'B')
# speed-section connector lines (from the design markup)
paths = ''.join(f'<path d="M0 {y} C 320 {y} 420 180 600 180"/>' for y in (20, 70, 120, 165, 200, 245, 295, 345))
paths += ''.join(f'<path d="M1200 {y} C 880 {y} 780 180 600 180"/>' for y in (20, 70, 120, 165, 200, 245, 295, 345))
open(os.path.join(OUT, 'sophus-speed-lines.svg'), 'w').write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" preserveAspectRatio="none">'
    f'<g fill="none" stroke="rgba(148,67,236,.32)" stroke-width="1" vector-effect="non-scaling-stroke">{paths}</g></svg>')
# accordion toggle: plus that becomes minus when the item is open (CSS hides the vertical stroke)
open(os.path.join(OUT, 'sophus-acc-toggle.svg'), 'w').write(
    '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round"><path d="M1.5 6h9"/><path d="M6 1.5v9"/></svg>')
# same toggle drawn in the 28px circle (Elementor's e-svg stretches the svg to its wrapper)
open(os.path.join(OUT, 'sophus-acc-plus.svg'), 'w').write(
    '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round"><path d="M8.5 14h11"/><path d="M14 8.5v11"/></svg>')
print('done')
