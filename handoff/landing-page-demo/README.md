# PPC landing page ("Landing Page Demo", page 412115)

Draft, slug `landing-page-demo`, template Elementor Full Width (site header and footer).
Edit: https://medcaredemo.online/medcare/wp-admin/post.php?post=412115&action=elementor

Built in Elementor V4 from *MedCare_MSO_PPC_Landing_Page.html*. The FAQ section and the design's own header and footer are left out; the site's header and footer are used instead.

## Rules followed
- **Width:** full width like the rest of the site. Sections use `parent-container` instead of the design's 1200px box.
- **Classes:** no new classes. The page uses `parent-container`, `heading-main` (H1), `specialties-heading` (H2s) and `global-text` (leads); everything else is a local style per element.
- **Colours and shadows:** the design system's tokens, written as hex.
- **Layout:** percentage or `fr` grids, no flex-basis. Breakpoints: tablet = 1 column, mobile = stacked.
- **Assets:** the Media Library already had NILA (392944), ASRM (393065) and ISO (401982). Everything else was uploaded from the design file as WebP under 100 KB; see `media.json` (412127–412149).

## Sections
1. **Hero:**
   - H1, lead, "Book a free demo" (scrolls to `#demo`) and "Call (505) 521-2145" (tel link);
   - V4 form card `#demo`: name, email, phone, practice, collections select;
   - stats strip and logo row.
2. **About:** photo with the 1,200+ card, the word-by-word reveal statement and the checklist.
3. **Services:** V4 tabs (Billing, Coding, Denials, A/R recovery, Credentialing, Prior auth), each with photo, icon, text and "What's included".
4. **Why us:** 98% meter (50 cells) and four pillars.
5. **Specialties:** photo plus vertical V4 tabs (7 specialties) and a blue description panel.
6. **Four steps, no disruption:** sticky stack (see below).
7. **Mid CTA band** with photo.
8. **Testimonials** (3).
9. **Closing contact band** with a second form, plus the mobile sticky bar (phone + Book a free demo).

## Four-steps animation (same as the design)
- **Sticky cards:** each card is `position: sticky`, with `top` 108/128/148/168px and z-index 1–4. These are the design's 88/108/128/148px plus 20px to clear the site header.
- **Scroll effect:** the helper script (`tools/helper.py`, one V3 HTML widget with `<script nowprocket>`) runs the design's own code. When card *i+1* slides over card *i*, it applies `p = clamp((top + h - nextTop) / (h - 20))`, then `scale(1 - .05p)` and `brightness(1 - .04p)`.
- **Fallbacks:** sticky only switches on when every card fits the viewport (the design's check). It's off on tablet and mobile, and there are no transforms with prefers-reduced-motion.
- **Verified in a browser:** the cards stick at 108/128/148, behind cards reach `scale(0.95)` and `brightness(0.96)`, and the stack releases together at the end.

## Other behaviour from the helper
- **About statement:** words go from #C9D3DB to #14212B as it scrolls through the viewport, using the design's formula.
- **Mobile sticky bar:** shown under 768px after 640px of scroll.

## Forms
Both forms are V4 `e-form` with email to mkamran@ and fashraf@medcaremso.com, plus collect submissions. This is the same setup as the AI Medical Coder page.

## Gotcha found here
The style converter strips `%`-escapes from url-encoded SVG data URIs, and a top-level `;base64` value gets cut at the `;`. Inline icons (lock, phone, select chevron) are therefore base64 data URIs used only inside pseudo-elements.

## Rebuild
```
python3 tools/run_build.py      # replace_children on 412115
python3 tools/helper.py         # adds the scroll helper widget (run after every rebuild)
```

## Change log
- Testimonials: the left heading column (`4fdcf16` on the live page) is now sticky (`top: 120px`, desktop only, static from tablet down),
  so it stays in view while the testimonial cards scroll. Applied with manage-elements and published; also in `lp.py`.
  Backup of the published page before this: `build/backup_412115_before-sticky.json`.
