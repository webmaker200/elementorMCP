"""Export Maximus assets from the Figma REST API -> WebP / clean SVG -> WP Media Library.

usage: FIGMA_TOKEN=... WP_BASIC_AUTH=... python3 export_assets.py <frame.json> [--upload]
  frame.json = GET /v1/files/<key>/nodes?ids=599:1630 (used for node bounds / render bounds)

Rasters are exported at 2x and cropped to the node's own box (Figma exports include
shadow/blur bleed); shadows are re-created in CSS. SVGs get their viewBox reset to the
node box and drop-shadow filters removed for the same reason.
"""
import json, os, re, subprocess, sys, time
from PIL import Image
import assets

KEY = 'oYqLJMmgAjdLKQeLgtDSM7'
TOK = os.environ['FIGMA_TOKEN']
OUT = assets.D

# key: (node id, kind, display width)
SVG = {
    'arrow-green': '599:1651', 'arrow-black': '599:2747',
    'logo-hitrust': '599:1654', 'logo-hipaa': '599:1691', 'logo-pci': '599:2131',
    'ic-hero-settings': '599:2734', 'ic-hero-cpu': '599:2721', 'ic-hero-file-plus': '599:2739',
    'ic-search': '599:2762', 'ic-claims-file': '599:2813', 'ic-payments': '599:2787', 'ic-pie': '599:2839',
    'pv-eligibility': '599:2765', 'pv-claims': '599:2820', 'pv-payments': '599:2792', 'pv-kpis': '599:2843',
    'logo-maximus': '599:3020', 'lineart': '599:3025', 'check-24': '599:3030', 'x-16': '599:3062',
    'check-28': '599:2867', 'chart-line': '599:3400', 'ic-shield': '599:3723',
    'ic-settings': '599:3742', 'ic-cpu': '599:3749', 'ic-eye': '599:3764', 'ic-link': '599:3771',
    'logo-mark': '599:3808', 'cta-mark': '599:3881', 'chevron-down': '599:3853',
}
PNG = {  # exported at 2x, cropped to the node box
    'logo-aicpa-soc': '599:1706',  # 424 vectors -> 270 KB as SVG, so WebP
    'avatar-1': '599:1639', 'avatar-2': '599:1641', 'avatar-3': '599:1643',
    'eligibility-workflow': '599:2881', 'eligibility-donut': '599:2955', 'eligibility-activity': '599:2979',
    'claims-rule-engine': '599:3172', 'claims-scrubbing': '599:3204', 'claims-status': '599:3268', 'claims-workflows': '599:3325',
    'trust-claims': '599:3491', 'trust-payments': '599:3602', 'trust-aging': '599:3664',
}
FILLS = {  # original image fills: (imageRef prefix, target width)
    'integrations-photo': ('353398e1d7', 1236),
    'watermark': ('f4bb4eb386', 1949),
}
ALT = {
    'avatar-1': 'Physician', 'avatar-2': 'Physician', 'avatar-3': 'Physician',
    'logo-hitrust': 'HITRUST CSF Certified', 'logo-hipaa': 'HIPAA compliant', 'logo-aicpa-soc': 'AICPA SOC', 'logo-pci': 'PCI Security Standards Council',
    'logo-maximus': 'Maximus', 'eligibility-workflow': 'Maximus eligibility verification workflow',
    'eligibility-donut': 'Coverage verified widget', 'eligibility-activity': 'Eligibility checks today chart',
    'claims-rule-engine': 'Intelligent rule engine screen', 'claims-scrubbing': 'Auto claim scrubbing screen',
    'claims-status': 'Auto claim status screen', 'claims-workflows': 'Smart workflows screen',
    'trust-claims': 'Maximus claims dashboard', 'trust-payments': 'Payments widget', 'trust-aging': 'A/R aging widget',
    'integrations-photo': 'Healthcare team using connected systems',
}


def api(path):
    for i in range(5):
        r = subprocess.run(['curl', '-sS', '-m', '180', '-H', 'X-Figma-Token: ' + TOK, 'https://api.figma.com/v1/' + path],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            d = json.loads(r.stdout)
            if not d.get('err') and d.get('status', 200) == 200:
                return d
        time.sleep(3 * (i + 1))
    raise RuntimeError(r.stdout[:300] + r.stderr)


def main(frame_json, upload):
    idx = {}

    def walk(n):
        idx[n['id']] = n
        for c in n.get('children', []):
            walk(c)
    walk(json.load(open(frame_json))['nodes']['599:1630']['document'])
    local = {}

    urls = api(f"images/{KEY}?ids={','.join(SVG.values())}&format=svg&svg_outline_text=false")['images']
    for k, nid in SVG.items():
        p = os.path.join(OUT, f'maximus-{k}.svg')
        assets.download(urls[nid], p)
        n = idx[nid]; b = n['absoluteBoundingBox']; rb = n.get('absoluteRenderBounds') or b
        svg = open(p).read()
        ox, oy = b['x'] - rb['x'], b['y'] - rb['y']
        if re.search(r'filter="url\(#filter[^)]*_d', svg):  # drop-shadow bleed -> crop back to the node box
            w, h = round(b['width'], 3), round(b['height'], 3)
            svg = re.sub(r'<svg width="[^"]+" height="[^"]+" viewBox="[^"]+"',
                         f'<svg width="{w}" height="{h}" viewBox="{round(ox, 3)} {round(oy, 3)} {w} {h}"', svg, 1)
            svg = re.sub(r'\sfilter="url\(#filter[^)]*_d[^)]*\)"', '', svg)
        svg = re.sub(r'\s(preserveAspectRatio="none"|overflow="visible"|style="[^"]*"|id="(?!(paint|clip|filter|mask|pattern|image))[^"]*")', '', svg)
        open(p, 'w').write(svg)
        local[k] = p

    urls = api(f"images/{KEY}?ids={','.join(PNG.values())}&format=png&scale=2")['images']
    for k, nid in PNG.items():
        raw = assets.download(urls[nid], os.path.join(OUT, f'maximus-{k}.png'))
        n = idx[nid]; b = n['absoluteBoundingBox']; rb = n.get('absoluteRenderBounds') or b
        im = Image.open(raw).convert('RGBA')
        # render bounds larger than the node = shadow/blur bleed; smaller = clipped by a parent (keep)
        x0, y0 = round(max(0, b['x'] - rb['x']) * 2), round(max(0, b['y'] - rb['y']) * 2)
        im = im.crop((max(0, x0), max(0, y0), max(0, x0) + round(b['width'] * 2), max(0, y0) + round(b['height'] * 2)))
        p = os.path.join(OUT, f'maximus-{k}.webp')
        im.save(p, 'WEBP', quality=84, method=6)
        os.remove(raw)
        local[k] = p

    fills = api(f'files/{KEY}/images')['meta']['images']
    for k, (ref, tw) in FILLS.items():
        url = next(v for r, v in fills.items() if r.startswith(ref))
        raw = assets.download(url, os.path.join(OUT, f'maximus-{k}.src'))
        p, size = assets.to_webp(raw, os.path.join(OUT, f'maximus-{k}.webp'), tw // 2, quality=72, max_w=tw)
        os.remove(raw)
        local[k] = p

    for k, p in local.items():
        print(f'{k:24s} {os.path.getsize(p):8d} B  {os.path.basename(p)}')
    if upload:
        reg = assets.reg()
        for k, p in local.items():
            if k in reg:
                continue
            info = assets.upload(p, 'Maximus ' + k.replace('-', ' '), ALT.get(k, ''))
            info['bytes'] = os.path.getsize(p)
            reg[k] = info
            assets.save_reg(reg)
            print('uploaded', k, info['id'])


if __name__ == '__main__':
    main(sys.argv[1], '--upload' in sys.argv)
