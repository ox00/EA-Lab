#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from statistics import mean
from statistics import pstdev


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small NSGA-II parameter scan.")
    parser.add_argument("--algorithm", type=str, default="nsga2")
    parser.add_argument("--population-sizes", nargs="+", type=int, default=[20, 30, 40])
    parser.add_argument("--mutation-rates", nargs="+", type=float, default=[0.1, 0.2, 0.3])
    parser.add_argument("--seeds", nargs="+", type=int, default=[7, 17, 27])
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--output-root", type=str, default="output/pcg/parameter_scan")
    return parser.parse_args()


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_std(values: list[float]) -> float | None:
    return pstdev(values) if len(values) > 1 else 0.0 if len(values) == 1 else None


def run_experiment(args: argparse.Namespace, population_size: int, mutation_rate: float, seed: int, run_dir: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    cmd = [
        sys.executable,
        "-m",
        "ea_lab.pcg.demo",
        "--algorithm",
        args.algorithm,
        "--population-size",
        str(population_size),
        "--mutation-rate",
        str(mutation_rate),
        "--generations",
        str(args.generations),
        "--seed",
        str(seed),
        "--render-backend",
        "ascii",
        "--output-dir",
        str(run_dir),
    ]
    subprocess.run(cmd, cwd=Path(__file__).resolve().parent.parent, env=env, check=True)


def load_run(run_dir: Path) -> dict[str, float | int | None]:
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    logs = json.loads((run_dir / "logs.json").read_text(encoding="utf-8"))
    evaluation = summary.get("evaluation") or {}
    last_log = logs[-1] if logs else {}
    return {
        "difficulty_error": evaluation.get("difficulty_error"),
        "structural_diversity": evaluation.get("structural_diversity"),
        "emptiness_error": evaluation.get("emptiness_error"),
        "emptiness": evaluation.get("emptiness"),
        "feasible_ratio": last_log.get("feasible_ratio"),
        "first_front_size": last_log.get("first_front_size"),
        "first_front_hv": last_log.get("first_front_hv"),
        "first_front_spread": last_log.get("first_front_spread"),
    }


def aggregate_combo(population_size: int, mutation_rate: float, records: list[dict[str, float | int | None]]) -> dict[str, float | int]:
    def values(key: str) -> list[float]:
        return [float(record[key]) for record in records if isinstance(record.get(key), (float, int))]

    return {
        "population_size": population_size,
        "mutation_rate": mutation_rate,
        "runs": len(records),
        "avg_difficulty_error": safe_mean(values("difficulty_error")),
        "std_difficulty_error": safe_std(values("difficulty_error")),
        "avg_structural_diversity": safe_mean(values("structural_diversity")),
        "avg_emptiness_error": safe_mean(values("emptiness_error")),
        "avg_emptiness": safe_mean(values("emptiness")),
        "avg_feasible_ratio": safe_mean(values("feasible_ratio")),
        "avg_first_front_size": safe_mean(values("first_front_size")),
        "avg_first_front_hv": safe_mean(values("first_front_hv")),
        "avg_first_front_spread": safe_mean(values("first_front_spread")),
    }


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fmt(value: float | int | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def write_markdown(path: Path, rows: list[dict[str, float | int]]) -> None:
    headers = [
        "population_size",
        "mutation_rate",
        "avg_difficulty_error",
        "avg_structural_diversity",
        "avg_emptiness_error",
        "avg_first_front_hv",
        "avg_first_front_spread",
    ]
    lines = [
        "# Parameter Scan Summary",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(header)) for header in headers) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    aggregated_rows: list[dict[str, float | int]] = []
    for population_size in args.population_sizes:
        for mutation_rate in args.mutation_rates:
            combo_records = []
            combo_dir = output_root / f"pop{population_size}_mut{str(mutation_rate).replace('.', '_')}"
            combo_dir.mkdir(parents=True, exist_ok=True)
            for seed in args.seeds:
                run_dir = combo_dir / f"seed{seed}"
                run_experiment(args, population_size, mutation_rate, seed, run_dir)
                combo_records.append(load_run(run_dir))
            aggregated_rows.append(aggregate_combo(population_size, mutation_rate, combo_records))

    aggregated_rows.sort(key=lambda row: (row["population_size"], row["mutation_rate"]))
    json_path = output_root / "scan_summary.json"
    csv_path = output_root / "scan_summary.csv"
    md_path = output_root / "scan_summary.md"
    json_path.write_text(json.dumps(aggregated_rows, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_path, aggregated_rows)
    write_markdown(md_path, aggregated_rows)
    print("Scan JSON:", json_path)
    print("Scan CSV:", csv_path)
    print("Scan Markdown:", md_path)


if __name__ == "__main__":
    main()
