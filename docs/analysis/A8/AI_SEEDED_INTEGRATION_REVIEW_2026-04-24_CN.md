# Mario PCG AI-Seeded Integration Review 2026-04-24

## 1. 文档目的
本文档记录 `AI-generated chromosome seeds` 接入当前 Mario PCG EA pipeline 的第一轮集成结果。

本轮工作的目标不是替代 EA，而是验证下面这个集成命题是否成立：

`AI 先生成更像真实 Mario 分布的 chromosome seed，EA 再负责 feasibility + multi-objective refinement。`

## 2. 本轮集成做了什么
### 2.1 新增能力
本轮新增了三层能力：

1. `ai_seeded` 初始化模式
2. `AI chromosome -> fixed-length chromosome` 适配器
3. `random_init vs ai_seeded_init` 最小对照实验脚本

### 2.2 接口位置
核心实现位置：

1. [src/ea_lab/pcg/ai_seed.py](../../../src/ea_lab/pcg/ai_seed.py)
2. [src/ea_lab/pcg/ea.py](../../../src/ea_lab/pcg/ea.py)
3. [src/ea_lab/pcg/nsga2.py](../../../src/ea_lab/pcg/nsga2.py)
4. [src/ea_lab/pcg/demo.py](../../../src/ea_lab/pcg/demo.py)
5. [scripts/run-ai-seeded-compare.py](../../../scripts/run-ai-seeded-compare.py)

## 3. 集成策略
### 3.1 为什么不是让 AI 直接替代 EA
当前项目主线仍然是：

`chromosome -> decode -> constraint check -> evaluate -> EA/NSGA-II`

因此 AI 更合理的角色不是“直接输出最终关卡”，而是：

1. 提供更接近真实关卡分布的初始 chromosome
2. 为 EA 提供更有结构先验的 seed population
3. 让 EA 在可行性和多目标约束下继续优化

### 3.2 当前适配器怎么做
当前适配器逻辑是：

1. 优先加载 `models/lstm_generator.pt`
2. 用 LSTM 从真实 VGLC 近似染色体分布中采样新的 segment sequence
3. 将生成序列映射为当前项目可接受的 `segment ID sequence`
4. 对长度做 `trim / sliding window / pad`
5. 最终输出固定长度 `cfg.num_segments` 的 chromosome

### 3.3 回退机制
如果 LSTM 加载或生成失败，则自动回退到：

1. 从 `vglc_chromosomes_approx.json` 中抽样
2. 再走同样的适配逻辑

这保证 `ai_seeded` 模式不会因为模型不可用而中断整个 EA pipeline。

## 4. 实验设计
### 4.1 对照目标
本轮只回答一个问题：

`AI seed initialization 相比 random initialization，是否已经对当前 PCG 搜索带来可观察收益？`

### 4.2 固定设置
1. algorithm: `nsga2`
2. objective_mode: `core_3obj`
3. population_size: `20`
4. generations: `10`
5. mutation_rate: `0.2`
6. seeds: `7, 17, 27`

### 4.3 输出目录
1. [output/pcg/ai_seeded_compare_v1](../../../output/pcg/ai_seeded_compare_v1)
2. [compare_summary.json](../../../output/pcg/ai_seeded_compare_v1/compare_summary.json)
3. [compare_summary.md](../../../output/pcg/ai_seeded_compare_v1/compare_summary.md)

## 5. 数据侧先验观察
在正式集成前，对 `vglc_chromosomes_approx.json` 做了频率分析。

观察结果：

1. `segment_id = 1` 占比极高
2. 高频转移几乎被 `1 -> 1` 主导
3. 内容分布明显偏向少量近似片段

这意味着：

1. 当前 AI 数据线确实能提供种子
2. 但它的表达空间目前还比较塌缩
3. 因此它更适合作为 initialization source，而不是最终生成质量的单独证据

## 6. 实验结果
### 6.1 汇总结果

| init_mode | runs | avg_difficulty_error | avg_structural_diversity | avg_emptiness_error | avg_difficulty_curve_error | avg_family_balance | avg_last_feasible_ratio | avg_last_first_front_size | avg_last_first_front_hv | avg_last_first_front_spread |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random | 3 | 0.4500 | 0.6250 | 0.3331 | 0.9286 | 0.6000 | 1.0000 | 9.3333 | 0.2400 | 0.0188 |
| ai_seeded | 3 | 0.4750 | 0.5938 | 0.3555 | 1.2679 | 0.5525 | 0.6667 | 6.5000 | 0.1370 | 0.0119 |

### 6.2 直接结论
第一轮结果很明确：

`在当前实现和当前数据分布下，ai_seeded 初始化没有优于 random 初始化。`

它在本轮对照中几乎所有核心指标都更差，包括：

1. `difficulty_error`
2. `structural_diversity`
3. `emptiness_error`
4. `difficulty_curve_error`
5. `family_balance`
6. `last_feasible_ratio`
7. `first_front_hv`
8. `first_front_spread`

### 6.3 最重要的现象
最关键的现象不是某个单独指标，而是：

1. `random` 三个 seed 都得到可行 best solution
2. `ai_seeded` 有一个 seed 在第 10 代结束时仍然没有恢复到可行 best solution

这说明当前 AI seed 不是“只是略差”，而是会在某些 run 中明显拖累初始搜索状态。

### 6.4 为什么会这样
结合数据分布分析，最合理的解释是：

1. `vglc_chromosomes_approx.json` 本身高度偏向少数 segment ID
2. 近似匹配把很多原始 Mario 结构压缩成了重复的 `1 / 3 / 15` 一类片段
3. 这些片段在当前 segment library 下容易组合出 `reachable = false` 的初始关卡
4. 因此 AI seed 提供的不是“高质量先验”，而是“偏窄且可行性偏弱的先验”

换句话说：

`当前 AI seed 已经成功接入了工程管线，但它提供的初始化偏置还不够好。`

## 7. 阶段判断
### 7.1 工程判断
从工程角度看，本轮是成功的。

原因不是结果更好，而是因为：

1. `ai_seeded` 已经成为正式可切换初始化模式
2. 它已经接入 `EA` 和 `NSGA-II` 主流程
3. 它可以通过统一 CLI 和实验脚本复现实验
4. 它已经能被量化比较，而不再只是“想法”

因此这一步已经把 AI 数据线从“旁路线素材”升级成了“主 pipeline 中的一个真实模块”。

### 7.2 研究判断
从研究角度看，本轮结果同样有价值。

它说明：

1. 不是所有 AI 生成先验都会自然改善 EA 搜索
2. `representation quality` 和 `seed distribution quality` 会直接影响 EA 初始搜索状态
3. 如果数据近似映射本身信息损失较大，AI 可能只会放大这种偏差

这其实是一个合理、且有课程讨论价值的负结果。

### 7.3 当前最合理的结论
当前最合理的结论不是“AI 线失败”，而是：

`AI-seeded initialization 已经完成接线，但当前版本还不具备正向收益，需要先提升 seed quality，再谈它是否值得进入正式展示主线。`

## 8. 当前结论模板
如果实验结果显示 AI seed 暂时不优，也不意味着这条线没有价值。

更可能的解释是：

1. `AI seed distribution` 还过于集中
2. 当前 segment library 与 VGLC 近似匹配的信息损失较大
3. AI 的价值更适合先体现在 initialization bias，而不是最终最优解质量

因此本轮最重要的产出是：

`我们已经把 AI data line 变成了 EA pipeline 的一个正式可切换初始化模式。`

## 9. 下一步建议
如果继续推进这条线，优先级建议如下：

1. 不要先继续调 LSTM 超参数
2. 先改善 `VGLC -> current segment library` 的映射质量
3. 引入更稳的 seed adapter，例如：
   - family-aware trimming
   - feasibility-aware repair
   - seed 过滤后再注入 population
4. 再做第二轮对照：
   - `random`
   - `ai_seeded_raw`
   - `ai_seeded_repaired`

当前阶段最务实的定位是：

`AI line 已经完成工程集成，但暂时保留为实验分支，不进入最终展示主线。`
