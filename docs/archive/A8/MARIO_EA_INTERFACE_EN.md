# Mario EA Interface (EN)

## Purpose
This document defines the shared interface between:
- the `level generation / decoding / rendering` side
- the `EA / MOEA optimisation` side

Its purpose is to freeze the representation early so both teammates can work in parallel without redesigning the encoding later.

## Core Idea
The EA does not directly optimise the final visual style.

The EA optimises:
- a searchable `genotype`

The genotype is decoded into:
- a logical Mario level, i.e. the `phenotype`

Then the phenotype is:
- checked by hard constraints
- evaluated by multiple objectives
- optionally rendered for demo and presentation

Pipeline:

```text
genotype
-> decode
-> phenotype
-> hard constraint check
-> multi-objective evaluation
-> EA selection / crossover / mutation
-> rendered output
```

## Recommended Encoding
For the course project, the recommended first version is:
- `segment sequence encoding`

Do not start from:
- full free-form tile mutation over the whole map
- a heavy generative model as the project foundation

Reason:
- smaller and cleaner search space
- easier mutation and crossover
- easier feasibility control
- easier explanation in the report

## Genotype
The genotype is the chromosome searched by the EA.

Example:
```text
[0, 5, 1, 4, 8, 7, 2, 0]
```

Each integer is a `segment ID`.

Business meaning:
- the level is composed of ordered reusable local structures
- each gene selects one segment for one position

## Phenotype
The phenotype is the decoded logical level map.

Example:
```text
16 x 112 tile grid
```

This representation is used by:
- constraint checking
- objective evaluation
- optional rendering

## Rendered Level
The rendered level is the visual presentation of the phenotype.

Important distinction:
- the EA optimises structure
- the renderer visualises that structure

So the same phenotype may have different visual skins without changing the actual level logic.

## Segment Library Example
Suggested segment examples:

```text
S0 = flat ground
S1 = small gap
S2 = stair up
S3 = stair down
S4 = flat ground with enemy
S5 = elevated platform
S6 = question block zone
S7 = pipe obstacle
S8 = wide safe ground
S9 = dense obstacle zone
```

Example chromosome:

```text
[S0, S5, S1, S4, S8, S7, S2, S0]
```

Numerical form:

```text
[0, 5, 1, 4, 8, 7, 2, 0]
```

## Decoder
The decoder concatenates the selected segments from left to right.

Example:

```text
decode([0, 5, 1, 4, 8, 7, 2, 0]) -> 16 x 112 tile map
```

That tile map is the phenotype.

## Tile Vocabulary
Suggested simplified tile vocabulary:
- `0` = empty
- `1` = solid ground
- `2` = breakable brick
- `3` = question block
- `4` = coin
- `5` = enemy
- `6` = pipe
- `7` = start marker
- `8` = goal marker

This vocabulary should be frozen early, because any later change affects:
- decoding
- rendering
- feasibility rules
- objective evaluation

## Shared API
The two teammates should agree on the following functions:

```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

Suggested output format:

```python
check_constraints(level) = {
    "is_feasible": True,
    "start_ok": True,
    "goal_ok": True,
    "reachable": True,
    "illegal_overlap": False,
}

evaluate(level) = {
    "difficulty_error": 0.18,
    "structural_diversity": 0.74,
    "emptiness": 0.41,
}
```

## Hard Constraints
Hard constraints mean immediate rejection.

A level should not enter the valid solution set if it violates them, even if it looks interesting.

Suggested first-version constraints:
1. The start area must be safe and walkable.
2. The goal area must exist.
3. The goal must be reachable.
4. Gap width must not exceed the jump capability threshold.
5. No illegal tile overlap is allowed.
6. Pipes, blocks, and enemies must respect placement rules.

## Objectives
Recommended first version:
1. `difficulty matching`
2. `structural diversity`
3. `emptiness` or `density balance`

Interpretation:
- `difficulty matching`: how close the level is to the target difficulty
- `structural diversity`: how much structural variation the level contains
- `emptiness`: how open or cluttered the level feels

Recommended formulation:
- feasibility as hard constraint
- the 2 or 3 objectives above as soft optimisation targets

## Difficulty Proxy
Difficulty should not be defined only by enemy count.

A better first proxy may combine:
- enemy density
- average gap width
- height variation
- required jump count
- narrow landing count

Example:

```text
difficulty_score =
0.35 * normalized_enemy_density +
0.30 * normalized_gap_risk +
0.20 * normalized_height_variation +
0.15 * normalized_jump_count
```

Then the optimisation target is:
- `difficulty_error = abs(difficulty_score - target_difficulty)`

## EA Operators
### Mutation
Recommended first version:
- randomly choose one chromosome position
- replace the segment ID with another valid segment ID

Example:

```text
[0, 5, 1, 4, 8, 7, 2, 0]
-> mutate position 3
-> [0, 5, 1, 9, 8, 7, 2, 0]
```

### Crossover
Recommended first version:
- one-point crossover
- or two-point crossover

Example:

```text
parent A = [0, 5, 1, 4, 8, 7, 2, 0]
parent B = [8, 8, 3, 2, 6, 1, 4, 5]

child    = [0, 5, 1, 2, 6, 1, 4, 5]
```

## What Must Be Frozen Now
1. Game domain: `Mario-like`
2. Map height
3. Segment width
4. Number of segments per level
5. Tile vocabulary
6. Genotype format: `segment ID sequence`
7. Segment library construction rule
8. Decoder behaviour
9. Hard constraints
10. Objective definitions
11. Difficulty proxy
12. Evaluator output schema

## Team Split
### EA side
- chromosome design review
- mutation / crossover
- selection / ranking
- MOEA loop
- experiment logging

### Generation side
- segment library
- decoder
- renderer
- constraint support
- phenotype-level metric helpers

## Final Recommendation
Before implementing a full MOEA, both sides should first make this chain stable:

```text
chromosome
-> decode
-> level
-> check_constraints
-> evaluate
```

If this chain is stable, the optimisation side and the generation side can proceed independently.
