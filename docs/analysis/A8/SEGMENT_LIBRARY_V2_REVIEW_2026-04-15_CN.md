# A8 Segment Library V2 复检（2026-04-15）

## 1. 本轮变更
本轮在原有 `10` 个 segment 基础上新增了 `8` 个更高密度的 segments：

1. `10`: 双层砖块平台 + coin
2. `11`: 砖块平台 + 双 enemy + question blocks
3. `12`: 顶部砖块走廊 + coins
4. `13`: 双侧阶梯 + question blocks
5. `14`: 双 pipe + 上层砖块平台
6. `15`: 厚实起伏地形 + enemy
7. `16`: 高密度奖励走廊
8. `17`: 混合型高密度障碍段

目标不是单纯“变复杂”，而是修正原始内容空间过空、过窄的问题。

## 2. 内容空间变化
新增前：

1. `segment_count = 10`
2. `avg_empty_ratio = 0.8504`
3. `9 / 10` 个 segments 的 `empty_ratio > 0.80`
4. `enemy segments = 2`
5. `pipe segments = 1`
6. `question segments = 2`

新增后：

1. `segment_count = 18`
2. `avg_empty_ratio = 0.8095`
3. `10 / 18` 个 segments 的 `empty_ratio > 0.80`
4. `enemy segments = 5`
5. `pipe segments = 3`
6. `question segments = 6`

解释：

1. 平均空旷度明显下降。
2. 内容类型覆盖明显扩大。
3. 搜索器现在更容易组合出“非极空”的可行关卡。

## 3. 参数扫描结果（V2）
本轮仍使用：

1. `algorithm = nsga2`
2. `population_size = {20, 30, 40}`
3. `mutation_rate = {0.1, 0.2, 0.3}`
4. `seed = {7, 17, 27}`
5. `generations = 20`

结果摘要：

1. 最低 `difficulty_error`: `population_size=40, mutation_rate=0.1`, 值约 `0.3833`
2. 最低 `emptiness_error`: `population_size=40, mutation_rate=0.3`, 值约 `0.3089`
3. 最高 `HV`: `population_size=20, mutation_rate=0.3`, 值约 `0.2667`
4. 最高 `front_spread`: `population_size=20, mutation_rate=0.3`, 值约 `0.0527`
5. 最高 `structural_diversity`: `0.6250`
6. 所有组合 `feasible_ratio = 1.0`

## 4. 与上一轮对比
上一轮代表性问题：

1. 原始 `emptiness` 常在 `0.84 - 0.86`
2. `HV` 约在 `0.125 - 0.138`
3. `structural_diversity` 多在 `0.31 - 0.38`

本轮代表性结果：

1. 原始 `emptiness` 已下降到 `0.75 - 0.79`
2. `HV` 提升到 `0.247 - 0.267`
3. `structural_diversity` 提升到 `0.54 - 0.63`

解释：

1. 这说明问题确实主要在内容空间，而不只是算法参数。
2. V2 segment library 让 `NSGA-II` 的多目标行为更充分地表现出来。
3. 现在的优化结果更接近“可用于展示”的阶段。

## 5. 当前建议
下一步不建议继续盲目加算法复杂度。

建议顺序：

1. 固定一组 V2 baseline 参数，建议优先考察 `pop=40, mut=0.1` 与 `pop=20, mut=0.3`
2. 选 2 到 3 组代表性参数导出前沿关卡截图，形成展示样例
3. 进入 V3 content-space 微调，而不是大改架构

## 6. 对老师的汇报口径
可以直接说：

1. 第一轮实验发现优化器有效，但内容库过空，限制了结果质量。
2. 第二轮我们优先扩展了内容空间，而不是继续堆算法复杂度。
3. 扩展后平均空旷率从 `0.8504` 降到 `0.8095`，同时 `HV` 和多样性都有明显提升。
4. 这说明项目当前最关键的工程能力，是把“内容空间设计”和“多目标优化”联动起来。
