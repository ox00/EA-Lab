from __future__ import annotations

from collections import deque
from typing import List, Optional, Tuple

from .config import MarioConfig
from .models import ConstraintResult, Level, Tile


def _is_solid(tile: int) -> bool:
    return tile in {Tile.GROUND, Tile.BRICK, Tile.QUESTION, Tile.PIPE}


def _find_tile(level: Level, target: int) -> Optional[Tuple[int, int]]:
    for row, row_values in enumerate(level.grid):
        for col, value in enumerate(row_values):
            if value == target:
                return row, col
    return None


def _standable(level: Level, row: int, col: int) -> bool:
    if row < 0 or row >= len(level.grid) - 1:
        return False
    if col < 0 or col >= len(level.grid[0]):
        return False
    return level.grid[row][col] in {Tile.EMPTY, Tile.START, Tile.GOAL, Tile.COIN} and _is_solid(
        level.grid[row + 1][col]
    )


def _max_ground_gap(level: Level) -> int:
    row = len(level.grid) - 2
    max_gap = 0
    current_gap = 0
    for col in range(len(level.grid[0])):
        if _is_solid(level.grid[row][col]):
            max_gap = max(max_gap, current_gap)
            current_gap = 0
        else:
            current_gap += 1
    return max(max_gap, current_gap)


def _enemy_rules_ok(level: Level) -> bool:
    height = len(level.grid)
    width = len(level.grid[0])

    for row in range(height):
        for col in range(width):
            if level.grid[row][col] != Tile.ENEMY:
                continue
            if row + 1 >= height or not _is_solid(level.grid[row + 1][col]):
                return False
    return True


def _pipe_rules_ok(level: Level) -> bool:
    height = len(level.grid)
    width = len(level.grid[0])

    for row in range(height):
        for col in range(width):
            if level.grid[row][col] != Tile.PIPE:
                continue

            has_left = col - 1 >= 0 and level.grid[row][col - 1] == Tile.PIPE
            has_right = col + 1 < width and level.grid[row][col + 1] == Tile.PIPE
            if has_left == has_right:
                return False

            below = level.grid[row + 1][col] if row + 1 < height else None
            if below is not None and below not in {Tile.PIPE, Tile.GROUND, Tile.BRICK, Tile.QUESTION}:
                return False

    return True


def _placement_rules_ok(level: Level) -> bool:
    height = len(level.grid)
    width = len(level.grid[0])

    for row in range(height):
        for col in range(width):
            tile = level.grid[row][col]
            if tile in {Tile.QUESTION, Tile.BRICK} and row >= height - 2:
                return False
            if tile == Tile.COIN and row == height - 1:
                return False
    return True


def _reachable(level: Level, start: Tuple[int, int], goal: Tuple[int, int], cfg: MarioConfig) -> bool:
    queue = deque([start])
    visited = {start}

    while queue:
        row, col = queue.popleft()
        if (row, col) == goal:
            return True

        for step in (-1, 1):
            ncol = col + step
            if _standable(level, row, ncol) and (row, ncol) not in visited:
                visited.add((row, ncol))
                queue.append((row, ncol))

        for jump in range(1, cfg.max_jumpable_gap + 1):
            for direction in (-1, 1):
                ncol = col + direction * jump
                if _standable(level, row, ncol) and (row, ncol) not in visited:
                    visited.add((row, ncol))
                    queue.append((row, ncol))

    return False


def check_constraints(level: Level, cfg: MarioConfig) -> ConstraintResult:
    start = _find_tile(level, Tile.START)
    goal = _find_tile(level, Tile.GOAL)

    start_ok = start is not None and _standable(level, start[0], start[1])
    goal_ok = goal is not None and _standable(level, goal[0], goal[1])
    illegal_overlap = False
    max_gap_ok = _max_ground_gap(level) <= cfg.max_jumpable_gap
    reachable = bool(start_ok and goal_ok and _reachable(level, start, goal, cfg))
    enemy_rules_ok = _enemy_rules_ok(level)
    pipe_rules_ok = _pipe_rules_ok(level)
    placement_rules_ok = _placement_rules_ok(level)

    violations: List[str] = []
    if not start_ok:
        violations.append("start")
    if not goal_ok:
        violations.append("goal")
    if not reachable:
        violations.append("reachable")
    if illegal_overlap:
        violations.append("illegal_overlap")
    if not max_gap_ok:
        violations.append("max_gap")
    if not enemy_rules_ok:
        violations.append("enemy_rules")
    if not pipe_rules_ok:
        violations.append("pipe_rules")
    if not placement_rules_ok:
        violations.append("placement_rules")

    return ConstraintResult(
        is_feasible=all(
            [
                start_ok,
                goal_ok,
                reachable,
                not illegal_overlap,
                max_gap_ok,
                enemy_rules_ok,
                pipe_rules_ok,
                placement_rules_ok,
            ]
        ),
        start_ok=start_ok,
        goal_ok=goal_ok,
        reachable=reachable,
        illegal_overlap=illegal_overlap,
        max_gap_ok=max_gap_ok,
        enemy_rules_ok=enemy_rules_ok,
        pipe_rules_ok=pipe_rules_ok,
        placement_rules_ok=placement_rules_ok,
        violations=violations,
    )
