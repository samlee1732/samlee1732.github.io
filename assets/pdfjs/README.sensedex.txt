Mozilla PDF.js 6.5.438 legacy distribution (Apache-2.0).
Source: https://github.com/mozilla/pdf.js/releases/tag/v6.5.438
Archive: https://github.com/mozilla/pdf.js/releases/download/v6.5.438/pdfjs-6.5.438-legacy-dist.zip

SenseDex integration: added web/sensedex.css and site title; disabled PDF scripting, annotation editing, ML model downloads, and persisted preferences; removed the sample PDF and source maps; retained English localization. Other runtime assets and license notices are preserved.

ActiveSPN profiles: web/activespn.js and web/activespn.css apply only to profile=activespn with activespn.pdf and profile=activespn2 with activespn2.pdf. They enable native local annotations, automatic zoom and a responsive outline. The supplied PDFs have no bookmarks, so each profile supplies its own section targets measured from its headings without changing either PDF. ActiveSPN2 is the 13-page image-only article-in-press PDF; its targets were verified on rendered pages, and it has no text layer for native full-text search. A future PDF's embedded outline takes precedence. Scripting and ML downloads remain disabled. Other papers retain the default reader configuration.
