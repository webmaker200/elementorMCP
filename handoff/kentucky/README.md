# Kentucky state page

Live: https://medcaredemo.online/medcare/states/medical-billing-kentucky/ (states post **411410**, published).
Content doc: "Medical Billing Services in Kentucky.docx" (Drive 1Tz80V7XjagAslhG9MSd2v0YRunlSvFDl).

All screenshots in the doc are California state-page sections; the one yellow-highlighted section,
**Kentucky Medicaid Billing Rules We Code To**, is new (V4, page-local styles, design = doc image14). The other yellow
item, the FAQ "Do we have to enroll with Kentucky Medicaid…", is added to the copied FAQ (6 → 7).

Rebuild: `python3 tools/build_ky.py && python3 tools/deploy_ky.py`.

Changes vs California: laws grid 5 → 6 cards (all half width), payers 4 cards, claims-review CTA moved under the new
section, case study and Google Map left out (not in the doc), testimonials shortcode kept as on every state page.

## Pending images
- Hero background: still California's (376853). Add `"hero": {"id": …, "url": …}` to `media.json` and rebuild.
- City cards: California photos. Add `"<City>-KY.webp": {"id": …, "url": …}` entries to `media.json` and rebuild.
- Featured image: not set (set it on the post: `featured_media`).
