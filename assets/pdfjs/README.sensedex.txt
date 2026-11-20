Mozilla PDF.js 6.5.438 legacy distribution (Apache-2.0).
Source: https://github.com/mozilla/pdf.js/releases/tag/v6.5.438
Archive: https://github.com/mozilla/pdf.js/releases/download/v6.5.438/pdfjs-6.5.438-legacy-dist.zip

SenseDex integration: added web/sensedex.css and site title; disabled PDF scripting, annotation editing, ML model downloads, and persisted preferences; removed the sample PDF and source maps; retained English localization. Other runtime assets and license notices are preserved.

Publication profiles: web/activespn.js and web/activespn.css retain their original filenames and now provide the same reader for all explicitly configured published papers. The profile must match its PDF filename; other files and readers without a profile retain the default configuration. Profiles enable native local annotations, automatic zoom, a 200px outline sidebar open on desktop and closed below 720px, and the light gray toolbar. Scripting and ML downloads remain disabled. No PDF is rewritten.

Iframe URL format (relative to the publication page):
../../assets/pdfjs/web/viewer.html?profile=PAPER_ID&file=../../publications/PDF_FILENAME#zoom=auto
Encode the query separator as &amp; in HTML. Keep the existing accessible iframe title and responsive 600px reader container.

Profile / allowed PDF / outline source:
activespn / activespn.pdf / measured heading positions, 8 pages
activespn2 / activespn2-author.pdf / native named section destinations plus measured abstract, 14 pages
active-surface / active-surface.pdf / measured chapter and subsection positions, 6 pages
flip-and-flap / flip-and-flap.pdf / measured chapter and subsection positions, 8 pages
adap / adap.pdf / original embedded outline, 16 pages
stable-quadrotor / stable-quadrotor.pdf / measured chapter, subsection and endmatter positions, 11 pages
parameter-adaptive-control / parameter-adaptive-control.pdf / measured chapter and subsection positions, 10 pages
oral-care / oral-care.pdf / measured headings, subsections and declarations, 20 pages

Embedded outlines always take precedence over supplied navigation. Fallback coordinates use PDF points and each document's actual page height, so sections on the same page have separate vertical targets. The additional PDFs above all have actual text and embedded font resources; they are not image-only replacements. The Oral Care PDF is web-optimized from the publisher's published PDF.

Parameter Adaptive Control uses a slightly wider page-number input with reduced side padding to show its six-digit printed page labels in full, including in the narrow mobile toolbar. Native page-label navigation is preserved.

Stable Quadrotor navigation deliberately uses measured headings: the source PDF's sec5 named destination points to page 7, while the actual Conclusions heading is on page 10. The supplied reader outline targets the actual heading without altering the source PDF.

ActiveSPN2 version note: the reader uses the author's searchable vector preprint (http://www.senli.site/files/2025-J-BIROB-LiDeformable.pdf). This version has no separate CRediT, declaration, acknowledgments or appendix sections. The original 13-page image-only activespn2.pdf remains a separate article-in-press download and is not assigned the vector version's outline.
