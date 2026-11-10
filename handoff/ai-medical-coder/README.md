# AI Medical Coder (Sophus) page

WP page **411494**, slug `ai-medical-coder`, built with Elementor V4 atomic elements from the `Sophus_AI_Web_Page_v2_1.html` design.
The site header, footer and orange "Schedule a free Demo" band come from the site templates and aren't part of this build.

- Live: https://medcaredemo.online/medcare/ai-medical-coder/
- Edit: https://medcaredemo.online/medcare/wp-admin/post.php?post=411494&action=elementor

## Sections
1. Hero with a Coder view / Manager view switch (V4 tabs) that shows the dashboard images.
2. KPI strip.
3. "What Sophus does" (`#how`): claim card plus a V4 accordion.
4. Speed: lines graphic, chips and the "0:32" figure.
5. Manager band.
6. Roles tabs: Coders / Coding managers / Billing companies.
7. Performance cards.
8. Marquee with floating cards. The cards hide below 1024px.
9. Testimonials: the site's 5 real testimonials and photos, with a prev/next slider.
10. Demo form (`#demo`, V4 form) and the Sophus AI wordmark.

## Conventions
- Every section uses the site class `parent-container` and has no local padding.
- Type uses the site classes `heading-main`, `specialties-heading`, `heading-h3`, `global-text` and `global-btn`. Columns use `w-45`/`w-50` (percentage widths, no flex-basis).
- Colours are hex values, not HealUs variables, so the page still works when copied to the live site.
- Every tab has hover, selected (`aria-selected`) and keyboard-focus (`:focus-visible`) states. Buttons, cards, chips, form fields and slider arrows have hover states.
- A small V3 HTML widget at the end of the testimonial section (`sophus-page-js`) holds what V4 styles can't:
  - the page background glows from the design (three glow images, `sophus-glow-*-sm`);
  - the marquee animation (CSS only);
  - the testimonial slider script, marked `nowprocket` so WP Rocket doesn't delay it.
  The widget finds its targets from the page structure, not element or page IDs, so it keeps working when the page is copied to the live site. Don't delete it.
- The roles section and the demo form panel are capped at 1160px wide. The speed-section lines span the full viewport width.
- The form emails mkamran@ and fashraf@medcaremso.com from email@medcaremso.com ("MedCare MSO"), the same recipients as the state-page forms, and also saves submissions.

## Rebuild
`tools/rebuild.sh` runs these steps in order:
1. `run_build.py`: build-composition with `replace_children`, then publish (a published page receives the build as an autosave).
2. Fetch the stored data.
3. `postprocess.py`: add the slider/keyframes widget.
4. `deploy_coder.py`: back up, write, touch and publish.

Assets come from `tools/prep_assets.py` and are uploaded by `tools/upload_assets.py`. Their Media Library IDs are listed in `media.json`.
