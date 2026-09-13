"""Canonical SHA-256 of match snapshots."""
from __future__ import annotations
import hashlib
import json
from typing import Any
from fighter.sim.state import MatchState
def canonical_bytes(snapshot: dict[str, Any]) -> bytes:
    return json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
def checksum_snapshot(snapshot: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(snapshot)).hexdigest()
def checksum_match(match: MatchState) -> str:
    return checksum_snapshot(match.snapshot())
