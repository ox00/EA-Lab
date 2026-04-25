# Mario PCG 项目汇报 PPT 提纲（CN）

## Slide 1. Title
### 标题
`Mario PCG with Hard Constraints and Multi-Objective Evolutionary Search`

### 建议副标题
`CDS526 A8 Project Final Presentation`

### 这一页讲什么
- 项目主题
- 团队成员
- 一句话定义项目目标

### 建议口径
`我们做的是一个基于 EA / NSGA-II 的 Mario 关卡生成项目。重点不是随机出图，而是建立一套可控、可解释、可比较的 PCG pipeline。`

## Slide 2. Problem and Motivation
### 标题
`Why This Problem`

### 这一页讲什么
- 为什么 Mario PCG 是一个合适的课程项目
- 为什么需要多目标优化
- 为什么需要 hard constraints

### 可放内容
- 关卡生成不是只看“能不能生成”
- 还要同时考虑：
  - feasibility
  - difficulty control
  - diversity
  - pacing / structure

### 建议口径
`如果只追求生成，问题太弱；如果不加约束，结果不可信；如果只有单目标，设计空间表达不够。因此这个题目天然适合用 hard constraints + multi-objective EA 来做。`

## Slide 3. System Pipeline
### 标题
`Pipeline Overview`

### 这一页讲什么
- 整个系统的数据流与模块结构

### 建议图示
- 直接放 pipeline 图
- 或简化为：
  `chromosome -> decode -> phenotype -> constraint check -> evaluate -> evolve -> render -> browser`

### 建议口径
`项目的工程核心是打通这条闭环。这样我们讨论的不是单点算法，而是一套可运行的生成与评估系统。`

## Slide 4. Representation and Constraints
### 标题
`Representation and Feasibility`

### 这一页讲什么
- genotype 是什么
- phenotype 是什么
- hard constraints 做了什么

### 可放内容
- chromosome = segment id sequence
- decode 后得到 level grid
- constraints:
  - start / goal
  - reachable
  - max gap
  - pipe rules
  - enemy rules
  - placement rules

### 建议口径
`representation 决定搜索空间，constraints 决定合法边界。先把这两件事设计清楚，EA 才有意义。`

## Slide 5. Objectives and Search
### 标题
`Objectives and Search Strategy`

### 这一页讲什么
- baseline objectives
- NSGA-II 为什么适合
- 后续如何扩展 objective tuple

### 可放内容
- core objectives:
  - difficulty_error
  - structural_diversity
  - emptiness_error
- extended objectives:
  - family_balance
  - difficulty_curve_error

### 建议口径
`我们不是把所有目标硬合成一个分数，而是使用 NSGA-II 保留 trade-off frontier，这更符合关卡设计这种没有唯一最优解的问题。`

## Slide 6. Experimental Progression
### 标题
`From Baseline to Semantic Objectives`

### 这一页讲什么
- 项目的演进主线

### 可放内容
1. MVP baseline
2. `core_3obj`
3. `family_4obj`
4. `curve_4obj`
5. `semantic_5obj` exploration

### 建议口径
`我们的实验不是平铺参数，而是一条清晰的演进路线：先打通闭环，再逐步把结构语义和节奏语义升格为正式优化目标。`

## Slide 7. Showcase Cases
### 标题
`Three Representative Cases`

### 这一页讲什么
- 为什么最后只展示三组
- 三组分别代表什么

### 可放内容
- `core_3obj_seed7`: baseline capability
- `family_4obj_seed27`: structure balance
- `curve_4obj_seed27`: pacing control

### 建议口径
`这三组 case 刚好构成一条最清晰的证据链：系统可运行、结构可塑形、节奏可控制。`

## Slide 8. Frontier Browser and Replay Evidence
### 标题
`Interactive Browser and Playability Evidence`

### 这一页讲什么
- frontier browser 的作用
- 两层 replay 证据的区别

### 可放内容
- browser screenshot
- Reachability Replay
- Lite Physics Replay
- lite physics action plan export

### 建议口径
`展示层不是单纯美化，而是证据层。我们把可玩性拆成 constraint-level 和 lite-physics-level 两层，提升最终演示的可信度。`

## Slide 9. What We Learned
### 标题
`Engineering and Academic Takeaways`

### 这一页讲什么
- 工程收获
- 学术方法收获

### 可放内容
- representation matters
- constraint design matters
- objective design changes frontier structure
- replay / visualization strengthens explanation

### 建议口径
`这次项目最重要的不是某个数值最好，而是我们证明了 representation、constraint design 和 objective design 会系统性影响最终关卡结构与节奏。`

## Slide 10. Conclusion and Future Work
### 标题
`Conclusion and Next Steps`

### 这一页讲什么
- 当前阶段结论
- 如果继续做，下一步可能是什么

### 可放内容
- current result:
  - complete PCG MVP
  - multi-objective search
  - frontier visualization
  - replay evidence
- future work:
  - richer segment library
  - stronger playability check
  - stronger renderer / playable demo
  - deeper AI seeded integration

### 建议口径
`从课程项目角度，我们已经完成了一个可运行、可解释、可展示的 Mario PCG prototype。后续如果继续深入，重点会是更强的内容空间、更强的可玩性验证，以及更强的展示体验。`
