from __future__ import annotations

import json
import random
from pathlib import Path
from typing import List

import torch

from ai_generator.model import SegmentLSTM

from .config import MarioConfig
from .constraints import check_constraints
from .decode import decode_chromosome
from .models import Chromosome
from .segments import build_segment_library
from .segments import build_segment_spec_library


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _valid_segment_ids(cfg: MarioConfig) -> set[int]:
    return set(build_segment_library(cfg).keys())


def _load_processed_sequences() -> list[list[int]]:
    data_path = _repo_root() / "data" / "processed" / "vglc_chromosomes_approx.json"
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    return [entry["chromosome"] for entry in payload.get("data", []) if entry.get("chromosome")]


def adapt_ai_chromosome(
    source: list[int],
    cfg: MarioConfig,
    rng: random.Random,
) -> Chromosome:
    valid_ids = _valid_segment_ids(cfg)
    filtered = [segment_id for segment_id in source if segment_id in valid_ids]
    if not filtered:
        filtered = [0]

    if len(filtered) >= cfg.num_segments:
        if len(filtered) == cfg.num_segments:
            return filtered[:]
        start = rng.randrange(0, len(filtered) - cfg.num_segments + 1)
        return filtered[start : start + cfg.num_segments]

    child = filtered[:]
    while len(child) < cfg.num_segments:
        child.append(rng.choice(filtered))
    return child


def sample_processed_seed(cfg: MarioConfig, rng: random.Random) -> Chromosome:
    sequences = _load_processed_sequences()
    chromosome = adapt_ai_chromosome(rng.choice(sequences), cfg, rng)
    return repair_ai_chromosome(chromosome, cfg, rng) if cfg.ai_seed_repair else chromosome


def _load_lstm_checkpoint() -> dict:
    checkpoint_path = _repo_root() / "models" / "lstm_generator.pt"
    return torch.load(checkpoint_path, map_location="cpu")


def _build_lstm_model(checkpoint: dict) -> SegmentLSTM:
    model = SegmentLSTM(
        vocab_size=checkpoint["vocab_size"],
        embedding_dim=checkpoint["embed_dim"],
        hidden_dim=checkpoint["hidden_dim"],
        num_layers=checkpoint["num_layers"],
        dropout=checkpoint["dropout"],
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model


def sample_lstm_seed(cfg: MarioConfig, rng: random.Random) -> Chromosome:
    sequences = _load_processed_sequences()
    checkpoint = _load_lstm_checkpoint()
    model = _build_lstm_model(checkpoint)

    seed_sequence = rng.choice(sequences)
    prefix_length = min(max(1, cfg.ai_seed_start_length), len(seed_sequence))
    start_ids = seed_sequence[:prefix_length]
    generated = model.generate(
        start_ids=start_ids,
        max_length=max(cfg.num_segments, len(start_ids)),
        temperature=cfg.ai_seed_temperature,
        device=torch.device("cpu"),
    )
    chromosome = adapt_ai_chromosome(generated, cfg, rng)
    return repair_ai_chromosome(chromosome, cfg, rng) if cfg.ai_seed_repair else chromosome


def _repair_candidate_ids(cfg: MarioConfig) -> list[int]:
    library = build_segment_spec_library(cfg)
    preferred = []
    fallback = []
    for segment_id, spec in library.items():
        if spec.family in {"flat_safe", "reward_relief", "pipe_pressure"}:
            preferred.append(segment_id)
        else:
            fallback.append(segment_id)
    return preferred + fallback


def repair_ai_chromosome(chromosome: Chromosome, cfg: MarioConfig, rng: random.Random) -> Chromosome:
    child = chromosome[:]
    constraints = check_constraints(decode_chromosome(child, cfg), cfg)
    if constraints.is_feasible:
        return child

    candidate_ids = _repair_candidate_ids(cfg)

    for _ in range(cfg.num_segments * 3):
        if constraints.reachable:
            break
        updated = False
        for idx, segment_id in enumerate(child):
            spec = build_segment_spec_library(cfg)[segment_id]
            if spec.family == "gap_jump":
                child[idx] = 0
                updated = True
                break
        if not updated:
            replace_idx = rng.randrange(len(child))
            child[replace_idx] = candidate_ids[0]
        constraints = check_constraints(decode_chromosome(child, cfg), cfg)
        if constraints.is_feasible:
            return child

    for _ in range(cfg.num_segments * 6):
        idx = rng.randrange(len(child))
        replacement = candidate_ids[rng.randrange(min(8, len(candidate_ids)))]
        old_value = child[idx]
        child[idx] = replacement
        constraints = check_constraints(decode_chromosome(child, cfg), cfg)
        if constraints.is_feasible:
            return child
        if constraints.violation_count > 1:
            child[idx] = old_value

    return child


def seeded_chromosome(cfg: MarioConfig, rng: random.Random) -> Chromosome:
    try:
        return sample_lstm_seed(cfg, rng)
    except Exception:
        return sample_processed_seed(cfg, rng)
