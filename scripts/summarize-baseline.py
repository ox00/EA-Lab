#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean
from statistics import pstdev


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize EA vs NSGA-II baseline outputs.")
    parser.add_argument("--base-dir", type=str, required=True, help="Directory that contains <algo>_seed*/")
    parser.add_argument("--algorithms", nargs="+", default=["ea", "nsga2"])
    parser.add_argument("--output-prefix", type=str, default="compare_summary")
    return parser.parse_args()


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_std(values: list[float]) -> float | None:
    return pstdev(values) if len(values) > 1 else 0.0 if len(values) == 1 else None


def load_run(run_dir: Path) -> dict[str, float | int | bool | None]:
    summary_path = run_dir / "summary.json"
    logs_path = run_dir / "logs.json"
    if not summary_path.exists() or not logs_path.exists():
        raise FileNotFoundError(f"Missing summary/logs in {run_dir}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    logs = json.loads(logs_path.read_text(encoding="utf-8"))
    evaluation = summary.get("evaluation") or {}
    constraints = summary.get("constraints") or {}
    last_log = logs[-1] if logs else {}

    return {
        "difficulty_error": evaluation.get("difficulty_error"),
        "structural_diversity": evaluation.get("structural_diversity"),
        "emptiness_error": evaluation.get("emptiness_error"),
        "emptiness": evaluation.get("emptiness"),
        "difficulty_curve_error": evaluation.get("difficulty_curve_error"),
        "family_balance": evaluation.get("family_balance"),
        "best_is_feasible": bool(constraints.get("is_feasible")),
        "feasible_generations": summary.get("feasible_generations"),
        "last_feasible_ratio": last_log.get("feasible_ratio"),
        "last_first_front_size": last_log.get("first_front_size"),
        "last_first_front_hv": last_log.get("first_front_hv"),
        "last_first_front_spread": last_log.get("first_front_spread"),
    }


def aggregate_runs(base_dir: Path, algorithm: str) -> dict[str, float | int | str | None]:
    run_dirs = sorted(base_dir.glob(f"{algorithm}_seed*"))
    records = [load_run(run_dir) for run_dir in run_dirs]

    difficulty = [r["difficulty_error"] for r in records if isinstance(r["difficulty_error"], (float, int))]
    diversity = [r["structural_diversity"] for r in records if isinstance(r["structural_diversity"], (float, int))]
    emptiness_error = [r["emptiness_error"] for r in records if isinstance(r["emptiness_error"], (float, int))]
    emptiness = [r["emptiness"] for r in records if isinstance(r["emptiness"], (float, int))]
    difficulty_curve_error = [r["difficulty_curve_error"] for r in records if isinstance(r["difficulty_curve_error"], (float, int))]
    family_balance = [r["family_balance"] for r in records if isinstance(r["family_balance"], (float, int))]
    best_feasible = [1.0 if r["best_is_feasible"] else 0.0 for r in records]
    feasible_generations = [
        float(r["feasible_generations"]) for r in records if isinstance(r["feasible_generations"], (float, int))
    ]
    last_feasible_ratio = [r["last_feasible_ratio"] for r in records if isinstance(r["last_feasible_ratio"], (float, int))]
    last_first_front_size = [
        float(r["last_first_front_size"]) for r in records if isinstance(r["last_first_front_size"], (float, int))
    ]
    last_first_front_hv = [
        float(r["last_first_front_hv"]) for r in records if isinstance(r["last_first_front_hv"], (float, int))
    ]
    last_first_front_spread = [
        float(r["last_first_front_spread"]) for r in records if isinstance(r["last_first_front_spread"], (float, int))
    ]

    return {
        "algorithm": algorithm,
        "runs": len(records),
        "avg_best_difficulty_error": safe_mean(difficulty),
        "std_best_difficulty_error": safe_std(difficulty),
        "avg_best_structural_diversity": safe_mean(diversity),
        "std_best_structural_diversity": safe_std(diversity),
        "avg_best_emptiness_error": safe_mean(emptiness_error),
        "std_best_emptiness_error": safe_std(emptiness_error),
        "avg_best_emptiness": safe_mean(emptiness),
        "std_best_emptiness": safe_std(emptiness),
        "avg_best_difficulty_curve_error": safe_mean(difficulty_curve_error),
        "avg_best_family_balance": safe_mean(family_balance),
        "best_feasible_ratio": safe_mean(best_feasible),
        "avg_feasible_generations": safe_mean(feasible_generations),
        "avg_last_feasible_ratio": safe_mean(last_feasible_ratio),
        "avg_last_first_front_size": safe_mean(last_first_front_size),
        "avg_last_first_front_hv": safe_mean(last_first_front_hv),
        "avg_last_first_front_spread": safe_mean(last_first_front_spread),
    }


def write_csv(path: Path, rows: list[dict[str, float | int | str | None]]) -> None:
    fields = [
        "algorithm",
        "runs",
        "avg_best_difficulty_error",
        "std_best_difficulty_error",
        "avg_best_structural_diversity",
        "std_best_structural_diversity",
        "avg_best_emptiness_error",
        "std_best_emptiness_error",
        "avg_best_emptiness",
        "std_best_emptiness",
        "avg_best_difficulty_curve_error",
        "avg_best_family_balance",
        "best_feasible_ratio",
        "avg_feasible_generations",
        "avg_last_feasible_ratio",
        "avg_last_first_front_size",
        "avg_last_first_front_hv",
        "avg_last_first_front_spread",
    ]
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fmt(value: float | int | str | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def write_markdown(path: Path, rows: list[dict[str, float | int | str | None]]) -> None:
    headers = [
        "algorithm",
        "runs",
        "avg_best_difficulty_error",
        "std_best_difficulty_error",
        "avg_best_structural_diversity",
        "avg_best_emptiness_error",
        "avg_best_emptiness",
        "avg_best_difficulty_curve_error",
        "avg_best_family_balance",
        "best_feasible_ratio",
        "avg_last_first_front_size",
        "avg_last_first_front_hv",
        "avg_last_first_front_spread",
    ]
    lines = [
        "# Baseline Compare Summary",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(header)) for header in headers) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    base_dir = Path(args.base_dir)
    rows = [aggregate_runs(base_dir, algorithm) for algorithm in args.algorithms]

    output_prefix = base_dir / args.output_prefix
    json_path = output_prefix.with_suffix(".json")
    csv_path = output_prefix.with_suffix(".csv")
    md_path = output_prefix.with_suffix(".md")

    json_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_path, rows)
    write_markdown(md_path, rows)

    print("Summary JSON:", json_path)
    print("Summary CSV:", csv_path)
    print("Summary Markdown:", md_path)


if __name__ == "__main__":
    main()
