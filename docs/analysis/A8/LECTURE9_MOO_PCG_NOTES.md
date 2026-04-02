# Lecture 9 Alignment Notes (MOO-PCG)

## Source
Primary lecture source:
- `/Users/liuzhicheng/1data/workspace_ln/Term2/CDS526-Optimization/L10/CDS526-lecture9-II.pdf`

Referenced lecture signals:
1. Sokoban level search with Two_Arch2.
2. Explicit chromosome representation for levels.
3. Multi-objective formulation on structural properties.

## Alignment Objective
This note defines how the lecture guidance constrains the A8 baseline design.

## Constraints Derived from Lecture
### Constraint 1
Baseline is allowed to optimize explicit level encodings directly.  
A heavy AI generator is not required for baseline legitimacy.

### Constraint 2
Decision variables should be level encodings (chromosomes), with clear genotype-to-phenotype mapping.

### Constraint 3
At least two computable structural objectives should be defined and optimized jointly.

### Constraint 4
Feasibility (playability) should be enforced as a gate condition before objective comparison.

## Practical Implication for A8
For MVP, the lecture-aligned path is:

1. Define explicit genotype.
2. Decode to level phenotype.
3. Run hard feasibility checks.
4. Evaluate structural objectives.
5. Run MOEA/EA selection and produce feasible candidate set.

## Non-Implication
Lecture alignment does not require:
1. Cross-game modeling.
2. End-to-end deep generation.
3. Human preference loops in baseline phase.

## Current A8 Decision Consistency
Current project baseline:
- segment-sequence genotype
- hard feasibility gate
- multi-objective evaluation

This is consistent with lecture constraints and suitable as MVP acceptance baseline.

## Follow-Up Rule
Any AI-based generation module must be introduced as extension scope and must preserve:

1. genotype/phenotype interface compatibility
2. existing feasibility policy
3. comparable objective definitions
