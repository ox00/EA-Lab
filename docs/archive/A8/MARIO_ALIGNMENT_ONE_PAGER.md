# Mario 核心对齐说明（1页）

## 这张 1 页纸是干什么的
用于：
- 开会快速对齐
- 开工前确认
- 中途复检有没有跑偏

## 一句话版本
我们这次做的是：

- `Mario-like level generation with explicit genotype + hard constraints + multi-objective EA`

不是：
- 先做大模型，再临时接 EA

## 我们的统一流程
```text
chromosome
-> decode
-> level phenotype
-> hard constraint check
-> objective evaluation
-> MOEA
-> render
```

## 现在已经推荐定下来的事情
1. 游戏域：`Mario-like`
2. 编码方式：`segment sequence encoding`
3. 可玩性：先做 `hard constraint`
4. 第一版目标：`difficulty matching`、`structural diversity`、`emptiness`
5. 第一版算法：可先用 `NSGA-II`

## Genotype / Phenotype 对齐
### Genotype
- 一串 segment ID
- 例子：`[0, 5, 1, 4, 8, 7, 2, 0]`

### Phenotype
- 解码后得到的一整张 Mario 逻辑地图
- 例如：`16 x 112` tile grid

### Render
- 只是把 phenotype 画出来用于展示
- 不属于 EA 的核心优化对象

## 生成侧必须提供
1. 固定 tile vocabulary
2. 固定地图尺寸
3. 固定 segment 宽度
4. segment library
5. `decode()`
6. `render()`

## EA 侧必须拿到
1. chromosome 长度
2. segment ID 合法范围
3. `check_constraints()`
4. `evaluate()`
5. mutation 规则
6. crossover 规则

## 必须冻结的 12 项
1. 游戏域
2. 地图高度
3. segment 宽度
4. 每关 segment 数量
5. tile vocabulary
6. genotype 格式
7. segment 库构造规则
8. decoder 行为
9. hard constraints
10. objective definitions
11. difficulty proxy
12. evaluator 输出格式

## 现在最容易出问题的点
1. 还没定接口就开始各写各的
2. tile 语义频繁变化
3. difficulty 定义太模糊
4. 不可行解处理方式没说清楚
5. 目标太多导致解释困难

## 本周最小交付
1. 手写一个 chromosome
2. 能 `decode`
3. 能 `check_constraints`
4. 能 `evaluate`
5. 能 `render`

只要这 5 步通了，项目就真正进入可执行状态。

## 对应详细文档
- 中文接口版：[EA-Lab/sample/A8/MARIO_EA_INTERFACE_CN.md](../../../sample/A8/MARIO_EA_INTERFACE_CN.md)
- 英文接口版：[EA-Lab/sample/A8/MARIO_EA_INTERFACE_EN.md](../../../sample/A8/MARIO_EA_INTERFACE_EN.md)
- 当前工作版：[EA-Lab/sample/A8/MARIO_EA_INTERFACE.md](../../../sample/A8/MARIO_EA_INTERFACE.md)
- EA 推进版：[EA-Lab/sample/A8/MARIO_EA_WORKFLOW.md](../../../sample/A8/MARIO_EA_WORKFLOW.md)
