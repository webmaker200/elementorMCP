"""Challenges Single Page (WP page 411126) from Figma 656:14, Elementor V4 atomic elements.

Reuses the Salus page helpers (pill / headings / glass cards / pill buttons) with this page's media.
The root-cause section follows the layout the user sent as a screenshot, in this design's palette.
"""
import json
from build import B
import salus as S

PID = 411126
MEDIA = json.load(open('chal/media.json'))
S.MEDIA = MEDIA  # helpers resolve media ids/urls through salus.MEDIA
F, GLASS, SH = S.F, S.GLASS, S.SH
para, image, pill, h2, sub, section, tile = S.para, S.image, S.pill, S.h2, S.sub, S.section, S.tile
DEMO = 'https://medcaremso.com/request-demo/?utm_source=challenges-single-page'
BLUE = '#1171A1'
CARD = f'background-color: rgba(255,255,255,0.1); border-radius: 20px; {SH} {GLASS}'


def green_button(b, cid, text, url, text_color='#000000', css=''):
    """Figma Button.base on this page: green glass pill, white circle with green arrow."""
    return S.pill_button(b, cid, text, url, 'arrow-btn', ('border-color: #B8DBD4; background-color: rgba(154,202,161,0.2); ' + css),
                         text_color, hover_bg='rgba(154,202,161,0.38)', hover_shadow='rgba(49,131,113,0.15)')


def text_link(b, cid, text, url, arrow, color):
    k = para(b, cid + 't', text, f'font-size: 14px; line-height: 19.6px; font-weight: 500; color: {color}; margin: 0px;')
    k += image(b, cid + 'i', arrow, 'width: 24px; height: 24px; display: block;')
    cfg = {'tag': 'a', 'link': {'destination': url}} if url else {'tag': 'div'}
    return b.el('e-flexbox', cid, k, cfg=cfg, css=('display: flex; width: max-content; align-items: center; gap: 13px; padding: 0px; '
                                                   'text-decoration: none; transition: transform 0.3s ease; &:hover{transform: translateX(4px);}'))


# ---------------------------------------------------------------- A. Hero
def metric_card(b):
    t = image(b, 'mc-li', 'icon-pill', 'width: 12px; height: 12px; display: block;')
    t += para(b, 'mc-lt', 'WHAT DENIALS REALLY COST', 'font-size: 10.2px; line-height: 12.7px; font-weight: 600; letter-spacing: 0.51px; color: #2689BB; margin: 0px; white-space: nowrap;')
    lab = b.el('e-flexbox', 'mc-lab', t, css='display: flex; width: max-content; align-items: center; gap: 10px; height: 26px; padding: 0px 12px; border-radius: 999px; background-color: rgba(227,241,255,0.2);')
    lab += para(b, 'mc-ld', 'Denied claims create operational overhead and impact revenue. Here’s what it looks like.',
                'font-size: 11.2px; line-height: 16.2px; font-weight: 500; letter-spacing: -0.25px; color: #6D7F98; margin: 0px; padding: 9.7px 0px 0px 0px; max-width: 300px;')
    left = b.el('e-div-block', 'mc-hl', lab, css='display: flex; flex-direction: column; padding: 0px; min-width: 0px;')
    dd = image(b, 'mc-ddi', 'icon-calendar', 'width: 13px; height: 13px; display: block;')
    dd += para(b, 'mc-ddt', 'Last 6 Months', 'font-size: 8.7px; line-height: 13px; font-weight: 500; color: #6D7F98; margin: 0px; white-space: nowrap;')
    dd += image(b, 'mc-ddc', 'icon-chevron-down', 'width: 10px; height: 10px; display: block;')
    drop = b.el('e-flexbox', 'mc-dd', dd, css=('display: flex; width: max-content; align-items: center; gap: 7px; height: 34px; padding: 0px 14px; flex-shrink: 0; '
                                               'border-radius: 999px; border: 0.4px solid rgba(139,195,67,0.8); background-color: rgba(255,255,255,0.1); @media(--mobile){display: none;}'))
    head = b.el('e-flexbox', 'mc-head', left + drop, css='display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 16px; padding: 0px; width: 100%;')

    rows = [('icon-row1', 'rgba(255,241,242,0.95)', 'Claims denied on first pass', 'Require additional review and follow-up.', '~10%', '2%'),
            ('icon-row2', 'rgba(227,241,255,0.95)', 'Never reworked or recovered', 'Result in permanent revenue loss.', '65%', '5%'),
            ('icon-row3', 'rgba(237,233,254,0.8)', 'Cost to rework one claim', 'Includes staff time and administrative effort.', '$25+', '12%'),
            ('icon-row4', 'rgba(247,253,236,0.95)', 'With MedCare MSO', 'Cleaner claims and stronger revenue outcomes.', '98.5%', None)]
    rr = ''
    for i, (ic, bg, t1, t2, val, delta) in enumerate(rows):
        x = b.el('e-div-block', f'mr{i}k', image(b, f'mr{i}ki', ic, 'width: 17px; height: 17px; display: block;'),
                 css=f'display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; flex-shrink: 0; padding: 0px; border-radius: 11.7px; background-color: {bg};')
        tx = para(b, f'mr{i}t', t1, 'font-size: 10.7px; line-height: 15.5px; font-weight: 600; letter-spacing: -0.25px; color: #07182D; margin: 0px;')
        tx += para(b, f'mr{i}s', t2, 'font-size: 9.2px; line-height: 14.7px; letter-spacing: -0.23px; color: #6D7F98; margin: 0px; padding: 2px 0px 0px 0px;')
        x += b.el('e-div-block', f'mr{i}x', tx, css='display: flex; flex-direction: column; padding: 0px; min-width: 0px; width: auto; flex: 1 1 0px;')
        v = para(b, f'mr{i}v', val, f"font-size: 19.3px; line-height: 23.2px; font-weight: 600; letter-spacing: -0.66px; color: {'#8BC343' if not delta else '#07182D'}; text-align: right; margin: 0px; white-space: nowrap;")
        if delta:
            d = image(b, f'mr{i}di', 'icon-up-red', 'width: 10px; height: 10px; display: block;')
            d += para(b, f'mr{i}dt', delta, 'font-size: 9.7px; line-height: 14.5px; font-weight: 500; color: #FF526E; margin: 0px;')
            v += b.el('e-flexbox', f'mr{i}d', d, css='display: flex; width: max-content; align-items: center; gap: 2px; padding: 4px 0px 0px 0px; align-self: flex-end;')
        else:
            v += para(b, f'mr{i}dt', 'Clean Claims', 'font-size: 9.2px; line-height: 13.7px; color: #6D7F98; text-align: right; margin: 0px; padding: 2px 0px 0px 0px;')
        x += b.el('e-div-block', f'mr{i}r', v, css='display: flex; flex-direction: column; align-items: flex-end; padding: 0px; flex-shrink: 0; width: max-content;')
        rr += b.el('e-flexbox', f'mr{i}', x, css=(
            'display: flex; flex-direction: row; align-items: center; gap: 16px; width: 100%; min-height: 64px; padding: 10px 14px; '
            'border-radius: 13.7px; border: 0.4px solid #FFFFFF; background-color: rgba(255,255,255,0.2); '
            'box-shadow: 0px 0px 0px 1px rgba(219,232,246,0.42); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);'))
    rcol = b.el('e-flexbox', 'mc-rows', rr, css='display: flex; flex-direction: column; gap: 7px; padding: 0px; min-width: 0px;')

    bd = b.el('e-div-block', 'mc-bdk', image(b, 'mc-bdki', 'icon-trend', 'width: 14px; height: 14px; display: block;'),
              css='display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; flex-shrink: 0; padding: 0px; border-radius: 50%; border: 0.4px solid rgba(139,195,67,0.3); background-color: #FFFFFF;')
    bt = para(b, 'mc-bdv', '98.5%', 'font-size: 14.3px; line-height: 17.8px; font-weight: 600; letter-spacing: -0.41px; color: #07182D; margin: 0px;')
    bt += para(b, 'mc-bdl', 'Clean Claims', 'font-size: 8.1px; line-height: 12.2px; color: #526781; margin: 0px; white-space: nowrap;')
    bd += b.el('e-div-block', 'mc-bdx', bt, css='display: flex; flex-direction: column; padding: 0px;')
    badge = b.el('e-flexbox', 'mc-badge', bd, css=(
        'display: flex; width: max-content; align-items: center; gap: 8.7px; padding: 10px 11px; position: absolute; z-index: 1; '
        'inset-block-start: 0px; inset-inline-start: 26%; border-radius: 13.7px; border: 0.4px solid #FFFFFF; '
        f'background-color: rgba(255,255,255,0.2); {GLASS}'))
    chart = b.el('e-div-block', 'mc-chart', image(b, 'mc-chi', 'chart', 'width: 100%; height: auto; display: block;', alt='Clean-claim rate trend') + badge,
                 css='position: relative; width: 100%; padding: 0px;')
    bb = image(b, 'mc-bti', 'icon-target', 'width: 16px; height: 16px; display: block; flex-shrink: 0;')
    bb += para(b, 'mc-btt', 'Higher claim accuracy.<br>Less revenue loss.', 'font-size: 10.7px; line-height: 16px; font-weight: 600; letter-spacing: -0.2px; color: #07182D; margin: 0px; flex: 1 1 auto;')
    bb += b.el('e-div-block', 'mc-btc', image(b, 'mc-btci', 'icon-chevron-right', 'width: 12px; height: 12px; display: block;'),
               css='display: flex; align-items: center; justify-content: center; width: 29px; height: 29px; flex-shrink: 0; padding: 0px; border-radius: 50%; background-color: #E3F1FF;')
    btn = b.el('e-flexbox', 'mc-btn', bb, css=(
        'display: flex; flex-direction: row; align-items: center; gap: 12px; width: 100%; min-height: 78px; padding: 0px 16px; '
        f'border-radius: 14.3px; border: 0.4px solid #FFFFFF; background-color: rgba(255,255,255,0.1); {GLASS}'))
    ccol = b.el('e-flexbox', 'mc-ccol', chart + btn, css='display: flex; flex-direction: column; justify-content: space-between; gap: 10px; padding: 0px; min-width: 0px;')
    body = b.el('e-div-block', 'mc-body', rcol + ccol, css=(
        'display: grid; grid-template-columns: minmax(0, 372fr) minmax(0, 239fr); gap: 30px; width: 100%; padding: 0px; margin: 14px 0px 0px 0px; '
        '@media(--mobile){grid-template-columns: minmax(0, 1fr); gap: 16px;}'))
    return b.el('e-flexbox', 'mc', head + body, css=(
        'display: flex; flex-direction: column; width: 100%; padding: 24px 30px 22px 29px; border-radius: 19.3px; '
        'border: 0.4px solid #FFFFFF; background-color: rgba(255,255,255,0.1); box-shadow: 0px 23px 20px 0px rgba(178,178,178,0.1); '
        f'{GLASS} @media(--mobile){{padding: 18px 14px;}}'))


def hero(b):
    av = ''
    for i in (1, 2, 3):
        av += image(b, f'hp-a{i}', f'avatar-{i}', ('width: 35px; height: 35px; object-fit: cover; border-radius: 50%; border: 1.5px solid #FFFFFF; '
                                                   f"margin: 0px 0px 0px {'0px' if i == 1 else '-12px'};"))
    av += para(b, 'hp-t', 'The #1 preventable revenue leak in medical practices', 'font-size: 12px; line-height: 14.4px; color: #7D7D7D; margin: 0px 0px 0px 11px;')
    k = b.el('e-flexbox', 'hp', av, css=('display: flex; width: max-content; max-width: 100%; align-items: center; gap: 0px; min-height: 46px; '
                                         'padding: 4px 26px 4px 9px; border-radius: 31px; border: 1px solid #7EB63E; margin: 0px 0px 25px 0px; '
                                         '@media(--tablet_extra){align-self: center;} @media(--mobile){padding: 4px 14px 4px 9px;}'))
    k += b.el('e-heading', 'h1', cfg={'tag': 'h1', 'title': 'Stop losing revenue to <span>claim denials</span> you could have prevented'}, css=(
        f'{F} font-size: 58px; line-height: 67px; font-weight: 400; color: #000000; max-width: 660px; margin: 0px 0px 24px 0px; '
        '& span{color: #1171A1; background-color: #F2F9FF; border-radius: 15px; padding: 0px 9px; -webkit-box-decoration-break: clone; box-decoration-break: clone;} '
        '@media(--laptop){font-size: 50px; line-height: 60px;} @media(--tablet_extra){max-width: 760px;} '
        '@media(--tablet){font-size: 44px; line-height: 54px;} @media(--mobile){font-size: 34px; line-height: 44px;}'))
    k += para(b, 'hero-p', ('Every denied claim is money you already earned — stuck in rework or written off for good. MedCare MSO catches '
                            'denials before submission and wins back the ones that slip through.'),
              'font-size: 16px; line-height: 32px; color: #4F4F4F; max-width: 660px; margin: 0px 0px 21px 0px; @media(--mobile){font-size: 15px; line-height: 28px;}')
    btns = green_button(b, 'hero-b1', 'Get a Free Denial Audit', DEMO)
    btns += text_link(b, 'hero-b2', 'How We Fix Denials', '#how-we-fix', 'arrow-black', '#000000')
    k += b.el('e-flexbox', 'hero-btns', btns, css='display: flex; flex-wrap: wrap; align-items: center; gap: 20px 42px; padding: 0px; @media(--tablet_extra){justify-content: center;}')
    tr = ''
    for i, (strong, rest) in enumerate([('98.5%', ' first-pass clean claims'), ('48-hr', ' appeal turnaround'), ('HIPAA', ' · SOC 2 secured')]):
        c = b.el('e-div-block', f'tr{i}k', image(b, f'tr{i}ki', 'icon-check-sm', 'width: 9px; height: 9px; display: block;'),
                 css='display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; flex-shrink: 0; padding: 0px; border-radius: 9px; border: 0.8px solid rgba(139,197,63,0.31); background-color: rgba(139,197,63,0.09);')
        c += para(b, f'tr{i}t', f'<strong>{strong}</strong>{rest}', 'font-size: 13px; line-height: 20.2px; color: #4F4F4F; margin: 0px; white-space: nowrap; & strong{font-weight: 600;}')
        tr += b.el('e-flexbox', f'tr{i}', c, css='display: flex; width: max-content; align-items: center; gap: 7px; padding: 0px;')
    k += b.el('e-flexbox', 'hero-trust', tr, css='display: flex; flex-wrap: wrap; align-items: center; gap: 12px 16px; padding: 0px; margin: 61px 0px 0px 0px; '
                                                 '@media(--tablet_extra){justify-content: center; margin: 40px 0px 0px 0px;}')
    left = b.el('e-flexbox', 'hero-l', k, css='display: flex; flex-direction: column; align-items: flex-start; padding: 0px; flex: 0 1 660px; min-width: 0px; '
                                              '@media(--tablet_extra){flex: 0 1 auto; width: 100%; align-items: center; text-align: center;}')
    chips = ''
    for i, (ic, px, txt, w) in enumerate([('icon-folder', 29, '$5M practice loses ~$50K+/yr to denials', 119),
                                         ('icon-clock-blue', 34, '90+ days average delay on an appealed claim', 148),
                                         ('icon-dollar', 29, '1 in 15 denied dollars never returns', 118)]):
        c = image(b, f'hc{i}i', ic, f'width: {px}px; height: {px}px; display: block; flex-shrink: 0;')
        c += para(b, f'hc{i}t', txt, f'font-size: 11.5px; line-height: 17.3px; color: #000000; margin: 0px; max-width: {w + 4}px; text-align: left;')
        chips += b.el('e-flexbox', f'hc{i}', c, css=(f'display: flex; width: max-content; align-items: center; gap: 12px; padding: 14px 18px; border-radius: 20px; '
                                                     f'background-color: rgba(255,255,255,0.2); {SH} {GLASS}'))
    crow = b.el('e-flexbox', 'hero-chips', chips, css='display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 15px; padding: 0px; margin: 16px 0px 0px 0px;')
    right = b.el('e-flexbox', 'hero-r', metric_card(b) + crow, css=(
        'display: flex; flex-direction: column; padding: 0px; flex: 0 1 700px; min-width: 0px; margin: 50px 0px 0px 0px; '
        '@media(--tablet_extra){flex: 0 1 auto; width: 100%; max-width: 700px; margin: 56px 0px 0px 0px;}'))
    row = b.el('e-flexbox', 'hero-row', left + right, css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 40px; width: 100%; max-width: 1490px; padding: 0px; '
        '@media(--tablet_extra){flex-direction: column; align-items: center; gap: 0px;}'))
    return section(b, 'sa', row, 'bg-hero', 119, 74)


# ---------------------------------------------------------------- B. Short answer + cost
def cost(b):
    t = b.el('e-heading', 'sb-st', cfg={'tag': 'h2', 'title': 'The short answer'}, css=(
        f'{F} font-size: 32px; line-height: 39px; font-weight: 400; color: #000000; margin: 0px 0px 23px 0px; @media(--mobile){{font-size: 26px; line-height: 34px;}}'))
    t += para(b, 'sb-sp', ('Claim denials happen when a payer refuses to reimburse a submitted claim — usually over eligibility, coding, authorization, '
                           'or documentation errors. Reducing them means catching those errors before submission and appealing denials fast, '
                           'which is exactly what a denial-focused billing partner does.'),
              'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px; @media(--mobile){font-size: 15px; line-height: 28px;}')
    k = b.el('e-flexbox', 'sb-short', t, css=(f'display: flex; flex-direction: column; width: 100%; max-width: 1475px; padding: 44px 111px 49px 111px; {CARD} '
                                              '@media(--laptop){padding: 40px 64px;} @media(--tablet){padding: 32px 32px;} @media(--mobile){padding: 26px 20px;}'))
    k += pill(b, 'sb-pill', 'What it\'s costing you')
    b.style['sb-pill'] += ' margin: 78px 0px 0px 0px; @media(--laptop){margin: 64px 0px 0px 0px;} @media(--tablet){margin: 52px 0px 0px 0px;} @media(--mobile){margin: 40px 0px 0px 0px;}'
    k += h2(b, 'sb-h2', "Denials aren't a billing nuisance — they're a silent revenue leak", 10, 1180, mt=23)
    k += sub(b, 'sb-sub', ('Most practices treat denials as routine rework. But every denied claim carries a cost to appeal, a delay to your cash flow, '
                           'and a real chance the revenue is never recovered at all.'), 59, '#4F4F4F', 870)
    stats = [('icon-search', 36, '~10%', 'of claims are denied on first submission industry-wide'),
             ('icon-payments', 48, '65%', 'of denied claims are never reworked or resubmitted'),
             ('icon-file-plus', 43, '$25+', 'average cost to rework a single denied claim'),
             ('icon-pie', 40, '98.5%', 'first-pass clean-claim rate with MedCare MSO')]
    g = ''
    for i, (ic, px, v, t2) in enumerate(stats):
        c = tile(b, f'sb{i}k', ic, 82, px)
        c += para(b, f'sb{i}v', v, 'font-size: 32px; line-height: 46px; color: #000000; text-align: center; margin: 41px 0px 6px 0px; @media(--mobile){margin: 24px 0px 4px 0px;}')
        c += para(b, f'sb{i}t', t2, 'font-size: 16px; line-height: 32px; color: #4F4F4F; text-align: center; margin: 0px; max-width: 285px; @media(--mobile){font-size: 15px; line-height: 28px;}')
        g += b.el('e-flexbox', f'sb{i}', c, css=f'display: flex; flex-direction: column; align-items: center; padding: 29px 16px 45px 16px; {CARD} @media(--mobile){{padding: 26px 16px 30px 16px;}}')
    k += b.el('e-div-block', 'sb-grid', g, css=(
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 34px; width: 100%; max-width: 1475px; padding: 0px; '
        '@media(--laptop){gap: 20px;} @media(--tablet_extra){grid-template-columns: repeat(2, minmax(0, 1fr));} '
        '@media(--mobile){grid-template-columns: minmax(0, 1fr); gap: 16px;}'))
    return section(b, 'sb', k, 'bg-cost', 74, 108)


# ---------------------------------------------------------------- C. Root cause (screenshot layout)
def cause(b):
    k = pill(b, 'sc-pill', 'Root cause')
    b.style['sc-pill'] = b.style['sc-pill'].replace('width: 248px', 'width: 137px')
    head = k + b.el('e-heading', 'sc-h2', cfg={'tag': 'h2', 'title': '<span>Why your claims</span> keep getting denied'}, css=(
        f'{F} font-size: 58px; line-height: 70px; font-weight: 400; letter-spacing: -1.16px; color: #000000; margin: 23px 0px 32px 0px; max-width: 1100px; '
        '& span{color: #1171A1;} @media(--laptop){font-size: 48px; line-height: 60px;} @media(--tablet){font-size: 38px; line-height: 50px;} '
        '@media(--mobile){font-size: 30px; line-height: 40px; margin: 20px 0px 24px 0px;}'))
    d = b.el('e-heading', 'sc-dt', cfg={'tag': 'h3', 'title': 'What is a claim denial?'}, css=f'{F} font-size: 18px; line-height: 32px; font-weight: 500; color: #000000; margin: 0px 0px 6px 0px;')
    d += para(b, 'sc-dp', ("A claim denial is a payer's refusal to pay a claim it has received and processed. Most denials trace back to four front-end "
                           'gaps — eligibility and authorization, coding and modifiers, documentation, and the missing feedback loop that lets the '
                           'same error repeat month after month.'),
              'font-size: 16px; line-height: 30px; color: #4F4F4F; margin: 0px; @media(--mobile){font-size: 15px; line-height: 28px;}')
    head += b.el('e-flexbox', 'sc-def', d, css=(
        f'display: flex; flex-direction: column; width: 100%; padding: 26px 32px 28px 32px; border-radius: 20px; background-color: rgba(255,255,255,0.5); {SH} {GLASS} '
        'border-style: solid; border-color: #2689BB; border-width: 0px 0px 0px 4px; margin: 0px 0px 44px 0px; '
        '@media(--mobile){padding: 20px 18px 22px 20px; margin: 0px 0px 32px 0px;}'))

    # left: numbered reasons
    lt = b.el('e-heading', 'sc-lh', cfg={'tag': 'h3', 'title': 'Why do claims get denied?'}, css=(
        f'{F} font-size: 18px; line-height: 28px; font-weight: 500; color: #000000; width: 100%; margin: 0px 0px 20px 0px; padding: 0px 0px 12px 0px; '
        'border-style: solid; border-color: rgba(7,24,45,0.1); border-width: 0px 0px 1px 0px;'))
    reasons = [('Eligibility & authorization gaps', "Coverage isn't verified or prior auth is missing or expired before the service — the most preventable denial of all."),
               ('Coding & modifier errors', 'Wrong codes, missing modifiers, or NCCI bundling mistakes trigger rejections that look random but are systematic.'),
               ('Documentation shortfalls', "Thin or late clinical notes can't support medical necessity, so technically correct claims still get denied."),
               ('No denial feedback loop', 'Without root-cause tracking, the same denial reason repeats every month instead of being fixed at the front end.')]
    g = ''
    for i, (t, p) in enumerate(reasons):
        c = para(b, f'sc{i}n', f'0{i + 1}', ('font-size: 12px; line-height: 16px; font-weight: 600; color: #5E8F24; margin: 0px; '
                                            'display: flex; align-items: center; justify-content: center; width: 32px; height: 26px; border-radius: 8px; background-color: rgba(139,195,67,0.14);'))
        c += b.el('e-heading', f'sc{i}t', cfg={'tag': 'h3', 'title': t}, css=f'{F} font-size: 18px; line-height: 28px; font-weight: 500; color: #000000; margin: 16px 0px 10px 0px;')
        c += para(b, f'sc{i}p', p, 'font-size: 16px; line-height: 28px; color: #4F4F4F; margin: 0px; @media(--mobile){font-size: 15px; line-height: 26px;}')
        g += b.el('e-flexbox', f'sc{i}', c, css=f'display: flex; flex-direction: column; align-items: flex-start; padding: 26px 26px 30px 26px; {CARD} @media(--mobile){{padding: 22px 20px 24px 20px;}}')
    lt += b.el('e-div-block', 'sc-grid', g, css=('display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; width: 100%; padding: 0px; '
                                                 '@media(--mobile){grid-template-columns: minmax(0, 1fr);}'))
    left = b.el('e-flexbox', 'sc-left', lt, css='display: flex; flex-direction: column; padding: 0px; flex: 1 1 56%; min-width: 0px; @media(--tablet_extra){flex: 1 1 auto; width: 100%;}')

    # right: cost card + how-to steps
    r = b.el('e-heading', 'sc-ct', cfg={'tag': 'h3', 'title': 'What do denials cost a practice?'}, css=(
        f'{F} font-size: 26px; line-height: 36px; font-weight: 400; color: #FFFFFF; margin: 0px 0px 14px 0px; @media(--mobile){{font-size: 22px; line-height: 32px;}}'))
    r += para(b, 'sc-cp', ('About 10% of claims are denied on first submission, and 65% of those are never reworked. Each rework costs $25+ in staff time, '
                           'an appealed claim waits 90+ days on average, and a $5M practice can lose $50K+ a year to denials.'),
              'font-size: 16px; line-height: 28px; color: rgba(255,255,255,0.92); margin: 0px; @media(--mobile){font-size: 15px; line-height: 26px;}')
    costc = b.el('e-flexbox', 'sc-cost', r, css=(
        'display: flex; flex-direction: column; width: 100%; padding: 34px 36px 36px 36px; border-radius: 20px; background-color: #1A6F99; '
        f"background-image: url('{S.bgurl('banner-case')}'); background-size: cover; background-position: center center; "
        'box-shadow: 0px 30px 50px 0px rgba(89,89,89,0.2); @media(--mobile){padding: 26px 22px 28px 22px;}'))
    s = b.el('e-heading', 'sc-sh', cfg={'tag': 'h3', 'title': 'How do you stop denials?'}, css=(
        f'{F} font-size: 22px; line-height: 32px; font-weight: 400; color: #000000; width: 100%; margin: 0px 0px 6px 0px; padding: 0px 0px 14px 0px; '
        'border-style: solid; border-color: rgba(7,24,45,0.1); border-width: 0px 0px 1px 0px;'))
    steps = [('Verify eligibility and prior auth before the visit', 'so coverage gaps never reach the claim.'),
             ('Scrub every claim before it goes out', '— our AI Rule Engine checks it against 3M+ payer rules.'),
             ('Appeal fast with the right documents', '— triaged by root cause and usually filed within 48 hours.'),
             ('Close the loop on every denial', 'by feeding each root cause back into front-end edits.')]
    for i, (lead, rest) in enumerate(steps):
        x = para(b, f'st{i}n', str(i + 1), ('font-size: 12px; line-height: 16px; font-weight: 600; color: #1171A1; margin: 0px; flex-shrink: 0; '
                                            'display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 50%; background-color: rgba(17,113,161,0.1);'))
        x += para(b, f'st{i}t', f'<strong>{lead}</strong> {rest}', 'font-size: 15px; line-height: 26px; color: #4F4F4F; margin: 0px; & strong{font-weight: 600;}')
        last = i == len(steps) - 1
        s += b.el('e-flexbox', f'st{i}', x, css=('display: flex; flex-direction: row; align-items: flex-start; gap: 14px; width: 100%; padding: 14px 0px; '
                                                 + ('' if last else 'border-style: solid; border-color: rgba(7,24,45,0.06); border-width: 0px 0px 1px 0px;')))
    stepsc = b.el('e-flexbox', 'sc-steps', s, css=(f'display: flex; flex-direction: column; width: 100%; padding: 28px 30px 16px 30px; border-radius: 20px; '
                                                   f'background-color: rgba(255,255,255,0.5); {SH} {GLASS} @media(--mobile){{padding: 22px 20px 10px 20px;}}'))
    right = b.el('e-flexbox', 'sc-right', costc + stepsc, css='display: flex; flex-direction: column; gap: 24px; padding: 0px; flex: 1 1 44%; min-width: 0px; @media(--tablet_extra){flex: 1 1 auto; width: 100%;}')
    row = b.el('e-flexbox', 'sc-row', left + right, css=('display: flex; flex-direction: row; align-items: flex-start; gap: 32px; width: 100%; padding: 0px; '
                                                         '@media(--tablet_extra){flex-direction: column; gap: 32px;}'))
    wrap = b.el('e-flexbox', 'sc-wrap', head + row, css='display: flex; flex-direction: column; align-items: flex-start; width: 100%; max-width: 1475px; padding: 0px;')
    return section(b, 'sc', wrap, 'bg-cause', 109, 79)


# ---------------------------------------------------------------- D. How we fix + case study
def fix(b):
    k = pill(b, 'sd-pill', 'How MedCare MSO fixes it')
    k += h2(b, 'sd-h2', 'We stop denials before submission — and win back the ones that slip through', 57, 1360)
    cards = [('icon-flag', 'Prevent at the source', "Our AI Rule Engine scores every claim against 3M+ payer rules and flags denial risk before it's ever submitted."),
             ('icon-clock', 'Resolve fast', 'Denied and underpaid claims are triaged by root cause and appealed with payer-specific documentation, usually within 48 hours.'),
             ('icon-edit', 'Fix it permanently', 'Every root cause feeds back into front-end edits, so the same denial reason stops recurring month after month.')]
    g = ''
    for i, (ic, t, p) in enumerate(cards):
        c = image(b, f'sd{i}i', ic, 'width: 43px; height: 43px; display: block; margin: 0px 0px 18px 0px;')
        c += b.el('e-heading', f'sd{i}t', cfg={'tag': 'h3', 'title': t}, css=f'{F} font-size: 22px; line-height: 32px; font-weight: 400; color: #000000; margin: 0px 0px 19px 0px;')
        c += para(b, f'sd{i}p', p, 'font-size: 16px; line-height: 28px; color: #4F4F4F; margin: 0px; @media(--mobile){font-size: 15px; line-height: 26px;}')
        g += b.el('e-flexbox', f'sd{i}', c, css=f'display: flex; flex-direction: column; align-items: flex-start; padding: 28px 24px 24px 27px; border-radius: 30px; background-color: rgba(255,255,255,0.5); {GLASS} @media(--mobile){{border-radius: 24px;}}')
    pw = para(b, 'sd-pw', 'Powered by', 'font-size: 22px; line-height: 32px; color: #000000; text-align: center; margin: 20px 0px 23px 0px; @media(--tablet_extra){margin: 8px 0px 16px 0px;}')
    for i, t in enumerate(['Consus AI Rule Engine', 'Denial Management Services']):
        pw += para(b, f'sd-p{i}', t, ('font-size: 22px; line-height: 32px; color: #000000; text-align: center; margin: 0px; width: 100%; '
                                      f'display: flex; align-items: center; justify-content: center; min-height: 93px; padding: 16px 20px; border-radius: 30px; background-color: rgba(255,255,255,0.5); {GLASS} '
                                      '@media(--mobile){font-size: 19px; line-height: 28px; min-height: 76px;}'))
    g += b.el('e-flexbox', 'sd-pwr', pw, css='display: flex; flex-direction: column; gap: 12px; padding: 0px; min-width: 0px; @media(--tablet_extra){grid-column: 1 / -1;}')
    k += b.el('e-div-block', 'sd-grid', g, css=(
        'display: grid; grid-template-columns: repeat(3, minmax(0, 343fr)) minmax(0, 411fr); gap: 12px; width: 100%; max-width: 1476px; padding: 0px; '
        '@media(--tablet_extra){grid-template-columns: repeat(3, minmax(0, 1fr));} @media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} '
        '@media(--mobile){grid-template-columns: minmax(0, 1fr);}'))
    chip = para(b, 'sd-chip', 'Proven result · EHP LLC', ('font-size: 14px; line-height: 19.6px; font-weight: 500; color: #FFFFFF; margin: 0px; width: max-content; '
                                                         f'padding: 11px 30px; border-radius: 61px; border: 1px solid #B8CEDB; background-color: rgba(154,189,202,0.2); {GLASS}'))
    lc = chip + b.el('e-heading', 'sd-ch', cfg={'tag': 'h3', 'title': 'How one practice cut denials 87% and unlocked months of stuck revenue'}, css=(
        f'{F} font-size: 42px; line-height: 62px; font-weight: 400; letter-spacing: -0.84px; color: #FFFFFF; max-width: 604px; margin: 12px 0px 0px 0px; '
        '@media(--laptop){font-size: 36px; line-height: 52px;} @media(--mobile){font-size: 28px; line-height: 40px;}'))
    left = b.el('e-flexbox', 'sd-cl', lc, css='display: flex; flex-direction: column; align-items: flex-start; padding: 0px; flex: 1 1 0px; min-width: 0px; @media(--tablet){flex: 1 1 auto; width: 100%;}')
    st = ''
    for i, (v, l) in enumerate([('87%', 'Denial reduction'), ('59%', 'Fewer A/R days'), ('$5K→$50K', 'Monthly collections')]):
        x = para(b, f'sd-s{i}v', v, 'font-size: 42px; line-height: 44px; color: #DAF6B6; margin: 0px; white-space: nowrap; @media(--mobile){font-size: 34px; line-height: 40px;}')
        x += para(b, f'sd-s{i}l', l, 'font-size: 16px; line-height: 32px; color: #FFFFFF; margin: 0px;')
        st += b.el('e-div-block', f'sd-s{i}', x, css='display: flex; flex-direction: column; padding: 0px;')
    right = b.el('e-div-block', 'sd-cr', st, css=('display: grid; grid-template-columns: repeat(2, minmax(0, 267px)); gap: 40px 0px; padding: 0px; flex-shrink: 0; width: max-content; '
                                                  '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr)); width: 100%; gap: 28px 20px;}'))
    k += b.el('e-flexbox', 'sd-case', left + right, css=(
        'display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 40px; width: 100%; max-width: 1476px; min-height: 316px; '
        'padding: 37px 74px 50px 87px; margin: 60px 0px 0px 0px; border-radius: 20px; background-color: #1A6F99; '
        f"background-image: url('{S.bgurl('banner-case')}'); background-size: 100% 100%; box-shadow: 0px 51px 64px 0px rgba(89,89,89,0.2); "
        '@media(--laptop){padding: 37px 48px 44px 56px;} @media(--tablet){flex-direction: column; align-items: flex-start; padding: 36px 32px;} '
        '@media(--mobile){padding: 30px 22px; margin: 40px 0px 0px 0px;}'))
    return section(b, 'sd', k, 'bg-fix', 80, 98, attrs=[{'key': 'id', 'value': 'how-we-fix'}])


# ---------------------------------------------------------------- E. FAQ
def faq(b):
    k = pill(b, 'se-pill', 'Questions')
    b.style['se-pill'] = b.style['se-pill'].replace('width: 248px', 'width: 166px')
    k += h2(b, 'se-h2', 'Denial questions practices ask us', 32, 1360)
    qa = [('What is the most common reason claims get denied?',
           "Eligibility and prior-authorization errors are the leading preventable cause — the coverage or approval wasn't confirmed before the "
           'service. Coding and documentation issues follow close behind.'),
          ('How quickly can denials be appealed?',
           'Denied and underpaid claims are triaged by root cause and appealed with payer-specific documentation, usually within 48 hours.'),
          ('Can you reduce denials without replacing our EHR?',
           'Yes. The work happens before and after submission — eligibility checks, AI Rule Engine claim scoring against 3M+ payer rules, '
           'and root-cause fixes fed back into front-end edits — so there is no need to change the EHR your team already uses.')]
    items = ''
    for i, (q, a) in enumerate(qa):
        title = b.el('e-accordion-item-title', f'fq{i}tt', b.el('e-heading', f'fq{i}q', cfg={'tag': 'h3', 'title': q}, css=(
            f'{F} font-size: 28px; line-height: 37px; font-weight: 400; color: #000000; margin: 0px; '
            '@media(--tablet){font-size: 22px; line-height: 32px;} @media(--mobile){font-size: 18px; line-height: 27px;}')),
                     css='padding: 0px; flex: 1 1 auto; min-width: 0px;')
        icon = b.el('e-accordion-item-icon', f'fq{i}ic', b.el('e-svg', f'fq{i}ii', cfg={'svg': {'id': S.mid('icon-faq')}}, css='width: 42px; height: 42px; display: block; @media(--mobile){width: 32px; height: 32px;}'),
                    css='width: 42px; height: 42px; padding: 0px; flex: 0 0 auto; display: inline-flex; align-items: center; justify-content: center; @media(--mobile){width: 32px; height: 32px;}')
        head = b.el('e-accordion-item-header', f'fq{i}h', title + icon, css=(
            'display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 30px 30px 30px 45px; cursor: pointer; '
            '@media(--mobile){padding: 20px 16px 20px 20px; gap: 12px;}'))
        body = b.el('e-accordion-item-content', f'fq{i}c', para(b, f'fq{i}a', a, 'font-size: 16px; line-height: 32px; color: #4F4F4F; margin: 0px; max-width: 1269px; @media(--mobile){font-size: 15px; line-height: 28px;}'),
                    css='padding: 0px 45px 30px 45px; @media(--mobile){padding: 0px 20px 20px 20px;}')
        items += b.el('e-accordion-item', f'fq{i}', head + body, css='display: block; padding: 0px; border-radius: 20px; background-color: #FFFFFF; overflow: hidden;')
    acc = b.el('e-accordion', 'fq', items, cfg={'default_state': 'first_expanded', 'max_expanded': 'one', 'show_icon': True, 'faq_schema': True},
               css='display: flex; flex-direction: column; gap: 14px; width: 100%; padding: 0px;')
    k += b.el('e-flexbox', 'se-panel', acc, css=(f'display: flex; flex-direction: column; width: 100%; max-width: 1473px; padding: 27px 19px; {CARD} '
                                                 '@media(--mobile){padding: 12px 8px;}'))
    return section(b, 'se', k, 'bg-faq', 99, 78)


# ---------------------------------------------------------------- F. CTA
def cta(b):
    l = b.el('e-heading', 'sf-h2', cfg={'tag': 'h2', 'title': 'See exactly why your claims are being denied'}, css=(
        f'{F} font-size: 58px; line-height: 72px; font-weight: 400; letter-spacing: -1.16px; color: #FFFFFF; max-width: 701px; margin: 0px 0px 25px 0px; '
        '@media(--laptop){font-size: 48px; line-height: 60px;} @media(--tablet){font-size: 38px; line-height: 50px;} @media(--mobile){font-size: 30px; line-height: 40px;}'))
    l += para(b, 'sf-p', 'A free denial audit reviews your recent denials, finds the root causes, and shows the revenue you can recover — no obligation.',
              'font-size: 16px; line-height: 32px; color: #FFFFFF; max-width: 689px; margin: 0px; @media(--mobile){font-size: 15px; line-height: 28px;}')
    left = b.el('e-flexbox', 'sf-l', l, css='display: flex; flex-direction: column; padding: 0px; flex: 1 1 0px; min-width: 0px; @media(--tablet){flex: 1 1 auto; width: 100%;}')
    r = green_button(b, 'sf-b1', 'Get a free denial audit', DEMO, '#FFFFFF')
    r += text_link(b, 'sf-b2', 'Explore all challenges', None, 'arrow-white', '#FFFFFF')
    right = b.el('e-flexbox', 'sf-r', r, css='display: flex; flex-wrap: wrap; align-items: center; gap: 16px 33px; padding: 0px; flex-shrink: 0; width: max-content; max-width: 100%;')
    k = b.el('e-flexbox', 'sf-box', left + right, css=(
        'display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 40px; width: 100%; max-width: 1476px; min-height: 336px; '
        'padding: 44px 77px 59px 87px; border-radius: 20px; background-color: #1A6F99; '
        f"background-image: url('{S.bgurl('banner-cta')}'); background-size: 100% 100%; box-shadow: 0px 51px 64px 0px rgba(89,89,89,0.2); "
        '@media(--laptop){padding: 44px 48px 52px 56px;} @media(--tablet){flex-direction: column; align-items: flex-start; padding: 40px 32px;} '
        '@media(--mobile){padding: 32px 22px;}'))
    return section(b, 'sf', k, 'bg-cta', 78, 222)


SECTIONS = [hero, cost, cause, fix, faq, cta]


def payload(mode='replace_children', dry=False):
    b = B()
    xml = ''.join(f(b) for f in SECTIONS)
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes,
            'mode': mode, 'dry_run': dry}
