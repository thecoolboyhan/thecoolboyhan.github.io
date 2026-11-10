---
title: 开源项目
slug: links
links:
  - title: Fishing Funds（独立维护版）
    description: 基金 / 大盘 / 股票 / 虚拟货币状态栏小应用 · Electron + TypeScript，基于 fishing-funds v8.7.1 独立维护（GPL-3.0）——项目官网与使用说明见本站文章。
    website: /p/fishing-funds/
    repo: https://github.com/thecoolboyhan/fishing-funds
  - title: type-text-injector
    description: 把文本「敲」进虚拟机与远程桌面的小工具 · Rust 编写，支持 macOS / Linux / Windows，含图形界面——官网与使用说明见本站文章。
    website: /p/type-text-injector/
    repo: https://github.com/thecoolboyhan/type-text-injector
  - title: xiaomi-watch-s3-diy
    description: 小米手表 S3（M2313W1）自研表盘工程 · 平滑扫秒 / AOD / 圆角进度弧 + ws3 打包工具，附格式逆向参考——官网与使用说明见本站文章。
    website: /p/xiaomi-watch-s3-diy/
    repo: https://github.com/thecoolboyhan/xiaomi-watch-s3-diy
  - title: ai-platform
    description: AI 中台 —— 基于 Spring AI 2.0.1 + Ollama + JDK 25 的数据分析平台，对接 billing 计费系统经营数据大屏——官网与使用说明见本站文章。
    website: /p/ai-platform/
    repo: https://github.com/thecoolboyhan/ai-platform
  - title: dmla-mps-lab
    description: 给《设计机器学习应用系统》读者的补充实验方案 —— 没有独显也能把 Transformer 预训练与 SFT 两章完整走一遍，自动检测 CUDA / MPS / CPU，不依赖 Docker 与 Git LFS；完整介绍见本站文章，代码与逐步手册见下方仓库。
    website: /p/dmla-mps-lab/
    repo: https://github.com/thecoolboyhan/dmla-mps-lab
  - title: blogserver
    description: 博客相关的服务端 / 前端项目（SCSS）。
    website: https://github.com/thecoolboyhan/blogserver
  - title: portfolio-blog
    description: 个人作品集与博客项目（TypeScript）。
    website: https://github.com/thecoolboyhan/portfolio-blog
  - title: th_blogs
    description: 我的博客（早期版本）。
    website: https://github.com/thecoolboyhan/th_blogs
  - title: weidadeyongshi2.github.io
    description: 个人主页（HTML）。
    website: https://github.com/thecoolboyhan/weidadeyongshi2.github.io
  - title: personStudy
    description: 个人学习所用的 Java 仓库。
    website: https://github.com/thecoolboyhan/personStudy
  - title: rustStudy
    description: 个人学习 Rust 的仓库。
    website: https://github.com/thecoolboyhan/rustStudy
  - title: goByExample
    description: Go 语言学习项目。
    website: https://github.com/thecoolboyhan/goByExample
  - title: StudyOfSpringCloud
    description: 个人学习 Spring Cloud 的仓库。
    website: https://github.com/thecoolboyhan/StudyOfSpringCloud
  - title: thecoolboyhan.github.io
    description: 你正在浏览的这个博客站点，基于 Hugo + Stack v4 构建（SCSS）。
    website: https://github.com/thecoolboyhan/thecoolboyhan.github.io
menu:
    main: 
        weight: 4
        params:
            icon: link

comments: false
---

这里收录了我维护的**开源项目与仓库**。按内容分为「主要项目」与「学习 / 其他仓库」，点开即可跳转到对应项目。

## 主要项目

- **Fishing Funds**：跨平台的基金 / 行情状态栏小应用，官网与使用说明见 [本站文章](/p/fishing-funds/)。
- **type-text-injector**：把文字稳定「打」进虚拟机与远程桌面的小工具，详见 [本站文章](/p/type-text-injector/)。
- **xiaomi-watch-s3-diy**：小米手表 S3 自研表盘与 ws3 打包工具，详见 [本站文章](/p/xiaomi-watch-s3-diy/)。
- **ai-platform**：基于 Spring AI + Ollama + JDK 25 的 AI 中台示例，详见 [本站文章](/p/ai-platform/)。
- **dmla-mps-lab**：没有独显也能走完 LLM 预训练与 SFT 两章的教学降配实验，自动检测 CUDA / MPS / CPU，不依赖 Docker 与 Git LFS；介绍见 [本站文章](/p/dmla-mps-lab/)，代码见 [GitHub 仓库](https://github.com/thecoolboyhan/dmla-mps-lab)。

### 关于 dmla-mps-lab

网页里的「Transformer 预训练」与「SFT 对话」两章默认要 NVIDIA 显卡 + Docker 沙箱，云端 Serverless 端点也因费用原因不开放 GPU。这个项目把两章改成本地可跑的脚本：设备自动检测 `CUDA / MPS / CPU`，用标准库 HTTP Range 下载语料取代 `dmla data` + Git LFS，再把模型降到 13.52M，把「数据 → 分词 → 训练 → loss 曲线 → checkpoint → 续写 → SFT 对话」完整走一遍。

它**不是对网页结果的复现**（原版是 63.9M 模型、127 万样本、RTX 5080 约 2.5 小时、loss 约 1.85），目标是跑通链路、看懂训练过程、亲手观察「续写 → 对话」的转变。在 Apple M5 上完整预训练实测 **86 分钟，loss 8.11 → 3.03**：中文续写通顺，但内容仍会胡说。项目按上游要求以 **CC BY-NC-SA 4.0** 发布，仅供个人学习、非商业用途。

| 链接 | 内容 |
|---|---|
| [项目介绍文章](/p/dmla-mps-lab/) | 与网页原版的逐项差异、平台支持、快速开始、八阶段脚本映射、实测记录与能力边界 |
| [GitHub 仓库](https://github.com/thecoolboyhan/dmla-mps-lab) | 全部代码、`GUIDE.md` 逐步手册、`COMPARISON.md`、`AGENTS.md`、许可证（仓库不含权重与语料） |
| [DMLA · Transformer 模型预训练实验](https://ai.icyfenix.cn/language-models/architecture-basics/llm-pretrain-experiment.html) | 第 1 章原文 |
| [DMLA · SFT 模型对话实验](https://ai.icyfenix.cn/language-models/pretraining/llm-sft-experiment.html) | 第 2 章原文 |

## 学习 / 其他仓库

- **personStudy**、**rustStudy**、**goByExample**、**StudyOfSpringCloud**：个人学习过程中沉淀的练习仓库。
- **blogserver**、**portfolio-blog**、**th_blogs**、**weidadeyongshi2.github.io**、**thecoolboyhan.github.io**：博客与个人主页相关的项目。

> 如果你对某个项目感兴趣，欢迎到对应仓库提 Issue 或点个 Star ⭐。
