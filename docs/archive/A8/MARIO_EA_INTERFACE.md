# Mario EA 对接接口说明

## 这份文档是给谁看的
这份文档是给两个人一起看的：

- 负责 `关卡生成 / 解码 / 渲染` 的同学
- 负责 `EA / MOEA 搜索` 的同学

它的作用只有一个：

- 尽早把接口定死，避免后面各写各的，最后拼不起来

## 先说最重要的一句话
我们这次不是让 EA 直接“画游戏画面”。

EA 真正在操作的是：

- 一串可搜索的编码

这串编码先被解码成：

- 一张逻辑上的 Mario 关卡地图

最后如果要展示给老师看，再由渲染器把它画出来。

所以整个流程是：

```text
基因型 genotype
-> 解码 decode
-> 关卡逻辑图 phenotype
-> 硬约束检查
-> 多目标评价
-> EA 选择 / 交叉 / 变异
-> 输出可展示的关卡
```

## 三个核心概念
### 1. 基因型 genotype
基因型就是 EA 真正拿来搜索的“染色体”。

你可以把它理解成：

- 关卡的压缩写法
- 机器方便操作的版本
- 不一定长得像最终地图

例子：

```text
[0, 5, 1, 4, 8, 7, 2, 0]
```

这不代表玩家直接看到这串数字。  
它代表“第 1 段放什么，第 2 段放什么，第 3 段放什么”。

### 2. 表现型 phenotype
表现型是基因型解码后得到的“逻辑关卡”。

比如：

- 一张 `16 x 112` 的 tile 地图
- 每个格子是什么类型：空地、地面、砖块、敌人、管道……

这时候它已经是一张真正的关卡了，只是还没换成好看的美术皮肤。

### 3. 渲染结果 rendered level
渲染结果是给人看的画面。

比如：

- 地面贴图
- 敌人的 sprite
- 背景图
- UI

同一张逻辑关卡，可以换不同画风来展示。  
所以：

- EA 不直接优化“画风”
- EA 优化的是“关卡结构”

## 推荐的编码方案
这次 Mario 项目，推荐用：

- `segment sequence encoding`

不要一开始就做：

- 整张图逐格自由编码
- 大模型先生成再说

原因很简单：

- 搜索空间太大
- 很容易生成坏关卡
- 交叉和变异不好设计
- 课程周期里不稳

## 什么是 segment sequence encoding
可以把一关 Mario 理解成很多“小关卡片段”拼起来。

比如先做一个片段库：

```text
S0 = 平地
S1 = 小坑
S2 = 上楼梯
S3 = 下楼梯
S4 = 平地 + 敌人
S5 = 高台
S6 = 奖励块区域
S7 = 管道障碍
S8 = 宽安全区
S9 = 密集障碍区
```

然后一条染色体就是：

```text
[S0, S5, S1, S4, S8, S7, S2, S0]
```

如果写成数字，就是：

```text
[0, 5, 1, 4, 8, 7, 2, 0]
```

这就是 `genotype`。

它表达的业务含义是：

- 这一关由 8 段组成
- 每一段选用哪一种局部结构

这样做的好处：

- 交叉很自然：交换几段
- 变异很自然：把某一段换成另一段
- 生成侧也容易维护片段库

## 一个非常直观的例子
假设每个片段宽度是 `8`，高度是 `16`。

其中一个片段 `S4` 的逻辑内容可能是：

```text
row 0: 0 0 0 0 0 0 0 0
row 1: 0 0 0 0 0 0 0 0
row 2: 0 0 0 0 0 0 0 0
row 3: 0 0 0 0 0 0 0 0
row 4: 0 0 0 0 0 0 0 0
row 5: 0 0 0 0 0 0 0 0
row 6: 0 0 0 3 0 0 0 0
row 7: 0 0 0 0 0 0 0 0
row 8: 0 0 0 0 0 0 0 0
row 9: 0 0 0 0 0 5 0 0
row10: 0 0 0 0 0 0 0 0
row11: 0 0 0 0 0 0 0 0
row12: 0 0 0 0 0 0 0 0
row13: 0 0 0 0 0 0 0 0
row14: 1 1 1 1 1 1 1 1
row15: 1 1 1 1 1 1 1 1
```

其中 tile 含义例如：

- `0` = 空
- `1` = 地面
- `3` = 问号砖块
- `5` = 敌人

于是：

- `S4` 这个片段的业务意义 = “一段有地面、有一个奖励块、有一个敌人的普通路段”

如果整关的 chromosome 是：

```text
[0, 5, 1, 4, 8, 7, 2, 0]
```

那解码器做的事情就是：

- 取出第 0 号片段
- 接上第 5 号片段
- 接上第 1 号片段
- ...
- 最后拼成一整张 Mario 地图

## 这就是你和同学的接口
### 生成侧要负责什么
负责生成和维护“关卡材料”。

至少要提供：

1. 固定的 tile 定义
2. 固定的地图尺寸
3. 固定的片段宽度
4. 一个稳定的 segment 库
5. `decode(chromosome)` 函数
6. `render(level)` 函数

### EA 侧要负责什么
负责在这个编码空间里搜索更好的关卡。

至少要依赖：

1. chromosome 长度是多少
2. 每个位置允许取哪些 segment ID
3. 如何 mutation
4. 如何 crossover
5. 某关卡是否合法
6. 某关卡的目标值是多少

## 最小 API 约定
你们应该尽快约定这 4 个函数：

```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

建议返回格式如下：

```python
check_constraints(level) = {
    "is_feasible": True,
    "start_ok": True,
    "goal_ok": True,
    "reachable": True,
    "illegal_overlap": False,
}

evaluate(level) = {
    "difficulty_error": 0.18,
    "structural_diversity": 0.74,
    "emptiness": 0.41,
}
```

业务意义也很清楚：

- `check_constraints` 回答：这关能不能当成合法关卡
- `evaluate` 回答：这关在目标上表现如何

## 现在必须先定死的全局参数
建议先固定：

1. 地图高度：`16`
2. 片段宽度：`14` 或 `16`
3. 每关片段数：比如 `8`
4. 总宽度：`segment_width * num_segments`

例如：

- height = `16`
- segment width = `14`
- num segments = `8`
- total width = `112`

如果这些参数不先定，后面：

- segment 库做不稳
- EA 染色体长度不稳
- fitness 统计也会漂

## 现在必须先定死的 tile vocabulary
推荐先用简化版：

- `0` = empty
- `1` = solid ground
- `2` = breakable brick
- `3` = question block
- `4` = coin
- `5` = enemy
- `6` = pipe
- `7` = start marker
- `8` = goal marker

注意：

- tile 语义一旦变动，解码、约束、渲染、评估都要跟着改
- 所以这个必须在早期冻结

## 硬约束是什么
硬约束就是“一票否决”。

也就是说：

- 再好看
- 再多样
- 再符合目标

只要不合法，就不能当有效解。

### 第一版建议的硬约束
1. 起点区域必须安全、可站立
2. 终点区域必须存在
3. 终点必须可到达
4. 坑宽不能超过角色跳跃能力上限
5. 不能出现非法重叠放置
6. 管道、砖块、敌人等必须遵守摆放规则

### 可选硬约束
1. 敌人总数上限
2. 最低地面覆盖率
3. 某类片段不能连续出现太多次

## 软目标是什么
软目标就是：

- 合法关卡之间，谁更值得保留

建议第一版只做 2 到 3 个目标，不要太多。

### 推荐目标 1：difficulty matching
不是越难越好，而是：

- 尽量接近目标难度

比如你们先定：

- target difficulty = medium

然后去最小化：

- `difficulty_error = |difficulty_score - target|`

### 推荐目标 2：structural diversity
它衡量：

- 关卡结构有没有变化
- 是否老是重复同一种模式

可以从这些角度算：

- 重复片段惩罚
- 行差异
- 局部结构熵
- 片段新颖度

### 推荐目标 3：emptiness 或 density balance
它衡量：

- 关卡是不是太空
- 或者太挤

业务意义就是：

- 控制视觉简洁度与信息密度

## Mario 的 difficulty 不要定义得太粗糙
不要只看敌人数量。

更合理的是组合几个因素：

- enemy density
- average gap width
- height variation
- required jump count
- narrow landing count

比如第一版可以这样算：

```text
difficulty_score =
0.35 * normalized_enemy_density +
0.30 * normalized_gap_risk +
0.20 * normalized_height_variation +
0.15 * normalized_jump_count
```

然后：

- EA 不是直接追求最大 difficulty
- 而是追求和目标难度接近

## EA 操作怎么设计
### Mutation
最简单、最稳的版本：

- 随机选一个位置
- 把这个位置的片段 ID 换成另一个合法 ID

例子：

```text
[0, 5, 1, 4, 8, 7, 2, 0]
-> mutate position 3
-> [0, 5, 1, 9, 8, 7, 2, 0]
```

### Crossover
最简单、最稳的版本：

- one-point crossover
- 或 two-point crossover

例子：

```text
parent A = [0, 5, 1, 4, 8, 7, 2, 0]
parent B = [8, 8, 3, 2, 6, 1, 4, 5]

child    = [0, 5, 1, 2, 6, 1, 4, 5]
```

业务意义：

- 把两个“还不错的关卡”局部拼接
- 看能不能组合出更好的后代

## 这个阶段必须先约定好的内容
### 必须立刻冻结
1. 游戏域：只做 `Mario-like`
2. 地图高度
3. 片段宽度
4. 每关片段数
5. tile vocabulary
6. genotype 格式：`segment ID sequence`
7. segment 库怎么建
8. `decode()` 行为
9. 硬约束定义
10. 目标函数定义
11. difficulty proxy
12. evaluator 输出格式

### 应该尽快约定
1. population size
2. mutation rate
3. crossover 方式
4. 不可行解如何处理
5. 第一版到底做 2 目标还是 3 目标
6. 最终 demo 用什么渲染方式导出

### 可以后面再说
1. 是否接 VAE / GAN
2. 是否做人类交互式评价
3. 是否做个性化关卡适配
4. 是否做 fancy UI

## 推荐的团队分工
### 你负责
- 染色体定义审查
- mutation / crossover
- selection / ranking
- MOEA 主循环
- 实验日志

### 你同学负责
- segment 库
- decode
- render
- 约束检查支持
- phenotype 上的指标计算辅助

## 最后一句建议
对你们现在这个阶段，最重要的不是“先把算法写多高级”，而是先把下面这条链路跑通：

```text
chromosome
-> decode
-> level
-> check_constraints
-> evaluate
```

只要这条链路稳定了：

- 你可以独立写 EA
- 同学可以独立做生成与渲染
- 后面再换 NSGA-II、MOEA/D、Two_Arch2 风格框架都不难
