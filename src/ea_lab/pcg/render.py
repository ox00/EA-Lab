from __future__ import annotations

import os
from pathlib import Path

from .models import Level, Tile


ASCII_TILE = {
    Tile.EMPTY: ".",
    Tile.GROUND: "#",
    Tile.BRICK: "B",
    Tile.QUESTION: "?",
    Tile.COIN: "o",
    Tile.ENEMY: "E",
    Tile.PIPE: "P",
    Tile.START: "S",
    Tile.GOAL: "G",
}

TILE_COLORS = {
    Tile.EMPTY: (186, 226, 255),
    Tile.GROUND: (117, 82, 50),
    Tile.BRICK: (157, 93, 48),
    Tile.QUESTION: (245, 201, 77),
    Tile.COIN: (255, 225, 84),
    Tile.ENEMY: (203, 79, 77),
    Tile.PIPE: (66, 163, 96),
    Tile.START: (92, 117, 214),
    Tile.GOAL: (242, 124, 58),
}


def level_to_ascii(level: Level) -> str:
    return "\n".join("".join(ASCII_TILE.get(value, "X") for value in row) for row in level.grid)


def render_ascii(level: Level, path: str) -> None:
    Path(path).write_text(level_to_ascii(level) + "\n", encoding="utf-8")


def _draw_background(pygame, surface, width: int, height: int) -> None:
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = (
            int(123 + (214 - 123) * ratio),
            int(198 + (233 - 198) * ratio),
            int(255 - 18 * ratio),
        )
        pygame.draw.line(surface, color, (0, y), (width, y))


def _draw_tile(pygame, surface, tile: int, rect) -> None:
    x, y, w, h = rect

    if tile == Tile.EMPTY:
        return

    if tile == Tile.GROUND:
        pygame.draw.rect(surface, (138, 94, 55), rect)
        pygame.draw.rect(surface, (115, 77, 44), (x, y + h * 0.18, w, h * 0.82))
        pygame.draw.rect(surface, (160, 116, 71), (x, y, w, h * 0.18))
        return

    if tile == Tile.BRICK:
        pygame.draw.rect(surface, (168, 93, 52), rect)
        pygame.draw.line(surface, (116, 62, 36), (x, y + h // 2), (x + w, y + h // 2), 2)
        pygame.draw.line(surface, (116, 62, 36), (x + w // 2, y), (x + w // 2, y + h // 2), 2)
        pygame.draw.line(surface, (116, 62, 36), (x + w // 3, y + h // 2), (x + w // 3, y + h), 2)
        return

    if tile == Tile.QUESTION:
        pygame.draw.rect(surface, (242, 187, 53), rect, border_radius=4)
        pygame.draw.circle(surface, (255, 243, 168), (x + w // 2, y + h // 2 - 2), max(2, w // 7))
        pygame.draw.rect(surface, (255, 243, 168), (x + w * 0.45, y + h * 0.68, w * 0.1, h * 0.1))
        return

    if tile == Tile.COIN:
        pygame.draw.ellipse(surface, (255, 214, 72), (x + w * 0.2, y + h * 0.12, w * 0.6, h * 0.76))
        pygame.draw.ellipse(surface, (250, 241, 169), (x + w * 0.33, y + h * 0.2, w * 0.14, h * 0.48))
        return

    if tile == Tile.ENEMY:
        pygame.draw.ellipse(surface, (177, 92, 70), (x + w * 0.14, y + h * 0.35, w * 0.72, h * 0.45))
        pygame.draw.circle(surface, (255, 255, 255), (int(x + w * 0.35), int(y + h * 0.46)), max(2, w // 10))
        pygame.draw.circle(surface, (255, 255, 255), (int(x + w * 0.65), int(y + h * 0.46)), max(2, w // 10))
        pygame.draw.circle(surface, (30, 30, 30), (int(x + w * 0.35), int(y + h * 0.46)), max(1, w // 20))
        pygame.draw.circle(surface, (30, 30, 30), (int(x + w * 0.65), int(y + h * 0.46)), max(1, w // 20))
        return

    if tile == Tile.PIPE:
        pygame.draw.rect(surface, (61, 153, 84), rect)
        pygame.draw.rect(surface, (81, 191, 104), (x + w * 0.08, y + h * 0.05, w * 0.18, h * 0.9))
        pygame.draw.rect(surface, (41, 120, 64), (x + w * 0.74, y + h * 0.05, w * 0.18, h * 0.9))
        pygame.draw.rect(surface, (72, 184, 98), (x - w * 0.08, y, w * 1.16, h * 0.22))
        return

    if tile == Tile.START:
        pygame.draw.rect(surface, (80, 101, 215), rect, border_radius=5)
        pygame.draw.polygon(
            surface,
            (232, 240, 255),
            [(x + w * 0.28, y + h * 0.2), (x + w * 0.28, y + h * 0.8), (x + w * 0.76, y + h * 0.5)],
        )
        return

    if tile == Tile.GOAL:
        pygame.draw.rect(surface, (238, 129, 58), (x + w * 0.2, y + h * 0.12, w * 0.14, h * 0.78))
        pygame.draw.polygon(
            surface,
            (255, 240, 201),
            [(x + w * 0.34, y + h * 0.18), (x + w * 0.82, y + h * 0.3), (x + w * 0.34, y + h * 0.42)],
        )
        return

    pygame.draw.rect(surface, TILE_COLORS.get(tile, (0, 0, 0)), rect)


def render_pygame(level: Level, path: str, tile_size: int = 24) -> None:
    try:
        import pygame
    except ImportError as exc:  # pragma: no cover - dependency/environment dependent
        raise RuntimeError("pygame is required for pygame rendering. Install via: pip install pygame") from exc

    rows = len(level.grid)
    cols = len(level.grid[0]) if rows else 0
    width = cols * tile_size
    height = rows * tile_size

    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    surface = pygame.Surface((width, height))
    _draw_background(pygame, surface, width, height)

    for row_idx, row in enumerate(level.grid):
        for col_idx, tile in enumerate(row):
            rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)
            _draw_tile(pygame, surface, tile, rect)

    for row_idx in range(rows):
        pygame.draw.line(surface, (255, 255, 255, 30), (0, row_idx * tile_size), (width, row_idx * tile_size), 1)
    for col_idx in range(cols):
        pygame.draw.line(surface, (255, 255, 255, 18), (col_idx * tile_size, 0), (col_idx * tile_size, height), 1)

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surface, str(output_path))
    pygame.quit()
