#!/usr/bin/env python3
"""Static site generator for MTD Finder. Run: python3 tools/build.py (outputs HTML to repo root)."""
import json,os,html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE="https://mtdfinder.co.uk"
UPDATED="2026-10-16"
PRIVACY_UPDATED="2026-10-19"
# GoatCounter visit counts (no cookies). Approved by Matthew, A-019; dashboard https://mtdfinder.goatcounter.com
# count.js is self-hosted at assets/count.js (version + SHA-256 in docs/goatcounter.md); hits still go to the GoatCounter /count endpoint.
GOATCOUNTER='<script data-goatcounter="https://mtdfinder.goatcounter.com/count" async src="/assets/count.js"></script>'
ICO_REG="ZC276141"
# Social preview images, made by tools/og_images.py (1200x630). Pages not listed use default.png.
OG_IMAGES={"guides/deadline-calendar/":"deadline-calendar","guides/7-november-deadline/":"7-november-deadline","guides/30k-threshold-april-2027/":"30k-threshold-april-2027"}
OG_DEFAULT_ALT="MTD Finder: Free Making Tax Digital checker and software finder"
ELIG="https://www.gov.uk/guidance/find-out-if-and-when-you-need-to-use-making-tax-digital-for-income-tax"
QI="https://www.gov.uk/guidance/work-out-your-qualifying-income-for-making-tax-digital-for-income-tax"
SW="https://www.gov.uk/guidance/choose-the-right-software-for-making-tax-digital-for-income-tax"
TOOL="https://www.tax.service.gov.uk/find-making-tax-digital-income-tax-software/"
QU="https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates"
TR="https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/submit-your-tax-return"
SIGN="https://www.gov.uk/guidance/sign-up-for-making-tax-digital-for-income-tax"
SADL="https://www.gov.uk/self-assessment-tax-returns/deadlines"
ICS="assets/mtd-deadlines-2026-27.ics"
EMAIL="hello@mtdfinder.co.uk"
SPONSOR_EMAIL="sponsors@mtdfinder.co.uk"
NEWS_EMAIL="newsletter@mtdfinder.co.uk"
KIT_FORM="https://app.kit.com/forms/10047232/subscriptions"
STRIPE="https://buy.stripe.com/fZu4gA75G9gW5qF59pa3u00"
PORTAL="https://billing.stripe.com/p/login/fZu4gA75G9gW5qF59pa3u00"
data=json.load(open(f"{ROOT}/data/products.json"))
N=data["count"]
_P=data["products"];NO_TR=sum(1 for x in _P if "Tax return" not in x["submissions"])
_lc=_dt0=__import__("datetime").date.fromisoformat(data["last_checked"])
LC_TEXT=f"{_lc.day} {_lc.strftime('%b %Y')}"
YEAR_END=f"{NO_TR} of {len(_P)} ({round(100*NO_TR/len(_P))}%) can't send the tax return, our count of HMRC's list, {_lc.day} {_lc.strftime('%b %Y')}"
NAV=[("finder/","Software finder"),("guides/deadlines/","Deadlines"),("guides/landlords/","Landlords"),("guides/tradespeople/","Trades"),("faq/","FAQ"),("sponsor/","Sponsor")]
import importlib.util as _ilu
_spec=_ilu.spec_from_file_location("mark",os.path.join(ROOT,"tools","mark.py"));_mark=_ilu.module_from_spec(_spec);_spec.loader.exec_module(_mark)
MARK_SVG=_mark.inline_svg()   # stacked-TD mark, same geometry as assets/mark.svg (tools/mark.py)
INDEXNOW_KEY="63c0dd59a7b04a26a8bf33b84a1ee5b7"
ORG={"@type":"Organization","@id":SITE+"/#org","name":"Sno Automations","alternateName":"MTD Finder","url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/assets/logo.png","width":512,"height":512},"image":SITE+"/assets/logo.png","email":EMAIL,"founder":{"@type":"Person","name":"Matthew Snow"},"areaServed":{"@type":"Country","name":"United Kingdom"},"knowsAbout":["Making Tax Digital for Income Tax","MTD software"],"contactPoint":[{"@type":"ContactPoint","contactType":"customer support","email":EMAIL,"availableLanguage":"en-GB"},{"@type":"ContactPoint","contactType":"sales","email":SPONSOR_EMAIL,"availableLanguage":"en-GB"}],"description":"MTD Finder is run by Matthew Snow trading as Sno Automations, a UK sole trader."}
def faq_ld(qs):return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html.unescape(__import__('re').sub('<[^>]+>','',a))}} for q,a in qs]}
def faq_html(qs):return "".join(f"<details class='reveal'><summary>{q}</summary><p>{a}</p></details>" for q,a in qs)
pages=[]
ITEMS={"@context":"https://schema.org","@type":"ItemList","name":"HMRC-recognised MTD for Income Tax software","numberOfItems":N,"itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"SoftwareApplication","name":p["name"],"applicationCategory":"FinanceApplication","operatingSystem":"Web","url":p["website"] or p["hmrc_url"]}} for i,p in enumerate(data["products"])]}

import re as _re
def ext_links(doc):
    def fix(m):
        attrs,inner=m.group(1),m.group(2)
        h=_re.search(r'href=["\'](https?://[^"\']+)',attrs)
        if not h or "mtdfinder.co.uk" in h.group(1):return m.group(0)
        attrs=_re.sub(r'\s*target=["\'][^"\']*["\']','',attrs)
        r=_re.search(r'rel=["\']([^"\']*)["\']',attrs)
        rels=(r.group(1).split() if r else [])
        for x in ("noopener",):
            if x not in rels:rels.append(x)
        attrs=_re.sub(r'\s*rel=["\'][^"\']*["\']','',attrs)+f' target="_blank" rel="{" ".join(rels)}"'
        if 'class="vh"' not in inner:inner+='<span class="vh"> (opens in new tab)</span>'
        return f'<a{attrs}>{inner}</a>'
    return _re.sub(r'<a(\s[^>]*)>(.*?)</a>',fix,doc,flags=_re.S)

def nl_form(pre,uid):
    return f"""<form class="nl" action="{KIT_FORM}" method="post" novalidate><div class="nl-row"><label class="vh" for="nl-{uid}">Email address</label><input id="nl-{uid}" type="email" name="email_address" required autocomplete="email" placeholder="you@example.co.uk"><button class="btn" type="submit">Subscribe</button></div><div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div><p class="small nl-note">When you subscribe, you'll get {CONSENT_SCOPE} You can unsubscribe at any time. We'll email you to confirm first. See our <a href="{pre}privacy/">privacy policy</a>.</p><p class="nl-msg" role="status" aria-live="polite"></p></form>"""
def signup_band(pre,uid):
    return f"""<section class='wrap narrow reveal'><div class='card nl-band'><span class='eyebrow'>Deadline reminders</span><h2 style='margin-top:0'>Get a nudge before <em>each deadline</em></h2><p>Deadline reminders and our newsletter, in plain English. Or add the dates straight to your calendar with our <a href='{pre}guides/deadline-calendar/'>free MTD deadline calendar</a>.</p>"""+nl_form(pre,uid)+"</div></section>"
def page(path,title,desc,body,faqs=None,extra_ld=None,eyebrow=None,draft=False,signup=None,notfound=False):
    # notfound: writes ROOT/404.html with root-absolute links (served at any depth), noindex, no canonical, kept out of the sitemap
    depth=path.count("/");pre="/" if notfound else "../"*depth
    url=f"{SITE}/{path}"
    lds=[{"@context":"https://schema.org","@graph":[ORG,{"@type":"WebSite","@id":SITE+"/#site","name":"MTD Finder","url":SITE+"/","publisher":{"@id":SITE+"/#org"}},{"@type":"WebPage","name":title,"url":url,"dateModified":PRIVACY_UPDATED if path=="privacy/" else UPDATED,"isPartOf":{"@id":SITE+"/#site"}}]}]
    if notfound:lds[0]["@graph"]=[n for n in lds[0]["@graph"] if n.get("@type")!="WebPage"]   # 404: no WebPage node, so no url claimed
    if path.startswith("guides/"):
        lds.append({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"url":url,"mainEntityOfPage":url,"inLanguage":"en-GB","dateModified":UPDATED,"author":{"@id":SITE+"/#org"},"publisher":{"@id":SITE+"/#org"},"isPartOf":{"@id":SITE+"/#site"}})
        lds.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Guides","item":SITE+"/guides/deadlines/"},{"@type":"ListItem","position":3,"name":title,"item":url}]})
        if signup is None:signup=True
    if signup:body+=signup_band(pre,path.strip("/").replace("/","-") or "home")
    if faqs:lds.append(faq_ld(faqs));body+=f"<section class='wrap narrow'><span class='eyebrow'>Questions</span><h2 style='margin-top:0'>Frequently asked</h2>{faq_html(faqs)}</section>"
    if extra_ld:lds.append(extra_ld)
    og_slug=OG_IMAGES.get(path,"default")
    og_img=f"{SITE}/assets/og/{og_slug}.png"
    og_alt=f"MTD Finder: {title}" if og_slug!="default" else OG_DEFAULT_ALT
    nav="".join(f'<li><a href="{pre}{h}"{" aria-current=page" if h==path else ""}>{t}</a></li>' for h,t in NAV)
    ld="".join(f'<script type="application/ld+json">{json.dumps(l,ensure_ascii=False)}</script>' for l in lds)
    doc=f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">{'' if notfound else f'<link rel="canonical" href="{url}">'}{'<meta name="robots" content="noindex">' if draft or notfound else ''}
<meta property="og:type" content="website"><meta property="og:site_name" content="MTD Finder"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">{'' if notfound else f'<meta property="og:url" content="{url}">'}<meta property="og:locale" content="en_GB"><meta property="og:image" content="{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="627"><meta property="og:image:alt" content="{html.escape(og_alt)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#f6f5f1"><link rel="icon" href="{pre}assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="{pre}assets/mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,300..600;1,7..72,300..600&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/style.css">{ld}</head><body>
<a href="#main" class="skip">Skip to content</a>
<header class="site"><div class="wrap nav"><a class="brand" href="{pre or './'}">{MARK_SVG}<span>MTD <em>Finder</em></span></a><button class="menu-btn" aria-expanded="false" aria-label="Menu">Menu</button><ul>{nav}</ul></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="cols"><div><a class="brand" href="{pre or './'}">MTD <em>Finder</em></a><p>An independent guide to Making Tax Digital for Income Tax software, for UK sole traders and landlords. Not affiliated with HMRC. Not tax advice. Run by Matthew Snow trading as Sno Automations.</p><p>Owner: Matthew Snow trading as Sno Automations · <a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Software data from <a href="{TOOL}" rel="noopener">HMRC's software finder</a>, last checked {data['last_checked']}.</p></div>
<ul><li><a href="{pre}finder/">Software finder</a></li><li><a href="{pre}guides/deadlines/">Deadlines</a></li><li><a href="{pre}guides/landlords/">Landlords</a></li><li><a href="{pre}guides/tradespeople/">Tradespeople</a></li><li><a href="{pre}guides/bridging-software/">Bridging software</a></li><li><a href="{pre}guides/deadline-calendar/">Deadline calendar</a></li><li><a href="{pre}guides/7-november-deadline/">7 November deadline</a></li><li><a href="{pre}guides/30k-threshold-april-2027/">£30k from April 2027</a></li><li><a href="{pre}acsp/">Find an ACSP</a></li><li><a href="{pre}faq/">FAQ</a></li></ul>
<ul><li><a href="{pre}about/">About</a></li><li><a href="{pre}sponsor/">Sponsor us</a></li><li><a href="{pre}newsletter/">Newsletter</a></li><li><a href="{pre}privacy/">Privacy</a></li><li><a href="{pre}disclaimer/">Disclaimer</a></li><li><a href="{pre}terms/">Terms</a></li><li><a href="{PORTAL}">Manage sponsorship</a></li></ul></div></div></footer>
<script src="{pre}assets/site.js" defer></script>{GOATCOUNTER}</body></html>"""
    if notfound:open(os.path.join(ROOT,"404.html"),"w").write(ext_links(doc));return
    d=os.path.join(ROOT,path);os.makedirs(d,exist_ok=True);open(os.path.join(d,"index.html"),"w").write(ext_links(doc))
    if not draft:pages.append(path)

def hero(eb,h1,lede,answer=None,btns=""):
    a=f"<div class='answer'><strong>Short answer:</strong> {answer[0].upper()+answer[1:]}</div>" if answer else ""
    return f"<section class='hero wrap'><div class='narrow'><span class='eyebrow'>{eb}</span><h1>{h1}</h1><p class='lede'>{lede}</p>{a}{btns}</div></section>"
def prose(s):return f"<section class='wrap narrow prose reveal'>{s}</section>"

THRESH=f"""<table><thead><tr><th>Qualifying income over</th><th>In tax year</th><th>Use MTD from</th></tr></thead><tbody>
<tr><td>£50,000</td><td>2024 to 2025</td><td>6 April 2026</td></tr><tr><td>£30,000</td><td>2025 to 2026</td><td>6 April 2027</td></tr><tr><td>£20,000</td><td>2026 to 2027</td><td>6 April 2028</td></tr></tbody></table><p class="small">Source: <a href="{ELIG}" rel="noopener">HMRC, Find out if and when you need to use Making Tax Digital for Income Tax</a>.</p>"""
# Checker help lines (meaning checked against HMRC's qualifying income guidance, QI)
SE_HELP="Your total sales or takings before expenses (turnover), not your profit."
PR_HELP="Your share of rent and other property income before expenses. If you own a property jointly, only count your share of the income (for example, half if you split it equally). If you're only told your share after expenses, use that figure."
SE_SHORT="Turnover, not profit."
PR_SHORT="Your share, before expenses."
yrs=[("2024 to 2025","£50k test"),("2025 to 2026","£30k test"),("2026 to 2027","£20k test")]
# --- Checker lead magnet: deadline reminder sign-up shown under the checker result ---
# Kit custom fields the form sends. They must exist in Kit before this goes live (Matthew to create them,
# see mtdfinder-plans/lead-magnet-draft.md). Kit makes the key from the label: "MTD segment" -> mtd_segment.
KIT_SEGMENT_FIELD="mtd_segment"
KIT_RESULT_FIELD="mtd_checker_result"
SEGMENTS=[("sole_trader","Sole trader"),("landlord","Landlord"),("both","Both"),("agent","Accountant or bookkeeper"),("","Prefer not to say")]   # "" = nothing sent to Kit
import datetime as _dt
# Next quarterly update deadline, worked out at build time. site.js repeats the same sum in the browser,
# so the page stays right between builds. Only this date moves on its own; everything else is reviewed by hand.
_DL=[(8,"6 April to 5 July"),(11,"6 April to 5 October"),(2,"6 April to 5 January"),(5,"6 April to 5 April (the whole tax year)")]
_MON={2:("Feb","February"),5:("May","May"),8:("Aug","August"),11:("Nov","November")}
def next_deadline(today=None):
    t=today or _dt.date.today()
    c=sorted(_dt.date(y,m,7) for y in (t.year,t.year+1) for m,_ in _DL)
    d=next(x for x in c if x>=t);per=dict(_DL)[d.month];sh,lo=_MON[d.month]
    # "full" is shown in bold, so it never breaks across lines. "href": the 7 November guide while that's next, otherwise the deadline calendar.
    return {"short":f"7 {sh} {d.year}","long":f"7&nbsp;{lo}","full":f"7&nbsp;{lo}&nbsp;{d.year}","period":per,"card":f"7 {sh}",
            "href":"guides/7-november-deadline/" if d.month==11 else "guides/deadline-calendar/","date":d}
NDL=next_deadline()
LEAD_REVIEW_FROM=_dt.date(2027,3,1)
if _dt.date.today()>=LEAD_REVIEW_FROM:
    print(f"WARNING: checker lead copy review due (from {LEAD_REVIEW_FROM}). The 'from 6 April 2027' copy ('you don't need to send quarterly updates yet') and any penalty wording change after the 2026 to 2027 tax year. Review LEAD in tools/build.py, then move LEAD_REVIEW_FROM on.")
def _dl(k):return f'<span data-dl="{k}">{NDL[k]}</span>'
def _src(url,label="HMRC"):return f'<a href="{url}" rel="noopener">{label}</a>'
# outcome -> (eyebrow, heading, paragraph). site.js picks one from the checker result. "blank" is the default before any figures go in.
LEAD={
 "blank":("Deadline reminders","Get a reminder before your MTD deadlines",
  "Put your figures in above to see when you start. Either way, we can email you before each deadline that applies to you."),
 "from_apr_2026":("<span>Next deadline: "+_dl("short")+"</span>",   # wrapped: .eyebrow is flex, so a bare inner span would get a gap
 "Get a reminder before "+_dl("long"),
  f"If you're already using MTD, your next quarterly update covers {_dl('period')} and is due by <strong>{_dl('full')}</strong> ({_src(QU)}). If you haven't signed up yet, you still can ({_src(ELIG)}). We'll email you in the week before each deadline."),
 "from_apr_2027":("You start: 6 April 2027","We'll remind you before your first deadline",
  f"You don't need to send quarterly updates yet. Your first one will be due by <strong>7&nbsp;August&nbsp;2027</strong> ({_src(QU)}). Before then, your 2025 to 2026 online tax return is due by 31 January 2027 ({_src(SADL,'GOV.UK')}). We'll email you in good time before you start, and before each deadline after that."),
 "from_apr_2028":("You start: 6 April 2028","We'll remind you before you need to start",
  f"On these figures you won't need MTD until <strong>6 April 2028</strong> ({_src(ELIG)}), so you don't need to send quarterly updates yet. We'll email you before you need to start, and let you know if the rules or dates change."),
 "under_threshold":("Not on these figures","Stay in the loop",
  f"You're not over any announced threshold on these figures. HMRC checks each year, so it's worth checking again if your income grows ({_src(ELIG)}). We'll email you if the thresholds or dates change."),
 "not_self_assessment":("Probably not yet","Stay in the loop",
  f"MTD for Income Tax is for sole traders and landlords registered for Self Assessment ({_src(ELIG)}). If that changes, or you look after clients who are affected, we'll keep you up to date."),
}
PEN="https://www.gov.uk/guidance/penalties-for-making-tax-digital-for-income-tax"
# Why-now line shown inside the checker result (site.js copies template "why-<outcome>").
# Penalty clause: 2026 to 2027 updates (deadlines up to 7 May 2027) get no points; later ones do. site.js shows the
# right one from the next deadline, so the line doesn't go stale. Sources: QU, SIGN, PEN.
_PEN_SWITCH=_dt.date(2027,5,7)
def _pen(k):
    hide=(NDL["date"]>_PEN_SWITCH)==(k=="pre")
    return f'<span data-pen="{k}"{" hidden" if hide else ""}>'
WHY={
 "from_apr_2026":f"<strong>Why act now:</strong> your next quarterly update covers {_dl('period')} and is due by <strong>{_dl('full')}</strong> ({_src(QU)}). You need to be signed up and have compatible software to send it ({_src(SIGN,'HMRC: sign up')}). "
   +_pen("pre")+f"HMRC won't give penalty points for late quarterly updates in 2026 to 2027, but you must send them before you can submit your tax return ({_src(QU)}).</span>"
   +_pen("post")+f"Each late quarterly update now gets a penalty point, and 4 points means a £200 penalty ({_src(PEN)}).</span>",
 "from_apr_2027":f"<strong>No rush, but don't leave it late:</strong> use the time before 6 April 2027 to choose software. HMRC says to check the software meets your needs before you sign up ({_src(SIGN,'HMRC: sign up')}).",
 "from_apr_2028":f"<strong>Nothing to do yet.</strong> We can remind you nearer the time, and tell you if the dates change.",
 "under_threshold":"<strong>Nothing to do on these figures.</strong> Check again after each tax return if your income grows.",
 "not_self_assessment":"",
}
WHY_CTA="Get a reminder before each deadline ↓"
# One consent scope for every box on the same Kit list. If it changes, log it in mtdfinder-plans/consent-log.md.
CONSENT_SCOPE="MTD deadline reminders and the MTD Finder newsletter. That's usually one or two short emails before each quarterly deadline (there are four a year), plus the odd update when HMRC changes something."
CONSENT_TEXT="Yes, email me "+CONSENT_SCOPE+" I can unsubscribe at any time."
def lead_signup(pre):
    e,h,p=LEAD["blank"]
    tpl="".join(f'<template id="why-{k}"><p class="why-now">{w}</p><p class="why-cta"><a class="btn" href="#lead" data-lead-jump>{WHY_CTA}</a></p></template>' for k,w in WHY.items() if w)
    tpl+="".join(f'<template id="lead-{k}"><span class="eyebrow">{a}</span><h3>{b}</h3><p class="small">{c}</p></template>' for k,(a,b,c) in LEAD.items())
    radios="".join(f'<label class="chk"><input type="radio" name="fields[{KIT_SEGMENT_FIELD}]" value="{v}"> {t}</label>' for v,t in SEGMENTS)
    return f"""<div class="after-check lead" id="lead"><div id="lead-copy"><span class="eyebrow">{e}</span><h3>{h}</h3><p class="small">{p}</p></div>{tpl}
<form class="nl lead-form" action="{KIT_FORM}" method="post" data-result-field="fields[{KIT_RESULT_FIELD}]">
<div class="lead-grid"><div class="field"><label for="lead-email">Email address</label><input id="lead-email" type="email" name="email_address" required autocomplete="email" placeholder="you@example.co.uk" aria-describedby="lead-msg"></div>
<fieldset class="seg"><legend>Which best describes you? <span class="small">(optional)</span></legend><div class="seg-opts">{radios}</div></fieldset></div>
<input type="hidden" name="fields[{KIT_RESULT_FIELD}]" value="">
<div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="consent"><input type="checkbox" id="lead-consent" name="consent" value="yes" required aria-describedby="lead-msg"><label for="lead-consent">{CONSENT_TEXT}</label></div>
<div class="lead-send"><button class="btn" type="submit">Remind me</button><p class="small nl-note">We'll email you to confirm first. See our <a href="{pre}privacy/">privacy policy</a>. Not tax advice. Prefer your calendar? <a href="{pre}guides/deadline-calendar/">Get the deadline calendar</a>.</p></div>
<p class="nl-msg" id="lead-msg" role="status" aria-live="polite"></p></form></div>"""
fields="".join(f"<fieldset><legend>{y} <span class='small'>({t})</span></legend><div class='row2'><div><label for='se{i}'>Self-employment turnover (£)</label><input id='se{i}' type='number' inputmode='decimal' min='0' step='100' placeholder='0' aria-describedby='se{i}-help'><p class='small' id='se{i}-help' style='margin:6px 0 0'>{SE_HELP if i==0 else SE_SHORT}</p></div><div><label for='pr{i}'>Property income, your share (£)</label><input id='pr{i}' type='number' inputmode='decimal' min='0' step='100' placeholder='0' aria-describedby='pr{i}-help'><p class='small' id='pr{i}-help' style='margin:6px 0 0'>{PR_HELP if i==0 else PR_SHORT}</p></div></div></fieldset>" for i,(y,t) in enumerate(yrs))
home_faq=[("Who needs to use Making Tax Digital for Income Tax?",f"Sole traders and landlords registered for Self Assessment whose qualifying income from self-employment and property is over the threshold for the relevant tax year. <a href='{ELIG}'>HMRC guidance</a>."),
("What counts as qualifying income?",f"Your total self-employment and property income before expenses (turnover). Employment (PAYE) income, dividends, pensions and your share of partnership profit do not count. <a href='{QI}'>HMRC guidance</a>."),
("Does HMRC recommend any MTD software?",f"No. HMRC says all listed software has been through its recognition process, but it does not recommend any product. <a href='{SW}'>HMRC guidance</a>."),
("Do I still need to file a Self Assessment return?",f"Yes. You still submit a Self Assessment return for the tax year before you start using MTD, and once you are using MTD you submit your tax return through your software by 31 January following the tax year. <a href='{ELIG}'>HMRC</a>, <a href='{SW}'>HMRC software guidance</a>.")]
page("","MTD Finder: Do I need Making Tax Digital, and which software?","Free Making Tax Digital for Income Tax checker and independent finder for all "+str(N)+" HMRC-recognised MTD software products for UK sole traders and landlords.",
hero("Making Tax Digital for Income Tax","Do I need MTD, <em>and when?</em>","An independent, plain-English guide for UK sole traders and landlords, with a finder covering every HMRC-recognised product.",
 f"if your self-employment and property income before expenses is over £50,000 (2024 to 2025), you should have started MTD from 6 April 2026. Over £30,000 in 2025 to 2026 means 6 April 2027, and over £20,000 in 2026 to 2027 means 6 April 2028. <a href='{ELIG}' rel='noopener'>Source: HMRC</a>.",
 "<div class='btns'><a class='btn' href='#checker'>Check in 30 seconds</a><a class='btn ghost' href='finder/'>Browse "+str(N)+" products</a></div><div class='trust'><span>Every claim linked to HMRC</span><span>Independent</span><span>Free to use</span></div>")+
f"""<section class="wrap" id="checker"><div class="calc reveal"><form id="calc" novalidate><span class="eyebrow">MTD checker</span><h2 style="margin-top:0">Making Tax Digital qualifying income checker</h2><p class="small">"Qualifying income is your total income from self-employment and property. This is the amount before expenses (also known as turnover), based on the tax return you submitted in the previous tax year." <a href="{QI}" rel="noopener">HMRC guidance</a>. Enter the figures from your Self Assessment returns, and leave years blank if you don't know them yet.</p>
<div class="field"><label><input type="checkbox" id="sa" checked> I'm a sole trader or landlord registered for Self Assessment</label></div>{fields}
<p class="small">Don't include wages (PAYE), dividends, pensions or partnership profit shares. They don't count towards <a href="{QI}" rel="noopener">qualifying income</a>.</p></form>
<div class="result" id="calc-out" aria-live="polite"></div>
{lead_signup('')}</div></section>
<section class="wrap narrow reveal"><h2>The thresholds</h2>{THRESH}</section>
<section class="wrap reveal explore"><h2>Explore</h2><div class="grid">
<a class="card" href="finder/"><span class="num">{N}</span><h3>Software finder</h3><p class="small">Filter HMRC-recognised products by income type, bridging or bookkeeping, free version, VAT and CIS.</p></a>
<a class="card" href="guides/deadlines/"><span class="num">4×</span><h3>Quarterly deadlines</h3><p class="small">7 August, 7 November, 7 February and 7 May, explained.</p></a>
<a class="card" href="{NDL['href']}" data-dl-href><span class="num">{_dl('card')}</span><h3>Next deadline</h3><p class="small">What to send by {_dl('long')}, and what happens if you're late.</p></a>
<a class="card" href="guides/tradespeople/"><span class="num">CIS</span><h3>For tradespeople</h3><p class="small">Electricians, plumbers, builders and solar installers.</p></a></div></section>
<section class="wrap narrow reveal"><div class="card nl-band"><span class="eyebrow">Newsletter</span><h2 style="margin-top:0">Never miss an <em>MTD deadline</em></h2>"""+nl_form("","home")+"""</div></section>""",faqs=home_faq)

page("finder/","MTD Software Finder: compare all "+str(N)+" HMRC-recognised products","Filter every HMRC-recognised Making Tax Digital for Income Tax product by sole trader or landlord, bridging or bookkeeping, free version, VAT, CIS and HMRC Assist.",
hero("Software finder","Find your <em>MTD software</em>","Every product listed in HMRC's software finder, with filters that match how you actually work.",
 f"pick software that supports all your income sources, sends quarterly updates and submits your tax return. All {N} products here are on <a href='{TOOL}' rel='noopener'>HMRC's list</a>; HMRC doesn't recommend any of them.")+
f"""<section class="wrap"><div class="searchbar"><div><label for="q">Search {N} products</label><input id="q" type="search" placeholder="Name, e.g. Xero, FreeAgent, spreadsheet" autocomplete="off"></div><button class="btn ghost filter-toggle" aria-expanded="false" aria-controls="side">Filters</button></div>
<div class="finder"><aside class="side" id="side" aria-label="Filters"><h2>Filter</h2>
<div class="grp"><label for="who">I am a</label><select id="who"><option value="any">Any</option><option value="st">Sole trader</option><option value="ll">Landlord</option><option value="both">Both</option></select></div>
<div class="grp"><label for="type">Software type</label><select id="type"><option value="any">Any</option><option value="records">Full bookkeeping (creates records)</option><option value="bridging">Bridging (connects spreadsheets)</option></select></div>
<div class="grp ready-grp"><label class="chk"><input type="checkbox" data-k="tax" aria-describedby="ready-help"> Quarterly updates and tax return (ready now, per HMRC)</label><p class="small" id="ready-help" style="margin:6px 0 0">Software HMRC lists as able to send both your quarterly updates and your tax return. HMRC's own status, last checked {LC_TEXT}. Check it covers all your income types (<a href="{SW}" rel="noopener">GOV.UK: choose the right software</a>).</p></div>
<div class="grp" role="group" aria-label="Features"><label>Features</label>
<label class="chk"><input type="checkbox" data-k="free"> Free version</label><label class="chk"><input type="checkbox" data-k="vat"> MTD for VAT</label><label class="chk"><input type="checkbox" data-k="cis"> CIS ready</label><label class="chk"><input type="checkbox" data-k="assist"> HMRC Assist</label><label class="chk"><input type="checkbox" data-k="welsh"> Welsh language</label></div>
<div class="grp"><button class="linkbtn" id="clear" type="button">Clear all filters</button></div>
<p class="small">Price band and mobile app filters are coming: HMRC's data doesn't include them yet.</p></aside>
<div><div class="resbar"><p class="small" style="margin:0" aria-live="polite"><strong id="count">…</strong> of <span id="count-total">{N}</span> products · alphabetical, never paid</p><p class="small" style="margin:0" id="year-end">{YEAR_END}.</p><p class="small" style="margin:0">Data: <a href="{TOOL}" rel="noopener">HMRC</a>, checked {data['last_checked']}</p></div>
<div class="grid"><article class="card featured"><span class="badge">Featured · Sponsored</span><h3>Your software here</h3><p class="small">One clearly labelled placement for an HMRC-recognised product. It never changes the order of the main list.</p><div><a class="btn" href="../sponsor/">Sponsor us</a></div></article></div>
<div class="grid" id="list" data-src="../data/products.json" style="margin-top:18px"></div></div></div></section>
<div class="tray" id="tray" aria-live="polite"><span id="tray-n">0 selected</span><button class="btn" id="cmp-open" type="button">Compare</button></div>
<dialog id="cmp"><div class="in"><div style="display:flex;justify-content:space-between;align-items:center"><h2 style="margin:0">Compare</h2><button class="btn ghost" id="cmp-close" type="button">Close</button></div><div id="cmp-body" style="overflow:auto;margin-top:18px"></div></div></dialog>""",extra_ld=ITEMS)

page("guides/deadlines/","MTD for Income Tax deadlines and quarterly update dates (2026)","Making Tax Digital for Income Tax start dates and quarterly update deadlines: 7 August, 7 November, 7 February and 7 May, plus the 31 January tax return.",
hero("Guide","MTD deadlines and <em>quarterly dates</em>","When you start, and when each update is due.",f"quarterly updates are due by 7 August, 7 November, 7 February and 7 May. Your tax return is due by 31 January after the tax year. <a href='{QU}' rel='noopener'>Source: HMRC</a>.")+
prose(f"""<h2>When you start</h2>{THRESH}<p class="notice">Next deadline: <a href="../7-november-deadline/">7 November 2026, what to send and what happens if you're late</a>.</p><h2>Quarterly update deadlines</h2><table><thead><tr><th>Standard update period</th><th>Deadline</th></tr></thead><tbody><tr><td>6 April to 5 July</td><td>7 August</td></tr><tr><td>6 April to 5 October</td><td>7 November</td></tr><tr><td>6 April to 5 January</td><td>7 February</td></tr><tr><td>6 April to 5 April</td><td>7 May (the following tax year)</td></tr></tbody></table>
<p>If your accounting period runs 1 April to 31 March, HMRC suggests you consider <strong>calendar update periods</strong>, which end on the last day of the month. The deadline to send each update is the same either way. You select calendar periods in your software before your first update. <a href="{QU}" rel="noopener">HMRC: send quarterly updates</a>.</p>
<p>Quarterly updates are summaries of your income and expenses. They are not tax returns. <a href="{SW}" rel="noopener">HMRC</a>.</p><h2>Your tax return</h2><p>You add any other income and submit your tax return through your software by 31 January the following year. <a href="{TR}" rel="noopener">HMRC: submit your tax return</a>.</p>"""),
faqs=[("When is the first MTD quarterly update due?",f"For the period 6 April to 5 July, the deadline is 7 August. <a href='{QU}'>HMRC</a>."),("Is a quarterly update a tax return?",f"No. HMRC describes quarterly updates as summaries of your self-employment and property income and expenses, not tax returns. <a href='{SW}'>HMRC</a>."),("Can I use calendar quarters?",f"Yes. If your accounting period covers 1 April to 31 March you can choose calendar update periods in your software; deadlines stay the same. <a href='{QU}'>HMRC</a>.")])

page("guides/landlords/","Making Tax Digital for landlords: thresholds, joint property and software","How MTD for Income Tax works for UK landlords: gross rental income thresholds, jointly owned property, foreign property and choosing landlord software.",
hero("Guide","MTD for <em>landlords</em>","What counts, how joint ownership works, and which software fits.",f"if your gross property income (plus any self-employment income) is over the threshold, you need MTD. For a jointly owned property, only your share counts. <a href='{QI}' rel='noopener'>Source: HMRC</a>.")+
prose(f"""<h2>Rental income is measured before expenses</h2><p>Qualifying income is your total self-employment and property income <em>before expenses</em>. HMRC's own example: £25,000 rental income plus £27,000 self-employment income gives qualifying income of £52,000. <a href="{QI}" rel="noopener">HMRC</a>.</p>
<h2>Jointly owned property</h2><p>Your share counts. HMRC's example: a property generating £50,000 shared equally with a sibling gives you qualifying income of £25,000. If you only get notice of your share after expenses, HMRC uses that figure. <a href="{QI}" rel="noopener">HMRC</a>.</p>
<h2>Foreign property</h2><p>If you were UK tax resident, foreign property income counts too. <a href="{QI}" rel="noopener">HMRC</a>. Filter the <a href="../../finder/">finder</a> for landlord products, and check foreign property support on each HMRC listing.</p>
<h2>One product per submission</h2><p>You can use more than one product, but not more than one to send quarterly updates for the same property income. <a href="{SW}" rel="noopener">HMRC</a>.</p><p><a class="btn" href="../../finder/">See landlord software</a></p>"""),
faqs=[("Do landlords need Making Tax Digital?",f"Yes, if you're registered for Self Assessment and your qualifying income from property and self-employment is over the threshold. <a href='{ELIG}'>HMRC</a>."),("Does my partner's half of a rental count?",f"No. Only your share of jointly owned property income counts towards your qualifying income. <a href='{QI}'>HMRC</a>."),("Do REIT dividends count?",f"No. Income from UK REITs or PAIFs does not count towards qualifying income. <a href='{QI}'>HMRC</a>.")])

cis=sum(p['cis'] for p in data['products'])
page("guides/tradespeople/","Making Tax Digital for tradespeople: electricians, plumbers and solar installers","MTD for Income Tax for self-employed electricians, plumbers, builders and solar installers: turnover thresholds, CIS and choosing software that fits trade work.",
hero("Guide","MTD for <em>tradespeople</em>","For self-employed electricians, plumbers, builders, heating engineers and solar installers.",f"it's your turnover that counts, not your profit. A sole trader taking more than £30,000 in 2025 to 2026 will need MTD from 6 April 2027. <a href='{ELIG}' rel='noopener'>Source: HMRC</a>.")+
prose(f"""<h2>Why turnover matters for trades</h2><p>Qualifying income is measured before expenses. <a href="{QI}" rel="noopener">HMRC</a>. Trades that buy in a lot of materials, such as panels, batteries, boilers or cable, can cross the threshold even with modest profits, so check your gross figure.</p>
<h2>Construction Industry Scheme (CIS)</h2><p>HMRC's software listings show whether each product supports the Construction Industry Scheme for your tax return. {cis} of the {N} products show CIS as ready now. Use the <strong>CIS ready</strong> filter in the <a href="../../finder/">finder</a>.</p>
<h2>VAT-registered trades</h2><p>If you're VAT registered, HMRC says you should check whether your VAT software also works with MTD for Income Tax, or that your new software meets your VAT needs. <a href="{SW}" rel="noopener">HMRC</a>.</p>
<h2>Electricians, plumbers and solar installers</h2><p>For most one-person trade businesses, full bookkeeping software that links to your bank and lets you photograph receipts on site is the simplest route. If you already keep good spreadsheets, <a href="../bridging-software/">bridging software</a> can be cheaper. Either way, filter for <strong>Sole trader</strong>, <strong>Quarterly updates and tax return (ready now, per HMRC)</strong> and <strong>CIS ready</strong> if you do subcontract work.</p><p><a class="btn" href="../../finder/">Find trade-friendly software</a></p>"""),
faqs=[("I'm an electrician earning £35k turnover but £18k profit. Do I need MTD?",f"Very likely, from 6 April 2027 if that £35,000 turnover was in 2025 to 2026, because the threshold uses income before expenses. <a href='{QI}'>HMRC</a>. Check your own figures with <a href='{ELIG}'>HMRC's tool</a>."),("Does wage income from a part-time job count?",f"No. Employment (PAYE) income doesn't count towards qualifying income. <a href='{QI}'>HMRC</a>."),("Which MTD software supports CIS?",f"HMRC's listing shows CIS support for each product. {cis} products currently show it as ready now. See our finder.")])

page("guides/bridging-software/","MTD bridging software explained: keep your spreadsheet","What MTD bridging software is, how it connects spreadsheets to HMRC, and when it's a better choice than full bookkeeping software.",
hero("Guide","Bridging software, <em>explained</em>","Keep your spreadsheet and let a small tool do the HMRC bit.",f"bridging software connects to records you already keep, such as spreadsheets, and makes your MTD submissions to HMRC. <a href='{SW}' rel='noopener'>Source: HMRC</a>.")+
prose(f"""<h2>Two types of MTD software</h2><p>HMRC describes two types: software that <strong>creates digital records</strong> (bank feeds, receipt scanning or manual entry) and software that <strong>connects to your records</strong>, sometimes called bridging software. <a href="{SW}" rel="noopener">HMRC</a>.</p>
<h2>Does bridging software file my tax return?</h2><p>Some do. HMRC notes that some bridging products let you both send quarterly updates and submit your tax return. <a href="{SW}" rel="noopener">HMRC</a>. Use the <strong>Bridging</strong> software type and the <strong>Quarterly updates and tax return (ready now, per HMRC)</strong> filter in the <a href="../../finder/">finder</a>.</p>
<h2>When it suits you</h2><ul><li>You're comfortable keeping a tidy spreadsheet.</li><li>You have simple income and few transactions.</li><li>You want to keep costs low. HMRC notes free products exist for simple affairs, but they may have limits. <a href="{SW}" rel="noopener">HMRC</a>.</li></ul><p><a class="btn" href="../../finder/">See bridging products</a></p>"""),
faqs=[("Can I keep using Excel for MTD?",f"Yes, with bridging software that connects your spreadsheet to HMRC. <a href='{SW}'>HMRC</a>."),("Can I use two products?",f"Yes, but only one product for each separate submission, so make sure they work together. <a href='{SW}'>HMRC</a>.")])

faqs_all=home_faq+[("When do I need to start MTD?",f"From 6 April 2026 if over £50,000 in 2024 to 2025; 6 April 2027 if over £30,000 in 2025 to 2026; 6 April 2028 if over £20,000 in 2026 to 2027. <a href='{ELIG}'>HMRC</a>. Over £30,000? See our <a href='../guides/30k-threshold-april-2027/'>April 2027 checklist</a>."),
("What if I didn't get a letter from HMRC?",f"It's still your responsibility to check if and when you need MTD and to sign up. <a href='{ELIG}'>HMRC</a>."),
("Can I stop using MTD if my income falls?",f"Once you've started, if your qualifying income drops below the threshold for 3 tax years in a row, you can choose to opt out. <a href='{QI}'>HMRC</a>."),
("What if I've only traded for part of a year?",f"For sole traders, HMRC annualises qualifying income where it has the information. For example, 6 months' trading is doubled. Landlords must annualise property income themselves. <a href='{QI}'>HMRC</a>."),
("Are partnerships included?",f"Not yet. HMRC says partnerships will need to use MTD in future, with a timeline to be set out later. <a href='{ELIG}'>HMRC</a>."),
("Can I be exempt?",f"Some people are, for example if digitally excluded. Exempt people still file a Self Assessment return. <a href='{ELIG}'>HMRC</a>."),
("How do I sign up?",f"You must be registered for Self Assessment and have submitted a return in the last 2 years. Choose software first, then <a href='{SIGN}'>sign up with HMRC</a>.")]
page("faq/","Making Tax Digital for Income Tax FAQ: plain answers with HMRC sources","Plain-English answers to common Making Tax Digital for Income Tax questions, from thresholds and qualifying income to exemptions and sign-up, each linked to HMRC.",
hero("FAQ","MTD questions, <em>answered</em>","Short answers first, each linked to the HMRC source."),faqs=faqs_all)

page("sponsor/","Sponsor MTD Finder: reach UK sole traders and landlords choosing MTD software","Sponsor MTD Finder to reach UK sole traders and landlords comparing Making Tax Digital for Income Tax software. Featured placements from £49 a month.",
hero("For software vendors","Sponsor <em>MTD Finder</em>","Put your HMRC-recognised product in front of sole traders and landlords at the moment they're choosing.")+
f"""<section class="wrap"><div class="grid two"><div class="card featured reveal"><span class="badge">Featured listing</span><div class="stat">£49<span style="font-size:1.1rem">/month</span></div><p>Introductory price. One clearly labelled featured slot on the software finder, plus a mention in the newsletter.</p><p class="small">Prices in GBP.</p><div class="btns" style="justify-content:flex-start"><a class="btn" href="{STRIPE}" rel="noopener">Become a sponsor, £49/month</a></div><p class="small" style="margin-top:12px">Billed monthly · cancel anytime. See the <a href="../terms/#sponsorship">sponsorship terms</a>.</p><p class="small">Already a sponsor? <a href="{PORTAL}">Manage your sponsorship</a></p><p class="small">Questions first? <a href="mailto:{SPONSOR_EMAIL}?subject=MTD%20Finder%20sponsorship">{SPONSOR_EMAIL}</a></p></div>
<div class="card reveal"><h3>Our rules</h3><ul class="small"><li>Only HMRC-recognised products.</li><li>Sponsored placements are always labelled.</li><li>Sponsorship never changes the main list order or our editorial content.</li><li>We may earn affiliate commission; we always disclose it.</li></ul></div></div></section>""")

page("newsletter/","MTD Finder newsletter: deadline reminders for sole traders and landlords","Sign up for MTD Finder's free newsletter: plain-English Making Tax Digital deadline reminders and software updates for UK sole traders and landlords.",
hero("Newsletter","Deadline reminders, <em>in plain English</em>","Short reminders before each quarterly deadline, plus the MTD Finder newsletter when HMRC changes something. Free, no spam.")+
f"""<section class="wrap narrow"><div class="card nl-band"><p class="notice nl-thanks" hidden>Nearly there. Check your inbox for a confirmation email from MTD Finder and click the link inside.</p><p class="notice nl-confirmed" hidden>Thanks, you're subscribed. Your first reminder will arrive before the next deadline.</p>"""+nl_form("../","page")+f"""<p class="small">Emails come from {NEWS_EMAIL}. Sign-ups are handled by Kit, our email provider.</p></div></section>""")

page("about/","About MTD Finder: independent, run by Sno Automations","MTD Finder is an independent guide to Making Tax Digital for Income Tax software, run by Matthew Snow trading as Sno Automations, a UK sole trader.",
hero("About","Built by a sole trader, <em>for sole traders</em>","MTD Finder is run by Matthew Snow trading as Sno Automations, a UK sole trader.")+
prose(f"""<p>We built MTD Finder because HMRC's official list is accurate but hard to browse, and many \"best MTD software\" articles are written by vendors ranking their own products.</p><h2>How we work</h2><ul><li>Every tax claim links to HMRC or GOV.UK.</li><li>Software data comes from <a href="{TOOL}" rel="noopener">HMRC's software finder</a> and is rechecked regularly. Last checked: {data['last_checked']}.</li><li>The main list is alphabetical. Sponsored slots are labelled.</li><li>We're independent and not affiliated with HMRC.</li></ul><p>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>. Sponsorship: <a href="mailto:{SPONSOR_EMAIL}">{SPONSOR_EMAIL}</a>.</p>"""))

page("privacy/","Privacy policy | MTD Finder","How MTD Finder, run by Matthew Snow trading as Sno Automations, handles personal data under UK GDPR.",
hero("Legal","Privacy policy","Last updated "+PRIVACY_UPDATED+".")+
prose(f"""<h2>Who we are</h2><p>MTD Finder (mtdfinder.co.uk) is run by Matthew Snow trading as Sno Automations, a sole trader based in the UK. For the purposes of UK data protection law (the UK GDPR and the Data Protection Act 2018), Matthew Snow is the data controller. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>. Matthew Snow is registered with the Information Commissioner's Office (ICO), registration number {ICO_REG}. You can check this on the <a href="https://ico.org.uk/ESDWebPages/Search" rel="noopener">ICO register</a>.</p>
<h2>Browsing the site</h2><p>We don't use advertising or tracking cookies, and this site sets no cookies of its own. The MTD checker runs entirely in your browser: the figures you type are never sent to us or stored. If you then sign up for reminders, only the result category is sent with your sign-up (see below).</p>
<p>The site is hosted by GitHub Pages (GitHub, Inc.). When you visit, GitHub processes technical information such as your IP address to deliver and secure the site, and may log it. Fonts are loaded from Google Fonts (Google LLC), so your browser connects to Google's servers, which receive your IP address. These providers may process data outside the UK under their own safeguards. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a> and <a href="https://policies.google.com/privacy">Google's privacy policy</a>. Our lawful basis is legitimate interests in running a secure, working website.</p>
<h2>Visitor statistics</h2><p>We use GoatCounter to count visits. It sets no cookies and doesn't store IP addresses or build profiles of visitors. It tells us totals such as which pages are read and which sites sent visitors. GoatCounter is run from Ireland and stores its data in Finland and Germany. Our lawful basis is legitimate interests in understanding how the site is used. See <a href="https://www.goatcounter.com/help/privacy" target="_blank" rel="noopener">GoatCounter's privacy notes<span class="vh"> (opens in new tab)</span></a>.</p>
<h2>If you email us</h2><p>If you contact us, we use your email address and message to reply, on the basis of legitimate interests. Our email is provided by Google Workspace. We keep correspondence only as long as needed, normally no more than two years.</p>
<h2>Sponsors and payments</h2><p>If you buy a featured listing, payment is taken by Stripe, which collects your card details directly. We never see your full card number. We receive your name, business name, email, billing address and payment status, and use them to provide the listing, invoice and keep accounts (lawful basis: contract and legal obligation). Accounting records are kept for at least six years, as UK tax law requires. See <a href="https://stripe.com/gb/privacy">Stripe's privacy policy</a>.</p>
<h2>Newsletter and deadline reminders</h2><p>If you sign up to the newsletter or to deadline reminders, we use your email address (and your name, if you give it) to send them, on the basis of your consent. That means MTD deadline reminders, usually one or two short emails before each quarterly deadline, and the MTD Finder newsletter. We'll ask you to confirm your subscription by email first.</p>
<p>If you sign up from the checker, we also store two extra details with your email address: which describes you best (sole trader, landlord, both, or accountant or bookkeeper), if you choose one, and the checker's headline result, if you ran it (for example "starts 6 April 2027"). We never receive the figures you typed into the checker. We use these details only to send you the reminders and updates that fit your situation, for example so someone who starts in 2027 isn't sent a reminder for a deadline that doesn't apply to them yet. They're kept for as long as you're subscribed and deleted with your address when you unsubscribe.</p>
<p>Sign-ups and our mailing list are managed by Kit (ConvertKit LLC), a US-based email service that processes the data for us as our processor under its <a href="https://kit.com/dpa">data processing addendum</a>. Transfers of UK personal data to the US are protected by the UK Extension to the EU-US Data Privacy Framework and/or the UK International Data Transfer Addendum to the EU standard contractual clauses. Kit may record whether you open or click our emails. Every email has an unsubscribe link, and you can also email <a href="mailto:{EMAIL}">{EMAIL}</a> to unsubscribe. When you unsubscribe, we delete your address, or keep only a suppression record so we don't email you again. See <a href="https://kit.com/privacy">Kit's privacy policy</a>.</p>
<h2>Find an ACSP list</h2><p>Our <a href="../acsp/">Find an ACSP</a> page republishes Companies House's public list of Authorised Corporate Service Providers under the Open Government Licence. Some entries are sole practitioners, so their name and town are personal data. We use them on the basis of legitimate interests in helping people find an authorised agent, and we only show what Companies House already publishes, minus the full postcode (we show the area only). We remove anyone on Companies House's ceased or suspended list each time we update. If you're listed and want your entry corrected or removed, email <a href="mailto:{EMAIL}">{EMAIL}</a>. We'll remove it from our page, and you can also ask Companies House to change the official list.</p>
<h2>Business contacts we approach</h2><p>Now and then we email organisations and businesses (for example landlord and trade associations, bookkeeping bodies and software vendors) to offer free resources, check listing details or discuss sponsorship. We use only business contact details they publish themselves, such as a role inbox or contact form, on the basis of legitimate interests in telling relevant organisations about the site. We keep a record of who we contacted and when, and if you ask us not to contact you again, we add you to a suppression list and won't. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Your rights</h2><p>You can ask to access, correct, delete or restrict your data, object to processing, ask for a copy to take elsewhere, or withdraw consent at any time. Email <a href="mailto:{EMAIL}">{EMAIL}</a>; we'll reply within one month. You can also complain to the <a href="https://ico.org.uk/make-a-complaint/">Information Commissioner's Office</a>.</p>
<h2>Changes</h2><p>We'll update this page if anything changes, and show the date at the top.</p>"""))

page("terms/","Terms of use and sponsorship terms | MTD Finder","Website terms of use and featured listing sponsorship terms for MTD Finder, run by Matthew Snow trading as Sno Automations.",
hero("Legal","Terms","Last updated "+UPDATED+".")+
prose(f"""<h2>About these terms</h2><p>These terms apply to your use of mtdfinder.co.uk ("MTD Finder"), run by Matthew Snow trading as Sno Automations, a UK sole trader ("we", "us"). Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>. By using the site you accept these terms.</p>
<h2>Using the site</h2><p>MTD Finder is an independent information site. We're not affiliated with or endorsed by HMRC, and nothing here is tax, legal or financial advice. Software details come from HMRC's public listing and vendors, and can change, so always confirm with HMRC or the vendor before you rely on them. See our <a href="../disclaimer/">disclaimer</a>.</p><p>You may use and share the content for personal, non-commercial use with a link back. Please don't copy the site wholesale, scrape it in a way that harms it, or misuse it.</p>
<h2>Our liability</h2><p>We provide the site "as is" and don't guarantee it will be accurate, complete or always available. As far as the law allows, we aren't liable for any loss arising from your use of, or reliance on, the site or any third-party site we link to. Nothing in these terms limits liability for death or personal injury caused by negligence, for fraud, or for anything else that can't be limited by law.</p>
<h2 id="sponsorship">Sponsorship terms</h2><p>These apply to businesses that buy a featured listing.</p>
<h3>The listing</h3><p>A featured listing is one clearly labelled "Featured · Sponsored" slot on the software finder, plus a mention in the newsletter while it runs. Listings are only for products on HMRC's list of MTD for Income Tax software. We may edit listing text for accuracy, clarity and tone.</p>
<h3>Editorial independence</h3><p>Sponsorship never changes the order of the main list, our guides or our editorial judgement, and we always label paid placements. Sponsors don't get to review or approve our content.</p>
<h3>Price and billing</h3><p>The listing costs £49 a month (or any other price shown when you subscribe), billed monthly in advance through Stripe until you cancel. We don't currently charge VAT. If that changes, we'll give you at least 30 days' notice of any price change.</p>
<h3>Cancelling</h3><p>You can cancel anytime, or update your card and download invoices, through our <a href="{PORTAL}">sponsor billing portal</a> (log in with the email you subscribed with), or by emailing <a href="mailto:{SPONSOR_EMAIL}">{SPONSOR_EMAIL}</a>. Cancellation takes effect at the end of the billing period you've paid for, and your listing stays live until then. We don't refund partial months, except where the law requires it.</p>
<h3>Refusing or removing listings</h3><p>We may refuse any listing. We may also remove a listing if the product leaves HMRC's list, the information is misleading, or the listing breaks these terms or the law. If we remove a listing for any reason other than your breach, we'll refund the unused part of the current month.</p>
<h3>Liability for sponsors</h3><p>We don't guarantee any level of traffic, clicks or sales. As far as the law allows, our total liability to a sponsor is limited to the fees paid in the three months before the claim, and we're not liable for indirect loss or loss of profit.</p>
<h2>Changes and law</h2><p>We may update these terms and will show the date at the top. For sponsors, we'll give 30 days' notice of material changes. These terms are governed by the law of England and Wales, and the courts of England and Wales have jurisdiction.</p>"""))

page("disclaimer/","Disclaimer and affiliate disclosure | MTD Finder","MTD Finder is independent, is not affiliated with HMRC, does not give tax advice and may earn affiliate commission.",
hero("Legal","Disclaimer","Please read before relying on anything here.")+
prose(f"""<h2>Not tax advice</h2><p>MTD Finder gives general information only. It isn't tax, legal or financial advice. Always check <a href="{ELIG}" rel="noopener">HMRC guidance</a> or speak to a qualified adviser.</p><h2>Independent</h2><p>We're not affiliated with or endorsed by HMRC. HMRC doesn't recommend any software product.</p><h2>Accuracy</h2><p>Software details come from HMRC's public listing and vendors' sites, and can change. Always confirm features and prices with the vendor.</p><h2>Affiliate disclosure</h2><p>Some links may be affiliate links, so we may earn a commission at no extra cost to you. Featured placements are paid and always labelled. Neither changes the order of the main list.</p>"""))

# ---- Lead magnet: .ics deadline calendar + checklist
EVENTS=[("20261107","MTD quarterly update due (6 April to 5 October)","Send your cumulative quarterly update for each self-employment and property business. "+QU),
("20270131","Self Assessment deadline for 2025 to 2026","Online tax return and payment due for 2025 to 2026. "+SADL),
("20270207","MTD quarterly update due (6 April to 5 January)","Send your cumulative quarterly update. "+QU),
("20270406","MTD starts if over £30,000 in 2025 to 2026","If your qualifying income in 2025 to 2026 was over £30,000, you need MTD from today. "+ELIG),
("20270507","MTD final quarterly update due (6 April to 5 April)","Send your fourth quarterly update for 2026 to 2027. "+QU),
("20270807","MTD quarterly update due (6 April to 5 July)","First quarterly update of 2027 to 2028. "+QU)]
def _ics_esc(t):return t.replace("\\","\\\\").replace(",","\\,").replace(";","\\;")
def _fold(line):
    b=line.encode();out=[]
    while len(b)>73:
        cut=73
        while (b[cut]&0xC0)==0x80:cut-=1
        out.append(b[:cut].decode());b=b[cut:]
    out.append(b.decode());return "\r\n ".join(out)
def _next(d):
    import datetime as _d;return (_d.date(int(d[:4]),int(d[4:6]),int(d[6:]))+_d.timedelta(days=1)).strftime("%Y%m%d")
ics=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//MTD Finder//Deadline calendar//EN","CALSCALE:GREGORIAN","METHOD:PUBLISH","X-WR-CALNAME:MTD deadlines (MTD Finder)"]
for d,t,desc in EVENTS:
    ics+=["BEGIN:VEVENT",f"UID:{d}-mtd@mtdfinder.co.uk","DTSTAMP:20261015T000000Z",f"DTSTART;VALUE=DATE:{d}",f"DTEND;VALUE=DATE:{_next(d)}",_fold("SUMMARY:"+_ics_esc(t)),_fold("DESCRIPTION:"+_ics_esc(desc+" Not tax advice. mtdfinder.co.uk")),"TRANSP:TRANSPARENT",
          "BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:"+_ics_esc("MTD deadline in 7 days"),"TRIGGER:-P7D","END:VALARM","END:VEVENT"]
ics.append("END:VCALENDAR")
open(f"{ROOT}/{ICS}","w",newline="").write("\r\n".join(ics)+"\r\n")
def _d(d):
    import datetime as _x;return _x.date(int(d[:4]),int(d[4:6]),int(d[6:])).strftime("%-d %B %Y")
rows="".join(f"<tr><td>{_d(d)}</td><td>{t}</td></tr>" for d,t,_ in EVENTS)
page("guides/deadline-calendar/","MTD deadline calendar and checklist for 2026 to 2027","Free Making Tax Digital deadline calendar to add to Google, Apple or Outlook, plus a plain-English checklist for sole traders and landlords. Every date linked to HMRC.",
hero("Free download","MTD deadline <em>calendar</em> and checklist","Every Making Tax Digital date for the next year, in your own calendar, with a reminder a week before each one.",
 f"quarterly updates are due by 7 November, 7 February, 7 May and 7 August, and the 2025 to 2026 tax return by 31 January 2027. <a href='{QU}' rel='noopener'>Source: HMRC</a>.",
 f"<div class='btns'><a class='btn' href='../../{ICS}' download>Add the dates to my calendar (.ics)</a><a class='btn ghost' href='#checklist'>See the checklist</a></div>")+
prose(f"""<h2>The dates</h2><table><thead><tr><th>Date</th><th>What's due</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">The file works with Google Calendar, Apple Calendar and Outlook. Each date is an all-day event with a reminder seven days before. Sources: <a href="{QU}" rel="noopener">HMRC: send quarterly updates</a>, <a href="{ELIG}" rel="noopener">HMRC: when you need MTD</a>, <a href="{SADL}" rel="noopener">GOV.UK: Self Assessment deadlines</a>. Checked {UPDATED}.</p>
<h2 id="checklist">Your MTD checklist</h2>
<ol class="checklist">
<li><strong>Check if and when you need MTD.</strong> It depends on your qualifying income, which means self-employment and property income before expenses. Use our <a href="../../#checker">checker</a> or <a href="{ELIG}" rel="noopener">HMRC's tool</a>. If you didn't get a letter, it's still on you to check.</li>
<li><strong>Check you can sign up.</strong> You need to be registered for Self Assessment and to have sent a tax return in the last 2 years. <a href="{ELIG}" rel="noopener">HMRC</a>.</li>
<li><strong>Choose compatible software.</strong> It must handle every income source you have. Compare all {N} HMRC-recognised products in the <a href="../../finder/">finder</a>. HMRC doesn't recommend any of them.</li>
<li><strong>Sign up with HMRC</strong> and authorise your software. <a href="{SIGN}" rel="noopener">HMRC: sign up</a>.</li>
<li><strong>Keep digital records</strong> of your income and expenses as you go.</li>
<li><strong>Send a quarterly update by each deadline.</strong> Each one covers the tax year so far, not just the last three months. If you had no income or expenses, you still send one. <a href="{QU}" rel="noopener">HMRC</a>.</li>
<li><strong>Know the penalty rules.</strong> HMRC won't give penalty points for late quarterly updates in 2026 to 2027, but you must send them before you can file your tax return. From 2027 to 2028, four points means a £200 penalty. <a href="{QU}" rel="noopener">HMRC</a>.</li>
<li><strong>File your tax return</strong> through your software by 31 January after the tax year. <a href="{TR}" rel="noopener">HMRC</a>.</li>
</ol>
<p class="small">General information, not tax advice. If you have an accountant, check with them which update periods to use.</p>"""),
faqs=[("Do I have to send a quarterly update if I earned nothing?",f"Yes. HMRC says you must still send your quarterly update if you had no income or expenses in the period. <a href='{QU}'>HMRC</a>."),
("Will I be fined for a late quarterly update in 2026 to 2027?",f"No penalty points for late quarterly updates in the 2026 to 2027 tax year, but you still need to send them before you can submit your tax return. Late tax returns still get points. <a href='{QU}'>HMRC</a>."),
("Are the deadlines different for calendar update periods?",f"No. The update periods differ, but the deadlines are the same: 7 August, 7 November, 7 February and 7 May. <a href='{QU}'>HMRC</a>.")])

# ---- 404 page (GitHub Pages and Cloudflare Pages both serve /404.html for missing paths)
page("","Page not found | MTD Finder","This page doesn't exist on MTD Finder.",
hero("Error 404","Page <em>not found</em>","Sorry, we couldn't find that page. It may have moved, or the address may have a typo.")+
prose("""<p>Try one of these instead:</p><ul>
<li><a href="/">Home and the MTD qualifying income checker</a></li>
<li><a href="/finder/">Software finder</a>: compare HMRC-recognised MTD software</li>
<li><a href="/guides/deadlines/">MTD deadlines and quarterly update dates</a></li>
<li><a href="/guides/landlords/">Guide for landlords</a> · <a href="/guides/tradespeople/">Guide for tradespeople</a> · <a href="/guides/bridging-software/">Bridging software</a> · <a href="/guides/deadline-calendar/">Deadline calendar</a></li>
</ul>"""),signup=False,notfound=True)

# ---- ACSP finder (A-030). Data: tools/acsp_sync.py -> data/acsp.json, from Companies House's GOV.UK lists (OGL v3).
ACSP=json.load(open(f"{ROOT}/data/acsp.json"))
ACSP_LIST="https://www.gov.uk/government/publications/list-of-authorised-corporate-service-providers-acsps"
ACSP_CEASED="https://www.gov.uk/government/publications/ceased-or-suspended-authorised-corporate-service-providers-acsps"
ACSP_USE="https://www.gov.uk/guidance/using-an-authorised-corporate-service-provider-acsp-to-verify-your-identity"
IDV="https://www.gov.uk/guidance/verify-your-identity-for-companies-house"
IDV_WHEN="https://www.gov.uk/guidance/when-you-need-to-verify-your-identity-for-companies-house"
AML_HMRC="https://www.gov.uk/guidance/money-laundering-regulations-supervised-business-register"
OGL="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
_ad=lambda k:_dt.date.fromisoformat(ACSP[k][:10]).strftime("%-d %B %Y")
DIRS=[("ICAEW","https://www.icaew.com/about-icaew/find-a-chartered-accountant","find a chartered accountant"),
("ACCA","https://www.accaglobal.com/gb/en/member/find-an-accountant.html","find an accountant"),
("AAT","https://www.aat.org.uk/find-an-accountant-or-bookkeeper","find an accountant or bookkeeper"),
("CIOT","https://pilot-portal.tax.org.uk/utilities/ciot/find-a-member/","find a Chartered Tax Adviser"),
("ATT","https://pilot-portal.tax.org.uk/utilities/att/find-a-member","find an ATT member")]
dirs="".join(f'<li><strong>{a}</strong>: <a href="{u}" rel="noopener">{t}</a></li>' for a,u,t in DIRS)
sups="".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in sorted({a["s"] for a in ACSP["agents"]}))
page("acsp/","Find an ACSP near you: Companies House authorised agents for ID verification","Search Companies House's public list of Authorised Corporate Service Providers (ACSPs) by town or postcode area, with ceased and suspended agents removed. Every fact linked to GOV.UK.",
hero("Companies House identity checks","Find an <em>ACSP</em> near you","Search Companies House's own public list of authorised agents by town or postcode area. Free, independent, and not run by Companies House.",
 f"an ACSP (Authorised Corporate Service Provider), also known as a Companies House authorised agent, is an agent such as an accountant or solicitor who is registered with Companies House and supervised for anti-money laundering. You can ask one to verify your identity for Companies House. <a href='{ACSP_USE}' rel='noopener'>Source: Companies House</a>.")+
f"""<section class="wrap" id="acsp-search"><div class="card reveal"><span class="eyebrow">Search {ACSP['count']:,} agents</span><h2 style="margin-top:0">Search the ACSP list</h2>
<div class="row2"><div class="field"><label for="acsp-q">Town, postcode area or name</label><input id="acsp-q" type="search" placeholder="e.g. Leeds, BS1 or WR10" autocomplete="off" aria-describedby="acsp-help"><p class="small" id="acsp-help" style="margin:6px 0 0">For a postcode, the first half is enough (for example BS1).</p></div>
<div class="field"><label for="acsp-s">Anti-money laundering supervisor</label><select id="acsp-s"><option value="">Any</option>{sups}</select></div></div>
<p class="small" aria-live="polite" id="acsp-count"></p><div id="acsp-out" data-src="../data/acsp.json"></div>
<p class="small">Listed A to Z. Nobody pays to be on this list or to appear higher. Data: Companies House, <a href="{ACSP_LIST}" rel="noopener">list of ACSPs</a> (updated {_ad('source_active_updated')}), with anyone on the <a href="{ACSP_CEASED}" rel="noopener">ceased or suspended list</a> (updated {_ad('source_ceased_updated')}) removed. Contains public sector information licensed under the <a href="{OGL}" rel="noopener">Open Government Licence v3.0</a>. We show the postcode area only.</p></div></section>"""+
prose(f"""<h2>Before you choose an agent</h2>
<p class="notice"><strong>This list isn't complete.</strong> Companies House says the agents on it "have requested to have their details published. It may not include all agents that have registered as an ACSP." It also says it doesn't update the list on a set schedule, and that it "does not endorse or recommend the agents on this list". <a href="{ACSP_LIST}" rel="noopener">Companies House</a>.</p>
<ul><li><strong>Ask your own accountant first.</strong> If you already have an accountant or solicitor, Companies House suggests asking them whether they're registered as an ACSP. <a href="{ACSP_USE}" rel="noopener">Companies House</a>.</li>
<li><strong>Check they haven't been ceased or suspended.</strong> An agent on the <a href="{ACSP_CEASED}" rel="noopener">ceased or suspended list</a> can't act as an ACSP. That list can be up to 2 weeks behind, so we remove anyone on it each time we update. <a href="{ACSP_CEASED}" rel="noopener">Companies House</a>.</li>
<li><strong>Ask what they charge and how they check.</strong> Companies House suggests asking agents directly what services they offer, what they charge, their terms, and whether checks are in person or remote. <a href="{ACSP_LIST}" rel="noopener">Companies House</a>.</li>
<li><strong>Check their anti-money laundering supervisor.</strong> Each listing shows one. If it's HMRC, you can check <a href="{AML_HMRC}" rel="noopener">HMRC's register of supervised businesses</a>. If it's a professional body, check with that body.</li></ul>
<h2>You may not need an agent at all</h2>
<p>You can verify yourself online with GOV.UK One Login if you have accepted photo ID, such as a biometric passport or a UK photo driving licence. There's also a route if you don't have those. <a href="{IDV}" rel="noopener">Companies House</a>.</p>
<h2>When you need to verify</h2>
<p>Identity verification became a legal requirement from 18 November 2025. Companies House says that date "is not a deadline". It started a 12-month transition period. Existing directors give their personal code as part of the company's next confirmation statement, and people with significant control (PSCs) have their own 14-day period. <a href="{IDV}" rel="noopener">Companies House</a>, <a href="{IDV_WHEN}" rel="noopener">when you need to verify</a>.</p>
<h2>What the agent needs from you</h2>
<p>Your full name, home address, email address and evidence to prove your identity. Companies House then emails your personal code to the address you gave your ACSP. <a href="{ACSP_USE}" rel="noopener">Companies House</a>.</p>
<h2>Other ways to find an accountant</h2>
<p>Professional bodies run their own directories. These list members, not ACSPs, so ask anyone you find there whether they're registered as an ACSP.</p><ul>{dirs}</ul>
<h2>Agents: not on the list?</h2><p>The list is Companies House's, not ours, and it only includes agents who asked to be published. We can't add or edit entries. See <a href="{ACSP_LIST}" rel="noopener">Companies House's ACSP list page</a>.</p>
<p class="small">General information, not legal or tax advice. MTD Finder isn't affiliated with Companies House or HMRC. List last synced {_dt.date.fromisoformat(ACSP['synced']).strftime('%-d %B %Y')}.</p>"""),
faqs=[("What is an ACSP?",f"An Authorised Corporate Service Provider, also known as a Companies House authorised agent. It's an agent, such as an accountant or solicitor, registered with Companies House and supervised for anti-money laundering. <a href='{ACSP_USE}'>Companies House</a>."),
("Is this the full list of ACSPs?",f"No. Companies House only publishes agents who asked to be listed, so it may not include every ACSP. <a href='{ACSP_LIST}'>Companies House</a>."),
("Do I have to use an ACSP?",f"No. You can verify yourself online with GOV.UK One Login if you have accepted photo ID. <a href='{IDV}'>Companies House</a>."),
("Is this the same as Making Tax Digital?",f"No. Companies House identity verification is separate from HMRC's Making Tax Digital for Income Tax. For MTD, use our <a href='../#checker'>checker</a>.")],signup=False)

exec(open(os.path.join(ROOT,'tools','drafts.py')).read())
# sitemap, robots, llms
open(f"{ROOT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE}/{p}</loc><lastmod>{UPDATED}</lastmod></url>" for p in pages)+"</urlset>\n")
BOTS=['Googlebot', 'Bingbot', 'Applebot', 'DuckDuckBot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'CCBot', 'Amazonbot', 'meta-externalagent', 'MistralAI-User']
open(f"{ROOT}/robots.txt","w").write("# Search engines and AI assistants are welcome to crawl MTD Finder.\n"+"".join(f"User-agent: {b}\n" for b in BOTS)+"Allow: /\n\nUser-agent: *\nAllow: /\n\n"+f"Sitemap: {SITE}/sitemap.xml\n")
open(f"{ROOT}/{INDEXNOW_KEY}.txt","w").write(INDEXNOW_KEY)
open(f"{ROOT}/llms.txt","w").write(f"""# MTD Finder
> Independent guide to Making Tax Digital (MTD) for Income Tax for UK sole traders and landlords, with a filterable directory of all {N} HMRC-recognised MTD software products. Run by Matthew Snow trading as Sno Automations. Not tax advice; all claims link to HMRC/GOV.UK.

## Key facts (source: {ELIG})
- Qualifying income (self-employment + property, before expenses) over £50,000 in 2024-25: MTD from 6 April 2026
- Over £30,000 in 2025-26: from 6 April 2027
- Over £20,000 in 2026-27: from 6 April 2028
- Quarterly update deadlines: 7 August, 7 November, 7 February, 7 May ({QU})
- Each quarterly update is cumulative from the start of the tax year; a nil update is still required ({QU})
- No penalty points for late quarterly updates in 2026-27; from 2027-28, 4 points = £200 penalty ({QU})
- Partnerships: later, timeline not yet set ({ELIG})
- Facts last checked against GOV.UK: {UPDATED}

## Pages
"""+"".join(f"- [{p or 'Home'}]({SITE}/{p})\n" for p in pages)+f"\n## Downloads\n- [MTD deadline calendar, .ics]({SITE}/{ICS})\n\n## Data\n- [Software data (JSON, from HMRC finder, last checked {data['last_checked']})]({SITE}/data/products.json)\n")
open(f"{ROOT}/.nojekyll","w").write("")
print("built",len(pages),"pages")
