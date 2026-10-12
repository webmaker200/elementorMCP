"""Salus AI page (WP page 410964) built from Figma 626:2408 with Elementor V4 atomic elements.

All styling is page-local (Figma values). Section backdrops are the Figma blurred-ellipse
composite, rendered per section and set through the native background-image control.
"""
import json
import re
from build_helper import B

PID = 410964
MEDIA = json.load(open('salus/media.json'))
DEMO = 'https://medcaremso.com/request-demo/?utm_source=salus-ai'
F = 'font-family: var(--Poppins);'
GLASS = 'backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);'
SH = 'box-shadow: 0px 15px 15px 0px rgba(194,194,194,0.1);'


def pfix(css):
    """Site CSS has p{margin-block-end:0 !important}; express paragraph bottom spacing as padding."""
    assert 'border' not in css or 'margin: 0px;' in css or not re.search(r'margin: \S+ \S+ (?!0px)\S+ \S+;', css), css
    return re.sub(r'margin: (\S+) (\S+) (\S+) (\S+);', lambda m: f'margin: {m[1]} {m[2]} 0px {m[4]}; padding-block-end: {m[3]};' if m[3] != '0px' else m[0], css)


def mid(n):
    return MEDIA[n]['id']


def bgurl(n):
    return MEDIA[n]['url']


def img(n, alt=''):
    return {'src': {'id': mid(n), 'alt': alt}, 'size': 'full'}


def scale(v, f):
    return max(int(round(v * f)), 0)


def section(b, cid, kids, bg, pt, pb, extra='', attrs=None):
    css = (f"display: flex; flex-direction: column; align-items: center; gap: 0px; width: 100%; "
           f"padding: {pt}px 53px {pb}px 53px; background-color: #ffffff; "
           f"background-image: url('{bgurl(bg)}'); background-size: 100% 100%; background-repeat: no-repeat; "
           f"overflow: hidden; position: relative; {extra}"
           f"@media(--laptop){{padding: {scale(pt, .8)}px 40px {scale(pb, .8)}px 40px;}} "
           f"@media(--tablet){{padding: {scale(pt, .65)}px 30px {scale(pb, .65)}px 30px;}} "
           f"@media(--mobile){{padding: {scale(pt, .5)}px 16px {scale(pb, .5)}px 16px;}}")
    cfg = {'tag': 'section'}
    if attrs:
        cfg['attributes'] = attrs
    return b.el('e-flexbox', cid, kids, cfg=cfg, css=css)


def pill(b, cid, text, mb=32):
    css = (f"{F} font-size: 12px; line-height: 14.4px; font-weight: 400; color: #7D7D7D; text-align: center; "
           f"display: flex; align-items: center; justify-content: center; width: 248px; max-width: 100%; height: 46px; "
           f"margin: 0px; padding: 0px 16px; border-radius: 34px; border: 1px solid #9ACAA1; "
           f"background-color: rgba(255,255,255,0.1); {SH} {GLASS}")
    return b.el('e-paragraph', cid, cfg={'paragraph': text}, css=css)


def h2(b, cid, text, mb=13, maxw=1428, mt=32):
    css = (f"{F} font-size: 58px; line-height: 82px; font-weight: 400; letter-spacing: -1.16px; color: #000000; "
           f"text-align: center; max-width: {maxw}px; margin: {mt}px 0px {mb}px 0px; "
           f"@media(--laptop){{font-size: 48px; line-height: 64px;}} "
           f"@media(--tablet_extra){{font-size: 42px; line-height: 56px;}} "
           f"@media(--tablet){{font-size: 38px; line-height: 50px; letter-spacing: -0.76px;}} "
           f"@media(--mobile){{font-size: 30px; line-height: 40px; letter-spacing: -0.6px; margin: 20px 0px 10px 0px;}}")
    return b.el('e-heading', cid, cfg={'tag': 'h2', 'title': text}, css=css)


def sub(b, cid, text, mb, color='#000000', maxw=1027):
    css = (f"{F} font-size: 16px; line-height: 32px; font-weight: 400; color: {color}; text-align: center; "
           f"max-width: {maxw}px; margin: 0px 0px {mb}px 0px; "
           f"@media(--laptop){{margin: 0px 0px {scale(mb, .8)}px 0px;}} "
           f"@media(--tablet){{margin: 0px 0px {scale(mb, .7)}px 0px;}} "
           f"@media(--mobile){{font-size: 15px; line-height: 28px; margin: 0px 0px 32px 0px;}}")
    return b.el('e-paragraph', cid, cfg={'paragraph': text}, css=pfix(css))


def para(b, cid, text, css):
    return b.el('e-paragraph', cid, cfg={'paragraph': text}, css=pfix(F + ' ' + css))


def image(b, cid, name, css, alt=''):
    return b.el('e-image', cid, cfg={'image': img(name, alt)}, css=css)


def circle_arrow(b, cid, arrow):
    k = image(b, cid + 'i', arrow, 'width: 24px; height: 24px; display: block;')
    return b.el('e-div-block', cid, k, css=('display: flex; align-items: center; justify-content: center; '
                                            'width: 39px; height: 39px; flex-shrink: 0; padding: 8px; '
                                            'border-radius: 41px; background-color: #FFFFFF;'))


def pill_button(b, cid, text, url, arrow='arrow-blue', css='', text_color='#000000'):
    k = para(b, cid + 't', text, f'font-size: 14px; line-height: 19.6px; font-weight: 500; color: {text_color}; margin: 0px;')
    k += circle_arrow(b, cid + 'c', arrow)
    cfg = {'tag': 'a', 'link': {'destination': url}} if url else {'tag': 'div'}
    base = ('display: flex; flex-direction: row; align-items: center; gap: 14px; height: 56px; width: max-content; flex-shrink: 0; '
            'padding: 0px 9px 0px 26px; border-radius: 61px; border: 1px solid #B8DBD4; '
            f'background-color: rgba(119,179,229,0.2); {GLASS} text-decoration: none; ')
    return b.el('e-flexbox', cid, k, cfg=cfg, css=base + css)


# ---------------------------------------------------------------- A. Hero
def hero(b):
    av = ''
    for i in (1, 2, 3):
        ml = '0px' if i == 1 else '-12px'
        av += image(b, f'hp-a{i}', f'avatar-{i}', ('width: 35px; height: 35px; object-fit: cover; border-radius: 50%; '
                                                   f'border: 1.5px solid #FFFFFF; margin: 0px 0px 0px {ml};'))
    av += para(b, 'hp-t', 'AI-Powered healthcare', 'font-size: 12px; line-height: 14.4px; color: #7D7D7D; margin: 0px 0px 0px 11px;')
    k = b.el('e-flexbox', 'hp', av, css=('display: flex; width: max-content; align-items: center; gap: 0px; height: 46px; '
                                         'padding: 0px 15px 0px 11px; border-radius: 31px; border: 1px solid #7EB63E; '
                                         f'background-color: rgba(255,255,255,0.1); {GLASS} margin: 0px 0px 25px 0px; align-self: flex-start; '
                                         '@media(--tablet){align-self: center;}'))
    k += b.el('e-heading', 'h1', cfg={'tag': 'h1', 'title': 'Give all your time to patients, Salus AI will make the notes'},
              css=(f"{F} font-size: 72px; line-height: 88px; font-weight: 400; letter-spacing: -1.44px; color: #000000; "
                   "max-width: 665px; margin: 0px 0px 23px 0px; "
                   "@media(--laptop){font-size: 60px; line-height: 74px; letter-spacing: -1.2px;} "
                   "@media(--tablet_extra){font-size: 50px; line-height: 62px; letter-spacing: -1px;} "
                   "@media(--tablet){font-size: 46px; line-height: 58px; max-width: 760px;} "
                   "@media(--mobile){font-size: 34px; line-height: 44px; letter-spacing: -0.68px; margin: 0px 0px 16px 0px;}"))
    k += para(b, 'hero-p', ("Before the patient reaches the door, Salus AI has already finished the clinical note and suggested the codes. "
                            "You review and sign. You do not need to find time for patients, you own the entire clock now."),
              ('font-size: 16px; line-height: 32px; color: #4F4F4F; max-width: 595px; margin: 0px 0px 43px 0px; '
               '@media(--tablet){max-width: 680px;} @media(--mobile){font-size: 15px; line-height: 28px; margin: 0px 0px 28px 0px;}'))
    btns = pill_button(b, 'hero-b1', 'Explore AI Ecosystem', None)
    vp = para(b, 'hero-b2t', 'View Pricing', 'font-size: 14px; line-height: 19.6px; font-weight: 500; color: #000000; margin: 0px;')
    vp += image(b, 'hero-b2i', 'arrow-black', 'width: 24px; height: 24px; display: block;')
    btns += b.el('e-flexbox', 'hero-b2', vp, cfg={'tag': 'a', 'link': {'destination': '#pricing'}},
                 css='display: flex; width: max-content; align-items: center; gap: 11px; padding: 0px; text-decoration: none;')
    k += b.el('e-flexbox', 'hero-btns', btns, css=('display: flex; flex-wrap: wrap; align-items: center; gap: 20px 47px; padding: 0px; @media(--tablet){justify-content: center;} '
                                                  '@media(--mobile){gap: 16px 28px;}'))
    left = b.el('e-flexbox', 'hero-l', k, css=('display: flex; flex-direction: column; align-items: flex-start; padding: 0px; '
                                               'flex: 0 1 665px; min-width: 0px; '
                                               '@media(--tablet){flex: 0 1 auto; width: 100%; align-items: center; text-align: center;}'))

    def float_card(cid, label, value, icon, tile_bg, label_color, bg, pos):
        t = image(b, cid + 'ii', icon, 'width: 15px; height: 15px; display: block;')
        tile = b.el('e-div-block', cid + 'i', t, css=(f'display: flex; align-items: center; justify-content: center; width: 30px; height: 30px; '
                                                      f'flex-shrink: 0; padding: 0px; border-radius: 9px; background-color: {tile_bg};'))
        tx = para(b, cid + 'l', label, (f'font-size: 9px; line-height: 13.5px; font-weight: 600; letter-spacing: 0.9px; '
                                        f'text-transform: uppercase; color: {label_color}; margin: 0px 0px 2px 0px; white-space: nowrap;'))
        tx += para(b, cid + 'v', value, 'font-size: 21px; line-height: 21px; font-weight: 500; color: #07182D; margin: 0px; white-space: nowrap;')
        txt = b.el('e-div-block', cid + 'x', tx, css='display: flex; flex-direction: column; padding: 0px;')
        return b.el('e-flexbox', cid, tile + txt, css=(
            'display: flex; flex-direction: row; align-items: center; gap: 8px; padding: 10px 14px; width: max-content; '
            f'border-radius: 16px; border: 0.8px solid rgba(255,255,255,0.8); background-color: {bg}; '
            f'box-shadow: 0px 10px 30px 0px rgba(168,168,168,0.25); {GLASS} position: absolute; z-index: 2; {pos}'))

    vis = image(b, 'dash', 'dashboard', ('width: 100%; height: auto; display: block; border-radius: 6px; '
                                         'box-shadow: 0px 30px 30px 0px rgba(142,142,142,0.15);'),
                alt='Salus AI clinical documentation dashboard')
    vis += float_card('fc1', 'STT Accuracy', '93%', 'icon-stt', 'rgba(0,102,255,0.1)', '#455873', 'rgba(255,255,255,0.2)',
                      'inset-inline-start: -69px; inset-block-start: 97.8%; '
                      '@media(--tablet_extra){inset-inline-start: -24px; inset-block-start: auto; inset-block-end: 5%;} @media(--tablet){inset-inline-start: -16px;} '
                      '@media(--mobile){inset-inline-start: -6px; inset-block-start: auto; inset-block-end: -30px;}')
    vis += float_card('fc2', 'Note Ready In', '90 sec', 'icon-bolt', 'rgba(112,221,177,0.14)', '#94A3B8', 'rgba(255,255,255,0.1)',
                      'inset-inline-end: 10.9%; inset-block-start: -45px; @media(--mobile){inset-block-start: -36px; inset-inline-end: 4%;}')
    wrap = b.el('e-div-block', 'dash-w', vis, css='position: relative; width: 100%; padding: 0px;')
    chips = ''
    for i, (v, l, bg) in enumerate([('93%', 'STT Accuracy', 'rgba(192,227,245,0.1)'), ('4 hrs', 'Saved Per Day', 'rgba(217,201,255,0.1)'),
                                    ('10+', 'Note Templates', 'rgba(221,255,178,0.1)'), ('$99', 'From/Provider/Mo', 'rgba(255,233,197,0.1)')]):
        c = para(b, f'ch{i}v', v, 'font-size: 19.6px; line-height: 22px; color: #000000; margin: 0px;')
        c += para(b, f'ch{i}l', l, 'font-size: 9.8px; line-height: 26px; color: #4F4F4F; margin: 0px; white-space: nowrap;')
        chips += b.el('e-div-block', f'ch{i}', c, css=(
            f'display: flex; flex-direction: column; width: 125px; height: 70px; padding: 14px 8px 8px 18px; border-radius: 16.3px; '
            f'background-color: {bg}; box-shadow: 0px 12px 12px 0px rgba(194,194,194,0.1); {GLASS} '
            '@media(--tablet_extra){width: auto; flex: 1 1 0px; min-width: 0px; padding: 14px 6px 8px 14px;} '
            '@media(--mobile){flex: 1 1 calc(50% - 4px);}'))
    chiprow = b.el('e-flexbox', 'chips', chips, css=('display: flex; flex-direction: row; justify-content: flex-end; gap: 7px; '
                                                    'padding: 0px; margin: 18px 0px 0px 0px; width: 100%; '
                                                    '@media(--tablet){justify-content: center;} '
                                                    '@media(--mobile){flex-wrap: wrap; gap: 8px; margin: 46px 0px 0px 0px;}'))
    right = b.el('e-flexbox', 'hero-r', wrap + chiprow, css=(
        'display: flex; flex-direction: column; padding: 0px; flex: 0 1 744px; min-width: 0px; margin: 128px 0px 0px 0px; '
        '@media(--laptop){margin: 110px 0px 0px 0px;} '
        '@media(--tablet){flex: 0 1 auto; width: 100%; max-width: 744px; margin: 70px 0px 0px 0px;} '
        '@media(--mobile){margin: 56px 0px 0px 0px;}'))
    row = b.el('e-flexbox', 'hero-row', left + right, css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 40px; '
        'width: 100%; max-width: 1516px; padding: 0px; '
        '@media(--tablet){flex-direction: column; align-items: center; gap: 0px;}'))
    return section(b, 'sa', row, 'bg-hero', 89, 113)


# ---------------------------------------------------------------- B. See it work
def see(b):
    k = pill(b, 'sb-pill', 'See It Work')
    k += h2(b, 'sb-h2', 'Turn entire conversations into note within moments', 16, mt=33)
    k += sub(b, 'sb-sub', 'From conversation to signed-ready notes, Salus AI structures the SOAP note and lines up the codes for review.', 55, '#4F4F4F', 800)
    k += mockup(b)
    panel = b.el('e-flexbox', 'sb-panel', k, css=(
        'display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 1814px; '
        f'padding: 54px 40px 79px 40px; border-radius: 20px; background-color: rgba(255,255,255,0.3); {GLASS} '
        '@media(--laptop){padding: 48px 32px 64px 32px;} @media(--tablet){padding: 40px 24px 48px 24px;} '
        '@media(--mobile){padding: 32px 14px 32px 14px;}'))
    return section(b, 'sb', panel, 'bg-see', 113, 72)


# ---------------------------------------------------------------- B mockup (native: listening card + SOAP note card)
def mockup(b):
    # left: AI listening card
    t = para(b, 'mk-lt', 'AI Listening', 'font-size: 18px; line-height: 18px; font-weight: 500; color: #07182D; margin: 0px;')
    t += para(b, 'mk-ls', 'Ambient capture · encrypted', 'font-size: 12px; line-height: 18px; color: #94A3B8; margin: 0px; padding: 3px 0px 0px 0px;')
    head = image(b, 'mk-lg', 'logo-mark', 'width: 33px; height: 43px; flex-shrink: 0; display: block;')
    head += b.el('e-div-block', 'mk-lh', t, css='display: flex; flex-direction: column; padding: 0px; min-width: 0px;')
    head += para(b, 'mk-live', 'Live', ('font-size: 11px; line-height: 16.5px; font-weight: 600; color: #144AE0; margin: 0px 0px 0px auto; '
                                        'padding: 0px 0px 0px 13px; flex-shrink: 0; '
                                        'background-image: radial-gradient(circle at 3.5px 50%, #144AE0 3px, rgba(20,74,224,0) 4px);'))
    c = b.el('e-flexbox', 'mk-lhead', head, css='display: flex; flex-direction: row; align-items: center; gap: 10px; padding: 0px; width: 100%;')
    c += image(b, 'mk-wave', 'wave', 'width: 100%; height: auto; display: block; margin: 22px 0px 0px 0px;',
               alt='Live audio waveform')
    bub = ''
    for i, (who, said) in enumerate([('Dr. Reyes', '"Any chest pain or shortness of breath?"'), ('Patient', '"Just the cough, worse at night."')]):
        x = para(b, f'mk-b{i}w', who, 'font-size: 11px; line-height: 16.5px; font-weight: 700; letter-spacing: 0.11px; color: #144AE0; margin: 0px;')
        x += para(b, f'mk-b{i}t', said, 'font-size: 12.5px; line-height: 18.8px; color: #475569; margin: 0px; padding: 4px 0px 0px 0px;')
        bub += b.el('e-div-block', f'mk-b{i}', x, css=('display: flex; flex-direction: column; padding: 10px 14px; border-radius: 12px; '
                                                       'border: 0.8px solid rgba(0,102,255,0.09); background-color: rgba(0,102,255,0.04);'))
    c += b.el('e-flexbox', 'mk-bubs', bub, css='display: flex; flex-direction: column; gap: 10px; padding: 20px 0px 0px 0px; width: 100%;')
    lcard = b.el('e-flexbox', 'mk-lcard', c, css=(
        'display: flex; flex-direction: column; width: 100%; max-width: 531px; padding: 26px; border-radius: 20px; '
        'border: 0.8px solid rgba(255,255,255,0.9); background-color: rgba(255,255,255,0.78); '
        'backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); '
        'box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.95), 0px 12px 40px 0px rgba(0,102,255,0.1); '
        '@media(--mobile){padding: 18px;}'))
    left = b.el('e-flexbox', 'mk-left', lcard, css=(
        'display: flex; align-items: center; justify-content: center; flex: 1 1 50%; min-width: 0px; padding: 60px 56px 60px 40px; '
        f"background-color: #FFFFFF; background-image: url('{bgurl('see-left-bg')}'); background-size: cover; background-position: center center; "
        '@media(--laptop){padding: 48px 48px 48px 32px;} @media(--tablet){flex: 1 1 auto; width: 100%; padding: 40px 24px 72px 24px;} '
        '@media(--mobile){padding: 24px 12px 64px 12px;}'))

    # right: clinical documentation card
    tile_ = b.el('e-div-block', 'mk-dk', image(b, 'mk-dki', 'icon-doc', 'width: 24px; height: 24px; display: block;'), css=(
        'display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; flex-shrink: 0; padding: 0px; '
        'border-radius: 13px; background-color: rgba(0,102,255,0.1);'))
    t = para(b, 'mk-dt', 'Clinical Documentation', 'font-size: 16px; line-height: 22.5px; font-weight: 500; color: #07182D; margin: 0px;')
    t += para(b, 'mk-ds', 'SOAP · auto-structured', 'font-size: 12px; line-height: 18px; color: #94A3B8; margin: 0px;')
    head = tile_ + b.el('e-div-block', 'mk-dh', t, css='display: flex; flex-direction: column; padding: 0px; min-width: 0px; flex: 1 1 auto;')
    head += para(b, 'mk-ready', 'Ready for review', ('font-size: 11px; line-height: 16.5px; font-weight: 700; color: #0D9E6E; margin: 0px 0px 0px auto; '
                                                     'padding: 4px 11px; border-radius: 999px; background-color: rgba(112,221,177,0.1); white-space: nowrap; flex-shrink: 0;'))
    c = b.el('e-flexbox', 'mk-dhead', head, css='display: flex; flex-direction: row; align-items: center; gap: 10px; padding: 0px; width: 100%;')
    soap = [('Subjective', '52M, 3-day productive cough with nocturnal worsening. No dyspnea or chest pain reported.'),
            ('Objective', 'Afebrile. Lungs: scattered rhonchi, clears with cough. SpO₂ 98% RA.'),
            ('Assessment', 'Acute bronchitis, likely viral.'),
            ('Plan', 'Symptomatic management, hydration, cough suppressant. Return precautions reviewed.')]
    for i, (lab, txt) in enumerate(soap):
        x = para(b, f'mk-s{i}l', lab, 'font-size: 11.5px; line-height: 17.2px; font-weight: 500; letter-spacing: 0.46px; color: #0A4BC2; margin: 0px;')
        x += para(b, f'mk-s{i}t', txt, 'font-size: 13px; line-height: 20.1px; color: #475569; margin: 0px; padding: 4px 0px 0px 0px;')
        c += b.el('e-div-block', f'mk-s{i}', x, css=(
            f"display: flex; flex-direction: column; width: 100%; padding: 0px 0px 13px 0px; margin: {20 if i == 0 else 13}px 0px 0px 0px; "
            'border-style: solid; border-color: rgba(7,24,45,0.08); border-width: 0px 0px 1px 0px;'))
    c += para(b, 'mk-cl', 'SUGGESTED CODES', 'font-size: 11px; line-height: 16.5px; font-weight: 600; color: #94A3B8; margin: 13px 0px 0px 0px;')
    chips = ''
    for i, code in enumerate(['J20.9 · Acute bronchitis', '99214 · E/M', 'ICD-10 verified']):
        x = image(b, f'mk-c{i}i', 'check-mint', 'width: 13px; height: 13px; flex-shrink: 0; display: block;')
        x += para(b, f'mk-c{i}t', code, 'font-size: 12px; line-height: 18px; font-weight: 600; color: #0A4BC2; margin: 0px; white-space: nowrap;')
        chips += b.el('e-flexbox', f'mk-c{i}', x, css=('display: flex; flex-direction: row; align-items: center; gap: 6px; padding: 5px 11px; width: max-content; '
                                                       'border-radius: 9px; border: 0.8px solid rgba(0,102,255,0.15); background-color: rgba(0,102,255,0.05);'))
    c += b.el('e-flexbox', 'mk-codes', chips, css='display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px; padding: 8px 0px 0px 0px; width: 100%;')
    rcard = b.el('e-flexbox', 'mk-rcard', c, css=(
        'display: flex; flex-direction: column; width: 100%; max-width: 531px; padding: 26px; border-radius: 20px; '
        'border: 0.8px solid rgba(7,24,45,0.08); background-color: #FFFFFF; position: relative; z-index: 1; '
        '@media(--mobile){padding: 18px;}'))
    logo = image(b, 'mk-logo', 'logo-3d', (
        'width: 92px; height: 91px; display: block; position: absolute; z-index: 3; inset-inline-start: 0px; inset-block-start: 50%; '
        'transform: translate(-50%, -50%); border-radius: 50%; '
        'box-shadow: 0px 0px 0px 18px rgba(245,248,255,0.12), 0px 0px 22px 18px rgba(17,43,177,0.1); '
        '@media(--tablet){inset-inline-start: 50%; inset-block-start: 0px;} '
        '@media(--mobile){width: 72px; height: 71px; box-shadow: 0px 0px 0px 12px rgba(245,248,255,0.12), 0px 0px 18px 12px rgba(17,43,177,0.1);}'),
        alt='Salus AI')
    right = b.el('e-flexbox', 'mk-right', rcard + logo, css=(
        'display: flex; align-items: center; justify-content: center; flex: 1 1 50%; min-width: 0px; padding: 60px 40px 60px 56px; position: relative; '
        'background-color: #144AE0; background-image: radial-gradient(circle at 50% 50%, #3A68E8 0%, #144AE0 62%); '
        '@media(--laptop){padding: 48px 32px 48px 48px;} @media(--tablet){flex: 1 1 auto; width: 100%; padding: 72px 24px 40px 24px;} '
        '@media(--mobile){padding: 64px 12px 24px 12px;}'))
    return b.el('e-flexbox', 'mk', left + right, css=(
        'display: flex; flex-direction: row; align-items: stretch; width: 100%; max-width: 1476px; min-height: 666px; padding: 0px; '
        'border-radius: 30px; overflow: hidden; '
        '@media(--laptop){min-height: 0px;} @media(--tablet){flex-direction: column;} @media(--mobile){border-radius: 16px;}'))


# ---------------------------------------------------------------- C. What Salus does
def tile(b, cid, icon, size, icon_px):
    t = image(b, cid + 'i', icon, f'width: {icon_px}px; height: {icon_px}px; display: block;')
    return b.el('e-div-block', cid, t, css=(
        f'display: flex; align-items: center; justify-content: center; width: {size}px; height: {size}px; flex-shrink: 0; '
        'padding: 0px; border-radius: 18.6px; border: 1.86px solid #EAEEF8; background-color: #FFFFFF; '
        'box-shadow: 0px 15px 37px 0px rgba(170,177,202,0.25);'))


def does(b):
    k = pill(b, 'sc-pill', 'What Salus Does')
    k += h2(b, 'sc-h2', 'Everything Salus AI does, from the first word to the last code')
    k += sub(b, 'sc-sub', ('No new hardware and nothing to press, Salus AI works during the visit you were already having. Built by billers, coders, '
                         'and engineers who know what a finished note should carry.'), 59)
    cards = [
        ('icon-voice', 36, 'Ambient Recording', 'Captures every word of the encounter automatically — no button-pressing, no workflow disruption.'),
        ('icon-edit', 30, 'Auto-Generated Notes', 'SOAP, H&P, Telemed, Procedure, Progress, Emergency, and Discharge notes — structured and ready to sign.'),
        ('icon-ai', 32, 'AI-Assisted Coding', 'ICD-10, SNOMED, LOINC, RxNorm codes on Pro — plus CPT and Modifiers on Ultimate. Coverage scales with your plan.'),
        ('icon-shield', 34, 'HIPAA by Design', 'PHI redaction, full audit trail, and zero audio retention — compliance is built into the architecture, not bolted on.'),
        ('icon-translate', 34, 'Multi-Language Support', 'English multi-accent on Basic. Spanish + 4 more on Pro. Full 10-language support on Ultimate.'),
        ('icon-settings', 34, 'Works Everywhere', 'Mobile-responsive web app — ambient, dictation, and audio upload modes across any device or setting.'),
    ]
    g = ''
    for i, (ic, px, t, p) in enumerate(cards):
        head = tile(b, f'sc{i}k', ic, 68, px)
        head += b.el('e-heading', f'sc{i}t', cfg={'tag': 'h3', 'title': t}, css=(
            f'{F} font-size: 32px; line-height: 36px; font-weight: 400; color: #000000; max-width: 267px; margin: 0px; '
            '@media(--laptop){font-size: 28px; line-height: 34px;} @media(--mobile){font-size: 24px; line-height: 30px;}'))
        c = b.el('e-flexbox', f'sc{i}h', head, css='display: flex; flex-direction: row; align-items: center; gap: 24px; padding: 0px; margin: 0px 0px 25px 0px;')
        c += para(b, f'sc{i}p', p, 'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px; '
                                   '@media(--mobile){font-size: 15px; line-height: 28px;}')
        g += b.el('e-flexbox', f'sc{i}', c, css=(
            'display: flex; flex-direction: column; align-items: flex-start; padding: 46px 32px 37px 29px; border-radius: 20px; '
            f'background-color: rgba(255,255,255,0.4); {SH} {GLASS} '
            '@media(--laptop){padding: 36px 26px 32px 26px;} @media(--mobile){padding: 28px 20px 28px 20px;}'))
    k += b.el('e-div-block', 'sc-grid', g, css=(
        'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; width: 100%; max-width: 1478px; padding: 0px; '
        '@media(--laptop){gap: 20px;} @media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} '
        '@media(--mobile){grid-template-columns: minmax(0, 1fr); gap: 16px;}'))
    return section(b, 'sc', k, 'bg-does', 73, 104)


# ---------------------------------------------------------------- D. Pricing
def pricing(b):
    k = pill(b, 'sd-pill', 'Pricing & Plans')
    k += h2(b, 'sd-h2', 'Three plans. Built for every practice size.')
    k += sub(b, 'sd-sub', 'All plans include onboarding, HIPAA compliance, and full Medcare MSO support.', 44)
    plans = [
        ('basic', 'Basic', 'Individual use', '$99/mo', '200 notes · English multi-accent · 1 pre-enrolled speaker',
         ['Real-time 93% STT transcription', 'SOAP, H&P, Telemed, Procedure & more', 'ICD-10 and SNOMED code suggestions',
          'HIPAA-compliant PHI redaction + audit trail', 'Ambient, dictation & audio upload modes']),
        ('pro', 'Pro', 'Small teams · 3–5 providers', '$199/mo', '400 notes · 5 languages · Up to 3 enrolled speakers',
         ['Everything in Basic', 'Customizable templates with drag & drop and voice commands', 'ICD-10, SNOMED, LOINC + RxNorm code suggestions',
          'Timestamped transcript linking', 'Pre-visit patient summary per encounter']),
        ('ult', 'Ultimate', 'Enterprise · multiple providers', '$249/mo', '500 notes · 10 languages · Unlimited enrolled speakers',
         ['Everything in Pro', 'Unlimited speaker diarization', 'Multiple audio uploads per encounter', 'Adaptive doctor style learning',
          'CPT + modifier code suggestions']),
    ]
    cards = ''
    for key, name, tag, price, summ, items in plans:
        pro = key == 'pro'
        p = f'sd-{key}'
        c = b.el('e-heading', p + 't', cfg={'tag': 'h3', 'title': name}, css=(
            f"{F} font-size: 32px; line-height: 36px; font-weight: 400; color: {'#0A4BC2' if pro else '#000000'}; margin: 0px 0px 5px 0px; "
            '@media(--mobile){font-size: 28px; line-height: 34px;}'))
        c += para(b, p + 'g', tag, 'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px 0px 53px 0px; @media(--laptop){margin: 0px 0px 36px 0px;}')
        c += para(b, p + 'pr', price, 'font-size: 62px; line-height: 65px; color: #000000; margin: 0px 0px 6px 0px; '
                                      '@media(--laptop){font-size: 52px; line-height: 58px;} @media(--mobile){font-size: 44px; line-height: 50px;}')
        c += para(b, p + 'pp', 'per provider', 'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px 0px 27px 0px;')
        c += para(b, p + 's', summ, 'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px 0px 49px 0px; @media(--laptop){margin: 0px 0px 32px 0px;}')
        bcss = 'width: 100%; justify-content: center; position: relative; padding: 0px 56px 0px 56px; '
        if pro:
            bcss += 'background-color: #144AE0; border: 1px solid #144AE0;'
        btn = pill_button(b, p + 'b', 'Get Started', DEMO, 'arrow-pro' if pro else 'arrow-btn', bcss, '#FFFFFF' if pro else '#000000')
        c += btn
        li = ''
        for j, it in enumerate(items):
            r = image(b, f'{p}l{j}i', 'icon-check-gray', 'width: 24px; height: 24px; flex-shrink: 0; display: block; margin: 4px 0px 0px 0px;')
            r += para(b, f'{p}l{j}t', it, 'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px; '
                                          + ('max-width: 320px; @media(--tablet){max-width: none;}' if pro else ''))
            li += b.el('e-flexbox', f'{p}l{j}', r, css='display: flex; flex-direction: row; align-items: flex-start; gap: 16px; padding: 0px 0px 0px 13px;')
        c += b.el('e-flexbox', p + 'l', li, css='display: flex; flex-direction: column; gap: 16px; padding: 0px; margin: 53px 0px 0px 0px; width: 100%; '
                                               '@media(--laptop){margin: 36px 0px 0px 0px;}')
        bg = ("background-color: #FFFFFF; border: 1px solid rgba(20,74,224,0.4); "
              f"background-image: url('{bgurl('bg-pricing-pro')}'); background-size: 100% 100%; background-repeat: no-repeat;"
              if pro else 'background-color: rgba(255,255,255,0.8);')
        cards += b.el('e-flexbox', p, c, css=(
            'display: flex; flex-direction: column; align-items: flex-start; flex: 1 1 0px; min-width: 0px; '
            f'padding: 48px 37px 55px 37px; border-radius: 30px; {bg} '
            '@media(--laptop){padding: 40px 28px 44px 28px;} @media(--tablet){flex: 1 1 auto; width: 100%;} '
            '@media(--mobile){padding: 32px 20px 36px 20px; border-radius: 24px;}'))
    row = b.el('e-flexbox', 'sd-cards', cards, css=(
        'display: flex; flex-direction: row; align-items: flex-start; gap: 16px; width: 100%; padding: 0px; '
        '@media(--tablet){flex-direction: column; align-items: stretch; max-width: 600px;}'))
    note = para(b, 'sd-note', ('Need more volume? <span>Usage-based overage billing</span> '
                               'available at $0.696/note.'),
                'font-size: 16px; line-height: 32px; color: #4F4F4F; text-align: center; margin: 35px 0px 0px 0px; '
                '@media(--mobile){font-size: 15px; line-height: 28px;} & span{color: #144AE0; font-weight: 500;}')
    panel = b.el('e-flexbox', 'sd-panel', row + note, css=(
        'display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 1636px; '
        'padding: 20px 21px 39px 21px; border-radius: 40px; border: 1px solid #E7E7E7; background-color: #FFFFFF; '
        f"background-image: url('{bgurl('bg-pricing-panel')}'); background-size: 100% 100%; background-repeat: no-repeat; "
        '@media(--tablet){padding: 16px 16px 32px 16px;} @media(--mobile){padding: 12px 10px 28px 10px; border-radius: 28px;}'))
    return section(b, 'sd', k + panel, 'bg-pricing', 104, 84, attrs=[{'key': 'id', 'value': 'pricing'}])


# ---------------------------------------------------------------- E. Add-ons
def addons(b):
    k = pill(b, 'se-pill', 'Available Add-Ons')
    k += h2(b, 'se-h2', 'Add-ons available on every plan')
    k += sub(b, 'se-sub', 'Add to any plan. Your MedCare MSO representative quotes pricing for your practice.', 56)
    items = [('icon-template', 42, 'Dynamic Template', 'Build note templates for your specialty with drag and drop and voice commands, so the note comes out in the structure your practice already uses.'),
             ('icon-search', 36, 'Face Sheet Scanner', 'Scan the patient face sheet and add the details of insurance demographics into the encounter, so the note starts with the patient record filled in.'),
             ('icon-letter', 38, 'Referral Letter', 'You can create the referral letter from the encounter note, with the reason and the findings relevant to the patient.'),
             ('icon-checklist', 38, 'Follow-Up Task/Order', 'Turn the plan section into follow-up tasks and orders, so nothing discussed in the room is left to memory.')]
    g = ''
    for i, (ic, px, t, body) in enumerate(items):
        c = tile(b, f'se{i}k', ic, 82, px)
        c += b.el('e-heading', f'se{i}t', cfg={'tag': 'h3', 'title': t}, css=(
            f'{F} font-size: 32px; line-height: 42px; font-weight: 400; color: #000000; text-align: center; max-width: 290px; '
            'margin: 41px 0px 36px 0px; @media(--laptop){font-size: 28px; line-height: 38px; margin: 32px 0px 24px 0px;} '
            '@media(--mobile){font-size: 24px; line-height: 32px; margin: 24px 0px 16px 0px;}'))
        c += para(b, f'se{i}p', body, 'font-size: 16px; line-height: 32px; color: #4F4F4F; text-align: center; margin: 0px; '
                                      '@media(--mobile){font-size: 15px; line-height: 28px;}')
        g += b.el('e-flexbox', f'se{i}', c, css=(
            'display: flex; flex-direction: column; align-items: center; padding: 29px 26px 33px 26px; border-radius: 20px; '
            f'background-color: rgba(255,255,255,0.2); {SH} {GLASS} @media(--mobile){{padding: 28px 20px 28px 20px;}}'))
    k += b.el('e-div-block', 'se-grid', g, css=(
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; width: 100%; max-width: 1476px; padding: 0px; '
        '@media(--tablet_extra){grid-template-columns: repeat(2, minmax(0, 1fr));} '
        '@media(--mobile){grid-template-columns: minmax(0, 1fr);}'))
    return section(b, 'se', k, 'bg-addons', 85, 82)


# ---------------------------------------------------------------- F. Comparison table
def compare(b):
    k = pill(b, 'sf-pill', 'Plan Comparison')
    k += h2(b, 'sf-h2', 'What Each Plan Includes')
    k += sub(b, 'sf-sub', 'Feature by feature across Basic, Pro, and Ultimate.', 85)
    Y, N = 'Y', '–'
    rows = [('Ambient recording', Y, Y, Y), ('Automated SOAP notes', Y, Y, Y), ('ICD-10 suggestions', Y, Y, Y),
            ('E/M + CPT coding', N, Y, Y), ('Multi-language support', N, Y, Y), ('Custom templates', N, Y, Y),
            ('EHR integrations', '1', '3', 'Unlimited'), ('Analytics dashboard', N, Y, Y),
            ('Dedicated success manager', N, N, Y), ('SSO & advanced security', N, N, Y), ('Support', 'Email', 'Priority', '24/7 SLA')]
    cells = ''
    pad_f = 'padding: 25.75px 30.9px; @media(--tablet){padding: 18px 16px;} @media(--mobile){padding: 14px 8px 14px 10px;}'
    pad_c = 'padding: 25.75px 20.6px; @media(--tablet){padding: 18px 8px;} @media(--mobile){padding: 14px 4px;}'
    cells += para(b, 'tf-h0', 'Feature', 'font-size: 18px; line-height: 25px; font-weight: 600; color: #64748B; margin: 0px; '
                                         f'display: flex; align-items: center; {pad_f} @media(--mobile){{font-size: 13px; line-height: 18px;}}')
    for j, (nm, col) in enumerate([('Basic', '#07182D'), ('Pro', '#144AE0'), ('Ultimate', '#07182D')], 1):
        bg = 'background-color: rgba(0,102,255,0.05); border-radius: 18px 18px 0px 0px;' if nm == 'Pro' else ''
        cells += para(b, f'tf-h{j}', nm, f'font-size: 22px; line-height: 29px; font-weight: 500; color: {col}; text-align: center; margin: 0px; '
                                         f'display: flex; align-items: center; justify-content: center; {bg} {pad_c} '
                                         '@media(--mobile){font-size: 14px; line-height: 20px;}')
    line = 'border-style: solid; border-color: rgba(7,24,45,0.08); border-width: 0px 0px 1.29px 0px;'
    for i, (feat, *vals) in enumerate(rows):
        last = i == len(rows) - 1
        cells += para(b, f'tf{i}f', feat, f'font-size: 18px; line-height: 27px; font-weight: 500; color: #475569; margin: 0px; '
                                          f'display: flex; align-items: center; {line} padding: 19.3px 30.9px; '
                                          '@media(--tablet){padding: 16px 16px; font-size: 16px; line-height: 24px;} '
                                          '@media(--mobile){padding: 12px 8px 12px 10px; font-size: 13px; line-height: 18px;}')
        for j, v in enumerate(vals, 1):
            pro = j == 2
            bg = 'background-color: rgba(0,102,255,0.04);' if pro else ''
            if pro and last:
                bg += ' border-radius: 0px 0px 18px 18px;'
            base = (f'display: flex; align-items: center; justify-content: center; {line} {bg} padding: 19.3px 20.6px; '
                    '@media(--tablet){padding: 16px 8px;} @media(--mobile){padding: 12px 4px;}')
            cid = f'tf{i}c{j}'
            if v == Y:
                ic = image(b, cid + 'i', 'icon-check-green', 'width: 22px; height: 22px; display: block; @media(--mobile){width: 18px; height: 18px;}')
                cells += b.el('e-div-block', cid, ic, css=base)
            elif v == N:
                cells += para(b, cid, '–', 'font-size: 23px; line-height: 35px; color: #94A3B8; margin: 0px; ' + base
                              + ' @media(--mobile){font-size: 18px; line-height: 24px;}')
            else:
                cells += para(b, cid, v, 'font-size: 16.7px; line-height: 25px; font-weight: 600; color: #07182D; text-align: center; margin: 0px; '
                              + base + ' @media(--mobile){font-size: 12px; line-height: 16px;}')
    table = b.el('e-div-block', 'tf-grid', cells, css=(
        'display: grid; grid-template-columns: minmax(0, 719fr) minmax(0, 212fr) minmax(0, 226fr) minmax(0, 283fr); '
        'width: 100%; padding: 0px; '
        '@media(--tablet){grid-template-columns: minmax(0, 2fr) repeat(3, minmax(0, 1fr));} '
        '@media(--mobile){grid-template-columns: minmax(0, 1.45fr) repeat(3, minmax(0, 1fr));}'))
    k += b.el('e-flexbox', 'sf-box', table, css=(
        'display: flex; width: 100%; max-width: 1463px; padding: 10px; border-radius: 31px; border: 1px solid rgba(255,255,255,0.8); '
        f'background-color: rgba(255,255,255,0.2); {GLASS} @media(--mobile){{padding: 4px; border-radius: 20px;}}'))
    return section(b, 'sf', k, 'bg-compare', 82, 96)


# ---------------------------------------------------------------- G. Why Salus
def why(b):
    k = pill(b, 'sg-pill', 'Why Salus?')
    k += h2(b, 'sg-h2', 'Built the way you work, not the way software does')
    k += sub(b, 'sg-sub', ('The note is structured and coded by the time the next patient arrives. Here is what that means for you and the practice.'), 69)
    cards = [
        ('icon-clock', 'Get your time back', 'The documentation is done during the visit, not after the clinic hours'),
        ('icon-git-merge', 'Lesser gaps in the note', 'Structured notes carry exactly what payers are looking for, which lower the chances of denials.'),
        ('icon-loader', 'No change to how you see patients', 'Ambient capture runs in the background. No new buttons during the visit.'),
        ('icon-trending-up', 'Coding-ready on every note', 'ICD-10 and SNOMED suggestions on every plan; CPT and modifiers on Ultimate. Your coders start from a draft, not a blank.'),
        ('icon-maximize', 'Grows with the practice', 'From one provider to a multi-specialty group on the same platform; tiered plans add languages, speakers, and integrations as you add clinicians.'),
        ('icon-shield-blue', 'Compliance in the design', 'PHI redaction, a full audit trail, and zero audio retention. These are how the system is built, not settings to switch on.'),
    ]
    g = ''
    for i, (ic, t, p) in enumerate(cards):
        c = image(b, f'sg{i}i', ic, 'width: 43px; height: 43px; display: block; margin: 0px 0px 19px 0px;')
        c += b.el('e-heading', f'sg{i}t', cfg={'tag': 'h3', 'title': t}, css=(
            f'{F} font-size: 22px; line-height: 32px; font-weight: 400; color: #000000; max-width: 296px; margin: 0px 0px 9px 0px; '
            '@media(--mobile){font-size: 20px; line-height: 28px;}'))
        c += para(b, f'sg{i}p', p, 'font-size: 16px; line-height: 28px; color: #4F4F4F; margin: 0px; max-width: 291px; '
                                   '@media(--tablet){max-width: none;} @media(--mobile){font-size: 15px; line-height: 26px;}')
        g += b.el('e-flexbox', f'sg{i}', c, css=(
            'display: flex; flex-direction: column; align-items: flex-start; padding: 28px 24px 28px 27px; border-radius: 30px; '
            f'background-color: rgba(255,255,255,0.5); {GLASS} @media(--mobile){{padding: 26px 20px 26px 20px; border-radius: 24px;}}'))
    q = para(b, 'sg-qm', '“', 'font-size: 92px; line-height: 61px; color: #144AE0; margin: 0px 0px 2px 0px;')
    q += para(b, 'sg-qt', ('Salus AI was built for one thing: the clinician leaves the room with the note written and the codes suggested, '
                           'and the way they see patients does not change.'),
              'font-size: 18px; line-height: 39px; color: #4F4F4F; max-width: 315px; margin: 0px 0px 39px 0px; @media(--tablet){max-width: none;} @media(--mobile){font-size: 16px; line-height: 32px;}')
    av = para(b, 'sg-av', 'M', 'font-size: 14.5px; line-height: 22px; font-weight: 500; letter-spacing: 0.14px; color: #FFFFFF; margin: 0px; '
                               'display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; flex-shrink: 0; '
                               'border-radius: 22px; background-color: #0066FF;')
    who = para(b, 'sg-an', 'MedCare MSO, product team', 'font-size: 16px; line-height: 32px; font-weight: 500; color: #000000; margin: 0px;')
    av += b.el('e-div-block', 'sg-aw', who, css='display: flex; flex-direction: column; padding: 0px; min-width: 0px;')
    q += b.el('e-flexbox', 'sg-auth', av, css=('display: flex; flex-direction: row; align-items: flex-start; gap: 19px; padding: 45px 0px 0px 0px; '
                                               'border-style: solid; border-color: #E3E3E3; border-width: 1px 0px 0px 0px; width: 100%;'))
    g += b.el('e-flexbox', 'sg-q', q, css=(
        'display: flex; flex-direction: column; align-items: flex-start; padding: 61px 13px 55px 53px; border-radius: 30px; '
        'background-color: #FFFFFF; grid-column: 4; grid-row: 1 / span 2; '
        '@media(--laptop){padding: 48px 20px 44px 32px;} '
        '@media(--tablet){grid-column: 1 / -1; grid-row: auto; padding: 48px 32px 44px 32px;} @media(--mobile){padding: 36px 22px 32px 22px; border-radius: 24px;}'))
    k += b.el('e-div-block', 'sg-grid', g, css=(
        'display: grid; grid-template-columns: repeat(3, minmax(0, 343fr)) minmax(0, 411fr); grid-auto-flow: row dense; '
        'gap: 15px 12px; width: 100%; max-width: 1475px; padding: 0px; '
        '@media(--tablet_extra){grid-template-columns: repeat(3, minmax(0, 1fr));} '
        '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} '
        '@media(--mobile){grid-template-columns: minmax(0, 1fr); gap: 14px;}'))
    return section(b, 'sg', k, 'bg-why', 96, 84)


# ---------------------------------------------------------------- H. CTA
def cta(b):
    k = pill(b, 'sh-pill', 'Ready to get started')
    k += h2(b, 'sh-h2', 'See Salus AI on one of your own encounters', 28, mt=29)
    k += para(b, 'sh-p', 'Request a demo from your MedCare MSO representative. Onboarding is included with every plan.',
              'font-size: 16px; line-height: 32px; color: #4F4F4F; text-align: center; max-width: 867px; margin: 0px; '
              '@media(--mobile){font-size: 15px; line-height: 28px;}')
    panel = b.el('e-flexbox', 'sh-panel', k, css=(
        'display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 1806px; '
        f'padding: 61px 40px 223px 40px; border-radius: 20px; background-color: rgba(255,255,255,0.6); {SH} {GLASS} '
        '@media(--tablet){padding: 48px 24px 200px 24px;} @media(--mobile){padding: 36px 16px 120px 16px;}'))
    stats = ''
    for i, (t, s) in enumerate([('From $99/mo', 'Per provider'), ('No Lock-In', 'Flexible terms'),
                                ('Onboarding Included', 'All plans'), ('HIPAA Compliant', 'Architecture-level')]):
        c = para(b, f'st{i}t', t, 'font-size: 24px; line-height: 32px; letter-spacing: -0.48px; color: #FFFFFF; text-align: center; margin: 0px 0px 6px 0px; '
                                  '@media(--mobile){font-size: 20px; line-height: 28px;}')
        c += para(b, f'st{i}s', s, 'font-size: 16px; line-height: 25px; color: #FFFFFF; text-align: center; margin: 0px; '
                                   '@media(--mobile){font-size: 14px; line-height: 22px;}')
        sep = ('border-style: solid; border-color: rgba(255,255,255,0.3); border-width: 0px 0px 0px 1px; '
               '@media(--tablet){border-width: 0px;}' if i else '')
        stats += b.el('e-div-block', f'st{i}', c, css=(
            'display: flex; flex-direction: column; align-items: center; justify-content: center; width: 218px; flex-shrink: 0; min-height: 115px; '
            f'padding: 0px 24px; {sep} @media(--tablet_extra){{width: 180px; padding: 0px 14px;}} '
            '@media(--tablet){width: auto; min-height: 0px; padding: 0px;}'))
    sg = b.el('e-flexbox', 'sh-stats', stats, css=(
        'display: flex; flex-direction: row; align-items: center; padding: 0px; '
        '@media(--tablet){display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 16px; width: 100%; max-width: 560px;} '
        '@media(--mobile){gap: 24px 12px;}'))
    btn = pill_button(b, 'sh-btn', 'Request Book a Demo', DEMO, 'arrow-cta',
                      ('border-color: #B8BCDB; background-color: rgba(154,161,202,0.2); margin: 0px 0px 0px auto; position: relative; z-index: 1; '
                       '@media(--tablet){margin: 0px;}'), '#FFFFFF')
    logo = image(b, 'sh-logo', 'cta-logo', ('position: absolute; width: 423px; height: 543px; max-width: none; inset-inline-end: 58px; '
                                            'inset-block-start: -114px; pointer-events: none; '
                                            '@media(--tablet){inset-inline-end: -60px;} @media(--mobile){width: 260px; height: 334px; inset-block-start: auto; inset-block-end: -120px; inset-inline-end: -70px;}'))
    bar = b.el('e-flexbox', 'sh-bar', sg + btn + logo, css=(
        'display: flex; flex-direction: row; align-items: center; width: 100%; max-width: 1476px; min-height: 316px; '
        'padding: 40px 134px 40px 52px; margin: -158px 0px 0px 0px; position: relative; overflow: hidden; border-radius: 20px; '
        'background-color: #1E4BD8; background-image: radial-gradient(circle at 20% 0%, #3F6FF5 0%, #002794 100%); '
        'box-shadow: 0px 51px 64px 0px rgba(89,89,89,0.2); z-index: 1; '
        '@media(--laptop){padding: 40px 48px 40px 32px;} '
        '@media(--tablet){flex-direction: column; justify-content: center; gap: 32px; padding: 48px 24px;} '
        '@media(--mobile){margin: -96px 0px 0px 0px; padding: 36px 18px; gap: 28px; min-height: 0px;}'))
    wm = image(b, 'sh-wm', 'watermark', ('width: 100%; max-width: 1662px; height: auto; display: block; opacity: 0.3; '
                                         'margin: 11px 0px max(-204px, -12.26%) 0px; pointer-events: none;'))
    return section(b, 'sh', panel + bar + wm, 'bg-cta', 84, 0)


SECTIONS = [hero, see, does, pricing, addons, compare, why, cta]


def payload(mode='replace_children', dry=False):
    b = B()
    xml = ''.join(f(b) for f in SECTIONS)
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes,
            'mode': mode, 'dry_run': dry}
