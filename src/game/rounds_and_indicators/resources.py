from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

INITIAL_ENEMY_SPEED = 30.0
INITIAL_MAX_NUMBER_OF_ENEMIES = 2


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


@dataclass
class RoundIndicators:
    round_number: int = 0
    max_enemies_this_round: int = INITIAL_MAX_NUMBER_OF_ENEMIES
    enemies_spawned: int = 0
    enemies_unlived: int = 0
    enemies_typed: int = 0
    enemy_base_speed: float = INITIAL_ENEMY_SPEED
    wpm: float = 0.0
    score: int = 0
    streak: int = 0
    elapsed_round_seconds: float = 0.0
    difficulty: Difficulty = Difficulty.MEDIUM
