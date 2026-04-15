from __future__ import annotations

from collections import Counter
from typing import List

from .config import MarioConfig
from .models import EvaluationResult, Level, Tile
from .segments import chromosome_difficulty_tiers
from .segments import chromosome_family_sequence


def _count_tiles(level: Level, tile: int) -> int:
    return sum(1 for row in level.grid for value in row if value == tile)


def _ground_profile(level: Level) -> List[int]:
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


def _difficulty_curve_error(chromosome: List[int], cfg: MarioConfig) -> float:
    tiers = chromosome_difficulty_tiers(chromosome, cfg)
    if len(tiers) <= 1:
        return 0.0

    target_curve = [1.0 + 2.0 * idx / (len(tiers) - 1) for idx in range(len(tiers))]
    return sum(abs(float(tier) - target) for tier, target in zip(tiers, target_curve)) / len(tiers)


def _family_balance(chromosome: List[int], cfg: MarioConfig) -> float:
    families = chromosome_family_sequence(chromosome, cfg)
    if not families:
        return 0.0

    counts = Counter(families)
    expected = len(families) / max(1, len(counts))
    deviation = sum(abs(count - expected) for count in counts.values()) / len(families)
    balance = max(0.0, 1.0 - deviation)
    adjacency_penalty = sum(1 for idx in range(1, len(families)) if families[idx] == families[idx - 1]) / max(
        1,
        len(families) - 1,
    )
    return max(0.0, balance * (1.0 - 0.35 * adjacency_penalty))


def evaluate_level(level: Level, cfg: MarioConfig, chromosome: List[int]) -> EvaluationResult:
    total_tiles = cfg.height * cfg.width
    empty_tiles = _count_tiles(level, Tile.EMPTY)
    enemy_tiles = _count_tiles(level, Tile.ENEMY)

    emptiness = empty_tiles / total_tiles
    emptiness_error = abs(emptiness - cfg.target_emptiness)
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
    structural_diversity = _row_diversity(level)
    difficulty_curve_error = _difficulty_curve_error(chromosome, cfg)
    family_balance = _family_balance(chromosome, cfg)

    return EvaluationResult(
        difficulty_score=difficulty_score,
        difficulty_error=difficulty_error,
        structural_diversity=structural_diversity,
        emptiness=emptiness,
        emptiness_error=emptiness_error,
        difficulty_curve_error=difficulty_curve_error,
        family_balance=family_balance,
    )
