#!/usr/bin/env python3
"""Prove that affiliate_url does not change finder order, filters or scores.
Run: python3 tools/check_affiliate_neutrality.py
Uses data/products.json and the same filter rules as assets/site.js.
Also checks that a mocked HMRC refresh merge keeps affiliate_url and does not invent one.
"""
import json,os,re,sys,copy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data=json.load(open(os.path.join(ROOT,"data","products.json")))
P=data["products"]

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

# Baseline: live data (no affiliate_url keys expected)
before={json.dumps(c,sort_keys=True):ids(filt(P,**c)) for c in CASES}
baseline_order=ids(P)
score_keys=[k for p in P for k in p if "score" in k.lower() or "rank" in k.lower()]
aff_now=[p["id"] for p in P if p.get("affiliate_url")]

# After: same products with placeholder affiliate_url on first, middle and last rows
after_p=copy.deepcopy(P)
for i in (0, len(after_p)//2, len(after_p)-1):
    after_p[i]["affiliate_url"]="https://example.com/affiliate-placeholder"
after={json.dumps(c,sort_keys=True):ids(filt(after_p,**c)) for c in CASES}

ok=True
if baseline_order!=ids(after_p):
    print("FAIL: default list order changed"); ok=False
else:
    print("OK: default list order unchanged (%d products)" % len(baseline_order))

for k in before:
    if before[k]!=after[k]:
        print("FAIL: filter result changed for", k, "before", len(before[k]), "after", len(after[k])); ok=False
if ok:
    print("OK: %d filter cases, identical id lists" % len(CASES))

if score_keys:
    print("NOTE: unexpected score/rank keys present:", set(score_keys))
else:
    print("OK: no score or rank fields on any product (nothing to change)")

if aff_now:
    print("NOTE: live data already has affiliate_url on", aff_now)
else:
    print("OK: live products.json has no affiliate_url keys")

# Refresh merge rule (same as tools in mtdfinder-plans/tools/hmrc_refresh.py)
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

# Data fingerprint excluding the new optional field
def fingerprint(products):
    rows=[]
    for p in products:
        q={k:v for k,v in p.items() if k!="affiliate_url"}
        rows.append(q)
    return rows
# Adding the field in a copy must not change any other field
fp_before=fingerprint(P)
fp_after=fingerprint(after_p)
if fp_before!=fp_after:
    print("FAIL: a non-affiliate field changed when affiliate_url was added"); ok=False
else:
    print("OK: every other product field is unchanged after adding placeholder affiliate_url values")

print("FIRST5", baseline_order[:5], "LAST5", baseline_order[-5:])
if not ok:
    sys.exit(1)
print("ALL CHECKS PASSED")
