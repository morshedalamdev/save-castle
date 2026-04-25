from __future__ import annotations

from pathlib import Path

import pygame


class MenuOverlay:
    """Sprite-based menu overlay with scroll banner and button images."""

    BANNER_W_RATIO = 0.22
    BANNER_H_RATIO = 0.58
    HOWTO_H_RATIO = 0.72
    DEMO_WORD = "best"

    _INSTRUCTIONS = [
        "The goal of the game is to prevent",
        "the animals that spawn at the",
        "borders of the screen from",
        "reaching the castle in the middle.",
        "This is done by typing the words",
        "that are above the animals. Try",
        "'typing' the animal below:",
    ]
    _HINTS = [
        "Hint: Try using backspace or",
        "intentionally typing wrong letters",
        "Also: Esc Pauses the game",
    ]

    def __init__(self, asset_root: Path) -> None:
        menu_root = asset_root / "ui" / "menu"
        self._banner_raw = pygame.image.load((menu_root / "mainMenuBanner.png").as_posix()).convert_alpha()
        self._btn_raw = pygame.image.load((menu_root / "mainMenuButton.png").as_posix()).convert_alpha()
        self._mushroom_sheet = pygame.image.load(
            (asset_root / "sprites" / "enemies" / "mushroom.png").as_posix()
        ).convert_alpha()
        self.state = "menu"
        self._btn_font = pygame.font.SysFont("courier", 22, bold=True)
        self._body_font = pygame.font.SysFont("courier", 19)
        self._button_rects: dict[str, pygame.Rect] = {}

    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event, started: bool) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action, rect in self._button_rects.items():
                if rect.collidepoint(event.pos):
                    return action
        return None

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface, started: bool) -> None:
        shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 130))
        screen.blit(shade, (0, 0))

        sw, sh = screen.get_size()
        bw = int(sw * self.BANNER_W_RATIO)
        h_ratio = self.HOWTO_H_RATIO if self.state == "howtoplay" else self.BANNER_H_RATIO
        bh = int(sh * h_ratio)
        bx = sw // 2 - bw // 2
        by = sh // 2 - bh // 2

        banner = pygame.transform.scale(self._banner_raw, (bw, bh))
        screen.blit(banner, (bx, by))

        self._button_rects.clear()
        if self.state == "howtoplay":
            self._draw_howtoplay(screen, bx, by, bw, bh)
        else:
            self._draw_main_buttons(screen, bx, by, bw, bh, started)

    # ------------------------------------------------------------------
    def _draw_main_buttons(
        self, screen: pygame.Surface, bx: int, by: int, bw: int, bh: int, started: bool
    ) -> None:
        if started:
            labels = ["Resume Game", "How to play", "Restart"]
            actions = ["resume", "howtoplay", "restart"]
        else:
            labels = ["Start Game", "How to play", "Exit"]
            actions = ["start", "howtoplay", "exit"]

        btn_w = int(bw * 0.82)
        btn_h = int(bh * 0.13)
        btn_x = bx + (bw - btn_w) // 2

        content_start = by + int(bh * 0.20)
        content_h = int(bh * 0.62)
        slot_h = content_h // 3

        for i, (label, action) in enumerate(zip(labels, actions)):
            btn_y = content_start + slot_h * i + (slot_h - btn_h) // 2
            rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            self._button_rects[action] = rect

            btn_img = pygame.transform.scale(self._btn_raw, (btn_w, btn_h))
            screen.blit(btn_img, rect.topleft)

            text = self._btn_font.render(label, True, (255, 255, 255))
            screen.blit(
                text,
                (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2),
            )

    # ------------------------------------------------------------------
    def _draw_howtoplay(
        self, screen: pygame.Surface, bx: int, by: int, bw: int, bh: int
    ) -> None:
        text_x = bx + int(bw * 0.07)
        text_y = by + int(bh * 0.07)
        for line in self._INSTRUCTIONS:
            surf = self._body_font.render(line, True, (255, 255, 255))
            screen.blit(surf, (text_x, text_y))
            text_y += surf.get_height() + 4

        demo_word = self.DEMO_WORD
        word_surf = self._btn_font.render(demo_word, True, (255, 255, 255))
        demo_word_x = bx + bw // 2 - word_surf.get_width() // 2
        demo_word_y = by + int(bh * 0.50)
        screen.blit(word_surf, (demo_word_x, demo_word_y))

        frame_w, frame_h = 32, 32
        sprite = self._mushroom_sheet.subsurface(pygame.Rect(0, 0, frame_w, frame_h))
        scale = max(2.0, bw / 192 * 1.4)
        scaled = pygame.transform.scale(sprite, (int(frame_w * scale), int(frame_h * scale)))
        enemy_x = bx + bw // 2 - scaled.get_width() // 2
        enemy_y = demo_word_y + word_surf.get_height() + 4
        screen.blit(scaled, (enemy_x, enemy_y))

        btn_w = int(bw * 0.36)
        btn_h = int(bh * 0.09)
        gap = int(bw * 0.06)
        total_btn_w = btn_w * 2 + gap
        btn_start_x = bx + (bw - total_btn_w) // 2
        btn_y = enemy_y + scaled.get_height() + int(bh * 0.025)

        for label, action, offset in [("Spawn", "spawn", 0), ("Back", "back", btn_w + gap)]:
            rect = pygame.Rect(btn_start_x + offset, btn_y, btn_w, btn_h)
            self._button_rects[action] = rect
            btn_img = pygame.transform.scale(self._btn_raw, (btn_w, btn_h))
            screen.blit(btn_img, rect.topleft)
            text = self._btn_font.render(label, True, (255, 255, 255))
            screen.blit(
                text,
                (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2),
            )

        hint_y = btn_y + btn_h + int(bh * 0.02)
        for hint in self._HINTS:
            surf = self._body_font.render(hint, True, (255, 255, 255))
            screen.blit(surf, (bx + int(bw * 0.05), hint_y))
            hint_y += surf.get_height() + 3
