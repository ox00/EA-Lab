from __future__ import annotations

import math
import random
from dataclasses import asdict
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from .config import MarioConfig
from .ea import crossover
from .ea import evaluate_chromosome
from .ea import get_objective_specs
from .ea import mutate
from .ea import random_chromosome
from .models import Individual


def _constraint_violations(individual: Individual) -> int:
    return sum(
        0 if ok else 1
        for key, ok in individual.constraints.as_dict().items()
        if key != "is_feasible"
    )


def _objective_vector(individual: Individual, objective_specs: Sequence[Tuple[str, bool]]) -> tuple[float, ...]:
    assert individual.evaluation is not None
    values = []
    for objective_name, minimize in objective_specs:
        value = getattr(individual.evaluation, objective_name)
        values.append(value if minimize else -value)
    return tuple(values)


def _metric_point(individual: Individual, cfg: MarioConfig) -> tuple[float, float, float]:
    assert individual.evaluation is not None
    if cfg.nsga2_objective_mode == "family_4obj":
        return (
            individual.evaluation.difficulty_error,
            individual.evaluation.emptiness_error,
            1.0 - individual.evaluation.family_balance,
        )
    return (
        individual.evaluation.difficulty_error,
        1.0 - individual.evaluation.structural_diversity,
        individual.evaluation.emptiness_error,
    )


def _clip_point(point: tuple[float, float, float], ref: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(min(max(value, 0.0), ref[idx]) for idx, value in enumerate(point))  # type: ignore[return-value]


def _hypervolume_2d(points: list[tuple[float, float]], ref: tuple[float, float]) -> float:
    if not points:
        return 0.0

    sorted_points = sorted(points, key=lambda value: value[0])
    area = 0.0
    best_z = ref[1]
    previous_y = ref[0]

    for y, z in reversed(sorted_points):
        width = previous_y - y
        best_z = min(best_z, z)
        if width > 0:
            area += width * max(0.0, ref[1] - best_z)
        previous_y = y

    return area


def hypervolume_3d(points: list[tuple[float, float, float]], ref: tuple[float, float, float] = (1.0, 1.0, 1.0)) -> float:
    if not points:
        return 0.0

    clipped_points = [_clip_point(point, ref) for point in points]
    sorted_points = sorted(clipped_points, key=lambda value: value[0])
    volume = 0.0
    active: list[tuple[float, float]] = []

    for idx, point in enumerate(sorted_points):
        x_value = point[0]
        next_x = sorted_points[idx + 1][0] if idx + 1 < len(sorted_points) else ref[0]
        active.append((point[1], point[2]))
        width = next_x - x_value
        if width > 0:
            volume += width * _hypervolume_2d(active, (ref[1], ref[2]))

    return volume


def front_spread(points: list[tuple[float, float, float]]) -> float:
    if len(points) <= 1:
        return 0.0

    dimensions = len(points[0])
    centroid = tuple(sum(point[idx] for point in points) / len(points) for idx in range(dimensions))
    distances = []
    for point in points:
        squared = sum((point[idx] - centroid[idx]) ** 2 for idx in range(dimensions))
        distances.append(math.sqrt(squared))
    return sum(distances) / len(distances)


def dominates(a: Individual, b: Individual, cfg: MarioConfig) -> bool:
    if a.feasible and not b.feasible:
        return True
    if not a.feasible and b.feasible:
        return False

    if not a.feasible and not b.feasible:
        av = _constraint_violations(a)
        bv = _constraint_violations(b)
        return av < bv

    objective_specs = get_objective_specs(cfg)
    av = _objective_vector(a, objective_specs)
    bv = _objective_vector(b, objective_specs)
    not_worse_all = all(x <= y for x, y in zip(av, bv))
    better_any = any(x < y for x, y in zip(av, bv))
    return not_worse_all and better_any


def fast_non_dominated_sort(population: List[Individual], cfg: MarioConfig) -> tuple[List[List[int]], List[int]]:
    size = len(population)
    dominated_sets: list[set[int]] = [set() for _ in range(size)]
    domination_counts = [0 for _ in range(size)]
    ranks = [0 for _ in range(size)]
    fronts: List[List[int]] = [[]]

    for p in range(size):
        for q in range(size):
            if p == q:
                continue
            if dominates(population[p], population[q], cfg):
                dominated_sets[p].add(q)
            elif dominates(population[q], population[p], cfg):
                domination_counts[p] += 1
        if domination_counts[p] == 0:
            ranks[p] = 0
            fronts[0].append(p)

    i = 0
    while i < len(fronts) and fronts[i]:
        next_front: List[int] = []
        for p in fronts[i]:
            for q in dominated_sets[p]:
                domination_counts[q] -= 1
                if domination_counts[q] == 0:
                    ranks[q] = i + 1
                    next_front.append(q)
        if next_front:
            fronts.append(next_front)
        i += 1

    return fronts, ranks


def crowding_distance(population: List[Individual], front: List[int], cfg: MarioConfig) -> dict[int, float]:
    if not front:
        return {}
    if len(front) <= 2:
        return {idx: float("inf") for idx in front}

    distances = {idx: 0.0 for idx in front}
    objective_specs = get_objective_specs(cfg)

    for objective_name, minimize in objective_specs:
        key_fn = lambda i: getattr(population[i].evaluation, objective_name) if population[i].evaluation else float("inf")
        sorted_front = sorted(front, key=key_fn, reverse=not minimize)
        distances[sorted_front[0]] = float("inf")
        distances[sorted_front[-1]] = float("inf")

        min_value = key_fn(sorted_front[0])
        max_value = key_fn(sorted_front[-1])
        if max_value == min_value:
            continue

        for pos in range(1, len(sorted_front) - 1):
            prev_value = key_fn(sorted_front[pos - 1])
            next_value = key_fn(sorted_front[pos + 1])
            distances[sorted_front[pos]] += (next_value - prev_value) / (max_value - min_value)

    return distances


def _tournament_select(
    population: List[Individual],
    ranks: List[int],
    distances: dict[int, float],
    rng: random.Random,
) -> Individual:
    a = rng.randrange(len(population))
    b = rng.randrange(len(population))

    if ranks[a] < ranks[b]:
        return population[a]
    if ranks[b] < ranks[a]:
        return population[b]

    da = distances.get(a, 0.0)
    db = distances.get(b, 0.0)
    if da > db:
        return population[a]
    if db > da:
        return population[b]
    return population[a] if rng.random() < 0.5 else population[b]


def _build_rank_and_distance(population: List[Individual], cfg: MarioConfig) -> tuple[List[int], dict[int, float], List[List[int]]]:
    fronts, ranks = fast_non_dominated_sort(population, cfg)
    distances: dict[int, float] = {}
    for front in fronts:
        distances.update(crowding_distance(population, front, cfg))
    return ranks, distances, fronts


def _environmental_selection(combined: List[Individual], population_size: int, cfg: MarioConfig) -> List[Individual]:
    fronts, _ = fast_non_dominated_sort(combined, cfg)
    next_population: List[Individual] = []

    for front in fronts:
        if len(next_population) + len(front) <= population_size:
            next_population.extend(combined[idx] for idx in front)
            continue

        distances = crowding_distance(combined, front, cfg)
        sorted_front = sorted(front, key=lambda idx: distances[idx], reverse=True)
        remaining = population_size - len(next_population)
        next_population.extend(combined[idx] for idx in sorted_front[:remaining])
        break

    return next_population


@dataclass
class Nsga2GenerationLog:
    generation: int
    feasible_ratio: float
    first_front_size: int
    first_front_hv: float
    first_front_spread: float
    best_difficulty_error: float | None
    best_structural_diversity: float | None
    best_emptiness_error: float | None
    best_emptiness: float | None
    best_difficulty_curve_error: float | None
    best_family_balance: float | None


def run_nsga2(cfg: MarioConfig) -> tuple[List[Individual], List[Nsga2GenerationLog]]:
    rng = random.Random(cfg.seed)
    population = [evaluate_chromosome(random_chromosome(cfg, rng), cfg) for _ in range(cfg.population_size)]
    logs: List[Nsga2GenerationLog] = []

    for generation in range(cfg.generations):
        ranks, distances, fronts = _build_rank_and_distance(population, cfg)
        feasible = [ind for ind in population if ind.feasible]
        best_eval = min(feasible, key=lambda ind: ind.evaluation.difficulty_error).evaluation if feasible else None
        first_front = [population[idx] for idx in fronts[0]] if fronts else []
        feasible_first_front = [individual for individual in first_front if individual.feasible]
        front_points = [_metric_point(individual, cfg) for individual in feasible_first_front]
        first_front_size = len(feasible_first_front)
        logs.append(
            Nsga2GenerationLog(
                generation=generation,
                feasible_ratio=len(feasible) / len(population),
                first_front_size=first_front_size,
                first_front_hv=hypervolume_3d(front_points),
                first_front_spread=front_spread(front_points),
                best_difficulty_error=best_eval.difficulty_error if best_eval else None,
                best_structural_diversity=best_eval.structural_diversity if best_eval else None,
                best_emptiness_error=best_eval.emptiness_error if best_eval else None,
                best_emptiness=best_eval.emptiness if best_eval else None,
                best_difficulty_curve_error=best_eval.difficulty_curve_error if best_eval else None,
                best_family_balance=best_eval.family_balance if best_eval else None,
            )
        )

        offspring: List[Individual] = []
        while len(offspring) < cfg.population_size:
            parent_a = _tournament_select(population, ranks, distances, rng).chromosome
            parent_b = _tournament_select(population, ranks, distances, rng).chromosome
            child = crossover(parent_a, parent_b, cfg, rng)
            child = mutate(child, cfg, rng)
            offspring.append(evaluate_chromosome(child, cfg))

        population = _environmental_selection(population + offspring, cfg.population_size, cfg)

    return population, logs


def logs_as_dicts(logs: Iterable[Nsga2GenerationLog]) -> list[dict[str, float | int | None]]:
    return [asdict(log) for log in logs]
