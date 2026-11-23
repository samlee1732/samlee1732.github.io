#!/usr/bin/env python3
"""Build publication, patent, project, team, teaching (including competitions), and news content, BibTeX, and site search."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/publications.json'
esc = html.escape


class SearchTextParser(HTMLParser):
    """Collect actual page section text for search."""

    VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                 'link', 'meta', 'param', 'source', 'track', 'wbr'}

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
                if attrs.get('id') in {'contact', 'research-interests', 'news', 'competitions', 'team', 'teaching', 'robotics-applications', 'automatic-control'}:
                    block = attrs['id']
                elif 'biography' in attrs.get('class', '').split():
                    block = 'about'
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


def search_index(papers, reviews, patents, projects, homepage, news_content, competitions_content, team_content, teaching_content):
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
        description += ' · Under Review'
        entries.append({
            'title': paper['title'],
            'text': description + ' 在审 投稿 论文 稿件 通讯作者 共同作者'
                    + (' 李森' if 'Sen Li' in paper.get('authors', paper.get('co_authors', [])) else ''),
            'description': description,
            # Search stays on public metadata; private workspace URLs are not indexed.
            'url': ('publications/' + paper['id'] + '/'
                    if has_public_review_page(paper)
                    else '#' + paper['id']),
            'kind': 'Under Review',
        })

    for patent in patents:
        description = ('发明人：' + '、'.join(patent['inventors'])
                       + ' · ' + patent['type'] + '（' + patent['status'] + '）')
        entries.append({
            'title': patent['title'],
            'text': description + ' 专利 发明 申请 Patents Patent application'
                    + (' Sen Li' if '李森' in patent['inventors'] else ''),
            'description': description,
            'url': '#' + patent['id'],
            'kind': 'Patent Application',
        })

    for project in projects:
        parts = [project['program'], project['status']]
        parts.extend(['项目经费：' + str(project['funding_wan_cny']) + '万元',
                      project_role(project)])
        if project.get('contribution'):
            parts.append(project['contribution'])
        description = ' · '.join(parts)
        entries.append({
            'title': project['title'],
            'text': description + ' 李森 Sen Li 科研项目 Research Projects',
            'description': description,
            'url': '#' + project['id'],
            'kind': 'Research Project',
        })

    parser = SearchTextParser()
    parser.feed(homepage)
    parser.feed(news_content)
    parser.feed(competitions_content)
    parser.feed(team_content)
    parser.feed(teaching_content)
    parser.close()
    sections = (
        ('about', 'About SenseDex Lab · 实验室简介', 'About', '简介 关于 履历 教育 经历 科研 项目'),
        ('research-interests', 'Research Interests', 'Research', '研究方向 研究兴趣'),
        ('contact', 'Contact · 联系方式', 'Contact', '联系 联系方式 邮箱 邮件 地址 办公室'),
        ('competitions', 'Student Competitions · 指导学生竞赛', 'Teaching', '比赛 竞赛 学生 团队 指导教师 成果 图片'),
        ('news', 'News · 最新动态', 'News', '新闻 动态 消息'),
        ('team', 'Team · 团队', 'Team', '团队 成员 实验室 合作者 合作 collaborators affiliation'),
        ('teaching', 'Teaching', 'Teaching', '教学 课程 授课 责任教师'),
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
        if block in {'robotics-applications', 'automatic-control'}:
            url = 'teaching/' + block + '/'
        elif block == 'competitions':
            url = 'teaching/#competitions'
        else:
            url = block + '/' if block in {'news', 'team', 'teaching'} else '#' + block
        entry = {'title': title, 'text': text + ' ' + keywords, 'description': description,
                 'url': url, 'kind': kind}
        entries.append(entry)
    return entries


def author_legend():
    return ('<p class="author-legend"><span># Equal contribution</span>'
            ' <span aria-hidden="true">·</span> <span>* Corresponding author</span></p>')


def authors(paper):
    names = []
    for name in paper['authors']:
        rendered = '<strong>Sen Li</strong>' if name == 'Sen Li' else esc(name)
        symbols, labels = [], []
        if name in paper.get('equal_contributors', []):
            symbols.append('#')
            labels.append('Equal contribution')
        if name in paper.get('corresponding_authors', []):
            symbols.append('*')
            labels.append('Corresponding author')
        if symbols:
            label = esc('; '.join(labels))
            rendered += (f'<sup class="author-marker" title="{label}" aria-label="{label}">'
                         + ''.join(symbols) + '</sup>')
        names.append(rendered)
    if paper.get('author_conjunction') and len(names) > 1:
        return ', '.join(names[:-1]) + (', and ' if len(names) > 2 else ' and ') + names[-1]
    return ', '.join(names)


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


def image(paper, prefix, lazy=True, preview=False):
    if preview and paper.get('overview_image'):
        # Overview collages are separate from the original detail-page media.
        paper = {**paper, 'image': paper['overview_image'],
                 'image_width': paper['overview_width'],
                 'image_height': paper['overview_height'],
                 'image_alt': paper['overview_alt']}
    if not paper.get('image'):
        return ('<div class="publication-placeholder">'
                '<span>Image / video coming soon</span>'
                '<span lang="zh-CN">论文图片或视频待补充</span></div>')
    attrs = ' loading="lazy"' if lazy else ''
    if paper.get('image_width') and paper.get('image_height'):
        attrs += f' width="{paper["image_width"]}" height="{paper["image_height"]}"'
    fallback = (f'<img src="{prefix}assets/publications/{esc(paper["image"])}"'
                f' alt="{esc(paper["image_alt"])}" decoding="async"{attrs}>')
    if preview and paper.get('preview_image'):
        # Prefer the compact WebP, with the selected image as fallback.
        return (f'<picture><source srcset="{prefix}assets/publications/{esc(paper["preview_image"])}"'
                f' type="image/webp">{fallback}</picture>')
    return fallback


def published_overview(papers):
    rows = []
    for p in papers:
        url = './publications/' + p['id'] + '/'
        description = 'Abstract' if p.get('abstract') else 'Summary'
        links = [(description, url + '#abstract'), ('Links', url + '#links'), ('BibTeX', url + '#bibtex')]
        if p.get('pdf'):
            links.append((p.get('pdf_label', 'PDF'), url + '#pdf'))
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
                <a href="{url}" aria-label="Read about {esc(p['marker'])}">{image(p, './', preview=True)}</a>
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


def private_workspace_url(paper):
    """Validate an optional GitHub workspace link without reading its contents."""
    url = paper.get('private_workspace_url')
    if not url:
        return None
    if not isinstance(url, str):
        raise ValueError('private_workspace_url must be a GitHub HTTPS URL.')
    parts = urlsplit(url)
    if (parts.scheme != 'https' or parts.netloc != 'github.com'
            or len([part for part in parts.path.split('/') if part]) < 2):
        raise ValueError('private_workspace_url must be a GitHub HTTPS repository URL.')
    return url


def has_public_review_page(paper):
    return bool(paper.get('demo')) and not paper.get('private_workspace_url')


def review_overview(papers):
    rows = []
    for p in papers:
        author_line = (authors(p) if p.get('authors') else 'Co-authors: ' + '; '.join(
            '<strong>Sen Li</strong>' if name == 'Sen Li' else esc(name) for name in p['co_authors']))
        corresponding = ('\n                <p>Corresponding author: '
                         + esc(p['corresponding_author']) + '</p>') if p.get('corresponding_author') else ''
        title = esc(p['title'])
        workspace_url = private_workspace_url(p)
        if workspace_url:
            url = esc(workspace_url)
            title = f'<a href="{url}">{title}</a>'
            # A real, keyboard-accessible link with a deliberately empty media area.
            figure = (f'<a class="publication-media publication-private-placeholder" href="{url}"'
                      f' aria-label="Open private GitHub workspace: {esc(p["title"])}"></a>')
        else:
            caption = ('\n                <figcaption class="publication-media-caption">'
                       + esc(p['image_caption']) + '</figcaption>') if p.get('image_caption') else ''
            preview = image(p, './', preview=True)
            figure = f'<figure class="publication-media">{preview}{caption}</figure>'
            if has_public_review_page(p):
                url = './publications/' + p['id'] + '/'
                title = f'<a href="{url}">{title}</a>'
                figure = (f'<a href="{url}" aria-label="View project and video: {esc(p["title"])}">'
                          f'<figure class="publication-media">{preview}'
                          '<figcaption class="publication-media-caption">View project and video</figcaption></figure></a>')
        rows.append(f'''          <li>
            <article id="{p['id']}" class="publication-row" aria-labelledby="{p['id']}-title" tabindex="-1">
              <div class="publication-details">
                <p class="publication-authors">{author_line}</p>
                <h4 id="{p['id']}-title" class="publication-title">{title} <span class="publication-type review-status">Under Review</span></h4>
                <p class="publication-citation">Submitted to <cite>{esc(p['journal'])}</cite>.</p>{corresponding}
              </div>
              {figure}
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
            + '        ' + author_legend() + '\n'
            + groups + '\n      </section>\n'
            + '      <!-- PUBLICATION CONTENT END -->')


def patent_overview(patents):
    rows = []
    for patent in patents:
        inventors = '、'.join('<strong>李森</strong>' if name == '李森' else esc(name)
                            for name in patent['inventors'])
        rows.append(f'''          <li>
            <article id="{esc(patent['id'])}" class="patent-entry" aria-labelledby="{esc(patent['id'])}-title" tabindex="-1" lang="zh-CN">
              <p class="publication-authors">发明人：{inventors}</p>
              <h3 id="{esc(patent['id'])}-title" class="publication-title">{esc(patent['title'])} <span class="publication-type">{esc(patent['type'])}</span> <span class="publication-type review-status">{esc(patent['status'])}</span></h3>
            </article>
          </li>''')
    return ('      <!-- PATENT CONTENT START -->\n'
            '      <section id="patents" class="publications patents" aria-labelledby="patents-heading" tabindex="-1">\n'
            '        <h2 id="patents-heading">Patents</h2>\n'
            '        <!-- Generated from data/patents.json by tools/build_publications.py. -->\n'
            '        <ol class="publication-list">\n'
            + '\n'.join(rows) + '\n        </ol>\n      </section>\n'
            + '      <!-- PATENT CONTENT END -->')


def project_month(value):
    year, month = value.split('-')
    return f'{year}年{int(month)}月'


def project_period(project):
    if not (project.get('start_date') and project.get('end_date')):
        return ''
    return project_month(project['start_date']) + '—' + project_month(project['end_date'])


def project_role(project):
    if project.get('principal_investigator'):
        return '主持：' + project['principal_investigator']
    return project['role']


def project_overview(projects):
    rows = []
    for project in projects:
        contribution = ('\n              <p>' + esc(project['contribution']) + '</p>'
                        if project.get('contribution') else '')
        rows.append(f'''          <li>
            <article id="{esc(project['id'])}" class="project-entry" aria-labelledby="{esc(project['id'])}-title" tabindex="-1" lang="zh-CN">
              <p class="project-program">{esc(project['program'])}</p>
              <h3 id="{esc(project['id'])}-title" class="publication-title">{esc(project['title'])} <span class="publication-type project-status">{esc(project['status'])}</span></h3>
              <p class="project-meta"><span>项目经费：{esc(str(project['funding_wan_cny']))}万元</span></p>
              <p>{esc(project_role(project))}</p>{contribution}
            </article>
          </li>''')
    return ('      <!-- PROJECT CONTENT START -->\n'
            '      <section id="projects" class="publications projects" aria-labelledby="projects-heading" tabindex="-1">\n'
            '        <h2 id="projects-heading">Projects</h2>\n'
            '        <p class="projects-intro" lang="zh-CN">近年主持及参与的纵向与横向科研项目。</p>\n'
            '        <!-- Generated from data/projects.json by tools/build_publications.py. -->\n'
            '        <ol class="publication-list">\n'
            + '\n'.join(rows) + '\n        </ol>\n      </section>\n'
            + '      <!-- PROJECT CONTENT END -->')


def site_header(homepage, prefix, current):
    header = re.search(r'    <header\b.*?</header>', homepage, re.S).group()
    header = header.replace('href="./', f'href="{prefix}')
    header = header.replace('href="#', f'href="{prefix}#')
    header = header.replace('src="./assets/', f'src="{prefix}assets/')
    header = header.replace(f'class="nav-link is-current" href="{prefix}" aria-current="page"', f'class="nav-link" href="{prefix}"')
    header = header.replace(f'class="nav-link" href="{prefix}{current}"', f'class="nav-link is-current" href="{prefix}{current}" aria-current="page"')
    return header


def content_page(homepage, content, slug, title, description, source=None):
    prefix = '../' * (slug.count('/') + 1)
    is_course = slug.startswith('teaching/')
    styles_version = {
        'teaching': '20261114-course-links',
        'team': '20261123-team-profiles',
    }.get(slug, '20261114-teaching-competitions')
    script_version = styles_version if slug == 'team' else '20261114-teaching-competitions'
    current = 'teaching/' if is_course else slug + '/'
    header = site_header(homepage, prefix, current)
    back_url = prefix + 'teaching/' if is_course else prefix
    back_label = 'Teaching' if is_course else 'Homepage'
    source = source or slug
    course_layout = ' course-document' if source == 'robotics-applications' else ''
    course_styles = (f'\n    <link rel="stylesheet" href="{prefix}assets/course-syllabus.css?v=20261114-simple">'
                     if source == 'robotics-applications' else '')
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{esc(description)}">
    <meta name="theme-color" content="#92316f">
    <title>{esc(title)} | SenseDex Lab</title>
    <link rel="icon" href="{prefix}assets/sensedex-mark-small.png" type="image/png">
    <link rel="apple-touch-icon" href="{prefix}assets/sensedex-mark-small.png">
    <link rel="stylesheet" href="{prefix}assets/styles.css?v={styles_version}">{course_styles}
    <script src="{prefix}assets/main.js?v={script_version}" defer></script>
    <script src="{prefix}assets/visits.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
{header}
    <main id="main-content" class="container main-content news-page{course_layout}">
      <a class="paper-back" href="{back_url}">← {back_label}</a>
      <!-- Page content is maintained in data/{esc(source)}.html. -->
{content.rstrip()}
    </main>
  </body>
</html>
'''


def news_page(homepage, content):
    return content_page(homepage, content, 'news', 'News',
                        'News and updates from SenseDex Lab — Sensing and Dexterous Manipulation.')


def competitions_page(homepage, content):
    # Preserve existing bookmarks after moving competitions into Teaching.
    return '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="0; url=../teaching/#competitions">
    <link rel="canonical" href="https://www.sensedex.online/teaching/#competitions">
    <title>Student Competitions | Teaching | SenseDex Lab</title>
    <script>window.location.replace('../teaching/#competitions');</script>
  </head>
  <body>
    <p>Student competitions are now part of Teaching. <a href="../teaching/#competitions">View student competitions</a>.</p>
  </body>
</html>
'''



def pdf_section(p):
    if not p.get('pdf'):
        return ''
    pdf_url = '../../assets/publications/' + p['pdf']
    paper_name = esc(p['marker'])
    version_line = ''
    if p.get('article_in_press_pdf'):
        publisher_url = '../../assets/publications/' + esc(p['article_in_press_pdf'])
        version_line = ('          <p class="paper-note">Author preprint · '
                        f'<a href="{publisher_url}">Publisher’s article-in-press PDF</a></p>\n')
    return f'''        <section id="pdf" class="paper-section" aria-label="Read the {paper_name} paper" tabindex="-1">
{version_line}          <iframe class="paper-pdf-viewer" src="../../assets/pdfjs/web/viewer.html?profile={p['id']}&amp;file=../../publications/{esc(p['pdf'])}#zoom=auto" title="PDF: {esc(p['title'])}" loading="lazy"></iframe>
          <noscript><p><a href="{esc(pdf_url)}">Open the {paper_name} PDF</a></p></noscript>
        </section>
'''


def paper_document(homepage, title, description, article, layout='paper-page'):
    header = site_header(homepage, '../../', '#publication')
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{esc(description)}">
    <meta name="theme-color" content="#92316f">
    <title>{esc(title)} | SenseDex Lab</title>
    <link rel="icon" href="../../assets/sensedex-mark-small.png" type="image/png">
    <link rel="apple-touch-icon" href="../../assets/sensedex-mark-small.png">
    <link rel="stylesheet" href="../../assets/styles.css?v=20261120-paper-resources">
    <script src="../../assets/main.js?v=20261114-teaching-competitions" defer></script>
    <script src="../../assets/visits.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
{header}
    <main id="main-content" class="container {layout}">
      <a class="paper-back" href="../../#publication">← All publications</a>
      <article>
{article}      </article>
      <a class="paper-back paper-back-bottom" href="../../#publication">← All publications</a>
    </main>
  </body>
</html>
'''


RESOURCE_ICONS = {
    'code': '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82A7.65 7.65 0 0 1 8 3.86c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>',
    'doi': '<circle cx="8" cy="8" r="7"/><text x="8" y="10.5" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="7.5" font-weight="bold">doi</text>',
    'video': '<rect x="1" y="3" width="14" height="10" rx="3"/><path d="M7 5.5v5l4-2.5z" fill="white"/>',
    'link': '<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="m6.5 5 2-2a3 3 0 0 1 4.2 4.2l-2 2M9.5 11l-2 2a3 3 0 0 1-4.2-4.2l2-2M5.5 10.5l5-5"/></g>',
}


def resource_section(p):
    resources = []
    code = p.get('code') or p.get('simulation_url')
    if code:
        resources.append(('code', code, code))
    if p.get('doi'):
        resources.append(('doi', 'doi:' + p['doi'], 'https://doi.org/' + p['doi']))
    elif p.get('paper'):
        resources.append(('link', 'Publisher’s article', p['paper']))
    if p.get('video') and not p.get('article_media'):
        resources.append(('video', 'Video on YouTube', p['video']))
    for resource in p.get('additional_links', []):
        resources.append(('link', resource['label'], resource['url']))
    if not resources:
        return ''
    rows = []
    for kind, label, url in resources:
        rows.append(f'''            <li>
              <a href="{esc(url)}">
                <svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">{RESOURCE_ICONS[kind]}</svg>
                <span>{esc(label)}</span>
              </a>
            </li>''')
    items = '\n'.join(rows)
    return f'''        <section id="links" class="paper-section" aria-labelledby="links-heading" tabindex="-1">
          <h2 id="links-heading">Links</h2>
          <ul class="article-resources">
{items}
          </ul>
        </section>
'''


def review_detail(p, homepage):
    demo = p['demo']
    prefix = '../../assets/publications/'
    video = prefix + esc(demo['file'])
    article = f'''        <header class="paper-heading">
          <p class="paper-eyebrow"><span class="publication-type review-status">Under Review</span></p>
          <h1>{esc(p['title'])}</h1>
          <p class="paper-authors">{authors(p)}</p>
          <p class="author-legend">* Corresponding author</p>
          <p class="paper-citation">Submitted to <cite>{esc(p['journal'])}</cite>.</p>
        </header>
        <section class="paper-section paper-demo" id="video" aria-labelledby="video-heading">
          <h2 id="video-heading">Video</h2>
          <video controls playsinline preload="none" poster="{prefix}{esc(demo['poster'])}" width="{demo['width']}" height="{demo['height']}" aria-label="{esc(demo['label'])}">
            <source src="{video}" type="video/mp4">
          </video>
        </section>
        <section class="paper-section" aria-labelledby="overview-heading">
          <h2 id="overview-heading">Project overview</h2>
          <p>{esc(p['summary'])}</p>
        </section>
{resource_section(p)}'''
    return paper_document(homepage, p['title'], p['summary'], article)


def illustrated_detail(p, homepage):
    media = p['article_media']
    assets = '../../assets/publications/'
    abstract = p['abstract'] if isinstance(p['abstract'], str) else ' '.join(p['abstract'])
    article = f'''        <header class="paper-heading">
          <p class="paper-eyebrow">{p['year']} · {esc(p['type'])}</p>
          <h1>{esc(p['title'])}</h1>
        </header>
        <figure class="article-summary-figure">
          <img src="{assets}{esc(media['figure'])}" alt="{esc(media['figure_alt'])}" width="{media['figure_width']}" height="{media['figure_height']}" decoding="async">
        </figure>
        <div class="article-byline">
          <p>{authors(p)}. <a href="{esc(p['paper'])}">{citation(p)}</a></p>
          <p class="author-legend">* Corresponding author</p>
        </div>
        <figure id="video" class="article-video">
          <video width="{media['video_width']}" height="{media['video_height']}" controls playsinline controlslist="nodownload" preload="none" poster="{assets}{esc(media['poster'])}" aria-label="{esc(p['marker'])} supplementary video">
            <source src="{assets}{esc(media['video'])}" type="video/mp4">
          </video>
        </figure>
        <section id="abstract" class="paper-section" aria-labelledby="abstract-heading" tabindex="-1">
          <h2 id="abstract-heading">Abstract</h2>
          <p>{esc(abstract)}</p>
        </section>
{resource_section(p)}        <section id="bibtex" class="paper-section" aria-labelledby="bibtex-heading" tabindex="-1">
          <h2 id="bibtex-heading">BibTeX <small>(<a href="./citation.bib" download="{esc(p['id'])}.bib">Download</a>)</small></h2>
          <pre class="bibtex"><code>{esc(bibtex(p))}</code></pre>
        </section>
{pdf_section(p)}'''
    return paper_document(homepage, p['marker'], p['summary'], article,
                          layout='paper-page illustrated-paper')


def detail(p, homepage):
    if p.get('article_media'):
        return illustrated_detail(p, homepage)
    section_name = 'Abstract' if p.get('abstract') else 'Summary'
    paragraphs = p.get('abstract') or [p['summary']]
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    paragraphs_html = '\n'.join('          <p>' + esc(text) + '</p>' for text in paragraphs)
    if not p.get('abstract'):
        paragraphs_html += '\n          <p class="paper-note">Full abstract to be added.</p>'
    article = f'''        <header class="paper-heading">
          <p class="paper-eyebrow">{p['year']} <span aria-hidden="true">·</span> {esc(p['type'])}</p>
          <h1>{esc(p['title'])}</h1>
          <p class="paper-authors">{authors(p)}</p>
          {author_legend()}
          <p class="paper-citation"><a href="{esc(p['paper'])}">{citation(p)}</a></p>
        </header>
        <figure class="paper-figure">
          {image(p, '../../', lazy=False)}
        </figure>
        <section id="abstract" class="paper-section" aria-labelledby="abstract-heading" tabindex="-1">
          <h2 id="abstract-heading">{section_name}</h2>
{paragraphs_html}
        </section>
{resource_section(p)}        <section id="bibtex" class="paper-section" aria-labelledby="bibtex-heading" tabindex="-1">
          <div class="paper-section-heading">
            <h2 id="bibtex-heading">BibTeX</h2>
            <a href="./citation.bib" download="{p['id']}.bib">Download .bib</a>
          </div>
          <pre class="bibtex"><code>{esc(bibtex(p))}</code></pre>
        </section>
{pdf_section(p)}'''
    return paper_document(homepage, p['marker'], p['summary'], article, layout='paper-page publication-paper')


def main():
    papers = json.loads(DATA.read_text())
    reviews = json.loads((ROOT / 'data/under-review.json').read_text())
    patents = json.loads((ROOT / 'data/patents.json').read_text())
    projects = json.loads((ROOT / 'data/projects.json').read_text())
    # Preserve the curated display order in data/publications.json.
    ids = [p['id'] for p in papers + reviews + patents + projects]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z0-9-]+', i) for i in ids):
        raise ValueError('Publication IDs must be unique lowercase URL slugs.')
    for paper in papers + reviews:
        for role in ('corresponding_authors', 'equal_contributors'):
            unknown = set(paper.get(role, [])) - set(paper.get('authors', []))
            if unknown:
                raise ValueError('Author role references unknown names: ' + ', '.join(sorted(unknown)))
        for key in ('image', 'pdf', 'article_in_press_pdf', 'preview_image', 'overview_image'):
            if paper.get(key) and not (ROOT / 'assets/publications' / paper[key]).is_file():
                raise FileNotFoundError(paper[key])
        if paper.get('article_media'):
            for key in ('figure', 'poster', 'video'):
                asset = ROOT / 'assets/publications' / paper['article_media'][key]
                if not asset.is_file():
                    raise FileNotFoundError(asset)
        if paper.get('demo'):
            for key in ('file', 'poster'):
                asset = ROOT / 'assets/publications' / paper['demo'][key]
                if not asset.is_file():
                    raise FileNotFoundError(asset)
    homepage_path = ROOT / 'index.html'
    homepage = homepage_path.read_text()
    homepage, count = re.subn(
        r'      <!-- PUBLICATION CONTENT START -->.*?<!-- PUBLICATION CONTENT END -->',
        lambda _: publication_overview(papers, reviews), homepage, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one marked Publication content block in index.html.')
    homepage, count = re.subn(
        r'      <!-- PATENT CONTENT START -->.*?<!-- PATENT CONTENT END -->',
        lambda _: patent_overview(patents), homepage, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one marked patent content block in index.html.')
    homepage, count = re.subn(
        r'      <!-- PROJECT CONTENT START -->.*?<!-- PROJECT CONTENT END -->',
        lambda _: project_overview(projects), homepage, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one marked project content block in index.html.')
    homepage_path.write_text(homepage)
    news_content = (ROOT / 'data/news.html').read_text()
    news_folder = ROOT / 'news'
    news_folder.mkdir(exist_ok=True)
    (news_folder / 'index.html').write_text(news_page(homepage, news_content))
    competitions_content = (ROOT / 'data/competitions.html').read_text()
    competitions_folder = ROOT / 'competitions'
    competitions_folder.mkdir(exist_ok=True)
    (competitions_folder / 'index.html').write_text(competitions_page(homepage, competitions_content))
    team_content = (ROOT / 'data/team.html').read_text()
    team_folder = ROOT / 'team'
    team_folder.mkdir(exist_ok=True)
    (team_folder / 'index.html').write_text(content_page(homepage, team_content, 'team', 'Team',
        'Meet the principal investigator, current students, collaborators, and alumni of SenseDex Lab.'))
    teaching_content = (ROOT / 'data/teaching.html').read_text()
    teaching_folder = ROOT / 'teaching'
    teaching_folder.mkdir(exist_ok=True)
    (teaching_folder / 'index.html').write_text(content_page(homepage, teaching_content + '\n' + competitions_content, 'teaching', 'Teaching',
        'Courses and student competition mentorship at Shenzhen Polytechnic University.'))
    for course_id, title in (
            ('robotics-applications', 'Robotics and Applications'),
            ('automatic-control', 'Principles of Automatic Control')):
        course_content = (ROOT / 'data' / (course_id + '.html')).read_text()
        course_folder = teaching_folder / course_id
        course_folder.mkdir(exist_ok=True)
        description = (title + ' at Shenzhen Polytechnic University. Course introduction, instructor information, teaching schedule, and robot platform resources.'
                       if course_id == 'robotics-applications' else title + ' at Shenzhen Polytechnic University. Course details and materials will be added.')
        (course_folder / 'index.html').write_text(content_page(homepage, course_content,
            'teaching/' + course_id, title, description, source=course_id))
        teaching_content += '\n' + course_content
    for paper in papers:
        folder = ROOT / 'publications' / paper['id']
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(detail(paper, homepage))
        (folder / 'citation.bib').write_text(bibtex(paper))
    review_pages = [paper for paper in reviews if has_public_review_page(paper)]
    for paper in review_pages:
        folder = ROOT / 'publications' / paper['id']
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(review_detail(paper, homepage))
    entries = search_index(papers, reviews, patents, projects, homepage, news_content, competitions_content, team_content, teaching_content)
    (ROOT / 'assets/search-index.json').write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Generated Team, Teaching (including competitions), two course and News pages, a legacy competition redirect, {len(reviews)} under-review entries, {len(patents)} patent entries, {len(projects)} project entries, {len(papers) + len(review_pages)} detail pages, {len(papers)} BibTeX files, and {len(entries)} search records.')


if __name__ == '__main__':
    main()
