"""Optional, non-authoritative match music playback."""

from pathlib import Path

MUSIC_TRACKS = (
    "battle_of_the_kitchen.wav",
    "mark_zuckerberg_in_battle.wav",
    "neon_warrior.wav",
    "make_america_great_again.wav",
    "hoosiers_stand_together.wav",
)


def start_match_music(pygame: object, seed: int) -> str | None:
    """Start one deterministic soundtrack selection, or continue silently."""
    track = MUSIC_TRACKS[seed % len(MUSIC_TRACKS)]
    path = Path(__file__).resolve().parents[3] / "assets" / "audio" / "music" / track
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=48000, channels=2)
        pygame.mixer.music.load(path.as_posix())
        pygame.mixer.music.set_volume(0.55)
        pygame.mixer.music.play(-1, fade_ms=500)
    except (OSError, pygame.error):
        return None
    return track
