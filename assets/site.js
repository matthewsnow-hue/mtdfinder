const h=document.querySelector('header.site');addEventListener('scroll',()=>h&&h.classList.toggle('scrolled',scrollY>8),{passive:true});
const mb=document.querySelector('.menu-btn');mb&&mb.addEventListener('click',()=>{const u=document.querySelector('.nav ul');u.classList.toggle('open');mb.setAttribute('aria-expanded',u.classList.contains('open'))});
const io='IntersectionObserver'in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08}):null;
document.querySelectorAll('.reveal').forEach(el=>io?io.observe(el):el.classList.add('in'));
// checker lead sign-up: swap in the copy for this result (copy lives in tools/build.py as <template>s)
const lead=document.getElementById('lead');
// next quarterly deadline (same sum as next_deadline() in tools/build.py)
const nextDl=(n=new Date())=>{const t=new Date(n.getFullYear(),n.getMonth(),n.getDate()),P={7:'6 April to 5 July',10:'6 April to 5 October',1:'6 April to 5 January',4:'6 April to 5 April (the whole tax year)'},S={7:'Aug',10:'Nov',1:'Feb',4:'May'},L={7:'August',10:'November',1:'February',4:'May'};
const d=[0,1].flatMap(a=>[7,10,1,4].map(m=>new Date(t.getFullYear()+a,m,7))).sort((a,b)=>a-b).find(x=>x>=t),m=d.getMonth();
return {short:'7 '+S[m]+' '+d.getFullYear(),long:'7\u00a0'+L[m],full:'7\u00a0'+L[m]+'\u00a0'+d.getFullYear(),period:P[m],card:'7 '+S[m],date:d,href:m==10?'guides/7-november-deadline/':'guides/deadline-calendar/'}};
const fillDl=root=>{const n=nextDl(),post=n.date>new Date(2027,4,7);root.querySelectorAll('[data-dl]').forEach(e=>e.textContent=n[e.dataset.dl]);root.querySelectorAll('[data-pen]').forEach(e=>e.hidden=(e.dataset.pen==='post')!==post)};
fillDl(document);document.querySelectorAll('[data-dl-href]').forEach(a=>a.setAttribute('href',nextDl().href));
const whyHtml=k=>{const t=document.getElementById('why-'+k);if(!t)return '';const c=t.content.cloneNode(true);fillDl(c);const d=document.createElement('div');d.append(c);return d.innerHTML};
const setLead=k=>{if(lead)lead.classList.toggle('lead-on',k!=='blank');if(!lead||lead.dataset.k===k)return;const t=document.getElementById('lead-'+k);if(!t)return;lead.dataset.k=k;
const c=t.content.cloneNode(true);fillDl(c);document.getElementById('lead-copy').replaceChildren(c);
const f=lead.querySelector('form'),h=f&&f.querySelector('input[type=hidden][name="'+f.dataset.resultField+'"]');if(h)h.value=k==='blank'?'':k};
// calculator
const cf=document.getElementById('calc');
let out0;if(cf){const gbp=n=>'£'+n.toLocaleString('en-GB');
const v=id=>Math.max(0,parseFloat(document.getElementById(id).value)||0);
const run=()=>{const y=[['2024 to 2025',50000,'6 April 2026'],['2025 to 2026',30000,'6 April 2027'],['2026 to 2027',20000,'6 April 2028']];
const out=document.getElementById('calc-out');let html='',hit=null;const blank=[...cf.querySelectorAll('input[type=number]')].every(i=>i.value.trim()==='');
y.forEach((r,i)=>{const t=v('se'+i)+v('pr'+i);if(!hit&&t>r[1])hit=[r,t];});
if(!document.getElementById('sa').checked){html='<span class="eyebrow">Your result</span><h3>Probably not yet</h3><p>MTD for Income Tax applies to sole traders and landlords registered for Self Assessment. If you start self-employment or letting, check again.</p>';setLead('not_self_assessment');}
else if(hit){html=`<span class="eyebrow">Your result</span><h3>From ${hit[0][2]}</h3><p>Your qualifying income for ${hit[0][0]} is ${gbp(hit[1])}, which is over the ${gbp(hit[0][1])} threshold. You will likely need MTD-compatible software from <strong>${hit[0][2]}</strong>, unless you're exempt.</p><p>${hit[0][1]===30000?'<a href="guides/30k-threshold-april-2027/">Your April 2027 checklist →</a><br>':''}<a href="finder/">Find compatible software →</a></p>`;setLead({50000:'from_apr_2026',30000:'from_apr_2027',20000:'from_apr_2028'}[hit[0][1]]);}
else{html='<span class="eyebrow">Your result</span><h3>Not on these figures</h3><p>Based on the income you entered, you are not over any announced threshold (up to 2026 to 2027). HMRC checks again each year, so revisit this if your turnover grows.</p>';setLead(blank?'blank':'under_threshold');}
out.innerHTML=html+whyHtml(lead&&lead.dataset.k||'')+'<p class="small">An estimate only, not tax advice. Confirm with <a href="https://www.gov.uk/guidance/find-out-if-and-when-you-need-to-use-making-tax-digital-for-income-tax" target="_blank" rel="noopener">HMRC\'s official checker<span class="vh"> (opens in new tab)</span></a>.</p>';};
cf.addEventListener('input',run);out0=document.getElementById('calc-out');out0.addEventListener('click',e=>{const a=e.target.closest('[data-lead-jump]');if(!a)return;e.preventDefault();lead.scrollIntoView({behavior:'smooth',block:'start'});document.getElementById('lead-email').focus({preventScroll:true})});cf.addEventListener('submit',e=>{e.preventDefault();run()});run();}
// finder
const list=document.getElementById('list');
if(list){fetch(list.dataset.src).then(r=>r.json()).then(d=>{const P=d.products;const st={who:'any',type:'any',free:false,vat:false,cis:false,assist:false,welsh:false,tax:false,q:''};const sel=new Set();
document.getElementById('count-total').textContent=P.length;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const yn=b=>b?'<span class="yes">Yes</span>':'<span class="no">No</span>';
const who=p=>[p.sole_trader&&'Sole trader',p.landlord&&'Landlord'].filter(Boolean).join(', ')||'See HMRC';
const typ=p=>[p.creates_records&&'Bookkeeping',p.bridging&&'Bridging'].filter(Boolean).join(' + ');
const tray=document.getElementById('tray');
const upd=()=>{document.getElementById('tray-n').textContent=sel.size+' selected (max 3)';tray.classList.toggle('show',sel.size>0)};
const draw=()=>{const q=st.q.toLowerCase().trim();const r=P.filter(p=>(st.who=='any'||(st.who=='st'&&p.sole_trader)||(st.who=='ll'&&p.landlord)||(st.who=='both'&&p.sole_trader&&p.landlord))&&(st.type=='any'||(st.type=='bridging'&&p.bridging)||(st.type=='records'&&p.creates_records))&&(!st.free||p.free_version)&&(!st.vat||p.vat)&&(!st.cis||p.cis)&&(!st.assist||p.hmrc_assist)&&(!st.welsh||p.welsh)&&(!st.tax||(/Tax return/.test(p.submissions)&&/Quarterly updates/.test(p.submissions)))&&(!q||p.name.toLowerCase().includes(q)));
document.getElementById('count').textContent=r.length;
list.innerHTML=r.map(p=>`<article class="card prod"><h3>${esc(p.name)}</h3><div class="tags">${p.bridging&&!p.creates_records?'<span class="tag tag-bridge">Bridging (spreadsheet)</span>':''}${p.vat?'<span class="tag">MTD for VAT</span>':''}${p.cis?'<span class="tag">CIS</span>':''}${p.hmrc_assist?'<span class="tag">HMRC Assist</span>':''}${p.welsh?'<span class="tag">Welsh</span>':''}</div><dl class="spec"><dt>For</dt><dd>${who(p)}</dd><dt>Type</dt><dd>${typ(p)}</dd><dt>Free version</dt><dd>${yn(p.free_version)}</dd><dt>Sends tax return</dt><dd>${yn(/Tax return/.test(p.submissions))}</dd><dt>Price</dt><dd>${p.free_version?'Free tier, check vendor':'Check vendor'}</dd></dl><div class="links">${p.website?`<a href="${esc(p.website)}" rel="noopener nofollow" target="_blank">Vendor ↗<span class="vh"> (opens in new tab)</span></a>`:''}<a href="${p.hmrc_url}" rel="noopener" target="_blank">HMRC listing ↗<span class="vh"> (opens in new tab)</span></a><label class="cmp"><input type="checkbox" data-id="${p.id}" ${sel.has(p.id)?'checked':''}> Compare</label></div></article>`).join('')||'<p>No products match. Try removing a filter.</p>';};
list.addEventListener('change',e=>{const id=e.target.dataset.id;if(!id)return;if(e.target.checked){if(sel.size>=3){e.target.checked=false;return}sel.add(id)}else sel.delete(id);upd()});
const dlg=document.getElementById('cmp');
document.getElementById('cmp-open').addEventListener('click',()=>{const ps=P.filter(p=>sel.has(p.id));const rows=[['For',who],['Type',typ],['Free version',p=>yn(p.free_version)],['Submits',p=>esc(p.submissions)],['Income sources',p=>esc(p.income_sources)],['MTD for VAT',p=>yn(p.vat)],['CIS',p=>yn(p.cis)],['HMRC Assist',p=>yn(p.hmrc_assist)],['Welsh',p=>yn(p.welsh)],['Links',p=>`${p.website?`<a href="${esc(p.website)}" target="_blank" rel="noopener nofollow">Vendor</a> · `:''}<a href="${p.hmrc_url}" target="_blank" rel="noopener">HMRC</a>`]];
document.getElementById('cmp-body').innerHTML=`<table><thead><tr><th></th>${ps.map(p=>`<th>${esc(p.name)}</th>`).join('')}</tr></thead><tbody>${rows.map(([k,f])=>`<tr><th scope="row">${k}</th>${ps.map(p=>`<td>${f(p)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;dlg.showModal()});
document.getElementById('cmp-close').addEventListener('click',()=>dlg.close());
document.querySelectorAll('[data-k]').forEach(b=>b.addEventListener('change',()=>{st[b.dataset.k]=b.checked;draw()}));
['who','type'].forEach(k=>document.getElementById(k).addEventListener('change',e=>{st[k]=e.target.value;draw()}));
let t;document.getElementById('q').addEventListener('input',e=>{clearTimeout(t);t=setTimeout(()=>{st.q=e.target.value;draw()},80)});
document.getElementById('clear').addEventListener('click',()=>{document.querySelectorAll('[data-k]').forEach(b=>{b.checked=false;st[b.dataset.k]=false});['who','type'].forEach(k=>{document.getElementById(k).value='any';st[k]='any'});draw()});
const ft=document.querySelector('.filter-toggle'),sd=document.getElementById('side');ft.addEventListener('click',()=>{sd.classList.toggle('open');ft.setAttribute('aria-expanded',sd.classList.contains('open'))});
draw();});}

(()=>{const q=new URLSearchParams(location.search);if(q.get('confirmed')){document.querySelectorAll('.nl-confirmed').forEach(e=>e.hidden=false)}if(q.get('thanks')){document.querySelectorAll('.nl-thanks').forEach(e=>e.hidden=false)}
document.querySelectorAll('form.nl').forEach(f=>{f.noValidate=true;const m=f.querySelector('.nl-msg'),b=f.querySelector('button'),lbl=b.textContent,ck=f.querySelector('input[name=consent]'),say=(t,c)=>{m.className='nl-msg '+c;m.innerHTML=t};
f.addEventListener('submit',async e=>{e.preventDefault();const em=f.email_address.value.trim();f.querySelectorAll('[aria-invalid]').forEach(x=>x.removeAttribute('aria-invalid'));
if(f.website.value){f.classList.add('done');say("Thanks! Please check your inbox to confirm.",'ok');return}
if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)){say('Please enter a valid email address.','err');f.email_address.setAttribute('aria-invalid','true');f.email_address.focus();return}
if(ck&&!ck.checked){say("Please tick the box to say you're happy for us to email you.",'err');ck.setAttribute('aria-invalid','true');ck.focus();return}
const body=new URLSearchParams({email_address:em});
if(ck){const seg=f.querySelector('input[type=radio]:checked');if(seg&&seg.value)body.append(seg.name,seg.value);const r=f.dataset.resultField&&f.querySelector('input[type=hidden][name="'+f.dataset.resultField+'"]');if(r&&r.value)body.append(r.name,r.value)}
b.disabled=true;b.textContent='Sending…';
try{const r=await fetch(f.action,{method:'POST',headers:{'Accept':'application/json'},body});const d=await r.json();
if(d.status==='success'){f.classList.add('done');say("Nearly there. We've sent a confirmation email to <strong>"+em.replace(/</g,'&lt;')+"</strong>. Click the link inside to start receiving reminders.",'ok')}
else if(d.status==='quarantined'&&d.url){say('One quick security check from our email provider, Kit. Taking you there now…','ok');location.href=d.url;return}
else{throw 0}}catch(_){say('Sorry, something went wrong. Please try again, or email <a href="mailto:hello@mtdfinder.co.uk">hello@mtdfinder.co.uk</a>.','err')}
finally{b.disabled=false;b.textContent=lbl}})})})();
// ACSP finder (acsp/): filters data/acsp.json in the browser. A to Z only, never paid.
(()=>{const out=document.getElementById('acsp-out');if(!out)return;const q=document.getElementById('acsp-q'),s=document.getElementById('acsp-s'),c=document.getElementById('acsp-count');
const esc=t=>String(t).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));const MAX=60;
fetch(out.dataset.src).then(r=>r.json()).then(d=>{const A=d.agents;const run=()=>{const v=q.value.trim().toUpperCase().replace(/\s+/g,' '),pc=v.replace(/\s/g,''),sv=s.value;
if(!v&&!sv){c.textContent=`${A.length.toLocaleString('en-GB')} agents on the list. Type a town, postcode area or name to search.`;out.innerHTML='';return}
const r=A.filter(a=>(!sv||a.s===sv)&&(!v||a.t.toUpperCase().includes(v)||a.n.toUpperCase().includes(v)||(pc.length>=2&&(a.d===pc||(/\d$/.test(pc)?false:a.d.replace(/\d.*$/,'')===pc)))));
c.textContent=r.length?`${r.length.toLocaleString('en-GB')} found${r.length>MAX?`, showing the first ${MAX}. Narrow your search to see more`:''}.`:'No agents found. Try a nearby town, or the first letters of a postcode (e.g. BS).';
out.innerHTML=r.length?'<div class="grid">'+r.slice(0,MAX).map(a=>`<article class="card prod"><h3>${esc(a.n)}</h3><dl class="spec"><dt>Town</dt><dd>${esc(a.t)}</dd><dt>Postcode area</dt><dd>${esc(a.d)}</dd><dt>AML supervisor</dt><dd>${esc(a.s)}</dd></dl></article>`).join('')+'</div>':'';};
q.addEventListener('input',run);s.addEventListener('change',run);run();}).catch(()=>{c.textContent='The list didn’t load. Try the Companies House list linked below.'})})();
