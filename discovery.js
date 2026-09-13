(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const make = (tag, text, cls) => { const el = document.createElement(tag); if (text) el.textContent = text; if (cls) el.className = cls; return el; };
  const url = path => new URL(path, base).href;
  const current = decodeURI(location.pathname.slice(base.pathname.length)) || 'index.html';
  const savedKey = 'aigearhub-shortlist-v1', recentKey = 'aigearhub-recent-v1';
  const dialog = make('dialog', '', 'discovery-dialog');
  dialog.setAttribute('aria-labelledby', 'discovery-title');
  const head = make('div', '', 'discovery-heading'), title = make('h2'); title.id = 'discovery-title';
  const close = make('button', 'Close'); close.type = 'button'; head.append(title, close);
  const body = make('div'); dialog.append(head, body); document.body.append(dialog);
  let opener, mode, entries = [], products = [], ready = false, failed = false;
  let saved = [], recent = [], memoryOnly = false;
  const buttons = [];
  const read = key => { try { const value = JSON.parse(localStorage.getItem(key) || '[]'); return Array.isArray(value) ? [...new Set(value.filter(x => typeof x === 'string'))] : []; } catch { return []; } };
  const write = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch { memoryOnly = true; } };
  const valid = ids => ids.filter(id => entries.some(p => p.path === id));
  function sync() { buttons.forEach(({el, path}) => { const on = saved.includes(path); el.textContent = on ? 'Saved — remove' : 'Save to shortlist'; el.setAttribute('aria-pressed', String(on)); }); }
  function saveButton(path) {
    const el = make('button', '', 'discovery-save'); el.type = 'button';
    const name = entries.find(p => p.path === path)?.title || 'this page';
    el.setAttribute('aria-label', `Save or remove ${name} from shortlist`);
    buttons.push({el, path});
    el.addEventListener('click', () => { saved = saved.includes(path) ? saved.filter(x => x !== path) : [...saved, path]; write(savedKey, saved); sync(); if (dialog.open && mode === 'saved') render(); });
    sync(); return el;
  }
  function list(pages, parent) {
    const ul = make('ul', '', 'discovery-results');
    pages.forEach(p => { const li = make('li', '', 'discovery-result'), a = make('a', p.title); a.href = url(p.path); li.append(a, make('p', `${p.category} · ${p.description}`), saveButton(p.path)); ul.append(li); });
    parent.append(ul);
  }
  function render() {
    body.replaceChildren(); buttons.splice(0, buttons.length, ...buttons.filter(b => b.el.isConnected));
    title.textContent = {search:'Search everything', saved:'My shortlist', recent:'Recently viewed'}[mode];
    if (!ready) { body.append(make('p', failed ? 'Search is temporarily unavailable. Explore the product catalogue or guides using the section menu.' : 'Loading guides and products…')); return; }
    if (mode === 'search') {
      const label = make('label', 'Search products, AI tools and guides'); label.htmlFor = 'discovery-query';
      const input = make('input'); input.id = 'discovery-query'; input.type = 'search'; input.placeholder = 'Try smart lock, microphone or AI tools';
      const filterLabel = make('label', 'Category'); filterLabel.htmlFor = 'discovery-category';
      const filter = make('select'); filter.id = 'discovery-category';
      ['', ...new Set(entries.map(p => p.category).sort())].forEach(c => { const opt = make('option', c || 'All categories'); opt.value = c; filter.append(opt); });
      const status = make('p', '', 'discovery-status'); status.setAttribute('role', 'status');
      const results = make('div'); body.append(label,input,filterLabel,filter,status,results);
      function search() {
        const terms = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
        const matches = entries.filter(p => (!filter.value || p.category === filter.value) && terms.every(t => `${p.title} ${p.description} ${p.keywords} ${p.category}`.toLowerCase().includes(t)));
        matches.sort((a,b) => Number(b.title.toLowerCase().includes(input.value.toLowerCase().trim())) - Number(a.title.toLowerCase().includes(input.value.toLowerCase().trim())));
        results.replaceChildren(); buttons.splice(0, buttons.length, ...buttons.filter(b => b.el.isConnected));
        status.textContent = `${matches.length} results${matches.length > 30 ? ' · Showing the first 30; narrow your search for more.' : ''}`;
        if (!matches.length) results.append(make('p', 'No matches. Try fewer words or choose another category.'));
        list(matches.slice(0,30), results);
      }
      input.addEventListener('input',search); filter.addEventListener('change',search); search(); input.focus();
    } else {
      body.append(make('p', memoryOnly ? 'Browser storage is unavailable. These items will last only while this page is open.' : 'Stored in this browser on this device. No account needed.'));
      const paths = mode === 'saved' ? saved : recent;
      if (!paths.length) body.append(make('p', mode === 'saved' ? 'Your shortlist is empty. Save a product or guide to find it here later.' : 'No recently viewed guides. Open a product or guide to get started.'));
      if (mode === 'recent' && paths.length) { const clear = make('button', 'Clear viewing history'); clear.type = 'button'; clear.addEventListener('click', () => { recent = []; write(recentKey,recent); render(); close.focus(); }); body.append(clear); }
      list(paths.map(id => entries.find(p => p.path === id)).filter(Boolean),body);
    }
  }
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { opener?.focus(); });
  document.querySelectorAll('[data-discovery-open]').forEach(el => { el.hidden = false; el.addEventListener('click', () => { opener = el; mode = el.dataset.discoveryOpen; dialog.showModal(); render(); }); });
  Promise.all([fetch(url('discovery-index.json')).then(r => { if (!r.ok) throw Error(); return r.json(); }), fetch(url('reader-catalog.json')).then(r => r.ok ? r.json() : []).catch(() => [])]).then(([index,catalog]) => {
    entries = index; products = catalog; ready = true;
    saved = valid(read(savedKey)); recent = valid(read(recentKey)).slice(0,12);
    const page = entries.find(p => p.path === current);
    const isGuide = page && (current.includes('review') || current.startsWith('product-guides/') || current.startsWith('best-') || current.includes('-guide.'));
    if (isGuide) {
      recent = [current,...recent.filter(p => p !== current)].slice(0,12); write(recentKey,recent);
      document.querySelector('h1')?.after(saveButton(current));
    }
    document.querySelectorAll('article.card, article.product-card, article.feature-card').forEach(card => {
      const a = [...card.querySelectorAll('a[href]')].find(a => entries.some(p => url(p.path) === a.href));
      if (a) card.append(saveButton(entries.find(p => url(p.path) === a.href).path));
    });
    const p = products.find(p => p.review === current || p.aliases?.includes(current));
    if (p) {
      const words = text => new Set(text.toLowerCase().match(/[a-z0-9]+/g)?.filter(w => w.length > 3 && !['with','from','smart','home','switchbot','best','your','that','this'].includes(w)) || []);
      const terms = words(`${p.name} ${p.bestFor}`);
      const related = products.filter(q => q.id !== p.id && q.category === p.category && entries.some(e => e.path === q.review)).map(q => ({q, score:[...words(`${q.name} ${q.bestFor}`)].filter(w => terms.has(w)).length})).filter(x => x.score > 0).sort((a,b) => b.score-a.score).slice(0,3);
      if (related.length) { const section = make('section','','discovery-related'); section.setAttribute('aria-label','Related products'); section.append(make('h2','Explore similar options'),make('p','Related by category and purpose. Check each guide for compatibility and limitations.')); const ul=make('ul'); related.forEach(({q}) => { const li=make('li'), a=make('a',q.name); a.href=url(q.review); li.append(a,make('p',q.bestFor),saveButton(q.review)); ul.append(li); }); section.append(ul); const main=document.querySelector('main, .wrap'); if(main) main.append(section); }
    }
    if (dialog.open) render();
  }).catch(() => { failed = true; if(dialog.open) render(); });
  window.addEventListener('storage', e => { if (![savedKey,recentKey,null].includes(e.key) || !ready) return; saved=valid(read(savedKey)); recent=valid(read(recentKey)).slice(0,12); sync(); if(dialog.open && mode !== 'search') render(); });
})();
