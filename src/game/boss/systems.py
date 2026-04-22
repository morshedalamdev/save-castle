from __future__ import annotations

from ..enemies.movement.components import EnemySpawnPoint
from ..enemies.systems import spawn_enemy

BOSS_WORD_COUNT_MULTIPLIER = 3


def spawn_boss_wave(words: list[str], round_number: int, width: int, height: int, base_speed: float):
    if round_number % 10 != 0:
        return []
    count = BOSS_WORD_COUNT_MULTIPLIER * round_number
    return [spawn_enemy(words[i % len(words)], width, height, base_speed, EnemySpawnPoint.BOTTOM_LEFT, ghost=True) for i in range(count)]
