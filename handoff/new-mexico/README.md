# New Mexico state page

Live: https://medcaredemo.online/medcare/states/medical-billing-new-mexico/ (states post **411391**, published,
featured image 411390 `New-Mexico-State-Card-328x333`).

Content doc: Google Doc "Medical Billing Services in New Maxico - Final". Every section has a screenshot of an existing
state-page section (New York, Texas, California); no section is highlighted as new, so nothing was designed from scratch.

## Rebuild
`python3 tools/build_nm.py && python3 tools/deploy_nm.py` (auth from `~/.claude.json` or `WP_BASIC_AUTH`).
deploy backs up the current page data to `backup/`, writes `build/nm_data.json` via WP REST, then publish → touch → publish
through the Elementor MCP so Elementor regenerates the page CSS.

## Section map (doc screenshot → source section)
| NM section | Source |
|---|---|
| Hero + "Talk to a Billing Expert" | NY 6f2914b3 (no form, as in the screenshot) |
| Proof … KPIs + "Ninety Days Go Fast" | TX d2e03a9 |
| Payer mix | NY 5fefeab8 (list removed: no list in the copy) |
| State-specific rules (5 cards) | TX 1d90565 (5th card spans the row; TX claims-review CTA removed: no copy) |
| Native American / IHS / 638 + coverage table | CA d60a587 case-study layout (table shown on mobile, scrolls sideways) |
| Medical Billing and RCM Services | NY 1f43affa |
| Billing needs (5 slides) | NY 5ca4fc10 + 5cd48903 nested carousel (1 slide on phones) |
| Gross receipts tax (2 cards) | TX 0497ce3 |
| Specialties | TX dfc38cd |
| Practices we support + map | TX 255873b (map = MedCare MSO office, same as TX) |
| Areas we serve (10 cities) | TX ca019d2 |
| Support system (2 cards) | NY 3731fb77 |
| Testimonials `[elementor-template id="388878"]` | TX e020f87 (not in the doc; on every state page) |
| FAQ (5) | TX e7635f0 |
| Give Your Team More Time … CTA | TX b7c86b8 |

## Pending images
- Hero background is still the New York banner (387370) — no New Mexico hero in the Media Library.
  Upload one and add `"hero": {"id": <id>, "url": "<url>"}` to `media.json`, then rebuild.
- City cards still show the Texas photos. Upload `<City>-NM.webp` files (e.g. `Las-Cruces-NM.webp`), add them to
  `media.json` as `{"<City>-NM.webp": {"id": …, "url": …}}`, then rebuild — the builder swaps them in by name.
