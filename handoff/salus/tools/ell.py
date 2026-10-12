import json,sys
d=json.load(open('salus/node.json'))
root=d['nodes']['626:2408']['document']
R=root['absoluteBoundingBox']; print('root',R, root.get('fills'))
out=[]
def walk(n,depth=0,path=''):
    if n.get('visible',True) is False: return
    if n['type']=='ELLIPSE' and any(e['type']=='LAYER_BLUR' and e.get('visible',True) for e in n.get('effects',[])):
        f=[x for x in n.get('fills',[]) if x.get('visible',True)]
        bb=n['absoluteBoundingBox']; rb=n.get('absoluteRenderBounds')
        c=f[0].get('color') if f else None
        out.append(dict(id=n['id'],path=path,x=bb['x']-R['x'],y=bb['y']-R['y'],w=bb['width'],h=bb['height'],size=n.get('size'),rot=n.get('rotation',0),
          col=[round(c['r']*255),round(c['g']*255),round(c['b']*255)] if c else None,a=(c['a'] if c else 0)*f[0].get('opacity',1)*n.get('opacity',1) if f else 0,
          blur=[e['radius'] for e in n['effects'] if e['type']=='LAYER_BLUR'][0], ftype=f[0]['type'] if f else None))
    for k in n.get('children',[]): walk(k,depth+1,path+'/'+n['name'][:15])
walk(root)
json.dump(out,open('salus/ellipses.json','w'),indent=0)
for e in out: print(e['id'],e['path'][-40:],round(e['x']),round(e['y']),round(e['w']),round(e['h']),e['size'] and [round(v) for v in e['size'].values()],round(e['rot'],3),e['col'],round(e['a'],3),e['blur'],e['ftype'])
