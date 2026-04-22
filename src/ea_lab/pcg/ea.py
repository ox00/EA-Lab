from __future__ import annotations

import random
from dataclasses import asdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

from .config import MarioConfig
from .constraints import check_constraints
from .decode import decode_chromosome
from .evaluation import evaluate_level
from .models import Chromosome, Individual
from .segments import build_segment_library
from .segments import chromosome_segment_metadata


def random_chromosome(cfg: MarioConfig, rng: random.Random) -> Chromosome:
    segment_ids = list(build_segment_library(cfg).keys())
    return [rng.choice(segment_ids) for _ in range(cfg.num_segments)]


def evaluate_chromosome(chromosome: Chromosome, cfg: MarioConfig) -> Individual:
    level = decode_chromosome(chromosome, cfg)
    constraints = check_constraints(level, cfg)
    evaluation = evaluate_level(level, cfg, chromosome) if constraints.is_feasible else None
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


OBJECTIVE_SPECS: Sequence[Tuple[str, bool]] = (
    ("difficulty_error", True),
    ("structural_diversity", False),
    ("emptiness_error", True),
)


def get_objective_specs(cfg: MarioConfig) -> Sequence[Tuple[str, bool]]:
    if cfg.nsga2_objective_mode == "family_4obj":
        return (
            ("difficulty_error", True),
            ("structural_diversity", False),
            ("emptiness_error", True),
            ("family_balance", False),
        )
    return OBJECTIVE_SPECS


def _constraint_violation_counts(population: Iterable[Individual]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for individual in population:
        for violation in individual.constraints.violations:
            counts[violation] = counts.get(violation, 0) + 1
    return dict(sorted(counts.items()))


def _dominates(individual_a: Individual, individual_b: Individual) -> bool:
    return _dominates_with_specs(individual_a, individual_b, OBJECTIVE_SPECS)


def _dominates_with_specs(
    individual_a: Individual,
    individual_b: Individual,
    objective_specs: Sequence[Tuple[str, bool]],
) -> bool:
    assert individual_a.evaluation is not None
    assert individual_b.evaluation is not None

    better_or_equal = True
    strictly_better = False
    for objective_name, minimize in objective_specs:
        value_a = getattr(individual_a.evaluation, objective_name)
        value_b = getattr(individual_b.evaluation, objective_name)
        if minimize:
            if value_a > value_b:
                better_or_equal = False
                break
            if value_a < value_b:
                strictly_better = True
        else:
            if value_a < value_b:
                better_or_equal = False
                break
            if value_a > value_b:
                strictly_better = True
    return better_or_equal and strictly_better


def _fast_non_dominated_sort(population: Sequence[Individual], objective_specs: Sequence[Tuple[str, bool]]) -> List[List[int]]:
    if not population:
        return []

    domination_counts = [0] * len(population)
    dominates = [[] for _ in population]
    fronts: List[List[int]] = [[]]

    for index_a, individual_a in enumerate(population):
        for index_b, individual_b in enumerate(population):
            if index_a == index_b:
                continue
            if _dominates_with_specs(individual_a, individual_b, objective_specs):
                dominates[index_a].append(index_b)
            elif _dominates_with_specs(individual_b, individual_a, objective_specs):
                domination_counts[index_a] += 1

        if domination_counts[index_a] == 0:
            fronts[0].append(index_a)

    front_index = 0
    while front_index < len(fronts) and fronts[front_index]:
        next_front: List[int] = []
        for index_a in fronts[front_index]:
            for index_b in dominates[index_a]:
                domination_counts[index_b] -= 1
                if domination_counts[index_b] == 0:
                    next_front.append(index_b)
        if next_front:
            fronts.append(next_front)
        front_index += 1

    return fronts


def _crowding_distance(
    population: Sequence[Individual],
    front: Sequence[int],
    objective_specs: Sequence[Tuple[str, bool]],
) -> Dict[int, float]:
    if not front:
        return {}
    if len(front) <= 2:
        return {index: float("inf") for index in front}

    distances = {index: 0.0 for index in front}
    for objective_name, minimize in objective_specs:
        ordered = sorted(
            front,
            key=lambda idx: getattr(population[idx].evaluation, objective_name),
            reverse=not minimize,
        )
        first_index = ordered[0]
        last_index = ordered[-1]
        distances[first_index] = float("inf")
        distances[last_index] = float("inf")

        minimum = getattr(population[first_index].evaluation, objective_name)
        maximum = getattr(population[last_index].evaluation, objective_name)
        if maximum == minimum:
            continue

        for position in range(1, len(ordered) - 1):
            current_index = ordered[position]
            if distances[current_index] == float("inf"):
                continue
            previous_value = getattr(population[ordered[position - 1]].evaluation, objective_name)
            next_value = getattr(population[ordered[position + 1]].evaluation, objective_name)
            distances[current_index] += (next_value - previous_value) / (maximum - minimum)

    return distances


def _rank_feasible_population(population: Sequence[Individual], cfg: MarioConfig) -> Tuple[List[Individual], int]:
    objective_specs = get_objective_specs(cfg)
    fronts = _fast_non_dominated_sort(population, objective_specs)
    ordered: List[Individual] = []
    first_front_size = len(fronts[0]) if fronts else 0

    for front in fronts:
        distances = _crowding_distance(population, front, objective_specs)
        ordered.extend(population[index] for index in sorted(front, key=lambda idx: distances[idx], reverse=True))

    return ordered, first_front_size


def top_k_feasible_frontier(population: Sequence[Individual], top_k: int, cfg: MarioConfig) -> List[Individual]:
    feasible = [individual for individual in population if individual.feasible]
    if not feasible or top_k <= 0:
        return []

    objective_specs = get_objective_specs(cfg)
    fronts = _fast_non_dominated_sort(feasible, objective_specs)
    if not fronts:
        return []

    first_front = fronts[0]
    distances = _crowding_distance(feasible, first_front, objective_specs)
    ordered_indices = sorted(first_front, key=lambda idx: distances[idx], reverse=True)
    unique_frontier: List[Individual] = []
    seen = set()
    for index in ordered_indices:
        chromosome_key = tuple(feasible[index].chromosome)
        if chromosome_key in seen:
            continue
        seen.add(chromosome_key)
        unique_frontier.append(feasible[index])
        if len(unique_frontier) >= top_k:
            break
    return unique_frontier


def infeasible_key(individual: Individual) -> Tuple[int, int, int]:
    penalty_flags = individual.constraints.as_dict()
    unmet_required = sum(0 if value else 1 for key, value in penalty_flags.items() if key != "is_feasible")
    return (
        individual.constraints.violation_count,
        unmet_required,
        sum(individual.chromosome),
    )


def select_survivors(population: Iterable[Individual], cfg: MarioConfig) -> List[Individual]:
    candidates = list(population)
    feasible = [individual for individual in candidates if individual.feasible]
    infeasible = [individual for individual in candidates if not individual.feasible]

    survivors: List[Individual] = []
    if feasible:
        objective_specs = get_objective_specs(cfg)
        fronts = _fast_non_dominated_sort(feasible, objective_specs)
        for front in fronts:
            if len(survivors) + len(front) <= cfg.population_size:
                ordered_front, _ = _rank_feasible_population([feasible[index] for index in front], cfg)
                survivors.extend(ordered_front)
                continue

            distances = _crowding_distance(feasible, front, objective_specs)
            survivors.extend(
                feasible[index]
                for index in sorted(front, key=lambda idx: distances[idx], reverse=True)[
                    : cfg.population_size - len(survivors)
                ]
            )
            break

    if len(survivors) < cfg.population_size:
        survivors.extend(sorted(infeasible, key=infeasible_key)[: cfg.population_size - len(survivors)])

    return survivors


@dataclass
class GenerationLog:
    generation: int
    feasible_ratio: float
    feasible_count: int
    best_front_size: int
    best_difficulty_error: Optional[float]
    best_structural_diversity: Optional[float]
    best_emptiness_error: Optional[float]
    best_emptiness: Optional[float]
    best_difficulty_curve_error: Optional[float]
    best_family_balance: Optional[float]
    constraint_violation_counts: Dict[str, int]


def _best_feasible_individual(population: Sequence[Individual], cfg: MarioConfig) -> Tuple[Optional[Individual], int]:
    feasible = [individual for individual in population if individual.feasible]
    if not feasible:
        return None, 0

    ordered, first_front_size = _rank_feasible_population(feasible, cfg)
    return ordered[0], first_front_size


def _metric_extrema(
    population: Sequence[Individual],
) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    feasible_evaluations = [individual.evaluation for individual in population if individual.evaluation is not None]
    if not feasible_evaluations:
        return None, None, None, None, None, None

    return (
        min(evaluation.difficulty_error for evaluation in feasible_evaluations),
        max(evaluation.structural_diversity for evaluation in feasible_evaluations),
        min(evaluation.emptiness_error for evaluation in feasible_evaluations),
        min(feasible_evaluations, key=lambda evaluation: evaluation.emptiness_error).emptiness,
        min(evaluation.difficulty_curve_error for evaluation in feasible_evaluations),
        max(evaluation.family_balance for evaluation in feasible_evaluations),
    )


def run_minimal_ea(cfg: MarioConfig) -> Tuple[List[Individual], List[GenerationLog]]:
    rng = random.Random(cfg.seed)
    population = [evaluate_chromosome(random_chromosome(cfg, rng), cfg) for _ in range(cfg.population_size)]
    logs: List[GenerationLog] = []

    for generation in range(cfg.generations):
        feasible = [ind for ind in population if ind.feasible]
        feasible_ratio = len(feasible) / len(population)
        _, best_front_size = _best_feasible_individual(population, cfg)
        (
            best_difficulty_error,
            best_structural_diversity,
            best_emptiness_error,
            best_emptiness,
            best_difficulty_curve_error,
            best_family_balance,
        ) = _metric_extrema(population)
        logs.append(
            GenerationLog(
                generation=generation,
                feasible_ratio=feasible_ratio,
                feasible_count=len(feasible),
                best_front_size=best_front_size,
                best_difficulty_error=best_difficulty_error,
                best_structural_diversity=best_structural_diversity,
                best_emptiness_error=best_emptiness_error,
                best_emptiness=best_emptiness,
                best_difficulty_curve_error=best_difficulty_curve_error,
                best_family_balance=best_family_balance,
                constraint_violation_counts=_constraint_violation_counts(population),
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


def individual_as_log_dict(individual: Individual, cfg: MarioConfig) -> Dict[str, object]:
    return {
        "chromosome": list(individual.chromosome),
        "segment_metadata": chromosome_segment_metadata(individual.chromosome, cfg),
        "constraints": individual.constraints.as_log_dict(),
        "evaluation": individual.evaluation.as_objectives() if individual.evaluation else None,
    }


def population_constraint_report(population: Sequence[Individual], cfg: MarioConfig) -> Dict[str, object]:
    feasible = [individual for individual in population if individual.feasible]
    best_individual, best_front_size = _best_feasible_individual(population, cfg)
    return {
        "population_size": len(population),
        "feasible_count": len(feasible),
        "best_front_size": best_front_size,
        "violation_counts": _constraint_violation_counts(population),
        "individuals": [individual_as_log_dict(individual, cfg) for individual in population],
        "best_individual": individual_as_log_dict(best_individual, cfg) if best_individual else None,
    }


def logs_as_dicts(logs: Iterable[GenerationLog]) -> List[Dict[str, Union[float, int, None, Dict[str, int]]]]:
    return [asdict(log) for log in logs]
