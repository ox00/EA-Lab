# A8 参数扫描与 Segment Library 复检（2026-04-14）

## 1. 目的
本轮工作有两个目标：

1. 检查 `NSGA-II` 对小范围参数变化是否敏感。
2. 检查当前 `segment library` 是否在结构上限制了优化结果。

## 2. 参数扫描设置
算法：

1. `nsga2`

参数网格：

1. `population_size`: `20, 30, 40`
2. `mutation_rate`: `0.1, 0.2, 0.3`
3. `seed`: `7, 17, 27`
4. `generations`: `20`

输出：

1. `output/pcg/parameter_scan/scan_summary.json`
2. `output/pcg/parameter_scan/scan_summary.csv`
3. `output/pcg/parameter_scan/scan_summary.md`

## 3. 参数扫描结果
核心观察：

1. `population_size=30, mutation_rate=0.3` 的 `difficulty_error` 最低，约为 `0.4208`。
2. `population_size=40, mutation_rate=0.3` 的 `HV` 最高，约为 `0.1385`。
3. `population_size=30, mutation_rate=0.3` 的 `front_spread` 较高，约为 `0.0471`。
4. `population_size=20, mutation_rate=0.3` 的 `emptiness_error` 最低，约为 `0.3958`。
5. 所有组合的 `feasible_ratio` 都为 `1.0`。

解释：

1. 增大 `mutation_rate` 明显提升了 Pareto front 的覆盖能力，`HV` 和 `spread` 普遍更高。
2. 较大的 `population_size` 有助于保留更完整的 front，但并不自动带来最好的 `difficulty_error`。
3. 参数变化可以改善结果，但改善幅度有限，说明当前瓶颈不只在算法超参数。

## 4. Segment Library 密度复检
输出：

1. `output/pcg/segment_library_analysis/segment_density.json`
2. `output/pcg/segment_library_analysis/segment_density.csv`
3. `output/pcg/segment_library_analysis/segment_density.md`

核心结果：

1. 当前 `segment_count = 10`
2. `avg_empty_ratio = 0.8504`
3. `min_empty_ratio = 0.7589`
4. `max_empty_ratio = 0.9018`
5. `9 / 10` 个 segments 的 `empty_ratio > 0.80`
6. 只有 `2` 个 segments 带 enemy
7. 只有 `1` 个 segment 带 pipe
8. 只有 `2` 个 segments 带 question block

解释：

1. 当前 segment library 整体极度偏空。
2. 优化器即使工作正常，也难以搜索到低 emptiness 的解，因为可选内容本身就稀疏。
3. 当前库对障碍、奖励、结构变化的覆盖不足，多样性上限受到限制。

## 5. 阶段性判断
本轮结果说明：

1. `NSGA-II` 已具备可比较的多目标行为。
2. 参数扫描可以优化前沿质量，但不是当前第一瓶颈。
3. 真正更大的问题在内容空间定义，即 `segment library` 设计过空、过窄。

## 6. 下一步建议
优先级建议如下：

1. 先扩展 `segment library`，增加更高密度的地形、障碍、奖励和混合结构段。
2. 再做第二轮参数扫描，验证更丰富内容空间下的 `HV` 是否继续提升。
3. 报告中明确写出：当前实验发现“优化器有效，但内容空间限制明显”。

## 7. 对老师的汇报口径
可以直接这样说：

1. 我们先验证了算法层的可行性和多目标行为。
2. 之后通过参数扫描确认，调参可以带来一定提升，但提升有限。
3. 进一步做内容库密度分析后发现，当前 segment library 平均空旷率超过 `0.85`，因此内容空间本身限制了结果质量。
4. 下一步不是盲目继续调算法，而是先扩展关卡片段库，再做第二轮对照实验。
