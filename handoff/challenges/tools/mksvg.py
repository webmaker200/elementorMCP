import json, numpy as np
d=json.load(open('chal/geo.json'))['nodes']['656:14']['document']
idx={}; ABS={}
def w(n, M):
    rt=n.get('relativeTransform')
    m=M if rt is None else M @ np.array([rt[0],rt[1],[0,0,1]])
    idx[n['id']]=n; ABS[n['id']]=m
    for k in n.get('children',[]): w(k, m)
w(d, np.eye(3))
def col(p, op=1):
    c=p['color']; a=c.get('a',1)*p.get('opacity',1)*op
    return f"#{round(c['r']*255):02X}{round(c['g']*255):02X}{round(c['b']*255):02X}", a
def grad(p, gid, op, bb):
    # linear gradient in object bbox space using handle positions
    h=p['gradientHandlePositions']; st=''.join(f'<stop offset="{s["position"]:.3f}" stop-color="#{round(s["color"]["r"]*255):02X}{round(s["color"]["g"]*255):02X}{round(s["color"]["b"]*255):02X}" stop-opacity="{s["color"].get("a",1)*p.get("opacity",1)*op:.3f}"/>' for s in p['gradientStops'])
    return f'<linearGradient id="{gid}" gradientUnits="objectBoundingBox" x1="{h[0]["x"]:.4f}" y1="{h[0]["y"]:.4f}" x2="{h[1]["x"]:.4f}" y2="{h[1]["y"]:.4f}">{st}</linearGradient>'
def svg(fid, pad=0, recolor=None):
    f=idx[fid]; fb=f['absoluteBoundingBox']; W,H=fb['width'],fb['height']
    ox,oy=fb['x'],fb['y']
    out=[]; defs=[]; gi=[0]
    def paint_attr(p, op, bb):
        if p['type']=='SOLID':
            c,a=col(p,op)
            if recolor: c=recolor
            return f'fill="{c}"'+(f' fill-opacity="{a:.3g}"' if a<0.999 else '')
        if p['type']=='GRADIENT_LINEAR':
            gi[0]+=1; gid=f'g{fid.replace(":","")}{gi[0]}'; defs.append(grad(p,gid,op,bb)); return f'fill="url(#{gid})"'
        return None
    def walk(n, op):
        if n.get('visible',True) is False: return
        op=op*n.get('opacity',1)
        if n is not f and ('fillGeometry' in n or 'strokeGeometry' in n):
            M=ABS[n['id']]
            tr=f'matrix({M[0,0]:.5f} {M[1,0]:.5f} {M[0,1]:.5f} {M[1,1]:.5f} {M[0,2]-ox+pad:.3f} {M[1,2]-oy+pad:.3f})'
            for g in n.get('fillGeometry',[]):
                for p in n.get('fills',[]):
                    if p.get('visible',True)==False: continue
                    a=paint_attr(p,op,None)
                    if a: out.append(f'<path transform="{tr}" d="{g["path"]}" {a}'+(' fill-rule="evenodd"' if g.get('windingRule')=='EVENODD' else '')+'/>')
            for g in n.get('strokeGeometry',[]):
                for p in n.get('strokes',[]):
                    if p.get('visible',True)==False: continue
                    a=paint_attr(p,op,None)
                    if a: out.append(f'<path transform="{tr}" d="{g["path"]}" {a}/>')
        for k in n.get('children',[]): walk(k, op)
    walk(f, 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W+2*pad:g}" height="{H+2*pad:g}" viewBox="0 0 {W+2*pad:g} {H+2*pad:g}" fill="none">'
            + (f'<defs>{"".join(defs)}</defs>' if defs else '') + ''.join(out) + '</svg>')
