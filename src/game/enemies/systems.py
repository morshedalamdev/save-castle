from __future__ import annotations

import random
from pathlib import Path

import pygame

from .components import Enemy, EnemyType
from .movement.components import EnemySpawnPoint
from .movement.systems import spawn_position, update_enemy_position

BASE_ANIMATION_SPEED = 5.0
ENEMY_SPRITE_SCALE_FACTOR = 1.4


class EnemyAssets:
    def __init__(self, asset_root: Path) -> None:
        self._sheet_cache: dict[str, pygame.Surface] = {}
        self.asset_root = asset_root

    def sprite_sheet(self, enemy: Enemy) -> pygame.Surface:
        key = enemy.sprite_name
        if key not in self._sheet_cache:
            path = self.asset_root / f"sprites/enemies/{key}.png"
            self._sheet_cache[key] = pygame.image.load(path.as_posix()).convert_alpha()
        return self._sheet_cache[key]


def spawn_enemy(word: str, width: int, height: int, base_speed: float, spawn_point: EnemySpawnPoint | None = None, *, ghost: bool = False) -> Enemy:
    if spawn_point is None:
        spawn_point = random.choice(list(EnemySpawnPoint))
    enemy_type = EnemyType.SNAIL if ghost else random.choice(list(EnemyType))
    x, y = spawn_position(spawn_point, width, height)
    speed = (random.random() * 0.75 + 0.625) * base_speed
    return Enemy(word=word, enemy_type=enemy_type, spawn_point=spawn_point.value, x=x, y=y, speed=speed, is_boss_ghost=ghost)


def update_enemies(enemies, dt: float, width: int, height: int) -> None:
    for enemy in enemies:
        update_enemy_position(enemy, dt, width, height)
        enemy.frame_timer += dt
        anim_interval = BASE_ANIMATION_SPEED / max(enemy.speed, 1)
        if enemy.frame_timer >= anim_interval:
            enemy.frame_timer = 0.0
            enemy.frame_index = (enemy.frame_index + 1) % max(enemy.animation_length, 1)


def draw_enemy(screen: pygame.Surface, enemy: Enemy, assets: EnemyAssets, font: pygame.font.Font) -> None:
    sheet = assets.sprite_sheet(enemy)
    frame_w, frame_h = enemy.frame_size
    frame_rect = pygame.Rect(enemy.frame_index * frame_w, 0, frame_w, frame_h)
    sprite = sheet.subsurface(frame_rect)
    scaled_size = (int(frame_w * ENEMY_SPRITE_SCALE_FACTOR), int(frame_h * ENEMY_SPRITE_SCALE_FACTOR))
    sprite = pygame.transform.scale(sprite, scaled_size)
    if enemy.spawn_point in {EnemySpawnPoint.TOP_LEFT.value, EnemySpawnPoint.LEFT.value, EnemySpawnPoint.BOTTOM_LEFT.value}:
        sprite = pygame.transform.flip(sprite, True, False)
    screen.blit(sprite, (enemy.x - scaled_size[0] // 2, enemy.y - scaled_size[1] // 2))

    normal_color = (180, 230, 255)
    typing_color = (255, 90, 55)
    done = max(enemy.typing_index + 1, 0)
    typed = enemy.word[:done]
    rest = enemy.word[done:]
    typed_surface = font.render(typed, True, typing_color)
    rest_surface = font.render(rest, True, normal_color)
    text_width = typed_surface.get_width() + rest_surface.get_width()
    tx = enemy.x - text_width / 2
    ty = enemy.y - enemy.text_offset_y
    screen.blit(typed_surface, (tx, ty))
    screen.blit(rest_surface, (tx + typed_surface.get_width(), ty))
