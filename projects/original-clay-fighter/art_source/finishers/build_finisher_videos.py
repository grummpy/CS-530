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
        if frame < 18:
            grounded(image, victim, victim_x)
        draw.rounded_rectangle(
            (205, 160, 237, 202), 6, fill=(30, 40, 66, 255), outline=(210, 220, 230, 255), width=2
        )
        if frame >= 9:
            for j in range(3):
                jet_x = 170 + ((frame * 28 + j * 190) % 700)
                draw.polygon(
                    ((jet_x, 70 + j * 18), (jet_x + 52, 80 + j * 18), (jet_x, 91 + j * 18)),
                    fill=(186, 202, 215, 255),
                )
        if frame >= 18:
            radius = min(105, 18 + (frame - 18) * 11)
            draw.ellipse(
                (465 - radius, 250 - radius, 465 + radius, 250 + radius),
                fill=(255, 143, 25, 235),
                outline=(255, 235, 122, 255),
                width=8,
            )
            splat(draw, 475, 300, min(78, radius), FIGHTERS.index(loser) + 4)
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
    if frame >= 24:
        draw.rounded_rectangle(
            (110, 250, 530, 312), 18, fill=(12, 7, 20, 225), outline=ACCENTS[winner], width=4
        )
        draw.text((267, 274), "CLAYMAGEDDON!", fill=(255, 244, 210, 255))
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
