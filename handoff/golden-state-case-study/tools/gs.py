"""Golden State Heart & Vascular case study -- post 411939 (case-study), Elementor V4, from
"Case Study Design Brief _ Golden State Case Study v3.html".

Brief:
- site header / footer come from the site templates (not built here);
- content is the design's text, word for word;
- no new global classes: sections use parent-container, headings heading-main / specialties-heading, copy global-text;
  everything else is a local style on the element;
- columns use percentage widths (no flex-basis); card grids use e-grid tracks with tablet / mobile columns;
- icons are existing Media Library SVGs; the banner is a 1000x1200 WebP (77 KB) cropped from the supplied photo.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PID = 411939
BANNER = 411941
ICONS = {  # existing Media Library SVGs
    'issue': [406661, 411694, 403764, 411682, 403657, 411684],  # billing doc $, record submission, authorization, coding, claim check, A/R follow-up
    'arrow': 411264, 'arrow_white': 411130, 'check': 410377,
}

INK, SLATE, MUTED, ACC, ACC2 = '#14212B', '#4A5966', '#6B7A87', '#2F7D6B', '#7EB03E'
F = 'font-family: var(--Poppins);'
GRAD = 'linear-gradient(95deg, #2F7D6B 0%, #3E8F6A 40%, #0367A1 100%)'
GRAD_TEXT = (f'background-image: {GRAD}; -webkit-background-clip: text; background-clip: text; '
             '-webkit-text-fill-color: transparent; color: transparent;')
CTA_GRAD = 'linear-gradient(135deg, #4C8A33 0%, #2F7D6B 55%, #1F6E8C 100%)'
BAND = ('background-color: #2F7D6B; background-image: radial-gradient(circle at 88% 12%, rgba(255,255,255,0.20) 0%, rgba(255,255,255,0) 32%), '
        'radial-gradient(circle at 12% 92%, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0) 28%), '
        'linear-gradient(120deg, #2F7D6B 0%, #2A8571 35%, #1C6F8E 72%, #0367A1 100%); '
        'box-shadow: 0px 40px 90px -40px rgba(47,125,107,0.55); color: #FFFFFF;')
SH = 'inset 0px 0px 0px 1px rgba(255,255,255,0.7), 0px 0px 0px 1px rgba(3,103,161,0.08)'
GLASS = (f'background-color: rgba(255,255,255,0.55); backdrop-filter: blur(22px) saturate(180%); -webkit-backdrop-filter: blur(22px) saturate(180%); '
         f'box-shadow: {SH}, 0px 24px 60px -32px rgba(2,40,66,0.25); border-radius: 24px;')
LIFT = (f'transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease; '
        f'&:hover{{transform: translateY(-4px); background-color: rgba(255,255,255,0.72); box-shadow: {SH}, 0px 30px 60px -28px rgba(2,40,66,0.32);}}')
INNER = 'background-color: rgba(255,255,255,0.12); box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.25); border-radius: 20px;'


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
    return b.el('e-div-block', cid, kids, cfg=cfg or None, css='padding: 0px; min-width: 0px; ' + css)  # base adds 10px padding + min-width 30px


def flex(cid, kids, css='', cls=None, cfg=None):
    return b.el('e-flexbox', cid, kids, cfg=cfg, css=('padding: 0px; ' if not cls else '') + css, cls=cls)


def grid(cid, kids, css='', anchor=None):
    # e-grid base: padding 10px and grid-template-rows repeat(2, 1fr) (adds an empty second row)
    return b.el('e-grid', cid, kids, cfg={'_cssid': anchor} if anchor else None, css='padding: 0px; grid-template-rows: auto; ' + css)


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


def h2(cid, title, color=INK, css=''):
    return h(cid, 'h2', title, cls=['specialties-heading'], css=(
        f'font-weight: 300; font-size: 46px; line-height: 1.1; letter-spacing: -0.04em; color: {color}; margin: 0px; '
        '@media(--tablet){font-size: 38px;} @media(--mobile){font-size: 30px;} ' + css))


def body(cid, html, size=16, color=SLATE, css=''):
    return p(cid, html, css=t(size, 1.7, color, 300, None, '& strong{font-weight: 500; color: ' + INK + ';} @media(--mobile){font-size: 15px;} ' + css))


def section(cid, kids, anchor=None, css=''):
    cfg = {'tag': 'section'}
    if anchor:
        cfg['_cssid'] = anchor
    return flex(cid, kids, cls=['parent-container'], cfg=cfg, css=(
        'display: flex; flex-direction: column; align-items: stretch; gap: 32px; width: 100%; position: relative; '
        'padding-block-start: 60px; padding-block-end: 60px; scroll-margin-top: 90px; '
        '@media(--tablet){padding-block-start: 44px; padding-block-end: 44px;} '
        '@media(--mobile){padding-block-start: 32px; padding-block-end: 32px; gap: 24px;} ' + css))


def row(cid, kids, css='', align='flex-start'):
    return flex(cid, kids, css=(
        f'display: flex; flex-direction: row; justify-content: space-between; align-items: {align}; gap: 0px; width: 100%; padding: 0px; '
        '@media(--tablet){flex-direction: column; align-items: stretch; gap: 32px;} ' + css))


def col(cid, kids, w, css='', gap=20):
    return box(cid, kids, css=(
        f'display: flex; flex-direction: column; gap: {gap}px; width: {w}%; padding: 0px; '
        '@media(--tablet){width: 100%;} ' + css))


def big(cid, label, size=40, css=''):
    """Thin gradient number."""
    return p(cid, label, css=t(size, 1, 'transparent', 200, '-0.04em', GRAD_TEXT + ' width: max-content; max-width: 100%; ' + css))


def arrow_circle(cid, mid, color, css=''):
    return box(cid, img(f'{cid}i', mid, css='width: 18px; height: 18px; display: block; transition: filter 0.25s ease;'), css=(
        f'display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 40px; height: 40px; border-radius: 999px; '
        f'border: 2px solid {color}; transition: background-color 0.25s ease, border-color 0.25s ease; ' + css))


# ---------------------------------------------------------------- 1. hero + at a glance
def hero():
    crumb = flex('hc', p('hc-1', 'Case studies', css=t(13, 1.5, MUTED, 400))
                 + p('hc-2', '/', css=t(13, 1.5, MUTED, 400))
                 + p('hc-3', 'A/R recovery', css=t(13, 1.5, INK, 400))
                 + p('hc-4', 'Aug 2025 – Jul 2026', css=t(13, 1.5, ACC, 500, None, (
                     'display: inline-flex; align-items: center; gap: 8px; height: 28px; padding: 0px 12px; border-radius: 999px; margin-inline-start: 4px; '
                     'background-color: rgba(255,255,255,0.55); box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.7), 0px 0px 0px 1px rgba(3,103,161,0.1); '
                     f'&::before{{content: ""; width: 6px; height: 6px; border-radius: 999px; background-color: {ACC2};}}'))),
                 css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 10px; padding: 0px;')
    h1 = h('h1', 'h1', 'How Golden State Heart &amp; Vascular Recovered <span>$1.8M+ in Aged A/R</span>', cls=['heading-main'], css=(
        f'font-weight: 300; font-size: 62px; line-height: 1.04; letter-spacing: -0.045em; color: {INK}; margin: 0px; '
        f'& span{{font-weight: 400; {GRAD_TEXT}}} '
        '@media(--tablet_extra){font-size: 52px;} @media(--mobile_extra){font-size: 44px;} @media(--mobile){font-size: 36px;}'))
    lead = p('hl', 'How a focused 30+ day A/R recovery and denial management strategy recovered $1.8M+ in aged receivables',
             css=t(18, 1.65, SLATE, 300, None, 'max-width: 560px; @media(--mobile){font-size: 16px;}'))
    demo = box('hb1', p('hb1t', 'Book a demo', css=t(15, 1, ACC, 500, None, 'transition: color 0.25s ease;'))
               + arrow_circle('hb1c', ICONS['arrow'], ACC), link='#contact', css=(
        f'display: inline-flex; flex-direction: row; align-items: center; gap: 14px; width: max-content; height: 56px; padding: 0px 6px 0px 26px; '
        f'border-radius: 999px; border: 2px solid {ACC}; background-color: rgba(255,255,255,0.35); text-decoration: none; cursor: pointer; '
        'box-shadow: 0px 12px 30px -16px rgba(47,125,107,0.45); transition: background-color 0.25s ease, box-shadow 0.25s ease; '
        f'&:hover{{background-color: {ACC}; box-shadow: 0px 16px 34px -14px rgba(47,125,107,0.6);}} '
        '&:hover p{color: #FFFFFF;} &:hover div{border-color: #FFFFFF;} &:hover img{filter: brightness(0) invert(1);}'))
    results = box('hb2', p('hb2t', 'See the results ↓', css=t(15, 1, ACC, 500, None, 'transition: color 0.2s ease;')), link='#results', css=(
        'display: inline-flex; align-items: center; width: max-content; height: 56px; padding: 0px 4px; text-decoration: none; '
        '&:hover p{color: #1F6E8C; text-decoration: underline; text-underline-offset: 4px;}'))
    btns = flex('hbs', demo + results, css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 24px; padding: 0px; margin-top: 8px;')

    def kpi(i, num, label):
        return box(f'hk{i}', big(f'hk{i}n', num, 40, '@media(--tablet_extra){font-size: 34px;}') + p(f'hk{i}l', label, css=t(13, 1.5, SLATE, 400)), css=(
            'display: flex; flex-direction: column; gap: 10px; padding: 0px 24px; '
            + ('' if i == 0 else 'border-left: 1px solid rgba(3,103,161,0.1); ')
            + '@media(--mobile){padding: 16px 20px; border-left: 0px; '
            + ('' if i == 0 else 'border-top: 1px solid rgba(3,103,161,0.1);') + '}'))
    kpis = grid('hk', kpi(0, '$1.8M+', 'Aged A/R recovered') + kpi(1, '~$150K', 'Monthly from aged A/R') + kpi(2, '$850K+', 'Previously in 90+ days'), css=(
        f'display: grid; grid-template-columns: repeat(3, 1fr); gap: 0px; width: 100%; padding: 24px 0px; margin-top: 16px; {GLASS} border-radius: 16px; '
        '@media(--mobile){grid-template-columns: 1fr; padding: 4px 0px;}'))
    left = col('h-l', crumb + h1 + lead + btns + kpis, 52, gap=24)

    photo = img('h-img', BANNER, alt='Cardiology team monitoring a patient during a cardiac stress test', css=(
        'display: block; width: 100%; height: auto; aspect-ratio: 5 / 6; max-height: 620px; object-fit: cover; border-radius: 24px; '
        'box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.08), 0px 40px 90px -40px rgba(2,40,66,0.35);'))
    float_card = box('h-f', eyebrow('h-fe', 'Aged A/R recovered') + big('h-fn', '$1.8M+', 48, '@media(--mobile){font-size: 38px;}')
                     + box('h-fbar', '', css=f'width: 100%; height: 3px; border-radius: 3px; background-image: {CTA_GRAD};')
                     + p('h-fp', 'August 2025 through July 2026', css=t(13, 1.5, SLATE, 400)), css=(
        f'position: absolute; left: 0px; bottom: 0px; display: flex; flex-direction: column; gap: 12px; width: 300px; max-width: 80%; padding: 22px; '
        f'{GLASS} background-color: rgba(255,255,255,0.72); border-radius: 20px; @media(--mobile){{padding: 18px;}}'))
    right = col('h-r', photo + float_card, 44, gap=0, css=(
        'position: relative; padding: 0px 0px 48px 40px; @media(--tablet){max-width: 600px; margin-inline: auto;} '
        '@media(--mobile){padding: 0px 0px 40px 16px;}'))

    def fact(i, lab, val):
        return box(f'hg{i}', eyebrow(f'hg{i}l', lab) + p(f'hg{i}v', val, css=t(15, 1.5, INK, 400)),
                   css='display: flex; flex-direction: column; gap: 8px; padding: 0px;')
    glance = grid('hg', fact(0, 'Practice', 'Golden State Heart &amp; Vascular') + fact(1, 'Service', 'A/R recovery &amp; denial management')
                  + fact(2, 'Focus', '30+ day aged claims') + fact(3, 'Period', 'Aug 2025 – Jul 2026'), css=(
        f'display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; width: 100%; padding: 24px 28px; margin-top: 24px; {GLASS} '
        '@media(--tablet){grid-template-columns: repeat(2, 1fr);} @media(--mobile){grid-template-columns: 1fr; gap: 18px; padding: 22px 20px;}'))
    return section('s-hero', row('h-row', left + right, align='center') + glance, css=(
        'padding-block-start: 72px; padding-block-end: 0px; @media(--tablet){padding-block-start: 48px; padding-block-end: 0px;} '
        '@media(--mobile){padding-block-start: 32px; padding-block-end: 0px;}'))


# ---------------------------------------------------------------- 2. executive summary
def summary():
    left = col('su-l', eyebrow('su-e', 'Executive summary')
               + h2('su-h', 'How Golden State Heart &amp; Vascular Recovered $1.8M+ in Aged A/R')
               + p('su-lead', 'Golden State Heart &amp; Vascular faced a significant aged accounts receivable challenge. More than $850,000 in reimbursement '
                   'was sitting in the 90+ day A/R bucket, while denied and unresolved claims required detailed follow-up beyond routine billing activity.',
                   css=t(18, 1.65, INK, 400, None, 'margin-top: 8px; @media(--mobile){font-size: 16px;}'))
               + body('su-p1', 'The outstanding claims involved medical record requests, authorization-related denials, coding discrepancies, modifier issues, '
                      'and payer follow-up. Without a dedicated recovery workflow, collectible revenue risked remaining unresolved as accounts continued to age.')
               + body('su-p2', 'MedCare MSO implemented a focused A/R recovery and denial management strategy centered on claim-level analysis, documentation '
                      'follow-up, appeals, coding and modifier review, and persistent payer engagement.')
               + body('su-p3', 'From August 2025 through July 2026, MedCare MSO recovered approximately <strong>$1.8 million+ from aged A/R</strong> for the '
                      'practice, equivalent to about $150,000 per month from aged receivables alone.'), 48, gap=20)
    band = box('su-b', eyebrow('su-be', 'Aug 2025 – Jul 2026', 'rgba(255,255,255,0.85)')
               + p('su-bn', '$1.8M+', css=t(92, 1, '#FFFFFF', 200, '-0.05em', 'margin-top: 6px; @media(--tablet_extra){font-size: 76px;} @media(--mobile){font-size: 60px;}'))
               + p('su-bp', 'Aged A/R recovered, August 2025 through July 2026', css=t(15, 1.5, 'rgba(255,255,255,0.92)', 400, None, 'max-width: 300px;')), css=(
        f'display: flex; flex-direction: column; gap: 14px; padding: 40px; border-radius: 24px; {BAND} '
        'transition: transform 0.3s ease; &:hover{transform: translateY(-4px);} @media(--mobile){padding: 28px 24px;}'))

    def stat(i, num, label):
        return box(f'su-s{i}', big(f'su-s{i}n', num, 48, '@media(--tablet_extra){font-size: 40px;} @media(--mobile){font-size: 36px;}')
                   + p(f'su-s{i}l', label, css=t(13, 1.5, SLATE, 400)),
                   css=f'display: flex; flex-direction: column; gap: 12px; padding: 26px; {GLASS} {LIFT} @media(--mobile){{padding: 22px;}}')
    stats = grid('su-g', stat(0, '~$150K', 'Monthly collections from aged A/R') + stat(1, '$850K+', 'Previously in the 90+ day A/R bucket'), css=(
        'display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; width: 100%; padding: 0px; @media(--mobile){grid-template-columns: 1fr;}'))
    right = col('su-r', band + stats, 46, gap=16)
    return section('s-sum', row('su-row', left + right), anchor='summary')


# ---------------------------------------------------------------- 3. challenge
ISSUES = ['More than $850K in reimbursement sitting in the 90+ day A/R bucket',
          'Medical record requests delaying payer reconsideration',
          'Authorization-related denials requiring detailed review and appeals',
          'Coding discrepancies affecting claim payment',
          'Modifier-related errors affecting adjudication',
          'Older accounts requiring targeted and persistent payer follow-up']


def challenge():
    top = row('ch-row', col('ch-l', eyebrow('ch-e', 'The challenge') + h2('ch-h', 'Aged A/R is rarely driven by a single issue'), 46, gap=14)
              + col('ch-r', body('ch-p1', 'For Golden State Heart &amp; Vascular, unpaid claims beyond 30 days reflected a combination of documentation, '
                                 'authorization, coding, modifier, and payer-related barriers.')
                    + body('ch-p2', 'The challenge was not simply identifying unpaid balances. Each claim required the team to determine why payment had '
                           'stalled, what documentation or correction was needed, and which action offered the best path to recovery.'), 48, gap=14),
              align='flex-end')
    key = flex('ch-k', h('ch-kh', 'h3', 'Key issues', css=t(13, 1.4, MUTED, 500, '0.1em', 'text-transform: uppercase; white-space: nowrap;'))
               + box('ch-kl', '', css='flex-grow: 1; height: 1px; background-color: rgba(3,103,161,0.1);'),
               css='display: flex; flex-direction: row; align-items: center; gap: 16px; width: 100%; padding: 0px; margin-top: 16px;')
    cards = ''
    for i, (txt, ico) in enumerate(zip(ISSUES, ICONS['issue'])):
        head = flex(f'ci{i}h', box(f'ci{i}c', img(f'ci{i}i', ico, css='display: block; width: 28px; height: 28px; transition: transform 0.3s ease;'), css=(
                        f'display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 999px; '
                        f'border: 2px solid {ACC}; background-color: rgba(255,255,255,0.35); transition: background-color 0.3s ease;'))
                    + p(f'ci{i}n', f'{i + 1:02d}', css=t(28, 1, 'rgba(3,103,161,0.28)', 200, '-0.04em', 'transition: color 0.3s ease;')),
                    css='display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 0px;')
        cards += box(f'ci{i}', head + p(f'ci{i}p', txt, css=t(16, 1.55, INK, 400)), css=(
            f'display: flex; flex-direction: column; gap: 18px; padding: 26px; {GLASS} {LIFT} '
            f'&:hover img{{transform: scale(1.08);}} &:hover p{{color: {INK};}} &:hover > div > p{{color: {ACC};}} @media(--mobile){{padding: 22px;}}'))
    grid_ = grid('ci', cards, css=(
        'display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; width: 100%; padding: 0px; '
        '@media(--tablet){grid-template-columns: repeat(2, 1fr);} @media(--mobile){grid-template-columns: 1fr;}'))
    panel = box('ch-pn', row('ch-pr', col('ch-pl', h('ch-ph', 'h3', 'Multiple denial types required different responses', css=t(28, 1.2, INK, 300, '-0.03em', '@media(--mobile){font-size: 22px;}')), 44)
                             + col('ch-pp', body('ch-pp1', 'The outstanding claims could not be resolved through a single standardized workflow. Some payers '
                                                 'required additional medical records before reconsideration. Others involved authorization issues that required '
                                                 'documentation review and appeal preparation. Coding and modifier-related denials required separate analysis before '
                                                 'claims could be corrected, resubmitted, or appealed.', 15)
                                   + body('ch-pp2', 'Segmenting accounts by root cause allowed the team to address the reason for nonpayment rather than repeatedly '
                                          'following up without moving the claim toward resolution.', 15), 50, gap=14)), css=(
        f'display: flex; padding: 36px; margin-top: 16px; {GLASS} @media(--tablet){{padding: 28px;}} @media(--mobile){{padding: 22px;}}'))
    return section('s-chal', top + key + grid_ + panel, anchor='challenge', css='gap: 24px;')


# ---------------------------------------------------------------- 4. bottom line band
def bottom_line():
    inner = row('bl-row', col('bl-l', eyebrow('bl-e', 'The bottom line', 'rgba(255,255,255,0.85)')
                              + p('bl-h', 'Golden State Heart &amp; Vascular had already earned the revenue.',
                                  css=t(42, 1.15, '#FFFFFF', 300, '-0.03em', '@media(--tablet){font-size: 34px;} @media(--mobile){font-size: 28px;}')), 46, gap=16)
                + col('bl-r', p('bl-p', 'The challenge was converting aging receivables into cash before filing limits, documentation gaps, and unresolved denial '
                                'issues made recovery more difficult. MedCare MSO treated the aged A/R inventory as a recoverable asset, with each account '
                                'assigned a defined next action and follow-up path.', css=t(16, 1.7, 'rgba(255,255,255,0.94)', 400)), 48,
                      css=f'padding: 28px; {INNER} @media(--mobile){{padding: 22px;}}'), align='center')
    band = box('bl', inner, css=f'display: flex; padding: 64px; border-radius: 24px; {BAND} @media(--tablet){{padding: 40px;}} @media(--mobile){{padding: 28px 22px;}}')
    return section('s-bl', band)


# ---------------------------------------------------------------- 5. solution
STEPS = [('A/R segmentation and prioritization',
          'MedCare MSO organized outstanding accounts by aging, payer status, denial reason, balance, and required next action. Claims beyond 30 days '
          'received dedicated attention, while older accounts were reviewed individually to determine the most appropriate recovery path. This approach '
          'allowed the team to prioritize collectible balances and direct resources toward accounts with clear recovery opportunities.'),
         ('Medical record denial management',
          'Claims delayed or denied because of medical record requirements were routed through a structured documentation workflow. The team reviewed '
          'payer requests, coordinated the required supporting records, submitted documentation, and continued follow-up through payer review.'),
         ('Authorization review and appeals',
          'Authorization-related denials were analyzed at the claim level to determine the reason for nonpayment and whether the account remained '
          'appealable. Where appropriate, the team assembled supporting documentation and submitted appeals for payer reconsideration.'),
         ('Coding and modifier review',
          'MedCare MSO reviewed coding discrepancies and modifier-related issues that could affect claim adjudication. When corrective action was '
          'appropriate, claims were corrected, resubmitted, or appealed according to payer requirements.'),
         ('Persistent payer follow-up',
          'Aged A/R recovery often requires multiple payer interactions. MedCare MSO maintained continuous follow-up across outstanding claims, tracking '
          'documentation requests, appeal status, corrected claims, payer responses, and next actions until each account reached an appropriate resolution.')]


def solution():
    nav = ''
    for i, (title, _) in enumerate(STEPS):
        nav += box(f'sn{i}', p(f'sn{i}t', f'<span>{i + 1:02d}</span>{title}', css=t(14, 1.4, INK, 400, None, (
            f'transition: color 0.2s ease; & span{{display: inline-block; min-width: 28px; font-size: 13px; font-weight: 500; color: {ACC};}}'))),
            link=f'#step-{i + 1:02d}', css=(
            'display: flex; padding: 10px 14px; border-radius: 999px; text-decoration: none; transition: background-color 0.2s ease; '
            f'&:hover{{background-color: rgba(47,125,107,0.08);}} &:hover p{{color: {ACC};}}'))
    navbox = box('sn', nav, css=f'display: flex; flex-direction: column; gap: 2px; padding: 10px; margin-top: 12px; {GLASS} @media(--mobile){{display: none;}}')
    left = col('so-l', eyebrow('so-e', 'The solution') + h2('so-h', 'A recovery path for every account') + navbox, 36, gap=14,
               css='position: sticky; top: 110px; @media(--tablet){position: static;}')
    cards = ''
    for i, (title, txt) in enumerate(STEPS):
        cards += grid(f'st{i}', big(f'st{i}n', f'{i + 1:02d}', 44, '@media(--mobile){font-size: 36px;}')
                      + box(f'st{i}b', h(f'st{i}h', 'h3', title, css=t(20, 1.3, INK, 400, None, '@media(--mobile){font-size: 18px;}'))
                            + body(f'st{i}p', txt, 15), css='display: flex; flex-direction: column; gap: 8px; padding: 0px; margin-top: 6px;'), css=(
            f'display: grid; grid-template-columns: 64px 1fr; gap: 20px; padding: 28px; scroll-margin-top: 110px; {GLASS} {LIFT} '
            '@media(--mobile){grid-template-columns: 1fr; gap: 10px; padding: 22px;}'), anchor=f'step-{i + 1:02d}')
    right = col('so-r', cards, 60, gap=16)
    return section('s-sol', row('so-row', left + right), anchor='solution')


# ---------------------------------------------------------------- 6. results
TABLE = [('90+ day A/R', '$850K+ in aged receivables', 'Dedicated recovery and resolution workflow'),
         ('Aged A/R collections', 'Aged balances required focused follow-up', '$1.8M+ collected August 2025 through July 2026'),
         ('Monthly aged A/R collections', 'Limited recovery visibility', 'Approximately $150K per month'),
         ('Medical record denials', 'Outstanding documentation issues', 'Structured record submission and follow-up'),
         ('Authorization denials', 'Required additional intervention', 'Claim-level review and appeals'),
         ('Coding &amp; modifier issues', 'Contributed to unpaid claims', 'Corrective review, resubmission, or appeal')]
COLS = 'display: grid; grid-template-columns: 1fr 1.2fr 1.4fr; gap: 24px; align-items: center;'


def results():
    left = col('re-l', eyebrow('re-e', 'The results')
               + h2('re-h', '<span>$150K</span> in monthly cash flow from existing A/R', css=f'& span{{font-weight: 400; {GRAD_TEXT}}}')
               + body('re-p', 'The focused recovery program converted older receivables into a consistent source of cash flow for Golden State Heart &amp; '
                      'Vascular. From August 2025 through July 2026, approximately <strong>$1.8 million+ was collected from aged A/R</strong>. That equates '
                      'to about $150,000 per month from old A/R alone, separate from collections generated through current billing activity.'), 50, gap=16)

    def stat(i, num, label):
        return box(f're-s{i}', big(f're-s{i}n', num, 60, '@media(--tablet_extra){font-size: 48px;} @media(--mobile){font-size: 40px;}')
                   + p(f're-s{i}l', label, css=t(13, 1.5, SLATE, 400)), css=(
            'display: flex; flex-direction: column; gap: 12px; padding: 4px 30px; '
            + ('' if i == 0 else 'border-left: 1px solid rgba(3,103,161,0.1); ')
            + '@media(--mobile){padding: 18px 22px; border-left: 0px; ' + ('' if i == 0 else 'border-top: 1px solid rgba(3,103,161,0.1);') + '}'))
    card = grid('re-c', stat(0, '$1.8M+', 'Collected from aged A/R, Aug 2025 – Jul 2026') + stat(1, '~$150K', 'Per month from old A/R alone'), css=(
        f'display: grid; grid-template-columns: repeat(2, 1fr); gap: 0px; width: 44%; padding: 26px 0px; {GLASS} {LIFT} '
        '@media(--tablet){width: 100%;} @media(--mobile){grid-template-columns: 1fr; padding: 4px 0px;}'))
    top = row('re-row', left + card, align='flex-end')

    hdr = grid('rt-h', p('rt-h0', 'Metric', css=t(11, 1.4, MUTED, 500, '0.12em', 'text-transform: uppercase;'))
               + p('rt-h1', 'Before focused recovery', css=t(11, 1.4, MUTED, 500, '0.12em', 'text-transform: uppercase;'))
               + p('rt-h2', 'Current outcome', css=t(11, 1.4, ACC, 500, '0.12em', 'text-transform: uppercase;')),
               css=f'{COLS} padding: 18px 28px; border-bottom: 1px solid rgba(3,103,161,0.08);')
    rows = ''
    for i, (a, bfr, c) in enumerate(TABLE):
        hi = i in (1, 2)
        ring = ACC if hi else ACC2
        out = flex(f'rt{i}o', box(f'rt{i}k', img(f'rt{i}ki', ICONS['check'], css='display: block; width: 12px; height: 12px;'), css=(
                        f'display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 24px; height: 24px; border-radius: 999px; border: 2px solid {ring};'))
                   + p(f'rt{i}c', c, css=t(14, 1.45, ACC if hi else INK, 500 if hi else 400)),
                   css='display: flex; flex-direction: row; align-items: center; gap: 10px; padding: 0px;')
        rows += grid(f'rt{i}', p(f'rt{i}a', a, css=t(14, 1.45, INK, 500)) + p(f'rt{i}b', bfr, css=t(14, 1.45, SLATE, 400)) + out, css=(
            f'{COLS} padding: 20px 28px; transition: background-color 0.2s ease; '
            + ('border-bottom: 1px solid rgba(3,103,161,0.06); ' if i < len(TABLE) - 1 else '')
            + (f'background-color: rgba(255,255,255,0.72); box-shadow: inset 3px 0px 0px 0px {ACC}; ' if hi else '')
            + '&:hover{background-color: rgba(255,255,255,0.85);}'))
    table = box('rt', box('rt-in', hdr + rows, css='display: flex; flex-direction: column; min-width: 720px; padding: 0px;'), css=(
        f'display: block; width: 100%; padding: 0px; overflow-x: auto; {GLASS} box-shadow: {SH}, 0px 30px 70px -36px rgba(2,40,66,0.3);'))
    close = row('re-cl', col('re-c1', body('re-c1p', 'The most important outcome is that older claims are producing cash. Approximately $150,000 per month is '
                                           'being collected from aged accounts receivable, demonstrating the value of dedicated denial expertise, coding review, '
                                           'appeals, documentation management, and disciplined payer follow-up.', 17), 47)
                + col('re-c2', body('re-c2p', 'For Golden State Heart &amp; Vascular, the initiative established a more systematic way to recover revenue that '
                                    'had already been earned but had not yet reached the practice.', 17), 47), css='@media(--tablet){gap: 16px;}')
    return section('s-res', top + table + close, anchor='results')


# ---------------------------------------------------------------- 7. contact band
def contact():
    left = col('co-l', eyebrow('co-e', 'Your growth, our promise', 'rgba(255,255,255,0.85)')
               + h2('co-h', 'Turn aging A/R into recoverable revenue', '#FFFFFF', 'font-size: 52px; @media(--tablet){font-size: 40px;} @media(--mobile){font-size: 30px;}')
               + body('co-p1', 'A/R that moves beyond 30, 60, or 90 days does not automatically become lost revenue. With focused claim-level analysis, '
                      'documentation management, coding expertise, appeals, and payer follow-up, a meaningful portion of aged receivables may still be recoverable.',
                      16, 'rgba(255,255,255,0.92)', 'font-weight: 400;')
               + body('co-p2', 'MedCare MSO helps healthcare organizations identify those opportunities, resolve the barriers delaying payment, and convert '
                      'outstanding A/R into cash.', 16, 'rgba(255,255,255,0.92)', 'font-weight: 400;'), 50, gap=16)
    call = box('co-b', p('co-bt', 'Call us at 800-640-6409', css=t(15, 1, '#FFFFFF', 500, None, 'white-space: nowrap; transition: color 0.25s ease; @media(--mobile){font-size: 14px;}'))
               + arrow_circle('co-bc', ICONS['arrow_white'], '#FFFFFF'), link='tel:8006406409', css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 14px; height: 56px; padding: 0px 6px 0px 26px; '
        'border-radius: 999px; border: 2px solid #FFFFFF; background-color: rgba(255,255,255,0.1); text-decoration: none; cursor: pointer; '
        'transition: background-color 0.25s ease; &:hover{background-color: #FFFFFF;} '
        f'&:hover p{{color: {ACC};}} &:hover div{{border-color: {ACC};}} &:hover img{{filter: brightness(0) saturate(100%) invert(38%) sepia(32%) saturate(720%) hue-rotate(117deg);}} '
        '@media(--mobile){padding-left: 18px; gap: 8px;}'))

    def line(i, lab, val, url):
        return box(f'co-r{i}', p(f'co-r{i}l', lab, css=t(14, 1.5, 'rgba(255,255,255,0.75)', 400))
                   + p(f'co-r{i}v', val, css=t(14, 1.5, '#FFFFFF', 400, None, 'text-align: right; word-break: break-word; transition: opacity 0.2s ease;')),
                   link=url, css=(
            'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 16px; padding: 14px 0px; '
            'border-top: 1px solid rgba(255,255,255,0.2); text-decoration: none; '
            '&:hover p:last-child{text-decoration: underline; text-underline-offset: 4px;}'))
    right = col('co-r', eyebrow('co-re', 'Talk to our A/R recovery team', 'rgba(255,255,255,0.85)') + call
                + box('co-rows', line(0, 'Email', 'info@medcaremso.com', 'mailto:info@medcaremso.com')
                      + line(1, 'Web', 'www.medcaremso.com', 'https://www.medcaremso.com'), css='display: flex; flex-direction: column; padding: 0px; margin-top: 4px;'),
                42, gap=18, css=f'padding: 28px; {INNER} box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.25), 0px 30px 60px -30px rgba(0,20,35,0.35); @media(--mobile){{padding: 22px;}}')
    band = box('co', row('co-row', left + right, align='center'), css=(
        f'display: flex; padding: 64px; border-radius: 24px; {BAND} @media(--tablet){{padding: 40px;}} @media(--mobile){{padding: 28px 22px;}}'))
    return section('s-con', band, anchor='contact', css='padding-block-end: 100px; @media(--tablet){padding-block-end: 64px;} @media(--mobile){padding-block-end: 44px;}')


SECTIONS = [hero, summary, challenge, bottom_line, solution, results, contact]

PAGE_BG = ('background-color: #F6FAF7; background-image: '
           'radial-gradient(ellipse 900px 700px at 0% 0%, rgba(156,216,246,0.28) 0%, rgba(156,216,246,0) 70%), '
           'radial-gradient(ellipse 800px 700px at 100% 6%, rgba(198,226,190,0.34) 0%, rgba(198,226,190,0) 70%), '
           'radial-gradient(ellipse 900px 800px at 0% 30%, rgba(126,176,62,0.168) 0%, rgba(126,176,62,0) 70%), '
           'radial-gradient(ellipse 900px 800px at 100% 46%, rgba(58,150,204,0.152) 0%, rgba(58,150,204,0) 70%), '
           'radial-gradient(ellipse 800px 700px at 15% 62%, rgba(156,216,246,0.28) 0%, rgba(156,216,246,0) 70%), '
           'radial-gradient(ellipse 900px 800px at 100% 78%, rgba(247,236,170,0.22) 0%, rgba(247,236,170,0) 70%), '
           'radial-gradient(ellipse 900px 700px at 0% 96%, rgba(198,226,190,0.34) 0%, rgba(198,226,190,0) 70%);')


def payload(mode='replace_children', dry=False):
    global b
    b = B()
    xml = flex('page', ''.join(f() for f in SECTIONS), css=(
        f'display: flex; flex-direction: column; align-items: stretch; gap: 0px; width: 100%; padding: 0px; {PAGE_BG}'))
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes, 'mode': mode, 'dry_run': dry}


if __name__ == '__main__':
    d = payload()
    print(len(json.dumps(d)), 'bytes', len(d['style']), 'styled elements')
