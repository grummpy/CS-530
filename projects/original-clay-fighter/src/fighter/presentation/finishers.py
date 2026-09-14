"""Bounded, match-owned finisher media loading and deterministic fallback."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

from fighter.resource_paths import asset_root

FRAME_COUNT = 30
SOURCE_SIZE = (640, 360)
DISPLAY_SIZE = (1280, 720)
DEFAULT_CACHE_BYTES = 48 * 1024 * 1024


def finisher_root() -> Path:
    return asset_root() / "finishers"


@dataclass(frozen=True, slots=True)
class FinisherVariant:
    name: str
    frames: tuple[Path, ...]


def resolve_finisher_variant(name: str | None, root: Path | None = None) -> FinisherVariant | None:
    """Validate a selected variant rather than silently globbing partial media."""
    if not name or "/" in name or "\\" in name or name in {".", ".."}:
        return None
    frame_root = (root or finisher_root()) / name / "frames"
    frames = tuple(frame_root / f"{index:03d}.png" for index in range(FRAME_COUNT))
    if not frame_root.is_dir() or not all(path.is_file() for path in frames):
        return None
    return FinisherVariant(name, frames)


def finisher_frame_paths(winner_id: str, loser_id: str) -> list[Path]:
    variant = resolve_finisher_variant(f"{winner_id}_vs_{loser_id}")
    return list(variant.frames) if variant else []


@dataclass(slots=True)
class RollingFrameCache:
    """LRU cache whose accounting is based on actual transformed surface bytes."""

    budget_bytes: int = DEFAULT_CACHE_BYTES
    _frames: OrderedDict[int, tuple[Any, int]] = field(default_factory=OrderedDict)
    bytes_used: int = 0
    peak_bytes: int = 0

    @staticmethod
    def _bytes(surface: Any) -> int:
        width, height = surface.get_size()
        return cast(int, width * height * surface.get_bytesize())

    def get(self, index: int) -> Any | None:
        value = self._frames.pop(index, None)
        if value is None:
            return None
        self._frames[index] = value
        return value[0]

    def put(self, index: int, surface: Any) -> bool:
        size = self._bytes(surface)
        if size > self.budget_bytes:
            return False
        previous = self._frames.pop(index, None)
        if previous:
            self.bytes_used -= previous[1]
        while self._frames and self.bytes_used + size > self.budget_bytes:
            _, (_, evicted) = self._frames.popitem(last=False)
            self.bytes_used -= evicted
        self._frames[index] = (surface, size)
        self.bytes_used += size
        self.peak_bytes = max(self.peak_bytes, self.bytes_used)
        return True

    def clear(self) -> None:
        self._frames.clear()
        self.bytes_used = 0


@dataclass(slots=True)
class FinisherPlayback:
    variant_name: str | None
    cache_budget_bytes: int = DEFAULT_CACHE_BYTES
    diagnostic: str | None = None
    _variant: FinisherVariant | None = None
    _next_frame: int = 0
    _failed: bool = False
    _reported: bool = False
    cache: RollingFrameCache = field(init=False)

    def __post_init__(self) -> None:
        self.cache = RollingFrameCache(self.cache_budget_bytes)
        self._variant = resolve_finisher_variant(self.variant_name)
        if self._variant is None:
            self._failure("Finisher unavailable — showing results.")

    @property
    def ready(self) -> bool:
        return self._variant is not None and not self._failed and self.cache.get(0) is not None

    @property
    def fallback(self) -> bool:
        return self._failed or self._variant is None

    def _failure(self, message: str) -> None:
        self._failed = True
        if not self._reported:
            self.diagnostic = message
            self._reported = True

    def preload_one(self, pygame: Any) -> bool:
        """Decode/transform at most one frame outside the KO render path."""
        if self.fallback or self._variant is None or self._next_frame >= len(self._variant.frames):
            return False
        index = self._next_frame
        try:
            source = pygame.image.load(self._variant.frames[index].as_posix()).convert_alpha()
            frame = pygame.transform.smoothscale(source, DISPLAY_SIZE)
        except (OSError, pygame.error, ValueError, AttributeError):
            self._failure("Finisher media failed — showing results.")
            return False
        self._next_frame += 1
        if not self.cache.put(index, frame):
            self._failure("Finisher exceeds cache budget — showing results.")
            return False
        return True

    def frame(self, index: int) -> Any | None:
        return self.cache.get(index % FRAME_COUNT)

    def teardown(self) -> None:
        self.cache.clear()
        self._variant = None


def fallback_card(pygame: Any, screen: Any, font: Any, label: str, diagnostic: str | None) -> None:
    """Render the same readable card for every media failure."""
    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((6, 8, 15, 225))
    screen.blit(overlay, (0, 0))
    screen.blit(pygame.font.Font(None, 70).render(label, True, (255, 235, 150)), (350, 280))
    screen.blit(font.render(diagnostic or "Finisher unavailable", True, (255, 255, 255)), (410, 360))
