"""Build the South Carolina state page (states post 411363) from the California state page.

Copies the California sections shown in the content doc's screenshots, swaps in the South Carolina
copy, adds the one new section ("Healthy Connections Compliance Rules"), regenerates every element id
(and the matching local style ids) and writes the result to ../build/sc_data.json.

usage: python3 build_sc.py            -> build only
       deploy with deploy_sc.py
"""
import base64, copy, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

CA_ID = 386954
SC_HERO = 411365          # South-Carolina-Hero-Banner-1920x900
ICONS = {1: (404840, '2026/07/icon-number01.svg'), 2: (404841, '2026/07/icon-number02.svg'),
         3: (404842, '2026/07/icon-number03.svg'), 4: (404843, '2026/07/icon-number04.svg'),
         5: (404844, '2026/07/icon-number05.svg'), 6: (408016, '2026/08/icon-number06.svg'),
         7: (411366, '2026/11/icon-number07.svg')}
SOURCE_ICON = 411367       # small document icon for the source note
UPLOADS = 'https://medcaredemo.online/medcare/wp-content/uploads/'
UTM_OLD, UTM_NEW = 'utm_source=medical-billing-california', 'utm_source=medical-billing-south-carolina'

# California top-level sections kept, in South Carolina page order. 'NEW' marks the new section.
ORDER = ['d8ac86e',   # hero + banner form
         'ad92569',   # KPIs + "Collect What You Billed"
         '5b8a846',   # outsourced billing (illustration + list)
         '242f0fb',   # five -> seven rules
         'b206976',   # two tracks
         'd4a5b2b',   # payers (CTA box moved below the new section)
         'NEW',       # Healthy Connections Compliance Rules (+ moved CTA box)
         'cbfc466',   # step-by-step
         'e0cbdde',   # certified coding
         'ce0a3b8',   # specialties (unchanged)
         '75d5ffd',   # EHR carousel
         '144eabc',   # built around your specialty
         '245b176',   # cities
         '5f5a6aed',  # testimonials shortcode (unchanged)
         'd303d44',   # FAQ
         'df3702f']   # bottom CTA


def a(href, text):
    return f'<a target="_blank" href="{href}"><u>{text}</u></a>'


# ---------------------------------------------------------------- copy (from the content doc)
TEXT = {
    # hero
    '9e08573': 'Medical Billing Services in South Carolina',
    '5813535': 'The complexities at the payers’ end make state-specific billing rules difficult to understand. However, you do not need to know these rules when MedCare MSO handles the claims in South Carolina. Our team understands the intricacies of claims and their various routes, like Palmetto GBA for Medicare claims, BlueCross BlueShield for commercial claims, TRICARE for military families, and Medicaid’s routes through Healthy Connections managed care organizations. Each payer has its own rules that make the claim correct and each has its own prior authorization rules. Our medical billing services in South Carolina are meant to help practices optimize revenue by submitting accurate claims to the relevant payer routes. The result is an efficient ' + a('https://medcaremso.com/services/revenue-cycle-management/', 'revenue cycle') + ' and improved overall collections.',
    # KPIs
    '2cc357f': 'The Numbers Behind Our Medical Billing Services in South Carolina',
    'de8d971': 'Collect What You Billed',
    '07b9858': 'Five Medicaid plans, one Medicare contractor and a 20-business-day prompt-pay clock: we work all of them so your South Carolina practice gets paid on the first submission.',
    # outsourced
    '64acd81': 'Outsourced Medical Billing for South Carolina Practices',
    '8627165': 'It rarely happens that a medical practice in Greenville, Charleston or Columbia bills one payer. What happens in one week at the front desk? Medicare claims for Palmetto GBA, Medicaid claims to one of the five Healthy Connections plan, BlueCross BlueShield of South Carolina claims on the prompt-pay clock, military families bill to TRICARE. Each of them has its own portal, own prior authorization rules and its own theory of an accurate claim. Our billers and coders provide peace of mind to your front desk and do the work based on the diverse payer rules in South Carolina.',
    '0c726e0': 'What do you get back? Ample time to focus on patient care. We verify the coverage details before the patient’s visit and submit electronic claims so the prompt-pay clock starts from the first day. We post every payment and help reduce denials by finding the root cause. Our reporting shows what payers are holding which makes the problems visible before they become an unpaid A/R. Outsourced medical billing in South Carolina means lesser hours spent in the administrative work and more time for the patients.',
    # rules
    'ae498ae': 'Five South Carolina Rules That Decide When You Get Paid',
    'e6b3a4a': 'South Carolina’s payment rules live in two places, the state insurance code and Healthy Connections policy. These are the five our team checks on every claim:',
    # two tracks
    '3650669': 'One Medicaid Program, Two Tracks: Fee-for-Service vs Managed Care',
    '348eddb': 'Healthy Connections pays a claim in one of the two ways. But what determines which way? It depends on the service and the member, not on the practice. Our experts track the claim from the beginning which is the time when eligibility is determined. So, every claim goes to the payer that will pay it.',
    'c9b905e': 'Which track pays the claim?',
    '9af9766': 'Fee-for-service',
    '6a56556': 'State track',
    '83ef38c': 'Who pays: SCDHHS, from the state Medicaid budget',
    '2564f1c': 'At what rate: the state fee schedule',
    '999bac4': 'Where the claim goes: to SCDHHS',
    'f7ddde8': 'Managed care',
    'a2cbd18': 'Plan track',
    'eb7c978': 'Who pays: the member’s managed care plan',
    'c1d368f': 'At what rate: the plan’s contracted rate',
    '304b7b7': 'Where the claim goes: the plan’s own portal',
    'ca0a010': 'Track checked before the claim is built',
    '2fdd08c': 'The claim is checked by our team before it is created, not after it comes back denied. The member’s plan is confirmed at eligibility on every date of service.',
    # payers
    'c86391c': 'South Carolina Medical Billing Services for Every Payer',
    '29080ac': 'Our billers and coders work the four payer types that fill a South Carolina practice’s A/R. We bill:',
    # CTA (moved under the new section)
    '3c78265': 'Is every claim on the right South Carolina clock?',
    '65d5700': 'We check your recent claims against the 20-business-day prompt-pay window, the 120-day clean-claim limit and each Healthy Connections plan’s rules, and show you where payment is stalling. The review is free and the findings are yours to keep.',
    # steps
    '55374bd': 'The process breakdown shows how we handle the medical claims for practices based in South Carolina. For Medicare claims, we check the claims against the coverage policies of Palmetto GBA. The Medicaid claims are analyzed against the managed care plan of the member. For commercial plans, we check it against the contract. The steps mentioned below are what medical practices in South Carolina see from the outside.',
    # coding
    'db3ea26': 'AAPC and AHIMA Coders for South Carolina Claims',
    '17443e8': 'The payers in South Carolina pay on the codes mentioned on the medical claim and coding accuracy is essential to get complete payments. Our medical coders hold AAPC or AHIMA credentials and work with CPT, ICD-10-CM and HCPCS daily.',
    '466b5ad': 'Certified coders identify errors that lead to denials in South Carolina, like a procedure code that invites an NCCI edit at Palmetto, a diagnosis that does not go with the medical necessity under a local coverage determination, or a modifier that does not align with the place of service. Every code is used correctly before the claims leave our team instead of reworking the denials.',
    'bf95439': 'What certified coding gives a South Carolina practice:',
    '6f5e5e7': 'Request a Consultation',
    # EHR
    '9f42ec6': 'EHR-Compatible Billing for South Carolina Practices',
    # built around your specialty
    'd8dfd3d': 'Medical Billing Company in South Carolina, Built Around Your Specialty',
    'a6d750d': 'A solo practice based in Florence and a multi-site group in Greenville are not billing in the same manner. The important thing is that these claims from different practices should not be billed the same way. Our medical billing and coding services in South Carolina are meant to cater the specialty, payer mix and volume. Whatever the size of the practice is, we ensure that the claim goes out right the first time. We take care of every track and different billing rules as per the payers.',
    # cities
    '226f454': 'Medical Billing Services Across South Carolina',
    '52b0c66': 'Our medical billing company works with providers in every part of the state: Columbia, Charleston, Greenville, Spartanburg, Rock Hill, Mount Pleasant, Myrtle Beach, Summerville, Sumter and Florence. From the Upstate to the Lowcountry, the service is the same: claims built to South Carolina’s rules, from the 20-business-day prompt-pay clock to the Healthy Connections plan each patient is actually enrolled in.',
    # FAQ
    '8c643c4': 'FAQs',
    # bottom CTA
    '4391013': 'Looking for the Best Medical Billing Company in South Carolina?',
    '4335f5a': 'Send us 90 days of remittance data and we’ll show you which South Carolina payer is holding your money and why: the Palmetto GBA edits, the Healthy Connections plan mismatches, the BCBS claims past the 20-day clock. The audit is free and the report is yours whether or not we work together.',
}

LISTS = {
    '7e4d3e0': [('Provider enrollment and credentialing', 'https://medcaremso.com/services/credentialing-services/'),
                ('Insurance eligibility verification', None),
                ('Medical coding & compliance', 'https://medcaremso.com/ai-eco-system/ai-medical-coding/'),
                ('Denial management and appeals', 'https://medcaremso.com/services/denial-management-services/'),
                ('A/R management and follow-ups', 'https://medcaremso.com/services/ar-recovery-services/'),
                ('Payment posting and reconciliation', None)],
    '5c173ee': [('Coders credentialed by AAPC and AHIMA', None),
                ('Coding matched to each payer’s level of specificity, from Medicaid managed care to TRICARE', None),
                ('Working knowledge of CPT, ICD-10-CM and HCPCS, including Palmetto GBA’s local coverage rules', None),
                ('Fewer coding denials and less revenue written off', None),
                ('Internal audits that keep the coding team’s accuracy measured, not assumed', None)],
}

RULES = [
    ('Prompt Pay: 20 Business Days Electronic, 40 Paper',
     'Under ' + a('https://www.scstatehouse.gov/code/t38c059.php', 'S.C. Code § 38-59-230') + ', an insurance company has 20 working days to pay or deny the electronic claim. If the insurer takes more time, they owe you interest on the money. It works the same way as a late load payment carries interest. We help submit accurate claims and log the receipt date so we can bill the interest if the commercial payer does not pay within the time limit.'),
    ('The 120-Business-Day Clean-Claim Window',
     'The deadline of the 20 business days applies to a “clean claim.” The definition of a clean claim contains the time as well. If the insurer receives the claim within 120 working days of the day the patient was seen, the claim is clean. If the claim is sent on the day 121, it is not clean and the 20-day deadline never starts.'),
    ('Billing Services May Not Downgrade Your Claims to Paper',
     'Some clearinghouses and billing companies used to print the electronic claim, print it out, and mail it. It started with a 40-day clock instead of a 20-day clock. South Carolina made this illegal and called it an unfair trade practice. We keep the claims electronic all the way to comply with the state rules.'),
    ('Dual-Eligible, Waiver and Nursing-Facility Members Are in Managed Care',
     'Healthy Connections members who have Medicare as well, members in home- and community-based waiver programs, and nursing-facility residents aged 18 and over are now ' + a('https://scdhhs.gov/partners/managed-care/managed-care-carve', 'enrolled in managed care plans') + ' for their medical services. The waiver services themselves and the nursing-facility stay in fee-for-service, so one patient can have two payers. Plans must honor a newly enrolled member’s existing prior authorizations for 180 days at fee-for-service rates, even out of network. We re-verify each affected patient’s plan and track that window so the claim goes where it will be paid.'),
    ('Healthy Connections Prime Has Ended',
     'Healthy Connections Prime, the plan that combined Medicare and Medicaid for dual-eligible members, ' + a('https://www.scdhhs.gov/partners/managed-care/healthy-connections-prime', 'no longer exists') + '. What do those members carry now? They carry a Dual Special Needs Plan or standard Medicare on one side and a Healthy Connections managed care plan on the other, which means two payers, two portals and two claims for one visit. We split and route each claim to the correct side to ensure accuracy.'),
    ('Insurers Have 18 Months to Take a Payment Back',
     'Under S.C. Code § 38-59-250, a commercial insurer may not start recovering an overpayment more than eighteen months after the provider received it, and must give thirty business days’ written notice before offsetting it against other claims. The limit does not apply where the insurer reasonably suspects fraud, to self-insured plans, or to government programs. We log the payment date on every commercial claim so a late recoupment can be challenged on the date alone.'),
    ('The Department of Insurance Enforces the Clock',
     'The prompt-pay article gives providers no right to sue; § 38-59-270 puts enforcement with the South Carolina Department of Insurance. When a fully insured plan runs past the deadline and does not pay interest, the route is a complaint to the Department, with the claim’s receipt date and the remittance attached. We keep both on file for every commercial claim so the complaint can be built without a search.'),
]

PAYERS = [
    ('Healthy Connections Managed Care Plans',
     'Most Medicaid patients have one of five plans: Absolute Total Care, Healthy Blue, Humana Healthy Horizons, Molina or Select Health. Each plan is different due to a different portal, different prior authorization rules, and different time windows for appeals. As a medical billing company in South Carolina, we confirm the member’s plan on every date the services are offered because we take care of the carve-in changes.'),
    ('BlueCross BlueShield of South Carolina',
     'Most commercial claims a practice based in South Carolina are sent to the BCBSSC. It runs on the 20-day prompt-pay clock, so we make sure that claim falls under the deadline before it goes out. We bill the interest when a clean claim is late.'),
    ('TRICARE',
     'Fort Jackson, Shaw Air Force Base, Joint Base Charleston and Parris Island put military families in waiting rooms from Columbia to the Lowcountry. TRICARE claims run through the regional contractor’s referral and authorization rules, not the base’s, and they fail for reasons commercial claims never do. Medical practices that outsource medical billing in South Carolina to us get a team that already knows those rules.'),
    ('Medicare',
     'South Carolina’s Part A and Part B claims are paid by Palmetto GBA, the Jurisdiction M contractor headquartered in Columbia. We code to Palmetto’s local coverage determinations and keep track of the prior authorizations. For documentation requests, we answer from the record. So, Medicare claims do not get delayed due to any discrepancies in the record.'),
    ('Workers’ Compensation',
     'Work-injury claims in South Carolina are paid under the ' + a('https://wcc.sc.gov/medical-fee-schedules', 'Workers’ Compensation Commission’s medical fee schedule') + ', not under the practice’s commercial contracts, and they go to the employer’s carrier with the claim number, not to the patient’s health plan. We bill them from the Commission’s schedule and keep them out of the commercial A/R so they are not worked against the wrong rules.'),
]

STEPS = {
    '3fae60e': ('Patient Registration and Verification', 'Before the patient’s visit, our team verifies eligibility to reduce the chances of claim rejections. For Healthy Connections, we confirm which plan among the five managed care plans the patient is enrolled with. It is not necessary that the plan on the card is going to pay for the rendered services. If the claim is sent to the wrong payer, it surely leads to a claim denial.'),
    '1a068db': ('Coding and Documentation Review', 'Our medical coders are adept at what they do and they match the documentation to the codes. They check the Medicare claims whether these claims align with the Palmetto GBA’s local coverage determinations before submitting to the payer.'),
    '9595d87': ('Claim Submission', 'Electronic claims are submitted electronically to Palmetto GBA, managed care plans, and the commercial payers by our team. The prompt-pay clock begins for the electronic claims sent to the commercial payers in South Carolina.'),
    '66512a0': ('Payment Posting', 'Our team posts payment from every payer against the claim. It is done line by line, so you see what was paid and what was adjusted. What the payer still owes and what the patient needs to pay, everything is mentioned.'),
    '709d64a': ('Denial Management and A/R Follow-Up', 'Claim denials are resubmitted by our team after corrections or our team of denial management experts appeal within the deadline of the payer. Aging accounts receivable is worked by our team until we help South Carolina practices get accurately paid.'),
    '56a301a': ('Reporting & Optimization', 'You get reports that have all the details about the claims and payments. The reports give you an idea about the payers that delay payments, which claims get denied the most, and which areas need improvement.'),
}

CITIES = ['Columbia', 'Charleston', 'Greenville', 'Spartanburg', 'Rock Hill',
          'Mount Pleasant', 'Myrtle Beach', 'Summerville', 'Sumter', 'Florence']

FAQ = [
    ('Who is the Medicare Administrative Contractor for South Carolina?', 'Palmetto GBA, under Jurisdiction M, processes Part A and Part B claims for South Carolina, North Carolina, Virginia and West Virginia. It is headquartered in Columbia. Its local coverage determinations and prior authorization programs are what a South Carolina Medicare claim is judged against, so coding to Palmetto’s rules is part of our standard workflow.'),
    ('Which managed care plans does Healthy Connections Medicaid use?', 'Managed care plans used by Healthy Connections are Absolute Total Care, Healthy Blue, Humana Healthy Horizons, Molina or Select Health (First Choice). Every managed care plan has its own portal, prior authorization requirements and time windows for appeal. We confirm the member’s plan on the date of service because the plan at the time of intake is not always the one that is going to pay.'),
    ('What changed for South Carolina Medicaid on January 1, 2026?', 'Two things. SCDHHS moved dual-eligible members, waiver members and nursing-facility residents aged 18 and over into managed care plans for their medical services, while waiver and nursing-facility services stayed fee-for-service; plans must honor existing prior authorizations for 180 days. On the same day, Healthy Connections Prime, the state’s Medicare-Medicaid plan, ended, and its members moved to a Dual Special Needs Plan or a standard Medicare plan alongside their Medicaid plan.'),
    ('How quickly do South Carolina insurers have to pay a clean claim?', 'Under S.C. Code § 38-59-230, an insurer must pay or deny a clean electronic claim within 20 business days and a paper claim within 40. Interest runs on late payment under § 38-59-240. The rule applies to fully insured commercial plans; Medicare, Medicaid and self-funded employer plans are outside it. We submit electronically and track the receipt date so the clock is on your side.'),
    ('Do you bill TRICARE for practices near Fort Jackson, Shaw or Joint Base Charleston?', 'Yes. TRICARE claims follow a path which is based on the regional contractor’s referral and different authorization rules as compared to commercial plans. Medical practices based in Columbia, Sumter and the Charleston area see enough military families. So, these rules are a daily part of their medical billing. We help medical practices submit these claims along with Medicare, Medicaid and BCBS of South Carolina.'),
    ('How long do we have to file a South Carolina Medicaid claim?', 'One year from the date of service, or from discharge for hospital claims; the claim has to be received and entered by then, not just sent. Medicare crossover claims get two years from the date of service or six months from the Medicare payment, whichever is later. Commercial claims run on the contract’s timely filing limit, which is often shorter, and the state’s prompt-pay protection only applies to a claim received within 120 business days.'),
    ('How much do your medical billing services in South Carolina cost?', 'The pricing of the medical billing services is a percentage of collections. So, when you get paid, we get paid. There are no setup fees and the percentage depends on specialty, volume of the claims, payer mix. This is what we determine after a short review of your current billing.'),
]

COMPLIANCE = [
    ('01', 'Timely filing', 'One Year to File', 'A Healthy Connections claim is considered for payment only if it is received and entered within one year of the date of service, or the discharge date for hospital claims. Medicare cost-sharing claims get two years from the date of service or six months from the Medicare payment date, whichever is later. We work the one-year date from the day the claim is created, not from the first denial.'),
    ('02', 'Enrollment', 'Enrolled With SCDHHS, Not Just the Plan', 'A provider who contracts with one or more Healthy Connections managed care plans must also be enrolled with SCDHHS. Plan credentialing alone does not make a provider a South Carolina Medicaid provider, and claims from an un-enrolled provider fail at the state level no matter which plan the member is in. We check SCDHHS enrollment before the first managed care claim goes out.'),
    ('03', 'Records', 'Four Years of Records', 'Medicaid providers must keep fiscal and health records for a minimum of four years after the last payment; hospitals and nursing facilities keep them for six. When SCDHHS Program Integrity asks for a record and it is not produced, the payment can be recovered and the provider sanctioned. We keep the claim, the remittance and the supporting documentation together for the full retention period.'),
    ('04', 'Program Integrity', 'Program Integrity Can Recover, Suspend and Exclude', 'SCDHHS Program Integrity exists to find waste, fraud and abuse in Medicaid funds, and the Provider Guide bars every form of kickback and self-referral. A records request from Program Integrity is answered from the record on time, because the alternative is recovery of the payment and, in the worst case, exclusion from the program.'),
]


# ---------------------------------------------------------------- V4 prop helpers
def size(v, u='px'): return {'$$type': 'size', 'value': {'size': v, 'unit': u}}
def s(v): return {'$$type': 'string', 'value': v}
def gvar(v): return {'$$type': 'global-color-variable', 'value': v}
def color(v): return {'$$type': 'color', 'value': v}
def dims(t, r, b, l, u='px'):
    return {'$$type': 'dimensions', 'value': {'block-start': size(t, u), 'inline-end': size(r, u), 'block-end': size(b, u), 'inline-start': size(l, u)}}
def bg(c): return {'$$type': 'background', 'value': {'color': color(c)}}
def raw(css): return {'raw': base64.b64encode(css.encode()).decode()}
def shadow(x, y, blur, spread, c):
    return {'$$type': 'box-shadow', 'value': [{'$$type': 'shadow', 'value': {
        'hOffset': size(x), 'vOffset': size(y), 'blur': size(blur), 'spread': size(spread), 'color': color(c)}}]}

POPPINS = {'$$type': 'global-font-variable', 'value': 'e-gv-4ceb0c1'}
WHITE, BLACK, GRAY, BLUE, GREEN = 'e-gv-518e8d8', 'e-gv-f89c7af', 'e-gv-ceec6cf', 'e-gv-5d14286', 'e-gv-bd42318'


def nid():
    return '%07x' % random.getrandbits(28)


def el(kind, settings=None, children=None, styles=None, gclasses=(), widget=True):
    """A V4 element. styles: {breakpoint: (props, css)} -> one local class."""
    i = nid()
    e = {'id': i, 'elType': 'widget' if widget else kind, 'settings': dict(settings or {}), 'isInner': False,
         'elements': children or [], 'styles': {}, 'interactions': [], 'editor_settings': [], 'version': '0.0'}
    if widget:
        e['widgetType'] = kind
    classes = list(gclasses)
    if styles:
        sid = f'e-{i}-{nid()}'
        e['styles'][sid] = {'id': sid, 'label': 'local', 'type': 'class', 'variants': [
            {'meta': {'breakpoint': bp, 'state': None}, 'props': props, 'custom_css': raw(css) if css else None}
            for bp, (props, css) in styles.items()]}
        classes.append(sid)
    if classes:
        e['settings']['classes'] = {'$$type': 'classes', 'value': classes}
    return e


def heading(text, tag, styles, gclasses=()):
    return el('e-heading', {'tag': s(tag), 'title': {'$$type': 'escaped-html', 'value': text}}, styles=styles, gclasses=gclasses)


def para(text, styles, gclasses=('g-6181ecc',)):
    return el('e-paragraph', {'paragraph': {'$$type': 'escaped-html', 'value': text}}, styles=styles, gclasses=gclasses)


def box(children, styles, kind='e-div-block', gclasses=()):
    return el(kind, children=children, styles=styles, gclasses=gclasses, widget=False)


def image(att_id, alt, styles):
    return el('e-image', {'image': {'$$type': 'image', 'value': {'src': {'$$type': 'image-src', 'value': {
        'id': {'$$type': 'image-attachment-id', 'value': att_id}, 'url': None}}, 'size': s('full')}}}, styles=styles)


def new_section(cta):
    """Healthy Connections Compliance Rules We Build Into Every Claim (the doc's one new section)."""
    cards = []
    for num, tag, title, body in COMPLIANCE:
        cards.append(box([
            box([para(num, {'desktop': ({'color': gvar(BLUE), 'font-size': size(15)},
                                        'font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: .04em;')}, gclasses=()),
                 para(tag, {'desktop': ({'color': gvar(BLUE), 'font-family': POPPINS, 'font-weight': s('500'), 'font-size': size(13),
                                         'padding': dims(4, 12, 4, 12), 'border-radius': size(999), 'background': bg('#EAF5FF'),
                                         'border-width': size(1), 'border-style': s('solid'), 'border-color': color('#D3E6F5')}, '')}, gclasses=())],
                {'desktop': ({'display': s('flex'), 'flex-direction': s('row'), 'align-items': s('center'), 'gap': size(10)}, '')}),
            heading(title, 'h3', {'desktop': ({'font-family': POPPINS, 'font-weight': s('500'), 'font-size': size(1.35, 'rem'),
                                               'line-height': size(130, '%'), 'color': gvar(BLUE)}, ''),
                                  'tablet': ({'font-size': size(1.25, 'rem')}, '')}),
            para(body, {'desktop': ({'color': gvar(GRAY), 'line-height': size(170, '%')}, '')}),
        ], {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'gap': size(14), 'padding': dims(34, 30, 34, 30),
                         'border-radius': size(20), 'background': bg('#FFFFFF'),
                         'box-shadow': shadow(0, 12, 32, 0, 'rgba(3, 103, 161, 0.08)')},
                        'position: relative; &::before { content: ""; position: absolute; top: 0; left: 30px; right: auto; '
                        'width: calc(100% - 60px); height: 3px; background: #7EB13E; border-radius: 0 0 3px 3px; }'),
            'mobile': ({'padding': dims(28, 22, 28, 22)}, 'h3 { font-size: 1.15rem; }')}))

    left = box([
        para('Medicaid Compliance', {'desktop': ({'color': gvar(GREEN), 'font-family': POPPINS, 'font-weight': s('600'), 'font-size': size(14)},
                                                 'text-transform: uppercase; letter-spacing: .14em;')}, gclasses=()),
        heading('Healthy Connections Compliance Rules We Build Into Every Claim', 'h2',
                {'desktop': ({'color': gvar(BLACK), 'line-height': size(120, '%')}, ''),
                 'tablet': ({'text-align': s('center')}, '')}, gclasses=('g-0a6ebf3',)),
        para('South Carolina Medicaid has its own deadlines and record rules, separate from the state insurance code. These four are in SCDHHS’s '
             + a('https://scdhhs.gov/sites/dhhs/files/Provider%20Administrative%20and%20Billing%20Guide.pdf', 'Provider Administrative and Billing Guide')
             + ', and each one is a denial or a recovery if it is missed.',
             {'desktop': ({'color': gvar(GRAY), 'line-height': size(170, '%')}, ''),
              'tablet': ({'text-align': s('center')}, '')}),
        box([image(SOURCE_ICON, '', {'desktop': ({'width': size(40), 'height': size(40), 'padding': dims(9, 9, 9, 9),
                                                  'border-radius': size(10), 'background': bg('#FFFFFF')},
                                                 'flex: 0 0 auto; box-shadow: 0 2px 6px rgba(0,0,0,.06);')}),
             para('Source: SCDHHS Provider Administrative and Billing Guide, Section 1',
                  {'desktop': ({'color': gvar(BLACK), 'font-size': size(15), 'line-height': size(150, '%')}, '')})],
            {'desktop': ({'display': s('flex'), 'flex-direction': s('row'), 'align-items': s('center'), 'gap': size(14),
                          'padding': dims(16, 20, 16, 20), 'border-radius': size(14), 'background': bg('#EEF6E8'),
                          'border-width': size(1), 'border-style': s('solid'), 'border-color': color('#C6E2BE')}, ''),
             'tablet': ({'align-self': s('center')}, '')}),
    ], {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'gap': size(20), 'width': size(34, '%')},
                    'flex: 0 0 34%; position: sticky; top: 120px;'),
        'tablet': ({'width': size(100, '%'), 'align-items': s('center')}, 'flex: 1 1 auto; position: static;')})

    grid = el('e-grid', children=cards, widget=False, styles={
        'desktop': ({'grid-template-columns': {'$$type': 'grid-track-size', 'value': {'size': 2, 'unit': 'fr'}},
                     'gap': size(24), 'width': size(100, '%')}, 'flex: 1 1 0; min-width: 0;'),
        'mobile_extra': ({'grid-template-columns': {'$$type': 'grid-track-size', 'value': {'size': 1, 'unit': 'fr'}}, 'gap': size(20)}, '')})
    row = box([left, grid], {'desktop': ({'display': s('flex'), 'flex-direction': s('row'), 'align-items': s('flex-start'),
                                          'gap': size(4, '%'), 'width': size(100, '%')}, ''),
                             'tablet': ({'flex-direction': s('column'), 'align-items': s('stretch'), 'gap': size(30)}, '')})
    sec = box([row, cta], {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'align-items': s('center'),
                                        'gap': size(50), 'background': bg('#F4F8FB')}, ''),
                           'mobile': ({'gap': size(30)}, '')}, kind='e-flexbox', gclasses=('g-a19eb3a',))
    return sec


# ---------------------------------------------------------------- tree helpers
def walk(e, fn):
    fn(e)
    for c in e.get('elements', []):
        walk(c, fn)


def find(root, i):
    out = []
    walk(root, lambda e: out.append(e) if e['id'] == i else None)
    return out[0]


def set_text(e, text):
    st = e['settings']
    t = e.get('widgetType')
    if t == 'e-heading':
        st['title']['value'] = text
    elif t == 'e-paragraph':
        st['paragraph']['value'] = text
    elif t == 'e-button':
        if isinstance(st.get('text'), dict):
            st['text']['value'] = text
        else:
            st['text'] = text
    elif t == 'icon-box':
        st['description_text'] = text
    else:
        raise ValueError(f'set_text: {t} {e["id"]}')


def set_icon_list(e, items):
    old = e['settings']['icon_list']
    new = []
    for k, (text, url) in enumerate(items):
        it = {'text': text, '_id': old[k]['_id'] if k < len(old) else nid()}
        if url:
            it['link'] = {'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}
        new.append(it)
    e['settings']['icon_list'] = new


def add_css(e, css):
    """Append raw CSS to the element's desktop local style variant."""
    for sty in e['styles'].values():
        for v in sty['variants']:
            if v['meta']['breakpoint'] == 'desktop' and v['meta']['state'] is None:
                old = base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
                v['custom_css'] = raw((old + ' ' + css).strip())
                return


def drop_css(e):
    for sty in e['styles'].values():
        for v in sty['variants']:
            v['custom_css'] = None


def set_grid_rows(e, desktop, mobile_extra):
    for sty in e['styles'].values():
        for v in sty['variants']:
            p = v['props']
            if 'grid-template-rows' in p:
                p['grid-template-rows']['value']['size'] = desktop if v['meta']['breakpoint'] == 'desktop' else mobile_extra


def regen_ids(e, seen):
    """New element id; local style ids follow the e-<element id>-<hash> convention."""
    old = e['id']
    new = nid()
    while new in seen:
        new = nid()
    seen.add(new)
    e['id'] = new
    st = e.get('styles')
    if isinstance(st, dict) and st:
        remap = {}
        for sid in list(st):
            nsid = f'e-{new}-{sid.rsplit("-", 1)[-1]}' if sid.startswith(f'e-{old}-') else f'e-{new}-{nid()}'
            remap[sid] = nsid
            body = st.pop(sid)
            body['id'] = nsid
            st[nsid] = body
        cl = e.get('settings', {}).get('classes')
        if isinstance(cl, dict):
            cl['value'] = [remap.get(c, c) for c in cl['value']]
    for c in e.get('elements', []):
        regen_ids(c, seen)


# ---------------------------------------------------------------- build
def build(ca):
    random.seed(411363)
    sections = {e['id']: copy.deepcopy(e) for e in ca}
    page = []

    hero = sections['d8ac86e']
    txt = json.dumps(hero).replace('"image-attachment-id", "value": 376853}', f'"image-attachment-id", "value": {SC_HERO}}}')
    assert str(SC_HERO) in txt, 'hero image id not swapped'
    sections['d8ac86e'] = json.loads(txt.replace('Medical Billing California', 'Medical Billing South Carolina'))

    # texts by California element id
    for sid in ORDER:
        if sid == 'NEW':
            continue
        root = sections[sid]
        for i, t in TEXT.items():
            try:
                set_text(find(root, i), t)
            except IndexError:
                pass
        for i, items in LISTS.items():
            try:
                set_icon_list(find(root, i), items)
            except IndexError:
                pass
        for i, (title, body) in STEPS.items():
            try:
                ib = find(root, i)
                ib['settings']['title_text'] = title
                ib['settings']['description_text'] = body
            except IndexError:
                pass

    # rules: 5 cards -> 7 (cards 1-6 half width, card 7 full width like California's card 5)
    rules = sections['242f0fb']
    grid = find(rules, '2264b96')
    half, full = grid['elements'][3], grid['elements'][4]
    cards = grid['elements'][:4] + [copy.deepcopy(half), copy.deepcopy(half), full]
    for k, (card, (title, body)) in enumerate(zip(cards, RULES), 1):
        ib, p = card['elements']
        ib['settings']['title_text'] = title
        ib['settings']['selected_icon']['value'] = {'url': UPLOADS + ICONS[k][1], 'id': ICONS[k][0]}
        p['settings']['paragraph']['value'] = body
    grid['elements'] = cards
    set_grid_rows(grid, 3, 1)   # last card's row sizes to its content

    # payers: 4 cards -> 5 (Workers' Compensation spans the full row) and move the CTA box out
    payers = sections['d4a5b2b']
    pgrid = find(payers, '3cc985f')
    five = copy.deepcopy(pgrid['elements'][3])
    add_css(five, 'grid-column: 1 / -1;')
    pcards = pgrid['elements'] + [five]
    for card, (title, body) in zip(pcards, PAYERS):
        h, p = card['elements']
        h['settings']['title']['value'] = title
        p['settings']['paragraph']['value'] = body
    pgrid['elements'] = pcards
    set_grid_rows(pgrid, 2, 1)
    cta = payers['elements'].pop()
    assert cta['id'] == 'b27b9a5'

    # cities (California photos stay as placeholders, as on the Alabama page)
    cgrid = find(sections['245b176'], '1293631')
    for card, name in zip(cgrid['elements'], CITIES):
        p = card['elements'][1]
        p['settings']['paragraph']['value'] = name

    # FAQ: 6 -> 7 items
    acc = find(sections['d303d44'], '912f39b')
    conts = acc['elements'] + [copy.deepcopy(acc['elements'][-1])]
    items = []
    for k, (cont, (q, ans)) in enumerate(zip(conts, FAQ)):
        cont['elements'][0]['settings']['paragraph']['value'] = ans
        items.append({'item_title': q, '_id': acc['settings']['items'][k]['_id'] if k < len(acc['settings']['items']) else nid()})
    acc['settings']['items'] = items
    acc['elements'] = conts

    for sid in ORDER:
        page.append(new_section(cta) if sid == 'NEW' else sections[sid])

    out = json.loads(json.dumps(page).replace(UTM_OLD, UTM_NEW))
    seen = set()
    for e in out:
        regen_ids(e, seen)
    return out


def check(out):
    t = json.dumps(out, ensure_ascii=False)
    bad = [w for w in ('California', 'Medi-Cal', 'Texas', ' CA ', 'DMHC', 'Knox', 'IPA', 'cardiology-billing-services/?') if w in t]
    ids = []
    for e in out:
        walk(e, lambda x: ids.append(x['id']))
    assert len(ids) == len(set(ids)), 'duplicate ids'
    return bad, len(ids)


if __name__ == '__main__':
    ca = json.loads(mcp.rest('GET', f'wp/v2/states/{CA_ID}?context=edit&_fields=meta')['meta']['_elementor_data'])
    out = build(ca)
    bad, n = check(out)
    os.makedirs(os.path.join(HERE, '..', 'build'), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, '..', 'build', 'sc_data.json'), 'w'), ensure_ascii=False)
    print('sections', len(out), 'elements', n, 'leftover CA words:', bad)
