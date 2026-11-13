#!/usr/bin/env python3
"""Build the publication overview, detail pages, and BibTeX using only Python 3."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/publications.json'
esc = html.escape


def authors(paper):
    return ', '.join('<strong>Sen Li</strong>' if name == 'Sen Li' else esc(name)
                     for name in paper['authors'])


def citation(paper):
    parts = [f'<cite>{esc(paper["venue"])}</cite>']
    if paper.get('volume'):
        parts.append('vol. ' + esc(str(paper['volume'])))
    if paper.get('number'):
        parts.append('no. ' + esc(str(paper['number'])))
    if paper.get('pages'):
        parts.append('pp. ' + esc(paper['pages'].replace('--', '–')))
    if paper.get('article_number'):
        parts.append('article ' + esc(str(paper['article_number'])))
    parts.append(str(paper['year']))
    if paper['status'] != 'Published':
        parts.append(esc(paper['status']))
    return ', '.join(parts) + '.'


def bibtex(paper):
    kind = 'inproceedings' if paper['type'] == 'Conference Paper' else 'article'
    key = re.sub(r'[^A-Za-z0-9]', '', paper['authors'][0].split()[-1] + str(paper['year']) + paper['marker'])
    tex = lambda value: str(value).replace('&', r'\&').replace('%', r'\%')
    fields = {'title': '{' + tex(paper['title']) + '}',
              'author': ' and '.join(tex(name) for name in paper['authors']),
              'booktitle' if kind == 'inproceedings' else 'journal': tex(paper['venue']),
              'year': str(paper['year'])}
    for name in ('volume', 'number', 'pages', 'doi'):
        if paper.get(name):
            fields[name] = tex(paper[name]).replace('–', '--')
    if paper.get('article_number'):
        fields['pages'] = str(paper['article_number'])
    fields['url'] = paper['paper']
    if paper['status'] != 'Published':
        fields['note'] = tex(paper['status'])
    return '@' + kind + '{' + key + ',\n' + ',\n'.join(
        '  ' + k + ' = {' + v + '}' for k, v in fields.items()) + '\n}\n'


def image(paper, prefix, lazy=True):
    attrs = ' loading="lazy"' if lazy else ''
    if paper.get('image_width') and paper.get('image_height'):
        attrs += f' width="{paper["image_width"]}" height="{paper["image_height"]}"'
    return (f'<img src="{prefix}assets/publications/{esc(paper["image"])}"'
            f' alt="{esc(paper["image_alt"])}" decoding="async"{attrs}>')


def overview(papers):
    rows = []
    for p in papers:
        url = './publications/' + p['id'] + '/'
        description = 'Abstract' if p.get('abstract') else 'Summary'
        links = [(description, url + '#abstract'), ('Links', url + '#links'), ('BibTeX', url + '#bibtex')]
        if p.get('pdf'):
            links.append((p.get('pdf_label', 'PDF'), './assets/publications/' + p['pdf']))
        if p.get('video'):
            links.append(('Video', p['video']))
        resources = '\n'.join(f'                  <li><a href="{esc(href)}">{label}</a></li>' for label, href in links)
        rows.append(f'''          <li>
            <article class="publication-row" aria-labelledby="{p['id']}-title">
              <div class="publication-details">
                <p class="publication-authors">{authors(p)}</p>
                <h3 id="{p['id']}-title" class="publication-title"><a href="{url}">{esc(p['title'])}</a> <span class="publication-type">{esc(p['type'])}</span></h3>
                <p class="publication-citation">{citation(p)}</p>
                <ul class="publication-resources" aria-label="Resources for {esc(p['marker'])}">
{resources}
                </ul>
              </div>
              <div class="publication-media">
                <a href="{url}" aria-label="Read about {esc(p['marker'])}">{image(p, './')}</a>
              </div>
            </article>
          </li>''')
    return '''      <section id="publication" class="publications" aria-labelledby="publication-heading" tabindex="-1">
        <h2 id="publication-heading">Publication</h2>
        <!-- Generated from data/publications.json by tools/build_publications.py. -->
        <ol class="publication-list">
''' + '\n'.join(rows) + '''
        </ol>
      </section>'''


def detail(p, homepage):
    header = re.search(r'    <header\b.*?</header>', homepage, re.S).group()
    header = header.replace('href="./"', 'href="../../"')
    header = header.replace('href="#', 'href="../../#')
    header = header.replace('src="./assets/', 'src="../../assets/')
    header = header.replace('class="nav-link is-current" href="../../" aria-current="page"', 'class="nav-link" href="../../"')
    header = header.replace('class="nav-link" href="../../#publication"', 'class="nav-link is-current" href="../../#publication" aria-current="page"')
    dialogs = homepage[homepage.index('    <dialog'):homepage.index('  </body>')]
    section_name = 'Abstract' if p.get('abstract') else 'Summary'
    paragraphs = p.get('abstract') or [p['summary']]
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    paragraphs_html = '\n'.join('          <p>' + esc(text) + '</p>' for text in paragraphs)
    if not p.get('abstract'):
        paragraphs_html += '\n          <p class="paper-note">Full abstract to be added.</p>'
    links = [('Publisher', p['paper'])]
    if p.get('doi'):
        links.append(('DOI: ' + p['doi'], 'https://doi.org/' + p['doi']))
    if p.get('pdf'):
        links.append((p.get('pdf_label', 'PDF'), '../../assets/publications/' + p['pdf']))
    if p.get('video'):
        links.append(('Video', p['video']))
    if p.get('code'):
        links.append(('Code', p['code']))
    links_html = '\n'.join(f'            <li><a href="{esc(url)}">{esc(label)}</a></li>' for label, url in links)
    missing = []
    if not p.get('pdf'):
        missing.append('PDF')
    if not p.get('video'):
        missing.append('Video')
    missing_html = '<p class="paper-note">' + ' / '.join(missing) + ' to be added.</p>' if missing else ''
    doi_html = (f'<p class="paper-doi">DOI: <a href="https://doi.org/{esc(p["doi"])}">{esc(p["doi"])}</a></p>' if p.get('doi') else '')
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{esc(p['summary'])}">
    <meta name="theme-color" content="#92316f">
    <title>{esc(p['marker'])} | SenseDex Lab</title>
    <link rel="icon" href="../../assets/sensedex-mark.png" type="image/png">
    <link rel="apple-touch-icon" href="../../assets/sensedex-mark.png">
    <link rel="stylesheet" href="../../assets/styles.css">
    <script src="../../assets/main.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
{header}
    <main id="main-content" class="container paper-page">
      <a class="paper-back" href="../../#publication">← All publications</a>
      <article>
        <header class="paper-heading">
          <p class="paper-eyebrow">{p['year']} <span aria-hidden="true">·</span> {esc(p['type'])}</p>
          <h1>{esc(p['title'])}</h1>
          <p class="paper-authors">{authors(p)}</p>
          <p class="paper-citation">{citation(p)}</p>
          {doi_html}
        </header>
        <figure class="paper-figure">
          {image(p, '../../', lazy=False)}
        </figure>
        <section id="abstract" class="paper-section" aria-labelledby="abstract-heading" tabindex="-1">
          <h2 id="abstract-heading">{section_name}</h2>
{paragraphs_html}
        </section>
        <section id="links" class="paper-section" aria-labelledby="links-heading" tabindex="-1">
          <h2 id="links-heading">Links</h2>
          <ul class="paper-links">
{links_html}
          </ul>
          {missing_html}
        </section>
        <section id="bibtex" class="paper-section" aria-labelledby="bibtex-heading" tabindex="-1">
          <div class="paper-section-heading">
            <h2 id="bibtex-heading">BibTeX</h2>
            <a href="./citation.bib" download="{p['id']}.bib">Download .bib</a>
          </div>
          <pre class="bibtex"><code>{esc(bibtex(p))}</code></pre>
        </section>
      </article>
      <a class="paper-back paper-back-bottom" href="../../#publication">← All publications</a>
    </main>
{dialogs}  </body>
</html>
'''


def main():
    papers = json.loads(DATA.read_text())
    papers.sort(key=lambda p: -int(p['year']))
    ids = [p['id'] for p in papers]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z0-9-]+', i) for i in ids):
        raise ValueError('Publication IDs must be unique lowercase URL slugs.')
    for paper in papers:
        for key in ('image', 'pdf'):
            if paper.get(key) and not (ROOT / 'assets/publications' / paper[key]).is_file():
                raise FileNotFoundError(paper[key])
    homepage_path = ROOT / 'index.html'
    homepage = homepage_path.read_text()
    homepage, count = re.subn(r'      <section id="publication".*?</section>',
                             lambda _: overview(papers), homepage, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one publication section in index.html.')
    homepage_path.write_text(homepage)
    for paper in papers:
        folder = ROOT / 'publications' / paper['id']
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(detail(paper, homepage))
        (folder / 'citation.bib').write_text(bibtex(paper))
    print(f'Generated overview, {len(papers)} detail pages, and {len(papers)} BibTeX files.')


if __name__ == '__main__':
    main()
