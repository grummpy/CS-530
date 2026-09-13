"""Export a fighter's committed clip manifest for quick inspection."""

import json
from pathlib import Path


def export_frame_data(fighter_id: str) -> str:
    root = Path(__file__).resolve().parents[3] / "assets" / "characters" / fighter_id
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    return json.dumps(
        {"fighter_id": fighter_id, "clips": manifest.get("clips", {})}, indent=2, sort_keys=True
    )
