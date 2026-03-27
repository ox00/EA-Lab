from __future__ import annotations

from typing import Dict, List

from .config import MarioConfig
from .models import LevelGrid, Tile


def _blank_segment(cfg: MarioConfig) -> LevelGrid:
    return [[Tile.EMPTY for _ in range(cfg.segment_width)] for _ in range(cfg.height)]


def _ground_segment(cfg: MarioConfig) -> LevelGrid:
    grid = _blank_segment(cfg)
    for row in range(cfg.height - 2, cfg.height):
        for col in range(cfg.segment_width):
            grid[row][col] = Tile.GROUND
    return grid


def _add_question(grid: LevelGrid, row: int, col: int) -> None:
    grid[row][col] = Tile.QUESTION


def _add_enemy(grid: LevelGrid, row: int, col: int) -> None:
    grid[row][col] = Tile.ENEMY


def build_segment_library(cfg: MarioConfig) -> Dict[int, LevelGrid]:
    segments: Dict[int, LevelGrid] = {}

    segments[0] = _ground_segment(cfg)

    segments[1] = _ground_segment(cfg)
    for col in range(5, 8):
        for row in range(cfg.height - 2, cfg.height):
            segments[1][row][col] = Tile.EMPTY

    segments[2] = _ground_segment(cfg)
    for offset, col in enumerate(range(6, cfg.segment_width)):
        top = cfg.height - 3 - min(offset, 3)
        for row in range(top, cfg.height):
            segments[2][row][col] = Tile.GROUND

    segments[3] = _ground_segment(cfg)
    for offset, col in enumerate(range(0, 8)):
        top = cfg.height - 6 + min(offset, 3)
        for row in range(top, cfg.height):
            segments[3][row][col] = Tile.GROUND

    segments[4] = _ground_segment(cfg)
    _add_enemy(segments[4], cfg.height - 3, cfg.segment_width // 2)

    segments[5] = _ground_segment(cfg)
    for col in range(4, 10):
        segments[5][cfg.height - 6][col] = Tile.GROUND

    segments[6] = _ground_segment(cfg)
    _add_question(segments[6], cfg.height - 7, 4)
    _add_question(segments[6], cfg.height - 7, 5)
    _add_question(segments[6], cfg.height - 7, 6)

    segments[7] = _ground_segment(cfg)
    for row in range(cfg.height - 6, cfg.height - 2):
        segments[7][row][6] = Tile.PIPE
        segments[7][row][7] = Tile.PIPE

    segments[8] = _ground_segment(cfg)
    for col in range(cfg.segment_width):
        segments[8][cfg.height - 3][col] = Tile.EMPTY
    for col in range(cfg.segment_width):
        segments[8][cfg.height - 2][col] = Tile.GROUND
        segments[8][cfg.height - 1][col] = Tile.GROUND

    segments[9] = _ground_segment(cfg)
    _add_enemy(segments[9], cfg.height - 3, 3)
    _add_enemy(segments[9], cfg.height - 3, 9)
    _add_question(segments[9], cfg.height - 7, 6)

    return segments
