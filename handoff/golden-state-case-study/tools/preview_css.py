"""struct json -> CSS file approximating Elementor's front-end output for local styles."""
import json, sys
st = json.load(open(sys.argv[1]))
MQ = {'laptop': 1440, 'tablet_extra': 1200, 'tablet': 1024, 'mobile_extra': 880, 'mobile': 767}
out = []
def walk(e):
    s = e.get('styles') or {}
    if isinstance(s, dict) and s.get('css'):
        css = s['css']
        for k, v in MQ.items():
            css = css.replace(f'@media(--{k})', f'@media (max-width:{v}px)')
        out.append(f".elementor .{s['__style_id']}{{{css}}}")
    for k in e.get('elements', []): walk(k)
for e in st['elements']: walk(e)
open(sys.argv[2], 'w').write('\n'.join(out))
print(len(out), 'rules')
