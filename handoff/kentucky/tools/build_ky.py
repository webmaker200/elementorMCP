"""Build the Kentucky state page (states post 411410) from the California state page.

Every screenshot in the content doc is a California state-page section; the only new section is the yellow-highlighted
"Kentucky Medicaid Billing Rules We Code To" (design: doc image14).  Copies the California sections in the doc's order,
swaps in the Kentucky copy, adds the new section, regenerates every element id (and the V4 local style ids) and writes
../build/ky_data.json.  Deploy with deploy_ky.py.
"""
import copy, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'south-carolina', 'tools'))
import mcp  # noqa: E402
from build_sc import (ICONS, UPLOADS, POPPINS, WHITE, BLUE, GREEN, a, add_css, bg, box, color, dims, el, find,  # noqa: E402
                      gvar, heading, nid, para, regen_ids, s, set_grid_rows, set_icon_list, set_text, size, walk)

CA_ID = 386954
SLUG = 'medical-billing-kentucky'
MEDIA_JSON = os.path.join(HERE, '..', 'media.json')

ORDER = ['d8ac86e',   # hero + banner form              <- doc image12
         'ad92569',   # KPIs + "Claim More, Faster"      <- image7
         '5b8a846',   # we handle billing                <- image9
         '242f0fb',   # billing laws (5 -> 6 cards)      <- image10
         'b206976',   # two regulators                   <- image5
         'd4a5b2b',   # payer landscape (CTA moved out)  <- image4
         'NEW',       # Kentucky Medicaid Billing Rules  <- image14 (yellow)
         'CTA',       # "Are your claims meeting Kentucky deadlines?" <- image3
         'cbfc466',   # step-by-step                     <- image13
         'e0cbdde',   # certified coding                 <- image11
         'ce0a3b8',   # specialties (unchanged)          <- image2
         '75d5ffd',   # EHR carousel                     <- image6
         '144eabc',   # top medical billing partner      <- image17
         '245b176',   # cities                           <- image15
         '5f5a6aed',  # testimonials shortcode (as on every state page)
         'd303d44',   # FAQ                              <- image16
         'df3702f']   # bottom CTA                       <- image1

TEXT = {
    # hero
    '9e08573': 'Medical Billing Services in Kentucky',
    '5813535': 'Are Kentucky Medicaid MCO denials, slow commercial payments, and stalled credentialing impacting your revenue cycle? Get customized Kentucky medical billing services based on your unique payer mix and specialty. Our billing team works with Kentucky-specific rules, from five Medicaid MCOs and CGS Medicare to the state\'s 30-day prompt-pay law. We help submit clean claims the first time and appeal every denial worth winning. With human oversight and AI-powered tools, MedCare MSO helps you improve ' + a('https://medcaremso.com/services/revenue-cycle-management/', 'revenue cycle') + ' and collect more payments.<br>Kentucky-Compliant RCM | HIPAA-Trained US Team | Live in 14 Days',
    # KPIs
    '2cc357f': 'KPIs That Define Top Medical Billing Services in Kentucky',
    'de8d971': 'Claim More, Faster',
    '07b9858': 'Find out which Kentucky payers are slowing your cash flow, then fix it at the source.',
    # we handle billing
    '64acd81': 'We Handle Billing So You Can Focus on Patient Care',
    '8627165': 'If you run a practice in Kentucky, you’re juggling a lot of payers. On any given day, your schedule might include patients from five different Medicaid MCOs, Medicare patients billed through CGS, people on Kynect Marketplace plans, Humana Medicare Advantage members, and commercial members of Anthem, UnitedHealthcare, and Aetna. Every one of them comes with its own eligibility checks, prior authorization rules, filing windows, and appeal steps.',
    '0c726e0': 'Our certified medical billers and coders take that work off your plate. We verify coverage before the visit, code every encounter to the payer\'s rules, follow every claim until it is paid, and fight the denials that should not have happened. That’s what sets us apart from other medical billing companies in Kentucky: we know how each payer here actually pays.',
    # laws
    'ae498ae': 'Kentucky Billing Laws and Compliance We Handle for You',
    'e6b3a4a': 'Kentucky law gives providers more leverage than most practices use. Here is what our team manages for you so those rules turn into payments:',
    # two regulators
    '3650669': 'Two Regulators, Two Rulebooks: DMS vs. DOI',
    '348eddb': 'In Kentucky, the agency that oversees a patient\'s plan decides how a denied claim gets fought. The Department for Medicaid Services (DMS) oversees the five Medicaid managed care organizations, while fully insured commercial and Kynect marketplace plans fall under the Kentucky Department of Insurance (DOI). Our experts identify the track at the time of eligibility to ensure every appeal goes to the right place.',
    'c9b905e': 'Patient\'s plan - Which regulator oversees it?',
    '9af9766': 'Medicaid managed care',
    '6a56556': 'DMS track',
    '83ef38c': 'Aetna Better Health, Humana Healthy Horizons, Passport by Molina, UnitedHealthcare Community Plan, and WellCare of Kentucky',
    '2564f1c': 'Kentucky Medicaid regulations and each MCO\'s contract rules',
    '999bac4': 'Denials go through the MCO\'s internal appeal, then external independent review, then an administrative hearing',
    'f7ddde8': 'Commercial / Kynect',
    'a2cbd18': 'DOI track',
    'eb7c978': 'Fully insured commercial and kynect plans such as Anthem, UnitedHealthcare, Aetna, Cigna, and Ambetter from WellCare of Kentucky',
    'c1d368f': 'Kentucky Insurance Code rules',
    '304b7b7': 'Disputes go through the plan\'s appeal process; prompt-pay complaints go to the Kentucky Department of Insurance',
    'ca0a010': 'Same 30-day clean-claim clock on both tracks',
    '2fdd08c': 'Self-funded employer plans and Medicare Advantage follow federal rules instead. We identify the regulator at eligibility, so every appeal goes to the right place.',
    # payers
    'c86391c': 'Billing Services for Kentucky\'s Payer Landscape',
    '29080ac': 'Our billers and coders are knowledgeable about the unique payer mix in Kentucky. We work with:',
    # CTA
    '3c78265': 'Are your claims meeting Kentucky deadlines?',
    '65d5700': 'We check your claims against the deadlines that matter in Kentucky, from the 30-day prompt-pay clock to the 60-day external review window, and show you where revenue is slipping.',
    # steps
    '6f0f65f': 'Step-by-Step Medical Billing Process',
    '55374bd': 'Our medical billing services in Kentucky follow a more organized method so that errors are minimized, claims are paid accurately, and providers get their payments on time. Every step is built around Kentucky\'s payers, from five Medicaid MCOs and CGS Medicare to commercial plans, with deadlines tracked at every stage of the revenue cycle.',
    # coding
    'db3ea26': 'Certified Coding Expertise Kentucky Practices Can Trust',
    '17443e8': 'Precision coding decides whether a Kentucky claim pays on the first pass. As a medical billing company in Kentucky, we have an accomplished team of coders certified by AAPC or AHIMA with rich experience in CPT, ICD-10-CM, and HCPCS coding protocols.',
    '466b5ad': 'Our certified coding staff review every claim against the rules Kentucky payers apply, from Medicaid MCO payment policies and CGS Medicare local coverage determinations to NCCI edits and commercial modifier requirements. Whether you need medical billing for small practices in Kentucky or are weighing medical billing companies in Louisville, KY for a multi-provider group, our coders code every unit to cut avoidable denials.',
    'bf95439': 'Why certified coders matter for Kentucky practices:',
    '6f5e5e7': 'Request a Consultation',
    # EHR
    '9f42ec6': 'EHR-Compatible Billing Tailored for Kentucky Providers',
    # top partner
    'd8dfd3d': 'Top Medical Billing Partner in Kentucky, Customized RCM for Every Specialty',
    'a6d750d': 'Are you looking for Kentucky medical billing services that understand your payer mix? Look no further! Our medical billing and coding services are customized to your specialty, your Medicaid MCO contracts, and your EHR. From ' + a('https://medcaremso.com/services/medical-billing-for-small-practices/', 'medical billing for small practices in Kentucky') + ' to multi-provider groups and rural health clinics in the east, our custom-tailored RCM helps you achieve maximum revenue-generating results.',
    # cities
    '226f454': 'Serving Healthcare Providers Across Kentucky',
    '52b0c66': 'Our medical billing company serves healthcare providers across Kentucky, with billing services in Louisville, Lexington, Bowling Green, Owensboro, Covington, Georgetown, Richmond, Florence, Elizabethtown, and Paducah. If you’re comparing medical billing companies in Louisville, KY, we help independent practices collect as effectively as Norton, Baptist Health, and UofL Health. From Northern Kentucky to the Appalachian region, we offer customized billing solutions based on Kentucky’s rules, like the 30-day prompt-pay law and its five Medicaid MCOs.',
    # FAQ
    '8c643c4': 'FAQs',
    # bottom CTA
    '4391013': 'Comparing Medical Billing Companies in Kentucky?',
    '4335f5a': 'We help you get paid within Kentucky\'s deadlines and take Medicaid MCO complexity off your plate. Request a free billing audit and find out where your revenue is leaking.',
}

LISTS = {
    '5c173ee': [('Coders certified by AAPC and AHIMA', None),
                ('Kentucky Medicaid MCO and CGS Medicare coding expertise', None),
                ('Accurate CPT, ICD-10-CM, and HCPCS code assignment', None),
                ('Fewer coding errors, denials, and revenue loss', None),
                ('Audit-ready documentation and quality control', None)],
    'ae7a75b': [('Solo Physician and Small Practices', None), ('Multi-Provider Medical Groups', None),
                ('Rural Health Clinics & FQHCs', None), ('Behavioral Health & Substance Use Treatment Providers', None),
                ('Hospitals & Ambulatory Surgery Centers', None), ('Growing and Enterprise Healthcare Networks', None)],
}

LAWS = [
    ('We Hold Payers to Kentucky\'s 30-Day Prompt-Pay Clock',
     'Under KRS 304.17A-702, insurers must pay a clean claim, or send notice denying or contesting it, within 30 calendar days. When they pay late, KRS 304.17A-730 adds interest at 12%, 18%, or 21% a year. We track every clean claim against the clock, flag payers that miss it, and make sure the interest owed to you shows up on the remittance.'),
    ('We File Every Medicaid MCO Claim Inside the 365-Day Window',
     'Kentucky Medicaid MCOs such as Humana Healthy Horizons and Passport generally allow 365 days from the date of service. We confirm each patient\'s MCO assignment at check-in, route every claim to the right plan the first time, and send corrected claims well before the deadline.'),
    ('We Take Denied Medicaid Claims to External Independent Review',
     'When an MCO upholds a denial on internal appeal, many practices stop there. KRS 205.646 gives you the right to an external independent third-party review, and 907 KAR 17:035 gives you 60 calendar days from the MCO’s final decision to request it. When one MCO policy is behind several denials, those claims can go into a single review. We build the case file and pursue it whenever the claim is worth it.'),
    ('We Get Telehealth Paid at In-Person Rates',
     'KRS 304.17A-138 requires plans to pay covered telehealth at the same rate as the in-person service unless your contract sets a lower rate. We check place-of-service codes and modifiers, confirm licensure, and challenge payments that fall below parity.'),
    ('We\'re Preparing You for Prior Authorization Gold Carding',
     'HB 176 requires state-regulated plans, including kynect plans, to offer prior authorization exemptions on contracts issued or renewed on or after January 1, 2028. Plans can’t require an approval rate above 93% to qualify, and Medicaid MCOs are excluded. We submit complete requests and track your approval rate by service and payer now.'),
    ('HIPAA Safeguards and Kentucky’s New Privacy Law',
     'The Kentucky Consumer Data Protection Act took effect January 1, 2026, and exempts PHI handled under HIPAA, so HIPAA remains the standard your billing data falls under. Our HIPAA-trained team works under a business associate agreement with role-based, logged access, backed by HITRUST, SOC 2 Type II, and PCI DSS controls.'),
]

PAYERS = [
    ('Kentucky Medicaid Managed Care',
     'Most Kentucky Medicaid members are enrolled in one of five MCOs: Aetna Better Health, Humana Healthy Horizons, Passport by Molina, UnitedHealthcare Community Plan, and WellCare of Kentucky. Each plan has its own portal, prior authorization rules, and appeal windows. We manage all five to verify and bill accurately.'),
    ('MCO Assignment and the SKY Program',
     'In Kentucky, the paying plan depends on the MCO a patient is assigned to today. SKY members in foster care are covered only by Aetna Better Health, and Anthem left Medicaid managed care in 2025. Wrong-plan claims are a common denial reason, so we confirm assignment at eligibility.'),
    ('Major Commercial Payers',
     'We help you get reimbursed by major commercial and marketplace payers like Anthem Blue Cross and Blue Shield, UnitedHealthcare, Aetna, Cigna, and kynect plans such as Ambetter from WellCare of Kentucky. Our team tracks each payer’s fee schedule, filing limits, and Kentucky’s 30-day prompt-pay rule so underpayments and late payments get caught.'),
    ('Medicare',
     'We help you receive payments for Medicare Part A and Part B claims through CGS Administrators, Kentucky\'s Medicare Administrative Contractor (MAC) for Jurisdiction 15, with LCD-aware coding for coverage rules in Kentucky. We also file claims within Medicare\'s 12-month limit and handle DME claims under CGS Jurisdiction B. We also bill Medicare Advantage plans, including Humana’s, under each plan’s own authorization and appeal rules.'),
]

STEPS = {
    '3fae60e': ('Patient Registration and Verification', 'Before each visit, we collect the patient’s details, verify insurance eligibility, and confirm whether one of Kentucky’s five Medicaid MCOs or a commercial plan covers them. That heads off denials.'),
    '1a068db': ('Coding and Documentation Review', 'Our certified coders read each clinical record and assign CPT, ICD-10-CM, and HCPCS codes fitting each MCO’s payment policies and CGS Medicare local coverage rules. Kentucky claims get no shortcuts.'),
    '9595d87': ('Claim Submission', 'We scrub every claim against payer-specific edits and send it to the right place, whether that’s an MCO, CGS, or a commercial plan. Clean claims start Kentucky’s 30-day prompt-pay clock.'),
    '66512a0': ('Payment Posting', 'Every payment and adjustment gets posted and reconciled against your payer contracts. Underpayments and skipped prompt-pay interest get flagged right away, so you always know where your practice finances stand.'),
    '709d64a': ('Denial Management and A/R Follow-Up', 'Our A/R experts find each denial’s root cause, fix it, and appeal before the payer deadline. If a Medicaid MCO still won’t budge, we take it to external independent review.'),
    '56a301a': ('Reporting & Optimization', 'Reports track collections, A/R aging, and denial trends by payer and MCO. When a problem keeps returning, we fix it at the front end and tighten your Kentucky medical billing.'),
}

CITIES = ['Louisville', 'Lexington', 'Bowling Green', 'Owensboro', 'Covington',
          'Georgetown', 'Richmond', 'Florence', 'Elizabethtown', 'Paducah']

FAQ = [
    ('What is the timely filing limit for Kentucky Medicaid claims?',
     'You\'ve got 365 days from the date of service with most Kentucky Medicaid MCOs, Humana Healthy Horizons and Passport by Molina among them. So a visit on January 15, 2026 needs to reach the plan by January 15, 2027. Retro eligibility is a different story. Those windows run shorter, and that\'s where practices tend to get caught.'),
    ('How quickly do Kentucky insurers have to pay claims?',
     'Thirty calendar days. Kentucky\'s prompt-pay law, KRS 304.17A-702, gives insurers that long to pay a clean claim or tell you why they won\'t. Miss it, and interest kicks in at 12%, 18%, or 21% a year, depending on how late they are. Most practices never check whether that interest got paid. We do.'),
    ('Does Kentucky’s prompt-pay law apply to self-funded employer plans?',
     'No. Self-funded employer plans fall under federal ERISA rules, not the Kentucky Insurance Code, so the 30-day clock and KRS 304.17A-730 interest don’t apply to them. The plan’s own terms and federal claims rules govern payment and appeals instead. We flag self-funded plans at eligibility so nobody waits on interest that isn’t owed.'),
    ('How long does it take to switch to MedCare MSO?',
     'Most practices are live in about two weeks. Appeals and credentialing are included in the fee, so there’s no extra charge when we enroll you with an MCO or take a denial to external review.'),
    ('Do you work with Kentucky Medicaid managed care plans?',
     'Yes, all five: Aetna Better Health, Humana Healthy Horizons, Passport by Molina, UnitedHealthcare Community Plan, and WellCare of Kentucky. We handle fee-for-service Medicaid too. Each plan has its own portal, prior auth rules, and appeal deadlines, and keeping them straight is a big part of what we do for you.'),
    ('Do we have to enroll with Kentucky Medicaid if we’re already contracted with an MCO?',
     'Yes. An MCO contract is a network agreement; Kentucky Medicaid enrollment is a separate application through KY MPPA, and it is the Department’s enrollment that makes a provider a Kentucky Medicaid provider. Processing can take up to 60 days, requested updates are due within 35 calendar days, and a provider number with no claims in twelve months can be terminated.'),
    ('How much do your medical billing services in Kentucky cost?',
     'We take a percentage of what we collect for you. There\'s no setup fee and nothing hidden. Your rate depends on claim volume and specialty, so the fastest way to a real number is a short call with our team.'),
]

# New section: (number, category, code pill, title, what it requires (html), how we bill to it)
RULES = [
    ('01', 'Timely filing', '907 KAR 1:673', 'Twelve Months to File, on Fee-for-Service Too',
     'Under ' + a('https://www.law.cornell.edu/regulations/kentucky/907-KAR-1-673', '907 KAR 1:673') + ', a Kentucky Medicaid claim must be submitted within twelve months of the date of service, and the Department pays only when the claim is complete, not under medical-necessity review, and every required report has been filed. The MCOs’ 365-day windows follow the same clock.',
     'We work the filing date from the visit, not from the first rejection.'),
    ('02', 'Enrollment', 'KY MPPA · 907 KAR 1:671', 'Enrolled Through KY MPPA, and Kept Current',
     'Every Kentucky Medicaid provider enrolls, revalidates and updates electronically through the ' + a('https://chfs.ky.gov/agencies/dms/provider/Pages/providerenroll.aspx', 'Kentucky Medicaid Partner Portal Application') + '; paper is no longer accepted and processing can take up to 60 days. Under 907 KAR 1:671 a provider who does not return a requested update within 35 calendar days, or who bills no claim in twelve consecutive months, can be terminated.',
     'We file the enrollment before the first MCO contract is signed and keep the record current.'),
    ('03', 'Telehealth', '907 KAR 3:170', 'Telehealth Billed the Way DMS Defines It',
     a('https://www.law.cornell.edu/regulations/kentucky/907-KAR-3-170', '907 KAR 3:170') + ' pays a Medicaid telehealth service at no less than 100 percent of the in-person rate, lets an MCO negotiate a different rate by contract, pays audio-only care at the lower of the two rates where a telephonic code exists, and requires the record to show the service was delivered by telehealth within 48 hours.',
     'We mark place of service as the Department designates and check every telehealth remittance against the in-person rate.'),
    ('04', 'Coding', 'CGS LCDs · NCCI', 'Coded to CGS and NCCI, Not to Habit',
     'Kentucky Medicare claims are judged against CGS Administrators’ local coverage determinations for Jurisdiction 15, and Kentucky Medicaid applies the National Correct Coding Initiative edits to professional claims. A modifier that clears an edit without a reason in the note pays now and is recouped later.',
     'We code to the LCD and the edit before submission, not to the last claim that happened to pay.'),
]

NAVY, INK, MUTED, LINE = '#0F2D4E', '#13294B', '#5B6B7F', '#D9E4EF'
MONO = 'font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;'
GRID = 'display: grid; grid-template-columns: 90px minmax(0, 1.05fr) minmax(0, 2fr) minmax(0, 1.3fr); column-gap: 32px;'


def label(text, color_css, extra=''):
    return para(text, {'desktop': ({'font-family': POPPINS, 'font-weight': s('600'), 'font-size': size(12)},
                                   f'color: {color_css}; text-transform: uppercase; letter-spacing: .12em; {extra}')}, gclasses=())


def new_section():
    """Kentucky Medicaid Billing Rules We Code To (doc image14)."""
    head = box([
        box([
            label('Medicaid Billing Rules', '#7EB13E'),
            heading('Kentucky Medicaid Billing Rules We Code To', 'h2',
                    {'desktop': ({'color': gvar(WHITE), 'line-height': size(120, '%')}, ''),
                     'tablet': ({'text-align': s('center')}, '')}, gclasses=('g-0a6ebf3',)),
            para('Kentucky’s insurance laws decide when a commercial payer owes you. The Department for Medicaid Services’ own regulations decide whether a Medicaid claim is payable at all. These four are the ones that fail most often.',
                 {'desktop': ({'line-height': size(170, '%')}, 'color: rgba(255,255,255,.82);'),
                  'tablet': ({'text-align': s('center')}, '')}),
        ], {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'gap': size(18), 'width': size(60, '%')}, ''),
            'tablet': ({'width': size(100, '%'), 'align-items': s('center')}, '')}),
        box([
            para('The regulation', {'desktop': ({'font-size': size(15)}, 'color: rgba(255,255,255,.85); display: inline-flex; align-items: center; gap: 10px; &::before { content: ""; width: 10px; height: 10px; border-radius: 50%; background: #2E8BEA; }')}, gclasses=('g-6181ecc',)),
            para('What we do with it', {'desktop': ({'font-size': size(15)}, 'color: rgba(255,255,255,.85); display: inline-flex; align-items: center; gap: 10px; &::before { content: ""; width: 10px; height: 10px; border-radius: 50%; background: #7EB13E; }')}, gclasses=('g-6181ecc',)),
        ], {'desktop': ({'display': s('flex'), 'flex-direction': s('row'), 'gap': size(28), 'align-items': s('center')}, 'flex-wrap: wrap;'),
            'tablet': ({'justify-content': s('center')}, '')}),
    ], {'desktop': ({'display': s('flex'), 'flex-direction': s('row'), 'justify-content': s('space-between'), 'align-items': s('flex-end'),
                     'gap': size(30), 'width': size(100, '%')}, ''),
        'tablet': ({'flex-direction': s('column'), 'align-items': s('center')}, '')})

    cols = box([para('', {'desktop': ({}, '')}, gclasses=()), label('Rule', '#9FB3C8'), label('What it requires', '#9FB3C8'),
                label('How we bill to it', '#9FB3C8')],
               {'desktop': ({'width': size(100, '%'), 'padding': dims(0, 40, 0, 40)}, GRID + ' margin-bottom: -16px;'),
                'tablet': ({}, 'display: none;')})

    rows = []
    for num, cat, code, title, body, how in RULES:
        rows.append(box([
            para(num, {'desktop': ({'font-size': size(32), 'line-height': size(110, '%')}, MONO + ' color: #1F6FB8;'),
                       'tablet': ({'font-size': size(26)}, '')}, gclasses=()),
            box([label(cat, MUTED),
                 para(code, {'desktop': ({'font-size': size(14)}, MONO + f' color: {INK}; background: #EEF3F8; border: 1px solid {LINE}; border-radius: 8px; padding: 6px 12px; width: fit-content;')}, gclasses=())],
                {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'gap': size(10)}, 'padding-top: 6px;')}),
            box([heading(title, 'h3', {'desktop': ({'font-family': POPPINS, 'font-weight': s('600'), 'font-size': size(1.35, 'rem'),
                                                    'line-height': size(130, '%')}, f'color: {INK};'),
                                       'mobile': ({'font-size': size(1.15, 'rem')}, '')}),
                 para(body, {'desktop': ({'line-height': size(170, '%')}, f'color: {MUTED};')})],
                {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'gap': size(12)}, ''),
                 'tablet': ({}, 'grid-column: 1 / -1;')}),
            box([label('How we bill to it', '#2E7D32'),
                 para(how, {'desktop': ({'line-height': size(160, '%')}, f'color: {INK};')})],
                {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'gap': size(10), 'padding': dims(20, 22, 20, 22),
                              'border-radius': size(14), 'background': bg('#EAF5EC')},
                             'border: 1px solid #CFE6D3; align-self: start;'),
                 'tablet': ({}, 'grid-column: 1 / -1;')}),
        ], {'desktop': ({'width': size(100, '%'), 'padding': dims(40, 40, 40, 40), 'border-radius': size(20), 'background': bg('#FFFFFF')},
                        GRID + ' row-gap: 20px;'),
            'tablet': ({'padding': dims(30, 28, 30, 28)}, 'grid-template-columns: 70px minmax(0, 1fr);'),
            'mobile': ({'padding': dims(24, 20, 24, 20)}, 'grid-template-columns: 56px minmax(0, 1fr); column-gap: 12px;')}))

    return box([head, cols] + rows,
               {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'align-items': s('center'), 'gap': size(20),
                             'background': bg(NAVY)}, ''),
                'mobile': ({'gap': size(16)}, '')}, kind='e-flexbox', gclasses=('g-a19eb3a',))


def cta_section(cta):
    return box([cta], {'desktop': ({'display': s('flex'), 'flex-direction': s('column'), 'align-items': s('center'),
                                    'background': bg('#FFFFFF')}, '')}, kind='e-flexbox', gclasses=('g-a19eb3a',))


def build(ca):
    random.seed(411410)
    secs = {e['id']: copy.deepcopy(e) for e in ca}
    media = json.load(open(MEDIA_JSON)) if os.path.exists(MEDIA_JSON) else {}

    hero = json.dumps(secs['d8ac86e'])
    if media.get('hero'):
        hero = hero.replace('"image-attachment-id", "value": 376853}', f'"image-attachment-id", "value": {media["hero"]["id"]}}}')
    secs['d8ac86e'] = json.loads(hero.replace('Medical Billing California', 'Medical Billing Kentucky'))

    for sid in ORDER:
        if sid in ('NEW', 'CTA'):
            continue
        root = secs[sid]
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

    # laws: 5 cards -> 6, all half width (California's 5th card spans the row)
    grid = find(secs['242f0fb'], '2264b96')
    half = grid['elements'][3]
    cards = grid['elements'][:4] + [copy.deepcopy(half), copy.deepcopy(half)]
    for k, (card, (title, body)) in enumerate(zip(cards, LAWS), 1):
        ib, p = card['elements']
        ib['settings']['title_text'] = title
        ib['settings']['selected_icon']['value'] = {'url': UPLOADS + ICONS[k][1], 'id': ICONS[k][0]}
        p['settings']['paragraph']['value'] = body
    grid['elements'] = cards
    set_grid_rows(grid, 3, 1)

    # payers: 4 cards; claims-review CTA moves below the new section
    payers = secs['d4a5b2b']
    for card, (title, body) in zip(find(payers, '3cc985f')['elements'], PAYERS):
        h, p = card['elements']
        h['settings']['title']['value'] = title
        p['settings']['paragraph']['value'] = body
    cta = payers['elements'].pop()
    assert cta['id'] == 'b27b9a5'

    # cities (California photos until Kentucky photos are in media.json as "<City>-KY.webp")
    cgrid = find(secs['245b176'], '1293631')
    for card, name in zip(cgrid['elements'], CITIES):
        img, p = card['elements']
        p['settings']['paragraph']['value'] = name
        f = name.replace(' ', '-') + '-KY.webp'
        if f in media:
            img['settings']['image']['value']['src']['value']['id']['value'] = media[f]['id']

    # FAQ: 6 -> 7
    acc = find(secs['d303d44'], '912f39b')
    conts = acc['elements'] + [copy.deepcopy(acc['elements'][-1])]
    items = []
    for k, (cont, (q, ans)) in enumerate(zip(conts, FAQ)):
        cont['elements'][0]['settings']['paragraph']['value'] = ans
        items.append({'item_title': q, '_id': acc['settings']['items'][k]['_id'] if k < len(acc['settings']['items']) else nid()})
    acc['settings']['items'] = items
    acc['elements'] = conts

    page = [new_section() if sid == 'NEW' else cta_section(cta) if sid == 'CTA' else secs[sid] for sid in ORDER]
    out = json.loads(json.dumps(page).replace('utm_source=medical-billing-california', 'utm_source=' + SLUG))
    seen = set()
    for e in out:
        regen_ids(e, seen)
    return out


def check(out):
    t = json.dumps(out, ensure_ascii=False)
    words = ['California', 'Medi-Cal', 'Texas', ' CA ', 'DMHC', 'Knox', 'IPA', 'CalAIM', 'Behavioral Health Practice']
    ids = []
    for e in out:
        walk(e, lambda x: ids.append(x['id']))
    assert len(ids) == len(set(ids)), 'duplicate ids'
    return [w for w in words if w in t], len(ids)


if __name__ == '__main__':
    ca = json.loads(mcp.rest('GET', f'wp/v2/states/{CA_ID}?context=edit&_fields=meta')['meta']['_elementor_data'])
    out = build(ca)
    bad, n = check(out)
    os.makedirs(os.path.join(HERE, '..', 'build'), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, '..', 'build', 'ky_data.json'), 'w'), ensure_ascii=False)
    print('sections', len(out), 'elements', n, 'leftover California words:', bad)
