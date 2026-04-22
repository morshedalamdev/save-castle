import unittest

from src.game.enemies.components import Enemy, EnemyType
from src.game.enemies.text.systems import on_letter_pressed
from src.game.rounds_and_indicators.resources import Difficulty, RoundIndicators
from src.game.rounds_and_indicators.systems import increase_round_difficulty, update_score_on_enemy_typed


class RoundAndTypingTests(unittest.TestCase):
    def test_round_difficulty_medium(self):
        indicators = RoundIndicators(round_number=3, difficulty=Difficulty.MEDIUM)
        interval = increase_round_difficulty(indicators)
        self.assertEqual(indicators.max_enemies_this_round, 14)
        self.assertAlmostEqual(indicators.enemy_base_speed, 52.5)
        self.assertAlmostEqual(interval, 1.7)

    def test_score_formula(self):
        indicators = RoundIndicators(round_number=5, difficulty=Difficulty.HARD, wpm=60.0, streak=50)
        update_score_on_enemy_typed(indicators)
        self.assertEqual(indicators.score, int(3 * 60.0 * (50 / 50 + 1) * (5 / 10 + 1)))

    def test_typing_kills_word(self):
        indicators = RoundIndicators()
        enemy = Enemy(word="go", enemy_type=EnemyType.BAT, spawn_point="left", x=0, y=0, speed=20)
        enemies = [enemy]
        typing_ids = set()

        first = on_letter_pressed("g", enemies, typing_ids, indicators)
        second = on_letter_pressed("o", enemies, typing_ids, indicators)

        self.assertEqual(first, 0)
        self.assertEqual(second, 1)
        self.assertGreaterEqual(indicators.streak, 2)


if __name__ == "__main__":
    unittest.main()
