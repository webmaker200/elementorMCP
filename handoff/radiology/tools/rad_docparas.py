import zipfile, re, json, sys, html
z = zipfile.ZipFile(sys.argv[1])
x = z.read('word/document.xml').decode('utf8')
body = x[x.find('<w:body'):]
out = []
# walk paragraphs in order; mark table cells
for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>', body, flags=re.S):
    blk = m.group(0)
    if blk.startswith('<w:tbl>'):
        for row in re.findall(r'<w:tr[ >].*?</w:tr>', blk, flags=re.S):
            cells = []
            for c in re.findall(r'<w:tc>.*?</w:tc>', row, flags=re.S):
                t = ' '.join(''.join(html.unescape(t) for t in re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p)) for p in re.findall(r'<w:p[ >].*?</w:p>', c, flags=re.S))
                cells.append(t)
            out.append({'type': 'row', 'cells': cells})
        continue
    style = re.search(r'<w:pStyle w:val="([^"]+)"', blk)
    parts = []
    for r in re.finditer(r'<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:tab/>|<w:br[^>]*/>', blk):
        parts.append(html.unescape(r.group(1)) if r.group(1) is not None else (' ' if 'tab' in r.group(0) else '\n'))
    t = ''.join(parts)
    if t.strip():
        out.append({'type': 'p', 'style': style.group(1) if style else '', 'text': t})
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print(len(out))
for o in out[:12]: print(o.get('style'), repr((o.get('text') or ' | '.join(o.get('cells', [])))[:100]))
