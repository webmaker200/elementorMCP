import sys,os,json,numpy as np
sys.path.insert(0,'salus'); import bg
from PIL import Image
A=np.load('salus/bgA.npy'); B=np.load('salus/bgB.npy')
C=bg.render(('626:2417',))
S=bg.S; os.makedirs('salus/out',exist_ok=True)
def im(X): return Image.fromarray((np.clip(X,0,1)*255+.5).astype(np.uint8))
cuts=[97,963,2206,3227,4634,5466,6826,7861,8926]; names='hero see does pricing addons compare why cta'.split()
for n,a,b in zip(names,cuts,cuts[1:]):
    p=f'salus/out/salus-bg-{n}.webp'; im(A[a//S:b//S]).save(p,'WEBP',quality=90,method=6); print(p,os.path.getsize(p))
def crop(X,x,y,w,h,name):
    p=f'salus/out/salus-bg-{name}.webp'; im(X[y//S:(y+h)//S, x//S:(x+w)//S]).save(p,'WEBP',quality=90,method=6); print(p,os.path.getsize(p))
crop(C,142,3588,1636,962,'pricing-panel'); crop(B,700,3608,521,836,'pricing-pro')
