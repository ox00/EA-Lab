#!/usr/bin/env python3
"""
VGLC Data Parser with Approximate Segment Matching.
Parses The VGLC level data into segment ID sequences using a similarity
metric to match against the existing segment library.
"""

import json
import sys
from pathlib import Path

# Add src directory to Python path to import ea_lab package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ea_lab.pcg.models import Tile
from ea_lab.pcg.config import MarioConfig

# Mapping from VGLC characters to Tile enum values
VGLC_TO_TILE = {
    "-": Tile.EMPTY,
    "X": Tile.GROUND,
    "B": Tile.BRICK,
    "?": Tile.QUESTION,
    "o": Tile.COIN,
    "E": Tile.ENEMY,
    "P": Tile.PIPE,
    "S": Tile.START,
    "G": Tile.GOAL,
}

VALID_CHARS = set(VGLC_TO_TILE.keys())


def parse_vglc_file(file_path: Path) -> list[list[int]]:
    """
    Parse a single VGLC .txt file into a 2D grid of Tile integer values.
    Filters out invalid characters and empty rows.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        raw_lines = [line.rstrip("\n") for line in f]

    lines = []
    for line in raw_lines:
        if not line:
            continue
        filtered = [ch for ch in line if ch in VALID_CHARS]
        if filtered:
            lines.append(filtered)

    if not lines:
        return []

    max_len = max(len(row) for row in lines)
    grid = []
    for row in lines:
        tile_row = [VGLC_TO_TILE[ch] for ch in row]
        tile_row.extend([Tile.EMPTY] * (max_len - len(row)))
        grid.append(tile_row)
    return grid


def slice_grid_to_segments(
    grid: list[list[int]], segment_width: int
) -> list[list[list[int]]]:
    """Slice a full level grid into fixed-width segment grids."""
    height = len(grid)
    width = len(grid[0])
    segments = []
    for start_col in range(0, width, segment_width):
        end_col = min(start_col + segment_width, width)
        segment = [row[start_col:end_col] for row in grid]
        if end_col - start_col < segment_width:
            missing = segment_width - (end_col - start_col)
            for row in segment:
                row.extend([Tile.EMPTY] * missing)
        segments.append(segment)
    return segments


def align_grids(
    grid1: list[list[int]], grid2: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    """
    Align two grids to the same dimensions by padding with EMPTY tiles.
    Returns copies of both grids with identical height and width.
    """
    h1, w1 = len(grid1), len(grid1[0]) if grid1 else 0
    h2, w2 = len(grid2), len(grid2[0]) if grid2 else 0

    target_h = max(h1, h2)
    target_w = max(w1, w2)

    def pad_grid(grid, target_h, target_w):
        result = [row[:] for row in grid]
        # Pad height
        while len(result) < target_h:
            result.append([Tile.EMPTY] * target_w)
        # Pad width
        for row in result:
            if len(row) < target_w:
                row.extend([Tile.EMPTY] * (target_w - len(row)))
        return result

    return pad_grid(grid1, target_h, target_w), pad_grid(grid2, target_h, target_w)


def hamming_distance(grid1: list[list[int]], grid2: list[list[int]]) -> int:
    """
    Calculate Hamming distance between two grids, automatically aligning them
    to the same dimensions by padding.
    """
    g1, g2 = align_grids(grid1, grid2)
    dist = 0
    for r1, r2 in zip(g1, g2):
        for v1, v2 in zip(r1, r2):
            if v1 != v2:
                dist += 1
    return dist


def segment_to_best_match(
    segment: list[list[int]], library: dict[int, list[list[int]]]
) -> int:
    """
    Find the segment ID in the library that most closely matches the given
    segment grid, using Hamming distance.
    """
    best_id = -1
    best_dist = float("inf")
    for seg_id, lib_grid in library.items():
        dist = hamming_distance(segment, lib_grid)
        if dist < best_dist:
            best_dist = dist
            best_id = seg_id
    return best_id


def main():
    cfg = MarioConfig()

    # Build library once
    from ea_lab.pcg.segments import build_segment_library
    library = build_segment_library(cfg)

    # Verify library is not empty and has correct dimensions
    if not library:
        print("Error: Segment library is empty.")
        return
    first_grid = next(iter(library.values()))
    print(f"Library segment dimensions: {len(first_grid)} x {len(first_grid[0])}")

    data_root = Path(__file__).parent.parent / "data" / "raw" / "vglc"
    smb1_dir = data_root / "smb1"
    smb2j_dir = data_root / "smb2j"

    output_dir = Path(__file__).parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_files = list(smb1_dir.glob("*.txt")) + list(smb2j_dir.glob("*.txt"))
    all_files = [f for f in all_files if f.name.startswith(("mario", "SuperMario"))]

    print(f"Found {len(all_files)} level files.")

    all_chromosomes = []
    total_segments_processed = 0

    for txt_file in all_files:
        print(f"Processing: {txt_file.name}")
        grid = parse_vglc_file(txt_file)
        if not grid:
            continue

        print(f"  Parsed grid size: {len(grid)} x {len(grid[0])}")

        segments = slice_grid_to_segments(grid, cfg.segment_width)
        chromosome = []
        for seg in segments:
            best_id = segment_to_best_match(seg, library)
            chromosome.append(best_id)
            total_segments_processed += 1

        if chromosome:
            all_chromosomes.append(
                {
                    "source": str(txt_file.relative_to(data_root)),
                    "chromosome": chromosome,
                    "length": len(chromosome),
                }
            )

    # Save results
    output_file = output_dir / "vglc_chromosomes_approx.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "config": {
                    "segment_width": cfg.segment_width,
                    "num_segments_max": cfg.num_segments,
                    "total_chromosomes": len(all_chromosomes),
                    "matching_method": "approximate (hamming distance with padding)",
                },
                "data": all_chromosomes,
            },
            f,
            indent=2,
        )
    print(f"\nSuccessfully parsed {len(all_chromosomes)} chromosome sequences.")
    print(f"Total segments processed: {total_segments_processed}")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()