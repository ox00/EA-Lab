from __future__ import annotations

from .config import MarioConfig
from .models import Chromosome, Level, Tile
from .segments import build_segment_library


def decode_chromosome(chromosome: Chromosome, cfg: MarioConfig) -> Level:
    library = build_segment_library(cfg)
    grid = [[Tile.EMPTY for _ in range(cfg.width)] for _ in range(cfg.height)]

    for seg_idx, segment_id in enumerate(chromosome):
        segment = library[segment_id]
        start_col = seg_idx * cfg.segment_width
        for row in range(cfg.height):
            for col in range(cfg.segment_width):
                grid[row][start_col + col] = segment[row][col]

    grid[cfg.height - 3][1] = Tile.START
    grid[cfg.height - 3][cfg.width - 2] = Tile.GOAL
    return Level(grid=grid)
