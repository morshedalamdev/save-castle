from __future__ import annotations

from typing import Dict, List, Tuple

from .components import EnemySpawnPoint

TURN_LEFT = (-1.0, 0.0)
TURN_RIGHT = (1.0, 0.0)
TURN_UP = (0.0, 1.0)
TURN_DOWN = (0.0, -1.0)

ROUTES: Dict[EnemySpawnPoint, List[Tuple[float, float]]] = {
    EnemySpawnPoint.TOP_LEFT: [(-0.31, 0.5), (-0.31, 0.31578), (0.0, 0.31778), (0.0, -0.31178), (0.20899, -0.31178), (0.20899, -1.0)],
    EnemySpawnPoint.BOTTOM_RIGHT: [(0.20899, -0.5), (0.20899, -0.31178), (0.0, -0.31178), (0.0, 0.31778), (-0.31, 0.31578), (-0.31, 1.0)],
    EnemySpawnPoint.TOP_RIGHT: [(0.27664, 0.5), (0.27664, 0.20252), (0.10299, 0.20252), (0.10299, 0.31778), (0.0, 0.31778), (0.0, -0.18552), (-0.20698, -0.18552), (-0.20698, -0.36841), (-1.0, -0.36841)],
    EnemySpawnPoint.BOTTOM_LEFT: [(-0.5, -0.36841), (-0.20698, -0.36841), (-0.20698, -0.18552), (0.0, -0.18552), (0.0, 0.31778), (0.10299, 0.31778), (0.10299, 0.20252), (0.27664, 0.20252), (0.27664, 1.0)],
    EnemySpawnPoint.LEFT: [(-0.5, 0.01), (1.0, 0.01)],
    EnemySpawnPoint.RIGHT: [(0.5, 0.01), (-1.0, 0.01)],
}

DIRECTIONS: Dict[EnemySpawnPoint, List[Tuple[float, float]]] = {
    EnemySpawnPoint.TOP_LEFT: [TURN_DOWN, TURN_RIGHT, TURN_DOWN, TURN_RIGHT, TURN_DOWN, TURN_DOWN],
    EnemySpawnPoint.BOTTOM_RIGHT: [TURN_UP, TURN_LEFT, TURN_UP, TURN_LEFT, TURN_UP, TURN_UP],
    EnemySpawnPoint.TOP_RIGHT: [TURN_DOWN, TURN_LEFT, TURN_UP, TURN_LEFT, TURN_DOWN, TURN_LEFT, TURN_DOWN, TURN_LEFT, TURN_LEFT],
    EnemySpawnPoint.BOTTOM_LEFT: [TURN_RIGHT, TURN_UP, TURN_RIGHT, TURN_UP, TURN_RIGHT, TURN_DOWN, TURN_RIGHT, TURN_UP, TURN_UP],
    EnemySpawnPoint.LEFT: [TURN_RIGHT, TURN_RIGHT],
    EnemySpawnPoint.RIGHT: [TURN_LEFT, TURN_LEFT],
}


def to_screen(scale_x: float, scale_y: float, width: int, height: int) -> tuple[float, float]:
    return width / 2 + width * scale_x, height / 2 + height * scale_y


def spawn_position(spawn_point: EnemySpawnPoint, width: int, height: int) -> tuple[float, float]:
    return to_screen(*ROUTES[spawn_point][0], width, height)


def update_enemy_position(enemy, dt: float, width: int, height: int) -> None:
    route = ROUTES[EnemySpawnPoint(enemy.spawn_point)]
    directions = DIRECTIONS[EnemySpawnPoint(enemy.spawn_point)]
    if enemy.checkpoint >= len(directions):
        enemy.checkpoint = len(directions) - 1
    dx, dy = directions[enemy.checkpoint]
    enemy.x += dx * enemy.speed * dt
    enemy.y += dy * enemy.speed * dt
    next_index = min(enemy.checkpoint + 1, len(route) - 1)
    next_x, next_y = to_screen(*route[next_index], width, height)
    reached = (dx > 0 and enemy.x >= next_x) or (dx < 0 and enemy.x <= next_x) or (dy > 0 and enemy.y >= next_y) or (dy < 0 and enemy.y <= next_y)
    if reached and enemy.checkpoint < len(directions) - 1:
        enemy.checkpoint += 1
