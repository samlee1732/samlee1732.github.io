# SenseDex Lab

**Sensing and Dexterous Manipulation Lab · 感知与灵巧操作实验室**

The academic website of **Sen Li, Ph.D.** and SenseDex Lab at Shenzhen Polytechnic University. It presents research publications, team members, teaching resources, student competitions, and news.

**[Visit the website](https://www.sensedex.online/)**

## Website sections

| Section | Content |
| --- | --- |
| [Homepage](https://www.sensedex.online/) | Biography, research interests, contact information, patents, and research projects |
| [Publication](https://www.sensedex.online/#publication) | Manuscripts under review followed by published papers; paper details, figures, available PDFs, and BibTeX |
| [Team](https://www.sensedex.online/team/) | Principal investigator, collaborators, current students, and alumni |
| [Teaching](https://www.sensedex.online/teaching/) | Course pages, learning resources, and student competitions |
| [News](https://www.sensedex.online/news/) | Research, teaching, conference, and competition updates in reverse chronological order |

## Local preview

The website serves static HTML, CSS, and JavaScript. No Node.js installation is required.

Run this command from the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080). Use the local server so that the browser can load the search index and other local resources.

## Updating content

| Source | Purpose |
| --- | --- |
| `index.html` | Homepage biography, contact information, and shared navigation |
| `data/publications.json` | Published papers and their resources |
| `data/under-review.json` | Manuscripts under review |
| `data/patents.json` / `data/projects.json` | Patents and research projects |
| `data/team.html` | Team members and alumni |
| `data/teaching.html` | Teaching overview |
| `data/robotics-applications.html` | Robotics and Applications course |
| `data/automatic-control.html` | Automatic Control course |
| `data/competitions.html` | Student competitions within Teaching |
| `data/news.html` | News entries |
| `assets/styles.css` | Shared styling and responsive layout |
| `assets/course-syllabus.css` | Course syllabus styling |

After editing a content source, regenerate the pages and search index:

```sh
python3 tools/build_publications.py
```

The script uses the Python standard library. Commit the edited sources, supporting assets, and generated HTML, BibTeX, and search index together. Changes made only to generated pages may be overwritten the next time the script runs.

### Publications and media

- Keep authors in the confirmed order. Store corresponding authors in `corresponding_authors` and equal contributors in `equal_contributors`; these generate `*` and `#` markers without changing BibTeX author names.
- Put publication assets in `assets/publications/` and news assets in `assets/news/`. Use the existing image fields and descriptive alternative text.
- Publication overview collages use a 5:3 aspect ratio. Prefer optimized images for the overview and retain original media where needed on detail pages.
- Add PDFs and external links only when available. Keep unpublished work labeled **Under Review** and conceptual illustrations identified as such.

## Deployment

- **Website:** https://www.sensedex.online/
- **Repository:** https://github.com/samlee1732/samlee1732.github.io
- **Hosting:** GitHub Pages, published from the root of the `main` branch.
- **Custom domain:** `www.sensedex.online`, maintained in `CNAME`.
- **Static publishing:** the empty `.nojekyll` marker disables Jekyll processing.

After committing to `main`, check the GitHub Pages deployment in the repository's Actions or Pages settings. Keep `CNAME` and `.nojekyll` in the repository root.

## Resources and credits

- Brand assets are stored as `assets/sensedex-mark-small.png`, `assets/sensedex-mark.png`, and `assets/sensedex-logo-v2.png`. Header text is rendered in HTML.
- Publication page organization was informed by the [Bionic Design & Learning Lab publication page](https://bionicdl.ancorasir.com/?p=2124).
- The PDF viewer uses [PDF.js](https://mozilla.github.io/pdf.js/); its license and third-party notices are retained in `assets/pdfjs/`.
- The asMagicForce news animation retains its source record and license in `assets/news/asmagicforce-aic-source.txt` and `assets/news/asmagicforce-aic-LICENSE.txt`.
- Visit statistics use [Busuanzi](https://busuanzi.9420.ltd/), with a source link in the website footer. Search runs locally in the browser.

Publication metadata sources and any applicable abstract attribution are retained with the individual paper records.
