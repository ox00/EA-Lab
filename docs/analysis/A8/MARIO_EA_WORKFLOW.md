# Mario EA Workflow Specification

## Objective
Define an executable and auditable workflow for MVP delivery.

This workflow is binding for the baseline implementation phase.

## Phase 0: Interface Freeze
Entry criteria:

1. Interface documents reviewed by both role owners.
2. Frozen-item checklist completed.

Exit criteria:

1. Shared API confirmed.
2. Map constants and tile vocabulary fixed.
3. Evaluation protocol version tagged.

## Phase 1: End-to-End Chain Bring-Up
Execution target:

Run one manually selected chromosome through the full chain:

`decode -> check_constraints -> evaluate -> render`

Exit criteria:

1. Decoder returns valid phenotype grid.
2. Constraint checker returns full structured result.
3. Evaluator returns complete objective tuple.
4. Renderer outputs readable level artifact.

## Phase 2: Minimal EA Baseline
Execution target:

Implement and run minimal EA loop over fixed generations.

Required components:

1. Random initialization.
2. Mutation on segment IDs.
3. Crossover on segment sequences.
4. Feasible-first survivor handling.
5. Generation logging.

Exit criteria:

1. Feasible individuals present in final population.
2. Logs contain per-generation feasibility ratio.
3. Logs contain objective values for feasible leaders.

## Phase 3: Multi-Objective Upgrade
Execution target:

Upgrade from single-objective sanity check to multi-objective ranking.

Required scope:

1. Difficulty objective.
2. Diversity objective.
3. Emptiness objective.
4. Feasibility remains hard constraint.

Exit criteria:

1. Multiple non-identical feasible candidates generated.
2. Objective trade-offs observable in recorded outputs.
3. Representative levels exported for review.

## Phase 4: Reporting Artifacts
Required artifacts:

1. Parameter table.
2. Evaluation protocol version.
3. Example feasible levels.
4. Objective and feasibility trend logs.
5. Constraint violation statistics.

Exit criteria:

1. Artifacts are reproducible from repository state.
2. Artifacts match current protocol version.

## Operational Rules
### Rule 1
No algorithm-level extension before end-to-end chain is stable.

### Rule 2
No objective formula update without protocol version increment.

### Rule 3
No silent decoder or tile-vocabulary change during active experiments.

### Rule 4
Infeasible-first ranking is forbidden in MVP baseline.

### Rule 5
All experiment runs must include seed value and generation count.

## Suggested Timeline
1. Day 1-2: Phase 0 + Phase 1.
2. Day 3-4: Phase 2.
3. Day 5-6: Phase 3.
4. Day 7: Phase 4 packaging and review.

## Failure Handling
If feasibility ratio does not improve after baseline iterations:

1. Verify constraint logic consistency.
2. Verify decoder outputs for illegal structure patterns.
3. Lower mutation aggressiveness.
4. Increase safe-segment presence in initialization.
5. Re-run with same seed for deterministic diagnosis.

## Expansion Policy
After MVP acceptance, optional enhancements may be evaluated:

1. AI-based initialization.
2. AI-based repair operator.
3. Learned difficulty estimator.
4. Human preference loop.

All enhancements must preserve:

1. Existing API contract.
2. Existing feasibility checker.
3. Existing evaluation protocol compatibility.
