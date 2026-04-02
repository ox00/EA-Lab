# A8 Project Baseline Specification

## Project Position
This project adopts a two-stage implementation policy:

1. `MVP baseline` (current mandatory scope): explicit Mario encoding + EA/MOEA search.
2. `AI extension` (optional later scope): AI-based generator or repair module integrated into the same pipeline.

The baseline is the acceptance anchor. AI extension is enhancement scope.

## Mandatory Scope (MVP)
The MVP must implement:

1. Genotype definition.
2. Deterministic decoding from genotype to level phenotype.
3. Feasibility check as hard constraints.
4. Multi-objective evaluation.
5. EA/MOEA search loop.
6. Rendered outputs for inspection and reporting.

The minimum executable chain is:

`chromosome -> decode -> check_constraints -> evaluate -> select`

## Encoding and Search Space
The active baseline encoding is:

- `segment sequence encoding`

Design constraints:

1. Single game domain: Mario-like 2D tile level.
2. Fixed map height and fixed segment width.
3. Stable segment ID library.
4. Stable tile vocabulary with fixed semantics.

This encoding is the collaboration interface between generation and EA modules.

## Constraint Policy
Feasibility is treated as hard constraints in MVP.

A level is invalid if any required constraint is violated.  
Invalid levels are not treated as successful outputs regardless of objective values.

Required constraints are defined in:

- `MARIO_EA_INTERFACE.md`
- `MARIO_EVALUATION_SPEC_EN.md`

## Objective Policy
MVP objective set:

1. `difficulty_error` (minimize)
2. `structural_diversity` (maximize)
3. `emptiness` or `density-balance` (project configuration)

These objectives are structural proxies and must be interpreted as such in reporting.

## Roles and Interfaces
Role separation:

1. Generation side: segment library, decode, render, constraint helpers.
2. EA side: population generation, crossover, mutation, feasible-first handling, selection.

Minimum shared API:

```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

## Deliverables for MVP Milestone
MVP milestone is complete when all items below are delivered:

1. Reproducible run command with fixed seed.
2. Constraint report for generated levels.
3. Objective values per generation.
4. Representative feasible levels in rendered form.
5. Short technical note of parameter settings.

## Non-Goals for MVP
The following are intentionally excluded from MVP acceptance:

1. Cross-game generalization.
2. Human-in-the-loop content preference optimization.
3. Complex AI generator training.
4. Full production-grade game engine integration.

## Change Control Rule
Any change in the following items requires a version bump in evaluation protocol:

1. Tile vocabulary.
2. Segment library schema.
3. Constraint definitions.
4. Objective formulas.
5. Difficulty proxy formula.

This rule prevents mixed and non-comparable experiment results.
