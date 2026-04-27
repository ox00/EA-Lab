# Mario Report 逐节对照修改清单

这份文档用于把 [docs/Mario.pdf](../Mario.pdf) 和新稿做逐节对照，方便直接改最终提交稿。

对照对象：
- 旧稿底稿：[docs/results/report/Mario_extracted_for_edit.md](Mario_extracted_for_edit.md)
- 新的近终稿英文版：[docs/results/report/MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md](MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md)
- 较完整的修订版草稿：[docs/results/report/MARIO_REPORT_REVISED_DRAFT_EN.md](MARIO_REPORT_REVISED_DRAFT_EN.md)

## 1. 总体判断
旧稿的问题不是结构完全错误，而是叙事重心偏了：
- 标题和摘要把 `data-driven / LSTM / AI seed` 放得过前
- 方法上已经有很强的 `explicit genotype + hard constraints + NSGA-II + browser evidence`，但正文没有把这条主线压实
- 实验部分缺少 `EA vs NSGA-II` 这一层，会让老师看不出为什么你们最后必须用 MOO
- `family_balance`、`difficulty_curve_error`、`adapter repair`、`lite physics replay` 定义不够具体
- 最终演示层已经做出来了，但旧稿还把它写成辅助说明，不像正式成果的一部分

所以新稿的处理原则是：
- 保留 AI 线
- 但主叙事改回 `representation -> constraints -> MOO -> evidence`

## 2. 标题
### 旧稿
`Mario Level Generation via Multi-Objective Evolutionary Search with Data-Driven Initialization`

### 新稿
`Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization`

### 为什么要改
旧标题容易让人以为整篇报告的核心贡献是 “data-driven initialization”。

新标题做了两件事：
- 把 `Hard-Constrained` 补出来，明确你们项目最扎实的工程骨架
- 把 `AI-seeded` 保留，但放在后置修饰位置，回到“增强线”而不是“唯一主角”

## 3. Abstract
### 旧稿主要问题
旧摘要整体可读，但句子顺序在引导读者关注：
1. VGLC
2. LSTM
3. AI seeds
4. NSGA-II refinement

这样读者会自然把项目理解成“AI init + NSGA-II 修一修”。

### 新稿处理
新稿摘要改成：
1. 先定义 PCG 的多目标问题
2. 再讲主系统：显式基因型、确定性 decode、硬约束、NSGA-II
3. 再讲 AI-seeded initialization 是 integrated upstream path
4. 再讲实验结论：semantic objectives 改变 frontier；repair 让 AI seeds 可用
5. 最后讲 browser + replay 展示层

### 你们改稿时要注意
摘要里不要让 `LSTM training details` 占篇幅。
摘要应该回答的是：
- 系统是什么
- 为什么它成立
- 你们发现了什么
- 最后怎么展示结果

## 4. Introduction
### 旧稿主要问题
旧稿 Introduction 是通顺的，但 contribution 排序仍然偏向 AI line：
- rule-based 不够
- 以前多是 random init
- 我们做了 VGLC + LSTM + NSGA-II

这会把读者注意力推向数据初始化，而不是整个 PCG formulation。

### 新稿处理
新稿把 Introduction 的叙事顺序改为：
1. Mario PCG 是 constrained multi-objective problem
2. 我们选择 explicit genotype 作为核心表示
3. 我们用 hard constraints 形成 feasibility gate
4. 我们用 NSGA-II 保留 trade-off frontier
5. AI seeded 是真实接入的 upstream initializer
6. browser + replay 是最终 interpretation layer

### 这一节最关键的替换点
旧稿贡献列表建议改成下面这类表达：
- explicit segment-based genotype and deterministic decoding
- hard feasibility constraints for playable search space control
- progressive objective design from core metrics to semantic metrics
- integrated AI-seeded initialization rather than detached AI generation
- interactive frontier browser with layered replay evidence

## 5. Problem Formulation
### 旧稿主要问题
这一节框架基本是对的，但定义偏简，容易让人觉得：
- objective 名字是合理的
- 但数学和业务含义还不够扎实

具体缺口：
- `structural_diversity` 定义过短
- `family_balance` 没有正式写法
- `difficulty_curve_error` 没有正式写法
- `feasibility` 作为 hard gate 没有强调到位

### 新稿处理
新稿在这一节补了四件事：
1. 把 genotype / phenotype 的关系写清楚
2. 把 feasibility 明确写成 hard gate
3. 把 emptiness 改为 `emptiness_error`
4. 把 `family_balance` 与 `difficulty_curve_error` 都写成更正式的定义

### 建议你们最终保留的表达重点
- `The phenotype is a direct spatial realization of the chromosome.`
- `Feasibility acts as a hard gate.`
- `Higher structural diversity reflects broader layout variation rather than repeated row patterns.`
- `Difficulty curve error measures alignment with a target easy-to-hard progression.`

## 6. Method
### 旧稿主要问题
旧稿 Method 的内容其实够多，但结构上仍然像：
`VGLC -> LSTM -> adapter -> NSGA-II`

问题是，这会把 AI pipeline 误写成系统主干。

### 新稿处理
新稿把 Method 改成两层：
- Core search pipeline
- AI-seeded augmentation

更具体地说，新稿把下面这些块压成正式方法链路：
1. segment library
2. decode and constraint checking
3. evaluation
4. genetic operators and NSGA-II
5. VGLC extraction and sequence modeling
6. adapter and feasibility-aware repair
7. frontier browser and replay evidence

### 这一节必须补强的点
#### 6.1 Adapter repair
旧稿只写了 repair 做了什么类型的操作，但不够像正式方法。

新稿把 repair 写成：
- invalid ID filtering
- length normalization
- targeted replacement of gap-heavy segments when reachability fails
- preference for safer families
- bounded local search that avoids worsening violations

这样老师会知道 repair 不是“神奇修复器”，而是一个明确的 heuristic bridge。

#### 6.2 Lite physics replay
旧稿只说有 lite physics replay，但没有最小动作模型定义。

新稿明确写了：
- gravity
- jump impulse
- collision with solid tiles
- short action alphabet `R / RR / RJ / J / N`

这会让 replay 成为一个可解释的 action-level evidence layer，而不是纯演示动画。

## 7. Experimental Study
### 旧稿主要问题
旧稿实验顺序是：
1. pipeline validation
2. AI-seeded vs random
3. objective progression

这个顺序最大的问题是：AI line 占了第二节主实验的位置，而 `EA vs NSGA-II` 根本没正式进入正文。

### 新稿处理
新稿把实验顺序改成：
1. core pipeline validation
2. EA vs NSGA-II baseline
3. AI-seeded vs random initialization
4. objective progression
5. parameter scan

### 为什么这个顺序更好
因为它更符合真实工程逻辑：
- 先证明 pipeline 跑通
- 再证明为什么要用 NSGA-II
- 然后再说明 AI seeded 是怎么接进来的
- 最后再讲 semantic objectives 和参数扫描

### 这一节的重点提醒
#### 7.1 EA vs NSGA-II 必须进正文
这是旧稿里最该补的一项。

它回答老师最核心的问题：
`如果你们最后用了 NSGA-II，那它相比普通 EA 到底带来了什么？`

新稿里已经把现有对照结果压进去了：
- EA difficulty error 0.4750
- NSGA-II difficulty error 0.4333
- NSGA-II 还能给 frontier size / hypervolume / spread

#### 7.2 AI 实验的定位要改
旧稿容易读成“AI is the center”。

新稿把它改成：
- this is an integrated initialization study
- raw AI seeds underperform because of skewed upstream data
- repaired AI seeds become usable

这更客观，也更稳。

#### 7.3 Objective progression 才是方法价值主线
你们最终最有方法味道的成果，其实是：
- `core_3obj`
- `family_4obj`
- `curve_4obj`
- （可选补充）`semantic_5obj`

这才是老师最容易看到 “EA + MOO 设计能力” 的部分。

## 8. Discussion
### 旧稿主要问题
旧稿 Discussion 不是不能用，而是更像项目总结备注，没有完全服务于主结论。

### 新稿处理
新稿把这一节压成三个判断：
- strengths: closed-loop pipeline, extensible objectives, interpretation layer
- limitations: segment library, AI seed skew, lite physics fidelity
- insight: representation and objective design matter as much as optimizer choice

### 为什么这样更适合最终提交
因为老师通常不会细看太长的 Discussion。
这节更适合写成：
- 你们做成了什么
- 还差什么
- 从 EA/PCG 角度学到了什么

## 9. Conclusion
### 旧稿主要问题
旧稿结论还是偏向：
`AI integration worked, but AI seeds are not yet better`

这句话没错，但它不是你们项目最强的总结。

### 新稿处理
新稿的结论主语改成了整个系统：
- explicit segment-based representation
- hard feasibility constraints
- NSGA-II multi-objective trade-off search
- semantic control over family composition and pacing
- AI-seeded initialization as real integrated extension
- frontier browser + replay as final evidence layer

### 最终结论要让老师记住什么
不是 “我们训了一个 LSTM，然后修了一下”。
而是：
`We established a controllable and presentation-ready Mario PCG pipeline.`

## 10. 图表层面的建议
这部分在 `Mario.pdf` 里还不够突出，但对最终提交很重要。

### 推荐保留
- VGLC segment frequency
- LSTM training / validation loss

因为这两张图能证明 AI 线不是口头添加。

### 推荐新增或强烈强调
- pipeline figure
- frontier browser screenshot
- lite physics replay screenshot with HUD
- representative level renders

如果页数有限，优先级是：
1. frontier browser screenshot
2. pipeline figure
3. replay screenshot

## 11. 最终改稿优先级
如果你们现在准备真正改最终提交稿，建议按这个顺序动手：

1. 改标题
2. 替换 Abstract
3. 替换 Introduction
4. 补强 Problem Formulation 中四个关键定义
5. 重写 Method 的结构顺序
6. 把 `EA vs NSGA-II` 正式放进实验
7. 把 objective progression 作为实验主线之一
8. 压缩 Discussion
9. 重写 Conclusion
10. 补最终展示层图示

## 12. 你现在最适合使用的文件
如果你想直接拿一版更接近提交稿的英文正文：
- [docs/results/report/MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md](MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md)

如果你想保留更完整的分析和可扩展写法：
- [docs/results/report/MARIO_REPORT_REVISED_DRAFT_EN.md](MARIO_REPORT_REVISED_DRAFT_EN.md)

如果你想快速定位旧稿哪里要改、为什么改：
- [docs/results/report/MARIO_REPORT_SECTION_BY_SECTION_GUIDE_CN.md](MARIO_REPORT_SECTION_BY_SECTION_GUIDE_CN.md)
