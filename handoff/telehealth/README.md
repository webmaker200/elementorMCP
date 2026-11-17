# Telehealth billing services page (411943): box hover

Section "Where Telehealth Revenue Leaks, and How We Stop It" (`7619303`): all 8 boxes in the grid get a subtle hover.
- 7 white cards: 8cf57c4, c4108cd, ac3d1e7, 031899d, bef4310, 4d8f3e3, fb31c4a.
- The blue CTA box: cf2e6ae.

Hover (added as a patch to each box's local style, nothing else changed):
- `transition: transform 0.3s ease, box-shadow 0.3s ease;`
- hover `transform: scale(1.02)`, plus a soft drop shadow (`0 12px 28px -12px rgba(3,103,161,0.22)`; 0.45 on the blue box). The original inset shadow is kept.

Applied with `elementor-manage-elements` (style_apply_mode patch), then published. Page data before the change: `backup/`.

## Section "What Our Telehealth Billing Services Include" (`679856a`)
Same subtle hover on all 11 boxes in grid `a241f7e`: 50c9fce, 4ace391, 43d2f2e, d4d1813, cca12aa, d6c50d0, fcbcea3, 35f83a0, b9f5d19,
e217f33, 08e6454. The hover is `scale(1.02)` plus `0 12px 28px -12px rgba(3,103,161,0.25)`, with a 0.3s transition. These boxes have no base shadow.
Backup before this change: `backup/telehealth_411943_before-hover2.json`.
