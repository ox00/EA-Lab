# Mario Report 修改建议稿（按当前项目真实重心）

## 1. 这份建议稿的目标
这份建议稿不是重写整篇 report，而是把当前 `docs/Mario.pdf` 的重心从

`AI-seeded initialization 主导`

调整为更符合当前项目真实成果的版本：

`explicit genotype + hard constraints + multi-objective EA / NSGA-II + interactive demo`

也就是说，AI 线仍然保留，但不再是整篇报告的唯一主角。

## 2. 当前 report 的主要问题
### 2.1 标题和摘要把 AI 放得过重
当前标题是：

`Mario Level Generation via Multi-Objective Evolutionary Search with Data-Driven Initialization`

这个标题没有错，但会让老师第一反应认为：

`这篇报告的核心贡献是 AI initialization`

而不是：

- controllable representation
- hard feasibility design
- NSGA-II objective progression
- frontier browser
- layered replay evidence

### 2.2 实验部分更像“AI seeded 子线总结”，不是“整个项目总结”
当前实验主要写了：

1. core pipeline validation
2. AI-seeded vs random
3. objective mode progression

这三部分中，第 2 部分占据的叙事权重过高。

### 2.3 最终展示层写到了，但还没有成为正文重点
目前 browser / replay 已进入 report，但还不够突出。

对于课程项目来说，这其实是你们最后非常强的展示层：

- frontier browser
- reachability replay
- lite physics replay
- lite physics action plan

这些内容应该从“补充说明”升级为“最终系统价值的一部分”。

## 3. 建议的标题改法
### 方案 A：最稳
`Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search`

适合强调：

- EA / NSGA-II 主线
- 课程项目最扎实部分

### 方案 B：保留 AI，但降级其主导感
`Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization`

这版更适合当前项目真实状态：

- 主线还是 EA / constraints / MOO
- AI 是扩展能力，而不是整个项目唯一核心

## 4. 建议的摘要改法
### 当前摘要的问题
当前摘要最大的问题不是写错，而是叙事排序偏了。

现在的摘要排序大概是：

1. PCG 很复杂
2. 我们用了 VGLC + LSTM
3. 再接 NSGA-II
4. 再说 browser 和 replay

建议改成：

1. 我们建立了一个 complete Mario PCG pipeline
2. 以 explicit genotype + hard constraints + NSGA-II 为主
3. objective 从 core 3obj 扩展到 family / curve
4. AI seeded init 是额外增强线
5. 最终通过 browser + replay 做可解释展示

### 建议摘要结构
建议摘要按下面 5 句组织：

1. 先定义问题
   - Mario PCG needs feasibility, controllable difficulty, diversity, and semantic pacing.
2. 再讲系统主线
   - We build a hard-constrained multi-objective evolutionary pipeline with explicit segment-based genotype.
3. 再讲扩展能力
   - We additionally integrate AI-seeded initialization from VGLC-derived segment sequences.
4. 再讲实验结论
   - Semantic objectives change frontier structure; repaired AI seeds become usable but do not dominate random initialization.
5. 最后讲最终展示层
   - The final system is presented through an interactive frontier browser with reachability replay and lite-physics replay.

## 5. 建议的正文重心调整
### 5.1 Introduction
当前 Introduction 可以保留大体框架，但建议把 contribution 顺序改成：

1. explicit genotype + deterministic decoder
2. hard feasibility constraints
3. NSGA-II multi-objective progression
4. interactive browser with layered playability evidence
5. AI-seeded initialization as extensible upstream module

这样老师会更容易读出项目主线。

### 5.2 Problem Formulation
这一节整体是清楚的，但建议补 3 个地方：

1. `family balance` 给更正式一点的定义
2. `difficulty curve error` 给更正式一点的定义
3. 明确 `feasible-first` selection policy 的一句话总结

建议加一句：

`Feasibility is treated as a hard gate, while objective values are only compared among feasible individuals.`

### 5.3 Method
Method 现在建议分成“主系统”和“扩展系统”两层：

#### 主系统
1. segment genotype
2. decoder
3. constraints
4. evaluation
5. NSGA-II

#### 扩展系统
1. VGLC extraction
2. LSTM training
3. AI-seeded initialization
4. adapter / repair

这样结构会更真实，也更符合你们项目最后的稳定成果。

### 5.4 Interactive Browser
建议把 browser 这一小节再提升一点存在感。

不要只写“为了方便解释结果”。

建议改成：

`The interactive browser is the final interpretation layer of the project. It turns optimization outputs into comparable, inspectable, and presentation-ready evidence.`

并明确它提供四类价值：

1. objective-mode compare
2. frontier inspection
3. replay evidence
4. plan-level playability summary

## 6. 建议的实验重组
当前实验顺序没错，但建议改成更像“项目主线”：

### Experiment 1. Baseline pipeline validation
保留，说明：

- genotype -> decode -> constraints -> evaluate -> evolve 跑通
- feasible population 可稳定得到

### Experiment 2. Objective progression
把这一节往前提，作为实验主线。

建议重点比较：

1. `core_3obj`
2. `family_4obj`
3. `curve_4obj`
4. （可选一句带过）`semantic_5obj`

这一节是最能代表项目“方法价值”的。

### Experiment 3. AI-seeded initialization
把 AI seeded comparison 放到后面。

这样它更像：

`我们在已经稳定的 EA 主线上，额外接入 AI upstream initialization 做增强实验`

而不是：

`整个项目主要是在讲 AI init`

## 7. 表格与图的建议
### 7.1 保留的图
建议保留：

1. VGLC segment frequency
2. LSTM training / validation loss

因为它们能证明 AI 线不是口头添加。

### 7.2 建议新增的图
至少加 1 张下面这种图，否则最终系统存在感不够：

1. Pipeline overview figure
2. Frontier browser screenshot
3. Lite Physics Replay screenshot with HUD

如果只能加 1 张，我建议优先加：

`frontier browser overall screenshot`

因为它最能体现项目最终交付物。

## 8. Conclusion 建议改法
当前结论写得通顺，但还是偏向：

`AI integration succeeded, even though AI seeds are not yet better`

建议改成更平衡的版本。

### 建议结论重点
1. 主系统已经完成
   - explicit genotype
   - hard constraints
   - multi-objective EA / NSGA-II
2. semantic objectives are meaningful
   - family balance changes structure
   - curve error changes pacing
3. AI seeding is integrated but not dominant yet
4. final demo layer strengthens explainability

### 建议结论句
可以参考：

`The most important outcome of this project is not merely that Mario-like levels can be generated, but that we have established a controllable, hard-constrained, multi-objective, and presentation-ready PCG pipeline. The AI-seeded line is functional and extensible, while the core contribution lies in the explicit search representation, semantic objective progression, and layered visualization of final solutions.`

## 9. 一版更符合当前项目的贡献列表
建议把 contribution 改成下面这组：

1. A complete Mario PCG pipeline with explicit segment genotype, deterministic decoding, and hard feasibility constraints.
2. A progressive NSGA-II objective framework covering baseline difficulty/diversity/density control as well as family balance and difficulty curve shaping.
3. An interactive frontier browser with layered playability evidence, including reachability replay, lite physics replay, and action-plan export.
4. A switchable AI-seeded initialization module that is integrated into the evolutionary pipeline and empirically evaluated against random initialization.

这比当前版本更接近你们真实成果。

## 10. 如果只允许小改，优先改哪 5 个点
如果时间有限，不重写全文，只建议优先改下面 5 个地方：

1. 改标题
2. 改摘要排序
3. 把 Experiment 2 和 Experiment 3 顺序对调
4. 在 Method 里提升 browser / replay 的地位
5. 改 Conclusion 的主结论句

## 11. 对整个 report 的最终判断
### 目前版本
优点：
- 结构清楚
- 论文语气稳定
- AI 线写得完整

不足：
- 对整个项目的总结还不够平衡
- 主重心偏 AI，弱化了 EA/MOO + demo 主线

### 调整后的目标
调整后的理想状态应该是：

`这是一篇以 Mario PCG 的 hard-constrained multi-objective evolutionary pipeline 为主线、以 AI-seeded initialization 为扩展线、以 browser + replay 为最终展示层的课程项目总结。`
