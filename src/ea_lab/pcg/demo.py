from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from .config import MarioConfig
from .decode import decode_chromosome
from .ea import individual_as_log_dict
from .ea import logs_as_dicts as ea_logs_as_dicts
from .ea import population_constraint_report
from .ea import run_minimal_ea
from .ea import top_k_feasible_frontier
from .nsga2 import logs_as_dicts as nsga2_logs_as_dicts
from .nsga2 import run_nsga2
from .render import render_ascii
from .render import render_pygame
from .segments import chromosome_segment_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Mario-like PCG baseline experiments.")
    parser.add_argument("--height", type=int, default=16)
    parser.add_argument("--segment-width", type=int, default=14)
    parser.add_argument("--num-segments", type=int, default=8)
    parser.add_argument("--max-jumpable-gap", type=int, default=3)
    parser.add_argument("--target-difficulty", type=float, default=0.55)
    parser.add_argument("--target-emptiness", type=float, default=0.45)
    parser.add_argument("--population-size", type=int, default=20)
    parser.add_argument("--crossover-rate", type=float, default=0.9)
    parser.add_argument("--mutation-rate", type=float, default=0.2)
    parser.add_argument("--generations", type=int, default=10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output-dir", type=str, default="output/pcg/mvp")
    parser.add_argument("--algorithm", choices=["ea", "nsga2"], default="ea")
    parser.add_argument("--init-mode", choices=["random", "ai_seeded"], default="random")
    parser.add_argument(
        "--nsga2-objective-mode",
        choices=["core_3obj", "family_4obj", "curve_4obj", "semantic_5obj"],
        default="core_3obj",
    )
    parser.add_argument("--ai-seed-ratio", type=float, default=0.5)
    parser.add_argument("--ai-seed-temperature", type=float, default=0.9)
    parser.add_argument("--ai-seed-start-length", type=int, default=3)
    parser.add_argument("--render-backend", choices=["ascii", "pygame", "both"], default="both")
    parser.add_argument("--tile-size", type=int, default=24)
    parser.add_argument("--top-k-frontier", type=int, default=5)
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> MarioConfig:
    return MarioConfig(
        height=args.height,
        segment_width=args.segment_width,
        num_segments=args.num_segments,
        max_jumpable_gap=args.max_jumpable_gap,
        target_difficulty=args.target_difficulty,
        target_emptiness=args.target_emptiness,
        population_size=args.population_size,
        crossover_rate=args.crossover_rate,
        mutation_rate=args.mutation_rate,
        generations=args.generations,
        seed=args.seed,
        nsga2_objective_mode=args.nsga2_objective_mode,
        init_mode=args.init_mode,
        ai_seed_ratio=args.ai_seed_ratio,
        ai_seed_temperature=args.ai_seed_temperature,
        ai_seed_start_length=args.ai_seed_start_length,
    )


def write_artifacts(
    output_dir: Path,
    algorithm: str,
    cfg: MarioConfig,
    best_chromosome: List[int],
    constraints: Dict[str, object],
    evaluation: Optional[Dict[str, float]],
    logs: List[Dict[str, Union[float, int, None, Dict[str, int]]]],
    constraint_report: Dict[str, object],
    frontier_levels: List[Dict[str, object]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(json.dumps(cfg.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "logs.json").write_text(json.dumps(logs, indent=2) + "\n", encoding="utf-8")
    (output_dir / "constraint_report.json").write_text(
        json.dumps(constraint_report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "frontier_summary.json").write_text(
        json.dumps({"top_k": len(frontier_levels), "levels": frontier_levels}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = {
        "algorithm": algorithm,
        "nsga2_objective_mode": cfg.nsga2_objective_mode if algorithm == "nsga2" else None,
        "init_mode": cfg.init_mode,
        "best_chromosome": best_chromosome,
        "best_segment_metadata": chromosome_segment_metadata(best_chromosome, cfg),
        "constraints": constraints,
        "evaluation": evaluation,
        "feasible_generations": sum(1 for log in logs if (log["feasible_ratio"] or 0) > 0),
        "constraint_report": "constraint_report.json",
        "frontier_summary": "frontier_summary.json",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    cfg = build_config(args)

    if args.algorithm == "ea":
        population, logs = run_minimal_ea(cfg)
        logs_dict = ea_logs_as_dicts(logs)
    else:
        population, logs = run_nsga2(cfg)
        logs_dict = nsga2_logs_as_dicts(logs)

    best = population[0]
    level = decode_chromosome(best.chromosome, cfg)
    constraint_report = population_constraint_report(population, cfg)
    frontier = top_k_feasible_frontier(population, args.top_k_frontier, cfg)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.render_backend in ("ascii", "both"):
        render_ascii(level, output_dir / "best_level.txt")
    if args.render_backend in ("pygame", "both"):
        try:
            render_pygame(level, output_dir / "best_level.png", tile_size=args.tile_size)
        except RuntimeError as exc:
            print("Pygame render skipped:", str(exc))

    frontier_dir = output_dir / "frontier_levels"
    frontier_dir.mkdir(parents=True, exist_ok=True)
    frontier_levels: List[Dict[str, object]] = []
    for rank, individual in enumerate(frontier, start=1):
        frontier_level = decode_chromosome(individual.chromosome, cfg)
        ascii_name = f"frontier_{rank:02d}.txt"
        render_ascii(frontier_level, frontier_dir / ascii_name)
        record: Dict[str, object] = {
            "rank": rank,
            "ascii_path": f"frontier_levels/{ascii_name}",
            "individual": individual_as_log_dict(individual, cfg),
        }
        if args.render_backend in ("pygame", "both"):
            png_name = f"frontier_{rank:02d}.png"
            try:
                render_pygame(frontier_level, frontier_dir / png_name, tile_size=args.tile_size)
                record["png_path"] = f"frontier_levels/{png_name}"
            except RuntimeError as exc:
                print(f"Pygame frontier render skipped for rank {rank}:", str(exc))
        frontier_levels.append(record)

    write_artifacts(
        output_dir=output_dir,
        algorithm=args.algorithm,
        cfg=cfg,
        best_chromosome=best.chromosome,
        constraints=best.constraints.as_log_dict(),
        evaluation=best.evaluation.as_objectives() if best.evaluation else None,
        logs=logs_dict,
        constraint_report=constraint_report,
        frontier_levels=frontier_levels,
    )

    print("Output dir:", str(output_dir))
    print("Algorithm:", args.algorithm)
    if args.algorithm == "nsga2":
        print("NSGA-II objective mode:", cfg.nsga2_objective_mode)
    print("Init mode:", cfg.init_mode)
    print("Best chromosome:", best.chromosome)
    print("Constraints:", best.constraints.as_log_dict())
    print("Evaluation:", best.evaluation.as_objectives() if best.evaluation else None)
    print("Constraint report:", json.dumps(individual_as_log_dict(best, cfg), indent=2))
    print("Frontier levels exported:", len(frontier_levels))
    print("Generations:", len(logs))


if __name__ == "__main__":
    main()
