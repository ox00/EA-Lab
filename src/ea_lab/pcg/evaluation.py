from __future__ import annotations

from .config import MarioConfig
from .models import EvaluationResult, Level, Tile


def _count_tiles(level: Level, tile: int) -> int:
    return sum(1 for row in level.grid for value in row if value == tile)


def _ground_profile(level: Level) -> list[int]:
    profile = []
    height = len(level.grid)
    width = len(level.grid[0])
    for col in range(width):
        ground_y = height - 1
        while ground_y >= 0 and level.grid[ground_y][col] == Tile.EMPTY:
            ground_y -= 1
        profile.append(ground_y)
    return profile


def _row_diversity(level: Level) -> float:
    rows = ["".join(map(str, row)) for row in level.grid]
    return len(set(rows)) / max(1, len(rows))


def _normalized_gap_risk(level: Level, cfg: MarioConfig) -> float:
    ground_row = cfg.height - 2
    width = len(level.grid[0])
    max_gap = 0
    current_gap = 0
    for col in range(width):
        if level.grid[ground_row][col] == Tile.EMPTY:
            current_gap += 1
            max_gap = max(max_gap, current_gap)
        else:
            current_gap = 0
    return min(1.0, max_gap / max(1, cfg.max_jumpable_gap + 1))


def evaluate_level(level: Level, cfg: MarioConfig) -> EvaluationResult:
    total_tiles = cfg.height * cfg.width
    empty_tiles = _count_tiles(level, Tile.EMPTY)
    enemy_tiles = _count_tiles(level, Tile.ENEMY)

    emptiness = empty_tiles / total_tiles
    enemy_density = enemy_tiles / max(1, cfg.width)

    profile = _ground_profile(level)
    height_variation = sum(abs(profile[i] - profile[i - 1]) for i in range(1, len(profile)))
    normalized_height_variation = min(1.0, height_variation / max(1, cfg.width))

    gap_risk = _normalized_gap_risk(level, cfg)
    jump_count = sum(1 for i in range(1, len(profile)) if profile[i] != profile[i - 1])
    normalized_jump_count = min(1.0, jump_count / max(1, cfg.width / 2))

    difficulty_score = (
        0.35 * min(1.0, enemy_density * 4)
        + 0.30 * gap_risk
        + 0.20 * normalized_height_variation
        + 0.15 * normalized_jump_count
    )
    difficulty_error = abs(difficulty_score - cfg.target_difficulty)
    structural_diversity = 0.6 * _row_diversity(level) + 0.4 * (1.0 - abs(emptiness - 0.45))

    return EvaluationResult(
        difficulty_score=difficulty_score,
        difficulty_error=difficulty_error,
        structural_diversity=structural_diversity,
        emptiness=emptiness,
    )
