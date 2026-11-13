"""Word-level comparison of the Radiology doc (docx paragraphs) with the live page text blocks.
Whitespace runs are collapsed (a browser can't show double spaces) but a MISSING space still shows as two words
joined. Curly vs straight quotes are treated as equal (WordPress converts quotes when it displays text)."""
import json, re, sys, difflib, html
docp = json.load(open(sys.argv[1])); page = json.load(open(sys.argv[2])); out = sys.argv[3]

def norm(t):
    t = t.replace(' ', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', t).strip()

D = []  # doc blocks
for i, o in enumerate(docp):
    if o['type'] == 'row':
        for c in o['cells']:
            if norm(c): D.append({'kind': 'table cell', 'text': c})
    else:
        if o['text'].startswith('AI Scan Report'): continue
        D.append({'kind': o.get('style') or 'paragraph', 'text': o['text']})
P = []
for o in page:
    t = norm(o['text'])
    if not t: continue
    if P and norm(P[-1]['text']) == t: continue  # desktop/mobile duplicate
    P.append(o)

def toks(blocks):
    tt = []
    for bi, b in enumerate(blocks):
        for w in norm(b['text']).split(' '):
            tt.append((w, bi))
    return tt
dt, pt = toks(D), toks(P)
sm = difflib.SequenceMatcher(None, [w for w, _ in dt], [w for w, _ in pt], autojunk=False)
dflag = [None] * len(dt); pflag = [None] * len(pt)
pairs = []
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal': continue
    for i in range(i1, i2): dflag[i] = op
    for j in range(j1, j2): pflag[j] = op
    pairs.append((op, i1, i2, j1, j2))

def classify(a, b):
    A, Bt = ' '.join(a), ' '.join(b)
    if A.replace(' ', '') == Bt.replace(' ', '') and A != Bt:
        return 'Space missing / extra'
    if A.lower() == Bt.lower(): return 'Capitalisation'
    if re.sub(r'[^\w\s]', '', A) == re.sub(r'[^\w\s]', '', Bt): return 'Punctuation'
    if not a: return 'Extra on page'
    if not b: return 'Missing on page'
    return 'Wording'
rows = []
for op, i1, i2, j1, j2 in pairs:
    a = [w for w, _ in dt[i1:i2]]; bb = [w for w, _ in pt[j1:j2]]
    big = len(a) > 40 or len(bb) > 40
    rows.append({'type': classify(a, bb), 'doc': ' '.join(a), 'page': ' '.join(bb), 'big': big,
                 'doc_block': dt[i1][1] if i1 < len(dt) else dt[-1][1], 'page_sec': P[pt[j1][1]]['sec'] if j1 < len(pt) else '',
                 'ctx_before': ' '.join(w for w, _ in dt[max(0, i1 - 6):i1]), 'ctx_after': ' '.join(w for w, _ in dt[i2:i2 + 6])})
# a block that is "missing" in one place and "extra" in another is a reorder, not missing content
from collections import Counter as _C
def _sim(a, b):
    A, B = _C(a.split()), _C(b.split())
    return sum((A & B).values()) / max(1, max(sum(A.values()), sum(B.values())))
for r in rows:
    if r['type'] == 'Missing on page':
        for q in rows:
            if q['type'] == 'Extra on page' and len(r['doc']) > 80 and _sim(r['doc'], q['page']) > 0.5:
                r['type'] = 'Order differs'; q['type'] = 'Order differs (same block)'
                r['page'] = 'Same text appears on the page in a different order: ' + q['page'][:200]
for r, (op, i1, i2, j1, j2) in zip(list(rows), pairs):
    if op == 'insert' and i1 > 0: r['doc_block'] = dt[i1 - 1][1]
rows = [r for r in rows if r['type'] != 'Order differs (same block)']
json.dump(rows, open(out + '.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(rows), Counter(r['type'] for r in rows))

# ---------------- inline HTML report: whole document, differences highlighted in place ----------------
E = html.escape
ins_at = {}   # doc token index -> list of page-only strings inserted before it
rep_end = {}  # last doc token index of a replaced/deleted group -> page text
for op, i1, i2, j1, j2 in pairs:
    ptxt = ' '.join(w for w, _ in pt[j1:j2])
    if op == 'insert':
        ins_at.setdefault(i1, []).append(ptxt)
    else:
        rep_end[i2 - 1] = (op, ptxt)
heading_of = []; cur = ''
for b in D:
    if b['kind'].startswith('Heading'): cur = norm(b['text'])
    heading_of.append(cur)
blocks_html = []
by_block = {}
for i, (w, bi) in enumerate(dt):
    by_block.setdefault(bi, []).append(i)
for bi, b in enumerate(D):
    parts = []
    for i in by_block.get(bi, []):
        for s in ins_at.get(i, []):
            parts.append(f'<span class="add" title="On the page, not in the document">＋ page has: {E(s)}</span>')
        w = dt[i][0]
        parts.append(f'<mark>{E(w)}</mark>' if dflag[i] else E(w))
        if i in rep_end:
            op, ptxt = rep_end[i]
            parts.append(f'<span class="pg">{"page has: " + E(ptxt) if ptxt else "missing on the page"}</span>')
    if bi == len(D) - 1 and len(dt) in ins_at:
        for s in ins_at[len(dt)]:
            parts.append(f'<span class="add">＋ page has: {E(s)}</span>')
    k = b['kind']
    tag = 'h1' if k == 'Heading1' else 'h2' if k == 'Heading2' else 'h3' if k == 'Heading3' else 'h4' if k == 'Heading4' else 'p'
    cls = ' class="cell"' if k == 'table cell' else ''
    blocks_html.append(f'<{tag}{cls}>{" ".join(parts)}</{tag}>')
sumrows = ''.join(
    f'<tr><td>{n + 1}</td><td><span class="tag t{r["type"].split()[0].lower()}">{E(r["type"])}</span></td><td>{E(heading_of[r["doc_block"]] if r["doc_block"] < len(heading_of) else "")}</td>'
    f'<td>{("…" + E(r["ctx_before"][-60:]) + " ") if r["ctx_before"] else ""}<mark>{E(r["doc"][:260]) or "—"}</mark></td><td class="pgc">{E(r["page"][:260]) or "— (not on page)"}</td></tr>'
    for n, r in enumerate(rows))
page_html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Radiology Content Check</title>
<style>
:root{{--bg:#fff;--ink:#14212B;--muted:#5b6670;--line:#e3e8ee;--mark:#FFE58A;--pg:#E8F1FB;--pgink:#0B4F86;--add:#E6F4DA;--addink:#2F5E12;--head:#F6F8FA}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#12171c;--ink:#e6edf3;--muted:#9aa7b2;--line:#2a333c;--mark:#7a6420;--pg:#163049;--pgink:#9fcaf2;--add:#1f3a14;--addink:#b9e39a;--head:#1a2128}}}}
:root[data-theme="dark"]{{--bg:#12171c;--ink:#e6edf3;--muted:#9aa7b2;--line:#2a333c;--mark:#7a6420;--pg:#163049;--pgink:#9fcaf2;--add:#1f3a14;--addink:#b9e39a;--head:#1a2128}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:980px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-size:26px;line-height:1.25;margin:0 0 6px}} .doc h1{{font-size:22px}} h2{{font-size:20px;margin:28px 0 8px}} h3{{font-size:17px;margin:20px 0 6px}} h4{{font-size:15px;margin:14px 0 4px}}
.lead{{color:var(--muted);margin:0 0 18px}}
.legend{{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 22px;font-size:13px}}
mark{{background:var(--mark);color:inherit;padding:0 2px;border-radius:3px}}
.pg{{background:var(--pg);color:var(--pgink);font-size:13px;padding:1px 6px;border-radius:4px;margin-left:4px}}
.add{{display:inline-block;background:var(--add);color:var(--addink);font-size:13px;padding:2px 8px;border-radius:4px;margin:2px 0}}
.wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:8px}}
table{{border-collapse:collapse;width:100%;min-width:720px;font-size:13.5px}} th,td{{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}
th{{background:var(--head)}} .pgc{{color:var(--pgink)}}
.tag{{font-size:12px;padding:1px 7px;border-radius:999px;background:var(--head);white-space:nowrap}}
.doc{{border:1px solid var(--line);border-radius:10px;padding:8px 20px 20px;margin-top:10px}}
.cell{{display:inline-block;margin:2px 10px 2px 0;padding:2px 8px;border:1px dashed var(--line);border-radius:6px;font-size:13.5px}}
</style></head><body><main>
<h1>Radiology page vs. content document</h1>
<p class="lead">Live page <a href="https://medcaredemo.online/medcare/specialties/radiology/">/specialties/radiology/</a> compared word-for-word with “Radiology Billing Services.docx”. Missing or joined spaces count as differences. Straight vs curly quotes are ignored, because WordPress converts them when it displays text.</p>
<div class="legend"><span><mark>highlighted</mark> = document text that differs on the page</span><span class="pg">page has: …</span><span class="add">＋ page has: … (only on the page)</span></div>
<h2>{len(rows)} differences</h2>
<div class="wrap"><table><tr><th>#</th><th>Type</th><th>Section</th><th>Document</th><th>Page</th></tr>{sumrows}</table></div>
<h2>Full document with differences highlighted</h2>
<div class="doc">{"".join(blocks_html)}</div>
</main></body></html>'''
open(out + '.html', 'w').write(page_html)
print('report', out + '.html')
