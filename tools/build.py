#!/usr/bin/env python3
"""Static site generator for MTD Finder. Run: python3 tools/build.py (outputs HTML to repo root)."""
import json,os,html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE="https://mtdfinder.co.uk"
UPDATED="2026-10-14"
ELIG="https://www.gov.uk/guidance/check-if-youre-eligible-for-making-tax-digital-for-income-tax"
QI="https://www.gov.uk/guidance/work-out-your-qualifying-income-for-making-tax-digital-for-income-tax"
SW="https://www.gov.uk/guidance/find-software-thats-compatible-with-making-tax-digital-for-income-tax"
TOOL="https://www.tax.service.gov.uk/find-making-tax-digital-income-tax-software/"
QU="https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates"
TR="https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/submit-your-tax-return"
SIGN="https://www.gov.uk/guidance/sign-up-your-business-for-making-tax-digital-for-income-tax"
EMAIL="hello@mtdfinder.co.uk"
data=json.load(open(f"{ROOT}/data/products.json"))
N=data["count"]
NAV=[("finder/","Software finder"),("guides/deadlines/","Deadlines"),("guides/landlords/","Landlords"),("guides/tradespeople/","Trades"),("faq/","FAQ"),("sponsor/","Sponsor")]
ORG={"@type":"Organization","@id":SITE+"/#org","name":"Sno Automations","url":SITE+"/","description":"MTD Finder is run by Matthew Snow trading as Sno Automations, a UK sole trader."}
def faq_ld(qs):return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html.unescape(__import__('re').sub('<[^>]+>','',a))}} for q,a in qs]}
def faq_html(qs):return "".join(f"<details class='reveal'><summary>{q}</summary><p>{a}</p></details>" for q,a in qs)
pages=[]
ITEMS={"@context":"https://schema.org","@type":"ItemList","name":"HMRC-recognised MTD for Income Tax software","numberOfItems":N,"itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"SoftwareApplication","name":p["name"],"applicationCategory":"FinanceApplication","operatingSystem":"Web","url":p["website"] or p["hmrc_url"]}} for i,p in enumerate(data["products"])]}
def page(path,title,desc,body,faqs=None,extra_ld=None,eyebrow=None):
    depth=path.count("/");pre="../"*depth
    url=f"{SITE}/{path}"
    lds=[{"@context":"https://schema.org","@graph":[ORG,{"@type":"WebSite","@id":SITE+"/#site","name":"MTD Finder","url":SITE+"/","publisher":{"@id":SITE+"/#org"}},{"@type":"WebPage","name":title,"url":url,"dateModified":UPDATED,"isPartOf":{"@id":SITE+"/#site"}}]}]
    if faqs:lds.append(faq_ld(faqs));body+=f"<section class='wrap narrow'><span class='eyebrow'>Questions</span><h2 style='margin-top:0'>Frequently asked</h2>{faq_html(faqs)}</section>"
    if extra_ld:lds.append(extra_ld)
    nav="".join(f'<li><a href="{pre}{h}"{" aria-current=page" if h==path else ""}>{t}</a></li>' for h,t in NAV)
    ld="".join(f'<script type="application/ld+json">{json.dumps(l,ensure_ascii=False)}</script>' for l in lds)
    doc=f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="MTD Finder"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="en_GB"><meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f8f4ec"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231d5c4a'/%3E%3Ctext x='16' y='22' font-size='17' text-anchor='middle' fill='white' font-family='Georgia'%3EM%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/style.css">{ld}</head><body>
<a href="#main" class="skip">Skip to content</a>
<header class="site"><div class="wrap nav"><a class="brand" href="{pre or './'}">MTD <em>Finder</em></a><button class="menu-btn" aria-expanded="false" aria-label="Menu">Menu</button><ul>{nav}</ul></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="cols"><div><a class="brand" href="{pre or './'}">MTD <em>Finder</em></a><p>An independent guide to Making Tax Digital for Income Tax software, for UK sole traders and landlords. Not affiliated with HMRC. Not tax advice. Run by Matthew Snow trading as Sno Automations.</p><p>Owner: Matthew Snow trading as Sno Automations · <a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Software data from <a href="{TOOL}" rel="noopener">HMRC's software finder</a>, last checked {data['last_checked']}.</p></div>
<ul><li><a href="{pre}finder/">Software finder</a></li><li><a href="{pre}guides/deadlines/">Deadlines</a></li><li><a href="{pre}guides/landlords/">Landlords</a></li><li><a href="{pre}guides/tradespeople/">Tradespeople</a></li><li><a href="{pre}guides/bridging-software/">Bridging software</a></li><li><a href="{pre}faq/">FAQ</a></li></ul>
<ul><li><a href="{pre}about/">About</a></li><li><a href="{pre}sponsor/">Sponsor us</a></li><li><a href="{pre}newsletter/">Newsletter</a></li><li><a href="{pre}privacy/">Privacy</a></li><li><a href="{pre}disclaimer/">Disclaimer</a></li></ul></div></div></footer>
<script src="{pre}assets/site.js" defer></script></body></html>"""
    d=os.path.join(ROOT,path);os.makedirs(d,exist_ok=True);open(os.path.join(d,"index.html"),"w").write(doc);pages.append(path)

def hero(eb,h1,lede,answer=None,btns=""):
    a=f"<div class='answer'><strong>Short answer:</strong> {answer[0].upper()+answer[1:]}</div>" if answer else ""
    return f"<section class='hero wrap'><div class='narrow'><span class='eyebrow'>{eb}</span><h1>{h1}</h1><p class='lede'>{lede}</p>{a}{btns}</div></section>"
def prose(s):return f"<section class='wrap narrow prose reveal'>{s}</section>"

THRESH=f"""<table><thead><tr><th>Qualifying income over</th><th>In tax year</th><th>Use MTD from</th></tr></thead><tbody>
<tr><td>£50,000</td><td>2024 to 2025</td><td>6 April 2026</td></tr><tr><td>£30,000</td><td>2025 to 2026</td><td>6 April 2027</td></tr><tr><td>£20,000</td><td>2026 to 2027</td><td>6 April 2028</td></tr></tbody></table><p class="small">Source: <a href="{ELIG}" rel="noopener">HMRC, Find out if and when you need to use Making Tax Digital for Income Tax</a>.</p>"""
yrs=[("2024 to 2025","£50k test"),("2025 to 2026","£30k test"),("2026 to 2027","£20k test")]
fields="".join(f"<fieldset><legend>{y} <span class='small'>({t})</span></legend><div class='row2'><div><label for='se{i}'>Self-employment turnover (£)</label><input id='se{i}' type='number' inputmode='decimal' min='0' step='100' placeholder='0'></div><div><label for='pr{i}'>Property income, your share (£)</label><input id='pr{i}' type='number' inputmode='decimal' min='0' step='100' placeholder='0'></div></div></fieldset>" for i,(y,t) in enumerate(yrs))
home_faq=[("Who needs to use Making Tax Digital for Income Tax?",f"Sole traders and landlords registered for Self Assessment whose qualifying income from self-employment and property is over the threshold for the relevant tax year. <a href='{ELIG}'>HMRC guidance</a>."),
("What counts as qualifying income?",f"Your total self-employment and property income before expenses (turnover). Employment (PAYE) income, dividends, pensions and your share of partnership profit do not count. <a href='{QI}'>HMRC guidance</a>."),
("Does HMRC recommend any MTD software?",f"No. HMRC says all listed software has been through its recognition process, but it does not recommend any product. <a href='{SW}'>HMRC guidance</a>."),
("Do I still need to file a Self Assessment return?",f"Yes. You still submit a Self Assessment return for the tax year before you start using MTD, and once you are using MTD you submit your tax return through your software by 31 January following the tax year. <a href='{ELIG}'>HMRC</a>, <a href='{SW}'>HMRC software guidance</a>.")]
page("","MTD Finder: Do I need Making Tax Digital, and which software?","Free Making Tax Digital for Income Tax checker and independent finder for all "+str(N)+" HMRC-recognised MTD software products for UK sole traders and landlords.",
hero("Making Tax Digital for Income Tax","Do I need MTD, <em>and when?</em>","An independent, plain-English guide for UK sole traders and landlords, with a finder covering every HMRC-recognised product.",
 f"if your self-employment and property income before expenses is over £50,000 (2024 to 2025), you should have started MTD from 6 April 2026. Over £30,000 in 2025 to 2026 means 6 April 2027, and over £20,000 in 2026 to 2027 means 6 April 2028. <a href='{ELIG}' rel='noopener'>Source: HMRC</a>.",
 "<div class='btns'><a class='btn' href='#checker'>Check in 30 seconds</a><a class='btn ghost' href='finder/'>Browse "+str(N)+" products</a></div><div class='trust'><span>Every claim linked to HMRC</span><span>Independent</span><span>Free to use</span></div>")+
f"""<section class="wrap" id="checker"><div class="calc reveal"><form id="calc" novalidate><span class="eyebrow">MTD checker</span><h2 style="margin-top:0">Enter your income</h2><p class="small">Gross income before expenses, from your Self Assessment returns. Leave years blank if you don't know them yet.</p>
<div class="field"><label><input type="checkbox" id="sa" checked> I'm a sole trader or landlord registered for Self Assessment</label></div>{fields}
<p class="small">Don't include wages (PAYE), dividends, pensions or partnership profit shares. They don't count towards <a href="{QI}" rel="noopener">qualifying income</a>.</p></form>
<div class="result" id="calc-out" aria-live="polite"></div></div></section>
<section class="wrap narrow reveal"><h2>The thresholds</h2>{THRESH}</section>
<section class="wrap reveal explore"><h2>Explore</h2><div class="grid">
<a class="card" href="finder/"><span class="num">{N}</span><h3>Software finder</h3><p class="small">Filter HMRC-recognised products by income type, bridging or bookkeeping, free version, VAT and CIS.</p></a>
<a class="card" href="guides/deadlines/"><span class="num">4×</span><h3>Quarterly deadlines</h3><p class="small">7 August, 7 November, 7 February and 7 May, explained.</p></a>
<a class="card" href="guides/tradespeople/"><span class="num">CIS</span><h3>For tradespeople</h3><p class="small">Electricians, plumbers, builders and solar installers.</p></a></div></section>""",faqs=home_faq)

page("finder/","MTD Software Finder: compare all "+str(N)+" HMRC-recognised products","Filter every HMRC-recognised Making Tax Digital for Income Tax product by sole trader or landlord, bridging or bookkeeping, free version, VAT, CIS and HMRC Assist.",
hero("Software finder","Find your <em>MTD software</em>","Every product listed in HMRC's software finder, with filters that match how you actually work.",
 f"pick software that supports all your income sources, sends quarterly updates and submits your tax return. All {N} products here are on <a href='{TOOL}' rel='noopener'>HMRC's list</a>; HMRC doesn't recommend any of them.")+
f"""<section class="wrap"><div class="searchbar"><div><label for="q">Search {N} products</label><input id="q" type="search" placeholder="Name, e.g. Xero, FreeAgent, spreadsheet" autocomplete="off"></div><button class="btn ghost filter-toggle" aria-expanded="false" aria-controls="side">Filters</button></div>
<div class="finder"><aside class="side" id="side" aria-label="Filters"><h2>Filter</h2>
<div class="grp"><label for="who">I am a</label><select id="who"><option value="any">Any</option><option value="st">Sole trader</option><option value="ll">Landlord</option><option value="both">Both</option></select></div>
<div class="grp"><label for="type">Software type</label><select id="type"><option value="any">Any</option><option value="records">Full bookkeeping (creates records)</option><option value="bridging">Bridging (connects spreadsheets)</option></select></div>
<div class="grp" role="group" aria-label="Features"><label>Features</label>
<label class="chk"><input type="checkbox" data-k="free"> Free version</label><label class="chk"><input type="checkbox" data-k="tax"> Files tax return</label><label class="chk"><input type="checkbox" data-k="vat"> MTD for VAT</label><label class="chk"><input type="checkbox" data-k="cis"> CIS ready</label><label class="chk"><input type="checkbox" data-k="assist"> HMRC Assist</label><label class="chk"><input type="checkbox" data-k="welsh"> Welsh language</label></div>
<div class="grp"><button class="linkbtn" id="clear" type="button">Clear all filters</button></div>
<p class="small">Price band and mobile app filters are coming: HMRC's data doesn't include them yet.</p></aside>
<div><div class="resbar"><p class="small" style="margin:0" aria-live="polite"><strong id="count">…</strong> of <span id="count-total">{N}</span> products · alphabetical, never paid</p><p class="small" style="margin:0">Data: <a href="{TOOL}" rel="noopener">HMRC</a>, checked {data['last_checked']}</p></div>
<div class="grid"><article class="card featured"><span class="badge">Featured · Sponsored</span><h3>Your software here</h3><p class="small">One clearly labelled placement for an HMRC-recognised product. It never changes the order of the main list.</p><div><a class="btn" href="../sponsor/">Sponsor us</a></div></article></div>
<div class="grid" id="list" data-src="../data/products.json" style="margin-top:18px"></div></div></div></section>
<div class="tray" id="tray" aria-live="polite"><span id="tray-n">0 selected</span><button class="btn" id="cmp-open" type="button">Compare</button></div>
<dialog id="cmp"><div class="in"><div style="display:flex;justify-content:space-between;align-items:center"><h2 style="margin:0">Compare</h2><button class="btn ghost" id="cmp-close" type="button">Close</button></div><div id="cmp-body" style="overflow:auto;margin-top:18px"></div></div></dialog>""",extra_ld=ITEMS)

page("guides/deadlines/","MTD for Income Tax deadlines and quarterly update dates (2026)","Making Tax Digital for Income Tax start dates and quarterly update deadlines: 7 August, 7 November, 7 February and 7 May, plus the 31 January tax return.",
hero("Guide","MTD deadlines and <em>quarterly dates</em>","When you start, and when each update is due.",f"quarterly updates are due by 7 August, 7 November, 7 February and 7 May. Your tax return is due by 31 January after the tax year. <a href='{QU}' rel='noopener'>Source: HMRC</a>.")+
prose(f"""<h2>When you start</h2>{THRESH}<h2>Quarterly update deadlines</h2><table><thead><tr><th>Standard update period</th><th>Deadline</th></tr></thead><tbody><tr><td>6 April to 5 July</td><td>7 August</td></tr><tr><td>6 April to 5 October</td><td>7 November</td></tr><tr><td>6 April to 5 January</td><td>7 February</td></tr><tr><td>6 April to 5 April</td><td>7 May (the following tax year)</td></tr></tbody></table>
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
<h2>Electricians, plumbers and solar installers</h2><p>For most one-person trade businesses, full bookkeeping software that links to your bank and lets you photograph receipts on site is the simplest route. If you already keep good spreadsheets, <a href="../bridging-software/">bridging software</a> can be cheaper. Either way, filter for <em>Sole trader</em>, <em>Files tax return</em> and <em>CIS ready</em> if you do subcontract work.</p><p><a class="btn" href="../../finder/">Find trade-friendly software</a></p>"""),
faqs=[("I'm an electrician earning £35k turnover but £18k profit. Do I need MTD?",f"Very likely, from 6 April 2027 if that £35,000 turnover was in 2025 to 2026, because the threshold uses income before expenses. <a href='{QI}'>HMRC</a>. Check your own figures with <a href='{ELIG}'>HMRC's tool</a>."),("Does wage income from a part-time job count?",f"No. Employment (PAYE) income doesn't count towards qualifying income. <a href='{QI}'>HMRC</a>."),("Which MTD software supports CIS?",f"HMRC's listing shows CIS support for each product. {cis} products currently show it as ready now. See our finder.")])

page("guides/bridging-software/","MTD bridging software explained: keep your spreadsheet","What MTD bridging software is, how it connects spreadsheets to HMRC, and when it's a better choice than full bookkeeping software.",
hero("Guide","Bridging software, <em>explained</em>","Keep your spreadsheet and let a small tool do the HMRC bit.",f"bridging software connects to records you already keep, such as spreadsheets, and makes your MTD submissions to HMRC. <a href='{SW}' rel='noopener'>Source: HMRC</a>.")+
prose(f"""<h2>Two types of MTD software</h2><p>HMRC describes two types: software that <strong>creates digital records</strong> (bank feeds, receipt scanning or manual entry) and software that <strong>connects to your records</strong>, sometimes called bridging software. <a href="{SW}" rel="noopener">HMRC</a>.</p>
<h2>Does bridging software file my tax return?</h2><p>Some do. HMRC notes that some bridging products let you both send quarterly updates and submit your tax return. <a href="{SW}" rel="noopener">HMRC</a>. Use the <strong>Bridging</strong> and <strong>Files tax return</strong> filters in the <a href="../../finder/">finder</a>.</p>
<h2>When it suits you</h2><ul><li>You're comfortable keeping a tidy spreadsheet.</li><li>You have simple income and few transactions.</li><li>You want to keep costs low. HMRC notes free products exist for simple affairs, but they may have limits. <a href="{SW}" rel="noopener">HMRC</a>.</li></ul><p><a class="btn" href="../../finder/">See bridging products</a></p>"""),
faqs=[("Can I keep using Excel for MTD?",f"Yes, with bridging software that connects your spreadsheet to HMRC. <a href='{SW}'>HMRC</a>."),("Can I use two products?",f"Yes, but only one product for each separate submission, so make sure they work together. <a href='{SW}'>HMRC</a>.")])

faqs_all=home_faq+[("When do I need to start MTD?",f"From 6 April 2026 if over £50,000 in 2024 to 2025; 6 April 2027 if over £30,000 in 2025 to 2026; 6 April 2028 if over £20,000 in 2026 to 2027. <a href='{ELIG}'>HMRC</a>."),
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
f"""<section class="wrap"><div class="grid"><div class="card featured reveal"><span class="badge">Featured listing</span><div class="stat">£49<span style="font-size:1.1rem">/month</span></div><p>Introductory price. One clearly labelled featured slot on the software finder, plus a mention in the newsletter.</p><p class="small">Payment link coming soon.</p><a class="btn" href="mailto:{EMAIL}?subject=MTD%20Finder%20sponsorship">Email to enquire</a></div>
<div class="card reveal"><h3>Our rules</h3><ul class="small"><li>Only HMRC-recognised products.</li><li>Sponsored placements are always labelled.</li><li>Sponsorship never changes the main list order or our editorial content.</li><li>We may earn affiliate commission; we always disclose it.</li></ul></div></div></section>""")

page("newsletter/","MTD Finder newsletter: deadline reminders for sole traders and landlords","Sign up for MTD Finder's newsletter for plain-English Making Tax Digital deadline reminders and software updates. Coming soon.",
hero("Newsletter","Deadline reminders, <em>coming soon</em>","A short email before each quarterly deadline, plus any changes HMRC makes. No spam.")+
f"""<section class="wrap narrow"><form class="card" onsubmit="event.preventDefault();this.querySelector('p.small').textContent='Thanks! Sign-ups open soon. Nothing has been stored.'"><!-- TODO: connect to newsletter backend (Gmail routine / provider) after privacy policy is finalised --><label for="em">Email address</label><input id="em" type="email" required placeholder="you@example.co.uk"><div class="btns"><button class="btn">Notify me</button></div><p class="small">Sign-ups aren't live yet, so nothing is stored. See our <a href="../privacy/">privacy policy</a>.</p></form></section>""")

page("about/","About MTD Finder: independent, run by Sno Automations","MTD Finder is an independent guide to Making Tax Digital for Income Tax software, run by Matthew Snow trading as Sno Automations, a UK sole trader.",
hero("About","Built by a sole trader, <em>for sole traders</em>","MTD Finder is run by Matthew Snow trading as Sno Automations, a UK sole trader.")+
prose(f"""<p>We built MTD Finder because HMRC's official list is accurate but hard to browse, and many \"best MTD software\" articles are written by vendors ranking their own products.</p><h2>How we work</h2><ul><li>Every tax claim links to HMRC or GOV.UK.</li><li>Software data comes from <a href="{TOOL}" rel="noopener">HMRC's software finder</a> and is rechecked regularly. Last checked: {data['last_checked']}.</li><li>The main list is alphabetical. Sponsored slots are labelled.</li><li>We're independent and not affiliated with HMRC.</li></ul><p>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""))

page("privacy/","Privacy policy | MTD Finder","How MTD Finder, run by Matthew Snow trading as Sno Automations, handles personal data.",
hero("Legal","Privacy policy","Last updated "+UPDATED+".")+
prose(f"""<p class="notice">Draft. To be reviewed before newsletter sign-ups go live.</p><h2>Who we are</h2><p>MTD Finder is run by Matthew Snow trading as Sno Automations, a UK sole trader, who is the data controller. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>What we collect</h2><p>The MTD checker runs entirely in your browser. The figures you enter are never sent to us. We don't currently use analytics or advertising cookies. The site is hosted on GitHub Pages, which may log technical data such as IP addresses for security. Fonts are loaded from Google Fonts.</p>
<h2>Newsletter (when live)</h2><p>If you sign up, we'll store your email address to send the newsletter, on the basis of your consent. You can unsubscribe at any time and we'll delete your address.</p><h2>Your rights</h2><p>Under UK GDPR you can ask to access, correct or delete your data, and complain to the <a href="https://ico.org.uk/" rel="noopener">Information Commissioner's Office</a>.</p>"""))

page("disclaimer/","Disclaimer and affiliate disclosure | MTD Finder","MTD Finder is independent, is not affiliated with HMRC, does not give tax advice and may earn affiliate commission.",
hero("Legal","Disclaimer","Please read before relying on anything here.")+
prose(f"""<h2>Not tax advice</h2><p>MTD Finder gives general information only. It isn't tax, legal or financial advice. Always check <a href="{ELIG}" rel="noopener">HMRC guidance</a> or speak to a qualified adviser.</p><h2>Independent</h2><p>We're not affiliated with or endorsed by HMRC. HMRC doesn't recommend any software product.</p><h2>Accuracy</h2><p>Software details come from HMRC's public listing and vendors' sites, and can change. Always confirm features and prices with the vendor.</p><h2>Affiliate disclosure</h2><p>Some links may be affiliate links, so we may earn a commission at no extra cost to you. Featured placements are paid and always labelled. Neither changes the order of the main list.</p>"""))

# sitemap, robots, llms
open(f"{ROOT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE}/{p}</loc><lastmod>{UPDATED}</lastmod></url>" for p in pages)+"</urlset>\n")
open(f"{ROOT}/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(f"{ROOT}/llms.txt","w").write(f"""# MTD Finder
> Independent guide to Making Tax Digital (MTD) for Income Tax for UK sole traders and landlords, with a filterable directory of all {N} HMRC-recognised MTD software products. Run by Matthew Snow trading as Sno Automations. Not tax advice; all claims link to HMRC/GOV.UK.

## Key facts (source: {ELIG})
- Qualifying income (self-employment + property, before expenses) over £50,000 in 2024-25: MTD from 6 April 2026
- Over £30,000 in 2025-26: from 6 April 2027
- Over £20,000 in 2026-27: from 6 April 2028
- Quarterly update deadlines: 7 August, 7 November, 7 February, 7 May ({QU})

## Pages
"""+"".join(f"- [{p or 'Home'}]({SITE}/{p})\n" for p in pages)+f"\n## Data\n- [Software data (JSON, from HMRC finder, last checked {data['last_checked']})]({SITE}/data/products.json)\n")
open(f"{ROOT}/.nojekyll","w").write("")
print("built",len(pages),"pages")
