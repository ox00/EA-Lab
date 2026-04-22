# Mario PCG 最终演示说明页

## 1. 文档目的
本文档用于最终课堂演示与组内对齐，说明本项目当前应如何展示、重点看什么、以及三组代表性 case 的业务含义。

本页不讨论实现细节，主要回答三件事：

1. 演示时先看什么
2. 三个代表 case 分别代表什么
3. 老师应如何理解本项目的阶段成果

## 2. 当前项目一句话定义
本项目实现了一个基于 Evolutionary Algorithm / NSGA-II 的 Mario 关卡生成原型系统。

系统输入是 `chromosome`，中间经过 `decode -> constraint check -> evaluate -> evolve`，输出为:

1. 可行关卡文本
2. 渲染后的关卡图片
3. Pareto frontier 候选解
4. 可用于对比展示的 frontier browser

## 3. 建议演示顺序
建议现场按下面顺序演示。

### Step 1. 先说明 pipeline
参考文档:

1. [MARIO_PCG_PIPELINE_DIAGRAM.md](../../docs/analysis/A8/MARIO_PCG_PIPELINE_DIAGRAM.md)
2. [MARIO_EA_INTERFACE_EN.md](../../docs/analysis/A8/MARIO_EA_INTERFACE_EN.md)

建议口径:

`我们没有先上复杂 AI 生成，而是先完成一个可控、可解释、可评估的 Mario PCG MVP。EA 负责在离散 segment 空间里搜索，硬约束保证关卡合法，多目标评价控制难度、结构差异、空间占用率和语义节奏。`

### Step 2. 再打开 frontier browser
浏览器入口:

1. [index.html](../../docs/results/frontier-browser/index.html)

浏览器的作用不是“展示一张图”，而是展示:

1. 不同 objective mode 会导向不同类型的好解
2. Pareto frontier 不是单一最优解，而是一组 trade-off 候选
3. 项目已经具备可解释比较能力，而不只是随机出图

### Step 3. 最后讲三组代表 case
本次最终展示不再铺很多实验，而是集中展示三组最有代表性的 run。

## 4. 三组代表 case 说明

### 4.1 `core_3obj_seed7`
路径:

1. [core_3obj_seed7](../../output/pcg/final_showcase/core_3obj_seed7)

定位:

1. 基线版本
2. 代表最基本的三目标搜索
3. 用来回答“如果只做 difficulty + diversity + emptiness，会得到什么结果”

重点看:

1. `difficulty_error`
2. `structural_diversity`
3. `emptiness_error`
4. frontier 的基本形态

演示意义:

`这是系统的 baseline。它证明最小闭环已经打通，并且能稳定生成可行关卡。`

### 4.2 `family_4obj_seed27`
路径:

1. [family_4obj_seed27](../../output/pcg/final_showcase/family_4obj_seed27)

定位:

1. 结构语义增强版本
2. 把 `family_balance` 升格为正式优化目标
3. 代表“内容家族分布更均衡”的搜索方向

重点看:

1. `family_balance`
2. `first_front_hv`
3. `first_front_spread`
4. `family sequence`

演示意义:

`这一组说明 objective design 会改变最终内容结构。系统不只是生成可行地图，还能通过目标函数塑造地图组成方式。`

### 4.3 `curve_4obj_seed27`
路径:

1. [curve_4obj_seed27](../../output/pcg/final_showcase/curve_4obj_seed27)

定位:

1. 节奏语义增强版本
2. 把 `difficulty_curve_error` 升格为正式优化目标
3. 代表“关卡难度节奏可控”的搜索方向

重点看:

1. `difficulty_curve_error`
2. `difficulty tier sequence`
3. frontier 中不同候选解的节奏差异

演示意义:

`这一组说明系统开始关注关卡节奏，而不仅是局部元素数量。它更接近课程里 PCG + MOO 的核心研究问题。`

## 5. 为什么最终只选这三组做展示
因为这三组刚好构成一条清晰的演化主线:

1. `core_3obj`: 先证明最小系统可运行
2. `family_4obj`: 再证明结构语义可以进入优化
3. `curve_4obj`: 再证明节奏语义也可以进入优化

这样展示的好处是:

1. 逻辑清楚
2. 证据链完整
3. 老师容易看出我们不是只调参数，而是在逐步提升 representation 和 objective design

## 6. `semantic_5obj` 为什么没有放进最终展示主视图
`semantic_5obj` 已经完成实验，但没有作为最终展示主 case。

参考文档:

1. [V33_SEMANTIC_5OBJ_REVIEW_2026-04-22_CN.md](../../docs/analysis/A8/V33_SEMANTIC_5OBJ_REVIEW_2026-04-22_CN.md)

原因很直接:

1. 它是有效的折中方案
2. 但没有形成统治性优势
3. 更适合作为“探索性实验结果”，而不是最终主展示版本

演示口径建议:

`我们做过五目标探索，证明 family semantics 和 pacing semantics 可以同时进入优化；但它的收益主要是折中，而不是全面领先，所以现阶段把它保留为研究记录，不作为主演示 case。`

## 7. 浏览器里每个信息块怎么看
### 7.1 Compare Summary
这里看的是三种 objective mode 的代表性差异。

建议解释方式:

1. `core baseline` 看基础能力
2. `family showcase` 看结构均衡
3. `curve showcase` 看节奏控制

### 7.2 Best Level
这里看的是该 run 当前被选中的代表解。

建议说明:

`它不是唯一答案，而是当前 run 中便于展示的一组代表候选之一。`

### 7.3 Frontier Members
这里看的是 Pareto front 候选。

建议说明:

`多目标优化没有单一正确答案。前沿解的意义是把不同 trade-off 明确摆出来，让设计者能选更合适的关卡。`

### 7.4 Family Sequence / Difficulty Tiers
这两个区域是本项目的关键可解释层。

建议说明:

1. `Family Sequence` 解释结构组成
2. `Difficulty Tiers` 解释节奏变化

这两块能把“objective 在优化什么”讲清楚。

## 8. 当前阶段成果应该如何对老师表述
建议用下面这个口径:

`当前阶段，我们已经完成了一个可运行、可解释、可比较的 Mario PCG 原型。它已经支持硬约束过滤、NSGA-II 多目标搜索、代表性关卡渲染、frontier 可视化和不同 objective mode 的对照实验。现阶段最重要的成果不是把所有目标都调到最好，而是证明 representation、constraint design 和 objective design 会系统性影响最终关卡结构与节奏。`

## 9. 项目演进主线
建议按下面主线汇报:

1. MVP: 打通 `chromosome -> decode -> check -> evaluate`
2. Baseline: 建立 `core_3obj`
3. V3.1: 引入 `family_balance`
4. V3.2: 引入 `difficulty_curve_error`
5. V3.3: 做 `semantic_5obj` 探索，但暂不继续深挖
6. 当前重点: 强化演示层与最终表达质量

## 10. 推荐配套材料
1. [index.html](../../docs/results/frontier-browser/index.html)
2. [REPORT_WORKING_DRAFT.md](../../docs/analysis/A8/REPORT_WORKING_DRAFT.md)
3. [V31_FAMILY_OBJECTIVE_REVIEW_2026-04-21_CN.md](../../docs/analysis/A8/V31_FAMILY_OBJECTIVE_REVIEW_2026-04-21_CN.md)
4. [V32_CURVE_OBJECTIVE_REVIEW_2026-04-22_CN.md](../../docs/analysis/A8/V32_CURVE_OBJECTIVE_REVIEW_2026-04-22_CN.md)
5. [V33_SEMANTIC_5OBJ_REVIEW_2026-04-22_CN.md](../../docs/analysis/A8/V33_SEMANTIC_5OBJ_REVIEW_2026-04-22_CN.md)

## 11. 最终结论
本次最终展示建议聚焦一个核心判断:

`这个项目当前最有价值的成果，不是“生成了一张 Mario 图”，而是已经建立起一套可控的、多目标的、可解释的关卡搜索与展示流程。`

这意味着后续无论继续补:

1. 更丰富的 segment library
2. 更强的可玩性检测
3. 更好的渲染器
4. 更复杂的目标函数

都已经有稳定的工程底座可以接上去。
