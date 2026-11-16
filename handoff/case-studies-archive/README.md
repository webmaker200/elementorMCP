# Case studies archive (demo page 412016)

Draft page `case-studies-archive-demo`, built so it can later be set as the case-study archive template.
Edit: https://medcaredemo.online/medcare/wp-admin/post.php?post=412016&action=elementor

Built in Elementor V4 from *Case Study Design Brief _ Case Studies copy.html*. Same rules as the Golden State case study:
- design text word for word, no header/footer;
- no new classes (`parent-container`, `heading-main`, `specialties-heading`, `global-text` plus local styles);
- percentage widths, no flex-basis;
- Media Library images;
- simple hovers.

## Sections
1. **Hero:** breadcrumb, "Case studies" H1, two CTA pills, and the floating C&CCC KPI card.
   - "Browse case studies" jumps to `#library`.
   - "Talk to a billing expert" goes to `/request-demo/`.
   - The portrait is a section background with the design's edge fades baked into a transparent WebP.
2. **Featured · Newest:** the Golden State card. The whole card is one link.
3. **All case studies (`#library`):** V4 tabs (All 11, A/R recovery 3, Billing & collections 5, Denial management 1, Credentialing 1, AI coding 1). Each tab holds its own card grid built from the design's data (`CASES` in `tools/csa.py`).
4. **Callback band (`#callback`):** "Request demo", phone and email.

## Deviations from the design
- The design filters with JavaScript. V4 has no script widget, so each filter is a V4 tab with its own copy of the cards. Adding a new study means adding a card to the All tab and to its category tab, or adding it to `CASES` and rebuilding.
- The design's "Show all 11 case studies" toggle needs JavaScript too, so the All tab simply shows all 11 cards.
- The header-pill floating animation (CSS keyframes) can't be stored in V4 local styles. The KPI card lifts on hover instead.
- **ODAT Services** has no post or image on the demo site. Its card links to the production URL from the design and uses a neutral Media Library photo (411229). Swap the image when the study is added.

## Media
| | ID |
|---|---|
| Hero portrait (transparent WebP, 31 KB) | 412015 |
| Cardiac stress test team (WebP, 44 KB) | 412014 |
| Card thumbnails (existing) | 409632, 411229, 401725, 399625, 397968, 397387, 395073, 392590, 390987, 395040 |
| Arrows (blue / white) | 410969 / 411130 |

## Rebuild / preview
```
python3 tools/run_build.py        # replace_children on 412016 ("dry" to validate)
```
Preview a draft offline with `../golden-state-case-study/tools/preview_render.js` (see that README).

## To use it as the archive
In Theme Builder, create an Archive template for Case Studies, then copy this page's content into it. Alternatively, set this page as the "Case studies" landing page.
