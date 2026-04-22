from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EnemyType(Enum):
    PIG = ("pig", 36, 30, 16)
    BAT = ("bat", 46, 30, 7)
    BEE = ("bee", 36, 34, 6)
    BUNNY = ("bunny", 34, 44, 12)
    CHICKEN = ("chicken", 32, 34, 14)
    MUSHROOM = ("mushroom", 32, 32, 16)
    TRUNK = ("trunk", 64, 32, 14)
    BLUEBIRD = ("bluebird", 32, 32, 9)
    RADISH = ("radish", 30, 38, 12)
    RINO = ("rino", 52, 34, 6)
    ROCK_ONE = ("rock_one", 38, 34, 14)
    ROCK_TWO = ("rock_two", 32, 28, 14)
    ROCK_THREE = ("rock_three", 22, 18, 14)
    SNAIL = ("snail", 38, 24, 10)


@dataclass
class Enemy:
    word: str
    enemy_type: EnemyType
    spawn_point: str
    x: float
    y: float
    speed: float
    checkpoint: int = 0
    frame_index: int = 0
    frame_timer: float = 0.0
    text_offset_y: float = 50.0
    typing_index: int = -1
    is_boss_ghost: bool = False

    @property
    def sprite_name(self) -> str:
        return self.enemy_type.value[0]

    @property
    def frame_size(self) -> tuple[int, int]:
        return int(self.enemy_type.value[1]), int(self.enemy_type.value[2])

    @property
    def animation_length(self) -> int:
        return int(self.enemy_type.value[3])
