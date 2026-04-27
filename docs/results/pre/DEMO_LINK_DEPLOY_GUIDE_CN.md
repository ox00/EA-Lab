# 演示链接部署说明（GitHub Pages vs Google Sites）

## 1. 这份文档要回答什么
你们最终演示时，希望 `frontier-browser` 不是本地文件，而是一个可以直接点击打开的链接。

这里主要回答三件事：

1. GitHub Pages 和 Google Sites 哪个更适合当前项目
2. 从你们现在的代码结构出发，哪种操作最省事
3. 具体怎么做

## 2. 结论先说
### 推荐方案
`优先使用 GitHub Pages`

### 原因
因为你们当前的演示层本质上就是一套静态站点：

- `index.html`
- `app.js`
- `styles.css`
- `browser_data.js/json`
- `lite_physics_plans.js/json/txt`
- assets 图片和 txt

GitHub Pages 天然就是为这种内容准备的。

## 3. 为什么 GitHub Pages 更适合
### 3.1 它直接吃仓库里的静态文件
GitHub Pages 可以直接从 GitHub 仓库发布 HTML / CSS / JavaScript 静态站点。

对于你们现在这种：

`docs/results/frontier-browser/`

非常合适。

### 3.2 它和代码仓天然一致
你们不需要：

- 手工复制页面到别的平台
- 再做二次嵌入
- 再维护另一套站点内容

只要仓库更新，Pages 可以一起更新。

### 3.3 它更像“项目演示链接”
老师或同学点开后，看到的是你们项目本身的网页。

而不是：

- 一个 Google Sites 容器
- 再嵌一个外链网页

从项目感和专业感上，GitHub Pages 更自然。

## 4. 为什么 Google Sites 不是优先方案
Google Sites 当然能用，但更适合：

- 做课程展示主页
- 聚合多个链接
- 加说明文字、截图、视频

它不太适合当你们核心 demo 的主承载层。

### Google Sites 的局限
1. 你们现在的 demo 不是 Google 文档式内容，而是完整静态网页
2. Google Sites 往往是“外层容器”
3. 如果用嵌入方式，体验通常不如直接打开原始站点
4. 某些嵌入内容可能受到外部站点策略影响

所以更合理的关系应该是：

- `GitHub Pages` 负责承载 demo
- `Google Sites` 只在你们确实需要“课程展示主页”时作为外层导航页

## 5. 从当前仓库结构看，最方便的发布方式
你们现在仓库里已经有 `docs/` 目录。

如果用 GitHub Pages，从仓库角度最顺的方式就是：

`Publish from branch -> main branch -> /docs folder`

这样发布根目录会是 `docs/`。

那么当前浏览器页面的最终路径就会是：

`https://ox00.github.io/EA-Lab/results/frontier-browser/`

注意这里没有 `docs/`，因为 `docs/` 会变成 Pages 的发布根。

## 6. GitHub Pages 的具体操作步骤
### Step 1. 确认仓库权限
需要你对仓库有管理权限。

### Step 2. 打开仓库设置
GitHub 仓库页面：

`EA-Lab -> Settings -> Pages`

### Step 3. 选择发布源
在 Pages 设置里：

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`

保存。

### Step 4. 等待发布
GitHub 会生成一个 Pages 链接。

项目站点默认类似：

`https://ox00.github.io/EA-Lab/`

因为你们页面在 `docs/results/frontier-browser/index.html`，所以最终入口通常是：

`https://ox00.github.io/EA-Lab/results/frontier-browser/`

### Step 5. 打开检查
重点检查：

1. 页面是否能打开
2. CSS 是否正常加载
3. browser data 是否正常加载
4. 图片和 txt 是否都能访问
5. `Lite Physics Replay` 是否正常播放

## 7. 对当前项目的一个小提醒
你们的页面已经做了 inline ascii fallback，这很好。

但 GitHub Pages 发布后，仍建议检查：

1. 相对路径是否全部正常
2. `browser_data.js`
3. `lite_physics_plans.js`
4. `assets/...` 下图片路径

因为 Pages 下 URL 根会和本地文件模式不同。

## 8. 是否需要 Google Sites
### 如果只是要一个可点击演示链接
`不需要。GitHub Pages 就够了。`

### 如果还想要一个“课程展示主页”
那可以后面再做 Google Sites，作为一个目录页：

- 项目简介
- Proposal PDF
- Report PDF
- GitHub 仓库链接
- GitHub Pages demo 链接
- 视频链接

这种情况下 Google Sites 是补充层，不是主 demo 层。

## 9. Google Sites 的最简单用法
如果未来你们真想做 Google Sites，可以这样：

1. 新建 Google Sites
2. 写一页项目简介
3. 放按钮：
   - GitHub repo
   - Report PDF
   - GitHub Pages demo
4. 如果需要，也可以尝试 Embed 外部网页

但即便这样，我仍建议：

`真正的 interactive demo 链接，还是直接指向 GitHub Pages。`

## 10. 推荐最终方案
### 最简方案
1. 用 GitHub Pages 发布 `docs/`
2. 演示入口直接发：
   - `https://ox00.github.io/EA-Lab/results/frontier-browser/`

### 稍完整方案
1. GitHub Pages 发布 demo
2. Google Sites 作为课程展示主页
3. Google Sites 上再放 GitHub Pages 链接

## 11. 对你们现在项目的实际建议
基于当前项目状态，我建议：

`先做 GitHub Pages，不要先做 Google Sites。`

原因很简单：

- 你们真正要演示的是静态网页 demo
- GitHub Pages 路径和代码仓最一致
- 工作量最小
- 后续维护最省事

Google Sites 可以做，但应该排在后面，而且只在你们确实需要“聚合主页”的时候再做。
