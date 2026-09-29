# Maximus AI Product page — handoff

Build the Figma design **"Maximus"** as the WordPress page **"Maximus AI Product"** with Elementor V4 (Atomic), 100% visual match, then publish.

## Targets
| What | Value |
|---|---|
| Site | https://medcaredemo.online/medcare/ (WordPress + Elementor V4 atomic, Elementor Pro) |
| Page | ID **410364**, post_type `page`, title "Maximus AI Product", currently **draft**, blank Elementor canvas |
| Figma file | key `oYqLJMmgAjdLKQeLgtDSM7`, frame **599:1630** "Maximus" (1920 × 11165) |
| Figma URL | https://www.figma.com/design/oYqLJMmgAjdLKQeLgtDSM7/MedCare-Designs-Copied?node-id=599-1630 |
| Elementor MCP | `https://medcaredemo.online/medcare/wp-json/elementor/mcp/` (HTTP, Basic auth) |

## Credentials (never commit)
- `FIGMA_TOKEN` — Figma personal access token (env). Use the **Figma REST API**, not the Figma MCP: the MCP is on the Starter plan and its monthly tool-call limit is exhausted.
  - `GET https://api.figma.com/v1/files/oYqLJMmgAjdLKQeLgtDSM7/nodes?ids=599:1631,...&geometry=paths` → exact fills/strokes/effects/typography/auto-layout per node.
  - `GET https://api.figma.com/v1/images/oYqLJMmgAjdLKQeLgtDSM7?ids=...&format=svg|png&scale=2` → export URLs.
  - `GET https://api.figma.com/v1/files/oYqLJMmgAjdLKQeLgtDSM7/images` → original image fills.
  - Header: `X-Figma-Token: $FIGMA_TOKEN`. `www.figma.com` and `api.figma.com` must be reachable (www.figma.com was allowlisted).
- WordPress: `tools/mcp.py` reads `WP_BASIC_AUTH` (base64 of `user:application_password`) from env.

## User's rules (apply to everything)
- Brand-new page → follow Figma 100%. Figma colors are used as **page-scoped local styles**; do **not** add/modify global classes, global variables, kit, header, footer, templates or other pages.
- Build only the 10 content sections. The site's global header, footer and orange "Schedule a free Demo" band already wrap the page (the Figma frame also contains them — skip those: header 599:3103, demo band 599:4003, footer 599:3893).
- Native V4 atomic elements, clean shallow DOM, no spacers/empty elements, one H1, logical H2/H3.
- **Images → WebP**, sized ~2× display width, keep file sizes small. **Icons/logos/simple vectors → SVG.** Upload to the Media Library (REST `POST /wp/v2/media`).
- Responsive check at 1920, 1750, 1600, 1440, 1366, 1200, 1024, 870, 430 (only a 1920 desktop frame exists — design the other breakpoints faithfully).
- Forms: build the demo form with V4 `e-form`; do **not** configure delivery (email/CRM actions) — tell the user it needs connecting. The Figma note "Prototype form only. Connect to your CRM…" is a designer note, not page copy.
- Publish only when done; report the preview URL.

## Elementor MCP / site facts learned the hard way
- Tools used: `elementor-build-composition` (XML + element_config + style + classes), `elementor-manage-elements`, `elementor-get-page-structure` (use `include_content` with `element_id` to read settings+CSS), `elementor-publish-document`, `elementor-get-widget-schema`, `elementor-list-assets`.
- **Build on a draft**: set the post to draft first (`POST /wp/v2/pages/410364 {"status":"draft"}`), `build-composition` with `mode:"replace_children"`, then publish. Building on an already-published doc writes to an autosave that publish sometimes doesn't promote.
- **CSS regeneration**: after the first publish, do one trivial `manage-elements` update (e.g. re-set a button text) and publish again — otherwise the page's local CSS file stays stale. See `tools/deploy_reference.py`.
- Local `style` strings support `&:hover`, `@media(--laptop|--tablet_extra|--tablet|--mobile_extra|--mobile)` and native CSS nesting is emitted as-is. Breakpoints: laptop ≤1440, tablet_extra ≤1200, tablet ≤1024, mobile_extra ≤880, mobile ≤767.
- `e-image` value shape: `{"image":{"src":{"id":<attachment id>,"alt":"..."},"size":"full"}}` (id only — adding `url` fails validation).
- Put icons in `e-image` (not `e-svg`): inline SVGs share internal class names and recolor each other.
- `<ul>` inside `e-paragraph` (a `<p>`) breaks out of the paragraph — build lists as elements (icon + text rows).
- No V4 table/icon-list widgets; the V4 form set is `e-form` (+ required children `e-form-success-message`, `e-form-error-message`), `e-form-label`, `e-form-input` (type text/email/tel…), `e-form-select` (options), `e-form-submit-button`.
- Site font "Poppins Optimized" via kit variable `var(--Poppins)`. Page content is inside `.elementor-410324`.
- Screenshots: `node tools/shot.js <url> <prefix> <width> 1` (Playwright + Chromium preinstalled). Run widths **sequentially** — parallel runs through the proxy drop stylesheets. The site header itself overflows 3px at 430px (not our bug).
- Figma SVG exports of a node can include the page background rect — prefer the per-vector `svgAssets`/REST `format=svg` of the icon node itself and strip `preserveAspectRatio="none"`, `style`, `id` (see `tools/assets.py`).

## Already done
- Media uploaded: **410369** `maximus-hero-dashboard.webp` (1496×1094, 48 KB) — hero dashboard 599:2133 @2x.
- Asset pipeline `tools/assets.py` (download → WebP via Pillow / SVG sanitize → upload, idempotent registry). `pip install pillow` first.
- Spec extraction: see `SPECS.md`. Exact values exist for sections D and G (`figma/design-context-*.txt`); the rest are geometry-exact but styling-estimated → **re-extract with the REST API** before building.
- Visual targets for each section: `figma/screens/*.png` (Figma renders, ~0.65–0.73 scale). Full layer geometry: `figma/page-geometry.xml`.

## Next steps
1. Verify `FIGMA_TOKEN` (`GET /v1/me`), then pull node JSON for all 10 sections (+ children) and export assets per `SPECS.md` → WebP/SVG → upload.
2. Build section by section (dry_run first) on the draft page, publish, regenerate CSS.
3. Screenshot at all 9 widths vs. `figma/screens`, fix, publish, report.
