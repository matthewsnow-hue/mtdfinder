#!/usr/bin/env python3
"""Per-page sitemap <lastmod> for MTD Finder: real, deterministic, no git needed at build time.

How it works
- data/lastmod.json holds, for every sitemap page, {"hash": ..., "lastmod": "YYYY-MM-DD"}.
- On each build, tools/build.py hashes the page's own content (see norm(): title, meta description and <main> only, so a footer
  count, nav, social tags or the dateModified value never count as a change) plus the data files the page loads in the browser (DEPS).
- Same hash as the manifest: keep the stored lastmod. Different hash, or a new page: lastmod becomes the build date (today,
  or MTD_BUILD_DATE=YYYY-MM-DD if set) and the manifest is updated. Commit data/lastmod.json with the pages.
- So a page only gets a new date when its content (or the data it loads) really changed. Nothing here calls git.

One-off seeding from git history (already done; only needed to rebuild the manifest from scratch):
    python3 tools/lastmod.py seed     # run on a checkout whose committed pages match the current build output
It sets each page's date to the last commit that changed its normalised content, or its data file for /finder/ and /acsp/.
"""
import hashlib,json,os,re,subprocess,sys,datetime
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST=os.path.join(ROOT,"data","lastmod.json")
PLACEHOLDER="@@LASTMOD@@"
# Data files a page loads in the browser, so a change to them is a change to the page.
DEPS={"finder/":["data/products.json"],"acsp/":["data/acsp.json"]}

def norm(doc):
    """The part of a page that counts as its content: <title>, meta description and <main>.
    Header, footer, social/OG tags, scripts and the dateModified value are ignored."""
    parts=[]
    for pat in (r'<title>.*?</title>',r'<meta name="description"[^>]*>',r'<main id="main">.*?</main>'):
        m=re.search(pat,doc,flags=re.S);parts.append(m.group(0) if m else "")
    return "\n".join(parts)
def digest(path,doc):
    h=hashlib.sha256(norm(doc).encode())
    for d in DEPS.get(path,[]):h.update(open(os.path.join(ROOT,d),"rb").read())
    return h.hexdigest()
def today():
    return os.environ.get("MTD_BUILD_DATE") or datetime.date.today().isoformat()
def load():
    try:return json.load(open(MANIFEST))
    except FileNotFoundError:return {}
def save(m):
    open(MANIFEST,"w").write(json.dumps(m,indent=1,sort_keys=True)+"\n")
def resolve(manifest,path,doc):
    """Return (lastmod, new_entry) for a page's doc (still holding the dateModified placeholder)."""
    h=digest(path,doc);e=manifest.get(path)
    if e and e.get("hash")==h:return e["lastmod"],e
    return today(),{"hash":h,"lastmod":today()}

def _git(*a):
    return subprocess.run(["git","-C",ROOT,*a],capture_output=True,text=True,check=True).stdout
def seed():
    m={}
    sm=open(os.path.join(ROOT,"sitemap.xml")).read()
    for path in re.findall(r"<loc>https://mtdfinder\.co\.uk/([^<]*)</loc>",sm):
        f=(path+"index.html")
        doc=open(os.path.join(ROOT,f)).read()
        date=None
        for line in _git("log","--format=%H %cs","--",f).splitlines():
            c,d=line.split()
            try:prev=_git("show",f"{c}^:{f}")
            except subprocess.CalledProcessError:date=d;break
            if norm(prev)!=norm(_git("show",f"{c}:{f}")):date=d;break
        for dep in DEPS.get(path,[]):
            d=_git("log","-1","--format=%cs","--",dep).strip()
            if d and (date is None or d>date):date=d
        m[path]={"hash":digest(path,doc),"lastmod":date}
    save(m);print("seeded",len(m),"pages")
if __name__=="__main__" and sys.argv[1:]==["seed"]:seed()
