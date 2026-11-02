"""Build the New Mexico state page (states post 411391) from New York, Texas and California state-page sections.

Every section in the content doc has a screenshot of an existing state-page section; there is no new section.
Copies those sections in the doc's order, swaps in the New Mexico copy, regenerates every element id (and the
matching V4 local style ids) and writes ../build/nm_data.json.  Deploy with deploy_nm.py.
"""
import copy, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'south-carolina', 'tools'))
import mcp  # noqa: E402
from build_sc import a, add_css, find, nid, regen_ids, set_grid_rows, walk  # noqa: E402

SRC = {'ny': 386956, 'tx': 386960, 'ca': 386954}
SLUG = 'medical-billing-new-mexico'
MEDIA_JSON = os.path.join(HERE, '..', 'media.json')

# (source page, top-level section id) in New Mexico page order
ORDER = [('ny', '6f2914b3'),   # hero (NY)                      <- doc image12
         ('tx', 'd2e03a9'),    # KPIs + CTA box (TX)            <- image7
         ('ny', '5fefeab8'),   # payer mix (NY, illustration)   <- image10
         ('tx', '1d90565'),    # state-specific rules (TX)      <- image2
         ('ca', 'd60a587'),    # Native American + table (CA)   <- image8
         ('ny', '1f43affa'),   # RCM services list (NY)         <- image6
         ('ny', '5ca4fc10'),   # billing needs heading (NY)     <- image11
         ('ny', '5cd48903'),   # billing needs carousel (NY)
         ('tx', '0497ce3'),    # gross receipts tax cards (TX)  <- image5
         ('tx', 'dfc38cd'),    # specialties (TX)               <- image4
         ('tx', '255873b'),    # practices we support + map (TX) <- image1
         ('tx', 'ca019d2'),    # areas we serve (TX)            <- image13
         ('ny', '3731fb77'),   # support system cards (NY)      <- image9
         ('tx', 'e020f87'),    # testimonials shortcode (as on every state page)
         ('tx', 'e7635f0'),    # FAQ (TX)
         ('tx', 'b7c86b8')]    # bottom CTA (TX)

UTMS = ['medical-billing-new-york', 'medical-billing-texas', 'medical-billing-california']


def p(*paras):
    # the theme forces p { margin-block-end: 0 !important }, so space paragraphs with margin-top
    return ''.join(f'<p>{x}</p>' if k == 0 else f'<p style="margin-top: 14px;">{x}</p>' for k, x in enumerate(paras))


# ---------------------------------------------------------------- copy (from the content doc)
TEXT = {
    # hero (NY, V3)
    '43dfde24': 'Medical Billing Services in New Mexico',
    '527a56ac': p('Unpaid claims and repeated corrections cost your practice time and revenue. MedCare MSO supports the full billing cycle with dependable medical billing services in New Mexico. We verify practitioners’ qualifications and support credentialing, manage claim submission with appropriate coding and payment posting, and efficiently follow the denial process around your specialty and New Mexico’s payer mix. With us, your team spends less time on billing and gets a clearer view of your collections.'),
    # KPIs (TX, V4)
    '4723a59': 'Proof from Practices That Outsourced Their Billing',
    'd623c89': '98.5%', '2973d54': 'First-Pass Clean Claim Rate',
    '4342a79': '35%', '43126a4': 'A/R Reduction',
    '82b00e5': '24/7', '3fcb0c0': 'Dedicated Account Support',
    '88f9a76': 'Ninety Days Go Fast',
    'd3ae281': 'New Mexico Medicaid gives you 90 days from the date of service to file. We make sure no claim gets close to the edge.',
    # payer mix (NY, V3)
    '5efb8db3': 'Medical Billing Built Around New Mexico’s Payer Mix',
    '2e258930': p('New Mexico practices submit claims under Medicare, Medicaid and commercial insurance plans, each with its own coverage and billing requirements. Turquoise Care is the state’s Medicaid managed care program that includes four plans: Presbyterian Health Plan, Blue Cross and Blue Shield of New Mexico, UnitedHealthcare Community Plan and Molina Healthcare, each with distinct coverage plans and billing requirements. Only billing operations that run smoothly here know the patient’s specific plan, check for the provider’s network participation, verify authorization and follow claim submission requests.',
                  'When expanding this picture, older adults add another dimension to reimbursement source breakdown. More than one in five ' + a('https://www.census.gov/quickfacts/fact/table/NM/AGE775224', 'New Mexico residents') + ' are 65 or older. The billing can be even trickier for practices that care for these patients, as it involves Original Medicare, Medicare Advantage, or any additional coverage. For patients covered by both Medicare and Medicaid, identifying the correct payer order, coordinating benefits and checking that documentation supports the billed services are particularly important.',
                  'MedCare MSO’s medical billing services in New Mexico bring AI-powered workflow to these day-to-day billing operations. We assist practices with billing administration, from eligibility checks to payment reconciliation.',
                  '<strong>Discuss your billing requirements with our specialists!</strong>'),
    # rules (TX, V4)
    '5ef1b33': 'Medical Billing and Coding in New Mexico: State-Specific Rules',
    '92ae833': 'Your practice needs to track more than claim submission dates. New Mexico’s billing requirements also affect payment follow-up, claim corrections and patient charges.',
    # Native American (CA, V4)
    'a46d790': 'Billing for Native American Patients, IHS, and 638 Facilities',
    '0bcaeb7': 'Your practice may see Native American patients with different Medicaid arrangements. These members generally choose whether to join Turquoise Care, although enrollment is required for long-term care. Your team needs to confirm whether each patient has fee-for-service coverage or an MCO plan. Members can also receive care through Indian Health Service, Tribal 638 and urban Indian programs, even without a contract between the program and their plan (' + a('https://www.hsd.state.nm.us/lookingforassistance/native_americans/', 'HCA') + ').',
    '09cf10b': 'We check the patient’s coverage at each visit to identify the applicable billing requirements and help prevent avoidable claim routing errors before submission.',
    'e9b3122': 'How is your patient covered?',
    # RCM services (NY, V3)
    '4cb5cacf': 'Medical Billing and RCM Services in New Mexico',
    'ef7f755': p('What makes us different from other medical billing companies in New Mexico is that we don’t let you chase us to find out about payment delays. MedCare MSO facilitates your healthcare practice with a team that understands your specialty and regularly follows up on rejected or denied claims. On top of that, you’ll be informed every step of the way to encourage a sense of transparency. Behind that support, our AI-supported checks help reduce potential errors before a claim submission. With this approach, you can focus on what your New Mexico practice actually needs.',
                 '<strong>Billing support across your revenue cycle:</strong>'),
    # billing needs (NY, V3)
    '351d8651': 'New Mexico Billing Needs We Help You Manage',
    # gross receipts tax (TX)
    '982952f': 'New Mexico Gross Receipts Tax and Your Billing Records',
    '798352e': 'New Mexico’s gross receipts tax can apply to your practice’s revenue, although certain healthcare payments qualify for deductions. Keeping those payments recorded helps your tax adviser review which receipts meet the requirements.',
    # specialties (TX)
    '3d54643': 'Specialties We Bill in New Mexico',
    # practices (TX)
    '9e2474a': 'Practices We Support Across New Mexico',
    # areas (TX)
    'f0a1c94': 'Areas We Serve Across New Mexico',
    '01ee728': 'Where your practice operates can affect the billing needs your team handles. Our medical billing company supports practices across New Mexico, from Albuquerque and Las Cruces to Gallup and Farmington. We consider your patient population, coverage arrangements and available staff when organizing billing support. This includes practices handling fee-for-service Medicaid, Turquoise Care plans and care for tribal communities.',
    # support (NY, V3)
    '58bda145': 'We Have Built a Support System That Fits the Way Your Practice Works',
    '539be11d': 'Clear Communication & Accountability',
    '75361877': p('When you see billing affecting your practice, you expect straight answers. We offer a dedicated point of contact that assists you in understanding what’s being worked on, what needs your input and where errors need further action.'),
    '4246075b': 'Support Around Your Existing Team',
    '3a2ac0f5': p('Your practice may need assistance with the entire revenue cycle or may have a few tasks stretching your staff thin. Our experts analyze your team’s workload and priorities to agree on what we’ll handle and how we’ll deal with it.'),
    # FAQ (TX)
    'd59fa7b': 'Frequently Asked Questions',
    # bottom CTA (TX)
    '497cf92': 'Give Your Team More Time for Patient Care',
    '58b14ce': 'Outsource your medical billing to ' + a('https://medcaremso.com/contact/', 'MedCare MSO') + ' to reduce your team’s administrative workload and keep billing tasks moving. From daily claim processing to unresolved A/R, our medical billing company in New Mexico provides support where your practice needs it.',
}

LISTS = {
    '34bcd151': [('Credentialing and provider enrollment with New Mexico Medicaid', None),
                 ('Coverage verification, authorization assistance and coordination of benefits', None),
                 ('Charge capture, selection of codes and clinical documentation review', None),
                 ('Claim preparation, clean submission, denial resolution and appeals', None),
                 ('Follow-up on outstanding balance and patient statement preparation', None),
                 ('Detailed payment recording, account reconciliation and financial reports', None)],
    '39561c4': [('Rural and frontier clinics', None),
                ('Federally qualified health centers', 'https://medcaremso.com/specialties/fqhc-billing-services/'),
                ('Behavioral health agencies', None),
                ('Practices serving tribal communities', None),
                ('Solo and small practices', 'https://medcaremso.com/services/medical-billing-for-small-practices/'),
                ('Multi-site and multi-specialty groups', None)],
    '6b241402': [('A consistent contact for billing questions', None), ('Get updates on open issues and next steps', None),
                 ('Regular discussion about your priorities', None), ('Clear request for information', None)],
    '5c470553': [('Full revenue cycle management', None), ('Clearly defined billing responsibilities', None),
                 ('Custom workflow around your systems', None), ('Coordination with your practice staff', None)],
}

RULES = [
    ('Medicaid’s 90-Day Filing Limit',
     'Under ' + a('https://regulations.justia.com/states/new-mexico/title-8/chapter-302/part-2/section-8-302-2-11/', '8.302.2.11 NMAC') + ', applicable Medicaid claims must reach the state or its claims processor within 90 calendar days of service. For inpatient care, the timeline starts at discharge. Newly enrolled providers have 90 days from their approval notice. If eligibility is granted retroactively, the window starts when that eligibility is added.'),
    ('One Grace Period for Claim Corrections',
     'If a timely claim is returned, denied or underpaid, your practice has one 90-day grace period from the remittance date to resubmit or request an adjustment. There is no second grace period. We review the response and address the identified issue before resubmission.'),
    ('Secondary Claims and the 210-Day Limit',
     'When another payer processes a claim first, your team needs to track its decision date. Under the applicable Medicaid rule, submission is due within 90 days of that decision and no later than 210 days after service. Submitting the primary claim promptly helps leave time for follow-up.'),
    ('Commercial Payment Timelines and Interest',
     'Under ' + a('https://regulations.justia.com/states/new-mexico/title-13/chapter-10/part-28/section-13-10-28-9', '13.10.28.9 NMAC') + ', applicable health carriers must pay clean electronic claims within 30 days and paper claims within 45 days. If payment is late, interest is due within 30 days after the claim is paid. Our team tracks payment dates and follows up on interest that remains unpaid.'),
    ('Surprise Billing Payments and Patient Responsibility',
     'For services covered by New Mexico’s Surprise Billing Protection Act, carriers pay out-of-network providers directly using the applicable state benchmark. ' + a('https://www.fairhealth.org/article/new-mexico-and-texas-select-fair-health-data-to-address-surprise-billing', 'FAIR Health') + ' describes this as the 60th percentile of allowed commercial rates for the area. Self-funded employer plans generally follow federal protections. Before billing your patients, we check which protections apply and whether their charges are limited to in-network cost-sharing.'),
]

NEEDS = [  # (title, html, icon (id, url) or None to keep the slide's own)
    ('New Mexico Medicaid Portal and Claim Requirements',
     p(a('https://www.hca.nm.gov/turquoise-claims/', 'Turquoise Claims') + ' replaced Omnicaid and the former New Mexico Medicaid Portal on March 23, 2026. This made practices wonder about the NM Medicaid provider portal. Here, MedCare MSO comes into play with reliable support, checking the latest submission requirements, identifying payers and handling claim acknowledgments to avoid processing delays.'), 0),
    ('Medicaid Fee Schedules and Payment Reviews',
     p('When practitioners receive lower payments than expected, they need to know why. Our billing experts compare the payment with the applicable NM Medicaid fee schedule or payer contract. We check the service date and billing conditions to determine whether the difference is valid or needs follow-up. If we identify underpayment, our billing team contacts the payer with supporting documentation to request correction.'), 1),
    ('Timely Filing and Appeal Deadlines',
     p('There is an applicable deadline NM Medicaid expects practices to submit their claims. That timeline varies, depending on the coverage, payer and circumstances. We track these dates and retain submission records and payer acknowledgement. But if it contains any sort of mistakes, our team follows the payer’s correction and resubmission. Or if a denial needs to be challenged, we follow the appeal procedure within the timeframe.'), 0),
    ('Prior Authorization and Documentation',
     p('It is for sure that the care listed on a claim should match the insurance company’s authorization. If the payer approves six therapy sessions within a specific period, the billing team should ensure the claim aligns with the approval. In case of misalignment in the date, services, or units, or if there’s missing information, we alert your practice so the issue can be resolved before submission.'), 2),
    ('New Mexico Surprise Billing Protections',
     p('An unpaid insurance balance does not automatically become the patient’s responsibility. The ' + a('https://law.justia.com/codes/new-mexico/chapter-59a/article-16/section-59a-16-21-3/', 'New Mexico Surprise Billing Law') + ' and the ' + a('https://www.cms.gov/newsroom/fact-sheets/no-surprises-understand-your-rights-against-surprise-medical-bills', 'Federal No Surprises Act') + ' limit patient charges in applicable situations. We check whether or not it applies to the patient’s plan beforehand. Our team sends the patient a bill with relevant cost-sharing and balance-billing restrictions to prevent inappropriate charges.'), 3),
]
TIMELY_ICON = {'id': 3788, 'url': 'https://medcaredemo.online/medcare/wp-content/uploads/2024/04/first-claim-rate-icon.svg'}

TAX = [
    ('Which Payments May Qualify for a Deduction',
     'Under Section 7-9-93 NMSA, eligible practitioners can deduct qualifying commercial contract and Medicare Part C payments from managed care organizations and health insurers. Since July 1, 2023, related patient copays and deductibles may also qualify. Fee-for-service payments from indemnity plans do not qualify under this deduction. Hospitals, hospices, nursing homes and outpatient facilities are excluded from its practitioner definition. The deduction requires the designated rate code when filing through the state’s TAP system.'),
    ('Payment Posting That Supports Your Tax Review',
     'When payments are recorded without payer details, separating eligible receipts can take additional work. Our team records the payer and plan type to help distinguish commercial contract payments, Medicare Part C receipts and related patient payments. Your tax adviser determines eligibility and what to claim, using those billing records for support.'),
]

SPECIALTIES_INTRO = 'Your specialty affects the billing requirements your team needs to follow. These can range from Medicaid enrollment rules for behavioral health agencies to Medicare Advantage authorizations for surgical practices. Select your specialty to explore our billing support.'
PRACTICES_INTRO = 'Your practice may need billing support for a rural clinic or a specialty group with several locations. MedCare MSO is a medical billing company that adjusts its support around your claim volume, payer mix and team’s workload.'

CITIES = ['Albuquerque', 'Las Cruces', 'Rio Rancho', 'Santa Fe', 'Roswell',
          'Farmington', 'Hobbs', 'Clovis', 'Carlsbad', 'Gallup']

FAQ = [
    ('How do I choose a medical billing company in Albuquerque?',
     'Start with fit: experience in your specialty and with your payer mix, including Turquoise Care plans and Medicare Advantage. Then ask how they handle denials inside Medicaid\'s 90-day grace period, how they work aging A/R, what reports you\'ll see and who your point of contact is. Also confirm whether they serve Albuquerque remotely or from a local office.'),
    ('What do medical billing companies in New Mexico charge for their offerings?',
     'The service cost varies, depending on various other factors. These elements can include a monthly fee, percentage of collections, charges for doing specific tasks. When it comes to MedCare MSO, we offer customized pricing, built around your specialty, claim volume, and the required services. Request a written breakdown, including credentialing, patient statements, coding and existing A/R.'),
    ('Does MedCare MSO offer medical billing for small practices in New Mexico?',
     'Absolutely. We offer a range of services for independent practices. These include eligibility confirmation, claim submission, payment posting and denial follow-up. We review your team, systems, and billing needs to agree on the tasks we’ll handle.'),
    ('Can we get help with New Mexico Medicaid provider enrollment and Turquoise Care Billing?',
     'Yes, as we offer reliable credentialing and enrollment support in addition to medical billing and coding services in New Mexico. Our team will evaluate your Medicaid enrollment status and find any additional proactive steps to take for the Turquoise Care plans you bill. Registering with New Mexico Medicaid doesn’t make you an in-network provider with each plan. We help you complete the applicable credentialing and contracting steps.'),
    ('What does onboarding include when we outsource medical billing in New Mexico?',
     'The onboarding process at MedCare MSO starts with reviewing the specialty of the healthcare practice. We proceed further with knowing payer mix, system and outstanding claims. Then, there’s an agreement outlining responsibilities, ensuring appropriate access, organizing workflows and validating the claim submission process. The timeline for execution hinges on the approved scope and enrollment or integration (if any).'),
]

TABLE_HEAD = ['Card', 'Turquoise Care MCO member', 'Fee-for-service Medicaid', 'IHS or Tribal 638 facility']
TABLE_ROWS = [
    ('Who it covers', 'Native American members who joined a plan voluntarily or need long-term care',
     'Native American members who remain outside managed care',
     'Services provided at an IHS or tribally operated 638 hospital or clinic'),
    ('Where the claim goes', 'Through Turquoise Claims to the member’s plan', 'Through Turquoise Claims for state payment',
     'Through Turquoise Claims, following facility-specific billing requirements'),
    ('What to check', 'Applicable CertifyOS credentialing steps and the plan’s authorization requirements',
     'The applicable 90-day filing deadline and state fee schedule',
     'The requirement to finalize applicable claims within two years of service'),
]


# ---------------------------------------------------------------- helpers
def set_text(e, text):
    st, t = e['settings'], e.get('widgetType')
    if t == 'e-heading':
        st['title']['value'] = text
    elif t == 'e-paragraph':
        st['paragraph']['value'] = text
    elif t == 'e-button':
        if isinstance(st.get('text'), dict):
            st['text']['value'] = text
        else:
            st['text'] = text
    elif t == 'heading':
        st['title'] = text
    elif t == 'text-editor':
        st['editor'] = text
    else:
        raise ValueError(f'set_text: {t} {e["id"]}')


def set_list(e, items):
    """Replace an icon-list's items, keeping the first item's icon/settings as the template."""
    old = e['settings']['icon_list']
    tpl = {k: v for k, v in old[0].items() if k not in ('text', 'link', '_id')}
    new = []
    for k, (text, url) in enumerate(items):
        it = dict(copy.deepcopy(tpl), text=text, _id=old[k]['_id'] if k < len(old) else nid())
        if url:
            it['link'] = {'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}
        new.append(it)
    e['settings']['icon_list'] = new


def remove(root, i):
    def w(e):
        e['elements'] = [c for c in e.get('elements', []) if c['id'] != i]
        for c in e['elements']:
            w(c)
    w(root)


def parent_of(root, i):
    out = []
    walk(root, lambda e: out.append(e) if any(c['id'] == i for c in e.get('elements', [])) else None)
    return out[0]


def table_html(tpl):
    style = tpl[:tpl.index('</style>') + len('</style>')]
    style = style.replace('table-layout: fixed;', 'table-layout: fixed;\n    min-width: 620px;')
    style = style.replace('font-size: 15px;\n    text-align: center;', 'font-size: 14px;\n    line-height: 1.5;\n    text-align: center;\n    vertical-align: top;')
    head = ''.join(f'<th style="text-align:center;">{h}</th>' for h in TABLE_HEAD)
    rows = ''.join('<tr>' + f'<td><strong>{r[0]}</strong></td>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in TABLE_ROWS)
    return f'{style}\n<div class="table_component">\n  <table>\n    <thead><tr>{head}</tr></thead>\n    <tbody>{rows}</tbody>\n  </table>\n</div>\n'


# ---------------------------------------------------------------- build
def build(src):
    random.seed(411391)
    tops = {k: {e['id']: e for e in copy.deepcopy(v)} for k, v in src.items()}
    secs = {sid: tops[pg][sid] for pg, sid in ORDER}
    every = lambda: [secs[sid] for _, sid in ORDER]  # noqa: E731

    # copy reusable widgets before their originals are edited
    intro_tpl = copy.deepcopy(find(secs['0497ce3'], '798352e'))     # centered V4 intro paragraph
    side_para_tpl = copy.deepcopy(find(tops['tx']['64b84d6'], '0f8bde9'))  # left-aligned V4 paragraph
    subhead_tpl = copy.deepcopy(find(tops['ca']['5b8a846'], 'fe4ae00'))    # "We offer assistance with" heading

    for root in every():
        for i, t in TEXT.items():
            try:
                set_text(find(root, i), t)
            except IndexError:
                pass
        for i, items in LISTS.items():
            try:
                set_list(find(root, i), items)
            except IndexError:
                pass

    # hero: NY banner button
    btn = find(secs['6f2914b3'], '4b31fa2')
    btn['settings']['html'] = btn['settings']['html'].replace('medical-billing-new-york', SLUG)

    # payer mix: no list in the New Mexico copy
    remove(secs['5fefeab8'], '132040a')

    # rules: 4 cards -> 5 (fifth spans the row); no claims-review CTA box in the New Mexico copy
    rules = secs['1d90565']
    grid = find(rules, '80b07a8')
    fifth = copy.deepcopy(grid['elements'][3])
    add_css(fifth, 'grid-column: 1 / -1;')
    grid['elements'].append(fifth)
    for card, (title, body) in zip(grid['elements'], RULES):
        h, para = card['elements']
        h['settings']['title']['value'] = title
        para['settings']['paragraph']['value'] = body
    set_grid_rows(grid, 2, 1)
    remove(rules, '49834db')

    # Native American: case-study layout (CA) with the coverage table
    na = secs['d60a587']
    remove(na, '2a7a5bc')    # case-study subtitle
    remove(na, 'af074db')    # "View All Case Study" button
    tbl = find(na, '64fe978')
    tbl['settings']['html'] = table_html(tbl['settings']['html'])
    right = find(na, '595a8f6')  # California hides this column on mobile; here the table is content
    for st in right['styles'].values():
        for v in st['variants']:
            if v['meta']['breakpoint'] == 'mobile' and 'display' in v['props']:
                v['props']['display']['value'] = 'flex'

    # RCM services: heading level
    rh = find(secs['1f43affa'], '4cb5cacf')['settings']
    rh['header_size'] = 'h2'
    rh.pop('_css_classes', None)  # its '.california-main-heading h2 {line-height:1.5}' rule only targeted the h2 tag

    # billing needs: intro paragraph under the heading, 4 slides -> 5
    head = secs['5ca4fc10']
    intro = copy.deepcopy(intro_tpl)
    intro['settings']['paragraph']['value'] = 'Your practice needs a billing team you can count on. We make claims moving, make reports easy to access and help you stay current with changes that affect your payments. MedCare MSO believes in building a working relationship that supports your practice as it grows.'
    head['elements'].append(intro)
    car = find(secs['5cd48903'], '159a38d8')
    slides = car['elements']
    order = [copy.deepcopy(slides[n]) for _, _, n in NEEDS]
    for k, (slide, (title, body, _)) in enumerate(zip(order, NEEDS)):
        inner = slide['elements'][0]
        img, h, txt = inner['elements']
        h['settings']['title'] = title
        txt['settings']['editor'] = body
        if k == 2:
            img['settings']['image'] = dict(img['settings']['image'], **TIMELY_ICON)
        slide['settings']['_title'] = f'Slide #{k + 1}'
    car['elements'] = order
    car['settings'].update({'slides_to_show_mobile_extra': '1', 'slides_to_show_mobile': '1',
                            # the 250px right offset left a ~120px slide on phones
                            'offset_width_mobile_extra': {'unit': 'px', 'size': 60, 'sizes': []},
                            'offset_width_mobile': {'unit': 'px', 'size': 40, 'sizes': []}})
    car['settings']['carousel_items'] = [{'slide_title': f'Slide #{k + 1}', '_id': nid()} for k in range(len(order))]

    # gross receipts tax: 2 cards, no closing paragraph
    tax = secs['0497ce3']
    cards = find(tax, '6308393')
    cards['elements'] = cards['elements'][:2]
    cards['settings']['grid_rows_grid'] = {'unit': 'fr', 'size': 1, 'sizes': []}
    cards['settings']['grid_rows_grid_mobile_extra'] = {'unit': 'fr', 'size': 2, 'sizes': []}
    for c, (title, body) in zip(cards['elements'], TAX):
        ib = c['elements'][0]
        ib['settings']['title_text'] = title
        ib['settings']['description_text'] = body
    remove(tax, '660d4a1')

    # specialties: intro paragraph under the heading
    spec = secs['dfc38cd']
    sp = copy.deepcopy(intro_tpl)
    sp['settings']['paragraph']['value'] = SPECIALTIES_INTRO
    spec['elements'].insert(1, sp)

    # practices: intro + "Who We Work With" before the list
    col = parent_of(secs['255873b'], '39561c4')
    k = [c['id'] for c in col['elements']].index('39561c4')
    pi = copy.deepcopy(side_para_tpl)
    pi['settings']['paragraph']['value'] = PRACTICES_INTRO
    sh = copy.deepcopy(subhead_tpl)
    sh['settings']['title']['value'] = 'Who We Work With'
    col['elements'][k:k] = [pi, sh]

    # areas: city names (Texas photos stay until New Mexico photos are in the Media Library)
    media = json.load(open(MEDIA_JSON)) if os.path.exists(MEDIA_JSON) else {}
    cgrid = find(secs['ca019d2'], 'ecb0376')
    for card, name in zip(cgrid['elements'], CITIES):
        img = [c for c in card['elements'] if c.get('widgetType') == 'e-image'][0]
        par = [c for c in card['elements'] if c.get('widgetType') == 'e-paragraph'][0]
        par['settings']['paragraph']['value'] = name
        f = name.replace(' ', '-') + '-NM.webp'
        if f in media:
            img['settings']['image']['value']['src']['value']['id']['value'] = media[f]['id']

    # support system cards: H3 titles
    for i in ('539be11d', '4246075b'):
        find(secs['3731fb77'], i)['settings']['header_size'] = 'h3'

    # FAQ: 5 items
    acc = find(secs['e7635f0'], '70dfcaa')
    for k, (cont, (q, ans)) in enumerate(zip(acc['elements'], FAQ)):
        cont['elements'][0]['settings']['paragraph']['value'] = ans
        acc['settings']['items'][k]['item_title'] = q
    assert len(acc['elements']) == len(FAQ)

    if media.get('hero'):
        secs['6f2914b3']['settings']['background_image'] = dict(secs['6f2914b3']['settings']['background_image'], **media['hero'])

    page = every()
    txt = json.dumps(page, ensure_ascii=False)
    for u in UTMS:
        txt = txt.replace(u, SLUG)
    out = json.loads(txt)
    seen = set()
    for e in out:
        regen_ids(e, seen)
    return out


def check(out):
    t = json.dumps(out, ensure_ascii=False)
    words = ['Texas', 'New York', '(NY)', 'California', 'Medi-Cal', 'TMHP', 'Dallas', 'Dr. Neufeld', 'Case Study', 'Behavioral Health Practice']
    ids = []
    for e in out:
        walk(e, lambda x: ids.append(x['id']))
    assert len(ids) == len(set(ids)), 'duplicate ids'
    return [w for w in words if w in t], len(ids)


if __name__ == '__main__':
    src = {k: json.loads(mcp.rest('GET', f'wp/v2/states/{i}?context=edit&_fields=meta')['meta']['_elementor_data']) for k, i in SRC.items()}
    out = build(src)
    bad, n = check(out)
    os.makedirs(os.path.join(HERE, '..', 'build'), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, '..', 'build', 'nm_data.json'), 'w'), ensure_ascii=False)
    print('sections', len(out), 'elements', n, 'leftover source words:', bad)
