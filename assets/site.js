const h=document.querySelector('header.site');addEventListener('scroll',()=>h&&h.classList.toggle('scrolled',scrollY>8),{passive:true});
const mb=document.querySelector('.menu-btn');mb&&mb.addEventListener('click',()=>{const u=document.querySelector('.nav ul');u.classList.toggle('open');mb.setAttribute('aria-expanded',u.classList.contains('open'))});
const io='IntersectionObserver'in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08}):null;
document.querySelectorAll('.reveal').forEach(el=>io?io.observe(el):el.classList.add('in'));
// calculator
const cf=document.getElementById('calc');
if(cf){const gbp=n=>'£'+n.toLocaleString('en-GB');
const v=id=>Math.max(0,parseFloat(document.getElementById(id).value)||0);
const run=()=>{const y=[['2024 to 2025',50000,'6 April 2026'],['2025 to 2026',30000,'6 April 2027'],['2026 to 2027',20000,'6 April 2028']];
const out=document.getElementById('calc-out');let html='',hit=null;
y.forEach((r,i)=>{const t=v('se'+i)+v('pr'+i);if(!hit&&t>r[1])hit=[r,t];});
if(!document.getElementById('sa').checked){html='<span class="eyebrow" style="color:#9fd3bf">Your result</span><h3>Probably not yet</h3><p>MTD for Income Tax applies to sole traders and landlords registered for Self Assessment. If you start self-employment or letting, check again.</p>';}
else if(hit){html=`<span class="eyebrow" style="color:#9fd3bf">Your result</span><h3>From ${hit[0][2]}</h3><p>Your qualifying income for ${hit[0][0]} is ${gbp(hit[1])}, which is over the ${gbp(hit[0][1])} threshold. You will likely need MTD-compatible software from <strong>${hit[0][2]}</strong>, unless you're exempt.</p><p><a href="finder/">Find compatible software →</a></p>`;}
else{html='<span class="eyebrow" style="color:#9fd3bf">Your result</span><h3>Not on these figures</h3><p>Based on the income you entered, you are not over any announced threshold (up to 2026 to 2027). HMRC checks again each year, so revisit this if your turnover grows.</p>';}
out.innerHTML=html+'<p class="small">An estimate only, not tax advice. Confirm with <a href="https://www.gov.uk/guidance/check-if-youre-eligible-for-making-tax-digital-for-income-tax" rel="noopener">HMRC\'s official checker</a>.</p>';};
cf.addEventListener('input',run);cf.addEventListener('submit',e=>{e.preventDefault();run()});run();}
// finder
const list=document.getElementById('list');
if(list){fetch(list.dataset.src).then(r=>r.json()).then(d=>{const P=d.products;const st={who:'any',type:'any',free:false,vat:false,cis:false,assist:false,welsh:false,tax:false,q:''};
document.getElementById('count-total').textContent=P.length;
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const draw=()=>{const q=st.q.toLowerCase();const r=P.filter(p=>(st.who=='any'||(st.who=='st'&&p.sole_trader)||(st.who=='ll'&&p.landlord)||(st.who=='both'&&p.sole_trader&&p.landlord))&&(st.type=='any'||(st.type=='bridging'&&p.bridging)||(st.type=='records'&&p.creates_records))&&(!st.free||p.free_version)&&(!st.vat||p.vat)&&(!st.cis||p.cis)&&(!st.assist||p.hmrc_assist)&&(!st.welsh||p.welsh)&&(!st.tax||/Tax return/.test(p.submissions))&&(!q||p.name.toLowerCase().includes(q)));
document.getElementById('count').textContent=r.length;
list.innerHTML=r.map(p=>`<article class="card prod"><h3>${esc(p.name)}</h3><div class="small">${esc(p.price)} · last checked ${d.last_checked}</div><div class="tags">${p.sole_trader?'<span class="tag">Sole trader</span>':''}${p.landlord?'<span class="tag">Landlord</span>':''}${p.creates_records?'<span class="tag">Bookkeeping</span>':''}${p.bridging?'<span class="tag">Bridging</span>':''}${p.free_version?'<span class="tag">Free version</span>':''}${p.vat?'<span class="tag grey">MTD for VAT</span>':''}${p.cis?'<span class="tag grey">CIS</span>':''}${p.hmrc_assist?'<span class="tag grey">HMRC Assist</span>':''}${p.welsh?'<span class="tag grey">Welsh</span>':''}</div><div class="small">Submits: ${esc(p.submissions||'see HMRC')}</div><div class="links">${p.website?`<a href="${esc(p.website)}" rel="noopener nofollow" target="_blank">Vendor site ↗</a>`:''}<a href="${p.hmrc_url}" rel="noopener" target="_blank">HMRC listing ↗</a></div></article>`).join('')||'<p>No products match. Try removing a filter.</p>';};
document.querySelectorAll('[data-k]').forEach(b=>b.addEventListener('click',()=>{const k=b.dataset.k;st[k]=!st[k];b.setAttribute('aria-pressed',st[k]);draw()}));
['who','type'].forEach(k=>document.getElementById(k).addEventListener('change',e=>{st[k]=e.target.value;draw()}));
document.getElementById('q').addEventListener('input',e=>{st.q=e.target.value;draw()});draw();});}
