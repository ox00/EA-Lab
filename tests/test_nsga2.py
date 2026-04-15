import unittest

from ea_lab.pcg.config import MarioConfig
from ea_lab.pcg.ea import select_survivors
from ea_lab.pcg.ea import top_k_feasible_frontier
from ea_lab.pcg.evaluation import evaluate_level
from ea_lab.pcg.decode import decode_chromosome
from ea_lab.pcg.models import ConstraintResult
from ea_lab.pcg.models import EvaluationResult
from ea_lab.pcg.models import Individual


def feasible_individual(chromosome, difficulty_error, structural_diversity, emptiness):
    return Individual(
        chromosome=list(chromosome),
        constraints=ConstraintResult(
            is_feasible=True,
            start_ok=True,
            goal_ok=True,
            reachable=True,
            illegal_overlap=False,
            max_gap_ok=True,
            violations=[],
        ),
        evaluation=EvaluationResult(
            difficulty_score=0.5,
            difficulty_error=difficulty_error,
            structural_diversity=structural_diversity,
            emptiness=emptiness,
            emptiness_error=abs(emptiness - 0.45),
            difficulty_curve_error=0.1,
            family_balance=0.8,
        ),
    )


def infeasible_individual(chromosome, violations):
    return Individual(
        chromosome=list(chromosome),
        constraints=ConstraintResult(
            is_feasible=False,
            start_ok=False,
            goal_ok=False,
            reachable=False,
            illegal_overlap=False,
            max_gap_ok=False,
            violations=list(violations),
        ),
        evaluation=None,
    )


class NsgaLiteTests(unittest.TestCase):
    def test_evaluation_emits_v3_metrics(self) -> None:
        cfg = MarioConfig()
        chromosome = [0, 6, 4, 7, 10, 11, 13, 17]
        level = decode_chromosome(chromosome, cfg)

        result = evaluate_level(level, cfg, chromosome)

        self.assertGreaterEqual(result.family_balance, 0.0)
        self.assertLessEqual(result.family_balance, 1.0)
        self.assertGreaterEqual(result.difficulty_curve_error, 0.0)

    def test_top_k_frontier_returns_only_first_front(self) -> None:
        population = [
            feasible_individual([1], 0.10, 0.50, 0.50),
            feasible_individual([2], 0.20, 0.90, 0.90),
            feasible_individual([3], 0.60, 0.40, 0.40),
        ]

        frontier = top_k_feasible_frontier(population, 5)

        chromosomes = {tuple(individual.chromosome) for individual in frontier}
        self.assertEqual(chromosomes, {(1,), (2,)})

    def test_top_k_frontier_deduplicates_same_chromosome(self) -> None:
        population = [
            feasible_individual([1], 0.10, 0.50, 0.50),
            feasible_individual([1], 0.10, 0.50, 0.50),
            feasible_individual([2], 0.20, 0.90, 0.90),
        ]

        frontier = top_k_feasible_frontier(population, 5)

        self.assertEqual([tuple(ind.chromosome) for ind in frontier], [(1,), (2,)])

    def test_select_survivors_prefers_feasible_front_over_infeasible(self) -> None:
        cfg = MarioConfig(population_size=2)
        population = [
            feasible_individual([1], 0.10, 0.50, 0.50),
            feasible_individual([2], 0.20, 0.90, 0.90),
            infeasible_individual([9], ["reachable", "max_gap"]),
            infeasible_individual([8], ["reachable"]),
        ]

        survivors = select_survivors(population, cfg)

        self.assertTrue(all(individual.feasible for individual in survivors))
        self.assertEqual({tuple(ind.chromosome) for ind in survivors}, {(1,), (2,)})


if __name__ == "__main__":
    unittest.main()
