from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import MarioConfig
from .decode import decode_chromosome
from .ea import logs_as_dicts as ea_logs_as_dicts
from .ea import run_minimal_ea
from .nsga2 import logs_as_dicts as nsga2_logs_as_dicts
from .nsga2 import run_nsga2
from .render import render_ascii
from .render import render_pygame


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run minimal Mario-like PCG EA MVP baseline.")
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
    parser.add_argument("--render-backend", choices=["ascii", "pygame", "both"], default="both")
    parser.add_argument("--tile-size", type=int, default=24)
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
    )


def write_artifacts(
    output_dir: Path,
    algorithm: str,
    cfg: MarioConfig,
    best_chromosome: list[int],
    constraints: dict[str, bool],
    evaluation: dict[str, float] | None,
    logs: list[dict[str, float | int | None]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(
        json.dumps(cfg.as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "logs.json").write_text(
        json.dumps(logs, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = {
        "algorithm": algorithm,
        "best_chromosome": best_chromosome,
        "constraints": constraints,
        "evaluation": evaluation,
        "feasible_generations": sum(1 for log in logs if (log["feasible_ratio"] or 0) > 0),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )


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

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.render_backend in ("ascii", "both"):
        render_ascii(level, output_dir / "best_level.txt")
    if args.render_backend in ("pygame", "both"):
        try:
            render_pygame(level, output_dir / "best_level.png", tile_size=args.tile_size)
        except RuntimeError as exc:
            print("Pygame render skipped:", str(exc))
    write_artifacts(
        output_dir=output_dir,
        algorithm=args.algorithm,
        cfg=cfg,
        best_chromosome=best.chromosome,
        constraints=best.constraints.as_dict(),
        evaluation=best.evaluation.as_objectives() if best.evaluation else None,
        logs=logs_dict,
    )

    print("Output dir:", str(output_dir))
    print("Algorithm:", args.algorithm)
    print("Best chromosome:", best.chromosome)
    print("Constraints:", best.constraints.as_dict())
    print("Evaluation:", best.evaluation.as_objectives() if best.evaluation else None)
    print("Generations:", len(logs))


if __name__ == "__main__":
    main()
