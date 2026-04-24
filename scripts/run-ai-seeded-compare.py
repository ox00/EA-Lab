#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare random init vs ai-seeded init for Mario PCG.")
    parser.add_argument("--algorithm", choices=["ea", "nsga2"], default="nsga2")
    parser.add_argument("--objective-mode", default="core_3obj")
    parser.add_argument("--population-size", type=int, default=20)
    parser.add_argument("--generations", type=int, default=10)
    parser.add_argument("--mutation-rate", type=float, default=0.2)
    parser.add_argument("--seeds", nargs="+", type=int, default=[7, 17, 27])
    parser.add_argument("--output-root", type=str, default="output/pcg/ai_seeded_compare")
    return parser.parse_args()


def run_once(args: argparse.Namespace, init_mode: str, seed: int, run_dir: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    cmd = [
        sys.executable,
        "-m",
        "ea_lab.pcg.demo",
        "--algorithm",
        args.algorithm,
        "--nsga2-objective-mode",
        args.objective_mode,
        "--init-mode",
        init_mode,
        "--population-size",
        str(args.population_size),
        "--generations",
        str(args.generations),
        "--mutation-rate",
        str(args.mutation_rate),
        "--seed",
        str(seed),
        "--render-backend",
        "ascii",
        "--output-dir",
        str(run_dir),
    ]
    subprocess.run(cmd, cwd=Path(__file__).resolve().parent.parent, env=env, check=True)


def load_run(run_dir: Path) -> dict[str, float | int | str | None]:
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    logs = json.loads((run_dir / "logs.json").read_text(encoding="utf-8"))
    evaluation = summary.get("evaluation") or {}
    last_log = logs[-1] if logs else {}
    return {
        "init_mode": summary.get("init_mode"),
        "difficulty_error": evaluation.get("difficulty_error"),
        "structural_diversity": evaluation.get("structural_diversity"),
        "emptiness_error": evaluation.get("emptiness_error"),
        "difficulty_curve_error": evaluation.get("difficulty_curve_error"),
        "family_balance": evaluation.get("family_balance"),
        "last_feasible_ratio": last_log.get("feasible_ratio"),
        "last_first_front_size": last_log.get("first_front_size") or last_log.get("best_front_size"),
        "last_first_front_hv": last_log.get("first_front_hv"),
        "last_first_front_spread": last_log.get("first_front_spread"),
    }


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def aggregate(init_mode: str, records: list[dict[str, float | int | str | None]]) -> dict[str, float | int | str | None]:
    def values(key: str) -> list[float]:
        return [float(record[key]) for record in records if isinstance(record.get(key), (int, float))]

    return {
        "init_mode": init_mode,
        "runs": len(records),
        "avg_difficulty_error": safe_mean(values("difficulty_error")),
        "avg_structural_diversity": safe_mean(values("structural_diversity")),
        "avg_emptiness_error": safe_mean(values("emptiness_error")),
        "avg_difficulty_curve_error": safe_mean(values("difficulty_curve_error")),
        "avg_family_balance": safe_mean(values("family_balance")),
        "avg_last_feasible_ratio": safe_mean(values("last_feasible_ratio")),
        "avg_last_first_front_size": safe_mean(values("last_first_front_size")),
        "avg_last_first_front_hv": safe_mean(values("last_first_front_hv")),
        "avg_last_first_front_spread": safe_mean(values("last_first_front_spread")),
    }


def write_markdown(path: Path, rows: list[dict[str, float | int | str | None]]) -> None:
    headers = [
        "init_mode",
        "runs",
        "avg_difficulty_error",
        "avg_structural_diversity",
        "avg_emptiness_error",
        "avg_difficulty_curve_error",
        "avg_family_balance",
        "avg_last_feasible_ratio",
        "avg_last_first_front_size",
        "avg_last_first_front_hv",
        "avg_last_first_front_spread",
    ]
    lines = [
        "# AI-Seeded Initialization Compare",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = row.get(header)
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    rows = []
    for init_mode in ["random", "ai_seeded"]:
        records = []
        for seed in args.seeds:
            run_dir = output_root / f"{init_mode}_seed{seed}"
            run_once(args, init_mode, seed, run_dir)
            records.append(load_run(run_dir))
        rows.append(aggregate(init_mode, records))

    (output_root / "compare_summary.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    write_markdown(output_root / "compare_summary.md", rows)
    print("Compare JSON:", output_root / "compare_summary.json")
    print("Compare Markdown:", output_root / "compare_summary.md")


if __name__ == "__main__":
    main()
