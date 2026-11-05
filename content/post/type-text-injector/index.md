---
title: type-text-injector：把文本「敲」进虚拟机与远程桌面的小工具
slug: type-text-injector
description: 一个用 Rust 写的跨平台小工具，把本机文本通过「逐键模拟键盘输入」打进当前光标处，专治 Parallels / VMware 虚拟机、远程桌面、受限 App 里没法粘贴的场景。v0.3.0 起 macOS / Linux / Windows 三端统一为真实键事件，支持长文本自动分批，含 Material 风格 GUI，MIT 开源。
date: 2021-01-01
image: gui-preview.png
categories:
  - 开源
  - 工具
tags:
  - 开源项目
  - Rust
  - 效率工具
  - 虚拟机
  - 远程桌面
---

## 项目简介

**type-text-injector** 解决的是一个很具体的痛点：

> 你 Mac 上有一份文本，要打进 **Parallels / VMware 里的 Windows 虚拟机** —— 剪贴板共享被禁、没法直接粘贴。
> 启动程序 → 粘贴文本 → 5 秒后，它替你把字**一个键一个键地「敲」** 进虚拟机里。

它把本机文本**逐键模拟键盘输入**到当前光标处，适合远程桌面、虚拟机、受限 App、没有粘贴接口的界面。

![GUI 界面](gui-preview.png)

{{< hint "warning" >}}
中文 / 非 ASCII 字符会被跳过：本工具只处理英文、数字与标点。三个平台都只做键盘模拟，不经过剪贴板。
{{< /hint >}}

- GitHub 仓库：<https://github.com/thecoolboyhan/type-text-injector>
- 当前版本：v0.3.0（[下载](https://github.com/thecoolboyhan/type-text-injector/releases/tag/v0.3.0)）
- 语言 / 许可：Rust（MIT）

## 为什么需要它

往虚拟机里打字，最朴素的写法是把整段文本一次性塞进键盘事件，但你会发现 —— **回车键生效了（行数对），字母数字却几乎全丢**，只剩下零星几个大写字母。

原因在于：

- 虚拟机 / 远程桌面只认 **HID 扫描码**；
- 一次性塞字符串走的是 **Unicode 字符串载荷**，客户机拿不到扫描码 → 整串被丢弃；
- 只有真实**虚拟键码**能映射成 HID 报告 → 正常进字。

这里有个很隐蔽的坑：v0.3.0 之前只有 macOS 后端是真正的 keycode 级注入，而 Windows 用的 `enigo.text()` 恰好就是「Unicode 字符串载荷」。它确实调用了 `SendInput`，但带的是 `KEYEVENTF_UNICODE` —— `wVk` 恒为 0、`wScan` 直接是 UTF-16 码元。普通窗口能收到，虚拟机 / 远程桌面 / 受限窗口收不到。代码读起来"在用 SendInput"，实际走的却是字符注入，光看 API 名字根本发现不了。

v0.3.0 把这条路径彻底删掉了。

## 三端注入方式

现在三个平台都是**逐键真实键事件**，同一个字符在三端按下的是同一组物理键：

| 平台 | 注入后端 | 事件载体 | 前置依赖 | GUI |
| --- | --- | --- | --- | --- |
| macOS | AppleScript `key code N` | 虚拟键码 → HID 扫描码 | 系统自带；需「辅助功能」授权 | ✅ |
| Linux | `xdotool type` / `key` | X11 XTEST 按键事件 | 需安装 `xdotool`；仅 X11 会话 | ✅ |
| Windows | enigo `key(Key::Other(vk))` | Win32 `SendInput` + `wVk` + 扫描码 | 自动包含，无需额外依赖 | ✅（glow 后端） |

Release 页提供三个平台编译好的可执行文件，开箱即用（Windows 版需本机有 VC++ 运行库，一般已自带）。

> 虚拟机场景的实测只覆盖 macOS（Parallels / VMware）。Linux / Windows 的事件层级与 macOS 相同，但本项目没有在虚拟机里实测过，建议先用 `-p` 自检。

### Windows 端两个必须自己处理的细节

1. **Shift 得自己按**。enigo 的 `Key::Unicode(c)` 会用 `VkKeyScanExW` 按**当前键盘布局**映射，而且把返回值里的 shift 状态位丢掉了 —— 直接用它打大写和 `@#$%` 会出错。所以字符映射写死成 US ANSI 表，需要 Shift 时显式 `Press` / `Release`。
2. **`Key::Other(vk)` 里的 vk 是 Win32 虚拟键码**，不是 macOS 键码。字母 `0x41..=0x5A`、数字 `0x30..=0x39`、`-`=0xBD、`=`=0xBB、`;`=0xBA、`'`=0xDE、`,`=0xBC、`.`=0xBE、`/`=0xBF、空格 0x20、Tab 0x09、回车 0x0D。macOS 那套数值不能直接搬过来。

## 三端一致性怎么保证

光"都是键盘事件"还不够。三端如果各算各的，同一段文本会打出不同的键、报不同的数字。所以口径全部抽到公共层，三端共用：

| 公共项 | 作用 |
| --- | --- |
| `plan(text)` | 决定哪些字符算一个键、跳过哪些、保留多少跳过样本 |
| `BATCH_KEYS = 4000` | 长文本分批大小，也是三端共同的批边界 |
| `line_delay_ms()` | 换行 / 批边界的额外停顿，`max(间隔×3, 60)` ms |
| `needs_shift(c)` | US ANSI 下该字符是否需要 Shift |
| `base_key(c)` | 字符对应的「未按 Shift 的基础键」：`A`→`a`、`@`→`2`、`?`→`/` |

配套的单测就是用来锁这件事的：新增的两条断言遍历全部可打印 ASCII，检查「归一后的基础字符一定可注入、且不需要 Shift」，以及「macOS 键码表里的 Shift 判定与公共判定逐字符一致」。这样才敢说三端按的是同一组物理键。

还有个容易忽略的点：`xdotool type` 自己默认每字 12ms 延迟，会和用户设置的每键间隔叠加，导致同样的参数在 Linux 上比另外两端慢一截。v0.3.0 改成 `--delay 0`，节奏统一由程序控制。

## 长文本

macOS 上单条 AppleScript 有个硬上限：`set ks to {...}` 字面量大约 8080 个数字项（等于 4039 键）就会报「堆栈溢出 (-2706)」。这跟文本内容无关，纯粹是解释器的项数上限。所以超过 4000 键必须拆。

v0.3.0 的做法是按 `BATCH_KEYS` 切片，逐批生成独立脚本依次执行，**仍然是 key code 级注入**，虚拟机场景不会因为分批而退化：

- 每批最多 4000 键；批间留一次 `max(间隔×3, 60)` ms 的缓冲停顿，避免交界处丢字；
- Linux / Windows 逐键循环本来没这个上限，但在同一位置留了同样的停顿，三端节奏一致；
- 中途失败会明确报「第 X/Y 批」，已注入的批次不会回滚。

实测 5 万字符拆成 13 批，单批从未超过 8000 项。

## 图形界面（GUI）

`type-text --gui` 打开 Material 风格的图形界面，**同进程调用注入逻辑**（不 spawn 子进程）：

- 文本框输入 / 粘贴 / 从文件读取 / 一键清空
- 输入时**实时统计**：可注入键数、预计耗时、批次数、被跳过的字符数（与 CLI 同一口径）
- **预览**：字符数、行数、注入键数、预计耗时、注入批次、跳过字符（纯函数解析，不注入）
- 倒计时 0–99 秒（0 = 立即注入）、每键间隔 1–5000 ms 拖拽调节
- 注入中显示**进度条**：已用时间 / 预计耗时、键数、批数
- Pixel 风格动画：环形倒计时（末 3 秒橙 → 红渐变）、旋转 spinner、按钮悬停反馈
- 三端界面结构、配色、字号保持一致，只有排错提示按平台变化；标题栏显示版本与平台

```bash
cargo build --release
./target/release/type-text --gui
```

{{< hint "info" >}}
macOS 首次真实注入需要在「系统设置 → 隐私与安全性 → 辅助功能」中授权。
{{< /hint >}}

## 前置条件

1. 运行时会先**倒计时 N 秒**，请把光标点到目标窗口（如虚拟机的记事本）再等它注入；
2. **macOS**：在「系统设置 → 隐私与安全性 → 辅助功能」中把运行本程序的终端 / App 加进去并勾选（未授权时按键会静默失效）；
3. **Linux**：已安装 `xdotool`，且当前是 X11 会话（Wayland 需改用 `ydotool`，本工具暂未支持）；
4. **Windows**：直接可用。

## 安装 / 编译

### 方式 A：直接下载 Release 二进制（最简单）

到 [Releases](https://github.com/thecoolboyhan/type-text-injector/releases) 页面，按系统下载：

- **macOS**：`type-text-macos`（Apple Silicon）
- **Linux**：`type-text-linux`（x86_64，静态链接 musl，纯 CLI）
- **Windows**：`type-text-windows.exe`

这些文件由 GitHub Actions 在推 `v*` tag 时自动交叉编译并发布到 Releases，无需本机编译。

### 方式 B：Cargo（推荐开发者）

```bash
git clone https://github.com/thecoolboyhan/type-text-injector.git
cd type-text-injector
cargo build --release
# 产物：target/release/type-text（平台对应后缀）
```

### 方式 C：零依赖单文件编译（仅 macOS / Linux，无需联网）

源码核心使用 Rust 标准库（Windows 版需 enigo，仍走 Cargo）：

```bash
rustc -O src/main.rs -o type-text
```

## 用法

### 交互式（最常用）

```bash
./type-text            # 启动后按提示粘贴文本，准备 5 秒、每键 50ms
```

流程大致如下：

```text
$ ./type-text
请输入要输入的文本，输入完后按回车，再按 Ctrl-D 结束：（Windows：Ctrl-Z 或 Ctrl-D）
（粘贴你的文本）
^D
已收到 25 行 / 1240 字符，每键间隔 50ms，预计耗时约 66 秒；5 秒后开始输入。
5 秒后开始输入，请把光标点到目标位置…   4   3   2   1
开始输入…
完成，共输入 1240 个键。
```

> 终端里结束输入：先按一次回车，再按 **Ctrl-D**（Windows 用 **Ctrl-Z** 或 Ctrl-D；若没反应，再按一次）。

### 管道 / 重定向

```bash
cat data.txt | ./type-text 5 80      # 准备 5 秒、每键 80ms
./type-text 10 < data.txt            # 准备 10 秒
echo "hello world" | ./type-text     # 直接喂一行
```

## 参数

位置无关，支持位置参数：

| 写法 | 含义 |
| --- | --- |
| `./type-text` | 默认：准备 5 秒，每键间隔 50ms |
| `./type-text 10` | 第 1 个数字 = **准备秒数**（注入前的倒计时） |
| `./type-text 5 80` | 第 2 个数字 = **每键间隔毫秒**（虚拟机丢字就调大这个） |
| `./type-text -n` | 只预览解析结果，不真正注入键盘（调试用） |
| `./type-text -p` | 自检：打一行标记，确认注入是否生效 |
| `./type-text --gui` | 打开图形界面 |

### 虚拟机里还漏字怎么办

字符仍可能被零星丢掉（客户机键盘缓冲溢出 / HID 队列丢弃）。唯一有效的手段是**拉大每键间隔**：

```bash
./type-text 5 80     # 还漏就 5 120、5 200，逐档加
```

代价是耗时：1240 字符 × 50ms ≈ 62 秒。开工前程序会打印预计耗时，心里有数即可。

## 支持的输入范围

- `a-z` `A-Z` `0-9`
- 符号：`!@#$%^&*()_-+=[]{};:'",.<>/?\|` `` ` `` `~`
- 空格、Tab、换行
- **非 ASCII（含中文）会被自动跳过**，并在结尾提示被跳过的字符（只列出前 20 个样本，总数单独给出）

## 常见问题

**Q：按了没反应，一个字都没打出来？**
检查三点：① 倒计时结束时光标是否在目标窗口；② macOS 是否给了「辅助功能」权限；③ Linux 是否装了 `xdotool`。可先用 `./type-text -n` 确认解析正常。

**Q：三端效果真的一样吗？**
事件层级一样：都是逐键真实键事件，同一个字符对应同一组物理键，节奏参数也共用一套。差别只剩平台 API 本身的开销（macOS 一个脚本跑一批、Linux 每字起一个进程、Windows 直接 SendInput），所以**速度**会有差异，**按键内容**不会。

**Q：能打中文吗？**
当前只支持英文 / 数字 / 标点，非 ASCII 会被跳过。这不是限制没做，而是刻意不做 —— 中文没有键码，只能走 Unicode 字符串注入，而那正是虚拟机收不到的东西。

**Q：会改我的剪贴板吗？**
不会。文本走临时文件 / 进程内，不经过粘贴板。

**Q：会动我的鼠标吗？**
不会。只发键盘事件，永远打进「当前前台窗口的光标处」。

**Q：Linux 上 xdotool 找不到？**
`apt install xdotool`（Debian / Ubuntu）或对应发行版的包管理器；Wayland 用户需自行改用 ydotool 或切到 X11。

## 发布新版本

打一个 `v*` tag 推到 GitHub，CI 会自动构建三个平台并上传产物到对应 Release：

```bash
git tag v0.3.0
git push origin v0.3.0
```

三个平台是矩阵并行构建的，整次发版实测约 3 分钟（macOS 最快 1 分半左右，Windows 因为要编 eframe 通常最慢）。等 Actions 跑完，到 Releases 即可看到 `type-text-macos` / `type-text-linux` / `type-text-windows.exe` 三个产物。

## 许可证

**MIT** © thecoolboyhan，详见仓库 [LICENSE](https://github.com/thecoolboyhan/type-text-injector/blob/main/LICENSE)。

## 相关链接

- GitHub 仓库：<https://github.com/thecoolboyhan/type-text-injector>
- 下载 Releases：<https://github.com/thecoolboyhan/type-text-injector/releases>
- v0.3.0 发布说明：<https://github.com/thecoolboyhan/type-text-injector/releases/tag/v0.3.0>
