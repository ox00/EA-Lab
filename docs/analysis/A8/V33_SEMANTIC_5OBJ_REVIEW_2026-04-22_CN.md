# Mario PCG V3.3 阶段分析：`semantic_5obj` 小实验

## 1. 文档目的
本文档记录 `semantic_5obj` 的可行性小实验结果。

这里的 `semantic_5obj` 指:

1. `difficulty_error`
2. `structural_diversity`
3. `emptiness_error`
4. `family_balance`
5. `difficulty_curve_error`

核心问题是:

`同时追求 structure semantics 和 pacing semantics，是否会明显优于前面几种 objective mode？`

## 2. 实验设置

固定设置:

1. algorithm: `nsga2`
2. objective_mode: `semantic_5obj`
3. seeds: `7, 17, 27`
4. population_size: `30`
5. generations: `12`

输出目录:

1. [EA-Lab/output/pcg/v33_semantic_compare/semantic_5obj_seed7](../../../output/pcg/v33_semantic_compare/semantic_5obj_seed7)

## 3. 与前三种模式的比较

| mode | avg_difficulty_error | avg_structural_diversity | avg_emptiness_error | avg_difficulty_curve_error | avg_family_balance | avg_first_front_hv | avg_first_front_spread | avg_first_front_size |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| core_3obj | 0.4000 | 0.6250 | 0.3366 | 0.8333 | 0.4450 | 0.2536 | 0.0306 | 7.33 |
| family_4obj | 0.4750 | 0.6250 | 0.3352 | 0.9940 | 0.8000 | 0.3371 | 0.1598 | 28.00 |
| curve_4obj | 0.4500 | 0.6042 | 0.3517 | 0.6548 | 0.4667 | 0.2167 | 0.1189 | 30.00 |
| semantic_5obj | 0.4917 | 0.6250 | 0.3378 | 0.7381 | 0.5275 | 0.2639 | 0.1384 | 30.00 |

## 4. 结果解读

### 4.1 `semantic_5obj` 的优点
它的优点是“折中”:

1. `difficulty_curve_error = 0.7381`
   - 明显优于 `core_3obj`
   - 也明显优于 `family_4obj`
2. `family_balance = 0.5275`
   - 明显优于 `core_3obj`
   - 明显优于 `curve_4obj`
3. `front_size = 30`
   - 与 `curve_4obj` 一样，front 很大

这说明:

1. 五目标不是完全失效
2. 它确实把 structure 和 pacing 两类语义都部分拉了起来

### 4.2 `semantic_5obj` 的问题
但它的问题同样明显:

1. `difficulty_error = 0.4917`
   - 是四种模式里最差的
2. `emptiness_error = 0.3378`
   - 没有明显优势
3. `HV = 0.2639`
   - 不如 `family_4obj`
4. 没有任何一项表现形成统治性领先

也就是说:

`semantic_5obj` 是一个“折中方案”，但不是一个“最优方案”。`

## 5. 阶段判断

### 5.1 可行，但不值得继续深挖
如果问题是:

`semantic_5obj 能不能跑？`

答案是:

`能。`

如果问题是:

`semantic_5obj 值不值得成为下一阶段主线？`

我的判断是:

`不值得。`

原因:

1. 它没有给出显著更强的综合收益
2. 它只是把多个目标都“拉到中间”
3. 但这不足以支撑继续投入很多时间做更深的 MOO 调参

### 5.2 当前算法层已经够了
到这一步，项目已经有:

1. `core_3obj` baseline
2. `family_4obj` structure objective extension
3. `curve_4obj` pacing objective extension
4. `semantic_5obj` combined-objective feasibility probe

这已经足够形成一条完整的方法演进线。

从课程项目角度看，这一层实验深度已经够支撑:

1. report 方法部分
2. report 实验部分
3. pre / demo 的技术讨论

## 6. 现在最合理的方向

### 6.1 结论
现在最合理的方向不是继续深挖 MOO，而是:

`把重心转向展示层。`

### 6.2 原因

1. 算法层已经有足够多可比较的 objective mode
2. 继续深挖目标函数会进入明显收益递减
3. 你们当前最缺的是“把这些差异直观讲给老师看”的能力

### 6.3 推荐动作
接下来优先级建议:

1. 强化 `pygame` 渲染输出
2. 强化 `frontier browser`
3. 补 `objective_mode / family_sequence / difficulty_tier_sequence` 的可视化
4. 准备一组最能体现三类模式差异的展示 case

## 7. 结论
`semantic_5obj` 的结论很直接:

1. 它证明了 structure semantics 和 pacing semantics 可以同时进入优化
2. 但它没有形成足够强的综合优势
3. 因此它更适合作为“实验探索结果”，而不是后续主路线

最终判断:

`算法层先收住，项目主线切换到展示层与演示质量提升。`
