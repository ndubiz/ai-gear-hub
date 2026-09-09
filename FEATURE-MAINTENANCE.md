# Product feature maintenance
## Shopping clarity (Guides 14–17)

Run `python scripts/refresh_shopping_features.py` and then `python scripts/refresh_reader_features.py` before publishing. The first builds the How We Pick page, disclosure strips, consistent rating states, manual price-history widgets and up to five relevant spec explanations per page. Both AI Gear Hub and Market Tech link to the shared methodology. Icons fall back to glossary links without JavaScript. Generated shopping UI is excluded from article freshness hashes.

`shopping-evidence.json` deliberately begins with empty `ratings` and `priceHistory` maps. Do not insert example scores or claim unobserved discounts. Missing evidence displays `Not yet scored` / `Price history unavailable`. No live feed, automatic monitoring or email alerts are implied.

Rating keys use the review path in `reader-catalog.json`. A record requires `reviewer`, `reviewed` and `reviewDue` ISO dates, HTTPS `sources`, and `criteria`: usefulness, compatibility, usability, limitations and value, each containing a 1–10 `score` and a nonempty `reason`. Scores are equally weighted. Publish evidence with the assessment, distinguish research from hands-on work, and never add an AggregateRating on the basis of an editorial score.

Price history keys use the same review paths. Each observation contains `date` (ISO date), `amount` (positive number), `currency` (three-letter code), `retailer`, exact `variant`, and HTTPS `source`. A series must use a single currency, retailer and variant. Records show their dates and sources; percentage changes compare recorded observations only, not continuous lows. The current implementation intentionally never makes a 90-day-low claim.

The feature data uses existing tracked retailer links. Preserve each partner tag and region; do not replace them with example tags.

Add real product photos only when sourced and permitted. Category icons are intentionally labeled illustrations.

Prices and numerical ratings are withheld until verified and visibly published with provenance. Never copy off-site aggregate reviews into your own AggregateRating markup. Product + Article JSON-LD identifies current pages. Existing editorial pros and cons are also marked up as Review where available. The five priority Market Tech reviews passed the live Google Rich Results Test on 8 September 2026. Other pages are not automatically eligible: they need supported Offer or qualifying review evidence. Do not invent that evidence to silence a validator.

New individual product pages need accurate Product/Article structured data; comparison pages use ItemList. Keep schema consistent with visible content. Validate JSON and use Google's Rich Results Test after publication.

Check every product-finder category/need/spending combination, back/restart navigation, mobile layout and keyboard operation after editing gear-features.js or its embedded catalog. The budget answer is a spending preference, not a guarantee about a live price. Recommendations must stay within the chosen purpose; missing matches must never fall back to unrelated products.

Update sitemap.xml when adding pages. Preserve analytics consent and existing affiliate-tracker.js / analytics.js.

## Reader features (Guides 10–13)

Run `python scripts/refresh_reader_features.py` after editing page content and before publishing. Requires Python with `beautifulsoup4` and Git on PATH (`GIT_EXECUTABLE` can override it). This rebuilds the comparison catalog from existing product data/review text and generates the shared trust strip, selective badges and visible dates. Do not hand-edit generated `reader-catalog.json` or reset `reader-freshness.json`.

The freshness manifest records a hash of main-page text, excluding shared navigation and generated features. Unchanged content keeps its date. New content changes advance `Content updated`; initial records prefer an explicit existing editorial date, otherwise use Git's last edit date labeled `Page last edited`. Do not call either date a price check. Only add a separate price-check date when evidence and a verified price exist.

Badge assignments, rationale, primary sources and review deadlines live in `scripts/refresh_reader_features.py`. Reassess by 9 November 2026. Only two current use-case assignments are approved: the Hue starter kit and C920 webcam. No Best Value or Best Overall claim is supported. The shared client removes expired badges and suppresses them in the comparison table; also regenerate/review the static pages when an assignment expires.

Quick compare uses browser-local storage only, caps selections at four and works on a page even when storage is blocked. Validate single-item disabled state, four-item limit, removal/clear, cross-page restore, invalid storage, keyboard dialog close and small-screen horizontal table scrolling after changes. Keep the tray above the analytics choice panel. Existing product-finder code and analytics must remain separate.
