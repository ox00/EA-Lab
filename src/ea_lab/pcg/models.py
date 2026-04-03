from dataclasses import dataclass
from dataclasses import field
from typing import Dict, List, Optional

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

    def as_objectives(self) -> Dict[str, float]:
        return {
            "difficulty_error": self.difficulty_error,
            "structural_diversity": self.structural_diversity,
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
    enemy_rules_ok: bool = True
    pipe_rules_ok: bool = True
    placement_rules_ok: bool = True
    violations: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, bool]:
        return {
            "is_feasible": self.is_feasible,
            "start_ok": self.start_ok,
            "goal_ok": self.goal_ok,
            "reachable": self.reachable,
            "illegal_overlap": self.illegal_overlap,
            "max_gap_ok": self.max_gap_ok,
        }

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    def as_log_dict(self) -> Dict[str, object]:
        data: Dict[str, object] = self.as_dict()
        data.update(
            {
                "enemy_rules_ok": self.enemy_rules_ok,
                "pipe_rules_ok": self.pipe_rules_ok,
                "placement_rules_ok": self.placement_rules_ok,
                "violation_count": self.violation_count,
                "violations": list(self.violations),
            }
        )
        return data


@dataclass
class Individual:
    chromosome: Chromosome
    constraints: ConstraintResult
    evaluation: Optional[EvaluationResult]

    @property
    def feasible(self) -> bool:
        return self.constraints.is_feasible
