"""Resolve immutable package resources without relying on a source checkout."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path


def resource_root() -> Path:
    """Return the installed resource directory."""
    return Path(str(files("fighter.resources")))


def resource_path(relative_path: str) -> Path:
    """Return a validated path beneath the installed resource directory."""
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe package resource path: {relative_path!r}")
    return resource_root() / relative


def asset_root() -> Path:
    return resource_path("assets")


def data_root() -> Path:
    return resource_path("data")
