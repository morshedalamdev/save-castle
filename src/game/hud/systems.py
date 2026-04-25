from __future__ import annotations

import pygame


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    indicators,
    lives: int,
    in_round: bool,
    hud_banner: pygame.Surface | None = None,
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

    if not in_round:
        msg = "Press SPACE to start next round"
        msg_surf = font.render(msg, True, (255, 220, 80))
        screen.blit(msg_surf, (sw // 2 - msg_surf.get_width() // 2, sh - 50))
