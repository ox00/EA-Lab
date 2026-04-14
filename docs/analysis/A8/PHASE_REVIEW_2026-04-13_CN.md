# A8 阶段性回顾（2026-04-13）

## 1. 当前 Pipeline 状态
当前工程链路已经可执行并可复现实验：

`chromosome -> decode -> check_constraints -> evaluate -> evolve -> render -> artifacts`

已落地能力：

1. 基因编码与解码：段级别 chromosome 可稳定映射为关卡网格。
2. 可行性硬约束：start/goal/reachable/max-gap 等检查已接入筛选。
3. 目标评估：difficulty/diversity/emptiness balance 已结构化输出。
4. 算法层：已支持 `EA` 与 `NSGA-II` 两条搜索路径。
5. 演示层：支持 ASCII 与 Pygame 渲染导出。
6. 产物层：每次运行都会输出配置、日志、摘要，便于回放。

结论：项目从“能跑通”进入“可对照实验”阶段。

## 2. Baseline 对照方法（本次）
对照原则：只比较算法，不改变其他条件。

固定参数：

1. 地图规模与约束参数固定。
2. 进化预算固定：`population_size=30`, `generations=20`。
3. 种子固定：`7, 17, 27, 37, 47`。
4. 渲染模式固定为 `ascii`（不影响优化结果）。

对照算法：

1. `ea`
2. `nsga2`

自动化脚本：

1. `scripts/run-baseline-compare.sh`
2. `scripts/summarize-baseline.py`

输出文件：

1. `output/pcg/baseline_compare/compare_summary.json`
2. `output/pcg/baseline_compare/compare_summary.csv`
3. `output/pcg/baseline_compare/compare_summary.md`

## 3. 本次结果（5 seeds 平均）

1. EA: `difficulty_error=0.3850`, `diversity=0.2750`, `emptiness_error=0.4119`, `best_feasible_ratio=1.0`
2. NSGA-II: `difficulty_error=0.4475`, `diversity=0.3375`, `emptiness_error=0.4025`, `best_feasible_ratio=1.0`

解释：

1. EA 更容易把解压到目标难度附近（difficulty_error 更低）。
2. NSGA-II 在结构多样性上更优（diversity 更高）。
3. NSGA-II 在 emptiness balance 上也略优（emptiness_error 更低）。
4. 两者可行性都稳定，说明硬约束和解码链路基本可靠。
5. 两者的原始 emptiness 都偏高，说明当前 segment library 整体仍偏空。

## 4. 当前阶段判断
项目阶段可定义为：

`MVP-B（可复现实验基线）`

已经完成：

1. 端到端工程闭环。
2. 算法可切换对照。
3. 多 seed 自动批跑与指标汇总。

尚未完成（当前主要短板）：

1. NSGA-II 的“解集质量”评估还不完整（缺少 hypervolume / spacing 等 Pareto 指标）。
2. 报告口径仍以“单最佳个体”指标为主，尚未充分体现 MOEA 的前沿优势。
3. 缺少统计显著性检验（例如 Mann-Whitney U）支撑“算法优劣”结论强度。

## 5. 下一步方向（建议顺序）

1. 先补 MOEA 指标：新增 Pareto front size、hypervolume、spread。
2. 增加实验矩阵：把 `population_size` 与 `mutation_rate` 做小网格扫描（低成本）。
3. 固化汇报模板：结果统一输出为“表 + 图 + 结论三句式”。
4. 再考虑扩展：引入 AI 作为初始化或修复算子，不替代现有基线。

执行顺序建议：

1. 本周先完成第 1 和第 2 项，形成可答辩数据面。
2. 下周再做第 3 和第 4 项，提升展示和拓展空间。

## 6. 对老师汇报的简版口径
本阶段核心产出不是“最强结果”，而是“可信实验系统”：

1. 同一问题定义下可复现实验。
2. 同一预算下可横向比较算法。
3. 已识别不同算法的优势方向和下一步验证路径。
