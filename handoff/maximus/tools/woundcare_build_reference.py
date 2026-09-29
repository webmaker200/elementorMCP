"""Builds the Wound Care AI specialty page from reference MedCare sections.

Each section reuses the classes + local CSS of an existing reference element
(looked up by its element id in idx.json) and swaps in the Google Doc content.
"""
import json, re, sys
import mcp

IDX = json.load(open('idx.json'))
UP = 'https://medcaredemo.online/medcare/wp-content/uploads/'
M = 'https://medcaremso.com/'


def ref(eid):
    n = IDX[eid]
    s = n.get('settings') or {}
    cls = [c for c in s.get('classes', []) if not c.startswith('e-')]
    st = n.get('styles')
    css = st.get('css', '') if isinstance(st, dict) else ''
    return cls, css


class B:
    def __init__(self):
        self.cfg, self.style, self.classes = {}, {}, {}
        self.n = 0

    def el(self, tag, cid, kids='', like=None, cfg=None, css=None, add_css='', cls=None, sub=None):
        """like: reference element id to copy classes/css from.
        sub: list of (old, new) replacements applied to the copied css."""
        assert cid not in self.style and cid not in self.cfg, cid
        c, s = ref(like) if like else ([], '')
        if cls is not None:
            c = cls
        if css is not None:
            s = css
        for a, b in (sub or []):
            assert a in s, (cid, a)
            s = s.replace(a, b)
        if add_css:
            s = (s + '\n' + add_css).strip()
        if cfg:
            self.cfg[cid] = cfg
        if s:
            self.style[cid] = s
        if c:
            self.classes[cid] = c
        return f'<{tag} configuration-id="{cid}">{kids}</{tag}>'

    def uid(self, p):
        self.n += 1
        return f'{p}{self.n}'


def link(url, text):
    return f'<a href="{url}">{text}</a>'


def img(aid, url, w, h, alt):
    return {'image': {'src': {'id': aid, 'alt': alt}, 'size': 'full'}}


# ---------- shared bits ----------
CHECK = UP + '2024/05/check-icon-green.svg'


def table(b, p, head, rows, cols, mobile_min='700px'):
    """Grid table styled like the reference html table (General Surgery CPT table)."""
    cells = ''
    for i, t in enumerate(head):
        cells += b.el('e-paragraph', f'{p}h{i}', cfg={'paragraph': t},
                      css='padding: 12px 14px; background-color: var(--DeepSkyBlue); color: var(--PureWhite); '
                          'font-family: var(--Poppins); font-weight: 600; font-size: 16px; text-align: start;')
    for r, row in enumerate(rows):
        bg = 'var(--Lightgray)' if r % 2 == 0 else '#A1DDFB66'
        for i, t in enumerate(row):
            cells += b.el('e-paragraph', f'{p}r{r}c{i}', cfg={'paragraph': t},
                          css=f'padding: 14px; background-color: {bg}; color: var(--DeepSkyBlue); '
                              'font-family: var(--Poppins); font-weight: 400; font-size: 15px; text-align: start;'
                              '\n@media(--mobile) { font-size: 14px; }')
    grid = b.el('e-grid', f'{p}grid', cells,
                css=f'padding: 0px; column-gap: 0px; row-gap: 0px; grid-template-columns: {cols}; '
                    'grid-template-rows: none !important; grid-auto-rows: auto !important;'
                    f'\n@media(--mobile) {{ grid-template-columns: {cols}; min-width: {mobile_min}; }}')
    return b.el('e-div-block', f'{p}wrap', grid,
                css='width: 100%; padding: 0px; margin-block-start: 30px; border-radius: 10px; border-width: 1px; '
                    'border-color: var(--DeepSkyBlue); border-style: solid; overflow: hidden;'
                    '\n@media(--mobile) { overflow-x: auto; }')


SVGS = {x['id']: x for x in json.load(open('svgs.json'))}


def card_head(b, p, svg_id, svg_url, title, title_css, icon_size):
    # e-image rather than e-svg: inline SVGs share internal class names and recolor each other
    icon = b.el('e-image', f'{p}ic', cfg={'image': {'src': {'id': svg_id, 'alt': ''}, 'size': 'full'}},
                css=f'width: {icon_size}; height: {icon_size}; flex-shrink: 0;')
    h = b.el('e-heading', f'{p}t', cfg={'tag': 'h3', 'title': title}, css=title_css)
    return b.el('e-flexbox', f'{p}hd', icon + h,
                css='padding: 0px; flex-direction: row; gap: 15px; align-items: center;'
                    '\n@media(--mobile) { gap: 10px; }')


# ================= SECTIONS =================

def s0_hero(b):
    kids = b.el('e-heading', 'h1', like='1b3f530',
                cfg={'tag': 'h1', 'title': 'Avoid Revenue Losses with Our Wound Care Billing Services'})
    kids += b.el('e-paragraph', 'hero-p', like='21766b9', cfg={'paragraph': (
        'Our specialized wound care billing services are designed to reduce administrative burdens, minimize errors, '
        'and ensure timely reimbursements. Whether you run a small practice or a large healthcare facility, our expert '
        'team has a proven track record of achieving 96% collection ratios and improving cash flow.')})
    kids += b.el('e-button', 'hero-btn', like='8703945', cfg={'text': 'Schedule Consultation'})
    return b.el('e-flexbox', 'hero', kids, like='e2c125d',
                sub=[('2025/01/urgent-care-banner.webp', '2024/05/wound-care-banner.webp')])


def s1_complex(b):
    txt = ('Outpatient wound care coding is complex for several reasons. One is that it may take place in different kinds '
           'of facilities, even for a single patient treating the same wound, such as when a hospital patient is released '
           'and wound care continues at an outpatient center. Each encounter must be billed correctly, including the code '
           'details indicating which location was used. This complexity is further compounded when wound care involves '
           'specialties such as ' + link(M + 'specialties/general-surgery-billing/', 'general surgery medical billing') +
           ', ' + link(M + 'specialties/internal-medicine-billing-services/', 'internal medicine medical billing') +
           ', and ' + link(M + 'specialties/infectious-disease-billing-services/', 'infectious disease billing services') + '.')
    left = b.el('e-div-block', 'cx-l',
                b.el('e-heading', 'cx-h2', like='0b837a9', cfg={'tag': 'h2', 'title': 'Wound Care Is Complex for Several Reasons'}) +
                b.el('e-paragraph', 'cx-p', like='dd393b0', cfg={'paragraph': txt}),
                like='b89a739')
    right = b.el('e-div-block', 'cx-r',
                 b.el('e-image', 'cx-img', like='d263916', cfg=img(380181, '2024/05/wound-care-reasons.svg', 722, 622,
                                                                'Wound care billing complexity illustration')),
                 like='2c44de0')
    return b.el('e-flexbox', 'cx', left + right, like='3f065fd')


def s2_wound_types(b):
    head = ['Wound type', 'Diagnosis pathway', 'Common procedure codes', 'Coverage rule that decides payment']
    rows = [
        ['Diabetic foot ulcer (DFU)', 'E11.621 with L97.4x/L97.5x site code', 'Debridement 97597/11042–11044; skin substitute application 15271–15278', 'Wagner grade, offloading documented, failed standard care before CTPs'],
        ['Venous leg ulcer (VLU)', 'I83.0x or I87.2 with L97.x', 'Compression 29580/29581; debridement; CTPs', 'Compression therapy documented before advanced modalities'],
        ['Arterial / ischemic ulcer', 'I70.23x/I70.24x', 'Debridement; vascular referral', 'Perfusion assessment (ABI) documented; CTPs often not covered without revascularization'],
        ['Pressure injury', 'L89.x with NPIAP stage digit', 'Debridement 11042–11044 by depth; NPWT 97605–97608', 'Stage in the diagnosis code must match the note'],
        ['Surgical wound dehiscence', 'T81.31XA / T81.32XA', 'Debridement; NPWT', "Linked to the original procedure's global period"],
        ['Traumatic wound', 'S-codes with 7th character', 'Debridement; repair codes', 'Encounter character (initial/subsequent) drives the code'],
        ['Burn', 'T31.x by TBSA + site codes', '16020–16030 by size', 'Burn dressings/debridement coded by percentage of body surface'],
        ['Radiation wound', 'L59.x', 'Debridement; wound care management', 'Cancer treatment history documented'],
    ]
    kids = b.el('e-heading', 'wt-h2', like='bf814e8', cfg={'tag': 'h2', 'title': 'Wound Types We Bill and Their Code Pathways'})
    kids += b.el('e-paragraph', 'wt-p', like='e293c52', cfg={'paragraph': (
        'Our wound care medical billing services help you achieve accurate reimbursements and reduce the chances of claim '
        'denials that occur due to incorrect codes. Here are some code pathways for wound care specialties. Each wound type '
        'follows a different code pathway and a different coverage rule.')})
    kids += table(b, 'wt', head, rows, '18% 22% 30% 30%', '760px')
    # same section shell as the General Surgery CPT table, slightly less side padding for a 4-column table
    return b.el('e-flexbox', 'wt', kids, like='fc40c7a',
                sub=[('padding-inline-start: 15%; padding-inline-end: 15%;', 'padding-inline-start: 10%; padding-inline-end: 10%;')],
                cls=['parent-container'],
                add_css='@media(--tablet_extra) { padding-inline-start: 5%; padding-inline-end: 5%; }\n'
                        '@media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }')


def s3_measure(b):
    kids = b.el('e-heading', 'ms-h2', like='af352e2', cfg={'tag': 'h2', 'title': 'Wound Care Medical Billing Services: Measurement and Tissue'})
    kids += b.el('e-paragraph', 'ms-p', like='252f275', cfg={'paragraph': (
        'There are two things that decide which code to pick for almost all the wound care procedures. The first one is the '
        'size of the wound, how big it is. The second one is how deep the debridement went. Our wound care billing services '
        'start with these two things before we look into anything else on the claim before submission.')})
    col = b.el('e-heading', 'ms-h3a', like='e424be5', cfg={'tag': 'h3', 'title': 'Measurement'})
    col += b.el('e-paragraph', 'ms-pa', like='40448df', cfg={'paragraph': (
        'Three dimensions tell the details about the wound and they are length, width, and depth. How are these recorded? '
        'These dimensions are recorded in centimeters and the surface area is recorded in square centimeters. The values of '
        'undermining and tunneling need to be measured separately from the wound bed itself. At the time of service, this '
        'measurement is taken and recorded accurately. Our wound care billing experts record these values separately to avoid '
        'the audit triggers. Surface area sets the count of the unit. The base debridement codes cover the first 20 cm², and '
        'each additional 20 cm² is an add-on unit.')})
    col += b.el('e-heading', 'ms-h3b', like='acc056e', cfg={'tag': 'h3', 'title': 'Tissue Type'})
    col += b.el('e-paragraph', 'ms-pb', like='6bfbc1f', cfg={'paragraph': (
        'The note tells what was removed during the procedure, slough, eschar, fibrin, biofilm, devitalized or necrotic tissue, '
        'granulation, epithelial tissue. For surgical debridement, the note says what was the deepest layer reached: '
        'subcutaneous tissue, fascia, muscle, or bone. The code family is based on the deepest tissue removed in the procedure.')})
    row = b.el('e-div-block', 'ms-row',
               b.el('e-div-block', 'ms-l', col, like='975b8e6') +
               b.el('e-div-block', 'ms-r', b.el('e-image', 'ms-img', like='f5a1522',
                                                 cfg=img(385311, '2024/11/radiology-NCCI.svg', 721, 622, 'Wound measurement and tissue coding illustration')),
                    like='52d4553', add_css='@media(--mobile_extra) { display: flex; justify-content: center; }'),
               like='91f0a1b')
    kids += row
    kids += table(b, 'db', ['Debridement type', 'Code', 'Key billing requirement'], [
        ['Selective (removing devitalized tissue without cutting viable tissue)', '97597 first 20 cm² · 97598 each additional 20 cm²', 'Surface area in cm², tissue type removed, instrument used'],
        ['Surgical, subcutaneous tissue', '11042 first 20 cm² · 11045 each additional 20 cm²', 'Note must state subcutaneous tissue was removed'],
        ['Surgical, muscle and/or fascia', '11043 first 20 cm² · 11046 each additional 20 cm²', 'Operative-level documentation of the layer reached'],
        ['Surgical, bone', '11044 first 20 cm² · 11047 each additional 20 cm²', 'Imaging or direct visualization of bone documented'],
    ], '30% 35% 35%', '640px')
    kids += b.el('e-heading', 'ms-h3c', like='acc056e', cfg={'tag': 'h3', 'title': 'Staging Systems in the Diagnosis'},
                 add_css='width: 100%; margin-block-start: 20px;\n@media(--mobile) { text-align: center; }')
    kids += b.el('e-paragraph', 'ms-pc', like='40448df', cfg={'paragraph': (
        'Under the NPIAP (National Pressure Injury Advisory Panel) system, pressure injuries are staged 1 through 4 based on '
        'their rank on a standard scale. There are two further categories: unstageable, where dead tissue covers the base so '
        'the depth cannot be seen, and deep tissue pressure injury, where the damage sits under skin that looks intact. The '
        'ICD-10 code for a pressure injury is L89, and the stage in the note must match the stage character in that code. '
        'Wagner scale (0 to 5) grades the diabetic foot ulcers or the University of Texas classification is used for them. As '
        'a wound care billing company, our experts check the notes to maintain accuracy.')},
                 add_css='width: 100%;\n@media(--mobile) { text-align: center; }')
    return b.el('e-flexbox', 'ms', kids, like='4ca3157')


def s4_note(b):
    items = ['Wound location and laterality',
             'Measurements in cm: length, width, depth, with undermining and tunneling recorded separately',
             'Tissue type removed', 'Instrument used', 'Anesthesia used or not', 'Patient tolerance',
             'Pre- and post-procedure wound description', "Photographs where the payer's policy requires them",
             'Failed conservative therapy history', 'Physician order and plan of care']
    lst = ''
    for i, t in enumerate(items):
        lst += b.el('e-paragraph', f'nt-li{i}', cfg={'paragraph': t}, cls=['global-text'],
                    css=f'color: var(--DarkGray); line-height: 24px; text-align: start; padding-inline-start: 24px; '
                        f'background-image: url("{CHECK}"); background-repeat: no-repeat; background-position: 0px 7px; background-size: 14px auto;')
    col = b.el('e-heading', 'nt-h2', like='fdb1513', cfg={'tag': 'h2', 'title': 'What the Wound Care Billing Note Has to Contain'})
    col += b.el('e-paragraph', 'nt-p', like='5810717', cfg={'paragraph': (
        'Medical necessity is the proof that the procedure was needed. Most claim denials in wound care claims occur due to '
        'the documentation errors. Here is the documentation checklist:')})
    col += b.el('e-div-block', 'nt-list', lst, css='width: 100%; padding: 0px; display: flex; flex-direction: column; gap: 8px;')
    col += b.el('e-heading', 'nt-h3', like='e424be5', cfg={'tag': 'h3', 'title': 'Medical Necessity'}, css='color: var(--PureBlack);')
    col += b.el('e-paragraph', 'nt-p2', like='5810717', cfg={'paragraph': (
        'Advanced therapies cost more as compared to ordinary ones. The documentation must show that the ordinary therapies '
        'are tried before performing advanced ones. The ordinary therapies are offloading, compression, and moist wound '
        'management. How long were the ordinary therapies tried? Four weeks is the common number payers want. The '
        'documentation should show that the wound was not healed after ordinary therapies and it should be mentioned as '
        'non-healing or deteriorated. The measurements must show the trajectory of how it was not treated by the ordinary therapies.')})
    left = b.el('e-div-block', 'nt-l', b.el('e-image', 'nt-img', like='347fcd3',
                                           cfg=img(386993, '2025/01/urgent-care-infograhic1.svg', 731, 622, 'Wound care documentation checklist illustration')),
                like='d73f264', add_css='@media(--mobile_extra) { display: flex; justify-content: center; }')
    right = b.el('e-div-block', 'nt-r', col, like='9308103')
    return b.el('e-flexbox', 'nt', left + right, like='26425af')


def s5_therapy(b):
    kids = b.el('e-heading', 'th-h2', like='133d27d', cfg={'tag': 'h2', 'title': 'Advanced Wound Therapy Codes and the 2026 Changes'})
    kids += b.el('e-paragraph', 'th-p', like='252f275', cfg={'paragraph': (
        'Outsource wound care billing services to our experts who know what happened on January 01, 2026. CMS reclassified most '
        'skin substitutes (cellular and tissue-based products) from individually priced biologics to incident-to supplies paid '
        'at a single national rate of about $127.28 per square centimeter, in physician offices, hospital outpatient '
        "departments, and ambulatory surgery centers alike. The product's HCPCS Q-code still goes on the claim to identify what "
        'was applied, but it no longer sets the price; the flat per-square-centimeter rate does.')})
    kids += table(b, 'tt', ['Therapy', 'Codes', 'Key billing requirement'], [
        ['Sharp / selective debridement', '97597, 97598', 'Surface area and tissue type in the note'],
        ['Surgical excisional debridement', '11042–11047', 'Deepest tissue removed documented'],
        ['Enzymatic (collagenase), autolytic, mechanical debridement', 'No separate procedure code', 'Dressing-based; the product or the visit bills, not a procedure'],
        ['Compression therapy', '29580 (Unna boot), 29581 (multilayer, lower leg)', 'Venous ulcer diagnosis; compression documented before CTPs'],
        ['Total contact casting', '29445', 'Diabetic foot ulcer offloading documented'],
        ['Negative pressure wound therapy (NPWT)', '97605 (≤50 cm²), 97606 (&gt;50 cm²) durable equipment · 97607, 97608 disposable', 'Wound size, device type, therapy frequency in the note'],
        ['Hyperbaric oxygen therapy (HBOT)', '99183 physician attendance per session · G0277 facility per 30-minute interval', 'Qualifying indication under the Medicare NCD; prior authorization for most Medicare Advantage and commercial plans'],
        ['Skin substitutes / CTPs', '15271–15278 application by site and size, product reported as a supply', 'Failed standard care documented; measurement supports the cm² billed'],
        ['Growth factors', 'Product-based (drug billing rules)', "Diagnosis supports the product's labeled indication"],
        ['MIST therapy (non-contact ultrasound)', '97610', 'Wound measurements and treatment frequency'],
        ['Burn care', '16020, 16025, 16030 by size', 'Percentage of body surface area documented'],
    ], '30% 35% 35%', '640px')
    kids += b.el('e-paragraph', 'th-p2', like='252f275', cfg={'paragraph': (
        'When the practice supplies the negative pressure equipment, the DME side bills separately: E2402 for the pump, A6550 '
        'for the dressing kit, and A7000 for the canister. E1399, the miscellaneous DME code, is used only when no specific '
        'code exists and is a frequent denial trigger.')}, add_css='margin-block-start: 10px;')
    return b.el('e-flexbox', 'th', kids, like='5f0b342')


def s6_challenges(b):
    box = b.el('e-heading', 'ch-h2', like='c6ad9b2', cfg={'tag': 'h2', 'title': 'Challenges Wound Care Practices Face'})
    box += b.el('e-paragraph', 'ch-p', like='4f64f4c', cfg={'paragraph': (
        'In today’s financial climate, with costs rising and budgets being cut, it is especially important to have effective '
        'wound care medical billing so that all claims are properly reimbursed. Most wound care practices that don’t have '
        'specialists managing their coding and billing are losing significant amounts of revenue.')},
        add_css='width: 80%;\n@media(--tablet) { width: 95%; }\n@media(--mobile) { width: 100%; }')
    return b.el('e-flexbox', 'ch', b.el('e-div-block', 'ch-box', box, like='f88dbc2'), like='f5d0046')


def s7_reasons(b):
    intro = ('Medical codes are complicated and on top of that, they change every year, making it extremely difficult for '
             'staff in medical practice to keep up, which results in expensive errors. Outsourcing to an ' +
             link(M + 'services/revenue-cycle-management/', 'RCM company') +
             ' like MedCare MSO can help you capture more of the reimbursement you are owed. These are three of the reasons '
             'it is especially beneficial for wound care centers to ' +
             link(M + 'services/medical-billing-services/', 'outsource medical billing') + '.')
    cards = [
        ('176a94d', 'Referrals', 'Most wound care patients come in on referral and the referring physician’s office will usually '
         'have checked to see if their insurance covers your services—but you can’t assume that is the case. When each new '
         'patient makes an appointment, the wound care center must verify ' +
         link(M + 'services/coverage-discovery-services/', 'insurance coverage') + '.'),
        ('60ececd', 'Rising Costs And Lowered Reimbursements', 'Wound care supplies include some very expensive products, such as '
         'cellular and/or tissue-based products for skin wounds, but reimbursements are going down. This means it is vital that '
         'every service delivered is properly coded and billed so there is no lost revenue due to claim rejections and denials.'),
        ('f0d063b', 'Prior Authorization', 'Many insurers and payers require prior authorization for treatment and will reject a '
         'claim that isn’t authorized in their system, even if it is something they would have authorized and paid, so it is '
         'important to find out about authorizations when confirming that the exam/visit is covered. Wound care also may be '
         'ongoing over a period of time and require additional authorizations, so staff must be proactive and attentive to '
         'such limitations.'),
    ]
    grid = ''
    for i, (rid, t, p) in enumerate(cards):
        head = card_head(b, f'rs{i}', 400193, '2026/02/cta-icon-clean-claim.svg', t,
                         'font-family: var(--Poppins); font-weight: 500; font-size: 1.3rem; color: var(--DeepSkyBlue); line-height: 1.3;'
                         '\n@media(--tablet_extra) { font-size: 1.2rem; }\n@media(--mobile) { font-size: 1.1rem; }', '40px')
        body = b.el('e-paragraph', f'rs{i}p', cfg={'paragraph': p}, cls=['global-text'], css='color: var(--DarkGray); line-height: 24px;')
        grid += b.el('e-div-block', f'rs{i}c', head + body, like=rid)
    kids = b.el('e-heading', 'rs-h2', like='fc180e1', cfg={'tag': 'h2', 'title': 'Top Reasons to Outsource Wound Care Billing'})
    kids += b.el('e-paragraph', 'rs-p', like='9aba6e3', cfg={'paragraph': intro})
    kids += b.el('e-grid', 'rs-grid', grid, like='4b7be86',
                 add_css='width: 100%; grid-template-columns: repeat(3, 1fr);\n'
                         '@media(--tablet) { grid-template-columns: repeat(1, 1fr); }')
    return b.el('e-flexbox', 'rs', kids, like='c44d2b2')


def s8_cycle(b):
    items = [
        (408087, '2026/08/Group-437380600.svg', 'Coverage confirmed for the place of service',
         'Before the first visit, we confirm not only that the patient is covered but that the payer covers wound care at the '
         'setting where it will be delivered, outpatient center, office, or hospital, since the same wound can be covered in one '
         'and denied in another.'),
        (407618, '2025/01/icon-files.svg', 'Authorizations matched to the product and the wound',
         'For skin substitutes, negative pressure therapy, and hyperbaric oxygen, the authorization we obtain names the specific '
         'product, the specific wound, and the number of applications, and we re-authorize before ongoing care runs past the '
         'approved count.'),
        (405743, '2024/05/icon-ai-medical-coder.svg', 'Measurement-based coding',
         'Coders read the wound measurement, the tissue removed, and the stage or grade before selecting the code, so the unit '
         'count and the code family both come from the note.'),
        (407601, '2025/01/icon-dollar.svg', 'Claim submission and payment posting',
         'Claims go out with the diagnosis pointer, laterality, and supply lines aligned, and remittances are posted at the 2026 '
         'skin substitute rate rather than a saved product price.'),
        (408485, '2024/05/icon-eligiblity-denials.svg', 'Denial management built on coverage policy',
         "Denials are worked against the payer's actual policy, not a generic appeal template. That means checking the "
         'four-week conservative care rule and the specific documentation the LCD requires, through our ' +
         link(M + 'services/denial-management-services/', 'denial management services') + '.'),
        (407602, '2025/01/icon-clock.svg', 'Accounts receivable and credentialing',
         'Aging claims are followed to resolution through ' + link(M + 'services/ar-recovery-services/', 'A/R recovery') +
         ', and provider enrollment with wound care payers is maintained through our credentialing experts.'),
    ]
    grid = ''
    for i, (sid, surl, t, p) in enumerate(items):
        head = card_head(b, f'rc{i}', sid, surl, t,
                         'font-family: var(--Poppins); font-weight: 500; font-size: 16px; color: var(--PureBlack); line-height: 1.3;', '42px')
        body = b.el('e-paragraph', f'rc{i}p', like='59c8d08', cfg={'paragraph': p},
                    css='font-family: var(--Poppins); font-weight: 400; font-size: 14px; line-height: 22px; color: var(--DarkGray);')
        grid += b.el('e-div-block', f'rc{i}c', head + body, like='7ad3c0e')
    kids = b.el('e-heading', 'rc-h2', like='b94cf5d', cfg={'tag': 'h2', 'title': 'Wound Care Billing Services Across the Revenue Cycle'})
    kids += b.el('e-paragraph', 'rc-p', like='c13580f', cfg={'paragraph': (
        'A wound care claim passes through six points where it can be lost. Our wound care billing services are built around each one.')})
    kids += b.el('e-grid', 'rc-grid', grid, like='ddb74ac', add_css='margin-block-start: 20px;')
    return b.el('e-flexbox', 'rc', kids, like='562dce4')


def s9_healus(b):
    txt = (link(M + 'ai-eco-system/ehr/', 'HealUs') +
           " is MedCare MSO's electronic health record, and it is built so that the documentation a wound care payer requires "
           'and the claim that goes to the payer come from the same record. This is built under the supervision of expert '
           'billers and coders, it helps to manage your practice in an integrated platform. It has a full patient portal and '
           'has every workflow in a single system. It has a built-in AI scribe that documents encounters by voice. Wound care '
           'practices can get this tool to improve their practice workflows.')
    left = b.el('e-div-block', 'hu-l', b.el('e-image', 'hu-img', like='6d0ea4d',
                                           cfg=img(393449, '2025/08/what-is-ehr-infographic.svg', 663, 559, 'HealUs EHR for wound care billing and coding')),
                like='c010aac')
    right = b.el('e-div-block', 'hu-r',
                 b.el('e-heading', 'hu-h2', like='1e580a7', cfg={'tag': 'h2', 'title': 'HealUs EHR for Wound Care Billing and Coding'}) +
                 b.el('e-paragraph', 'hu-p', like='594c400', cfg={'paragraph': txt}),
                 like='2b81108')
    return b.el('e-flexbox', 'hu', left + right, like='c464ab1')


def s10_standards(b):
    items = [
        (406660, '2026/07/icon-badge-check.svg', 'Clinical Standards and Credentials',
         'The rules that govern the wound care coding are set by the clinical bodies. Our wound care billing services are built '
         'to match these standards. For pressure injuries, the staging comes from NPIAP. Wound care practice standards are set '
         'by the Association for the Advancement of Wound Care (AAWC), the WOCN society, and the Alliance of Wound Care '
         'Stakeholders. Undersea and Hyperbaric Medical Society (UHMS) set the standards of hyperbaric medicine. In the same way, '
         'the American Board of Wound Management (ABWM) certifies the CWS, CWSP, and CWCA. There are separate certifying boards '
         'that offer WCC and CWOCN credentials, held by wound and ostomy nurses.'),
        (390753, '2025/05/insurance-verification.svg', 'Credentials and Systems of Our Wound Care Billing Company',
         'Coding teams should hold AAPC and AHIMA credentials — CPC, CPMA, COC, CCS. These certifications help ensure '
         'specialty-specific coding for wound care practices. We work with wound-specific platforms like Net Health WoundExpert, '
         'Tissue Analytics, Intellicure, Swift Medical, eKare, and WoundZoom. These platforms capture measurements and images '
         'that help to select the relevant codes. EHRs like athenahealth, eClinicalWorks, AdvancedMD, NextGen, and Tebra capture '
         'the encounter and the charge.'),
        (386106, '2024/05/Group-437380473.svg', 'Product and Network Documentation We Reconcile',
         'The accurate documentation requires the product details too. Organogenesis, MiMedx, Integra LifeSciences, Smith+Nephew, '
         '3M/KCI, and Medline offer skin substitutes and dressings for the wound. Each manufacturer carries its own application '
         'and supply documentation. Wound care networks, like Healogics and RestorixHealth have their own standards for '
         'charting. As a wound care billing company, we make sure all the documentation is accurate based on the standards. We '
         'create error-free claims for wound care practices and do not endorse any product.'),
    ]
    grid = ''
    for i, (sid, surl, t, p) in enumerate(items):
        head = card_head(b, f'sd{i}', sid, surl, t,
                         'font-family: var(--Poppins); font-weight: 500; font-size: 1.3rem; color: var(--DeepSkyBlue); line-height: 1.3;'
                         '\n@media(--tablet_extra) { font-size: 1.2rem; }\n@media(--mobile) { font-size: 1.1rem; }', '44px')
        body = b.el('e-paragraph', f'sd{i}p', like='c3664b6', cfg={'paragraph': p}, add_css='line-height: 24px;')
        grid += b.el('e-div-block', f'sd{i}c', head + body, like='bac13a3', add_css='@media(--mobile) { padding: 6%; }')
    kids = b.el('e-heading', 'sd-h2', like='133d27d', cfg={'tag': 'h2', 'title': 'Standards Behind Our Wound Care Billing Services'})
    kids += b.el('e-grid', 'sd-grid', grid, like='85f631f',
                 add_css='width: 100%; column-gap: 30px; grid-template-columns: repeat(3, 1fr); grid-template-rows: none !important; grid-auto-rows: auto !important;\n'
                         '@media(--tablet_extra) { column-gap: 20px; }\n'
                         '@media(--tablet) { grid-template-columns: repeat(1, 1fr); }')
    return b.el('e-flexbox', 'sd', kids, like='5f0b342')


def s11_different(b):
    items = [
        ('We code from the operative note, not the charge sheet',
         'Measurements and tissue depth determine wound care codes. Our medical coders read the note before selecting a code, '
         'so we pick the exact code that matches the procedure.'),
        ('We rebuilt skin substitute billing for the 2026 rule',
         'The January reclassification moved CTPs to a flat rate per square centimeter. Our posting and pricing reflect it, so '
         'your claims are priced on the latest model.'),
        ('We track the four-week conservative care requirement per wound',
         'We keep track of the four-week duration of every wound separately, so an expensive therapy is not billed early '
         'leading to claim denial.'),
        ('We work inside the platform your practice already uses',
         'Measurements and photos stay where they were captured. Nothing is typed again, so the errors the platform was meant '
         'to prevent are not reintroduced.'),
        ('We appeal medical necessity denials by adding what was missing',
         'Denials in a wound care specialty are documentation disputes. Resubmitting the same claim gets denied again, so we '
         'identify the missing element and supply it.'),
        ('We report denials by cause, days in A/R by payer',
         'A single collection percentage hides where money leaks. Our reporting shows it all.'),
    ]
    grid = ''
    for i, (t, p) in enumerate(items):
        h = b.el('e-heading', f'df{i}t', cfg={'tag': 'h3', 'title': t}, like='c3fa560',
                 css='font-family: var(--Poppins); font-weight: 400; font-size: 1.3rem; line-height: 1.3; color: var(--PureWhite);'
                     '\n@media(--tablet_extra) { font-size: 1.15rem; }\n@media(--mobile) { font-size: 1.1rem; }')
        body = b.el('e-paragraph', f'df{i}p', like='5850f12', cfg={'paragraph': p}, add_css='line-height: 22px;')
        grid += b.el('e-div-block', f'df{i}c', h + body, like='5b27bda', add_css='@media(--mobile) { padding: 6%; }')
    kids = b.el('e-heading', 'df-h2', like='fc180e1', cfg={'tag': 'h2', 'title': 'What Our Wound Care Billing Company Does Differently'})
    kids += b.el('e-paragraph', 'df-p', like='9aba6e3', cfg={'paragraph': (
        'Most billing companies describe the same services. Here is what MedCare MSO actually does for wound care practices.')})
    kids += b.el('e-grid', 'df-grid', grid, like='678f032',
                 css='width: 100%; padding: 0px; grid-template-columns: repeat(3, 1fr); grid-template-rows: none !important; grid-auto-rows: auto !important;\n'
                     '@media(--tablet_extra) { grid-template-columns: repeat(2, 1fr); }\n'
                     '@media(--mobile) { grid-template-columns: repeat(1, 1fr); }')
    return b.el('e-flexbox', 'df', kids, like='c44d2b2')


def s12_outsource(b):
    col = b.el('e-heading', 'os-h2', like='c648599', cfg={'tag': 'h2', 'title': 'Outsource Wound Care Billing Services to MedCare MSO'})
    col += b.el('e-heading', 'os-h3a', like='e424be5', cfg={'tag': 'h3', 'title': 'Outsource Medical Billing Services'},
                css='color: var(--PureBlack);')
    col += b.el('e-paragraph', 'os-pa', like='40448df', cfg={'paragraph': (
        link(M + 'services/medical-billing-services/', 'Outsourcing medical billing') +
        ' has proven to be a low cost way to increase revenue. All our staff are trained in HIPAA compliance to ensure your '
        'patient information is safe, and we have certified billers who are experienced in wound care billing and coding. An '
        'additional, and perhaps an even greater, benefit of having us take care of all the billing and coding hassles is a '
        'tremendous reduction in stress for physicians. Our clients report finding their practice enjoyable once again.')})
    col += b.el('e-heading', 'os-h3b', like='e424be5', cfg={'tag': 'h3', 'title': 'Dedicated To Improving Your Revenue Cycle Management'},
                css='color: var(--PureBlack);')
    col += b.el('e-paragraph', 'os-pb', like='40448df', cfg={'paragraph': (
        'MedCare MSO is dedicated to improving your medical revenue cycle management (RCM). Billing is our most popular service, '
        'but we offer a customized suite of services to our clients that includes our proprietary software to make sure all '
        'your claims are filed with the most up-to-date codes. We can manage ' +
        link(M + 'services/medical-credentialing-services/', 'payer credentialing') +
        ', compliance reviews, annual payer adjustments and payback, and much more.')})
    left = b.el('e-div-block', 'os-l', col, like='2f05bad')
    right = b.el('e-div-block', 'os-r', b.el('e-image', 'os-img', like='5017c67',
                                            cfg=img(399656, '2026/01/urology-banner-why-choose.webp', 729, 733, 'Banner Why Choose MedCare MSO')),
                 like='b9351d3')
    return b.el('e-flexbox', 'os', left + right, like='7174a22')


SECTIONS = [s0_hero, s1_complex, s2_wound_types, s3_measure, s4_note, s5_therapy, s6_challenges,
            s7_reasons, s8_cycle, s9_healus, s10_standards, s11_different, s12_outsource]


def payload(fns, post_id, mode='append', dry=False):
    b = B()
    xml = ''.join(f(b) for f in fns)
    return {'post_id': post_id, 'xml_structure': xml, 'element_config': b.cfg, 'style': b.style,
            'classes': b.classes, 'mode': mode, 'dry_run': dry}


if __name__ == '__main__':
    p = payload(SECTIONS, 410324, dry=True)
    print(len(json.dumps(p)), 'bytes;', len(p['style']), 'styled elements')
