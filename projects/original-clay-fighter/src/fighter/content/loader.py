"""Content root and shared graybox move catalog."""
from pathlib import Path
from fighter.sim.moves import MOVES

def data_root() -> Path: return Path(__file__).resolve().parents[3] / "data"
def load_catalog():
    fighter_files = (data_root() / "fighters").glob("*.yaml")
    return {path.stem: dict(MOVES) for path in fighter_files}
