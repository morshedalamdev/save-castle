from __future__ import annotations

import pygame


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    indicators,
    lives: int,
    in_round: bool,
    hud_banner: pygame.Surface | None = None,
    settings_bg: pygame.Surface | None = None,
) -> None:
    sw, sh = screen.get_size()

    if hud_banner is not None:
        banner_w = int(sw * 0.42)
        banner_h = int(banner_w * hud_banner.get_height() / hud_banner.get_width())
        banner_x = sw // 2 - banner_w // 2
        banner_y = 4
        scaled = pygame.transform.scale(hud_banner, (banner_w, banner_h))
        screen.blit(scaled, (banner_x, banner_y))

    color = (220, 230, 255)
    stats = [
        f"Score: {indicators.score}",
        f"Streak: {indicators.streak}",
        f"WPM: {int(indicators.wpm)}",
        f"Round: {indicators.round_number}",
    ]
    texts = [font.render(s, True, color) for s in stats]
    gap = int(sw * 0.03)
    total_w = sum(t.get_width() for t in texts) + gap * (len(texts) - 1)
    x = sw // 2 - total_w // 2
    y = 12
    for text in texts:
        screen.blit(text, (x, y))
        x += text.get_width() + gap

    if settings_bg is not None:
        diff_name = indicators.difficulty.value
        diff_font = pygame.font.SysFont("courier", 20, bold=True)
        diff_surf = diff_font.render(diff_name, True, (255, 255, 255))
        padding = 12
        bg_w = max(diff_surf.get_width() + padding * 2, 80)
        bg_h = max(diff_surf.get_height() + padding * 2, 60)
        bg_x = sw - bg_w - 8
        bg_y = 8
        scaled_bg = pygame.transform.scale(settings_bg, (bg_w, bg_h))
        screen.blit(scaled_bg, (bg_x, bg_y))
        screen.blit(
            diff_surf,
            (bg_x + bg_w // 2 - diff_surf.get_width() // 2, bg_y + bg_h // 2 - diff_surf.get_height() // 2),
        )

    if not in_round:
        msg = "Press SPACE to start next round"
        msg_surf = font.render(msg, True, (255, 220, 80))
        screen.blit(msg_surf, (sw // 2 - msg_surf.get_width() // 2, sh - 50))
