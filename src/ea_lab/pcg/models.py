from dataclasses import dataclass
from typing import Dict, List

LevelGrid = List[List[int]]
Chromosome = List[int]


class Tile:
    EMPTY = 0
    GROUND = 1
    BRICK = 2
    QUESTION = 3
    COIN = 4
    ENEMY = 5
    PIPE = 6
    START = 7
    GOAL = 8


@dataclass
class Level:
    grid: LevelGrid


@dataclass
class EvaluationResult:
    difficulty_score: float
    difficulty_error: float
    structural_diversity: float
    emptiness: float
    emptiness_error: float

    def as_objectives(self) -> Dict[str, float]:
        return {
            "difficulty_error": self.difficulty_error,
            "structural_diversity": self.structural_diversity,
            "emptiness_error": self.emptiness_error,
            "emptiness": self.emptiness,
        }


@dataclass
class ConstraintResult:
    is_feasible: bool
    start_ok: bool
    goal_ok: bool
    reachable: bool
    illegal_overlap: bool
    max_gap_ok: bool

    def as_dict(self) -> Dict[str, bool]:
        return {
            "is_feasible": self.is_feasible,
            "start_ok": self.start_ok,
            "goal_ok": self.goal_ok,
            "reachable": self.reachable,
            "illegal_overlap": self.illegal_overlap,
            "max_gap_ok": self.max_gap_ok,
        }


@dataclass
class Individual:
    chromosome: Chromosome
    constraints: ConstraintResult
    evaluation: EvaluationResult | None

    @property
    def feasible(self) -> bool:
        return self.constraints.is_feasible
