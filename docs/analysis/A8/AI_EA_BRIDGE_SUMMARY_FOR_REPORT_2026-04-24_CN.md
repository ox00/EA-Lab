# AI-EA Bridge Summary for Report / PPT 2026-04-24

## 1. 背景
本项目原始主线是一个可解释的 Mario PCG EA pipeline：

`chromosome -> decode -> constraint check -> evaluate -> NSGA-II`

在此基础上，项目新增了上游 AI 生成关卡数据能力。为了让 AI 结果真正进入当前工程闭环，而不是停留在独立分支，本轮工作完成了 AI 与 EA 的桥接。

## 2. 本轮优化目标
本轮优化不追求“AI 直接替代 EA”，而是明确采用如下分工：

1. AI 负责提供带有真实 Mario 分布先验的 chromosome seed
2. Adapter 负责把 AI 输出转换成当前项目可接受的固定长度 chromosome
3. EA / NSGA-II 负责 feasibility 与多目标 refinement

核心目标是建立：

`AI generation -> adapter -> repaired seed -> EA refinement`

这一完整闭环。

## 3. 方法设计
### 3.1 AI-seeded initialization
在 `random` 初始化之外，新增 `ai_seeded` 初始化模式。

其逻辑为：

1. 优先读取训练好的 `LSTM segment generator`
2. 从 VGLC 近似染色体分布中采样新的 segment sequence
3. 生成固定长度前缀扩展序列
4. 输出 segment ID sequence 作为 EA 初始个体来源

### 3.2 Adapter layer
为保证 AI 输出能直接进入当前 Mario PCG 系统，新增 adapter 层。

Adapter 的职责包括：

1. 非法 segment ID 过滤
2. 长度标准化
3. `trim / sliding window / pad`
4. 保证最终输出满足当前 `cfg.num_segments`

这一步保证了 AI 与现有 `segment chromosome representation` 的接口对齐。

### 3.3 Optional repair
由于原始 AI seed 在第一轮实验中暴露出明显的可行性问题，本轮进一步在 adapter 内加入可选 repair。

Repair 的设计原则是：

1. 不改 AI 模型代码
2. 不依赖上游同学继续改生成器才能复测
3. 作为 adapter 的可开关阶段单独存在
4. 为未来新的 AI 输出保留统一后处理入口

当前 repair 主要针对：

1. `reachable` 风险
2. 高风险 gap-heavy segment 组合
3. 过于集中的低可行性 seed pattern

## 4. 两轮实验结论
### 4.1 第一轮：AI seed baseline
第一轮比较 `random` 与 `ai_seeded`。

结果表明：

1. `ai_seeded` 没有优于 `random`
2. 一个 seed 在实验结束时仍未恢复到可行最优解
3. 原始 AI seed 会把可行性风险直接带进初始化种群

这一轮的意义在于证明：

`AI 输出已成功接入主 pipeline，但原始 seed quality 不足。`

### 4.2 第二轮：AI seed + adapter repair
第二轮比较三组：

1. `random`
2. `ai_seeded`
3. `ai_seeded_repaired`

结果表明：

1. `ai_seeded_repaired` 把 `last_feasible_ratio` 恢复到 `1.0000`
2. `difficulty_error` 优于 `random`
3. `difficulty_curve_error` 优于 `random`
4. `family_balance` 明显优于 `random`
5. 但 `structural_diversity`、`emptiness_error`、`HV` 仍略弱于 `random`

这说明：

`adapter repair 能把 AI seed 从“不可用或不稳定”修到“可用且带方向性收益”的状态。`

## 5. 本轮优化的工程价值
本轮工作的工程价值主要体现在四点：

1. 完成了 AI 与 EA 的正式桥接
2. 建立了可复用的 adapter 层
3. 将 repair 设计成可选后处理模块，便于未来复测
4. 让 AI 线不再是独立原型，而是成为主项目中的一个可切换初始化模式

## 6. 本轮优化的研究价值
本轮结果同样具有方法层价值：

1. 证明 AI seed 不会自动改善 EA 搜索
2. 说明 seed distribution quality 会直接影响多目标搜索起点
3. 说明 adapter / repair 不只是工程补丁，而是 hybrid PCG 系统中的关键中间层
4. 支持一个重要论点：

`在 hybrid PCG 中，AI generation 和 EA optimization 之间需要 representation-aware bridging layer。`

## 7. 当前阶段结论
本轮最合理的阶段结论是：

1. 项目闭环已经成立
2. AI 线已经不是概念，而是已经进入主 pipeline
3. 原始 AI seed 仍不稳定
4. adapter-level repair 已经把它拉回到可用状态
5. 当前最合理的系统形态是：

`AI generation + optional adapter repair + EA refinement`

## 8. 对 report / PPT 的建议表述
可以直接使用下面这句作为阶段总结：

`We bridged the upstream AI-generated Mario chromosome seeds into the EA pipeline through an adapter layer, and further introduced an optional repair stage. The results show that raw AI seeds are not sufficient by themselves, but adapter-level repair can recover feasibility and make AI-seeded initialization practically usable for downstream EA refinement.`
