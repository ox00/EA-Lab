# 报告集成说明（给负责整合报告的同学）

这份说明的目的不是重复写一遍 report，而是帮助快速理解：我们这轮到底改了什么，为什么这么改，以及你整合报告时应该优先吸收哪些内容。

## 1. 先看哪里
如果你要快速接手报告，请按这个顺序看：

1. [近终稿英文正文](MARIO_REPORT_PASTE_READY_EN-final.md)
2. [更完整的英文修订稿](MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md)
3. [逐节对照修改清单](MARIO_REPORT_SECTION_BY_SECTION_GUIDE_CN.md)
4. [旧稿抽取底稿](Mario_extracted_for_edit.md)
5. [项目可用性说明](MARIO_PROJECT_AVAILABILITY_EN.md)

最关键的一份是第 1 个文件。它已经尽量压成可直接贴回 Word/LaTeX 的正文版本。

## 2. 这轮修改的核心方向

旧稿更像：
- `VGLC -> LSTM -> AI seeds -> NSGA-II refinement`

新稿改成：
- `explicit genotype -> deterministic decode -> hard constraints -> NSGA-II multi-objective search -> browser/replay evidence`
- `AI-seeded initialization` 保留，在“真实接入的上游增强模块”这个位置

一句话总结：
`我们没有弱化 AI，而是把它调整成AI seeded+EA NSGA-II multi-objective search平衡。`

## 3. 为什么要这么改
增强：
1. 有显式基因型表示
2. 有确定性的 genotype -> decode 链路
3. 有 hard feasibility constraints
4. 有 EA vs NSGA-II 的方法对比
5. 有 semantic objectives 的逐步扩展
6. 有 frontier browser + replay 作为最终展示证据层

需要平衡 “LSTM 初始化”+"EA op（也是课程重点）”。

## 4. 这轮新增或补强了哪些关键点
### 4.1 标题重排
新标题：
`Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization`

关键变化：
- 加入 `Hard-Constrained`
- 把 `AI-Seeded Initialization` 放到后置位置

这样保留 AI，同时让主语顺序更符合项目重心。

### 4.2 摘要重写
摘要的顺序已经改为：
1. 问题定义
2. 主系统
3. AI seeded integration
4. 实验结论
5. 最终展示层

旧摘要容易会让人觉得：
`这是一篇 LSTM 初始化 + NSGA-II 修补的报告`

新摘要要让人读出：
`这是一套 hard-constrained multi-objective Mario PCG system，AI 是 integrated upstream enhancement。`

### 4.3 Introduction 重写
Introduction 已经不再从“以前都 random init，所以我们做 data-driven init”切入，而是从：
- Mario PCG 是 constrained multi-objective problem
- 显式基因型为什么重要
- feasibility gate 为什么重要
- NSGA-II 为什么合适
- AI seed 是怎么接入的

这会让老师更快读懂项目工程骨架。

### 4.4 Problem Formulation 补强
这轮把四个技术点补得更正式了：

1. `structural_diversity`
说明它不是随便的“越花越好”，而是结构变化度量。

2. `emptiness_error`
不再直接写成 emptiness，而是对目标值的偏差，这更合理。

3. `family_balance`
从 family usage 的角度正式解释其业务意义：避免单一家族过度堆积。

4. `difficulty_curve_error`
正式解释成：沿 chromosome 的难度 tier 是否符合目标节奏曲线。

另外还明确强调：
`feasibility is a hard gate`

这点很关键，因为它直接决定了报告是不是一个像样的 constrained optimization project。

### 4.5 Method 重组
Method 结构已经改得更清晰：
- Core search pipeline
- AI-seeded augmentation
- Interpretation layer

特别是两块补强：

#### adapter repair
以前写得偏抽象，现在写清楚了：
- filter invalid IDs
- normalize length
- replace gap-heavy segments when reachability fails
- prefer safer families
- bounded local repair

#### lite physics replay
以前更像“有个 replay 动画”，现在写成：
- gravity
- jump impulse
- collision against solid tiles
- action alphabet `R / RR / RJ / J / N`

这会让它更像 action-level evidence，而不是纯演示效果。

## 5. 实验叙事最重要的变化
这是整轮修改里最关键的一点。

### 旧稿问题
旧实验顺序是：
1. pipeline validation
2. AI-seeded vs random
3. objective progression

### 新稿改法
新稿把实验逻辑整理成：
1. core pipeline validation
2. EA vs NSGA-II baseline
3. AI-seeded vs random initialization
4. objective progression
5. parameter scan

### 为什么这样更合理
因为老师最自然会问：
- 你们 pipeline 跑通了吗
- 为什么一定要 NSGA-II
- AI 到底接在什么位置
- semantic objectives 真带来了什么

这个顺序更符合真实的方法论推导。

## 6. 这轮保留 AI，但不“神化 AI”

我们没有把 AI 写弱，也没有否定同学的上游工作。
相反，我们明确保留了三件事：

1. AI-seeded 是真实接入到 initial population 的
2. raw AI seeds 受 upstream data skew 影响，效果有限
3. adapter-level repair 后，AI seeded 变成可用初始化模式

所以正确说法不是：
`AI 不行`

而是：
`AI is already integrated, but its usefulness currently depends on upstream data quality and repair.`

这既真实，也能展示协作成功。

## 7. 最终展示层已经被正式升格
旧稿里 browser / replay 有写到，但不够像正式成果。

现在新稿里已经把它明确写成：
- final interpretation layer
- frontier browser
- constraint-level replay
- lite-physics replay
- action-plan evidence

这意味着最终展示不再只是“加分项”，而是项目结果的一部分。

## 8. 报告里建议加入的外部链接
建议在报告的 `Project Availability` 或结尾加入：

- Demo: [https://ox00.github.io/EA-Lab/](https://ox00.github.io/EA-Lab/)
- Source Code: [https://github.com/ox00/EA-Lab](https://github.com/ox00/EA-Lab)

原因：
- Pages 链接给 TA / Prof 直接看效果
- GitHub 仓库链接给他们看代码、文档、实验结果

两者一起放最完整。

## 9. 你整合时建议直接采用哪些文件
### 最推荐直接吸收 
- [MARIO_REPORT_PASTE_READY_EN-final.md](MARIO_REPORT_PASTE_READY_EN-final.md)

### 如果需要看完整推导和更多可裁剪文本
- [MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md](MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md)
- [MARIO_REPORT_REVISED_DRAFT_EN.md](MARIO_REPORT_REVISED_DRAFT_EN.md)

### 如果要理解“为什么这样改”
- [MARIO_REPORT_SECTION_BY_SECTION_GUIDE_CN.md](MARIO_REPORT_SECTION_BY_SECTION_GUIDE_CN.md)

## 10. 最后一句最重要的提醒
整合最终报告时，请始终保持这个主线：

`This is a hard-constrained multi-objective Mario PCG project with explicit genotype and a real AI-seeded initialization path, rather than an AI generation report with some evolutionary post-processing.`

这句话基本就是整轮改稿的核心判断。
