const menuBtn=document.getElementById('menuBtn');
const nav=document.getElementById('nav');
if(menuBtn&&nav){
  menuBtn.addEventListener('click',()=>nav.classList.toggle('open'));
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
    if(msg) msg.textContent='Newsletter signup is coming soon. No email was stored.';
    e.target.reset();
  });
}

const year=document.getElementById('year');
if(year) year.textContent=new Date().getFullYear();

// Keep unfinished template links from sending visitors to GitHub Pages 404s.
// Until real affiliate/product URLs are supplied, route them to useful on-site guides.
document.querySelectorAll('a').forEach(link=>{
  const href=link.getAttribute('href')||'';
  const label=link.textContent.trim().toLowerCase();

  if(href.startsWith('YOUR-AFFILIATE-LINK-1')) link.setAttribute('href','guides.html#writing');
  if(href.startsWith('YOUR-AFFILIATE-LINK-4')) link.setAttribute('href','guides.html#coding');
  if(href.startsWith('YOUR-GEAR-AFFILIATE-LINK')) link.setAttribute('href','guides.html#creator');

  if(href==='#'){
    if(label.includes('contact')) link.setAttribute('href','contact.html');
    else if(label.includes('privacy')) link.setAttribute('href','privacy.html');
    else if(label.includes('terms')) link.setAttribute('href','terms.html');
    else if(label.includes('best ai tools for beginners')) link.setAttribute('href','guides.html#beginners');
    else if(label.includes('choose an ai writing tool')) link.setAttribute('href','guides.html#writing');
    else if(label.includes('creator setup')) link.setAttribute('href','guides.html#creator');
    else if(label.includes('free vs paid ai tools')) link.setAttribute('href','guides.html#free-paid');
  }
});
