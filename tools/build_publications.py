#!/usr/bin/env python3
"""Build publication, news, and competition pages, BibTeX, and site search."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/publications.json'
esc = html.escape


class SearchTextParser(HTMLParser):
    """Collect actual homepage section and dialog-template text for search."""

    VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    PANELS = {'team', 'robotics-applications', 'automatic-control'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = {}
        self.active = None
        self.depth = 0
        self.ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.active is None:
            block = None
            if tag == 'section':
                if attrs.get('id') in {'contact', 'news', 'competitions'}:
                    block = attrs['id']
                elif 'biography' in attrs.get('class', '').split():
                    block = 'about'
            elif tag == 'template' and attrs.get('id') in self.PANELS:
                block = attrs['id']
            if block:
                self.active = block
                self.blocks.setdefault(block, [])
                self.depth = 1
        elif tag not in self.VOID_TAGS:
            self.depth += 1
            if tag in {'script', 'style'} or self.ignored_depth:
                self.ignored_depth += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.active is None or tag in self.VOID_TAGS:
            return
        if self.ignored_depth:
            self.ignored_depth -= 1
        self.depth -= 1
        if self.depth == 0:
            self.active = None

    def handle_data(self, data):
        if self.active is not None and not self.ignored_depth:
            self.blocks[self.active].append(data)


def search_index(papers, reviews, homepage, news_content, competitions_content):
    """Use one shared index on the homepage and all publication detail pages."""
    entries = []
    for paper in papers:
        terms = []
        for field in ('title', 'authors', 'marker', 'venue', 'year', 'doi',
                      'summary', 'abstract', 'type', 'status'):
            value = paper.get(field)
            if value:
                if isinstance(value, list):
                    terms.extend(str(item) for item in value)
                else:
                    terms.append(str(value))
        entries.append({
            'title': paper['title'],
            'text': ' '.join(terms + ['论文 发表 文献 研究成果 作者 摘要']
                             + (['李森'] if 'Sen Li' in paper['authors'] else [])),
            'description': ', '.join(paper['authors']) + ' · ' + paper['venue'] + ' · ' + str(paper['year']),
            'url': 'publications/' + paper['id'] + '/',
            'kind': 'Publication',
        })

    for paper in reviews:
        description = ('Authors: ' + ', '.join(paper['authors']) if paper.get('authors')
                       else 'Co-authors: ' + '; '.join(paper['co_authors']))
        if paper.get('corresponding_author'):
            description += ' · Corresponding author: ' + paper['corresponding_author']
        description += ' · Submitted to ' + paper['journal']
        if paper.get('manuscript_number'):
            description += ' · ' + paper['manuscript_number']
        description += ' · Under Review'
        entries.append({
            'title': paper['title'],
            'text': description + ' 在审 投稿 论文 稿件 通讯作者 共同作者'
                    + (' 李森' if 'Sen Li' in paper.get('authors', paper.get('co_authors', [])) else ''),
            'description': description,
            'url': '#' + paper['id'],
            'kind': 'Under Review',
        })

    parser = SearchTextParser()
    parser.feed(homepage)
    parser.feed(news_content)
    parser.feed(competitions_content)
    parser.close()
    sections = (
        ('about', 'About SenseDex Lab · 实验室简介', 'About', '简介 关于 履历 教育 经历 科研 项目'),
        ('contact', 'Contact · 联系方式', 'Contact', '联系 联系方式 邮箱 邮件 地址 办公室'),
        ('competitions', 'Student Competitions · 指导学生竞赛', 'Competitions', '比赛 竞赛 学生 团队 指导教师 成果 图片'),
        ('news', 'News · 最新动态', 'News', '新闻 动态 消息'),
        ('team', 'Team · 团队', 'Team', '团队 成员 实验室'),
        ('robotics-applications', 'Robotics and Applications · 机器人学及应用', 'Teaching', '教学 课程 机器人学及应用'),
        ('automatic-control', 'Principles of Automatic Control · 自动控制原理', 'Teaching', '教学 课程 自动控制原理'),
    )
    for block, title, kind, keywords in sections:
        text = ' '.join(' '.join(parser.blocks.get(block, [])).split())
        if not text:
            raise ValueError('Missing site search content: ' + block)
        description = text
        if block == 'contact':
            emails = re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text)
            if emails:
                description = ' · '.join(emails) + ' · ' + text
        entry = {'title': title, 'text': text + ' ' + keywords, 'description': description,
                 'url': block + '/' if block in {'news', 'competitions'} else '#' + block, 'kind': kind}
        if block in parser.PANELS:
            entry['panel'] = block
        entries.append(entry)
    return entries


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
    if not paper.get('image'):
        return ('<div class="publication-placeholder">'
                '<span>Image / video coming soon</span>'
                '<span lang="zh-CN">论文图片或视频待补充</span></div>')
    attrs = ' loading="lazy"' if lazy else ''
    if paper.get('image_width') and paper.get('image_height'):
        attrs += f' width="{paper["image_width"]}" height="{paper["image_height"]}"'
    return (f'<img src="{prefix}assets/publications/{esc(paper["image"])}"'
            f' alt="{esc(paper["image_alt"])}" decoding="async"{attrs}>')


def published_overview(papers):
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
                <h4 id="{p['id']}-title" class="publication-title"><a href="{url}">{esc(p['title'])}</a> <span class="publication-type">{esc(p['type'])}</span></h4>
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
    return '''      <section id="published-papers" class="publication-group" aria-labelledby="published-papers-heading" tabindex="-1">
        <h3 id="published-papers-heading">Published Papers</h3>
        <!-- Generated from data/publications.json by tools/build_publications.py. -->
        <ol class="publication-list">
''' + '\n'.join(rows) + '''
        </ol>
      </section>'''


def review_overview(papers):
    rows = []
    for p in papers:
        author_line = (authors(p) if p.get('authors') else 'Co-authors: ' + '; '.join(
            '<strong>Sen Li</strong>' if name == 'Sen Li' else esc(name) for name in p['co_authors']))
        manuscript = ('\n                <p>Manuscript no.: <span class="manuscript-number">'
                      + esc(p['manuscript_number']) + '</span></p>') if p.get('manuscript_number') else ''
        corresponding = ('\n                <p>Corresponding author: '
                         + esc(p['corresponding_author']) + '</p>') if p.get('corresponding_author') else ''
        rows.append(f'''          <li>
            <article id="{p['id']}" class="publication-row" aria-labelledby="{p['id']}-title" tabindex="-1">
              <div class="publication-details">
                <p class="publication-authors">{author_line}</p>
                <h4 id="{p['id']}-title" class="publication-title">{esc(p['title'])} <span class="publication-type review-status">Under Review</span></h4>
                <p class="publication-citation">Submitted to <cite>{esc(p['journal'])}</cite>.</p>{corresponding}{manuscript}
                <ul class="publication-resources" aria-label="Pending manuscript resources">
                  <li><span aria-disabled="true">Abstract <span class="resource-pending">(to be added)</span></span></li>
                  <li><span aria-disabled="true">BibTeX <span class="resource-pending">(to be added)</span></span></li>
                </ul>
              </div>
              <div class="publication-media">{image(p, './')}</div>
            </article>
          </li>''')
    return '''      <section id="under-review" class="publication-group under-review" aria-labelledby="under-review-heading" tabindex="-1">
        <h3 id="under-review-heading">Under Review</h3>
        <!-- Generated from data/under-review.json by tools/build_publications.py. -->
        <ol class="publication-list">
''' + '\n'.join(rows) + '''
        </ol>
      </section>'''


def publication_overview(papers, reviews):
    groups = review_overview(reviews) + '\n' + published_overview(papers)
    groups = '\n'.join('  ' + line for line in groups.splitlines())
    return ('      <!-- PUBLICATION CONTENT START -->\n'
            '      <section id="publication" class="publications" aria-labelledby="publication-heading" tabindex="-1">\n'
            '        <h2 id="publication-heading">Publication</h2>\n'
            + groups + '\n      </section>\n'
            + '      <!-- PUBLICATION CONTENT END -->')


def site_header(homepage, prefix, current):
    header = re.search(r'    <header\b.*?</header>', homepage, re.S).group()
    header = header.replace('href="./', f'href="{prefix}')
    header = header.replace('href="#', f'href="{prefix}#')
    header = header.replace('src="./assets/', f'src="{prefix}assets/')
    header = header.replace(f'class="nav-link is-current" href="{prefix}" aria-current="page"', f'class="nav-link" href="{prefix}"')
    header = header.replace(f'class="nav-link" href="{prefix}{current}"', f'class="nav-link is-current" href="{prefix}{current}" aria-current="page"')
    return header


def content_page(homepage, content, slug, title, description):
    header = site_header(homepage, '../', slug + '/')
    dialogs = homepage[homepage.index('    <dialog'):homepage.index('  </body>')]
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{esc(description)}">
    <meta name="theme-color" content="#92316f">
    <title>{esc(title)} | SenseDex Lab</title>
    <link rel="icon" href="../assets/sensedex-mark.png" type="image/png">
    <link rel="apple-touch-icon" href="../assets/sensedex-mark.png">
    <link rel="stylesheet" href="../assets/styles.css">
    <script src="../assets/main.js" defer></script>
    <script src="../assets/visits.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
{header}
    <main id="main-content" class="container main-content news-page">
      <a class="paper-back" href="../">← Homepage</a>
      <!-- Page content is maintained in data/{esc(slug)}.html. -->
{content.rstrip()}
    </main>
{dialogs}  </body>
</html>
'''


def news_page(homepage, content):
    return content_page(homepage, content, 'news', 'News',
                        'News and updates from SenseDex Lab — Sensing and Dexterous Manipulation.')


def competitions_page(homepage, content):
    return content_page(homepage, content, 'competitions', 'Student Competitions',
                        'Student competitions and faculty mentorship at SenseDex Lab. Details will be added as they become available.')


def detail(p, homepage):
    header = site_header(homepage, '../../', '#publication')
    dialogs = homepage[homepage.index('    <dialog'):homepage.index('  </body>')]
    section_name = 'Abstract' if p.get('abstract') else 'Summary'
    paragraphs = p.get('abstract') or [p['summary']]
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    paragraphs_html = '\n'.join('          <p>' + esc(text) + '</p>' for text in paragraphs)
    if not p.get('abstract'):
        paragraphs_html += '\n          <p class="paper-note">Full abstract to be added.</p>'
    elif p.get('abstract_license') and p.get('abstract_source'):
        paragraphs_html += ('\n          <p class="paper-note"><a href="' + esc(p['abstract_source'])
                            + '">Abstract source</a> · <a href="' + esc(p['abstract_license'])
                            + '">CC BY 4.0</a></p>')
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
    <script src="../../assets/visits.js" defer></script>
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
    reviews = json.loads((ROOT / 'data/under-review.json').read_text())
    papers.sort(key=lambda p: -int(p['year']))
    ids = [p['id'] for p in papers + reviews]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z0-9-]+', i) for i in ids):
        raise ValueError('Publication IDs must be unique lowercase URL slugs.')
    for paper in papers + reviews:
        for key in ('image', 'pdf'):
            if paper.get(key) and not (ROOT / 'assets/publications' / paper[key]).is_file():
                raise FileNotFoundError(paper[key])
    homepage_path = ROOT / 'index.html'
    homepage = homepage_path.read_text()
    homepage, count = re.subn(
        r'      <!-- PUBLICATION CONTENT START -->.*?<!-- PUBLICATION CONTENT END -->',
        lambda _: publication_overview(papers, reviews), homepage, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one marked Publication content block in index.html.')
    homepage_path.write_text(homepage)
    news_content = (ROOT / 'data/news.html').read_text()
    news_folder = ROOT / 'news'
    news_folder.mkdir(exist_ok=True)
    (news_folder / 'index.html').write_text(news_page(homepage, news_content))
    competitions_content = (ROOT / 'data/competitions.html').read_text()
    competitions_folder = ROOT / 'competitions'
    competitions_folder.mkdir(exist_ok=True)
    (competitions_folder / 'index.html').write_text(competitions_page(homepage, competitions_content))
    for paper in papers:
        folder = ROOT / 'publications' / paper['id']
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(detail(paper, homepage))
        (folder / 'citation.bib').write_text(bibtex(paper))
    entries = search_index(papers, reviews, homepage, news_content, competitions_content)
    (ROOT / 'assets/search-index.json').write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Generated News and Competitions pages, {len(reviews)} under-review entries, {len(papers)} detail pages, {len(papers)} BibTeX files, and {len(entries)} search records.')


if __name__ == '__main__':
    main()
