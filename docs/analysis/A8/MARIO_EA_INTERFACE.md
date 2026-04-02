# Mario EA Interface Specification

## Status
This document is the canonical interface contract for A8 MVP.

Scope:
- Mario-like single-domain level generation
- Explicit genotype and deterministic decoding
- Feasibility-first evaluation and EA/MOEA search

## Pipeline
The mandatory data flow is:

```text
chromosome -> decode -> phenotype -> check_constraints -> evaluate -> selection
```

## Core Terms
### Genotype
Search-space representation used by EA.

MVP format:
- `segment ID sequence`
- fixed-length integer list

### Phenotype
Decoded logical level grid.

The phenotype is the object consumed by:
- constraints
- objective evaluation
- rendering

### Rendered Level
Visual projection of phenotype for review artifacts.
Rendering style does not modify level logic.

## Frozen Constants
The following constants must be fixed before baseline experiments:

1. `map_height`
2. `segment_width`
3. `num_segments`
4. `tile_vocabulary`
5. `segment_library_schema`

Derived:
- `map_width = segment_width * num_segments`

## Tile Vocabulary Requirement
Each tile ID must have one and only one semantic meaning.

Any vocabulary change requires:
1. protocol version update
2. experiment reset or clear split by version

## Segment Encoding Requirement
### Allowed genotype
`chromosome = [s_0, s_1, ..., s_(N-1)]`

Where:
- `N = num_segments`
- `s_i` is valid segment ID from the active library

### Decoder requirement
`decode(chromosome)` must be deterministic.

Same input chromosome and same library version must produce identical phenotype.

## Shared API Contract
```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

### Constraint output (required keys)
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

### Evaluation output (required keys)
```python
{
  "difficulty_score": float,
  "difficulty_error": float,
  "structural_diversity": float,
  "emptiness": float
}
```

## Constraint Policy
Feasibility is mandatory hard constraint in MVP.

Interpretation:
- infeasible candidates are not valid final outputs
- feasible candidates have strict priority in survivor logic

## Objective Policy
MVP objectives:

1. `difficulty_error` (minimize)
2. `structural_diversity` (maximize)
3. `emptiness` or target-balanced density (project configuration)

Objective semantics are governed by:
- `MARIO_EVALUATION_SPEC_EN.md`

## Responsibility Boundary
### Generation module owner
1. Segment library lifecycle.
2. Decoder implementation.
3. Rendering implementation.
4. Tile-semantic consistency support.

### EA module owner
1. Population generation.
2. Crossover and mutation.
3. Feasible-first selection.
4. Optimization loop and logs.

## Acceptance Gate
The interface is accepted when:

1. API signatures are stable.
2. One full end-to-end run succeeds.
3. Output keys match this specification.
4. Re-run with same seed yields deterministic chain behavior.

## Change Control
Any of the following changes require protocol bump:

1. Tile vocabulary
2. Segment schema
3. Constraint definitions
4. Objective formulas
5. API output keys
