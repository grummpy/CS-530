"""Canonical content identifiers used by the playable prototype."""

from __future__ import annotations

from fighter.content.loader import load_fighter

PLAYABLE = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
STAGES = ("roadside_truck_stop", "executive_lawn", "electric_assembly_hall")
DUMMY_MODES = ("stand", "crouch", "jump", "block")


def display_name(fighter_id: str) -> str:
    try:
        return load_fighter(fighter_id).profile.display_name
    except ValueError:
        return fighter_id
