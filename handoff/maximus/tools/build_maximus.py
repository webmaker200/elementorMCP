"""Builds the Maximus AI Product page (410364) from the Figma frame 599:1630 with V4 atomic elements.

All styling is page-local (no global classes/variables are created or changed). Values are the
Figma REST numbers at 1920; responsive rules follow the kit breakpoints
(laptop <=1440, tablet_extra <=1200, tablet <=1024, mobile_extra <=880, mobile <=767).

usage: python3 build_maximus.py [--dry] [frame.json]   (frame.json optional: glows are cached in figma/glows.json)
"""
import json, math, os, sys
import numpy as np
import mcp

PID = 410364
HERE = os.path.dirname(os.path.abspath(__file__))
REG = json.load(open(os.path.join(HERE, 'figma', 'assets', 'registry.json')))
FRAME = next((a for a in sys.argv[1:] if a.endswith('.json')), None)


def A(k):
    return REG[k]['id']


def U(k):
    return REG[k]['url']


BPS = ['laptop', 'tablet_extra', 'tablet', 'mobile_extra', 'mobile']
FONT = 'font-family: var(--Poppins);'
G = 'max(40px, calc((100% - 1475px) / 2))'  # content gutter -> 1475px content column at 1920


def S(base='', **bp):
    return {'': base, **bp}


def merge(*parts):
    out = {}
    for p in parts:
        if isinstance(p, str):
            p = {'': p}
        for k, v in p.items():
            if v:
                out[k] = (out.get(k, '') + ' ' + v).strip()
    return out


def render(d):
    s = d.get('', '')
    for k in ('&:hover', '&:focus', '&::before'):
        if d.get(k):
            s += f'\n{k} {{ {d[k]} }}'
    for bp in BPS:
        if d.get(bp):
            s += f'\n@media(--{bp}) {{ {d[bp]} }}'
    return s.strip()


def rgba(hexc, a):
    h = hexc.lstrip('#')
    return f'rgba({int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}, {round(a, 4)})'


# ---------- background glows (Figma blurred ellipses -> radial gradients) ----------
_prof = {}


def disc_blur(rho, sigma, rs):
    """Intensity of a unit disc of radius rho blurred by a gaussian sigma, at radii rs."""
    key = (round(rho), round(sigma))
    s = np.linspace(0, rho, 240)[:, None]
    th = np.linspace(0, 2 * np.pi, 240, endpoint=False)[None, :]
    out = []
    for r in rs:
        d2 = r * r + s * s - 2 * r * s * np.cos(th)
        g = np.exp(-d2 / (2 * sigma * sigma)) / (2 * np.pi * sigma * sigma)
        out.append(float((g * s).sum() * (rho / 239) * (2 * np.pi / 240)))
    return out


def glow(cx, cy, d, color, alpha, blur, width, yoff=0):
    rho, sig = d / 2, blur / 2
    R = rho + 3 * sig
    rs = [0, max(0, rho - 2 * sig), max(0, rho - sig), rho, rho + sig * .5, rho + sig, rho + sig * 1.6, rho + sig * 2.2, R]
    rs = sorted(set(round(r) for r in rs))
    iv = disc_blur(rho, sig, rs)
    stops = ', '.join(f'{rgba(color, alpha * i) if r < R else rgba(color, 0)} {r}px' for r, i in zip(rs, iv))
    return f'radial-gradient(circle {round(R)}px at {cx / width * 100:.2f}% {round(cy + yoff)}px, {stops})'


GLOW_FILE = os.path.join(HERE, 'figma', 'glows.json')  # ellipse params extracted from the REST node JSON


def glow_params():
    """Blurred ELLIPSE children per section: [cx, cy, d, hex, alpha, blur] relative to the section box.
    Read from frame.json when given (and cached to figma/glows.json), else from the cache."""
    if not FRAME:
        return json.load(open(GLOW_FILE))
    fr = json.load(open(FRAME))
    idx = {}

    def walk(n):
        idx[n['id']] = n
        for c in n.get('children', []):
            walk(c)
    walk(fr['nodes']['599:1630']['document'])
    out = {}
    for sid in ('599:1631', '599:2749', '599:3011', '599:2857', '599:3164', '599:3391', '599:3443', '599:3468', '599:3732', '599:3776'):
        sec = idx[sid]; sb = sec['absoluteBoundingBox']; out[sid] = []
        for c in sec['children']:
            blur = [e for e in c.get('effects', []) if e['type'] == 'LAYER_BLUR' and e.get('visible', True)]
            if c['type'] != 'ELLIPSE' or not blur:
                continue
            b = c['absoluteBoundingBox']; f = c['fills'][0]['color']
            out[sid].append([round(b['x'] - sb['x'] + b['width'] / 2, 1), round(b['y'] - sb['y'] + b['height'] / 2, 1),
                             round(min(b['width'], b['height']), 1),  # rotated ellipses report an inflated bbox
                             '#%02X%02X%02X' % (round(f['r'] * 255), round(f['g'] * 255), round(f['b'] * 255)),
                             round(c.get('opacity', 1) * f.get('a', 1), 4), blur[0]['radius']])
    json.dump(out, open(GLOW_FILE, 'w'), indent=1)
    return out


_GP = None


def glows_from_figma(section_id, width=1920, yoff=0):
    global _GP
    _GP = _GP or glow_params()
    layers = [glow(cx, cy, d, hexc, a, blur, width, yoff) for cx, cy, d, hexc, a, blur in _GP[section_id]]
    return ', '.join(reversed(layers))  # Figma paints later children on top; CSS lists the top layer first


GLOWS = {}


def glows(sid, width=1920, yoff=0):
    if (sid, yoff) not in GLOWS:
        GLOWS[(sid, yoff)] = glows_from_figma(sid, width, yoff)
    return GLOWS[(sid, yoff)]


BLEED = 600  # Figma glows are unclipped and bleed into neighbouring sections


# ---------- builder ----------
class B:
    def __init__(self):
        self.cfg, self.style = {}, {}

    def el(self, tag, cid, kids='', cfg=None, css=None):
        assert cid not in self.style and cid not in self.cfg, cid
        if cfg:
            self.cfg[cid] = cfg
        if css:
            self.style[cid] = render(merge(css)) if not isinstance(css, str) else css
        return f'<{tag} configuration-id="{cid}">{kids}</{tag}>'


# ---------- shared styles ----------
def txt(size, lh, color='#000000', weight=400, ls=None):
    return (f'{FONT} font-size: {size}px; line-height: {lh}px; font-weight: {weight}; color: {color};'
            + (f' letter-spacing: {ls}px;' if ls is not None else ''))


H2 = S(txt(58, 82, ls=-1.16) + ' margin: 0;',
       laptop='font-size: 50px; line-height: 68px; letter-spacing: -1px;',
       tablet_extra='font-size: 44px; line-height: 58px;',
       tablet='font-size: 40px; line-height: 52px;',
       mobile='font-size: 32px; line-height: 42px; letter-spacing: -0.64px;')
H3_32 = S(txt(32, 46), laptop='font-size: 28px; line-height: 40px;', mobile='font-size: 24px; line-height: 34px;')
BODY = S(txt(16, 32, '#4F4F4F'), mobile='font-size: 15px; line-height: 28px;')
GLASS = 'backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);'
CARD = f'background-color: rgba(255, 255, 255, 0.1); border-radius: 20px; box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1); {GLASS}'
TILE_SHADOW = 'box-shadow: 0 14.91px 37.27px 0 rgba(170, 177, 202, 0.25);'


def section(b, cid, kids, pad_top, pad_bottom, sid, extra=None, tag='section', cssid=None, width=1920):
    bg = glows(sid, width, BLEED)
    css = merge(
        S(f'position: relative; overflow-x: clip; overflow-y: visible; width: 100%; box-sizing: border-box; display: flex; '
          f'flex-direction: column; gap: 0px; padding: {pad_top}px {G} {pad_bottom}px;',
          **({'&::before': f'content: ""; position: absolute; top: -{BLEED}px; bottom: -{BLEED}px; left: 0; right: 0; '
                           f'z-index: -1; pointer-events: none; background: {bg}; '
                           f'-webkit-mask-image: linear-gradient(transparent 0, #000 {BLEED // 2}px, #000 calc(100% - {BLEED // 2}px), transparent 100%); '
                           f'mask-image: linear-gradient(transparent 0, #000 {BLEED // 2}px, #000 calc(100% - {BLEED // 2}px), transparent 100%);'} if bg else {}),
          laptop=f'padding-top: {round(pad_top * .85)}px; padding-bottom: {round(pad_bottom * .8)}px;',
          tablet=f'padding: {min(72, round(pad_top * .8))}px 32px {min(80, round(pad_bottom * .7))}px;',
          mobile=f'padding: {min(56, round(pad_top * .7))}px 16px {min(64, round(pad_bottom * .6))}px;'),
        extra or {})
    cfg = {'tag': tag}
    if cssid:
        cfg['_cssid'] = cssid
    return b.el('e-flexbox', cid, kids, cfg, css)


def pill(b, cid, text, width=248, align='flex-start', extra=''):
    return b.el('e-paragraph', cid, cfg={'paragraph': text, 'tag': 'p'}, css=S(
        f'{txt(12, 14.4, "#7D7D7D")} display: flex; align-items: center; justify-content: center; box-sizing: border-box; '
        f'width: {width}px; max-width: 100%; height: 46px; padding: 0 16px; border: 1px solid #9ACAA1; border-radius: 34px; '
        f'background-color: rgba(255, 255, 255, 0.1); box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1); {GLASS} '
        f'align-self: {align}; text-align: center; {extra}'))


def h2(b, cid, text, extra='', center=False):
    return b.el('e-heading', cid, cfg={'tag': 'h2', 'title': text},
                css=merge(H2, ('text-align: center; ' if center else '') + extra))


def para(b, cid, text, css):
    return b.el('e-paragraph', cid, cfg={'paragraph': text, 'tag': 'p'}, css=css)


def img(b, cid, key, alt='', css=''):
    return b.el('e-image', cid, cfg={'image': {'src': {'id': A(key), 'alt': alt}, 'size': 'full'}}, css=css)


def button(b, cid, text, href, width, variant='light', extra=None):
    """Button.base from Figma: pill, label left, white 39px arrow circle inset 9px right."""
    color = '#000000' if variant == 'light' else '#FFFFFF'
    base = 'rgba(154, 202, 161, 0.2)' if variant != 'solid' else '#9ACAA1'
    hover = 'rgba(154, 202, 161, 0.38)' if variant != 'solid' else '#8BC196'
    align = 'left' if variant != 'solid' else 'center'
    pad = '17px 0 17px 26px' if variant != 'solid' else '17px 60px'
    css = merge(S(
        f'{FONT} font-size: 14px; line-height: 20px; font-weight: 500; color: {color}; text-align: {align}; '
        f'display: inline-block; box-sizing: border-box; width: {width}px; max-width: 100%; padding: {pad}; '
        f'border: 1px solid #B8DBD4; border-radius: 61px; white-space: nowrap; flex-shrink: 0; '
        f'background: url({U("arrow-green")}) no-repeat right 16.5px center / 24px 24px, '
        f'radial-gradient(circle at calc(100% - 28.5px) 50%, #FFFFFF 19px, rgba(255, 255, 255, 0) 19.6px), {base}; '
        f'{GLASS} transition: background-color 0.3s, box-shadow 0.3s;'),
        {'&:hover': f'background-color: {hover}; box-shadow: 0 10px 24px rgba(49, 131, 113, 0.15); color: {color};'},
        extra or {})
    return b.el('e-button', cid, cfg={'text': text, 'link': {'destination': href, 'tag': 'a'}}, css=css)


def tile(b, cid, key, size, icon, border='#EAEEF8', radius=18.64):
    pad = (size - 2 * 1.86 - icon) / 2
    return img(b, cid, key, '', S(
        f'display: block; box-sizing: border-box; width: {size}px; height: {size}px; padding: {pad:.2f}px; flex-shrink: 0; '
        f'background-color: #FFFFFF; border: 1.86px solid {border}; border-radius: {radius}px; object-fit: contain; {TILE_SHADOW}'))


def check_row(b, cid, text, icon='check-24', size=18, lh=32, pad=41, top=4, isz=24, color='#000000'):
    return para(b, cid, text, S(
        f'{txt(size, lh, color)} display: block; padding-left: {pad}px; '
        f'background: url({U(icon)}) no-repeat 0 {top}px / {isz}px {isz}px;',
        mobile='font-size: 16px; line-height: 28px; background-position: 0 2px;'))


def check_item(b, cid, title, sub):
    """D / J checklist: 28px check, title 22/32, sub 16/32, text column at +57px."""
    kids = b.el('e-heading', cid + '-t', cfg={'tag': 'h3', 'title': title}, css=S(txt(22, 32), mobile='font-size: 19px; line-height: 28px;'))
    kids += para(b, cid + '-p', sub, merge(BODY, 'margin-top: 5px;'))
    return b.el('e-flexbox', cid, kids, css=S(
        f'display: flex; flex-direction: column; gap: 0px; padding: 0 0 0 57px; '
        f'background: url({U("check-28")}) no-repeat 0 3px / 28px 28px;',
        mobile='padding-left: 44px;'))


# ================= SECTIONS =================

def s_hero(b):
    avatars = ''.join(img(b, f'hero-avatar-{i}', f'avatar-{i}', 'Physician', S(
        'display: block; box-sizing: border-box; width: 34.6px; height: 34.6px; border: 1.5px solid #FFFFFF; '
        'border-radius: 50%; object-fit: cover; flex-shrink: 0;' + (' margin-left: -10.6px;' if i > 1 else '')))
        for i in (1, 2, 3))
    avatars += para(b, 'hero-tag-label', 'AI-Powered healthcare', txt(12, 14.4, '#7D7D7D') + ' margin-left: 11.4px; white-space: nowrap;')
    tag = b.el('e-flexbox', 'hero-tag', avatars, css=S(
        'display: flex; flex-direction: row; align-items: center; gap: 0px; box-sizing: border-box; width: 258px; height: 46px; '
        'padding: 0 0 0 9px; border: 1px solid #7EB63E; border-radius: 31px; margin-bottom: 25px;'))
    h1 = b.el('e-heading', 'hero-title', cfg={'tag': 'h1', 'title': 'Your Revenue Cycle,<br>Working Smarter.'}, css=S(
        txt(72, 88, ls=-1.44) + ' margin: 0 0 21px;',
        laptop='font-size: 62px; line-height: 76px; letter-spacing: -1.24px;',
        tablet_extra='font-size: 56px; line-height: 68px;',
        tablet='font-size: 48px; line-height: 60px; letter-spacing: -0.96px;',
        mobile='font-size: 36px; line-height: 46px; letter-spacing: -0.72px;'))
    p = para(b, 'hero-text', 'Maximus connects billing, claims, coding, payments, and reporting in one intelligent platform — '
             'helping your practice reduce administrative friction and stay ahead of revenue leakage.',
             merge(BODY, 'max-width: 595px; margin-bottom: 43px;'))
    btns = button(b, 'hero-btn-explore', 'Explore AI Ecosystem', '#maximus-integrations', 240)
    btns += b.el('e-button', 'hero-btn-demo', cfg={'text': 'Request a Demo', 'link': {'destination': '#book-demo', 'tag': 'a'}}, css=S(
        f'{txt(14, 20, weight=500)} display: inline-block; padding: 17px 38px 17px 0; background: url({U("arrow-black")}) '
        f'no-repeat right center / 24px 24px; background-color: transparent; border: 0; border-radius: 0; white-space: nowrap; '
        f'transition: background-position 0.3s;',
        **{'&:hover': 'background-position: right -4px center; color: #318371;'}))
    row = b.el('e-flexbox', 'hero-actions', btns, css=S(
        'display: flex; flex-direction: row; align-items: center; flex-wrap: wrap; gap: 34px; padding: 0; margin-bottom: 48px;',
        mobile='gap: 20px;'))
    logos = ''.join(img(b, f'hero-logo-{k}', f'logo-{k}', alt, f'display: block; width: {w}px; height: 81.3px; flex-shrink: 0;')
                    for k, alt, w in (('hitrust', 'HITRUST CSF Certified', 73.2), ('hipaa', 'HIPAA compliant', 63),
                                      ('aicpa-soc', 'AICPA SOC', 63), ('pci', 'PCI Security Standards Council', 97.6)))
    logos = b.el('e-flexbox', 'hero-compliance', logos, css=S(
        'display: flex; flex-direction: row; align-items: flex-start; flex-wrap: wrap; gap: 34px; box-sizing: border-box; '
        'width: 438px; max-width: 100%; padding: 0 0 0 12px; margin-left: -6px; '
        'background: linear-gradient(90deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0) 100%);',
        mobile='gap: 20px; width: auto;'))
    left = b.el('e-flexbox', 'hero-content', tag + h1 + p + row + logos, css=S(
        'display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0; flex: 0 1 780px; min-width: 0; '
        'position: relative; z-index: 2;',
        tablet_extra='flex: 0 0 auto; width: 100%;'))

    def float_card(cid, key, icon_w, text, top, w, h, pl, gap):
        kids = img(b, cid + '-icon', key, '', f'display: block; width: {icon_w}px; height: auto; flex-shrink: 0;')
        kids += para(b, cid + '-text', text, txt(11.53, 17.3))
        return b.el('e-flexbox', cid, kids, css=S(
            f'position: absolute; left: -157px; top: {top}%; z-index: 3; display: flex; flex-direction: row; align-items: center; '
            f'gap: {gap}px; box-sizing: border-box; width: {w}px; height: {h}px; padding: 0 0 0 {pl}px; '
            f'background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 20px; '
            f'box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);',
            tablet='left: -72px;', mobile_extra='left: -24px;', mobile='display: none;'))
    right = img(b, 'hero-dashboard', 'hero-dashboard', 'Maximus revenue cycle dashboard', S(
        'display: block; width: 100%; height: auto; border-radius: 15px; box-shadow: 0 0 55.56px 0 rgba(134, 157, 180, 0.1);'))
    right += float_card('hero-card-era', 'ic-hero-settings', 31, 'Automated ERA<br>Posting', 51.64, 194.6, 62.7, 17, 19)
    right += float_card('hero-card-scrub', 'ic-hero-cpu', 33, 'Claim Scrubbing by<br>Rule Engine', 66.34, 242.9, 84.3, 18, 15)
    right += float_card('hero-card-denial', 'ic-hero-file-plus', 32, 'Denial<br>Management', 85.3, 194.6, 62.7, 19, 16)
    right = b.el('e-div-block', 'hero-visual', right, css=S(
        'position: relative; flex: 0 0 748px; min-width: 0; padding: 0; margin-top: 70px;',
        laptop='flex: 0 1 640px;',
        tablet_extra='flex: 0 0 auto; width: 100%; max-width: 748px; margin: 64px 0 0 auto;',
        tablet='margin-top: 48px;'))
    return section(b, 'hero', left + right, 119, 156, '599:1631', extra=S(
        'flex-direction: row; justify-content: space-between; align-items: flex-start;',
        laptop='gap: 40px;', tablet_extra='flex-direction: column; align-items: stretch; gap: 0px;'))


def s_problems(b):
    head = pill(b, 'problems-tag', 'The Problems with Traditional PMS', align='center', extra='margin-bottom: 23px;')
    head += h2(b, 'problems-title', 'Everything You Need to<br>Take Control of Your Revenue Cycle', 'max-width: 1089px; margin-bottom: 11px;', True)
    head += para(b, 'problems-text', 'Maximus brings billing, claims, coding, payments, analytics, and automation together in one '
                 'connected platform — giving your team greater visibility and control.',
                 merge(BODY, 'max-width: 870px; text-align: center; margin-bottom: 59px;'))
    cards = ''
    for key, (title, body, ic, isz, pv, pvw, tw) in {
        'eligibility': ('Eligibility', 'Still checking insurance eligibility and benefits patient by patient?', 'ic-search', 36, 'pv-eligibility', 193.8, 240),
        'claims': ('Claims', 'Still relying on teams to identify claim issues, check statuses, and determine the next action?', 'ic-claims-file', 43, 'pv-claims', 193.8, 285),
        'payments': ('Payments', 'Still spending valuable staff time manually posting and reconciling payments?', 'ic-payments', 48, 'pv-payments', 164, 269),
        'kpis': ('KPIs &amp; Reporting', 'Still waiting for reports to understand how the practice is performing?', 'ic-pie', 40, 'pv-kpis', 170, 285),
    }.items():
        c = f'problem-{key}'
        top = tile(b, c + '-icon', ic, 82, isz)
        top += img(b, c + '-preview', pv, '', f'display: block; width: {pvw}px; height: 82px; flex-shrink: 1; min-width: 0; '
                                              f'border-radius: 18.64px; {TILE_SHADOW}')
        kids = b.el('e-flexbox', c + '-visual', top, css='display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 16px; padding: 0; margin-bottom: 41px; max-width: 100%;')
        kids += b.el('e-heading', c + '-title', cfg={'tag': 'h3', 'title': title}, css=merge(H3_32, 'text-align: center; margin-bottom: 6px;'))
        kids += para(b, c + '-text', body, merge(BODY, f'text-align: center; max-width: {tw}px;'))
        cards += b.el('e-flexbox', c, kids, css=S(
            f'display: flex; flex-direction: column; align-items: center; gap: 0px; box-sizing: border-box; min-width: 0; '
            f'padding: 29px 16px 32px; {CARD}'))
    grid = b.el('e-div-block', 'problems-grid', cards, css=S(
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 34px; width: 100%; padding: 0; margin-bottom: 43px;',
        laptop='gap: 24px;', tablet_extra='grid-template-columns: repeat(2, minmax(0, 1fr));',
        mobile='grid-template-columns: minmax(0, 1fr); gap: 20px;'))
    return section(b, 'problems', head + grid + cta_bar(b, 'problems-cta', 'Maximus changes that.',
                   'AI, automation, analytics, workflows, and interoperability in one connected PMS.',
                   '#maximus-automation', 124, 127), 73, 98, '599:2749', extra='align-items: center;', cssid='maximus-platform')


def cta_bar(b, cid, title, text, href, pl, pr):
    t = b.el('e-heading', cid + '-title', cfg={'tag': 'h3', 'title': title}, css=merge(H3_32, 'line-height: 39px;'))
    t += para(b, cid + '-text', text, merge(BODY, 'margin-top: 13px;'))
    t = b.el('e-flexbox', cid + '-copy', t, css='display: flex; flex-direction: column; gap: 0px; padding: 0; min-width: 0;')
    t += button(b, cid + '-btn', 'See What Maximus Automates', href, 310)
    return b.el('e-flexbox', cid, t, css=S(
        f'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 32px; box-sizing: border-box; '
        f'width: 100%; min-height: 152px; padding: 0 {pr}px 0 {pl}px; {CARD}',
        laptop='padding: 0 48px;', tablet='flex-direction: column; align-items: flex-start; padding: 32px; gap: 24px;',
        mobile='padding: 28px 20px;'))


def s_comparison(b):
    PADIN = 'max(24px, calc((100% - 1475px) / 2))'
    head = pill(b, 'compare-tag', 'Not Your Regular PMS', extra='margin-bottom: 23px;')
    head += h2(b, 'compare-title', 'From Practice Management to<br>Practice Intelligence.', 'max-width: 1089px; margin-bottom: 14px;')
    head += para(b, 'compare-text', 'Traditional PMS software helps your team manage tasks. Maximus helps perform them.', merge(BODY, 'color: #000000;'))
    head = b.el('e-flexbox', 'compare-head', head, css='display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0; min-width: 0; flex: 1 1 auto;')
    rows = [('Stores patient and claim data'), 'Manual eligibility workflows', 'Staff checks claim errors', 'Manual claim-status follow-up',
            'Manual payment posting', 'Static reports', 'Disconnected KPIs', 'Manual workflow routing', 'Staff prepares appeals',
            'Limited external connectivity']
    trad = b.el('e-heading', 'compare-legacy-title', cfg={'tag': 'h3', 'title': 'Traditional PMS / Billing Software'},
                css=S(txt(24, 32) + ' margin-bottom: 6px;', mobile='font-size: 21px; line-height: 30px;'))
    trad += ''.join(check_row(b, f'compare-legacy-{i + 1}', t, 'x-16', 16, 32, 30, 8, 16, '#4F4F4F') for i, t in enumerate(rows))
    trad = b.el('e-flexbox', 'compare-legacy', trad, css=S(
        'display: flex; flex-direction: column; gap: 12px; box-sizing: border-box; flex: 0 0 495px; padding: 38px 53px 33px; '
        'margin: 159px 0 -369px; position: relative; z-index: 2; background-color: #F0FFFC; border: 1px solid #318371; '
        'border-radius: 20px; box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1);',
        laptop='flex: 0 0 440px; padding: 34px 40px 30px;',
        tablet_extra='flex: 0 0 auto; width: 100%; max-width: 495px; margin: 40px 0 32px;',
        mobile='padding: 28px 22px;'))
    top = b.el('e-flexbox', 'compare-top', head + trad, css=S(
        f'display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 32px; '
        f'padding: 0 {PADIN}; position: relative; z-index: 2;',
        tablet_extra='flex-direction: column; gap: 0px;', mobile='padding: 0 4px;'))
    col1 = ['Acts on patient and claim data', 'Automated eligibility + benefits verification', 'Automated claim scrubbing',
            'Automated status + Agentic AI follow-ups', 'AI-driven payment posting']
    col2 = ['HL7 + FHIR + APIs + RPA', 'One-click AI-assisted appeals', 'Intelligent rule engine + smart workflows',
            'Integrated KPI monitoring', 'Smart BI + financial analytics']
    items = ''.join(check_row(b, f'compare-maximus-{i + 1}', t) for i, t in enumerate(col1 + col2))
    grid = b.el('e-div-block', 'compare-maximus-list', items, css=S(
        'display: grid; grid-template-columns: 490px 490px; grid-template-rows: repeat(5, auto); grid-auto-flow: column; '
        'gap: 14px 0px; padding: 0; max-width: 100%;',
        laptop='grid-template-columns: repeat(2, minmax(0, 1fr)); max-width: calc(100% - 500px); column-gap: 24px;',
        tablet_extra='max-width: 100%;',
        tablet='grid-template-columns: minmax(0, 1fr); grid-template-rows: none; grid-auto-flow: row;'))
    panel = img(b, 'compare-maximus-logo', 'logo-maximus', 'Maximus', 'display: block; width: 245px; height: auto; margin-bottom: 40px;')
    panel = b.el('e-flexbox', 'compare-maximus', panel + grid, css=S(
        f'display: flex; flex-direction: column; align-items: flex-start; gap: 0px; box-sizing: border-box; width: 100%; '
        f'min-height: 464px; padding: 82px {PADIN}; border-radius: 20px; overflow: hidden; '
        f'background: url({U("lineart")}) no-repeat right 180px top -102px / 770px 791px, rgba(255, 255, 255, 0.8); {GLASS}',
        tablet_extra='min-height: 0; padding: 56px 40px; background-position: right -200px top -102px;',
        mobile='padding: 40px 20px; border-radius: 16px;'))
    return section(b, 'comparison', top + panel, 49, 138, '599:3011', extra=S(
        'padding-left: 57px; padding-right: 57px;', laptop='padding-left: 24px; padding-right: 24px;',
        mobile='padding-left: 16px; padding-right: 16px;'))


def s_eligibility(b):
    left = pill(b, 'eligibility-tag', 'Start the Revenue Cycle Right', extra='margin-bottom: 23px;')
    left += h2(b, 'eligibility-title', 'Verify Coverage Before It Becomes a Revenue Problem.', 'max-width: 659px; margin-bottom: 14px;')
    left += para(b, 'eligibility-text', 'Maximus automates patient eligibility and benefits verification, helping teams validate '
                 'coverage earlier and reduce repetitive front-office work.',
                 merge(BODY, 'box-sizing: border-box; width: 633px; max-width: 100%; padding-bottom: 37px; '
                             'border-bottom: 1px solid rgba(79, 79, 79, 0.2); margin-bottom: 32px;'))
    left += check_item(b, 'eligibility-auto', 'Automated Eligibility Verification', 'Reduce manual payer lookups.')
    left += check_item(b, 'eligibility-benefits', 'Benefits Verification', 'Bring benefit visibility into the patient workflow.')
    left += check_item(b, 'eligibility-batch', 'Batch Eligibility', 'Verify multiple scheduled patients in one workflow.')
    for c in ('eligibility-benefits', 'eligibility-batch'):
        b.style[c] = b.style[c].replace('padding: 0 0 0 57px;', 'padding: 0 0 0 57px; margin-top: 26px;')
    left = b.el('e-flexbox', 'eligibility-content', left, css=S(
        'display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0; flex: 0 1 659px; min-width: 0;',
        tablet_extra='flex: 0 0 auto; width: 100%;'))
    side = img(b, 'eligibility-donut', 'eligibility-donut', 'Coverage verified widget', 'display: block; width: 100%; height: auto;')
    side += img(b, 'eligibility-activity', 'eligibility-activity', 'Eligibility checks today chart', 'display: block; width: 100%; height: auto;')
    side = b.el('e-flexbox', 'eligibility-widgets', side, css=S(
        'display: flex; flex-direction: column; gap: 10px; padding: 0; flex: 0 1 262px; min-width: 0;',
        mobile='flex: 0 0 auto; width: 100%; max-width: 448px;'))
    right = img(b, 'eligibility-workflow', 'eligibility-workflow', 'Maximus eligibility verification workflow', S(
        'display: block; flex: 0 1 448px; min-width: 0; width: 448px; height: auto;', mobile='width: 100%; max-width: 448px; flex: 0 0 auto;'))
    right = b.el('e-flexbox', 'eligibility-visual', right + side, css=S(
        'display: flex; flex-direction: row; align-items: flex-start; gap: 12px; padding: 0; flex: 0 1 722px; min-width: 0; margin-top: 161px;',
        laptop='margin-top: 120px;',
        tablet_extra='flex: 0 0 auto; width: 100%; max-width: 722px; margin: 56px auto 0;',
        mobile='flex-direction: column; align-items: center;'))
    return section(b, 'eligibility', left + right, 73, 94, '599:2857', extra=S(
        'flex-direction: row; justify-content: space-between; align-items: flex-start;',
        laptop='gap: 40px;', tablet_extra='flex-direction: column; gap: 0px;'))


def s_claims(b):
    head = pill(b, 'claims-tag', 'Smarter Claims Start Before Submission', 290, 'center', 'margin-bottom: 23px;')
    head += h2(b, 'claims-title', 'Catch More Issues Before the Payer Does.', 'max-width: 833px; margin-bottom: 11px;', True)
    head += para(b, 'claims-text', 'Maximus uses intelligent rules and automated claim validation to identify issues and trigger '
                 'the appropriate workflow before they become downstream problems.',
                 merge(BODY, 'max-width: 834px; text-align: center; margin-bottom: 59px;'))
    cols = ''
    for key, (title, body, alt) in {
        'rule-engine': ('Intelligent Rule Engine', 'Define conditions, routing logic, and actions across claims, payments, eligibility, and workflows.', 'Intelligent rule engine screen'),
        'scrubbing': ('Auto Claim Scrubbing', 'Identify missing information, inconsistencies, and potential claim issues before submission.', 'Auto claim scrubbing screen'),
        'status': ('Auto Claim Status', 'Reduce repetitive payer checking and surface stalled claims sooner.', 'Auto claim status screen'),
        'workflows': ('Smart Workflows', 'Automatically trigger tasks, route exceptions, and move work to the next action.', 'Smart workflows screen'),
    }.items():
        c = f'claims-{key}'
        kids = img(b, c + '-image', f'claims-{key}', alt, 'display: block; width: 100%; height: auto; border-radius: 20px; '
                                                          'box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1);')
        kids += b.el('e-heading', c + '-title', cfg={'tag': 'h3', 'title': title}, css=merge(
            H3_32, 'line-height: 42px; margin-top: 31px; padding-left: 9px; max-width: 305px;'))
        kids += para(b, c + '-text', body, merge(BODY, 'margin-top: 22px; padding-left: 9px; max-width: 301px;'))
        cols += b.el('e-flexbox', c, kids, css='display: flex; flex-direction: column; align-items: stretch; gap: 0px; padding: 0; min-width: 0;')
    grid = b.el('e-div-block', 'claims-grid', cols, css=S(
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 34px; width: 100%; padding: 0;',
        laptop='gap: 24px;', tablet_extra='grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 48px;',
        mobile='grid-template-columns: minmax(0, 1fr); row-gap: 40px;'))
    return section(b, 'claims', head + grid, 73, 88, '599:3164', extra='align-items: center;', cssid='maximus-automation')


def s_reporting(b):
    head = pill(b, 'reporting-tag', 'The Problems with Traditional PMS', extra='margin-bottom: 23px;')
    head += h2(b, 'reporting-title', 'Know How Your Practice Is Performing — Without Waiting for the Report.', 'max-width: 848px;')
    head = b.el('e-flexbox', 'reporting-head', head, css=S('display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0; flex: 0 1 848px; min-width: 0;',
                                                          tablet_extra='flex: 0 0 auto;'))
    head += para(b, 'reporting-text', 'Maximus turns operational and financial information into real-time visibility for practice leadership.',
                 merge(BODY, S('max-width: 397px; margin: 130px 31px 0 0;', laptop='margin-right: 0;', tablet_extra='max-width: 633px; margin: 16px 0 0;')))
    head = b.el('e-flexbox', 'reporting-header', head, css=S(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 32px; padding: 0; margin-bottom: 47px;',
        tablet_extra='flex-direction: column; gap: 0px;'))

    W = 'color: #FFFFFF;'

    def stat(cid, text, size, lh, ls):
        return para(b, cid, text, S(f'{txt(size, lh, "#FFFFFF", ls=ls)} white-space: nowrap;',
                                    mobile=f'font-size: {round(size * .72)}px; line-height: {round(lh * .72)}px;'))
    tl = stat('reporting-collections-label', 'Collections', 28, 43, -0.56) + stat('reporting-collections-value', '$842K', 72, 79, -1.44)
    tl = b.el('e-flexbox', 'reporting-collections', tl, css='width: auto; display: flex; flex-direction: column; gap: 4px; padding: 0;')
    tr = stat('reporting-payments-label', 'Payments', 18, 29, -0.36) + stat('reporting-payments-value', '+18%', 42, 63, -0.84)
    tr = b.el('e-flexbox', 'reporting-payments', tr, css='width: auto; display: flex; flex-direction: row; align-items: baseline; gap: 12px; padding: 0;')
    top = b.el('e-flexbox', 'reporting-card-top', tl + tr, css='display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 16px; padding: 0; flex-wrap: wrap;')
    bl = stat('reporting-ar-label', 'A/R', 18, 36, -0.36) + stat('reporting-ar-value', '$1.12M', 42, 79, -0.84)
    bl = b.el('e-flexbox', 'reporting-ar', bl, css='width: auto; display: flex; flex-direction: row; align-items: baseline; gap: 14px; padding: 0 0 0 7px;')
    br = stat('reporting-denial-label', 'Denial Rate', 18, 36, -0.36) + stat('reporting-denial-value', '4.8%', 42, 79, -0.84)
    br = b.el('e-flexbox', 'reporting-denial', br, css='width: auto; display: flex; flex-direction: row; align-items: baseline; gap: 14px; padding: 0;')
    bot = b.el('e-flexbox', 'reporting-card-bottom', bl + br, css='display: flex; flex-direction: row; justify-content: space-between; align-items: baseline; gap: 16px; padding: 0; flex-wrap: wrap;')
    green = b.el('e-flexbox', 'reporting-collections-card', top + bot, css=S(
        f'display: flex; flex-direction: column; justify-content: space-between; gap: 24px; box-sizing: border-box; flex: 0 0 737px; '
        f'min-width: 0; min-height: 541px; padding: 38px 24px 27px 46px; border-radius: 20px; overflow: hidden; '
        f'box-shadow: 0 51px 63.6px 0 rgba(89, 89, 89, 0.2); '
        f'background: url({U("chart-line")}) no-repeat 0 calc(100% + 9px) / 100% auto, '
        f'radial-gradient(ellipse 1155px 1571px at 28% 27%, #3DA28C 0%, #006750 100%); {W}',
        laptop='flex: 737 1 0px;', tablet_extra='flex: 0 0 auto; width: 100%; min-height: 0; aspect-ratio: 737 / 541;',
        mobile='aspect-ratio: auto; min-height: 380px; padding: 28px 20px 20px 24px;'))

    def feature(cid, title, text, text_lh, pad):
        kids = tile(b, cid + '-icon', 'ic-pie', 82, 40, '#F8F4EA')
        t = b.el('e-heading', cid + '-title', cfg={'tag': 'h3', 'title': title}, css=H3_32)
        t += para(b, cid + '-text', text, merge(BODY, f'line-height: {text_lh}px; margin-top: 6px; max-width: 528px;'))
        kids += b.el('e-flexbox', cid + '-copy', t, css='display: flex; flex-direction: column; gap: 0px; padding: 0; min-width: 0;')
        return b.el('e-flexbox', cid, kids, css=S(
            f'display: flex; flex-direction: row; align-items: flex-start; gap: 27px; box-sizing: border-box; min-height: 136px; '
            f'padding: {pad}; {CARD}', mobile='flex-direction: column; gap: 16px; padding: 24px 20px;'))
    rc = feature('reporting-bi', 'Smart BI Reporting', 'Modern dashboards for operational and financial performance.', 32, '27px 34px 27px 44px')
    rc += feature('reporting-kpi', 'Integrated KPI Tracking', 'Monitor the metrics that matter without jumping between disconnected systems.', 22, '27px 34px 20px 44px')
    t = para(b, 'reporting-act-text', 'Give CFOs, CEOs, practice owners, and RCM leaders a clearer view of what is happening across the business.',
             merge(BODY, 'max-width: 315px;'))
    t += button(b, 'reporting-act-btn', 'Book a Demo', '#book-demo', 190)
    t = b.el('e-flexbox', 'reporting-act-row', t, css=S(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 24px; padding: 0; margin-top: 7px;',
        mobile='flex-direction: column; align-items: flex-start;'))
    t = b.el('e-heading', 'reporting-act-title', cfg={'tag': 'h3', 'title': 'See it. Understand it. Act on it.'}, css=merge(H3_32, 'line-height: 48px;')) + t
    rc += b.el('e-flexbox', 'reporting-act', t, css=S(
        f'display: flex; flex-direction: column; gap: 0px; box-sizing: border-box; '
        f'flex: 1 1 auto; padding: 35px 38px 51px 49px; {CARD}',
        mobile='padding: 28px 20px;'))
    right = b.el('e-flexbox', 'reporting-features', rc, css=S(
        'display: flex; flex-direction: column; gap: 16px; padding: 0; flex: 1 1 707px; min-width: 0;',
        laptop='flex: 707 1 0px;', tablet_extra='flex: 0 0 auto; width: 100%;'))
    grid = b.el('e-flexbox', 'reporting-grid', green + right, css=S(
        'display: flex; flex-direction: row; align-items: stretch; gap: 31px; padding: 0; margin-bottom: 16px;',
        laptop='gap: 20px;', tablet_extra='flex-direction: column; gap: 20px;'))
    bar = cta_bar(b, 'reporting-cta', 'See it. Understand it. Act on it.',
                  'Give CFOs, CEOs, practice owners, and RCM leaders a clearer view of what is happening across the business.',
                  '#maximus-automation', 72, 48)
    return section(b, 'reporting', head + grid + bar, 73, 130, '599:3391')


def s_integrations(b):
    ov = para(b, 'integrations-photo-title', 'Connect the data. Trigger the workflow. Automate the action.',
              S(txt(24, 32, '#FFFFFF', 500), mobile='font-size: 19px; line-height: 27px;'))
    ov += para(b, 'integrations-photo-text', 'EHRs • Payers • Clearinghouses • Labs • Payment systems • Third-party healthcare platforms',
               merge(BODY, 'color: #C8EDFF; margin-top: 4px;'))
    ov = b.el('e-flexbox', 'integrations-photo-caption', ov, css=S(
        f'position: absolute; left: 19px; right: 14px; bottom: 20px; z-index: 2; display: flex; flex-direction: column; gap: 0px; '
        f'padding: 18px 47px 21px 36px; border-radius: 20px; background-color: rgba(13, 54, 82, 0.52); {GLASS}',
        mobile='left: 12px; right: 12px; bottom: 12px; padding: 16px 18px;'))
    photo = img(b, 'integrations-photo-image', 'integrations-photo', 'Healthcare team using connected systems', S(
        'position: absolute; top: 0; left: 0; display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% 83.6%; opacity: 0.9;'))
    photo = b.el('e-div-block', 'integrations-photo', photo + ov, css=S(
        'position: relative; overflow: hidden; box-sizing: border-box; flex: 0 0 618px; height: 695px; padding: 0; '
        'border: 1px solid #1171A1; border-radius: 20px; background-color: #E6F1F3;',
        laptop='flex: 0 1 560px; height: auto; aspect-ratio: 618 / 695;',
        tablet_extra='flex: 0 0 auto; width: 100%; max-width: 618px;'))
    txtc = pill(b, 'integrations-tag', 'Connected by Design', extra='margin-bottom: 23px;')
    txtc += h2(b, 'integrations-title', 'Your PMS Shouldn’t Live on an Island.', 'max-width: 659px; margin-bottom: 5px;')
    txtc += para(b, 'integrations-text', 'Maximus is designed to operate within the modern healthcare technology ecosystem and connect '
                 'to the systems your organization already relies on.', merge(BODY, 'max-width: 633px; margin-bottom: 41px;'))
    items = ''
    for k, (t, d) in {'hl7': ('HL7', 'Support established healthcare interoperability standards.'),
                      'fhir': ('FHIR', 'Enable modern healthcare data exchange and interoperability.'),
                      'apis': ('APIs', 'Connect Maximus with external applications, platforms, and services.'),
                      'rpa': ('RPA', 'Automate repetitive workflows where direct integration is limited.')}.items():
        it = b.el('e-heading', f'integrations-{k}-title', cfg={'tag': 'h3', 'title': t}, css=S(txt(24, 32, weight=500), mobile='font-size: 21px;'))
        it += para(b, f'integrations-{k}-text', d, BODY)
        items += b.el('e-flexbox', f'integrations-{k}', it, css='display: flex; flex-direction: column; gap: 0px; padding: 0;')
    txtc += b.el('e-flexbox', 'integrations-list', items, css=S(
        'display: flex; flex-direction: column; gap: 32px; padding: 0 0 0 30px; border-left: 1px solid #B8B8B8;',
        mobile='gap: 24px; padding-left: 20px;'))
    txtc = b.el('e-flexbox', 'integrations-content', txtc, css=S(
        'display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0; flex: 0 0 666px; min-width: 0;',
        laptop='flex: 1 1 0px;', tablet_extra='flex: 0 0 auto; width: 100%; margin-top: 56px;'))
    return section(b, 'integrations', photo + txtc, 39, 178, '599:3443', cssid='maximus-integrations', extra=S(
        'flex-direction: row; align-items: flex-start; gap: 246px;', laptop='gap: 80px;',
        tablet_extra='flex-direction: column; gap: 0px;'))


def s_trust(b):
    left = pill(b, 'trust-tag', 'Built for Healthcare Operations', extra='margin: 0 0 23px 5px;')
    left += h2(b, 'trust-title', 'Technology Is Only Valuable When Practices Can Trust It.', 'max-width: 659px; margin: 0 0 46px 5px;')
    stats = ''
    for k, (v, lab, d) in {'physicians': ('200+', 'Physicians', 'Trusted across physician workflows and practice operations.'),
                           'interop': ('HL7', 'Interoperability', 'HL7, FHIR, and API-supported connectivity.'),
                           'automation': ('AI', 'Automation-First', 'AI, RPA, intelligent rules, and smart workflows built into the platform.'),
                           'visibility': ('360°', 'Executive Visibility', 'Financial, operational, and revenue-cycle insights in one environment.')}.items():
        c = f'trust-stat-{k}'
        row = para(b, c + '-value', v, txt(36, 47, '#1171A1', 500) + ' white-space: nowrap;')
        row += para(b, c + '-label', lab, txt(18, 32, weight=500) + ' white-space: nowrap;')
        kids = b.el('e-flexbox', c + '-head', row, css='display: flex; flex-direction: row; align-items: baseline; gap: 8px; padding: 0;')
        kids += para(b, c + '-text', d, merge(BODY, 'margin-top: 14px; max-width: 215px;'))
        stats += b.el('e-flexbox', c, kids, css=S(
            f'display: flex; flex-direction: column; gap: 0px; box-sizing: border-box; min-height: 203px; padding: 23px 20px 20px 29px; min-width: 0; {CARD}',
            mobile='min-height: 0; padding: 22px 20px;'))
    left += b.el('e-div-block', 'trust-stats', stats, css=S(
        'display: grid; grid-template-columns: repeat(2, 296px); gap: 15px 16px; padding: 0; max-width: 100%;',
        laptop='grid-template-columns: repeat(2, minmax(0, 1fr)); width: 100%;',
        mobile='grid-template-columns: minmax(0, 1fr);'))
    left = b.el('e-flexbox', 'trust-content', left, css=S(
        'display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0; flex: 0 0 608px; min-width: 0;',
        laptop='flex: 0 1 560px;', tablet_extra='flex: 0 0 auto; width: 100%;'))
    right = img(b, 'trust-claims', 'trust-claims', 'Maximus claims dashboard', 'display: block; width: 100%; height: auto;')
    half = S('display: block; width: calc(50% - 16.5px); height: auto; min-width: 0;', mobile='width: 100%;')
    row = img(b, 'trust-payments', 'trust-payments', 'Payments widget', half)
    row += img(b, 'trust-aging', 'trust-aging', 'A/R aging widget', half)
    right += b.el('e-flexbox', 'trust-widgets', row, css=S('display: flex; flex-direction: row; gap: 33px; padding: 0;',
                                                           mobile='flex-direction: column; gap: 16px;'))
    badge = b.el('e-image', 'trust-badge-icon', cfg={'image': {'src': {'id': A('ic-shield'), 'alt': ''}, 'size': 'full'}},
                 css='display: block; box-sizing: border-box; width: 36px; height: 36px; padding: 9px; background-color: #23B26D; border-radius: 12px; flex-shrink: 0;')
    bt = para(b, 'trust-badge-label', 'Trusted by', txt(12, 16, '#5B6B85'))
    bt += para(b, 'trust-badge-value', '200+ Physicians', txt(14, 20, '#1A2B4A', 600) + ' white-space: nowrap;')
    badge += b.el('e-flexbox', 'trust-badge-copy', bt, css='width: auto; display: flex; flex-direction: column; gap: 0px; padding: 0;')
    right += b.el('e-flexbox', 'trust-badge', badge, css=S(
        f'position: absolute; top: -26px; left: 36.8%; z-index: 2; width: auto; display: flex; flex-direction: row; align-items: center; gap: 12px; '
        f'padding: 12px 20px; border-radius: 16px; background-color: rgba(228, 244, 236, 0.3); {GLASS}',
        mobile='left: 12px;'))
    right = b.el('e-flexbox', 'trust-visual', right, css=S(
        'position: relative; display: flex; flex-direction: column; gap: 26px; padding: 0; flex: 0 1 712px; min-width: 0; margin-top: 16px;',
        mobile='gap: 16px;', tablet_extra='flex: 0 0 auto; width: 100%; max-width: 712px; margin-top: 64px;'))
    box = b.el('e-flexbox', 'trust-panel', left + right, css=S(
        f'position: relative; overflow: hidden; display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; '
        f'gap: 40px; box-sizing: border-box; width: 100%; padding: 57px 82px 59px; border: 1px solid #E7E7E7; border-radius: 40px; '
        f'background: {glows("599:3468", 1636)}, #FFFFFF;',
        laptop='padding: 48px;', tablet_extra='flex-direction: column; gap: 0px;',
        mobile='padding: 32px 16px; border-radius: 24px;'))
    return b.el('e-flexbox', 'trust', box, cfg={'tag': 'section'}, css=S(
        'width: 100%; box-sizing: border-box; display: flex; flex-direction: column; gap: 0px; '
        'padding: 0 max(40px, calc((100% - 1636px) / 2)) 82px;',
        laptop='padding-left: 24px; padding-right: 24px;', mobile='padding: 0 12px 56px;'))


def s_why(b):
    head = pill(b, 'why-tag', 'Why Maximus', align='center', extra='margin-bottom: 23px;')
    head += h2(b, 'why-title', 'Your Software Shouldn’t Add More Work to Your Practice.', 'max-width: 1089px; margin-bottom: 14px;', True)
    head += para(b, 'why-text', 'It should remove it.', merge(BODY, 'color: #000000; text-align: center; margin-bottom: 42px;'))
    cards = ''
    for k, (title, d, ic, isz) in {
        'automation': ('More Automation', 'Still checking insurance eligibility and benefits patient by patient?', 'ic-settings', 34),
        'intelligence': ('More Intelligence', 'For operational decisions.', 'ic-cpu', 33),
        'visibility': ('More Visibility', 'For leadership.', 'ic-eye', 35),
        'connectivity': ('More Connectivity', 'Between systems.', 'ic-link', 34)}.items():
        c = f'why-{k}'
        row = tile(b, c + '-icon', ic, 68, isz)
        row += b.el('e-heading', c + '-title', cfg={'tag': 'h3', 'title': title}, css=merge(H3_32, 'line-height: 36px; margin-top: -2px;'))
        kids = b.el('e-flexbox', c + '-head', row, css='display: flex; flex-direction: row; align-items: flex-start; gap: 24px; padding: 0;')
        kids += para(b, c + '-text', d, merge(BODY, 'margin-top: 25px; padding-left: 2px;'))
        cards += b.el('e-flexbox', c, kids, css=S(
            f'display: flex; flex-direction: column; gap: 0px; box-sizing: border-box; min-width: 0; min-height: 247px; '
            f'padding: 46px 29px 30px; background-color: rgba(255, 255, 255, 0.4); border-radius: 20px; '
            f'box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1); {GLASS}',
            laptop='padding: 36px 24px 28px;', mobile='min-height: 0;'))
    grid = b.el('e-div-block', 'why-grid', cards, css=S(
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 15px; width: calc(100% + 5px); padding: 0;',
        tablet_extra='grid-template-columns: repeat(2, minmax(0, 1fr)); width: 100%; gap: 20px;',
        mobile='grid-template-columns: minmax(0, 1fr);'))
    return section(b, 'why', head + grid, 49, 111, '599:3732', extra='align-items: center;')


def s_demo(b):
    PADIN = 'max(24px, calc((100% - 1475px) / 2))'
    left = pill(b, 'demo-tag', 'See Maximus in Action', extra='margin-bottom: 23px;')
    left += h2(b, 'demo-title', 'What Would Your Practice Look Like With Less Manual Work?', 'max-width: 650px; margin-bottom: 13px;')
    left += para(b, 'demo-text', 'See how Maximus can help automate eligibility, claims, payments, follow-ups, reporting, and other '
                 'revenue-cycle workflows — while giving leadership clearer visibility into performance.', merge(BODY, S(
                     'box-sizing: border-box; width: 631px; max-width: 100%; padding: 0 159px 33px 0; '
                     'border-bottom: 1px solid rgba(79, 79, 79, 0.2); margin-bottom: 32px;', mobile='padding-right: 0;')))
    left += check_item(b, 'demo-live', 'See the platform live', 'Explore the workflows most relevant to your organization.')
    left += check_item(b, 'demo-map', 'Map your current workflow', 'Identify where automation and visibility can make the biggest difference.')
    left += check_item(b, 'demo-interop', 'Review interoperability', 'Discuss EHR, payer, API, HL7, and FHIR connectivity needs.')
    for c in ('demo-map', 'demo-interop'):
        b.style[c] = b.style[c].replace('padding: 0 0 0 57px;', 'padding: 0 0 0 57px; margin-top: 18px;')
    left = b.el('e-flexbox', 'demo-content', left, css=S(
        'display: flex; flex-direction: column; align-items: flex-start; gap: 0px; padding: 0 0 0 3px; flex: 0 1 650px; min-width: 0;',
        tablet_extra='flex: 0 0 auto; width: 100%;'))

    # ---- form card ----
    hd = img(b, 'demo-form-logo', 'logo-mark', '', 'display: block; width: 29px; height: 29px; flex-shrink: 0;')
    ht = b.el('e-heading', 'demo-form-title', cfg={'tag': 'h3', 'title': 'Book Your Maximus Demo'}, css=txt(24, 32, weight=500, ls=-0.6))
    ht += para(b, 'demo-form-text', 'Tell us a little about your organization.', txt(14, 20, '#4F4F4F') + ' margin-top: 4px;')
    hd += b.el('e-flexbox', 'demo-form-heading', ht, css='display: flex; flex-direction: column; gap: 0px; padding: 0;')
    hd = b.el('e-flexbox', 'demo-form-header', hd, css='display: flex; flex-direction: row; align-items: flex-start; gap: 12px; padding: 0;')

    FIELD = ('display: block; box-sizing: border-box; width: 100%; height: 44px; padding: 12px 16px; border-radius: 12px; '
             f'border: 1px solid rgba(0, 0, 0, 0.05); background-color: rgba(244, 244, 244, 0.35); {FONT} font-size: 14px; '
             'line-height: 20px; color: #1A1A1A; box-shadow: 0 1px 2px 0 rgba(26, 43, 74, 0.04); outline: none; '
             'transition: border-color 0.2s, box-shadow 0.2s;')
    FOCUS = {'&:focus': 'border-color: #9ACAA1; box-shadow: 0 0 0 3px rgba(154, 202, 161, 0.25);'}
    LABEL = txt(16, 19.5, weight=500) + ' display: block; margin-bottom: 8px;'

    def field(cid, label, placeholder, typ='text', full=False, required=True):
        f = b.el('e-form-label', cid + '-label', cfg={'text': label, 'input-id': 'maximus-' + cid}, css=LABEL)
        f += b.el('e-form-input', cid + '-input', cfg={'placeholder': placeholder, 'type': typ, 'required': required, '_cssid': 'maximus-' + cid},
                  css=merge(FIELD, FOCUS, {'': 'color: #1A1A1A;'}))
        return b.el('e-div-block', cid, f, css=S(
            f'box-sizing: border-box; width: {"100%" if full else "calc(50% - 10px)"}; min-width: 0; padding: 0;',
            mobile='width: 100%;'))

    def select(cid, label, options, full=False):
        f = b.el('e-form-label', cid + '-label', cfg={'text': label, 'input-id': 'maximus-' + cid}, css=LABEL)
        f += b.el('e-form-select', cid + '-select', cfg={'name': cid.replace('demo-', ''), 'options': [{'key': o, 'value': o} for o in options],
                                                          'has-default-value': True, 'value': options[0], '_cssid': 'maximus-' + cid},
                  css=merge(FIELD, FOCUS, {'': f'color: #4A4A4A; appearance: none; -webkit-appearance: none; padding-right: 44px; '
                                               f'background: url({U("chevron-down")}) no-repeat right 14px center / 16px 16px, rgba(244, 244, 244, 0.35);'}))
        return b.el('e-div-block', cid, f, css=S(
            f'box-sizing: border-box; width: {"100%" if full else "calc(50% - 10px)"}; min-width: 0; padding: 0;',
            mobile='width: 100%;'))
    fields = field('demo-first-name', 'First Name', 'Jane')
    fields += field('demo-last-name', 'Last Name', 'Smith')
    fields += field('demo-email', 'Work Email', 'jane@yourclinic.com', 'email', True)
    fields += field('demo-phone', 'Phone', 'Enter your phone number', 'tel', required=False)
    fields += field('demo-organization', 'Organization', 'Your clinic or group')
    fields += select('demo-providers', 'Number of Providers', ['1–5', '6–10', '11–25', '26–50', '51+'])
    fields += field('demo-pms', 'Current PMS / EHR', 'e.g. Epic, athenahealth', required=False)
    # e-form-select stores options HTML-escaped and escapes them again on render, so '&' would show as '&amp;'
    fields += select('demo-challenge', 'Primary Challenge', ['Eligibility and Benefits', 'Claim Denials', 'Payment Posting',
                                                             'A/R Follow-up', 'Reporting and KPIs', 'Interoperability'], True)
    fields += b.el('e-form-submit-button', 'demo-submit', cfg={'text': 'Schedule My Demo'}, css=merge(S(
        f'{FONT} font-size: 14px; line-height: 20px; font-weight: 500; color: #FFFFFF; display: flex; justify-content: center; '
        f'align-items: center; box-sizing: border-box; width: 100%; height: 56px; margin-top: 12px; padding: 0 60px; '
        f'border: 1px solid #B8DBD4; border-radius: 61px; cursor: pointer; '
        f'background: url({U("arrow-green")}) no-repeat right 16.5px center / 24px 24px, '
        f'radial-gradient(circle at calc(100% - 28.5px) 50%, #FFFFFF 19px, rgba(255, 255, 255, 0) 19.6px), #9ACAA1; '
        f'transition: background-color 0.3s, box-shadow 0.3s;'),
        {'&:hover': 'background-color: #86BD90; box-shadow: 0 10px 24px rgba(49, 131, 113, 0.18);'}))
    fields += b.el('e-form-success-message', 'demo-form-success',
                   para(b, 'demo-form-success-text', 'Thank you — our team will contact you shortly to schedule your demo.', txt(14, 20, '#318371')),
                   css='width: 100%; padding: 0;')
    fields += b.el('e-form-error-message', 'demo-form-error',
                   para(b, 'demo-form-error-text', 'Something went wrong. Please check the fields and try again.', txt(14, 20, '#E6545A')),
                   css='width: 100%; padding: 0;')
    form = b.el('e-form', 'demo-form', fields, cfg={'form-name': 'Maximus demo request'}, css=S(
        'display: flex; flex-direction: row; flex-wrap: wrap; align-items: flex-start; gap: 20px; padding: 0; margin-top: 32px;'))
    card = b.el('e-flexbox', 'demo-form-card', hd + form, css=S(
        f'display: flex; flex-direction: column; gap: 0px; box-sizing: border-box; flex: 0 0 560px; padding: 40px; margin: 27px 47px 0 0; '
        f'border-radius: 24px; background-color: rgba(255, 255, 255, 0.1); box-shadow: 0 30px 80px 0 rgba(26, 43, 74, 0.1); {GLASS}',
        laptop='flex: 0 0 520px; margin-right: 0;',
        tablet_extra='flex: 0 0 auto; width: 100%; max-width: 560px; margin: 56px 0 0;',
        mobile='padding: 28px 18px;'))
    box = b.el('e-flexbox', 'demo-panel', left + card, css=S(
        f'display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 40px; box-sizing: border-box; '
        f'width: 100%; min-height: 1189px; padding: 61px {PADIN} 349px; border-radius: 20px; '
        f'background: url({U("lineart")}) no-repeat right -59px top -206px / 770px 791px, rgba(255, 255, 255, 0.6); '
        f'box-shadow: 0 15px 15px 0 rgba(194, 194, 194, 0.1); {GLASS}',
        laptop='padding-bottom: 300px; min-height: 0;',
        tablet_extra='flex-direction: column; gap: 0px; padding-bottom: 280px;',
        tablet='padding: 56px 32px 300px;', mobile='padding: 40px 16px 320px; border-radius: 16px;'))

    # ---- green CTA overlapping the panel ----
    ct = h2(b, 'demo-cta-title', 'Manage Less. Automate More. See Everything.', 'color: #FFFFFF; max-width: 843px;')
    ct += para(b, 'demo-cta-text', 'AI-Powered Practice Management — Intelligent. Automated. Connected.', merge(BODY, 'color: #FFFFFF; margin-top: 11px;'))
    ct = b.el('e-flexbox', 'demo-cta-copy', ct, css='display: flex; flex-direction: column; gap: 0px; padding: 0; min-width: 0;')
    ct += button(b, 'demo-cta-btn', 'Book a Demo', '#book-demo', 193, 'dark', extra={'': 'padding-left: 29px;'})
    cta = b.el('e-flexbox', 'demo-cta', ct, css=S(
        f'position: relative; z-index: 2; display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 32px; '
        f'box-sizing: border-box; width: auto; min-height: 316px; margin: -257px {PADIN} 0; padding: 52px 134px 52px 86px; border-radius: 20px; '
        f'overflow: hidden; box-shadow: 0 51px 63.6px 0 rgba(89, 89, 89, 0.2); '
        f'background: url({U("cta-mark")}) no-repeat right -201px top -166px / 631px 648px, '
        f'radial-gradient(ellipse 951px 1374px at 28% 27%, #3DA28C 0%, #006750 100%);',
        laptop='padding: 48px 56px;', tablet='flex-direction: column; align-items: flex-start; margin: -240px 16px 0; min-height: 0;',
        mobile='padding: 36px 22px; margin: -270px 8px 0;'))
    mark = img(b, 'demo-watermark', 'watermark', '', S(
        'display: block; width: calc(100% + 144px); max-width: none; height: auto; aspect-ratio: 1949 / 261; object-fit: cover; '
        'object-position: 50% 30%; opacity: 0.2; margin: 76px -72px 0; pointer-events: none;',
        mobile='margin-top: 40px;'))
    return section(b, 'demo', box + cta + mark, 0, 0, '599:3776', cssid='book-demo', extra=S(
        'padding: 0 57px;', laptop='padding: 0 24px;', tablet='padding: 0 24px;', mobile='padding: 0 12px;'))


SECTIONS = [s_hero, s_problems, s_comparison, s_eligibility, s_claims, s_reporting, s_integrations, s_trust, s_why, s_demo]


def move_paragraph_margins(b, xml):
    """The theme sets `p { margin-block-end: 0 !important; }`, so a paragraph's bottom margin is moved
    onto its next sibling as margin-top (base styles only)."""
    import re, xml.etree.ElementTree as ET
    root = ET.fromstring('<r>' + xml + '</r>')
    for parent in root.iter():
        kids = list(parent)
        for a, nxt in zip(kids, kids[1:]):
            if a.tag != 'e-paragraph':
                continue
            cid = a.get('configuration-id'); st = b.style.get(cid, '')
            base, sep, rest = st.partition('\n')
            mb = None
            m = re.search(r'margin-bottom:\s*(-?[\d.]+px);', base)
            if m:
                mb = m.group(1); base = base.replace(m.group(0), '')
            m = re.search(r'margin:\s*(-?[\d.]+(?:px)?)\s+(-?[\d.]+(?:px)?)\s+(-?[\d.]+px)(\s+-?[\d.]+(?:px)?)?;', base)
            if m and m.group(3) not in ('0px',):
                mb = m.group(3)
                l = (m.group(4) or ' ' + m.group(2)).strip()
                base = base.replace(m.group(0), f'margin: {m.group(1)} {m.group(2)} 0 {l};')
            if not mb or mb in ('0px', '0'):
                continue
            b.style[cid] = (base + sep + rest).strip()
            ncid = nxt.get('configuration-id')
            nb, nsep, nrest = b.style.get(ncid, '').partition('\n')
            b.style[ncid] = (nb + f' margin-top: {mb};' + nsep + nrest).strip()


def payload(fns, mode='replace_children', dry=False):
    b = B()
    xml = ''.join(f(b) for f in fns)
    move_paragraph_margins(b, xml)
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style,
            'mode': mode, 'parent_id': 'document', 'dry_run': dry}


if __name__ == '__main__':
    p = payload(SECTIONS, dry='--dry' in sys.argv)
    open(os.path.join(HERE, '_payload.json'), 'w').write(json.dumps(p))
    print(len(json.dumps(p)), 'bytes;', len(p['style']), 'styled elements;', len(p['element_config']), 'configured')
