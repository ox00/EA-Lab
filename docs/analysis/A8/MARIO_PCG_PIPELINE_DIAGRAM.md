# Mario PCG Pipeline And Metric Map

## Purpose
This note gives one visual summary of the current Mario-like PCG baseline.

It is intended for:
- team alignment
- report drafting
- presentation explanation

## Pipeline
```mermaid
flowchart LR
    A["random_seed"] --> B["population initialization"]
    B --> C["chromosome<br/>segment ID sequence"]
    C --> D["decode"]
    D --> E["phenotype<br/>tile grid"]
    E --> F["constraint check"]
    E --> G["evaluation"]
    F --> H{"is_feasible?"}
    H -- "no" --> I["penalize or discard"]
    H -- "yes" --> J["objective tuple"]
    G --> J
    J --> K["EA or NSGA-II selection"]
    K --> L["next population"]
    L --> C
    E --> M["render ascii / pygame"]
    J --> N["logs / summary / compare tables"]
```

## Metric Assignment
```mermaid
flowchart TD
    A["chromosome"] --> B["decode"]
    B --> C["level grid"]
    C --> D["feasibility"]
    C --> E["difficulty_score"]
    C --> F["structural_diversity"]
    C --> G["emptiness"]
    E --> H["difficulty_error = |difficulty_score - target_difficulty|"]
    G --> I["emptiness_error = |emptiness - target_emptiness|"]
    D --> J["hard constraint gate"]
    H --> K["optimization inputs"]
    F --> K
    I --> K
    G --> L["reported descriptor"]
```

## Interpretation
1. `random_seed` controls the random search trajectory, not the content semantics of a level.
2. `chromosome` is the EA search object.
3. `phenotype` is the decoded logical level layout.
4. `feasibility` is checked on phenotype and acts as a hard gate.
5. `difficulty_error` and `emptiness_error` are target-matching objectives.
6. `structural_diversity` is the variation objective.
7. `emptiness` is still reported, but no longer optimized directly.

## Algorithm Reading
### EA
- Uses a simplified scalarized survivor rule.
- Tends to compress toward one strong region.

### NSGA-II
- Uses Pareto non-dominated sorting.
- Uses crowding distance to keep the front spread out.
- Better suited for preserving trade-off solutions.
