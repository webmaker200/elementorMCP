"""Case studies archive -- demo page 412016 (to be set as the case-study archive later), Elementor V4, from
"Case Study Design Brief _ Case Studies copy.html".

Brief (same rules as the Golden State case study):
- site header / footer come from the site templates (not built here);
- content is the design's text and card data word for word (11 case studies, incl. ODAT Services, which links to the
  production site like every other card);
- no new global classes: sections use parent-container, H1 heading-main, H2 specialties-heading, copy global-text;
  everything else is a local style on the element;
- columns use percentage widths (no flex-basis); card grids use e-grid tracks with tablet / mobile columns;
- images/icons are Media Library items; the two new photos are WebP under 100 KB.
- The design filters cards with a script; here each filter is a V4 tab with its own card grid (no custom JS).
  V4 has no show/hide toggle, so the All tab lists every card and the design's "Show all" button is not built.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PID = 412016
SITE = 'https://medcaremso.com'
DEMO = f'{SITE}/request-demo/'
MEDIA = json.load(open(os.path.join(HERE, '..', 'media.json')))
HERO_IMG = MEDIA['case-studies-hero-portrait']['url']
STRESS = MEDIA['cardiac-stress-test-team']['id']
ARROW, ARROW_W = 410969, 411130  # salus-arrow-btn (#1171A1), chal-arrow-white

INK, SLATE, MUTED, ACC = '#14212B', '#4A5966', '#6B7A87', '#0367A1'
F = 'font-family: var(--Poppins);'
GRAD = 'linear-gradient(95deg, #023B5C 0%, #0367A1 45%, #3A96CC 100%)'
UP = 'linear-gradient(95deg, #486323 0%, #5E8A2C 50%, #6E9E36 100%)'
CLIP = '-webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;'
GRAD_TEXT = f'background-image: {GRAD}; {CLIP}'
UP_TEXT = f'background-image: {UP}; {CLIP}'
BAND = ('background-color: #023B5C; background-image: radial-gradient(circle at 12% 0%, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0) 30%), '
        'radial-gradient(circle at 96% 100%, rgba(156,216,246,0.30) 0%, rgba(156,216,246,0) 32%), '
        'radial-gradient(130% 160% at 0% 0%, #0B6AA6 0%, #023B5C 52%, #14212B 100%); '
        'box-shadow: 0px 40px 90px -40px rgba(2,40,66,0.5); color: #FFFFFF;')
BLUR = 'backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%);'
SH = 'inset 0px 0px 0px 1px rgba(255,255,255,0.7), 0px 0px 0px 1px rgba(3,103,161,0.08)'
GLASS = f'background-color: rgba(255,255,255,0.55); {BLUR} box-shadow: {SH}, 0px 20px 50px -30px rgba(2,40,66,0.25);'

CASES = [  # design data, in the design's order (newest first)
    dict(k='gs', client='Golden State Heart &amp; Vascular', tag='A/R recovery', cat='ar', new=True, img=STRESS, pos='70% 50%', kpi='$1.8M+',
         label='Aged A/R recovered, Aug 2025 – Jul 2026', title='How Golden State Heart &amp; Vascular recovered $1.8M+ in aged A/R',
         desc='How a focused 30+ day A/R recovery and denial management strategy recovered $1.8M+ in aged receivables.',
         href=f'{SITE}/case-study/golden-state-heart-vascular-aged-ar-recovery/'),
    dict(k='so', client='Sophus · AI coder', tag='AI coding', cat='ai', img=409632, kpi='5x', label='Coding throughput · 95% accuracy',
         title='50,000+ claims later: 5x coding throughput while maintaining 95% accuracy',
         desc='Production-scale laboratory coding results showing how Sophus reduced average coding time while preserving measured coding accuracy.',
         href=f'{SITE}/case-study/50000-claims-coding-throughput-95-percent-accuracy/'),
    dict(k='od', client='ODAT Services', tag='Claim recovery', cat='ar', img=411229, pos='50% 20%', frm='$65K', kpi='$140K',
         label='Monthly collections · ~$80K recovered', title='How ODAT Services grew from $65K to $140K in collections with MedCare MSO',
         desc='Here’s how ODAT Services recovered $80K in revenue and got their monthly collections to $140K monthly.',
         href=f'{SITE}/case-study/odat-services-65k-to-140k-collections/'),
    dict(k='dt', client='DT Nephrology', tag='Medical billing', cat='billing', img=401725, kpi='$28K', label='Monthly collections',
         title='How we helped DT Nephrology achieve $28,000 in monthly collections',
         desc='See how DT Nephrology achieved $28,000 in monthly collections after partnering with MedCare MSO.',
         href=f'{SITE}/case-study/dt-nephrology-28k-monthly-collections/'),
    dict(k='eh', client='EHP LLC', tag='Home health billing', cat='billing', img=399625, frm='$5K', kpi='$50K',
         label='Monthly collections · 95% collection ratio', title='How we took EHP LLC’s home health billing from $5K to $50K monthly collections',
         desc='See how MedCare MSO took EHP LLC’s collection ratio to 95% from 45%.',
         href=f'{SITE}/case-study/ehp-llc-home-health-billing-from-5k-to-50k/'),
    dict(k='id', client='ID Labs', tag='Credentialing', cat='cred', img=397968, kpi='$347K', label='Lost revenue recovered',
         title='How we recovered $347K in lost revenue for ID Labs through strategic credentialing',
         desc='See how MedCare MSO recovered $347K in lost revenue.',
         href=f'{SITE}/case-study/recovered-347k-lost-revenue-strategic-credentialing/'),
    dict(k='cc', client='C&amp;CCC', tag='Revenue cycle', cat='billing', img=397387, frm='$160K', kpi='$1.5M+',
         label='Monthly collections · A/R days cut to 32', title='How C&amp;CCC collections grew from $160K to $1.5M+ monthly and cut A/R days to 32',
         desc='See how a practice scaled from $160K to $1.5M monthly with precision.',
         href=f'{SITE}/case-study/how-c-and-ccc-collections-grew-revenue-and-reduced-ar-days/'),
    dict(k='gl', client='GLML', tag='A/R recovery', cat='ar', img=395073, kpi='56%', label='Revenue growth · 76% aged A/R recovery',
         title='GLML achieves 56% revenue growth and 76% aged A/R recovery with MedCare MSO',
         desc='Discover the process behind a 95% collection ratio.',
         href=f'{SITE}/case-study/glml-achieves-56-revenue-growth-and-76-aged-ar-recovery-with-medcare-mso-partnership/'),
    dict(k='sw', client='SWCA', tag='Collections', cat='billing', img=392590, kpi='35%', label='Higher monthly collections',
         title='How MedCare MSO lifted SWCA’s monthly collections by 35%', desc='Discover the process behind a 95% collection ratio.',
         href=f'{SITE}/case-study/how-medcare-mso-lifted-swcas-monthly-collections/'),
    dict(k='oc', client='Oceana Gastroenterology', tag='Denial management', cat='denial', img=390987, kpi='30%', label='More, from 2,000 denied claims',
         title='Oceana Gastroenterology’s journey to a stabilized reimbursement cycle with MedCare MSO',
         desc='See how 2,000 denied claims turned into 30% more.',
         href=f'{SITE}/case-study/oceana-gastroenterologys-journey-to-a-stabilized-reimbursement-cycle-with-medcare-mso/'),
    dict(k='cl', client='CCL', tag='Medical billing', cat='billing', img=395040, kpi='91%', label='First-pass rate · 30% A/R reduction',
         title='How MedCare MSO transformed CCL’s billing with a 91% first-pass rate and 30% A/R reduction',
         desc='Explore the full transformation story.', href=f'{SITE}/case-study/how-medcare-mso-transformed-ccls-billing/'),
]
FILTERS = [('all', 'All'), ('ar', 'A/R recovery'), ('billing', 'Billing &amp; collections'), ('denial', 'Denial management'),
           ('cred', 'Credentialing'), ('ai', 'AI coding')]


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


def grid(cid, kids, css=''):
    # e-grid base: padding 10px and grid-template-rows repeat(2, 1fr) (adds an empty second row)
    return b.el('e-grid', cid, kids, css='padding: 0px; grid-template-rows: auto; ' + css)


def p(cid, html, css='', cls=('global-text',)):
    return b.el('e-paragraph', cid, cfg={'paragraph': html}, css=css, cls=list(cls) if cls else None)


def h(cid, tag, title, css='', cls=None):
    return b.el('e-heading', cid, cfg={'tag': tag, 'title': title}, css=css, cls=cls)


def img(cid, mid, css='', alt=''):
    return b.el('e-image', cid, cfg={'image': {'src': {'id': mid, 'alt': alt}, 'size': 'full'}}, css=css)


def t(size, lh, color, weight=300, ls=None, extra=''):
    return (f'{F} font-size: {size}px; line-height: {lh}; font-weight: {weight}; color: {color}; margin: 0px; '
            + (f'letter-spacing: {ls}; ' if ls else '') + extra)


def eyebrow(cid, label, color=ACC, css=''):
    return p(cid, label, css=t(12, 1.4, color, 500, '0.12em', 'text-transform: uppercase; ' + css))


def section(cid, kids, anchor=None, css=''):
    cfg = {'tag': 'section'}
    if anchor:
        cfg['_cssid'] = anchor
    return flex(cid, kids, cls=['parent-container'], cfg=cfg, css=(
        'display: flex; flex-direction: column; align-items: stretch; gap: 24px; width: 100%; position: relative; '
        'padding-block-start: 56px; padding-block-end: 56px; scroll-margin-top: 90px; '
        '@media(--tablet){padding-block-start: 40px; padding-block-end: 40px;} '
        '@media(--mobile){padding-block-start: 28px; padding-block-end: 28px;} ' + css))


def circle(cid, size, color, mid, icon=16, css=''):
    return box(cid, img(f'{cid}i', mid, css=f'display: block; width: {icon}px; height: {icon}px;'), css=(
        f'display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: {size}px; height: {size}px; '
        f'border-radius: 999px; border: 2px solid {color}; transition: background-color 0.25s ease; ' + css))


def pill(cid, label, url, light=False, height=56, down=False, css=''):
    """Glass pill link with an arrow circle; simple hover (tint + shadow)."""
    color = '#FFFFFF' if light else ACC
    look = ('background-color: rgba(255,255,255,0.10); box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.35); '
            '&:hover{background-color: rgba(255,255,255,0.22); box-shadow: 0px 14px 30px -12px rgba(0,20,35,0.45);}') if light else (
            f'background-color: rgba(255,255,255,0.35); {BLUR} box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.8), 0px 12px 28px -16px rgba(2,40,66,0.3); '
            '&:hover{background-color: rgba(3,103,161,0.08); box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.8), 0px 18px 34px -14px rgba(3,103,161,0.45);}')
    size = 40 if height >= 56 else 36
    arrow = circle(f'{cid}c', size, color, ARROW_W if light else ARROW, css='transform: rotate(90deg);' if down else '')
    return box(cid, p(f'{cid}t', label, css=t(15, 1, color, 500, None, 'white-space: nowrap;')) + arrow, link=url, css=(
        f'display: inline-flex; flex-direction: row; align-items: center; gap: 12px; width: max-content; max-width: 100%; height: {height}px; '
        f'padding: 0px {(height - size) // 2}px 0px {26 if height >= 56 else 22}px; border-radius: 999px; border: 2px solid {color}; '
        f'text-decoration: none; cursor: pointer; transition: background-color 0.25s ease, box-shadow 0.25s ease; {look} ' + css))


# ---------------------------------------------------------------- 1. hero
def hero():
    crumb = flex('hc', p('hc-1', 'Resources', css=t(13, 1.5, MUTED, 400)) + p('hc-2', '/', css=t(13, 1.5, MUTED, 400))
                 + p('hc-3', 'Case studies', css=t(13, 1.5, INK, 400)),
                 css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 10px;')
    h1 = h('h1', 'h1', 'Case <span>studies</span>', cls=['heading-main'], css=(
        f'font-weight: 300; font-size: 112px; line-height: 0.94; letter-spacing: -0.055em; color: {INK}; margin: 0px; '
        f'& span{{display: block; width: max-content; font-weight: 400; padding-bottom: 0.06em; {GRAD_TEXT}}} '
        '@media(--tablet_extra){font-size: 96px;} @media(--tablet){font-size: 88px;} @media(--mobile_extra){font-size: 72px;} @media(--mobile){font-size: 56px;}'))
    sub = box('hs', p('hs-1', 'Strategic insights, perspectives, and industry trends', css=t(24, 1.35, INK, 400, '-0.02em', '@media(--mobile){font-size: 20px;}'))
              + p('hs-2', 'Each example shared here highlights how the right strategy, team, and tools can turn operational hurdles into long-term wins.',
                  css=t(17, 1.7, SLATE, 300, None, '@media(--mobile){font-size: 16px;}')),
              css='display: flex; flex-direction: column; gap: 12px; max-width: 480px;')
    btns = flex('hb', pill('hb1', 'Browse case studies', '#library', down=True) + pill('hb2', 'Talk to a billing expert', DEMO),
                css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 14px;')
    left = box('h-l', crumb + h1 + sub + btns, css=(
        'display: flex; flex-direction: column; gap: 26px; width: 48%; max-width: 580px; @media(--tablet){width: 100%;}'))
    card = box('h-card', eyebrow('hcd-e', 'C&amp;CCC', ACC, 'font-size: 11px;')
               + flex('hcd-r', p('hcd-f', '$160K', css=t(16, 1.4, MUTED, 300, None, 'text-decoration: line-through; text-decoration-color: rgba(107,122,135,0.5);'))
                      + p('hcd-n', '$1.5M+', css=t(36, 1, 'transparent', 200, '-0.045em', UP_TEXT)),
                      css='display: flex; flex-direction: row; align-items: baseline; gap: 8px;')
               + p('hcd-l', 'Monthly collections', css=t(13, 1.5, INK, 400)), css=(
        f'display: flex; flex-direction: column; gap: 6px; width: 240px; align-self: flex-end; padding: 20px 22px; border-radius: 16px; '
        f'background-color: rgba(255,255,255,0.55); {BLUR} box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.7), 0px 30px 70px -30px rgba(2,40,66,0.35); '
        'transition: transform 0.3s ease; &:hover{transform: translateY(-4px);} @media(--tablet){align-self: flex-start;}'))
    row = flex('h-row', left + card, css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 40px; width: 100%; '
        '@media(--tablet){flex-direction: column; align-items: stretch; gap: 28px;}'))
    return section('s-hero', row, css=(
        'justify-content: center; min-height: 720px; padding-block-start: 56px; padding-block-end: 72px; '
        f"background-image: url('{HERO_IMG}'); background-repeat: no-repeat; background-position: right top; background-size: auto 100%; "
        '@media(--tablet){min-height: 0px; padding-block-start: 380px; padding-block-end: 40px; background-size: auto 420px;} '
        '@media(--mobile){padding-block-start: 270px; padding-block-end: 28px; background-size: 100% auto; background-position: center top;}'))


# ---------------------------------------------------------------- 2. featured · newest
def kpi_chip(cid, num, label):
    return box(cid, p(f'{cid}n', num, css=t(30, 1, 'transparent', 300, '-0.045em', UP_TEXT + ' width: max-content; @media(--tablet_extra){font-size: 24px;} @media(--mobile){font-size: 20px;}'))
               + p(f'{cid}l', label, css=t(12, 1.35, SLATE, 400, None, '@media(--mobile){font-size: 11px;}')), css=(
        f'display: flex; flex-direction: column; gap: 4px; padding: 14px 16px; border-radius: 16px; background-color: rgba(255,255,255,0.82); {BLUR} '
        'box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.7), 0px 20px 40px -24px rgba(2,40,66,0.5); @media(--mobile){padding: 10px 10px;}'))


def featured():
    head = flex('fe-h', eyebrow('fe-e', 'Featured · Newest', ACC, 'white-space: nowrap;')
                + box('fe-ln', '', css='flex-grow: 1; height: 1px; background-color: rgba(3,103,161,0.12);'),
                css='display: flex; flex-direction: row; align-items: center; gap: 16px; width: 100%;')
    chip = ('display: inline-flex; align-items: center; height: 28px; padding: 0px 12px; border-radius: 999px; '
            'background-color: rgba(255,255,255,0.12); box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.25); white-space: nowrap;')
    chips = flex('fe-cs', p('fe-c1', 'Golden State Heart &amp; Vascular', css=t(12, 1, '#FFFFFF', 500, None, chip + (
                     ' gap: 8px; &::before{content: ""; width: 7px; height: 7px; border-radius: 999px; background-color: #9CD8F6;}')))
                 + p('fe-c2', 'A/R recovery', css=t(12, 1, '#FFFFFF', 500, None, chip))
                 + p('fe-c3', 'Aug 2025 – Jul 2026', css=t(12, 1, '#FFFFFF', 500, None, chip)),
                 css='display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px;')
    read = box('fe-rm', p('fe-rmt', 'Read more', css=t(15, 1, '#FFFFFF', 500, None, 'white-space: nowrap;')) + circle('fe-rmc', 36, '#FFFFFF', ARROW_W), css=(
        'display: inline-flex; flex-direction: row; align-items: center; gap: 12px; width: max-content; height: 48px; padding: 0px 4px 0px 22px; margin-top: 4px; '
        'border-radius: 999px; border: 2px solid #FFFFFF; background-color: rgba(255,255,255,0.10); box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.35); '
        'transition: background-color 0.25s ease;'))
    left = box('fe-l', chips + h('fe-t', 'h2', 'How Golden State Heart &amp; Vascular recovered $1.8M+ in aged A/R', css=t(
        34, 1.15, '#FFFFFF', 300, '-0.035em', '@media(--tablet_extra){font-size: 30px;} @media(--mobile){font-size: 24px;}'))
               + p('fe-p', 'How a focused 30+ day A/R recovery and denial management strategy recovered $1.8M+ in aged receivables.',
                   css=t(15, 1.65, 'rgba(255,255,255,0.88)', 400, None, 'max-width: 500px;'))
               + read, css='display: flex; flex-direction: column; justify-content: center; gap: 16px; padding: 40px; @media(--mobile){padding: 24px 20px;}')
    photo = box('fe-r', img('fe-img', STRESS, alt='Cardiology team monitoring a patient during a cardiac stress test', css=(
        'position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; max-width: none; object-fit: cover; object-position: 70% 50%; transition: transform 0.5s ease;'))
        + box('fe-ov', '', css='position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(2,30,48,0.55), rgba(2,30,48,0) 55%);')
        + p('fe-tag', 'Featured · New', css=t(12, 1, '#FFFFFF', 500, None, (
            f'position: absolute; left: 14px; top: 14px; width: max-content; display: inline-flex; align-items: center; height: 30px; padding: 0px 14px; border-radius: 999px; '
            f'background-color: rgba(255,255,255,0.30); {BLUR} box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.45);')))
        + grid('fe-k', kpi_chip('fe-k1', '$1.8M+', 'Aged A/R recovered') + kpi_chip('fe-k2', '~$150K', 'Monthly from aged A/R')
               + kpi_chip('fe-k3', '$850K+', 'Previously in 90+ days'), css=(
            'position: absolute; left: 14px; right: 14px; bottom: 14px; width: calc(100% - 28px); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; '
            '@media(--mobile){left: 10px; right: 10px; bottom: 10px; width: calc(100% - 20px); gap: 6px;}')), css=(
        'position: relative; overflow: hidden; width: calc(100% - 20px); min-height: 340px; margin: 10px; border-radius: 16px; @media(--mobile){min-height: 300px;}'))
    card = b.el('e-div-block', 'fe', grid('fe-g', left + photo, css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: stretch; gap: 0px; @media(--tablet){grid-template-columns: 1fr;}')),
        cfg={'link': {'destination': CASES[0]['href']}}, css=(
        f'padding: 0px; display: block; position: relative; overflow: hidden; border-radius: 24px; text-decoration: none; {BAND} '
        'transition: transform 0.25s ease, box-shadow 0.25s ease; '
        '&:hover{transform: translateY(-4px); box-shadow: 0px 48px 90px -36px rgba(2,40,66,0.6);} '
        '&:hover img{transform: scale(1.03);} &:hover > div > div:first-child > div:last-child{background-color: rgba(255,255,255,0.22);}'))
    return section('s-feat', head + card, css='padding-block-start: 0px; @media(--tablet){padding-block-start: 0px;} @media(--mobile){padding-block-start: 0px;}')


# ---------------------------------------------------------------- 3. library: filter tabs + cards
def card(pre, c):
    k = pre + c['k']
    top = flex(f'{k}tp', p(f'{k}tg', c['tag'], css=t(11.5, 1, ACC, 500, None, (
        f'display: inline-flex; align-items: center; height: 26px; padding: 0px 11px; border-radius: 999px; white-space: nowrap; '
        f'background-color: rgba(255,255,255,0.82); {BLUR}')))
        + (p(f'{k}nw', 'New', css=t(11.5, 1, ACC, 500, None, (
            f'display: inline-flex; align-items: center; height: 26px; padding: 0px 11px; border-radius: 999px; border: 2px solid {ACC}; '
            f'background-color: rgba(255,255,255,0.35); {BLUR}'))) if c.get('new') else ''), css=(
        'position: absolute; left: 10px; top: 10px; right: 10px; width: calc(100% - 20px); display: flex; flex-direction: row; justify-content: space-between; gap: 8px;'))
    nums = ''
    if c.get('frm'):
        nums += p(f'{k}fr', c['frm'], css=t(13, 1, MUTED, 300, None, 'text-decoration: line-through;'))
        nums += p(f'{k}ar', '→', css=t(12, 1, MUTED, 400))
    nums += p(f'{k}kp', c['kpi'], css=t(26, 1, 'transparent', 300, '-0.045em', UP_TEXT + ' width: max-content;'))
    kpi = box(f'{k}kb', flex(f'{k}kr', nums, css='display: flex; flex-direction: row; align-items: baseline; gap: 6px;')
              + p(f'{k}kl', c['label'], css=t(11.5, 1.3, SLATE, 400)), css=(
        f'position: absolute; left: 10px; bottom: 10px; display: flex; flex-direction: column; gap: 4px; width: max-content; max-width: calc(100% - 20px); '
        f'padding: 10px 14px; border-radius: 12px; background-color: rgba(255,255,255,0.82); {BLUR} box-shadow: 0px 16px 30px -18px rgba(2,40,66,0.5);'))
    media = box(f'{k}m', img(f'{k}i', c['img'], alt=c['client'].replace('&amp;', '&'), css=(
        f"position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; object-fit: cover; object-position: {c.get('pos', '50% 30%')}; transition: transform 0.5s ease;"))
        + box(f'{k}ov', '', css='position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(2,30,48,0.5), rgba(2,30,48,0) 60%);')
        + top + kpi, css='position: relative; height: 168px; border-radius: 12px; overflow: hidden; background-color: #EAF5FF;')
    body = box(f'{k}b', p(f'{k}cl', c['client'], css=t(11, 1.4, MUTED, 500, '0.12em', 'text-transform: uppercase;'))
               + h(f'{k}h', 'h3', c['title'], css=t(16.5, 1.35, INK, 500, '-0.015em'))
               + p(f'{k}p', c['desc'], css=t(13.5, 1.55, SLATE, 300)),
               css='display: flex; flex-direction: column; gap: 8px; padding: 16px 8px 6px; flex-grow: 1;')
    foot = flex(f'{k}f', p(f'{k}ft', 'Read more', css=t(13.5, 1, ACC, 500)) + circle(f'{k}fc', 32, ACC, ARROW, 14, f'background-color: rgba(255,255,255,0.35); {BLUR}'), css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 10px 8px 4px; border-top: 1px solid rgba(3,103,161,0.08);'))
    return box(k, media + body + foot, link=c['href'], css=(
        f'display: flex; flex-direction: column; padding: 10px; border-radius: 16px; text-decoration: none; background-color: rgba(255,255,255,0.6); {BLUR} '
        'box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.75), 0px 0px 0px 1px rgba(3,103,161,0.08), 0px 24px 60px -32px rgba(2,40,66,0.25); '
        'transition: transform 0.25s ease, box-shadow 0.25s ease, background-color 0.25s ease; '
        '&:hover{transform: translateY(-4px); background-color: rgba(255,255,255,0.78); '
        'box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.75), 0px 0px 0px 1px rgba(3,103,161,0.12), 0px 30px 60px -28px rgba(2,40,66,0.32);} '
        f'&:hover img{{transform: scale(1.04);}} &:hover > div:last-child > div{{background-color: rgba(3,103,161,0.10);}}'))


def library():
    head = grid('lb-h', box('lb-hl', eyebrow('lb-e', 'All case studies', ACC, 'margin-bottom: 14px;')
                            + h('lb-t', 'h2', 'Real results, <span>real practices</span>', cls=['specialties-heading'], css=(
                                f'font-weight: 300; font-size: 48px; line-height: 1.1; letter-spacing: -0.04em; color: {INK}; margin: 0px; '
                                f'& span{{font-weight: 400; {GRAD_TEXT}}} @media(--tablet){{font-size: 40px;}} @media(--mobile){{font-size: 32px;}}')))
                + p('lb-p', 'Take a look at how we partner with healthcare organizations to deliver result-driven revenue cycle solutions that lead to real financial growth.',
                    css=t(16, 1.7, SLATE, 300)), css=(
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 64px; row-gap: 16px; align-items: end; '
        '@media(--tablet){grid-template-columns: 1fr;}'))
    tab_css = (f'{F} display: inline-flex; align-items: center; flex-shrink: 0; width: auto; height: 40px; padding: 0px 14px; border: 0px; border-radius: 999px; '
               f'font-size: 14px; font-weight: 400; line-height: 1; color: {INK}; background-color: transparent; cursor: pointer; white-space: nowrap; outline: none; '
               'transition: background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease; '
               '&:hover{background-color: rgba(255,255,255,0.7);} '
               f'&[aria-selected="true"]{{font-weight: 500; color: {ACC}; background-color: rgba(255,255,255,0.35); '
               f'box-shadow: inset 0px 0px 0px 2px {ACC}, inset 0px 1px 0px 0px rgba(255,255,255,0.8);}} '
               f'&:focus-visible{{box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.30);}}')
    tabs, panels = '', ''
    for i, (key, label) in enumerate(FILTERS):
        items = [c for c in CASES if key == 'all' or c['cat'] == key]
        tabs += b.el('e-tab', f'lt-{key}', p(f'lt-{key}l', f'{label}<span>{len(items)}</span>', css=(
            'margin: 0px; font: inherit; color: inherit; white-space: nowrap; & span{margin-inline-start: 8px; font-size: 12px; font-weight: 500; opacity: 0.7;}')), css=tab_css)
        cards = ''.join(card(f'{key[:2]}', c) for c in items)
        panels += b.el('e-tab-content', f'lc-{key}', grid(f'lg-{key}', cards, css=(
            'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; '
            '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile){grid-template-columns: 1fr;}')),
            css='display: block; width: 100%; padding: 0px;')
    menu = b.el('e-tabs-menu', 'lt', tabs, css=(
        f'display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: flex-start; gap: 4px; width: max-content; max-width: 100%; padding: 6px; '
        f'border-radius: 999px; overflow-x: auto; scrollbar-width: none; {GLASS} '
        '@media(--mobile){border-radius: 20px;}'))
    area = b.el('e-tabs-content-area', 'la', panels, css='display: block; width: 100%; padding: 0px;')
    tabs_el = b.el('e-tabs', 'lb-tabs', menu + area, cfg={'default-active-tab': 0}, css=(
        'display: flex; flex-direction: column; align-items: flex-start; gap: 24px; width: 100%; padding: 0px;'))
    return section('s-lib', head + tabs_el, anchor='library')


# ---------------------------------------------------------------- 4. callback band
def callback():
    left = box('cb-l', eyebrow('cb-e', 'Your growth, our promise', '#9CD8F6')
               + h('cb-h', 'h2', 'Schedule a free demo', cls=['specialties-heading'], css=(
                   'font-weight: 300; font-size: 48px; line-height: 1.06; letter-spacing: -0.045em; color: #FFFFFF; margin: 0px; '
                   '@media(--tablet){font-size: 42px;} @media(--mobile){font-size: 32px;}'))
               + p('cb-p', 'A member of our team will get in touch with you in 12 hours. If you’d like to talk to someone now, give us a call at 800-640-6409.',
                   css=t(16, 1.7, 'rgba(255,255,255,0.92)', 400, None, 'max-width: 520px;')),
               css='display: flex; flex-direction: column; gap: 20px; width: 48%; @media(--tablet){width: 100%;}')

    def line(i, lab, val, url, last=False):
        return box(f'cb-r{i}', p(f'cb-r{i}v', val, css=t(15, 1.5, '#FFFFFF', 400, None, 'order: 2; text-align: right; word-break: break-word;'))
                   + p(f'cb-r{i}l', lab, css=t(15, 1.5, 'rgba(255,255,255,0.75)', 400, None, 'order: 1;')), link=url, css=(
            f'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 12px; padding: 14px 0px {0 if last else 14}px; '
            'border-top: 1px solid rgba(255,255,255,0.2); text-decoration: none; '
            '&:hover p:first-child{text-decoration: underline; text-underline-offset: 4px;}'))
    right = box('cb-r', eyebrow('cb-re', 'Talk to a billing expert', '#9CD8F6')
                + pill('cb-b', 'Request demo', DEMO, light=True, css='display: flex; width: 100%; justify-content: space-between;')
                + box('cb-rows', line(0, 'Phone', '800-640-6409', 'tel:8006406409') + line(1, 'Email', 'info@medcaremso.com', 'mailto:info@medcaremso.com', True),
                      css='display: flex; flex-direction: column;'), css=(
        f'display: flex; flex-direction: column; gap: 18px; width: 44%; padding: 28px; border-radius: 16px; background-color: rgba(255,255,255,0.10); {BLUR} '
        'box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.25); @media(--tablet){width: 100%;} @media(--mobile){padding: 22px;}'))
    band = flex('cb', left + right, css=(
        f'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 48px; padding: 64px; border-radius: 24px; {BAND} '
        '@media(--tablet){flex-direction: column; align-items: stretch; gap: 32px; padding: 40px;} @media(--mobile){padding: 28px 22px;}'))
    return section('s-cb', band, anchor='callback', css='padding-block-end: 100px; @media(--tablet){padding-block-end: 64px;} @media(--mobile){padding-block-end: 44px;}')


SECTIONS = [hero, featured, library, callback]
PAGE_BG = ('background-color: #F3F8FC; background-image: '
           'radial-gradient(ellipse 1000px 1000px at 0% 0%, rgba(156,216,246,0.30) 0%, rgba(156,216,246,0) 60%), '
           'radial-gradient(ellipse 900px 900px at 100% 30%, rgba(156,216,246,0.22) 0%, rgba(156,216,246,0) 60%), '
           'radial-gradient(ellipse 900px 800px at 15% 60%, rgba(3,103,161,0.07) 0%, rgba(3,103,161,0) 60%), '
           'radial-gradient(ellipse 900px 900px at 90% 80%, rgba(156,216,246,0.20) 0%, rgba(156,216,246,0) 60%);')


def payload(mode='replace_children', dry=False):
    global b
    b = B()
    xml = flex('page', ''.join(f() for f in SECTIONS), css=(
        f'display: flex; flex-direction: column; align-items: stretch; gap: 0px; width: 100%; overflow-x: clip; {PAGE_BG}'))
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes, 'mode': mode, 'dry_run': dry}


if __name__ == '__main__':
    d = payload()
    print(len(json.dumps(d)), 'bytes', len(d['style']), 'styled elements')
