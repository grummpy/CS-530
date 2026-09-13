"""Content root and shared graybox move catalog."""
from pathlib import Path
from fighter.sim.moves import MOVES

def data_root() -> Path: return Path(__file__).resolve().parents[3] / "data"
def load_catalog():
    fighter_files = (data_root() / "fighters").glob("*.yaml")
    return {path.stem: dict(MOVES) for path in fighter_files}

def load_finisher(fighter_id: str) -> dict[str, str] | None:
    """Return declared finisher metadata when authored media/timelines exist.

    The current prototype has no committed finisher data, so callers get an
    explicit empty result instead of failing at package import time.
    """
    path = data_root() / "finishers" / f"{fighter_id}.yaml"
    if not path.exists():
        return None
    import yaml
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else None
