"""Build character-authentic 3-second clay finishers and review MP4s."""

from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "finishers"
FIGHTERS = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
STAGES = (
    "roadside_truck_stop_concept.png",
    "executive_lawn_concept.png",
    "electric_assembly_hall_concept.png",
)
ACCENTS = {
    "rhinestone_angel": (255, 61, 153, 255),
    "mr_president": (255, 113, 24, 255),
    "tech_billionaire": (42, 229, 230, 255),
    "master_chef": (255, 196, 91, 255),
}


def fighter_art(fighter: str, index: int) -> Image.Image:
    path = ROOT / "assets" / "characters" / fighter / "sprites" / f"premium_{index:02}.png"
    art = Image.open(path).convert("RGBA")
    art = art.crop(art.getbbox() or (0, 0, art.width, art.height))
    art.thumbnail((205, 205), Image.Resampling.LANCZOS)
    return art


def grounded(canvas: Image.Image, art: Image.Image, x: int, angle: float = 0) -> None:
    if angle:
        art = art.rotate(angle, Image.Resampling.BICUBIC, expand=True)
    canvas.alpha_composite(art, (x - art.width // 2, 315 - art.height))


def splat(draw: ImageDraw.ImageDraw, x: int, y: int, radius: int, seed: int) -> None:
    points = []
    for i in range(18):
        angle = i * math.tau / 18
        reach = radius * (0.62 + ((i * 17 + seed * 11) % 9) / 16)
        points.append((x + math.cos(angle) * reach, y + math.sin(angle) * reach * 0.58))
    draw.polygon(points, fill=(139, 17, 39, 245), outline=(76, 8, 24, 255), width=3)
    for i in range(14):
        dx, dy = (
            ((i * 37 + seed * 19) % (radius * 3)) - radius * 1.5,
            ((i * 23 + seed * 7) % radius) - radius * 0.7,
        )
        r = 3 + i % 5
        draw.ellipse((x + dx - r, y + dy - r, x + dx + r, y + dy + r), fill=(218, 44, 57, 235))


def render(winner: str, loser: str, frame: int) -> Image.Image:
    stage = STAGES[(FIGHTERS.index(winner) + FIGHTERS.index(loser)) % len(STAGES)]
    image = (
        Image.open(ROOT / "assets" / "stages" / stage)
        .convert("RGB")
        .resize((640, 360), Image.Resampling.LANCZOS)
        .convert("RGBA")
    )
    image = ImageEnhance.Brightness(image).enhance(0.48)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 640, 42), fill=(7, 5, 15, 220))
    draw.rectangle((0, 326, 640, 360), fill=(7, 5, 15, 220))
    draw.text(
        (18, 14),
        f"{winner.replace('_', ' ').upper()}  •  FINAL CLAY",
        fill=(255, 235, 174, 255),
        stroke_width=1,
        stroke_fill=(30, 8, 20, 255),
    )
    beat = min(4, frame // 6)
    victor, victim = (
        fighter_art(winner, 10 if frame >= 5 else 14),
        fighter_art(loser, 11 if frame < 20 else 12),
    )
    victim_x = 465 + int(math.sin(frame * 2.5) * (5 + beat * 2))

    if winner == "rhinestone_angel":
        grounded(image, victor, 185, (-28, 38, -20, 48, 62)[beat])
        if beat < 4:
            grounded(image, victim, victim_x, -beat * 5)
            for hit in range(beat + 1):
                cx, cy = 415 + hit * 12, 180 - hit * 9
                draw.regular_polygon((cx, cy, 18), 8, fill=(255, 217, 67, 245))
        else:
            splat(draw, 475, 292, 78, FIGHTERS.index(loser))
    elif winner == "mr_president":
        grounded(image, victor, 175)
        if frame < 19:
            grounded(image, victim, victim_x, -max(0, frame - 14) * 3)
        # Oversized 1980s handset: the call is the joke, never a featureless block.
        draw.arc((190, 146, 246, 205), 70, 290, fill=(225, 232, 240, 255), width=8)
        draw.ellipse(
            (197, 145, 215, 165), fill=(27, 35, 55, 255), outline=(235, 238, 242, 255), width=2
        )
        draw.ellipse(
            (221, 183, 240, 203), fill=(27, 35, 55, 255), outline=(235, 238, 242, 255), width=2
        )
        if 7 <= frame < 21:
            for j in range(3):
                jet_x = 170 + ((frame * 28 + j * 190) % 700)
                draw.polygon(
                    (
                        (jet_x, 68 + j * 18),
                        (jet_x + 58, 80 + j * 18),
                        (jet_x + 17, 88 + j * 18),
                        (jet_x - 8, 101 + j * 18),
                    ),
                    fill=(176, 194, 211, 255),
                    outline=(31, 38, 54, 255),
                )
                if frame >= 12:
                    bomb_y = 100 + min(125, (frame - 12) * 17 + j * 8)
                    draw.ellipse(
                        (jet_x + 12, bomb_y, jet_x + 25, bomb_y + 23),
                        fill=(42, 45, 53, 255),
                        outline=(255, 180, 45, 255),
                        width=2,
                    )
        if frame >= 19:
            growth = min(1.0, (frame - 18) / 7)
            # Layered clay fireball, smoke lobes, crater, costume fragments, and splatter.
            for j in range(11):
                angle = j * math.tau / 11 + frame * 0.07
                reach = 25 + growth * (35 + (j % 4) * 8)
                cx = 470 + math.cos(angle) * reach
                cy = 245 + math.sin(angle) * reach * 0.72
                radius = 13 + int(growth * (22 + j % 3 * 5))
                color = ((255, 224, 76, 250), (255, 124, 27, 245), (91, 61, 67, 235))[j % 3]
                draw.ellipse(
                    (cx - radius, cy - radius, cx + radius, cy + radius),
                    fill=color,
                    outline=(83, 22, 29, 220),
                    width=2,
                )
            draw.ellipse(
                (380, 282, 565, 326), fill=(31, 24, 29, 245), outline=(237, 76, 51, 255), width=4
            )
            splat(draw, 470, 292, 46 + int(growth * 48), FIGHTERS.index(loser) + 4)
            # Rhinestone wings, guitar, boots, and hair remain recognizable in the debris.
            draw.polygon(
                ((405, 205), (375, 168), (423, 184)),
                fill=(255, 222, 112, 255),
                outline=(255, 255, 238, 255),
            )
            draw.polygon(
                ((520, 196), (551, 162), (536, 211)),
                fill=(255, 222, 112, 255),
                outline=(255, 255, 238, 255),
            )
            draw.line((414, 236, 545, 180), fill=(147, 61, 176, 255), width=10)
            draw.regular_polygon(
                (545, 180, 20),
                5,
                rotation=18,
                fill=(255, 83, 175, 255),
                outline=(255, 218, 69, 255),
            )
            draw.text(
                (391, 310),
                "PROPERTY VALUE: LIQUID",
                fill=(255, 228, 170, 255),
                stroke_width=1,
                stroke_fill=(38, 7, 19, 255),
            )
    elif winner == "tech_billionaire":
        grounded(image, victor, 180)
        if beat < 4:
            grounded(image, victim, victim_x, beat * 4)
        for j in range(min(8, 1 + frame // 3)):
            angle = frame * 0.22 + j * math.tau / max(1, min(8, 1 + frame // 3))
            ox, oy = 465 + int(math.cos(angle) * 75), 210 + int(math.sin(angle) * 62)
            draw.ellipse(
                (ox - 10, oy - 10, ox + 10, oy + 10),
                fill=ACCENTS[winner],
                outline=(230, 255, 255, 255),
                width=3,
            )
        if beat == 4:
            splat(draw, 470, 292, 78, FIGHTERS.index(loser) + 8)
    else:
        grounded(image, victor, 180, -8 + beat * 5)
        if beat < 4:
            grounded(image, victim, victim_x, -beat * 7)
        for j in range(1 + beat):
            y = 145 + j * 31
            draw.line((260, y + 35, 520, y - 18), fill=(240, 248, 250, 255), width=8)
            draw.line((260, y + 35, 520, y - 18), fill=ACCENTS[winner], width=2)
        if beat == 4:
            splat(draw, 475, 292, 82, FIGHTERS.index(loser) + 12)
    if frame >= 24 and winner != "mr_president":
        draw.text(
            (250, 294),
            "CLAYMAGEDDON!",
            fill=(255, 244, 210, 255),
            stroke_width=2,
            stroke_fill=(38, 7, 19, 255),
        )
    return image.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for winner in FIGHTERS:
        for loser in FIGHTERS:
            if winner == loser:
                continue
            identifier = f"{winner}_vs_{loser}"
            directory = OUT / identifier / "frames"
            directory.mkdir(parents=True, exist_ok=True)
            for frame in range(30):
                render(winner, loser, frame).save(directory / f"{frame:03}.png", optimize=True)
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-loglevel",
                    "error",
                    "-framerate",
                    "10",
                    "-i",
                    str(directory / "%03d.png"),
                    "-pix_fmt",
                    "yuv420p",
                    "-movflags",
                    "+faststart",
                    str(OUT / f"{identifier}.mp4"),
                ],
                check=True,
            )


if __name__ == "__main__":
    main()
