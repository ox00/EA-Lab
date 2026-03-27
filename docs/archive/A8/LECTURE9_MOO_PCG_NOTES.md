# A8 Lecture 9 Notes: MOO for PCG

## Source
- Lecture file reviewed: `/Users/liuzhicheng/1data/workspace_ln/Term2/CDS526-Optimization/L10/CDS526-lecture9-II.pdf`
- Relevant pages from text extraction:
- `p.6`: `Search for Sokoban Levels with Two_Arch2`
- `p.6`: two-objective demo uses level-based optimisation
- `p.7`: `Representation of Chromosome`
- `p.13`: `Overall Process`

## What The Lecture Changes For Our A8 Plan
The lecture pushes A8 in a more concrete direction:

1. We do not need to start from a heavy generative model.
- The professor's example is multi-objective evolutionary search over game levels.
- That means a valid course project can use `EA + level encoding + fitness design` directly.

2. The optimisation target should be a `level`, not only a model.
- In the lecture demo, the decision variable is the level/chromosome.
- Objectives are defined on generated levels, then MOEA searches a Pareto set.

3. Multi-objective PCG is a strong fit for CDS526.
- This is more aligned with the course than a pure GAN/VAE training project.
- It gives a clearer story: representation -> objectives -> MOEA -> Pareto levels.

## Key Signals From The Lecture
### Sokoban Demo
- The lecture references `Search for Sokoban Levels with Two_Arch2`.
- This is a direct example of using a multi-objective evolutionary algorithm for level generation.

### Objectives Used In The Demo
From the extracted text, two objectives were used:

1. `f1(level)`: proportion of empty tiles
2. `f2(level)`: spatial diversity, measuring how different rows are

This matters because it shows:
- objectives can be simple, structural, and computable
- they do not need to be learned rewards
- diversity can be a first-class optimisation target

### Chromosome Representation
The slide titles explicitly mention:
- `Representation of Chromosome`
- `Level Setups and its Representation`

Even though the PDF text extraction does not recover the figure details, the lecture structure is clear:
- the level has an explicit chromosome encoding
- the chromosome is the searchable genotype
- the rendered level is the phenotype

## Implications For Our A8 Design
### Recommended project framing
Use:
- one game domain
- one explicit chromosome encoding
- two or three hand-crafted objectives
- one MOEA baseline such as `NSGA-II`, `MOEA/D`, or `Two_Arch2`-style reasoning

Avoid starting with:
- cross-game generation
- large latent generative models
- end-to-end deep generation without explicit evolutionary representation

### Recommended game domain
Prefer a small tile-based puzzle/platform game:
- `Sokoban-like` if we want to align closely with the lecture
- `Mario-like` if we want richer visuals and more public resources

Tradeoff:
- Sokoban-like is easier for solvability checking and chromosome explanation
- Mario-like is easier for presentation and public dataset reuse

### Recommended genotype choices
The lecture reinforces that genotype should be an optimisation encoding, not necessarily the final visible map.

Good course-level options:

1. Direct tile encoding
- genotype: flattened tile grid
- phenotype: decoded map
- simplest to explain

2. Segment sequence encoding
- genotype: sequence of segment IDs
- phenotype: level assembled from pre-defined or extracted chunks
- more stable than mutating single tiles

3. Parametric generator encoding
- genotype: generator parameters
- phenotype: map produced by rules
- easiest search space, but less expressive

For our case study, the best compromise is usually:
- `segment sequence encoding` for Mario-like levels
- `direct grid encoding` for Sokoban-like levels

## Practical A8 Pipeline After This Lecture
### Route A: Most aligned with lecture
1. Choose a tile-based game
2. Define chromosome representation
3. Define 2-3 objectives
4. Run MOEA to generate a Pareto set of levels
5. Evaluate playability and diversity

### Route B: Extended version
1. Build a segment library from source levels
2. Encode levels as segment sequences
3. Use MOEA to optimise the sequence
4. Optionally add a learned model later as a repair or initialization module

## Suggested objective set for our A8
If we want to stay close to lecture logic, start with objectives that are cheap to compute:

1. Playability / solvability
- hard constraint or first objective

2. Structural diversity
- row diversity, pattern entropy, segment novelty, repetition penalty

3. Difficulty control
- path length, enemy density, jump count, dead-end count, puzzle push count

Suggested formulation:
- treat solvability as a feasibility condition
- optimise diversity + difficulty matching

## What This Means For Your Two Questions
### Q1: Do we need a large and diverse game package?
Not necessarily.

The lecture example suggests:
- start with one game
- define a usable encoding
- optimise directly in level space

So the source data should mainly support:
- valid tile vocabulary
- reusable structural patterns
- a segment or template library if needed

It does not need to be a huge multi-game corpus.

### Q2: How should genotype be defined?
The lecture strongly supports this interpretation:
- genotype is the chromosome used by the MOEA
- phenotype is the rendered map

For A8, genotype can be:
- tile array
- segment ID sequence
- generator parameter vector

This is exactly the missing conceptual bridge between EA and PCG.

## Recommended Decision For Our Team
If we want the highest course fit:

1. Pick `Mario-like` or `Sokoban-like`
2. Use `segment sequence` or `direct tile grid` as genotype
3. Use `multi-objective EA` as the core method
4. Keep learned generation as optional extension, not the project foundation

## Next Step
Translate this into an implementation memo:
- game choice
- genotype
- phenotype decoder
- objective functions
- mutation/crossover operators
- feasibility check
- evaluation protocol
