# Golden State Heart & Vascular case study (post 411939)

Post type `case-study`, slug `golden-state-heart-vascular-aged-ar-recovery`, **draft**.
Edit: https://medcaredemo.online/medcare/wp-admin/post.php?post=411939&action=elementor

Built in Elementor V4 from *Case Study Design Brief _ Golden State Case Study v3.html* (content word for word, site header/footer not included).

- No new global classes. Sections use `parent-container`, H1 `heading-main`, H2 `specialties-heading`, copy `global-text`; everything else is a local style on the element.
- Columns use percentage widths (no flex-basis). Card grids use e-grid tracks with tablet/mobile columns. The results table scrolls sideways under 720px.
- Section anchors are `#summary`, `#challenge`, `#solution`, `#results` and `#contact`. The solution nav links to `#step-01`..`#step-05`; the nav is sticky on desktop and hidden on mobile.
- "Book a demo" and "Call us" carry `data-class="custom-button"` (site CTA animation).
- Hover effects:
  - glass cards lift;
  - challenge icons scale;
  - CTA pills fill;
  - nav pills, table rows and contact rows highlight.

## Media (all in the Media Library)
| | ID |
|---|---|
| Banner `golden-state-cardiac-stress-test.webp` (1000x1200, 77 KB, cropped 5:6 from the supplied photo) | 411941 |
| Challenge icons 01-06 | 406661, 411694, 403764, 411682, 403657, 411684 |
| Arrow teal / arrow white / check | 411264 / 411130 / 410377 |

## Rebuild
```
python3 tools/run_build.py        # replace_children on 411939 (add "dry" to validate only)
python3 tools/post_build.py       # CTA data-class attributes
```

## V4 gotchas handled in gs.py
- e-grid's base style adds `grid-template-rows: repeat(2, 1fr)`, which creates an empty second row. Every grid sets `grid-template-rows: auto`.
- e-div-block's base adds `padding: 10px; min-width: 30px`, so box() resets both.

## Preview without publishing
Drafts can't be opened from outside (the preview token 404s). `preview_render.js` loads a live V4 page, swaps in this post's rendered HTML (REST `content.rendered`) and the element styles (`elementor-get-page-structure` → `preview_css.py`), then screenshots it. `preview_globals.css` approximates the site classes.
