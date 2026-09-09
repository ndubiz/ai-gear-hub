/* Progressive enhancement: without JS the info icons link to the glossary. */
(() => {
  'use strict';
  let active = null;
  let pointerFocus = false;
  document.addEventListener('pointerdown', () => { pointerFocus = true; }, true);
  document.addEventListener('keydown', () => { pointerFocus = false; }, true);
  function close() {
    if (!active) return;
    active.tip.hidden = true;
    active.button.setAttribute('aria-expanded', 'false');
    active = null;
  }
  function place() {
    if (!active) return;
    const r = active.button.getBoundingClientRect(), tip = active.tip;
    const width = tip.getBoundingClientRect().width;
    tip.style.left = Math.max(12, Math.min(r.left, window.innerWidth - width - 12)) + 'px';
    const height = tip.getBoundingClientRect().height;
    tip.style.top = Math.max(12, r.top - height - 8 >= 12 ? r.top - height - 8 : Math.min(r.bottom + 8, window.innerHeight - height - 12)) + 'px';
  }
  document.querySelectorAll('.shopping-info').forEach((host, i) => {
    const link = host.querySelector('a');
    if (!link) return;
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = '?';
    button.setAttribute('aria-label', link.getAttribute('aria-label'));
    button.setAttribute('aria-expanded', 'false');
    const tip = document.createElement('span');
    tip.className = 'shopping-tooltip'; tip.id = 'shopping-tip-' + i;
    tip.setAttribute('role', 'tooltip'); tip.textContent = host.dataset.explanation; tip.hidden = true;
    button.setAttribute('aria-describedby', tip.id);
    button.setAttribute('aria-controls', tip.id);
    host.replaceChildren(button, tip);
    function open() { close(); active = { button, tip, host }; tip.hidden = false; button.setAttribute('aria-expanded', 'true'); place(); }
    host.addEventListener('pointerenter', e => { if (e.pointerType !== 'touch') open(); });
    host.addEventListener('pointerleave', () => { if (document.activeElement !== button && active?.host === host) close(); });
    // Keyboard focus opens it; taps use click so first tap never immediately closes it.
    button.addEventListener('focus', () => { if (!pointerFocus) open(); });
    button.addEventListener('blur', () => { if (active?.host === host) close(); });
    button.addEventListener('click', () => active?.host === host ? close() : open());
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  document.addEventListener('pointerdown', e => { if (active && !active.host.contains(e.target)) close(); });
  window.addEventListener('resize', close);
  window.addEventListener('scroll', close, true);
})();
