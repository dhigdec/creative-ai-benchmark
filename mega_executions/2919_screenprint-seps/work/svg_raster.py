"""Minimal SVG path rasterizer (M/L/C/Z, absolute) for the vectorized lettering plate.
Renders filled paths into a PIL image. The vectorize output fills letters; we render
them as solid ink on a chosen ground so the vector plate can be shown in the contact sheet.
"""
import re, sys
from PIL import Image, ImageDraw

def flatten_path(d, steps=12):
    # returns list of subpaths, each a list of (x,y)
    toks = re.findall(r'[MLCZmlczHhVv]|-?\d*\.?\d+(?:[eE][-+]?\d+)?', d)
    subpaths, cur, start = [], [], (0,0)
    pos = (0,0); i=0; cmd=None
    def num():
        nonlocal i
        v=float(toks[i]); i+=1; return v
    while i < len(toks):
        t = toks[i]
        if t in 'MLCZHV':
            cmd=t; i+=1
        else:
            # implicit repeat of last cmd
            pass
        if cmd=='M':
            if cur: subpaths.append(cur); cur=[]
            x=num(); y=num(); pos=(x,y); start=pos; cur=[pos]
            cmd='L'
        elif cmd=='L':
            x=num(); y=num(); pos=(x,y); cur.append(pos)
        elif cmd=='H':
            x=num(); pos=(x,pos[1]); cur.append(pos)
        elif cmd=='V':
            y=num(); pos=(pos[0],y); cur.append(pos)
        elif cmd=='C':
            x1=num();y1=num();x2=num();y2=num();x=num();y=num()
            p0=pos
            for s in range(1,steps+1):
                tt=s/steps; mt=1-tt
                bx=mt*mt*mt*p0[0]+3*mt*mt*tt*x1+3*mt*tt*tt*x2+tt*tt*tt*x
                by=mt*mt*mt*p0[1]+3*mt*mt*tt*y1+3*mt*tt*tt*y2+tt*tt*tt*y
                cur.append((bx,by))
            pos=(x,y)
        elif cmd=='Z':
            if cur: cur.append(start); subpaths.append(cur); cur=[]
            pos=start
        else:
            i+=1
    if cur: subpaths.append(cur)
    return subpaths

def render(svg_path, out_path, W, H, ink=(255,255,255), ground=(0,0,0)):
    s=open(svg_path).read()
    m=re.search(r'width="(\d+)"',s); sw=int(m.group(1)) if m else W
    m=re.search(r'height="(\d+)"',s); sh=int(m.group(1)) if m else H
    img=Image.new('RGBA',(sw,sh),tuple(ground)+(255,))
    dr=ImageDraw.Draw(img)
    for d in re.findall(r'<path[^>]*\bd="([^"]+)"',s):
        for sp in flatten_path(d):
            if len(sp)>=3:
                dr.polygon(sp, fill=tuple(ink)+(255,))
    img=img.resize((W,H), Image.LANCZOS)
    img.convert('RGB').save(out_path)
    return img.size

if __name__=='__main__':
    svg,out,W,H=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
    ink=(255,255,255); ground=(0,0,0)
    if len(sys.argv)>5:
        ink=tuple(int(x) for x in sys.argv[5].split(','))
    if len(sys.argv)>6:
        ground=tuple(int(x) for x in sys.argv[6].split(','))
    print('rendered', render(svg,out,W,H,ink,ground))
