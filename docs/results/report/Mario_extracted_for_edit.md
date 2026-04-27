# Mario Report Extracted Draft

Source: `docs/Mario.pdf`

Note: This is an extracted editable draft for revision planning. Equation/layout fidelity is limited.

## Page 1

```text
JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 1
Mario Level Generation via Multi-Objective
Evolutionary Search with Data-Driven Initialization
Bie Xiaofeng, Zhang Dingbang, Wang Xuan
Abstract—Procedural Content Generation (PCG) for plat-
former games requires balancing multiple conflicting objectives,
including difficulty control, structural diversity, and playability
guarantees. This paper presents a hybrid PCG system that com-
bines a data-driven initialization module with a multi-objective
evolutionary algorithm (NSGA-II) for Mario-like level genera-
tion. The system extracts segment transition patterns from the
Video Game Level Corpus (VGLC) and trains an LSTM language
model to generate realistic chromosome seeds. These seeds are
then refined by NSGA-II under hard feasibility constraints and
a progressively extended objective set. We demonstrate that the
AI-seeded initialization, after adapter-level repair, can match
random initialization performance while providing a foundation
for future data-quality improvements. The complete pipeline is
visualized through an interactive frontier browser with layered
playability evidence.
Index Terms—Procedural Content Generation, Multi-
Objective Optimization, NSGA-II, LSTM, Mario Level Design
I. INTRODUCTION
P
ROCEDURAL content generation (PCG) plays a central
role in game AI research, particularly for platformer
titles such asSuper Mario Bros.. Automatically generating
levels demands not only playability guarantees but also the
simultaneous optimization of conflicting design objectives,
including difficulty, structural diversity, and layout density.
Rule-based generators often fail to offer controllable trade-offs
among these criteria. Recent studies have applied evolutionary
algorithms to PCG [1]; however, most implementations rely
on purely random initialization, thereby ignoring the distri-
butional patterns embedded in professionally designed game
levels.
In this work, we propose a hybrid framework that bridges
data-driven pattern learning and evolutionary multi-objective
optimization. The framework consists of three stages: (1)
extraction of segment-level chromosome sequences from the
VGLC dataset [2] via approximate matching against a hand-
crafted segment library; (2) training of an LSTM language
model to capture transition regularities among these segments;
and (3) integration of LSTM-generated seeds into an NSGA-
II [3] optimization loop with hard feasibility constraints and
progressively extended objectives.
Our principal contributions are: (i) a complete, reproducible
PCG pipeline spanning data extraction, evolutionary search,
and interactive visualization; (ii) an empirical comparison
between random and AI-seeded initialization strategies; and
All authors are with the Department of Computing and Decision Sciences,
Lingnan University, Hong Kong.
(iii) a layered playability evidence system that combines tile-
level reachability with lite physics replay.
II. PROBLEMFORMULATION
We formulate Mario level generation as a constrained multi-
objective optimization problem.
A. Genotype and Phenotype
Genotype: A chromosome is represented as a fixed-length
sequencec= [s 1, s2, . . . , sn], wheres i ∈ {0,1, . . . ,17}
denotes a segment identifier chosen from our library. Unless
otherwise specified,n= 8.
Phenotype: A deterministic decoderdecode(c)transforms the
chromosome into a two-dimensional tile gridL∈ T H×W ,
whereTis the tile vocabulary{Ground, Brick, Question,
Coin, Enemy, Pipe, Start, Goal}, the grid heightH= 16, and
widthW=segment width×num segments= 14×8 = 112.
B. Hard Feasibility Constraints
A valid level must satisfy the following hard constraints
C(L):
•Start and Goal tiles must be present and standable.
•A traversable path exists from start to goal under sim-
plified movement rules (walking and jumping across a
maximum gap of 3 tiles).
•No ground gap exceeds the jumpable threshold.
•Placement rules for enemies, pipes, and bricks are re-
spected (e.g., enemies must rest on solid ground).
Only levels that meet all constraints are considered feasible.
Infeasible individuals are deprioritized during the selection
phase.
C. Objective Functions
We optimize the following soft objectives, each to be
minimized:
•Difficulty Error:f diff(L) =|D(L)−D target|. The com-
posite difficultyD(L)combines enemy density (weight
0.35), gap risk (0.30), height variation (0.20), and re-
quired jump count (0.15). The default target difficulty is
Dtarget = 0.55.
•Structural Diversity:f div(L) = 1−row diversity(L),
where row diversity is defined as the ratio of unique tile
rows.
•Emptiness Error:f empty(L) =|E(L)−E target|, where
E(L)denotes the proportion of empty tiles. By default,
Etarget = 0.45.
```

## Page 2

```text
JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 2
To further enrich the semantic quality of generated levels,
two supplementary objectives are introduced:
•Family Balance:f fam(L)penalizes over-representation
of any single segment family (e.g.,flat_safe,
gap_jump,enemy_pressure).
•Difficulty Curve Error:f curve(L)measures the deviation
from a prescribed difficulty progression across segments.
Since these objectives are inherently conflicting, we employ
the NSGA-II algorithm [3] to approximate the Pareto front,
thereby preserving a diverse set of trade-off solutions.
III. METHOD
A. System Pipeline
The overall data flow is summarized below:
VGLC Data→Segment Extraction→LSTM
Training→
AI Seed Generation→Adapter/Repair→
NSGA-II Optimization→
Rendering→Interactive Browser
Each stage is detailed in the following subsections.
B. VGLC Data Extraction and Processing
We obtain level data from the Video Game Level Corpus
(VGLC) [2], specifically the processed tile files forSuper
Mario Bros.andSuper Mario Bros. 2 (Japan). Each tile
character (e.g.,Xfor ground,Efor enemy) is mapped to
our internalTileenumeration. Complete levels are sliced
into fixed-width segments consistent with our configuration
(segment width= 14).
Because VGLC segments do not perfectly align with our
hand-crafted library (18 segments), we apply approximate
matching based on Hamming distance with automatic height
alignment (shorter grids are padded with empty tiles). Each
VGLC segment is then assigned to the closest library segment.
Fig. 1. Segment ID frequency distribution extracted from VGLC. Segment
ID 1 (flat ground with a small gap) accounts for 78.5% of the data, consistent
with its foundational role in Mario level design.
Fig. 1 reports the resulting distribution. Segment ID 1
clearly dominates (78.5%, 431/549), reflecting its fundamental
role in Mario level structures. IDs 3 (ascending stairs, 11.7%)
and 2 (ascending staircase, 3.6%) contribute necessary vertical
variation. The skewed distribution further justifies the adoption
of an LSTM to capture non-uniform segment transitions.
C. LSTM Language Model for Segment Sequences
We treat chromosome generation as a language modeling
task: each segment ID is regarded as a token, and a chromo-
some corresponds to a sentence. An LSTM model is trained
to predict the next segment given the preceding sequence.
Architecture: TheSegmentLSTMcomprises an embed-
ding layer (dimension 64), two LSTM layers (hidden dimen-
sion 128), dropout with probability 0.3, and a linear projection
to vocabulary-sized logits.
Training: We minimize cross-entropy loss using the
AdamW optimizer (learning rate10 −3) with a cosine anneal-
ing schedule. The batch size is 32, sequence length is 8, and
we train for 50 epochs. The dataset (37 chromosomes) is split
into 80% training and 20% validation.
Fig. 2. Training and validation loss curves for the LSTM model. After 10
epochs the loss declines sharply; the best validation loss of 0.5256 lies well
below the random baselineln(16)≈2.77. The tight alignment between
curves indicates the absence of overfitting.
Fig. 2 illustrates the convergence behavior. The validation
loss drops from 2.14 to approximately 0.53, substantially lower
than the random baseline ofln(16)≈2.77, confirming that
the model has successfully learned segment transition patterns.
D. AI-Seeded Initialization and Adapter Layer
The trained LSTM generates chromosome sequences au-
toregressively using temperature-controlled sampling (default
τ= 0.8). However, raw outputs may contain invalid segment
IDs or incorrect lengths. An adapter layer is therefore intro-
duced to perform the following operations:
•Length normalization (trimming or padding to exactly
num segments).
•Filtering of out-of-vocabulary IDs and substitution with
safe alternatives.
•Optional feasibility-aware repair that identifies and re-
places high-risk gap combinations.
If the LSTM model is unavailable at runtime, the system
falls back to sampling from the VGLC chromosome distribu-
tion, ensuring uninterrupted execution of the pipeline.
E. NSGA-II Optimization
The main optimization loop follows the standard NSGA-II
framework [3]:
•Initialization: either purely random or AI-seeded.
```

## Page 3

```text
JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 3
•Genetic operators: one-point crossover (rate 0.9) and
segment-level mutation (rate 0.2, randomly replacing one
segment ID).
•Survivor selection: non-dominated sorting with crowd-
ing distance; feasible individuals always dominate infea-
sible ones.
•Termination: a fixed number of generations (10–20).
F . Extended Objective Modes
To study the effect of semantic objectives, we define the
following configurations:
•core_3obj: difficulty error + structural diversity +
emptiness error.
•family_4obj: core 3obj + family balance.
•curve_4obj: core 3obj + difficulty curve error.
A fifth variant (semantic_5obj, combining all five objec-
tives) was explored but retained as auxiliary evidence, since it
showed trade-off benefits without a clear superiority over the
four-objective configurations.
G. Interactive Frontier Browser
To facilitate the interpretation of results, we developed an
interactive browser-based visualization that includes:
•Compare Summary: side-by-side comparison of differ-
ent objective modes.
•Best Level View: the best chromosome rendered as a
level image.
•Frontier Members: ranked Pareto-optimal solutions with
detailed metric breakdowns.
•Layered Replay: a tile-level reachability replay matching
EA constraints, and a lite physics replay with simplified
gravity, collision, and jump mechanics, offering action-
level executability evidence.
IV. EXPERIMENTALSTUDY
A. Experiment 1: Core Pipeline V alidation
We ran the NSGA-II pipeline under three objective con-
figurations with fixed parameters: population size 30, 12
generations, and mutation rate 0.2. All runs produced feasible
final populations, confirming the stability of the pipeline.
B. Experiment 2: AI-Seeded versus Random Initialization
We compared three initialization strategies using NSGA-II
withcore_3obj, population size 20, 10 generations, and
three random seeds (7, 17, 27). The results are summarized in
Table I.
TABLE I
COMPARISON OF INITIALIZATION STRATEGIES(NSGA-II,C O R E_3O B J, 3
SEEDS EACH). HYPERVOLUME(HV)IS COMPUTED ON THE NORMALIZED
FIRST FRONT.
Init Mode Diff. Error Struct. Div. HV Feas. Ratio
random 0.4500 0.6250 0.2400 1.0000
ai seeded 0.4750 0.5938 0.1370 0.6667
ai seeded repaired 0.4583 0.6042 0.2188 1.0000
Key Observations:
1)Raw AI seeds underperform: Theai_seededmode
yields a higher difficulty error (0.4750 vs. 0.4500), lower
diversity (0.5938 vs. 0.6250), and critically, a lower
feasible ratio (0.6667 vs. 1.0000). The hypervolume also
drops from 0.2400 to 0.1370.
2)Adapter repair restores feasibility: The
ai_seeded_repairedconfiguration brings the
feasible ratio back to 1.0000 and raises the hypervolume
to 0.2188, approaching the random baseline.
3)Data skew is the root cause: With segment ID 1
accounting for 78.5% of the training data, pure AI
sampling tends to generate repetitive sequences that
often fail feasibility checks. Repair mitigates this issue
but does not eliminate it.
4)Engineering integration is successful: The AI data line
has become a switchable initialization mode, enabling
direct comparison and paving the way for future data-
level improvements.
C. Experiment 3: Objective Mode Progression
Table II illustrates three representative runs that demonstrate
the effect of adding semantic objectives.
TABLE II
REPRESENTATIVE CASE STUDIES. ALL RUNS USENSGA-IIWITH
POPULATION SIZE30AND12GENERATIONS.
Config Diff. Error Struct. Div. Family Bal. Curve Error
core 3obj (seed 7) 0.375 0.625 0.525 —
family 4obj (seed 27) 0.500 0.625 1.000 —
curve 4obj (seed 27) 0.500 0.625 0.450 0.393
Thefamily_4objrun achieves a perfect family bal-
ance of 1.0, with segments now coveringreward_relief,
gap_jump,enemy_pressure, andpipe_pressure
families. Thecurve_4objrun reduces the difficulty curve
error to 0.393, confirming that the optimizer can effectively
shape difficulty progression. These three cases form a clear
evolutionary path: from baseline feasibility, through structural
control, to pacing control.
V. DISCUSSION
A. Advantages
1)Complete closed-loop system: Every stage from data
extraction to interactive visualization is reproducible
using fixed random seeds.
2)Multi-objective awareness: NSGA-II preserves a di-
verse set of trade-off solutions rather than collapsing to
a single answer.
3)Extensible objective framework: Adding new objec-
tives only requires implementing new evaluation func-
tions; no modifications to the core search algorithm are
needed.
4)Layered playability evidence: The two-tier replay sys-
tem (tile-level reachability plus lite physics) provides
stronger credibility than reachability checks alone.
```

## Page 4

```text
JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 4
B. Limitations
1)Segment library expressiveness: The current library
(18 segments approximated from VGLC) still limits the
richness of the generated levels.
2)AI seed quality: The LSTM reproduces the bias present
in the training data, which restricts its practical utility
at this stage.
3)Lite physics fidelity: Although the replay provides
proof-of-concept collision checking, it does not capture
full Mario mechanics such as item interactions and
enemy AI.
C. Insights
1)Representation matters: The choice of a segment-level
genotype fundamentally shapes the search space. Future
work should prioritize enriching the content library.
2)AI integration is not automatic: The quality of the
learned distribution critically determines whether AI-
seeded initialization helps or hinders optimization.
3)Objective design is itself a design task: Each additional
objective encodes a specific design philosophy into the
optimization process, rather than representing a mere
technical tuning step.
VI. CONCLUSION
We presented a hybrid PCG system for Mario levels that
integrates data-driven AI initialization with multi-objective
evolutionary search. The system successfully extracts segment-
level patterns from VGLC, trains an LSTM model for chromo-
some generation, and seamlessly connects AI-seeded initial-
ization with NSGA-II optimization. Our experiments indicate
that while raw AI seeds do not yet outperform random initial-
ization, adapter-level repair restores competitive performance,
and the engineering integration is fully functional. Future
directions include improving the VGLC-to-library matching
procedure, expanding the segment library with more diverse
families, and incorporating human preference feedback.
REFERENCES
[1] J. Liu, S. Snodgrass, A. Khalifa, S. Risi, G. N. Yannakakis, and
J. Togelius, “Deep learning for procedural content generation,”Neural
Computing and Applications, vol. 33, no. 1, pp. 19–37, 2021.
[2] A. Summerville, S. Snodgrass, M. Guzdial, C. Holmg ˚ard, A. K. Hoover,
A. Isaksen, A. Nealen, and J. Togelius, “The VGLC: The Video Game
Level Corpus,” inProceedings of the 7th Workshop on Procedural Content
Generation, 2016.
[3] K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan, “A fast and elitist
multiobjective genetic algorithm: NSGA-II,”IEEE Transactions on Evo-
lutionary Computation, vol. 6, no. 2, pp. 182–197, 2002.
```
