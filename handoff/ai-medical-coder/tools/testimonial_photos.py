"""Re-style the site's testimonial photos for the Sophus page (originals stay untouched in the Media Library).

The originals are greyscale portraits on a flat green (#7EB63F) background; the design's photo sits on a soft,
cool-grey studio background. This keys out the green (un-mixing it from the edge pixels), puts the person on
that grey gradient and saves a 680x860 WebP per person. Pillow only.
Usage: testimonial_photos.py <dir with orig_<id>.* files> <out dir>
"""
import glob, math, os, sys
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
GR, GG, GB = 126.0, 182.0, 63.0
W, H = 680, 860


def backdrop():
    top, bottom = (206, 209, 209), (166, 174, 188)
    img = Image.new('RGB', (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        base = [top[k] * (1 - t) + bottom[k] * t for k in range(3)]
        dy = ((y - H * 0.3) / (H * 0.35)) ** 2
        for x in range(W):
            glow = 14.0 * math.exp(-(((x - W * 0.5) / (W * 0.45)) ** 2 + dy))  # soft light behind the head
            px[x, y] = tuple(min(255, int(base[k] + glow)) for k in range(3))
    return img


def cutout(path):
    im = Image.open(path).convert('RGB')
    im = im.crop((10, 10, im.size[0] - 10, im.size[1] - 10))  # drop the rounded corners some originals have
    w, h = im.size
    src = im.load()
    alpha = Image.new('L', (w, h))
    a = alpha.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            greenness = g - (r + b) / 2  # ~120 on the backdrop, ~0 on the greyscale person
            a[x, y] = int(255 * min(1.0, max(0.0, (95 - greenness) / 55)))
    alpha = alpha.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    a = alpha.load()
    fg = Image.new('L', (w, h))
    f = fg.load()
    for y in range(h):
        for x in range(w):
            al = max(a[x, y] / 255, 0.05)
            r, g, b = src[x, y]
            # un-mix the green; red / blue only, since green is the contaminated channel
            rr = (r - (1 - al) * GR) / al
            bb = (b - (1 - al) * GB) / al
            f[x, y] = int(min(255, max(0, (rr + bb) / 2)))
    return fg.convert('RGB'), alpha


bd = backdrop()
for path in sorted(glob.glob(os.path.join(SRC, 'orig_*'))):
    mid = os.path.basename(path).split('_')[1].split('.')[0]
    fg, alpha = cutout(path)
    size = (W, round(fg.size[1] * W / fg.size[0]))
    fg = fg.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    alpha = alpha.resize(size, Image.LANCZOS)
    canvas = bd.copy()
    canvas.paste(fg, (0, H - size[1]), alpha)  # bottom-aligned, like the design
    out = os.path.join(OUT, f'sophus-testimonial-{mid}.webp')
    canvas.save(out, 'WEBP', quality=86, method=6)
    print(out, os.path.getsize(out))
