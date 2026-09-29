"""Figma asset pipeline: download -> (raster: WebP, resized) / (vector: SVG) -> WP media upload."""
import json, os, subprocess, time, re
from PIL import Image
import mcp

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figma', 'assets')
os.makedirs(D, exist_ok=True)
REG = os.path.join(D, 'registry.json')


def reg():
    return json.load(open(REG)) if os.path.exists(REG) else {}


def save_reg(r):
    json.dump(r, open(REG, 'w'), indent=1)


def download(url, path):
    for i in range(5):
        r = subprocess.run(['curl', '-sSL', '-m', '120', '-o', path, '-w', '%{http_code}', url], capture_output=True, text=True)
        if r.stdout.strip() == '200' and os.path.getsize(path) > 0:
            return path
        time.sleep(2 * (i + 1))
    raise RuntimeError(f'download failed {url}: {r.stdout} {r.stderr}')


def to_webp(src, dst, display_w, quality=82, max_w=1600):
    """Resize to 2x the displayed width (capped) and encode WebP."""
    im = Image.open(src)
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGBA')
    target = min(max_w, display_w * 2, im.width)
    if im.width > target:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=quality, method=6)
    return dst, im.size


def upload(path, title, alt=''):
    mime = 'image/svg+xml' if path.endswith('.svg') else 'image/webp'
    name = os.path.basename(path)
    cmd = ['curl', '-sS', '-m', '180', '-X', 'POST', '-H', mcp.AUTH,
           '-H', f'Content-Disposition: attachment; filename="{name}"', '-H', f'Content-Type: {mime}',
           '--data-binary', '@' + path, 'https://medcaredemo.online/medcare/wp-json/wp/v2/media']
    for i in range(5):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            d = json.loads(r.stdout)
            if 'id' not in d:
                raise RuntimeError(f'upload rejected {name}: {r.stdout[:300]}')
            if title or alt:
                mcp.rest('POST', f"media/{d['id']}", {'title': title, 'alt_text': alt})
            md = d.get('media_details') or {}
            return {'id': d['id'], 'url': d['source_url'], 'w': md.get('width'), 'h': md.get('height')}
        time.sleep(2 * (i + 1))
    raise RuntimeError(r.stderr)


def process(key, url, kind, display_w=None, title='', alt=''):
    """kind: 'svg' or 'webp'. Idempotent via registry."""
    r = reg()
    if key in r:
        return r[key]
    slug = 'maximus-' + re.sub(r'[^a-z0-9]+', '-', key.lower()).strip('-')
    if kind == 'svg':
        p = download(url, os.path.join(D, slug + '.svg'))
        svg = open(p).read()
        # strip Figma export noise so the file renders at its intrinsic size
        svg = re.sub(r'\s(preserveAspectRatio="none"|overflow="visible"|style="display: block;"|id="[^"]*")', '', svg)
        open(p, 'w').write(svg)
        info = upload(p, title or key, alt)
        info['bytes'] = os.path.getsize(p)
    else:
        raw = download(url, os.path.join(D, slug + '.src'))
        p, size = to_webp(raw, os.path.join(D, slug + '.webp'), display_w or 800)
        info = upload(p, title or key, alt)
        info.update({'bytes': os.path.getsize(p), 'px': size})
    r[key] = info
    save_reg(r)
    return info
