from __future__ import annotations

from .resources import Difficulty, RoundIndicators, INITIAL_ENEMY_SPEED, INITIAL_MAX_NUMBER_OF_ENEMIES

BOSS_WORD_COUNT_MULTIPLIER = 3


def increase_round_counter(indicators: RoundIndicators) -> None:
    indicators.round_number += 1


def increase_round_difficulty(indicators: RoundIndicators) -> float:
    increments = {
        Difficulty.EASY: (2, 3.75, 0.05),
        Difficulty.MEDIUM: (4, 7.5, 0.1),
        Difficulty.HARD: (6, 10.5, 0.15),
    }
    count_inc, speed_inc, interval_dec = increments[indicators.difficulty]
    if indicators.round_number % 10 == 0:
        indicators.max_enemies_this_round = BOSS_WORD_COUNT_MULTIPLIER * indicators.round_number
        indicators.enemy_base_speed = INITIAL_ENEMY_SPEED * 0.5
    else:
        indicators.max_enemies_this_round = INITIAL_MAX_NUMBER_OF_ENEMIES + indicators.round_number * count_inc
        indicators.enemy_base_speed = INITIAL_ENEMY_SPEED + indicators.round_number * speed_inc
    return max(0.5, 2.0 - indicators.round_number * interval_dec)


def reset_round(indicators: RoundIndicators) -> None:
    indicators.enemies_spawned = 0
    indicators.enemies_unlived = 0
    indicators.enemies_typed = 0
    indicators.wpm = 0.0
    indicators.elapsed_round_seconds = 0.0


def update_wpm(indicators: RoundIndicators) -> None:
    if indicators.elapsed_round_seconds <= 0:
        indicators.wpm = 0.0
    else:
        indicators.wpm = indicators.enemies_typed / (indicators.elapsed_round_seconds / 60.0)


def update_score_on_enemy_typed(indicators: RoundIndicators) -> None:
    multiplier = {Difficulty.EASY: 1, Difficulty.MEDIUM: 2, Difficulty.HARD: 3}[indicators.difficulty]
    indicators.score += int(multiplier * indicators.wpm * (indicators.streak / 50.0 + 1.0) * (indicators.round_number / 10.0 + 1.0))
