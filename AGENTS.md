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

- **静态站点生成器**：Hugo **Extended**。本地与 CI **统一为 v0.166.0**（`deploy.yml` / `update-theme.yml` 的 `HUGO_VERSION` 是唯一定义处）。
  - ⚠️ **下限 0.158.0，不可下调**：主题 v4.0.3 的 `layouts/baseof.html:2` 与 `layouts/rss.xml:33` 用了
    `.Site.Language.Locale`，该字段自 Hugo 0.158.0 起才存在。低于此版本会导致**全站每一页**渲染失败。
    `deploy.yml` 的 `Verify installations` 步骤里有版本断言，会在构建前拦截。
  - SCSS 编译必须用 **Extended** 版；CI 另外装了 Dart Sass 1.97.1。
- **主题**：`CaiJimmy/hugo-theme-stack` **v4**（通过 Hugo Modules 引入，见 `go.mod`、`config/_default/module.toml`）
- **样式**：SCSS，自定义覆盖集中在 `assets/scss/custom.scss`
- **部署**：GitHub Actions → GitHub Pages
- **语言**：中文（`defaultContentLanguage = "zh"`，`hasCJKLanguage = true`）
- **评论**：Giscus
- **脚本**：Python3（`scripts/format_posts.py`、`scripts/optimize_images.py`、`scripts/cover_to_webp.py`）

> ✅ **时区**：`config.toml` 已显式设置 `timeZone = "Asia/Shanghai"`，CI 里的 `TZ: Europe/Oslo`（starter 遗留）已删除。
> 本地与线上日期渲染保持一致。**不要再删掉 `timeZone`，也不要重新引入 `TZ` 环境变量。**

## 目录结构（只看自定义/关键部分）

```text
config/_default/
  config.toml            # baseurl / 语言 / 时区（timeZone）/ 分页（pagerSize）/ timeout（5m）/ RSS limit
  params.toml            # 侧边栏、文章、widget、评论、图片派生宽度等（主要改动文件）
  module.toml            # 引入 Stack 主题
  _languages.toml / menu.toml / markup.toml / permalinks.toml / related.toml
assets/
  img/avatar.webp        # 侧边栏头像（400x400 WebP，45 KB）
  scss/
    custom.scss            # 【全部自定义样式】按编号分节，见文件内注释
layouts/
  _markup/
    render-image.html    # 【覆盖主题】远程图片直连、不再下载到本地（见「5. 图片处理」）
  _partials/
    widget/featured.html # 【自定义】精选文章 widget
    article/components/links.html  # 【覆盖主题】links 页卡片：额外显示项目地址（.link-website）
    article/components/content.html # 【覆盖主题】仅给带 links 的页面加 has-links 类（便于只对该页正文链接做强调）
    head/custom.html     # 【自定义】代码字体 JetBrains Mono（jsDelivr CDN）
    footer/custom.html   # 【自定义】品牌渐变条 / 不蒜子统计 / 阅读进度条 / 返回顶部
  shortcodes/
    hint.html            # 【自定义】提示框 {{< hint "tip" >}}
    color.html           # 【自定义】文字颜色 {{< color "red" >}}
  partials/extend-footer.html  # 空占位文件
scripts/
  format_posts.py        # 文章批量排版 / 错别字修复
  optimize_images.py     # 压缩 content/ 下图片（保持文件名与格式不变）
  cover_to_webp.py       # 把大体积封面图迁移为 WebP 并同步 front matter
.github/workflows/       # deploy.yml（构建部署）、update-theme.yml（每日更新主题，推 ci/update-theme 分支）
content/post/            # 文章（中文）
static/                  # 静态资源（favicon.png，180x180）
```

## 本地运行

```bash
hugo server -D          # 预览：http://localhost:1313/
hugo --quiet            # 构建校验（不启动服务）
```

## 内容规范

- 文章存放于 `content/post/`，按系列或日期组织（部分目录为 page bundle：`index.md` + 图片）。
- **「精选文章」通过 front matter 标记**：当前 **30** 篇文章在 `categories` 中包含 `精选`；**`tags` 中 0 篇**（`params.toml` 配的却是 `taxonomy = "tags"`，靠 `featured.html` 的回退逻辑兜住）。
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

### `scripts/optimize_images.py`

压缩 `content/` 下的 PNG/JPG，**保持文件名与扩展名不变**，因此不需要改动任何文章引用。
依赖 Pillow（`pip3 install Pillow`）。

```bash
python3 scripts/optimize_images.py --dry    # 预览
python3 scripts/optimize_images.py          # 实际写入
```

策略：超过 1600px 的先等比缩放 → PNG 转 8-bit 调色板量化（256 色，带 alpha 的走 FASTOCTREE）→
JPEG 用 `quality=82` 重编码 → 压缩后反而更大的文件自动跳过。默认只处理 ≥250 KB 的图。

### `scripts/cover_to_webp.py`

把**体积较大的封面图**（书籍封面等照片类 PNG）迁移为 WebP，并同步更新 front matter 的 `image` 字段。
照片类 PNG 即便量化到 256 色仍有 1 MB+，WebP 通常只有 1/10。

```bash
python3 scripts/cover_to_webp.py --dry    # 预览
python3 scripts/cover_to_webp.py          # 实际执行
```

三重安全约束（任一不满足即跳过并报告，不会写坏文章）：

1. 该图片**只能**被 front matter 的 `image:` 引用；正文若出现 `![](x.png)` 或 `<img src="x.png">` 则跳过；
2. 转换后体积未降到原来的一半则跳过并删除产物；
3. front matter 的 `image:` 必须精确等于该文件名才替换（只替换 1 处）。

> 新增文章时若放了照片类封面，建议直接存 WebP 并在 front matter 写 `image: xxx.webp`。

## 配置要点

- 分页大小：`config/_default/config.toml` 的 `pagerSize`（当前 20）。
- 时区：`config.toml` 的 `timeZone = "Asia/Shanghai"`（**必须保留**）。
- 语言标签：`config.toml` 的 `locale = "zh-cn"`。
  ⚠️ **不要再写 `languageCode`**——自 Hugo 0.158.0 起已更名，每次构建都会打 deprecation WARN；
  且主题 v4.0.3 的 `baseof.html` / `rss.xml` 依赖的 `.Site.Language.Locale` 就是随这次更名新增的字段
  （这也正是上一条记录里 Hugo 版本下限事故的根因）。
- 配色 / 排版：**全部集中在 `assets/scss/custom.scss` 第 0 节「设计令牌」**，
  改动前务必先读「2.1 CSS 变量纪律」。
- RSS：`config.toml` 的 `[services.rss] limit = 20` + `params.toml` 的 `rssFullContent = false`。
- 图片派生宽度：`params.toml` 的 `[imageProcessing.content] widths = [800, 1400]`
  （主题默认 `[800, 1600, 2400]`，每张图会多生成 1 份大图）。
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

### 2.1 CSS 变量纪律（⚠️ 改样式前必读，历史上最大的坑）

1. **引用主题变量时绝不要写 fallback 值。**
   主题一定会定义该变量，`var(--accent-color, #6a8cff)` 里的 `#6a8cff`
   **永远不会生效**，却会让人误以为生效了——本项目曾因此产生 14 处死样式。
   需要新颜色 → 在 `custom.scss` 第 0 节「设计令牌」里定义自己的变量，再引用。
2. **改配色只改第 0 节一处**，其余位置一律引用变量。深浅两套值在
   `@mixin dark-tokens` / `dark-text-colors` / `dark-hint-bg` 里各写一次。
3. **覆盖前先确认变量真实存在**（避免重蹈第 1 条的覆辙）：
   ```bash
   hugo --quiet && grep -oE '\-\-[a-z0-9-]+:' public/scss/*.css | sed 's/.*css://' | sort -u
   ```
4. 深色令牌有两处入口，**都要保留**：
   - `:root[data-scheme="dark"]` —— 用户手动切深色；
   - `@media (prefers-color-scheme: dark) :root:not([data-scheme="light"])` —— 无 JS 兜底。
   主题的内联脚本在 `<body>` 首个子节点处**同步**执行
   （`document.documentElement.dataset.scheme = "dark" | "light"`，属性总是显式设置），
   所以显式浅色模式下不会误命中深色令牌，且不会闪白。

### 2.2 已定制的排版（改动前先了解现状）

- **标题字号阶梯**：主题 v4 **完全没有**标题字号定制（浏览器默认导致 h4 与正文同大、
  h5 反而比正文小）。已在 `custom.scss` 补h1~h6 = `1.9 / 1.55 / 1.3 / 1.12 / 1 / 0.95em`，
  左侧竖线宽度随层级递减并**同步补偿 `padding-inline-start`**，保持所有标题文字左边界一致。
- **中文排版**：`text-align: justify` + `text-justify: inter-ideograph`、`line-break: strict`、
  `hanging-punctuation: allow-end`、`text-autospace: normal`（中英文自动间距，低版本浏览器忽略）。
  代码块 / 表格 / 提示框 / 引用块通过 `:is(...)` 改回 `text-align: left`，避免被 justify 拉伸。
- **代码块**：主题给 `pre` 设了 `word-break: break-all`，会让长代码行硬折行、
  导致 `overflow-x: auto` 永远不触发（横向滚动条出不来）。已覆盖为 `word-break: normal` + `white-space: pre`。
- **列表**：站内列表极密集（无序 ~3000 条、有序 ~1800 条），原先完全走浏览器默认值。
  已补缩进、间距、`li::marker` 强调色、嵌套层级降权、任务列表复选框对齐。
- **对比度**：正文/引用/日期/行内代码/链接均已按 WCAG AA 校准（深浅两套值都 ≥4.5:1，
  行内代码由原先深色下 2.4:1 提升到 6.9:1）。
- **主题色**：浅色 `#4263eb` / 深色 `#a8bcff`（覆盖主题默认的 `#34495e` / `#ecf0f1`——后者在深色下近乎纯白，
  导致标题竖线、正文链接与正文几乎同色）。渐变条等统一走 `--brand-gradient`。

### 2.3 内容排版与配色规范（写文章 / 改文章前必读）

全站 36 篇精选文章已完成排版与配色改造，共 **422 处语义着色**。

#### 配色语义（全站固定，不要自创）

| class | 语义 |典型用途 |
| --- | --- | --- |
| `text-red` | 风险 / 错误做法 / 禁止 / 坑 / 缺点 | 「会导致…」「不能…」「❌」 |
| `text-yellow` | 注意事项 / 边界条件 / 易混淆前提 | 「特殊情形」「前提是…」 |
| `text-blue` | 核心机制 / 关键定义 / 原理 | 「本质是…」「关键在于…」 |
| `text-green` | 优势 / 推荐做法 | 「更高效」「建议…」 |
| `text-gray` | 中性术语首次定义 | 灰度术语首现 |

**密度参考**：约每 400 字 1 处；同一小节不超过 2 处。
**优先级**：能用 `**加粗**` 解决就不要上色，颜色只承担语义分类。

#### 三条写法铁律（都是实际踩过的坑）

1. **不要用 `<font color="red">`**—— 废弃标签，且颜色写死不随深色模式切换。
   用 `<span class="text-red">**文字**</span>`（内部Markdown 会被正常解析）。
2. **列表标记必须留在 `span` 之外**。写成 `<span class="text-red">**- 列表项**</span>`
   会让整行被span 包住，**列表结构直接失效**。正确写法：`- <span class="text-red">**列表项**</span>`。
3. **`**小标题：**内容`** 中若 `**` 紧贴字母/数字/汉字，**整段都渲染不出来**
   （Markdown 要求右闭合符后接空白/标点/行尾）。必须写成 `**小标题：** 内容`（中间留空格）。

> 2026-10-10 的批量改造中，因脚本把整条列表项连同 `- ` 一起包进 `span`，
> 一次性破坏了 13 处列表结构；已全部修复并加入脚本校验。

#### 相关脚本

- `scripts/enhance_posts.py` —— 通用排版结构优化（松散列表合并、标题层级跳级修正）。
  规则保守、带 5 道结构自洽校验（标签配对、加粗配对、说明段落非列表项等）。
  `--dry` 预览，`--all` 覆盖非精选文章。
- `scripts/format_posts.py` —— 原有脚本，错别字词典**未包含**本文档提到的那些词，
  上面的错别字是单独修的，不要指望它。

### 3. 视觉 / 交互增强（`custom.scss` + `footer/custom.html`）

- 顶部品牌渐变条、阅读进度条、返回顶部按钮（JS 在 `footer/custom.html`）。
- 不蒜子访问统计（国内可用，无需账号）。
- 文章卡片 / 标签胶囊 hover 动画、自定义滚动条、表格 / 引用块 / 代码块美化。
- hint 提示框（`note/info/tip/success/warning/danger`）与文字颜色类（`.text-red` 等）。
- **所有 hover 效果都包在 `@media (hover: hover)` 里**：触屏上 `:hover` 会「粘住」，
  图片点一下就永久保持放大态。
- **可访问性**：`:focus-visible` 键盘焦点框、`prefers-reduced-motion: reduce`（关闭动画与位移）、
  `@media print`（隐藏侧栏/按钮/评论，打印时展开外链地址，代码块与表格不跨页断裂）。
- **正文外链标识**：`a[href^="http"]::after` 加 SVG mask 图标，站内域名自动排除。

### 4. 图片处理与体积控制（`layouts/_markup/render-image.html` + 两个脚本）

**这是本项目体积控制的重点，改图片相关配置前务必先读本节。**

- **本地图片**：走 Hugo 原生 `imageProcessing`，派生宽度由 `params.toml` 的
  `[imageProcessing.content] widths = [800, 1400]` 控制（`srcset` 最大项始终是原图）。
- **远程图片**：`render-image.html` 覆盖了主题同名文件，**对 `http://` / `https://` / `//` 开头的图片
  直接输出原URL**，不调用 `helper/image`（也就不会触发内部的 `resources.GetRemote`），也不生成 srcset。

  为什么必须这样：主题默认会把正文里所有外链图床图片**下载一份到本地并全量发布到 public 根目录**
  （实测 778 个文件 / 139 MB，占 public 的 88%），而且构建成败取决于外部图床
  （实测 gitee / helloimg / camo.githubusercontent.com 均有403 或解析失败，那些图在页面上直接是坏图）。

- **新增图片建议**：照片类封面直接存 WebP；`optimize_images.py` 保持文件名不变可安全批量压缩；
  `cover_to_webp.py` 用于把已有的大封面迁移为 WebP（会自动同步 front matter）。

### 5. 评论 / 代码

- 评论为 Giscus，配置 `params.toml` 的 `[comments.giscus]`（仓库需开启 Discussions）。
- 代码高亮 Chroma，行号、`tabWidth=4`；代码字体 JetBrains Mono 由 `head/custom.html` 引入。

## 修改记录（Changelog）

### 2026-10-10 · Hello 文章封面改为 Hermes Agent 官网风格的抽象几何封面

**改动**：`content/post/2022-01-01hello-world/`（page bundle，`/p/hello-world/`）

- front matter 由 `image: welcome.jpg` 改为 `image: hello-cover.webp`。
- 新封面为 AI 生成的抽象几何构成画，风格参照 **Hermes Agent 官网**（Nous Research 的开源 AI 智能体，
  <https://hermes-agent.nousresearch.com/>）：深靛蓝底 + 纯电光蓝同心圆环 + 荧光黄 / 纯白线条 + 少量品红，
  瑞士国际主义排版风格，硬边几何、克制留白、中央柔和径向光晕。
- 落地处理：裁掉底部 8% 去除生成工具的「AI 生成」角标（此图底部是纯深色，裁切完全无损）→
  转 WebP（`quality=88`），**2.03 MB PNG → 107 KB WebP**（约 1/19），
  走 Hugo 原生 `imageProcessing` 派生 800/1400 两档 srcset。
- 旧图 `welcome.jpg`（带 VCG 水印的漫画）与从未被引用的 `cover.jpg` **保留**在目录里，不再作为封面。
- 构建验证通过：305 页 / 189 张派生图 / 918 ms；文章页与首页卡片均正确引用新封面，旧图已无引用。

**参考来源（想复刻同类风格时先看这里）**

Hermes Agent 官网的视觉语言可直接从其 CSS 变量读出，不用猜：

| token | 值 | 说明 |
| --- | --- | --- |
| `--hermes-color-blue` | `#0000f2` | **主色**，极高纯度电光蓝，出现 51 次 |
| `--hermes-color-indigo` | `#7900f2` | 紫 |
| `--hermes-color-yellow` | `#f2f200` | 荧光黄，主强调色 |
| `--hermes-color-magenta` | `#f200f2` | 品红 |
| `--hermes-color-neon` | `#79f200` | 荧光绿 |
| `--hermes-color-cyan` | `#00f2f2` | 青 |
| `--hermes-color-orange` | `#f27900` | 橙 |
| `--hermes-color-neutral` | `#616191` | 中性灰紫 |
| 次级蓝 | `#0847c4` / `#ebf5ff` / `#c3ddfd` | 深浅蓝阶 |

字体：`Rules Condensed` / `Rules Extended` / `Rules Gothic Compressed`（压缩展示体）、
`EB Garamond`（衬线）、`Aeonik Fono Pro`（无衬线）、等宽字体。
风格关键词：**瑞士国际主义 + 大字号压缩标题 + 高纯度原色 + 深底高对比**。

> ⚠️ **AI 生成图带角标水印**：生成结果右下角固定有平台水印，直接当封面会很突兀。
> 常规处理是**裁掉底部约 8%**，前提是该区域本就不是构图主体
> （构图主体在上下渐变或地面网格时就安全；若水印压在主体上则需换构图重生成，不要为此做 inpainting）。

> 💡 **生成脚本在本项目不可用**：`buddy-cloud.py image` 用 IDE 会话 JWT 调用会报
> `invalid or expired JWT token`，直接用内置的 `image_gen` 工具即可，不要在脚本上纠结。

### 2026-10-10 · 全站 36 篇精选文章逐篇排版与配色改造

**背景**：在上一条「站点样式体检」之后，进一步逐篇阅读 36 篇精选文章，
按语义补充颜色标记与结构优化。

**新增脚本 `scripts/enhance_posts.py`**（通用、保守、可复现）

- **松散列表合并**：把「列表项是词条 + 说明另起一段」合并为「列表项：说明」。
  站内这类写法极多（无序列表约 3000 条、有序约 1800 条），原先完全靠浏览器默认渲染。
- **标题层级跳级修正**：`h2` 后直接出现 `h4` 时降为 `h3`（只降不升）。
- 带 5 道结构自洽校验，避免误伤：标签配对、加粗配对、说明段落不是列表项、
  不吞并`**词条：**说明` 结构、合并后长度上限。

**内容侧修复（真实bug）**

1. **`<font color='red'>` → `<span class="text-red">`**（79 处 / 15 篇）。
   原写法颜色写死，深色模式下不切换；`text-red` 深浅两套均 ≥4.5:1。
2. **失效的加粗修复**（36 处 / 8 篇）：`**词：**内容` 中 `**` 紧贴文字时整段渲染不出来。
3. **提示框内的 Markdown 未渲染**：`hint.html` / `color.html` 原用 `{{ .Inner }}`，
   直接输出原始文本，导致 **75 个提示框中有 20 个内容是坏的**（`**加粗**` 显示为字面量）。
   改为 `{{ .Inner | .Page.RenderString (dict "display" "block") }}`。
4. **本地绝对路径泄露**：seata篇 9 处 `file:///Users/tom/...`（含用户名）→ 换成 GitHub 链接。
5. **图片 URL 含未编码空格与括号** 1 处 → 线上必然加载失败，已编码。
6. **`[!NOTE]` 是 GitHub 专有语法**，Hugo 不识别会原样显示 → 改为 `hint` shortcode。
7. **表格缺空行导致不渲染**、有序列表编号重复、空列表项、标题内零宽字符、
   重复插图、引用块包裹 shortcode 等，共 218 处（`doc_health`体检脚本产出）。
8. 错别字与术语：`Excutor`、`commitAsyc`、`LOCK_ORNIDARY`、`CLassLoader`、`navtive`、
   `cansel`、`锁卷/炼狱`、`破话枚举单例`、`范逼近定理` 等数十处。

**语义着色**：36 篇逐篇精读，共 **422 处**（红 177 /蓝 109 / 黄 78 / 绿 41 / 灰 17）。
配色语义与三条写法铁律见「2.3 内容排版与配色规范」。

**踩坑记录（重要）**

批量改造用的临时应用器存在缺陷：`{o, c}` 格式的条目没有 `n` 字段，
`nn` 取到空串，**把所有匹配文本替换成了空字符串**，导致一次 git checkout 前的
约 200 处着色与部分正文丢失。发现后已修正为「`n` 为空则跳过」并加断言，
随后从快照回填 + 重新跑通全部批次，最终 422 处全部就位。
**教训：任何批量文本替换都必须有「空结果保护」，且替换后必须统计 before/after 数量。**

**验证**：`hugo --gc --minify` 干净构建通过（69 篇文章页 / 305 页），
全站检查 `加粗失效 0` / `<font> 残留 0` / `空列表项 0` / 异常页 0。

### 2026-10-10 · 全站排版 / 配色 / 可访问性体检并修复

**背景**：对 `custom.scss` 与主题 v4.0.3 的实际编译产物做逐项比对，发现**一批「写了但根本没生效」
的死样式**（长期被误认为生效），以及深色模式配色、中文排版、对比度上的多处实质问题。

**1. 失效的样式（真 bug）**

- **14 处`var(--accent-color, #6a8cff)` 的fallback 从未生效**——主题必定定义了 `--accent-color`
  （浅色 `#34495e` / 深色 `#ecf0f1`），fallback 是死代码。后果：
  深色模式下**每个h1~h6 左侧的3px 竖线、TOC 当前项、正文链接全是近白色**，
  与正文 `rgba(255,255,255,.9)` 几乎无法区分；浅色模式下正文链接是暗灰，辨识度弱。
- **标题锚点样式 20 行全是死代码**：写的是 `.anchor`，主题实际类名是 `a.header-anchor`
  （且用 `position:absolute` 定位，不是 `margin-left`）。
- **表格三个变量全部写错**：`--table-head-background` / `--table-stripe-background` /
  `--table-hover-background` 在主题里都不存在，只靠 `rgba(0,0,0,4%)` fallback 兜住——
  **深色模式下等于没有**，表头无底色、斑马纹不可见（站内 35 篇文章、1253 行表格受影响）。
- `body { line-height: 1.75 }` 无效：`.article-content` 已有 `--article-line-height`(1.85)，优先级更高。
- 行内代码用了不存在的 `--inline-code-color`，绕过了主题的 `--code-text-color`，
  导致**深色模式下玫红字on `#272822` 仅 2.4:1，几乎不可读**。
- `config.toml` 的 `languageCode` 自 0.158.0 起已更名，**每次构建都打 deprecation WARN** → 改为 `locale`。

**2. 额外挖出两个此前没注意到的问题**

- 主题 v4 **完全没有标题字号定制**（只做了左侧竖线 + 锚点）。浏览器默认下
  `h4` 与正文同大、`h5`(0.83em) 反而比正文还小，中文长文里 h3/h4/h5 层级几乎分不出来。
- 主题给 `.article-content pre` 设了 `word-break: break-all`，会让长代码行**硬折行**，
  导致同时设置的 `overflow-x: auto` 永远不触发（横向滚动条根本出不来）。

**3. 已落地的修复**

- **配色令牌化**（`custom.scss` 第 0 节）：强调色统一为浅色 `#4263eb` / 深色 `#a8bcff`
  （均 ≥4.5:1），深浅两套文字色、行内代码色、表格色全部按 **WCAG AA** 重新校准；
  渐变条 / 进度条 / 头像装饰统一走 `--brand-gradient`。
- **中文排版**：`line-break: strict`、`hanging-punctuation`、`text-autospace`（中英文自动间距）、
  `overflow-wrap`（替掉已废弃的 `break-word`）；代码块/表格/提示框/引用块改回 `text-align: left`，
  避免被 `justify` 拉伸。
- **标题阶梯** h1~h6 = 1.9/1.55/1.3/1.12/1/0.95em，竖线宽度随层级递减并同步补偿 padding，
  保证所有标题文字左边界一致；补 `scroll-margin-top` 防止点目录跳转时贴顶。
- **列表**：站内列表极密集（无序 ~3000、有序 ~1800），原先零样式。补缩进、间距、
  `::marker` 强调色、嵌套降权、任务列表对齐。
- **代码块**：覆盖 `word-break`为 `normal` + `white-space: pre`，横向滚动恢复；
  `pre` 补边框（浅色下主题底色 `#fafafa` 与卡片白底区分度不足）。
- **表格**：表头加粗 + 强调色淡底 + 首尾单元格圆角；窄屏（≤700px）整表横向滚动而非把单元格挤成竖排。
- **分隔线**：改为居中渐隐细线（原100px 实心短横）。
- **可访问性**：`:focus-visible` 键盘焦点框、`prefers-reduced-motion: reduce`、
  `@media print`（隐藏侧栏/按钮/评论、展开外链地址、代码块与表格不跨页断裂）。
- **所有 hover 效果包进 `@media (hover: hover)`**：触屏上 `:hover` 会粘住，
  图片点一下就永久保持放大态（此前 `transform: scale(1.01)` 就是如此）。
- **正文外链标识**：`a[href^="http"]::after` 加 SVG mask 图标，站内域名自动排除。

**已验证**：`hugo --gc --minify` 构建通过（305 页），`languageCode` deprecation WARN 已消失，
仅剩原有的 `Widget series not found`（series widget 无数据，属 P2）；
编译产物逐项核对 18 项断言全部 OK；CSS 72.1 KB（+0.5 KB）。
已确认 `data-scheme` 由内联脚本**同步**挂在 `<html>` 上且总是显式设为 `dark`/`light`，
故深色令牌不会污染浅色模式，也不会闪白。

> 📌 **教训**：`var(--主题变量, fallback值)` 这种写法在本项目里**一律是陷阱**——
> fallback 永远不生效，却掩盖了「变量名写错了」这个事实。改样式前先按 2.1 节的命令
> 列出主题真实变量，再动笔。

> 📌 **`custom.scss` 分节编号已整体重排**（现共 31 节，配色令牌集中在第 0 节）。
> 历史变更记录里引用的「第 N 节」是**当时**的编号，仅作历史参考；
> 定位请以**类名 / 选择器**为准，不要按数字找。

### 2026-10-10 · 修复 CI 构建失败：Hugo 版本下限事故

**现象**：2026-10-10 的 P0 优化推送后，CI 全站渲染失败：

```text
Error: failed to render pages: render of "/home/runner/work/.../content/_index.md" failed:
".../hugo-theme-stack/v4@v4.0.3/layouts/baseof.html:2:20":
template: home.html:2:20: executing "home.html" at <.Site.Language.Locale>:
can't evaluate field Locale in type *langs.Language
```

**根因**：上一条记录里的「把 `hugo-version: latest` 锁定为 `HUGO_VERSION`」这一步做错了——

- 锁定时**直接沿用了 starter 遗留的 `0.154.2`**（这个数字本身就是个错误信息：`latest` 时代 CI 实际跑的是 Hugo 0.16x，主题依赖新API），
  并且只在本机（0.166.0）做了验证；
- 主题 v4.0.3 的 `baseof.html:2` 与 `rss.xml:33` 使用 `.Site.Language.Locale`，
  这是 **Hugo 0.158.0 随 `languageCode → locale` 更名一起新增的字段**，0.154.2 的 `langs.Language` 上不存在；
- 于是**每一页**都渲染失败。本地是 0.166.0 所以本地全绿，掩盖了问题。

**修复**：

1. `deploy.yml` 与 `update-theme.yml` 的 `HUGO_VERSION` 由 `0.154.2` → **`0.166.0`**（与本地一致）；
2. `deploy.yml` 的 `Verify installations` 增加**版本下限断言**（`>= 0.158.0`），
   用`sort -V` 比较，不满足直接 `::error::` 退出——以后再把版本调低，会在构建第一步就失败，
   而不是等到渲染阶段才发现全站挂掉；
3. 两个 workflow 均补注释说明该下限的来源（主题模板的 API 依赖）。

**已验证**：

- 断言逻辑：`0.166.0` / `0.158.0` 通过，`0.154.2` / `0.146.0` 被拒；
- `hugo_0.166.0` 的 release 资产存在，且有 `hugo_extended_0.166.0_linux-amd64.tar.gz`（extended 为SCSS 必需）；
- `peaceiris/actions-hugo` **未归档**且 2026-09 仍在维护，此前用 `latest` 能正常下载，说明已适配小写 `linux-amd64` 新命名；
- 本地 `hugo --gc --minify`（0.166.0，与 CI 同版本）构建通过，305 页；
- 两个 workflow 的 YAML 已用 ruby 解析校验通过。

> 📌 **教训**：锁定工具链版本时，**不能沿用历史文档里的版本号**（本项目里`0.154.2` 就是 starter 留下的假信息），
> 必须先确认「该版本 + 当前依赖（本例为主题 v4.0.3）」能否工作；本地验证也要**用与 CI 完全相同的版本**。

### 2026-10-10 · P0 性能与工程可靠性优化

**背景**：全项目排查后按「收益/风险比」选出7 项 P0 并全部落地。核心结果：
**`public/` 293 MB → 18 MB，构建 11 s → 4.8 s，首页 RSS 7.4 MB → 34 KB。**

1. **侧边栏头像 6.6 MB → 45 KB**
   - 根因：主题 `sidebar/left.html` 只调 `helper/image`（**不做任何 Resize**），
     直接把原图 permalink 放进 `<img>`，而原图是 1773×2364 的 6.6 MB PNG，每页首屏都加载。
   - 处理：`assets/img/avatar.png` → 居中裁剪为 400×400 → WebP q82（`assets/img/avatar.webp`），
     `params.toml` 的 `sidebar.avatar` 同步改为 `img/avatar.webp`。
2. **favicon 1.2 MB → 30 KB**：`static/favicon.png` 由 1024×1024 缩到 180×180（路径不变，无需改配置）。
3. **`public/` 293 MB → 18 MB**（两条独立原因）
   - **本地源图 63 MB → 3.9 MB**：
     - 新增 `scripts/optimize_images.py`：保持文件名/格式不变地压缩（缩放 + PNG 8-bit 量化 + JPEG q82），
       **零引用改动**，处理 36 张，60.9 MB → 32.7 MB；
     - 新增 `scripts/cover_to_webp.py`：29 张照片类大封面（书籍封面，量化后仍 1 MB+）→ WebP，
       1 MB → 30~144 KB，并自动同步 front matter 的 `image:`。带三重安全校验（详见「脚本工具」）。
   - **远程图片本地化 139 MB → 0**：主题 `render-image.html` 对**所有**图片（含远程）调用
     `helper/image`，其内部 `resources.GetRemote` 会把外链图床图片下载并**全量发布到 public 根目录**
     （778 个文件 / 139 MB，占 public 的 88%）；同时构建依赖外部图床，实测 gitee / helloimg /
     camo.githubusercontent.com 有 403 与解析失败，**这些图在页面上本来就是坏的**，每次构建刷大量 WARN。
     新增 `layouts/_markup/render-image.html`：远程图片直连原URL，不下载、不生成 srcset。
     本地图片逻辑与主题完全一致（仍带 srcset）。
   - 顺带把 `params.toml` 的 `[imageProcessing.content] widths` 从主题默认 `[800, 1600, 2400]`
     收窄为 `[800, 1400]`。
   - 副作用（正向）：构建不再有远程抓取 WARN，`Processed images` 625 → 187。
4. **RSS 7.4 MB → 34 KB**：`rssFullContent = false`（`params.toml`）+ `[services.rss] limit = 20`（`config.toml`）。
   此前首页 `index.xml` 塞进了全部 75 篇全文（单篇最长 112 KB）。
5. **时区统一**：`config.toml` 新增 `timeZone = "Asia/Shanghai"`，并删除 CI 里的 `TZ: Europe/Oslo`
   （starter 遗留）。此前本地与线上日期渲染依赖构建机时区，可能差一天。
6. **`deploy.yml` 修复**
   - `hugo-version: 'latest'` → `${{ env.HUGO_VERSION }}`（此前版本号形同摆设，构建不可复现）。
     ⚠️ 但这一步当时锁成了 starter 遗留的 `0.154.2`，**锁错了**，导致 CI 全站渲染失败，
     已由上一条记录（2026-10-10 Hugo 版本下限事故）修正为 `0.166.0`；
   - 缓存key 由 `hugo-${{ github.run_id }}`（每次运行都唯一）改为
     `hugo-${{ runner.os }}-${{ hashFiles('go.sum', 'config/**', 'assets/**') }}`。
     原写法导致**缓存内容永不刷新**（save 复用 restore 的旧 primary key）且**每次运行新增一条缓存**，
     会迅速吃满仓库 Actions 缓存配额。
   - 删除无效步骤：`setup-node`、无 `package.json` 的 `npm ci || true`、
     `submodules: recursive`（无 submodule）、`fetch-depth: 0`，以及 `Verify installations` 里的 Node 打印。
7. **`update-theme.yml` 加固**
   - 补`actions/setup-go`（此前 `hugo mod get/tidy` 依赖 runner 镜像预装的 go，版本不可控）；
   - 补 `concurrency`，避免定时任务与手动触发并发写同一分支；
   - 提交前**先完整构建校验**（`hugo --gc --minify --destination /tmp/hugo-verify`），失败则不产生提交；
   - 提交目标从默认分支改为 `ci/update-theme`（`deploy.yml` 只监听 main/master），
     **主题升级不再自动上线**，需人工验证后合并。

> 验证：`hugo --gc --minify` 干净构建通过（305 页 / 11.3 s→4.8 s），仅剩一条既有 WARN
> `Widget series not found`（series widget 无数据，属 P2）。两个 workflow 的 YAML 已用 ruby 解析校验通过。
> 临时文件备份在 `/tmp/hblog-bak/`（原头像与 favicon）。

### 2026-10-09 · 解决 CI渲染超时

- **问题**：GitHub Actions 构建时报 `timed out rendering the page content ... timeout after 1m0s`，
  出错文章为《读〈设计数据密集型应用系统〉（第1版）有感 第二部分》（长文渲染超过默认 60s）。
- **修复**：`config/_default/config.toml` 新增 `timeout = "5m"`（Hugo 渲染超时，含页面内容渲染）。
- 已验证本地 `hugo --quiet` 构建通过；如 CI 仍超时可继续调大。

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

### 2026-09-22 · links 页卡片显示「项目地址」并强调

- **新增覆盖模板** `layouts/_partials/article/components/links.html`（基于主题同名文件改造）：
  在「标题 + 描述」下方额外渲染 `<span class="link-website">`，内容为 `$link.website`（站内相对链接用 `absURL` 补全），
  站内文章卡片显示完整文章地址、GitHub 卡片显示仓库地址；同时把 `helper/image` 的 `Context` 修正为页面（原主题传的是 link dict）。
- **新增样式** `custom.scss` 第 23 节：`.article-list--compact.links .link-website` 用**强调色 + 加粗**（`var(--accent-color)` / `font-weight:700`），
  hover 变深并加下划线；`.article-details` 加 `min-width:0` 避免长链接撑破卡片。
- 需求来源：让 links 页的项目地址更醒目、便于访客点击。

### 2026-09-22 · links 页正文「本站文章」链接换色加粗

- **问题**：`links` 页正文里的 `[本站文章](/p/xxx/)` 链接仍是默认链接样式（强调色、不加粗），与卡片里已强调的地址不一致。
- **踩坑**：用 `{{< color "blue" >}}[**本站文章**](/p/xxx/){{< /color >}}` 包裹 **不会生效**——
  `{{< >}}` 短代码的 inner 内容不做 Markdown 渲染，链接会原样输出成纯文本。
- **采用方案（纯 Markdown，无需写行内 HTML）**：
  1. 新增覆盖模板 `layouts/_partials/article/components/content.html`，仅当页面有 `links` 参数时给 `.article-content` 加 `has-links` 类；
  2. `custom.scss` 第 24 节：`.article-content.has-links a { font-weight: 700; color: var(--c-blue); }`（hover 变深 + 下划线）。
- 效果：links 页正文的站内链接变成 **深蓝色 + 加粗**；其他文章页完全不受影响（已验证 `has-links` 只出现在 `/links/`）。

## 未来计划 / TODO

> AI 接手时建议优先阅读本节。
>
> 2026-10-10 已完成 P0（性能 + CI 可信度），`public/` 293 MB → 18 MB。
> 以下是排查中发现的 **P1 / P2**，均**尚未处理**，按优先级排列。

### P1 · 内容与 SEO

- [ ] **60 篇文章无 `slug`**：URL 由中文标题生成（percent-encoded，如 `/p/算法-排序/`），
  可读性差、换标题即换 URL。需脚本化补ASCII slug + 同步 `aliases` 保护老URL（改动较大，务必分批）。
- [ ] **35 篇文章缺 `description`**：列表页摘要靠 `.Summary` 截技术正文，常在代码块中间断掉；分享到微信/微博无摘要。
- [ ] **`精选` 标记与配置错位**：30 篇全在 `categories`，`tags` 中 0 篇；而 `params.toml` 配的是 `taxonomy = "tags"`，
  现在靠 `featured.html` 的回退兜底跑着，删掉回退代码就会静默失效。
- [ ] **categories / tags 语义重叠**：26 vs 68 个词条中有 **15 个重复**（AI / java / mysql / 架构 / 算法 / 信贷核心…），
  同一内容生成两套归档页（已产生 209 个分类/标签 HTML），SEO 重复。建议明确规则：分类=领域大类，tags=主题/技术栈。
- [ ] **两篇 MapReduce 近乎重复**：`content/post/2024-07-15-Powerjob/2024-09-10-MapReduce.md` 与
  `content/post/2025-01-01之前的杂项/2024-09-10-MapReduce.md`（diff 后仅差`hashmap`/`HashMap` 大小写与一个 hint 块）。删一篇 + `aliases`。
- [ ] **og:image 全缺**：`params.toml` 的 `defaultImage.opengraph.enabled = false`；配一张 1200×630 兜底图。
- [ ] **无 robots.txt**：加 `enableRobotsTXT = true` + `static/robots.txt`（写明 `Sitemap:`）。
- [ ] **3 篇文章的 `image:` 指向不存在的文件**（构建时会WARN）：
  `2025-12-25-账务是怎样运行的`、`1连载中/读《设计机器学习应用系统》有感-神经网络与机器学习`、`2025-07-17-状态机`。
- [ ] **`series` 是死配置**：0 篇文章设置，但 `params.toml` 配了 series widget → 构建 WARN `Widget series not found`。要么补series，要么删 widget。

### P2 · 代码质量与一致性

- [x] ~~**死 CSS**~~（2026-10-10 修正判断）：原判定「`@media (prefers-color-scheme: dark)` 永不生效」**不准确**——
  主题内联脚本正常工作时确实总会设置 `data-scheme`，但它位于 `<body>` 首个子节点、
  **属于渲染关键路径**，一旦被 CSP 拦截或 JS 失败，属性就不会存在，此时系统深色偏好仍应生效。
  故该 `@media` 块作为**无 JS 兜底予以保留**，并在 `custom.scss` 与本文「2.1」节写明原因。
- [x] **无障碍**：`prefers-reduced-motion: reduce` 已落地（关闭动画/位移/平滑滚动），
  另补 `:focus-visible` 键盘焦点框与 `@media print` 打印样式。
- [x] **主题一致性**：3 处硬编码 `linear-gradient(90deg, #6a8cff, #9b6cff)` 已抽成 `--brand-gradient`
  （深浅两套），随 `--accent-color` 走；深色模式下的固定黑阴影（`rgba(0,0,0,.08~.18)`）
  改为半透明的 `rgba(15,20,30,…)`，深浅通用。
- [ ] **死配置**：`params.toml` 的 `[imageProcessing.cover]`（主题 0 引用）、`math = false` 但 `markup.toml` 配了 `$$` passthrough
  （写公式会渲染成裸公式）、`config.toml` 的 `disqusShortname`（v3 遗留）、`params.toml` 里约 70 行未使用评论渠道的空字段。
- [ ] **配置隐患**：`config/_default/_languages.toml` 写着 `title = "Example Site"`，一旦被改名为 `languages.toml` 启用多语言会生效。建议删除。
- [ ] **JS 性能**：`footer/custom.html:30-46` 的 scroll 监听无节流，每次事件都读 `scrollHeight`/`clientHeight` 强制重排
  + 写 `style.width`（还叠了 CSS `transition`），长文滚动掉帧。建议 rAF 包裹 + 缓存尺寸 + resize debounce。
- [ ] **供应链 / 第三方**：`head/custom.html` 从 jsDelivr 拉 JetBrains Mono，两个 `<link rel=stylesheet>` 是**渲染阻塞**且无 SRI；
  `footer/custom.html:10` 不蒜子用协议相对 URL `//`。
- [ ] **工程基线**：`.gitignore` 漏 `.DS_Store`（当前工作区已有 5 个未跟踪）；缺 `.editorconfig` / `.gitattributes` / Dependabot；
  `assets/jsconfig.json` 提交了本机绝对路径 `../../../Library/Caches/...`。
- [ ] **文档失真**：`README.md` 标题仍是 "Hugo Theme Stack Starter Template"，还在教人拉 v3 主题和改 gh-pages 分支；
  `LICENSE` 是主题作者的 MIT，而站点声明 CC BY-NC-SA 4.0（且文章多为公司内部系统设计内容，非商业条款有授权风险）。
- [ ] （后续新增待办请追加到此处）

## CI/CD

- 推送 `main` / `master` 自动触发 `.github/workflows/deploy.yml`：Hugo 构建（`--gc --minify`）→ 上传 artifact → 部署 GitHub Pages。
- `.github/workflows/update-theme.yml` 每日自动更新 Stack 主题，但**推到 `ci/update-theme` 分支、不自动上线**，
  需人工验证后合并（构建校验失败时不会产生提交）。
- CI 环境：**Hugo 0.166.0 Extended**（`HUGO_VERSION` 唯一定义，下限 0.158.0，有断言保护）、
  Dart Sass 1.97.1、Go 1.25.5。**已移除** `TZ: Europe/Oslo`（改由 `config.toml` 的 `timeZone` 控制）、
  Node 24.12.0（无 `package.json`，已删除相关步骤）。
- Hugo 资源缓存 key 由 `hashFiles('go.sum', 'config/**', 'assets/**')` 决定，**不要改回 `github.run_id`**。
- **升级/下调 Hugo 版本前**，务必确认主题 v4.0.3 所需的 API（当前下限 0.158.0），
  并让**本地与 CI 用同一版本**验证——历史上正是「本地 0.166 + CI 0.154」这个错配导致过全站渲染失败。

## 交接提示（Quick Start）

1. 改**样式**：先看 `assets/scss/custom.scss`（有编号分节），注意 `1rem = 10px`。
2. 改**首页 widget**：`config/_default/params.toml` 的 `[[widgets.homepage]]` + `layouts/_partials/widget/*`。
3. 改**布局/短代码**：`layouts/`（覆盖主题同名文件即可）。
4. 改**图片**：先读「4. 图片处理与体积控制」。远程图片不会自动下载，照片类封面请直接用 WebP。
5. 提交前建议执行 `hugo --quiet` 做一次构建校验。
6. 完成后**记得回来更新本文件**（尤其「修改记录」与「未来计划」）。
