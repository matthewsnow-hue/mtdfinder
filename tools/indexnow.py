#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver...) with changed URLs.
Usage:  python3 tools/indexnow.py https://mtdfinder.co.uk/page/ [...]
        python3 tools/indexnow.py --sitemap      (all URLs in sitemap.xml)
Only run after the key file is live at https://mtdfinder.co.uk/<key>.txt."""
import json,os,re,sys,urllib.request
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY=re.search(r'INDEXNOW_KEY="([0-9a-f]+)"',open(f"{ROOT}/tools/build.py").read()).group(1)
HOST="mtdfinder.co.uk"
urls=re.findall(r"<loc>(.*?)</loc>",open(f"{ROOT}/sitemap.xml").read()) if "--sitemap" in sys.argv else [u for u in sys.argv[1:] if u.startswith("https://"+HOST)]
if not urls:sys.exit("No URLs given (must be on https://"+HOST+")")
body=json.dumps({"host":HOST,"key":KEY,"keyLocation":f"https://{HOST}/{KEY}.txt","urlList":urls}).encode()
req=urllib.request.Request("https://api.indexnow.org/indexnow",data=body,headers={"Content-Type":"application/json; charset=utf-8"})
try:
    r=urllib.request.urlopen(req,timeout=30);print("HTTP",r.status,"for",len(urls),"URLs",r.read().decode()[:200])
except urllib.error.HTTPError as e:
    print("HTTP",e.code,e.read().decode()[:300]);sys.exit(1)
