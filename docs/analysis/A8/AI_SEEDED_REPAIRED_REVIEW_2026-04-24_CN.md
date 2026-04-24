# Mario PCG AI-Seeded Repaired Review 2026-04-24

## 1. 文档目的
本文档记录 `ai_seeded_repaired` 的第二轮集成实验结果。

这轮实验关注的问题是：

`如果在 adapter 层加入一个可选 repair 阶段，是否能在不改 AI 模型的情况下，改善 AI seed 的可行性与搜索起点质量？`

## 2. 设计原则
### 2.1 repair 放在哪一层
本轮明确把 repair 放在 adapter 层，而不是 AI 训练/生成代码里。

原因：

1. 便于和同学的 AI 模块解耦
2. 便于后续继续替换或升级生成模型
3. 便于做统一的后处理对照测试

### 2.2 当前 repair 的定位
当前 repair 不是“最终最优修复器”，而是一个工程上可复用的可选阶段：

1. 输入：AI 生成的 segment sequence
2. 输出：固定长度且更偏向可行的 chromosome
3. 作用：降低明显的 `reachable` 风险

## 3. 实验设计
### 3.1 对照组
本轮比较三组初始化模式：

1. `random`
2. `ai_seeded`
3. `ai_seeded_repaired`

### 3.2 固定设置
1. algorithm: `nsga2`
2. objective_mode: `core_3obj`
3. population_size: `20`
4. generations: `10`
5. mutation_rate: `0.2`
6. seeds: `7, 17, 27`

### 3.3 输出目录
1. [output/pcg/ai_seeded_compare_v2](../../../output/pcg/ai_seeded_compare_v2)
2. [compare_summary.json](../../../output/pcg/ai_seeded_compare_v2/compare_summary.json)
3. [compare_summary.md](../../../output/pcg/ai_seeded_compare_v2/compare_summary.md)

## 4. 预期解释框架
本轮结果可能出现三种情况：

1. repair 同时提升 feasibility 和质量指标
2. repair 提升 feasibility，但牺牲内容质量
3. repair 几乎无帮助，说明 adapter 级修复还不够

其中第 2 种也仍然是有价值结果，因为它能说明：

`repair 可以先解决“能不能跑”，再继续优化“跑得好不好”。`

## 5. 实验结果
### 5.1 汇总结果

| init_mode | runs | avg_difficulty_error | avg_structural_diversity | avg_emptiness_error | avg_difficulty_curve_error | avg_family_balance | avg_last_feasible_ratio | avg_last_first_front_size | avg_last_first_front_hv | avg_last_first_front_spread |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random | 3 | 0.4500 | 0.6250 | 0.3331 | 0.9286 | 0.6000 | 1.0000 | 9.3333 | 0.2400 | 0.0188 |
| ai_seeded | 3 | 0.4625 | 0.6250 | 0.3477 | 1.1250 | 0.5700 | 0.6667 | 4.5000 | 0.1491 | 0.0119 |
| ai_seeded_repaired | 3 | 0.4375 | 0.6042 | 0.3465 | 0.8690 | 0.7000 | 1.0000 | 7.6667 | 0.2339 | 0.0188 |

### 5.2 直接结论
这轮结果说明：

`adapter-level repair 是有效的，而且已经把 ai_seeded 从“明显劣化”拉回到了“部分优于 random baseline”的状态。`

### 5.3 repair 带来的主要收益
相对 `ai_seeded` 原始版本，`ai_seeded_repaired` 的提升非常明显：

1. `avg_last_feasible_ratio` 从 `0.6667` 回升到 `1.0000`
2. `avg_difficulty_error` 从 `0.4625` 改善到 `0.4375`
3. `avg_difficulty_curve_error` 从 `1.1250` 改善到 `0.8690`
4. `avg_family_balance` 从 `0.5700` 提升到 `0.7000`
5. `avg_first_front_hv` 从 `0.1491` 提升到 `0.2339`
6. `avg_first_front_spread` 从 `0.0119` 回升到 `0.0188`

这说明 repair 不只是“把非法解修成合法解”，它还明显改善了搜索起点质量。

### 5.4 与 random baseline 的比较
和 `random` 直接比较，`ai_seeded_repaired` 呈现的是“部分超越、部分落后”：

优于 `random` 的部分：

1. `difficulty_error`: `0.4375 < 0.4500`
2. `difficulty_curve_error`: `0.8690 < 0.9286`
3. `family_balance`: `0.7000 > 0.6000`
4. `last_feasible_ratio`: 同样是 `1.0000`

仍弱于 `random` 的部分：

1. `structural_diversity`: `0.6042 < 0.6250`
2. `emptiness_error`: `0.3465 > 0.3331`
3. `first_front_size`: `7.6667 < 9.3333`
4. `first_front_hv`: `0.2339 < 0.2400`

这意味着当前 repair 已经把 AI seed 从“负资产”修成了“有方向性的初始化偏置”，但还没有形成全面优势。

### 5.5 最有价值的现象
最值得保留的现象是：

1. 原始 `ai_seeded_seed17` 在第一轮里无法恢复可行 best solution
2. `ai_seeded_repaired_seed17` 在第二轮里恢复为可行，并取得了 `difficulty_error = 0.4125`、`family_balance = 0.75`

这说明 adapter repair 的工程价值是真实存在的。

## 6. 阶段判断
### 6.1 工程判断
当前 repair 设计已经达到一个可提交、可反馈同学、可继续复用的阶段。

原因：

1. repair 放在 adapter 层，不依赖 AI 代码内部修改
2. 可以作为可选开关独立开启/关闭
3. 可以用于未来任何一轮新的 AI 生成结果测试
4. 已经通过三组对照说明其价值不是理论猜测

### 6.2 研究判断
当前最合理的研究判断是：

`AI seed 本身并不会自动改善 EA；但 adapter-level repair 能把它转化为更可用的 initialization bias。`

也就是说，当前有效的不是“裸 AI 输出”，而是：

`AI generation + adapter repair + EA refinement`

这个组合才开始接近你们项目要的工程闭环。

### 6.3 现在该怎么和同学反馈
建议反馈口径如下：

1. 当前 AI 线已经成功接到 EA 主 pipeline
2. 原始 AI seed 会带来可行性风险
3. adapter repair 可以显著降低这类风险
4. 后续如果同学继续优化 AI 生成质量，你们这边可以直接复用 repair adapter 再做测试

### 6.4 当前定位
当前最务实的定位是：

`ai_seeded_repaired 已经足够作为“实验增强分支”保留，并可作为后续 AI 版本测试的统一接入口。`
