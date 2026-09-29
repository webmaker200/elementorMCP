# Maximus — section specs (from Figma, 1920 frame)

Legend: **exact** = from Figma design context; *~est* = measured from renders/sibling components — re-verify via REST API.
Section y values are page coordinates inside frame 599:1630 (header 0–97 is the site header, skip).

## Global tokens
- Font Poppins; weights Regular 400 / Medium 500 (SemiBold 600, Bold 700 appear in UI mockups only).
- **H2 display**: 58px / 82px, letter-spacing −1.16px, #000, 400 (**exact**, sections D/G). Hero H1 uses the same style.
- **Body**: 16px / 32px, #4F4F4F, 400 (**exact**).
- **Item title**: 24px/32px 500 #000 (G) · 22px/32px 400 #000 (D checklist).
- **Pill tag "Frame 30"** (**exact**): 248×46 (hero 258×46, E 290×46), bg rgba(255,255,255,0.1), border 1px #9ACAA1, radius 34px, shadow `0 15px 15px 0 rgba(194,194,194,0.1)`, label 12px/1.2 #7D7D7D centered.
- **Button.base** (*~est*): h56, pill radius, bg ≈#EAF3E6, border 1px ≈#CCE4DD, label 14px/20px 500 #000, padding-left ~24–26, white 39×39 arrow circle inset 9px right, 24px `arrow-narrow-right` stroke ≈#318371.
- **Background glows** (**exact** style): solid ellipse + opacity + `feGaussianBlur stdDeviation 150` (layer blur 300). Colors by name: Ellipse 4 = #8BC343 @0.1, Ellipse 5 = #10AFFF @0.1, Ellipse 6 = #FFE27A @0.1; small ones (7–10) @0.3 (#D9FF50 / #8BC343 / #FFE27A / #10AFFF). Rotated ellipses: meta bbox = D×1.366; centers below are corrected. Reproduce with radial-gradients on the section background, or absolutely positioned blurred divs; sections clip (`overflow:hidden`).
- Figma variables: Primary Base Green #9BCBA2, Active Hover #318371, Light Selection #B1DBCF, Active Field Label #618468, Gray 2 #4F4F4F, Un-focused Description #7D7D7D, Stroke #EAEAEA/#E0E0E0/#D3D3D3, Backgrounds #F8F8F8/#F3F3F3.

---
## A · Hero — 599:1631 (y 97, 1920×867)
- Glows: E4 green D803 c(1640,264) · E5 blue D803 c(979,440) · E6 yellow D887 c(184,704).
- Left column x=223, max-w 819: pill (258×46, y22) with 3 overlapping avatars (34.6px frames, 33.2px photos, overlap ~10px; nodes 599:1639/1641/1643) + label "AI-Powered healthcare".
- H1 (y93): "Your Revenue Cycle,<br>Working Smarter." (H2 display style).
- P (y290, w595): "Maximus connects billing, claims, coding, payments, and reporting in one intelligent platform — helping your practice reduce administrative friction and stay ahead of revenue leakage."
- Buttons row y429, gap 34: Button.base 240×56 "Explore AI Ecosystem" (599:1647) + text link "Request a Demo" + black 24px arrow (599:2747).
- Compliance logos row (599:1653, y533, 438×81, gaps ~33.5): HITRUST 599:1654 (73×81), HIPAA 599:1691 (63×81), AICPA SOC 599:1706 (63×81), PCI 599:2131 (98×81) → SVG (webp if raster inside).
- Dashboard 599:2133 at (1013,92) 748×517 → **uploaded 410369**.
- Floating glass cards (left −157px of dashboard; tops 267/343/441 relative to dashboard): 
  - 599:2733 194.6×62.7 settings icon 599:2734 (31px, #1171A1) "Automated ERA<br>Posting"
  - 599:2720 242.9×84.3 cpu icon 599:2721 (33px, #8B5CF6) "Claim Scrubbing by<br>Rule Engine"
  - 599:2738 194.6×62.7 file-plus icon 599:2739 (32px, #8BC343) "Denial<br>Management"
  - *~est*: 12px/17px #000, bg rgba(255,255,255,.5), border 1px rgba(255,255,255,.8), radius ~16, backdrop blur ~10px, shadow ~0 10px 30px rgba(17,113,161,.06).

## B · Problems — 599:2749 (y 964, 1920×1028)
- Glows: E4 green D888 c(1728,236) · E6 yellow D980 c(846,588) · E5 blue D887 c(68,866).
- Centered header: pill "The Problems with Traditional PMS" (y73) · H2 "Everything You Need to<br>Take Control of Your Revenue Cycle" (y142, w1089) · P (y317, w870) "Maximus brings billing, claims, coding, payments, analytics, and automation together in one connected platform — giving your team greater visibility and control."
- 4 cards y440, 343×332, gap 34 (x 223/600/977/1355). Top illustration row y29 h82 = white icon tile 82×82 + mini preview card (sibling frames): Eligibility 599:2761+599:2765 · Claims 599:2812+599:2820 · Payments 599:2786+599:2792 · KPIs 599:2838+599:2843 → export each pair as SVG (or tiles/icons separately). Title 32px/46px 400 centered; body 16/32 #4F4F4F centered:
  - Eligibility — "Still checking insurance eligibility and benefits patient by patient?"
  - Claims — "Still relying on teams to identify claim issues, check statuses, and determine the next action?"
  - Payments — "Still spending valuable staff time manually posting and reconciling payments?"
  - KPIs & Reporting — "Still waiting for reports to understand how the practice is performing?"
  - Card *~est*: translucent (≈rgba(236,244,247,.6)), 1px rgba(255,255,255,.8), radius ~20, shadow ~0 12px 30px rgba(0,0,0,.04).
- Bar 599:2773 (y815, 1475×152): "Maximus changes that." (32px) + "AI, automation, analytics, workflows, and interoperability in one connected PMS." + button "See What Maximus Automates" (310×56).

## C · Comparison — 599:3011 (y 2029, 1920×1024)
- Glows: E4 green D947 c(1022,568) · E5 blue c(~1837,~446) · E6 yellow ≈D900 c(~150,~800) (*~est*).
- Pill "Not Your Regular PMS" (x221,y49) · H2 "From Practice Management to<br>Practice Intelligence." (y118) · P (y296) "Traditional PMS software helps your team manage tasks. Maximus helps perform them." (#000 per render).
- Panel 599:3019 (x57, y388, 1806×464, ~rgba(255,255,255,.7), radius ~20, overflow hidden): Maximus logo 599:3020 (244.8×44, SVG) at (169,82); faint line art 599:3025 (SVG) behind right half; 2-col checklist (24px check 599:3030 #8BC343, gap 17, rows 46px), ~18px/32px #000:
  - Col 1: Acts on patient and claim data · Automated eligibility + benefits verification · Automated claim scrubbing · Automated status + Agentic AI follow-ups · AI-driven payment posting
  - Col 2: HL7 + FHIR + APIs + RPA · One-click AI-assisted appeals · Intelligent rule engine + smart workflows · Integrated KPI monitoring · Smart BI + financial analytics
- Traditional card 599:3059 (x1206, y208, 495×549, above the panel; ~bg #F0FFFC, border 1px ~#6FAA9C, radius ~20, pad 38/53): title "Traditional PMS / Billing Software" (~22px) + 10 rows with red x icon 599:3062 (16px ~#E87378), 16/32 #4F4F4F, pitch 44: Stores patient and claim data · Manual eligibility workflows · Staff checks claim errors · Manual claim-status follow-up · Manual payment posting · Static reports · Disconnected KPIs · Manual workflow routing · Staff prepares appeals · Limited external connectivity

## D · Eligibility — 599:2857 (y 3019, 1920×870) — **exact** (`figma/design-context-section-D-599_2857.txt`)
- Glows: E6 #FFE27A .1 D980 c(846,588) · E5 #10AFFF .1 D887 c(68,866) · E7 #D9FF50 .3 407×408 blur 178 c(1562,306) · E10 #8BC343 .3 same c(1651,680) · E8 #FFE27A .3 D527 blur 195 c(1370,680) · E9 #FFE27A .3 D438 blur 172 c(1193,345).
- Left col x220 w659: pill "Start the Revenue Cycle Right" (y73) · H2 "Verify Coverage Before It Becomes a Revenue Problem." (y142, 3 lines) · P (y402, w633) "Maximus automates patient eligibility and benefits verification, helping teams validate coverage earlier and reduce repetitive front-office work." · divider (y505, w631, 1px rgba(79,79,79,.2)) · checklist rows pitch 96, check 28px (#8BC343 stroke 2, **uploaded? no** — re-export) at x224, text x281: title 22/32 400 #000 + sub 16/32 #4F4F4F:
  - Automated Eligibility Verification — Reduce manual payer lookups.
  - Benefits Verification — Bring benefit visibility into the patient workflow.
  - Batch Eligibility — Verify multiple scheduled patients in one workflow.
- Right: MainWorkflowCard 599:2881 (975,234) 448×467 · CoverageDonutWidget 599:2955 (1435,234) 262×199 · ActivityChartWidget 599:2979 (1435,443) 262×258 → **WebP @2x with alpha** (cards are rgba(255,255,255,.4), border .9px rgba(0,0,0,.07), radius ~18).

## E · Claims — 599:3164 (y 3909, 1920×1073)
- Glows: E4 green D888 c(1728,236) · E6 yellow D980 c(846,588) · E5 blue D887 c(68,866).
- Centered: pill 290×46 "Smarter Claims Start Before Submission" · H2 (w833) "Catch More Issues Before the Payer Does." · P (w834) "Maximus uses intelligent rules and automated claim validation to identify issues and trigger the appropriate workflow before they become downstream problems."
- 4 columns 343 wide, gap 34 (x 223/600/977/1354): image frame 343×332 at y440 → export whole frames **WebP @2x**: 599:3172, 599:3204, 599:3268, 599:3325 (colored bg ~#C0D9E4 / #E2EDCB / #E4D8EE / #F8EAC0, radius ~16, chart clipped). Title (~32px, 2 lines, margin-left 9, 31 below frame) + desc 16/32 #4F4F4F w301:
  - Intelligent Rule Engine — Define conditions, routing logic, and actions across claims, payments, eligibility, and workflows.
  - Auto Claim Scrubbing — Identify missing information, inconsistencies, and potential claim issues before submission.
  - Auto Claim Status — Reduce repetitive payer checking and surface stalled claims sooner.
  - Smart Workflows — Automatically trigger tasks, route exceptions, and move work to the next action.

## F · Reporting — 599:3391 (y 5002, 1920×1183)
- Glows: E4 green D1064 c(1728,325) · E6 yellow D~1160 c(969,621) · E5 blue D~1433 c(~292,~1355).
- Header row: pill "The Problems with Traditional PMS" · H2 (x224, w848, 3 lines) "Know How Your Practice Is Performing — Without Waiting for the Report." · P right (x1270, w397) "Maximus turns operational and financial information into real-time visibility for practice leadership."
- Grid y440: green card 599:3399 737×541 (gradient ~#31967F→#1B816A, radius ~16; texts white: Collections / $842K / Payments +18% / A/R $1.12M / Denial Rate 4.8%; chart line 599:3400 SVG 737×386 at top 163) — build as CSS card + SVG line, or one WebP.
- Right column 707 wide, gap 16: card 599:3409 (136h) pie icon 599:3413 in 82px white tile — "Smart BI Reporting" / "Modern dashboards for operational and financial performance." · card 599:3417 (136h) — "Integrated KPI Tracking" / "Monitor the metrics that matter without jumping between disconnected systems." · card 599:3425 (237h) — "See it. Understand it. Act on it." / "Give CFOs, CEOs, practice owners, and RCM leaders a clearer view of what is happening across the business." + button "Book a Demo" (190×56).
- CTA bar 599:3434 (y997, 1475×152): "See it. Understand it. Act on it." + same description + button "See What Maximus Automates".

## G · Integrations — 599:3443 (y 6281, 1920×829) — **exact** (`figma/design-context-section-G-599_3443.txt`)
- Glows: E4 #8BC343 .1 c(1330,508) D1064 · E5 #10AFFF .1 c(1975,167) D887 · E6 #FFE27A .1 c(326,658) D1069 · E7 #D9FF50 .3 c(698,130) 342 · E8 #FFE27A .3 c(570,512) D405 · E9 #10AFFF .3 c(361,211) D382.
- Photo card 599:3461 (x222, y39, 618×695, border 1px #1171A1, radius 20, overflow hidden; photo 1248×1872 → WebP ~1236w, `object-fit:cover; object-position:50% 83.6%`). Glass overlay at (19,503) 584×171, bg rgba(13,54,82,.52), radius 20: "Connect the data. Trigger the workflow. Automate the action." (24/32 500 #fff) + "EHRs • Payers • Clearinghouses • Labs • Payment systems • Third-party healthcare platforms" (16/32 #C8EDFF).
- Text col x1086 w~666: pill "Connected by Design" (y39) · H2 "Your PMS Shouldn’t Live on an Island." (y108) · P (w633) "Maximus is designed to operate within the modern healthcare technology ecosystem and connect to the systems your organization already relies on." · list (y382, border-left 1px #B8B8B8, padding-left 30, items 24/32 500 #000 + 16/32 #4F4F4F, 32px gaps): HL7 — Support established healthcare interoperability standards. · FHIR — Enable modern healthcare data exchange and interoperability. · APIs — Connect Maximus with external applications, platforms, and services. · RPA — Automate repetitive workflows where direct integration is limited.

## H · Trust — 599:3468 (x142, y 7193, 1636×898)
- Big rounded container (fill/radius to verify). Glows E5 (-635,860) D1335 · E4 (214,18) 1064 · E7 (818,410) D1460.
- Left: pill "Built for Healthcare Operations" (87,57) · H2 "Technology Is Only Valuable When Practices Can Trust It." (3 lines) · 2×2 stat cards 296×203 (gaps 16/15): big stat (blue ~#1171A1, ~40px) + label + desc 16/32:
  - 200+ Physicians — Trusted across physician workflows and practice operations.
  - HL7 Interoperability — HL7, FHIR, and API-supported connectivity.
  - AI Automation-First — AI, RPA, intelligent rules, and smart workflows built into the platform.
  - 360° Executive Visibility — Financial, operational, and revenue-cycle insights in one environment.
- Right: dashboard mockups → WebP @2x: 599:3491 (712×503), 599:3602 (340×237), 599:3664 (340×237). Badge 599:3721 "Trusted by / 200+ Physicians" (203×60) → build as small card + SVG icon 599:3723.

## I · Why — 599:3732 (y 8173, 1920×770)
- Glows E4 (548,95) 948 · E6 (99,1294) 1234×1307 · E5 (1231,608) D1212.
- Centered: pill "Why Maximus" · H2 "Your Software Shouldn’t Add More Work to Your Practice." · sub "It should remove it." (#000 per render).
- 4 cards 359×247 (x 221/594.5/968.5/1342, y370): 68px white icon tile + 2-line title (~32px) + body 16/32: More Automation (settings 599:3742) — Still checking insurance eligibility and benefits patient by patient? · More Intelligence (cpu 599:3749) — For operational decisions. · More Visibility (eye 599:3764) — For leadership. · More Connectivity (link-2 599:3771) — Between systems. Icons → SVG.

## J · Demo form — 599:3776 (y 8943, 1920×1833)
- Main container 599:3784 (x57, y−42, 1806×1189; fill/radius to verify) with faint logo-mark vectors 599:3785 top-right.
- Left (x168 rel.): pill "See Maximus in Action" · H2 "What Would Your Practice Look Like With Less Manual Work?" · P (w472) "See how Maximus can help automate eligibility, claims, payments, follow-ups, reporting, and other revenue-cycle workflows — while giving leadership clearer visibility into performance." · divider · checklist (28px checks): See the platform live — Explore the workflows most relevant to your organization. · Map your current workflow — Identify where automation and visibility can make the biggest difference. · Review interoperability — Discuss EHR, payer, API, HL7, and FHIR connectivity needs.
- Form card 599:3806 (560×752, pad 40): logo mark 599:3808 (29px SVG) + "Book Your Maximus Demo" / "Tell us a little about your organization." · 2-col grid (230+20+230), rows gap 20, label 20px line + 44px input (text inset 16):
  - First Name (Jane) | Last Name (Smith) · Work Email full (jane@yourclinic.com) · Phone (Enter your phone number) | Organization (Your clinic or group) · Number of Providers select (1–5) | Current PMS / EHR (e.g. Epic, athenahealth) · Primary Challenge select full (Eligibility & Benefits)
  - Submit 480×56 "Schedule My Demo" (green ~#9BCBA2 bg, white arrow circle). Skip the "Prototype form only…" designer note.
- Green CTA 599:3880 (x222, y932, 1476×316): H2-size "Manage Less. Automate More. See Everything." + "AI-Powered Practice Management — Intelligent. Automated. Connected." + button "Book a Demo" (193×56); decorative logo mark 599:3881.
- Watermark 599:3783 (1949×351 at y1324, blurred "Maximus" wordmark image fill) → WebP full-bleed.
