"""Add "How Billing for Mental Health Services Works" to the Mental Health Billing Services page (specialties 384461),
right after "Helping You Get Faster, Timely & Accurate Reimbursements" (6ee35c6).

Built with the page's own patterns: parent-container section, specialties-heading H2 + global-text intro (as in
section 912cf78), and its rounded pastel cards (#EBF6FF / #F2FCF3 / #FDF9F0, radius 30px, 2rem padding) with H3 titles
styled like the page's card titles (Poppins 500, 1.4rem, DeepSkyBlue). Step numbers use the existing
icon-number01..06 SVGs from the Media Library.  Grid: 3 columns, 2 at tablet (<=1024), 1 at mobile_extra (<=880).

usage: python3 add_billing_steps.py [--dry]
"""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST, AFTER = 384461, '6ee35c6'
ICONS = [404840, 404841, 404842, 404843, 404844, 408016]
BGS = ['#EBF6FF', '#F2FCF3', '#FDF9F0']
STEPS = [
    ('Verify Eligibility and Benefits', 'Confirm the patient’s mental health coverage, copays, visit limits and any prior authorization before the first session.'),
    ('Document the Session', 'The clinician records the service provided, including start and stop times for time-based psychotherapy.'),
    ('Assign the Codes', 'A coder selects the CPT code the documentation supports and pairs it with an ICD-10 diagnosis that shows medical necessity.'),
    ('Submit the Claim', 'Submit the claim electronically, adding telehealth modifiers and place-of-service codes where needed.'),
    ('Post the Payment', 'Post the payment and check it against the contracted rate.'),
    ('Follow Up on Denials', 'Any denied or underpaid claim is corrected and appealed so the revenue isn’t written off.'),
]

xml = ['<e-flexbox configuration-id="sec">', '<e-heading configuration-id="h"></e-heading>',
       '<e-paragraph configuration-id="intro"></e-paragraph>', '<e-grid configuration-id="grid">']
config = {
    'h': {'tag': 'h2', 'title': 'How Billing for Mental Health Services Works'},
    'intro': {'paragraph': 'Billing for mental health services follows the same basic steps for every session, but each step has rules specific to behavioral health:'},
}
style = {
    'sec': 'background-color: #ffffff; display: flex; flex-direction: column; gap: 30px; align-items: center; '
           '@media(--tablet_extra) { gap: 16px; }',
    'h': 'color: var(--PureBlack); line-height: 120%; text-align: center; '
         '@media(--tablet_extra) { width: 100%; font-size: 2rem; } @media(--mobile) { font-size: 1.6rem; }',
    'intro': 'color: var(--DarkGray); line-height: 24px; text-align: center; width: 75%; '
             '@media(--tablet) { width: 100%; }',
    'grid': 'width: 100%; padding: 0px; column-gap: 32px; row-gap: 20px; grid-template-columns: repeat(3, 1fr); '
            'grid-template-rows: none; grid-auto-rows: auto; '
            '@media(--tablet_extra) { column-gap: 20px; } '
            '@media(--tablet) { grid-template-columns: repeat(2, 1fr); } '
            '@media(--mobile_extra) { grid-template-columns: repeat(1, 1fr); }',
}
classes = {'sec': ['parent-container'], 'h': ['specialties-heading'], 'intro': ['global-text']}
for k, (title, body) in enumerate(STEPS):
    c, i, t, p = f'card{k}', f'icon{k}', f'title{k}', f'body{k}'
    xml += [f'<e-div-block configuration-id="{c}">', f'<e-image configuration-id="{i}"></e-image>',
            f'<e-heading configuration-id="{t}"></e-heading>', f'<e-paragraph configuration-id="{p}"></e-paragraph>', '</e-div-block>']
    config[i] = {'image': {'src': {'id': ICONS[k]}, 'size': 'full'}}
    config[t] = {'tag': 'h3', 'title': title}
    config[p] = {'paragraph': body}
    style[c] = (f'width: 100%; padding: 2rem; border-radius: 30px; background-color: {BGS[k % 3]}; display: flex; '
                'flex-direction: column; gap: 16px; @media(--tablet_extra) { padding: 1.5rem; }')
    style[i] = 'width: 52px; height: 52px;'
    style[t] = ('font-family: var(--Poppins); font-weight: 500; font-size: 1.4rem; line-height: 140%; color: var(--DeepSkyBlue); '
                '@media(--mobile) { font-size: 1.25rem; }')
    style[p] = 'color: var(--DarkGray); line-height: 24px;'
    classes[p] = ['global-text']
xml += ['</e-grid>', '</e-flexbox>']

args = {'post_id': POST, 'xml_structure': ''.join(xml), 'element_config': config, 'style': style, 'classes': classes}
dry = '--dry' in sys.argv
mcp.init()
res = mcp.call('elementor-build-composition', dict(args, dry_run=dry))
print(json.dumps(res)[:1500])
if dry:
    sys.exit()

sec_id = res['root_element_ids'][0]
json.dump({'section_id': sec_id, 'result': res}, open(os.path.join(HERE, '..', 'build', 'billing_steps_result.json'), 'w'))
st = mcp.call('elementor-get-page-structure', {'post_id': POST})
ids = [e['id'] for e in st['elements']]
idx = ids.index(AFTER) + 1
print('new section', sec_id, 'move to index', idx)
mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
    {'action': 'move', 'element_id': sec_id, 'new_parent_id': 'document', 'index': idx}]})
print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
# editing a published document can land in an autosave: touch one new element and publish again
mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
    {'action': 'update', 'element_id': sec_id, 'style': 'background-color: #ffffff;'}]})
print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
st = mcp.call('elementor-get-page-structure', {'post_id': POST})
print([e['id'] for e in st['elements']])
