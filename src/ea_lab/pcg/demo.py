from __future__ import annotations

from pathlib import Path

from .config import MarioConfig
from .decode import decode_chromosome
from .ea import run_minimal_ea
from .render import render_ascii


def main() -> None:
    cfg = MarioConfig()
    population, logs = run_minimal_ea(cfg)
    best = population[0]
    level = decode_chromosome(best.chromosome, cfg)

    output_dir = Path("output/pcg")
    output_dir.mkdir(parents=True, exist_ok=True)
    render_ascii(level, output_dir / "best_level.txt")

    print("Best chromosome:", best.chromosome)
    print("Constraints:", best.constraints.as_dict())
    print("Evaluation:", best.evaluation.as_objectives() if best.evaluation else None)
    print("Generation logs:")
    for log in logs:
        print(log)


if __name__ == "__main__":
    main()
