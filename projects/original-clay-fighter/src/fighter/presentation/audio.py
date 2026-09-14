"""Failure-safe, non-authoritative mixer service and cue registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from fighter.resource_paths import asset_root
from fighter.sim.events import PresentationEvent

AudioCategory = Literal["master", "music", "sfx", "voice", "ui"]
MUSIC_TRACKS = (
    "battle_of_the_kitchen.wav",
    "mark_zuckerberg_in_battle.wav",
    "neon_warrior.wav",
    "make_america_great_again.wav",
    "hoosiers_stand_together.wav",
)
CUE_MANIFEST_VERSION = 1
CUE_MANIFEST: dict[str, tuple[str, AudioCategory, int]] = {
    "hit": ("placeholder_impact.wav", "sfx", 80),
    "block": ("placeholder_block.wav", "sfx", 70),
    "throw": ("placeholder_throw.wav", "sfx", 90),
    "throw_tech": ("placeholder_tech.wav", "sfx", 85),
    "land": ("placeholder_land.wav", "sfx", 35),
    "ko": ("placeholder_ko.wav", "voice", 100),
    "result": ("placeholder_result.wav", "ui", 65),
}


@dataclass(frozen=True, slots=True)
class AudioLevels:
    master: int = 100
    music: int = 55
    sfx: int = 80
    voice: int = 80
    ui: int = 80
    muted: tuple[str, ...] = ()

    def gain(self, category: AudioCategory) -> float:
        if category in self.muted or "master" in self.muted:
            return 0.0
        category_level = {
            "master": self.master,
            "music": self.music,
            "sfx": self.sfx,
            "voice": self.voice,
            "ui": self.ui,
        }[category]
        return self.master * category_level / 10_000


@dataclass(slots=True)
class MixerAudioService:
    """All mixer exceptions become a persistent, diagnosable silent mode."""

    pygame: Any
    levels: AudioLevels = field(default_factory=AudioLevels)
    channel_limit: int = 12
    safe_mode: bool = False
    diagnostic: str | None = None
    cache: dict[str, Any] = field(default_factory=dict)

    def _fail(self, error: Exception) -> None:
        self.safe_mode, self.diagnostic = True, f"Audio disabled: {type(error).__name__}: {error}"

    def apply_levels(self, levels: AudioLevels) -> None:
        self.levels = levels
        if self.safe_mode:
            return
        try:
            self.pygame.mixer.music.set_volume(levels.gain("music"))
        except (AttributeError, OSError, self.pygame.error) as error:
            self._fail(error)

    def start_match_music(self, seed: int) -> str | None:
        track = MUSIC_TRACKS[seed % len(MUSIC_TRACKS)]
        if self.safe_mode:
            return None
        try:
            mixer = self.pygame.mixer
            if mixer.get_init() is None:
                mixer.init(frequency=48000, channels=2)
            mixer.set_num_channels(self.channel_limit)
            path = asset_root() / "audio" / "music" / track
            mixer.music.load(path.as_posix())
            mixer.music.set_volume(self.levels.gain("music"))
            mixer.music.play(-1, fade_ms=500)
            return track
        except (AttributeError, OSError, self.pygame.error) as error:
            self._fail(error)
            return None

    def dispatch(self, event: PresentationEvent) -> None:
        cue = CUE_MANIFEST.get(event.kind)
        if cue is None or self.safe_mode:
            return
        filename, category, _priority = cue
        try:
            sound = self.cache.get(filename)
            if sound is None:
                sound = self.pygame.mixer.Sound(
                    (asset_root() / "audio" / "cues" / filename).as_posix()
                )
                self.cache[filename] = sound
            channel = self.pygame.mixer.find_channel(True)
            if channel is None:
                return
            channel.set_volume(self.levels.gain(category))
            channel.play(sound)
        except (AttributeError, OSError, self.pygame.error) as error:
            self._fail(error)

    def shutdown(self) -> None:
        if not self.safe_mode:
            try:
                self.pygame.mixer.stop()
                self.pygame.mixer.quit()
            except (AttributeError, OSError, self.pygame.error) as error:
                self._fail(error)


def start_match_music(pygame: object, seed: int) -> str | None:
    """Compatibility wrapper for callers that do not retain a service."""
    return MixerAudioService(pygame).start_match_music(seed)
