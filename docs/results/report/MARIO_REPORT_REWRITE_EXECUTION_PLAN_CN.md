# Mario Report 重写执行稿（结合当前项目真实重心）

## 1. 这份文档的目的
这份文档比 `MARIO_REPORT_REVISION_GUIDE_CN.md` 更进一步。

它不是只有 review 建议，而是把后续 report 修改拆成可以直接执行的改法。

目标是：

1. 保留 AI 线，不打击组员信心
2. 但把整篇 report 的主线重新拉回真实项目重心
3. 补齐你指出的关键技术定义、实验链路和最终展示层

## 2. 先回答两个关键判断
### 2.1 `Mario.pdf` 能否导出成可编辑文档
答案：`可以，但建议优先用 Markdown 版本改，再决定是否回写成 LaTeX / Word。`

原因：

- PDF 文本提取可以做到“内容可编辑”
- 但不能保证公式、图表、分页、标题层级完全保真
- 所以 PDF -> DOCX 适合做“内容搬运”，不适合做最终排版母稿

当前我已经额外导出：

1. `docs/results/report/Mario_extracted_for_edit.md`
2. `docs/results/report/Mario_extracted_for_edit.docx`

它们适合作为“修改底稿”，不适合作为最终提交格式。

### 2.2 AI seeded 是否真实接入了关卡生成主线
答案：`是，真实接入了初始化 population。`

代码证据：

- `initial_population_chromosomes()` 在 `cfg.init_mode == "ai_seeded"` 时，不是全随机初始化。
- 它会先按 `ai_seed_ratio` 生成一部分 AI seeded chromosomes。
- 这些 seeded chromosomes 来自 `seeded_chromosome()`。
- `seeded_chromosome()` 会优先尝试 `sample_lstm_seed()`，失败时 fallback 到 `sample_processed_seed()`。
- 如果 `ai_seed_repair` 打开，还会经过 `repair_ai_chromosome()`。
- 之后这些 chromosomes 与随机初始化样本混合、打乱，组成初始 population。
- 后续 EA / NSGA-II 再基于这个 population 做 crossover / mutation / selection。

所以准确说法应该是：

`AI-seeded initialization is a real upstream integration into the initial population, and the subsequent EA / NSGA-II process performs the actual multi-objective search and trade-off refinement on top of that initialized population.`

这和你想要的项目目标是一致的。

## 3. 总体改写原则
你给出的方向我认为是合理的，建议正式定为下面这条主线：

`This report should present a hard-constrained multi-objective Mario PCG system whose core engine is explicit genotype + EA/NSGA-II, while AI-seeded initialization is a real integrated upstream enhancement rather than a detached side experiment.`

换成中文：

`整篇报告要把项目定义为一个以显式基因表示、硬约束和多目标进化搜索为核心的 Mario PCG 系统，其中 AI-seeded initialization 是真实接入的上游增强线，而不是孤立的旁支实验。`

## 4. 标题建议
你给的标题我认为可以直接采用：

`Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization`

原因：

- 保留 AI 线
- 但把主语顺序重新排对
- 先强调 `Hard-Constrained Multi-Objective Evolutionary Search`
- 再说明 `with AI-Seeded Initialization`

这会比原版更平衡。

## 5. 摘要应如何改
### 5.1 摘要目标
摘要不应让人觉得整篇项目主要是在讲 LSTM 是否好用。

摘要应让人读出：

1. 主系统已经完整成立
2. AI 线是真实接入的
3. semantic objectives 是项目方法价值的重要部分
4. 最终还有 browser / replay 作为展示层

### 5.2 建议摘要结构
建议改成 5 句：

1. 问题定义：Mario PCG 需要 feasibility、difficulty、diversity、semantic pacing 等多个目标。
2. 主系统：我们建立了 explicit segment genotype + hard constraints + NSGA-II 的 PCG pipeline。
3. AI 扩展：我们接入了基于 VGLC 的 AI-seeded initialization，并通过 adapter / repair 使其可用于初始化 population。
4. 实验结论：semantic objectives 明显改变 frontier 结构；AI seeds 原始质量有限，但 repair 后达到可用水平。
5. 展示层：最终系统通过 interactive frontier browser 和 layered playability evidence 展示。

## 6. 正文重写建议（逐节）
### 6.1 Introduction
建议把 contribution 顺序改成：

1. explicit genotype and deterministic decode
2. hard feasibility constraints
3. progressive NSGA-II objective design
4. real AI-seeded initialization integration
5. interactive browser and layered replay evidence

注意：这里不是弱化 AI，而是让 AI 回到“扩展模块”的正确层级。

### 6.2 Problem Formulation
这一节总体框架是好的，但你指出的几个技术定义确实需要补强。

建议补：

#### `structural_diversity`
当前定义过简。

建议补一句更正式的描述：

- whether it is based on unique row patterns, segment family transitions, or another structural signature
- why it reflects layout variation rather than mere tile noise

#### `family_balance`
建议加正式定义，例如：

- 以 family frequency distribution 为基础
- 计算其与理想均衡分布之间的偏差
- 或使用 normalized entropy / inverse concentration

#### `difficulty_curve_error`
建议加正式定义，例如：

- 把每个 segment 的 difficulty tier 映射到一条目标曲线
- 用平均绝对误差或平方误差度量偏差

#### `feasible-first`
建议明确写：

`Feasibility is a hard gate. Objective values are only meaningfully compared among feasible individuals.`

### 6.3 Method
建议把 Method 分成两层：

#### Core System
1. segment representation
2. decode
3. constraints
4. evaluation
5. NSGA-II

#### AI-Augmented Initialization
1. VGLC extraction
2. approximate segment matching
3. LSTM sequence generation
4. adapter normalization
5. optional feasibility-aware repair
6. seeded population initialization

这一改法非常关键，因为它会让读者看明白：

`AI 线是 integrated upstream initializer，而不是替代 EA 的主系统。`

### 6.4 Adapter Repair 需要补清楚
你指出这点非常对。

建议明确写 repair 的逻辑，不要只写抽象话：

- remove / replace high-risk gap-heavy segments
- prefer safer families such as `flat_safe`, `reward_relief`, `pipe_pressure`
- repeat local replacement until feasibility improves or budget is exhausted

这样读者才会知道：

`repair` 不是 magic fix，而是一个明确的 heuristic adapter layer。

### 6.5 Lite Physics Replay 需要补一句简洁模型说明
建议补一个短段落，说明它至少包含：

- position and velocity state
- gravity
- jump velocity
- collision against ground / pipe / brick / question blocks
- short action alphabet such as `R / RR / RJ / J / N`

这样它就不只是“有一个 replay”，而是一个可解释的小型 action-level validation layer。

## 7. 实验部分怎么增强
你提的方向我完全同意，而且建议分成“必须增强”和“可增强”两层。

### 7.1 必须增强
#### A. EA vs NSGA-II baseline
这一条非常值得补。

原因：

- 它能证明 MOO 不是装饰
- 它能解释为什么最后要用 NSGA-II 而不是单目标 EA

建议只需要 1 个小表格，不必写太长。

#### B. objective progression
这部分应升级为实验主线。

建议结构：

1. `core_3obj`
2. `family_4obj`
3. `curve_4obj`
4. `semantic_5obj`（定位为 exploratory extension）

老师看完这部分，会更清楚你们的方法价值。

#### C. frontier browser and replay as final evidence layer
当前这一块虽然写到了，但应进入实验/结果表达，而不是只在 Method 尾部轻描淡写。

原因：

- 对课程项目来说，这是最终成果的一部分
- 它提升了结果的可解释性和可信度

### 7.2 可增强
#### parameter scan / hypervolume / spread summary
如果篇幅允许，建议加一个非常短的系统总结表，而不是写很多展开分析。

目的：

- 表明你们确实做过系统调参与指标比较
- 但不让报告变成实验日志

## 8. 图表建议
你提到的“最终展示成果可见度补强”是必须做的。

### 推荐新增图的优先级
#### 第一优先级
`frontier browser screenshot`

原因：
- 它最能说明项目最终交付物
- 也是老师最容易理解的结果图

#### 第二优先级
`pipeline figure`

原因：
- 它能统一 AI / EA / demo 三条线

#### 第三优先级
`replay evidence screenshot`

原因：
- 它能直观补强“可玩性证据不是静态图”

#### 第四优先级
`representative level renders`

原因：
- 对展示友好
- 能配合三组 case 讲 progression

## 9. 建议的实验顺序重排
当前建议改成：

1. Core pipeline validation
2. EA vs NSGA-II baseline
3. Objective progression (`core_3obj -> family_4obj -> curve_4obj -> semantic_5obj`)
4. AI-seeded initialization comparison
5. Final browser / replay evidence

这比原来更接近“整个项目总结”。

## 10. 结论应如何改
结论不要再只围绕：

`AI seeds after repair become competitive`

建议结论重心改成：

1. 完成了一个 hard-constrained multi-objective Mario PCG pipeline
2. semantic objectives can systematically alter structure and pacing
3. AI-seeded initialization is truly integrated and usable, though not dominant yet
4. browser + replay turn optimization results into presentation-ready evidence

## 11. 推荐结论句
建议可以直接用下面这句作为结论核心：

`The most important outcome of this project is not merely that Mario-like levels can be generated, but that we have established a controllable, hard-constrained, multi-objective, and presentation-ready PCG pipeline. AI-seeded initialization is genuinely integrated into the upstream population construction process, while the main contribution lies in the evolutionary search design, semantic objective progression, and layered interpretation of final solutions.`

## 12. 接下来怎么改最有效
如果你们不打算重写 LaTeX 全文，只想用有限时间做最有效修改，建议顺序如下：

1. 改标题
2. 重写摘要
3. 补 Problem Formulation 里的 formal definitions
4. 重组实验顺序
5. 增加 browser / replay / pipeline 图
6. 改结论

## 13. 当前建议的实际文件分工
### 你可以直接用于修改的底稿
1. `docs/results/report/Mario_extracted_for_edit.md`
2. `docs/results/report/Mario_extracted_for_edit.docx`

### 你可以直接用于指导改稿的文档
1. `docs/results/report/MARIO_REPORT_REVISION_GUIDE_CN.md`
2. `docs/results/report/MARIO_REPORT_REWRITE_EXECUTION_PLAN_CN.md`

## 14. 最后判断
你现在的判断是对的：

- 不应弱化 AI 到让同学失去信心
- 但也不能让 report 继续把 AI 写成唯一主轴

更好的平衡是：

`AI is real, integrated, and worth presenting; but the project’s strongest final contribution is the hard-constrained multi-objective Mario PCG pipeline and its explainable demo layer.`
