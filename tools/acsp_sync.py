#!/usr/bin/env python3
"""Sync data/acsp.json from Companies House's two public ACSP lists on GOV.UK (Open Government Licence v3.0).
Run: python3 tools/acsp_sync.py   (then python3 tools/build.py)
- Active list: agents who asked Companies House to publish their details (opt-in, so incomplete).
- Ceased or suspended list: any agent on it is dropped, matched on name + AML supervisor.
- Data minimisation: we keep only the postcode district (e.g. 'WR10'), never the full postcode,
  because some entries are sole practitioners (personal data). Privacy policy explains this.
"""
import csv,io,json,os,re,urllib.request,datetime
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API="https://www.gov.uk/api/content/government/publications/"
PUB={"active":"list-of-authorised-corporate-service-providers-acsps","ceased":"ceased-or-suspended-authorised-corporate-service-providers-acsps"}
def get(u):return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"mtdfinder-acsp-sync"}),timeout=60).read()
def latest(slug):
    d=json.loads(get(API+slug));a=[x for x in d["details"]["attachments"] if x["url"].lower().endswith(".csv")][0]
    return d["public_updated_at"],a["url"],dec(get(a["url"]))
def dec(b):
    try:return b.decode("utf-8-sig")
    except UnicodeDecodeError:return b.decode("cp1252")
def norm(s):return re.sub(r"\s+"," ",s).strip().upper()
def district(pc):
    pc=norm(pc).replace(" ","");return pc[:-3] if len(pc)>=5 else ""
def main():
    au,aurl,atext=latest(PUB["active"]);cu,curl,ctext=latest(PUB["ceased"])
    bad={(norm(r["ACSP Name"]),norm(r["Supervisor Name"])) for r in csv.DictReader(io.StringIO(ctext))}
    sp=f"{ROOT}/data/acsp-suppress.json"   # names (upper case) removed on request, see privacy policy
    sup={norm(x) for x in (json.load(open(sp)) if os.path.exists(sp) else [])}
    rows=[];dropped=0;seen=set()
    for r in csv.DictReader(io.StringIO(atext)):
        n,s=norm(r["ACSP"]),norm(r["Supervisor Name"])
        if (n,s) in bad:dropped+=1;continue
        if n in sup:continue
        t=norm(r["Town"]).title();k=(n,s,t,district(r["Postcode"]))
        if k in seen:continue
        seen.add(k);rows.append({"n":r["ACSP"].strip(),"s":r["Supervisor Name"].strip(),"t":t,"d":district(r["Postcode"])})
    rows.sort(key=lambda x:(x["n"].upper(),x["t"]))
    out={"source_active":aurl,"source_active_updated":au,"source_ceased":curl,"source_ceased_updated":cu,
         "synced":datetime.date.today().isoformat(),"dropped_ceased_or_suspended":dropped,"count":len(rows),"licence":"Open Government Licence v3.0","agents":rows}
    json.dump(out,open(f"{ROOT}/data/acsp.json","w"),ensure_ascii=False,separators=(",",":"))
    print(f"acsp.json: {len(rows)} agents, {dropped} dropped as ceased/suspended")
if __name__=="__main__":main()
