import unittest

from ea_lab.pcg.config import MarioConfig
from ea_lab.pcg.constraints import check_constraints
from ea_lab.pcg.decode import decode_chromosome
from ea_lab.pcg.models import Level, Tile


class ConstraintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = MarioConfig()

    def test_feasible_level_has_no_violations(self) -> None:
        level = decode_chromosome([0] * self.cfg.num_segments, self.cfg)

        constraints = check_constraints(level, self.cfg)

        self.assertTrue(constraints.is_feasible)
        self.assertEqual(constraints.violations, [])
        self.assertEqual(constraints.violation_count, 0)

    def test_unreachable_level_reports_reachable_violation(self) -> None:
        level = decode_chromosome([1] * self.cfg.num_segments, self.cfg)

        constraints = check_constraints(level, self.cfg)

        self.assertFalse(constraints.is_feasible)
        self.assertIn("reachable", constraints.violations)

    def test_enemy_without_support_fails_enemy_rule(self) -> None:
        grid = [[Tile.EMPTY for _ in range(self.cfg.width)] for _ in range(self.cfg.height)]
        for col in range(self.cfg.width):
            grid[self.cfg.height - 2][col] = Tile.GROUND
            grid[self.cfg.height - 1][col] = Tile.GROUND
        grid[self.cfg.height - 3][1] = Tile.START
        grid[self.cfg.height - 3][self.cfg.width - 2] = Tile.GOAL
        grid[self.cfg.height - 5][10] = Tile.ENEMY
        level = Level(grid=grid)

        constraints = check_constraints(level, self.cfg)

        self.assertFalse(constraints.enemy_rules_ok)
        self.assertIn("enemy_rules", constraints.violations)


if __name__ == "__main__":
    unittest.main()
