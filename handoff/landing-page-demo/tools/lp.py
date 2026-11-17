"""PPC landing page ("Landing Page Demo", page 412115), Elementor V4, from "MedCare_MSO_PPC_Landing_Page.html".

Brief:
- full width like the rest of the site: sections use the site class parent-container (no 1200px box); the site's own
  header / footer frame the page (the design's header, footer and FAQ section are not built);
- existing classes only (parent-container, heading-main, specialties-heading, global-text); everything else is a local
  style per element; colours / shadows are the design system's tokens written as hex;
- Media Library assets first (NILA, ASRM, ISO logos); everything else was uploaded from the design file (media.json);
- "Four steps, no disruption" = the design's sticky stack: cards stick at 108/128/148/168px (the design's 88px + 20px
  steps, moved down by the site header) with z-index 1-4; the helper script (tools/helper.py) adds the design's
  scroll-linked scale(1 - .05p) / brightness(1 - .04p) and the "sticky only if every card fits" check;
- the About statement's word-by-word reveal and the mobile sticky bar also come from the helper script.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PID = 412115
M = json.load(open(os.path.join(HERE, '..', 'media.json')))
LIB = {'nila': 392944, 'asrm': 393065, 'iso': 401982}
PHONE, TEL = '(505) 521-2145', 'tel:+15055212145'
DEMO = '#demo'

INK, SLATE, MUTE, BLUE, BLUE_H, MID = '#14212B', '#4A5966', '#6B7A87', '#0367A1', '#034D77', '#023B5C'
B50, B100, B300, GREEN_DK, G100 = '#EAF5FF', '#D6EDFB', '#9CD8F6', '#486323', '#E3F0DC'
HAIR, HAIRS, WASH = 'rgba(3,103,161,0.10)', 'rgba(3,103,161,0.18)', '#F3F8FC'
F = 'font-family: var(--Poppins);'
GRAD = 'linear-gradient(115deg, #1A7CB5 0%, #0367A1 55%, #1E6E81 100%)'
RING = f'box-shadow: 0px 0px 0px 1px {HAIR};'
SH_SM = f'0px 0px 0px 1px {HAIR}, 0px 8px 24px 0px rgba(2,40,66,0.06)'
SH_MD = '0px 0px 0px 1px rgba(3,103,161,0.12), 0px 16px 40px 0px rgba(2,40,66,0.10)'
SH_LG = '0px 0px 0px 1px rgba(3,103,161,0.12), 0px 24px 60px 0px rgba(2,40,66,0.16)'
BLUR = 'backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%);'
EASE = 'cubic-bezier(0.2,0,0,1)'
# inline icons as base64 (the style converter strips %-escapes from url-encoded SVG data URIs)
SVG_LOCK = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCcgZmlsbD0nbm9uZScgc3Ryb2tlPScjNkI3QTg3JyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcgc3Ryb2tlLWxpbmVqb2luPSdyb3VuZCc+PHJlY3QgeD0nNCcgeT0nMTEnIHdpZHRoPScxNicgaGVpZ2h0PScxMCcgcng9JzInLz48cGF0aCBkPSdNOCAxMVY3YTQgNCAwIDAgMSA4IDB2NCcvPjwvc3ZnPg=="
SVG_PHONE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCcgZmlsbD0nbm9uZScgc3Ryb2tlPScjMDM2N0ExJyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcgc3Ryb2tlLWxpbmVqb2luPSdyb3VuZCc+PHBhdGggZD0nTTIyIDE2LjkydjNhMiAyIDAgMCAxLTIuMTggMiAxOS43OSAxOS43OSAwIDAgMS04LjYzLTMuMDcgMTkuNSAxOS41IDAgMCAxLTYtNkExOS43OSAxOS43OSAwIDAgMSAyLjEyIDQuMTggMiAyIDAgMCAxIDQuMTEgMmgzYTIgMiAwIDAgMSAyIDEuNzJjLjEzLjk2LjM2IDEuOS43IDIuODFhMiAyIDAgMCAxLS40NSAyLjExTDguMDkgOS45MWExNiAxNiAwIDAgMCA2IDZsMS4yNy0xLjI3YTIgMiAwIDAgMSAyLjExLS40NWMuOTEuMzQgMS44NS41NyAyLjgxLjdBMiAyIDAgMCAxIDIyIDE2LjkyeicvPjwvc3ZnPg=="
SVG_CHEVRON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMicgaGVpZ2h0PSc4JyB2aWV3Qm94PScwIDAgMTIgOCc+PHBhdGggZD0nTTEgMS41bDUgNSA1LTUnIGZpbGw9J25vbmUnIHN0cm9rZT0nIzZCN0E4Nycgc3Ryb2tlLXdpZHRoPScyJyBzdHJva2UtbGluZWNhcD0ncm91bmQnIHN0cm9rZS1saW5lam9pbj0ncm91bmQnLz48L3N2Zz4="


class B:
    def __init__(self):
        self.cfg, self.style, self.classes = {}, {}, {}

    def el(self, tag, cid, kids='', cfg=None, css='', cls=None):
        assert cid not in self.style and cid not in self.cfg and cid not in self.classes, cid
        if cfg:
            self.cfg[cid] = cfg
        if css:
            self.style[cid] = ' '.join(css.split())
        if cls:
            self.classes[cid] = cls
        return f'<{tag} configuration-id="{cid}">{kids}</{tag}>'


b = B()


def box(cid, kids, css='', link=None, anchor=None):
    cfg = {}
    if link:
        cfg['link'] = {'destination': link}
    if anchor:
        cfg['_cssid'] = anchor
    return b.el('e-div-block', cid, kids, cfg=cfg or None, css='padding: 0px; min-width: 0px; ' + css)  # base: padding 10px, min-width 30px


def flex(cid, kids, css='', cls=None, cfg=None):
    return b.el('e-flexbox', cid, kids, cfg=cfg, css=('padding: 0px; ' if not cls else '') + css, cls=cls)


def grid(cid, kids, css='', anchor=None):
    # e-grid base: padding 10px and grid-template-rows repeat(2, 1fr) (adds an empty second row)
    return b.el('e-grid', cid, kids, cfg={'_cssid': anchor} if anchor else None, css='padding: 0px; grid-template-rows: auto; ' + css)


def p(cid, html, css='', cls=None, anchor=None):
    cfg = {'paragraph': html}
    if anchor:
        cfg['_cssid'] = anchor
    return b.el('e-paragraph', cid, cfg=cfg, css=css, cls=cls)


def h(cid, tag, title, css='', cls=None):
    return b.el('e-heading', cid, cfg={'tag': tag, 'title': title}, css=css, cls=cls)


def img(cid, mid, css='', alt=''):
    return b.el('e-image', cid, cfg={'image': {'src': {'id': mid, 'alt': alt}, 'size': 'full'}}, css=css)


def mid_(name):
    return M[name]['id']


def t(size, lh, color, weight=400, ls=None, extra=''):
    return (f'{F} font-size: {size}px; line-height: {lh}; font-weight: {weight}; color: {color}; margin: 0px; '
            + (f'letter-spacing: {ls}; ' if ls else '') + extra)


def tick(color, w=5, hgt=10, sw=2):
    """CSS check mark (the design's 14px stroke tick) for a ::before / ::after."""
    return (f'content: ""; flex-shrink: 0; width: {w}px; height: {hgt}px; border-style: solid; border-color: {color}; '
            f'border-width: 0px {sw}px {sw}px 0px; transform: rotate(45deg); margin: -3px 3px 0px 3px;')


def check_item(cid, text, color=GREEN_DK, size=14, ink=INK, extra=''):
    return p(cid, text, css=t(size, 1.5, ink, 400, None, f'display: flex; align-items: center; gap: 10px; &::before{{{tick(color)}}} ' + extra))


def eyebrow(cid, label, bg='#FFFFFF', ring=True, css=''):
    return p(cid, label, css=t(11, 1.5, BLUE, 500, '0.12em', (
        f'display: inline-flex; align-items: center; gap: 8px; width: max-content; max-width: 100%; align-self: flex-start; padding: 6px 12px; '
        f'border-radius: 999px; background-color: {bg}; text-transform: uppercase; ' + (RING if ring else '')
        + f' &::before{{content: ""; flex-shrink: 0; width: 6px; height: 6px; border-radius: 999px; background-color: {BLUE};}} ' + css)))


def h2(cid, title, color=INK, size=44, css=''):
    return h(cid, 'h2', title, cls=['specialties-heading'], css=(
        f'{F} font-size: {size}px; font-weight: 500; line-height: 1.08; letter-spacing: -0.035em; color: {color}; margin: 0px; '
        '@media(--tablet_extra){font-size: 40px;} @media(--tablet){font-size: 36px;} @media(--mobile){font-size: 30px;} ' + css))


def lead(cid, text, size=16, color=SLATE, css=''):
    return p(cid, text, cls=['global-text'], css=f'font-size: {size}px; line-height: 1.6; color: {color}; margin: 0px; ' + css)


def btn(cid, label, url=DEMO, kind='primary', size='lg', css=''):
    dims = {'lg': 'height: 52px; padding: 0px 28px; font-size: 16px;', 'md': 'height: 42px; padding: 0px 20px; font-size: 15px;'}[size]
    look = {'primary': f'background-color: {BLUE}; color: #FFFFFF; &:hover{{background-color: {BLUE_H}; color: #FFFFFF;}}',
            'white': f'background-color: #FFFFFF; color: {MID}; &:hover{{background-color: {B50}; color: {MID};}}'}[kind]
    return b.el('e-button', cid, cfg={'text': label, 'link': {'destination': url}}, css=(
        f'{F} display: inline-flex; align-items: center; justify-content: center; width: max-content; {dims} font-weight: 500; line-height: 1; '
        f'white-space: nowrap; border: 0px; border-radius: 999px; text-decoration: none; cursor: pointer; '
        f'transition: background-color 0.18s {EASE}; {look} &:focus-visible{{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.22);}} ' + css))


def section(cid, kids, anchor=None, css=''):
    cfg = {'tag': 'section'}
    if anchor:
        cfg['_cssid'] = anchor
    return flex(cid, kids, cls=['parent-container'], cfg=cfg, css=(
        'display: flex; flex-direction: column; align-items: stretch; gap: 40px; width: 100%; position: relative; '
        'padding-block-start: 0px; padding-block-end: 120px; '
        '@media(--tablet){padding-block-end: 88px;} @media(--mobile){padding-block-end: 64px; gap: 32px;} ' + css))


def badge(cid, text, tone):
    bg, fg = {'neutral': ('#EFF2F5', SLATE), 'blue': ('rgba(3,103,161,0.09)', BLUE), 'success': ('rgba(126,176,62,0.16)', GREEN_DK),
              'warning': ('#FCECCB', '#8A5A06')}[tone]
    return p(cid, text, css=t(11, 1, fg, 500, None, (
        f'display: inline-flex; align-items: center; width: max-content; height: 20px; padding: 0px 8px; border-radius: 999px; '
        f'background-color: {bg}; white-space: nowrap;')))


# ---------------------------------------------------------------- form (hero + closing)
COLLECTIONS = ['Under $100K', '$100K–$500K', '$500K–$1M', '$1M–$2M', 'Over $2M']


def form(pre, heading=True):
    label = t(13, 1.5, INK, 500, None, 'display: block; margin-bottom: 6px; & span{color: #E0533D; margin-inline-start: 2px;}')
    field = (f'{F} display: block; width: 100%; height: 44px; padding: 0px 14px; margin: 0px; border: 0px; border-radius: 8px; background-color: {WASH}; '
             f'font-size: 15px; line-height: 1.5; color: {INK}; outline: none; box-shadow: inset 0px 0px 0px 1px {HAIRS}; '
             f'transition: background-color 0.12s ease, box-shadow 0.12s ease; &::placeholder{{color: #9AA7B2;}} '
             f'&:hover{{box-shadow: inset 0px 0px 0px 1px rgba(3,103,161,0.32);}} '
             f'&:focus{{background-color: #FFFFFF; box-shadow: inset 0px 0px 0px 2px {BLUE}, 0px 0px 0px 3px rgba(3,103,161,0.22);}}')
    chevron = 'appearance: none; -webkit-appearance: none; padding-inline-end: 38px; cursor: pointer;'
    # a <select> has no pseudo-elements, so the arrow is drawn by the wrapper (bottom-right, over the field)
    arrow = (f"position: relative; &::after{{content: \"\"; position: absolute; right: 14px; bottom: 18px; width: 12px; height: 8px; pointer-events: none; "
             f"background-repeat: no-repeat; background-size: 12px 8px; background-image: url('{SVG_CHEVRON}');}}")
    fields = ''
    for key, lab, typ, ph, span in (('name', 'Full name', 'text', 'Dr. Jane Smith', True), ('email', 'Work email', 'email', 'jane@practice.com', False),
                                    ('phone', 'Phone', 'tel', '(555) 555-0100', False), ('practice', 'Practice name', 'text', 'Smith Family Medicine', True)):
        fields += box(f'{pre}f-{key}', b.el('e-form-label', f'{pre}l-{key}', cfg={'text': f'{lab} <span>*</span>', 'input-id': f'{pre}{key}'}, css=label)
                      + b.el('e-form-input', f'{pre}i-{key}', cfg={'type': typ, 'placeholder': ph, 'required': True, '_cssid': f'{pre}{key}'}, css=field),
                      css='width: 100%;' + (' grid-column: 1 / -1;' if span else ''))
    fields += box(f'{pre}f-coll', b.el('e-form-label', f'{pre}l-coll', cfg={'text': 'Monthly collections (optional)', 'input-id': f'{pre}coll'}, css=label)
                  + b.el('e-form-select', f'{pre}s-coll', cfg={'name': 'collections', 'options': [{'key': o, 'value': o} for o in ['Select a range'] + COLLECTIONS],
                                                             'has-default-value': True, 'value': 'Select a range', '_cssid': f'{pre}coll'},
                         css=field + ' ' + chevron), css='width: 100%; grid-column: 1 / -1; ' + arrow)
    fields += b.el('e-form-submit-button', f'{pre}sub', cfg={'text': 'Book my free demo'}, css=(
        f'{F} grid-column: 1 / -1; display: flex; align-items: center; justify-content: center; width: 100%; height: 52px; padding: 0px 28px; margin-top: 4px; '
        f'border: 0px; border-radius: 999px; background-color: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 500; line-height: 1; cursor: pointer; '
        f'transition: background-color 0.18s {EASE}; &:hover{{background-color: {BLUE_H};}} '
        '&:focus-visible{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.22);}'))
    if heading:
        fields += p(f'{pre}note', 'Your details stay private. No obligation.', css=t(12, 1.5, MUTE, 400, None, (
            'grid-column: 1 / -1; display: flex; align-items: center; gap: 8px; '
            f"&::before{{content: \"\"; flex-shrink: 0; width: 14px; height: 14px; background-repeat: no-repeat; background-size: 14px 14px; background-image: url('{SVG_LOCK}');}}")))
    fields += b.el('e-form-success-message', f'{pre}ok', p(f'{pre}okt', '<strong>Thanks. Your request is in.</strong> A billing specialist will call you within 15 minutes '
                                                                       'during business hours to schedule your demo.', css=t(15, 1.6, SLATE, 400, None, (
        f'& strong{{display: block; font-size: 22px; font-weight: 500; letter-spacing: -0.02em; color: {INK}; margin-bottom: 8px;}}'))),
        css=f'grid-column: 1 / -1; padding: 20px; border-radius: 12px; background-color: #F1F8EC; box-shadow: inset 0px 0px 0px 1px rgba(126,176,62,0.3);')
    fields += b.el('e-form-error-message', f'{pre}err', p(f'{pre}errt', 'Something went wrong. Please check the fields and try again.', css=t(14, 1.5, '#C8412C')),
                   css='grid-column: 1 / -1; padding: 0px;')
    return b.el('e-form', f'{pre}form', fields, cfg={
        'form-name': 'PPC landing page demo request' + (' (hero)' if heading else ' (closing)'),
        'actions-after-submit': ['email', 'collect-submissions'],
        'email': {'to': ['mkamran@medcaremso.com', 'fashraf@medcaremso.com'], 'subject': 'New demo request: PPC landing page',
                  'message': '[all-fields]', 'from': 'email@medcaremso.com', 'from-name': 'MedCare MSO', 'send-as': 'html'}}, css=(
        'display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto; gap: 16px; width: 100%; padding: 0px; '
        '@media(--mobile){grid-template-columns: 1fr;}'))


# ---------------------------------------------------------------- 1. hero + stats
def hero():
    h1 = h('h1', 'h1', f'Clean claims.<br>Faster payments.<br><span>Revenue in plain sight.</span>', cls=['heading-main'], css=(
        f'{F} font-size: 68px; font-weight: 500; line-height: 1.02; letter-spacing: -0.04em; color: {INK}; margin: 0px; & span{{color: {BLUE};}} '
        '@media(--laptop){font-size: 62px;} @media(--tablet_extra){font-size: 54px;} @media(--tablet){font-size: 56px;} @media(--mobile){font-size: 40px;}'))
    call = box('h-call', p('h-callt', f'Call {PHONE}', css=t(15, 1, INK, 500, None, 'white-space: nowrap;')), link=TEL, css=(
        f'display: inline-flex; align-items: center; width: max-content; height: 52px; padding: 0px 24px; border-radius: 999px; background-color: #FFFFFF; {RING} '
        f'text-decoration: none; transition: background-color 0.18s {EASE}; &:hover{{background-color: {B50};}}'))
    trust = flex('h-tr', ''.join(check_item(f'h-tr{i}', s, GREEN_DK, 13, SLATE, 'gap: 6px;') for i, s in enumerate(('HIPAA compliant', 'Works with your EHR', 'All 50 states'))),
                 css='display: flex; flex-direction: row; flex-wrap: wrap; column-gap: 20px; row-gap: 8px;')
    left = box('h-l', eyebrow('h-e', 'Medical billing &amp; RCM services') + h1
               + lead('h-p', 'MedCare MSO runs your full revenue cycle, from eligibility checks to payment posting. 800+ AAPC-certified billers and AI-assisted '
                             'claim scrubbing keep claims clean and cash flow steady.', 18, css='max-width: 520px; @media(--mobile){font-size: 16px;}')
               + flex('h-btns', btn('h-b1', 'Book a free demo') + call, css='display: flex; flex-direction: row; flex-wrap: wrap; gap: 12px;')
               + trust, css='display: flex; flex-direction: column; gap: 24px;')
    card = box('h-form', h('h-fh', 'h2', 'Book a free demo', css=t(24, 1.3, INK, 500, '-0.03em'))
               + p('h-fp', 'See how we would run your billing. A specialist calls you back within 15 minutes during business hours.', css=t(14, 1.5, SLATE, 400, None, 'margin-top: 6px; margin-bottom: 20px;'))
               + form('lph-'), anchor='demo', css=(
        f'background-color: #FFFFFF; border-radius: 16px; box-shadow: {SH_LG}; padding: 36px; scroll-margin-top: 100px; '
        '@media(--mobile){padding: 24px;}'))
    top = grid('h-grid', left + card, css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 72px; row-gap: 40px; align-items: center; '
        '@media(--tablet_extra){column-gap: 48px;} @media(--tablet){grid-template-columns: 1fr;}'))

    def stat(i, lab, num):
        return box(f'hs{i}', p(f'hs{i}l', lab, css=t(11, 1.5, MUTE, 500, '0.12em', 'text-transform: uppercase;'))
                   + p(f'hs{i}n', num, css=t(56, 1, INK, 500, '-0.04em', (
                       f'& span{{font-size: 18px; letter-spacing: 0px; color: {SLATE}; margin-left: 8px;}} '
                       '@media(--tablet_extra){font-size: 48px;} @media(--mobile){font-size: 40px;}'))),
                   css='display: flex; flex-direction: column; gap: 28px; padding: 24px 28px; background-color: #FFFFFF;')
    stats = grid('hs', stat(0, 'Clean claim rate', '98%') + stat(1, 'Reduction in A/R', '30%') + stat(2, 'Revenue increase', '15–20%')
                 + stat(3, 'Turnaround time', '7–14<span>days</span>'), css=(
        f'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; background-color: {HAIR}; border-radius: 24px; overflow: hidden; box-shadow: {SH_SM}; '
        '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile){grid-template-columns: 1fr;}'))
    logo_css = 'display: block; height: 32px; width: auto; filter: grayscale(1); opacity: 0.85; transition: opacity 0.2s ease, filter 0.2s ease; &:hover{opacity: 1; filter: grayscale(0);}'
    logos = flex('hl', img('hl1', mid_('lp-logo-aapc'), logo_css, 'AAPC') + img('hl2', mid_('lp-logo-hipaa'), logo_css, 'HIPAA compliant')
                 + img('hl3', LIB['iso'], logo_css, 'ISO 9001') + img('hl4', LIB['asrm'], logo_css, 'ASRM') + img('hl5', LIB['nila'], logo_css, 'NILA'),
                 css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; column-gap: 32px; row-gap: 16px; width: max-content; max-width: 100%;')
    note = flex('hn', p('hn-t', 'MedCare MSO client averages. Results vary by specialty and payer mix.', css=t(12, 1.5, MUTE, 400, None, 'width: max-content; max-width: 100%;')) + logos, css=(
        'display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: space-between; column-gap: 40px; row-gap: 16px; padding: 8px 4px;'))
    return section('lp-hero', top + box('h-stats', stats + note, css='display: flex; flex-direction: column; gap: 16px; padding-top: 16px;'), css=(
        'padding-block-start: 80px; gap: 40px; @media(--tablet){padding-block-start: 56px;} @media(--mobile){padding-block-start: 40px;}'))


# ---------------------------------------------------------------- 2. about (word reveal)
STATEMENT = ('We are MedCare MSO. We help physicians, group practices and specialty clinics collect what they have earned. Our AAPC-certified '
             'billers and AI-assisted tools handle every step of the revenue cycle, so you can focus on patients while we handle the billing.')


def about():
    photo = box('ab-pic', img('ab-img', mid_('lp-about-physician-desk'), 'display: block; width: 100%; height: 100%; object-fit: cover;',
                              'Physician at his desk in his clinic'), css=(
        f'border-radius: 24px; overflow: hidden; aspect-ratio: 4 / 3; background-color: {B50}; box-shadow: {SH_SM};'))
    badge_ = box('ab-st', p('ab-stn', '1,200+', css=t(44, 1, '#FFFFFF', 500, '-0.04em'))
                 + p('ab-stl', 'practices trust us with their billing', css=t(13, 1.45, 'rgba(255,255,255,0.9)')), css=(
        f'position: absolute; left: 28px; bottom: 0px; display: flex; flex-direction: column; gap: 8px; width: 240px; max-width: 60%; padding: 24px; '
        f'border-radius: 16px; background-image: {GRAD}; box-shadow: {SH_MD}; @media(--mobile){{left: 16px;}}'))
    left = box('ab-l', photo + badge_, css='position: relative; padding-bottom: 48px;')
    words = ' '.join(f'<span>{w}</span>' for w in STATEMENT.split(' '))
    statement = p('ab-s', words, anchor='lp-statement', css=t(30, 1.35, INK, 500, '-0.02em', (
        f'& span{{color: #C9D3DB; transition: color 280ms {EASE};}} @media(--tablet_extra){{font-size: 26px;}} @media(--mobile){{font-size: 22px;}}')))
    rows = ''
    for i, s in enumerate(('End-to-end revenue cycle management', 'AI-assisted coding and claim scrubbing', 'Real-time reporting on claims and collections')):
        rows += flex(f'ab-r{i}', p(f'ab-r{i}t', s, css=t(15, 1.5, INK, 500))
                     + box(f'ab-r{i}c', '', css=(f'display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 28px; height: 28px; '
                                                f'border-radius: 999px; background-color: {B50}; &::after{{{tick(BLUE, 5, 9)} margin: -2px 0px 0px 0px;}}')),
                     css=f'display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 16px; padding: 16px 0px; border-bottom: 1px solid {HAIRS};')
    right = box('ab-r', eyebrow('ab-e', 'About MedCare MSO') + statement
                + box('ab-list', rows, css=f'display: flex; flex-direction: column; border-top: 1px solid {HAIRS};'),
                css='display: flex; flex-direction: column; gap: 28px;')
    g = grid('ab-g', left + right, css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 88px; row-gap: 40px; align-items: center; '
        '@media(--tablet_extra){column-gap: 56px;} @media(--tablet){grid-template-columns: 1fr;}'))
    return section('lp-about', g, css='padding-block-start: 120px; @media(--tablet){padding-block-start: 88px;} @media(--mobile){padding-block-start: 64px;}')


# ---------------------------------------------------------------- 3. services (tabs)
TABS = [
    ('Billing', 'Medical billing &amp; claim submission', 'lp-svc-billing', 'cover', 'center 25%', 'lp-icon-invoice',
     'We submit clean claims to 800+ payers and post every payment against the right account, so your books match your deposits.',
     ['Charge entry and claim submission', 'Electronic claims (CMS-1500, UB-04)', 'Payment posting and reconciliation', 'Patient statements', 'Monthly financial reporting']),
    ('Coding', 'Medical coding', 'lp-svc-coding', 'cover', 'center 25%', 'lp-icon-claims',
     'Certified coders apply current CPT and ICD guidelines before a claim goes out. Our clean claim rate is 98%.',
     ['CPT, ICD-10 and HCPCS coding', 'Modifier review', 'Pre-submission claim scrubbing', 'Coding audits', 'Documentation feedback for providers']),
    ('Denials', 'Denial management', 'lp-svc-denials', 'auto 155%', '65% 22%', 'lp-icon-shield-check',
     'Every denial is analyzed, appealed and traced to its cause, reducing denials by up to 50%.',
     ['Root-cause analysis', 'Corrected claims and appeals', 'Payer trend reporting', 'Prevention rules in claim scrubbing']),
    ('A/R recovery', 'Accounts receivable recovery', 'lp-svc-ar-recovery', 'cover', 'center 25%', 'lp-icon-payment-cycle',
     'We work every open balance, including claims over 120 days, and reduce outstanding A/R by 30% on average.',
     ['Aged A/R clean-up (120+ days)', 'Payer follow-up', 'Underpayment detection', 'Patient balance follow-up']),
    ('Credentialing', 'Medical credentialing', 'lp-svc-credentialing', 'cover', 'center 25%', 'lp-icon-people',
     'We enroll your providers with commercial and government payers, with a 95% success rate.',
     ['Payer enrollment', 'CAQH profile management', 'Re-credentialing tracking', 'Revalidation reminders']),
    ('Prior auth', 'Eligibility &amp; prior authorization', 'lp-svc-prior-auth', 'cover', 'center 25%', 'lp-icon-stethoscope',
     'We verify coverage and secure authorizations before the visit, so claims don’t stall on missing paperwork.',
     ['Eligibility and benefits verification', 'Prior authorization requests', 'Authorization tracking', 'Patient registration review']),
]


def glass_item(cid, text):
    return check_item(cid, text, '#C6E2BE', 14, '#FFFFFF', (
        'gap: 12px; padding: 10px 14px; border-radius: 8px; background-color: rgba(255,255,255,0.10); box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.16);'))


def services():
    head = grid('sv-head', box('sv-hl', eyebrow('sv-e', 'Our services', B50, False) + h2('sv-h2', 'Your full revenue cycle, handled end to end'),
                                css='display: flex; flex-direction: column; gap: 16px;')
                + lead('sv-p', 'One team owns every step between the patient visit and the payment in your account, so nothing falls between vendors.'), css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 48px; row-gap: 24px; align-items: end; padding: 56px 56px 32px; '
        '@media(--tablet){grid-template-columns: 1fr; padding: 40px 32px 24px;} @media(--mobile){padding: 32px 24px 24px;}'))
    tab_css = (f'{F} display: inline-flex; align-items: center; flex-shrink: 0; width: auto; padding: 8px 16px; border: 0px; border-radius: 999px; '
               f'font-size: 13px; font-weight: 500; line-height: 1.5; color: {SLATE}; background-color: transparent; cursor: pointer; white-space: nowrap; outline: none; '
               f'transition: background-color 0.18s {EASE}, color 0.18s {EASE}, box-shadow 0.18s {EASE}; &:hover{{color: {INK};}} '
               f'&[aria-selected="true"]{{background-color: #FFFFFF; color: {INK}; box-shadow: 0px 1px 2px 0px rgba(2,40,66,0.08), 0px 0px 0px 1px {HAIR};}} '
               '&:focus-visible{box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.22);}')
    tabs, panels = '', ''
    for i, (label, title, pic, size, pos, icon, desc, items) in enumerate(TABS):
        tabs += b.el('e-tab', f'sv-t{i}', p(f'sv-t{i}l', label, css='margin: 0px; font: inherit; color: inherit;'), css=tab_css)
        photo = box(f'sv{i}-pic', '', css=(
            f"min-height: 280px; height: 100%; background-color: {B50}; background-image: url('{M[pic]['url']}'); background-size: {size}; "
            f'background-position: {pos}; background-repeat: no-repeat; @media(--tablet){{display: none;}}'))
        mid = box(f'sv{i}-m', img(f'sv{i}-ic', mid_(icon), 'display: block; width: 44px; height: 44px; object-fit: contain;')
                  + h(f'sv{i}-h', 'h3', title, css=t(24, 1.25, INK, 500, '-0.02em'))
                  + p(f'sv{i}-p', desc, css=t(15, 1.65, SLATE))
                  + p(f'sv{i}-a', f'<a href="{DEMO}">Discuss this on your demo<span>→</span></a>', css=t(14, 1.5, BLUE, 500, None, (
                      f'margin-top: auto; padding-top: 8px; & a{{display: inline-flex; align-items: center; gap: 8px; color: {BLUE}; text-decoration: none;}} '
                      f'& span{{transition: transform 0.18s {EASE};}} & a:hover{{color: {BLUE_H};}} & a:hover span{{transform: translateX(3px);}}'))),
                  css='display: flex; flex-direction: column; gap: 16px; padding: 40px; @media(--mobile){padding: 28px 24px;}')
        inc = box(f'sv{i}-inc', p(f'sv{i}-il', 'What’s included', css=t(11, 1.5, B300, 500, '0.12em', 'text-transform: uppercase;'))
                  + box(f'sv{i}-ul', ''.join(glass_item(f'sv{i}-li{j}', it) for j, it in enumerate(items)), css='display: flex; flex-direction: column; gap: 10px;'),
                  css=f'display: flex; flex-direction: column; gap: 20px; padding: 40px; background-image: {GRAD}; @media(--mobile){{padding: 28px 24px;}}')
        panels += b.el('e-tab-content', f'sv-c{i}', grid(f'sv{i}', photo + mid + inc, css=(
            'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0px; align-items: stretch; '
            '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile){grid-template-columns: 1fr;}')),
            css='display: block; width: 100%; padding: 0px;')
    menu = b.el('e-tabs-menu', 'sv-menu', tabs, css=(
        f'display: inline-flex; flex-direction: row; justify-content: flex-start; gap: 2px; width: max-content; max-width: calc(100% - 112px); padding: 5px; '
        f'margin: 0px 56px 24px; border-radius: 999px; background-color: rgba(255,255,255,0.6); {BLUR} overflow-x: auto; scrollbar-width: none; '
        f'box-shadow: 0px 0px 0px 1px {HAIR}, 0px 8px 24px 0px rgba(2,40,66,0.06); '
        '@media(--tablet){margin: 0px 32px 24px; max-width: calc(100% - 64px);} @media(--mobile){margin: 0px 24px 24px; max-width: calc(100% - 48px);}'))
    area = b.el('e-tabs-content-area', 'sv-area', panels, css=f'display: block; width: 100%; padding: 0px; border-top: 1px solid {HAIR};')
    tabs_el = b.el('e-tabs', 'sv-tabs', menu + area, cfg={'default-active-tab': 0}, css='display: flex; flex-direction: column; align-items: flex-start; gap: 0px; width: 100%; padding: 0px;')
    card = box('sv-card', head + tabs_el, css=f'background-color: #FFFFFF; border-radius: 24px; box-shadow: {SH_SM}; overflow: hidden;')
    return section('lp-services', card)


# ---------------------------------------------------------------- 4. why us
def why():
    left = box('wy-l', eyebrow('wy-e', 'Why MedCare MSO') + h2('wy-h2', 'Built for clean claims and steady cash flow')
               + lead('wy-p', 'Certified billers, AI-assisted checks and clear reporting, working together on every claim.', css='max-width: 480px;'),
               css='display: flex; flex-direction: column; gap: 16px;')
    meter = p('wy-bar', ''.join('<span>​</span>' for _ in range(50)), css=(
        'display: grid; grid-template-columns: repeat(50, minmax(0, 1fr)); gap: 3px; margin: 0px; font-size: 0px; line-height: 0; '
        f'& span{{display: block; height: 14px; border-radius: 2px; background-color: {BLUE};}} & span:last-child{{background-color: {B100};}}'))
    card = box('wy-card', flex('wy-ct', p('wy-cl', 'Clean claim rate', css=t(11, 1.5, MUTE, 500, '0.12em', 'text-transform: uppercase;'))
                                + p('wy-cn', '98%', css=t(22, 1.5, INK, 500, '-0.02em')),
                                css='display: flex; flex-direction: row; justify-content: space-between; align-items: baseline; gap: 16px;')
               + meter + p('wy-cp', '98 of every 100 claims we submit are accepted on the first pass. MedCare MSO client average.', css=t(13, 1.5, SLATE)), css=(
        f'display: flex; flex-direction: column; gap: 14px; padding: 24px 28px; background-color: #FFFFFF; border-radius: 16px; box-shadow: {SH_SM};'))
    top = grid('wy-top', left + card, css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 64px; row-gap: 32px; align-items: center; @media(--tablet){grid-template-columns: 1fr;}'))
    cells = ''
    for i, (k, v) in enumerate((('01 · Accuracy', '98% clean claims, coded by AAPC-certified staff'), ('02 · Speed', '7–14 day turnaround on reimbursements'),
                                ('03 · Compliance', 'HIPAA compliant and ISO 9001 certified'), ('04 · Coverage', '800+ payers across all 50 states'))):
        cells += box(f'wy{i}', p(f'wy{i}k', k, css=t(12, 1.5, BLUE)) + p(f'wy{i}v', v, css=t(20, 1.25, INK, 500, '-0.02em')), css=(
            f'display: flex; flex-direction: column; justify-content: space-between; gap: 32px; min-height: 180px; padding: 28px; background-color: #FFFFFF; '
            f'transition: background-color 0.2s ease; &:hover{{background-color: {WASH};}}'))
    row = grid('wy-row', cells, css=(
        f'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; background-color: {HAIR}; border-radius: 24px; overflow: hidden; box-shadow: {SH_SM}; '
        '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile){grid-template-columns: 1fr;}'))
    return section('lp-why', top + row)


# ---------------------------------------------------------------- 5. specialties (vertical tabs)
SPECS = [('Cardiology', 'Imaging and procedure authorizations, modifier-heavy E/M coding and high-value claims that can’t sit in A/R. We track each one from authorization to payment.'),
         ('Behavioral health', 'Time-based psychotherapy codes, telehealth rules and frequent authorization renewals. We keep sessions authorized and coded correctly.'),
         ('Orthopedics', 'Surgical global periods, DME and multiple-procedure modifiers. We code each encounter so surgical claims pay on the first pass.'),
         ('Urgent care', 'High visit volume, walk-in eligibility checks and a wide payer mix. We verify coverage fast and keep daily claim volume moving.'),
         ('Oncology', 'Infusion coding, drug units and frequent prior authorizations. We match every dose and authorization so high-cost claims aren’t underpaid.'),
         ('Laboratory &amp; pathology', 'Medical necessity checks, high claim volume and payer-specific test coverage. We screen each claim before it goes out.'),
         ('Physical therapy', 'Timed units, plan-of-care certifications and visit limits. We track caps and recertifications so visits stay billable.')]


def specialties():
    chips = flex('sp-chips', ''.join(p(f'sp-ch{i}', s, css=t(13, 1.5, INK, 400, None, f'padding: 7px 14px; border-radius: 999px; background-color: #FFFFFF; {RING} width: max-content;'))
                                     for i, s in enumerate(('30+ specialties covered', '800+ payers', 'Solo practices to multi-site groups'))),
                 css='display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px;')
    head = grid('sp-head', box('sp-hl', eyebrow('sp-e', 'Specialties') + h2('sp-h2', 'Billing that knows your specialty')
                               + lead('sp-p', 'Every specialty has its own codes, authorizations and payer rules. Our billers work in yours every day.', css='max-width: 480px;'),
                               css='display: flex; flex-direction: column; gap: 16px;') + chips, css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 64px; row-gap: 24px; align-items: end; @media(--tablet){grid-template-columns: 1fr;}'))
    photo = box('sp-pic', img('sp-img', mid_('lp-specialties-consult'), 'display: block; width: 100%; height: 100%; object-fit: cover; object-position: 40% center;',
                              'Physician consulting with a patient'), css=f'min-height: 300px; background-color: {B50}; @media(--tablet){{display: none;}}')
    tab_css = (f'{F} display: flex; align-items: center; width: 100%; padding: 14px 28px; border: 0px; border-radius: 0px; font-size: 15px; font-weight: 400; '
               f'line-height: 1.5; color: {INK}; background-color: transparent; cursor: pointer; text-align: left; outline: none; '
               f'transition: background-color 0.18s {EASE}, color 0.18s {EASE}; &:hover{{background-color: rgba(234,245,255,0.55);}} '
               f'&[aria-selected="true"]{{background-color: {B50}; color: {BLUE}; font-weight: 600;}} &[aria-selected="true"] span{{opacity: 1;}} '
               '&:focus-visible{box-shadow: inset 0px 0px 0px 2px rgba(3,103,161,0.35);} @media(--mobile){padding: 12px 20px;}')
    tabs, panels = '', ''
    for i, (name, desc) in enumerate(SPECS):
        tabs += b.el('e-tab', f'sp-t{i}', p(f'sp-t{i}l', f'{name}<span>→</span>', css=(
            f'display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%; margin: 0px; font: inherit; color: inherit; '
            f'& span{{font-size: 18px; color: {BLUE}; opacity: 0; transition: opacity 0.18s {EASE};}}')), css=tab_css)
        panels += b.el('e-tab-content', f'sp-c{i}', box(f'sp{i}', box(f'sp{i}-t', p(f'sp{i}-n', name, css=t(11, 1.5, B300, 500, '0.12em', 'text-transform: uppercase;'))
                                                                     + p(f'sp{i}-d', desc, css=t(18, 1.55, '#FFFFFF')), css='display: flex; flex-direction: column; gap: 16px;')
                                                         + btn(f'sp{i}-b', 'Book a free demo', DEMO, 'white', 'md'), css=(
            f'display: flex; flex-direction: column; justify-content: space-between; gap: 32px; height: 100%; padding: 40px; background-image: {GRAD}; '
            '@media(--mobile){padding: 28px 24px;}')), css='display: block; width: 100%; height: 100%; padding: 0px;')
    menu = b.el('e-tabs-menu', 'sp-menu', tabs, css='display: flex; flex-direction: column; justify-content: flex-start; gap: 0px; width: 100%; padding: 12px 0px; margin: 0px;')
    area = b.el('e-tabs-content-area', 'sp-area', panels, css='display: block; width: 100%; height: 100%; padding: 0px;')
    tabs_el = b.el('e-tabs', 'sp-tabs', menu + area, cfg={'default-active-tab': 0}, css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); grid-column: span 2; gap: 0px; padding: 0px; align-items: stretch; '
        '@media(--mobile){grid-template-columns: 1fr; grid-column: span 1;}'))
    panel = grid('sp-panel', photo + tabs_el, css=(
        f'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0px; border-radius: 24px; overflow: hidden; box-shadow: {SH_SM}; background-color: #FFFFFF; '
        '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile){grid-template-columns: 1fr;}'))
    return section('lp-specialties', head + panel)


# ---------------------------------------------------------------- 6. four steps (sticky stack)
def table(cid, title, tone, tone_text, body):
    return box(cid, flex(f'{cid}-h', p(f'{cid}-ht', title, css=t(14, 1.4, INK, 600)) + badge(f'{cid}-hb', tone_text, tone), css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 12px; padding: 14px 16px; '
        'border-bottom: 1px solid rgba(3,103,161,0.08);')) + body, css=(
        f'border-radius: 16px; overflow: hidden; background-color: rgba(255,255,255,0.96); box-shadow: 0px 0px 0px 1px {HAIR}, 0px 12px 32px 0px rgba(2,40,66,0.06);'))


def trow(cid, cols, kids, extra=''):
    return grid(cid, kids, css=(f'display: grid; grid-template-columns: {cols}; gap: 12px; align-items: center; padding: 12px 16px; '
                                f'border-top: 1px solid rgba(3,103,161,0.06); {F} font-size: 13.5px; color: {INK}; ' + extra))


def cell(cid, text, extra=''):
    return p(cid, text, css=t(13.5, 1.45, INK, 400, None, extra))


def visual(cid, inner):
    return box(cid, inner, css=(
        'border-radius: 24px; padding: 32px; background-color: #EAF5FF; '
        'background-image: radial-gradient(70% 80% at 100% 100%, rgba(58,150,204,0.30) 0%, rgba(58,150,204,0) 70%), '
        'radial-gradient(60% 70% at 0% 0%, rgba(156,216,246,0.45) 0%, rgba(156,216,246,0) 70%); '
        f'box-shadow: 0px 0px 0px 1px {HAIR}; @media(--mobile){{padding: 16px;}}'))


def step_visual(i):
    if i == 0:
        rows = ''.join(trow(f'v0r{j}', 'minmax(0, 1fr) auto', cell(f'v0r{j}t', a) + badge(f'v0r{j}b', bt, tn))
                       for j, (a, bt, tn) in enumerate((('Denials from missing modifiers', 'Fixable', 'warning'), ('Claims in A/R over 90 days', 'Recoverable', 'warning'),
                                                        ('Eligibility checked after the visit', 'Process gap', 'blue'))))
        tbl = table('v0t', 'Billing review · findings', 'neutral', 'Sample', rows)
        return visual('v0', box('v0-pic', img('v0-img', mid_('lp-step-billing-review'), 'display: block; width: 100%; height: 100%; object-fit: cover;',
                                              'Physician reviewing paperwork at his desk')
                                + box('v0-ov', tbl, css='position: absolute; left: 12px; right: 12px; bottom: 12px; width: calc(100% - 24px);'), css=(
            f'position: relative; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 3; box-shadow: 0px 0px 0px 1px {HAIR}; @media(--mobile){{aspect-ratio: 3 / 4;}}')))
    if i == 1:
        def ico(cid, done):
            if done:
                return box(cid, '', css=(f'display: flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 999px; '
                                         f'background-color: {G100}; &::after{{{tick(GREEN_DK, 4, 8)} margin: -2px 0px 0px 0px;}}'))
            return box(cid, '', css=(f'display: flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 999px; '
                                     f'background-color: {B50}; &::after{{content: ""; width: 6px; height: 6px; border-radius: 999px; background-color: {BLUE};}}'))
        rows = ''.join(trow(f'v1r{j}', '22px minmax(0, 1fr) auto', ico(f'v1r{j}i', d) + cell(f'v1r{j}t', a) + badge(f'v1r{j}b', bt, tn))
                       for j, (a, bt, tn, d) in enumerate((('EHR and PM access connected', 'Done', 'success', True), ('Payer enrollments confirmed', 'Done', 'success', True),
                                                           ('Open claims imported', 'Done', 'success', True), ('Billing team assigned', 'Today', 'blue', False))))
        prog = box('v1p', flex('v1p-r', p('v1p-l', 'Setup progress', css=t(12, 1.5, MUTE)) + p('v1p-v', '3 of 4', css=t(12, 1.5, MUTE)),
                               css='display: flex; flex-direction: row; justify-content: space-between;')
                   + box('v1p-bar', box('v1p-fill', '', css=f'width: 75%; height: 100%; border-radius: 999px; background-color: {BLUE};'),
                         css=f'height: 8px; border-radius: 999px; background-color: {B50}; overflow: hidden;'), css=(
            'display: flex; flex-direction: column; gap: 8px; padding: 14px 16px 16px; border-top: 1px solid rgba(3,103,161,0.06);'))
        return visual('v1', table('v1t', 'Onboarding · Smith Family Medicine', 'blue', 'In progress', rows + prog))
    if i == 2:
        lab = t(11, 1.5, MUTE, 500, '0.08em', 'text-transform: uppercase;')
        rows = trow('v2h', '92px minmax(0, 1fr) auto', p('v2h1', 'Claim No.', css=lab) + p('v2h2', 'Payer', css=lab) + p('v2h3', 'Status', css=lab))
        for j, (no, payer, bt, tn) in enumerate((('CLM-20418', 'Medicare', 'Paid', 'success'), ('CLM-20419', 'Blue Cross', 'Paid', 'success'), ('CLM-20422', 'Aetna', 'Submitted', 'blue'),
                                                 ('CLM-20425', 'UnitedHealthcare', 'Appeal sent', 'warning'), ('CLM-20431', 'Cigna', 'Submitted', 'blue'))):
            rows += trow(f'v2r{j}', '92px minmax(0, 1fr) auto', p(f'v2r{j}n', no, css=t(12.5, 1.45, SLATE, 400, None, 'font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;'))
                         + cell(f'v2r{j}p', payer) + badge(f'v2r{j}b', bt, tn))
        return visual('v2', table('v2t', 'Claims · today', 'neutral', 'Sample', rows))
    bars = ''.join(box(f'v3b{j}', '', css=f'flex-grow: 1; height: {hgt}; border-radius: 6px 6px 2px 2px; background-color: {BLUE if j == 5 else B300};')
                   for j, hgt in enumerate(('48%', '56%', '54%', '66%', '74%', '86%')))
    chart = flex('v3c', bars, css='display: flex; flex-direction: row; align-items: flex-end; gap: 10px; height: 160px; padding: 20px 16px 12px;')
    months = flex('v3m', ''.join(p(f'v3m{j}', m, css=t(11, 1.5, MUTE)) for j, m in enumerate(('Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'))),
                  css='display: flex; flex-direction: row; justify-content: space-between; padding: 0px 16px 14px;')
    tiles = grid('v3s', ''.join(box(f'v3s{j}', p(f'v3s{j}l', a, css=t(11, 1.5, MUTE)) + p(f'v3s{j}v', v, css=t(16, 1.4, INK, 600)),
                                    css='padding: 10px 12px; border-radius: 8px; background-color: #FFFFFF; box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.08);')
                                for j, (a, v) in enumerate((('Clean claims', '98%'), ('Days in A/R', '28'), ('Collection ratio', '96%')))), css=(
        f'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; padding: 12px 16px 16px; background-color: {WASH}; '
        'border-top: 1px solid rgba(3,103,161,0.06);'))
    return visual('v3', table('v3t', 'Collections · last 6 months', 'success', 'On track', chart + months + tiles))


STEPS = [('01', 'Discover', 'Free billing review', 'On your demo we look at your claims, denials and A/R together and show you where revenue is slipping.',
          ['Denial patterns by payer', 'Aged A/R you can still recover', 'Gaps in eligibility and coding']),
         ('02', 'Set up', 'Onboarding and credentialing', 'We connect to your EHR and practice management software, confirm payer enrollments and take over open claims.',
          ['No new software for your staff', 'Payer enrollments checked', 'Open claims picked up from day one']),
         ('03', 'Bill', 'Clean claims, worked denials', 'Certified coders scrub and submit claims, post payments, and work every denial and aged balance.',
          ['98% clean claim rate', 'Every denial appealed or corrected', 'Payments posted and reconciled']),
         ('04', 'Report', 'Reporting you can see into', 'Real-time reports on claims, billing and collections, reviewed with you so nothing is hidden.',
          ['Live claim and payment status', 'Monthly performance reviews', 'A/R kept under 30 days'])]


def steps():
    head = box('st-head', eyebrow('st-e', 'How we work', css='align-self: center;') + h2('st-h2', 'Four steps, no disruption', css='text-align: center;')
               + lead('st-p', 'A structured handover that takes billing off your plate without interrupting daily operations.', css='max-width: 560px; text-align: center;'),
               css='display: flex; flex-direction: column; align-items: center; gap: 16px;')
    cards = ''
    for i, (num, kicker, title, text, items) in enumerate(STEPS):
        txt = box(f'st{i}-l', flex(f'st{i}-k', p(f'st{i}-n', num, css=t(13, 1.5, BLUE, 600))
                                   + box(f'st{i}-ln', '', css=f'width: 24px; height: 1px; background-color: {HAIRS};')
                                   + p(f'st{i}-kk', kicker, css=t(12, 1.5, MUTE, 500, '0.12em', 'text-transform: uppercase;')),
                                   css='display: flex; flex-direction: row; align-items: center; gap: 10px;')
                  + h(f'st{i}-h', 'h3', title, css=t(30, 1.15, INK, 500, '-0.025em', '@media(--tablet_extra){font-size: 26px;} @media(--mobile){font-size: 22px;}'))
                  + p(f'st{i}-p', text, css=t(15, 1.65, SLATE, 400, None, 'max-width: 460px;'))
                  + box(f'st{i}-ul', ''.join(check_item(f'st{i}-li{j}', it) for j, it in enumerate(items)),
                        css='display: flex; flex-direction: column; gap: 8px; margin-top: 8px;'),
                  css='display: flex; flex-direction: column; gap: 12px;')
        cards += grid(f'st{i}', txt + step_visual(i), css=(
            f'position: sticky; top: {108 + 20 * i}px; z-index: {i + 1}; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); '
            f'column-gap: 56px; row-gap: 32px; align-items: center; padding: 48px; border-radius: 24px; background-color: rgba(255,255,255,0.6); {BLUR} '
            'border: 1px solid rgba(255,255,255,0.8); transform-origin: 50% 0%; will-change: transform; '
            f'box-shadow: 0px 0px 0px 1px {HAIR}, inset 0px 1px 0px 0px rgba(255,255,255,0.9), 0px 24px 48px 0px rgba(2,40,66,0.08); '
            '@media(--tablet_extra){column-gap: 40px; padding: 40px;} '
            '@media(--tablet){position: static; grid-template-columns: 1fr;} @media(--mobile){padding: 24px;}'))
    stack = flex('st-stack', cards, cfg={'_cssid': 'lp-stack'}, css='display: flex; flex-direction: column; gap: 24px; padding-bottom: 24px;')
    return section('lp-steps', head + stack)


# ---------------------------------------------------------------- 7. mid CTA
def mid_cta():
    left = box('mc-l', h2('mc-h2', 'Find out what your practice should be collecting', '#FFFFFF', 42, 'line-height: 1.1;')
               + lead('mc-p', 'From a 98% clean claim rate to a 30% drop in A/R, see what changes when we run your billing.', 16, 'rgba(255,255,255,0.9)', 'max-width: 460px;')
               + btn('mc-b', 'Book a free demo', DEMO, 'white', css='margin-top: 8px;'), css=(
        'display: flex; flex-direction: column; justify-content: center; gap: 20px; padding: 64px; @media(--tablet){padding: 48px 40px;} @media(--mobile){padding: 32px 24px;}'))
    right = box('mc-r', img('mc-img', mid_('lp-billing-team-report'), 'position: absolute; top: 0px; left: 0px; display: block; width: 100%; height: 100%; max-width: none; object-fit: cover;',
                            'Billing specialists reviewing a report together'), css='position: relative; min-height: 280px; overflow: hidden;')
    card = grid('mc', left + right, css=(
        f'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0px; align-items: stretch; border-radius: 24px; overflow: hidden; background-image: {GRAD}; '
        '@media(--tablet){grid-template-columns: 1fr;}'))
    return section('lp-mid', card)


# ---------------------------------------------------------------- 8. testimonials
QUOTES = [('JB', 'James Berg', 'Chief Operations Officer, Ion Diagnostics',
           '“Medcare MSO has been and continues to be critical to the success of Ion Diagnostics. Our needs are rooted in compliance and dedicated, responsive '
           'client service. They deliver on both ends and are outstanding in revenue cycle management. Medcare MSO is a true partner.”'),
          ('SS', 'Shobha Solomon', 'CEO, Care Now Clinic',
           '“I am very thankful to Medcare because they rectified all the mistakes which were done by my previous billing partner. They are so fast and efficient.”'),
          ('JA', 'Joshua Arant', 'COO, Mako Medical Laboratories',
           '“Our experience with Medcare MSO is great. They help us to increase our revenue with their quality billing and customer support services. Always recommend them to others.”')]


def testimonials():
    left = box('ts-l', eyebrow('ts-e', 'Client stories') + h2('ts-h2', 'Trusted by 1,200+ practices')
               + lead('ts-p', 'Feedback from practice and lab leaders who moved their billing to MedCare MSO.', css='max-width: 420px;'),
               css='display: flex; flex-direction: column; gap: 16px; position: sticky; top: 120px; @media(--tablet){position: static;}')
    figs = ''
    for i, (ini, name, role, quote) in enumerate(QUOTES):
        avatar = p(f'ts{i}-a', ini, css=t(17.6, 1, BLUE, 600, None, (
            f'display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 44px; height: 44px; border-radius: 999px; '
            f'background-color: {B50}; box-shadow: 0px 0px 0px 1px {HAIR};')))
        cap = box(f'ts{i}-c', p(f'ts{i}-n', name, css=t(15, 1.5, INK, 600)) + p(f'ts{i}-r', role, css=t(13, 1.5, MUTE)), css='display: flex; flex-direction: column;')
        figs += box(f'ts{i}', flex(f'ts{i}-h', avatar + cap, css='display: flex; flex-direction: row; align-items: center; gap: 12px;')
                    + p(f'ts{i}-q', quote, css=t(17 if i == 0 else 15, 1.6 if i == 0 else 1.65, INK)), css=(
            f'display: flex; flex-direction: column; gap: 24px; padding: 28px; background-color: #FFFFFF; border-radius: 16px; box-shadow: {SH_SM}; '
            f'transition: transform 0.25s ease, box-shadow 0.25s ease; &:hover{{transform: translateY(-3px); box-shadow: {SH_MD};}} '
            + ('grid-column: 1 / -1; ' if i == 0 else '') + '@media(--mobile){padding: 24px;}'))
    right = grid('ts-g', figs, css=('display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; '
                                    '@media(--mobile){grid-template-columns: 1fr;}'))
    g = grid('ts', left + right, css=('display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 64px; row-gap: 40px; align-items: start; '
                                      '@media(--tablet){grid-template-columns: 1fr;}'))
    return section('lp-testimonials', g)


# ---------------------------------------------------------------- 9. contact
def contact():
    items = grid('ct-ul', ''.join(glass_item(f'ct-li{j}', s) for j, s in enumerate(('Review claims and denials', 'Look at your aged A/R', 'Check your payer mix', 'Give you a clear quote'))),
                 css='display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; @media(--mobile){grid-template-columns: 1fr;}')
    left = box('ct-l', p('ct-e', 'Free demo', css=t(12, 1.5, B300, 500, '0.12em', 'text-transform: uppercase;'))
               + h2('ct-h2', 'Let’s talk about your billing', '#FFFFFF', 48, 'line-height: 1.06; letter-spacing: -0.04em;')
               + lead('ct-p', 'A focused conversation with a billing specialist. No pitch deck, no obligation.', 17, 'rgba(255,255,255,0.9)', 'max-width: 460px;')
               + p('ct-on', 'On your demo we will:', css=t(13, 1.5, '#FFFFFF', 500, None, 'margin-top: 4px;')) + items
               + box('ct-ph', p('ct-ph1', 'Prefer to talk now?', css=t(13, 1.5, 'rgba(255,255,255,0.86)'))
                     + p('ct-ph2', f'<a href="{TEL}">{PHONE}</a>', css=t(24, 1.3, '#FFFFFF', 500, '-0.02em', (
                         '& a{color: #FFFFFF; text-decoration: none;} & a:hover{text-decoration: underline; text-underline-offset: 4px;}'))),
                     css='display: flex; flex-direction: column; gap: 4px; margin-top: 8px;'),
               css='display: flex; flex-direction: column; gap: 20px;')
    right = box('ct-form', form('lpc-', heading=False), css=f'background-color: #FFFFFF; border-radius: 16px; box-shadow: {SH_LG}; padding: 32px; @media(--mobile){{padding: 24px;}}')
    card = grid('ct', left + right, css=(
        f'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 64px; row-gap: 32px; align-items: center; padding: 72px; '
        f'border-radius: 24px; background-image: {GRAD}; '
        '@media(--tablet_extra){padding: 56px; column-gap: 48px;} @media(--tablet){grid-template-columns: 1fr; padding: 48px 40px;} @media(--mobile){padding: 32px 24px;}'))
    # design's mobile sticky bar (shown by the helper script after 640px of scroll on phones)
    sticky = grid('lp-sticky-bar', box('sb-call', '', link=TEL, css=(
        f'display: flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 999px; background-color: #FFFFFF; {RING} '
        f"&::after{{content: \"\"; width: 20px; height: 20px; background-repeat: no-repeat; background-size: 20px 20px; background-image: url('{SVG_PHONE}');}}"))
        + btn('sb-b', 'Book a free demo', DEMO, css='width: 100%;'), css=(
        'display: none; position: fixed; left: 0px; right: 0px; bottom: 0px; z-index: 60; grid-template-columns: auto minmax(0, 1fr); gap: 10px; '
        f'padding: 12px 16px; background-color: rgba(255,255,255,0.82); {BLUR} box-shadow: 0px -1px 0px 0px {HAIR}, 0px -8px 24px 0px rgba(2,40,66,0.06); '
        f'transform: translateY(110%); transition: transform 0.28s {EASE}; &[data-on="1"]{{transform: translateY(0%);}} '
        '@media(--mobile){display: grid;}'), anchor='lp-sticky')
    return section('lp-contact', card + sticky, css='padding-block-end: 104px; @media(--tablet){padding-block-end: 80px;} @media(--mobile){padding-block-end: 96px;}')


SECTIONS = [hero, about, services, why, specialties, steps, mid_cta, testimonials, contact]
PAGE_BG = ('background-color: #FBFDFE; background-image: '
           'radial-gradient(900px 760px at 0% 2%, #E3FBFE 0%, rgba(227,251,254,0) 70%), radial-gradient(820px 700px at 96% 0%, #FDF8CB 0%, rgba(253,248,203,0) 70%), '
           'radial-gradient(760px 640px at 100% 11%, #EAFBE5 0%, rgba(234,251,229,0) 70%), radial-gradient(700px 620px at 18% 17%, #FDF8CB 0%, rgba(253,248,203,0) 68%), '
           'radial-gradient(880px 720px at 92% 24%, #E3FBFE 0%, rgba(227,251,254,0) 70%), radial-gradient(760px 660px at 4% 31%, #EAFBE5 0%, rgba(234,251,229,0) 70%), '
           'radial-gradient(640px 560px at 60% 37%, #FDF8CB 0%, rgba(253,248,203,0) 68%), radial-gradient(860px 700px at 100% 44%, #EAFBE5 0%, rgba(234,251,229,0) 70%), '
           'radial-gradient(820px 700px at 0% 50%, #E3FBFE 0%, rgba(227,251,254,0) 70%), radial-gradient(700px 600px at 78% 57%, #FDF8CB 0%, rgba(253,248,203,0) 68%), '
           'radial-gradient(760px 640px at 12% 64%, #FDF8CB 0%, rgba(253,248,203,0) 68%), radial-gradient(900px 740px at 98% 70%, #E3FBFE 0%, rgba(227,251,254,0) 70%), '
           'radial-gradient(720px 620px at 40% 77%, #EAFBE5 0%, rgba(234,251,229,0) 70%), radial-gradient(820px 700px at 0% 84%, #E3FBFE 0%, rgba(227,251,254,0) 70%), '
           'radial-gradient(760px 660px at 100% 90%, #FDF8CB 0%, rgba(253,248,203,0) 70%), radial-gradient(880px 720px at 22% 99%, #EAFBE5 0%, rgba(234,251,229,0) 70%);')


def payload(mode='replace_children', dry=False):
    global b
    b = B()
    xml = flex('lp-page', ''.join(f() for f in SECTIONS), css=(
        f'display: flex; flex-direction: column; align-items: stretch; gap: 0px; width: 100%; overflow-x: clip; {F} color: {SLATE}; {PAGE_BG}'))
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes, 'mode': mode, 'dry_run': dry}


if __name__ == '__main__':
    d = payload()
    print(len(json.dumps(d)), 'bytes', len(d['style']), 'styled elements')
