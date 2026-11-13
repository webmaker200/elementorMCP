# Radiology specialty (375428)

- Page size: all 172 local V4 styles moved into global classes `rad-s01`..`rad-s97` (`tools/shrink.py --pid=375428 --prefix=rad-s --all`),
  pixel-checked at 1440 and 390 (only the testimonial carousel differs). Backup of the V4 content before: `backup/`.
- Content check vs "Radiology Billing Services.docx": `radiology-content-check.html`
  (`tools/rad_docparas.py` docx -> paragraphs, `tools/rad_pagetext.js` live page -> text blocks, `tools/rad_compare.py` word diff + report).
