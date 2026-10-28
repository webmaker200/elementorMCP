"""Build HealUs page assets (WebP rasters + SVGs from Figma vector geometry) and upload them.

usage: python3 assets.py <scratch dir with frame.json and raw/>  -> writes media.json next to this file
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageOps

S = sys.argv[1]
OUT = os.path.join(S, 'out'); os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA_JSON = os.path.join(HERE, '..', 'media.json')
AUTH = json.load(open(os.path.expanduser('~/.claude.json')))['mcpServers']['medcare-mso-elementor']['headers']['Authorization']
API = 'https://medcaredemo.online/medcare/wp-json/wp/v2/'

# ---------- SVG from Figma geometry (same approach as handoff/challenges/tools/mksvg.py)
doc = json.load(open(os.path.join(S, 'frame.json')))['nodes']['671:593']['document']
IDX, ABS = {}, {}


def walk(n, M):
    rt = n.get('relativeTransform')
    m = M if rt is None else M @ np.array([rt[0], rt[1], [0, 0, 1]])
    IDX[n['id']] = n; ABS[n['id']] = m
    for k in n.get('children', []):
        walk(k, m)


walk(doc, np.eye(3))


def svg(fid, color, opacity=1.0):
    f = IDX[fid]; fb = f['absoluteBoundingBox']; W, H = fb['width'], fb['height']
    ox, oy = ABS[fid][0, 2], ABS[fid][1, 2]
    out = []
    def go(n):
        if n.get('visible', True) is False:
            return
        if n is not f:
            M = ABS[n['id']]
            tr = f'matrix({M[0,0]:.5f} {M[1,0]:.5f} {M[0,1]:.5f} {M[1,1]:.5f} {M[0,2]-ox:.3f} {M[1,2]-oy:.3f})'
            for g in n.get('fillGeometry', []) if n.get('fills') else []:
                out.append(f'<path transform="{tr}" d="{g["path"]}"' + (' fill-rule="evenodd"' if g.get('windingRule') == 'EVENODD' else '') + '/>')
            for g in n.get('strokeGeometry', []) if n.get('strokes') else []:
                out.append(f'<path transform="{tr}" d="{g["path"]}"/>')
        for k in n.get('children', []):
            go(k)
    go(f)
    op = f' fill-opacity="{opacity:g}"' if opacity < 1 else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}" height="{H:g}" viewBox="0 0 {W:g} {H:g}">'
            f'<g fill="{color}"{op}>' + ''.join(out) + '</g></svg>')


SVGS = {
    'healus-mark-form': svg('671:1659', '#7FBCAE', 0.08),
    'healus-mark-cta': svg('671:1734', '#1A6554', 0.30),
    'healus-arrow-teal': svg('671:1743', '#318371'),
    # FAQ toggle: circle with + ; the vertical bar (last path) is hidden by page CSS when the item is open
    'healus-select-chevron': ('<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">'
                              '<path d="M2.5 5 7 9.5 11.5 5" fill="none" stroke="#318371" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'),
    'healus-faq-toggle': ('<svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 34 34">'
                          '<circle cx="17" cy="17" r="17" fill="#3DA28C" fill-opacity="0.14"/>'
                          '<path d="M11.5 17h11" stroke="#006750" stroke-width="1.4" stroke-linecap="round"/>'
                          '<path d="M17 11.5v11" stroke="#006750" stroke-width="1.4" stroke-linecap="round"/></svg>'),
}
for n, s in SVGS.items():
    open(os.path.join(OUT, n + '.svg'), 'w').write(s)

# ---------- rasters -> WebP
R = os.path.join(S, 'raw')


def webp(src, name, size=None, crop_square=False, q=82):
    im = Image.open(os.path.join(R, src))
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    if crop_square:
        im = ImageOps.fit(im, (min(im.size),) * 2, Image.LANCZOS)
    if size:
        im = im.resize(size, Image.LANCZOS)
    p = os.path.join(OUT, name + '.webp')
    im.save(p, 'WEBP', quality=q, method=6)
    return p


webp('mock-dashboard.png', 'healus-hero-dashboard')                  # 1500x902 (2x of 750x451)
webp('mock-note.png', 'healus-progress-note')                        # 1140x866 (2x of 570x433)
webp('mock-template.png', 'healus-specialty-template')               # 1338x883 (2x of 669x441)
webp('photo-crop.jpg', 'healus-physician-desk', q=80)                # 772x799 (1.25x of 617x639)
webp('logo', 'healus-logo', (388, 97))                               # 2x of 194px max display (97x24 in form)
for i in (1, 2, 3):
    webp(f'avatar-{i}', f'healus-avatar-{i}', (70, 70), crop_square=True, q=80)
for src, n in (('ic-note', 'healus-icon-note'), ('ic-rx', 'healus-icon-rx'), ('ic-lab', 'healus-icon-lab'),
               ('ic-contact', 'healus-icon-contact'), ('ic-shield', 'healus-icon-shield')):
    webp(src, n, q=90)

# ---------- upload (idempotent by file name)
media = json.load(open(MEDIA_JSON)) if os.path.exists(MEDIA_JSON) else {}
ALT = {'healus-hero-dashboard': 'HealUs EHR dashboard with appointments, referrals and claims',
       'healus-progress-note': 'HealUs progress note with completed charting sections',
       'healus-specialty-template': 'HealUs primary care annual wellness visit template',
       'healus-physician-desk': 'Physician working at her desk',
       'healus-logo': 'HealUs'}
for f in sorted(os.listdir(OUT)):
    name, ext = os.path.splitext(f)
    if name in media:
        continue
    mime = 'image/svg+xml' if ext == '.svg' else 'image/webp'
    r = subprocess.run(['curl', '-sS', '-m', '120', '-X', 'POST', '-H', 'Authorization: ' + AUTH,
                        '-H', f'Content-Disposition: attachment; filename="{f}"', '-H', 'Content-Type: ' + mime,
                        '--data-binary', '@' + os.path.join(OUT, f), API + 'media'], capture_output=True, text=True)
    d = json.loads(r.stdout)
    if 'id' not in d:
        print('UPLOAD FAILED', f, r.stdout[:200]); continue
    alt = ALT.get(name, '')
    subprocess.run(['curl', '-sS', '-m', '60', '-X', 'POST', '-H', 'Authorization: ' + AUTH, '-H', 'Content-Type: application/json',
                    '--data', json.dumps({'alt_text': alt, 'title': name}), API + f'media/{d["id"]}'], capture_output=True)
    media[name] = {'id': d['id'], 'url': d['source_url'], 'w': d.get('media_details', {}).get('width'),
                   'h': d.get('media_details', {}).get('height'), 'bytes': os.path.getsize(os.path.join(OUT, f))}
    print('uploaded', f, d['id'], media[name]['bytes'], 'B')
json.dump(media, open(MEDIA_JSON, 'w'), indent=1)
