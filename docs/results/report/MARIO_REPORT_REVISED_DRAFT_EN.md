# Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization

This draft is a structured revision of the current report. It keeps the existing project evidence, but it resets the narrative so that the main line is explicit genotype design, hard constraints, multi-objective search, and final interpretability. The AI-seeded module remains in the paper as a real upstream integration rather than a detached side story.

## Abstract
Procedural content generation for platform games requires more than producing valid layouts. A useful generator must enforce playability, control difficulty, preserve structural variation, and expose the trade-offs among these goals. We present a Mario level generation pipeline built around an explicit segment-based genotype, deterministic decoding, hard feasibility constraints, and multi-objective evolutionary search. The search process uses NSGA-II to optimize difficulty error, structural diversity, and emptiness error, and it is later extended with family balance and difficulty curve error to shape higher-level level semantics. We also integrate an AI-seeded initialization path based on VGLC-derived segment sequences and an adapter layer that normalizes or repairs generated chromosomes before they enter the initial population. The experiments show that the hard-constrained search pipeline is stable, that semantic objectives materially change the shape of the Pareto frontier, and that repaired AI-seeded initialization becomes usable even when raw AI seeds are biased by the training distribution. The final system is presented through an interactive frontier browser with representative level renders, constraint-level reachability replay, and lite-physics replay, which turns optimization outputs into inspectable evidence rather than static screenshots.

## I. Introduction
Procedural content generation is a natural testbed for evolutionary computation because good content is rarely defined by a single criterion. In a Mario-like platformer, a generated level should be traversable, but it should also have readable pacing, non-trivial structure, and enough variation to avoid repetitive layouts. These requirements often conflict. A flat level with few hazards is easy to make feasible, but it is unlikely to be interesting. A dense level with many hazards may appear richer, yet it can easily violate reachability or placement rules. This makes Mario level generation a constrained multi-objective optimization problem rather than a pure prediction problem.

This project approaches that problem through an explicit search representation. A level is encoded as a fixed-length chromosome of segment identifiers, where each identifier selects one handcrafted segment template from a library. The chromosome is decoded deterministically into a tile grid. Hard constraints then decide whether the level is admissible. This design keeps the optimization interface clear: the search algorithm only needs to manipulate chromosomes, while decoding, feasibility checking, and rendering remain deterministic and reproducible.

On this foundation, we use evolutionary search to optimize soft design goals. The baseline objective set contains difficulty error, structural diversity, and emptiness error. We then extend the formulation with family balance, which rewards broader use of segment families, and difficulty curve error, which encourages a more deliberate progression across the chromosome. Because these objectives are not naturally reducible to one score, we use NSGA-II to maintain a frontier of trade-off solutions. This is more appropriate for level design than a single weighted objective because it preserves alternative solutions that differ in structure and pacing.

The project also includes an AI-seeded initialization line. Mario levels from VGLC are approximately matched to the internal segment library, converted into chromosome sequences, and used to train an LSTM language model. At runtime, LSTM outputs are adapted into valid chromosome length, filtered for valid segment IDs, and optionally repaired before entering the initial population. This keeps AI in a concrete and limited role: it contributes search initialization, while the downstream EA or NSGA-II loop remains responsible for feasibility filtering and trade-off optimization.

The contribution of the project is therefore not a claim that AI alone solves Mario PCG. The stronger result is a complete, inspectable, and extensible pipeline. It includes explicit genotype design, deterministic decoding, hard feasibility constraints, progressive multi-objective search, AI-seeded initialization as an integrated extension, and a browser-based interpretation layer with replay evidence. This combination makes the project suitable not only for generation experiments but also for report and presentation settings where the reasoning behind each generated level must be visible.

## II. Problem Formulation
We formulate Mario level generation as a hard-constrained multi-objective optimization problem.

### A. Genotype and Phenotype
A chromosome is a fixed-length sequence

$$
\mathbf{c} = [s_1, s_2, \ldots, s_n], \quad s_i \in \{0,1,\ldots,17\},
$$

where each $s_i$ denotes a segment identifier drawn from the current segment library and $n = 8$ by default. Each segment spans 14 columns, so the decoded level width is $14 \times 8 = 112$ tiles. The phenotype is obtained through a deterministic decoder,

$$
L = \mathrm{decode}(\mathbf{c}),
$$

which concatenates the corresponding segment grids and then inserts the start tile near the left boundary and the goal tile near the right boundary. In this project, genotype and phenotype are therefore tightly linked: the search operates on segment sequences, while the rendered level is a direct spatial realization of that sequence.

### B. Hard Feasibility Constraints
A decoded level is considered feasible only if it satisfies all of the following checks. The start tile and goal tile must exist and be standable. A traversable path must exist from start to goal under the same simplified movement model used in the checker, namely horizontal walking and jumps that cross at most three tiles. The longest ground gap must not exceed the configured jumpable threshold. Enemies must stand on solid support, pipe tiles must appear in valid left-right paired columns with solid support below, and bricks or question blocks must not be placed in invalid rows. If any of these checks fail, the individual is infeasible and is deprioritized in selection.

This feasible-first policy is central to the project. Objective values are computed only for feasible individuals, and infeasible solutions never compete on the same footing as feasible ones. In practice, this means feasibility acts as a hard gate rather than another soft objective.

### C. Objective Functions
Among feasible levels, we optimize several soft objectives.

The first objective is difficulty error,

$$
f_{\mathrm{diff}}(L) = |D(L) - D^\star|,
$$

where $D^\star = 0.55$ is the target difficulty and the composite score is defined as

$$
D(L) = 0.35 \cdot \min(1, 4 \rho_{\mathrm{enemy}})
+ 0.30 \cdot r_{\mathrm{gap}}
+ 0.20 \cdot v_{\mathrm{height}}
+ 0.15 \cdot v_{\mathrm{jump}}.
$$

Here $\rho_{\mathrm{enemy}}$ is enemy density, $r_{\mathrm{gap}}$ is normalized gap risk, $v_{\mathrm{height}}$ is normalized height variation, and $v_{\mathrm{jump}}$ is normalized jump-count variation.

The second objective is structural diversity. In the current implementation, it is measured by unique row patterns in the decoded tile grid,

$$
\mathrm{div}(L) = \frac{|\mathcal{R}(L)|}{H},
$$

where $\mathcal{R}(L)$ is the set of distinct tile rows and $H$ is the map height. Higher values indicate that the level uses a broader range of vertical structures instead of repeating the same row patterns.

The third objective is emptiness error,

$$
f_{\mathrm{empty}}(L) = |E(L) - E^\star|,
$$

where $E(L)$ is the proportion of empty tiles and $E^\star = 0.45$ is the target emptiness. This formulation is more useful than maximizing emptiness directly because both overly dense and overly empty levels are undesirable.

Two semantic objectives are added in later stages. Family balance is computed from the sequence of segment families induced by the chromosome. Let $m$ be the chromosome length and let $n_k$ be the count of family $k$ among the families that appear in the chromosome. The balance term first measures deviation from the per-chromosome expected count $m / K'$, where $K'$ is the number of families that actually appear, and then penalizes long runs of the same family in adjacent positions. In implementation, this yields a normalized score in $[0,1]$, where higher values indicate more even family usage and less local repetition.

Difficulty curve error measures whether segment difficulty tiers follow a desired progression across the chromosome. Let $t_i$ be the difficulty tier of segment $s_i$, and let the target curve increase linearly from tier 1 to tier 3. The error is

$$
f_{\mathrm{curve}}(\mathbf{c}) = \frac{1}{n} \sum_{i=1}^{n} |t_i - \hat{t}_i|,
$$

where $\hat{t}_i$ is the target tier at position $i$. Lower values indicate better alignment with the intended easy-to-hard pacing profile.

## III. Method
### A. Core Search Pipeline
The overall system follows a genotype-to-evidence pipeline:

VGLC data $\rightarrow$ optional AI seed generation $\rightarrow$ chromosome initialization $\rightarrow$ decode $\rightarrow$ hard constraint check $\rightarrow$ objective evaluation $\rightarrow$ NSGA-II search $\rightarrow$ render and replay evidence.

The core engine does not depend on AI. A chromosome is created either randomly or through the seeded initializer. It is decoded into a level grid, checked for feasibility, evaluated on the active objective set, and then evolved through crossover, mutation, and survivor selection.

### B. Segment Library
The segment library currently contains 18 templates grouped into interpretable families such as `flat_safe`, `gap_jump`, `stair_climb`, `enemy_pressure`, `reward_relief`, `pipe_pressure`, and `mixed_challenge`. Each template also carries a difficulty tier used by the pacing objective. This design makes the chromosome semantically meaningful: changing one gene changes one segment, and the resulting structural meaning is visible both to the evaluator and to the final renderer.

### C. Decoding and Constraint Checking
Decoding is deterministic. Each segment ID selects a fixed tile grid, and the full level is obtained by concatenating the segment grids in order. Start and goal tiles are then inserted at fixed boundary positions. Constraint checking uses the decoded level rather than any hidden latent representation. The checker verifies standable start and goal tiles, a jumpable gap limit, simplified reachability, enemy support, pipe validity, and placement rules. This is the operational definition of feasibility used by both EA and NSGA-II.

### D. Evaluation
Evaluation is only applied to feasible levels. The baseline objective set is `core_3obj`, which includes difficulty error, structural diversity, and emptiness error. Two semantic extensions are then introduced. The `family_4obj` mode adds family balance, while `curve_4obj` adds difficulty curve error. A fifth exploratory mode, `semantic_5obj`, combines both semantic objectives with the core three. These modes are not treated as arbitrary ablations. They represent a progression from basic playability-oriented optimization toward more controlled structural and pacing behavior.

### E. Genetic Operators and NSGA-II
Crossover uses a one-point operator with rate 0.9, and mutation replaces one segment ID with probability 0.2. For single-objective baseline comparison, a standard EA collapses the active goals into a scalar objective. For the main experiments, we use NSGA-II. Feasible individuals dominate infeasible ones. Among feasible individuals, non-dominated sorting ranks solutions by Pareto dominance under the active objective set, and crowding distance preserves dispersion within each front. This makes NSGA-II a better fit than a weighted-sum EA for Mario PCG because it keeps multiple good trade-off solutions instead of pushing the search toward one compromise score.

### F. AI-Seeded Initialization
The AI branch begins with VGLC Mario levels. Processed tile maps are sliced into 14-column segments and approximately matched to the internal segment library. This produces chromosome-like training sequences even though the handcrafted library and the raw VGLC tiles are not perfectly aligned. We then train an LSTM language model on these sequences and sample segment IDs autoregressively.

The raw AI outputs are not passed into the optimizer directly. They first go through an adapter that removes invalid IDs, trims or pads the sequence to the exact chromosome length, and optionally applies feasibility-aware repair. The repair rule is intentionally simple. It first tries to replace gap-heavy segments when reachability is violated, and it prefers safer families such as `flat_safe`, `reward_relief`, and `pipe_pressure`. If the chromosome is still infeasible, it performs a bounded local replacement search and keeps changes only when constraint violations do not worsen. This means the adapter is a heuristic bridge between upstream AI outputs and the hard-constrained search space, not a hidden second optimizer.

When `init_mode = ai_seeded`, a fraction of the initial population is generated through this seeded path and the rest is sampled randomly. The whole population is then evolved by the same downstream search algorithm. This makes the AI-seeded setting directly comparable to the random baseline.

### G. Final Interpretation Layer
The final system includes an interactive frontier browser that serves as the interpretation layer of the project. It presents representative runs, exposes frontier members, renders the corresponding levels, and shows their metric values side by side. It also provides two forms of playability evidence. The first is a constraint-level reachability replay, which uses the same standable-tile model and jumpable-gap rule as the hard feasibility checker. The second is a lite-physics replay, which searches over short action labels such as `R`, `RR`, `RJ`, `J`, and `N` under lightweight gravity, jump velocity, and collision rules against solid tiles including pipes, bricks, and question blocks. The lite-physics layer is still simpler than full Mario physics, but it is stronger evidence than tile-level reachability because it respects collision during traversal.

## IV. Experimental Setup
Unless otherwise noted, the search uses chromosomes of length 8, segment width 14, map height 16, population sizes between 20 and 30, crossover rate 0.9, and mutation rate 0.1 or 0.3 depending on the experiment. The target difficulty is 0.55 and the target emptiness is 0.45. We report feasibility ratio, best objective values, first-front size, hypervolume, and front spread when NSGA-II is used.

The report should include the following figure and table assets. Figure 1 should be the pipeline overview that shows the relation among genotype, constraints, objectives, NSGA-II, and browser output. Figure 2 should be the VGLC segment frequency plot. Figure 3 should be the LSTM training and validation loss curves. Figure 4 should be a frontier-browser screenshot. Figure 5 should be a lite-physics replay screenshot with the action HUD visible. Table I should compare initialization modes, Table II should compare EA and NSGA-II, and Table III should summarize representative objective-mode cases.

## V. Results and Discussion
### A. Pipeline Validation and Baseline Comparison
The first result is that the hard-constrained pipeline is stable. Across the baseline comparisons, both EA and NSGA-II reach a best feasible ratio of 1.0000, which confirms that the genotype-decode-check-evaluate loop is functioning as intended. This is an important engineering result because the rest of the project depends on the constraint layer producing a usable feasible search space.

The second result is that NSGA-II is preferable to the single-objective EA baseline for this task. In the baseline comparison, EA reaches an average best difficulty error of 0.4750, whereas NSGA-II improves this to 0.4333. Structural diversity remains the same at 0.6250, but NSGA-II also achieves slightly lower emptiness error at 0.3229 versus 0.3292 and slightly better family balance at 0.5611 versus 0.5267. More importantly, NSGA-II exposes a frontier with an average final size of 5.3333, an average hypervolume of 0.2524, and an average spread of 0.0212. The single-objective EA cannot provide that trade-off structure. This is the practical reason NSGA-II becomes the main algorithm in the final system.

### B. AI-Seeded Initialization
The AI-seeded comparison should be framed as an integrated initialization study rather than the main contribution of the report. Under `core_3obj`, random initialization reaches average difficulty error 0.4500, structural diversity 0.6250, emptiness error 0.3331, and final feasible ratio 1.0000. Raw `ai_seeded` initialization underperforms on several fronts, with difficulty error 0.4625, emptiness error 0.3477, feasible ratio 0.6667, and hypervolume 0.1491. This is consistent with the strong skew in the extracted training distribution.

The repaired setting changes that picture. `ai_seeded_repaired` improves difficulty error to 0.4375, recovers full feasible ratio at 1.0000, improves difficulty curve error to 0.8690 relative to both raw AI seeds and random initialization, and raises hypervolume to 0.2339. These results support a measured conclusion. AI-seeded initialization is already integrated and usable, but its value depends on upstream data quality and on the adapter layer that maps raw model outputs into the constrained chromosome space.

### C. Objective Progression
The clearest evidence for the project's methodological value comes from the objective progression experiments. In the browser summary, the representative `core_3obj` case (`core_3obj_seed7`) reaches difficulty error 0.3750, emptiness error 0.3363, difficulty curve error 1.0000, family balance 0.5250, frontier hypervolume 0.2650, and front spread 0.0299. This case gives a reasonable baseline, but it does not explicitly control higher-level semantic structure.

The `family_4obj` representative case (`family_4obj_seed27`) changes the frontier substantially. It reaches a perfect family-balance score of 1.0000, increases frontier spread to 0.1703, and expands the first front to 30 members. This shows that once family composition is formalized as an objective, the search does not merely tune one metric. It explores a broader set of structurally distinct solutions.

The `curve_4obj` representative case (`curve_4obj_seed27`) emphasizes pacing instead. It reduces difficulty-curve error to 0.3929 while keeping emptiness error in a similar range at 0.3396. Its frontier spread of 0.0922 is lower than the family-oriented run but still much higher than the core baseline, which suggests that pacing control also reshapes the frontier, though in a different way. Together, these cases support the claim that objective design is itself a level-design decision. Different objectives produce different frontier geometries and different types of candidate levels.

An exploratory `semantic_5obj` mode is also available. At the current stage it is better treated as supporting evidence than as the main showcase. It demonstrates that the framework scales to a richer objective set, but the clearest narrative still comes from the progression `core_3obj -> family_4obj -> curve_4obj`.

### D. Parameter Scan
A small parameter scan provides additional evidence that the system has moved beyond a one-off demo. With population sizes 20 and 30 and mutation rates 0.1 and 0.3, the average difficulty error ranges from 0.4167 to 0.4583, the average emptiness error ranges from 0.3126 to 0.3543, and the average first-front hypervolume ranges from 0.2351 to 0.2575. The setting with population 30 and mutation 0.3 gives the best average difficulty error and the highest hypervolume, while population 30 and mutation 0.1 gives the lowest emptiness error. This again supports the broader point of the project: there is no single universally best configuration because different settings emphasize different trade-offs.

## VI. Final Demonstration Layer
The final demonstration layer should be treated as part of the contribution rather than a cosmetic add-on. The frontier browser makes the Pareto frontier visible. It lets a reader compare representative runs, inspect best levels and frontier members, read off objective values, and observe how the active objective mode changes level structure. It also distinguishes two levels of playability evidence.

The first level is constraint-level evidence. The reachability replay uses the same standable-node logic and maximum jumpable gap assumption as the hard feasibility checker. This is the correct visualization of what the EA gate actually certifies.

The second level is lite-physics evidence. The browser replay uses a lightweight actor state with position, velocity, gravity, jump impulse, and collision against solid tiles. An internal planner searches over short action tokens and exports action plans that can be shown in the browser or included in presentation material. This evidence is still not a full game simulation, but it is materially stronger than a pure grid-based path because pipes, walls, bricks, and question blocks can block traversal.

For a course project, this layer matters. Optimization metrics alone do not show whether the resulting levels are interpretable or presentation-ready. The browser and replay system close that gap.

## VII. Limitations
The segment library remains the main bottleneck of content richness. Although the current families are expressive enough to support meaningful optimization and demo cases, the design space is still small compared with real Mario level structure. This also affects the upstream AI line, because approximate matching against a limited handcrafted library compresses the source distribution before learning begins.

The AI-seeded branch is functional but not yet strong. The extracted VGLC sequences are highly imbalanced, and the learned model tends to reproduce that skew. As a result, raw seeded chromosomes are often repetitive and require repair before they become competitive. This is a data-quality issue more than a failure of the evolutionary layer.

The lite-physics replay is intentionally lightweight. It models gravity, jump impulse, and collision with static tiles, but it does not implement full Mario mechanics such as enemy behavior, item collection, acceleration curves, or richer interaction rules. It should therefore be presented as stronger traversal evidence than the hard constraint checker, not as proof of full game-level playability.

## VIII. Conclusion
This project delivers a complete Mario PCG pipeline in which explicit representation, hard feasibility control, multi-objective search, AI-seeded initialization, and browser-based interpretation are integrated into one coherent system. The central result is not that an AI model alone generates superior levels. The central result is that a hard-constrained search pipeline can produce feasible levels, expose meaningful trade-offs, and support semantic control over family composition and pacing.

The experimental evidence supports this conclusion. NSGA-II provides a stronger optimization framework than a single-objective EA because it preserves a frontier of trade-off solutions. Semantic objectives change both level structure and frontier geometry. AI-seeded initialization is genuinely integrated into the search pipeline and becomes practically usable after adapter-level repair, even though the upstream data distribution remains skewed. The final browser and replay layers then make these optimization results visible and defensible.

The most realistic next steps are to enlarge the segment library, improve the VGLC-to-library alignment and sequence modeling quality, and tighten the connection between optimization evidence and playable rendering. Because the current pipeline already has a clear genotype interface, a working constraint gate, stable multi-objective search, and a presentation-ready evidence layer, it provides a solid foundation for those next iterations.
