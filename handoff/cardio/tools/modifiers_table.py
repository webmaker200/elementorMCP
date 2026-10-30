"""Cardiology Billing Challenges (post 411188, type 'challenges'): heading + 5-column table appended to the end of the
'Challenge 2' section content (sc-wrap 966a421), styled like the Salus AI 'What Each Plan Includes' table (410964 / 6319da0f).
usage: python3 modifiers_table.py [--dry]"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'healus', 'tools'))
import mcp

PID, PARENT = 411188, '966a421'
F = 'font-family: var(--Poppins);'
HEAD = ['Modifier', 'Use when', 'Global period', 'Payment', 'Orthopedic example']
ROWS = [
    ['58', 'Planned, staged or more extensive related procedure', 'New global starts', '100% of allowed',
     'Hardware removal planned and documented at the time of the original fixation'],
    ['78', 'Unplanned return to the OR for a related complication', 'Original global continues',
     'Intra-operative share only, about 69% on many orthopedic 90-day codes (set per code)', 'Hematoma washout after fixation'],
    ['79', 'Unrelated procedure, different site or diagnosis', 'New global starts', '100% of allowed',
     'Arthroscopy in the opposite knee during a hip global'],
]
CELL = ('margin: 0px; padding-block-start: 19.3px; padding-block-end: 19.3px; padding-inline-start: 20.6px; padding-inline-end: 20.6px; '
        'display: flex; align-items: center; min-width: 0px; overflow-wrap: break-word; ')
BORDER = 'border-block-end: 1.29px solid rgba(7,24,45,0.08); '
TAB = '@media(--tablet){padding-block-start: 16px; padding-block-end: 16px; padding-inline-start: 14px; padding-inline-end: 14px;} '
MOB = '@media(--mobile){padding-block-start: 14px; padding-block-end: 14px; padding-inline-start: 12px; padding-inline-end: 12px;} '

cfg, style, xml = {}, {}, []


def el(tag, cid, kids='', c=None, css=''):
    if c:
        cfg[cid] = c
    if css:
        style[cid] = css
    return f'<{tag} configuration-id="{cid}">{kids}</{tag}>'


heading = el('e-heading', 'mod-h', c={'tag': 'h3', 'title': 'What is the difference between modifiers 58, 78 and 79?'}, css=(
    f'width: 100%; max-width: 1428px; {F} font-weight: 400; font-size: 58px; color: #000000; letter-spacing: -1.16px; line-height: 82px; '
    'text-align: center; margin-block-start: 110px; margin-block-end: 48px; margin-inline-start: auto; margin-inline-end: auto; '
    '@media(--laptop){font-size: 48px; line-height: 64px; margin-block-start: 90px; margin-block-end: 40px;} '
    '@media(--tablet_extra){font-size: 42px; line-height: 56px;} '
    '@media(--tablet){font-size: 38px; letter-spacing: -0.76px; line-height: 50px; margin-block-start: 64px; margin-block-end: 32px;} '
    '@media(--mobile){font-size: 26px; letter-spacing: -0.52px; line-height: 36px; margin-block-start: 48px; margin-block-end: 24px;}'))
cells = ''
for i, t in enumerate(HEAD):
    first = i == 0
    cells += el('e-paragraph', f'mod-h{i}', c={'paragraph': t}, css=(
        CELL + f'{F} font-weight: {600 if first else 500}; font-size: 18px; line-height: 25px; color: {"#64748B" if first else "#07182D"}; '
        'padding-block-start: 25.75px; padding-block-end: 25.75px; ' + BORDER + TAB + MOB.replace('{', '{font-size: 13px; line-height: 18px; ', 1)))
for r, row in enumerate(ROWS):
    for i, t in enumerate(row):
        first = i == 0
        last_row = r == len(ROWS) - 1
        cells += el('e-paragraph', f'mod-r{r}c{i}', c={'paragraph': t}, css=(
            CELL + f'{F} font-weight: {600 if first else 500}; font-size: {18 if first else 16}px; line-height: {27 if first else 25}px; '
            f'color: {"#07182D" if first else "#475569"}; ' + ('' if last_row else BORDER) + TAB +
            MOB.replace('{', '{font-size: 13px; line-height: 19px; ', 1)))
grid = el('e-div-block', 'mod-grid', cells, css=(
    'width: 100%; padding: 0px; display: grid; grid-template-columns: 0.6fr 1.5fr 1.1fr 1.5fr 1.8fr; grid-template-rows: auto; gap: 0px; '
    '@media(--mobile){grid-template-columns: 0.6fr 1.5fr 1.1fr 1.5fr 1.8fr; min-width: 760px;}'))
box = el('e-flexbox', 'mod-box', grid, css=(
    'width: 100%; max-width: 1463px; padding: 10px; border-radius: 31px; border: 1px solid rgba(255,255,255,0.8); '
    'background-color: rgba(255,255,255,0.2); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); display: flex; '
    'margin-inline-start: auto; margin-inline-end: auto; '
    '@media(--tablet){max-width: 100%;} @media(--mobile){padding: 4px; border-radius: 20px; overflow-x: auto;}'))

payload = {'post_id': PID, 'parent_id': PARENT, 'mode': 'append', 'xml_structure': heading + box,
           'element_config': cfg, 'style': style, 'dry_run': '--dry' in sys.argv}
r = mcp.call('elementor-build-composition', payload)
print('warnings:', json.dumps(r.get('warnings'))[:800] if r.get('warnings') else 'none')
if '--dry' not in sys.argv:
    ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml']))
    json.dump(ids, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modifiers_ids.json'), 'w'))
    print('added', len(ids), 'elements; heading', ids.get('mod-h'), 'box', ids.get('mod-box'))
