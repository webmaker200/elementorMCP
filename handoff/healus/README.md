# HealUs New Page — build notes

- Page: WP page **411263** `/healus-new-page/` (Elementor V4 atomic, 9 sections, 402 elements), Figma `oYqLJMmgAjdLKQeLgtDSM7` node **671:593**.
  Site header, the orange "Schedule a free Demo" band and the footer come from the site templates (Figma 671:1590 / 671:1895 / 671:1785 skipped).
- Status: **published with a post password** while under review (Yoast's "remove unregistered URL parameters" setting strips
  Elementor preview tokens, so anonymous preview links do not work on this site). Remove the password in WP Admin to go live.
- Builder: `tools/healus.py` (source of truth), deploy with `tools/deploy_healus.py` (draft → build-composition replace →
  publish → touch → publish). Auth is read from the local MCP config (`~/.claude.json`), never from the repo.
  The page may later be edited in the Elementor editor — then prefer `elementor-manage-elements` for small changes, because
  re-running the deploy overwrites editor changes.
- Assets: `tools/assets.py` (Figma image fills + 2x node renders → WebP; logo watermarks / arrow from Figma vector geometry → SVG;
  idempotent upload). Media ids in `media.json` (18 files, ~227 KB).
- Section glows: `tools/glows.py` turns the Figma blurred ellipses into CSS radial-gradient layers per section (`glows.json`),
  including neighbouring ellipses that bleed in — no background images.
- Checks: `tools/shot.js` (screenshots through the post-password form, `PW=<password>`), `tools/probe.js` (section heights,
  tab switching, accordion), `tools/ovf.js` (horizontal overflow).

## Design system use (added for this page)
- Global colour variables: `HealUsInk #14212B`, `HealUsSlate #4A5966`, `HealUsMuted #6B7A87`, `HealUsGreen #006750`,
  `HealUsTeal #318371` (+ existing DarkGray, PureWhite, PureBlack, HealthGreen, Poppins).
- Global classes: `healus-pill`, `healus-h2`, `healus-lead`, `healus-glass`, `healus-btn`, `healus-btn-ghost`,
  `healus-check-item`, `healus-num`, `healus-tab`, `healus-tab-label`, `healus-chip`, `healus-cmp-no`, `healus-cmp-yes`;
  existing `parent-container` (sections), `global-text`, `w-45`, `w-50`.
- Layout rules from the brief: plain `fr` grid tracks (no repeat/minmax/calc), percentage widths (no flex-basis), max-widths
  reset to 100% on small screens, small-device section spacing 3% top/bottom and 5% left/right.

## Gotchas found here
- `e-grid` has a default mobile rule that forces one column: every grid that should keep columns on phones sets
  `@media(--mobile){grid-template-columns: ...}` explicitly.
- Local desktop rules beat global-class media rules (same specificity, local CSS loads later): never set a property locally that
  a class varies per breakpoint (e.g. `font-size` on `healus-h2`).
- Heading `<br>`s are hidden below 1024px by `healus-h2`; keep a space before each `<br>` so words don't join.
- Active tab styling: V4 tabs render `<button role="tab" aria-selected="true" class="… e--selected">`; `healus-tab` styles
  `&[aria-selected="true"]`.
- `p { margin-block-end: 0 !important }` in the theme → spacing is expressed with `margin-block-start` / padding.

## Open items for the owner
- Forms (hero work-email form and the demo form) have **no delivery action** (email/CRM/webhook) configured yet.
- All six feature tabs share the Charting content for now; "Next: …" links scroll to the tab bar.
- FAQ answers 2–5 are bracketed placeholders; the specialty chips (section 4) are static; "Show all 10 differences" is a label
  (the design only lists 6 rows).
