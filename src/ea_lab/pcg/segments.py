from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List

from .config import MarioConfig
from .models import LevelGrid, Tile


@dataclass(frozen=True)
class SegmentSpec:
    segment_id: int
    family: str
    variant: str
    difficulty_tier: int
    grid: LevelGrid

    def metadata(self) -> Dict[str, object]:
        return {
            "segment_id": self.segment_id,
            "family": self.family,
            "variant": self.variant,
            "difficulty_tier": self.difficulty_tier,
        }


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


def _add_segment(
    library: Dict[int, SegmentSpec],
    segment_id: int,
    family: str,
    variant: str,
    difficulty_tier: int,
    grid: LevelGrid,
) -> None:
    library[segment_id] = SegmentSpec(
        segment_id=segment_id,
        family=family,
        variant=variant,
        difficulty_tier=difficulty_tier,
        grid=grid,
    )


@lru_cache(maxsize=16)
def _build_segment_spec_library(
    height: int,
    segment_width: int,
    num_segments: int,
) -> Dict[int, SegmentSpec]:
    cfg = MarioConfig(height=height, segment_width=segment_width, num_segments=num_segments)
    segments: Dict[int, SegmentSpec] = {}

    _add_segment(segments, 0, "flat_safe", "plain_run", 1, _ground_segment(cfg))

    grid = _ground_segment(cfg)
    for col in range(5, 8):
        for row in range(cfg.height - 2, cfg.height):
            grid[row][col] = Tile.EMPTY
    _add_segment(segments, 1, "gap_jump", "micro_gap", 2, grid)

    grid = _ground_segment(cfg)
    for offset, col in enumerate(range(6, cfg.segment_width)):
        top = cfg.height - 3 - min(offset, 3)
        for row in range(top, cfg.height):
            grid[row][col] = Tile.GROUND
    _add_segment(segments, 2, "stair_climb", "right_ramp", 2, grid)

    grid = _ground_segment(cfg)
    for offset, col in enumerate(range(0, 8)):
        top = cfg.height - 6 + min(offset, 3)
        for row in range(top, cfg.height):
            grid[row][col] = Tile.GROUND
    _add_segment(segments, 3, "stair_climb", "left_ramp", 2, grid)

    grid = _ground_segment(cfg)
    _add_enemy(grid, cfg.height - 3, cfg.segment_width // 2)
    _add_segment(segments, 4, "enemy_pressure", "single_patrol", 2, grid)

    grid = _ground_segment(cfg)
    for col in range(4, 10):
        grid[cfg.height - 6][col] = Tile.GROUND
    _add_segment(segments, 5, "reward_relief", "mid_platform", 1, grid)

    grid = _ground_segment(cfg)
    _add_question(grid, cfg.height - 7, 4)
    _add_question(grid, cfg.height - 7, 5)
    _add_question(grid, cfg.height - 7, 6)
    _add_segment(segments, 6, "reward_relief", "triple_question", 1, grid)

    grid = _ground_segment(cfg)
    for row in range(cfg.height - 6, cfg.height - 2):
        grid[row][6] = Tile.PIPE
        grid[row][7] = Tile.PIPE
    _add_segment(segments, 7, "pipe_pressure", "center_pipe", 2, grid)

    grid = _ground_segment(cfg)
    for col in range(cfg.segment_width):
        grid[cfg.height - 3][col] = Tile.EMPTY
    for col in range(cfg.segment_width):
        grid[cfg.height - 2][col] = Tile.GROUND
        grid[cfg.height - 1][col] = Tile.GROUND
    _add_segment(segments, 8, "gap_jump", "full_gap_lane", 3, grid)

    grid = _ground_segment(cfg)
    _add_enemy(grid, cfg.height - 3, 3)
    _add_enemy(grid, cfg.height - 3, 9)
    _add_question(grid, cfg.height - 7, 6)
    _add_segment(segments, 9, "mixed_challenge", "dual_enemy_reward", 3, grid)

    grid = _ground_segment(cfg)
    for col in range(2, 12):
        grid[cfg.height - 5][col] = Tile.BRICK
    for col in range(4, 10):
        grid[cfg.height - 8][col] = Tile.BRICK
    _add_coin(grid, cfg.height - 9, 6)
    _add_segment(segments, 10, "reward_relief", "double_shelf_coin", 1, grid)

    grid = _ground_segment(cfg)
    for col in range(1, 13):
        grid[cfg.height - 6][col] = Tile.BRICK
    _add_enemy(grid, cfg.height - 3, 3)
    _add_enemy(grid, cfg.height - 3, 10)
    _add_question(grid, cfg.height - 8, 5)
    _add_question(grid, cfg.height - 8, 8)
    _add_segment(segments, 11, "enemy_pressure", "double_enemy_bridges", 3, grid)

    grid = _ground_segment(cfg)
    for col in range(0, 14):
        if col not in {6, 7}:
            grid[cfg.height - 4][col] = Tile.BRICK
    for col in range(3, 11):
        grid[cfg.height - 7][col] = Tile.BRICK
    _add_coin(grid, cfg.height - 8, 6)
    _add_coin(grid, cfg.height - 8, 7)
    _add_segment(segments, 12, "gap_jump", "ceiling_gap_reward", 3, grid)

    grid = _ground_segment(cfg)
    for offset, col in enumerate(range(1, 7)):
        top = cfg.height - 3 - offset
        for row in range(top, cfg.height):
            grid[row][col] = Tile.GROUND
    for offset, col in enumerate(range(8, 13)):
        top = cfg.height - 7 + offset
        for row in range(top, cfg.height):
            grid[row][col] = Tile.GROUND
    _add_question(grid, cfg.height - 9, 5)
    _add_question(grid, cfg.height - 7, 9)
    _add_segment(segments, 13, "stair_climb", "dual_slope_reward", 2, grid)

    grid = _ground_segment(cfg)
    for row in range(cfg.height - 7, cfg.height - 2):
        grid[row][4] = Tile.PIPE
        grid[row][5] = Tile.PIPE
        grid[row][9] = Tile.PIPE
        grid[row][10] = Tile.PIPE
    for col in range(2, 12):
        grid[cfg.height - 8][col] = Tile.BRICK
    _add_coin(grid, cfg.height - 9, 7)
    _add_segment(segments, 14, "pipe_pressure", "double_pipe_bridge", 3, grid)

    grid = _ground_segment(cfg)
    for col in range(0, 5):
        for row in range(cfg.height - 4, cfg.height):
            grid[row][col] = Tile.GROUND
    for col in range(5, 9):
        for row in range(cfg.height - 6, cfg.height):
            grid[row][col] = Tile.GROUND
    for col in range(9, 14):
        for row in range(cfg.height - 4, cfg.height):
            grid[row][col] = Tile.GROUND
    _add_enemy(grid, cfg.height - 7, 6)
    _add_segment(segments, 15, "mixed_challenge", "ridge_enemy", 3, grid)

    grid = _ground_segment(cfg)
    for col in range(1, 13):
        grid[cfg.height - 6][col] = Tile.BRICK
    for col in range(3, 11):
        grid[cfg.height - 9][col] = Tile.QUESTION
    for col in range(4, 10, 2):
        _add_coin(grid, cfg.height - 10, col)
    _add_segment(segments, 16, "reward_relief", "question_arc", 1, grid)

    grid = _ground_segment(cfg)
    for col in range(2, 12):
        grid[cfg.height - 5][col] = Tile.BRICK
    for col in range(4, 10):
        grid[cfg.height - 8][col] = Tile.BRICK
    for row in range(cfg.height - 6, cfg.height - 2):
        grid[row][2] = Tile.PIPE
        grid[row][3] = Tile.PIPE
    _add_enemy(grid, cfg.height - 3, 8)
    _add_enemy(grid, cfg.height - 3, 11)
    _add_question(grid, cfg.height - 10, 6)
    _add_segment(segments, 17, "mixed_challenge", "pipe_enemy_stack", 3, grid)

    return segments


def build_segment_spec_library(cfg: MarioConfig) -> Dict[int, SegmentSpec]:
    return _build_segment_spec_library(cfg.height, cfg.segment_width, cfg.num_segments)


def build_segment_library(cfg: MarioConfig) -> Dict[int, LevelGrid]:
    return {segment_id: spec.grid for segment_id, spec in build_segment_spec_library(cfg).items()}


def chromosome_family_sequence(chromosome: List[int], cfg: MarioConfig) -> List[str]:
    library = build_segment_spec_library(cfg)
    return [library[segment_id].family for segment_id in chromosome]


def chromosome_difficulty_tiers(chromosome: List[int], cfg: MarioConfig) -> List[int]:
    library = build_segment_spec_library(cfg)
    return [library[segment_id].difficulty_tier for segment_id in chromosome]


def chromosome_segment_metadata(chromosome: List[int], cfg: MarioConfig) -> List[Dict[str, object]]:
    library = build_segment_spec_library(cfg)
    return [library[segment_id].metadata() for segment_id in chromosome]
