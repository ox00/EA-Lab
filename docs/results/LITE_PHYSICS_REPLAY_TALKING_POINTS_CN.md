# Lite Physics Replay 讲稿提纲（CN）

## 1. 这一页要回答什么问题
这一页不是为了证明“我们做了一个完整马里奥游戏引擎”，而是为了回答一个更具体的问题：

`我们的可玩性验证，是否比纯粹的 tile-level reachable 更有说服力？`

答案是：`是。`

因为我们现在把可玩性证据分成了两层。

## 2. 两层可玩性证据
### 2.1 Constraint-Level Evidence
第一层是 `Reachability Replay`。

它对应的是我们 EA pipeline 里的硬约束检查：

`chromosome -> decode -> constraint check -> evaluate -> evolve`

这里的 `reachable` 是 tile-level 的简化可达性规则。
它证明的是：

- 起点和终点是有效的
- 角色存在一条可站立路径到达终点
- 这个判断与 EA 的 feasibility gate 完全一致

它的优点是：

- 快
- 稳定
- 与优化流程直接对齐

它的局限是：

- 不检查完整跳跃轨迹上的碰撞
- 对管道、砖块、墙体的阻挡表达不够强

### 2.2 Lite-Physics-Level Evidence
第二层是 `Lite Physics Replay`。

它在浏览器端加入了一个轻量动作规划器：

- 有角色位置与速度状态
- 有重力
- 有跳跃速度
- 有地面/管道/砖块/问号块碰撞
- 有动作集合：`R / RR / RJ / J / N`

这层证明的是：

- 不是只看“落点可达”
- 而是在一套明确的 lightweight physics 下，能找到一条动作序列走到终点

所以它的说服力高于 constraint-level replay。

## 3. 为什么不直接做 full Mario physics
原因很直接：

- 对课程项目来说实现成本高
- 与当前 MVP 的研究重点不完全一致
- 会把工程重心从 EA representation / constraints / objective design 转移走

所以我们选择了一个更合理的中间层：

`lite physics + action planning`

这个方案的价值是：

- 比 tile-level replay 更真实
- 比 full physics agent 更轻量
- 足够服务课程展示和项目论证

## 4. Lite Physics Plan 是什么
我们现在会为每个代表性关卡导出一个 `Lite Physics Plan`。

导出的内容包括：

- `plan_found`
- `action_count`
- `estimated_seconds`
- `action_counts`
- `actions`

举例来说，一条 plan 可能是：

`RR RR RR RJ RR RR RR RJ ...`

它表示：

- `RR`：持续向右跑
- `RJ`：向右跑并起跳
- `J`：原地跳
- `N`：短暂停顿

这就把“可通过”从抽象判断，变成了可以展示的动作证据。

## 5. 这一页怎么讲
推荐讲法：

1. 先说我们不是只做了静态地图展示。
2. 然后说当前项目把可玩性证据拆成两层。
3. 第一层是 constraint-level，对应 EA 的 feasibility gate。
4. 第二层是 lite-physics-level，对应更强的动作可执行证据。
5. 最后强调：这已经足够支撑课程项目中的“可玩性展示与方法论解释”。

## 6. 建议配图
建议在 PPT 里放三块内容：

1. 左侧：关卡截图
2. 中间：浏览器 replay 截图，带动作 HUD
3. 右侧：Lite Physics Plan 摘要

右侧摘要建议只放：

- `plan_found = true`
- `action_count = xx`
- `estimated_seconds = xx`
- 一小段代表性动作序列

不要整段把全部动作贴上去，否则信息密度过高。

## 7. 汇报时的结论句
可以直接使用下面这句：

`Our project does not stop at tile-level reachability. We further added a lightweight physics replay layer, so the final showcase demonstrates not only feasibility under hard constraints, but also executable action-level traversal under collision-aware browser physics.`

中文版可说：

`我们的项目没有停留在 tile-level 的 reachable 判断上，而是进一步增加了 lite physics replay。因此最终展示的不只是硬约束下的可行性，还包括一条在碰撞感知轻量物理下可执行的动作路径。`

## 8. 这部分在整个项目中的定位
这部分不是新的核心算法贡献，而是：

- 对 EA feasibility 的解释层补强
- 对最终展示效果的可信度补强
- 对 report 和 presentation 的证据链补强

也就是说，它非常适合作为课程项目收尾阶段的“展示增强模块”。
