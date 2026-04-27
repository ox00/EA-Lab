# Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization

Bie Xiaofeng, Zhang Dingbang, Wang Xuan

## Abstract
Procedural content generation for platform games requires balancing several competing requirements, including feasibility, difficulty control, structural variation, and readable level pacing. We present a Mario level generation pipeline built around an explicit segment-based genotype, deterministic decoding, hard feasibility constraints, and multi-objective evolutionary search. The baseline search optimizes difficulty error, structural diversity, and emptiness error, and it is later extended with family balance and difficulty curve error to shape higher-level level semantics. We also integrate an AI-seeded initialization path from VGLC-derived segment sequences, together with an adapter layer that normalizes and optionally repairs generated chromosomes before they enter the initial population. The results show that the hard-constrained search pipeline is stable, that semantic objectives materially change the structure of the Pareto frontier, and that repaired AI-seeded initialization becomes usable even though raw seeds remain biased by the training distribution. The final system is presented through an interactive frontier browser with representative renders, constraint-level reachability replay, and lite-physics replay.

## I. Introduction
Procedural content generation (PCG) is a natural application area for evolutionary computation because good game content is rarely defined by a single objective. In a Mario-like platformer, a generated level should be traversable, but it should also maintain non-trivial structure, readable density, and a reasonable progression of local challenge. These goals often conflict. Simple layouts are easier to keep feasible, while richer layouts are more likely to violate traversal and placement constraints. This makes Mario level generation better suited to constrained multi-objective search than to a single scalar optimization target.

This project adopts an explicit search representation. Each level is encoded as a fixed-length chromosome of segment identifiers. The chromosome is decoded deterministically into a tile grid, and a hard feasibility checker determines whether the resulting level is admissible. This design keeps the interface between search, evaluation, and rendering transparent. The search algorithm manipulates only chromosomes, while level geometry, constraint logic, and visualization remain deterministic and reproducible.

On top of this representation, we optimize several soft design objectives. The baseline configuration controls difficulty error, structural diversity, and emptiness error. We then introduce two semantic extensions. Family balance encourages broader use of segment families and discourages local repetition, while difficulty curve error encourages the chromosome to follow a target easy-to-hard progression. Because these goals are not naturally reducible to a single score, we use NSGA-II to preserve a set of non-dominated trade-off solutions rather than collapsing the search into a weighted sum.

The project also includes an AI-seeded initialization line. VGLC Mario levels are approximately matched to the internal segment library and converted into chromosome sequences. An LSTM model is trained on these sequences and used to seed part of the initial population. The generated chromosomes are passed through an adapter layer that normalizes length, filters invalid IDs, and can optionally apply feasibility-aware repair. This means the AI component is a real integrated upstream initializer, while the downstream EA or NSGA-II loop remains responsible for hard feasibility control and trade-off refinement.

The main contribution of the project is therefore not a claim that AI alone generates superior Mario levels. The stronger result is a complete PCG pipeline in which genotype design, hard constraints, multi-objective search, semantic objective design, and final result interpretation work together. The system is supported by an interactive frontier browser and layered replay evidence, which make optimization outputs easier to inspect and explain.

## II. Problem Formulation
We formulate Mario level generation as a hard-constrained multi-objective optimization problem.

### A. Genotype and phenotype
A chromosome is represented as a fixed-length sequence

$$
\mathbf{c} = [s_1, s_2, \ldots, s_n], \quad s_i \in \{0,1,\ldots,17\},
$$

where $s_i$ is a segment identifier drawn from the current library and $n = 8$ by default. Each segment spans 14 columns, so the decoded level width is $14 \times 8 = 112$ tiles.

A deterministic decoder transforms the chromosome into a two-dimensional tile grid,

$$
L = \mathrm{decode}(\mathbf{c}),
$$

by concatenating the corresponding segment templates and then placing the start and goal tiles near the left and right boundaries. The phenotype is therefore a direct spatial realization of the chromosome.

### B. Hard feasibility constraints
A decoded level is feasible only if all of the following conditions hold: the start and goal tiles are present and standable; a traversable route exists from start to goal under the same simplified movement model used in the checker; no ground gap exceeds the jumpable threshold; enemies stand on solid support; pipes form valid columns with legal support below; and placement rules for bricks, question blocks, and coins are respected.

Feasibility acts as a hard gate. Objective values are only compared among feasible individuals, while infeasible individuals are always deprioritized during selection.

### C. Objective functions
Among feasible levels, we optimize a set of soft objectives.

The first objective is difficulty error,

$$
f_{\mathrm{diff}}(L) = |D(L) - D^\star|,
$$

where $D^\star = 0.55$ is the target difficulty. The composite difficulty score is

$$
D(L) = 0.35 \cdot \min(1, 4\rho_{\mathrm{enemy}})
+ 0.30 \cdot r_{\mathrm{gap}}
+ 0.20 \cdot v_{\mathrm{height}}
+ 0.15 \cdot v_{\mathrm{jump}}.
$$

Here $\rho_{\mathrm{enemy}}$ is enemy density, $r_{\mathrm{gap}}$ is normalized gap risk, $v_{\mathrm{height}}$ is normalized height variation, and $v_{\mathrm{jump}}$ is normalized jump-count variation.

The second objective is structural diversity. In the current implementation, it is measured by the ratio of unique row patterns in the decoded tile grid,

$$
\mathrm{div}(L) = \frac{|\mathcal{R}(L)|}{H},
$$

where $\mathcal{R}(L)$ denotes the set of distinct tile rows and $H$ is the map height. Higher values indicate broader structural variation rather than repeated row patterns.

The third objective is emptiness error,

$$
f_{\mathrm{empty}}(L) = |E(L) - E^\star|,
$$

where $E(L)$ is the proportion of empty tiles and $E^\star = 0.45$ is the target emptiness.

Two semantic objectives are introduced in the extended settings. Family balance measures whether segment families are used in a more even and less locally repetitive way across the chromosome. The current implementation combines deviation from per-chromosome family balance with an adjacency penalty for repeated neighboring families, producing a normalized score in $[0,1]$ where higher is better.

Difficulty curve error measures whether the sequence of segment difficulty tiers follows a target progression from easier content to harder content. Let $t_i$ denote the difficulty tier of segment $s_i$, and let $\hat{t}_i$ be the corresponding target tier on a linear curve from 1 to 3. The error is

$$
f_{\mathrm{curve}}(\mathbf{c}) = \frac{1}{n} \sum_{i=1}^{n} |t_i - \hat{t}_i|.
$$

Lower values indicate better alignment with the desired pacing profile.

## III. Method
### A. Overall pipeline
The full system can be summarized as

VGLC data $\rightarrow$ optional AI seed generation $\rightarrow$ chromosome initialization $\rightarrow$ decode $\rightarrow$ hard constraint check $\rightarrow$ objective evaluation $\rightarrow$ NSGA-II search $\rightarrow$ rendering and replay evidence.

The core engine does not depend on AI. A chromosome is initialized either randomly or through the seeded path, decoded into a tile grid, checked for feasibility, evaluated under the active objective set, and then evolved by crossover, mutation, and survivor selection.

### B. Segment library
The segment library currently contains 18 handcrafted templates grouped into interpretable families such as `flat_safe`, `gap_jump`, `stair_climb`, `enemy_pressure`, `reward_relief`, `pipe_pressure`, and `mixed_challenge`. Each segment also carries a difficulty tier used by the pacing objective. This makes each gene semantically meaningful: changing one segment ID changes a visible local structure in the final level.

### C. VGLC extraction and sequence modeling
To support AI-seeded initialization, we use processed Mario levels from VGLC. Each level is sliced into fixed-width segments and approximately matched to the internal segment library. This produces chromosome-like training sequences even though the original tiles and the handcrafted library do not align perfectly.

We then treat chromosome generation as a sequence modeling problem. Segment IDs serve as tokens, and chromosomes serve as short sentences. An LSTM with an embedding layer, two recurrent layers, dropout, and a final projection layer is trained to predict the next segment ID. The model is used only for upstream initialization and does not replace the downstream evolutionary search.

### D. Adapter and feasibility-aware repair
Raw AI outputs are not inserted into the search population directly. They first pass through an adapter that filters invalid segment IDs, trims or pads sequences to the configured chromosome length, and can optionally apply a bounded repair procedure. The repair stage first targets gap-heavy structures when reachability is violated and prefers safer replacement families such as `flat_safe`, `reward_relief`, and `pipe_pressure`. If needed, it then performs a small local replacement search and keeps changes only when constraint violations do not worsen. This adapter is a heuristic bridge between the learned sequence model and the hard-constrained search space.

### E. Evolutionary search
Crossover uses a one-point operator with rate 0.9, and mutation replaces one segment ID with probability 0.2. For single-objective baseline comparison, we also keep a simple EA that collapses the active goals into a scalar objective. For the main experiments, we use NSGA-II. Feasible individuals dominate infeasible ones, and feasible individuals are ranked by non-dominated sorting under the active objective set. Crowding distance is then used to preserve dispersion within each front.

### F. Objective modes
We study the following configurations:

- `core_3obj`: difficulty error + structural diversity + emptiness error.
- `family_4obj`: `core_3obj` + family balance.
- `curve_4obj`: `core_3obj` + difficulty curve error.
- `semantic_5obj`: all five objectives.

The first three modes provide the clearest narrative for the project because they show how the search evolves from basic feasibility-aware optimization to more explicit structural and pacing control.

### G. Interactive frontier browser
To interpret the final results, we build an interactive browser-based visualization layer. It presents representative runs, renders best levels and frontier members, displays their metric values, and provides layered playability evidence. The first evidence layer is a reachability replay that follows the same simplified standable-tile logic as the hard feasibility checker. The second is a lite-physics replay that simulates gravity, jump impulse, collision against solid tiles, and short action labels such as `R`, `RR`, `RJ`, `J`, and `N`. The lite-physics layer is still lighter than full Mario physics, but it provides stronger traversal evidence than a pure tile-level path.

## IV. Experimental Study
### A. Core pipeline validation
We first validate that the genotype-decode-check-evaluate loop is stable. Across the baseline runs, the final feasible ratio reaches 1.0000 for both EA and NSGA-II, indicating that the hard feasibility gate produces a usable search space for optimization rather than eliminating most candidate levels.

### B. EA versus NSGA-II baseline
We compare a single-objective EA baseline with NSGA-II under the same core objective setting. The EA achieves an average best difficulty error of 0.4750, whereas NSGA-II improves this to 0.4333. Structural diversity remains the same at 0.6250, while NSGA-II also achieves slightly lower emptiness error (0.3229 versus 0.3292) and slightly better family balance (0.5611 versus 0.5267). More importantly, NSGA-II produces a non-trivial Pareto frontier with an average final front size of 5.3333, average hypervolume of 0.2524, and average spread of 0.0212. These results justify treating NSGA-II as the main optimizer for the final system.

### C. AI-seeded versus random initialization
We then compare three initialization modes under `core_3obj`: random initialization, raw `ai_seeded`, and `ai_seeded_repaired`. Random initialization achieves average difficulty error 0.4500, structural diversity 0.6250, emptiness error 0.3331, hypervolume 0.2400, and feasible ratio 1.0000. Raw AI seeds underperform, reaching difficulty error 0.4625, emptiness error 0.3477, hypervolume 0.1491, and feasible ratio 0.6667. This is consistent with the skewed segment distribution extracted from VGLC.

Repair changes the result substantially. The `ai_seeded_repaired` mode improves difficulty error to 0.4375, restores feasible ratio to 1.0000, improves family balance to 0.7000, and raises hypervolume to 0.2339. The conclusion is therefore moderate but clear: AI-seeded initialization is genuinely integrated and already usable, but its benefit depends on the quality of the upstream sequence distribution and on adapter-level repair.

### D. Objective progression
The strongest methodological evidence comes from the objective progression runs. In the representative `core_3obj` case, the system reaches difficulty error 0.3750, emptiness error 0.3363, family balance 0.5250, and front spread 0.0299. This provides a reasonable baseline but does not explicitly shape family composition or pacing.

In the representative `family_4obj` case, family balance reaches 1.0000 and the frontier becomes much wider, with front spread 0.1703 and front size 30. This indicates that once family composition is formalized as an objective, the search explores a broader range of structurally distinct solutions.

In the representative `curve_4obj` case, difficulty curve error drops to 0.3929 while emptiness error stays in a similar range at 0.3396. Its front spread is 0.0922, which is lower than the family-oriented case but still much higher than the core baseline. Together, these runs show that objective design changes both frontier geometry and the visible structure of generated levels.

### E. Parameter scan
A small parameter scan further confirms that the system has moved beyond a one-off demo. With population sizes 20 and 30 and mutation rates 0.1 and 0.3, average difficulty error ranges from 0.4167 to 0.4583, average emptiness error ranges from 0.3126 to 0.3543, and average first-front hypervolume ranges from 0.2351 to 0.2575. Population 30 with mutation 0.3 gives the best average difficulty error and the highest hypervolume, while population 30 with mutation 0.1 gives the best emptiness error. This again supports the core message of the project: there is no single universally best configuration, because different settings emphasize different trade-offs.

## V. Discussion
The main strength of the project is that it forms a closed loop from representation to interpretation. The chromosome design makes the search space explicit, the hard constraints keep the generated levels meaningful, the objective framework is extensible, and the browser plus replay system turns optimization outputs into inspectable evidence.

The main limitations are equally clear. First, the segment library still limits the richness of the generated content. Second, the AI-seeded branch inherits the skew of the extracted VGLC data, so raw seeds are often repetitive. Third, the lite-physics replay is still an approximation and should be presented as stronger traversal evidence than the hard constraint checker, not as proof of full Mario gameplay fidelity.

The broader insight is that representation and objective design matter as much as algorithm choice. A better optimizer is useful, but in Mario PCG the structure of the search space and the meaning of the objectives largely determine what kinds of levels can emerge.

## VI. Conclusion
We present a Mario PCG pipeline that combines explicit segment-based representation, hard feasibility constraints, and multi-objective evolutionary search with a real AI-seeded initialization path. The system produces feasible levels, preserves multiple design trade-offs through NSGA-II, and supports semantic control over family composition and pacing through additional objectives.

The experiments show that the hard-constrained search pipeline is stable, that NSGA-II is more appropriate than a single-objective EA for this setting, and that semantic objectives materially change the resulting frontier. They also show that AI-seeded initialization is genuinely integrated into the pipeline, although its performance still depends on upstream data quality and repair. Finally, the frontier browser and replay layers make the final solutions easier to inspect, compare, and present. Taken together, these components establish a solid foundation for future work on richer segment libraries, better upstream data modeling, and stronger playable evaluation.
