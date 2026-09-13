"""Presentation-only shell state; it deliberately never mutates simulation state."""

from __future__ import annotations

from dataclasses import dataclass

from fighter.platform.input import SemanticAction


@dataclass
class Shell:
    screen: str = "title"
    focus: int = 0
    paused: bool = False
    pause_reason: str | None = None
    input_display: bool = False

    def navigate(self, action: SemanticAction, count: int) -> None:
        if action in (SemanticAction.MENU_UP, SemanticAction.MENU_LEFT):
            self.focus = (self.focus - 1) % count
        elif action in (SemanticAction.MENU_DOWN, SemanticAction.MENU_RIGHT):
            self.focus = (self.focus + 1) % count

    def pause(self, reason: str) -> None:
        self.paused, self.pause_reason = True, reason

    def resume(self) -> bool:
        if not self.paused:
            return False
        self.paused, self.pause_reason = False, None
        return True
