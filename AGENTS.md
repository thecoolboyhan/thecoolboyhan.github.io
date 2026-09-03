# AGENTS.md

## 项目概述

这是基于 Hugo + Stack v4 主题构建的个人博客项目，托管于 GitHub Pages。博客内容以中文为主，涵盖技术读书笔记、算法题解、架构设计等主题。

## 技术栈

- **静态站点生成器**: Hugo Extended (v0.154.2+)
- **主题**: CaiJimmy/hugo-theme-stack v4
- **部署**: GitHub Actions → GitHub Pages
- **时区**: Asia/Shanghai
- **语言**: 中文 (zh-CN)，启用 hasCJKLanguage

## 本地运行

```bash
hugo server -D
```

默认访问 `http://localhost:1313/`。

## 内容规范

- 文章存放于 `content/post/`，按系列或日期组织
- Front matter 中可设置 `series: ["系列名称"]` 以启用系列关联
- 图片建议放在 `static/images/` 或文章目录内（主题已开启 imageProcessing）

## 脚本工具

### `scripts/format_posts.py`

博客文章批量排版与错别字修复脚本。仅作用于非代码块区域，安全可复现。

**用法：**

```bash
# 预览改动（不写文件）
python3 scripts/format_posts.py --dry

# 实际应用修改
python3 scripts/format_posts.py

# 只处理单个文件
python3 scripts/format_posts.py --file content/post/xxx.md
```

**功能：**
- 压缩连续空行（最多保留 1 行）
- 标题/列表前后自动补空行
- 基于词典修复常见错别字（仅正文区域，代码块内完全保护）

## 配置要点

- 分页大小：`config/_default/config.toml` 中的 `pagerSize`
- 首页 widget：`config/_default/params.toml`
- 评论：Giscus（需开启仓库 Discussions）
- 代码高亮：Chroma，已配置行号、tabWidth=4

## CI/CD

- 推送至 `main`/`master` 分支自动触发 GitHub Actions 构建部署
- 每日自动更新主题（`update-theme.yml`）
