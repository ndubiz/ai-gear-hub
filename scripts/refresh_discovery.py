"""Rebuild site search and shared navigation after adding or changing guides (stdlib only)."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import json, re, posixpath

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.title = ''; self.description = ''; self.in_title = False
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title': self.in_title = True
        if tag == 'meta' and a.get('name') == 'description': self.description = a.get('content', '')
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

links = [('index.html', 'Home'), ('guides.html#ai-tools', 'AI Tools'), ('amazon-products.html', 'Products & Gear'), ('switchbot-hub.html', 'SwitchBot'), ('guides.html', 'Comparisons & Guides'), ('reels.html', 'Reels & Content'), ('https://ndubizmarketechcomstart.com/', 'Market Tech')]
catalog = json.loads((ROOT / 'reader-catalog.json').read_text(encoding='utf-8'))
by_path = {p['review']: p for p in catalog}
entries = []
for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(('marketplace/', 'gearhub/')): continue
    original = path.read_text(encoding='utf-8')
    if '<head' not in original or '<h1' not in original: continue
    if 'data-campaign-landing' in original:
        cleaned = re.sub(r'<!-- discovery:start -->.*?<!-- discovery:end -->', '', original, flags=re.S)
        if cleaned != original: path.write_text(cleaned, encoding='utf-8')
        continue
    page = Page(original)
    if rel not in ['404.html', 'checklist-download.html'] and not re.search(r'name=["\']robots["\'][^>]*noindex', original, re.I):
        p = by_path.get(rel, {})
        entries.append(dict(path=rel, title=p.get('name', re.sub(r'\s*[-—|]\s*AI\s*Gear Hub.*$', '', page.title).strip()), description=page.description, category=p.get('category', 'Guides & resources'), keywords=p.get('bestFor', '')))
    prefix = '../' * (len(path.relative_to(ROOT).parts) - 1)
    source = re.sub(r'<!-- discovery:start -->.*?<!-- discovery:end -->', '', original, flags=re.S)
    assets = f'<!-- discovery:start --><link rel="stylesheet" href="{prefix}discovery.css"><script defer src="{prefix}discovery.js"></script><!-- discovery:end -->'
    source = source.replace('</head>', assets + '</head>')
    nav_links = ''.join(f'<a href="{h if h.startswith("https:") else prefix+h}">{escape(label)}</a>' for h, label in links)
    bar = '<!-- discovery:start --><div class="discovery-bar"><details><summary>Explore sections</summary><nav aria-label="Explore AI Gear Hub">'+nav_links+'</nav></details><button type="button" data-discovery-open="search" hidden>Search everything</button><button type="button" data-discovery-open="saved" hidden>My shortlist</button><button type="button" data-discovery-open="recent" hidden>Recently viewed</button></div><!-- discovery:end -->'
    if '</header>' in source: source = source.replace('</header>', '</header>'+bar, 1)
    else: source = re.sub(r'(<body[^>]*>)', lambda m:m[0]+bar, source, count=1)
    source = re.sub(r'<p\b[^>]*>\s*These buttons send an optional purchase-intent click alert.*?</p>', '', source, flags=re.S)
    if rel == 'privacy.html' and 'id="discovery-privacy"' not in source:
        source = source.replace('</main>', '<section id="discovery-privacy"><h2>Saved items and recently viewed pages</h2><p>Your shortlist and up to 12 recently viewed guides are stored in this browser on this device. They are not sent to us or synced to an account. Remove saved items or clear your history using the navigation controls. If browser storage is unavailable, these features work only until you leave the page.</p></section></main>')
    if source != original: path.write_text(source, encoding='utf-8')
(ROOT / 'discovery-index.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Indexed {len(entries)} pages; shared navigation refreshed.')
