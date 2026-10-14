import re,json,sys
def parse(f):
  h=open(f).read(); out={}
  for blk in re.findall(r'<div id="software-vendor-\d+">(.*?)</p>\s*</div>',h,re.S):
    name=re.search(r'<h3[^>]*>\s*(.*?)\s*</h3>',blk,re.S).group(1).strip()
    d={k.strip():v.strip() for k,v in re.findall(r'__key">\s*(.*?)\s*</dt>\s*<dd class="govuk-summary-list__value">\s*(.*?)\s*</dd>',blk,re.S)}
    pid=re.search(r'productId=(\d+)',blk).group(1)
    out[pid]=dict(name=name,**d)
  return out
