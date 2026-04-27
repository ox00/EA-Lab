# 3 分钟 Pre 节奏建议（EA + 演示部分）

## 1. 你的定位
你在 pre 里的重点是：

1. EA / NSGA-II 这一条主线
2. 最终演示层

总时长大约 3 分钟，所以不适合铺太多技术细节，也不适合从头讲所有实验历史。

你的目标应该是：

`用最短时间，让老师知道这个项目的核心方法、你负责的关键价值，以及最终演示为什么可信。`

## 2. 3 分钟应该怎么分配
建议节奏：

1. `0:00 - 0:35` 项目一句话定义 + pipeline
2. `0:35 - 1:25` EA / NSGA-II 主线
3. `1:25 - 2:20` objective progression + case difference
4. `2:20 - 3:00` frontier browser + replay evidence

## 3. 推荐分享顺序
### Part 1. 先讲一句话定义
建议开场：

`Our project builds a Mario PCG pipeline based on explicit genotype, hard feasibility constraints, and multi-objective evolutionary search.`

中文可理解为：

`我们的项目是一个基于显式基因表示、硬约束和多目标进化搜索的 Mario 关卡生成系统。`

这一句的作用是先把老师的注意力放到正确主线上。

### Part 2. 再讲 EA 主线
建议紧接着讲：

`My focus is the EA side: we define a segment-based chromosome, decode it into a level, filter infeasible levels with hard constraints, and then use NSGA-II to search for better trade-off solutions.`

这里的关键词只要老师听到就够了：

- chromosome
- decode
- hard constraints
- NSGA-II
- trade-off solutions

### Part 3. 再讲为什么不是单一目标
建议口径：

`This problem does not have one single best level. We need to balance difficulty control, structural diversity, layout density, and later semantic objectives such as family balance and difficulty curve quality.`

这一步的目标是回答：

`为什么要用 NSGA-II，而不是简单打分排序`

### Part 4. 再讲三组代表 case
你不需要讲很多历史实验，只要讲三组就够：

1. `core_3obj`
2. `family_4obj`
3. `curve_4obj`

建议说法：

`These three representative runs show our project progression: baseline feasibility, structural semantic control, and pacing control.`

这句话很关键，因为它把实验讲成一条主线，而不是一堆结果。

### Part 5. 最后讲演示层
你最后 40 秒左右，建议直接切到 browser 页面。

重点讲两件事：

1. frontier browser 让 Pareto trade-off 变得可见
2. replay 让 playability evidence 更可信

建议说法：

`The browser is not just a visualization layer. It is our interpretation layer. It lets us compare different objective modes, inspect frontier members, and present layered playability evidence.`

然后再补一句：

`We show both reachability replay and lite physics replay, so the final demo goes beyond static level screenshots.`

## 4. 你这 3 分钟里不要做什么
### 不要做的 1
不要把大量时间花在 LSTM 训练细节上。

原因：
- 这不是你 3 分钟的最强价值点
- 会冲淡 EA 主线

### 不要做的 2
不要讲太多实现参数。

例如：
- hidden size
- dropout
- optimizer schedule

这些适合问答，不适合你 3 分钟主讲。

### 不要做的 3
不要把 `AI seeded` 讲成整个项目主角。

更准确的说法应该是：

`AI seeded initialization is an upstream extension, while the core project contribution lies in the hard-constrained multi-objective PCG pipeline.`

## 5. 推荐的实际口播版本
下面是一版更接近你可直接讲的英文节奏。

### 版本（约 3 分钟）
`Our project builds a Mario procedural content generation pipeline based on explicit genotype, hard feasibility constraints, and multi-objective evolutionary search.`  

`My main responsibility is the EA side. We represent each level as a fixed-length chromosome of segment IDs, decode it into a level grid, filter invalid levels with hard constraints, and then use NSGA-II to search for better trade-off solutions.`  

`The reason we use multi-objective optimization is that Mario level design does not have a single best answer. We need to balance difficulty control, structural diversity, emptiness balance, and later semantic objectives such as family balance and difficulty curve quality.`  

`To explain the system progression clearly, we focus on three representative runs: core_3obj, family_4obj, and curve_4obj. They show how the project evolves from baseline feasibility, to structure control, and then to pacing control.`  

`Finally, we present the outputs through an interactive frontier browser. This is not just for visualization; it is our interpretation layer. It allows us to inspect Pareto frontier candidates, compare objective modes, and show layered playability evidence through both reachability replay and lite physics replay.`  

`So the final contribution is not simply generating a Mario-like map, but building a controllable, explainable, and presentation-ready PCG system.`  

## 6. 如果你是中文讲
中文建议节奏：

1. 先一句话定义项目
2. 讲你负责 EA 主线
3. 讲为什么必须多目标
4. 讲三组代表 case
5. 讲 browser 和 replay 是最终解释层

最后一句可以这样收：

`所以我们这个项目最后最重要的价值，不是生成了一张 Mario 图，而是建立了一套可控、可解释、可展示的关卡搜索系统。`

## 7. 你和同学之间的节奏衔接建议
如果你前面有人讲背景或 AI 部分，你接的时候建议用：

`Based on that setup, my part focuses on the EA pipeline and the final demo evidence.`  

如果你后面还有同学讲总结或 future work，你收尾时建议用：

`I will stop here and pass to the next part for the broader conclusion and future directions.`  

## 8. 这 3 分钟里你最该强调的关键词
老师如果最后只记住几个词，我建议是这几个：

- explicit genotype
- hard constraints
- NSGA-II
- Pareto frontier
- semantic objectives
- layered replay evidence

这几个词基本就能把你的部分定住。
