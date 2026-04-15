# Mario Segment Library V3 设计计划

## 1. 文档目的
本文档用于约束 `Mario PCG` 项目的下一轮内容空间升级。

V3 的目标不是继续“多加几个 segment”，而是把当前 `segment library` 从离散素材集合，升级为一个更可控、更适合实验和汇报的内容空间。

## 2. 当前问题诊断
V2 已经证明一件事:

1. 仅靠算法调参，无法弥补内容空间本身过窄的问题
2. 当 `segment` 类型太少时，优化器只能在有限结构里反复重排
3. 结果会出现:
   - 视觉上像是在“换排列”，不像在“换关卡风格”
   - `difficulty_error` 可以优化，但难度形成机制不够清晰
   - `structural_diversity` 有数值变化，但内容语义差异仍然偏弱

因此，V3 的核心工作不是“再做一版素材补丁”，而是建立一套更清楚的内容设计坐标系。

## 3. V3 的设计原则

### 3.1 从“单个 segment”转为“segment family”
V2 的基本单位是 `segment id`。

V3 建议引入更高一层的概念:

1. `family`: 一类结构主题
2. `variant`: 该主题下的具体实例

例如:

1. `flat_safe`
2. `gap_jump`
3. `pipe_pressure`
4. `enemy_pressure`
5. `reward_relief`
6. `stair_climb`
7. `mixed_challenge`

业务意义:
这样做以后，我们不再只是说“用了 17 号 segment”，而是可以说“这一段属于 jump pressure family”。这会让实验解释、组内对齐和最终汇报都更清楚。

### 3.2 显式区分难度层级
目前难度更多是通过结果统计反推出来的。

V3 建议每个 `segment` 在设计时就带上 `difficulty tier`:

1. `tier 1`: 低风险，主要用于开场、缓冲、节奏恢复
2. `tier 2`: 中等压力，包含基础障碍或单个敌人
3. `tier 3`: 高压力，包含组合障碍、连续跳跃或更紧密的敌人配置

业务意义:
这样 EA 优化的不只是“随机拼块”，而是在一个有难度语义的零件库里组合关卡。难度目标会更容易解释，也更容易调试。

### 3.3 每个 family 内保持“同主题多变体”
如果一个 family 只有 1 个 variant，EA 仍然会很快陷入模板重复。

V3 建议:

1. 每个核心 family 至少准备 `3` 个 variant
2. variant 间保持同主题，但在位置、密度、节奏上有差异

例如 `gap_jump` family:

1. 小 gap + 平台恢复
2. 双 gap + 奖励块引导
3. gap 前加敌人或高低差

学术价值:
这能让 `structural_diversity` 更接近“可解释的结构差异”，而不只是 ID 层面的不同。

## 4. V3 推荐的内容结构

### 4.1 建议的 family 结构
建议 V3 至少覆盖以下 family:

1. `flat_safe`
   - 低风险平地
   - 用于起点、恢复段、节奏缓冲
2. `reward_relief`
   - 奖励块、金币、较安全的平台
   - 用于正反馈和视觉变化
3. `gap_jump`
   - 跳跃型挑战
   - 控制基础难度曲线
4. `pipe_pressure`
   - 管道与落脚区组合
   - 引入地形阻挡与路径约束
5. `enemy_pressure`
   - 基于敌人位置的风险段
   - 形成操作压力
6. `stair_climb`
   - 台阶、高低差
   - 形成节奏与高度变化
7. `mixed_challenge`
   - gap + enemy / pipe + reward 的组合段
   - 作为高难度表达单元

### 4.2 建议的 family 元数据
每个 segment 不只保留 tile layout，还建议附带以下元信息:

1. `family`
2. `variant`
3. `difficulty_tier`
4. `empty_ratio`
5. `enemy_count`
6. `pipe_count`
7. `reward_count`
8. `hazard_score`
9. `recovery_score`

工程意义:
这会让后续评估函数、repair operator、甚至可解释展示层都有更稳定的接口。

## 5. V3 对 EA 的直接帮助

### 5.1 更适合做 genotype 解释
当前 chromosome 是 `segment id` 序列。

V3 后，虽然编码表面上仍可保持 `segment id`，但解释层会更强:

1. 每个 gene 不再只是“编号”
2. 每个 gene 对应一个有语义的结构单元
3. 一个 chromosome 可以被解释成:
   - 开场缓冲
   - 中段跳跃
   - 奖励恢复
   - 高压混合挑战
   - 终点收束

这对团队协作很重要，因为这让 genotype 不再抽象。

### 5.2 更适合做 repair 和约束
当 segment 有 family 和 tier 信息后，可以更自然地增加规则:

1. 起点附近禁止 `tier 3`
2. 连续两个 `mixed_challenge` 时自动降压
3. 若前一段为大 gap，则后一段优先接 `reward_relief` 或 `flat_safe`

这类规则不是拍脑袋，而是把“关卡节奏”变成可执行约束。

### 5.3 更适合做新目标
V3 为下一步增加更合理的目标函数提供条件，例如:

1. `difficulty_curve_error`
2. `family_balance_score`
3. `pressure_recovery_balance`
4. `motif_repetition_penalty`

这比单纯依赖空白率更接近真正的关卡设计逻辑。

## 6. V3 推荐的落地方式

### 6.1 不要一次重做全部 library
建议使用“小步升级”方式。

第一阶段:

1. 保留现有 V2 segment
2. 新增一批带 family / tier 标注的 segment
3. 先让分析脚本能读出 family 分布与 tier 分布

第二阶段:

1. 更新评估脚本
2. 增加 family/tier 统计指标
3. 比较 V2 与 V3 的 Pareto front 差异

第三阶段:

1. 再考虑 repair operator 或更细的 difficulty proxy
2. 再考虑更强展示层或可玩 demo

### 6.2 建议的最小 V3 规模
为了控制工作量，建议先做一个“够用但不臃肿”的版本:

1. `7` 个 family
2. 每个 family `3` 个 variant
3. 总数约 `21` 个核心 segment

如果保留部分 V2 内容，总量可以在 `24-30` 个 segment 左右。

这个规模已经足以支持:

1. 更可信的 diversity 实验
2. 更清楚的 difficulty 结构
3. 更有说服力的展示效果

## 7. 建议的阶段目标

### 7.1 工程目标
形成一个可维护的 `segment library schema`，让后续:

1. 新增内容有统一入口
2. 分析脚本能直接读语义元信息
3. 渲染和实验层不需要反复改接口

### 7.2 学术目标
让项目从“EA 拼接示例”升级为“带有内容空间设计意识的 PCG 实验系统”。

这会使报告能更明确地回答:

1. 为什么不是只有算法重要
2. 为什么 representation design 会决定优化上限
3. 为什么内容库设计本身就是 EA 项目的一部分

## 8. 结论
V3 的核心不是增加素材数量，而是提升内容空间的结构化程度。

一句话概括:

`V2 解决的是“太空”，V3 要解决的是“太散、太弱语义”。`

如果 V3 做好，后面的算法增强、repair、可解释展示、甚至课堂汇报，都会更顺。
