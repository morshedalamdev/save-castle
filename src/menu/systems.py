from __future__ import annotations

import pygame


def draw_menu_overlay(screen: pygame.Surface, title_font: pygame.font.Font, body_font: pygame.font.Font, started: bool) -> None:
    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 170))
    screen.blit(shade, (0, 0))
    title = "Typing Defense"
    prompt = "Press SPACE to start" if not started else "Paused - Press ESC to resume"
    tips = "1/2/3 change difficulty | Backspace cancels current typing"
    screen.blit(title_font.render(title, True, (245, 245, 255)), (screen.get_width() // 2 - 190, screen.get_height() // 2 - 120))
    screen.blit(body_font.render(prompt, True, (255, 210, 110)), (screen.get_width() // 2 - 160, screen.get_height() // 2 - 40))
    screen.blit(body_font.render(tips, True, (200, 220, 240)), (screen.get_width() // 2 - 270, screen.get_height() // 2 + 5))
