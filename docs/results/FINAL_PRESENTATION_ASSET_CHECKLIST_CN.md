# 最终汇报截图与素材清单（CN）

## 1. 文档目的
本文档用于准备最终汇报时所需的截图、图表、页面素材和备用材料。

目标是两件事：

1. 保证 PPT 制作时知道该截什么
2. 保证现场演示时知道该开哪些页面

## 2. 核心展示素材
### 2.1 Pipeline 图
用途：解释系统整体流程。

建议素材：
- `docs/analysis/A8/MARIO_PCG_PIPELINE_DIAGRAM.md`

### 2.2 Frontier Browser 首页截图
用途：说明系统不仅能出图，还能比较不同 objective mode。

建议截图内容：
- 左侧 case list
- 顶部 compare summary
- best level 主视图

路径：
- `docs/results/frontier-browser/index.html`

### 2.3 三组代表 case 截图
用途：解释三条实验主线。

建议分别截图：
- `core_3obj_seed7`
- `family_4obj_seed27`
- `curve_4obj_seed27`

每组建议截：
- best level render
- metrics card
- family sequence / difficulty tiers

### 2.4 Replay 证据截图
用途：展示可玩性证据分层。

建议截图两种：
- `Reachability Replay`
- `Lite Physics Replay`

`Lite Physics Replay` 截图时建议保留 HUD：
- 当前动作
- 动作进度
- plan progress

### 2.5 Lite Physics Plan 摘要
用途：说明 replay 不是动画，而是动作计划证据。

建议素材：
- `docs/results/frontier-browser/lite_physics_plans.txt`
- 或浏览器页面中的 `Lite Physics Plan` 面板

PPT 中不建议贴整段动作，只建议摘取：
- `plan_found = true`
- `action_count`
- `estimated_seconds`
- 一段 10~16 个动作的代表性片段

## 3. 推荐最终 PPT 图文对应关系
### Page A: 问题定义
建议素材：
- 一张 Mario level 图
- 一句项目定义

### Page B: Pipeline
建议素材：
- pipeline 图

### Page C: Representation + Constraints
建议素材：
- chromosome 示例
- constraint 列表

### Page D: Objectives + NSGA-II
建议素材：
- objective 列表
- frontier 概念图或 compare summary

### Page E: 三组代表 case
建议素材：
- 三张 best level 图
- 三组关键指标对照

### Page F: Frontier Browser
建议素材：
- 浏览器总览截图

### Page G: Replay Evidence
建议素材：
- Reachability Replay 截图
- Lite Physics Replay 截图
- Lite Physics Plan 摘要

### Page H: Conclusion
建议素材：
- 项目阶段成果总结
- future work

## 4. 现场演示建议打开的文件
1. `docs/results/frontier-browser/index.html`
2. `docs/results/FINAL_DEMO_GUIDE_CN.md`
3. `docs/results/LITE_PHYSICS_REPLAY_TALKING_POINTS_CN.md`
4. `docs/results/frontier-browser/lite_physics_plans.txt`

## 5. 备用材料
如果老师追问技术细节，可备用：

1. `docs/analysis/A8/REPORT_WORKING_DRAFT.md`
2. `docs/analysis/A8/MARIO_EVALUATION_SPEC_EN.md`
3. `docs/analysis/A8/V31_FAMILY_OBJECTIVE_REVIEW_2026-04-21_CN.md`
4. `docs/analysis/A8/V32_CURVE_OBJECTIVE_REVIEW_2026-04-22_CN.md`
5. `docs/analysis/A8/AI_SEEDED_REPAIRED_REVIEW_2026-04-24_CN.md`

## 6. 最终检查项
汇报前建议逐项确认：

- browser 页面能本地直接打开
- `Lite Physics Replay` 能正常播放
- HUD 能显示当前动作和进度
- `Lite Physics Plan` 面板有内容
- 三组代表 case 都能切换
- 关键截图都已保存
- PPT 中不要放太长动作串
- 结论页要强调“可控、可解释、可展示”
