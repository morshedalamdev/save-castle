from __future__ import annotations

from pathlib import Path

import pygame

from game.runtime import GameRuntime
from menu.systems import draw_menu_overlay
from game.rounds_and_indicators.resources import Difficulty

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Typing Defense")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    runtime = GameRuntime(Path(__file__).resolve().parent.parent, screen)
    title_font = pygame.font.SysFont("arial", 64)
    body_font = pygame.font.SysFont("arial", 34)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                runtime.screen = screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and runtime.has_started:
                    runtime.toggle_pause()
                elif event.key == pygame.K_SPACE:
                    if not runtime.has_started or not runtime.in_round:
                        runtime.paused = False
                        runtime.start_next_round()
                elif event.key == pygame.K_BACKSPACE:
                    runtime.reset_typing()
                elif event.key == pygame.K_1:
                    runtime.set_difficulty(Difficulty.EASY)
                elif event.key == pygame.K_2:
                    runtime.set_difficulty(Difficulty.MEDIUM)
                elif event.key == pygame.K_3:
                    runtime.set_difficulty(Difficulty.HARD)
                else:
                    if event.unicode and event.unicode.isalpha() and runtime.in_round and not runtime.paused:
                        runtime.handle_letter(event.unicode.lower())

        runtime.update(dt)
        runtime.draw()

        if not runtime.has_started or runtime.paused or runtime.lives.number <= 0:
            draw_menu_overlay(screen, title_font, body_font, runtime.has_started)
            if runtime.lives.number <= 0:
                game_over = body_font.render("Game Over - Press SPACE to restart", True, (255, 120, 120))
                screen.blit(game_over, (screen.get_width() // 2 - 230, screen.get_height() // 2 + 60))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
