import json

import pytest

from fighter.platform.input import DeviceLifecycle, InputRouter, SemanticAction
from fighter.platform.settings import Settings, load, save, validate
from fighter.presentation.shell import Shell
from fighter.sim.bits import Action
from fighter.sim.kernel import SessionKernel


def test_router_converts_physical_state_to_tick_edges_without_shell_leakage() -> None:
    router = InputRouter()
    router.event("key", "key:106", True)
    router.event("key", "key:13", True)
    first = router.frames()[0]
    assert first.held == Action.LIGHT and first.pressed == Action.LIGHT
    assert router.shell_edges() == {SemanticAction.CONFIRM}
    assert router.frames()[0].pressed == 0
    assert router.shell_edges() == set()


def test_router_supports_mixed_controller_assignment_and_remap_conflicts() -> None:
    router = InputRouter()
    router.lifecycle.connect(44, "Supported Pad")
    router.lifecycle.assign(44, 1)
    router.set_binding(1, SemanticAction.LIGHT, "button:0")
    router.event("button", "button:0", True, 44)
    assert router.frames()[1].held == Action.LIGHT
    with pytest.raises(ValueError, match="conflicts"):
        router.set_binding(1, SemanticAction.MEDIUM, "button:0")


def test_quick_press_and_release_survives_until_next_simulation_tick() -> None:
    router = InputRouter()
    router.event("key", "key:106", True)
    router.event("key", "key:106", False)
    first = router.frames()[0]
    assert first.held == Action.LIGHT and first.pressed == Action.LIGHT
    second = router.frames()[0]
    assert second.held == 0 and second.released == Action.LIGHT


def test_lifecycle_disconnect_only_marks_assigned_player_and_reconnects() -> None:
    devices = DeviceLifecycle()
    devices.connect(1, "unassigned")
    assert devices.disconnect(1) is None
    devices.connect(2, "assigned")
    devices.assign(2, 0)
    assert devices.disconnect(2) == 0
    restored = devices.connect(3, "assigned again")
    assert restored.player == 0
    assert devices.awaiting_reconnect == set()


def test_pause_focus_loss_freezes_checksum_and_clears_held_input() -> None:
    game, router, shell = SessionKernel(), InputRouter(), Shell(screen="match")
    router.event("key", "key:100", True)
    game.tick(router.frames())
    frozen = game.checksum()
    shell.pause("Focus lost")
    router.clear()
    assert shell.paused and router.frames()[0].held == 0
    assert game.checksum() == frozen
    assert shell.resume()


def test_settings_round_trip_is_atomic_and_outside_install_path(tmp_path) -> None:
    path = tmp_path / "user-data" / "settings.json"
    settings = Settings()
    settings.accessibility.high_contrast = True
    save(settings, path)
    loaded, diagnostic = load(path)
    assert diagnostic is None and loaded.accessibility.high_contrast
    assert not path.with_name(".settings.json.new").exists()


@pytest.mark.parametrize(
    "payload",
    [
        {"unexpected": 1},
        {"bindings": [{"left": "key:1"}, {}]},
        {"accessibility": {"high_contrast": "yes"}},
    ],
)
def test_invalid_or_corrupt_settings_recover_to_defaults(tmp_path, payload) -> None:
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    settings, diagnostic = load(path)
    assert diagnostic is not None and settings.version == 3
    with pytest.raises(ValueError):
        validate(payload)


def test_version_zero_settings_migrate_to_current_defaults() -> None:
    assert validate({"version": 0}).version == 3


def test_training_reset_and_move_list_onboarding_are_reachable() -> None:
    shell = Shell(screen="training")
    shell.navigate(SemanticAction.MENU_DOWN, 3)
    assert shell.focus == 1
    shell.screen = "moves"
    assert shell.screen == "moves"
    training = SessionKernel(training=1)
    training.tick()
    training.reset()
    assert training.match.training == 1 and training.match.result is None
