from __future__ import annotations

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


def level_to_ascii(level: Level) -> str:
    return "\n".join("".join(ASCII_TILE.get(value, "X") for value in row) for row in level.grid)


def render_ascii(level: Level, path: str) -> None:
    Path(path).write_text(level_to_ascii(level) + "\n", encoding="utf-8")
