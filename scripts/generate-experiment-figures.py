#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-codex")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output" / "pcg" / "figures"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def plot_baseline_compare() -> None:
    rows = load_json(ROOT / "output" / "pcg" / "baseline_compare" / "compare_summary.json")
    algorithms = [row["algorithm"] for row in rows]
    difficulty = [row["avg_best_difficulty_error"] for row in rows]
    diversity = [row["avg_best_structural_diversity"] for row in rows]
    emptiness_error = [row["avg_best_emptiness_error"] for row in rows]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle("Baseline Compare: EA vs NSGA-II", fontsize=14)

    axes[0].bar(algorithms, difficulty, color=["#8b5e34", "#2a9d8f"])
    axes[0].set_title("Difficulty Error")
    axes[0].set_ylabel("Lower is better")

    axes[1].bar(algorithms, diversity, color=["#8b5e34", "#2a9d8f"])
    axes[1].set_title("Structural Diversity")
    axes[1].set_ylabel("Higher is better")

    axes[2].bar(algorithms, emptiness_error, color=["#8b5e34", "#2a9d8f"])
    axes[2].set_title("Emptiness Error")
    axes[2].set_ylabel("Lower is better")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "baseline_compare_metrics.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def _heatmap_matrix(rows, key):
    populations = sorted({row["population_size"] for row in rows})
    mutations = sorted({row["mutation_rate"] for row in rows})
    matrix = []
    for pop in populations:
        row_values = []
        for mut in mutations:
            matched = next(item for item in rows if item["population_size"] == pop and item["mutation_rate"] == mut)
            row_values.append(matched[key])
        matrix.append(row_values)
    return populations, mutations, matrix


def plot_parameter_scan_heatmaps() -> None:
    rows = load_json(ROOT / "output" / "pcg" / "parameter_scan" / "scan_summary.json")
    metrics = [
        ("avg_difficulty_error", "Difficulty Error", "lower"),
        ("avg_emptiness_error", "Emptiness Error", "lower"),
        ("avg_first_front_hv", "Hypervolume", "higher"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("NSGA-II Parameter Scan (V2 Segment Library)", fontsize=14)

    for axis, (key, title, _) in zip(axes, metrics):
        populations, mutations, matrix = _heatmap_matrix(rows, key)
        image = axis.imshow(matrix, cmap="YlGnBu", aspect="auto")
        axis.set_title(title)
        axis.set_xticks(range(len(mutations)), [str(value) for value in mutations])
        axis.set_yticks(range(len(populations)), [str(value) for value in populations])
        axis.set_xlabel("Mutation Rate")
        axis.set_ylabel("Population Size")
        for row_index, values in enumerate(matrix):
            for col_index, value in enumerate(values):
                axis.text(col_index, row_index, f"{value:.3f}", ha="center", va="center", color="black", fontsize=8)
        fig.colorbar(image, ax=axis, fraction=0.046, pad=0.04)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "parameter_scan_heatmaps.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_showcase_curves() -> None:
    cases = {
        "pop40_mut0.1_seed7": ROOT / "output" / "pcg" / "showcase" / "pop40_mut0_1_seed7" / "logs.json",
        "pop20_mut0.3_seed7": ROOT / "output" / "pcg" / "showcase" / "pop20_mut0_3_seed7" / "logs.json",
    }
    loaded = {name: load_json(path) for name, path in cases.items()}

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Showcase Runs: Generation Trends", fontsize=14)
    metric_specs = [
        ("best_difficulty_error", "Difficulty Error"),
        ("best_structural_diversity", "Structural Diversity"),
        ("best_emptiness_error", "Emptiness Error"),
        ("first_front_hv", "First-Front Hypervolume"),
    ]

    for axis, (metric_key, title) in zip(axes.flat, metric_specs):
        for name, logs in loaded.items():
            generations = [log["generation"] for log in logs]
            values = [log.get(metric_key) for log in logs]
            axis.plot(generations, values, label=name, linewidth=2)
        axis.set_title(title)
        axis.set_xlabel("Generation")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "showcase_generation_curves.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_baseline_compare()
    plot_parameter_scan_heatmaps()
    plot_showcase_curves()
    print("Figures generated in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
