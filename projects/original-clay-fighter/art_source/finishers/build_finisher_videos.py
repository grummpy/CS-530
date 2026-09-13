"""Render twelve editable, non-photoreal clay finisher animatics and MP4s.

Each sequence is 3 seconds at 10 fps. The PNG frames are the runtime source;
the MP4 is a review/export deliverable encoded from those same frames.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "finishers"; OUT.mkdir(parents=True, exist_ok=True)
FIGHTERS = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
PALETTES = {"rhinestone_angel":((227,65,138),(255,202,66)),"mr_president":((255,94,0),(23,54,110)),"tech_billionaire":((24,214,220),(72,75,82)),"master_chef":((246,225,188),(239,148,87))}
MODES = {"rhinestone_angel":"five-beat star-guitar clay crush","mr_president":"rotary-phone airstrike confetti blast","tech_billionaire":"satellite-orb clay disassembly","master_chef":"knife-and-salmon kitchen rush"}

def puppet(draw, x, y, body, accent, defeated=False):
    if defeated:
        draw.ellipse((x-70,y-15,x+72,y+26),fill=(126,24,32),outline=(32,18,26),width=3); return
    draw.ellipse((x-20,y-110,x+20,y-70),fill=(238,145,94),outline=(32,25,30),width=3)
    draw.rounded_rectangle((x-30,y-70,x+30,y),radius=10,fill=body,outline=(32,25,30),width=3)
    draw.rectangle((x-25,y,x-6,y+70),fill=body,outline=(32,25,30),width=3);draw.rectangle((x+6,y,x+25,y+70),fill=body,outline=(32,25,30),width=3)
    draw.line((x-28,y-55,x-55,y-25),fill=accent,width=8);draw.line((x+28,y-55,x+55,y-25),fill=accent,width=8)

def render(winner, loser, frame):
    w,h=640,360; im=Image.new("RGB",(w,h),(37,39,49)); d=ImageDraw.Draw(im); body,accent=PALETTES[winner]; lbody,laccent=PALETTES[loser]
    d.rectangle((0,262,w,h),fill=(77,71,65)); d.text((18,16),f"{winner.replace('_',' ').upper()}  //  FINISHER",fill=(238,236,225))
    beat=frame//6; defeated=beat>=4
    puppet(d,180,250,body,accent); puppet(d,465,250,lbody,laccent,defeated)
    # Distinct non-photoreal action language for each winner.
    if winner=="rhinestone_angel":
        d.polygon([(210,148),(245,192),(188,192)],fill=accent); d.line((180,185,430,210),fill=(114,50,160),width=16)
        for i in range(min(beat,5)): d.ellipse((415-i*12,165-i*8,435-i*12,185-i*8),fill=(255,205,52))
    elif winner=="mr_president":
        d.rounded_rectangle((130,140,180,185),radius=6,fill=(24,37,65)); d.ellipse((143,151,153,161),fill=(255,104,0));
        if beat>=2:
            for jetx in (240,340,440): d.polygon([(jetx,80),(jetx+28,88),(jetx,96)],fill=(140,153,164)); d.line((jetx+8,96,jetx+8,190),fill=(255,188,46),width=4)
    elif winner=="tech_billionaire":
        d.ellipse((145,125,185,165),outline=accent,width=8)
        for i in range(beat+1): d.ellipse((415+i*9,160-i*10,435+i*9,180-i*10),fill=accent,outline=(20,30,35),width=2)
    else:
        d.line((155,190,260,145),fill=(215,220,225),width=9); d.ellipse((242,145,275,205),fill=(235,145,93)); d.polygon([(275,160),(300,145),(292,180)],fill=(48,84,107))
    if defeated:
        for i in range(24):
            px=430+(i*29)%150; py=210+(i*17)%75; d.ellipse((px,py,px+9,py+7),fill=((156,28,38) if i%2 else (236,80,58)))
        d.text((236,315),"CLAY SPLAT!",fill=(255,226,160))
    return im

for winner in FIGHTERS:
    for loser in FIGHTERS:
        if winner==loser: continue
        ident=f"{winner}_vs_{loser}"; directory=OUT/ident/"frames"; directory.mkdir(parents=True,exist_ok=True)
        for frame in range(30): render(winner,loser,frame).save(directory/f"{frame:03}.png")
        subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","10","-i",str(directory/"%03d.png"),"-pix_fmt","yuv420p","-movflags","+faststart",str(OUT/f"{ident}.mp4")],check=True)
