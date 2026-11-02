# South Carolina state page

Live: https://medcaredemo.online/medcare/states/medical-billing-south-carolina/ (states post **411363**, published).

## How it was built
- Source of copy: Google Doc "Medical Billing Services in South Carolina" (all screenshots in it are California page sections).
- `tools/build_sc.py` copies the California state page (post 386954) sections in the doc's order, swaps in the SC copy,
  regenerates every element id + local style id, and writes `build/sc_data.json`.
- `tools/deploy_sc.py` backs up the current page data to `backup/`, writes the new data via WP REST
  (`meta._elementor_data`), then publish + touch + publish through the Elementor MCP so Elementor regenerates the page CSS.
- Rebuild: `python3 tools/build_sc.py && python3 tools/deploy_sc.py` (auth from `~/.claude.json` or `WP_BASIC_AUTH`).

## Section map (California source element → SC)
Hero + banner form (d8ac86e, form copied as-is, hero bg = media 411365) · KPIs (ad92569) · Outsourced billing (5b8a846) ·
Rules (242f0fb, 5 → 7 cards) · Two tracks (b206976) · Payers (d4a5b2b, 4 → 5 cards, Workers' Comp spans full row) ·
**NEW: Healthy Connections Compliance Rules** (V4, page-local styles) + the "Is every claim…" CTA box moved under it ·
Step-by-step (cbfc466) · Certified coding (e0cbdde) · Specialties (ce0a3b8, unchanged) · EHR carousel (75d5ffd) ·
Built around your specialty (144eabc) · Cities (245b176) · Testimonials `[elementor-template id="388878"]` · FAQ (d303d44, 6 → 7) · Bottom CTA (df3702f).
Skipped (not in the doc): California case study (d60a587) and Google Map embed (42f734d4).

## Media
- 411366 `icon-number07.svg` (new, matches 01–06), 411367 `icon-source-doc.svg` (new section source note).
- City cards: 411379–411388 `<City>-SC.webp` (all < 100 KB, alt "<City>, South Carolina"). Columbia, Charleston, Greenville and
  Spartanburg are 200×200 (only Canva's preview size was downloadable); the other six are 520–600px, re-encoded from the owner's
  uploads 411373–411378 (`south-carolina-cities-images*.webp`, 360–640 KB, now unused).

## Notes for the owner
- Form email subject changed to "… Medical Billing South Carolina"; everything else in the form is as on California.
- Copy kept verbatim from the doc even where it now disagrees with the page: rules heading/intro say "Five" (7 rules), payers intro says "four payer types" (5 cards).
