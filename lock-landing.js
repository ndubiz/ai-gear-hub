(() => {
  'use strict';
  const incoming = new URLSearchParams(location.search);
  const sources = ['facebook','instagram','youtube','tiktok','email','newsletter'];
  const media = ['social','video','email','cpc','referral'];
  const source = sources.includes(incoming.get('utm_source')) ? incoming.get('utm_source') : 'ai-gear-hub';
  const medium = media.includes(incoming.get('utm_medium')) ? incoming.get('utm_medium') : 'referral';
  document.querySelectorAll('a[data-cta-position]').forEach(link => {
    const url = new URL(link.href);
    url.searchParams.set('utm_source',source);
    url.searchParams.set('utm_medium',medium);
    url.searchParams.set('utm_campaign','switchbot-lock-ultra');
    url.searchParams.set('utm_content',link.dataset.ctaPosition);
    link.href = url.href;
    link.dataset.campaignSource = source;
    link.dataset.campaignMedium = medium;
    link.dataset.campaignName = 'switchbot-lock-ultra';
  });
})();
