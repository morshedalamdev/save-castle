from __future__ import annotations

from .resources import NumberOfLivesLeft


def reset_lives(lives: NumberOfLivesLeft) -> None:
    lives.number = 5
