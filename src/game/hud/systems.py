from __future__ import annotations

import pygame


def draw_hud(screen: pygame.Surface, font: pygame.font.Font, indicators, lives: int, in_round: bool) -> None:
    color = (220, 230, 255)
    status = [
        f"Round: {indicators.round_number}",
        f"WPM: {indicators.wpm:.1f}",
        f"Score: {indicators.score}",
        f"Streak: {indicators.streak}",
        f"Lives: {lives}",
        f"Difficulty: {indicators.difficulty.value}",
    ]
    for i, text in enumerate(status):
        screen.blit(font.render(text, True, color), (20 + 220 * i, 14))
    if not in_round:
        msg = "Press SPACE to start next round"
        screen.blit(font.render(msg, True, (255, 220, 80)), (screen.get_width() // 2 - 210, screen.get_height() - 50))
