#!/usr/bin/env python3
"""Social preview (Open Graph / Twitter card) images for MTD Finder.

Run: python3 tools/og_images.py   -> writes assets/og/*.png (1200x630)

Fonts: Literata (headings, Light) and Instrument Sans (body), as on the site.
Looks for them in the system font folders first, then in ~/.cache/mtdfinder-fonts,
and downloads them from the Google Fonts repo on GitHub if neither has them.
Wording on the cards is taken from the page titles/headings only. Wrap a phrase
in *asterisks* to colour it green, like the <em> accents on the site.
"""
import os,glob,urllib.request
from PIL import Image,ImageDraw,ImageFont

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"assets","og")
W,H=1200,627               # LinkedIn's recommended 1.91:1 size
M=84                      # safe margin all round (LinkedIn/X crop very little at 1.91:1)
BG="#f6f5f1";PAPER="#fdfdfb";INK="#0e1b26";MUTED="#5a6470";LINE="#e3e2dc";ACCENT="#1b6b4f";SOFT="#dfece5"

# slug -> (eyebrow, title, subtitle). Titles mirror each page's <h1>/<title>.
CARDS={
 "default":("Independent · Not affiliated with HMRC","MTD *Finder*","Free Making Tax Digital checker and software finder"),
 "deadline-calendar":("Guide · Free download","MTD deadline *calendar* and checklist","For 2026 to 2027"),
 "7-november-deadline":("Guide · Deadline","MTD 7 November *deadline*","What to send, and what happens if you're late"),
 "30k-threshold-april-2027":("Guide · April 2027","Do I need MTD at *£30,000*?","Your April 2027 checklist"),
}

FONTS={"serif":("Literata*VariableFont_opsz,wght.ttf","Literata[opsz,wght].ttf","https://github.com/google/fonts/raw/main/ofl/literata/Literata%5Bopsz,wght%5D.ttf"),
       "sans":("InstrumentSans-VariableFont_wdth,wght.ttf","InstrumentSans[wdth,wght].ttf","https://github.com/google/fonts/raw/main/ofl/instrumentsans/InstrumentSans%5Bwdth,wght%5D.ttf")}
CACHE=os.path.expanduser("~/.cache/mtdfinder-fonts")

def font_path(kind):
    pat,name,url=FONTS[kind]
    for d in ("/usr/share/fonts","/usr/local/share/fonts",os.path.expanduser("~/.fonts"),os.path.expanduser("~/.local/share/fonts")):
        hits=[h for h in glob.glob(os.path.join(d,"**",pat),recursive=True) if "Italic" not in os.path.basename(h)]
        if hits:return hits[0]
    p=os.path.join(CACHE,name)
    if not os.path.exists(p):
        os.makedirs(CACHE,exist_ok=True);print("downloading",url);urllib.request.urlretrieve(url,p)
    return p

def serif(size,wght=300):
    f=ImageFont.truetype(font_path("serif"),size);f.set_variation_by_axes([72 if size>=40 else 12,wght]);return f
def sans(size,wght=400):
    f=ImageFont.truetype(font_path("sans"),size);f.set_variation_by_axes([100,wght]);return f

TILE=100                  # mark size on the cards, px
def mark(size):
    """The stacked-TD mark from tools/mark.py: assets/logo.png (rendered from the same geometry as
    assets/mark.svg) downsampled, with mark.svg's corner radius. Run tools/mark.py first if the mark changes."""
    import importlib.util
    spec=importlib.util.spec_from_file_location("mark",os.path.join(ROOT,"tools","mark.py"));mk=importlib.util.module_from_spec(spec);spec.loader.exec_module(mk)
    ss=4;big=Image.open(os.path.join(ROOT,"assets","logo.png")).convert("RGB").resize((size*ss,size*ss),Image.LANCZOS)
    mask=Image.new("L",big.size,0);ImageDraw.Draw(mask).rounded_rectangle([0,0,size*ss-1,size*ss-1],radius=round(mk.RADIUS*size*ss/mk.UNIT),fill=255)
    big.putalpha(mask);return big.resize((size,size),Image.LANCZOS)

def runs(text):
    """'Do I need *£30,000*?' -> words, each a list of (piece, is_accent), so punctuation hugs the accent."""
    words=[[]];
    for i,part in enumerate(text.split("*")):
        acc=i%2==1
        for j,chunk in enumerate(part.split(" ")):
            if j>0 and words[-1]:words.append([])
            if chunk:words[-1].append((chunk,acc))
    return [w for w in words if w]

def wlen(draw,word,font):return sum(draw.textlength(t,font=font) for t,_ in word)

def wrap(words,font,maxw,draw):
    sp=draw.textlength(" ",font=font)
    def fill(limit):
        lines=[[]];cur=0
        for w in words:
            lw=wlen(draw,w,font)
            if lines[-1] and cur+sp+lw>limit:lines.append([]);cur=0
            cur+=(sp if lines[-1] else 0)+lw;lines[-1].append(w)
        return lines
    lines=fill(maxw);n=len(lines);lim=maxw
    while n>1 and lim>maxw*0.5:          # balance lines so there's no lone last word
        t=fill(lim-10)
        if len(t)>n:break
        lines=t;lim-=10
    return lines

def draw_line(draw,x,y,line,font,col,acc):
    sp=draw.textlength(" ",font=font)
    for w in line:
        for t,a in w:
            draw.text((x,y),t,font=font,fill=acc if a else col);x+=draw.textlength(t,font=font)
        x+=sp

def tracked(draw,xy,text,font,fill,track):
    x,y=xy
    for ch in text:
        draw.text((x,y),ch,font=font,fill=fill);x+=draw.textlength(ch,font=font)+track
    return x

def card(slug,eyebrow,title,sub):
    im=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,14],fill=ACCENT)                     # green band, top
    # brand row: logo + wordmark
    mk=mark(TILE);im.paste(mk,(M,M-26),mk)
    wm=serif(46,400);bx=M+TILE+22;by=M-26+TILE//2
    if slug!="default":   # the default card already has the name as its headline
        d.text((bx,by),"MTD ",font=wm,fill=INK,anchor="lm");d.text((bx+d.textlength("MTD ",font=wm),by),"Finder",font=wm,fill=ACCENT,anchor="lm")
    # eyebrow, right aligned on the brand row
    eb=sans(20,500);t=3.2
    ebw=sum(d.textlength(c,font=eb)+t for c in eyebrow.upper())-t
    tracked(d,(W-M-ebw,by-12),eyebrow.upper(),eb,MUTED,t)
    # title: largest size that fits in 3 lines (default card gets a bigger cap)
    maxw=W-2*M;top=M+110;bottom=H-M-60
    for size in range(150 if slug=="default" else 96,52,-2):
        tf=serif(size,300);lines=wrap(runs(title),tf,maxw,d);lh=int(size*1.1)
        sf=sans(max(30,int(size*0.42)),400);sub_lines=wrap(runs(sub),sf,maxw,d) if sub else []
        sh=len(sub_lines)*int(sf.size*1.3)
        total=len(lines)*lh+(36+sh if sub else 0)
        if len(lines)<=3 and len(sub_lines)<=2 and total<=bottom-top:break
    y=top+((bottom-top)-total)//2
    for ln in lines:
        draw_line(d,M,y,ln,tf,INK,ACCENT);y+=lh
    if sub:
        y+=36
        for ln in sub_lines:
            draw_line(d,M,y,ln,sf,MUTED,MUTED);y+=int(sf.size*1.3)
    # footer: rule + domain
    d.line([M,H-M-14,W-M,H-M-14],fill=LINE,width=2)
    ff=sans(26,500)
    d.text((M,H-M+4),"mtdfinder.co.uk",font=ff,fill=ACCENT,anchor="lm")
    os.makedirs(OUT,exist_ok=True);p=os.path.join(OUT,f"{slug}.png")
    im.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(p,optimize=True)
    return p

if __name__=="__main__":
    import shutil,sys
    paths=[]
    for slug,(e,t,s) in CARDS.items():
        p=card(slug,e,t,s);paths.append(p);print(p,os.path.getsize(p)//1024,"KB")
    # optional: python3 tools/og_images.py --export DIR  -> review copies, LinkedIn uploads, contact sheet
    if "--export" in sys.argv:
        out=sys.argv[sys.argv.index("--export")+1];up=os.path.join(out,"linkedin-upload");os.makedirs(up,exist_ok=True)
        for p in paths:
            shutil.copy(p,out)
            if not p.endswith("default.png"):shutil.copy(p,up)
        sheet=Image.new("RGB",(W,len(paths)*(H+10)-10),"white")
        for i,p in enumerate(paths):sheet.paste(Image.open(p).convert("RGB"),(0,i*(H+10)))
        sheet.resize((600,sheet.height//2),Image.LANCZOS).save(os.path.join(out,"contact-sheet.png"),optimize=True)
        print("exported to",out)
