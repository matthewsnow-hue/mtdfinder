import re,sys,subprocess,html
f=sys.argv[1]; extra=sys.argv[2:]
h=open(f).read()
m=re.search(r'<form[^>]*action="([^"]*)".*?</form>',h,re.S)
form=m.group(0); act=m.group(1)
t=re.search(r'name="csrfToken" value="([^"]*)"',form).group(1)
print("ACTION",act)
for n,v in re.findall(r'name="([^"]+)"[^>]*value="([^"]*)"',form): print(" opt",n,v)
if extra:
  args=["curl","-sL","-c","cj","-b","cj","-o","out.html","-w","%{url_effective}","--data-urlencode","csrfToken="+t]
  for e in extra: args+=["--data-urlencode",e]
  args.append("https://www.tax.service.gov.uk"+html.unescape(act))
  print(subprocess.run(args,capture_output=True,text=True).stdout)
