"""Create the transparent runtime pose library for the original Mr. President.

This is a deterministic Pillow fallback while the local Blender executable is
unavailable. It is intentionally retained as editable source: replace its
draw routines with a Blender export once Blender is accessible, keeping the
clip names, dimensions, and ground pivot unchanged.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets" / "characters" / "mr_president" / "sprites"
OUT.mkdir(parents=True, exist_ok=True)
W = H = 512

NAVY = (21, 48, 100, 255); NAVY_DARK = (12, 29, 66, 255)
ORANGE = (255, 94, 0, 255); HAIR = (242, 194, 76, 255)
WHITE = (250, 250, 242, 255); BLACK = (20, 18, 24, 255)
CORAL = (239, 91, 76, 255); GREEN = (111, 184, 79, 255)

def ellipse(d, box, fill, width=5): d.ellipse(box, fill=fill, outline=BLACK, width=width)
def poly(d, pts, fill, width=5): d.polygon(pts, fill=fill); d.line(pts + [pts[0]], fill=BLACK, width=width, joint="curve")
def rect(d, box, fill, width=5): d.rounded_rectangle(box, radius=12, fill=fill, outline=BLACK, width=width)

def frame(clip, i):
    image = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(image)
    bounce = (i % 2) * 5 if clip in {"idle", "walk", "run"} else 0
    lean = -18 if clip in {"light", "medium", "heavy", "hostile_takeover"} else 0
    y = bounce
    # Shoes and legs retain a shared 480-pixel ground line.
    rect(d, (135 + lean, 446, 229 + lean, 478), BLACK); rect(d, (284 + lean, 446, 378 + lean, 478), BLACK)
    poly(d, [(152+lean, 334+y),(225+lean,334+y),(234+lean,450),(151+lean,450)], NAVY)
    poly(d, [(275+lean, 334+y),(348+lean,334+y),(364+lean,450),(281+lean,450)], NAVY)
    # Torso and shirt.
    rect(d, (130+lean, 215+y, 380+lean, 360+y), NAVY)
    poly(d, [(228+lean,219+y),(282+lean,219+y),(270+lean,280+y),(240+lean,280+y)], WHITE)
    poly(d, [(251+lean,246+y),(271+lean,246+y),(278+lean,330+y),(250+lean,306+y)], CORAL)
    # Head, ears, eyes, brows, hair.
    ellipse(d, (181+lean, 90+y, 329+lean, 240+y), ORANGE)
    ellipse(d, (169+lean, 143+y, 194+lean, 181+y), ORANGE); ellipse(d, (316+lean, 143+y, 341+lean, 181+y), ORANGE)
    ellipse(d, (207+lean, 132+y, 244+lean, 169+y), WHITE, 4); ellipse(d, (267+lean, 132+y, 304+lean, 169+y), WHITE, 4)
    ellipse(d, (224+lean, 143+y, 236+lean, 157+y), BLACK, 1); ellipse(d, (275+lean, 143+y, 287+lean, 157+y), BLACK, 1)
    d.line((204+lean,123+y,244+lean,112+y), fill=BLACK, width=11); d.line((267+lean,112+y,307+lean,123+y), fill=BLACK, width=11)
    poly(d, [(180+lean,139+y),(188+lean,103+y),(213+lean,73+y),(272+lean,62+y),(324+lean,99+y),(329+lean,133+y),(295+lean,112+y),(256+lean,110+y),(215+lean,117+y)], HAIR)
    ellipse(d, (255+lean, 48+y, 303+lean, 94+y), HAIR)
    # Mouth varies with combat state.
    if clip in {"hit", "lose"}: ellipse(d, (238+lean, 184+y, 280+lean, 207+y), BLACK, 3)
    elif clip in {"win", "intro", "hostile_takeover"}: ellipse(d, (231+lean, 178+y, 290+lean, 211+y), BLACK, 3)
    else: d.arc((224+lean, 169+y, 292+lean, 215+y), start=5, end=175, fill=BLACK, width=6)
    # Arms / briefcase poses.
    if clip in {"block_high", "block_low"}:
        rect(d, (98+lean, 213+y, 166+lean, 310+y), NAVY); rect(d, (344+lean, 213+y, 412+lean, 310+y), NAVY)
    elif clip in {"light", "medium", "heavy", "hostile_takeover"}:
        rect(d, (55+lean, 225+y, 167+lean, 284+y), NAVY); ellipse(d, (42+lean, 235+y, 84+lean, 278+y), ORANGE)
        rect(d, (340+lean, 220+y, 410+lean, 330+y), NAVY)
        if clip == "hostile_takeover":
            rect(d, (20+lean, 250+y, 155+lean, 355+y), NAVY_DARK); d.rectangle((33+lean, 271+y, 142+lean, 322+y), fill=GREEN, outline=BLACK, width=4)
    else:
        rect(d, (83+lean, 232+y, 163+lean, 350+y), NAVY); rect(d, (346+lean, 232+y, 426+lean, 350+y), NAVY)
        rect(d, (342+lean, 315+y, 462+lean, 404+y), NAVY_DARK)
        if clip in {"intro", "win"}: d.rectangle((355+lean, 334+y, 449+lean, 381+y), fill=GREEN, outline=BLACK, width=4)
    return image

CLIPS = {"idle":4,"walk":4,"run":4,"jump":4,"crouch":1,"block_high":1,"block_low":1,"light":1,"medium":1,"heavy":1,"hostile_takeover":1,"hit":1,"knockdown":1,"wake":1,"intro":1,"win":1,"lose":1}
for clip, count in CLIPS.items():
    for index in range(count):
        frame(clip, index).save(OUT / f"{clip}_{index:02}.png")
