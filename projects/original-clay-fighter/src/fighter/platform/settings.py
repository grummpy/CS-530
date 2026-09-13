"""Validated user settings with atomic, install-path-independent persistence."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fighter.platform.input import COMBAT_ACTIONS, SemanticAction, default_bindings

SETTINGS_VERSION = 1


@dataclass
class Accessibility:
    high_contrast: bool = False
    reduced_effects: bool = False


@dataclass
class Settings:
    version: int = SETTINGS_VERSION
    bindings: list[dict[str, str]] = field(default_factory=default_bindings)
    accessibility: Accessibility = field(default_factory=Accessibility)
    onboarding_complete: bool = False


def user_settings_path() -> Path:
    root = Path(os.environ.get("APPDATA") or os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return root / "papier-parade" / "settings.json"


def validate(raw: object) -> Settings:
    if not isinstance(raw, dict) or set(raw) - {"version", "bindings", "accessibility", "onboarding_complete"}:
        raise ValueError("settings schema is invalid")
    version = raw.get("version", SETTINGS_VERSION)
    if version == 0:
        raw = {**raw, "version": SETTINGS_VERSION}
    elif version != SETTINGS_VERSION:
        raise ValueError("unsupported settings version")
    bindings = raw.get("bindings", default_bindings())
    if not isinstance(bindings, list) or len(bindings) != 2:
        raise ValueError("settings bindings are invalid")
    expected = set(default_bindings()[0])
    checked: list[dict[str, str]] = []
    for player in bindings:
        if not isinstance(player, dict) or set(player) != expected:
            raise ValueError("settings binding actions are invalid")
        values = list(player.values())
        combat_values = [player[action.value] for action in COMBAT_ACTIONS]
        shell_values = [player[action.value] for action in set(SemanticAction) - set(COMBAT_ACTIONS)]
        if (any(not isinstance(value, str) or not _binding(value) for value in values)
                or len(combat_values) != len(set(combat_values))
                or len(shell_values) != len(set(shell_values))):
            raise ValueError("settings bindings conflict or are invalid")
        checked.append(dict(player))
    access = raw.get("accessibility", {})
    if not isinstance(access, dict) or set(access) - {"high_contrast", "reduced_effects"}:
        raise ValueError("accessibility settings are invalid")
    high = access.get("high_contrast", False)
    reduced = access.get("reduced_effects", False)
    complete = raw.get("onboarding_complete", False)
    if not all(isinstance(value, bool) for value in (high, reduced, complete)):
        raise ValueError("settings booleans are invalid")
    return Settings(bindings=checked, accessibility=Accessibility(high, reduced), onboarding_complete=complete)


def load(path: Path | None = None) -> tuple[Settings, str | None]:
    path = path or user_settings_path()
    try:
        return validate(json.loads(path.read_text(encoding="utf-8"))), None
    except FileNotFoundError:
        return Settings(), None
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return Settings(), f"Settings recovered to defaults: {error}"


def save(settings: Settings, path: Path | None = None) -> None:
    path = path or user_settings_path()
    validated = validate(_as_dict(settings))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.new")
    try:
        temporary.write_text(json.dumps(_as_dict(validated), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _as_dict(settings: Settings) -> dict[str, Any]:
    return {
        "version": settings.version, "bindings": settings.bindings,
        "accessibility": {"high_contrast": settings.accessibility.high_contrast,
                          "reduced_effects": settings.accessibility.reduced_effects},
        "onboarding_complete": settings.onboarding_complete,
    }


def _binding(token: str) -> bool:
    prefix, separator, value = token.partition(":")
    return prefix in {"key", "button", "hat"} and bool(separator) and value.isascii() and len(value) <= 24
