# Mario EA 接口规范（CN）

## 文档定位
本文件是 A8 MVP 阶段的中文约束摘要。

权威接口定义以：
- [MARIO_EA_INTERFACE.md](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/docs/analysis/A8/MARIO_EA_INTERFACE.md)
- [MARIO_EA_INTERFACE_EN.md](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/docs/analysis/A8/MARIO_EA_INTERFACE_EN.md)

为准。

## MVP 核心约束
1. 仅做 `Mario-like` 单域。
2. 基因型采用 `segment ID sequence`。
3. 可玩性采用硬约束。
4. 目标函数采用三项：
`difficulty_error`、`structural_diversity`、`emptiness`。
5. 先完成 MVP，再评估 AI 扩展模块。

## 强制流程
`chromosome -> decode -> phenotype -> check_constraints -> evaluate -> selection`

## 最小 API
```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

## 必须冻结项
1. 地图常量（高度、segment 宽度、segment 数量）
2. tile vocabulary
3. segment library 结构
4. 约束规则
5. 目标公式
6. API 输出键

## 变更规则
上述冻结项任一变动，必须：
1. 提升协议版本
2. 分离新旧实验结果
