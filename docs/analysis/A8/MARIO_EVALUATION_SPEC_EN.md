# Mario Evaluation Specification (EN)

## Purpose
This document defines the evaluation contract for the Mario-like A8 project.

It is intended to keep the following aligned:
- level generation
- constraint checking
- EA / MOEA optimisation
- report and presentation wording

The evaluation pipeline is:

```text
chromosome
-> decode
-> phenotype
-> feasibility check
-> objective evaluation
-> optimisation
```

## Scope
This specification covers four evaluation dimensions:
- `feasibility`
- `difficulty`
- `structural diversity`
- `emptiness`

In the first project version:
- `feasibility` is treated as a hard constraint
- the other three are soft objectives

## 1. Feasibility
### Role
Feasibility is a hard constraint.

Business meaning:
- a level that cannot be meaningfully played should not survive, even if it looks diverse or visually clean

### First-version feasibility rules
The constraint checker should return whether the level is valid under at least these rules:

1. Start area exists and is safe.
2. Goal area exists.
3. Start and goal are both standable.
4. The level contains a traversable path from start to goal under the simplified movement model.
5. No illegal tile overlap exists.
6. Gap width does not exceed the maximum jumpable threshold.
7. Pipes, enemies, blocks, and special tiles follow placement rules.

### Output schema
Recommended format:

```python
{
    "is_feasible": True,
    "start_ok": True,
    "goal_ok": True,
    "reachable": True,
    "illegal_overlap": False,
    "max_gap_ok": True,
}
```

### Violation handling
Recommended policy:
- `feasible-first`

Interpretation:
- feasible individuals always rank above infeasible ones
- infeasible individuals may still be kept temporarily during search, but only for repair pressure or diversity support

## 2. Difficulty
### Role
Difficulty is not treated as "the harder the better".

Instead, optimisation should target:
- closeness to a predefined target difficulty level

Business meaning:
- the team can generate levels for a chosen audience profile such as easy, medium, or hard

### Recommended proxy design
Difficulty should not depend on enemy count alone.

A first proxy should combine:
- enemy density
- average gap width / gap risk
- height variation
- required jump count
- narrow landing count

Suggested example:

```text
difficulty_score =
0.35 * normalized_enemy_density +
0.30 * normalized_gap_risk +
0.20 * normalized_height_variation +
0.15 * normalized_jump_count
```

Then define:

```text
difficulty_error = abs(difficulty_score - target_difficulty)
```

### Objective direction
- minimise `difficulty_error`

### Notes
This makes the metric usable for:
- adaptive content generation
- controlled benchmark generation
- report-ready interpretation

## 3. Structural Diversity
### Role
Structural diversity measures how much internal variation a level contains.

Business meaning:
- prevents levels from becoming repetitive, flat, or visually monotonous
- promotes content variety for player experience

### Recommended first-version signals
Use one or a combination of:
- segment repetition penalty
- row diversity
- local pattern entropy
- unique segment ratio
- repeated motif penalty

### Suggested first implementation
For a segment-sequence genotype, a practical first metric is:

```text
structural_diversity =
0.60 * unique_segment_ratio +
0.40 * row_diversity_score
```

Where:
- `unique_segment_ratio = unique_segments / total_segments`
- `row_diversity_score` can be approximated from row-wise Hamming difference or row uniqueness

### Objective direction
- maximise `structural_diversity`

### Notes
This is a proxy for variation, not a full model of user fun.

## 4. Emptiness
### Role
Emptiness measures how open or cluttered the level is.

Business meaning:
- controls visual simplicity
- helps avoid overly dense or overly empty layouts

### Definition
A first simple version:

```text
emptiness = number_of_empty_tiles / total_tiles
```

### Objective direction
Two options are valid:

1. Maximise `emptiness`
- if the design goal is cleaner and more open levels

2. Match a target emptiness range
- if the design goal is balanced density rather than maximum openness

Recommended first version for coursework:
- optimise toward a target range, or
- explicitly state whether you maximise openness or balance it

### Notes
Do not present emptiness as a direct difficulty metric.
It is a structural style proxy.

## 5. Recommended Objective Set
### First project version
Recommended objective tuple:

```text
(
    minimise difficulty_error,
    maximise structural_diversity,
    maximise or target-match emptiness
)
```

Under:
- feasibility as hard constraint

### Why this set is good
It balances:
- controllability
- structural variety
- visual simplicity

And it is:
- easy to compute
- easy to explain in the report
- aligned with the lecture direction for MOO-PCG

## 6. Evaluation API Contract
Recommended evaluator output:

```python
{
    "difficulty_score": 0.62,
    "difficulty_error": 0.18,
    "structural_diversity": 0.74,
    "emptiness": 0.41,
}
```

The constraint checker should be called before objective use.

Suggested pipeline:

```python
level = decode(chromosome)
constraints = check_constraints(level)

if constraints["is_feasible"]:
    objectives = evaluate(level)
else:
    objectives = None
```

## 7. Reporting Guidance
When writing the report or presentation:

1. Clearly separate:
- hard constraints
- soft objectives

2. Explain business meaning for every metric.

3. Avoid claiming:
- "diversity = fun"
- "emptiness = difficulty"

Instead say:
- these are computable structural proxies used to guide search

4. Show both:
- metric values
- representative generated levels

## 8. Versioning Rule
If any of the following changes, the team should treat it as an evaluation version change:

1. tile vocabulary
2. feasibility rules
3. difficulty proxy formula
4. diversity formula
5. emptiness target or direction

Reason:
- otherwise experiments before and after the change are not directly comparable
