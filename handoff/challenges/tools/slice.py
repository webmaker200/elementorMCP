import sys,os,numpy as np
sys.path.insert(0,'chal'); import bg
from PIL import Image
A=bg.render(); S=bg.S
Image.fromarray((np.clip(A,0,1)*255+.5).astype(np.uint8)).save('chal/bg_page.png')
os.makedirs('chal/out',exist_ok=True)
cuts=[97,847,2014,2890,4022,4858,5494]; names='hero cost cause fix faq cta'.split()
for n,a,b in zip(names,cuts,cuts[1:]):
    p=f'chal/out/chal-bg-{n}.webp'; Image.fromarray((np.clip(A[a//S:b//S],0,1)*255+.5).astype(np.uint8)).save(p,'WEBP',quality=90,method=6); print(p,os.path.getsize(p))
