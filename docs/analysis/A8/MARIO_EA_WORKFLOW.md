# Mario EA Workflow

## 这份文档解决什么问题
这份文档是给你这一侧用的。

它不讨论美术，不讨论 fancy 生成模型。  
它只回答一件事：

- 作为负责 EA 的同学，你现在应该按什么顺序推进

## 总体流程
建议你按下面这条线推进：

```text
1. 冻结接口
2. 跑通 decode
3. 跑通 constraint check
4. 跑通 objective evaluation
5. 写最小 EA
6. 换成 MOEA
7. 做实验和可视化
```

## 第 1 步：冻结接口
你先不要急着写 NSGA-II。

先确保这些东西已经固定：

1. 染色体长度
2. segment ID 取值范围
3. decode 输入输出格式
4. constraint checker 输出格式
5. evaluator 输出格式

如果这里没定死，后面算法白写。

## 第 2 步：先跑通最小样例
目标不是“找到最优关卡”，而是验证整条链路没断。

你应该先拿一个手写 chromosome 做这 4 件事：

1. decode 成 level
2. check_constraints
3. evaluate
4. render

比如：

```text
[0, 5, 1, 4, 8, 7, 2, 0]
```

如果这一步跑不通，后面 EA 不可能稳定。

## 第 3 步：把不可行解处理方式定掉
这一步很重要。

建议第一版采用：

- `feasible-first`

意思是：

- 先区分合法和非法
- 合法的一定比非法的优先
- 非法之间再按约束违反程度比较

原因：

- 对课程项目最稳
- 逻辑好解释
- 比直接乱罚分更可控

## 第 4 步：先做单目标最小 EA 验证
不要一上来就写完整 MOEA。

先写一个最小 EA，只优化一个简单目标，比如：

- `difficulty_error`

最小流程：

1. 随机初始化 population
2. decode 每个个体
3. 过滤 / 标记可行性
4. 计算 fitness
5. selection
6. crossover
7. mutation
8. survivor update

这一步的目的不是最终结果，而是：

- 验证你的 mutation / crossover 是否合理
- 验证 population 是否真的在进步

## 第 5 步：升级成多目标
等单目标版本跑稳以后，再切到多目标。

推荐第一版多目标：

1. `difficulty_error`
2. `structural_diversity`
3. `emptiness`

其中：

- `difficulty_error` 越小越好
- `structural_diversity` 越大越好
- `emptiness` 可以按目标方向处理成最大化或最小化

## 第 6 步：MOEA 的推荐顺序
如果你时间有限，建议实现顺序是：

1. 简化版 NSGA-II
2. 再考虑 MOEA/D
3. Two_Arch2 作为课堂案例理解和报告讨论

原因：

- NSGA-II 资料最成熟
- 好实现
- 最容易 debug
- 对课程汇报也足够成立

## 第 7 步：你要记录什么日志
不要只保存最终关卡。

建议每代至少记录：

1. generation id
2. feasible ratio
3. best difficulty_error
4. best structural_diversity
5. best emptiness
6. Pareto front size
7. representative chromosomes

业务意义：

- 你不是只想展示“最后一关”
- 你要展示“搜索过程确实在优化”

## 第 8 步：每周交付什么
### 第 1 周
目标：

- 接口冻结
- 手写 chromosome 能完整通过 decode -> check -> evaluate -> render

### 第 2 周
目标：

- 单目标 EA 跑通
- mutation / crossover 稳定
- 能观察到指标改善

### 第 3 周
目标：

- 多目标版跑通
- 能输出一组 Pareto levels

### 第 4 周
目标：

- 做消融实验
- 做可视化和报告图

## 第 9 步：你现在最容易踩的坑
### 坑 1
还没定接口就先写算法。

结果：

- decode 一改，算法全崩

### 坑 2
目标太多。

结果：

- 指标互相打架
- 很难解释结果

### 坑 3
把不可行解直接混进正常排序。

结果：

- population 里很多垃圾图
- 搜索效率很差

### 坑 4
只看最终最好关卡，不看过程。

结果：

- 你没法证明 EA 真有效

## 第 10 步：你这一侧的最小待办
你可以直接按这个列表开工：

1. 和同学确认 [MARIO_EA_INTERFACE.md](/Users/liuzhicheng/1data/workspace2026/LN-projs/EA-Lab/sample/A8/MARIO_EA_INTERFACE.md)
2. 拿到 `decode()` 的最小实现
3. 拿到 `check_constraints()` 的最小实现
4. 拿到 `evaluate()` 的最小实现
5. 写 random initialization
6. 写 mutation
7. 写 crossover
8. 写 feasible-first selection
9. 先做单目标基线
10. 再切到多目标

## 最后的建议
你这个阶段最重要的交付物不是“复杂算法”，而是：

- 一个稳定的搜索接口
- 一个能跑通的最小 EA 闭环

只要这两个完成，后面换算法框架是增量工作，不是重做。
