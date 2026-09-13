"""Package entry point: `python -m fighter`."""
from __future__ import annotations
import sys
from fighter.platform.app import headless_main, main

def _dispatch() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "headless":
        sys.argv = [sys.argv[0], "--headless", *sys.argv[2:]]
    return main()

if __name__ == "__main__":
    raise SystemExit(_dispatch())
