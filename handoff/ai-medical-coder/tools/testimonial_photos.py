"""Re-style the site's testimonial photos for the Sophus page (originals stay untouched in the Media Library).

The originals are greyscale portraits on a flat green (#7EB63F) background; the design's photo sits on a soft,
cool-grey studio background. This keys out the green (with colour un-mixing on the edges), puts the person on
that grey gradient and saves a 680x860 WebP per person.
Usage: testimonial_photos.py <dir with orig_<id>.* files> <out dir>
"""
import glob, os, sys
import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
GREEN = np.array([126.0, 182.0, 63.0])
W, H = 680, 860


def backdrop():
    y = np.linspace(0, 1, H)[:, None, None]
    top, bottom = np.array([206.0, 209.0, 209.0]), np.array([166.0, 174.0, 188.0])
    g = top * (1 - y) + bottom * y
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - W * 0.5) / (W * 0.45)) ** 2 + ((yy - H * 0.3) / (H * 0.35)) ** 2))[..., None]
    g = g + glow * 14.0  # soft light behind the head, like a studio backdrop
    return np.repeat(g, W, axis=1) if g.shape[1] == 1 else g


def cutout(path):
    im = np.asarray(Image.open(path).convert('RGB'), dtype=float)
    im = im[10:-10, 10:-10]  # drop the rounded corners some originals have
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    greenness = g - (r + b) / 2  # ~120 on the backdrop, ~0 on the greyscale person
    alpha = np.clip((95 - greenness) / 55, 0, 1)
    a = Image.fromarray((alpha * 255).astype('uint8')).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    alpha = np.asarray(a, dtype=float) / 255
    # un-mix the green from edge pixels, then keep the person greyscale like the original
    safe = np.maximum(alpha, 0.05)[..., None]
    fg = np.clip((im - (1 - safe) * GREEN) / safe, 0, 255)
    grey = (0.5 * fg[..., 0] + 0.5 * fg[..., 2])  # red/blue only: green is the contaminated channel
    fg = np.repeat(grey[..., None], 3, axis=2)
    return fg, alpha


bd = backdrop()
for f in sorted(glob.glob(os.path.join(SRC, 'orig_*'))):
    mid = os.path.basename(f).split('_')[1].split('.')[0]
    fg, alpha = cutout(f)
    fgi = Image.fromarray(fg.astype('uint8')).resize((W, round(fg.shape[0] * W / fg.shape[1])), Image.LANCZOS)
    ai = Image.fromarray((alpha * 255).astype('uint8')).resize(fgi.size, Image.LANCZOS)
    fgi = fgi.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    canvas = Image.fromarray(np.clip(bd, 0, 255).astype('uint8'))
    y0 = H - fgi.size[1]  # bottom-aligned, like the design
    canvas.paste(fgi, (0, y0), ai)
    out = os.path.join(OUT, f'sophus-testimonial-{mid}.webp')
    canvas.save(out, 'WEBP', quality=86, method=6)
    print(out, os.path.getsize(out))
