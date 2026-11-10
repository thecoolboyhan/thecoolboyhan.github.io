---
title: dmla-mps-lab：没有独显，也能走完 LLM 预训练与 SFT 两章
slug: dmla-mps-lab
description: 给《设计机器学习应用系统》读者的补充实验方案：把网页里 GPU-only 的 Transformer 预训练与 SFT 对话两章，搬到 Apple Silicon / Linux / Windows 上，用降配模型跑通完整链路。设备自动检测 CUDA / MPS / CPU，不依赖 Docker、CUDA 与 Git LFS，仅用于个人学习。
date: 2021-01-01
categories:
  - 开源
  - AI
tags:
  - 开源项目
  - 大语言模型
  - PyTorch
  - Apple Silicon
  - LLM
---

[TOC]

## 项目简介

**dmla-mps-lab** 是我在读《设计机器学习应用系统》（DMLA）时整理的一套**补充实验材料**：把书里两个 GPU-only 的章节——Transformer 预训练与 SFT 对话——搬到没有 NVIDIA 显卡的机器上，用降配模型把完整链路亲手跑一遍。

> **项目定位**：这是写给「没有独显、显存不够、或只有 Apple Silicon / 纯 CPU」的读者的教学方案，<span class="text-red">**不是对网页结果的复现**</span>。目标是把链路跑通、把 loss 曲线看懂、观察「续写模型」经 SFT 变成「对话模型」，而不是训出一个能用的助手。

- GitHub 仓库：<https://github.com/thecoolboyhan/dmla-mps-lab>
- 配套文章：[Transformer 模型预训练实验](https://ai.icyfenix.cn/language-models/architecture-basics/llm-pretrain-experiment.html)、[工程实训：SFT 模型对话实验](https://ai.icyfenix.cn/language-models/pretraining/llm-sft-experiment.html)
- 许可证：**CC BY-NC-SA 4.0**（上游要求衍生作品同许可证、非商业）

## 为什么要做这个

网页的预训练章节有 6 个可点击代码块，其中 **5 个标了 `data-gpu-only="true"`**；云端 Serverless 端点也因费用原因未开放 GPU，训练章必须自行部署 Docker + NVIDIA GPU 沙箱。而 Apple Silicon 上既没有 CUDA，也没有 FlashAttention / NVIDIA Container Toolkit 的对应实现。

我实测过同构的 63.91M 模型在 M5 上的单步耗时，按网页原版规模外推需要 **66~105 小时以上**——这个量级显然不适合作为「跟着书做一遍」的实验。

所以这个项目只做三件事：

1. **运行后端通用化**：设备自动检测 `cuda > mps > cpu`，BF16 autocast 按后端能力启用；DataLoader 单进程；checkpoint 存 FP32 便于跨平台互读。
2. **数值降配**：模型 13.52M（384 / 6 层）、序列 256、12 万条语料，把训练压到 1~2 小时。<span class="text-blue">**等效批大小仍保持 256 不变**</span>，改的只是梯度累积频率，优化语义与网页一致。
3. **去掉环境依赖**：用 Python 标准库的 HTTP Range 分段下载语料，代替 `dmla data` + Git LFS + Docker + curl，macOS / Linux / Windows 行为一致。

模型定义、数据集类、损失函数、优化器、余弦调度、ChatML 模板与 labels 掩码都沿用网页原版，**改的只有「跑在什么上面」和「跑多大」**。

## 与网页原版的差异

| 项 | 网页原版 | 本项目 standard 档 |
| --- | --- | --- |
| 模型 | 63.91M（768 / 8 层） | 13.52M（384 / 6 层） |
| 语料 | 约 127 万条 × 2 epoch | 12 万条 × 2 epoch |
| 序列长度 | 512 | 256 |
| 等效批大小 | 256 | 256（不变） |
| 运行方式 | 网页 Run → Docker + CUDA 沙箱 | 本地终端逐脚本，三后端通用 |
| 数据获取 | `dmla data` 全量 1.2 GB | 标准库 Range 采样约 160 MB |
| 设备 / 耗时 | RTX 5080 约 2.5 h | Apple M5 实测 86 min |
| 最终 loss | 约 1.85 | 实测 3.029 |

缩短序列的依据是真实语料的 token 长度分布：p50≈211、p90≈378、mean≈237，`seq_len=512` 时约 **59% 的算力花在 padding 上**；改成 256 只损失少量有效 token，注意力计算量却减半。

完整的逐项对照（环境、超参、SFT、代码改了什么没改什么、能得到什么）写在仓库的 [COMPARISON.md](https://github.com/thecoolboyhan/dmla-mps-lab/blob/main/COMPARISON.md) 里。

## 支持哪些平台

| 平台 | 自动选中 | 状态 |
| --- | --- | --- |
| Apple Silicon Mac（macOS 14+） | MPS + BF16 | 完整实测 |
| Linux / Windows + NVIDIA GPU | CUDA + BF16 | 自动启用，真机未实测 |
| 纯 CPU / WSL2 | CPU + FP32 | 链路一致，慢一个数量级 |
| Intel Mac（macOS x86_64） | — | `torch 2.15.0` 只有 arm64 wheel，需自行换版本 |

有 N 卡也会自动走 CUDA，但降配仍在——想复现网页原版指标，还是该直接用书里的 GPU 沙箱。

## 快速开始

```bash
git clone https://github.com/thecoolboyhan/dmla-mps-lab.git
cd dmla-mps-lab

bash setup.sh        # macOS / Linux；Windows 用 setup.ps1

# 第 1 章：预训练
<venv-python> stage0_setup.py       # 首次联网下载语料与分词器
<venv-python> stage1_tokenizer.py
<venv-python> stage2_model.py
<venv-python> stage3_train.py       # M5 standard 档约 86 分钟
<venv-python> stage4_generate.py
<venv-python> play_pretrain.py      # 可选：输入一句话看它接什么

# 第 2 章：SFT
<venv-python> stage5_sft_data.py
<venv-python> stage6_sft_train.py
<venv-python> stage7_sft_chat.py
```

`<venv-python>` 在 macOS / Linux 是 `.venv/bin/python`，在 Windows PowerShell 是 `.venv\Scripts\python.exe`；脚本运行时打印的「下一步」会自动给出正确路径。想先验证链路，<span class="text-green">**用 `PRESET=quick` 十几分钟就能走完 0→4**</span>。

## 八个阶段脚本

| 网页 | 本项目 |
| --- | --- |
| 实验准备 · `dmla data` + 文件检查 | `stage0_setup.py`、`stage1_tokenizer.py` |
| 第 1 阶段 · 分词器 / `PretrainDataset` | `stage1_tokenizer.py`、`shared/pretrain_dataset.py` |
| 第 2 阶段 · 模型定义 | `stage2_model.py`、`shared/mini_mind_config.py` |
| 第 3 阶段 · 预训练 | `stage3_train.py` |
| 第 4 阶段 · 推理续写 | `stage4_generate.py`、`play_pretrain.py` |
| 第 2 章 · SFT 语料 / ChatML / labels 掩码 | `stage5_sft_data.py`、`shared/sft_dataset.py` |
| 第 2 章 · SFT 训练 | `stage6_sft_train.py` |
| 第 2 章 · 对话服务 | `stage7_sft_chat.py` |

逐步该看懂什么、验收清单、对照实验和常见坑见仓库的 [GUIDE.md](https://github.com/thecoolboyhan/dmla-mps-lab/blob/main/GUIDE.md)；接手维护的 AI 助手可以先读仓库里的 [AGENTS.md](https://github.com/thecoolboyhan/dmla-mps-lab/blob/main/AGENTS.md)。

## 实测记录

| 项目 | 结果（Apple M5 / 16GB） |
| --- | --- |
| 预训练 standard 档 | 15,000 步，86.3 分钟，平均 0.345 s/step |
| loss 曲线 | 8.110 → **3.029**，降幅 5.08 |
| 续写效果 | 中文通顺、有主题词，但内容会胡说、重复；英文 prompt 破碎 |
| 权重健康 | `missing=0 / unexpected=0`，FP32，无 NaN/Inf |
| SFT 阶段 | 20 步冒烟通过，初始 loss 1.906 |

{{< hint "warning" >}}
**完整 SFT 1,875 步训练尚未跑完**，最终对话质量未实测，文档里的「约 30 分钟」只是前 200 步外推。CUDA 分支目前也只做了逻辑测试，本机没有 N 卡。这些边界在 README 与 COMPARISON 里都如实标注了。
{{< /hint >}}

## 能得到什么，得不到什么

**能得到**：完整链路（数据 → 分词 → Dataset → 模型 → 训练 → loss 曲线 → checkpoint → 推理 → SFT → 对话）；亲手观察 loss 从 ≈8.76 下降、初期陡降后期趋缓与余弦 LR 的关系；混合精度、梯度累积、梯度裁剪、checkpoint 的工程手感；以及 ChatML + labels 掩码如何把续写变成对话。

**得不到**：网页的 loss 1.85、64M 全量指标、一个日常可用的助手、英文能力、事实正确性，以及 CUDA / FlashAttention / 多卡分布式的真实经验。

预训练模型只会续写、不会对话，这是网页的设计，不是 bug；SFT 赋予的是**对话行为**而非知识，64M 级模型仍会把「1+1」答成 3。

## 仓库里不含什么

模型权重、语料、分词器、官方预训练权重、`.venv`、checkpoint 都不在仓库里，全部由脚本按需联网下载（ModelScope 国内镜像）或训练生成。仓库只有代码和文档，约 600 KB。仓库里附了一份真实的 150 点 loss 曲线样例，不训练也能看曲线形状。

## 许可证与署名

上游《设计机器学习应用系统》采用 **CC BY-NC-SA 4.0**，其 README 明确要求衍生作品署名、非商业、以相同许可证发布。因此本项目同许可证发布，**不能改用 MIT / Apache，也不得用于商业用途**；逐文件引用与改编清单见仓库的 `NOTICE.md`。本项目不是 DMLA 官方项目，与作者无关联。

## 关于我

这个项目是我在读 DMLA 的大语言模型章节时，因为手头没有独显而整理出来的补充材料；博客里也有一组《读〈设计机器学习应用系统〉有感》的读书笔记，欢迎一起交流。

- 博客：[韩永发的博客](https://thecoolboyhan.github.io)
- GitHub：[thecoolboyhan](https://github.com/thecoolboyhan)
- 项目地址：<https://github.com/thecoolboyhan/dmla-mps-lab>

如果这套材料帮你把两章跑通了，欢迎到仓库提 Issue 或点个 Star ⭐。
