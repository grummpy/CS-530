"""Canonical six-fighter roster plus the graybox dummy."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from fighter.content.loader import data_root
PLAYABLE = ("rhinestone_angel", "mr_president", "captain_campaign", "baron_boardroom", "doctor_broadcast", "general_gadget", "general_gravy", "influence_oracle")
STAGES = ("municipal_parade_depot", "wellness_mall_studio", "test_grid")
DUMMY_MODES = ("stand", "crouch", "jump", "block")

def load_profile(fighter_id: str) -> dict[str, Any]:
    path = data_root() / "fighters" / f"{fighter_id}.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"bad profile {fighter_id}")
    return raw

def display_name(fighter_id: str) -> str:
    path = data_root() / "fighters" / f"{fighter_id}.yaml"
    if not path.exists():
        return fighter_id
    return str(load_profile(fighter_id).get("display_name", fighter_id))
