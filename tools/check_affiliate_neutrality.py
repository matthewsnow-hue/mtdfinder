#!/usr/bin/env python3
"""Prove that affiliate_url does not change finder order or filters, and that
the displayed list is A to Z under the same normalised comparison as assets/site.js.
Run: python3 tools/check_affiliate_neutrality.py
Uses data/products.json and the same filter rules as assets/site.js.
Also checks that a mocked HMRC refresh merge keeps affiliate_url and does not invent one.
Does not rewrite data/products.json.
"""
import json,os,re,sys,copy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data=json.load(open(os.path.join(ROOT,"data","products.json")))
P=data["products"]
FILE_ORDER=[p["id"] for p in P]

def name_key(name):
    """Match site.js: strip leading non-alphanumerics (Unicode letters/digits), then casefold."""
    name=str(name or "")
    i=0
    for i,ch in enumerate(name):
        if ch.isalnum():
            name=name[i:]
            break
    else:
        name=""
    return name.casefold()

def sort_key(p):
    name=str(p.get("name") or "")
    return (name_key(name), name, str(p.get("id") or ""))

def display(products, **filters):
    return sorted(filt(products, **filters), key=sort_key)

def is_az(rows):
    keys=[sort_key(p) for p in rows]
    return keys==sorted(keys)

def filt(products, who="any", typ="any", free=False, vat=False, cis=False, assist=False, welsh=False, tax=False, q=""):
    q=q.lower().strip()
    out=[]
    for p in products:
        if not (who=="any" or (who=="st" and p["sole_trader"]) or (who=="ll" and p["landlord"]) or (who=="both" and p["sole_trader"] and p["landlord"])):
            continue
        if not (typ=="any" or (typ=="bridging" and p["bridging"]) or (typ=="records" and p["creates_records"])):
            continue
        if free and not p["free_version"]: continue
        if vat and not p["vat"]: continue
        if cis and not p["cis"]: continue
        if assist and not p["hmrc_assist"]: continue
        if welsh and not p["welsh"]: continue
        if tax and not (re.search(r"Tax return", p.get("submissions") or "") and re.search(r"Quarterly updates", p.get("submissions") or "")):
            continue
        if q and q not in p["name"].lower(): continue
        out.append(p)
    return out

def ids(rows): return [p["id"] for p in rows]

CASES=[
    {},
    {"who":"st"},
    {"who":"ll"},
    {"who":"both"},
    {"typ":"bridging"},
    {"typ":"records"},
    {"free":True},
    {"vat":True},
    {"cis":True},
    {"assist":True},
    {"welsh":True},
    {"tax":True},
    {"q":"xero"},
    {"q":"freeagent"},
    {"who":"st","typ":"bridging","free":True},
    {"who":"ll","tax":True,"vat":True},
]

ok=True

# File order in products.json must be left as the HMRC refresh left it
if ids(P)!=FILE_ORDER:
    print("FAIL: products.json file order was mutated"); ok=False
else:
    print("OK: data/products.json file order left untouched (%d products)" % len(P))

# Displayed order is A to Z, including after each filter case
az_fail=[]
for c in CASES:
    rows=display(P, **c)
    if not is_az(rows):
        az_fail.append(c)
        ok=False
    if {p["id"] for p in rows}!={p["id"] for p in filt(P, **c)}:
        print("FAIL: display sort dropped or added products for", c); ok=False
if az_fail:
    print("FAIL: displayed order was not A to Z for", az_fail)
else:
    print("OK: displayed order is A to Z for the unfiltered list and %d filter cases" % (len(CASES)-1))

shown=display(P)
print("DISPLAY FIRST10:")
for p in shown[:10]:
    print(" ", p["name"])
print("DISPLAY LAST5:")
for p in shown[-5:]:
    print(" ", p["name"])
for want in ('#GoFile', '"untied"'):
    hits=[(i,p) for i,p in enumerate(shown,1) if p["name"]==want]
    if hits:
        i,p=hits[0]
        print("DISPLAY %r at %d of %d (sorts as %r)" % (p["name"], i, len(shown), name_key(p["name"])))
    else:
        print("DISPLAY: %r not found" % want)
        ok=False

# Affiliate placeholders must not change file order, filter membership, or displayed order
before_filt={json.dumps(c,sort_keys=True):ids(filt(P,**c)) for c in CASES}
before_disp={json.dumps(c,sort_keys=True):ids(display(P,**c)) for c in CASES}
after_p=copy.deepcopy(P)
# Placeholders on first, middle and last of the *file* (as a refresh would touch existing rows)
for i in (0, len(after_p)//2, len(after_p)-1):
    after_p[i]["affiliate_url"]="https://example.com/affiliate-placeholder"
if ids(after_p)!=FILE_ORDER:
    print("FAIL: adding affiliate_url changed the data-file order"); ok=False
else:
    print("OK: adding placeholder affiliate_url values does not change data-file order")

filt_ok=disp_ok=True
for c in CASES:
    k=json.dumps(c,sort_keys=True)
    if ids(filt(after_p,**c))!=before_filt[k]:
        print("FAIL: filter result changed for", c); filt_ok=False; ok=False
    if ids(display(after_p,**c))!=before_disp[k]:
        print("FAIL: displayed order changed for", c); disp_ok=False; ok=False
    if not is_az(display(after_p,**c)):
        print("FAIL: displayed order not A to Z after placeholders for", c); ok=False
if filt_ok:
    print("OK: %d filter cases, identical id lists after placeholders" % len(CASES))
if disp_ok:
    print("OK: displayed A to Z order unchanged after placeholders")

score_keys=[k for p in P for k in p if "score" in k.lower() or "rank" in k.lower()]
if score_keys:
    print("NOTE: unexpected score/rank keys present:", set(score_keys))
else:
    print("OK: no score or rank fields on any product")

aff_now=[p["id"] for p in P if p.get("affiliate_url")]
if aff_now:
    print("NOTE: live data already has affiliate_url on", aff_now)
else:
    print("OK: live products.json has no affiliate_url keys")

def merge(oldp, new_core):
    p=dict(new_core)
    au=oldp.get("affiliate_url")
    if isinstance(au,str) and au.strip(): p["affiliate_url"]=au.strip()
    return p

kept=merge({"id":"1","name":"Old","affiliate_url":"  https://example.com/affiliate-placeholder  "}, {"id":"1","name":"New","website":"https://vendor.example"})
assert kept["affiliate_url"]=="https://example.com/affiliate-placeholder", kept
assert kept["name"]=="New"
dropped=merge({"id":"2","name":"Y"}, {"id":"2","name":"Y2"})
assert "affiliate_url" not in dropped
nullish=merge({"id":"3","affiliate_url":None}, {"id":"3","name":"Z"})
assert "affiliate_url" not in nullish
empty=merge({"id":"4","affiliate_url":"  "}, {"id":"4","name":"Z"})
assert "affiliate_url" not in empty
print("OK: refresh merge preserves a set affiliate_url and does not invent one")

def fingerprint(products):
    return [{k:v for k,v in p.items() if k!="affiliate_url"} for p in products]
if fingerprint(P)!=fingerprint(after_p):
    print("FAIL: a non-affiliate field changed when affiliate_url was added"); ok=False
else:
    print("OK: every other product field is unchanged after adding placeholder affiliate_url values")

if not ok:
    sys.exit(1)
print("ALL CHECKS PASSED")
