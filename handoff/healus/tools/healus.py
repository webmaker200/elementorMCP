"""HealUs New Page (WP page 411263) from Figma oYqLJMmgAjdLKQeLgtDSM7 node 671:593, Elementor V4 atomic.

Rules from the brief:
- global classes / variables first (parent-container, global-text, w-45/w-50, healus-* classes, HealUs* + kit colours);
- grids use plain fr tracks (no repeat()/minmax()/calc()); columns use percentage widths (no flex-basis);
- any max-width becomes 100% on small devices; small devices: 3% top/bottom, 5% left/right section spacing;
- section glows are CSS radial gradients computed from the Figma blurred ellipses (no background images).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PID = 411263
MEDIA = json.load(open(os.path.join(HERE, '..', 'media.json')))
GLOWS = json.load(open(os.path.join(HERE, '..', 'glows.json')))
DEMO = '#healus-demo'
TABS = '#healus-features'
PHONE = '<a href="tel:8006406409">800-640-6409</a>'

INK, SLATE, MUTED, GREEN, TEAL = 'var(--HealUsInk)', 'var(--HealUsSlate)', 'var(--HealUsMuted)', 'var(--HealUsGreen)', 'var(--HealUsTeal)'
GRAY, WHITE, BLACK = 'var(--DarkGray)', 'var(--PureWhite)', 'var(--PureBlack)'
F = 'font-family: var(--Poppins);'
BLUR = 'backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);'
GRAD_TEXT = ('background-image: linear-gradient(100deg, #006750 0%, #2E8A6E 55%, #5B9A35 100%); '
             '-webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;')
GRAD_BTN = 'linear-gradient(115deg, #318371 0%, #006750 100%)'


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


def p(cid, html, css='', cls=None, link=None):
    cfg = {'paragraph': html}
    if link:
        cfg['link'] = {'destination': link}
    return b.el('e-paragraph', cid, cfg=cfg, css=css, cls=cls)


def h(cid, tag, title, css='', cls=None):
    return b.el('e-heading', cid, cfg={'tag': tag, 'title': title}, css=css, cls=cls)


def img(cid, name, css='', alt=None):
    m = MEDIA[name]
    return b.el('e-image', cid, cfg={'image': {'src': {'id': m['id'], 'alt': alt if alt is not None else ''}, 'size': 'full'}}, css=css)


def button(cid, text, url, cls='healus-btn', css=''):
    return b.el('e-button', cid, cfg={'text': text, 'link': {'destination': url}}, css=css, cls=[cls])


def pill(cid, text, css=''):
    return p(cid, text, css, cls=['healus-pill'])


def pill_lg(cid, text, css=''):
    """Figma 'Frame 30': 46px pill with a 1px border, softer fill and a drop shadow."""
    return pill(cid, text, ('min-height: 46px; padding: 0px 30px; line-height: 14.4px; color: #7D7D7D; '
                            'background-color: rgba(255,255,255,0.1); '
                            'box-shadow: 0px 15px 15px 0px rgba(194,194,194,0.1), inset 0px 0px 0px 1px #9ACAA1; ' + css))


def h2(cid, title, css=''):
    return h(cid, 'h2', title, css, cls=['healus-h2'])


def lead(cid, html, css=''):
    return p(cid, html, css, cls=['global-text', 'healus-lead'])


def section(cid, kids, pt, pb, anchor=None, css=''):
    cfg = {'tag': 'section'}
    if anchor:
        cfg['attributes'] = [{'key': 'id', 'value': anchor}]
    glow = ', '.join(GLOWS[cid])
    return flex(cid, kids, cfg=cfg, cls=['parent-container'], css=(
        'display: flex; flex-direction: column; align-items: center; gap: 0px; width: 100%; position: relative; '
        f'padding-block-start: {pt}px; padding-block-end: {pb}px; padding-inline-start: 11.6%; padding-inline-end: 11.6%; '
        f'background-image: {glow}; background-repeat: no-repeat; ' + css +
        ' @media(--tablet_extra){padding-inline-start: 5%; padding-inline-end: 5%;}'
        ' @media(--tablet){padding-block-start: 3%; padding-block-end: 3%;}'))


def row(cid, kids, css='', stack='tablet', reverse=False):
    """Two-column row: percentage widths on the children, stacks below the given breakpoint."""
    return flex(cid, kids, css=(
        'display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-between; align-items: center; '
        'gap: 0px; width: 100%; padding: 0px; ' + css +
        f' @media(--{stack}){{flex-direction: {"column-reverse" if reverse else "column"}; align-items: stretch; gap: 40px;}}'))


def col(cid, kids, width_cls=None, width=None, css='', stack='tablet'):
    w = f'width: {width}; ' if width else ''
    return box(cid, kids, cls=[width_cls] if width_cls else None, css=(
        f'display: flex; flex-direction: column; align-items: flex-start; padding: 0px; {w}' + css +
        f' @media(--{stack}){{width: 100%;}}'))


def text(size, lh, color, weight=400, ls=0, extra=''):
    return (f'{F} font-size: {size}px; line-height: {lh}px; font-weight: {weight}; color: {color}; '
            + (f'letter-spacing: {ls}px; ' if ls else '') + 'margin: 0px; ' + extra)


# ================================================================ 1. Hero
def hero():
    av = ''.join(img(f'hp-a{i}', f'healus-avatar-{i}', (
        'width: 35px; height: 35px; object-fit: cover; border-radius: 50%; border: 1.5px solid #FFFFFF; '
        f'margin-inline-start: {"0px" if i == 1 else "-11px"};'), alt='') for i in (1, 2, 3))
    av += p('hp-t', 'AI-Powered healthcare', text(12, 14.4, '#7D7D7D', extra='margin-inline-start: 11px;'))
    k = flex('hp', av, css=('display: flex; flex-direction: row; align-items: center; gap: 0px; width: max-content; max-width: 100%; '
                            'height: 46px; padding: 0px 15px 0px 9px; border-radius: 31px; border: 1px solid var(--HealthGreen);'))
    k += h('h1', 'h1', 'Close the chart <span>before the patient leaves</span> the room.', (
        f'{F} font-size: 72px; line-height: 1.097; font-weight: 300; letter-spacing: -2.16px; color: {INK}; margin: 0px; '
        f'margin-block-start: 25px; & span{{font-weight: 400; {GRAD_TEXT}}} '
        '@media(--laptop){font-size: 62px; letter-spacing: -1.8px;} @media(--tablet_extra){font-size: 54px; letter-spacing: -1.5px;} '
        '@media(--tablet){font-size: 50px;} @media(--mobile){font-size: 36px; letter-spacing: -1px; margin-block-start: 20px;}'))
    k += lead('hero-p', 'HealUs is the EHR built by a billing team. Specialty templates, e-prescribing, labs, telehealth and a patient '
                        'portal share one record, so the note is finished in the visit and ready for the claim.',
              'line-height: 2; max-width: 618px; margin-block-start: 26px; @media(--tablet){max-width: 100%;} @media(--mobile){line-height: 1.8;}')

    # Work-email form (Elementor form; delivery actions are configured by the site owner)
    f = b.el('e-form-label', 'hf-l', cfg={'text': 'Work email', 'input-id': 'healus-hero-email'}, css=(
        'position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; margin: 0px; padding: 0px;'))
    f += b.el('e-form-input', 'hf-i', cfg={'type': 'email', 'placeholder': 'Work email', 'required': True, '_cssid': 'healus-hero-email'}, css=(
        f'{F} flex-grow: 1; width: 100%; min-width: 0px; height: 52px; padding: 0px; margin: 0px; border: 0px; border-radius: 0px; '
        f'background-color: transparent; box-shadow: none; outline: none; font-size: 15px; line-height: 22.5px; color: {INK}; '
        f'&::placeholder{{color: {MUTED};}}'))
    f += b.el('e-form-submit-button', 'hf-b', cfg={'text': 'Book a demo'}, cls=['healus-btn'], css=(
        'flex-shrink: 0; height: 52px; padding: 0px 8px 0px 24px; &::after{width: 36px; height: 36px; font-size: 16px;}'))
    f += b.el('e-form-success-message', 'hf-ok', p('hf-okt', 'Thanks! Our team will be in touch shortly.', text(13, 19.5, TEAL)),
              css='position: absolute; left: 24px; top: 100%; margin-top: 8px; padding: 0px;')
    f += b.el('e-form-error-message', 'hf-err', p('hf-errt', 'Something went wrong. Please check your email and try again.', text(13, 19.5, '#C0392B')),
              css='position: absolute; left: 24px; top: 100%; margin-top: 8px; padding: 0px;')
    k += b.el('e-form', 'hero-form', f, cfg={'form-name': 'HealUs hero demo request'}, css=(
        'display: flex; flex-direction: row; flex-wrap: nowrap; align-items: center; gap: 6px; position: relative; '
        'width: 520px; max-width: 100%; height: 64px; padding: 6px 6px 6px 24px; margin-block-start: 42px; border-radius: 999px; '
        'background-color: rgba(255,255,255,0.32); '
        'box-shadow: 0px 24px 50px -28px rgba(2,40,66,0.3), 0px 0px 0px 1px rgba(49,131,113,0.16), inset 0px -10px 20px -14px rgba(2,40,66,0.14), '
        'inset 0px 1px 0px 0px rgba(255,255,255,0.95), inset 0px 0px 0px 1px rgba(255,255,255,0.85); ' + BLUR +
        ' @media(--tablet){width: 100%;} @media(--mobile){padding: 6px 6px 6px 18px;}'))
    k += p('hero-note', 'No obligation&nbsp;&nbsp;•&nbsp;&nbsp;30 minutes on your own specialty',
           text(13, 19.5, MUTED, extra='margin-block-start: 22px; margin-inline-start: 3px;'))
    chip = (f'{F} display: flex; align-items: center; gap: 8px; width: max-content; height: 32px; padding: 0px 14px; margin: 0px; '
            f'border-radius: 999px; background-color: rgba(255,255,255,0.55); box-shadow: inset 0px 0px 0px 1px rgba(49,131,113,0.16); '
            f'font-size: 13px; line-height: 19.5px; font-weight: 400; color: {INK};')
    s = p('hs-l', 'Built to standard', text(12, 18, MUTED, 500, 1.44, 'text-transform: uppercase; margin-inline-end: 7px; '
                                                                    '@media(--mobile){width: 100%; margin-block-end: 4px;}'))
    s += flex('hs-1', img('hs-1i', 'healus-icon-shield', 'width: 16px; height: 16px; display: block;') + p('hs-1t', 'HIPAA', text(13, 19.5, INK)), css=chip)
    s += p('hs-2', 'HITRUST CSF', chip)
    s += p('hs-3', 'HL7 &amp; FHIR', chip)
    k += flex('hs', s, css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 10px; padding: 0px; margin-block-start: 34px;')
    left = col('hero-l', k, 'w-45', css='@media(--tablet){align-items: flex-start;}')

    r = img('hero-img', 'healus-hero-dashboard', 'display: block; width: 100%; height: auto; border-radius: 12px;',
            alt='HealUs EHR dashboard with appointments, referrals and claims')
    glass_chip = ('display: flex; flex-direction: row; align-items: center; gap: 10px; width: max-content; height: 46px; '
                  'padding: 0px 16px 0px 8px; border-radius: 16px; background-color: rgba(255,255,255,0.4); '
                  'box-shadow: 0px 18px 40px -22px rgba(2,40,66,0.3), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); '
                  + BLUR)
    tile = 'width: 32px; height: 32px; padding: 7px; border-radius: 10px; background-color: rgba(61,162,140,0.12); display: block; flex-shrink: 0;'
    cc = ''
    for i, (ic, t) in enumerate((('healus-icon-note', 'Note signed in visit'), ('healus-icon-rx', 'e-Rx sent to pharmacy'),
                                 ('healus-icon-lab', 'Lab result filed'))):
        cc += flex(f'hc{i}', img(f'hc{i}i', ic, tile) + p(f'hc{i}t', t, text(13, 19.5, INK)), css=glass_chip)
    r += flex('hc', cc, css=('display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; gap: 13px; width: 100%; '
                             'padding: 0px; margin-block-start: 25px;'))
    right = col('hero-r', r, 'w-50', css='align-items: center;')
    return section('s1', row('s1-row', left + right, 'align-items: center;'), 91, 118)


# ================================================================ 2. Stats + problems
def problems():
    stats = (('80,000+', 'Providers supported by MedCare MSO'), ('13+ yrs', 'Running revenue cycles since 2012'),
             ('[50+]', 'Specialty templates in HealUs'), ('[X] min', 'Saved per note with HealUs'))
    g = ''
    for i, (v, l) in enumerate(stats):
        border = '' if i == 0 else 'border-left: 1px solid rgba(49,131,113,0.12); '
        g += p(f'st{i}', f'<span>{v}</span>{l}', (
            f'{F} display: block; margin: 0px; padding: 0px 34px; {border}font-size: 14px; line-height: 21px; color: {SLATE}; '
            f'& span{{display: block; width: max-content; margin-bottom: 6px; font-size: 46px; line-height: 46px; font-weight: 300; '
            f'letter-spacing: -1.84px; {GRAD_TEXT}}} '
            + ('@media(--tablet){border-left: 0px;} ' if i == 2 else '') +
            '@media(--mobile){padding: 0px 16px; & span{font-size: 32px; line-height: 36px; letter-spacing: -1px;}}'))
    k = grid('stats', g, css=(
        'display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; grid-template-rows: auto; gap: 0px; width: 100%; padding: 32px 0px; '
        'border-radius: 24px; box-shadow: 0px 24px 60px -32px rgba(2,40,66,0.25), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); '
        '@media(--tablet){grid-template-columns: 1fr 1fr; row-gap: 28px;} @media(--mobile){grid-template-columns: 1fr 1fr; padding: 24px 0px;}'))
    k += p('stats-note', 'First two are MedCare MSO figures. Bracketed values are HealUs figures to confirm before launch.',
           text(12, 18, MUTED, extra='text-align: center; margin-block-start: 12px;'))
    k += pill_lg('s2-pill', 'The problem with traditional EHRs', 'margin-block-start: 106px; @media(--tablet){margin-block-start: 48px;}')
    k += h2('s2-h2', "Your EHR shouldn't be the <br>reason you chart at night", (
        f'color: {BLACK}; line-height: 1.103; text-align: center; width: 100%; max-width: 865px; margin-block-start: 23px; '
        '@media(--tablet){max-width: 100%;}'))
    k += lead('s2-p', "Most systems store the visit. They don't help you finish it. Every gap below turns <br>into clicks, callbacks or a late night.",
              'line-height: 2; text-align: center; max-width: 870px; @media(--tablet){max-width: 100%; & br{display: none;}}')
    cards = (('healus-icon-note', 'Documentation', 'Still finishing notes after the last patient leaves?'),
             ('healus-icon-rx', 'Prescribing', 'Still answering refill faxes and pharmacy callbacks between visits?'),
             ('healus-icon-lab', 'Lab results', 'Still chasing results across fax, portals and paper?'),
             ('healus-icon-contact', 'Patient contact', 'Still playing phone tag to book visits and share results?'))
    g = ''
    for i, (ic, t, d) in enumerate(cards):
        c = img(f'pc{i}i', ic, 'display: block; width: 56px; height: 56px; padding: 13px; border-radius: 16px; background-color: rgba(61,162,140,0.12);')
        c += h(f'pc{i}h', 'h3', t, text(24, 26.4, INK, 300, -0.48, 'margin-block-start: 17px; @media(--mobile){font-size: 21px;}'))
        c += p(f'pc{i}p', d, text(15, 25.5, SLATE, 300, extra='margin-block-start: 18px; max-width: 240px; @media(--tablet){max-width: 100%;}'))
        g += box(f'pc{i}', c, cls=['healus-glass'], css='display: flex; flex-direction: column; padding: 28px; background-color: rgba(255,255,255,0.2);')
    k += grid('pcards', g, css=('display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; grid-template-rows: auto; gap: 20px; width: 100%; '
                                'padding: 0px; margin-block-start: 47px; @media(--tablet){grid-template-columns: 1fr 1fr;} '
                                '@media(--mobile){grid-template-columns: 1fr; gap: 16px; margin-block-start: 32px;}'))
    bar = box('bar-l', h('bar-h', 'h3', 'HealUs changes that.', text(30, 33, INK, 300, -0.9, '@media(--mobile){font-size: 24px; line-height: 30px;}'))
              + p('bar-p', 'Charting, prescribing, labs, telehealth and patient contact in one record, wired to billing.',
                  text(15, 22.5, SLATE, 300, extra='margin-block-start: 5px;')), css='display: flex; flex-direction: column; padding: 0px;')
    bar += button('bar-b', 'See how it works', TABS, 'healus-btn-ghost', "&::after{content: '\\2193';}")
    k += flex('bar', bar, cls=['healus-glass'], css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 24px; width: 100%; '
        'padding: 26px 26px 26px 40px; margin-block-start: 20px; border-radius: 24px; background-color: rgba(255,255,255,0.2); '
        '@media(--mobile_extra){flex-direction: column; align-items: flex-start;} @media(--mobile){padding: 22px;}'))
    return section('s2', k, 24, 61)


# ================================================================ 3. Tabs (features)
TAB_NAMES = ['Charting', 'e-Prescribing', 'Labs &amp; imaging', 'Patient portal', 'Telehealth', 'Scheduling']


def tab_panel(i):
    q = f't{i}'
    nxt = TAB_NAMES[(i + 1) % len(TAB_NAMES)]
    l = h(f'{q}h', 'h3', 'Notes that are done <br>when the visit is', text(38, 43.7, INK, 300, -1.33, (
        'max-width: 560px; @media(--tablet){max-width: 100%;} @media(--mobile){font-size: 30px; line-height: 36px; letter-spacing: -0.9px;}')))
    l += p(f'{q}p', 'Specialty templates, smart phrases and a single view of history, meds and allergies keep documentation moving '
                    'while you talk with the patient.', text(16, 28.8, SLATE, 300, extra='margin-block-start: 15px; @media(--mobile){font-size: 15px; line-height: 26px;}'))
    items = (('Templates and smart phrases', 'Type a few characters; get a full, editable section.'),
             ('Everything on one screen', 'Problem list, medications, allergies, vitals and prior notes beside the note you are writing.'),
             ('AI drafting when you want it', 'Pairs with Salus · AI scribe to draft the note from the visit conversation.'))
    li = ''.join(p(f'{q}c{j}', f'<strong>{a}</strong>{d}', cls=['healus-check-item']) for j, (a, d) in enumerate(items))
    l += box(f'{q}l', li, css='display: flex; flex-direction: column; width: 100%; padding: 11px 0px 0px 0px; margin-block-start: 27px; '
                              'border-top: 1px solid rgba(49,131,113,0.12);')
    bt = button(f'{q}b', 'See it on your workflow', DEMO)
    bt += p(f'{q}n', f'Next: {nxt} →', text(14, 21, GREEN, extra='& a{color: inherit; text-decoration: none;}'), link=TABS)
    l += flex(f'{q}bt', bt, css='display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 16px 24px; padding: 0px; margin-block-start: 35px;')
    left = col(f'{q}L', l, 'w-45')

    m = box(f'{q}g', img(f'{q}gi', 'healus-progress-note', (
        'display: block; width: 100%; height: auto; border-radius: 16px; box-shadow: 0px 0px 0px 1px rgba(49,131,113,0.08);'),
        alt='HealUs progress note with completed charting sections'), css=(
        'display: block; padding: 10px; border-radius: 24px; background-color: rgba(255,255,255,0.4); '
        'box-shadow: 0px 40px 90px -40px rgba(2,40,66,0.35), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); ' + BLUR))
    fl = p(f'{q}fl', 'Avg. note time', text(11, 16.5, MUTED, 500, 1.1, 'text-transform: uppercase;'))
    fl += p(f'{q}fv', '6 min<span>↓ 41%</span>', text(36, 54, INK, 300, -1.44, (
        f'margin-block-start: 6px; & span{{margin-inline-start: 8px; font-size: 12px; line-height: 18px; font-weight: 500; letter-spacing: 0px; color: {GREEN};}}')))
    m += box(f'{q}f', fl, css=(
        'position: absolute; right: 0px; bottom: 0px; width: 220px; padding: 18px 20px; border-radius: 16px; background-color: rgba(255,255,255,0.65); '
        'box-shadow: 0px 24px 50px -24px rgba(2,40,66,0.4), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); ' + BLUR +
        ' @media(--mobile){position: relative; width: 200px; margin: -36px 0px 0px auto;}'))
    right = col(f'{q}R', m, width='41.8%', css='display: block; position: relative; padding: 0px 26px 34px 0px; '
                                              '@media(--tablet){max-width: 640px; align-self: center;} @media(--mobile){padding: 0px;}')
    return row(f'{q}row', left + right)


def features():
    l = pill('s3-pill', 'Everything in one record')
    l += h2('s3-h2', 'One patient, one chart, <br>every step of the visit', 'margin-block-start: 24px;')
    top = row('s3-top', col('s3-tl', l, 'w-45') + lead('s3-tr', 'Pick a feature to see what HealUs does at that point in the day.',
                                                        'width: 27%; @media(--tablet){width: 100%;}'), stack='tablet')
    tabs = ''
    for i, name in enumerate(TAB_NAMES):
        tabs += b.el('e-tab', f'tab{i}', p(f'tab{i}t', f'<span>{i + 1}</span>{name}', cls=['healus-tab-label']), cls=['healus-tab'])
    menu = b.el('e-tabs-menu', 'tabs-menu', tabs, css=(
        'display: flex; flex-direction: row; flex-wrap: wrap; justify-content: flex-start; gap: 4px; width: max-content; max-width: 100%; '
        'padding: 6px; border-radius: 999px; background-color: rgba(255,255,255,0.4); '
        'box-shadow: 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); ' + BLUR +
        ' @media(--tablet){width: 100%; flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none;}'))
    panels = ''.join(b.el('e-tab-content', f'tc{i}', tab_panel(i), css='display: block; padding: 0px;') for i in range(len(TAB_NAMES)))
    area = b.el('e-tabs-content-area', 'tabs-area', panels, css='display: block; padding: 0px; margin-block-start: 66px; @media(--tablet){margin-block-start: 40px;}')
    t = b.el('e-tabs', 'tabs', menu + area, cfg={'default-active-tab': 0}, css=(
        'display: flex; flex-direction: column; gap: 0px; width: 100%; padding: 0px; margin-block-start: 38px; @media(--mobile){margin-block-start: 28px;}'))
    return section('s3', top + t, 0, 90, anchor='healus-features')


# ================================================================ 4. Specialty templates
def templates():
    g = img('s4-img', 'healus-specialty-template', 'display: block; width: 100%; height: auto; border-radius: 17px; box-shadow: 0px 0px 0px 1px rgba(49,131,113,0.08);',
            alt='HealUs primary care annual wellness visit template')
    g += p('s4-cap', 'Illustrative data', text(11.7, 17.6, MUTED, extra='width: 100%; text-align: right; padding-inline-end: 12px;'))
    left = box('s4-l', g, css=(
        'display: flex; flex-direction: column; gap: 11px; width: 47%; padding: 11px; border-radius: 25.6px; background-color: rgba(255,255,255,0.1); '
        'box-shadow: 0px 42.7px 96px -42.7px rgba(2,40,66,0.35), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); '
        + BLUR + ' @media(--tablet){width: 100%;}'))
    k = pill('s4-pill', 'Specialty templates')
    k += h2('s4-h2', 'Templates that document the way <br>your specialty does', 'margin-block-start: 24px;')
    k += lead('s4-p', 'Sections, measures and common codes are set up for your specialty before go-live. Pick one to see its template.',
              'margin-block-start: 17px;')
    chips = ''
    for i, c in enumerate(('Primary care', 'Behavioral health', 'Cardiology', 'Pain management', 'Podiatry', 'Pediatrics')):
        active = ('background-color: #006750; background-image: ' + GRAD_BTN + '; box-shadow: 0px 10px 24px -12px rgba(0,103,80,0.6); '
                  'color: var(--PureWhite); font-weight: 500;') if i == 0 else ''
        chips += p(f's4c{i}', c, cls=['healus-chip'], css=active)
    k += flex('s4-chips', chips, css='display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px; padding: 0px; margin-block-start: 29px;')
    k += p('s4-ask', "Don't see yours? <a href=\"#healus-demo\">Ask about your specialty →</a>",
           text(14, 21, SLATE, extra=f'margin-block-start: 23px; & a{{color: {GREEN}; font-weight: 500; text-decoration: none;}}'))
    right = col('s4-r', k, width='42.2%')
    return section('s4', row('s4-row', left + right, reverse=True), 63, 111)


# ================================================================ 5. Comparison
def comparison():
    k = pill('s5-pill', 'Specialty templates')
    k += h2('s5-h2', 'From a filing cabinet <br>to a working chart', 'margin-block-start: 17px;')
    k += lead('s5-p', 'A traditional EHR records what happened. HealUs moves the visit forward, from check-in to signed note to claim.',
              'margin-block-start: 21px;')
    k += button('s5-b', 'Book a demo', DEMO, css='margin-block-start: 34px;')
    left = col('s5-l', k, width='42.2%')
    rows = (('Notes typed from scratch after hours', 'Specialty templates and smart phrases, with optional AI drafting'),
            ('Refill faxes and pharmacy callbacks', 'e-prescribing with EPCS and one refill queue'),
            ('Lab results by fax and outside portals', 'Bidirectional lab interfaces that file results to the chart'),
            ('A separate telehealth tool, charted twice', 'Video visits documented in the same note'),
            ('Phone-only booking and manual reminders', 'Online booking, automated reminders and waitlist fill'),
            ('Paper intake re-keyed at check-in', 'Digital intake completed before the visit'))
    c = p('cmp-h0', 'Traditional EHR', text(14, 21, MUTED, extra='padding: 22px 28px; @media(--mobile){padding: 16px 14px;}'))
    c += box('cmp-h1', img('cmp-logo', 'healus-logo', 'display: block; width: 88px; height: auto;', alt='HealUs'),
             css='display: flex; align-items: center; padding: 21.5px 28px; background-color: rgba(255,255,255,0.7); @media(--mobile){padding: 16px 14px;}')
    for i, (a, z) in enumerate(rows):
        c += p(f'cmp{i}a', f'<span>×</span>{a}', cls=['healus-cmp-no'])
        c += p(f'cmp{i}b', f'<span>✓</span>{z}', cls=['healus-cmp-yes'])
    c += box('cmp-ea', '', css='padding: 0px; border-top: 1px solid rgba(49,131,113,0.1);')
    c += p('cmp-more', 'Show all 10 differences ↓', cls=['healus-cmp-yes'], css=f'font-weight: 500; color: {GREEN};')
    table = grid('cmp', c, cls=['healus-glass'], css=(
        'display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto; gap: 0px; width: 50.7%; padding: 0px; overflow: hidden; '
        'border-radius: 24px; box-shadow: 0px 30px 70px -36px rgba(2,40,66,0.3), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); '
        '@media(--tablet){width: 100%;} @media(--mobile){grid-template-columns: 1fr 1fr;}'))
    return section('s5', row('s5-row', left + table), 54, 54)


# ================================================================ 6. Dashboards
def insight():
    l = pill('s6-pill', 'Clinical and practice insight', f'color: #7D7D7D;')
    l += h2('s6-h2', 'Know how the clinic is running without waiting for a report', 'margin-block-start: 24px;')
    top = row('s6-top', col('s6-tl', l, width='47.5%') + p('s6-tr', 'Dashboards update as notes are signed, results arrive and visits close.',
                                                          cls=['global-text', 'healus-lead'], css='font-weight: 300; width: 26.4%; @media(--tablet){width: 100%;}'),
              'align-items: flex-end;')
    w = 'color: rgba(255,255,255,0.86);'
    hd = p('gc-v', 'Visits today<span>42</span>', text(14, 21, 'rgba(255,255,255,0.86)', extra=(
        '& span{display: block; font-size: 64px; line-height: 67.2px; font-weight: 300; letter-spacing: -2.88px; color: #FFFFFF;} '
        '@media(--mobile){& span{font-size: 48px; line-height: 52px;}}')))
    hd += p('gc-d', 'vs last Tuesday<span>+9%</span>', text(13, 19.5, 'rgba(255,255,255,0.86)', extra=(
        'text-align: right; & span{display: block; font-size: 28px; line-height: 42px; font-weight: 300; letter-spacing: -0.84px; color: #FFFFFF;}')))
    c = flex('gc-top', hd, css='display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 16px; width: 100%; padding: 0px;')
    bars = ''.join(box(f'gb{i}', '', css=(f'height: {v}px; padding: 0px; border-radius: 6px 6px 2px 2px; '
                                           f'background-color: {"#FFFFFF" if i == 6 else "rgba(255,255,255,0.28)"};'))
                   for i, v in enumerate((55, 74, 65, 94, 84, 106, 120)))
    c += grid('gc-bars', bars, css=('display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr; grid-template-rows: auto; gap: 10px; '
                                    'align-items: end; width: 100%; height: 140px; padding: 10px 0px; margin-block-start: 18px; '
                                    '@media(--mobile){grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr; gap: 6px;}'))
    st = ''.join(p(f'gs{i}', f'{v}<span>{t}</span>', text(28, 42, '#FFFFFF', 300, -0.84, (
        f'& span{{display: block; font-size: 13px; line-height: 19.5px; font-weight: 400; letter-spacing: 0px; {w}}} '
        '@media(--mobile){font-size: 22px; line-height: 32px; & span{font-size: 12px; line-height: 17px;}}')))
        for i, (v, t) in enumerate((('96%', 'Notes signed same day'), ('18', 'Open care gaps'), ('7', 'Unread portal messages'))))
    c += grid('gc-stats', st, css=('display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: auto; gap: 16px; width: 100%; '
                                   'padding: 22px 0px 0px 0px; margin-block-start: 18px; border-top: 1px solid rgba(255,255,255,0.22); @media(--mobile){grid-template-columns: 1fr 1fr 1fr; gap: 10px;}'))
    c += p('gc-n', 'Illustrative data', text(11, 16.5, 'rgba(255,255,255,0.8)', extra='margin-block-start: 18px;'))
    card = box('gc', c, css=(
        'display: flex; flex-direction: column; width: 47.8%; padding: 36px 36px 40px 36px; border-radius: 20px; background-color: #006750; '
        'background-image: radial-gradient(37% 32% at 31% 108%, rgba(75,174,152,0.5) 0%, rgba(75,174,152,0) 100%), '
        'radial-gradient(140% 214% at 28% 27%, #3DA28C 0%, #006750 100%); '
        'box-shadow: 0px 51px 63.6px -20px rgba(89,89,89,0.25); @media(--tablet){width: 100%;} @media(--mobile){padding: 26px 20px 28px 20px;}'))
    items = (('01', 'rgba(255,226,121,0.45)', 'Clinical dashboards', 'Visits, open notes, pending results and refills for the day, on one screen.'),
             ('02', 'rgba(196,242,205,0.7)', 'Quality measure tracking', 'Care gaps and MIPS measures surface in the chart while the patient is still in the room.'),
             ('03', 'rgba(156,216,246,0.45)', 'Role-based views', "Providers, nurses, front desk and owners each see the work that's theirs."))
    r = ''
    for i, (n, bg, t, d) in enumerate(items):
        x = p(f'ir{i}n', n, cls=['healus-num'], css=f'background-color: {bg};')
        x += p(f'ir{i}t', f'<strong>{t}</strong>{d}', text(14, 23.1, SLATE, extra=(
            f'& strong{{display: block; margin-bottom: 3px; font-size: 20px; line-height: 30px; font-weight: 400; letter-spacing: -0.3px; color: {INK};}}')))
        r += flex(f'ir{i}', x, cls=['healus-glass'], css='display: flex; flex-direction: row; align-items: flex-start; gap: 18px; padding: 24px 26px; '
                                                         '@media(--mobile){padding: 20px; gap: 14px;}')
    last = p('ir-s', '<strong>See it. Understand it. Act on it.</strong>Every metric links back to the chart behind it.', text(14, 21, SLATE, extra=(
        f'& strong{{display: block; font-size: 22px; line-height: 33px; font-weight: 300; letter-spacing: -0.44px; color: {INK};}}')))
    last += button('ir-b', 'Book a demo', DEMO, 'healus-btn-ghost', 'height: 48px; padding: 0px 7px 0px 20px; gap: 10px; &::after{width: 34px; height: 34px;}')
    r += flex('ir-last', last, css='display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; align-items: center; '
                                   'gap: 16px; padding: 22px 26px; @media(--mobile){padding: 16px 0px;}')
    right = box('ir', r, css='display: flex; flex-direction: column; gap: 16px; width: 48.8%; padding: 0px; @media(--tablet){width: 100%;}')
    body = row('s6-row', card + right, 'align-items: flex-start; margin-block-start: 40px;')
    return section('s6', top + body, 50, 119)


# ================================================================ 7. Integrations
def integrations():
    cap = p('ph-c', ('<strong>Signed note to submitted claim, without re-keying</strong>'
                     'HealUs hands the encounter to <b>Maximus · Billing &amp; claims</b>'), text(14.3, 21.5, SLATE, extra=(
        f'& strong{{display: block; margin-bottom: 6.6px; font-size: 19.8px; line-height: 29.7px; font-weight: 400; letter-spacing: -0.2px; color: {INK};}} '
        f'& b{{font-weight: 500; color: {INK};}} @media(--mobile){{& strong{{font-size: 17px; line-height: 24px;}}}}')))
    photo = img('ph-i', 'healus-physician-desk', ('display: block; width: 100%; height: auto; aspect-ratio: 617/639; object-fit: cover; '
                                                  '@media(--tablet){aspect-ratio: 4/3;} @media(--mobile){aspect-ratio: 4/5;}'),
                alt='Physician working at her desk')
    photo += box('ph-o', cap, css=(
        'position: absolute; left: 22px; right: 22px; bottom: 21px; padding: 22px 26px; border-radius: 17.6px; background-color: rgba(255,255,255,0.82); '
        'box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.5); backdrop-filter: blur(26px); -webkit-backdrop-filter: blur(26px); '
        '@media(--mobile){left: 12px; right: 12px; bottom: 12px; padding: 16px 18px;}'))
    left = box('ph', photo, css=(
        'position: relative; width: 42%; padding: 0px; overflow: hidden; border-radius: 26.4px; '
        'box-shadow: 0px 33px 77px -39.7px rgba(2,40,66,0.35), 0px 0px 0px 1px rgba(49,131,113,0.1); @media(--tablet){width: 100%;}'))
    k = pill('s7-pill', 'Connected by design')
    k += h2('s7-h2', "Your EHR shouldn't <br>live on an island", 'margin-block-start: 23px;')
    k += lead('s7-p', 'HealUs exchanges data with labs, pharmacies, hospitals and your billing system, so information arrives in the chart instead of the fax tray.',
              'margin-block-start: 23px;')
    cards = (('HL7', 'Lab orders, results and ADT messages with hospitals and reference labs.'),
             ('FHIR', 'Modern API exchange for patient access and connected health apps.'),
             ('e-Rx network', 'Prescriptions, refills and medication history with pharmacies.'),
             ('APIs', 'Direct connections to the billing, imaging and practice tools you already use.'))
    g = ''.join(p(f'ic{i}', f'<strong>{t}</strong>{d}', cls=['healus-glass'], css=text(14, 23.1, SLATE, extra=(
        'padding: 22px 24px 26px 24px; box-shadow: 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); '
        f'& strong{{display: block; margin-bottom: 5px; font-size: 22px; line-height: 33px; font-weight: 300; letter-spacing: -0.22px; color: {GREEN};}}')))
        for i, (t, d) in enumerate(cards))
    k += grid('ic', g, css=('display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto; gap: 14px; width: 100%; padding: 0px; '
                            'margin-block-start: 38px; @media(--mobile){grid-template-columns: 1fr;}'))
    right = col('s7-r', k, width='42.2%')
    return section('s7', row('s7-row', left + right), 90, 91)


# ================================================================ 8. Why HealUs
def why():
    k = pill('s8-pill', 'Why HealUs')
    k += h2('s8-h2', "Your software shouldn't add <br>more work to your practice", 'text-align: center; margin-block-start: 23px;')
    k += lead('s8-p', 'It should take it away.', 'text-align: center; margin-block-start: 30px; @media(--mobile){margin-block-start: 16px;}')
    cards = (('01', 'rgba(255,226,121,0.45)', 'Built by a billing team', 'Documentation is structured to support the claim, because the people who built it run revenue cycles.'),
             ('02', 'rgba(196,242,205,0.7)', 'Set up for <br>your specialty', 'Templates, order sets and smart phrases configured before your first patient, not after.'),
             ('03', 'rgba(156,216,246,0.45)', 'Guided migration', 'Our team moves demographics, problem lists, medications and recent notes, and trains your staff.'),
             ('04', 'rgba(61,162,140,0.16)', 'One partner, <br>EHR to payment', 'EHR, billing software and billing experts from one company, with one number to call.'))
    g = ''
    for i, (n, bg, t, d) in enumerate(cards):
        c = p(f'wc{i}n', n, cls=['healus-num'], css=f'background-color: {bg}; font-size: 16.6px; line-height: 24.9px;')
        c += h(f'wc{i}h', 'h3', t, text(24.9, 32.4, INK, 400, -0.37, 'margin-block-start: 17px; @media(--mobile){font-size: 21px; line-height: 28px;}'))
        c += p(f'wc{i}p', d, text(16.6, 28.2, SLATE, extra='margin-block-start: 14px; @media(--mobile){font-size: 15px; line-height: 25px;}'))
        g += box(f'wc{i}', c, cls=['healus-glass'], css='display: flex; flex-direction: column; padding: 33px; border-radius: 23.7px; @media(--mobile){padding: 26px;}')
    k += grid('wc', g, css=('display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; grid-template-rows: auto; gap: 24px; width: 100%; padding: 0px; '
                            'margin-block-start: 40px; @media(--tablet){grid-template-columns: 1fr 1fr;} @media(--mobile){grid-template-columns: 1fr; gap: 16px;}'))
    return section('s8', k, 95, 143)


# ================================================================ 9. Demo form + CTA + FAQ
def demo():
    # ---- left copy
    l = pill_lg('d-pill', 'See HealUs in action')
    l += h2('d-h2', 'What would your <br>day look like with <br>less charting?', f'color: {BLACK}; line-height: 1.276; letter-spacing: -1.16px; margin-block-start: 23px;')
    l += lead('d-p', 'Thirty minutes, built around your specialty. Not a slide deck.', 'line-height: 2; margin-block-start: 21px;')
    items = (('Walk through a visit in your specialty', 'From check-in to signed note, with your template.'),
             ('Map your current system', 'What migrates, what connects and what changes for your staff.'),
             ('Get a go-live plan and quote', 'Timeline and pricing based on providers and modules.'))
    li = ''.join(p(f'dc{j}', f'<strong>{a}</strong>{d}', cls=['healus-check-item'], css='line-height: 22.4px;') for j, (a, d) in enumerate(items))
    l += box('d-list', li, css='display: flex; flex-direction: column; width: 100%; max-width: 488px; padding: 17px 0px 0px 0px; margin-block-start: 37px; '
                               'border-top: 1px solid rgba(49,131,113,0.12); @media(--tablet){max-width: 100%;}')
    l += p('d-call', f'Prefer to talk now? Call {PHONE}', text(14, 21, SLATE, extra=(
        f'margin-block-start: 25px; & a{{color: {TEAL}; font-weight: 500; text-decoration: none;}}')))
    left = col('d-l', l, width='44%')

    # ---- form card
    fh = img('df-logo', 'healus-logo', 'display: block; width: 97px; height: auto;', alt='HealUs')
    fh += p('df-step', 'Step 1 of 2', text(14.5, 21.8, MUTED))
    c = flex('df-head', fh, css='display: flex; flex-direction: row; justify-content: space-between; align-items: center; width: 100%; padding: 0px;')
    c += grid('df-prog', box('df-p1', '', css=f'height: 4px; padding: 0px; border-radius: 999px; background-image: linear-gradient(90deg, #3DA28C 0%, #006750 100%);')
              + box('df-p2', '', css='height: 4px; padding: 0px; border-radius: 999px; background-color: rgba(49,131,113,0.12);'),
              css='display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto; gap: 7px; width: 100%; padding: 0px; @media(--mobile){grid-template-columns: 1fr 1fr;}')
    c += h('df-h', 'h3', 'Book your HealUs demo', text(31.5, 34.6, INK, 300, -0.79, 'padding-block-start: 7px; @media(--mobile){font-size: 26px; line-height: 30px;}'))
    label = text(15.7, 23.6, INK, 500, extra=f'display: block; margin-block-end: 7px; & span{{font-weight: 400; color: {MUTED};}}')
    field = (f'{F} display: block; width: 100%; height: 61px; padding: 16px 22px; margin: 0px; border: 0px; border-radius: 9.7px; '
             f'background-color: rgba(255,255,255,0.32); font-size: 18.2px; line-height: 27.2px; color: {INK}; outline: none; '
             'box-shadow: 0px 0px 0px 1.2px rgba(49,131,113,0.16), inset 0px -9.7px 19.4px -14.5px rgba(2,40,66,0.12), inset 0px 1.2px 0px 0px rgba(255,255,255,0.95); '
             f'transition: box-shadow 0.2s ease; &::placeholder{{color: {MUTED};}} '
             '&:focus{box-shadow: 0px 0px 0px 2px rgba(49,131,113,0.45), inset 0px 1.2px 0px 0px rgba(255,255,255,0.95);} '
             '@media(--mobile){height: 54px; font-size: 16px; padding: 13px 18px;}')
    fd = b.el('e-form-label', 'df-l1', cfg={'text': 'Full name', 'input-id': 'healus-name'}, css=label)
    fd += b.el('e-form-input', 'df-i1', cfg={'type': 'text', 'placeholder': 'Dr. Jane Smith', 'required': False, '_cssid': 'healus-name'}, css=field)
    fw = box('df-f1', fd, css='width: 100%; padding: 0px;')
    fd = b.el('e-form-label', 'df-l2', cfg={'text': 'Work email <span>(required)</span>', 'input-id': 'healus-email'}, css=label)
    fd += b.el('e-form-input', 'df-i2', cfg={'type': 'email', 'placeholder': 'you@practice.com', 'required': True, '_cssid': 'healus-email'}, css=field)
    fw += box('df-f2', fd, css='width: 100%; padding: 0px;')
    opts = ['Select', 'Primary care', 'Behavioral health', 'Cardiology', 'Pain management', 'Pediatrics']
    fd = b.el('e-form-label', 'df-l3', cfg={'text': 'Specialty', 'input-id': 'healus-specialty'}, css=label)
    fd += b.el('e-form-select', 'df-s', cfg={'name': 'specialty', 'options': [{'key': o, 'value': o} for o in opts],
                                            'has-default-value': True, 'value': 'Select', '_cssid': 'healus-specialty'}, css=(
        field + ' appearance: none; -webkit-appearance: none; padding-inline-end: 54px; color: ' + INK + '; '
        f"background-image: url('{MEDIA['healus-select-chevron']['url']}'); background-repeat: no-repeat; "
        'background-position: right 22px center; background-size: 14px 14px;'))
    fw += box('df-f3', fd, css='width: 100%; padding: 0px;')
    fw += b.el('e-form-submit-button', 'df-b', cfg={'text': 'Continue →'}, cls=['healus-btn'], css=(
        'justify-content: center; width: 93%; height: 68px; padding: 0px 24px; margin-block-start: 7px; font-size: 18.2px; line-height: 27.2px; '
        'box-shadow: 0px 17px 36px -17px rgba(0,103,80,0.6); &::after{content: none; display: none;} @media(--mobile){width: 100%; height: 58px; font-size: 16px;}'))
    fw += b.el('e-form-success-message', 'df-ok', p('df-okt', 'Thanks! Our team will contact you to schedule your demo.', text(14.5, 21.8, TEAL)),
               css='width: 100%; padding: 0px;')
    fw += b.el('e-form-error-message', 'df-err', p('df-errt', 'Something went wrong. Please check the fields and try again.', text(14.5, 21.8, '#C0392B')),
               css='width: 100%; padding: 0px;')
    c += b.el('e-form', 'df-form', fw, cfg={'form-name': 'HealUs demo request'}, css=(
        'display: flex; flex-direction: column; flex-wrap: nowrap; align-items: flex-start; gap: 17px; width: 100%; padding: 5px 0px 0px 0px;'))
    c += p('df-note', 'HIPAA-secure. Your information is never shared.', text(14.5, 21.8, MUTED, extra='width: 100%; text-align: center;'))
    card = box('df', c, cls=['healus-glass'], css=(
        'display: flex; flex-direction: column; gap: 19.4px; width: 46%; padding: 43.6px; border-radius: 24.2px; background-color: rgba(255,255,255,0.5); '
        'box-shadow: 0px 36.3px 84.8px -36.3px rgba(2,40,66,0.35), 0px 0px 0px 1.2px rgba(49,131,113,0.1), inset 0px 1.2px 0px 0px rgba(255,255,255,0.9), '
        'inset 0px 0px 0px 1.2px rgba(255,255,255,0.5); @media(--tablet){width: 100%;} @media(--mobile){padding: 26px 20px;}'))
    panel = row('d-row', left + card, 'align-items: flex-start;')
    box_ = flex('d-box', panel, css=(
        'display: flex; flex-direction: column; align-items: center; width: 100%; padding: 61px 9.3% 277px 9.3%; border-radius: 20px; '
        'background-color: rgba(255,255,255,0.6); box-shadow: 0px 15px 15px 0px rgba(194,194,194,0.1); overflow: hidden; '
        f"background-image: url('{MEDIA['healus-mark-form']['url']}'); background-repeat: no-repeat; "
        'background-position: right -75px top -127px; background-size: 545px 545px; ' + BLUR +
        ' @media(--tablet){padding: 40px 5% 120px 5%;} @media(--mobile){padding: 28px 5% 80px 5%; background-size: 300px 300px;}'))

    # ---- CTA band (overlaps the bottom of the panel)
    cl = h2('cta-h2', 'Chart less. Care more. <br>Go home on time.', 'color: var(--PureWhite); font-weight: 400; line-height: 1.414; letter-spacing: -1.16px;')
    cl += p('cta-p', 'See HealUs on a visit from your own specialty before you decide.', text(16, 32, WHITE, extra='margin-block-start: 11px; @media(--mobile){font-size: 15px; line-height: 26px;}'))
    cta = box('cta-l', cl, css='display: flex; flex-direction: column; width: 57%; padding: 0px; @media(--tablet){width: 100%;}')
    cta += button('cta-b', 'Book a Demo', DEMO, 'healus-btn-ghost', (
        'color: var(--PureWhite); padding: 0px 8px 0px 29px; gap: 22px; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); '
        '&:hover{color: var(--PureWhite);} &::after{width: 39px; height: 39px;}'))
    band = flex('cta', cta, css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 32px; position: relative; '
        'width: 81.7%; padding: 52px 134px 52px 86px; margin-block-start: -158px; border-radius: 20px; background-color: #006750; '
        f"background-image: url('{MEDIA['healus-mark-cta']['url']}'), radial-gradient(135% 135% at 28% 27%, #3DA28C 0%, #006750 100%); "
        'background-repeat: no-repeat, no-repeat; background-position: right -83px top -176px, center center; background-size: 457px 457px, 100% 100%; '
        'box-shadow: 0px 51px 63.6px 0px rgba(89,89,89,0.2); '
        '@media(--laptop){padding: 48px 64px 48px 64px;} @media(--tablet){flex-direction: column; align-items: flex-start; width: 90%; padding: 40px 32px; margin-block-start: -80px;} '
        '@media(--mobile){width: 100%; padding: 32px 22px; margin-block-start: -50px;}'))

    # ---- FAQ
    fl = pill('faq-pill', 'FAQ', f'color: #7D7D7D;')
    fl += h2('faq-h2', 'Questions <br>practices ask <br>before switching', 'margin-block-start: 24px;')
    fl += lead('faq-call', f'Something else? Call {PHONE}', f'line-height: 2; margin-block-start: 24px; & a{{color: {TEAL}; font-weight: 600; text-decoration: none;}}')
    fleft = col('faq-l', fl, width='31.8%')
    qa = (('How long does it take to switch to HealUs?',
           '[Typical implementation timeline]. Our team handles data migration, template setup and staff training, and schedules go-live around your clinic hours.'),
          ('Can you move data from our current EHR?', '[Answer to confirm before launch.]'),
          ('Is HealUs certified?', '[Answer to confirm before launch.]'),
          ('Does HealUs work with our billing company?', '[Answer to confirm before launch.]'),
          ('How is HealUs priced?', '[Answer to confirm before launch.]'))
    items = ''
    for i, (q, a) in enumerate(qa):
        title = b.el('e-accordion-item-title', f'fq{i}tt', h(f'fq{i}q', 'h3', q, text(19, 28.5, INK, 300, -0.19, '@media(--mobile){font-size: 17px; line-height: 25px;}')),
                     css='padding: 0px; min-width: 0px;')
        icon = b.el('e-accordion-item-icon', f'fq{i}ic', b.el('e-svg', f'fq{i}ii', cfg={'svg': {'id': MEDIA['healus-faq-toggle']['id']}},
                                                              css='width: 34px; height: 34px; display: block;'),
                    css='width: 34px; height: 34px; padding: 0px; flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center;')
        head = b.el('e-accordion-item-header', f'fq{i}h', title + icon, css=(
            'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 24px; padding: 24px 0px; cursor: pointer; '
            '@media(--mobile){padding: 18px 0px; gap: 14px;}'))
        body = b.el('e-accordion-item-content', f'fq{i}c', p(f'fq{i}a', a, text(15, 25.5, SLATE, extra='max-width: 660px; @media(--tablet){max-width: 100%;}')),
                    css='padding: 0px 0px 24px 0px;')
        sep = '' if i == len(qa) - 1 else 'border-bottom: 1px solid rgba(49,131,113,0.12); '
        items += b.el('e-accordion-item', f'fq{i}', head + body, css=f'display: block; padding: 0px; {sep}&[open] svg path:last-child{{opacity: 0;}}')
    acc = b.el('e-accordion', 'faq-acc', items, cfg={'default_state': 'first_expanded', 'max_expanded': 'one', 'show_icon': True, 'faq_schema': True},
               css='display: flex; flex-direction: column; gap: 0px; width: 100%; padding: 0px;')
    fright = box('faq-r', acc, cls=['healus-glass'], css=(
        'width: 62%; padding: 8px 36px; border-radius: 24px; '
        'box-shadow: 0px 24px 60px -32px rgba(2,40,66,0.25), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5); '
        '@media(--tablet){width: 100%;} @media(--mobile){padding: 4px 20px;}'))
    faq = row('faq', fleft + fright, 'align-items: flex-start; width: 81.7%; margin-block-start: 133px; '
                                     '@media(--tablet){width: 100%; margin-block-start: 48px;}')
    return section('s9', box_ + band + faq, 0, 100, anchor='healus-demo', css=(
        'padding-inline-start: 3%; padding-inline-end: 3%;'))


SECTIONS = [hero, problems, features, templates, comparison, insight, integrations, why, demo]


def payload(mode='replace_children', dry=False):
    global b
    b = B()
    xml = ''.join(f() for f in SECTIONS)
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes,
            'mode': mode, 'dry_run': dry}
