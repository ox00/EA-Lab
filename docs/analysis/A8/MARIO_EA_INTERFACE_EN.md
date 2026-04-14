# Mario EA Interface Specification (EN)

## Document Role
This document defines the formal collaboration contract for A8 MVP.

It governs:
- level generation / decoding module
- EA or MOEA optimization module
- evaluation and reporting consistency

## Baseline Policy
MVP policy is fixed as:

1. Explicit Mario segment encoding.
2. Hard feasibility constraints.
3. Multi-objective EA optimization.

AI-based generation is out of MVP scope and can be added only as a later extension.

## Mandatory Pipeline
```text
chromosome -> decode -> phenotype -> check_constraints -> evaluate -> selection
```

## Representation Contract
### Genotype
MVP genotype format:
- fixed-length sequence of integer segment IDs

### Phenotype
Decoded tile grid used for:
- feasibility validation
- objective evaluation
- rendering

### Rendering
Rendering is presentation output only.
It must not alter logical level structure.

## Frozen Configuration
The following values are frozen per protocol version:

1. `map_height`
2. `segment_width`
3. `num_segments`
4. tile vocabulary and semantics
5. segment library schema
6. `target_difficulty`
7. `target_emptiness`

Derived:
- `map_width = segment_width * num_segments`

## API Contract
```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

### Required constraint keys
```python
{
  "is_feasible": bool,
  "start_ok": bool,
  "goal_ok": bool,
  "reachable": bool,
  "illegal_overlap": bool,
  "max_gap_ok": bool
}
```

### Required evaluation keys
```python
{
    "difficulty_score": float,
    "difficulty_error": float,
    "structural_diversity": float,
    "emptiness_error": float,
    "emptiness": float
}
```

## Feasibility Policy
Feasibility is a hard gate in MVP.

Rules:
1. Infeasible candidates cannot be accepted final outputs.
2. Survivor logic must prioritize feasible candidates.

## Objective Policy
MVP objective tuple:

1. minimize `difficulty_error`
2. maximize `structural_diversity`
3. minimize `emptiness_error`

Notes:
- `emptiness` is retained as an observable descriptor
- `emptiness_error = abs(emptiness - target_emptiness)`

Formal metric definitions are governed by:
- [MARIO_EVALUATION_SPEC_EN.md](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/docs/analysis/A8/MARIO_EVALUATION_SPEC_EN.md)

## Responsibility Split
### Generation side
1. Segment library management
2. Decode implementation
3. Render implementation
4. Tile semantic consistency

### EA side
1. Population initialization
2. Mutation and crossover
3. Feasible-first handling
4. Optimization loop and logs

## Acceptance Conditions
Interface acceptance requires:

1. stable API signatures
2. successful end-to-end run
3. complete required output keys
4. deterministic behavior under fixed seed

## Change Control
Any change to frozen configuration, constraints, objectives, or output schema requires:

1. protocol version increment
2. explicit split of experimental result sets by version
