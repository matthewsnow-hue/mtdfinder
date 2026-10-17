#!/usr/bin/env python3
"""MTD Finder mark, option B 'stacked TD' (chosen by Matthew, 17 Oct 2026). One geometry for every output.

Run: python3 tools/mark.py
Writes:
  assets/mark.svg              master: rounded green tile, white serif M with T over D (letters as paths,
                               so it looks the same everywhere, no font needed). Also the SVG favicon.
  assets/favicon-32.png        PNG favicon fallback (rendered from mark.svg)
  assets/apple-touch-icon.png  180x180, full-bleed square (iOS rounds the corners itself)
  assets/logo.png              512x512 schema logo, full-bleed square like the old one
  favicon.ico                  16/32/48 for anything that asks for /favicon.ico
Rendering uses headless Chrome via Playwright (same engine as the screenshots).
og_images.py and the site header use the same numbers from this file.

Geometry, in a 60-unit tile (the signature spec was M 32 / T,D 13; T and D are enlarged so they
read at feed and favicon size):
  TD   = 17   font size of T and D
  GAP  = 2    space between M and the T/D column, and between T and D
  the M is sized so its cap height equals T cap + GAP + D cap (T top = M top, D foot = M baseline)
  RADIUS = 8, green #1b6b4f, white Gelasio Regular (a metric match for Georgia, from Google Fonts)
"""
import os,glob,urllib.request
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GREEN="#1b6b4f";UNIT=60;RADIUS=8;TD=17;GAP=2
FONT_URL="https://github.com/google/fonts/raw/main/ofl/gelasio/Gelasio%5Bwght%5D.ttf"

def font_file():
    hits=[h for d in ("/usr/share/fonts","/usr/local/share/fonts",os.path.expanduser("~/.fonts")) for h in glob.glob(d+"/**/Gelasio-VariableFont_wght.ttf",recursive=True)]
    if hits:return hits[0]
    p=os.path.expanduser("~/.cache/mtdfinder-fonts/Gelasio[wght].ttf")
    if not os.path.exists(p):os.makedirs(os.path.dirname(p),exist_ok=True);urllib.request.urlretrieve(FONT_URL,p)
    return p

def letters():
    """Returns [(svg path d, ), ...] for M, T, D laid out in the 60-unit tile (y down)."""
    f=TTFont(font_file());gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f["head"].unitsPerEm
    def bounds(ch):
        bp=BoundsPen(gs);gs[cmap[ord(ch)]].draw(bp);return bp.bounds   # xmin,ymin,xmax,ymax font units
    bT,bD,bM=bounds("T"),bounds("D"),bounds("M")
    k_td=TD/upm
    capT=(bT[3]-bT[1])*k_td;capD=(bD[3]-bD[1])*k_td
    capM=capT+GAP+capD;k_m=capM/(bM[3]-bM[1])
    wM=(bM[2]-bM[0])*k_m;wT=(bT[2]-bT[0])*k_td;wD=(bD[2]-bD[0])*k_td;wS=max(wT,wD)
    x0=(UNIT-(wM+GAP+wS))/2;top=(UNIT-capM)/2
    out=[]
    def place(ch,b,k,x,ytop):
        pen=SVGPathPen(gs,ntos=lambda v:("%.2f"%v).rstrip("0").rstrip("."))
        # font y-up -> svg y-down; glyph bbox left/top lands at (x,ytop)
        tp=TransformPen(pen,(k,0,0,-k,x-b[0]*k,ytop+b[3]*k))
        gs[cmap[ord(ch)]].draw(tp);out.append(pen.getCommands())
    place("M",bM,k_m,x0,top)
    xs=x0+wM+GAP
    place("T",bT,k_td,xs+(wS-wT)/2,top)
    place("D",bD,k_td,xs+(wS-wD)/2,top+capT+GAP)
    return out,dict(m_size=round(k_m*upm,2),td_size=TD,cap_m=round(capM,2),width=round(wM+GAP+wS,2))

def svg(rounded=True,size=None):
    paths,_=letters()
    attr=f' width="{size}" height="{size}"' if size else ""
    rx=f' rx="{RADIUS}"' if rounded else ""
    d="".join(f'<path d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {UNIT} {UNIT}"{attr} role="img" aria-label="MTD Finder">'
            f'<rect width="{UNIT}" height="{UNIT}"{rx} fill="{GREEN}"/><g fill="#fff">{d}</g></svg>')

def inline_svg(css_class="mark"):
    """Small decorative copy for the site header (the wordmark next to it carries the name)."""
    paths,_=letters()
    d="".join(f'<path d="{p}"/>' for p in paths)
    return (f'<svg class="{css_class}" viewBox="0 0 {UNIT} {UNIT}" aria-hidden="true" focusable="false">'
            f'<rect width="{UNIT}" height="{UNIT}" rx="{RADIUS}" fill="{GREEN}"/><g fill="#fff">{d}</g></svg>')

def render(svg_text,size,path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        exe="/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b=p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg=b.new_page(viewport={"width":size,"height":size})
        pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg_text.replace('<svg ',f'<svg width=\"{size}\" height=\"{size}\" style=\"display:block\" ',1)}</body></html>")
        pg.screenshot(path=path,omit_background=True);b.close()
    from PIL import Image
    Image.open(path).save(path,optimize=True)

if __name__=="__main__":
    A=os.path.join(ROOT,"assets")
    open(os.path.join(A,"mark.svg"),"w").write(svg()+"\n")
    render(svg(),32,os.path.join(A,"favicon-32.png"))
    render(svg(rounded=False),180,os.path.join(A,"apple-touch-icon.png"))
    render(svg(rounded=False),512,os.path.join(A,"logo.png"))
    from PIL import Image
    im=Image.open(os.path.join(A,"logo.png")).convert("RGB");im.save(os.path.join(A,"logo.png"),optimize=True)
    im=Image.open(os.path.join(A,"apple-touch-icon.png")).convert("RGB");im.save(os.path.join(A,"apple-touch-icon.png"),optimize=True)
    # favicon.ico for browsers and tools that ask for /favicon.ico (16, 32, 48 from one 256px render)
    tmp=os.path.join(A,"_ico.png");render(svg(),256,tmp)
    Image.open(tmp).convert("RGBA").save(os.path.join(ROOT,"favicon.ico"),sizes=[(16,16),(32,32),(48,48)]);os.remove(tmp)
    print(letters()[1])
    for n in ("mark.svg","favicon-32.png","apple-touch-icon.png","logo.png"):print(n,os.path.getsize(os.path.join(A,n)),"bytes")
