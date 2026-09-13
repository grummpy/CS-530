"""Window lifecycle and headless runner. Presentation only."""
from __future__ import annotations
import argparse
import os
import sys
from collections.abc import Callable
from fighter import WINDOW_TITLE
from fighter.tools.replay import run_replay

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="clay-fighter")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--ticks", type=int, default=60)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--dump-hash", action="store_true")
    parser.add_argument("--title", default=WINDOW_TITLE)
    parser.add_argument("--p1", default="captain_campaign")
    parser.add_argument("--p2", default="graybox_rival")
    parser.add_argument("--training", action="store_true")
    parser.add_argument("--export-frames", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--perf", action="store_true")
    return parser.parse_args(argv)

def _configure_headless_video() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

def run_headless(ticks: int, seed: int = 1) -> str:
    _ticks, digest = run_replay(ticks, seed=seed)
    return digest

def run_windowed(title: str = WINDOW_TITLE, on_tick: Callable[[int], None] | None = None, seed: int = 1) -> int:
    from fighter.presentation.app_loop import run_windowed_g3
    return run_windowed_g3(title=title, seed=seed, on_tick=on_tick)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.perf:
        import json
        from fighter.tools.perf import report
        sys.stdout.write(json.dumps(report(), indent=2) + "\n")
        return 0
    if args.smoke:
        import json
        from fighter.tools.smoke import run_sample_matrix
        sys.stdout.write(json.dumps(run_sample_matrix(), indent=2) + "\n")
        return 0
    if args.export_frames:
        from fighter.tools.frame_data import export_frame_data
        sys.stdout.write(export_frame_data(args.p1) + "\n")
        return 0
    if args.headless:
        _configure_headless_video()
        digest = run_headless(args.ticks, seed=args.seed)
        if args.dump_hash:
            sys.stdout.write(f"{digest}\n")
        return 0
    return run_windowed(title=args.title, seed=args.seed)

def headless_main() -> int:
    return main(["--headless", "--dump-hash", "--ticks", "180"])
