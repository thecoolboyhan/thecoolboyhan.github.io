---
title: AI 中台：Spring AI 2.0.1 + Ollama + JDK 25 的数据分析平台
slug: ai-platform
description: 一个以「学习新特性」为导向的 AI 中台示例：基于 Spring AI 2.0.1 + Ollama（deepseek-r1:7b）+ JDK 25，对接 billing 计费系统经营数据大屏，提供 AI 智能分析能力。涵盖 record 化、sealed 接口、结构化并发、虚拟线程、声明式 HTTP Interface 等现代 Java 写法。
date: 2021-01-01
categories:
  - 开源
  - AI
tags:
  - 开源项目
  - Spring AI
  - Ollama
  - JDK25
  - Java
---

[TOC]

## 项目简介

**AI 中台**是一个基于 **Spring AI 2.0.1 + Ollama + JDK 25** 的数据分析平台，对接 billing 计费系统的经营数据大屏，提供 AI 智能分析能力。

> **项目定位**：这是一个**学习型项目**——通过实践熟悉 Java / Spring 生态的最新特性。业务功能是载体，掌握新特性才是目的。

- GitHub 仓库：<https://github.com/thecoolboyhan/ai-platform>
- 语言 / 许可：Java（MIT，见仓库 README）

## 特性一览

| 功能 | 说明 |
| --- | --- |
| **AI 智能分析** | 基于 Ollama（`deepseek-r1:7b`）的经营数据 AI 分析 |
| **大屏数据对接** | 代理 billing API，获取 KPI / 趋势 / Top 客户 / 成本 |
| **SSE 流式输出** | AI 分析结果实时流式返回，前端渐进渲染 |
| **历史持久化** | 分析结果按日期存储，支持跨期对比 |
| **全 record 化** | DTO 层 100% record，样板代码减少约 70% |
| **Java 25 现代写法** | sealed / 结构化并发 / 虚拟线程 / RestClient / 声明式 HTTP Interface |

## 技术栈

| 组件 | 版本 | 说明 |
| --- | --- | --- |
| JDK | 25（GraalVM CE 25.0.2） | 支持 preview 特性 |
| Spring Boot | 4.1.1 | 支持虚拟线程、Jackson 3 |
| Spring AI | 2.0.1 | ChatClient + Ollama 模型 |
| Ollama | `deepseek-r1:7b` | 本地推理，无需外部 API |
| Maven | 3.9.16 | 构建工具 |
| Jackson 3 | 3.1.5 | 序列化（`tools.jackson` 包路径） |

## 快速开始

### 前置条件

1. **JDK 25**（建议 GraalVM CE）
2. **Ollama** 已安装并启动（`ollama serve`）
3. **`deepseek-r1:7b`** 模型已下载：`ollama pull deepseek-r1:7b`
4. **billing 项目** 已启动（默认 `localhost:8080`）

### 启动步骤

```bash
# 1. 克隆仓库
git clone https://github.com/thecoolboyhan/ai-platform.git
cd ai-platform

# 2. 编译打包
./mvnw clean package -DskipTests

# 3. 启动（spring-boot-maven-plugin 已配 --enable-preview）
./mvnw spring-boot:run

# 或运行 jar（必须手动加 --enable-preview）
java --enable-preview -jar target/ai-platform-0.0.1-SNAPSHOT.jar
```

### 访问地址

| 服务 | 地址 |
| --- | --- |
| 分析前端 | <http://localhost:8081/> |
| 健康检查 | <http://localhost:8081/api/ping> |
| AI 健康 | <http://localhost:8081/api/ai/health> |

## API 接口

### AI 分析大屏数据（同步）

```http
POST /api/analysis/dashboard
Content-Type: application/json

{
  "type": "daily",
  "date": "20260828",
  "query": "今天的数据有什么异常？"
}
```

响应为 `AnalysisReport` record（含 `insights` / `anomalies` / `suggestions`）。

### AI 分析大屏数据（流式 SSE）

```http
POST /api/analysis/dashboard/stream
Content-Type: application/json
Accept: text/event-stream
```

SSE 协议：

- 普通事件：AI 输出分片（多次）
- `event: report`：结构化报告（JSON）
- `event: error`：错误信息

### 获取原始大屏数据

```http
GET /api/analysis/dashboard/raw?type=daily&date=20260828
```

### 并发获取全量数据（结构化并发）

```http
GET /api/analysis/dashboard/snapshot?type=daily&date=20260828&bizType=all
```

使用 `StructuredTaskScope` 并发拉取 dashboard / topClients / providerCosts，耗时降为 `max(t1,t2,t3)`。

## 架构设计

### 调用链

```text
前端 → billing API (HTTP Interface) → 数据摘要 → ChatClient (P0+P2+P1) → Ollama
                                      ↓
                              结构化报告 → 存历史 (P3)
```

### 组件职责

| 层级 | 组件 | 文件 | 作用 |
| --- | --- | --- | --- |
| **P0** | System Prompt | `SpringAiConfig.defaultSystem` | 定义 AI 角色、输出格式、必守规则 |
| **P1** | PromptTemplate | `AnalysisPromptTemplate` | 数据摘要 → 标准文本（文本块） |
| **P2** | Advisor | `AnalysisRuleAdvisor` | 注入动态上下文（当前 / 昨日 / 上周日期） |
| **P3** | History | `AnalysisHistoryRepository` | 保存 / 加载上期结果，支持跨期对比 |

## 新特性改造（学习导向）

本项目已采用 **Java 21+ 现代写法**，核心改造点：

| 特性 | 入口文件 | 学习要点 |
| --- | --- | --- |
| `record` 嵌套 | `DashboardDTO.java` | 镜像 billing JSON 层级，精简约 72% 代码 |
| 紧凑构造器 | `AnalysisRequest.java` | DTO 构造时即校验，非法请求返回 400 |
| `sealed` interface | `AnalysisRequest.AnalysisPeriod` | 穷尽性建模 daily / monthly，switch 无需 break |
| 声明式 HTTP Interface | `BillingHttpInterface.java` | `@GetExchange` 替代硬编码 URL |
| `@ConfigurationProperties` | `BillingProperties.java` | record 绑定配置，类型安全 |
| 结构化并发 | `BillingApiClient.fetchSnapshot()` | `StructuredTaskScope` 并发多数据源 |
| 虚拟线程 | `application.yml` | `spring.threads.virtual.enabled=true` |
| 文本块 | `SpringAiConfig.java` | `"""` 包裹多行 Prompt，无需转义 |

## 已知坑

### Java 25 preview 特性

{{< hint "warning" >}}
必须同时配置编译期 + 运行期 --enable-preview。StructuredTaskScope（JEP 505）在 Java 25 仍为 preview 特性。
{{< /hint >}}

- `spring-boot-maven-plugin` 已配 `<jvmArguments>--enable-preview</jvmArguments>`，`./mvnw spring-boot:run` 无需手动加；
- `java -jar` 运行必须手动加：`java --enable-preview -jar xxx.jar`。

### Spring AI 2.0

- **`augmentSystemMessage(String)` 是替换，不是追加**：会覆盖整个 `defaultSystem`，导致报告解析为空；
- 正确做法：用 `augmentSystemMessage(Function)` 重载，手动拼接 `systemMessage.getText()`。

### Jackson 3

- 包路径是 `tools.jackson`，不是 `com.fasterxml`；
- 模块化：`@JsonInclude` 等注解需单独加 `tools.jackson` 依赖。

## 本地开发

### 依赖 billing 项目

本项目代理 billing API，需确保 billing 项目已启动（默认 `localhost:8080`）。

```yaml
billing:
  api:
    base-url: http://localhost:8080
```

### 配置 Ollama

```bash
# 拉取模型（如未安装）
ollama pull deepseek-r1:7b

# 启动 Ollama 服务（默认 11434 端口）
ollama serve
```

```yaml
spring:
  ai:
    ollama:
      base-url: http://localhost:11434
      chat:
        model: deepseek-r1:7b
```

## 项目结构

```text
ai-platform/
├── pom.xml                              # Maven 配置（JDK 25 + Spring Boot 4.1.1）
├── AGENTS.md                            # AI 协作规范
├── CHANGELOG.md                         # 变更日志
├── README.md                            # 项目说明
├── src/main/java/com/wiseco/aiplatform/
│   ├── AiPlatformApplication.java       # 启动类
│   ├── config/                          # 配置类（Spring AI、HTTP Interface、Properties）
│   ├── advisor/                         # Advisor（动态注入时间上下文）
│   ├── dto/                             # DTO（全 record 化）
│   ├── client/                          # Billing 客户端（结构化并发）
│   ├── repository/                      # 分析历史持久化（文件存储）
│   ├── service/                         # AI 分析服务、Prompt 模板
│   └── controller/                      # REST API（分析、健康检查）
└── src/main/resources/
    ├── application.yml                  # 主配置（虚拟线程、Ollama、billing）
    ├── static/index.html                # 前端分析看板（Vue2 + ECharts）
    └── templates/                       # Thymeleaf 模板（备用）
```

## 许可

本项目采用 **MIT** 许可（见仓库 README 说明）。

## 相关链接

- GitHub 仓库：<https://github.com/thecoolboyhan/ai-platform>
- 问题反馈：<https://github.com/thecoolboyhan/ai-platform/issues>
