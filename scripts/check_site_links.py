"""Check all published HTML links, fragments, local assets and analytics coverage."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ndubiz.github.io/ai-gear-hub/'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.scripts = [], set(), []
        self.redirect = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            self.redirect = True
        if tag == 'script' and attrs.get('src'):
            self.scripts.append(attrs['src'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])

pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in ROOT.rglob('*.html')}
errors = []
for path, page in pages.items():
    name = path.relative_to(ROOT).as_posix()
    if not page.redirect and not any(urlsplit(s).path.endswith('analytics.js') for s in page.scripts):
        errors.append(f'{name}: analytics script missing')
    for href in page.links:
        url = urlsplit(urljoin(BASE + name, href))
        if url.scheme not in ('http', 'https') or url.netloc != 'ndubiz.github.io':
            continue
        if not url.path.startswith('/ai-gear-hub/'):
            continue
        target = (ROOT / unquote(url.path[len('/ai-gear-hub/'):])).resolve()
        if not target.is_relative_to(ROOT):
            errors.append(f'{name}: link outside site -> {href}')
            continue
        if target.is_dir():
            target = target / 'index.html'
        if not target.is_file():
            errors.append(f'{name}: missing file -> {href}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{name}: missing fragment -> {href}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} HTML pages: links, fragments, assets and analytics OK')
