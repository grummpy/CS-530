"""Canonical content identifiers used by the playable prototype."""

from __future__ import annotations

from typing import Any

import yaml

from fighter.content.loader import data_root

PLAYABLE = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
STAGES = ("roadside_truck_stop", "executive_lawn", "electric_assembly_hall")
DUMMY_MODES = ("stand", "crouch", "jump", "block")


def load_profile(fighter_id: str) -> dict[str, Any]:
    path = data_root() / "fighters" / f"{fighter_id}.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError(f"bad profile {fighter_id}")
    return raw


def display_name(fighter_id: str) -> str:
    path = data_root() / "fighters" / f"{fighter_id}.yaml"
    if not path.exists():
        return fighter_id
    return str(load_profile(fighter_id).get("display_name", fighter_id))
