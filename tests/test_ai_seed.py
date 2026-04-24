import random
import unittest

from ea_lab.pcg.ai_seed import adapt_ai_chromosome
from ea_lab.pcg.ai_seed import repair_ai_chromosome
from ea_lab.pcg.ai_seed import seeded_chromosome
from ea_lab.pcg.config import MarioConfig
from ea_lab.pcg.ea import initial_population_chromosomes
from ea_lab.pcg.segments import build_segment_library


class AiSeedTests(unittest.TestCase):
    def test_adapt_ai_chromosome_trims_to_fixed_length(self) -> None:
        cfg = MarioConfig(num_segments=8)
        rng = random.Random(7)

        adapted = adapt_ai_chromosome([1, 1, 1, 3, 2, 15, 1, 1, 3, 2], cfg, rng)

        self.assertEqual(len(adapted), cfg.num_segments)

    def test_adapt_ai_chromosome_pads_short_sequence(self) -> None:
        cfg = MarioConfig(num_segments=8)
        rng = random.Random(7)

        adapted = adapt_ai_chromosome([1, 3], cfg, rng)

        self.assertEqual(len(adapted), cfg.num_segments)
        self.assertTrue(all(segment_id in {1, 3} for segment_id in adapted))

    def test_seeded_chromosome_uses_valid_segment_ids(self) -> None:
        cfg = MarioConfig(num_segments=8)
        rng = random.Random(7)
        valid_ids = set(build_segment_library(cfg).keys())

        chromosome = seeded_chromosome(cfg, rng)

        self.assertEqual(len(chromosome), cfg.num_segments)
        self.assertTrue(all(segment_id in valid_ids for segment_id in chromosome))

    def test_repair_ai_chromosome_preserves_valid_domain(self) -> None:
        cfg = MarioConfig(num_segments=8, ai_seed_repair=True)
        rng = random.Random(7)
        valid_ids = set(build_segment_library(cfg).keys())

        repaired = repair_ai_chromosome([1, 1, 1, 1, 1, 1, 1, 1], cfg, rng)

        self.assertEqual(len(repaired), cfg.num_segments)
        self.assertTrue(all(segment_id in valid_ids for segment_id in repaired))

    def test_initial_population_ai_seeded_mode_mixes_population(self) -> None:
        cfg = MarioConfig(population_size=10, num_segments=8, init_mode="ai_seeded", ai_seed_ratio=0.6)
        rng = random.Random(7)

        chromosomes = initial_population_chromosomes(cfg, rng)

        self.assertEqual(len(chromosomes), cfg.population_size)
        self.assertTrue(all(len(chromosome) == cfg.num_segments for chromosome in chromosomes))


if __name__ == "__main__":
    unittest.main()
