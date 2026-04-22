from __future__ import annotations

import pygame

from .components import EXPLOSION_ANIMATION_SPEED


def animate_explosions(explosions, dt: float) -> None:
    to_remove = []
    for idx, explosion in enumerate(explosions):
        explosion.timer += dt
        if explosion.timer >= EXPLOSION_ANIMATION_SPEED:
            explosion.timer = 0.0
            explosion.frame += 1
            if explosion.frame >= 9:
                to_remove.append(idx)
    for idx in reversed(to_remove):
        explosions.pop(idx)


def draw_explosions(screen: pygame.Surface, explosions, sprite_sheet: pygame.Surface | None) -> None:
    if sprite_sheet is None:
        return
    frame_w, frame_h = 192, 192
    for e in explosions:
        rect = pygame.Rect(e.frame * frame_w, 0, frame_w, frame_h)
        frame = sprite_sheet.subsurface(rect)
        screen.blit(frame, (e.x - frame_w // 2, e.y - frame_h // 2))
