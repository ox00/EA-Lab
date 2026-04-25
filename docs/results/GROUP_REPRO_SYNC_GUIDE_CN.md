# 组内复现与同步说明（CN）

## 1. 这份文档是给谁看的
这份文档主要给项目组同学使用。

目标不是讲完整技术细节，而是帮助大家快速完成三件事：

1. 知道这个项目现在做到哪里了
2. 知道仓库里先看什么、后看什么
3. 知道如果要本地复现，最小应该怎么跑

## 2. 项目当前一句话状态
当前项目已经完成一个可运行、可解释、可展示的 Mario PCG 课程项目原型。

它的核心流程是：

`chromosome -> decode -> constraint check -> evaluate -> evolve -> render -> browser demo`

当前从课程项目角度，系统已经基本收口，后续重点应转向：

- 最终汇报材料整理
- PPT 制作
- 演示彩排
- 少量展示层 polish

而不是继续大规模改算法。

## 3. 组内快速理解建议顺序
如果是第一次同步项目，建议按下面顺序看。

### Step 1. 先看最终演示说明
文件：
- `docs/results/FINAL_DEMO_GUIDE_CN.md`

作用：
- 快速知道项目想怎么讲
- 知道三组代表 case 是什么
- 知道老师最终应该看到什么

### Step 2. 再看最终浏览器演示
入口：
- `docs/results/frontier-browser/index.html`

作用：
- 直接看到当前最完整的最终展示层
- 看不同 objective mode 的代表 case
- 看 best level / frontier / replay / lite physics plan

### Step 3. 再看 docs 导航
文件：
- `docs/README.md`

作用：
- 知道仓库中文档的结构
- 知道 `analysis / results / ref / archive` 分别放什么

### Step 4. 如果要理解方法，再看 analysis/A8
建议先看：
- `docs/analysis/A8/analysis.md`
- `docs/analysis/A8/MARIO_PCG_PIPELINE_DIAGRAM.md`
- `docs/analysis/A8/MARIO_EA_INTERFACE_EN.md`
- `docs/analysis/A8/MARIO_EVALUATION_SPEC_EN.md`

## 4. 当前项目的核心结构怎么理解
### 4.1 代码层
主要代码在：
- `src/ea_lab/pcg/`

重要模块：
- `segments.py`: segment library
- `decode.py`: chromosome -> level
- `constraints.py`: hard feasibility check
- `evaluation.py`: objective evaluation
- `ea.py`: EA / selection / logging
- `nsga2.py`: NSGA-II search
- `demo.py`: 命令行运行入口
- `render.py`: ascii / pygame render
- `ai_seed.py`: AI seeded initialization bridge

### 4.2 脚本层
主要脚本在：
- `scripts/`

常见入口：
- `scripts/run-mvp.sh`
- `scripts/run-baseline-compare.sh`
- `scripts/run-parameter-scan.py`
- `scripts/run-ai-seeded-compare.py`
- `scripts/build-frontier-browser-data.py`

### 4.3 文档层
主要文档在：
- `docs/analysis/`: 方法、实验、设计文档
- `docs/results/`: 最终展示与汇报材料
- `docs/ref/`: 课堂材料与参考资料
- `docs/archive/`: 早期 topic analysis

## 5. 如果只想看最终展示，应该看什么
最重要的展示入口只有两个：

1. `docs/results/frontier-browser/index.html`
2. `docs/results/FINAL_DEMO_GUIDE_CN.md`

浏览器页面里当前已经包括：

- 三组代表性 case
- Compare Summary
- Best Level render
- Frontier Members
- Reachability Replay
- Lite Physics Replay
- Lite Physics Plan 摘要

说明：
- `Reachability Replay` 对应 hard constraint 中的 tile-level reachable
- `Lite Physics Replay` 是更强一层的 collision-aware action replay

## 6. 最小复现怎么跑
### 6.1 先确认环境
建议本地有：
- `python3`
- 如需图片渲染，安装 `pygame`

如果没有 `pygame`，也可以先跑 ascii 输出。

### 6.2 跑最小 MVP
命令：

```bash
bash scripts/run-mvp.sh
```

作用：
- 跑一个最小 Mario PCG demo
- 输出结果到默认目录

### 6.3 跑 baseline 对照
命令：

```bash
bash scripts/run-baseline-compare.sh
```

作用：
- 跑 `ea` 和 `nsga2` 的基础对照
- 默认使用多个 random seeds
- 汇总 compare summary

### 6.4 手动跑单次 demo
命令模板：

```bash
PYTHONPATH=src python3 -m ea_lab.pcg.demo \
  --algorithm nsga2 \
  --nsga2-objective-mode curve_4obj \
  --seed 27 \
  --generations 12 \
  --population-size 30 \
  --render-backend both \
  --output-dir output/pcg/manual_test
```

说明：
- `--algorithm`: `ea` 或 `nsga2`
- `--nsga2-objective-mode`: `core_3obj / family_4obj / curve_4obj / semantic_5obj`
- `--render-backend`: `ascii / pygame / both`

### 6.5 重建浏览器展示数据
如果输出目录有更新，想刷新 `frontier-browser` 展示数据：

```bash
python3 scripts/build-frontier-browser-data.py
```

作用：
- 复制展示所需图片和文本
- 重建 `browser_data.json/js`
- 重建 `lite_physics_plans.json/js/txt`

## 7. 当前最终展示推荐看哪三组
当前最终展示主视图以三组代表性 case 为主：

1. `core_3obj_seed7`
2. `family_4obj_seed27`
3. `curve_4obj_seed27`

这三组的意义分别是：

- `core_3obj`: baseline capability
- `family_4obj`: family balance / structure semantics
- `curve_4obj`: difficulty curve / pacing semantics

如果同学做汇报准备，优先围绕这三组理解项目，不需要先从所有历史实验开始看。

## 8. 当前项目中 AI 模块怎么理解
仓库里已经有 AI generator 模块和 AI seeded integration。

但从当前课程项目主线看，最稳的理解方式是：

- 主线系统仍然是 `explicit genotype + hard constraints + EA / NSGA-II`
- AI 更像是“上游 seed initialization 扩展能力”
- 不是最终主展示的唯一核心

所以组内同步时不要把项目误解成“一个纯 AI 生成项目”。

更准确的表达应该是：

`这是一个以 EA / MOO 为核心的 Mario PCG 项目，AI 模块是可以接入的上游增强能力。`

## 9. 组内分工视角怎么对齐
如果从协作角度理解，当前可以把项目拆成四层：

1. 生成表示层
   - genotype / segment library / decode
2. 搜索优化层
   - EA / NSGA-II / objective modes
3. 展示解释层
   - render / frontier browser / replay
4. 汇报表达层
   - report / demo guide / ppt materials

这样分层以后，同学更容易知道自己负责部分处在整个项目中的什么位置。

## 10. 当前最值得同学重点阅读的文件
如果时间有限，优先看下面这些：

1. `docs/results/FINAL_DEMO_GUIDE_CN.md`
2. `docs/results/frontier-browser/index.html`
3. `docs/results/PPT_OUTLINE_CN.md`
4. `docs/results/LITE_PHYSICS_REPLAY_TALKING_POINTS_CN.md`
5. `docs/analysis/A8/analysis.md`
6. `docs/analysis/A8/MARIO_PCG_PIPELINE_DIAGRAM.md`

## 11. 当前项目的最终展示层里，新增了什么
这部分是最近迭代的重点。

浏览器展示层里现在新增了：

- 内嵌 renderer
- Auto-Scroll
- Reachability Replay
- Lite Physics Replay
- Lite Physics Plan export
- Replay HUD

它们的作用不是单纯“好看”，而是增强最终演示的可信度与可解释性。

## 12. 如果同学只需要项目同步结论，可以直接记住这几句
### 项目定位
`这是一个以 explicit genotype、hard constraints 和 multi-objective EA / NSGA-II 为核心的 Mario PCG 项目。`

### 当前状态
`项目已经完成可运行、可解释、可展示的课程项目闭环。`

### 目前重点
`当前重点不是继续大改算法，而是准备最终汇报与展示。`

### 最终展示入口
`先看 docs/results/frontier-browser/index.html。`

## 13. 当前阶段建议组内怎么协作
建议按照下面方式推进：

1. 所有人先统一阅读最终演示说明与浏览器展示
2. 再根据分工补 PPT / 报告 / 彩排材料
3. 非必要不要继续引入大规模算法改动
4. 如果要补内容，优先补展示、表达和截图质量

## 14. 最后一条提醒
当前仓库里材料很多，但并不是所有内容都要一次性读完。

组内同步最重要的是先建立一个共同认知：

`我们已经有一个完整的课程项目主线，后面工作的重点是把它讲清楚、演示好，而不是再重新定义项目。`
