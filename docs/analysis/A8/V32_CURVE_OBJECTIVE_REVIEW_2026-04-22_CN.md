# Mario PCG V3.2 阶段分析：`difficulty_curve_error` 升格为正式 NSGA-II 目标

## 1. 文档目的
本文档记录 `difficulty_curve_error` 从诊断指标升级为 `NSGA-II` 正式优化目标后的第一轮对照实验结果。

本轮分析的核心问题是:

`如果让优化器正式追求 pacing / difficulty curve，会不会比 family objective 更值得保留？`

## 2. 实验设计

### 2.1 三组 objective mode
本轮统一比较三种模式:

1. `core_3obj`
   - `difficulty_error`
   - `structural_diversity`
   - `emptiness_error`
2. `family_4obj`
   - `difficulty_error`
   - `structural_diversity`
   - `emptiness_error`
   - `family_balance`
3. `curve_4obj`
   - `difficulty_error`
   - `structural_diversity`
   - `emptiness_error`
   - `difficulty_curve_error`

### 2.2 固定设置

1. algorithm: `nsga2`
2. seeds: `7, 17, 27`
3. population_size: `30`
4. generations: `12`
5. render_backend: `ascii`

### 2.3 输出目录

1. `core_3obj`: [output/pcg/v31_compare/core_3obj_seed7](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/output/pcg/v31_compare/core_3obj_seed7)
2. `family_4obj`: [output/pcg/v31_compare/family_4obj_seed7](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/output/pcg/v31_compare/family_4obj_seed7)
3. `curve_4obj`: [output/pcg/v32_curve_compare/curve_4obj_seed7](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/output/pcg/v32_curve_compare/curve_4obj_seed7)

## 3. 平均结果

| mode | avg_difficulty_error | avg_structural_diversity | avg_emptiness_error | avg_difficulty_curve_error | avg_family_balance | avg_first_front_hv | avg_first_front_spread | avg_first_front_size |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| core_3obj | 0.4000 | 0.6250 | 0.3366 | 0.8333 | 0.4450 | 0.2536 | 0.0306 | 7.33 |
| family_4obj | 0.4750 | 0.6250 | 0.3352 | 0.9940 | 0.8000 | 0.3371 | 0.1598 | 28.00 |
| curve_4obj | 0.4500 | 0.6042 | 0.3517 | 0.6548 | 0.4667 | 0.2167 | 0.1189 | 30.00 |

## 4. 结果解读

### 4.1 `curve_4obj` 的直接收益
`curve_4obj` 的核心收益很明确:

1. `avg_difficulty_curve_error` 从 `0.8333` 降到 `0.6548`
2. front 规模从 `7.33` 提升到 `30.00`
3. front spread 从 `0.0306` 提升到 `0.1189`

这说明:

1. 当 pacing 正式进入目标集合时，优化器会认真去追求更平滑的 difficulty tier 序列
2. 它不只是“偶然碰到几个好解”，而是显著改变了整个 Pareto front 结构

### 4.2 `curve_4obj` 的代价
`curve_4obj` 也带来了比较明显的代价:

1. `avg_difficulty_error` 从 `0.4000` 变差到 `0.4500`
2. `avg_emptiness_error` 从 `0.3366` 变差到 `0.3517`
3. `avg_structural_diversity` 从 `0.6250` 降到 `0.6042`
4. `avg_first_front_hv` 从 `0.2536` 降到 `0.2167`

这说明:

1. pacing 目标生效了
2. 但它在当前 content space 下会压缩部分原有目标表现
3. 特别是 emptiness 和 diversity 没有自动被兼顾

### 4.3 与 `family_4obj` 的比较
如果把 `curve_4obj` 与 `family_4obj` 直接比较:

`family_4obj` 更强的地方:

1. `family_balance`
2. `HV`
3. `spread`
4. 展示上的结构均衡性

`curve_4obj` 更强的地方:

1. `difficulty_curve_error`
2. 更接近“关卡节奏控制”这个研究问题

这意味着:

1. `family_4obj` 更像“内容结构型目标”
2. `curve_4obj` 更像“玩法节奏型目标”

两者解决的是不同层面的问题。

## 5. 阶段判断

### 5.1 `difficulty_curve_error` 升格是有效的
如果问题是:

`把 difficulty_curve_error 升格为正式目标，有没有起作用？`

答案是:

`有，而且作用足够明显。`

### 5.2 `curve_4obj` 比 `family_4obj` 更接近课程主题
从 EA / PCG 研究视角看:

1. `family_balance` 更偏向结构组织
2. `difficulty_curve_error` 更直接对应 controllable level design

因此如果你们要强调:

1. 难度控制
2. 节奏设计
3. procedural level pacing

那么 `curve_4obj` 的学术价值更高。

### 5.3 但 `curve_4obj` 还不能独立成为最终版本
原因很直接:

1. 它没有带来更好的 family mix
2. 它让 emptiness 和 diversity 有一定退化
3. 说明当前 content space 还不足以同时支撑 pacing 和 structure 两类目标

换句话说:

`curve_4obj` 是对的方向，但还不是“最终最好版本”。`

## 6. 现阶段三种模式各自的定位

### `core_3obj`
定位:

1. 最稳的 baseline
2. 适合做课程报告中的基线对照

### `family_4obj`
定位:

1. 最适合展示“结构均衡”与 front coverage
2. 最适合前沿解展示和 browser 演示

### `curve_4obj`
定位:

1. 最适合展示“难度节奏目标可以进入优化”
2. 最适合写到 report 的方法改进与实验分析部分

## 7. 下一步方向判断

### 7.1 现在更应该优先做什么
如果只在下面两件事里选一个优先级更高的:

1. 继续优化 MOO
2. 把游戏渲染做得更好看

我的判断是:

`短期优先继续优化 MOO，但只再推进一小步；之后就应该切到展示层。`

原因:

1. 现在已经有三组 objective mode，对报告来说实验层次已经足够有内容
2. 再继续深挖算法会迅速进入收益递减区间
3. 但目前展示层还不能把这些差异直观传达给老师或同学

### 7.2 最合理的顺序
建议顺序:

1. 先做一个 `semantic_5obj` 可行性小实验，确认是否值得继续
2. 如果 5 目标没有明显综合收益，就停止继续深挖 MOO
3. 转而投入:
   - pygame 渲染表现
   - frontier browser 展示增强
   - family / tier / objective mode 可视化

这是更稳的工程路径。

## 8. 结论
V3.2 的核心结论可以概括为:

1. `difficulty_curve_error` 升格为正式目标后，优化器确实开始主动追求更合理的 difficulty tier 节奏
2. 这证明 pacing 可以成为 Mario PCG 的正式优化维度
3. 但它也牺牲了部分其他目标表现，说明当前项目已经进入“目标间真实冲突”的阶段

因此，当前最合理的策略不是无限继续加目标，而是:

`最多再做一轮 semantic_5obj 可行性试验；之后把重点转向更强的展示层，把已经得到的研究结果讲清楚、展示好。`
