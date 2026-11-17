"""Draw the Kansas cities map (SVG) used in the "Medical Billing Services Across Kansas Cities and Regions" section.
Real lon/lat projected to the viewBox; Blue KC area = Johnson + Wyandotte counties (approximate outlines)."""
import math
W, H, PAD, PADR = 700, 330, 18, 150
LON0, LON1, LAT0, LAT1 = -102.08, -94.55, 36.97, 40.03
k = math.cos(math.radians(38.5))
sx = (W - PAD - PADR) / ((LON1 - LON0) * k)
sy = sx
H = round((LAT1 - LAT0) * sy + 2 * PAD)


def xy(lon, lat):
    return round(PAD + (lon - LON0) * k * sx, 1), round(PAD + (LAT1 - lat) * sy, 1)


STATE = [(-102.05, 40.0), (-95.31, 40.0), (-95.08, 39.87), (-94.88, 39.78), (-95.11, 39.56), (-94.95, 39.40),
         (-94.88, 39.20), (-94.61, 39.11), (-94.61, 37.0), (-102.05, 37.0)]
BLUEKC = [(-94.91, 39.20), (-94.88, 39.20), (-94.61, 39.11), (-94.61, 38.74), (-95.06, 38.74), (-95.06, 39.04), (-94.91, 39.04)]
CITIES = [('Kansas City, KS', 39.114, -94.627, 'r'), ('Overland Park', 38.982, -94.671, 'l'), ('Manhattan', 39.184, -96.572, 'a'),
          ('Hays', 38.879, -99.327, 'b'), ('Salina', 38.840, -97.611, 'b'), ('Topeka', 39.048, -95.678, 'a'),
          ('Lawrence', 38.972, -95.235, 'b'), ('Wichita', 37.687, -97.330, 'b'), ('Garden City', 37.971, -100.873, 'b'),
          ('Dodge City', 37.753, -100.017, 'b'), ('Pittsburg', 37.411, -94.705, 'r')]


def poly(pts):
    return ' '.join(f'{x},{y}' for x, y in (xy(*p) for p in pts))


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-label="Kansas cities served by MedCare MSO medical billing services">',
       f'<polygon points="{poly(STATE)}" fill="#EAF5FF" stroke="#0367A1" stroke-width="2.5" stroke-linejoin="round"/>',
       f'<polygon points="{poly(BLUEKC)}" fill="#7EB13E" fill-opacity="0.85" stroke="#5E8A2C" stroke-width="1.2" stroke-linejoin="round"/>']
for name, lat, lon, pos in CITIES:
    x, y = xy(lon, lat)
    out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#0367A1" stroke="#FFFFFF" stroke-width="2"/>')
    dx, dy, anchor = {'r': (12, 6, 'start'), 'l': (-12, 6, 'end'), 'a': (0, -14, 'middle'), 'b': (0, 26, 'middle')}[pos]
    if name == 'Kansas City, KS':
        dx, dy, anchor = (12, -6, 'start')
    if name == 'Overland Park':
        dx, dy, anchor = (12, 20, 'start')
    if name == 'Topeka':
        dx, dy, anchor = (0, -14, 'middle')
    if name == 'Manhattan':
        dx, dy, anchor = (0, 26, 'middle')
    if name == 'Lawrence':
        dx, dy, anchor = (-2, 26, 'end')
    if name == 'Garden City':
        dx, dy, anchor = (0, -14, 'middle')
    out.append(f'<text x="{x + dx}" y="{y + dy}" font-family="Poppins, Arial, sans-serif" font-size="19" font-weight="500" fill="#14212B" text-anchor="{anchor}">{name}</text>')
out.append('</svg>')
open('assets/kansas-cities-map.svg', 'w').write('\n'.join(out))
print(W, H)
