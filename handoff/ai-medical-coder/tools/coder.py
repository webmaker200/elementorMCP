"""AI Medical Coder (Sophus) page -- WP page 411494, Elementor V4 atomic, from Sophus_AI_Web_Page_v2_1.html.

Brief:
- site header/footer/orange demo band come from the site templates (not built here);
- sections use the site's `parent-container` class for spacing on every device (no local padding override);
- site classes for type and layout: heading-main (H1), specialties-heading (H2), heading-h3, global-text, global-btn, w-45/w-50/w-55;
- columns use percentage widths (no flex-basis); grids use plain fr tracks with explicit tablet/mobile columns;
- colours are hex (page portable to the live site); font via the kit's Poppins variable;
- tabs (hero view switch, roles) are V4 e-tabs, the feature list is a V4 e-accordion, the form is a V4 e-form;
- testimonials are the site's real ones (template 388878) with their photos; a small script (added by deploy) runs the slider.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PID = 411494
MEDIA = json.load(open(os.path.join(HERE, '..', 'media.json')))
DEMO, HOW = '#demo', '#how'
PHONE = '800-640-6409'

INK, SLATE, MUTED = '#14212B', '#4A5966', '#6B7A87'
BLUE, BLUE_H, NAVY, SKY, GREEN_T = '#0367A1', '#034D77', '#023B5C', '#9CD8F6', '#486323'
PURPLE, PURPLE_D = '#9443EC', '#3E0C7C'
F = 'font-family: var(--Poppins);'
GLASS = ('background-image: linear-gradient(145deg, rgba(255,255,255,0.74), rgba(255,255,255,0.46)); '
         'backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); '
         'border: 1px solid rgba(255,255,255,0.75); '
         'box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.10), inset 0px 1px 0px 0px rgba(255,255,255,0.9), 0px 12px 32px 0px rgba(2,40,66,0.07);')
FOCUS = '&:focus-visible{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.30);}'

TESTIMONIALS = [  # site template 388878; photos are the site's ones (401937, 401412, 399532, 397918, 396539) restyled on the design's grey backdrop
    ('I highly recommend MedCare MSO if you are looking for help with your billing and gain some freedom to see more patients or manage your business.',
     'Dr. Jose Correa', 'Practice Owner, TXEC', 411546),
    ('MedCare MSO has been an excellent organization to work with, I highly recommend them for their quality of service and commitment to excellence.',
     'Shaunna Mock', 'Back Office Manager, STST', 411545),
    ("We are definitely impressed by the Team's performance. I worked with a lot of different folks from all over the world on different business transactions, and Mark is truly a top notch talent!",
     'Max Owens', 'Director of Corporate Development, SC & SF', 411544),
    ("MedCare MSO's exceptional communication and expertise elevated our RCM experience and my bank accounts!",
     'Kelly Ballou', 'Owner, R.D.', 411543),
    ('MedCare MSO did a great job with our billing and helping clean up old AR. Regular updates and good communication were very appreciated.',
     'Bret', 'Co-Owner, PCP', 411542),
]
STORIES_URL = 'https://medcaremso.com/testimonial/'


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


def box(cid, kids, css='', cls=None, tag='e-div-block', cfg=None):
    return b.el(tag, cid, kids, cfg=cfg, css=css, cls=cls)


def flex(cid, kids, css='', cls=None, cfg=None):
    return b.el('e-flexbox', cid, kids, cfg=cfg, css=css, cls=cls)


def grid(cid, kids, css='', cls=None):
    return b.el('e-grid', cid, kids, css=css, cls=cls)


def p(cid, html, css='', cls=None, tag=None):
    cfg = {'paragraph': html}
    if tag:
        cfg['tag'] = tag
    return b.el('e-paragraph', cid, cfg=cfg, css=css, cls=cls)


def h(cid, tag, title, css='', cls=None):
    return b.el('e-heading', cid, cfg={'tag': tag, 'title': title}, css=css, cls=cls)


def img(cid, name, css='', alt=None, mid=None):
    i = mid or MEDIA[name]['id']
    return b.el('e-image', cid, cfg={'image': {'src': {'id': i, 'alt': alt or ''}, 'size': 'full'}}, css=css)


def svg(cid, name, css=''):
    return b.el('e-svg', cid, cfg={'svg': {'id': MEDIA[name]['id']}}, css=css)


def text(size, lh, color, weight=400, ls=None, extra=''):
    return (f'{F} font-size: {size}px; line-height: {lh}; font-weight: {weight}; color: {color}; '
            + (f'letter-spacing: {ls}; ' if ls else '') + 'margin: 0px; ' + extra)


def button(cid, label, url, kind='primary', size='lg', css=''):
    dims = {'lg': 'height: 52px; padding: 0px 28px; font-size: 16px;', 'md': 'height: 42px; padding: 0px 20px; font-size: 15px;'}[size]
    look = {
        'primary': f'background-color: {BLUE}; color: #FFFFFF; &:hover{{background-color: {BLUE_H}; color: #FFFFFF;}}',
        'ghost': f'background-color: transparent; color: {SLATE}; &:hover{{background-color: rgba(3,103,161,0.07); color: {INK};}}',
    }[kind]
    return b.el('e-button', cid, cfg={'text': label, 'link': {'destination': url}}, cls=['global-btn'], css=(
        f'display: inline-flex; align-items: center; justify-content: center; {dims} font-weight: 500; line-height: 1; '
        'white-space: nowrap; border: 0px; border-radius: 999px; text-decoration: none; cursor: pointer; '
        f'transition: background-color 0.18s cubic-bezier(0.2,0,0,1), color 0.12s ease, box-shadow 0.12s ease; {look} {FOCUS} ' + css))


def pill(cid, label, css=''):
    """Eyebrow pill with the soft green ring."""
    return p(cid, label, cls=['global-text'], css=(
        f'display: inline-flex; width: max-content; max-width: 100%; padding: 8px 20px; border-radius: 999px; font-size: 13px; line-height: 1.5; '
        f'color: {SLATE}; border: 1px solid rgba(126,176,62,0.45); background-color: rgba(255,255,255,0.55); '
        'box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.9), 0px 6px 16px 0px rgba(2,40,66,0.05); margin: 0px; ' + css))


def h2(cid, title, css=''):
    """Site H2 class (responsive sizes); weight / tracking from the design."""
    return h(cid, 'h2', title, cls=['specialties-heading'], css=(
        f'font-weight: 500; line-height: 1.1; letter-spacing: -0.03em; color: {INK}; margin: 0px; ' + css))


def lead(cid, html, css=''):
    return p(cid, html, cls=['global-text'], css=f'line-height: 1.65; color: {SLATE}; margin: 0px; ' + css)


def section(cid, kids, css='', anchor=None):
    cfg = {'tag': 'section'}
    if anchor:
        cfg['_cssid'] = anchor
    return flex(cid, kids, cfg=cfg, cls=['parent-container'], css=(
        'display: flex; flex-direction: column; align-items: center; gap: 0px; width: 100%; position: relative; ' + css))


def row(cid, kids, css='', stack='tablet', gap='6%', reverse=False):
    return flex(cid, kids, css=(
        f'display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-between; align-items: center; gap: {gap}; '
        'width: 100%; padding: 0px; ' + css +
        f' @media(--{stack}){{flex-direction: {"column-reverse" if reverse else "column"}; align-items: stretch; gap: 40px;}}'))


def col(cid, kids, cls=None, css='', stack='tablet'):
    return box(cid, kids, cls=cls, css=(
        'display: flex; flex-direction: column; align-items: flex-start; padding: 0px; ' + css +
        f' @media(--{stack}){{width: 100%;}}'))


GLOW_BLUE = 'radial-gradient(38% 40% at 0% 30%, rgba(156,216,246,0.28) 0%, rgba(156,216,246,0) 100%)'
GLOW_YELLOW = 'radial-gradient(40% 45% at 100% 10%, rgba(253,232,160,0.32) 0%, rgba(253,232,160,0) 100%)'
GLOW_GREEN = 'radial-gradient(40% 45% at 85% 85%, rgba(198,226,190,0.30) 0%, rgba(198,226,190,0) 100%)'


# ================================================================ 1. Hero + coder / manager view
def browser(cid, path, image, alt):
    dots = ''.join(box(f'{cid}d{i}', '', css=f'width: 10px; height: 10px; padding: 0px; border-radius: 999px; background-color: {c};')
                   for i, c in enumerate(('#F37A6E', '#F4C76B', '#95C59C')))
    bar = flex(f'{cid}dots', dots, css='display: flex; flex-direction: row; gap: 6px; width: 46px; padding: 0px; @media(--mobile){display: none;}')
    bar += p(f'{cid}url', f'sophus.medcaremso.com/{path}', css=text(12, 1.5, MUTED, extra=(
        'display: flex; align-items: center; justify-content: center; width: 100%; max-width: 420px; height: 28px; padding: 0px 14px; '
        'margin: 0px auto; border-radius: 999px; background-color: rgba(255,255,255,0.7); box-shadow: inset 0px 0px 0px 1px rgba(3,103,161,0.10); '
        'white-space: nowrap; overflow: hidden; text-overflow: ellipsis; @media(--mobile){font-size: 11px; height: 24px;}')))
    bar += box(f'{cid}sp', '', css='width: 46px; padding: 0px; @media(--mobile){display: none;}')
    k = flex(f'{cid}bar', bar, css='display: flex; flex-direction: row; align-items: center; gap: 14px; width: 100%; padding: 4px 8px 12px 8px; '
                                   '@media(--mobile){padding: 2px 4px 8px 4px;}')
    k += img(f'{cid}img', image, alt=alt, css='display: block; width: 100%; height: auto; border-radius: 16px; background-color: #F6F2FB; '
                                                '@media(--mobile){border-radius: 10px;}')
    return box(cid, k, css=(
        'display: flex; flex-direction: column; width: 100%; max-width: 1120px; margin: 0px auto; padding: 10px; border-radius: 24px; ' + GLASS +
        ' box-shadow: 0px 0px 0px 1px rgba(148,67,236,0.14), inset 0px 1px 0px 0px rgba(255,255,255,0.9), 0px 30px 70px 0px rgba(90,36,158,0.16); '
        '-webkit-mask-image: linear-gradient(180deg, #000 66%, transparent 99%); mask-image: linear-gradient(180deg, #000 66%, transparent 99%); '
        '@media(--mobile){padding: 6px; border-radius: 16px;}'))


def hero():
    k = flex('h-pill', img('h-pill-logo', 'sophus-mark', css=(
                'display: flex; width: 30px; height: 30px; padding: 7px; border-radius: 999px; background-color: #FFFFFF; '
                'box-shadow: 0px 0px 0px 1px rgba(148,67,236,0.14); object-fit: contain;'))
             + p('h-pill-b', 'Sophus', css=text(13, 1.5, INK, 600))
             + p('h-pill-t', '· AI medical coder', css=text(13, 1.5, SLATE, extra='white-space: nowrap;')),
             css=('display: flex; flex-direction: row; align-items: center; gap: 6px; width: max-content; max-width: 100%; '
                  'padding: 5px 18px 5px 6px; border-radius: 999px; border: 1px solid rgba(148,67,236,0.28); '
                  'background-color: rgba(255,255,255,0.55); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); '
                  'box-shadow: inset 0px 1px 0px 0px rgba(255,255,255,0.9), 0px 6px 16px 0px rgba(2,40,66,0.05);'))
    k += h('h1', 'h1', 'AI medical coding your coders can verify in seconds.', cls=['heading-main'], css=(
        f'width: 100%; max-width: 900px; margin: 28px 0px 0px 0px; font-size: 72px; line-height: 1.04; font-weight: 500; '
        f'letter-spacing: -0.04em; color: {INK}; text-align: center; text-wrap: balance; '
        '@media(--laptop){font-size: 64px;} @media(--tablet_extra){font-size: 58px;} @media(--tablet){font-size: 50px;} '
        '@media(--mobile_extra){font-size: 44px;} @media(--mobile){font-size: 36px; line-height: 1.1; margin-block-start: 22px;}'))
    k += lead('h-lead', 'Sophus reads each chart, assigns CPT, ICD-10 and HCPCS codes with the evidence behind them, and runs payer edits '
                        'before the claim goes out. Coders review and approve. Managers see the whole queue.',
              'width: 100%; max-width: 640px; margin-block-start: 24px; font-size: 17px; text-align: center; @media(--mobile){font-size: 15px;}')
    k += flex('h-cta', button('h-b1', 'Book a demo', DEMO) + button('h-b2', 'See how it works →', HOW, 'ghost'),
              css='display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-items: center; gap: 12px; '
                  'width: 100%; padding: 0px; margin-block-start: 32px;')
    top = col('h-top', k, css='align-items: center; width: 100%; text-align: center;')

    # view switch: V4 tabs; selected / hover / keyboard focus states on each tab button
    tab_css = (f'{F} display: inline-flex; align-items: center; justify-content: center; text-align: center; padding: 8px 16px; border: 0px; border-radius: 999px; font-size: 13px; '
               f'font-weight: 500; line-height: 1.5; color: {SLATE}; background-color: transparent; cursor: pointer; white-space: nowrap; '
               'transition: background-color 0.18s cubic-bezier(0.2,0,0,1), color 0.12s ease, box-shadow 0.12s ease; '
               f'&:hover{{background-color: rgba(255,255,255,0.75); color: {INK};}} '
               f'&[aria-selected="true"]{{background-color: #FFFFFF; color: {INK}; '
               'box-shadow: 0px 1px 2px 0px rgba(2,40,66,0.08), 0px 0px 0px 1px rgba(3,103,161,0.10);} '
               '&:focus-visible{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.30);}')
    tabs = ''.join(b.el('e-tab', f'hv-t{i}', p(f'hv-t{i}l', name, css='width: 100%; margin: 0px; font: inherit; color: inherit; text-align: center;'), css=tab_css)
                   for i, name in enumerate(('Coder view', 'Manager view')))
    menu = b.el('e-tabs-menu', 'hv-menu', tabs, css=(
        'display: inline-flex; flex-direction: row; gap: 2px; width: max-content; max-width: 100%; margin: 0px auto; padding: 5px; '
        'border-radius: 999px; background-color: rgba(255,255,255,0.6); backdrop-filter: blur(20px) saturate(180%); '
        '-webkit-backdrop-filter: blur(20px) saturate(180%); box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.10), 0px 8px 24px 0px rgba(2,40,66,0.06);'))
    views = (('queue', 'sophus-coder-dashboard', 'Coder view: suggested codes with the evidence behind each one. Sample data.'),
             ('manager', 'sophus-manager-dashboard-v2', 'Manager view: team output, review queue and AI coder performance. Sample data.'))
    panels = ''
    for i, (path, image, cap) in enumerate(views):
        c = browser(f'hv-f{i}', path, image, cap.split(':')[0] + ' dashboard, sample data')
        c += p(f'hv-cap{i}', cap, css=text(13, 1.5, MUTED, extra='width: 100%; margin-block-start: 4px; text-align: center;'))
        panels += b.el('e-tab-content', f'hv-c{i}', c, css='display: block; width: 100%; padding: 0px;')
    area = b.el('e-tabs-content-area', 'hv-area', panels, css='display: block; width: 100%; padding: 0px; margin-block-start: 20px;')
    t = b.el('e-tabs', 'hv', menu + area, cfg={'default-active-tab': 0}, css=(
        'display: flex; flex-direction: column; align-items: center; gap: 0px; width: 100%; padding: 0px; margin-block-start: 48px; '
        'background-image: radial-gradient(42% 46% at 50% 55%, rgba(169,70,244,0.30) 0%, rgba(207,138,253,0.16) 48%, rgba(207,138,253,0) 74%);'))
    return section('s1', top + t)


# ================================================================ 2. KPI strip
def stats():
    kp = (('50,000+', 'Claims coded'), ('4.7×', 'Coder throughput'), ('95%', 'Coding accuracy'), ('79%', 'Less coding time'))
    cells = ''
    for i, (v, l) in enumerate(kp):
        line = '' if i == 0 else 'border-left: 1px solid rgba(3,103,161,0.12); '
        cells += box(f'k{i}', p(f'k{i}v', v, css=text(44, 1, INK, 500, '-0.035em', '@media(--tablet){font-size: 38px;} @media(--mobile){font-size: 32px;}'))
                     + p(f'k{i}l', l, cls=['global-text'], css=f'font-size: 14px; line-height: 1.5; color: {SLATE}; margin: 0px;'),
                     css=(f'display: flex; flex-direction: column; gap: 10px; padding: 4px 24px; {line}'
                          + ('padding-inline-start: 0px; ' if i == 0 else '')
                          + '@media(--tablet){gap: 8px; padding: 4px 20px;}'
                          + (' @media(--tablet){border-left: 0px; padding-inline-start: 0px;}' if i == 2 else '')))
    g = grid('k-grid', cells, css=(
        'display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; grid-template-rows: auto; row-gap: 32px; column-gap: 0px; width: 100%; padding: 0px; '
        '@media(--tablet){grid-template-columns: 1fr 1fr;} @media(--mobile){grid-template-columns: 1fr 1fr; row-gap: 28px;}'))
    g += p('k-note', 'Our figures, from one anonymous Sophus deployment. Results vary by specialty, documentation and payer mix.',
           css=text(12.5, 1.5, MUTED, extra='width: 100%; margin-block-start: 24px; text-align: center;'))
    return section('s2', box('k-wrap', g, css='display: flex; flex-direction: column; width: 100%; max-width: 1080px; padding: 0px;'))


# ================================================================ 3. What Sophus does (accordion)
def how():
    left = col('w-l', img('w-panel', 'sophus-claim-card-panel', alt=None, css=(
        'display: block; width: 100%; height: auto; border-radius: 24px; '
        'box-shadow: 0px 0px 0px 1px rgba(148,67,236,0.2), 0px 24px 56px 0px rgba(90,36,158,0.18);')), cls=['w-50'], css='@media(--tablet){max-width: 560px; margin: 0px auto;}')
    r = pill('w-pill', 'What Sophus does')
    r += h2('w-h2', 'Sophus does the first pass on every chart.', 'margin-block-start: 20px; text-wrap: balance;')
    r += lead('w-lead', 'Your coders keep the final say. They check the codes, the evidence and the edits, then approve.',
              'max-width: 520px; margin-block-start: 18px;')
    items = (('Codes straight from the documentation',
              'CPT, ICD-10 and HCPCS codes assigned from notes, labs, imaging and operative reports, with pointers, modifiers, POS and units mapped to CMS-1500 and UB-04.'),
             ('Shows the evidence for every code',
              'Each suggestion links to the sentence that supports it and carries a confidence score, so a coder can confirm it at a glance.'),
             ('Runs the payer rules before submission',
              'NCCI, MUE, LCD/NCD and payer-specific edits run on every claim. Anything uncertain is flagged for a coder.'),
             ('Adapts to your specialty',
              'Coding logic tuned to your specialty, from E/M levels to labs, pathology and complex surgical cases.'))
    acc = ''
    for i, (q, a) in enumerate(items):
        title = b.el('e-accordion-item-title', f'a{i}tt',
                     p(f'a{i}n', f'0{i + 1}.', css=text(14, 1.5, MUTED, 600, extra='flex-shrink: 0; width: 22px;'))
                     + h(f'a{i}q', 'h3', q, css=text(18, 1.5, INK, 500, '-0.015em', '@media(--mobile){font-size: 16px;}')),
                     css='display: flex; flex-direction: row; align-items: center; gap: 16px; padding: 0px; min-width: 0px;')
        icon = b.el('e-accordion-item-icon', f'a{i}ic', svg(f'a{i}ii', 'sophus-acc-plus', css='display: block; width: 28px; height: 28px;'),
                    css=(f'display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; width: 28px; height: 28px; '
                         f'padding: 0px; border-radius: 999px; background-color: rgba(3,103,161,0.09); color: {BLUE}; '
                         'transition: background-color 0.18s ease, color 0.18s ease;'))
        head = b.el('e-accordion-item-header', f'a{i}h', title + icon, css=(
            'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0px; cursor: pointer; '
            f'&:hover h3{{color: {BLUE};}} &:focus-visible{{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.30); border-radius: 8px;}}'))
        body = b.el('e-accordion-item-content', f'a{i}c', p(f'a{i}a', a, cls=['global-text'], css=(
            f'font-size: 14.5px; line-height: 1.6; color: {SLATE}; margin: 0px; padding: 0px 44px 0px 38px; '
            '@media(--mobile){padding: 0px 0px 0px 38px;}')), css='padding: 0px 0px 20px 0px;')
        acc += b.el('e-accordion-item', f'a{i}', head + body, css=(
            'display: block; padding: 0px; border-bottom: 1px solid rgba(3,103,161,0.12); '
            f'&[open] .e-accordion-item-icon, &[open] [class*="accordion-item-icon"]{{background-color: {NAVY}; color: #FFFFFF;}} '
            '&[open] svg path:last-child{opacity: 0;}'))
    r += b.el('e-accordion', 'w-acc', acc, cfg={'default_state': 'first_expanded', 'max_expanded': 'one', 'show_icon': True, 'faq_schema': False},
              css='display: flex; flex-direction: column; gap: 0px; width: 100%; padding: 0px; margin-block-start: 28px; '
                  'border-top: 1px solid rgba(3,103,161,0.12);')
    right = col('w-r', r, cls=['w-45'])
    return section('s3', row('w-row', left + right), anchor='how')


# ================================================================ 4. Speed
def speed():
    k = pill('sp-pill', 'Speed')
    k += h2('sp-h2', 'Coding time per claim went from 2:30 to 0:32.', 'max-width: 760px; margin-block-start: 20px; text-align: center; text-wrap: balance;')
    k += lead('sp-lead', 'In one Sophus deployment across 50,000+ claims, coders moved from keying codes to checking them. The same team cleared 4.7× the charts.',
              'max-width: 620px; margin-block-start: 18px; text-align: center;')
    k += box('sp-cta', button('sp-b', 'Book a demo', DEMO, size='md'), css='display: flex; justify-content: center; width: 100%; padding: 0px; margin-block-start: 28px;')
    top = col('sp-top', k, css='align-items: center; width: 100%;')
    chip = ('position: absolute; width: max-content; padding: 8px 14px; border-radius: 999px; '
            'background-image: linear-gradient(145deg, rgba(255,255,255,0.86), rgba(255,255,255,0.6)); '
            'backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); '
            'box-shadow: 0px 0px 0px 1px rgba(148,67,236,0.16), 0px 10px 24px 0px rgba(90,36,158,0.12); '
            'transition: transform 0.25s ease, box-shadow 0.25s ease; '
            '&:hover{transform: translateY(-3px); box-shadow: 0px 0px 0px 1px rgba(148,67,236,0.28), 0px 16px 30px 0px rgba(90,36,158,0.18);} '
            '@media(--mobile){padding: 6px 10px; font-size: 11.5px;}')
    chips = (('Progress note', 'left: 12%; top: 14%;', False), ('Lab results', 'left: 22%; top: 44%;', False), ('Op report', 'left: 8%; top: 74%;', False),
             ('CPT', 'right: 12%; top: 14%;', True), ('ICD-10', 'right: 22%; top: 44%;', True), ('HCPCS', 'right: 8%; top: 74%;', True))
    c = box('sp-tile', img('sp-logo', 'sophus-mark-light', css=(
        'display: block; width: 42px; height: auto; opacity: 0.7; '
        'filter: drop-shadow(0px 0px 10px rgba(235,169,255,0.55)) drop-shadow(0px 4px 8px rgba(35,0,76,0.35));')), css=(
        'position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); display: flex; align-items: center; justify-content: center; '
        'width: 88px; height: 88px; padding: 0px; border-radius: 22px; '
        f'background-image: radial-gradient(80% 80% at 30% 20%, #B35FFF 0%, rgba(179,95,255,0) 70%), linear-gradient(145deg, #762FC6, {PURPLE_D}); '
        'box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.25), 0px 18px 40px 0px rgba(90,36,158,0.35); '
        '@media(--mobile){width: 70px; height: 70px; border-radius: 18px;}'))
    for i, (label, pos, code) in enumerate(chips):
        look = (f'font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; font-weight: 600; color: {NAVY}; ' if code
                else f'{F} font-size: 13px; font-weight: 500; color: {PURPLE_D}; ')
        middle = ' @media(--mobile){display: none;}' if i in (1, 4) else ''
        c += p(f'sp-c{i}', label, css=look + 'line-height: 1.5; margin: 0px; ' + pos + ' ' + chip + middle)
    bleed = box('sp-bleed', '', css=(
        'position: absolute; top: 0px; bottom: 0px; left: 50%; width: 100vw; transform: translateX(-50%); padding: 0px; pointer-events: none; '
        f"background-image: url('{MEDIA['sophus-speed-lines']['url']}'); background-repeat: no-repeat; background-size: 100% 100%; background-position: center center;"))
    lines = box('sp-lines', bleed + c, css=(
        'position: relative; width: 100%; height: 360px; padding: 0px; margin-block-start: 0px; '
        'background-image: radial-gradient(22% 46% at 50% 50%, rgba(169,70,244,0.20) 0%, rgba(169,70,244,0) 75%); '
        'background-repeat: no-repeat; background-size: 100% 100%; background-position: center center; '
        '@media(--tablet){height: 300px;} @media(--mobile){height: 220px;}'))
    big = p('sp-num', '0:32', css=text(236, 0.9, INK, 500, '-0.06em', (
        'font-variant-numeric: tabular-nums; text-align: center; '
        '@media(--laptop){font-size: 210px;} @media(--tablet_extra){font-size: 190px;} @media(--tablet){font-size: 160px;} @media(--mobile){font-size: 112px;}')))
    big += p('sp-cap', 'Average coding time per claim, down from 2:30', cls=['global-text'], css=f'margin: 14px 0px 0px 0px; font-size: 15px; color: {SLATE}; text-align: center;')
    big += p('sp-note', 'Our figures, from one anonymous Sophus deployment', css=text(12.5, 1.5, MUTED, extra='margin-block-start: 4px; text-align: center;'))
    bottom = col('sp-bot', big, css='align-items: center; width: 100%; margin-block-start: -12px;')
    return section('s4', top + lines + bottom, css='overflow: hidden;')


# ================================================================ 5. Manager band
def manager():
    l = p('mb-eye', 'For coding managers', css=text(12, 1.5, SKY, 500, '0.12em', 'text-transform: uppercase;'))
    l += h2('mb-h2', 'Run the whole coding team from one queue.', 'color: #FFFFFF; margin-block-start: 14px; text-wrap: balance;')
    rows = ''
    for i, (lab, val) in enumerate((('Coder throughput', '4.7×'), ('Coding accuracy', '95%'))):
        rows += flex(f'mb-r{i}', p(f'mb-r{i}l', lab, cls=['global-text'], css='font-size: 14px; color: rgba(255,255,255,0.82); margin: 0px;')
                     + p(f'mb-r{i}v', val, css=text(34, 1.5, '#FFFFFF', 500, '-0.03em', '@media(--mobile){font-size: 28px;}')),
                     css=('display: flex; flex-direction: row; justify-content: space-between; align-items: baseline; gap: 16px; width: 100%; '
                          'padding: 18px 0px; border-top: 1px solid rgba(255,255,255,0.16);'
                          + (' border-bottom: 1px solid rgba(255,255,255,0.16);' if i == 1 else '')))
    l += box('mb-rows', rows, css='display: flex; flex-direction: column; width: 100%; padding: 0px; margin-block-start: 36px;')
    left = col('mb-l', l, cls=['w-45'])
    feats = (('assign', 'Assign claims', 'Select unassigned claims and route them to the coder with the lightest load.'),
             ('review', 'Review queue', 'Flagged and submitted claims land in one list, ready to approve or send back.'),
             ('returns', 'Auditor returns', 'Returned claims go back to the coder with the note and the fix.'),
             ('audit', 'Audit trail', 'Every code, edit and approval is logged in HIPAA-secure audit records.'))
    cells = ''
    for i, (ic, t, d) in enumerate(feats):
        head = flex(f'mb-f{i}h', box(f'mb-f{i}i', img(f'mb-f{i}img', f'sophus-icon-{ic}', css='display: block; width: 22px; height: 22px; object-fit: contain;'),
                                     css='display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; padding: 0px; '
                                         'border-radius: 10px; background-color: #FFFFFF; flex-shrink: 0; transition: transform 0.25s ease;')
                    + h(f'mb-f{i}t', 'h3', t, css=text(17, 1.5, '#FFFFFF', 500)),
                    css='display: flex; flex-direction: row; align-items: center; gap: 12px; padding: 0px;')
        cells += box(f'mb-f{i}', head + p(f'mb-f{i}d', d, cls=['global-text'], css='font-size: 14.5px; line-height: 1.6; color: rgba(255,255,255,0.82); margin: 0px;'),
                     css='display: flex; flex-direction: column; gap: 12px; padding: 0px; &:hover [class*="e-div-block"]{transform: translateY(-2px);}')
    right = grid('mb-g', cells, css=(
        'display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto; gap: 36px 40px; width: 48%; padding: 0px; align-content: start; '
        '@media(--tablet){width: 100%;} @media(--mobile){grid-template-columns: 1fr; gap: 28px;}'))
    band = row('mb-row', left + right, 'align-items: flex-start;', gap='6%')
    panel = box('mb', band, css=(
        'display: flex; width: 100%; padding: 72px; border-radius: 24px; overflow: hidden; color: #FFFFFF; '
        'background-image: radial-gradient(60% 80% at 100% 0%, rgba(58,150,204,0.55) 0%, rgba(58,150,204,0) 70%), '
        'radial-gradient(55% 80% at 0% 100%, rgba(118,47,198,0.45) 0%, rgba(118,47,198,0) 70%); '
        f'background-color: {NAVY}; '
        '@media(--tablet_extra){padding: 56px;} @media(--tablet){padding: 44px 36px;} @media(--mobile){padding: 32px 22px; border-radius: 18px;}'))
    return section('s5', panel)


# ================================================================ 6. Roles tabs
def seats():
    top = row('st-top', h2('st-h2', 'Built for every seat in the coding workflow.', 'width: 55%; text-wrap: balance; @media(--tablet){width: 100%;}')
              + button('st-b', 'Book a demo', DEMO, size='md', css='@media(--mobile_extra){align-self: flex-start;}'), 'align-items: flex-end;', stack='mobile_extra')
    roles = (('Coders', 'Approve codes instead of keying them.',
              'Each claim opens with codes suggested and evidence highlighted. Accept, edit or query the provider, then move to the next chart.', 'sophus-seat-coders'),
             ('Coding managers', 'See every coder’s output against target.',
              'Track claims completed per coder per day, rebalance workloads and assign new claims from the manager view.', 'sophus-seat-managers'),
             ('Billing companies', 'Code for every client from one queue.',
              'Filter by client, see volume per account and take on new practices without adding coders for each one.', 'sophus-seat-billing'))
    tab_css = (f'{F} display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 12px; width: 100%; '
               f'padding: 16px 20px; border: 0px; border-radius: 16px; background-color: rgba(3,103,161,0.06); color: {INK}; cursor: pointer; '
               'transition: background-color 0.2s cubic-bezier(0.2,0,0,1), color 0.2s ease, box-shadow 0.12s ease; '
               '&:hover{background-color: rgba(3,103,161,0.12);} '
               f'&[aria-selected="true"]{{background-color: {NAVY}; color: #FFFFFF;}} '
               '&:focus-visible{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.35);} '
               '& p{color: inherit;} @media(--mobile){padding: 14px 16px;}')
    tabs = ''
    for i, (name, *_r) in enumerate(roles):
        tabs += b.el('e-tab', f'st-t{i}', p(f'st-t{i}l', name, css=f'{F} font-size: 15px; font-weight: 500; line-height: 1.5; margin: 0px;')
                     + p(f'st-t{i}n', f'0{i + 1}', css=f'{F} font-size: 13px; font-weight: 500; line-height: 1.5; opacity: 0.8; margin: 0px;'), css=tab_css)
    menu = b.el('e-tabs-menu', 'st-menu', tabs, css=(
        'display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; width: 100%; padding: 0px; '
        '@media(--mobile_extra){grid-template-columns: 1fr;}'))
    panels = ''
    for i, (name, t, d, image) in enumerate(roles):
        txt = col(f'st-c{i}l', h(f'st-c{i}h', 'h3', t, cls=['heading-h3'], css=f'font-weight: 500; line-height: 1.15; letter-spacing: -0.025em; color: {INK}; margin: 0px; text-wrap: balance;')
                  + lead(f'st-c{i}p', d, 'max-width: 420px; margin-block-start: 16px; font-size: 15px; @media(--tablet){max-width: 100%;}'),
                  css='width: 46%; padding: 48px; @media(--tablet_extra){padding: 32px;} @media(--tablet){padding: 24px 12px 8px 12px;}')
        pic = col(f'st-c{i}r', img(f'st-c{i}img', image, css='display: block; width: 100%; height: auto; border-radius: 16px;'), css='width: 50%;')
        panels += b.el('e-tab-content', f'st-c{i}', row(f'st-c{i}row', txt + pic, 'align-items: center;', gap='4%'),
                       css='display: block; width: 100%; padding: 0px; margin-block-start: 10px;')
    area = b.el('e-tabs-content-area', 'st-area', panels, css='display: block; width: 100%; padding: 0px;')
    t = b.el('e-tabs', 'st', menu + area, cfg={'default-active-tab': 0}, css=(
        f'display: flex; flex-direction: column; gap: 0px; width: 100%; margin-block-start: 40px; padding: 10px; border-radius: 24px; {GLASS} '
        '@media(--mobile){padding: 8px; border-radius: 18px;}'))
    return section('s6', top + t)


# ================================================================ 7. Performance widgets
def performance():
    k = h2('pf-h2', 'Know how Sophus and your team are performing.', 'max-width: 720px; text-align: center; text-wrap: balance;')
    k += lead('pf-lead', 'The manager view tracks how often coders keep Sophus’s suggestions, by code type and by coder.',
              'max-width: 600px; margin-block-start: 18px; text-align: center;')
    top = col('pf-top', k, css='align-items: center; width: 100%;')
    card = (f'display: flex; flex-direction: column; gap: 10px; padding: 28px; border-radius: 16px; {GLASS} '
            'transition: box-shadow 0.25s ease, transform 0.25s ease; '
            '&:hover{transform: translateY(-4px); box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.12), inset 0px 1px 0px 0px rgba(255,255,255,0.9), 0px 22px 44px -12px rgba(2,40,66,0.16);} '
            '@media(--tablet){padding: 20px;} @media(--mobile){padding: 22px;}')
    inner = 'margin-block-start: 14px; border-radius: 16px; background-color: #FFFFFF; box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.08), 0px 8px 20px 0px rgba(2,40,66,0.05);'
    ht = lambda cid, t: h(cid, 'h3', t, css=text(20, 1.1, INK, 500, '-0.02em', 'text-align: center;'))
    pt = lambda cid, t: p(cid, t, cls=['global-text'], css=f'font-size: 14px; line-height: 1.55; color: {SLATE}; margin: 0px; text-align: center;')
    c1 = ht('pf1h', 'AI coder performance') + pt('pf1p', 'Share of Sophus suggestions your coders keep.')
    c1 += box('pf1k', img('pf1k-m', 'sophus-mark-white', css='position: absolute; right: -24px; top: -26px; width: 110px; height: auto; opacity: 0.2; filter: brightness(0) invert(1); pointer-events: none;')
              + p('pf1k-e', 'Last 30 days', css=text(11, 1.5, 'rgba(255,255,255,0.86)', 500, '0.1em', 'text-transform: uppercase; position: relative;'))
              + p('pf1k-v', '87%', css=text(56, 1, '#FFFFFF', 400, '-0.04em', 'margin-block-start: 10px; position: relative;'))
              + p('pf1k-l', 'of AI-suggested codes kept by coders', css=text(13, 1.5, 'rgba(255,255,255,0.86)', extra='margin-block-start: 8px; position: relative;')),
              css=('display: flex; flex-direction: column; margin-block-start: 14px; padding: 24px; border-radius: 16px; overflow: hidden; position: relative; '
                   f'background-image: radial-gradient(80% 90% at 100% 0%, #C488FC 0%, rgba(196,136,252,0) 65%), linear-gradient(145deg, #762FC6, {PURPLE_D}); '
                   'box-shadow: 0px 14px 30px 0px rgba(90,36,158,0.22);'))
    bars = ''
    for i, (lab, v) in enumerate((('CPT', 91), ('ICD-10', 84), ('Modifiers', 78))):
        bars += grid(f'pf2r{i}', p(f'pf2r{i}l', lab, css=text(13, 1.5, INK, 500))
                     + box(f'pf2r{i}t', box(f'pf2r{i}f', '', css=f'width: {v}%; height: 100%; padding: 0px; border-radius: 4px; background-color: {PURPLE};'),
                           css='height: 8px; padding: 0px; border-radius: 4px; background-color: #F1EAF9; overflow: hidden;')
                     + p(f'pf2r{i}v', f'{v}%', css=text(13, 1.5, INK, 500, extra='text-align: right;')),
                     css='display: grid; grid-template-columns: 76px 1fr 38px; grid-template-rows: auto; gap: 12px; align-items: center; padding: 0px; '
                         '@media(--mobile){grid-template-columns: 76px 1fr 38px;}')
    c2 = ht('pf2h', 'Acceptance by code type') + pt('pf2p', 'Where coders agree with Sophus most, and where they edit.')
    c2 += box('pf2k', bars, css=f'display: flex; flex-direction: column; gap: 16px; padding: 22px; {inner}')
    lb = ''
    for i, (n, v) in enumerate((('Abdullah M.', 268), ('Abner M.', 254), ('Abraham S.', 241))):
        badge = (f'background-color: {PURPLE}; color: #FFFFFF;' if i == 0 else f'background-color: #F1EAF9; color: {SLATE};')
        lb += grid(f'pf3r{i}', p(f'pf3r{i}n', str(i + 1), css=text(12, 1, SLATE if i else '#FFFFFF', 600, extra=(
                        f'display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 999px; {badge}')))
                   + p(f'pf3r{i}l', n, css=text(13.5, 1.5, INK))
                   + p(f'pf3r{i}v', str(v), css=text(13.5, 1.5, INK, 600, extra='text-align: right;')),
                   css=('display: grid; grid-template-columns: 28px 1fr auto; grid-template-rows: auto; gap: 12px; align-items: center; padding: 11px 0px; '
                        + ('' if i == 2 else 'border-bottom: 1px solid rgba(3,103,161,0.07); ') + '@media(--mobile){grid-template-columns: 28px 1fr auto;}'))
    c3 = ht('pf3h', 'Coder leaderboard') + pt('pf3p', 'Claims completed this week, across the whole team.')
    c3 += box('pf3k', lb, css=f'display: flex; flex-direction: column; padding: 12px 22px; {inner}')
    g = grid('pf-g', box('pf1', c1, css=card) + box('pf2', c2, css=card) + box('pf3', c3, css=card), css=(
        'display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: auto; gap: 16px; width: 100%; padding: 0px; margin-block-start: 48px; '
        '@media(--tablet){gap: 12px;} @media(--mobile_extra){grid-template-columns: 1fr;} @media(--mobile){grid-template-columns: 1fr; margin-block-start: 32px;}'))
    tag = flex('pf-tag', p('pf-tag-b', 'Manager view', css=text(11, 1.5, '#FFFFFF', 600, '0.06em', (
                   f'text-transform: uppercase; padding: 5px 10px; border-radius: 999px; background-color: {NAVY}; white-space: nowrap;')))
               + p('pf-tag-t', 'Sample data from the Sophus manager dashboard', css=text(13, 1.5, SLATE)),
               css=('display: flex; flex-direction: row; align-items: center; gap: 10px; width: max-content; max-width: 100%; margin-block-start: 28px; '
                    'padding: 5px 16px 5px 5px; border-radius: 999px; background-color: rgba(255,255,255,0.55); box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.10); '
                    '@media(--mobile){padding: 8px 14px; border-radius: 16px; flex-wrap: wrap; justify-content: center;}'))
    return section('s7', top + g + tag)


# ================================================================ 8. Marquee + floating cards
def marquee():
    words = ''
    for i in range(4):
        words += p(f'mq-w{i}', 'Code every chart faster', css=text(200, 1, INK, 500, '-0.055em', (
            'white-space: nowrap; flex-shrink: 0; @media(--tablet_extra){font-size: 160px;} @media(--tablet){font-size: 130px;} @media(--mobile){font-size: 88px;}')))
        words += img(f'mq-i{i}', 'sophus-mark-white', css=(
            'display: block; flex-shrink: 0; width: 100px; height: auto; opacity: 0.18; filter: brightness(0.2); '
            '@media(--tablet){width: 64px;} @media(--mobile){width: 44px;}'))
    track = flex('mq-track', words, css=(
        'display: flex; flex-direction: row; flex-wrap: nowrap; align-items: center; gap: 64px; width: max-content; padding: 0px 64px 0px 0px; '
        'animation: sophus-marquee 60s linear infinite; will-change: transform; '
        '@media(--tablet){gap: 40px; padding-inline-end: 40px;} @media(--mobile){gap: 32px; padding-inline-end: 32px;}'))
    band = box('mq-band', track, css=(
        'position: absolute; left: 0px; right: 0px; top: 50%; transform: translateY(-50%); width: 100%; padding: 0px; overflow: hidden; pointer-events: none;'))
    card = lambda cid, name, pos, w: img(cid, name, css=(
        f'position: absolute; {pos} width: {w}px; height: auto; display: block; z-index: 2; '
        'transition: transform 0.3s ease; &:hover{transform: translateY(-6px);} '
        '@media(--tablet){display: none;}'))
    k = band
    k += card('mq-pay', 'sophus-card-payer', 'left: 6%; top: 6%;', 330)
    k += card('mq-sta', 'sophus-card-status', 'left: 4%; bottom: 6%;', 350)
    k += card('mq-kep', 'sophus-card-kept', 'right: 5%; top: 8%;', 330)
    k += card('mq-aud', 'sophus-card-audit', 'right: 6%; bottom: 8%;', 320)
    k += img('mq-ph', 'sophus-card-phone', alt=None, css=(
        'position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 400px; max-width: 92%; height: auto; display: block; z-index: 3; '
        '@media(--mobile){width: 320px;}'))
    stage = box('mq', k, css='position: relative; width: 100%; height: 640px; padding: 0px; @media(--tablet){height: 560px;} @media(--mobile){height: 460px;}')
    return section('s8', stage, css='overflow: hidden; padding-inline-start: 0px; padding-inline-end: 0px;')


# ================================================================ 9. Testimonials (real, from the site)
def testimonials():
    photos = ''
    for i, (q, n, r, mid) in enumerate(TESTIMONIALS):
        photos += img(f'ts-p{i}', None, alt=n, mid=mid, css=(
            'display: block; grid-area: 1 / 1; width: 100%; height: auto; aspect-ratio: 680 / 860; object-fit: cover; border-radius: 24px; '
            'box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.08), 0px 24px 56px 0px rgba(2,40,66,0.10); transition: opacity 0.4s ease; '
            + ('' if i == 0 else 'opacity: 0; visibility: hidden;')))
    left = col('ts-l', box('ts-photos', photos, css='display: grid; width: 100%; max-width: 520px; padding: 0px; @media(--tablet){max-width: 420px; margin: 0px auto;}'),
               cls=['w-45'], css='align-items: center;')
    r = p('ts-eye', 'What our clients say', css=text(13, 1.5, BLUE, 500, '0.16em', 'text-transform: uppercase;'))
    r += box('ts-mark', '', css=(
        'width: 40px; height: 36px; padding: 0px; margin: 28px 0px 0px 6px; '
        f'background-image: linear-gradient({BLUE}, {BLUE}), linear-gradient({BLUE}, {BLUE}); background-repeat: no-repeat; '
        'background-size: 12px 36px, 12px 36px; background-position: 0px 0px, 20px 0px; transform: skewX(-18deg);'))
    quotes = ''
    for i, (q, n, rl, mid) in enumerate(TESTIMONIALS):
        hide = '' if i == 0 else 'opacity: 0; visibility: hidden;'
        quotes += box(f'ts-q{i}', p(f'ts-q{i}t', q, css=text(36, 1.4, INK, 400, '-0.02em', (
                            'text-wrap: pretty; @media(--laptop){font-size: 32px;} @media(--tablet){font-size: 26px;} @media(--mobile){font-size: 21px;}')))
                      + p(f'ts-q{i}n', n, css=text(18, 1.5, INK, 500, extra='margin-block-start: 40px; padding-block-start: 28px; border-top: 1px solid rgba(3,103,161,0.12);'))
                      + p(f'ts-q{i}r', rl, cls=['global-text'], css=f'font-size: 16px; color: {MUTED}; margin: 6px 0px 0px 0px;'),
                      css=f'display: flex; flex-direction: column; grid-area: 1 / 1; padding: 0px; transition: opacity 0.4s ease; {hide}')
    r += box('ts-quotes', quotes, css='display: grid; width: 100%; padding: 0px; margin-block-start: 36px;')
    nav_btn = (f'{F} display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; padding: 0px; border: 0px; '
               f'border-radius: 999px; background-color: rgba(255,255,255,0.7); box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.14); color: {INK}; '
               'cursor: pointer; transition: background-color 0.18s ease, box-shadow 0.18s ease, color 0.18s ease; '
               f'&:hover{{background-color: {NAVY}; color: #FFFFFF; box-shadow: 0px 0px 0px 1px {NAVY};}} '
               '&:focus-visible{outline: none; box-shadow: 0px 0px 0px 3px rgba(3,103,161,0.35);} & p{color: inherit;} '
               '@media(--mobile){width: 46px; height: 46px;}')
    nav = p('ts-count', f'1 / {len(TESTIMONIALS)}', css=text(16, 1.5, MUTED, extra='margin-inline-end: 6px;'))
    nav += box('ts-prev', p('ts-prev-l', '←', css='font-size: 18px; line-height: 1; margin: 0px;'), tag='e-div-block', cfg={'tag': 'button'}, css=nav_btn)
    nav += box('ts-next', p('ts-next-l', '→', css='font-size: 18px; line-height: 1; margin: 0px;'), tag='e-div-block', cfg={'tag': 'button'}, css=nav_btn)
    r += flex('ts-nav', nav, css='display: flex; flex-direction: row; align-items: center; gap: 14px; padding: 0px; margin-block-start: 24px;')
    r += b.el('e-button', 'ts-more', cfg={'text': 'Read more client stories →', 'link': {'destination': STORIES_URL}}, css=(
        f'{F} display: inline-flex; padding: 0px; margin-block-start: 28px; font-size: 17px; font-weight: 500; line-height: 1.5; color: {BLUE}; '
        f'background-color: transparent; border: 0px; text-decoration: none; transition: color 0.15s ease; &:hover{{color: {BLUE_H}; text-decoration: underline;}} {FOCUS}'))
    right = col('ts-r', r, cls=['w-50'])
    return section('s9', row('ts-row', left + right, gap='6%'))


# ================================================================ 10. Demo form + wordmark
def demo():
    l = pill('d-pill', 'Book a demo')
    l += h2('d-h2', 'Bring your own charts to the demo.', 'margin-block-start: 20px; text-wrap: balance;')
    l += lead('d-lead', 'Thirty minutes with a coding specialist. We code a sample of your de-identified charts live and show the evidence for each code.',
              'width: 100%; margin-block-start: 16px; padding-block-end: 24px; border-bottom: 1px solid rgba(3,103,161,0.10);')
    checks = (('Your charts, coded live', 'Compare Sophus’s codes and evidence with your coders’ work.'),
              ('Your payers’ rules', 'See the edits that apply to your specialty and payer mix.'),
              ('Coder and manager views', 'Walk through review, assignment and reporting, then scope the EHR connection.'))
    li = ''
    for i, (t, d) in enumerate(checks):
        li += grid(f'd-c{i}', p(f'd-c{i}i', '✓', css=text(13, 1, GREEN_T, 600, extra=(
                        'display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 999px; '
                        'background-color: rgba(126,176,62,0.16);')))
                   + box(f'd-c{i}b', h(f'd-c{i}t', 'h3', t, css=text(17, 1.5, INK, 500))
                         + p(f'd-c{i}d', d, cls=['global-text'], css=f'font-size: 14.5px; line-height: 1.55; color: {SLATE}; margin: 4px 0px 0px 0px;'),
                         css='display: flex; flex-direction: column; padding: 0px;'),
                   css='display: grid; grid-template-columns: 28px 1fr; grid-template-rows: auto; gap: 12px; padding: 0px; '
                       '@media(--mobile){grid-template-columns: 28px 1fr;}')
    l += box('d-list', li, css='display: flex; flex-direction: column; gap: 20px; width: 100%; padding: 0px; margin-block-start: 24px;')
    left = col('d-l', l, cls=['w-50'])

    head = grid('df-head', img('df-logo', 'sophus-mark', css='display: block; width: 26px; height: auto; margin-block-start: 3px;')
                + box('df-ht', h('df-h', 'h3', 'Book your Sophus demo', css=text(22, 1.5, INK, 500, '-0.02em'))
                      + p('df-sub', 'Tell us a little about your coding team.', cls=['global-text'], css=f'font-size: 14px; color: {SLATE}; margin: 4px 0px 0px 0px;'),
                      css='display: flex; flex-direction: column; padding: 0px;'),
                css='display: grid; grid-template-columns: 26px 1fr; grid-template-rows: auto; gap: 12px; padding: 0px; @media(--mobile){grid-template-columns: 26px 1fr;}')
    label = text(13, 1.5, INK, 500, extra='display: block; margin-block-end: 6px; & span{color: #E0533D; margin-inline-start: 2px;}')
    field = (f'{F} display: block; width: 100%; height: 44px; padding: 0px 14px; margin: 0px; border: 0px; border-radius: 8px; '
             f'background-color: #F3F8FC; font-size: 15px; line-height: 1.5; color: {INK}; outline: none; '
             'box-shadow: inset 0px 0px 0px 1px rgba(3,103,161,0.18); transition: background-color 0.12s ease, box-shadow 0.12s ease; '
             '&::placeholder{color: #9AA7B2;} &:hover{box-shadow: inset 0px 0px 0px 1px rgba(3,103,161,0.32);} '
             f'&:focus{{background-color: #FFFFFF; box-shadow: inset 0px 0px 0px 2px {BLUE}, 0px 0px 0px 3px rgba(3,103,161,0.22);}}')
    chevron = ('appearance: none; -webkit-appearance: none; padding-inline-end: 38px; cursor: pointer; '
               "background-image: url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E"
               "%3Cpath d='M1 1.5l5 5 5-5' fill='none' stroke='%236B7A87' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\"); "
               'background-repeat: no-repeat; background-position: right 14px center; background-size: 12px 8px;')
    fields = ''
    inputs = (('name', 'Name', 'text', 'Jane Smith', True), ('org', 'Organization', 'text', 'Riverside Billing Group', False),
              ('email', 'Work email', 'email', 'you@company.com', True), ('phone', 'Phone', 'tel', '(555) 000-0000', False))
    for key, lab, typ, ph, req in inputs:
        fields += box(f'df-f-{key}', b.el('e-form-label', f'df-l-{key}', cfg={'text': lab + (' <span>*</span>' if req else ''), 'input-id': f'sophus-{key}'}, css=label)
                      + b.el('e-form-input', f'df-i-{key}', cfg={'type': typ, 'placeholder': ph, 'required': req, '_cssid': f'sophus-{key}'}, css=field),
                      css='width: 100%; padding: 0px;')
    selects = (('volume', 'Charts per month', 'Select a range', ['Under 2,000', '2,000–10,000', '10,000–50,000', 'Over 50,000']),
               ('role', 'Your role', 'Select a role', ['Medical coder', 'Coding manager', 'Billing company / RCM', 'Practice owner', 'Other']))
    for key, lab, ph, opts in selects:
        fields += box(f'df-f-{key}', b.el('e-form-label', f'df-l-{key}', cfg={'text': lab, 'input-id': f'sophus-{key}'}, css=label)
                      + b.el('e-form-select', f'df-s-{key}', cfg={'name': key, 'options': [{'key': o, 'value': o} for o in [ph] + opts],
                                                                    'has-default-value': True, 'value': ph, '_cssid': f'sophus-{key}'},
                             css=field + ' ' + chevron),
                      css='width: 100%; padding: 0px;')
    consent = ('By checking this box, you agree to receive SMS messages from MedCare MSO about follow-ups, meeting notifications and medical billing '
               'services. Reply STOP to opt out at any time, or HELP to 800-640-6409 for assistance. Message and data rates may apply; frequency varies. '
               'See our <a href="https://medcaremso.com/privacy-policy/">Privacy Policy</a> and '
               '<a href="https://medcaremso.com/terms-and-conditions/">Terms &amp; Conditions</a>.')
    fields += grid('df-f-sms', b.el('e-form-checkbox', 'df-cb', cfg={'name': 'sms_consent', 'value': 'yes', 'required': False, 'has-default-value': True, 'checked': True, '_cssid': 'sophus-sms'}, css=(
                        'width: 16px; height: 16px; margin: 2px 0px 0px 0px; accent-color: #7EB03E; cursor: pointer;'))
                   + b.el('e-form-label', 'df-l-sms', cfg={'text': consent, 'input-id': 'sophus-sms'}, css=text(11.5, 1.5, MUTED, extra=(
                       f'display: block; cursor: pointer; & a{{color: {BLUE}; text-decoration: none;}} & a:hover{{text-decoration: underline;}}'))),
                   css='display: grid; grid-template-columns: 18px 1fr; grid-template-rows: auto; gap: 10px; grid-column: 1 / -1; padding: 0px; '
                       '@media(--mobile){grid-template-columns: 18px 1fr;}')
    fields += b.el('e-form-submit-button', 'df-b', cfg={'text': 'Book my demo'}, cls=['global-btn'], css=(
        f'grid-column: 1 / -1; display: flex; align-items: center; justify-content: center; width: 100%; height: 52px; padding: 0px 28px; '
        f'border: 0px; border-radius: 999px; background-color: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 500; line-height: 1; cursor: pointer; '
        f'transition: background-color 0.18s cubic-bezier(0.2,0,0,1), box-shadow 0.12s ease; &:hover{{background-color: {BLUE_H};}} {FOCUS}'))
    fields += p('df-note', 'A member of our team will reply within 12 hours.', css=text(12.5, 1.5, MUTED, extra='grid-column: 1 / -1; text-align: center;'))
    fields += b.el('e-form-success-message', 'df-ok', p('df-okt', '<strong>Thanks, your request is in.</strong> A member of our team will contact you within 12 hours to schedule your demo.',
                                                        css=text(15, 1.6, SLATE, extra=f'& strong{{display: block; font-size: 18px; font-weight: 600; color: {GREEN_T}; margin-bottom: 6px;}}')),
                   css='grid-column: 1 / -1; padding: 24px; border-radius: 16px; background-color: #F1F8EC; box-shadow: inset 0px 0px 0px 1px rgba(126,176,62,0.3);')
    fields += b.el('e-form-error-message', 'df-err', p('df-errt', 'Something went wrong. Please check the fields and try again.', css=text(14, 1.5, '#C8412C')),
                   css='grid-column: 1 / -1; padding: 0px;')
    form = b.el('e-form', 'df-form', fields, cfg={'form-name': 'Sophus AI Medical Coder demo request', 'actions-after-submit': ['email', 'collect-submissions'],
                                             'email': {'to': ['mkamran@medcaremso.com', 'fashraf@medcaremso.com'], 'subject': 'New Sophus AI Medical Coder demo request',
                                                       'message': '[all-fields]', 'from': 'email@medcaremso.com', 'from-name': 'MedCare MSO', 'send-as': 'html'}}, css=(
        'display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto; gap: 16px 18px; width: 100%; padding: 0px; margin-block-start: 28px; '
        '@media(--mobile){grid-template-columns: 1fr;}'))
    card = col('d-r', head + form, cls=['w-45'], css=(
        'align-items: stretch; padding: 36px; border-radius: 16px; background-color: #FFFFFF; '
        'box-shadow: 0px 0px 0px 1px rgba(3,103,161,0.10), 0px 24px 60px 0px rgba(2,40,66,0.10); @media(--mobile){padding: 24px 20px;}'))
    panel = box('d-box', row('d-row', left + card, gap='6%'), css=(
        f'display: flex; width: 100%; padding: 72px; border-radius: 24px; {GLASS} '
        '@media(--tablet_extra){padding: 48px;} @media(--tablet){padding: 36px 28px;} @media(--mobile){padding: 24px 16px; border-radius: 18px;}'))
    mark = flex('wm', img('wm-logo', 'sophus-mark', css=(
                    'display: block; flex-shrink: 0; width: 160px; height: auto; opacity: 0.22; filter: blur(1.5px); margin-block-start: 62px; '
                    '@media(--tablet){width: 90px; margin-block-start: 36px;} @media(--mobile){width: 48px; margin-block-start: 26px;}'))
                + p('wm-t', 'Sophus AI', css=text(230, 0.9, 'transparent', 600, '-0.055em', (
                    'white-space: nowrap; margin-block-start: 42px; filter: blur(1.5px); '
                    'background-image: linear-gradient(180deg, rgba(20,33,43,0.20), rgba(20,33,43,0.03) 85%); '
                    '-webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; '
                    '@media(--laptop){font-size: 200px;} @media(--tablet_extra){font-size: 160px;} @media(--tablet){font-size: 120px;} @media(--mobile_extra){font-size: 96px;} @media(--mobile){font-size: 54px; margin-block-start: 24px;}'))),
                css=('display: flex; flex-direction: row; justify-content: center; align-items: flex-start; gap: 36px; width: 100%; height: 290px; '
                     'padding: 56px 0px 0px 0px; overflow: hidden; pointer-events: none; '
                     '@media(--tablet){height: 200px; gap: 20px;} @media(--mobile){height: 120px; gap: 12px; padding-block-start: 30px;}'))
    return section('s10', panel + mark, anchor='demo', css='padding-block-end: 0px;')


SECTIONS = [hero, stats, how, speed, manager, seats, performance, marquee, testimonials, demo]


def payload(mode='replace_children', dry=False):
    global b
    b = B()
    xml = ''.join(f() for f in SECTIONS)
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes,
            'mode': mode, 'dry_run': dry}
