# Guide 18: social landing page pilot

Published path: `switchbot-lock-deal.html`. This is a single-product SwitchBot Lock Ultra campaign destination, intentionally absent from main navigation and the sitemap, with noindex/follow metadata. Both feature generators preserve pages marked `data-campaign-landing` so future catalogue updates cannot add comparison trays, unrelated products or general navigation to the campaign.

The three offer buttons retain the existing `sca_ref=12132756.ItVThAjDrd` affiliate referral. They use `utm_campaign=switchbot-lock-ultra` and placement-specific `utm_content` values: hero, benefits, final. The landing script accepts known source/medium values and never forwards arbitrary incoming parameters to the retailer. Without JavaScript, the referral and default campaign tags still work.

Use inbound UTM tags on the landing URL for GA4 acquisition attribution. Outbound tags alone cannot attribute inbound traffic, and neither an outbound click nor a GA4 event proves a completed sale. Confirm purchases/commission in the affiliate platform.

After analytics consent, the existing `affiliate_click` event includes `cta_position`, `campaign_source`, `campaign_medium` and `campaign_name` for this page. No separate duplicate click handler is added. Register these event parameters as event-scoped custom dimensions in GA4 if they are needed in reports. Metricool reporting depends on the user's connected analytics configuration; this change does not create a Metricool integration.

After the first full week of campaign traffic, review the landing page's GA4 users, sessions and affiliate_click users by session source/medium. User click-through rate = users with an affiliate_click on this landing page divided by users who viewed this landing page, using the same reporting period. Account for analytics consent and low sample sizes. Compare CTA placements using click events; do not label repeated clicks as unique visitors or purchases. Review before launching another landing page.

Product image: SwitchBot's official listing CDN. Product claims checked against https://www.switch-bot.com/products/switchbot-lock-ultra on 2026-09-09. The existing partner coupon is displayed as unverified with checkout eligibility caveats; no discount, commission rate, customer testimonial, score or editorial award is invented.
