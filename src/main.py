from __future__ import annotations

from pathlib import Path

import pygame

from game.runtime import GameRuntime
from menu.systems import MenuOverlay
from game.rounds_and_indicators.resources import Difficulty

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Typing Defense")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    root = Path(__file__).resolve().parent.parent
    runtime = GameRuntime(root, screen)
    menu = MenuOverlay(root / "assets")

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        show_menu = not runtime.has_started or runtime.paused or runtime.lives.number <= 0
        menu_started = runtime.has_started and runtime.paused and runtime.lives.number > 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                runtime.screen = screen

            elif show_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and runtime.has_started and runtime.lives.number > 0:
                        menu.state = "menu"
                        runtime.toggle_pause()
                action = menu.handle_event(event, menu_started)
                if action == "start":
                    menu.state = "menu"
                    if runtime.lives.number <= 0:
                        runtime.restart()
                    runtime.paused = False
                    runtime.start_next_round()
                elif action == "resume":
                    menu.state = "menu"
                    runtime.toggle_pause()
                elif action == "restart":
                    menu.state = "menu"
                    runtime.restart()
                    runtime.start_next_round()
                elif action == "howtoplay":
                    menu.state = "howtoplay"
                elif action == "back":
                    menu.state = "menu"
                elif action == "spawn":
                    # Spawn a demo mushroom enemy so the player can practice
                    from game.enemies.systems import spawn_enemy
                    from game.enemies.movement.components import EnemySpawnPoint
                    demo = spawn_enemy(
                        MenuOverlay.DEMO_WORD,
                        screen.get_width(),
                        screen.get_height(),
                        runtime.indicators.enemy_base_speed,
                        EnemySpawnPoint.LEFT,
                    )
                    runtime.enemies.append(demo)
                elif action == "exit":
                    running = False

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and runtime.has_started:
                        runtime.toggle_pause()
                    elif event.key == pygame.K_SPACE:
                        if not runtime.in_round:
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

        if show_menu:
            menu.draw(screen, menu_started)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
