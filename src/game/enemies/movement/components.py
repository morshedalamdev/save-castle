from enum import Enum


class EnemySpawnPoint(str, Enum):
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    LEFT = "left"
    RIGHT = "right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
