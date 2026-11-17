"""Redesign of "Where Revenue Slips With Each Kansas Payer" (section b1a29ab on states post 412021): Option A, "2 + 3, grouped".

Row 1: one wide card holding the two Blue plans side by side (BCBSKS | Blue KC) under a blue strip.
Row 2: Medicare, Marketplace and Workers' Comp in three columns (tablet: 2 + 1 full-width; mobile: stacked).
Same look as the page's other cards (#E8EFF4, radius 30, blue 1.3rem titles, global-text copy), no new classes,
same subtle hover as the rest of the page. Copy and icons come from the existing cards (build/payer_cards.json).

Usage: payer_redesign.py [dry]  -> appends the new block to the section, deletes the old grid (5b5aaf7), publishes.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

PID, SECTION, OLD_GRID = 412021, 'b1a29ab', '5b5aaf7'
CARDS = json.load(open(os.path.join(HERE, '..', 'build', 'payer_cards.json')))
STRIP = 'Two Blue plans, one state: check the home plan first'

cfg, style, classes = {}, {}, {}


def el(tag, cid, kids='', c=None, css='', cls=None):
    if c:
        cfg[cid] = c
    if css:
        style[cid] = ' '.join(css.split())
    if cls:
        classes[cid] = cls
    return f'<{tag} configuration-id="{cid}">{kids}</{tag}>'


HOVER = ('transition: transform 0.3s ease, box-shadow 0.3s ease; '
         '&:hover{transform: scale(1.02); box-shadow: 0px 12px 28px -12px rgba(3,103,161,0.25);}')


def card_inner(k, c):
    head = el('e-flexbox', f'{k}-hd',
              el('e-image', f'{k}-ic', c={'image': {'src': {'id': c['img'], 'alt': ''}, 'size': 'full'}}, css='width: 44px; height: 44px; flex: 0 0 auto;')
              + el('e-heading', f'{k}-t', c={'tag': 'h3', 'title': c['title']}, css=(
                  'font-family: var(--Poppins); font-weight: 500; font-size: 1.3rem; color: var(--DeepSkyBlue); line-height: 1.3; margin: 0px; '
                  '@media(--tablet_extra){font-size: 1.2rem;} @media(--mobile){font-size: 1.1rem;}')),
              css='padding: 0px; display: flex; flex-direction: row; gap: 15px; align-items: center; @media(--mobile){gap: 10px;}')
    para = el('e-paragraph', f'{k}-p', c={'paragraph': c['text']}, cls=['global-text'], css='color: var(--DarkGray); line-height: 24px; margin: 0px;')
    return head + para


def build():
    blue = ''
    for i, c in enumerate(CARDS[:2]):
        blue += el('e-div-block', f'py-b{i}', card_inner(f'py-b{i}', c), css=(
            'padding: 28px; min-width: 0px; display: flex; flex-direction: column; gap: 15px; '
            + ('border-right: 1px solid #CFDBE5; ' if i == 0 else '')
            + '@media(--mobile_extra){padding: 24px;' + (' border-right: 0px; border-bottom: 1px solid #CFDBE5;' if i == 0 else '') + '}'))
    strip = el('e-paragraph', 'py-strip', c={'paragraph': STRIP}, css=(
        'grid-column: 1 / -1; margin: 0px; padding: 14px 28px; background-color: var(--DeepSkyBlue); color: var(--PureWhite); '
        'font-family: var(--Poppins); font-size: 14px; font-weight: 500; line-height: 1.5; letter-spacing: 0.08em; text-transform: uppercase; '
        '@media(--mobile){font-size: 12px; padding: 12px 20px;}'))
    blue_card = el('e-grid', 'py-blue', strip + blue, css=(
        'width: 100%; padding: 0px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); grid-template-rows: auto; gap: 0px; '
        'border-radius: 30px; overflow: hidden; background-color: #E8EFF4; ' + HOVER.replace('scale(1.02)', 'scale(1.01)') + ' '
        '@media(--mobile_extra){grid-template-columns: 1fr;}'))
    three = ''
    for i, c in enumerate(CARDS[2:]):
        three += el('e-div-block', f'py-c{i}', card_inner(f'py-c{i}', c), css=(
            'width: 100%; min-width: 0px; padding: 28px; border-radius: 30px; background-color: #E8EFF4; display: flex; flex-direction: column; gap: 15px; '
            + HOVER + ' '
            + ('@media(--tablet){grid-column: 1 / -1;} @media(--mobile_extra){grid-column: auto;} ' if i == 2 else '')
            + '@media(--mobile){padding: 24px;}'))
    row = el('e-grid', 'py-row', three, css=(
        'width: 100%; padding: 0px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: auto; gap: 20px; '
        '@media(--tablet){grid-template-columns: repeat(2, minmax(0, 1fr));} @media(--mobile_extra){grid-template-columns: 1fr;}'))
    wrap = el('e-flexbox', 'py-layout', blue_card + row, css='width: 100%; padding: 0px; display: flex; flex-direction: column; gap: 20px;')
    return wrap


def main(dry=False):
    xml = build()
    r = mcp.call('elementor-build-composition', {'post_id': PID, 'parent_id': SECTION, 'mode': 'append', 'xml_structure': xml,
                                                 'element_config': cfg, 'style': style, 'classes': classes, 'dry_run': dry})
    resolved = r.pop('resolved_xml', '')
    print(json.dumps(r)[:400])
    if dry:
        return
    open(os.path.join(HERE, '..', 'build', 'payer_resolved.xml'), 'w').write(resolved)
    ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', resolved))
    r = mcp.call('elementor-manage-elements', {'post_id': PID, 'operations': [{'action': 'delete', 'element_id': OLD_GRID}]})
    print('delete old grid:', [x['status'] for x in r['results']], 'new layout id', ids['py-layout'])


if __name__ == '__main__':
    main('dry' in sys.argv)
