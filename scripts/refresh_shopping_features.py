"""Build Guides 14-17. Run before refresh_reader_features.py; no invented evidence."""
from pathlib import Path
from datetime import date
import json
import re
from html import escape
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ndubiz.github.io/ai-gear-hub/'
TODAY = date.today()
evidence = json.loads((ROOT / 'shopping-evidence.json').read_text())
catalog = json.loads((ROOT / 'reader-catalog.json').read_text())
aliases = {a: p['id'] for p in catalog for a in [p['review']] + p.get('aliases', [])}
TERMS = {
 'Matter': 'A shared smart-home standard; check that your device and controller support the features you need.',
 'Thread': 'A low-power network for smart-home devices that usually needs a compatible border router.',
 'Zigbee': 'A low-power wireless system that connects compatible smart devices through a hub.',
 'Wi-Fi': 'The wireless network linking a device to your router; check which frequency bands the device supports.',
 'Bluetooth': 'A short-range wireless connection between nearby compatible devices.',
 '1080p': 'A video resolution of 1920 by 1080 pixels; image quality also depends on the lens, lighting and processing.',
 '4K': 'A high-resolution video format, commonly 3840 by 2160 pixels; useful detail also depends on the camera and lighting.',
 'HDR': 'High dynamic range helps retain detail in bright and dark areas when the camera and display support it.',
 'IP rating': 'A protection code for dust and water resistance; check the exact code and manufacturer limits before outdoor use.',
 'IP54': 'Protection against limited dust entry and splashing water, not immersion.',
 'microSD': 'A small removable memory card used for local storage; check supported capacity and recording requirements.',
 'local storage': 'Recordings saved on a device or memory card rather than only on an online service.',
 'cloud storage': 'Recordings saved online by a service, which may require a subscription and internet access.',
 'two-way audio': 'A microphone and speaker let you listen and talk through the device.',
 'USB-C': 'A connector shape; charging power, data speed and video support vary by cable and device.',
 'USB-A': 'The larger rectangular USB connector commonly found on computers and chargers.',
 'GaN': 'Gallium nitride is a semiconductor that can help chargers deliver power in a compact design.',
 'ANC': 'Active noise cancellation uses microphones and processing to reduce some background sounds.',
 'HEPA': 'A high-efficiency particle filter; check the stated standard, fit and replacement cost.',
 'LiDAR': 'Laser-based distance sensing that can help a robot map rooms and navigate.',
 'lumens': 'A measure of visible light output; more lumens means more light, not necessarily better color quality.',
 'color temperature': 'The warm or cool appearance of white light, measured in kelvin.',
 'response time': 'How quickly a display pixel changes; it is different from the delay between your input and the screen response.'
}
def parse(s): return BeautifulSoup(s, 'html.parser')
def fragment(s): return parse(s).find()
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def href_key(href, path):
    u = urljoin(BASE + path, href)
    return u[len(BASE):].split('#')[0] if u.startswith(BASE) else ''
def paid(a):
    h = a.get('href', '')
    return 'sponsored' in a.get('rel', []) or a.has_attr('data-affiliate') or bool(re.search(r'https?://(?:www\.)?(?:amazon\.|amzn\.to)', h))

def score(product, prefix):
    record = evidence['ratings'].get(product)
    if record:
        # A numerical editorial score requires dated supporting reasoning in all five dimensions.
        values = record['criteria']
        assert set(values) == {'usefulness','compatibility','usability','limitations','value'}
        assert all(type(v['score']) in (int,float) and 1 <= v['score'] <= 10 and v['reason'].strip() for v in values.values())
        assert record['reviewer'].strip() and record['sources'] and all(urlparse(u).scheme == 'https' for u in record['sources'])
        assert date.fromisoformat(record['reviewed']) <= TODAY
        assert date.fromisoformat(record['reviewDue']) >= TODAY
        number = sum(v['score'] for v in values.values()) / 5
        content = f'<strong>{number:.1f}/10</strong> Editorial score'
        content += f'<details><summary>Score evidence</summary><p>Research assessment by {escape(record["reviewer"])}. Reviewed {escape(record["reviewed"])}.</p><ul>'
        for criterion, v in values.items():
            content += f'<li>{escape(criterion.capitalize())}: {v["score"]}/10 — {escape(v["reason"])}</li>'
        content += '</ul>' + ' '.join(f'<a href="{escape(u,quote=True)}">Source {i+1}</a>' for i,u in enumerate(record['sources'])) + '</details>'
    else:
        content = 'Not yet scored'
    return fragment(f'<div class="shopping-score" data-shopping-generated="score">{content} <a href="{prefix}how-we-test.html#ratings">Rating approach</a></div>')

def price(product, prefix):
    rows = evidence['priceHistory'].get(product, [])
    if rows:
        assert all(type(r['amount']) in (int,float) and r['amount'] > 0 and date.fromisoformat(r['date']) <= TODAY and urlparse(r['source']).scheme == 'https' and len(r['currency']) == 3 and r['variant'] and r['retailer'] for r in rows)
        rows = sorted(rows, key=lambda r: r['date'])
        assert len({(r['currency'],r['variant'],r['retailer']) for r in rows}) == 1, 'Do not mix regions, currencies, sellers or variants.'
        latest = rows[-1]
        body = f'<p>Last recorded: {latest["amount"]:.2f} {escape(latest["currency"])} on {escape(latest["date"])}. This is not a live price.</p>'
        if len(rows) >= 2 and rows[0]['date'] != latest['date']:
            change = (latest['amount'] / rows[0]['amount'] - 1) * 100
            body += f'<p>Change between first and latest recorded observations: {change:+.1f}%. Prices between observations are unknown.</p>'
        body += '<details><summary>View recorded observations</summary><div class="shopping-price-scroll"><table><thead><tr><th>Date</th><th>Recorded price</th><th>Source</th></tr></thead><tbody>'
        for r in rows:
            body += f'<tr><td>{escape(r["date"])}</td><td>{r["amount"]:.2f} {escape(r["currency"])}</td><td><a href="{escape(r["source"],quote=True)}" rel="nofollow noopener">{escape(r["retailer"])}: {escape(r["variant"])}</a></td></tr>'
        body += '</tbody></table></div></details>'
    else:
        body = '<p>Price history unavailable</p><details><summary>What this means for your purchase</summary><p>We do not yet have verified, dated price observations for this product. Check the retailer for the current price, seller, delivery costs and exact model. No price-drop or 90-day-low claim is available.</p></details>'
    return fragment(f'<aside class="shopping-price" data-shopping-generated="price" aria-label="Price history"><strong>Price Trend</strong>{body}<a href="{prefix}how-we-test.html#prices">How we record prices</a></aside>')

# New page reflects the site's established research-only status.
glossary = ''.join(f'<dt id="term-{slug(t)}"><strong>{escape(t)}</strong></dt><dd>{escape(d)}</dd>' for t,d in TERMS.items())
method = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>How We Pick Products | AI Gear Hub &amp; Market Tech</title><meta name="description" content="How AI Gear Hub and Ndubiz Market Tech select products, explain specifications, disclose affiliate links and handle ratings and price history."><link rel="canonical" href="{BASE}how-we-test.html"><link rel="stylesheet" href="styles.css"><script src="analytics.js" defer></script></head><body><header class="site-header"><div class="container nav-wrap"><a class="brand" href="index.html">AI Gear Hub</a><a href="amazon-products.html">Browse products</a><a href="marketplace/index.html">Market Tech</a></div></header><main class="shopping-method"><p>AI Gear Hub · Ndubiz Market Tech</p><h1>How we pick products</h1><p>We want to help you find gear that fits your needs, with clear reasons to consider it and clear reasons to look elsewhere. Our current guides are research-based. We do not claim hands-on or laboratory testing unless a review describes the actual testing performed.</p><nav aria-label="On this page"><a href="#selection">Our process</a><a href="#ratings">Ratings</a><a href="#prices">Price history</a><a href="#disclosure">Disclosure</a><a href="#glossary">Spec glossary</a></nav><h2>What we look for</h2><p>Start with the job a product needs to do. Compare useful features, compatibility, setup requirements and limitations. The total cost can include a hub, accessories or a subscription, so the sticker price alone is not enough.</p><h2 id="selection">How we choose products</h2><p>Our buying guides describe intended uses, strengths and cautions using product information and linked sources where provided. Manufacturer claims are not independent test results. Customer reviews can highlight questions to investigate, but a customer star average is not our own score.</p><p>Before buying, check the exact model and regional version against the manufacturer's documentation and current retailer listing. Where evidence is missing, our pages should say so. Selection does not mean we compared every alternative on the market.</p><h2 id="ratings">One consistent rating approach</h2><p>Numerical editorial ratings use a 1–10 scale. A published score requires documented evidence and a reason for each of five equally weighted areas: usefulness for the intended task, compatibility, usability, limitations and overall cost/value. The overall score is their average, rounded to one decimal place.</p><p><strong>Not yet scored</strong> means that assessment has not been documented. It is not a zero, a negative review or a customer rating. We currently withhold numerical scores where the required evidence is absent. A score must identify its reviewer, sources and review date before publication; research-based scores must never imply hands-on testing.</p><p>Our selective <a href="editorial-standards.html#badges">Editor's Pick and Beginner badges</a> describe a particular use case and are separate from numerical ratings.</p><h2 id="prices">How we record prices</h2><p>The Price Trend box is a manual record, not a live price feed or an alert service. Each observation must identify the date, price, currency, retailer, exact product variant and source. We compare observations only within the same currency, retailer and variant.</p><p>With no verified records, we show <strong>Price history unavailable</strong>. With one record, we show only that observation. With multiple dated records, we can show the change between those observations. That does not establish the lowest price over the days between them. We do not claim a 90-day low without evidence covering that period.</p><p>Prices and stock can change after a check. Confirm the final price, shipping, coupons and seller at the retailer before you order. A page's content-update date is not a price-check date.</p><h2 id="disclosure">Our affiliate disclosure</h2><p>As an Amazon Associate we earn from qualifying purchases. AI Gear Hub and Ndubiz Market Tech may also earn commissions from other affiliate links, at no extra cost to you. An affiliate relationship does not prove product quality. Check the strengths, limitations and suitability before following a shopping link.</p><h2 id="glossary">Specifications in plain English</h2><p>Use the question-mark icons beside selected terms for a quick explanation. You can also read the definitions here.</p><dl>{glossary}</dl><p><a href="editorial-standards.html">Read our editorial standards and date policy</a> · <a href="contact.html">Contact us about a correction</a></p></main><footer><a href="about.html">About us</a> · <a href="privacy.html">Privacy</a></footer></body></html>'''
# The existing About page may use another filename; use the real home About section if needed.
if not (ROOT/'about.html').exists(): method = method.replace('<a href="about.html">About us</a>','<a href="contact.html">Contact</a>')
(ROOT/'how-we-test.html').write_text(method, encoding='utf8', newline='\n')

counts = {'pages':0, 'ratings':0, 'prices':0, 'tooltips':0}
for path in sorted(ROOT.rglob('*.html')):
    if '.git' in path.parts: continue
    rel = path.relative_to(ROOT).as_posix(); prefix = '../' * rel.count('/')
    soup = parse(path.read_text(encoding='utf8'))
    if not soup.head or not soup.body or not soup.h1 or soup.find('meta',attrs={'http-equiv':re.compile('refresh',re.I)}): continue
    for x in soup.select('[data-shopping-generated], link[href$="shopping-features.css"], script[src$="shopping-features.js"]'): x.decompose()
    paid_links = [a for a in soup.select('a[href]') if paid(a)]
    if paid_links:
        banner = fragment(f'<aside class="shopping-disclosure" data-shopping-generated="disclosure">This page contains affiliate links. We may earn a commission at no extra cost to you. <a href="{prefix}how-we-test.html#disclosure">See how we pick products</a>.</aside>')
        trust = soup.select_one('.reader-trust')
        if trust: trust.insert_after(banner)
        elif soup.body.find('header',recursive=False): soup.body.find('header',recursive=False).insert_after(banner)
        else: soup.body.insert(0,banner)
    review = rel in aliases or (rel.endswith('-review.html') and bool(paid_links))
    if review:
        soup.h1.insert_after(score(aliases.get(rel,rel),prefix)); counts['ratings'] += 1
        if paid_links:
            target = paid_links[0].find_parent(class_=re.compile(r'^(actions|cta-row|cta-group|buttons)$')) or paid_links[0].parent
            # Keep the price box adjacent to the shopping action, outside paragraphs.
            if target.name in ('body','main'): paid_links[0].insert_after(price(aliases.get(rel,rel),prefix))
            else: target.insert_after(price(aliases.get(rel,rel),prefix))
            counts['prices'] += 1
    else:
        for card in soup.select('article, div.card, .product-card, .gear-card'):
            if card.find_parent(['article']) or card.select_one('.shopping-score'): continue
            links = card.select('a[href]')
            k = next((aliases[href_key(a['href'],rel)] for a in links if href_key(a['href'],rel) in aliases),None)
            if not k and not any(paid(a) for a in links): continue
            heading = card.find(['h2','h3'])
            if not heading: continue
            heading.insert_before(score(k or rel+'#'+slug(heading.get_text()),prefix)); counts['ratings'] += 1
            if rel == 'amazon-ai-picks.html' and any(paid(a) for a in links):
                card.append(price(k or rel+'#'+slug(heading.get_text()),prefix)); counts['prices'] += 1
    if rel != 'how-we-test.html' and (review or paid_links):
        used = set()
        # Explain up to five distinct terms per page; never alter links, navigation or headings.
        for node in list(soup.select('main li, main td, main p, .feat li, .pros-box li, .cons-box li')):
            if node.find_parent(['header','footer','nav']) or node.find_parent(attrs={'data-shopping-generated':True}): continue
            for textnode in list(node.find_all(string=True)):
                if textnode.find_parent(['a','script','style','button']) or textnode.find_parent(attrs={'data-shopping-generated':True}): continue
                original = str(textnode); matches=[]
                for term in TERMS:
                    if term in used or len(used)>=5: continue
                    match = re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',original,re.I)
                    if match: matches.append((match.start(), match.end(), term)); used.add(term)
                if not matches: continue
                cursor=0
                for start,end,term in sorted(matches):
                    textnode.insert_before(original[cursor:end])
                    textnode.insert_before(fragment(f'<span class="shopping-info" data-shopping-generated="tooltip" data-explanation="{escape(TERMS[term],quote=True)}"><a href="{prefix}how-we-test.html#term-{slug(term)}" aria-label="Explain {escape(term,quote=True)}">?</a></span>'))
                    cursor=end; counts['tooltips'] += 1
                textnode.insert_before(original[cursor:]); textnode.extract()
    footer = soup.select_one('footer, .footer-nav')
    link = fragment(f'<span class="shopping-footer" data-shopping-generated="footer"><a href="{prefix}how-we-test.html">How we pick products</a></span>')
    if footer: footer.append(link)
    else: soup.body.append(link)
    soup.head.append(soup.new_tag('link',rel='stylesheet',href=prefix+'shopping-features.css'))
    soup.head.append(soup.new_tag('script',src=prefix+'shopping-features.js',defer=''))
    path.write_text(str(soup),encoding='utf8',newline='\n'); counts['pages'] += 1
print(counts)
