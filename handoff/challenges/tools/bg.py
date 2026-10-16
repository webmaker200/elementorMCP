import json, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
d=json.load(open('chal/geo.json')); root=d['nodes']['656:14']['document']; R=root['absoluteBoundingBox']
S=4  # px per output px
W,H=1920,6101; PAD=900
idx={}
def walk(n,anc):
    idx[n['id']]=(n,anc)
    for k in n.get('children',[]): walk(k,anc+[n])
walk(root,[])
def bb(n):
    b=n['absoluteBoundingBox']; return (b['x']-R['x'],b['y']-R['y'],b['width'],b['height'])
cw,ch=(W+2*PAD)//S,(H+2*PAD)//S
def mask_ellipse(n):
    x,y,w,h=bb(n); sw,sh=n['size']['x'],n['size']['y'] if isinstance(n.get('size'),dict) else (w,h)
    sw,sh=n['size']['x'],n['size']['y']
    cx,cy=(x+w/2+PAD)/S,(y+h/2+PAD)/S
    big=int(max(sw,sh)/S*1.6)+4
    im=Image.new('L',(big,big),0); dr=ImageDraw.Draw(im)
    dr.ellipse([big/2-sw/S/2,big/2-sh/S/2,big/2+sw/S/2,big/2+sh/S/2],fill=255)
    im=im.rotate(math.degrees(n.get('rotation',0)),resample=Image.BICUBIC)
    m=Image.new('L',(cw,ch),0); m.paste(im,(int(round(cx-big/2)),int(round(cy-big/2))))
    blur=[e['radius'] for e in n['effects'] if e['type']=='LAYER_BLUR'][0]
    m=m.filter(ImageFilter.GaussianBlur(blur/2/S))
    return np.asarray(m,dtype=np.float32)/255
def clip_mask(n):
    x,y,w,h=bb(n); r=n.get('cornerRadius',0)
    m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).rounded_rectangle([(x+PAD)/S,(y+PAD)/S,(x+w+PAD)/S,(y+h+PAD)/S],radius=r/S,fill=255)
    return np.asarray(m,dtype=np.float32)/255
def render(opaque_ids=()):
    C=np.ones((ch,cw,3),np.float32)
    def visit(n):
        if n.get('visible',True) is False: return
        t=n['type']
        if t=='ELLIPSE' and any(e['type']=='LAYER_BLUR' for e in n.get('effects',[])):
            f=[x for x in n.get('fills',[]) if x.get('visible',True) and x['type']=='SOLID']
            if not f: return
            c=f[0]['color']; a=c['a']*f[0].get('opacity',1)*n.get('opacity',1)
            m=mask_ellipse(n)*a
            # clipping by ancestors
            for anc in idx[n['id']][1]:
                if anc.get('clipsContent') and anc['id']!='656:14': m=m*clip_mask(anc)
            col=np.array([c['r'],c['g'],c['b']],np.float32)
            C[:]=C*(1-m[...,None])+col*m[...,None]
            return
        if n['id'] in opaque_ids:
            f=[x for x in n.get('fills',[]) if x.get('visible',True) and x['type']=='SOLID'][0]
            a=f.get('opacity',1)*f['color']['a']; m=clip_mask(n)*a
            col=np.array([f['color']['r'],f['color']['g'],f['color']['b']],np.float32)
            C[:]=C*(1-m[...,None])+col*m[...,None]
        for k in n.get('children',[]): visit(k)
    for k in root['children']:
        if k['id'] in ('656:247','656:308','656:418','656:245','656:246'): continue
        visit(k)
    return C[PAD//S:(PAD+H)//S, PAD//S:(PAD+W)//S]
def save(C,path): Image.fromarray((np.clip(C,0,1)*255+.5).astype(np.uint8)).save(path)
if False:
    A=render(); np.save('salus/bgA.npy',A); save(A,'salus/bg_page.png')
    B=render(('626:2417','626:2424','626:2451','626:2481')); np.save('salus/bgB.npy',B); save(B,'salus/bg_cards.png')
    for i in ['626:2417','626:2424','626:2451','626:2481']: print(i,bb(idx[i][0]),idx[i][0].get('cornerRadius'))
