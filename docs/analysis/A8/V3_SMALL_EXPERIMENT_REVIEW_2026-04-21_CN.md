# Mario PCG V3 小型实验阶段分析

## 1. 文档目的
本文档记录 `V3 segment semantics + diagnostic metrics` 落地后的第一轮小型实验结果。

目标不是做最终结论，而是回答三个更实际的问题：

1. `V3` 的语义化 segment 设计是否已经真正接入实验链路
2. 新指标 `difficulty_curve_error` 与 `family_balance` 是否已经产生可读信息
3. 当前项目下一步应该优先改“目标函数”，还是优先改“内容空间设计”

## 2. 本轮实验范围

### 2.1 Baseline compare (V3)
输出目录:

1. [EA-Lab/output/pcg/baseline_compare_v3/compare_summary.json](../../../output/pcg/baseline_compare_v3/compare_summary.json)
2. [EA-Lab/output/pcg/baseline_compare_v3/compare_summary.md](../../../output/pcg/baseline_compare_v3/compare_summary.md)

设置:

1. algorithms: `ea`, `nsga2`
2. seeds: `7, 17, 27`
3. generations: `12`
4. population_size: `30`

### 2.2 V3 小型参数扫描
输出目录:

1. [EA-Lab/output/pcg/parameter_scan_v3_small/scan_summary.json](../../../output/pcg/parameter_scan_v3_small/scan_summary.json)
2. [EA-Lab/output/pcg/parameter_scan_v3_small/scan_summary.md](../../../output/pcg/parameter_scan_v3_small/scan_summary.md)

设置:

1. algorithm: `nsga2`
2. population_size: `20, 30`
3. mutation_rate: `0.1, 0.3`
4. seeds: `7, 17, 27`
5. generations: `12`

## 3. 本轮关键结果

### 3.1 EA vs NSGA-II (V3)
平均结果如下:

| algorithm | avg_best_difficulty_error | avg_best_structural_diversity | avg_best_emptiness_error | avg_best_difficulty_curve_error | avg_best_family_balance |
| --- | --- | --- | --- | --- | --- |
| ea | 0.4750 | 0.6250 | 0.3292 | 0.9226 | 0.5267 |
| nsga2 | 0.4333 | 0.6250 | 0.3229 | 0.9107 | 0.5611 |

观察:

1. `NSGA-II` 在当前 V3 版本下整体优于 `EA`
2. 改善最明显的是:
   - `difficulty_error`
   - `emptiness_error`
   - `family_balance`
3. `structural_diversity` 两者持平
4. `difficulty_curve_error` 有轻微改善，但幅度不大

解释:

1. `family_balance` 的提升说明 `NSGA-II` 更容易保留不同结构组合
2. 但 `difficulty_curve_error` 没有显著下降，说明搜索过程并没有主动去追求“前低后高”的节奏
3. 这与当前实现一致，因为 `difficulty_curve_error` 还只是诊断指标，不是优化目标

### 3.2 NSGA-II 小型参数扫描
平均结果如下:

| population_size | mutation_rate | avg_difficulty_error | avg_emptiness_error | avg_difficulty_curve_error | avg_family_balance | avg_first_front_hv | avg_first_front_spread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 0.1 | 0.4250 | 0.3543 | 1.0833 | 0.6478 | 0.2351 | 0.0195 |
| 20 | 0.3 | 0.4583 | 0.3225 | 0.9286 | 0.5278 | 0.2502 | 0.0352 |
| 30 | 0.1 | 0.4500 | 0.3126 | 0.9048 | 0.5475 | 0.2485 | 0.0116 |
| 30 | 0.3 | 0.4167 | 0.3238 | 0.9405 | 0.3917 | 0.2575 | 0.0314 |

观察:

1. `pop=30, mut=0.3` 的 `difficulty_error` 最好
2. `pop=30, mut=0.1` 的 `emptiness_error` 最好
3. `pop=30, mut=0.3` 的 `HV` 与 `spread` 最好
4. `pop=20, mut=0.1` 的 `family_balance` 最好
5. `pop=30, mut=0.1` 的 `difficulty_curve_error` 最低

解释:

1. 更高 `mutation` 仍然更有利于 Pareto 覆盖
2. 但更高 `mutation` 不保证更好的 family 结构平衡
3. `difficulty_curve_error` 与 `family_balance` 和原有目标之间并不总是同向
4. 这说明 V3 新指标提供的是“新增观察维度”，而不是原有指标的重复表达

## 4. 当前阶段判断

### 4.1 已经验证成功的部分
本轮实验可以确认以下几点:

1. `V3 segment semantics` 已经真正进入实验链路
2. `summary / logs / frontier` 已经可以输出语义元信息
3. `difficulty_curve_error` 和 `family_balance` 已经能稳定产出数值
4. 新指标对不同 chromosome 会产生可区分的读数

这意味着:

`V3` 不再只是文档设计，而已经是工程上可运行的协议升级。

### 4.2 当前仍未解决的问题
本轮实验同样暴露出两个关键问题:

1. `difficulty_curve_error` 普遍偏高
2. `family_balance` 波动较大，且容易被“重复高压 family”拉低

这说明:

1. 虽然 segment 已经有 `difficulty_tier`
2. 但现有搜索仍然主要优化旧目标
3. 因此算法没有动力主动学会“节奏曲线”与“family 配比”

换句话说:

`V3 目前更像“语义化观测升级”，还不是“语义化优化升级”。`

## 5. 对项目价值的判断

### 5.1 工程价值
这一轮的工程价值是明确的:

1. 团队接口更清楚了
2. chromosome 不再只是 segment ID 序列，而是带结构语义的关卡表达
3. 输出结果现在可以解释“这一关是由哪些 family 组合出来的”
4. 这为后续展示层、调试和汇报提供了更强支撑

### 5.2 学术价值
这轮实验最大的学术价值在于:

1. 它开始把“representation design”从隐含问题变成显式变量
2. 它证明了新指标并不是旧指标的简单重复
3. 它为下一步讨论“是否把 pacing / family metrics 纳入优化目标”提供了依据

## 6. 下一步建议

### 6.1 第一优先级
建议下一步优先做:

1. 将 `difficulty_curve_error` 或 `family_balance` 之一正式纳入 `NSGA-II` 目标集合

建议顺序:

1. 先纳入 `family_balance`
2. 再考虑 `difficulty_curve_error`

原因:

1. `family_balance` 更稳定
2. 更容易解释
3. 更直接影响“生成内容看起来是不是重复”

### 6.2 第二优先级
建议补一轮 `segment family` 扩展，而不是只调算法参数。

方向:

1. 增加 `flat_safe` 和 `reward_relief` 的中间过渡段
2. 增加真正的 `tier 2` segment
3. 降低当前 library 里 `tier 3` family 的占比

原因:

当前 `difficulty_curve_error` 偏高，不只是算法问题，也有内容空间本身“高压段太多、缓冲段不够”的原因。

### 6.3 第三优先级
在 `frontier browser` 中增加两个展示字段:

1. `family sequence`
2. `difficulty tier sequence`

这样团队就能直接肉眼看出:

1. 某个解为什么 `family_balance` 高或低
2. 某个解为什么 `difficulty_curve_error` 高或低

## 7. 结论
本轮 V3 小型实验的结论可以概括为三句话:

1. `V3` 已经从文档进入可运行工程状态
2. 新语义指标已经有信息量，但还没有真正被优化器利用
3. 下一阶段最值得做的，不是继续盲目调参，而是推进“语义目标正式进入优化”
