"""Behavioral Health Billing Services -- specialty 411549, Elementor V4, content from the Google Doc
"Behavioral Health Billing Services" (1D3qOwNd_N6SYib9q0iMeHc3H0AfywvxKpWzAiZwe4EY).

Specialty posts can't take V3 data from outside the editor (the post type has no custom-fields support), so
the page is built in V4 with elementor-build-composition. Every component copies the measured styling of the
Anesthesia Billing Services specialty (410669), the newest V4 specialty page:
  - sections: site class parent-container (spacing on every device), H2 specialties-heading, H1 heading-main,
    body copy global-text;
  - cards / blue cards / KPI-style cards / white link cards / FAQ / final CTA bar / why-choose checklist as on Anesthesia;
  - codes table styled like the Anesthesia modifier table (grid instead of an HTML widget);
  - hero with a demo form like the Dental specialty hero.
"Behavioral Health Billing Results" (KPIs + case-study card) is left out on purpose (client will advise).
"""
import json
import os

PID = 411549
SLUG = 'behavioral-health-billing-services'
SITE = 'https://medcaremso.com'
DEMO = f'{SITE}/request-demo/?utm_source={SLUG}'
UP = 'https://medcaredemo.online/medcare/wp-content/uploads'

BLUE, BLUE2, GREEN, INK, GREY = '#0367A1', '#0367A5', '#7EB13E', '#000000', '#4F4F4F'
F = 'font-family: var(--Poppins);'

# Media Library IDs (all existing assets)
IMG = {
    'hero_bg': f'{UP}/2024/05/rehab-banner.webp',
    'circle': f'{UP}/2024/07/Cirlce-webinar02.webp',
    'circle_green': f'{UP}/2024/07/Cirlce-webinar-bg.webp',
    'check': f'{UP}/2024/05/check-icon-green.svg',
    'hipaa': 380042, 'therapy': 380045, 'why': 399656, 'chevron': 410675,
    'num': [404840, 404841, 404842, 404843],
}


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


def box(cid, kids, css='', cls=None, cfg=None):
    return b.el('e-div-block', cid, kids, cfg=cfg, css=css, cls=cls)


def flex(cid, kids, css='', cls=None, cfg=None):
    return b.el('e-flexbox', cid, kids, cfg=cfg, css=css, cls=cls)


def grid(cid, kids, css=''):
    return b.el('e-grid', cid, kids, css=css)


def p(cid, html, css='', cls=None):
    return b.el('e-paragraph', cid, cfg={'paragraph': html}, css=css, cls=cls)


def h(cid, tag, title, css='', cls=None):
    return b.el('e-heading', cid, cfg={'tag': tag, 'title': title}, css=css, cls=cls)


def img(cid, mid, css='', alt=''):
    return b.el('e-image', cid, cfg={'image': {'src': {'id': mid, 'alt': alt}, 'size': 'full'}}, css=css)


def txt(size, lh, color, weight=400, extra=''):
    return f'{F} font-size: {size}; line-height: {lh}; font-weight: {weight}; color: {color}; margin: 0px; ' + extra


BTN = {
    'green': f'background-color: {GREEN}; border: 1px solid {GREEN}; color: #FFFFFF; &:hover{{background-color: #6A9A32; border-color: #6A9A32; color: #FFFFFF;}}',
    'black': '&:hover{background-color: #333333; border-color: #333333; color: #FFFFFF;} background-color: #000000; border: 1px solid #000000; color: #FFFFFF;',
    'outline': 'background-color: transparent; border: 1px solid #FFFFFF; color: #FFFFFF; &:hover{background-color: #FFFFFF; color: #0367A1;}',
}


def button(cid, label, url=DEMO, kind='green', css=''):
    return b.el('e-button', cid, cfg={'text': label, 'link': {'destination': url}}, css=(
        f'{F} display: inline-flex; align-items: center; justify-content: center; width: max-content; max-width: 100%; '
        'padding: 12px 24px; border-radius: 100px; font-size: 15px; font-weight: 400; line-height: 1.5; text-align: center; '
        f'text-decoration: none; transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease; {BTN[kind]} ' + css))


def section(cid, kids, css=''):
    return flex(cid, kids, cls=['parent-container'], cfg={'tag': 'section'}, css=(
        'display: flex; flex-direction: column; align-items: center; gap: 16px; width: 100%; position: relative; ' + css))


def h2(cid, title, css=''):
    return h(cid, 'h2', title, cls=['specialties-heading'], css=f'font-weight: 300; color: {INK}; text-align: center; margin: 0px; ' + css)


def intro(cid, html, css=''):
    return p(cid, html, cls=['global-text'], css=f'color: {GREY}; text-align: center; margin: 0px; ' + css)


def circle_bg(color='#FFFFFF', which='circle'):
    return (f"background-color: {color}; background-image: url('{IMG[which]}'); background-repeat: no-repeat; "
            'background-position: right top; background-size: 18% auto; @media(--mobile){background-size: 40% auto;}')


def card_grid(cid, kids, cols=3, css=''):
    tab = 'repeat(2, 1fr)' if cols >= 2 else '1fr'
    return grid(cid, kids, css=(
        f'display: grid; grid-template-columns: repeat({cols}, 1fr); grid-template-rows: auto; gap: 20px; width: 100%; padding: 0px; '
        f'@media(--tablet){{grid-template-columns: {tab};}} @media(--mobile_extra){{grid-template-columns: 1fr;}} ' + css))


def card_a(cid, icon, title, body):
    """Anesthesia 'care settings' card: #E8EFF4, radius 30, icon 44 + blue H3."""
    head = flex(f'{cid}h', img(f'{cid}i', icon, css='width: 44px; height: 44px; flex-shrink: 0; object-fit: contain;')
                + h(f'{cid}t', 'h3', title, css=txt('1.3rem', '1.3', BLUE, 500, '@media(--mobile){font-size: 1.15rem;}')),
                css='display: flex; flex-direction: row; align-items: center; gap: 15px; padding: 0px;')
    return box(cid, head + p(f'{cid}p', body, cls=['global-text'], css=f'color: {GREY}; margin: 0px;'), css=(
        'display: flex; flex-direction: column; gap: 15px; padding: 1.3rem; border-radius: 30px; background-color: #E8EFF4; '
        'transition: box-shadow 0.25s ease, transform 0.25s ease; &:hover{box-shadow: 0px 10px 24px 0px rgba(3,103,161,0.12);}'))


def card_b(cid, icon, title, body, link=None):
    """Anesthesia 'services' card: white, thin blue border, radius 16, icon 42 + black H3 16px."""
    head = flex(f'{cid}h', img(f'{cid}i', icon, css='width: 42px; height: 42px; flex-shrink: 0; object-fit: contain;')
                + h(f'{cid}t', 'h3', title, css=txt('16px', '1.3', INK, 500)),
                css='display: flex; flex-direction: row; align-items: center; gap: 15px; padding: 0px;')
    cfg = {'link': {'destination': link}} if link else None
    return box(cid, head + p(f'{cid}p', body, css=txt('14px', '22px', GREY)), cfg=cfg, css=(
        'display: flex; flex-direction: column; gap: 15px; padding: 1.2rem; border-radius: 16px; background-color: #FFFFFF; '
        'border: 1px solid rgba(3,103,161,0.1); box-shadow: inset 0px 2px 12px 0px rgba(0,0,0,0.04); text-decoration: none; '
        'transition: box-shadow 0.25s ease, border-color 0.25s ease; '
        '&:hover{border-color: rgba(3,103,161,0.3); box-shadow: 0px 10px 24px 0px rgba(3,103,161,0.10);}'))


def card_blue(cid, title, body):
    """Anesthesia 'in-house vs outsourced' blue card."""
    return box(cid, h(f'{cid}t', 'h3', title, css=txt('1.3rem', '1.3', '#FFFFFF', 400, '@media(--mobile){font-size: 1.15rem;}'))
               + p(f'{cid}p', body, css=txt('14px', '22px', '#FFFFFF')), css=(
        f'display: flex; flex-direction: column; gap: 10px; padding: 1.2rem; border-radius: 16px; background-color: {BLUE}; '
        'border: 1px solid rgba(3,103,161,0.1); transition: transform 0.25s ease, box-shadow 0.25s ease; '
        '&:hover{transform: translateY(-3px); box-shadow: 0px 12px 24px 0px rgba(3,103,161,0.25);}'))


# ---------------------------------------------------------------- 1. hero + form
def hero():
    left = h('h1', 'h1', 'Behavioral Health Billing Services for Treatment Programs and Facilities', cls=['heading-main'],
             css='font-weight: 300; color: #FFFFFF; margin: 0px; text-align: left; @media(--tablet){text-align: center;}')
    left += p('h-p', ('MedCare MSO’s behavioral health billing services cover the program-level claims that general billing teams '
                      'often get wrong: IOP and PHP per diems, residential stays, detox and CMHC/CCBHC programs. We track your '
                      'authorizations and concurrent reviews, build each claim for its level of care payer, and keep working denials '
                      'until they’re paid. If your organization runs several services, one team bundles both your facility and '
                      'professional claims.'), cls=['global-text'],
              css='color: #FFFFFF; margin: 0px; @media(--tablet){text-align: center;}')
    left += button('h-b', 'Get a Free Behavioral Health Billing Audit', css='margin-top: 8px; @media(--tablet){align-self: center;}')
    lcol = box('h-l', left, css='display: flex; flex-direction: column; gap: 20px; width: 56%; padding: 0px; @media(--tablet){width: 100%; align-items: center;}')

    label = txt('13px', '1.4', '#555555', 400, 'display: block; margin-bottom: 4px; & span{color: #E0533D;}')
    field = (f'{F} width: 100%; padding: 8px 0px; border: 0px; border-bottom: 1px solid #BDBDBD; border-radius: 0px; background-color: transparent; '
             'font-size: 15px; color: #000000; outline: none; transition: border-color 0.2s ease; '
             f'&:focus{{border-bottom-color: {BLUE};}} &::placeholder{{color: #9E9E9E;}}')
    fields = ''
    for key, lab, typ in (('name', 'Full Name', 'text'), ('email', 'Email', 'email'), ('phone', 'Phone', 'tel')):
        fields += box(f'hf-{key}', b.el('e-form-label', f'hf-l-{key}', cfg={'text': f'{lab} <span>*</span>', 'input-id': f'bh-{key}'}, css=label)
                      + b.el('e-form-input', f'hf-i-{key}', cfg={'type': typ, 'placeholder': '', 'required': True, '_cssid': f'bh-{key}'}, css=field),
                      css='width: 100%; padding: 0px;')
    fields += box('hf-msg', b.el('e-form-label', 'hf-l-msg', cfg={'text': 'Your Message', 'input-id': 'bh-msg'}, css=label)
                  + b.el('e-form-textarea', 'hf-i-msg', cfg={'placeholder': '', 'required': False, '_cssid': 'bh-msg'}, css=field + ' min-height: 70px; resize: vertical;'),
                  css='width: 100%; padding: 0px;')
    fields += b.el('e-form-submit-button', 'hf-b', cfg={'text': 'Send Message'}, css=(
        f'{F} width: 100%; padding: 12px 24px; border: 0px; border-radius: 4px; background-color: {GREEN}; color: #FFFFFF; '
        'font-size: 16px; font-weight: 400; cursor: pointer; transition: background-color 0.2s ease; &:hover{background-color: #6A9A32;}'))
    fields += b.el('e-form-success-message', 'hf-ok', p('hf-okt', 'Thank you! A member of our team will get back to you within 12 hours.', css=txt('15px', '1.5', '#2E5E10')),
                   css='padding: 14px; border-radius: 8px; background-color: #F1F8EC;')
    fields += b.el('e-form-error-message', 'hf-err', p('hf-errt', 'Something went wrong. Please check the fields and try again.', css=txt('14px', '1.5', '#C8412C')), css='padding: 0px;')
    form = b.el('e-form', 'hf', fields, cfg={
        'form-name': 'Behavioral Health billing audit request', 'actions-after-submit': ['email', 'collect-submissions'],
        'email': {'to': ['mkamran@medcaremso.com', 'fashraf@medcaremso.com'], 'subject': 'New Behavioral Health Billing audit request',
                  'message': '[all-fields]', 'from': 'email@medcaremso.com', 'from-name': 'MedCare MSO', 'send-as': 'html'}},
        css='display: flex; flex-direction: column; gap: 18px; width: 100%; padding: 0px;')
    card = box('h-r', h('hf-h', 'h2', 'See Where Your Program Is Losing Revenue', css=txt('1.4rem', '1.3', INK, 600)) + form, css=(
        'display: flex; flex-direction: column; gap: 20px; width: 38%; padding: 24px; border-radius: 10px; background-color: #FFFFFF; '
        'box-shadow: 0px 10px 30px 0px rgba(0,0,0,0.15); @media(--tablet){width: 100%; max-width: 560px;}'))
    row = flex('h-row', lcol + card, css=(
        'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 40px; width: 100%; padding: 0px; '
        '@media(--tablet){flex-direction: column; gap: 32px;}'))
    return flex('s-hero', row, cls=['parent-container'], cfg={'tag': 'section'}, css=(
        'display: flex; flex-direction: column; justify-content: center; width: 100%; min-height: 650px; padding-top: 160px; '
        "background-image: linear-gradient(0deg, rgba(0,0,0,0.5) 19%, rgba(255,255,255,0) 100%), "
        f"linear-gradient(rgba(4,79,148,0.58), rgba(4,79,148,0.58)), url('{IMG['hero_bg']}'); "
        'background-size: auto, auto, cover; background-position: center center; background-repeat: no-repeat; '
        '@media(--tablet){padding-top: 140px; min-height: 0px;} @media(--mobile){padding-top: 120px;}'))


# ---------------------------------------------------------------- 2. why it breaks down (6 cards)
def why():
    items = [
        (389494, 'Authorizations That Expire Mid-Stay',
         'Payers usually approve residential, PHP and IOP stays a few days at a time. Each extension needs a concurrent review with current clinical notes before the last covered day. A step-down to a lower level of care needs its own authorization too. If either one is missed, the days your team already treated can go unpaid.'),
        (389496, 'Hours and Day Thresholds',
         'Medicare certifies PHP patients for at least 20 hours of treatment a week and IOP patients for 9 to 19 hours. Payment is made per day. A PHP day needs at least three qualifying services, while IOP pays a higher rate for days with four or more. Commercial and Medicaid plans set their own minimums. Days without enough documented services, or without start and stop times, may be denied or underpaid.'),
        (389495, 'The Wrong Claim Form or Revenue Code',
         'Program services are billed on the UB-04 with a bill type, revenue codes and, for Medicare, a condition code: 92 for IOP and 41 for PHP. Services from psychiatrists and nurse practitioners go on the CMS-1500. A single mismatch between the revenue code, HCPCS code and condition code can get the entire claim rejected.'),
        (379602, 'Carve-Outs and Out-of-Network Payers',
         'A patient’s insurance card doesn’t always show who pays the behavioral health claim. Many plans hand behavioral benefits to a separate company, so the card names one insurer while the claims belong to another. Out-of-network programs often need a single case agreement before admission. Without one, payment depends on out-of-network benefits or falls to the patient.'),
        (389497, 'Limits That Break Parity Rules',
         'Some plans cap visits, require stricter prior authorization or ask for more frequent reviews for behavioral care than for comparable medical care. The Mental Health Parity and Addiction Equity Act restricts limits like these. We flag them, raise parity in appeals and, with the patient’s authorization, request the plan’s comparative analysis.'),
        (389493, 'Consent Before SUD Records Leave the Building',
         'Substance use disorder programs covered by 42 CFR Part 2 need written patient consent before records go to a payer. Its latest 2024 update permits a single consent for treatment, payment and health care operations. And compliance has been required since February 16, 2026. Every claim, appeal and records request needs to stay within the consent on file.'),
    ]
    cards = ''.join(card_a(f'w{i}', ic, t, d) for i, (ic, t, d) in enumerate(items))
    return section('s-why', h2('w-h2', 'Why Behavioral Health Billing Breaks Down at the Program Level')
                   + intro('w-p', 'Behavioral health billing at the program level brings together three things outpatient billing rarely handles at once: per diem claims, authorizations that renew every few days and federal privacy rules for substance use records. When one review is missed or one code doesn’t match, a full week of treatment can go unpaid. Here are six places where program revenue commonly slips through.')
                   + card_grid('w-g', cards, 3, 'margin-top: 14px;'), css='gap: 16px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 3. CTA box
def cta_auth():
    inner = p('c1-t', 'Is An Authorization Lapse Holding Up Your Claims?', css=txt('2rem', '1.3', BLUE, 300, 'text-align: center; @media(--mobile){font-size: 1.5rem;}'))
    inner += p('c1-p', 'Get a free review of your open authorizations and denied days!', cls=['global-text'], css=f'color: {GREY}; text-align: center; margin: 0px;')
    inner += button('c1-b', 'Get a Free Review', css='margin-top: 6px;')
    panel = box('c1-box', inner, css=(
        'display: flex; flex-direction: column; align-items: center; gap: 14px; width: 100%; padding: 2.4rem; border-radius: 20px; '
        f"background-color: #F4F4F4; background-image: url('{IMG['circle']}'); background-repeat: no-repeat; background-position: right top; "
        'background-size: 14% auto; @media(--mobile){padding: 1.6rem 1.2rem; background-size: 30% auto;}'))
    return section('s-cta1', panel, css='background-color: #FFFFFF;')


# ---------------------------------------------------------------- 4. levels of care (8 white cards)
def levels():
    items = [
        (385140, 'Intensive Outpatient Programs',
         'IOPs operate in hospital outpatient departments, community mental health centers and freestanding programs. Since January 1, 2024, Medicare has also covered IOP in FQHCs, RHCs and opioid treatment programs. Medicare IOP billing uses the UB-04 (bill type 13X or 76X) with condition code 92, and each service goes on its own lines with a revenue code and a CPT or HCPCS code. Commercial plans generally pay a per diem, and IOP billing codes depend on the contract: S9480 under revenue code 0905 for psychiatric IOP or H0015 under 0906 for SUD IOP. Authorizations are usually approved a few days at a time.'),
        (385138, 'Partial Hospitalization Programs',
         'Hospitals and CMHCs run PHPs for patients who need at least 20 hours of treatment a week. Medicare partial hospitalization billing uses the UB-04 with condition code 41 and the same line-by-line revenue codes as IOP. Medicare pays one per diem for each day with three or more services. A physician must certify that the patient needs this level of care and recertify it periodically. Commercial and Medicaid plans often pay a per diem billed with S0201 or H0035 under revenue code 0912 or 0913, with frequent reviews.'),
        (4556, 'Residential Treatment',
         'Licensed residential programs provide round-the-clock mental health and substance use treatment outside a hospital. Residential treatment billing uses the UB-04 with revenue code 1001 (psychiatric) or 1002 (chemical dependency), usually as a per diem. Medicaid plans often require H0018 (short-term) or H0019 (long-term), which exclude room and board. Medicare doesn’t cover non-hospital residential treatment. For adults in facilities with more than 16 beds, Medicaid’s IMD exclusion limits payment unless the state has a Section 1115 waiver. Reviews typically come every few days.'),
        (4632, 'Detox and Withdrawal Management',
         f'Withdrawal management ranges from ambulatory detox to medically managed inpatient care, depending on the patient’s ASAM level. Non-hospital residential detox is billed per diem with H0010 (sub-acute) or H0011 (acute), on the UB-04 or CMS-1500, depending on the payer. Hospital-based detox is billed as an inpatient stay with detox room-and-board revenue codes such as 0116 or 0126. Since approvals are short and reviewed often, our <a href="{SITE}/specialties/substance-abuse-rehabilitation/">rehab billing services</a> confirm benefits and authorization at admission.'),
        (5021, 'Community Mental Health Centers and CCBHCs',
         'CMHCs bill Medicare for PHP and IOP on bill type 76X, following the same condition code and line-item rules as hospitals. CCBHCs are paid by state Medicaid programs through a prospective payment system: a daily rate (PPS-1), a monthly rate (PPS-2) or either one with separate crisis service rates (PPS-3 and PPS-4). In community behavioral health billing, the qualifying visit is what triggers the payment, so CCBHC billing depends on capturing every qualifying visit.'),
        (391925, 'Outpatient Therapy, Psychiatry and Psychological Testing',
         f'Many programs also offer outpatient services, which are billed on the CMS-1500. Psychotherapy uses time-based codes (90832, 90834, 90837). Psychiatrists and nurse practitioners pair E/M visits with psychotherapy add-ons (90833, 90836, 90838), while psychological testing uses 96130-96139. If your practice offers only outpatient care, see our <a href="{SITE}/specialties/mental-health-billing-service/">mental health billing services</a>, <a href="{SITE}/specialties/psychiatric-billing-services/">psychiatric billing services</a> and <a href="{SITE}/specialties/psychology-billing-services/">psychology billing services</a>.'),
        (379603, 'ABA Therapy',
         'Applied behavior analysis is billed on the CMS-1500 in 15-minute units under 97151-97158, and payers authorize a set number of units per week or month. Each code has its own rules on who can deliver it, and payers set supervision requirements for RBTs working under a BCBA. Our ABA billing services track units against each authorization, so your team doesn’t deliver sessions beyond what was approved.'),
        (379600, 'Collaborative Care and Behavioral Health Integration',
         f'When medical groups add behavioral health, they bill the psychiatric Collaborative Care Model monthly with 99492, 99493 and 99494, and general behavioral health integration with 99484. These time-based codes are billed by the treating practitioner with patient consent on file and minutes tracked across the month. FQHCs and RHCs follow different rules. For those, see our <a href="{SITE}/specialties/fqhc-billing-services/">FQHC billing services</a>.'),
    ]
    cards = ''.join(card_b(f'l{i}', ic, t, d) for i, (ic, t, d) in enumerate(items))
    return section('s-levels', h2('l-h2', 'Behavioral Health Billing Services by Level of Care')
                   + intro('l-p', 'Each level of care comes with its own claim forms, revenue codes, authorization cycle and denial pattern, and the rules shift again from one payer to the next. Here’s how our behavioral health billing services handle each one.')
                   + card_grid('l-g', cards, 2, 'margin-top: 20px; @media(--tablet){grid-template-columns: 1fr;}'),
                   css=f'gap: 16px; {circle_bg("#EAF5FF")}')


# ---------------------------------------------------------------- 5. end-to-end RCM (10 cards)
def rcm():
    items = [
        (411151, 'VOB and Out-of-Network Checks', 'Before your program admits a patient, we check active coverage, benefits for the planned level of care, deductibles and out-of-pocket maximums. Our team also identifies who manages the behavioral benefit. For out-of-network care, we review available benefits and whether a single case agreement is needed.'),
        (411137, 'Prior Authorization, Concurrent Review and Recertification', 'Your patient’s treatment may continue beyond the initial approval. We request authorizations, track covered dates and coordinate concurrent reviews and required recertifications with your team. If the patient moves from residential care to PHP or IOP, we follow the payer’s requirements for the new authorization.'),
        (379602, 'Credentialing, Payer Enrollment and Single Case Agreements', 'Your facility and clinicians need the appropriate enrollment and network arrangements for the plans you bill. We support credentialing, Medicare, Medicaid and commercial enrollment, and CAQH updates. Where no contract exists, our team requests a single case agreement and follows up on proposed payment terms.'),
        (411139, 'Coding and Charge Capture by Level of Care', 'Your claims should reflect the services documented. Our coders review per diem billing, revenue codes and applicable CPT and HCPCS codes against the payer’s requirements. We check service counts, required start and stop times, and treatment plans, requesting clarification when supporting information is missing.'),
        (411140, 'UB-04 and CMS-1500 Claim Submission', 'We prepare facility claims on the UB-04 (837I) and professional claims on the CMS-1500 (837P), following the applicable billing requirements. Our team reviews bill types, condition codes and payer edits before submission. These checks help identify errors while your practice can still address them.'),
        (411141, 'Denial Management and Parity Appeals', 'When a claim is denied, your team needs to know why and what to do next. We review the denial, correct submission errors and prepare appropriate appeals with supporting documentation. If coverage restrictions raise potential mental health parity concerns, we address those issues in the appeal.'),
        (411144, 'A/R Follow-Up, Including Out-of-Network Claims', 'Our A/R team works every open claim by age and payer, including out-of-network and single case agreement claims, which usually need more follow-up. We escalate aging accounts before they reach the payer’s timely filing limit.'),
        (411143, 'Payment Posting and Underpayment Review', 'We post payments from ERAs and EOBs, then compare each one with your contracted or agreed rate. Underpaid per diems and short-paid single case agreements are flagged and appealed rather than written off.'),
        (411138, 'Patient Financial Counseling and Statements', 'At admission, we explain each patient’s expected costs, provide Good Faith Estimates to self-pay patients and send clear statements afterward. Setting up payment plans early helps keep patient balances from turning into bad debt.'),
        (406179, 'Reporting by Program, Payer and Level of Care', 'Your reports break revenue, denials and A/R down by program, payer and level of care, so you can see which service line or contract is losing money. Live dashboards in Maximus PMS show claim status and payment timelines as they change.'),
    ]
    cards = ''.join(card_a(f'r{i}', ic, t, d) for i, (ic, t, d) in enumerate(items))
    return section('s-rcm', h2('r-h2', 'End-to-End Behavioral Health Revenue Cycle Management')
                   + intro('r-p', 'Your program’s billing needs begin before admission and continue through payment reconciliation. MedCare MSO’s behavioral health revenue cycle management brings these responsibilities together, with one team following authorizations, claims and collections. Need help with only part of the cycle? We also offer revenue cycle management for behavioral health in modules, such as credentialing or A/R recovery on its own.')
                   + card_grid('r-g', cards, 2, 'margin-top: 14px; @media(--tablet){grid-template-columns: 1fr;}'), css='gap: 16px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 6. codes table (grid, Anesthesia table styling)
def codes():
    head = ['Level of care', 'Claim form', 'Revenue code family', 'Common HCPCS/CPT', 'Key rule']
    rows = [
        ('IOP (Medicare)', 'UB-04, bill type 13X or 76X', '0900, 0914–0916, 0918, 0942, listed per service', 'CPT/HCPCS per service, e.g. 90791, G0410', 'Condition code 92; per diem paid by services per day; recertify at least every 60 days'),
        ('IOP (commercial, Medicaid)', 'UB-04 or CMS-1500, per contract', '0905 (psychiatric), 0906 (SUD)', 'S9480, H0015', 'Per diem; authorized a few days at a time'),
        ('PHP (Medicare)', 'UB-04, bill type 13X or 76X', '0900, 0904, 0914–0916, 0918, 0942, listed per service', 'CPT/HCPCS per service', 'Condition code 41; 3+ services per day; 20+ hours a week certified'),
        ('PHP (commercial, Medicaid)', 'UB-04', '0912, 0913', 'S0201, H0035', 'Per diem; frequent concurrent reviews'),
        ('Residential', 'UB-04', '1001 (psychiatric), 1002 (chemical dependency)', 'H0018, H0019', 'Not covered by Medicare; Medicaid IMD exclusion applies'),
        ('Detox', 'UB-04 or CMS-1500; inpatient UB-04 for hospital detox', '0116, 0126 (hospital detox)', 'H0010, H0011', 'Match the ASAM level; authorize at admission'),
        ('CCBHC', 'Per state Medicaid rules', 'Set by the state', 'Qualifying encounter codes set by the state', 'Qualifying visit triggers the daily or monthly PPS payment'),
        ('Outpatient professional', 'CMS-1500', 'None', '90791, 90792, 90832–90838, 96130–96139', 'Time-based codes; add-ons pair with an E/M visit'),
        ('ABA', 'CMS-1500', 'None', '97151–97158', '15-minute units against the authorized total'),
        ('Collaborative care / BHI', 'CMS-1500', 'None', '99492–99494, 99484', 'Monthly minute thresholds; patient consent on file'),
    ]
    cells = ''.join(p(f'tb-hd{j}', t, css=txt('16px', '24px', '#FFFFFF', 600, f'padding: 13px; background-color: {BLUE};')) for j, t in enumerate(head))
    for i, r in enumerate(rows):
        bg = 'rgba(128,128,128,0.07)' if i % 2 == 0 else '#FFFFFF'
        for j, t in enumerate(r):
            color, weight = (BLUE2, 500) if j == 0 else ('#333333', 400)
            cells += p(f'tb-{i}-{j}', t, css=txt('15px', '22.5px', color, weight, f'padding: 16px 13px; background-color: {bg}; height: 100%;'))
    table = grid('tb-g', cells, css=(
        'display: grid; grid-template-columns: 1.05fr 1.1fr 1.2fr 1.2fr 1.6fr; grid-template-rows: auto; gap: 0px; width: 100%; '
        'min-width: 980px; padding: 0px; @media(--mobile){grid-template-columns: 1.05fr 1.1fr 1.2fr 1.2fr 1.6fr;}'))
    wrap = box('tb-w', table, css=(
        f'width: 100%; padding: 0px; margin-top: 14px; border: 1px solid {BLUE2}; border-radius: 10px; overflow-x: auto; overflow-y: hidden;'))
    return section('s-codes', h2('tb-h2', 'Behavioral Health Billing Codes by Level of Care')
                   + intro('tb-p', 'Use this table as a quick reference for the behavioral health billing codes and claim formats each program type uses. The same service can need a different form, revenue code and HCPCS code depending on who pays. That’s why Medicare rules are listed separately wherever they differ from commercial and Medicaid plans.')
                   + wrap + p('tb-n', 'Codes vary by payer and state Medicaid Program; we verify against each contract.', css=txt('14px', '22px', GREY, 400, 'width: 100%; font-style: italic;')),
                   css='gap: 16px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 7. compliance (Anesthesia compliance layout)
def compliance():
    items = [
        ('42 CFR Part 2 and SUD Record Confidentiality', '42 CFR Part 2 protects records from federally assisted substance use disorder programs more strictly than HIPAA alone. The 2024 final rule brought Part 2 closer to HIPAA by allowing one patient consent to cover treatment, payment and health care operations. Compliance has been required since February 16, 2026, and violations now carry HIPAA-level penalties. We release records only within the consent on file.'),
        ('Mental Health Parity', 'When a payer limits behavioral health coverage, your team needs to understand whether those restrictions meet parity requirements. MHPAEA generally prevents applicable plans from imposing more restrictive financial requirements or treatment limitations than permitted for comparable medical care. Federal agencies have paused enforcement of provisions newly introduced by the 2024 rule, but existing statutory obligations remain. We review potential concerns and identify issues that may support an appeal.'),
        ('Medicare IOP and PHP Requirements', 'Your records need to support the physician’s certification and the patient’s treatment needs. Medicare requires at least 20 hours weekly for PHP and at least nine for IOP. Applicable facility claims use condition code 41 for PHP or 92 for IOP, with services reported by date. We check required time records and certification schedules, including IOP recertification at least every 60 days, before submission.'),
        ('Telehealth for Behavioral Health', 'Medicare permanently covers behavioral health telehealth in the patient’s home. Its in-person visit requirement for tele-mental health has been delayed to January 1, 2028, and audio-only coverage runs through December 31, 2027. Each claim needs the right place of service (02 or 10) and modifier (95 for video, 93 for audio-only). Commercial and Medicaid rules vary by plan.'),
        ('No Surprises Act for Self-Pay Clients', 'Your uninsured and self-pay patients generally need a written Good Faith Estimate when care is requested or scheduled within applicable timelines. A bill at least $400 above that provider’s estimate may qualify for dispute. We help prepare estimates around the planned services and expected length of stay.'),
        ('HIPAA and Data Security', 'MedCare MSO works as a HIPAA-compliant business associate. We sign a business associate agreement, limit access to patient records by role and use only the minimum information needed to bill each claim.'),
    ]
    right = h2('cp-h2', 'Behavioral Health Billing Compliance', 'text-align: left; @media(--tablet){text-align: center;}')
    right += p('cp-p', 'Behavioral health programs answer to more rules than most practices do. These include federal privacy law for addiction records, parity law, Medicare’s IOP and PHP conditions and CMS behavioral health billing guidelines for telehealth. We build each one into the billing workflow, so your claims are prepared to hold up in an audit.', cls=['global-text'], css=f'color: {GREY}; margin: 0px; @media(--tablet){{text-align: center;}}')
    lst = ''
    for i, (t, d) in enumerate(items):
        lst += box(f'cp{i}', h(f'cp{i}t', 'h3', t, css=txt('1.15rem', '1.35', BLUE, 500)) + p(f'cp{i}p', d, cls=['global-text'], css=f'color: {GREY}; margin: 0px;'),
                   css='display: flex; flex-direction: column; gap: 8px; padding: 0px 0px 0px 16px; border-left: 3px solid #7EB13E;')
    right += box('cp-list', lst, css='display: flex; flex-direction: column; gap: 22px; width: 100%; padding: 0px; margin-top: 8px;')
    left = box('cp-l', img('cp-img', IMG['hipaa'], alt='HIPAA compliant behavioral health billing', css='width: 100%; height: auto;'),
               css='width: 42%; padding: 0px; position: sticky; top: 120px; align-self: flex-start; @media(--tablet){width: 70%; position: static; align-self: center;} @media(--mobile){width: 100%;}')
    row = flex('cp-row', left + box('cp-r', right, css='display: flex; flex-direction: column; gap: 16px; width: 54%; padding: 0px; @media(--tablet){width: 100%;}'),
               css='display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 48px; width: 100%; padding: 0px; @media(--tablet){flex-direction: column; gap: 30px;}')
    return section('s-comp', row, css=circle_bg('#D6EAD9', 'circle_green'))


# ---------------------------------------------------------------- 8. payers (blue cards)
def payers():
    items = [
        ('Medicare', 'Hospital and CMHC IOP and PHP, plus professional services from psychiatrists, psychologists, LCSWs, marriage and family therapists and mental health counselors.'),
        ('Medicaid and Managed Care Plans', 'State-specific H-codes, modifiers and authorization rules, including CCBHC PPS billing.'),
        ('Commercial Plans', 'Per diem contracts for IOP, PHP, residential and detox.'),
        ('Behavioral Health Carve-out Companies', 'Optum Behavioral Health, Carelon Behavioral Health, Magellan Health and Evernorth Behavioral Health.'),
        ('TRICARE and VA Community Care', 'Claims following the program’s referral, authorization and submission requirements.'),
        ('Employee Assistance Programs (EAPs)', 'Approved sessions billed using the EAP’s authorization details.'),
        ('Single Case Agreements', 'Out-of-network care billed according to negotiated payment terms.'),
    ]
    cards = ''.join(card_blue(f'py{i}', t, d) for i, (t, d) in enumerate(items))
    return section('s-payers', h2('py-h2', 'Payers and Programs We Bill')
                   + intro('py-p', 'Behavioral health insurance billing involves more payer types than a typical medical practice deals with, and often two companies for the same patient. Our team bills:')
                   + grid('py-g', cards, css=('display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: auto; gap: 20px; width: 100%; padding: 0px; margin-top: 14px; '
                                             '@media(--tablet_extra){grid-template-columns: repeat(3, 1fr);} @media(--tablet){grid-template-columns: repeat(2, 1fr);} @media(--mobile_extra){grid-template-columns: 1fr;}'))
                   + intro('py-n', 'Coverage can differ sharply by level of care. For example, Medicare doesn’t pay for non-hospital residential treatment, so residential programs rely on commercial plans, self-pay and Medicaid where state waivers allow it.', 'margin-top: 14px;'),
                   css='gap: 16px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 9. who we serve (KPI-style cards)
def serve():
    items = [(385140, 'Intensive outpatient programs for mental health and substance use'), (385138, 'Partial hospitalization programs'),
             (4556, 'Residential treatment centers'), (4632, 'Detox and withdrawal management programs'),
             (5021, 'Community mental health centers and CCBHCs'), (379603, 'Multi-service behavioral health organizations'),
             (391925, 'Hospital outpatient behavioral health departments'), (389493, 'Medical groups adding collaborative care')]
    cards = ''
    for i, (ic, t) in enumerate(items):
        cards += box(f'sv{i}', img(f'sv{i}i', ic, css='width: 55px; height: 55px; object-fit: contain;')
                     + b.el('e-divider', f'sv{i}d', css='width: 100%; height: 1px; background-color: #D9D9D9; border: 0px;')
                     + p(f'sv{i}p', t, css=txt('16px', '24px', INK)), css=(
            'display: flex; flex-direction: column; gap: 18px; padding: 1.9rem 1rem; border-radius: 10px; background-color: #F8F8F8; '
            'box-shadow: 0px 0px 10px 1px rgba(0,0,0,0.01); transition: box-shadow 0.25s ease; &:hover{box-shadow: 0px 10px 24px 0px rgba(3,103,161,0.12);}'))
    g = grid('sv-g', cards, css=('display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: auto; gap: 20px; width: 100%; padding: 0px; margin-top: 14px; '
                                 '@media(--tablet){grid-template-columns: repeat(2, 1fr);} @media(--mobile){grid-template-columns: 1fr;}'))
    return section('s-serve', h2('sv-h2', 'Who We Serve')
                   + intro('sv-p', 'Our behavioral &amp; mental health billing services support organizations that deliver care at more than one level:')
                   + g + intro('sv-n', f'Running a solo or group outpatient practice? Explore our <a href="{SITE}/specialties/mental-health-billing-service/">mental health billing services</a>.', 'margin-top: 14px;'),
                   css='gap: 16px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 10. AI ecosystem (white link cards)
def ai():
    items = [
        (408038, 'AI Authorization Verification', 'Authorization status checks, with alerts for approvals nearing their end date before the next service is delivered.', None),
        (405743, 'Sophus AI Coder', 'CPT, ICD-10 and HCPCS code suggestions, with the correct modifiers, based on clinical documentation.', f'{SITE}/ai-eco-system/ai-medical-coding/'),
        (408083, 'AI Rule Engine', 'Pre-submission checks against payer rules, including revenue code, condition code and bill type combinations.', f'{SITE}/ai-rule-engine/'),
        (405740, 'HealUs EHR', 'Clinical charting with integrated billing for programs that want documentation and claims in one system.', f'{SITE}/ai-eco-system/ehr/'),
        (405741, 'Maximus PMS', 'Charge entry, claim submission and real-time claim status, integrated with your existing EHR.', f'{SITE}/product/medical-billing-software/'),
    ]
    cards = ''.join(card_b(f'ai{i}', ic, t, d, link) for i, (ic, t, d, link) in enumerate(items))
    g = grid('ai-g', cards, css=('display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: auto; gap: 20px; width: 100%; padding: 0px; margin-top: 14px; '
                                 '& > *:last-child{grid-column: 1 / -1;} @media(--mobile_extra){grid-template-columns: 1fr;}'))
    return section('s-ai', h2('ai-h2', 'Behavioral Health Billing Solutions Powered by MedCare’s AI Ecosystem')
                   + intro('ai-p', 'Our behavioral health billing solutions pair certified billers with MedCare MSO’s AI tools. Routine checks run automatically, which leaves our team more time for reviews, appeals and payer follow-up.')
                   + g + button('ai-b', 'Explore the AI ecosystem', f'{SITE}/ai-eco-system/', 'black', 'margin-top: 20px;'),
                   css=f'gap: 16px; {circle_bg("#F8F8F8")}')


# ---------------------------------------------------------------- 11. EHR systems
def ehr():
    logos = [(396576, 'Credible'), (396574, 'CareLogic'), (396585, 'Valant'), (396584, 'TherapyNotes'), (396581, 'SimplePractice'), (396578, 'ICANotes'),
             (396579, 'Netsmart'), (396582, 'Streamline Healthcare'), (396577, 'Epic'), (396575, 'Oracle Cerner'), (396580, 'NextGen'), (396583, 'Tebra')]
    tiles = ''.join(box(f'eh{i}', img(f'eh{i}i', mid, alt=f'{n} EHR', css='width: 100%; height: 56px; object-fit: contain;'), css=(
        'display: flex; align-items: center; justify-content: center; padding: 14px; border-radius: 10px; background-color: #FFFFFF; '
        'border: 1px solid rgba(3,103,161,0.1); transition: box-shadow 0.25s ease; &:hover{box-shadow: 0px 8px 20px 0px rgba(3,103,161,0.10);}'))
        for i, (mid, n) in enumerate(logos))
    g = grid('eh-g', tiles, css=('display: grid; grid-template-columns: repeat(6, 1fr); grid-template-rows: auto; gap: 16px; width: 100%; padding: 0px; margin-top: 14px; '
                                 '@media(--tablet){grid-template-columns: repeat(4, 1fr);} @media(--mobile){grid-template-columns: repeat(2, 1fr);}'))
    return section('s-ehr', h2('eh-h2', 'EHR Systems We Work With')
                   + intro('eh-p', 'Your clinicians should be able to continue documenting in the system they know. We work within your program’s existing EHR, using those records to support the billing process.') + g,
                   css='gap: 16px; background-color: #EAF5FF;')


# ---------------------------------------------------------------- 12. why choose (Anesthesia layout)
def choose():
    items = [
        ('A utilization review team', 'Reviewers who prepare concurrent reviews and recertifications with your clinical staff, so authorizations are renewed before the last covered day'),
        ('Facility and professional billing together', 'UB-04 program claims and CMS-1500 claims for your psychiatrists and therapists handled by one team, so services are neither billed twice nor missed'),
        ('Parity-informed appeals', 'Parity raised in the appeal whenever a payer applies a stricter limit to behavioral care than to comparable medical care'),
        ('42 CFR Part 2 workflows', 'SUD records released only within the consent on file, with access limited to the staff who bill those claims'),
        ('A named account manager', 'One contact who knows your programs, payers and contracts'),
        ('Live dashboards', 'Claim status, denials and A/R by program and level of care in Maximus PMS'),
        ('Simple pricing', 'A percentage of what we collect, with no setup fees'),
    ]
    left = h2('ch-h2', 'Why Choose MedCare MSO as Your Behavioral Health Billing Company', 'text-align: left;')
    left += p('ch-p', 'A behavioral health billing company that serves treatment programs needs to understand clinical reviews as well as claims. Here’s what your program gets with MedCare MSO:', cls=['global-text'], css=f'color: {GREY}; margin: 0px;')
    lst = ''.join(p(f'ch{i}', f'<strong>{t}:</strong> {d}', cls=['global-text'], css=(
        f"color: {GREY}; margin: 0px; padding-left: 26px; background-image: url('{IMG['check']}'); background-repeat: no-repeat; "
        'background-position: left 4px; background-size: 16px auto; & strong{color: #000000; font-weight: 500;}')) for i, (t, d) in enumerate(items))
    left += box('ch-list', lst, css='display: flex; flex-direction: column; gap: 12px; width: 100%; padding: 0px;')
    left += button('ch-b', 'Get a Free Behavioral Health Billing Audit', kind='black', css='margin-top: 8px;')
    lcol = box('ch-l', left, css='display: flex; flex-direction: column; gap: 16px; width: 50%; padding: 0px 0px 2.4rem 0px; @media(--tablet){width: 100%;}')
    rcol = box('ch-r', img('ch-img', IMG['why'], alt='Behavioral health billing specialist at MedCare MSO', css='width: 100%; height: auto;'),
               css='display: flex; align-items: flex-end; justify-content: flex-end; width: 46%; padding: 0px; @media(--tablet){width: 70%; align-self: center;} @media(--mobile){width: 100%;}')
    row = flex('ch-row', lcol + rcol, css=('display: flex; flex-direction: row; justify-content: space-between; align-items: flex-end; gap: 32px; width: 100%; padding: 0px; '
                                           '@media(--tablet){flex-direction: column; align-items: stretch;}'))
    return section('s-choose', row, css='background-color: #EAF5FF; padding-bottom: 0px;')


# ---------------------------------------------------------------- 13. how we take over (4 steps)
def steps():
    items = [
        ('Step 1: Free Audit', 'MedCare MSO’s billing experts review your practice’s denials, A/R aging, open authorizations and payer contracts. After an audit, we show you where revenue is being lost.'),
        ('Step 2: Workflow and Payer Mapping', 'Our team documents each level of care, payer, contract rate and authorization rule, and sets up access to your EHR.'),
        ('Step 3: Parallel Run', 'We work alongside your current billing process, so no claim or review falls through.'),
        ('Step 4: Go-Live', 'Our specialists take over claim submission, reviews and A/R follow-up, and you receive your first reports by program and payer.'),
    ]
    bgs = ['#EBF6FF', '#F2FCF3', '#FDF9F0', '#EBF6FF']
    cards = ''
    for i, (t, d) in enumerate(items):
        cards += box(f'st{i}', img(f'st{i}i', IMG['num'][i], css='width: 52px; height: 52px;')
                     + h(f'st{i}t', 'h3', t, css=txt('1.3rem', '1.35', BLUE, 500, '@media(--mobile){font-size: 1.15rem;}'))
                     + p(f'st{i}p', d, cls=['global-text'], css=f'color: {GREY}; margin: 0px;'), css=(
            f'display: flex; flex-direction: column; gap: 16px; padding: 2rem; border-radius: 30px; background-color: {bgs[i]}; '
            'transition: transform 0.25s ease, box-shadow 0.25s ease; &:hover{transform: translateY(-3px); box-shadow: 0px 10px 24px 0px rgba(3,103,161,0.10);} '
            '@media(--tablet_extra){padding: 1.5rem;}'))
    g = grid('st-g', cards, css=('display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: auto; gap: 20px; width: 100%; padding: 0px; margin-top: 14px; '
                                 '@media(--tablet){grid-template-columns: repeat(2, 1fr);} @media(--mobile_extra){grid-template-columns: 1fr;}'))
    return section('s-steps', h2('st-h2', 'How We Take Over Your Behavioral Health Billing')
                   + intro('st-p', 'Switching billing companies shouldn’t put your open authorizations or unpaid claims at risk. That’s why we approach every billing process with four clear steps:') + g,
                   css='gap: 16px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 14. testimonials (existing site template via shortcode)
def testimonials():
    sc = b.el('e-paragraph', 'ts-sc', cfg={'paragraph': {'name': 'shortcode', 'settings': {'shortcode': '[elementor-template id="388878"]'}}, 'tag': 'span'},
              css='display: block; width: 100%; margin: 0px;')
    return section('s-testi', sc, css='gap: 0px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 15. FAQ (Anesthesia accordion)
FAQS = [
    ('How much do behavioral health billing services cost?', 'The service charges depend on various factors. They include the levels of care you provide, claim volume, payer mix and the required support. Most programs pay a percentage of collections, with no setup fees. You can choose full revenue cycle management or assistance with specific tasks, such as A/R recovery or credentialing. Our free audit helps us review your billing needs and prepare a customized quote.'),
    ('How do you bill IOP and PHP services?', 'We check your program’s settings and payer requirements before preparing claims. Medicare hospital and CMHC claims use the UB-04 with condition code 92 for IOP or 41 for PHP and individual service lines. Commercial and Medicaid contracts may require per diem codes such as S9480, H0015, S0201 or H0035. We review applicable authorizations, service counts and required time documentation before submission.'),
    ('Are behavioral health programs billed on a UB-04 or a CMS-1500?', 'Your program may need both forms, depending on the services and payer. Facility claims generally use the UB-04 (837I), while separately billable professional services use the CMS-1500 (837P). Some Medicaid programs and commercial contracts require freestanding programs to submit per diem claims on the CMS-1500. We check the applicable requirements before deciding how each service should be billed.'),
    ('How do you handle concurrent reviews and authorization renewals?', 'Your team needs to know when approved coverage ends and what the payer requires next. We record authorization dates, schedule reviews and coordinate with your clinical staff for updated notes, treatment plans and discharge progress. If a patient moves to a lower level of care, we request any required authorization before that treatment begins and follow up on the payer’s decision.'),
    ('How do you protect SUD records under 42 CFR Part 2?', 'Before sharing protected SUD records for billing, we check the patient’s consent and applicable disclosure requirements. The updated Part 2 rule, with compliance required since February 16, 2026, permits one consent for treatment, payment and healthcare operations. Our team examines consent before sending claims, appeals or supporting records, with staff access assigned according to their responsibilities.'),
    ('Can you bill out-of-network payers and single case agreements?', 'Yes. We review relevant benefits before admission and request a single case agreement where appropriate. If the payer approves an agreement, we bill according to its terms, track outstanding claims and follow up on payment differences. We support Good Faith Estimates under the applicable No Surprises Act requirements for uninsured or self-pay patients.'),
    ('What is the difference between behavioral health billing and mental health billing?', f'The terms overlap. Mental health billing usually refers to outpatient services billed on the CMS-1500: therapy sessions, psychiatric visits and testing. Behavioral health billing is broader. It also covers substance use treatment and program-level care such as IOP, PHP, residential and detox, which are billed per diem on the UB-04 with their own authorizations. If you run an outpatient practice, see our <a href="{SITE}/specialties/mental-health-billing-service/">mental health billing services</a>.'),
    ('How long does it take to switch behavioral health billing companies?', 'Most programs move over in 4 to 8 weeks. The timeline depends on how many levels of care and payers you have, and whether credentialing or EHR access needs updating. During the parallel run, your current process continues until we confirm every open authorization and claim is covered, so nothing stalls during the switch.'),
]


def faq():
    items = ''
    for i, (q, a) in enumerate(FAQS):
        title = b.el('e-accordion-item-title', f'fq{i}tt', p(f'fq{i}q', q, css=txt('17px', '1.3', INK, 500)), css='padding: 0px;')
        icon = b.el('e-accordion-item-icon', f'fq{i}ic', img(f'fq{i}ii', IMG['chevron'], css='width: 14px; height: auto;'),
                    css='display: flex; align-items: center; justify-content: flex-end; width: 14px; flex-shrink: 0; padding: 0px; transition: transform 0.25s ease;')
        head = b.el('e-accordion-item-header', f'fq{i}h', title + icon, css=(
            'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 10px; padding: 14px 10px; '
            f'border-bottom: 1px solid #EEEEEE; cursor: pointer; &:hover p{{color: {BLUE};}}'))
        body = b.el('e-accordion-item-content', f'fq{i}c', p(f'fq{i}a', a, cls=['global-text'], css=f'color: {GREY}; margin: 0px;'),
                    css='padding: 20px 26px; @media(--mobile){padding: 16px 10px;}')
        items += b.el('e-accordion-item', f'fq{i}', head + body, css='padding: 0px; &[open] .e-accordion-item-icon-base, &[open] [class*="accordion-item-icon"]{transform: rotate(180deg);}')
    acc = b.el('e-accordion', 'fq', items, cfg={'default_state': 'first_expanded', 'max_expanded': 'one', 'show_icon': True, 'faq_schema': True},
               css='display: flex; flex-direction: column; width: 100%; padding: 0px;')
    return section('s-faq', h('fq-h2', 'h2', 'Frequently Asked Questions', css=txt('1.75rem', '1.4', INK, 600, 'width: 100%; @media(--mobile){font-size: 1.4rem;}')) + acc,
                   css='align-items: flex-start; gap: 30px; background-color: #FFFFFF;')


# ---------------------------------------------------------------- 16. final CTA bar (Anesthesia)
def final_cta():
    left = box('fc-l', h('fc-h', 'h2', 'Considering Outsourced Behavioral Health Billing?', css=txt('1.3rem', '1.3', INK, 400))
               + p('fc-p', 'We’ll review your current billing for behavioral health services, including denials, A/R aging and open authorizations, and show you where your program is losing revenue.', cls=['global-text'], css=f'color: {GREY}; margin: 0px;'),
               css='display: flex; flex-direction: column; gap: 10px; width: 75%; padding: 0px; @media(--tablet){width: 100%;}')
    right = box('fc-r', button('fc-b', 'Get a Free Billing Audit', kind='black'), css='display: flex; justify-content: flex-end; width: 25%; padding: 0px; @media(--tablet){width: 100%; justify-content: flex-start;}')
    row = flex('fc-row', left + right, css='display: flex; flex-direction: row; align-items: center; gap: 30px; width: 100%; padding: 0px; @media(--tablet){flex-direction: column; align-items: flex-start; gap: 18px;}')
    return section('s-final', row, css='background-color: #F8F8F8; padding-top: 2rem; padding-bottom: 2rem;')


# testimonials(): the site's carousel is a V3 template ([elementor-template id="388878"]); V4 has no shortcode/HTML widget and a
# dynamic-shortcode paragraph escapes the template's markup, so the carousel is added in the editor (Shortcode widget) after 'steps'.
SECTIONS = [hero, why, cta_auth, levels, rcm, codes, compliance, payers, serve, ai, ehr, choose, steps, faq, final_cta]


def payload(mode='replace_children', dry=False):
    global b
    b = B()
    xml = ''.join(f() for f in SECTIONS)
    return {'post_id': PID, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style, 'classes': b.classes, 'mode': mode, 'dry_run': dry}
