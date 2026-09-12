import unittest

from starfall.game import FIXED_TIMESTEP, FighterInput, GameState


class FighterEngineTests(unittest.TestCase):
    def test_light_attack_damages_opponent_during_active_frames(self) -> None:
        game = GameState()
        game.fighters[0].x = 450
        game.fighters[1].x = 495

        game.step(FIXED_TIMESTEP, FighterInput(light=True), FighterInput())
        for _ in range(8):
            game.step(FIXED_TIMESTEP, FighterInput(), FighterInput())

        self.assertEqual(game.fighters[1].health, 945)

    def test_heavy_attack_launches_opponent(self) -> None:
        game = GameState()
        game.fighters[0].x = 450
        game.fighters[1].x = 500

        game.step(FIXED_TIMESTEP, FighterInput(heavy=True), FighterInput())
        for _ in range(17):
            game.step(FIXED_TIMESTEP, FighterInput(), FighterInput())

        self.assertEqual(game.fighters[1].health, 885)
        self.assertLess(game.fighters[1].velocity_y, 0)

    def test_jump_input_is_buffered_until_the_fighter_can_act(self) -> None:
        game = GameState()
        fighter = game.fighters[0]
        fighter.hitstun = FIXED_TIMESTEP

        game.step(FIXED_TIMESTEP, FighterInput(jump=True), FighterInput())
        game.step(FIXED_TIMESTEP, FighterInput(), FighterInput())

        self.assertLess(fighter.velocity_y, 0)
        self.assertEqual(fighter.state, "jump")

    def test_defeating_fighter_awards_round(self) -> None:
        game = GameState()
        game.fighters[1].health = 0

        game.step(FIXED_TIMESTEP, FighterInput(), FighterInput())

        self.assertTrue(game.round_over)
        self.assertEqual(game.wins, [1, 0])

    def test_match_ends_after_two_round_wins(self) -> None:
        game = GameState()
        game.wins = [1, 0]
        game.fighters[1].health = 0

        game.step(FIXED_TIMESTEP, FighterInput(), FighterInput())

        self.assertTrue(game.match_over)
