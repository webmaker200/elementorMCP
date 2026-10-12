import json,sys
d=json.load(open('salus/mock_geo.json'))['nodes']['626:3455']['document']
idx={}
def w(n):
    idx[n['id']]=n
    for k in n.get('children',[]): w(k)
w(d)
def col(p,op=1):
    c=p['color']; a=c.get('a',1)*p.get('opacity',1)*op
    return f"#{round(c['r']*255):02X}{round(c['g']*255):02X}{round(c['b']*255):02X}", a
def svg(fid, pad=0, extra_op=1):
    f=idx[fid]; fb=f['absoluteBoundingBox']; W,H=fb['width'],fb['height']
    out=[]
    def walk(n,op):
        if n.get('visible',True) is False: return
        op=op*n.get('opacity',1)
        rt=n.get('relativeTransform'); b=n.get('absoluteBoundingBox')
        if 'fillGeometry' in n or 'strokeGeometry' in n:
            # absolute transform: use absoluteTransform if present else bbox origin
            at=n.get('absoluteTransform') 
            if at: tr=f'matrix({at[0][0]} {at[1][0]} {at[0][1]} {at[1][1]} {at[0][2]-fb["x"]+pad} {at[1][2]-fb["y"]+pad})'
            else: tr=f'translate({b["x"]-fb["x"]+pad} {b["y"]-fb["y"]+pad})'
            for g in n.get('fillGeometry',[]):
                for p in n.get('fills',[]):
                    if p.get('visible',True) and p['type']=='SOLID':
                        c,a=col(p,op); out.append(f'<path transform="{tr}" d="{g["path"]}" fill="{c}"'+(f' fill-opacity="{a:.3g}"' if a<1 else '')+(f' fill-rule="evenodd"' if g.get('windingRule')=='EVENODD' else '')+'/>')
            for g in n.get('strokeGeometry',[]):
                for p in n.get('strokes',[]):
                    if p.get('visible',True) and p['type']=='SOLID':
                        c,a=col(p,op); out.append(f'<path transform="{tr}" d="{g["path"]}" fill="{c}"'+(f' fill-opacity="{a:.3g}"' if a<1 else '')+'/>')
        for k in n.get('children',[]): walk(k,op)
    walk(f,extra_op)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W+2*pad:g}" height="{H+2*pad:g}" viewBox="0 0 {W+2*pad:g} {H+2*pad:g}" fill="none">'+''.join(out)+'</svg>'
if __name__=='__main__':
    print('absT' , 'absoluteTransform' in idx['626:3608'], list(idx['626:3608'].keys()))
    for fid,name in [('626:3607','wave'),('626:3552','doc'),('626:3593','check-mint'),('626:3681','logo-mark')]:
        s=svg(fid); open(f'salus/up/salus-{name}.svg','w').write(s); print(name,len(s))
