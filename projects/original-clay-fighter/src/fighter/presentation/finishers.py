"""Read-only finisher media lookup; presentation owns playback and skipping."""
from pathlib import Path

def finisher_frame_paths(winner_id: str, loser_id: str) -> list[Path]:
    root = Path(__file__).resolve().parents[3] / "assets" / "finishers" / f"{winner_id}_vs_{loser_id}" / "frames"
    return sorted(root.glob("*.png"))
