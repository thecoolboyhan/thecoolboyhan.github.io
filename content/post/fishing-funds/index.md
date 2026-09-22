---
title: Fishing Funds：基金 / 大盘 / 股票 / 虚拟货币状态栏小应用
slug: fishing-funds
description: Fishing Funds 是一款基于 Electron 的跨平台状态栏小应用，可在菜单栏实时查看基金涨跌与估算收益、大盘指数、板块行情、股票走势和加密货币行情。本文是该项目的官方主页与使用说明（独立维护版，基于 fishing-funds v8.7.1，GPL-3.0）。
date: 2021-01-01
image: banner.png
categories:
  - 开源
  - 工具
tags:
  - 开源项目
  - Electron
  - TypeScript
  - 基金
  - 理财
---

[TOC]

## 项目简介

**Fishing Funds** 是一款跨平台（macOS / Windows / Linux）的**状态栏 / 菜单栏小应用**，常驻在系统顶栏，随手一点就能看到：

- 基金实时涨跌与**估算收益**
- 大盘指数行情
- 板块涨跌排行
- 股票走势
- 加密虚拟货币行情

数据来源于天天基金、蚂蚁基金、同花顺·爱基金、腾讯证券等公开接口。软件完全开源免费，纯个人自用的状态栏小插件，仅供学习交流。

> 项目地址：<https://github.com/thecoolboyhan/fishing-funds>
> 当前分支：`maintain-8.7.1` ｜ 许可证：GPL-3.0 ｜ 技术栈：Electron + TypeScript + React

## 为什么会有这个独立维护版

这个仓库的代码**派生自 [`1zilc/fishing-funds`](https://github.com/1zilc/fishing-funds) v8.7.1**（GPL-3.0），目前由本仓库**独立维护，与上游不再同步**。

选择 v8.7.1 作为基线的原因：

- 官方 8.8.0 把**数据层核心**（东方财富反爬绕过逻辑）抽成了**闭源子模块**，仅凭公开源码无法独立编译；
- v8.7.1 的数据层是**完整开源**的，可以自行构建、自行修复，更适合长期自维护。

因此本仓库**关闭了官方自动更新**——你拿到的构建产物只来自本仓库的代码。

{{< hint "info" >}}
一句话总结：这是一个「能自己编译、能自己改」的版本，数据层逻辑全部可见。
{{< /hint >}}

## 功能一览

### 基金：涨跌与估算收益

支持添加基金、标记持有份额与持仓成本价，实时展示今日涨幅、净值、持有收益与估算收益。

![基金列表与今日涨幅](1.png)

### 指数：一屏看全大盘

上证指数、深证成指、沪深 300、中小 100、创业板指、上证 50、中证 500 等常用指数一屏尽览。

![大盘指数行情](2.png)

### 板块行情与排行

板块涨跌幅、领涨个股、总市值、涨跌家数、换手率等信息一目了然。

![板块行情与排行](3.png)

除此之外，还包含：

- **股票 / 虚拟货币**行情展示
- **AI 识别录入**：截图即可批量导入基金
- **导入 / 导出**：JSON 配置随时备份
- **配置同步**：借助 iCloud、OneDrive 实现多设备同步

## 数据源与推荐

不同数据源可能存在反爬机制，刷新速度会有差异。

| 数据源 | 评级 | 说明 |
| --- | --- | --- |
| 东方财富 · 天天基金 | ★★★★★ | 推荐，最快且估值最准确 |
| 支付宝 · 蚂蚁基金 | ★★★☆☆ | 可用 |
| 同花顺 · 爱基金 | ★★★☆☆ | 可用 |
| 腾讯证券 | ★★★☆☆ | 可用 |

{{< hint "tip" >}}
强烈建议使用「天天基金」数据源，刷新最快、估值最准。
{{< /hint >}}

## 下载与安装

可直接在仓库的 Releases 或自行构建产物中下载对应平台的客户端。

{{< hint "warning" >}}
macOS 不允许直接打开未签名程序。若提示「已损坏」或无法打开，可通过「系统设置 → 隐私与安全性 → 仍要打开」放行，或使用 xattr 命令解除隔离标记。此类操作涉及运行未签名程序，请自行确认来源可信后再进行。
{{< /hint >}}

## 本地构建

本地构建需要 **Node ≥ 22.8**。

```bash
# 跳过 phantomjs 等会下载二进制的 postinstall
npm install --ignore-scripts

# 单独下载 Electron 运行时
node node_modules/electron/install.js

# 构建，产出 release/app/dist
npm run build

# 打包 macOS dmg（未签名）
npm run package-mac
```

说明：开发热更新 `npm run dev` 依赖 **bun**；而 `build` / `package-*` 只需要 electron-vite + electron-builder，**无需 bun**。

## 系统代理配置

受网络环境影响，部分货币行情接口可能无法直接访问。本应用已适配系统代理，支持 **HTTP 代理**与 **SOCKS 代理**。

只需把下面两个域名加入代理软件规则，然后重启应用即可：

```text
api.coingecko.com
api.coincap.io
```

## AI 识别录入

应用支持用 AI **识别截图导入基金**，需要具备**视觉能力**的大模型（推荐 `gpt-4o`、`grok`、`gemini-2.5-pro`、`qwen2.5vl:32b` 及以上）。

使用方式：

1. 在「设置 → AI」中配置 **OpenAI 兼容接口**的请求地址与 API Key；
2. 进入某宝 → 理财 → 总资产 → 我的资产 → 全部持有，**长截图**，确保包含基金名称、持有收益、累计收益三项数据；
3. 交给应用识别并导入。

{{< hint "danger" >}}
使用前请务必了解该功能：请确保接口地址安全，应用不保证识别过程中的数据不会泄露至第三方。你的 API Key 由应用本地保存，不会收集或上传。
{{< /hint >}}

## 导入 / 导出

右键菜单支持导入 / 导出基金 JSON 配置，方便备份与迁移。

```typescript
interface FundSetting {
  code: string;   // 基金代码（必填）
  name?: string;  // 基金名称
  cyfe?: number;  // 持有份额
  cbj?: number;   // 持仓成本价
}
```

示例：

```json
[
  { "code": "320007", "name": "诺安成长混合", "cyfe": 1000.0, "cbj": 1.6988 },
  { "code": "161725", "name": "招商中证白酒指数(LOF)", "cyfe": 1000.0, "cbj": 1.4896 }
]
```

## 配置同步

在设置中开启后，应用会自动把配置文件存储到指定路径，并在启动时优先读取该路径的配置。

借助 iCloud、OneDrive 等工具同步这个文件，即可实现**多设备配置同步**，支持钱包、基金、指数、板块、股票、货币、H5 的配置。

## 技术栈

- **框架 / 运行时**：Electron、electron-vite、electron-builder
- **UI 与组件**：React、Ant Design、menubar、Remix Icon
- **图表**：echarts
- **工具库**：ahooks
- **语言 / 工程**：TypeScript、PostCSS、pnpm
- **环境要求**：Node ≥ 22.8（开发热更新需 bun）

## 常见问题

**Q：为什么打不开 / 提示已损坏？**
macOS 对未签名程序的限制，按「下载与安装」中的方式放行即可。

**Q：数据准确吗？**
所有数据仅供参考，**收益或亏损以当天实际为准**；走势与排行数据均来自第三方网站，不代表作者观点。软件不构成任何投资建议。

**Q：货币行情刷不出来？**
把 `api.coingecko.com`、`api.coincap.io` 加入代理规则后重启应用。

**Q：会收集我的数据吗？**
不会。API Key 仅保存在本地，不会收集或上传；但 AI 识别功能依赖第三方大模型，请自行评估数据泄露风险。

## 许可证

本项目基于 **GPL-3.0** 开源。原项目及本派生版本均遵循 GPL-3.0：

- 个人自用 / 自行构建：**零义务**；
- 若对外发布：须保持 GPL-3.0，并**公开你的修改源码**。

详见仓库 [LICENSE](https://github.com/thecoolboyhan/fishing-funds/blob/maintain-8.7.1/LICENSE)。

## 致谢

UI 与数据层代码派生自 [`1zilc/fishing-funds`](https://github.com/1zilc/fishing-funds) v8.7.1，并在此基础上独立维护。同时感谢以下优秀的开源项目：

- [electron-vite](https://github.com/alex8088/electron-vite)
- [menubar](https://github.com/maxogden/menubar)
- [Ant Design](https://github.com/ant-design/ant-design/)
- [ahooks](https://github.com/alibaba/hooks)
- [echarts](https://github.com/apache/echarts)
- [Remix Icon](https://github.com/Remix-Design/RemixIcon)

## 相关链接

- GitHub 仓库：<https://github.com/thecoolboyhan/fishing-funds>
- 上游原项目：<https://github.com/1zilc/fishing-funds>
- 问题反馈：欢迎在仓库提 Issue；如果对你有帮助，欢迎点个 Star ⭐
