"""Generate static trust/badge/date markup and the quick-compare catalog.

Run after editorial changes: python scripts/refresh_reader_features.py
Dependency: beautifulsoup4. Never infer a price-check date from an edit date.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from datetime import date, datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ndubiz.github.io/ai-gear-hub/'
TODAY = date.today().isoformat()
GIT = os.environ.get('GIT_EXECUTABLE', 'git')
MANIFEST = ROOT / 'reader-freshness.json'
previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
records = {}

def parse(text): return BeautifulSoup(text, 'html.parser')
def text(el): return el.get_text(' ', strip=True) if el else ''
def key(href, page='index.html'):
    u = urljoin(BASE + page, href)
    return u[len(BASE):].split('#')[0] if u.startswith(BASE) else u.split('#')[0]

badges = {
 'product-guides/philips-hue-white-and-color-ambiance-starter-kit.html': {
  'label': "Editor's Pick", 'kind':'editor', 'reason':'For building a coordinated Hue lighting setup. Choose the correct fitting and check which Bridge and bulbs the kit includes; this is not a lowest-price award.',
  'source':'https://www.philips-hue.com/en-us/products/smart-light-starter-kits', 'reviewed':'2026-09-09', 'reviewDue':'2026-11-09'},
 'product-guides/logitech-c920-hd-pro-webcam.html': {
  'label':'Best for Beginners', 'kind':'beginner', 'reason':'For straightforward computer video calls: a USB-A webcam with 1080p capture. Check ports and software support; this is not a home-security camera.',
  'source':'https://secure.logitech.com/assets/45920/8/hd-pro-webcam-c920-quick-start-guide.pdf', 'reviewed':'2026-09-09', 'reviewDue':'2026-11-09'}
}

pages = {p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8') for p in ROOT.rglob('*.html') if '.git' not in p.parts}
catalog = {}
for p in json.loads((ROOT/'product-guides/products.json').read_text(encoding='utf-8')):
    review = 'product-guides/'+p['slug']+'.html'
    if review not in pages: continue
    catalog[review] = dict(id=review, review=review, name=p['name'], category=p['category'], bestFor=p['best_for'], strengths=p['strengths'], cautions=p['cautions'], badge=badges.get(review))

for path, html in pages.items():
    if not re.match(r'switchbot-.+-review\.html$', path): continue
    soup = parse(html)
    fields = {text(tr.find('th')):text(tr.find('td')) for tr in soup.select('table tr') if tr.find('th') and tr.find('td')}
    if not fields.get('Core purpose'): continue
    name = text(soup.h1).split(' Review')[0]
    cautions = [text(li) for li in soup.select('.cons-box li, .cons li, .review-cons li')]
    if not cautions: cautions = ['Check exact setup compatibility, any required hub and regional availability.']
    catalog[path] = dict(id=path,review=path,name=name,category=fields.get('Category','Smart home'),bestFor=fields.get('Best for','See review'),strengths=[fields['Core purpose']],cautions=cautions,badge=None)

for path, html in pages.items():
    if '/' in path or not path.endswith('-review.html') or path in catalog: continue
    soup = parse(html)
    strengths = [text(li) for li in soup.select('.pros-box li')]
    cautions = [text(li) for li in soup.select('.cons-box li')]
    if not soup.h1 or not strengths or not cautions: continue
    lead = soup.select_one('.review-lead, .lead')
    catalog[path] = dict(id=path, review=path, name=text(soup.h1), category='Review / buying guide', bestFor=text(lead) or 'See the full guide for the intended use.', strengths=strengths, cautions=cautions, badge=None)

# Reuse the existing comparison rows rather than inventing specifications or prices.
for path in ['best-smart-cameras-2026.html','best-smart-lighting-2026.html','best-smart-locks-2026.html']:
    soup = parse(pages[path])
    for row in soup.select('.gear-table tbody tr'):
        cells = row.find_all(['th','td'],recursive=False)
        a = next((a for a in row.select('a[href]') if 'review' in text(a).lower()),None)
        if len(cells)<3 or not a: continue
        review = key(a['href'],path)
        match = next((p for p in catalog.values() if p['name'].lower() == text(cells[0]).lower()),None)
        if match:
            if review != match['review']: match.setdefault('aliases',[]).append(review)
        elif review not in catalog:
            catalog[review] = dict(id=review,review=review,name=text(cells[0]),category={'best-smart-cameras-2026.html':'Cameras','best-smart-lighting-2026.html':'Lighting','best-smart-locks-2026.html':'Locks'}[path],bestFor=text(cells[1]),strengths=[text(cells[1])],cautions=[text(cells[2])],badge=None)

aliases = {a:p for p in catalog.values() for a in [p['review']]+p.get('aliases',[])}

def meaningful_hash(soup):
    clean = parse(str(soup.find('main') or soup.body or soup))
    for el in clean.select('script, style, header, footer, nav, .reader-trust, .reader-freshness, .reader-badge, .reader-select, [data-reader-generated]'):
        el.decompose()
    return hashlib.sha256(text(clean).encode()).hexdigest()

def badge_markup(b):
    a = parse('<a class="reader-badge" data-reader-generated="badge"></a>').a
    a['class'].append(b['kind']); a['href'] = BASE+'editorial-standards.html#badges'
    a['title'] = b['reason']; a.string = b['label']
    a['data-reader-expires'] = b['reviewDue']
    return a

for path, original in pages.items():
    soup = parse(original)
    if not soup.body or not soup.h1 or soup.find('meta',attrs={'http-equiv':re.compile('refresh',re.I)}): continue
    # Repeatable: remove only our own generated additions.
    for el in soup.select('[data-reader-generated], link[href$="reader-features.css"], script[src$="reader-features.js"]'): el.decompose()
    prefix = '../' * path.count('/')
    h = meaningful_hash(soup)
    old = previous.get(path)
    if old and old['contentHash'] == h:
        record = old
    elif old:
        record = {'date':TODAY,'label':'Content updated','contentHash':h}
    else:
        # Honor a visible editorial date before falling back to the last source edit.
        bodytext = text(soup.find('main') or soup.body)
        m = re.search(r'(?:Updated|Last updated|Last reviewed|Research updated)\s*:?\s*(\d{1,2}\s+[A-Za-z]+\s+20\d{2}|[A-Za-z]+\s+\d{1,2},?\s+20\d{2}|20\d{2}-\d{2}-\d{2})',bodytext,re.I)
        recorded = None
        if m:
            for fmt in ['%d %B %Y','%B %d, %Y','%B %d %Y','%Y-%m-%d']:
                try: recorded = datetime.strptime(m[1],fmt).date().isoformat(); break
                except ValueError: pass
        if recorded:
            record = {'date':recorded,'label':'Content updated','contentHash':h}
        else:
            edited = subprocess.check_output([GIT,'log','-1','--format=%cs','--',path],cwd=ROOT,text=True).strip() or TODAY
            record = {'date':edited,'label':'Page last edited','contentHash':h}
    records[path]=record
    # Static, crawlable markup; UI changes alone never reset a content date.
    trust = parse(f'<aside class="reader-trust" data-reader-generated="trust" aria-label="Our editorial commitments"><span><span aria-hidden="true">✓</span>Research-based guidance</span><span><span aria-hidden="true">✓</span>Strengths &amp; limitations</span><a href="{prefix}editorial-standards.html#disclosure">Affiliate disclosure</a><a href="{prefix}editorial-standards.html">How we choose</a></aside>').aside
    header = soup.body.find('header',recursive=False)
    if header: header.insert_after(trust)
    else: soup.body.insert(0,trust)
    date_text = datetime.strptime(record['date'],'%Y-%m-%d').strftime('%d %B %Y').lstrip('0')
    freshness = parse(f'<p class="reader-freshness" data-reader-generated="freshness">{record["label"]}: <time datetime="{record["date"]}">{date_text}</time> · <a href="{prefix}editorial-standards.html#dates">About these dates</a></p>').p
    soup.h1.insert_after(freshness)
    for card in soup.select('article.card, article.product-card, .gear-card, .gear-table tbody tr'):
        product = next((aliases[key(a['href'],path)] for a in card.select('a[href]') if key(a['href'],path) in aliases),None)
        if not product or not product.get('badge'): continue
        target = card.find('th') if card.name=='tr' else (card.find('summary') if card.name=='details' else card)
        target.append(badge_markup(product['badge']))
    if path in badges:
        freshness.insert_after(badge_markup(badges[path]))
    link = soup.new_tag('link',rel='stylesheet',href=prefix+'reader-features.css'); soup.head.append(link)
    script = soup.new_tag('script',src=prefix+'reader-features.js',defer=True); soup.head.append(script)
    (ROOT/path).write_text(str(soup),encoding='utf-8',newline='\n')

(ROOT/'reader-catalog.json').write_text(json.dumps(list(catalog.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
MANIFEST.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Updated {len(records)} pages; comparison catalog: {len(catalog)} products; badge types: 2.')
