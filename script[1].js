const menuBtn=document.getElementById('menuBtn');
const nav=document.getElementById('nav');
menuBtn.addEventListener('click',()=>nav.classList.toggle('open'));
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nav.classList.remove('open')));

const cats=[...document.querySelectorAll('.cat')];
const items=[...document.querySelectorAll('.searchable')];
const searchForm=document.getElementById('searchForm');
const searchInput=document.getElementById('searchInput');
const emptyState=document.getElementById('emptyState');

function applyFilter(category='all', term=''){
  term=term.trim().toLowerCase();
  let visibleProducts=0;
  items.forEach(item=>{
    const cats=(item.dataset.category||'').split(' ');
    const text=(item.dataset.search||'')+' '+item.textContent.toLowerCase();
    const catOk=category==='all'||cats.includes(category);
    const searchOk=!term||text.includes(term);
    const show=catOk&&searchOk;
    item.classList.toggle('hidden',!show);
    if(show && item.classList.contains('product-card')) visibleProducts++;
  });
  emptyState.style.display=(visibleProducts===0 && document.querySelector('#tools:not(.hidden)'))?'block':'none';
}
cats.forEach(btn=>btn.addEventListener('click',()=>{
  cats.forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  applyFilter(btn.dataset.filter, searchInput.value);
  if(btn.dataset.filter==='gear') document.getElementById('gear').scrollIntoView({behavior:'smooth'});
  else document.getElementById('tools').scrollIntoView({behavior:'smooth'});
}));
searchForm.addEventListener('submit',e=>{
  e.preventDefault();
  cats.forEach(b=>b.classList.remove('active'));
  cats[0].classList.add('active');
  applyFilter('all',searchInput.value);
  document.getElementById('tools').scrollIntoView({behavior:'smooth'});
});
document.getElementById('newsletterForm').addEventListener('submit',e=>{
  e.preventDefault();
  const msg=document.getElementById('formMessage');
  msg.textContent='Thanks! Connect this form to your email service before publishing.';
  e.target.reset();
});
document.getElementById('year').textContent=new Date().getFullYear();
