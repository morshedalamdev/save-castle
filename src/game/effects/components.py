from dataclasses import dataclass

EXPLOSION_ANIMATION_SPEED = 0.08


@dataclass
class Explosion:
    x: float
    y: float
    frame: int = 0
    timer: float = 0.0
