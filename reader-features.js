(() => {
  'use strict';
  const source = document.currentScript;
  const base = new URL('.', source.src);
  const today = new Date().toISOString().slice(0, 10);
  document.querySelectorAll('[data-reader-expires]').forEach(b => { if (b.dataset.readerExpires < today) b.remove(); });
  const key = 'aigearhub-compare-v1';
  const make = (tag, text, cls) => { const e = document.createElement(tag); if (text) e.textContent = text; if (cls) e.className = cls; return e; };
  const url = path => new URL(path, base).href;
  const pathOf = href => { try { const u = new URL(href, location.href); return u.origin === base.origin && u.pathname.startsWith(base.pathname) ? decodeURI(u.pathname.slice(base.pathname.length)) : u.href.split('#')[0]; } catch { return ''; } };
  fetch(url('reader-catalog.json')).then(r => { if (!r.ok) throw Error('Catalog unavailable'); return r.json(); }).then(catalog => {
    catalog.forEach(p => { if (p.badge && p.badge.reviewDue < today) p.badge = null; });
    const products = new Map(catalog.map(p => [p.id, p]));
    const aliases = new Map();
    catalog.forEach(p => [p.review, ...(p.aliases || [])].forEach(a => aliases.set(pathOf(url(a)), p.id)));
    let selected = [];
    try { const saved = JSON.parse(localStorage.getItem(key) || '[]'); if (Array.isArray(saved)) selected = [...new Set(saved.filter(id => products.has(id)))].slice(0, 4); } catch {}
    const controls = [];
    const live = make('div', '', 'reader-live'); live.setAttribute('role', 'status'); document.body.append(live);
    let messageTimer;
    function announce(text) { live.textContent = text; clearTimeout(messageTimer); messageTimer = setTimeout(() => { live.textContent = ''; }, 5000); }
    const tray = make('aside', '', 'reader-tray'); tray.hidden = true; tray.setAttribute('aria-label', 'Selected products');
    const trayHead = make('div', '', 'reader-tray-head'), count = make('strong'), actions = make('div', '', 'reader-actions'), items = make('div', '', 'reader-tray-items');
    const compare = make('button', 'Compare now', 'reader-primary'), clear = make('button', 'Clear all'); compare.type = clear.type = 'button';
    actions.append(compare, clear); trayHead.append(count, actions); tray.append(trayHead, items); document.body.append(tray);
    const dialog = make('dialog', '', 'reader-dialog'); dialog.setAttribute('aria-labelledby', 'reader-compare-title');
    const dialogHead = make('div', '', 'reader-actions'), title = make('h2', 'Your comparison'), close = make('button', 'Close comparison'); title.id = 'reader-compare-title'; close.type = 'button';
    dialogHead.append(title, close); const body = make('div'); dialog.append(dialogHead, body); document.body.append(dialog);
    close.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
    let previousFocus;
    dialog.addEventListener('close', () => { if (previousFocus?.isConnected) previousFocus.focus(); });
    function setSelection(id, checked) {
      if (checked && !selected.includes(id)) { if (selected.length >= 4) { announce('Compare up to four products. Remove one before adding another.'); sync(); return; } selected.push(id); }
      else if (!checked) selected = selected.filter(x => x !== id);
      try { localStorage.setItem(key, JSON.stringify(selected)); } catch {}
      sync(); announce(`${selected.length} of 4 products selected.`);
    }
    function sync() {
      controls.forEach(({input, id}) => { input.checked = selected.includes(id); });
      tray.hidden = !selected.length; compare.disabled = selected.length < 2; count.textContent = `${selected.length} of 4 selected${selected.length === 1 ? ' · Choose one more' : ''}`;
      items.replaceChildren();
      selected.forEach(id => { const p = products.get(id), chip = make('div', '', 'reader-chip'), remove = make('button', '×'); remove.type = 'button'; remove.setAttribute('aria-label', `Remove ${p.name}`); remove.addEventListener('click', () => { setSelection(id, false); if (!tray.hidden) (items.querySelector('button') || clear).focus(); else controls.find(c => c.id === id)?.input.focus(); }); chip.append(make('span', p.name), remove); items.append(chip); });
      updateSpace();
    }
    const originalPadding = parseFloat(getComputedStyle(document.body).paddingBottom) || 0;
    function updateSpace() {
      if (typeof document === 'undefined' || !document.body) return;
      const consent = document.querySelector('[aria-label="Analytics preferences"]');
      const offset = consent ? consent.getBoundingClientRect().height + 32 : 0;
      tray.style.bottom = `${offset}px`; live.style.bottom = `${offset + (tray.hidden ? 12 : tray.getBoundingClientRect().height + 12)}px`;
      document.body.style.paddingBottom = `${originalPadding + (tray.hidden ? 0 : tray.getBoundingClientRect().height + offset)}px`;
    }
    const resizeObserver = new ResizeObserver(updateSpace); resizeObserver.observe(tray);
    const observer = new MutationObserver(updateSpace); observer.observe(document.body, {childList: true}); window.addEventListener('resize', updateSpace);
    window.addEventListener('pagehide', () => { resizeObserver.disconnect(); observer.disconnect(); });
    clear.addEventListener('click', () => { const id = selected[0]; selected = []; try { localStorage.removeItem(key); } catch {} sync(); controls.find(c => c.id === id)?.input.focus(); announce('Comparison cleared.'); });
    compare.addEventListener('click', () => {
      if (selected.length < 2) return;
      previousFocus = document.activeElement; body.replaceChildren();
      body.append(make('p', 'Compare the intended use and limitations before choosing. These research-based summaries are not hands-on scores. Prices and availability must be checked with the retailer.'));
      const scroll = make('div', '', 'reader-table-scroll'); scroll.tabIndex = 0; scroll.setAttribute('role', 'region'); scroll.setAttribute('aria-label', 'Side-by-side comparison; scroll horizontally on small screens');
      const table = make('table', '', 'reader-table'), caption = make('caption', 'Your selected products'), head = make('thead'), heading = make('tr'); heading.append(make('th', 'What matters'));
      const picks = selected.map(id => products.get(id)); picks.forEach(p => { const th = make('th', p.name); th.scope = 'col'; heading.append(th); }); head.append(heading); table.append(caption, head);
      const tbody = make('tbody');
      [['Category', 'category'], ['Best suited to', 'bestFor'], ['Strengths / purpose', 'strengths'], ['Limitations', 'cautions'], ['Editorial selection', 'badge'], ['Price', 'price']].forEach(([label, field]) => {
        const row = make('tr'), th = make('th', label); th.scope = 'row'; row.append(th);
        picks.forEach(p => { const td = make('td'); const value = field === 'badge' ? (p.badge ? `${p.badge.label}: ${p.badge.reason}` : 'No badge assigned') : field === 'price' ? 'Check current retailer price; no verified price stored.' : p[field]; if (Array.isArray(value)) value.forEach(t => td.append(make('p', t))); else td.textContent = value || 'See full review'; row.append(td); }); tbody.append(row);
      });
      const links = make('tr'), label = make('th', 'Read more'); label.scope = 'row'; links.append(label);
      picks.forEach(p => { const td = make('td'), a = make('a', 'Read the full review'); a.href = url(p.review); td.append(a); links.append(td); }); tbody.append(links); table.append(tbody); scroll.append(table); body.append(scroll); dialog.showModal(); close.focus();
    });
    function addControl(container, id, details = false) {
      if (!id || container.querySelector('[data-reader-compare]')) return;
      const p = products.get(id), label = make('label', '', 'reader-select'), input = make('input'); input.type = 'checkbox'; input.dataset.readerCompare = id; input.setAttribute('aria-label', `Compare ${p.name}`); label.append(input, make('span', 'Compare')); input.addEventListener('change', () => setSelection(id, input.checked));
      if (details) { const wrap = make('div', '', 'reader-card-wrapper'); container.before(wrap); wrap.append(container); const controls = make('div', '', 'reader-controls'); controls.append(label); wrap.append(controls); } else container.append(label);
      controls.push({input, id});
    }
    document.querySelectorAll('article.card, article.feature-card, article.product-card, .gear-card, .gear-table tbody tr').forEach(card => {
      const a = [...card.querySelectorAll('a[href]')].find(a => aliases.has(pathOf(a.href)));
      if (a) addControl(card.tagName === 'TR' ? card.lastElementChild : card, aliases.get(pathOf(a.href)), card.tagName === 'DETAILS');
    });
    const current = aliases.get(pathOf(location.href));
    if (current) { const h1 = document.querySelector('h1'); if (h1) { const wrap = make('div'); h1.after(wrap); addControl(wrap, current); } }
    window.addEventListener('storage', e => { if (e.key !== key) return; try { const ids = JSON.parse(e.newValue || '[]'); selected = Array.isArray(ids) ? [...new Set(ids.filter(id => products.has(id)))].slice(0, 4) : []; } catch { selected = []; } sync(); });
    sync();
  }).catch(() => { /* The static guides, badges, dates and links remain available. */ });
})();
