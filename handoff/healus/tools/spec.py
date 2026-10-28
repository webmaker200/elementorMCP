"""Dump a compact, readable spec of each HealUs section from the Figma REST node JSON."""
import json, sys
d = json.load(open(sys.argv[1]))['nodes']['671:593']['document']
OX, OY = d['absoluteBoundingBox']['x'], d['absoluteBoundingBox']['y']


def col(c, op=1):
    a = c.get('a', 1) * op
    h = '#%02X%02X%02X' % (round(c['r'] * 255), round(c['g'] * 255), round(c['b'] * 255))
    return h if a > 0.995 else f'{h}@{a:.2f}'


def paints(ps):
    out = []
    for p in ps or []:
        if p.get('visible', True) is False:
            continue
        op = p.get('opacity', 1)
        if p['type'] == 'SOLID':
            out.append(col(p['color'], op))
        elif p['type'].startswith('GRADIENT'):
            h = p['gradientHandlePositions']
            stops = ','.join(col(s['color'], op) + '@%.2f' % s['position'] for s in p['gradientStops'])
            out.append('%s(%s h0=%.2f,%.2f h1=%.2f,%.2f)' % (p['type'][9:].lower(), stops, h[0]['x'], h[0]['y'], h[1]['x'], h[1]['y']))
        elif p['type'] == 'IMAGE':
            out.append(f"IMAGE({p.get('scaleMode')} ref={p.get('imageRef', '')[:8]})")
    return out


def fx(es):
    out = []
    for e in es or []:
        if e.get('visible', True) is False:
            continue
        if e['type'] in ('DROP_SHADOW', 'INNER_SHADOW'):
            o = e['offset']
            out.append(f"{'inset ' if e['type'] == 'INNER_SHADOW' else ''}shadow({o['x']:g},{o['y']:g},{e['radius']:g},{e.get('spread', 0):g},{col(e['color'])})")
        else:
            out.append(f"{e['type'].lower()}({e.get('radius', 0):g})")
    return out


def line(n, sx, sy):
    b = n.get('absoluteBoundingBox') or {}
    s = f"{n['type']} {n['id']} '{n['name'][:34]}' @{round(b.get('x', 0) - sx)},{round(b.get('y', 0) - sy)} {round(b.get('width', 0))}x{round(b.get('height', 0))}"
    if n.get('visible', True) is False:
        s += ' HIDDEN'
    if n.get('opacity', 1) < 1:
        s += f" op={n['opacity']:.2f}"
    if n.get('layoutMode') and n['layoutMode'] != 'NONE':
        pad = [n.get(k, 0) for k in ('paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft')]
        s += f" {n['layoutMode'][0]}gap={n.get('itemSpacing', 0):g} pad={','.join(f'{p:g}' for p in pad)} align={n.get('primaryAxisAlignItems', '')[:5]}/{n.get('counterAxisAlignItems', '')[:5]}"
        if n.get('layoutWrap') == 'WRAP':
            s += ' wrap'
    f = paints(n.get('fills')) if n['type'] != 'TEXT' else []
    if f:
        s += ' fill=' + '|'.join(f)
    st = paints(n.get('strokes'))
    if st:
        s += f" stroke={n.get('strokeWeight', 1):g}:{'|'.join(st)}"
        if n.get('individualStrokeWeights'):
            s += ' sides=' + ','.join(f'{v:g}' for v in n['individualStrokeWeights'].values())
    r = n.get('cornerRadius') or n.get('rectangleCornerRadii')
    if r:
        s += f' r={r}'
    e = fx(n.get('effects'))
    if e:
        s += ' fx=' + ' '.join(e)
    if n.get('clipsContent'):
        s += ' clip'
    if n['type'] == 'TEXT':
        t = n.get('style', {})
        lh = t.get('lineHeightPx')
        s += (f" «{n.get('characters', '').replace(chr(10), ' / ')[:140]}» font={t.get('fontFamily')} {t.get('fontWeight')} "
              f"{t.get('fontSize'):g}/{lh:.1f} ls={t.get('letterSpacing', 0):.2f} color={'|'.join(paints(n.get('fills')))} align={t.get('textAlignHorizontal', '')[:4]}")
        if t.get('textCase'):
            s += f" case={t['textCase']}"
        ov = n.get('styleOverrideTable')
        if ov:
            s += ' overrides=' + ';'.join(f"{k}:{v.get('fontWeight', '')}/{'|'.join(paints(v.get('fills')))}" for k, v in ov.items())
    return s


def walk(n, sx, sy, depth, out, maxd):
    out.append('  ' * depth + line(n, sx, sy))
    if depth < maxd and n['type'] not in ('VECTOR', 'BOOLEAN_OPERATION'):
        for c in n.get('children', []):
            walk(c, sx, sy, depth + 1, out, maxd)


for sec in d['children']:
    sid = sec['id']
    if sid not in sys.argv[3].split(','):
        continue
    b = sec['absoluteBoundingBox']
    out = []
    walk(sec, b['x'], b['y'], 0, out, int(sys.argv[4]) if len(sys.argv) > 4 else 99)
    open(f"{sys.argv[2]}/spec-{sid.replace(':', '_')}.txt", 'w').write('\n'.join(out))
    print(sid, len(out), 'lines')
