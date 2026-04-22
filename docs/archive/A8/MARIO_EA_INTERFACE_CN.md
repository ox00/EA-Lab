# Mario EA 对接接口说明（CN）

本文件是 [EA-Lab/sample/A8/MARIO_EA_INTERFACE.md](../../../sample/A8/MARIO_EA_INTERFACE.md) 的中文归档版，供中文讨论、对齐和后续修改使用。

当前建议：
- 继续把 [EA-Lab/sample/A8/MARIO_EA_INTERFACE.md](../../../sample/A8/MARIO_EA_INTERFACE.md) 作为日常阅读版
- 把本文件作为中文冻结副本
- 把英文版作为 report / presentation / technical appendix 的正式素材来源

## 当前冻结结论
1. 游戏域：`Mario-like`
2. 编码方式：`segment sequence encoding`
3. 搜索对象：`genotype`
4. 评价对象：`phenotype`
5. 可玩性：优先作为 `hard constraint`
6. 第一版目标：`difficulty matching`、`structural diversity`、`emptiness`

## 最核心接口
```python
decode(chromosome: list[int]) -> Level
check_constraints(level: Level) -> dict
evaluate(level: Level) -> dict
render(level: Level, path: str) -> None
```

## 最重要的团队共识
1. EA 不直接优化画风，而是优化关卡结构。
2. 同一个 genotype 可以渲染成不同视觉风格，但逻辑关卡不变。
3. 先把 `chromosome -> decode -> check -> evaluate` 跑通，再谈复杂模型。
4. 如果接口没冻结，后面算法和生成模块都会反复返工。

## 使用建议
如果你们需要快速开会对齐：
- 先看 [EA-Lab/sample/A8/MARIO_ALIGNMENT_ONE_PAGER.md](../../../sample/A8/MARIO_ALIGNMENT_ONE_PAGER.md)
- 再看 [EA-Lab/sample/A8/MARIO_EA_INTERFACE.md](../../../sample/A8/MARIO_EA_INTERFACE.md)
- 英文输出时参考 [EA-Lab/sample/A8/MARIO_EA_INTERFACE_EN.md](../../../sample/A8/MARIO_EA_INTERFACE_EN.md)
