from __future__ import annotations

import random
from dataclasses import asdict
from dataclasses import dataclass
from typing import Iterable, List

from .config import MarioConfig
from .constraints import check_constraints
from .decode import decode_chromosome
from .evaluation import evaluate_level
from .models import Chromosome, Individual
from .segments import build_segment_library


def random_chromosome(cfg: MarioConfig, rng: random.Random) -> Chromosome:
    segment_ids = list(build_segment_library(cfg).keys())
    return [rng.choice(segment_ids) for _ in range(cfg.num_segments)]


def evaluate_chromosome(chromosome: Chromosome, cfg: MarioConfig) -> Individual:
    level = decode_chromosome(chromosome, cfg)
    constraints = check_constraints(level, cfg)
    evaluation = evaluate_level(level, cfg) if constraints.is_feasible else None
    return Individual(chromosome=chromosome, constraints=constraints, evaluation=evaluation)


def mutate(chromosome: Chromosome, cfg: MarioConfig, rng: random.Random) -> Chromosome:
    child = chromosome[:]
    if rng.random() < cfg.mutation_rate:
        idx = rng.randrange(len(child))
        segment_ids = list(build_segment_library(cfg).keys())
        child[idx] = rng.choice(segment_ids)
    return child


def crossover(parent_a: Chromosome, parent_b: Chromosome, cfg: MarioConfig, rng: random.Random) -> Chromosome:
    if rng.random() > cfg.crossover_rate:
        return parent_a[:]
    point = rng.randrange(1, len(parent_a))
    return parent_a[:point] + parent_b[point:]


def feasible_first_key(individual: Individual) -> tuple[float, float, float, float]:
    if not individual.feasible:
        penalties = sum(
            0 if value else 1
            for key, value in individual.constraints.as_dict().items()
            if key != "is_feasible"
        )
        return (1.0, penalties, float("inf"), float("inf"))

    assert individual.evaluation is not None
    return (
        0.0,
        0.0,
        individual.evaluation.difficulty_error,
        individual.evaluation.emptiness_error - individual.evaluation.structural_diversity,
    )


def select_survivors(population: Iterable[Individual], cfg: MarioConfig) -> List[Individual]:
    return sorted(population, key=feasible_first_key)[: cfg.population_size]


@dataclass
class GenerationLog:
    generation: int
    feasible_ratio: float
    best_difficulty_error: float | None
    best_structural_diversity: float | None
    best_emptiness_error: float | None
    best_emptiness: float | None


def run_minimal_ea(cfg: MarioConfig) -> tuple[List[Individual], List[GenerationLog]]:
    rng = random.Random(cfg.seed)
    population = [evaluate_chromosome(random_chromosome(cfg, rng), cfg) for _ in range(cfg.population_size)]
    logs: List[GenerationLog] = []

    for generation in range(cfg.generations):
        feasible = [ind for ind in population if ind.feasible]
        feasible_ratio = len(feasible) / len(population)
        best_eval = min(feasible, key=lambda ind: ind.evaluation.difficulty_error).evaluation if feasible else None
        logs.append(
            GenerationLog(
                generation=generation,
                feasible_ratio=feasible_ratio,
                best_difficulty_error=best_eval.difficulty_error if best_eval else None,
                best_structural_diversity=best_eval.structural_diversity if best_eval else None,
                best_emptiness_error=best_eval.emptiness_error if best_eval else None,
                best_emptiness=best_eval.emptiness if best_eval else None,
            )
        )

        offspring: List[Individual] = []
        while len(offspring) < cfg.population_size:
            parent_a = rng.choice(population).chromosome
            parent_b = rng.choice(population).chromosome
            child = crossover(parent_a, parent_b, cfg, rng)
            child = mutate(child, cfg, rng)
            offspring.append(evaluate_chromosome(child, cfg))

        population = select_survivors(list(population) + offspring, cfg)

    return population, logs


def logs_as_dicts(logs: Iterable[GenerationLog]) -> list[dict[str, float | int | None]]:
    return [asdict(log) for log in logs]
