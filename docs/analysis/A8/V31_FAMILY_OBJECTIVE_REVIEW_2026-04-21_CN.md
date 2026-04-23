# Mario PCG V3.1 阶段分析：`family_balance` 升格为正式 NSGA-II 目标

## 1. 文档目的
本文档记录 `family_balance` 从诊断指标升级为 `NSGA-II` 正式优化目标后的第一轮对照实验结果。

这轮分析只回答一个核心问题：

`把 family_balance 纳入 Pareto objective，究竟换来了什么，牺牲了什么，值不值得保留？`

## 2. 实验设计

### 2.1 对照组
本轮实验只改变 `NSGA-II objective mode`，其余条件保持一致。

模式:

1. `core_3obj`
   - `difficulty_error`
   - `structural_diversity`
   - `emptiness_error`
2. `family_4obj`
   - `difficulty_error`
   - `structural_diversity`
   - `emptiness_error`
   - `family_balance`

### 2.2 固定设置

1. algorithm: `nsga2`
2. seeds: `7, 17, 27`
3. population_size: `30`
4. generations: `12`
5. render_backend: `ascii`

### 2.3 输出目录

1. `core_3obj`: [core_3obj_seed7](../../../output/pcg/v31_compare/core_3obj_seed7)
2. `family_4obj`: [family_4obj_seed7](../../../output/pcg/v31_compare/family_4obj_seed7)

## 3. 平均结果

| mode | avg_difficulty_error | avg_structural_diversity | avg_emptiness_error | avg_difficulty_curve_error | avg_family_balance | avg_first_front_hv | avg_first_front_spread | avg_first_front_size |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| core_3obj | 0.4000 | 0.6250 | 0.3366 | 0.8333 | 0.4450 | 0.2536 | 0.0306 | 7.33 |
| family_4obj | 0.4750 | 0.6250 | 0.3352 | 0.9940 | 0.8000 | 0.3371 | 0.1598 | 28.00 |

## 4. 结果解读

### 4.1 明确得到的收益
`family_4obj` 模式带来了三个非常明确的收益:

1. `avg_family_balance` 从 `0.4450` 提升到 `0.8000`
2. `avg_first_front_hv` 从 `0.2536` 提升到 `0.3371`
3. `avg_first_front_spread` 从 `0.0306` 提升到 `0.1598`

这说明:

1. front 变得更大
2. front 变得更分散
3. 保留下来的解在 family 结构上明显更均衡

从工程和展示角度看，这是一次真实有效的升级。

### 4.2 明确付出的代价
`family_4obj` 同时也带来了两个清楚的代价:

1. `avg_difficulty_error` 从 `0.4000` 变差到 `0.4750`
2. `avg_difficulty_curve_error` 从 `0.8333` 变差到 `0.9940`

这说明:

1. 搜索开始更认真地追求 family mix
2. 但它没有自动学会更好的难度贴合
3. 它也没有自动带来更好的 pacing

换句话说:

`family_balance` 是有效的新目标，但它不是“免费收益”。`

### 4.3 没有明显变化的部分
下列指标几乎没有变化:

1. `structural_diversity`
2. `emptiness_error`

这表明:

1. `family_balance` 和 `structural_diversity` 并不等价
2. 同样地，family mix 变好也不会自动让 emptiness 更接近目标

这进一步说明 `family_balance` 是一个独立有意义的优化维度。

## 5. 单个 seed 的现象

### 5.1 seed 7
`family_4obj` 的代表性最强:

1. `family_balance = 0.95`
2. 但 `difficulty_error = 0.45`

说明:

1. 优化器确实能主动推高 family mix
2. 但它会接受一定的难度偏差来换取结构均衡

### 5.2 seed 27
`family_4obj` 得到:

1. `family_balance = 1.0`
2. `difficulty_error = 0.5`

这说明 `family_balance` 目标已经强到足以明显改变最优解选择。

## 6. 阶段判断

### 6.1 结论一：升级是有效的
如果问题是:

`把 family_balance 升格为正式目标，有没有起作用？`

答案是:

`有，而且作用非常明显。`

### 6.2 结论二：升级不是最终答案
如果问题是:

`升格之后，整体质量是不是全面变好？`

答案是:

`不是。`

它主要改善的是:

1. family 结构均衡
2. Pareto front 覆盖度
3. 展示层的多样性

它没有改善，甚至拉低的是:

1. 难度贴合
2. pacing 贴合

### 6.3 结论三：V3.1 是正确方向，但还不完整
本轮实验说明当前项目正在从:

`语义化观测升级`

走向:

`语义化优化升级`

但目前只完成了一半，因为只有 `family_balance` 被正式纳入优化，而 `difficulty_curve_error` 还没有。

## 7. 对项目的实际意义

### 7.1 工程意义
现在你们可以更有把握地说:

1. representation 不是装饰
2. family-level semantics 可以进入优化目标
3. objective design 会直接改变最终关卡结构

这比“只是做出一些可行关卡”更像一个真正的 EA-PCG 项目。

### 7.2 学术意义
这轮结果很好地支持一个报告论点:

`在 Mario PCG 中，objective set 的变化不仅改变数值结果，还会改变内容结构分布。`

这个论点是有实验依据的。

## 8. 下一步建议

### 8.1 第一优先级
建议下一步直接做:

1. 新增 `pacing_4obj` 或 `semantic_5obj` 试验分支

推荐顺序:

1. 先做 `difficulty_curve_error` 升格实验
2. 再比较:
   - `core_3obj`
   - `family_4obj`
   - `semantic_5obj`

### 8.2 第二优先级
建议同步补内容空间:

1. 增加更多 `tier 2` segment
2. 增加真正的缓冲段和过渡段
3. 降低当前高压 family 的主导性

原因:

如果 content space 本身对 pacing 不友好，即便把 `difficulty_curve_error` 纳入目标，优化器也未必能找到足够好的解。

### 8.3 第三优先级
建议把 `frontier browser` 补两项展示:

1. `family_balance`
2. `objective_mode`

必要时再加:

1. `difficulty tier sequence`

这样展示时可以直观看到:

1. 为什么 `family_4obj` front 更大
2. 为什么它的解看起来更均衡

## 9. 结论
V3.1 的核心结论是:

1. `family_balance` 升格为正式目标后，优化器确实会主动追求更均衡的 family 组合
2. 这样做显著提升了 front coverage 和结构均衡性
3. 但它牺牲了部分难度贴合，并没有自动解决 pacing 问题

因此，当前最合理的判断是:

`family_balance 应该保留，但项目下一步必须继续推进 pacing 目标，否则语义优化会停在“结构更均衡”这一层。`
