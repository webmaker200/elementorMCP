"""Kansas state page (states post 412021) -- two new V4 sections from the Google Doc "Medical Billing Services in Kansas"
(1-W7kEGA7sj_G9zKPYNp-9_25pT2pIOr1y78y3FngESg), designs = the screenshots above each heading in the doc:

  1. "Outsourced Medical Billing Services in Kansas from Eligibility to A/R"  (doc image6) + the doc's
     "Which of these eight steps is costing you the most?" CTA (styled like the page's existing deadlines CTA)
     -> placed after "The Numbers Behind Cleaner Kansas Claims".
  2. "Medical Billing Services Across Kansas Cities and Regions" (doc image10)
     -> placed after "A Medical Billing Company in Kansas That Fits Your Practice".

No new classes: parent-container / specialties-heading / global-text as on the rest of the page; everything else is a
local style. Colours use the kit variables the page already uses (DeepSkyBlue, AzureMist, HealthGreen, DarkGray ...).
Copy is the doc's text word for word; the Blue plan / Systems details in the city cards come from the design.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PID = 412021
SITE = 'https://medcaremso.com'
DEMO = f'{SITE}/request-demo/?utm_source=medical-billing-kansas'
MAP = json.load(open(os.path.join(HERE, '..', 'media.json')))['kansas-cities-map']['id']
ICONS = [383393, 410976, 405743, 408704, 386106, 383394, 392595, 411681]  # calendar, shield, code, arrow, document, clock, chart, user
CIRCLE_ARC = 'https://medcaredemo.online/medcare/wp-content/uploads/2026/04/Cirlce-center-right-arc.svg'

F = 'font-family: var(--Poppins);'
CARD = ('border-radius: 16px; border: 1px solid #0367A11A; background-color: var(--PureWhite); '
        'box-shadow: inset 0px 2px 12px 0px rgba(0,0,0,0.04);')
SOFT = '#F3F8FC'


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


def box(cid, kids, css=''):
    return b.el('e-div-block', cid, kids, css='padding: 0px; min-width: 0px; ' + css)  # base: padding 10px, min-width 30px


def flex(cid, kids, css='', cls=None, cfg=None):
    return b.el('e-flexbox', cid, kids, cfg=cfg, css=('padding: 0px; ' if not cls else '') + css, cls=cls)


def grid(cid, kids, css=''):
    return b.el('e-grid', cid, kids, css='padding: 0px; grid-template-rows: auto; ' + css)  # base adds 2 equal rows


def p(cid, html, css='', cls=None):
    return b.el('e-paragraph', cid, cfg={'paragraph': html}, css=css, cls=cls)


def h(cid, tag, title, css='', cls=None):
    return b.el('e-heading', cid, cfg={'tag': tag, 'title': title}, css=css, cls=cls)


def img(cid, mid, css='', alt=''):
    return b.el('e-image', cid, cfg={'image': {'src': {'id': mid, 'alt': alt}, 'size': 'full'}}, css=css)


def t(size, lh, color, weight=400, extra=''):
    return f'{F} font-size: {size}; line-height: {lh}; font-weight: {weight}; color: {color}; margin: 0px; ' + extra


def a(text, url):
    return f'<a href="{url}">{text}</a>'


def section(cid, kids, bg='var(--PureWhite)'):
    """Same shell as the page's other sections (parent-container, column, 1rem gap)."""
    return flex(cid, kids, cls=['parent-container'], cfg={'tag': 'section'}, css=(
        f'background-color: {bg}; display: flex; flex-direction: column; gap: 1rem; align-items: center; width: 100%;'))


def h2(cid, title):
    return h(cid, 'h2', title, cls=['specialties-heading'], css=(
        'color: var(--PureBlack); line-height: 120%; text-align: center; '
        '@media(--tablet_extra){font-size: 2rem;} @media(--mobile){font-size: 1.6rem;}'))


def intro(cid, html):
    return p(cid, html, cls=['global-text'], css='width: 90%; color: var(--DarkGray); line-height: 24px; text-align: center; @media(--mobile){width: 100%;}')


def body(cid, html, size='14px', css=''):
    return p(cid, html, css=t(size, '22px', 'var(--DarkGray)', 400,
                              '& a{color: var(--HealthGreen); text-decoration: none; font-weight: 500;} & a:hover{text-decoration: underline;} ' + css))


# ---------------------------------------------------------------- 1. outsourced billing, eligibility to A/R
STEPS = [
    ('Eligibility and KanCare MCO Verification',
     'We verify insurance eligibility of the patients in the KanCare plan before the visit. It depends which KanCare plan the patient is holding '
     'in that month, Healthy Blue, Sunflower or UnitedHealthcare. If the claim is sent to the last month’s MCO, it is a claim denial. There are '
     'two Blue Cross companies, Blue Cross and Blue Shield of Kansas (BCBSKS) or Blue Cross and Blue Shield of Kansas City (BCBSKC), we confirm '
     f'this for commercial patients. Patients with no active coverage go to {a("coverage discovery", SITE + "/services/coverage-discovery-services/")}.'),
    ('Prior Authorization for Kansas Payers',
     'We take care of the prior authorization rules in Kansas as every managed care organization and Medicare Advantage plan has its own portal '
     'and turnaround time. We find prior authorization under the plan which the patient has, then we match it to CPT codes that will be '
     'submitted to payers.'),
    ('Medical Billing and Coding for Kansas Practices',
     'Our medical billing and coding Kansas team assigns accurate CPT, ICD-10 and modifiers from the note. Certified coders review every claim '
     f'that is flagged by our {a("AI coding", SITE + "/ai-eco-system/ai-medical-coding/")}, it ensures that the code sent on the claim is '
     'supported by the documentation.'),
    ('Claim Scrubbing and Submission',
     'Claims are scrubbed based on the relevance. They are checked against the rules of the specific payer to ensure accurate submissions on '
     'relevant routes. KanCare fee-for-service through the KMAP portal or EDI, managed care claims to the member’s MCO, Medicare Part B claims '
     'go to the Jurisdiction 5 contractor, and commercial claims through payer portals or our clearinghouse connections.'),
    ('Payment Posting and Underpayment Recovery',
     'We record every payment from the payer into your billing system against the contracted fee schedule, not just the charge. Commercial '
     'claims that pass 30 days with no payment and no status notice from the payer are flagged under Kansas’s prompt pay law. The 1% monthly '
     'interest the law provides is requested with the balance in this case.'),
    ('Denial Management and Appeals',
     'We manage the denials based on the rules of the payer. If it is NCBSKS denial, the fixes are different from the Healthy Blue denial. '
     'KanCare appeals go to the MCO first and then to a state fair hearing if it is needed. See '
     f'{a("denial management", SITE + "/services/denial-management-services/")}.'),
    ('A/R Follow-Up and Recovery',
     'Kansas has its own filing limits and the open claims are worked by an aging bucket. There is a 12-month window for KanCare '
     'fee-for-service and shorter windows for the MCOs and most commercial plans. Claims that have had no attention for 90 days are the first '
     f'ones our {a("A/R recovery", SITE + "/services/ar-recovery-services/")} team pulls.'),
    ('Credentialing and KMAP Enrollment',
     'In Kansas, the order is important. KMAP enrollment is done first through Gainwell. The reason is that no MCO credentials a provider '
     'without the KMAP ID. Then Healthy Blue, Sunflower and UnitedHealthcare. After that, Medicare through PECOS and commercial plans through '
     'CAQH. We help practices in Kansas get credentialed to grow their network. We also track the Kansas Board of Healing Arts license, CAQH '
     'attestation and every revalidation date, so no provider’s enrollment lapses. See '
     f'{a("medical credentialing", SITE + "/services/medical-credentialing-services/")}.'),
]


def band_half(cid, label, title, text, first):
    pill = p(f'{cid}-pl', label, css=t('10px', '1', 'var(--PureWhite)', 600, (
        'display: inline-flex; align-items: center; flex-shrink: 0; width: max-content; height: max-content; padding: 7px 12px; '
        'border-radius: 999px; background-color: var(--HealthGreen); letter-spacing: 0.12em; text-transform: uppercase; margin-top: 3px;')))
    copy = box(f'{cid}-c', h(f'{cid}-t', 'h3', title, css=t('18px', '1.3', 'var(--PureWhite)', 500))
               + p(f'{cid}-p', text, css=t('14px', '22px', 'rgba(255,255,255,0.9)', 400)),
               css='display: flex; flex-direction: column; gap: 6px;')
    return flex(cid, pill + copy, css=(
        'display: flex; flex-direction: row; align-items: flex-start; gap: 16px; padding: 28px 36px; '
        + ('' if first else 'border-left: 1px solid rgba(255,255,255,0.18); ')
        + '@media(--tablet){padding: 24px;} @media(--mobile){flex-direction: column; gap: 12px; padding: 22px 20px; '
        + ('' if first else 'border-left: 0px; border-top: 1px solid rgba(255,255,255,0.18);') + '}'))


def outsourced():
    band = grid('os-band', band_half('os-b1', 'Start here', 'Free billing audit',
                                     'Send us 90 days of data of your claims and payments. We analyze the revenue cycle, find denial rates payer-wise, '
                                     'days in A/R by the bucket and the underpayments we see, before you see anything.', True)
                + band_half('os-b2', 'Then', 'Onboarding in 2–4 weeks',
                            'We set up KMAP, MCO and Medicare EDI and ERA under your tax ID, connect to your EHR, and map your fee schedules.', False)
                + p('os-b-ar', '›', css=t('16px', '1', 'var(--PureWhite)', 600, (
                    'position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); display: flex; align-items: center; justify-content: center; '
                    'width: 24px; height: 24px; border-radius: 999px; background-color: var(--HealthGreen); '
                    'box-shadow: 0px 0px 0px 4px rgba(255,255,255,0.12); @media(--mobile){display: none;}'))), css=(
        'position: relative; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0px; width: 100%; margin-top: 20px; '
        'border-radius: 16px; background-color: var(--DeepSkyBlue); box-shadow: 0px 20px 40px -24px rgba(3,103,161,0.6); '
        '@media(--mobile){grid-template-columns: 1fr;}'))
    cards = ''
    for i, ((title, text), icon) in enumerate(zip(STEPS, ICONS)):
        ic = box(f'os{i}-i', img(f'os{i}-im', icon, css='display: block; width: 20px; height: 20px; object-fit: contain;'), css=(
            'display: flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 10px; '
            'background-color: var(--AzureMist); transition: background-color 0.25s ease;'))
        cards += box(f'os{i}', ic + h(f'os{i}-t', 'h3', title, css=t('16px', '1.35', 'var(--PureBlack)', 500)) + body(f'os{i}-p', text), css=(
            f'display: flex; flex-direction: column; gap: 12px; padding: 22px; {CARD} '
            'transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease; '
            '&:hover{transform: translateY(-4px); border-color: rgba(3,103,161,0.25); '
            'box-shadow: inset 0px 2px 12px 0px rgba(0,0,0,0.04), 0px 16px 32px -18px rgba(3,103,161,0.35);} '
            '&:hover > div:first-child{background-color: #D6EBFA;} @media(--mobile){padding: 20px;}'))
    steps = grid('os-grid', cards, css=(
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; width: 100%; margin-top: 20px; '
        '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile){grid-template-columns: 1fr; gap: 14px;}'))
    # doc CTA after the eight steps; same look as the page's "Are your Kansas claims meeting these deadlines?" box
    cta = box('os-cta', p('os-cta-t', 'Which of these eight steps is costing you the most?', css=(
                  f'{F} font-weight: 300; font-size: 2rem; color: var(--PureWhite); text-align: center; margin: 0px; '
                  '@media(--tablet_extra){font-size: 1.7rem;} @media(--tablet){font-size: 1.74rem;} @media(--mobile){font-size: 1.3rem;}'))
              + p('os-cta-p', 'Send us 90 days of Kansas claims. We check them against KanCare, Medicare and Blue plan rules and show you where revenue is slipping.',
                  cls=['global-text'], css='color: var(--PureWhite); text-align: center; max-width: 760px; margin: 0px;')
              + b.el('e-button', 'os-cta-b', cfg={'text': 'Book a Free Billing Audit', 'link': {'destination': DEMO}}, css=(
                  f'{F} font-weight: 400; font-size: 15px; color: var(--PureWhite); border-radius: 100px; border: 1px solid var(--HealthGreen); '
                  'background-color: var(--HealthGreen); display: flex; justify-content: center; align-self: center; padding: 12px 24px; '
                  'transition: background-color 0.2s ease, border-color 0.2s ease; &:hover{background-color: #6A9A32; border-color: #6A9A32;}')),
              css=(f"width: 100%; padding: 3%; margin-top: 30px; border-radius: 20px; background-image: url('{CIRCLE_ARC}'); background-repeat: no-repeat; "
                   'background-size: auto; background-position: center right; background-color: var(--DeepSkyBlue); display: flex; flex-direction: column; '
                   'gap: 1rem; align-items: center; @media(--mobile_extra){background-image: none;} @media(--mobile){padding: 5%;}'))
    return section('s-ks-outsourced', h2('os-h2', 'Outsourced Medical Billing Services in Kansas from Eligibility to A/R')
                   + intro('os-p', 'Our outsourced medical billing services in Kansas cover the end-to-end revenue cycle, right from the beginning to the end. '
                                   'So, we help you from checking the eligibility to managing the accounts receivable. Each step below names the Kansas rule our team applies to it.')
                   + band + steps + cta)


# ---------------------------------------------------------------- 2. cities and regions
REGIONS = [
    ('Medical Billing Services in Wichita and South-Central Kansas',
     'Wichita, Derby, Hutchinson and Newton are present in the territory of BCBSKS which has the largest claim volume outside the Kansas city '
     'metro. Ascension Via Christi and Wesley Medical Center work on the referral network. So, specialty groups bill hospital-based and services '
     'offered in the office side by side. That means place-of-service accuracy, split billing for hospital-employed and independent providers, '
     'and BCBSKS contracting rules applied to every claim.',
     'BCBSKS', 'Ascension Via Christi, Wesley Medical Center'),
    ('Overland Park, Olathe, and Johnson County Medical Billing',
     'Overland Park, Olathe, Shawnee, Lenexa, Leawood and Gardner are Blue KC territory, not BCBSKS, and many patients work for Missouri employers '
     'with Missouri plans. AdventHealth Shawnee Mission and Olathe Health lead the local systems. Johnson County also has the most marketplace '
     'carriers in the state, all EPO (Exclusive Provider Organization). Billing here is plan identification: the right Blue, the right network, '
     'and Missouri payer IDs on Kansas patients.',
     '<span>Blue KC</span>', 'AdventHealth Shawnee Mission, Olathe Health'),
    ('Kansas City, KS, Wyandotte County, and Leavenworth',
     'Kansas City, Kansas is Blue KC; neighboring Leavenworth County is BCBSKS despite sitting in the same metro. The University of Kansas Health '
     'System’s main campus is in KCK, and Fort Leavenworth brings TRICARE West families to Leavenworth providers. Two Blue plans and a military '
     'payer inside one commute means the eligibility check decides whether the claim pays.',
     '<span>Blue KC</span> / BCBSKS', 'The University of Kansas Health System'),
    ('Topeka and Lawrence Medical Billing in Northeast Kansas',
     'Topeka is the state capital and home to BCBSKS headquarters; Stormont Vail is the largest local system and LMH Health serves Lawrence. State '
     'Employee Health Plan members are concentrated here, so practices see SEHP plan designs more than anywhere else in Kansas. West along I-70, '
     'Manhattan and Junction City add Fort Riley’s TRICARE West families and Kansas State’s student plans, so northeast Kansas practices carry '
     'SEHP, TRICARE and BCBSKS rules at once.',
     'BCBSKS', 'Stormont Vail, LMH Health'),
    ('Western Kansas: Garden City, Dodge City, and Hays',
     'West of Salina, Kansas is critical access hospital and rural health clinic country, anchored by HaysMed in Hays, Salina Regional Health Center '
     'as the north-central referral hub, and regional hospitals in Garden City and Dodge City. Twenty-one western counties have no Medicare '
     'Advantage plan, so Original Medicare and KanCare dominate. Billing here is institutional: UB-04 claims, cost-based CAH payment and RHC '
     'encounters, covered in our rural billing section above.',
     'BCBSKS', 'HaysMed, Salina Regional Health Center'),
]


def cities():
    def legend(cid, label, color):
        return p(cid, label, css=t('12px', '1.4', 'var(--DarkGray)', 400, (
            f'display: flex; align-items: center; gap: 8px; &::before{{content: ""; flex-shrink: 0; width: 12px; height: 12px; border-radius: 3px; background-color: {color};}}')))
    mapcard = box('cr-map', img('cr-map-img', MAP, alt='Kansas cities served by MedCare MSO medical billing services',
                                css='display: block; width: 100%; height: auto;')
                  + flex('cr-leg', legend('cr-leg1', 'BCBSKS territory (103 counties)', 'var(--DeepSkyBlue)')
                         + legend('cr-leg2', 'Blue KC (Johnson, Wyandotte)', 'var(--HealthGreen)'),
                         css='display: flex; flex-direction: row; flex-wrap: wrap; gap: 10px 20px;'), css=(
        f'display: flex; flex-direction: column; gap: 16px; width: 34%; padding: 20px; border-radius: 16px; border: 1px solid #0367A11A; '
        f'background-color: {SOFT}; position: sticky; top: 110px; '
        '@media(--tablet){width: 100%; max-width: 640px; align-self: center; position: static;}'))
    cards = ''
    for i, (title, text, plan, systems) in enumerate(REGIONS):
        num = p(f'cr{i}-n', str(i + 1), css=t('15px', '1', 'var(--PureWhite)', 600, (
            'display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 36px; height: 36px; border-radius: 999px; '
            'background-color: var(--DeepSkyBlue);')))
        copy = box(f'cr{i}-c', h(f'cr{i}-t', 'h3', title, css=t('16px', '1.35', 'var(--PureBlack)', 500)) + body(f'cr{i}-p', text),
                   css='display: flex; flex-direction: column; gap: 8px;')
        lab = 'letter-spacing: 0.1em; text-transform: uppercase;'
        meta = box(f'cr{i}-m', p(f'cr{i}-ml1', 'Blue plan', css=t('10px', '1.3', 'var(--DeepSkyBlue)', 600, lab))
                   + p(f'cr{i}-mv1', plan, css=t('13px', '1.45', 'var(--PureBlack)', 400, '& span{color: var(--HealthGreen); font-weight: 500;} margin-bottom: 10px;'))
                   + p(f'cr{i}-ml2', 'Systems', css=t('10px', '1.3', 'var(--DeepSkyBlue)', 600, lab))
                   + p(f'cr{i}-mv2', systems, css=t('13px', '1.45', 'var(--PureBlack)', 400)), css=(
            'display: flex; flex-direction: column; gap: 3px; padding-left: 16px; border-left: 1px solid #0367A11A; '
            '@media(--mobile){grid-column: 1 / -1; padding-left: 0px; padding-top: 12px; border-left: 0px; border-top: 1px solid #0367A11A;}'))
        cards += grid(f'cr{i}', num + copy + meta, css=(
            f'display: grid; grid-template-columns: auto minmax(0, 1fr) 180px; gap: 18px; align-items: start; padding: 22px; border-radius: 16px; '
            f'border: 1px solid #0367A11A; background-color: {SOFT}; transition: background-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease; '
            '&:hover{background-color: var(--PureWhite); transform: translateY(-3px); box-shadow: 0px 16px 32px -18px rgba(3,103,161,0.35);} '
            '@media(--tablet_extra){grid-template-columns: auto minmax(0, 1fr) 150px;} '
            '@media(--mobile){grid-template-columns: auto minmax(0, 1fr); gap: 14px; padding: 18px;}'))
    right = box('cr-list', cards, css='display: flex; flex-direction: column; gap: 14px; width: 63%; @media(--tablet){width: 100%;}')
    row = flex('cr-row', mapcard + right, css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; width: 100%; margin-top: 20px; '
        '@media(--tablet){flex-direction: column; align-items: stretch; gap: 20px;}'))
    return section('s-ks-cities', h2('cr-h2', 'Medical Billing Services Across Kansas Cities and Regions')
                   + intro('cr-p', 'Our Kansas medical billing services are remote, but the payer map is local. Which Blue plan a patient carries, which MCO '
                                   'dominates a county, and whether the nearest hospital is a CAH all change the claim. Here is what changes by region.')
                   + row)


def payload(dry=False):
    global b
    b = B()
    xml = outsourced() + cities()
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes,
            'mode': 'append', 'parent_id': 'document', 'dry_run': dry}


if __name__ == '__main__':
    d = payload()
    print(len(json.dumps(d)), 'bytes', len(d['style']), 'styled elements')
