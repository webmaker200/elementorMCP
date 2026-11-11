# Behavioral Health Billing Services (specialty 411549)

Live: https://medcaredemo.online/medcare/specialties/behavioral-health-billing-services/
Edit: https://medcaredemo.online/medcare/wp-admin/post.php?post=411549&action=elementor
Content: Google Doc "Behavioral Health Billing Services" (1D3qOwNd_N6SYib9q0iMeHc3H0AfywvxKpWzAiZwe4EY)

## Why V4
The Specialties post type (ACF post type 4510) does not support custom fields, so Elementor's `_elementor_data` can't be read
or written from outside the editor (REST / XML-RPC). V3 sections could not be copied in; the page is built in V4 with
`elementor-build-composition`, copying the styling of the Anesthesia specialty (410669). To allow V3 copying in future:
ACF -> Post Types -> Specialties -> Supports -> tick Custom Fields (backup of the current setting in `backup/`).

## Sections
Hero + audit form (Dental-style) / Why billing breaks down (6 cards) / Authorization CTA box / Levels of care (8 cards) /
End-to-end RCM (10 cards) / Codes table / Compliance / Payers (blue cards) / Who we serve / AI ecosystem / EHR logos /
Why choose (checklist + image) / 4 steps / FAQ (FAQ schema) / Final CTA bar.
- Skipped on request: "Behavioral Health Billing Results" (KPIs + case-study card).
- Testimonials: the site carousel is a V3 template (`[elementor-template id="388878"]`); V4 has no shortcode widget, so it is
  added in the editor with a Shortcode widget between "How We Take Over" and the FAQ.

## Details
- CTA buttons: `data-class="custom-button"` (set by `tools/post_build.py`), link to medcaremso.com/request-demo/?utm_source=behavioral-health-billing-services, same window.
- Links in copy go to medcaremso.com pages (same site, same window); no external links in the doc.
- Form: V4 form -> email to mkamran@ / fashraf@medcaremso.com from email@medcaremso.com, plus saved submissions.
- Listing: featured image = new icon `assets/behavioral-health-billing-services.svg` (media 411551); ACF display-name "Behavioral Health"; specialty_rank empty (shows first).
- Yoast title/description set from the doc.

## Rebuild
`python3 tools/run_build.py && python3 tools/post_build.py` (replace_children; the editor-added testimonial widget would need re-adding).
