# Mario Report 逐节对照修改清单

这份文档用于把 [docs/Mario.pdf](../Mario.pdf) 和当前新稿做逐节对照，方便后续直接整合到最终提交版里。

对照对象：
- 旧稿底稿：[Mario_extracted_for_edit.md](Mario_extracted_for_edit.md)
- 近终稿英文正文：[MARIO_REPORT_PASTE_READY_EN-final.md](MARIO_REPORT_PASTE_READY_EN-final.md)
- 完整修订版草稿：[MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md](MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md)

## 1. 先说整体变化
旧稿本身不是结构有问题，主要是叙事重心偏前了。

旧稿读下来更像：
- `VGLC -> LSTM -> AI seeds -> NSGA-II refinement`

这轮改完后的主线是：
- `explicit genotype -> deterministic decode -> hard constraints -> NSGA-II multi-objective search -> browser/replay evidence`
- `AI-seeded initialization` 保留，但回到“真实接入的上游增强模块”这个位置

所以这里的改法不是弱化 AI，而是把它放回更合适的位置，让整篇 report 更贴近项目真实重心。

## 2. 标题
### 旧稿
`Mario Level Generation via Multi-Objective Evolutionary Search with Data-Driven Initialization`

### 当前建议
`Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search with AI-Seeded Initialization`

### 调整原因
这次标题主要做了两件事：
- 加上 `Hard-Constrained`，把项目最扎实的骨架直接写出来
- 保留 `AI-Seeded Initialization`，但放在后面，避免整篇报告一上来就被理解成 “主要是 data-driven init”

## 3. Abstract
### 旧稿的问题
旧摘要本身是通顺的，但句子顺序会把读者注意力先带到：
1. VGLC
2. LSTM
3. AI seeds
4. NSGA-II refinement

这样读者很容易先形成一个印象：
`这是一个 AI 初始化为主、EA 作为后处理的项目。`

### 当前版本的改法
摘要现在改成：
1. 先定义 Mario PCG 的多目标问题
2. 再讲主系统：显式基因型、确定性 decode、硬约束、NSGA-II
3. 再讲 AI seeded integration
4. 再讲实验结论
5. 最后讲 browser + replay 展示层

### 整合时建议
摘要里不要放太多 LSTM 训练细节。对最终报告来说，更重要的是让人一眼看明白：
- 系统是什么
- AI 接在什么位置
- 方法上最有价值的点是什么
- 最后的展示证据是什么

## 4. Introduction
### 旧稿的问题
旧稿 Introduction 更像从 “以前多是 random init，所以我们做 data-driven init” 这个角度切入。

这个切法没有错，但会把重点带到初始化策略，而不是整套 PCG formulation。

### 当前版本的改法
Introduction 现在按下面这个顺序展开：
1. Mario PCG 是一个 constrained multi-objective problem
2. 为什么选择 explicit genotype
3. 为什么 hard feasibility gate 很关键
4. 为什么 NSGA-II 比单一目标更合适
5. AI seeded 是怎么接进来的
6. browser + replay 为什么是最终 interpretation layer

### 整合时建议
这一节的任务是帮读者建立“项目骨架认知”，所以建议优先保留下面几类表述：
- explicit segment-based genotype
- hard feasibility constraints
- progressive objective design
- integrated AI-seeded initialization
- browser and replay as interpretation layer

## 5. Problem Formulation
### 旧稿的问题
这一节框架本来就还可以，问题主要在于定义不够完整，尤其是几个核心指标的“业务含义”和“数学含义”之间还没完全对齐。

### 这轮补强了什么
#### `structural_diversity`
从“一个名字合理的指标”补成“它到底衡量什么结构差异”。

#### `emptiness_error`
从原来偏直觉的 `emptiness` 调整成对目标值的偏差，这样和 difficulty error 的表达方式更一致。

#### `family_balance`
补成更正式的 family usage / repetition 角度定义，而不是只停留在“避免偏科”。

#### `difficulty_curve_error`
补成沿 chromosome 的 difficulty tier 和目标曲线之间的偏差。

#### `feasibility`
明确强调：
`feasibility is a hard gate`

### 整合时建议
这一节建议尽量保留“定义清楚但不过度展开”的写法。报告里把它写成可信的 optimization formulation 就够了，不需要堆太多讲义式说明。

## 6. Method
### 旧稿的问题
旧稿 Method 内容其实不少，但章节顺序读起来仍然更像：
`VGLC -> LSTM -> adapter -> NSGA-II`

这样会让 AI pipeline 看起来像系统主干。

### 当前版本的改法
Method 现在分成三层更清晰：
- core search pipeline
- AI-seeded augmentation
- interpretation layer

展开以后大概是：
1. segment library
2. decode and constraint checking
3. evaluation
4. genetic operators and NSGA-II
5. VGLC extraction and sequence modeling
6. adapter and feasibility-aware repair
7. frontier browser and replay evidence

### 这轮比较关键的两个补强
#### adapter repair
以前更像一句抽象描述，现在明确成：
- invalid ID filtering
- length normalization
- gap-heavy replacement when reachability fails
- safer family preference
- bounded local repair

#### lite physics replay
以前更像“有个 replay 动画”，现在说明了最小动作模型：
- gravity
- jump impulse
- solid collision
- `R / RR / RJ / J / N`

这样它在报告里就更像 evidence layer，而不是单纯 demo 效果。

## 7. Experimental Study
### 旧稿的问题
旧稿实验顺序是：
1. pipeline validation
2. AI-seeded vs random
3. objective progression

主要问题是：AI line 放得太靠前，而 `EA vs NSGA-II` 这条关键对照没有正式进入正文主线。

### 当前版本的改法
现在实验顺序调整成：
1. core pipeline validation
2. EA vs NSGA-II baseline
3. AI-seeded vs random initialization
4. objective progression
5. parameter scan

### 这样调整的原因
这个顺序更贴近项目真实推导：
- 先证明 pipeline 跑通
- 再说明为什么要用 NSGA-II
- 再说明 AI 是怎么接进来的
- 最后再看 semantic objectives 和参数扫描

### 这一节最值得保留的变化
#### EA vs NSGA-II baseline
这一项建议正式保留进最终稿。

它回答的是一个很直接的问题：
`既然最后用了 NSGA-II，那它相对普通 EA 的增益到底是什么？`

#### AI 实验定位
这一块现在改成了更稳的说法：
- AI seeded 是 integrated initialization study
- raw seeds 受 upstream data skew 影响
- repaired seeds 变成可用模式

#### objective progression
这一块其实是方法价值最清楚的一条线：
- `core_3obj`
- `family_4obj`
- `curve_4obj`
- `semantic_5obj` 作为补充

如果报告篇幅有限，这部分建议优先保留。

## 8. Discussion
### 旧稿的问题
旧稿 Discussion 更像总结性备注，和主结论之间的连接还不够紧。

### 当前版本的改法
现在更集中在三件事：
- strengths: closed-loop pipeline, extensible objectives, interpretation layer
- limitations: segment library, AI seed skew, lite physics fidelity
- insight: representation and objective design matter as much as optimizer choice

### 整合时建议
这一节保持克制一点会更合适。把“做成了什么、还有什么限制、从中看到什么方法层面的认识”写清楚就够了。

## 9. Conclusion
### 旧稿的问题
旧稿结论更偏向：
`AI integration worked, but AI seeds are not yet better`

这句话不算错，但它不能代表整个项目最成熟的部分。

### 当前版本的改法
现在结论主语已经换成整套系统：
- explicit segment-based representation
- hard feasibility constraints
- NSGA-II multi-objective trade-off search
- semantic control over family composition and pacing
- AI-seeded initialization as real integrated extension
- frontier browser + replay as final evidence layer

### 整合时建议
结论最好让人记住的是：
`We established a controllable and presentation-ready Mario PCG pipeline.`

这比把结论落在 “我们训了一个 LSTM” 上更符合项目现在的完成度。

## 10. 图表和展示层
### 现有图里建议保留
- VGLC segment frequency
- LSTM training / validation loss

它们的作用主要是证明 AI 线确实有真实工作量和真实接入。

### 更建议强调的展示图
- pipeline figure
- frontier browser screenshot
- lite physics replay screenshot with HUD
- representative level renders

如果版面有限，优先顺序建议是：
1. frontier browser screenshot
2. pipeline figure
3. replay screenshot

## 11. 当前可直接拿来用的文件
### 如果要直接整合英文正文
- [MARIO_REPORT_PASTE_READY_EN-final.md](MARIO_REPORT_PASTE_READY_EN-final.md)

### 如果要看更完整的可裁剪版本
- [MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md](MARIO_REPORT_FINAL_SUBMISSION_DRAFT_EN.md)
- [MARIO_REPORT_REVISED_DRAFT_EN.md](MARIO_REPORT_REVISED_DRAFT_EN.md)

### 如果要快速看这一轮修改的核心思路
- [REPORT_INTEGRATION_HANDOFF_CN.md](REPORT_INTEGRATION_HANDOFF_CN.md)

## 12. 一句话总结
这轮修改的核心不是把 AI 线拿掉，而是把 report 的主叙事调整成：

`This is a hard-constrained multi-objective Mario PCG project with explicit genotype and a real AI-seeded initialization path, rather than an AI generation report with some evolutionary post-processing.`
