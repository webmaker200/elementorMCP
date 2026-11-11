"""Replace "How We Take Over Your Behavioral Health Billing" with the Cardiology-style process section
(numbered timeline with gradient line on the left, cycle diagram on the right). Repeated parts use global classes
so the page stays small.  usage: process.py [dry]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402
PID = 411549
MEDIA = json.load(open(os.path.join(HERE, '..', 'media.json')))
dry = 'dry' in sys.argv

CLASSES = {
    'bh-proc-item': 'display: flex; flex-direction: row; align-items: center; gap: 15px; width: 100%; padding: 0px; position: relative; z-index: 1;',
    'bh-proc-num': 'width: 50px; height: 50px; flex-shrink: 0; object-fit: contain; background-color: #FFFFFF; border-radius: 999px; @media(--mobile){width: 44px; height: 44px;}',
    'bh-proc-body': 'display: flex; flex-direction: column; width: 100%; padding: 0px;',
    'bh-proc-title': 'font-family: var(--Poppins); font-size: 16px; font-weight: 500; line-height: 1.2; color: #0A1628; margin: 8px 0px 4px 0px;',
    'bh-proc-text': 'font-family: var(--Poppins); font-size: 14px; font-weight: 400; line-height: 21px; color: #333333; margin: 0px;',
}
STEPS = [
    ('Step 1: Free Audit', 'MedCare MSO’s billing experts review your practice’s denials, A/R aging, open authorizations and payer contracts. After an audit, we show you where revenue is being lost.'),
    ('Step 2: Workflow and Payer Mapping', 'Our team documents each level of care, payer, contract rate and authorization rule, and sets up access to your EHR.'),
    ('Step 3: Parallel Run', 'We work alongside your current billing process, so no claim or review falls through.'),
    ('Step 4: Go-Live', 'Our specialists take over claim submission, reviews and A/R follow-up, and you receive your first reports by program and payer.'),
]

if not dry:
    have = {x['label'] for x in mcp.rest('GET', 'elementor/v1/global-classes?context=frontend')['data']}
    ops = [{'action': 'create', 'label': k, 'css': v} for k, v in CLASSES.items() if k not in have]
    if ops:
        r = mcp.call('elementor-manage-classes', {'operations': ops})
        new = [x['id'] for x in r['results'] if x['status'] == 'ok']
        mcp.call('elementor-reorder-classes', {'order': new + [x for x in r['order'] if x not in new]})
        print('classes', [x['status'] for x in r['results']])

xml, cfg, style, cls = [], {}, {}, {}
def el(tag, cid, kids='', c=None, s=None, k=None):
    if c: cfg[cid] = c
    if s: style[cid] = s
    if k: cls[cid] = k
    return f'<{tag} configuration-id="{cid}">{kids}</{tag}>'

items = ''
for i, (t, d) in enumerate(STEPS):
    items += el('e-div-block', f'pi{i}',
                el('e-image', f'pi{i}n', c={'image': {'src': {'id': MEDIA[f'bh-step-number-{i + 1}']['id'], 'alt': f'Step {i + 1}'}, 'size': 'full'}}, k=['bh-proc-num'])
                + el('e-div-block', f'pi{i}b', el('e-heading', f'pi{i}t', c={'tag': 'h3', 'title': t.split(': ', 1)[1]}, k=['bh-proc-title'])
                     + el('e-paragraph', f'pi{i}p', c={'paragraph': d}, k=['bh-proc-text']), k=['bh-proc-body']),
                k=['bh-proc-item'])
left = el('e-div-block', 'pl', items, s=(
    'display: flex; flex-direction: column; justify-content: space-between; gap: 48px; width: 46%; padding: 0px; position: relative; '
    '&::before{content: ""; position: absolute; left: 24px; top: 30px; bottom: 30px; width: 2px; background-image: linear-gradient(180deg, #2064AF 0%, #7FB63F 100%); z-index: 0;} '
    '@media(--tablet){width: 100%; gap: 36px;} @media(--mobile){&::before{left: 21px;}}'))
right = el('e-div-block', 'pr', el('e-image', 'primg', c={'image': {'src': {'id': MEDIA['bh-takeover-cycle']['id'], 'alt': 'Behavioral health billing takeover plan in four steps'}, 'size': 'full'}},
                                  s='width: 100%; height: auto;'),
           s='display: flex; width: 48%; padding: 0px; @media(--tablet){width: 80%; align-self: center;} @media(--mobile){width: 100%;}')
row = el('e-flexbox', 'prow', left + right, s=(
    'display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: 40px; width: 100%; padding: 0px; margin-top: 20px; '
    '@media(--tablet){flex-direction: column; align-items: stretch;}'))
sec = el('e-flexbox', 'psec',
         el('e-heading', 'ph2', c={'tag': 'h2', 'title': 'How We Take Over Your Behavioral Health Billing'}, k=['specialties-heading'],
            s='font-weight: 300; color: #000000; text-align: center; margin: 0px;')
         + el('e-paragraph', 'pp', c={'paragraph': 'Switching billing companies shouldn’t put your open authorizations or unpaid claims at risk. That’s why we approach every billing process with four clear steps:'},
              k=['global-text'], s='color: #4F4F4F; text-align: center; margin: 0px;')
         + row,
         c={'tag': 'section'}, k=['parent-container'],
         s='display: flex; flex-direction: column; align-items: center; gap: 16px; width: 100%; background-color: #FFFFFF;')
r = mcp.call('elementor-build-composition', {'post_id': PID, 'xml_structure': sec, 'element_config': cfg, 'style': style, 'classes': cls,
                                              'mode': 'append', 'dry_run': dry})
xmlr = r.pop('resolved_xml', '') if isinstance(r, dict) else ''
print(json.dumps(r)[:800])
if not dry:
    open(os.path.join(HERE, '..', 'build', 'process_resolved.xml'), 'w').write(xmlr)
