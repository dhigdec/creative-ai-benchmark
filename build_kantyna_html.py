#!/usr/bin/env python3
import json, os
RUN = open("/tmp/kantyna_run.txt").read().strip()
U = json.load(open(f"{RUN}/_datauris.json"))  # scallops, schnitzel, interior, pierogi, zurek, sernik

# palette
GROUND="#0E0E10"; PANEL="#16161A"; INK="#EDE7DB"; MUT="#9A9186"; LINE="#2A2A2E"; GOLD="#B08A46"
DISP='"gastromond", Georgia, serif'; TEXT='"ivyora-text", Georgia, serif'

def img(src, style):  # object-fit cover box
    return f'<div style="position:absolute;overflow:hidden;{style}"><img src="{src}" style="width:100%;height:100%;object-fit:cover;display:block"></div>'

CSS = f"""
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
.slide{{position:relative;overflow:hidden;background:{GROUND};color:{INK};font-family:{TEXT};font-weight:400}}
.disp{{font-family:{DISP};font-weight:400}}
.ey{{font-family:{TEXT};font-weight:500;letter-spacing:.32em;text-transform:uppercase;color:{GOLD}}}
.mut{{color:{MUT}}}
.price{{font-family:{TEXT};font-weight:500;color:{INK}}}
table{{border-collapse:collapse;width:100%}}
td,th{{text-align:left;font-family:{TEXT};font-weight:400}}
</style>
"""

slides=[]

# ---------- MENU PAGE 1 (A4 794x1123) : chef's tasting ----------
courses=[
 ("I","Seared Scallop","celeriac veloute, brown butter, sea herbs"),
 ("II","Wild Mushroom Pierogi","smoked cream, aged comte, chive oil"),
 ("III","Sour Rye Soup","white sausage, soft quail egg, horseradish"),
 ("IV","Veal Schnitzel","lingonberry, braised red cabbage, dill"),
 ("V","Baked Cheesecake","wildflower honey, poppy seed, creme fraiche"),
]
rows=""
for num,name,desc in courses:
    rows+=f"""<div style="display:flex;gap:22px;padding:19px 0;border-top:1px solid {LINE}">
      <div class="disp" style="font-size:19px;color:{GOLD};width:34px;flex:none;padding-top:3px">{num}</div>
      <div style="flex:1">
        <div class="disp" style="font-size:25px;line-height:1.15;color:{INK}">{name}</div>
        <div class="mut" style="font-size:14px;line-height:1.5;margin-top:5px">{desc}</div>
      </div></div>"""
slides.append(f"""<div class="slide" data-canvas-width="794" data-canvas-height="1123" style="width:794px;height:1123px">
  {img(U['scallops'],'left:0;top:0;width:794px;height:300px;opacity:.9')}
  <div style="position:absolute;left:0;top:0;width:794px;height:300px;background:linear-gradient(180deg,rgba(14,14,16,.35),rgba(14,14,16,.95))"></div>
  <div style="position:absolute;left:64px;top:196px;right:64px">
     <div class="ey" style="font-size:12px">Copenhagen</div>
     <div class="disp" style="font-size:52px;line-height:1;margin-top:8px">Kantyna Nova</div>
  </div>
  <div style="position:absolute;left:64px;top:360px;right:64px">
     <div class="ey" style="font-size:12px;margin-bottom:6px">Chef's Tasting Menu</div>
     <div class="mut" style="font-size:13.5px;line-height:1.6;max-width:560px">Five courses drawn from a Central European winter larder, plated one at a time. Please advise us of dietary needs when you arrive.</div>
     <div style="margin-top:14px;border-bottom:1px solid {LINE}">{rows}</div>
     <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:26px">
        <div class="disp" style="font-size:22px">Five courses</div>
        <div class="price" style="font-size:22px;color:{GOLD}">$185</div>
     </div>
     <div class="mut" style="font-size:12px;margin-top:8px">Wine pairing available. Please see the following page.</div>
  </div>
</div>""")

# ---------- MENU PAGE 2 (A4) : wine pairing table ----------
wines=[
 ("Scallop","Chablis 1er Cru","Burgundy","$26"),
 ("Pierogi","Gruner Veltliner","Kamptal","$19"),
 ("Sour Rye","Dry Riesling","Mosel","$18"),
 ("Schnitzel","Barolo","Piedmont","$28"),
 ("Cheesecake","Tokaji late harvest","Tokaj","$22"),
]
wrows=""
for course,wine,region,price in wines:
    wrows+=f"""<tr>
      <td style="padding:16px 0;border-top:1px solid {LINE};width:26%"><span class="mut" style="font-size:12px;letter-spacing:.06em;text-transform:uppercase">{course}</span></td>
      <td style="padding:16px 0;border-top:1px solid {LINE}"><span class="disp" style="font-size:20px">{wine}</span><br><span class="mut" style="font-size:12.5px">{region}</span></td>
      <td style="padding:16px 0;border-top:1px solid {LINE};text-align:right;width:16%"><span class="price" style="font-size:17px;color:{GOLD}">{price}</span></td>
    </tr>"""
slides.append(f"""<div class="slide" data-canvas-width="794" data-canvas-height="1123" style="width:794px;height:1123px">
  <div style="position:absolute;left:64px;top:72px;right:64px">
    <div class="ey" style="font-size:12px">Kantyna Nova</div>
    <div class="disp" style="font-size:40px;margin-top:8px">Wine Pairing</div>
    <div class="mut" style="font-size:13px;line-height:1.6;margin-top:10px;max-width:520px">A glass chosen for each course by our sommelier. The full pairing is $95 when taken with the tasting menu.</div>
    <table style="margin-top:22px">{wrows}</table>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:22px;border-top:1px solid {LINE};padding-top:18px">
       <div class="disp" style="font-size:20px">Full pairing, five glasses</div>
       <div class="price" style="font-size:20px;color:{GOLD}">+$95</div>
    </div>
  </div>
  {img(U['pierogi'],f'left:64px;top:760px;width:666px;height:300px;border:1px solid {LINE}')}
</div>""")

# ---------- DECK SLIDE 1 (1920x1080) : concept ----------
slides.append(f"""<div class="slide" data-canvas-width="1920" data-canvas-height="1080" style="width:1920px;height:1080px">
  {img(U['interior'],'left:0;top:0;width:1920px;height:1080px;opacity:.85')}
  <div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:linear-gradient(90deg,rgba(14,14,16,.92)0%,rgba(14,14,16,.55)55%,rgba(14,14,16,.2)100%)"></div>
  <div style="position:absolute;left:120px;top:392px;max-width:900px">
    <div class="ey" style="font-size:16px">Partner Deck . Copenhagen</div>
    <div class="disp" style="font-size:92px;line-height:.98;margin-top:14px">Kantyna Nova</div>
    <div style="font-size:23px;line-height:1.5;color:{INK};margin-top:22px;max-width:640px">A modern tasting-menu house reworking a Central European table for an evening that lasts. Twenty-eight seats, one seating a night.</div>
  </div>
</div>""")

# ---------- DECK SLIDE 2 (1920x1080) : the range (5 dishes, cross-consistency) ----------
dishes=[("scallops","Seared Scallop"),("pierogi","Wild Mushroom Pierogi"),("zurek","Sour Rye Soup"),("schnitzel","Veal Schnitzel"),("sernik","Baked Cheesecake")]
cards=""
cw=300; gap=30; x0=120
for i,(k,label) in enumerate(dishes):
    x=x0+i*(cw+gap)
    cards+=f"""{img(U[k],f'left:{x}px;top:300px;width:{cw}px;height:360px;border:1px solid {LINE}')}
    <div style="position:absolute;left:{x}px;top:672px;width:{cw}px" class="mut"><span style="font-family:{DISP};font-size:19px;color:{INK}">{label}</span></div>"""
slides.append(f"""<div class="slide" data-canvas-width="1920" data-canvas-height="1080" style="width:1920px;height:1080px">
  <div style="position:absolute;left:120px;top:120px">
    <div class="ey" style="font-size:16px">The Menu</div>
    <div class="disp" style="font-size:58px;margin-top:10px">One winter table, five courses</div>
    <div class="mut" style="font-size:18px;margin-top:12px;max-width:900px">Every plate graded to one house look so the range reads as a single evening, not five photographs.</div>
  </div>
  {cards}
</div>""")

# ---------- DECK SLIDE 3 (1920x1080) : price ladder (table) ----------
ladder=[("Chef's Tasting","five courses","$185"),("Wine Pairing","five glasses","+$95"),("Reserve Pairing","rare and back-vintage","+$180"),("Corkage","per 750ml bottle","$45")]
lrows=""
for name,note,price in ladder:
    lrows+=f"""<tr>
      <td style="padding:26px 0;border-top:1px solid {LINE}"><span class="disp" style="font-size:34px">{name}</span></td>
      <td style="padding:26px 0;border-top:1px solid {LINE}"><span class="mut" style="font-size:18px">{note}</span></td>
      <td style="padding:26px 0;border-top:1px solid {LINE};text-align:right"><span class="price" style="font-size:34px;color:{GOLD}">{price}</span></td>
    </tr>"""
slides.append(f"""<div class="slide" data-canvas-width="1920" data-canvas-height="1080" style="width:1920px;height:1080px">
  <div style="position:absolute;left:120px;top:130px;right:120px">
    <div class="ey" style="font-size:16px">What a seat costs</div>
    <div class="disp" style="font-size:64px;margin-top:12px">The price ladder</div>
    <table style="margin-top:40px">{lrows}</table>
    <div class="mut" style="font-size:16px;margin-top:34px">Average spend per guest, food and pairing, $280 before service. One seating a night, twenty-eight covers.</div>
  </div>
</div>""")

# ---------- RESERVATIONS ONE-PAGER (1200x1600 web) ----------
hours=[("Tuesday","6:00 pm . one seating"),("Wednesday","6:00 pm . one seating"),("Thursday","6:00 pm . one seating"),("Friday","6:00 pm . one seating"),("Saturday","5:30 pm . one seating"),("Sunday","5:30 pm . one seating"),("Monday","Closed")]
hrows=""
for day,val in hours:
    hrows+=f"""<tr><td style="padding:13px 0;border-top:1px solid {LINE}"><span class="disp" style="font-size:19px">{day}</span></td>
      <td style="padding:13px 0;border-top:1px solid {LINE};text-align:right"><span class="mut" style="font-size:14px">{val}</span></td></tr>"""
slides.append(f"""<div class="slide" data-canvas-width="1200" data-canvas-height="1600" style="width:1200px;height:1600px">
  {img(U['sernik'],'left:0;top:0;width:1200px;height:520px;opacity:.9')}
  <div style="position:absolute;left:0;top:0;width:1200px;height:520px;background:linear-gradient(180deg,rgba(14,14,16,.25),rgba(14,14,16,.9))"></div>
  <div style="position:absolute;left:90px;top:300px;right:90px">
    <div class="ey" style="font-size:13px">Reservations</div>
    <div class="disp" style="font-size:66px;line-height:1;margin-top:10px">Book a table</div>
  </div>
  <div style="position:absolute;left:90px;top:600px;width:620px">
     <div class="mut" style="font-size:15px;line-height:1.6">The tasting menu is served to the whole table. Reservations open six weeks ahead and are held with a card. We ask that you let us know of changes at least forty-eight hours before.</div>
     <table style="margin-top:26px">{hrows}</table>
  </div>
  <div style="position:absolute;left:760px;top:600px;width:350px;background:{PANEL};border:1px solid {LINE};padding:34px">
     <div class="ey" style="font-size:12px">Reserve</div>
     <div class="disp" style="font-size:30px;margin-top:8px;line-height:1.1">Call the room</div>
     <div class="price" style="font-size:22px;color:{GOLD};margin-top:16px">+45 33 12 40 60</div>
     <div class="mut" style="font-size:14px;line-height:1.7;margin-top:18px">48 Harbour Lane<br>Copenhagen 1051<br>reservations@kantynanova.example</div>
  </div>
</div>""")

# ---------- SOCIAL SET : 1:1, 4:5, 9:16 (mixed canvas in one doc) ----------
def social(w,h,src,head_px,name_px):
    return f"""<div class="slide" data-canvas-width="{w}" data-canvas-height="{h}" style="width:{w}px;height:{h}px">
      {img(src,f'left:0;top:0;width:{w}px;height:{h}px;opacity:.88')}
      <div style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;background:linear-gradient(180deg,rgba(14,14,16,.15),rgba(14,14,16,.9))"></div>
      <div style="position:absolute;left:{int(w*0.08)}px;bottom:{int(h*0.09)}px;right:{int(w*0.08)}px">
        <div class="ey" style="font-size:{head_px}px">Now taking December</div>
        <div class="disp" style="font-size:{name_px}px;line-height:1;margin-top:10px">Kantyna Nova</div>
        <div class="mut" style="font-size:{head_px+4}px;margin-top:10px">Chef's tasting, five courses, $185</div>
      </div>
    </div>"""
slides.append(social(1080,1080,U['scallops'],15,64))
slides.append(social(1080,1350,U['schnitzel'],15,64))
slides.append(social(1080,1920,U['pierogi'],17,74))

html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="hz:slide-selector" content=".slide">
<title>Kantyna Nova collateral</title>
<link rel="stylesheet" href="https://use.typekit.net/ycu8eys.css">
{CSS}</head><body>
{''.join(slides)}
</body></html>"""

open(f"{RUN}/kantyna_collateral.html","w").write(html)
# em-dash guard
bad = html.count("—")
print("wrote kantyna_collateral.html", len(html.encode())//1024,"KB ; slides:",len(slides),"; em-dashes:",bad)
