from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
REF = "12132756.ItVThAjDrd"
COUPON = "10UPLTVTHAJDRA"

PRODUCTS = [
    ("Smart Hubs", "SwitchBot Hub 2", "switchbot-hub-2", "Best seller and the ecosystem anchor", "A practical control center for connecting compatible SwitchBot devices and automations.", "Established hub for everyday smart-home routines", "Users building a connected SwitchBot setup"),
    ("Smart Hubs", "SwitchBot Hub 3", "switchbot-hub-3", "Newer Matter-ready hub with IR and integrated sensing", "A newer hub designed to bring device control, infrared appliances and environmental awareness together.", "Matter-focused hub with broader control options", "Homes that want a current, expandable hub"),
    ("Smart Hubs", "SwitchBot AI Hub", "switchbot-ai-hub", "Local AI automation and a strong AI Gear Hub fit", "A hub aimed at more responsive, locally informed smart-home automations.", "AI-focused automation hub", "Early adopters who want advanced automation"),
    ("Smart Hubs", "SwitchBot Hub Mini", "switchbot-hub-mini", "Budget entry hub", "A compact entry point for controlling compatible SwitchBot devices and infrared appliances.", "Compact, lower-cost hub", "First-time SwitchBot buyers"),
    ("Smart Hubs", "SwitchBot Hub Mini Matter Enabled", "switchbot-hub-mini-matter-enabled", "Budget hub with Matter", "A compact SwitchBot hub for buyers who want Matter support without stepping up to a larger hub.", "Compact Matter-enabled hub", "Budget-conscious Matter users"),
    ("Curtains & Blinds", "SwitchBot Curtain 3", "switchbot-curtain-3", "Overall brand best seller", "A retrofit motor that automates compatible curtains without replacing the curtain rail.", "Retrofit smart-curtain motor", "Renters and homeowners automating existing curtains"),
    ("Curtains & Blinds", "SwitchBot Curtain 3 Rod Type 1", "switchbot-curtain-3-rod-type-1", "Rod-compatible Curtain 3 variant", "A Curtain 3 configuration made for compatible rod-style curtain setups.", "Rod-style curtain automation", "Homes with compatible curtain rods"),
    ("Curtains & Blinds", "SwitchBot Roller Shade", "switchbot-roller-shade", "Best seller that does not require an existing curtain", "A smart roller-shade solution for automated light and privacy control.", "Automated roller shade", "Rooms needing a complete smart shade"),
    ("Curtains & Blinds", "SwitchBot Blind Tilt", "switchbot-blind-tilt", "Designed for blinds rather than curtains", "A retrofit device that adjusts compatible horizontal blinds for scheduled or remote light control.", "Retrofit blind-angle control", "Homes with compatible horizontal blinds"),
    ("Curtains & Blinds", "SwitchBot Curtain 2", "switchbot-curtain", "Older, lower-cost curtain option", "A value-oriented retrofit motor for automating compatible curtains.", "Budget smart-curtain motor", "Buyers comparing price with newer Curtain models"),
    ("Smart Locks", "SwitchBot Lock Ultra", "switchbot-lock-ultra", "New flagship lock", "A flagship retrofit smart-lock option for convenient entry and SwitchBot ecosystem integration.", "Flagship retrofit smart lock", "Homes wanting SwitchBot's newest lock platform"),
    ("Smart Locks", "SwitchBot Lock Vision", "switchbot-lock-vision", "New lock with facial recognition", "A smart-entry system that adds face-based access to the SwitchBot lock lineup.", "Facial-recognition smart entry", "Households prioritizing hands-free access"),
    ("Smart Locks", "SwitchBot Lock Vision Pro", "switchbot-lock-vision-pro", "Higher-spec facial-recognition model", "A higher-spec smart-entry package centered on face-based access.", "Premium facial-recognition entry", "Buyers seeking the top Vision configuration"),
    ("Smart Locks", "SwitchBot Lock Pro", "switchbot-lock-pro", "Previous best seller and a strong value pick", "A retrofit smart lock balancing broad everyday features with value.", "Value-focused retrofit smart lock", "Most households comparing smart-lock options"),
    ("AI / Smart Displays", "SwitchBot AI Art Frame", "switchbot-ai-art-frame", "The most AI-focused product in the lineup", "A connected display that brings changing digital and AI-assisted artwork into a room.", "AI-oriented digital art display", "Design-conscious AI and smart-home enthusiasts"),
    ("AI / Smart Displays", "SwitchBot E-Ink Home Dashboard", "switchbot-weather-station", "AI daily insights, weather and calendar", "An e-ink information display for at-a-glance home, weather and schedule updates.", "Low-power home information dashboard", "People who want calm, glanceable information"),
    ("Robot Vacuums", "SwitchBot K11+", "switchbot-robot-vacuum-k11", "Best seller and especially compact", "A compact robot-vacuum system designed for automated cleaning with a small footprint.", "Compact robot vacuum", "Apartments and space-conscious homes"),
    ("Robot Vacuums", "SwitchBot S20", "switchbot-floor-cleaning-robot-s20", "New mopping model with auto-fill and drain", "A floor-cleaning robot focused on reducing hands-on mopping maintenance.", "Automated vacuuming and mopping", "Homes prioritizing low-maintenance floor care"),
    ("Robot Vacuums", "SwitchBot K10+ Pro", "switchbot-mini-robot-vacuum-k10-pro", "Compact and pet-friendly", "A compact robot vacuum designed to navigate smaller spaces and everyday pet mess.", "Compact automated cleaning", "Apartments and pet-owning households"),
    ("Robot Vacuums", "SwitchBot K20+ Pro", "switchbot-multitasking-household-robot-k20-pro", "Top-tier multitasking household robot", "An ambitious household robot platform built for more than routine floor cleaning.", "Multitasking household robotics", "Early adopters seeking an advanced home robot"),
    ("Cameras & Doorbells", "SwitchBot Smart Video Doorbell", "switchbot-video-doorbell", "Connected front-door monitoring", "A video doorbell for viewing and responding to visitors as part of a connected-home setup.", "Smart video doorbell", "Households upgrading front-door awareness"),
    ("Cameras & Doorbells", "SwitchBot Outdoor Spotlight Cam 2K", "switchbot-outdoor-spotlight-cam", "Outdoor camera with spotlight", "An outdoor security camera combining video monitoring with a built-in spotlight.", "Outdoor video monitoring", "Entrances, gardens and outdoor areas"),
    ("Cameras & Doorbells", "SwitchBot Pan/Tilt Cam Plus 3K", "switchbot-pan-tilt-cam-plus-3k", "Indoor pan-and-tilt camera", "An indoor camera with motorized viewing and high-resolution monitoring.", "Indoor pan-and-tilt monitoring", "Rooms where a wider adjustable view matters"),
    ("Sensors & Meters", "SwitchBot Meter Pro CO2 Monitor", "switchbot-meter-pro-co2-monitor", "Best seller in the sensor category", "A home environment monitor that helps track carbon dioxide and indoor conditions.", "Indoor air and CO2 monitoring", "Offices, bedrooms and shared indoor spaces"),
    ("Sensors & Meters", "SwitchBot Presence Sensor", "switchbot-presence-sensor", "New mmWave presence sensing", "A presence sensor designed to detect occupancy more precisely than basic motion triggers.", "mmWave room-presence detection", "Automations that need reliable occupancy awareness"),
    ("Sensors & Meters", "SwitchBot Water Leak Detector", "switchbot-water-leak-detector", "Early warning for water leaks", "A compact sensor for detecting water where a leak could cause damage.", "Water-leak alerts", "Kitchens, bathrooms, basements and utility areas"),
    ("Sensors & Meters", "SwitchBot Contact Sensor", "contact-sensor", "Door and window sensing", "A simple sensor for tracking whether a compatible door or window is open or closed.", "Door/window status sensing", "Entry alerts and occupancy automations"),
    ("Sensors & Meters", "SwitchBot Indoor/Outdoor Thermo-Hygrometer", "switchbot-indoor-outdoor-thermo-hygrometer", "Lowest-cost entry sensor", "A compact sensor for tracking temperature and humidity indoors or outdoors.", "Temperature and humidity monitoring", "Budget-friendly environmental tracking"),
    ("Home Appliances", "SwitchBot Air Purifier Table", "switchbot-air-purifier-table", "Best-selling multifunction appliance", "An air purifier designed to double as a useful piece of home furniture.", "Air purification with table-style design", "Living spaces where footprint and function both matter"),
    ("Home Appliances", "SwitchBot Battery Circulator Fan 2 Pro", "switchbot-battery-circulator-fan-2-pro", "New cordless circulation fan", "A battery-powered fan for flexible air circulation and connected control.", "Portable smart air circulation", "Rooms needing flexible, cordless airflow"),
    ("Home Appliances", "SwitchBot Evaporative Humidifier", "switchbot-evaporative-humidifier-auto-refill", "Auto-refill capable", "An evaporative humidifier designed to reduce the routine work of maintaining indoor humidity.", "Connected evaporative humidification", "Dry rooms and low-maintenance routines"),
    ("Lighting", "SwitchBot Candle Warmer Lamp", "switchbot-candle-warmer-lamp", "Best seller with an unusual smart-lighting angle", "A lamp that warms compatible candles while adding ambient light and smart control.", "Smart candle warming and ambient light", "Candle lovers seeking flame-free fragrance"),
    ("Lighting", "SwitchBot RGBICWW Floor Lamp", "switchbot-rgbicww-floor-lamp", "Color and tunable-white floor lighting", "A connected floor lamp for colorful scenes, ambient effects and adjustable white light.", "Smart RGB and white floor lamp", "Gaming, entertainment and ambient room lighting"),
    ("Power & Access", "SwitchBot Garage Door Opener", "switchbot-garage-door-opener", "Best-selling access product", "A connected controller for adding remote status and operation to compatible garage doors.", "Smart garage-door control", "Drivers upgrading a compatible garage door"),
    ("Power & Access", "SwitchBot Universal Remote", "switchbot-universal-remote", "Best seller for controlling multiple devices", "A handheld controller intended to bring multiple compatible devices into one control surface.", "Multi-device smart remote", "Living rooms with several remotes and devices"),
    ("Power & Access", "SwitchBot Plug Mini", "switchbot-plug-mini", "Affordable product with broad appeal", "A compact smart plug for schedules, remote switching and simple power automations.", "Compact smart power control", "Lamps and small appliances"),
    ("Power & Access", "SwitchBot Bot", "switchbot-bot", "The original SwitchBot product", "A small retrofit device that physically presses compatible buttons and switches.", "Physical button-pushing automation", "Making a simple existing appliance smart"),
    ("Trackers", "SwitchBot Safety Alarm", "switchbot-safety-alarm", "130 dB personal alarm", "A portable personal-safety alarm designed to draw attention in an emergency.", "Portable personal alarm", "Commuters, travelers and students"),
    ("Trackers", "SwitchBot Wallet Finder Card", "switchbot-wallet-finder-card", "Slim Find My-style tracker", "A card-shaped tracker designed to fit inside a wallet.", "Wallet-friendly item tracking", "People who frequently misplace a wallet"),
]

PAGE_STYLE = """
body{font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,Arial,sans-serif;line-height:1.7;color:#1f2430;background:#fafafa;margin:0}.wrap{max-width:760px;margin:0 auto;padding:60px 24px 100px}a{color:#2f6fed;text-decoration:none}a:hover{text-decoration:underline}h1{font-size:2rem;margin-bottom:.2em}h2{font-size:1.3rem;margin-top:2em}.subtitle{color:#667089;font-size:1.05rem;margin-bottom:1.5em}.backlink{display:inline-block;margin-bottom:32px;font-size:.95rem}.disclosure{background:#f1f4fb;border-left:3px solid #2f6fed;padding:12px 16px;font-size:.9rem;color:#475467;margin:24px 0 2em;border-radius:4px}.product-hero{background:linear-gradient(135deg,#eef4ff,#f7f0ff);border:1px solid #dfe7f5;border-radius:16px;padding:34px;text-align:center;font-size:4rem;margin:1.5em 0}.verdict{background:#fff;border:1px solid #e4e7ec;border-radius:10px;padding:20px 24px;margin:2em 0}.verdict h2{margin-top:0}.coupon{background:#ecfdf3;border:1px dashed #12b76a;border-radius:8px;padding:10px 14px;margin:16px 0;font-weight:700}.pros-cons{display:flex;gap:24px;flex-wrap:wrap;margin:1.5em 0}.pros-cons div{flex:1;min-width:240px}.pros-cons h3{font-size:1rem;margin-bottom:8px}.pros-cons ul{padding-left:20px;margin:0}.cta{display:inline-block;margin:12px 0;padding:14px 28px;background:#1f2430;color:#fff;border-radius:8px;font-weight:600}.cta:hover{background:#2f6fed;text-decoration:none}table{width:100%;border-collapse:collapse;margin:1.5em 0;font-size:.95rem}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #e4e7ec}th{color:#667085;font-weight:600}footer{text-align:center;color:#98a2b3;font-size:.85rem;padding:40px 0}@media(max-width:600px){h1{font-size:1.65rem}.wrap{padding-top:32px}.product-hero{font-size:3rem}}
"""

def product_url(handle):
    return f"https://www.switch-bot.com/products/{handle}?sca_ref={REF}"

def page(category, name, handle, note, summary, core, best_for):
    url = product_url(handle)
    title = escape(name)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} Review (2026) - AI Gear Hub</title><meta name="description" content="A practical {title} review covering what it does, who it is for, limitations, coupon code and the official product link.">
<link rel="canonical" href="https://ndubiz.github.io/ai-gear-hub/{handle}-review.html"><style>{PAGE_STYLE}</style></head><body><div class="wrap">
<a class="backlink" href="index.html#switchbot-products">← Back to SwitchBot products</a>
<h1>{title} Review: Is It Right for Your Smart Home?</h1><p class="subtitle">{escape(note)}.</p>
<div class="disclosure">Affiliate disclosure: This page contains an affiliate link. If you buy through it, AI Gear Hub may earn a commission at no extra cost to you. This does not affect our opinions.</div>
<div class="product-hero" role="img" aria-label="{title}">🏠</div>
<p>{escape(summary)} It is best evaluated as one part of a practical smart-home setup rather than as a gadget that needs to do everything.</p>
<h2>What It Does</h2><p>{escape(core)}. Confirm that your home setup, phone platform and any required SwitchBot hub are compatible before buying.</p>
<div class="pros-cons"><div><h3>What's good</h3><ul><li>Fits into the broader SwitchBot ecosystem</li><li>Designed to automate a clear everyday task</li><li>Can be expanded with compatible SwitchBot devices</li></ul></div><div><h3>What to consider</h3><ul><li>Compatibility depends on your exact home setup</li><li>Some features may require a compatible hub or app account</li><li>Specifications, bundles and availability can change</li></ul></div></div>
<h2>Who It's For</h2><p>{escape(best_for)}. It is less compelling if the same job is already handled reliably by equipment you own or if your setup is outside the listed compatibility requirements.</p>
<div class="verdict"><h2>Our Verdict</h2><p>{title} is worth considering when its specific automation matches a real need in your home. Check the current product page for compatibility, included accessories, regional availability and the latest price before ordering.</p><div class="coupon">Coupon code: {COUPON}</div><a class="cta" href="{url}" rel="nofollow sponsored" target="_blank">View {title} on SwitchBot ↗</a></div>
<h2>Quick Specs</h2><table><tr><th>Category</th><td>{escape(category)}</td></tr><tr><th>Core purpose</th><td>{escape(core)}</td></tr><tr><th>Best for</th><td>{escape(best_for)}</td></tr><tr><th>Product page</th><td><a href="{url}" rel="nofollow sponsored" target="_blank">Full SwitchBot product URL ↗</a></td></tr></table>
<p><em>Pricing, specifications and compatibility can change. Confirm current details on the official product page before buying.</em></p></div><footer>© AI Gear Hub. All rights reserved.</footer></body></html>'''

for item in PRODUCTS:
    category, name, handle, *_ = item
    (ROOT / f"{handle}-review.html").write_text(page(*item), encoding="utf-8")

cards = []
icons = {"Smart Hubs":"◎","Curtains & Blinds":"▥","Smart Locks":"🔒","AI / Smart Displays":"✦","Robot Vacuums":"🤖","Cameras & Doorbells":"📹","Sensors & Meters":"◌","Home Appliances":"⌂","Lighting":"💡","Power & Access":"⚡","Trackers":"⌖"}
for category, name, handle, note, *_ in PRODUCTS:
    cards.append(f'<article class="gear-card searchable" data-category="gear ai" data-search="switchbot {escape(category.lower())} {escape(name.lower())}"><div class="gear-visual">{icons[category]}</div><div class="gear-info"><span>SwitchBot · {escape(category)}</span><h3>{escape(name)}</h3><p>{escape(note)}.</p><a href="{handle}-review.html">View product review →</a></div></article>')

index = (ROOT / "index.html").read_text(encoding="utf-8")
start = '<!-- SWITCHBOT_PRODUCTS_START -->'
end = '<!-- SWITCHBOT_PRODUCTS_END -->'
section = start + '<section class="section" id="switchbot-products"><div class="container"><div class="section-head"><div><span class="eyebrow">33-product buyer hub</span><h2>Explore SwitchBot products</h2></div><p>Browse hubs, curtains, locks, displays, cleaning robots, cameras, sensors and more. Every review includes the current product-page link and coupon code.</p></div><div class="gear-grid">' + ''.join(cards) + '</div></div></section>' + end
if start in index:
    before, rest = index.split(start, 1)
    _, after = rest.split(end, 1)
    index = before + section + after
else:
    index = index.replace('<section class="section" id="compare">', section + '<section class="section" id="compare">')
(ROOT / "index.html").write_text(index, encoding="utf-8")

print(f"Generated {len(PRODUCTS)} SwitchBot pages and homepage cards.")
