"""Export a fighter's committed clip manifest for quick inspection."""

import json

from fighter.resource_paths import asset_root


def export_frame_data(fighter_id: str) -> str:
    root = asset_root() / "characters" / fighter_id
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    return json.dumps(
        {"fighter_id": fighter_id, "clips": manifest.get("clips", {})}, indent=2, sort_keys=True
    )
