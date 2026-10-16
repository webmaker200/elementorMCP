# Challenges Single Page — build notes

- Page: WP page **411126** `/challenges-single-page/`, Figma `oYqLJMmgAjdLKQeLgtDSM7` node **656:14**.
- Builder: `tools/chal.py` (reuses the Salus helpers in `handoff/salus/tools/salus.py`); deploy with `build_chal.py`.
- Section "Why your claims keep getting denied" uses the layout from the user's screenshot (definition box, numbered reason cards, dark cost card, numbered steps) in this design's palette; the Figma doctor photo is not used there.
- Backgrounds: `bg.py` + `slice.py` (Figma blurred ellipses → one WebP per section, background-size 100% 100%); the two blue banners are rendered from the Figma radial gradient + blurred green ring.
- Icons: `mksvg.py` builds SVGs from Figma vector geometry (REST `geometry=paths`), so no image-export quota is needed.
- FAQ: native `e-accordion` (details/summary, FAQPage schema on). The +/× icon is an inline SVG with a one-line style that rotates it 45° when the item is open (the built-in rule only rotates 180°).
- The page may be edited in the Elementor editor later; for small changes prefer `elementor-manage-elements` over re-running the builder.
