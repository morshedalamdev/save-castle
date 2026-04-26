from __future__ import annotations

import pygame

# Matches the Rust reference: UI_TEXT_COLOR (dark gray) / UI_NUMBER_TEXT_COLOR (white)
_LABEL_COLOR = (169, 169, 169)
_VALUE_COLOR = (255, 255, 255)
_DIFF_TITLE_COLOR = (80, 60, 40)
_DIFF_VALUE_COLOR = (255, 255, 255)


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    indicators,
    lives: int,
    in_round: bool,
    hud_banner: pygame.Surface | None = None,
    settings_bg: pygame.Surface | None = None,
    plus_img: pygame.Surface | None = None,
    minus_img: pygame.Surface | None = None,
    close_img: pygame.Surface | None = None,
) -> dict[str, pygame.Rect]:
    """Draw the in-game HUD and return a dict of clickable rects."""
    button_rects: dict[str, pygame.Rect] = {}
    sw, sh = screen.get_size()

    # ------------------------------------------------------------------ banner
    banner_y = 4
    banner_h = 0
    if hud_banner is not None:
        banner_w = int(sw * 0.48)
        banner_h = int(banner_w * hud_banner.get_height() / hud_banner.get_width())
        banner_x = sw // 2 - banner_w // 2
        scaled = pygame.transform.scale(hud_banner, (banner_w, banner_h))
        screen.blit(scaled, (banner_x, banner_y))

    # ---- two-tone stats text (label = muted gray, value = white) ----
    stats = [
        ("Score: ", str(indicators.score)),
        ("Streak: ", str(indicators.streak)),
        ("WPM: ", str(int(indicators.wpm))),
        ("Round: ", str(indicators.round_number)),
    ]
    label_surfs = [font.render(lbl, True, _LABEL_COLOR) for lbl, _ in stats]
    value_surfs = [font.render(val, True, _VALUE_COLOR) for _, val in stats]

    gap = int(sw * 0.025)
    pair_widths = [ls.get_width() + vs.get_width() for ls, vs in zip(label_surfs, value_surfs)]
    total_w = sum(pair_widths) + gap * (len(stats) - 1)
    text_h = max(s.get_height() for s in label_surfs)

    if banner_h > 0:
        text_y = banner_y + (banner_h - text_h) // 2
    else:
        text_y = banner_y + 8

    x = sw // 2 - total_w // 2
    for ls, vs, pw in zip(label_surfs, value_surfs, pair_widths):
        screen.blit(ls, (x, text_y))
        screen.blit(vs, (x + ls.get_width(), text_y))
        x += pw + gap

    # ------------------------------------------------------ difficulty panel
    if settings_bg is not None:
        diff_name = indicators.difficulty.value

        title_font = pygame.font.SysFont("courier", 18, bold=True)
        val_font = pygame.font.SysFont("courier", 20, bold=True)

        panel_w = max(180, int(sw * 0.10))
        panel_h = max(80, int(sh * 0.09))
        panel_x = sw - panel_w - 10
        panel_y = 8

        scaled_bg = pygame.transform.scale(settings_bg, (panel_w, panel_h))
        screen.blit(scaled_bg, (panel_x, panel_y))

        # "Difficulty" title
        title_surf = title_font.render("Difficulty", True, _DIFF_TITLE_COLOR)
        screen.blit(
            title_surf,
            (panel_x + panel_w // 2 - title_surf.get_width() // 2, panel_y + 6),
        )

        # Close (X) button — top-right corner of panel
        close_sz = max(20, int(panel_h * 0.28))
        close_rect = pygame.Rect(panel_x + panel_w - close_sz - 4, panel_y + 4, close_sz, close_sz)
        if close_img is not None:
            screen.blit(pygame.transform.scale(close_img, (close_sz, close_sz)), close_rect.topleft)
        button_rects["difficulty_close"] = close_rect

        # [-]  value  [+] row
        btn_sz = max(26, int(panel_h * 0.35))
        val_surf = val_font.render(diff_name, True, _DIFF_VALUE_COLOR)
        padding = 8
        row_w = btn_sz + padding + val_surf.get_width() + padding + btn_sz
        row_x = panel_x + panel_w // 2 - row_w // 2
        row_y = panel_y + panel_h // 2 + int(panel_h * 0.10)

        minus_rect = pygame.Rect(row_x, row_y - btn_sz // 2, btn_sz, btn_sz)
        if minus_img is not None:
            screen.blit(pygame.transform.scale(minus_img, (btn_sz, btn_sz)), minus_rect.topleft)
        button_rects["difficulty_minus"] = minus_rect

        val_x = row_x + btn_sz + padding
        screen.blit(val_surf, (val_x, row_y - val_surf.get_height() // 2))

        plus_rect = pygame.Rect(val_x + val_surf.get_width() + padding, row_y - btn_sz // 2, btn_sz, btn_sz)
        if plus_img is not None:
            screen.blit(pygame.transform.scale(plus_img, (btn_sz, btn_sz)), plus_rect.topleft)
        button_rects["difficulty_plus"] = plus_rect

    # ---------------------------------------- between-rounds message
    if not in_round:
        msg = "Press SPACE to start next round"
        msg_surf = font.render(msg, True, (255, 220, 80))
        screen.blit(msg_surf, (sw // 2 - msg_surf.get_width() // 2, sh - 50))

    return button_rects
