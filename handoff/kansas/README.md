# Kansas state page: two new sections

Live: https://medcaredemo.online/medcare/states/medical-billing-kansas/ (states post **412021**, published).
Content doc: Google Doc "Medical Billing Services in Kansas" (1-W7kEGA7sj_G9zKPYNp-9_25pT2pIOr1y78y3FngESg). The designs are the
screenshots above each heading in the doc (image6 and image10 in the DOCX export).

## What was added (V4, no new classes)
| Section | Position | Design |
|---|---|---|
| **Outsourced Medical Billing Services in Kansas from Eligibility to A/R** (`41d1bf9f`) | after "The Numbers Behind Cleaner Kansas Claims" | doc image6 |
| **Medical Billing Services Across Kansas Cities and Regions** (`2947994b`) | after "A Medical Billing Company in Kansas That Fits Your Practice" | doc image10 |

**Outsourced section:**
- H2 and intro.
- Blue band with "Start here: Free billing audit" and "Then: Onboarding in 2–4 weeks".
- 8 step cards with Media Library icons.
- The doc's "Which of these eight steps is costing you the most?" CTA, styled like the page's existing deadlines CTA. Its button carries `data-class="custom-button"`, like the page's other buttons.

**Cities section:**
- H2 and intro.
- Kansas map card with legend (sticky on desktop).
- 5 numbered region cards with the design's Blue plan / Systems details.

**Shared styling:**
- Sections use `parent-container`, headings use `specialties-heading`, intros and CTA text use `global-text`. Everything else is a local style using the kit variables the page already uses (DeepSkyBlue, AzureMist, HealthGreen, DarkGray…).
- Copy is the doc's text word for word, including "If it is NCBSKS denial" (probably meant BCBSKS).
- Links: medcaremso.com links open in the same window. The CTA goes to `/request-demo/?utm_source=medical-billing-kansas`.

## Media
- 412098 `kansas-cities-map-1.svg`: new map drawn by `tools/make_map.py` (real city coordinates; Johnson and Wyandotte shaded as Blue KC). Alt: "Kansas cities served by MedCare MSO medical billing services".
- Step icons (existing): 383393, 410976, 405743, 408704, 386106, 383394, 392595, 411681.

## How it was deployed
1. `tools/ks.py` builds both sections. They were appended with `elementor-build-composition` (this wrote an autosave, because the page is published).
2. `elementor-manage-elements` moved them into place and added the CTA button attribute.
3. `elementor-publish-document` published the page.

Backup of the page before the change: `backup/kansas_412021_before-new-sections_*.json`.
To preview a section before publishing, build it on a temporary draft and inject its rendered HTML into the live page with `tools/preview_inject.js`.

## Hover on existing boxes (2026-11-17)
Same subtle hover as the telehealth page (`scale(1.02)` + soft blue drop shadow, 0.3s), added as a style patch:
- "Kansas Billing Laws and Filing Deadlines We Track for You": e5dbce6, 8087a9d, 0c2c6e8, 1bf1125, bcca53e, 4405aaa (inset shadow kept);
- "Rural Kansas Billing for Critical Access Hospitals, RHCs, and FQHCs": 3ebce4b, 480be57, 765a6bd.
Backup before: `backup/kansas_412021_before-hover.json`. Published; diff showed only these 9 style entries changed.

## "Where Revenue Slips With Each Kansas Payer" redesign (Option A, 2026-11-17)
Three mockups were shown (A: 2 + 3 grouped, B: featured card + 2×2, C: full-width rows); the client picked **A**.
`tools/payer_redesign.py` appended the new block (`5723af0f`) to section b1a29ab and deleted the old grid 5b5aaf7, then published:
- row 1: one wide #E8EFF4 card with a DeepSkyBlue strip ("Two Blue plans, one state: check the home plan first"; this strip
  text is new, not from the doc) and the two Blue plans side by side (BCBSKS | Blue KC, divider between; stacked from 880px);
- row 2: Medicare, Marketplace, Workers' Comp in 3 columns; tablet 2 + 1 full width; mobile stacked;
- same card look, icons and copy as before (build/payer_cards.json); same subtle hover.
Backup before: `backup/kansas_412021_before-payer-redesign.json`; diff showed only section b1a29ab changed.
