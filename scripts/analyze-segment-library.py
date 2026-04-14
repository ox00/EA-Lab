#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

from ea_lab.pcg.config import MarioConfig
from ea_lab.pcg.models import Tile
from ea_lab.pcg.segments import build_segment_library


SOLID_TILES = {Tile.GROUND, Tile.BRICK, Tile.QUESTION, Tile.PIPE}


def count_tile(grid: list[list[int]], tile: int) -> int:
    return sum(1 for row in grid for value in row if value == tile)


def main() -> None:
    cfg = MarioConfig()
    segments = build_segment_library(cfg)
    rows = []
    total_tiles = cfg.height * cfg.segment_width

    for segment_id, grid in sorted(segments.items()):
        empty_count = count_tile(grid, Tile.EMPTY)
        solid_count = sum(1 for row in grid for value in row if value in SOLID_TILES)
        row = {
            "segment_id": segment_id,
            "empty_ratio": empty_count / total_tiles,
            "solid_ratio": solid_count / total_tiles,
            "enemy_count": count_tile(grid, Tile.ENEMY),
            "question_count": count_tile(grid, Tile.QUESTION),
            "pipe_count": count_tile(grid, Tile.PIPE),
            "coin_count": count_tile(grid, Tile.COIN),
        }
        rows.append(row)

    output_dir = Path("output/pcg/segment_library_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "segment_count": len(rows),
        "avg_empty_ratio": sum(row["empty_ratio"] for row in rows) / len(rows),
        "max_empty_ratio": max(row["empty_ratio"] for row in rows),
        "min_empty_ratio": min(row["empty_ratio"] for row in rows),
        "segments_over_0_80_empty": [row["segment_id"] for row in rows if row["empty_ratio"] > 0.80],
        "segments_with_enemy": [row["segment_id"] for row in rows if row["enemy_count"] > 0],
        "segments_with_pipe": [row["segment_id"] for row in rows if row["pipe_count"] > 0],
        "segments_with_question": [row["segment_id"] for row in rows if row["question_count"] > 0],
    }

    (output_dir / "segment_density.json").write_text(
        json.dumps({"summary": summary, "segments": rows}, indent=2) + "\n",
        encoding="utf-8",
    )

    with (output_dir / "segment_density.csv").open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    lines = [
        "# Segment Library Density",
        "",
        f"- segment_count: {summary['segment_count']}",
        f"- avg_empty_ratio: {summary['avg_empty_ratio']:.4f}",
        f"- min_empty_ratio: {summary['min_empty_ratio']:.4f}",
        f"- max_empty_ratio: {summary['max_empty_ratio']:.4f}",
        f"- segments_over_0_80_empty: {summary['segments_over_0_80_empty']}",
        f"- segments_with_enemy: {summary['segments_with_enemy']}",
        f"- segments_with_pipe: {summary['segments_with_pipe']}",
        f"- segments_with_question: {summary['segments_with_question']}",
        "",
        "| segment_id | empty_ratio | solid_ratio | enemy_count | question_count | pipe_count | coin_count |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['segment_id']} | {row['empty_ratio']:.4f} | {row['solid_ratio']:.4f} | "
            f"{row['enemy_count']} | {row['question_count']} | {row['pipe_count']} | {row['coin_count']} |"
        )
    (output_dir / "segment_density.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Segment density JSON:", output_dir / "segment_density.json")
    print("Segment density CSV:", output_dir / "segment_density.csv")
    print("Segment density Markdown:", output_dir / "segment_density.md")


if __name__ == "__main__":
    main()
