from __future__ import annotations

import random
from pathlib import Path

import pygame

from .boss.systems import spawn_boss_wave
from .castle.components import Castle
from .castle.resources import NumberOfLivesLeft
from .effects.components import Explosion
from .effects.systems import animate_explosions, draw_explosions
from .enemies.movement.components import EnemySpawnPoint
from .enemies.resources import EnemySpawnTimer
from .enemies.systems import EnemyAssets, draw_enemy, spawn_enemy, update_enemies
from .enemies.text.systems import on_letter_pressed, reset_typing
from .hud.systems import draw_hud
from .rounds_and_indicators.resources import Difficulty, RoundIndicators
from .rounds_and_indicators.systems import (
    increase_round_counter,
    increase_round_difficulty,
    reset_round,
    update_score_on_enemy_typed,
    update_wpm,
)


class GameRuntime:
    def __init__(self, root_dir: Path, screen: pygame.Surface) -> None:
        self.root_dir = root_dir
        self.screen = screen
        self.asset_root = root_dir / "assets"
        self.background = pygame.image.load((self.asset_root / "background/background_new.png").as_posix()).convert()
        self.castle_image = self._load_random_castle()
        self.explosion_sheet = pygame.image.load((self.asset_root / "sprites/effects/explosion.png").as_posix()).convert_alpha()
        self.enemy_assets = EnemyAssets(self.asset_root)
        self.words = self._load_words()

        self.indicators = RoundIndicators()
        self.lives = NumberOfLivesLeft()
        self.spawn_timer = EnemySpawnTimer()
        self.enemies = []
        self.typing_ids: set[int] = set()
        self.explosions: list[Explosion] = []
        self.in_round = False
        self.has_started = False
        self.paused = False

        self.hud_banner = pygame.image.load((self.asset_root / "ui" / "hud" / "hud_banner.png").as_posix()).convert_alpha()

        self.font = pygame.font.SysFont("arial", 34)
        self.hud_font = pygame.font.SysFont("arial", 32)

    def _load_words(self) -> list[str]:
        words_file = self.asset_root / "words/plain_words.txt"
        return [w.strip().lower() for w in words_file.read_text(encoding="utf-8").splitlines() if w.strip()]

    def _load_random_castle(self) -> pygame.Surface:
        idx = random.randint(0, 3)
        return pygame.image.load((self.asset_root / f"sprites/castle/castle{idx}.png").as_posix()).convert_alpha()

    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.indicators.difficulty = difficulty

    def start_next_round(self) -> None:
        self.has_started = True
        self.in_round = True
        increase_round_counter(self.indicators)
        reset_round(self.indicators)
        self.spawn_timer.interval = increase_round_difficulty(self.indicators)
        self.spawn_timer.elapsed = 0.0
        self.enemies.extend(
            spawn_boss_wave(self.words, self.indicators.round_number, self.screen.get_width(), self.screen.get_height(), self.indicators.enemy_base_speed)
        )

    def restart(self) -> None:
        self.indicators = RoundIndicators()
        self.lives = NumberOfLivesLeft()
        self.spawn_timer = EnemySpawnTimer()
        self.enemies = []
        self.typing_ids = set()
        self.explosions = []
        self.in_round = False
        self.has_started = False
        self.paused = False
        self.castle_image = self._load_random_castle()

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def handle_letter(self, letter: str) -> None:
        kills = on_letter_pressed(letter, self.enemies, self.typing_ids, self.indicators)
        if kills:
            self._remove_typed_enemies(kills)

    def reset_typing(self) -> None:
        reset_typing(self.enemies, self.typing_ids)

    def _remove_typed_enemies(self, kill_count: int) -> None:
        removed = 0
        kept = []
        for enemy in self.enemies:
            if enemy.typing_index >= len(enemy.word) - 1 and removed < kill_count:
                removed += 1
                self.indicators.enemies_typed += 1
                self.indicators.enemies_unlived += 1
                update_wpm(self.indicators)
                update_score_on_enemy_typed(self.indicators)
                self.typing_ids.discard(id(enemy))
            else:
                kept.append(enemy)
        self.enemies = kept

    def _spawn_enemy_if_needed(self, dt: float) -> None:
        if self.indicators.enemies_spawned >= self.indicators.max_enemies_this_round:
            return
        self.spawn_timer.elapsed += dt
        if self.spawn_timer.elapsed < self.spawn_timer.interval:
            return
        self.spawn_timer.elapsed = 0.0
        word = random.choice(self.words)
        last_spawn = self.enemies[-1].spawn_point if self.enemies else None
        candidates = [sp for sp in EnemySpawnPoint if sp.value != last_spawn]
        spawn_point = random.choice(candidates)
        self.enemies.append(
            spawn_enemy(word, self.screen.get_width(), self.screen.get_height(), self.indicators.enemy_base_speed, spawn_point)
        )
        self.indicators.enemies_spawned += 1

    def _enemy_castle_collision(self) -> None:
        castle_rect = pygame.Rect(self.screen.get_width() // 2 - 145, self.screen.get_height() // 2 - 65, 290, 205)
        survivors = []
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(int(enemy.x - 20), int(enemy.y - 20), 40, 40)
            if castle_rect.colliderect(enemy_rect):
                self.indicators.enemies_unlived += 1
                self.indicators.streak = 0
                self.lives.number = max(0, self.lives.number - 1)
                self.explosions.append(Explosion(enemy.x, enemy.y))
                self.typing_ids.discard(id(enemy))
            else:
                survivors.append(enemy)
        self.enemies = survivors

    def _despawn_outside(self) -> None:
        width, height = self.screen.get_size()
        survivors = []
        for enemy in self.enemies:
            if enemy.x < -0.2 * width or enemy.x > 1.2 * width or enemy.y < -0.2 * height or enemy.y > 1.2 * height:
                self.indicators.enemies_unlived += 1
                self.indicators.streak = 0
                self.typing_ids.discard(id(enemy))
            else:
                survivors.append(enemy)
        self.enemies = survivors

    def update(self, dt: float) -> None:
        if self.paused or not self.has_started:
            return
        if self.lives.number <= 0:
            self.in_round = False
            return
        if self.in_round:
            self.indicators.elapsed_round_seconds += dt
            self._spawn_enemy_if_needed(dt)
            update_enemies(self.enemies, dt, self.screen.get_width(), self.screen.get_height())
            self._enemy_castle_collision()
            self._despawn_outside()
            update_wpm(self.indicators)
            if self.indicators.enemies_unlived >= self.indicators.max_enemies_this_round:
                self.in_round = False

        animate_explosions(self.explosions, dt)

    def draw(self) -> None:
        bg = pygame.transform.scale(self.background, self.screen.get_size())
        self.screen.blit(bg, (0, 0))

        castle_size = (480, 360)
        castle = pygame.transform.scale(self.castle_image, castle_size)
        self.screen.blit(castle, (self.screen.get_width() // 2 - castle_size[0] // 2, self.screen.get_height() // 2 - castle_size[1] // 2 + 20))

        for enemy in self.enemies:
            draw_enemy(self.screen, enemy, self.enemy_assets, self.font)
        draw_explosions(self.screen, self.explosions, self.explosion_sheet)

        draw_hud(self.screen, self.hud_font, self.indicators, self.lives.number, self.in_round, self.hud_banner)
