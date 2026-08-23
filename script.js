const menuBtn=document.getElementById('menuBtn');
const nav=document.getElementById('nav');
if(menuBtn&&nav){
  menuBtn.addEventListener('click',()=>{
    const isOpen=nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded',String(isOpen));
    menuBtn.setAttribute('aria-label',isOpen?'Close navigation':'Open navigation');
  });
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nav.classList.remove('open')));
}

const cats=[...document.querySelectorAll('.cat')];
const items=[...document.querySelectorAll('.searchable')];
const searchForm=document.getElementById('searchForm');
const searchInput=document.getElementById('searchInput');
const emptyState=document.getElementById('emptyState');

function applyFilter(category='all', term=''){
  term=term.trim().toLowerCase();
  let visibleProducts=0;
  items.forEach(item=>{
    const itemCats=(item.dataset.category||'').split(' ');
    const text=((item.dataset.search||'')+' '+item.textContent).toLowerCase();
    const catOk=category==='all'||itemCats.includes(category);
    const searchOk=!term||text.includes(term);
    const show=catOk&&searchOk;
    item.classList.toggle('hidden',!show);
    if(show&&item.classList.contains('product-card')) visibleProducts++;
  });
  if(emptyState) emptyState.style.display=visibleProducts===0?'block':'none';
}

cats.forEach(btn=>btn.addEventListener('click',()=>{
  cats.forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  applyFilter(btn.dataset.filter,searchInput?searchInput.value:'');
  const target=btn.dataset.filter==='gear'?document.getElementById('gear'):document.getElementById('tools');
  if(target) target.scrollIntoView({behavior:'smooth'});
}));

if(searchForm&&searchInput){
  searchForm.addEventListener('submit',e=>{
    e.preventDefault();
    cats.forEach(b=>b.classList.remove('active'));
    if(cats[0]) cats[0].classList.add('active');
    applyFilter('all',searchInput.value);
    const tools=document.getElementById('tools');
    if(tools) tools.scrollIntoView({behavior:'smooth'});
  });
}

const newsletterForm=document.getElementById('newsletterForm');
if(newsletterForm){
  newsletterForm.addEventListener('submit',e=>{
    e.preventDefault();
    const msg=document.getElementById('formMessage');
    if(msg) msg.textContent='Thanks for your interest. Email updates are being prepared; no address was stored.';
    e.target.reset();
  });
}

const year=document.getElementById('year');
if(year) year.textContent=new Date().getFullYear();

document.querySelectorAll('a').forEach(link=>{
  const href=link.getAttribute('href')||'';
  const label=link.textContent.trim().toLowerCase();
  if(href.startsWith('YOUR-AFFILIATE-LINK-1')) link.setAttribute('href','guides.html#writing');
  if(href.startsWith('YOUR-AFFILIATE-LINK-4')) link.setAttribute('href','guides.html#coding');
  if(href.startsWith('YOUR-GEAR-AFFILIATE-LINK')) link.setAttribute('href','amazon-ai-picks.html');
  if(href==='#'){
    if(label.includes('contact')) link.setAttribute('href','contact.html');
    else if(label.includes('privacy')) link.setAttribute('href','privacy.html');
    else if(label.includes('terms')) link.setAttribute('href','terms.html');
    else if(label.includes('best ai tools for beginners')) link.setAttribute('href','guides.html#beginners');
    else if(label.includes('choose an ai writing tool')) link.setAttribute('href','guides.html#writing');
    else if(label.includes('creator setup')) link.setAttribute('href','amazon-ai-picks.html');
    else if(label.includes('free vs paid ai tools')) link.setAttribute('href','guides.html#free-paid');
  }
});

if(nav&&!nav.querySelector('a[href="amazon-ai-picks.html"]')){
  const a=document.createElement('a');
  a.href='amazon-ai-picks.html';
  a.textContent='Amazon Picks';
  const about=[...nav.querySelectorAll('a')].find(x=>x.textContent.trim().toLowerCase()==='about');
  if(about) nav.insertBefore(a,about); else nav.appendChild(a);
}
if(nav&&!nav.querySelector('a[href="anthbot-de.html"]')){
  const a=document.createElement('a');
  a.href='anthbot-de.html';
  a.textContent='ANTHBOT DE';
  const about=[...nav.querySelectorAll('a')].find(x=>x.textContent.trim().toLowerCase()==='about');
  if(about) nav.insertBefore(a,about); else nav.appendChild(a);
}

const navCta=document.querySelector('.nav-cta');
if(navCta){
  navCta.href='amazon-ai-picks.html';
  navCta.textContent='Shop AI gear';
}

const main=document.querySelector('main');
if(main&&!document.getElementById('amazonDisclosure')){
  const disclosure=document.createElement('div');
  disclosure.id='amazonDisclosure';
  disclosure.style.cssText='max-width:1180px;margin:18px auto 0;padding:0 24px;font-size:12px;line-height:1.55;color:#667085';
  disclosure.innerHTML='<strong>Affiliate disclosure:</strong> As an Amazon Associate I earn from qualifying purchases. AI Gear Hub may also earn commissions from other approved affiliate partners at no extra cost to you.';
  main.insertBefore(disclosure,main.firstChild.nextSibling);
}

document.querySelectorAll('.product-card').forEach(card=>{
  const text=(card.textContent||'').toLowerCase();
  const placeholder=[...card.querySelectorAll('span,a')].find(el=>el.textContent.toLowerCase().includes('affiliate link coming soon'));
  if(placeholder){
    const replacement=document.createElement('a');
    replacement.className='affiliate-btn';
    replacement.href=text.includes('coding')?'guides.html#coding':'guides.html#writing';
    replacement.textContent=text.includes('coding')?'See coding recommendations →':'See writing recommendations →';
    placeholder.replaceWith(replacement);
  }
  const rating=card.querySelector('.rating');
  if(rating&&rating.textContent.includes('★★★★★')&&(text.includes('ai writing assistant')||text.includes('ai coding assistant'))){
    rating.innerHTML='<span>Buyer guide</span>';
  }
});

const gear=document.getElementById('gear');
if(gear){
  const sectionCopy=gear.querySelector('.section-head p');
  if(sectionCopy) sectionCopy.textContent='Practical AI hardware and creator gear with buyer guides, product comparisons and affiliate-supported shopping links.';

  gear.querySelectorAll('.gear-card').forEach(card=>{
    const body=(card.textContent||'').toLowerCase();
    const pending=[...card.querySelectorAll('span')].find(s=>s.textContent.toLowerCase().includes('recommendations coming soon'));
    if(pending){
      const a=document.createElement('a');
      a.href='amazon-ai-picks.html';
      a.textContent='Browse current gear picks →';
      pending.replaceWith(a);
    }
    const review=card.querySelector('a');
    if(review&&(body.includes('plaud')||body.includes('roborock')||body.includes('eufy')||body.includes('translation'))&&!card.querySelector('.shop-picks-link')){
      const shop=document.createElement('a');
      shop.className='shop-picks-link';
      shop.href='amazon-ai-picks.html';
      shop.style.marginLeft='8px';
      shop.textContent='Shop picks →';
      review.insertAdjacentElement('afterend',shop);
    }
  });

  const gearGrid=gear.querySelector('.gear-grid');
  const eufyCard=[...gear.querySelectorAll('.gear-card')].find(card=>card.textContent.toLowerCase().includes('eufy ai security camera'));
  if(gearGrid&&eufyCard&&!gear.querySelector('[data-search*="amazon ai picks"]')){
    eufyCard.insertAdjacentHTML('afterend',`
      <article class="gear-card searchable" data-category="gear ai" data-search="amazon ai picks tools security cameras gadgets">
        <div class="gear-visual">🛠️</div><div class="gear-info"><span>AI Gadgets</span><h3>5 AI Tools & Security Cameras</h3><p>Hand-picked AI accessories and security cameras worth buying right now.</p><a href="amazon-ai-picks.html">Read full review →</a></div>
      </article>
      <article class="gear-card searchable" data-category="gear ai" data-search="eufy picks s3 pro doorbell e340 cameras">
        <div class="gear-visual">📹</div><div class="gear-info"><span>AI Security</span><h3>More eufy Cameras Compared</h3><p>eufyCam S3 Pro and Video Doorbell E340 — two more eufy picks beyond the SoloCam S340.</p><a href="eufy-picks.html">Read full review →</a></div>
      </article>`);
  }
  if(gearGrid&&!gear.querySelector('[data-search*="anthbot"]')){
    gearGrid.insertAdjacentHTML('beforeend',`
      <article class="gear-card searchable" data-category="gear ai" data-search="anthbot robot lawn mower smart garden n8 germany de">
        <div class="gear-visual">🌱</div><div class="gear-info"><span>AI Garden · Germany</span><h3>ANTHBOT Smart Lawn Robots</h3><p>Robot lawn mowers and smart outdoor automation, with a dedicated German partner page and tracked ANTHBOT DE buying links.</p><a href="anthbot-de.html">German buying guide →</a></div>
      </article>
      <article class="gear-card searchable" data-category="gear ai" data-search="anthbot international global robot lawn mower smart garden">
        <div class="gear-visual">🌍</div><div class="gear-info"><span>AI Garden · International</span><h3>ANTHBOT International Guide</h3><p>English-language buyer guidance for international visitors, kept separate from the ANTHBOT DE affiliate funnel.</p><a href="anthbot-global.html">International guide →</a></div>
      </article>`);
  }
}

const compare=document.getElementById('compare');
if(compare){
  const cards=[...compare.querySelectorAll('.compare-card')];
  if(cards[0]) cards[0].innerHTML='<span class="compare-kicker">AI Gear</span><h3>Which smart gadget fits your workflow?</h3><div class="compare-row"><span>Meetings & notes</span><strong>PLAUD NotePin</strong></div><div class="compare-row"><span>Home security</span><strong>eufy SoloCam</strong></div><div class="compare-row"><span>Smart garden</span><strong>ANTHBOT</strong></div><a href="amazon-ai-picks.html">Compare our current picks →</a>';
  if(cards[1]) cards[1].innerHTML='<span class="compare-kicker">Video</span><h3>Create once, publish everywhere</h3><div class="compare-row"><span>AI video creation</span><strong>BlueFX</strong></div><div class="compare-row"><span>Distribution</span><strong>Repurpose.io</strong></div><div class="compare-row"><span>Best starting point</span><strong>Read the workflow</strong></div><a href="#tools">See video tools →</a>';
  if(cards[2]) cards[2].innerHTML='<span class="compare-kicker">Buying Guide</span><h3>Best AI gear for everyday use</h3><div class="compare-row"><span>Security</span><strong>AI cameras</strong></div><div class="compare-row"><span>Garden</span><strong>ANTHBOT robots</strong></div><div class="compare-row"><span>Productivity</span><strong>AI recorders</strong></div><a href="anthbot-de.html">See ANTHBOT DE →</a>';
}
