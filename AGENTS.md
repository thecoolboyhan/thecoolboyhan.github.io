# AGENTS.md

> **【维护约定 · 写给 AI 协作方】**
> 本文件是本项目的 **AI 交接说明书**。**每次完成修改后，请同步更新本文件中的
> 「项目概述 / 目录结构 / 自定义实现说明 / 修改记录 / 未来计划」等章节**，
> 让后续接手的 AI 或开发者无需重新摸索即可继续工作。
> 本条约定本身也应一直保留在本文件中，不要删除。
>
> **关于开源项目文章**：每个开源项目仓库都有自己的 `AGENTS.md`（记录该项目的更新与修改）。
> 维护对应的博客文章前，请先读取该项目仓库的 `AGENTS.md`——详见下文
> 「开源项目文章的维护约定」。

## 项目概述

- 站点名：**韩永发的博客**，地址 <https://thecoolboyhan.github.io>
- 基于 **Hugo + Stack v4** 主题构建的个人博客，托管于 **GitHub Pages**（GitHub Actions 自动部署）。
- 内容以中文为主，涵盖技术读书笔记、算法题解、架构设计、JVM/并发、账务与金融系统等。
- 在主题基础上做了较多自定义：**精选文章 widget、字体与排版、配色、hint/color shortcode、返回顶部、阅读进度条、访问统计**等。

## 技术栈

- **静态站点生成器**：Hugo **Extended**（本地 v0.166.0，CI 固定 v0.154.2；SCSS 编译必须 Extended）
- **主题**：`CaiJimmy/hugo-theme-stack` **v4**（通过 Hugo Modules 引入，见 `go.mod`、`config/_default/module.toml`）
- **样式**：SCSS，自定义覆盖集中在 `assets/scss/custom.scss`
- **部署**：GitHub Actions → GitHub Pages
- **语言**：中文（`defaultContentLanguage = "zh"`，`hasCJKLanguage = true`）
- **评论**：Giscus
- **脚本**：Python3（`scripts/format_posts.py`）

> ⚠️ **时区坑**：`config.toml` 未设置 `timeZone`，日期依赖构建机时区；CI 中为 `TZ: Europe/Oslo`（starter 遗留）。
> 若出现日期显示异常，请在 `config.toml` 补充 `timeZone = "Asia/Shanghai"`。

## 目录结构（只看自定义/关键部分）

```text
config/_default/
  config.toml            # baseurl / 语言 / 分页（pagerSize）
  params.toml            # 侧边栏、文章、widget、评论等（主要改动文件）
  module.toml            # 引入 Stack 主题
  _languages.toml / menu.toml / markup.toml / permalinks.toml / related.toml
assets/scss/
  custom.scss            # 【全部自定义样式】按编号分节，见文件内注释
layouts/
  _partials/
    widget/featured.html # 【自定义】精选文章 widget
    head/custom.html     # 【自定义】代码字体 JetBrains Mono（jsDelivr CDN）
    footer/custom.html   # 【自定义】品牌渐变条 / 不蒜子统计 / 阅读进度条 / 返回顶部
  shortcodes/
    hint.html            # 【自定义】提示框 {{< hint "tip" >}}
    color.html           # 【自定义】文字颜色 {{< color "red" >}}
  partials/extend-footer.html  # 空占位文件
scripts/format_posts.py  # 文章批量排版 / 错别字修复
.github/workflows/       # deploy.yml（构建部署）、update-theme.yml（每日更新主题）
content/post/            # 文章（中文）
static/                  # 静态资源
```

## 本地运行

```bash
hugo server -D          # 预览：http://localhost:1313/
hugo --quiet            # 构建校验（不启动服务）
```

## 内容规范

- 文章存放于 `content/post/`，按系列或日期组织（部分目录为 page bundle：`index.md` + 图片）。
- **「精选文章」通过 front matter 标记**：当前 35 篇文章在 `categories` 中包含 `精选`；**`tags` 中暂无 `精选`**。
- 可设置 `series: ["系列名称"]` 启用系列关联；`slug` / `permalink` 可固定链接（站内已有多篇使用）。
- **注意**：不写 `slug` 时，文章的 URL 会由**标题**生成（`post = "/p/:slug/"`）。新增文章若希望 URL 干净，请显式设置 `slug`。
- **`content/page/links/index.md`**：开源项目导航页（侧边栏「开源项目」菜单），用 front matter 的 `links` 数组渲染卡片，
  每项支持 `title` / `description` / `website` / `image`（可留空）。已固定 `slug: links` 以保持 `/links/` 地址不变。
- **开源项目官网文章**（均为 page bundle，含仓库真实截图，URL 用显式 `slug`）：
  - `content/post/fishing-funds/index.md` → `/p/fishing-funds/`（`banner.png` + `1~3.png`）
  - `content/post/type-text-injector/index.md` → `/p/type-text-injector/`（`gui-preview.png`）
  - `content/post/xiaomi-watch-s3-diy/index.md` → `/p/xiaomi-watch-s3-diy/`（`preview-banner.png` / `roulette-s3.png` / `minimal-s3.png` / `daynight-day.png` / `daynight-night.png`）
  - `content/post/ai-platform/index.md` → `/p/ai-platform/`（仓库无截图，纯文字）
  - 这几篇同时也是 links 页「主要项目」卡片的落地页。
- 图片建议放文章目录内或 `static/`；主题已开启 imageProcessing。

### 开源项目文章的维护约定（重要）

- 每个开源项目仓库（`thecoolboyhan/<项目名>`）都会维护**自己的 `AGENTS.md`**，其中记录该项目的更新、修改、已知坑与当前状态。
- **维护对应的博客文章前，先读取该项目仓库的 `AGENTS.md`（配合 `README.md` / `CHANGELOG.md`）**，
  据此同步更新文章内容与配图，避免博客文章与项目实际脱节。
- **项目侧仓库的 `AGENTS.md` 是「项目真源」**；本文件只负责记录「文章 ↔ 仓库」的映射与同步约定。
- 文章 ↔ 仓库对应关系（四个仓库均已自带 `AGENTS.md`）：
  - `content/post/fishing-funds/index.md` ↔ <https://github.com/thecoolboyhan/fishing-funds>
  - `content/post/type-text-injector/index.md` ↔ <https://github.com/thecoolboyhan/type-text-injector>
  - `content/post/xiaomi-watch-s3-diy/index.md` ↔ <https://github.com/thecoolboyhan/xiaomi-watch-s3-diy>
  - `content/post/ai-platform/index.md` ↔ <https://github.com/thecoolboyhan/ai-platform>

- **新增开源项目文章时**：按同样结构建 page bundle（`index.md` + 真实截图）+ 显式 `slug`，
  在 `content/page/links/index.md` 加卡片，并**回到本表补一行映射**。
- **项目有更新时**：先在项目仓库更新其 `AGENTS.md` / `CHANGELOG.md`，再回来同步博客文章（正文、版本号、截图、命令）。

## 脚本工具

### `scripts/format_posts.py`

文章批量排版与错别字修复脚本，仅作用于非代码块区域，安全可复现。

```bash
python3 scripts/format_posts.py --dry          # 预览改动（不写文件）
python3 scripts/format_posts.py                # 实际应用修改
python3 scripts/format_posts.py --file content/post/xxx.md   # 只处理单个文件
```

功能：压缩连续空行（最多 1 行）、标题/列表前后补空行、基于词典修复常见错别字（代码块完全保护）。

## 配置要点

- 分页大小：`config/_default/config.toml` 的 `pagerSize`（当前 20）。
- 首页 widget 列表：`config/_default/params.toml` 的 `[[widgets.homepage]]`。
- 评论：Giscus（需仓库开启 Discussions），见 `params.toml` 的 `[comments.giscus]`。
- 代码高亮：Chroma，已配置行号、`tabWidth=4`；代码字体 JetBrains Mono。
- 代码复制按钮文案：`params.toml` 的 `[codeblock]`。

## 自定义功能与关键实现

### 1. 精选文章 widget（`layouts/_partials/widget/featured.html`）

- 在 `params.toml` 中通过 `[[widgets.homepage]] type = "featured"` 启用，参数在 `[widgets.homepage.params]`：
  `title` / `taxonomy` / `term` / `limit` / `groupBy` / `icon` / `showLink` / `uncategorizedName`。
- **取数逻辑**：
  - 优先在 `tags` 中查找 `term`（默认「精选」）；**tags 中没有时回退到 `categories`**。
  - 按日期倒序（`.ByDate.Reverse`）。
  - `limit = 0` 或不填 = **显示全部**；`limit > 0` 才用 `first` 截断。
- **分组（`groupBy`）**：把相关文章排到一起，组标题为分组名。
  - `none`：不分组（纯日期倒序）；`category`（当前默认）：按「第一个非精选分类」分组；
    `series`：按 front matter `series` 分组；`auto`：有 series 用 series，否则用分类。
  - 没有系列/分类的文章归入 `uncategorizedName`（默认「其他」）。
  - 组的先后顺序 = 该组内最新文章的日期顺序；组内按日期倒序。
  - 模板实现：先为每篇算「分组键」，再按出现顺序输出分组（见 `featured.html` 的 `$items` / `$order`）。
- **渲染**：**仅显示文章标题**（已去除封面图与日期）；标题链接到文章，`title` 属性做悬浮提示。
- **样式**：`custom.scss` 第 22 节。固定 `50vh` 高、列表内部滚动（变量 `--featured-box-h`），标题字号 **1.6rem** 且自动换行；
  顶部图标 + 标题用 `.featured-header` 横排（`display:flex` + `align-items:center`）；
  分组样式 `.featured-group` / `.featured-group-title`（组内紧凑、组间留白、标题右侧细分隔线）。

### 2. 字体与排版（重要换算坑）

- 主题 `html { font-size: 62.5% }`，因此 **1rem = 10px**（不是 16px）。
- 参考字号：正文/`body` **1.6rem(16px)**、文章列表标题 **1.8rem(18px)**、普通 widget 文本 **1.4rem(14px)**。
- 在 `custom.scss` 写 `rem` 时务必按此换算，否则会明显偏小（曾出现 1rem=10px 过小的问题）。

### 3. 视觉 / 交互增强（`custom.scss` + `footer/custom.html`）

- 顶部品牌渐变条、阅读进度条、返回顶部按钮（JS 在 `footer/custom.html`）。
- 不蒜子访问统计（国内可用，无需账号）。
- 文章卡片 / 标签胶囊 hover 动画、自定义滚动条、表格 / 引用块 / 代码块美化。
- hint 提示框（`note/info/tip/success/warning/danger`）与文字颜色类（`.text-red` 等）。

### 4. 评论 / 代码

- 评论为 Giscus，配置 `params.toml` 的 `[comments.giscus]`（仓库需开启 Discussions）。
- 代码高亮 Chroma，行号、`tabWidth=4`；代码字体 JetBrains Mono 由 `head/custom.html` 引入。

## 修改记录（Changelog）

### 2026-09-22 · 精选框调整

- `layouts/_partials/widget/featured.html`
  - 移除封面图与日期，**仅保留文章标题**。
  - 取数改为 **tags 优先、categories 回退**；`limit` 语义改为 `0`=全部。
- `config/_default/params.toml`：`taxonomy = "tags"`、`term = "精选"`、`limit = 0`。
- `assets/scss/custom.scss`：精选标题字号 `0.85rem → 1rem → 1.6rem`；取消两行截断，改为自动换行。
- **排查结论**：此前精选框只显示 5 篇，原因是 `limit = 5`，**并非取数错误**（全站 35 篇标记了精选）；改为 `limit = 0` 后全部显示。

### 2026-09-22 · 精选框按分类/系列分组

- 需求：把相关的精选文章排到一起（按系列或分类分布）。
- `featured.html`：新增 `groupBy` 参数（`none` / `category` / `series` / `auto`），按分组键输出 `.featured-group` + 组标题。
- `params.toml`：新增 `groupBy = "category"`。
- `custom.scss`：新增 `.featured-group` / `.featured-group-title` 样式。
- **现状数据**：35 篇精选文章中 **0 篇设置了 `series`**；按 `category` 分组得到 16 组（AI / 架构 / 金融 / 其他 / web3 / 分布式事务 / …），其中「其他」组约 10 篇（这些文章只标了 `精选`，没有其他分类）。
- 已验证 `series` / `none` / `auto` 三种模式均可正常构建（`series` 模式因无数据会全部归入「其他」）。

### 2026-09-22 · 精选框头部图标与标题同行

- `featured.html`：把 `.widget-icon` 与 `h2.widget-title` 包进 `.featured-header`（原来图标独占一行）。
- `custom.scss`：新增 `.featured-header` 横排样式（flex + 居中 + `gap: 0.6rem`），并去掉标题自身额外外边距。

### 2026-09-22 · 新增开源项目官网文章 + 重写 links 页

- **新增** `content/post/fishing-funds/index.md`（`slug: fishing-funds` → `/p/fishing-funds/`）：开源项目 Fishing Funds 的官网文章，
  内容来自仓库 README（简介、独立维护背景、功能、数据源、下载/构建、代理、AI 录入、导入导出、配置同步、技术栈、FAQ、许可证、致谢）。
  配图为仓库 `screenshots/` 下的真实截图，已下载到该 page bundle：`banner.png`（封面）、`1.png`（基金）、`2.png`（指数）、`3.png`（板块）。
- **重写** `content/page/links/index.md`：由 Stack 主题示例内容改为「我的开源项目」导航页，
  收录 13 个自有（非 fork）仓库；固定 `slug: links` 保持 `/links/`；Fishing Funds 卡片指向站内官网文章。
  未收录 fork 仓库（TheAlgorithms-Java、hugo-theme-stack-starter、yxip、MoonTV）。
- 新增分类 `开源` / `工具`（未加入 `精选`，如需上精选框可自行添加）。

### 2026-09-22 · 补齐另外三个开源项目官网文章

- **新增** 三篇开源项目官网文章（内容取自各自仓库 README，配图取自仓库内真实图片）：
  - `content/post/type-text-injector/index.md`（`slug: type-text-injector`，Rust + MIT，含 GUI 截图）
  - `content/post/xiaomi-watch-s3-diy/index.md`（`slug: xiaomi-watch-s3-diy`，表盘逆向，含三套表盘预览图）
  - `content/post/ai-platform/index.md`（`slug: ai-platform`，Spring AI + Ollama + JDK 25，仓库无截图，纯文字）
- **更新** `content/page/links/index.md`：「主要项目」四张卡片（Fishing Funds / type-text-injector / xiaomi-watch-s3-diy / ai-platform）的 `website` 改为站内官网文章地址，正文同步补充链接。
- 新增分类 `逆向`（xiaomi 文章）、复用 `AI`（ai-platform 文章）。
- **日期调整**：这 4 篇开源项目官网文章的 `date` 统一改为 `2021-01-01`（早于站内最早文章 2022-03-06），
  使其沉到文章列表/归档最底部，不影响作者自己文章的时间排序；入口靠侧边栏「开源项目」(`/links/`) 页。

### 2026-09-22 · 记录开源项目 AGENTS.md 协作约定

- 前后 4 个开源项目仓库（fishing-funds / type-text-injector / xiaomi-watch-s3-diy / ai-platform）**均已自带 `AGENTS.md`**。
- 需求：后续这些项目若有更新/修改，会记录到各自仓库的 `AGENTS.md`；维护博客文章时应直接读取对应文件。
- 已在本文档**顶部维护约定**与**「开源项目文章的维护约定」小节**中记录：
  维护文章前先读项目仓库的 `AGENTS.md`（配合 README / CHANGELOG），并补充了「文章 ↔ 仓库」映射清单与新增项目的操作步骤。

## 未来计划 / TODO

> AI 接手时建议优先阅读本节。

- [ ] **确定「精选」最终归类**：目前标记在 `categories`，widget 走回退逻辑。若改用 `tags`，需给现有 35 篇补 `精选` 标签（可用脚本批量）。
- [ ] **补齐分组依据**：约 10 篇精选文章只有 `精选` 分类（无其他分类/系列），分组后落到「其他」。可考虑给它们补 `categories` 或 `series`，或把 `groupBy` 换成 `series` 并统一维护系列。
- [ ] **精选框体验**：条目 35 条 + 16 个分组后，评估 `50vh` 高度 + 滚动的观感，必要时调整 `--featured-box-h` 或改回限量展示。
- [ ] **统一时区**：在 `config.toml` 补 `timeZone = "Asia/Shanghai"`，避免依赖构建机时区。
- [ ] （后续新增待办请追加到此处）

## CI/CD

- 推送 `main` / `master` 自动触发 `.github/workflows/deploy.yml`：Hugo 构建（`--gc --minify`）→ 上传 artifact → 部署 GitHub Pages。
- `.github/workflows/update-theme.yml` 每日自动更新 Stack 主题。
- CI 环境：Dart Sass 1.97.1、Go 1.25.5、Hugo 0.154.2（`peaceiris/actions-hugo` 用 latest）、Node 24.12.0、`TZ: Europe/Oslo`。

## 交接提示（Quick Start）

1. 改**样式**：先看 `assets/scss/custom.scss`（有编号分节），注意 `1rem = 10px`。
2. 改**首页 widget**：`config/_default/params.toml` 的 `[[widgets.homepage]]` + `layouts/_partials/widget/*`。
3. 改**布局/短代码**：`layouts/`（覆盖主题同名文件即可）。
4. 提交前建议执行 `hugo --quiet` 做一次构建校验。
5. 完成后**记得回来更新本文件**（尤其「修改记录」与「未来计划」）。
