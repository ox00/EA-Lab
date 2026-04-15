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


def _add_coin(grid: LevelGrid, row: int, col: int) -> None:
    grid[row][col] = Tile.COIN


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

    segments[10] = _ground_segment(cfg)
    for col in range(2, 12):
        segments[10][cfg.height - 5][col] = Tile.BRICK
    for col in range(4, 10):
        segments[10][cfg.height - 8][col] = Tile.BRICK
    _add_coin(segments[10], cfg.height - 9, 6)

    segments[11] = _ground_segment(cfg)
    for col in range(1, 13):
        segments[11][cfg.height - 6][col] = Tile.BRICK
    _add_enemy(segments[11], cfg.height - 3, 3)
    _add_enemy(segments[11], cfg.height - 3, 10)
    _add_question(segments[11], cfg.height - 8, 5)
    _add_question(segments[11], cfg.height - 8, 8)

    segments[12] = _ground_segment(cfg)
    for col in range(0, 14):
        if col not in {6, 7}:
            segments[12][cfg.height - 4][col] = Tile.BRICK
    for col in range(3, 11):
        segments[12][cfg.height - 7][col] = Tile.BRICK
    _add_coin(segments[12], cfg.height - 8, 6)
    _add_coin(segments[12], cfg.height - 8, 7)

    segments[13] = _ground_segment(cfg)
    for offset, col in enumerate(range(1, 7)):
        top = cfg.height - 3 - offset
        for row in range(top, cfg.height):
            segments[13][row][col] = Tile.GROUND
    for offset, col in enumerate(range(8, 13)):
        top = cfg.height - 7 + offset
        for row in range(top, cfg.height):
            segments[13][row][col] = Tile.GROUND
    _add_question(segments[13], cfg.height - 9, 5)
    _add_question(segments[13], cfg.height - 7, 9)

    segments[14] = _ground_segment(cfg)
    for row in range(cfg.height - 7, cfg.height - 2):
        segments[14][row][4] = Tile.PIPE
        segments[14][row][5] = Tile.PIPE
        segments[14][row][9] = Tile.PIPE
        segments[14][row][10] = Tile.PIPE
    for col in range(2, 12):
        segments[14][cfg.height - 8][col] = Tile.BRICK
    _add_coin(segments[14], cfg.height - 9, 7)

    segments[15] = _ground_segment(cfg)
    for col in range(0, 5):
        for row in range(cfg.height - 4, cfg.height):
            segments[15][row][col] = Tile.GROUND
    for col in range(5, 9):
        for row in range(cfg.height - 6, cfg.height):
            segments[15][row][col] = Tile.GROUND
    for col in range(9, 14):
        for row in range(cfg.height - 4, cfg.height):
            segments[15][row][col] = Tile.GROUND
    _add_enemy(segments[15], cfg.height - 7, 6)

    segments[16] = _ground_segment(cfg)
    for col in range(1, 13):
        segments[16][cfg.height - 6][col] = Tile.BRICK
    for col in range(3, 11):
        segments[16][cfg.height - 9][col] = Tile.QUESTION
    for col in range(4, 10, 2):
        _add_coin(segments[16], cfg.height - 10, col)

    segments[17] = _ground_segment(cfg)
    for col in range(2, 12):
        segments[17][cfg.height - 5][col] = Tile.BRICK
    for col in range(4, 10):
        segments[17][cfg.height - 8][col] = Tile.BRICK
    for row in range(cfg.height - 6, cfg.height - 2):
        segments[17][row][2] = Tile.PIPE
        segments[17][row][3] = Tile.PIPE
    _add_enemy(segments[17], cfg.height - 3, 8)
    _add_enemy(segments[17], cfg.height - 3, 11)
    _add_question(segments[17], cfg.height - 10, 6)

    return segments
