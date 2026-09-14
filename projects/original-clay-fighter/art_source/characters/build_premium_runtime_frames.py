"""Slice the approved premium pose sheets into transparent runtime frames."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

ROOT = Path(__file__).resolve().parent
PROJECT = Path(__file__).resolve().parents[2]
CHARACTERS = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
POSE_INDEX = {
    "idle": 0,
    "intro": 0,
    "walk": 1,
    "run": 2,
    "jump": 3,
    "crouch": 4,
    "block_high": 5,
    "block_low": 6,
    "light": 7,
    "medium": 8,
    "heavy": 9,
    "star_chord": 10,
    "hostile_takeover": 10,
    "exosuit_call": 10,
    "armor_idle": 10,
    "armor_punch": 8,
    "armor_kick": 9,
    "kitchen_rush": 10,
    "hit": 11,
    "knockdown": 12,
    "wake": 13,
    "win": 14,
    "lose": 15,
}


def _remove_green(surface: pygame.Surface) -> pygame.Surface:
    converted = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    converted.blit(surface, (0, 0))
    pixels = pygame.PixelArray(converted)
    for x in range(converted.get_width()):
        for y in range(converted.get_height()):
            color = converted.unmap_rgb(pixels[x, y])
            if color.g > 160 and color.g > color.r * 1.35 and color.g > color.b * 1.35:
                pixels[x, y] = (0, 0, 0, 0)
    del pixels
    return converted


def build() -> None:
    pygame.init()
    pygame.display.set_mode((1, 1))
    for fighter_id in CHARACTERS:
        sheet_path = ROOT / fighter_id / "premium_pose_sheet_v1.png"
        sheet = pygame.image.load(sheet_path.as_posix()).convert_alpha()
        if fighter_id == "tech_billionaire":
            sheet = _remove_green(sheet)
        bounds = [round(index * sheet.get_width() / 4) for index in range(5)]
        destination = PROJECT / "assets" / "characters" / fighter_id / "sprites"
        for index in range(16):
            column, row = index % 4, index // 4
            rect = pygame.Rect(
                bounds[column],
                bounds[row],
                bounds[column + 1] - bounds[column],
                bounds[row + 1] - bounds[row],
            )
            pose = sheet.subsurface(rect).copy()
            pose = pygame.transform.smoothscale(pose, (512, 512))
            pygame.image.save(pose, (destination / f"premium_{index:02d}.png").as_posix())
        manifest_path = PROJECT / "assets" / "characters" / fighter_id / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["pivot"] = {"x": 256, "y": 500}
        manifest["source"] = "sprites/premium_*.png"
        manifest["usage"] = "Premium approved clay pose sheet frames wired to gameplay states"
        for clip_name, clip in manifest["clips"].items():
            clip["frames"] = [f"premium_{POSE_INDEX.get(clip_name, 0):02d}.png"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    pygame.quit()


if __name__ == "__main__":
    build()
