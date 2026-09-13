from __future__ import annotations

from types import SimpleNamespace

from fighter.platform.settings import Settings, validate
from fighter.presentation.audio import AudioLevels, MixerAudioService
from fighter.presentation.effects import ClayEffectPool
from fighter.presentation.events import PresentationDispatcher
from fighter.sim.bits import Action
from fighter.sim.events import PRESENTATION_EVENT_VERSION, PresentationEvent, PresentationPayload
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel


def _event(event_id: int, kind: str = "hit") -> PresentationEvent:
    return PresentationEvent(PRESENTATION_EVENT_VERSION, event_id, 4, kind, 1, 2, (400, 600),
                             PresentationPayload("light", 40))


def test_events_are_immutable_monotonic_and_checksum_exempt() -> None:
    game = SessionKernel()
    game.match.p2.x = game.match.p1.x + 50
    baseline = SessionKernel()
    baseline.match.p2.x = baseline.match.p1.x + 50
    game.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    baseline.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    events = ()
    for _ in range(10):
        game.tick()
        baseline.tick()
        if game.presentation_events():
            events = game.presentation_events()
    assert events and [event.event_id for event in events] == sorted(event.event_id for event in events)
    assert all(event.version == PRESENTATION_EVENT_VERSION and event.payload.move for event in events)
    assert game.checksum() == baseline.checksum()
    first_id = events[0].event_id
    game.reset()
    game.match.p2.x = game.match.p1.x + 50
    game.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    for _ in range(10):
        game.tick()
        if game.presentation_events():
            break
    assert game.presentation_events()[0].event_id > first_id


def test_ko_event_and_reset_keep_id_sequence() -> None:
    game = SessionKernel()
    game.match.p1.health = game.match.p2.health = 0
    game.tick()
    events = game.presentation_events()
    assert [event.kind for event in events] == ["ko"]
    assert [event.event_id for event in events] == [1]
    game.reset()
    game.match.p1.health = 0
    game.tick()
    assert game.presentation_events()[0].event_id == 2


def test_dispatcher_and_pool_are_exactly_once_bounded_and_reduced_safe() -> None:
    received: list[int] = []
    dispatcher = PresentationDispatcher()
    event = _event(1)
    assert dispatcher.dispatch((event, event), lambda item: received.append(item.event_id)) == 1
    assert dispatcher.dispatch((event,), lambda item: received.append(item.event_id)) == 0
    pool = ClayEffectPool(capacity=2)
    pool.trigger(event, reduced=True)
    pool.trigger(_event(2, "block"), reduced=True)
    pool.trigger(_event(3, "land"), reduced=True)
    assert [effect.kind for effect in pool.effects] == ["impact", "block"]


def test_audio_safe_mode_survives_init_load_and_channel_failures() -> None:
    class Mixer:
        music = SimpleNamespace(set_volume=lambda _: None)

        def get_init(self):
            return None

        def init(self, **kwargs):
            raise OSError("no device")

    pygame = SimpleNamespace(mixer=Mixer(), error=RuntimeError)
    service = MixerAudioService(pygame)
    assert service.start_match_music(1) is None and service.safe_mode and service.diagnostic
    assert AudioLevels(master=50, music=50).gain("music") == 0.25

    class ReadyMixer:
        music = SimpleNamespace(load=lambda _: (_ for _ in ()).throw(OSError("bad asset")),
                               set_volume=lambda _: None, play=lambda *args, **kwargs: None)

        def get_init(self):
            return (48000, -16, 2)

        def set_num_channels(self, _limit):
            return None

    asset_failure = MixerAudioService(SimpleNamespace(mixer=ReadyMixer(), error=RuntimeError))
    assert asset_failure.start_match_music(1) is None and asset_failure.safe_mode

    class ChannelMixer(ReadyMixer):
        def Sound(self, _path):
            return object()

        def find_channel(self, _force):
            raise OSError("channel unavailable")

    channel_failure = MixerAudioService(SimpleNamespace(mixer=ChannelMixer(), error=RuntimeError))
    channel_failure.dispatch(_event(9))
    assert channel_failure.safe_mode


def test_audio_settings_migrate_and_bound_levels() -> None:
    settings = validate({"version": 1, "audio": {"master": 25, "muted": ["music"]}})
    assert settings.version == 2 and settings.audio.master == 25 and settings.audio.music == 55
    try:
        validate({"audio": {"sfx": 101}})
    except ValueError:
        pass
    else:
        raise AssertionError("out-of-range level was accepted")
    assert Settings().audio.ui == 80
