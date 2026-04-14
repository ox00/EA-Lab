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


def render_pygame(level: Level, path: str, tile_size: int = 24) -> None:
    try:
        import pygame
    except ImportError as exc:  # pragma: no cover - dependency/environment dependent
        raise RuntimeError("pygame is required for pygame rendering. Install via: pip install pygame") from exc

    rows = len(level.grid)
    cols = len(level.grid[0]) if rows else 0
    width = cols * tile_size
    height = rows * tile_size

    # Default to headless mode so PNG export works on CI/servers without display.
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    surface = pygame.Surface((width, height))
    for row_idx, row in enumerate(level.grid):
        for col_idx, tile in enumerate(row):
            color = TILE_COLORS.get(tile, (0, 0, 0))
            rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surface, str(output_path))
    pygame.quit()
