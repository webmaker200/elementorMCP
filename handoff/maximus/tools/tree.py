import json,sys,re
def txt(s):
    for k in ('title','paragraph','text'):
        v=s.get(k)
        if isinstance(v,str): return re.sub('<[^>]+>','',v)[:70]
    return ''
def show(n,d=0,css=False):
    s=n.get('settings',{}) or {}
    cls=[c for c in s.get('classes',[]) if not c.startswith('e-')]
    t=n.get('widgetType') or n.get('elType')
    extra=''
    if s.get('link',{}).get('href'): extra+=' href='+s['link']['href'][:60]
    for k in ('image','svg','src'):
        if k in s: extra+=f' {k}='+json.dumps(s[k])[:120]
    print('  '*d+f"{t} [{n['id']}] tag={n.get('tag','')} cls={cls} {txt(s)!r}{extra}")
    if css and isinstance(n.get('styles'),dict) and n['styles'].get('css'): print('  '*d+'   css: '+n['styles']['css'].replace('\n',' | ')[:400])
    for c in n.get('elements',[]): show(c,d+1,css)
f=json.load(open(sys.argv[1])); css=len(sys.argv)>2
for i,r in enumerate(f):
    print(f'===== ROOT {i}')
    if 'error' in r: print(r); continue
    for e in r['elements']: show(e,0,css)
