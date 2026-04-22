# Mario Alignment One Pager

## Baseline Decision
Project baseline is fixed as:

`Mario-like PCG with explicit segment genotype + hard feasibility constraints + multi-objective EA`

AI-based generation is extension scope after MVP acceptance.

## Pipeline Contract
Mandatory execution chain:

```text
chromosome -> decode -> phenotype -> check_constraints -> evaluate -> selection
```

## Frozen Items (Required)
The following items must remain stable during MVP:

1. Game domain: Mario-like only.
2. Genotype format: segment ID sequence.
3. Map shape constants: height, segment width, segment count.
4. Tile vocabulary and semantics.
5. Segment library schema.
6. Decoder behavior and output format.
7. Hard constraint definitions.
8. Objective set and objective direction.
9. Difficulty proxy formula.
10. Evaluator output schema.

## Role Boundary
Generation side delivers:

1. Segment library.
2. Decode function.
3. Render function.
4. Constraint helper logic tied to tile semantics.

EA side delivers:

1. Population generation.
2. Mutation and crossover.
3. Feasible-first handling.
4. Ranking and survivor selection.
5. Generation logs and representative outputs.

## MVP Acceptance Criteria
MVP is accepted only if all conditions below are met:

1. Reproducible run with fixed seed.
2. At least one feasible level produced and rendered.
3. Constraint report available per evaluated level.
4. Objective values recorded per generation.
5. End-to-end chain runs without manual intervention.

## Immediate Risk Triggers
If any trigger appears, stop and re-align before new coding:

1. Tile meaning changed without version update.
2. Decoder output format changed.
3. Constraint logic changed silently.
4. Objective formulas changed without protocol note.
5. Team members run different evaluation versions.

## Reference Documents
1. Interface CN: [EA-Lab/docs/analysis/A8/MARIO_EA_INTERFACE_CN.md](../../../docs/analysis/A8/MARIO_EA_INTERFACE_CN.md)
2. Interface EN: [EA-Lab/docs/analysis/A8/MARIO_EA_INTERFACE_EN.md](../../../docs/analysis/A8/MARIO_EA_INTERFACE_EN.md)
3. Workflow: [EA-Lab/docs/analysis/A8/MARIO_EA_WORKFLOW.md](../../../docs/analysis/A8/MARIO_EA_WORKFLOW.md)
4. Evaluation spec: [EA-Lab/docs/analysis/A8/MARIO_EVALUATION_SPEC_EN.md](../../../docs/analysis/A8/MARIO_EVALUATION_SPEC_EN.md)
