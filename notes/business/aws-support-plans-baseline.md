---
title: AWS 支持计划能力基线与实测证据（Business Support+）
tags: [AWS, 支持计划, 能力基线, 实测证据, 竞品, BusinessSupport+]
created: 2026-09-27
updated: 2026-09-27
source: dist/aws-support-plans/AWS支持计划能力基线.md（26.3 KB，2026-09-26 23:07）｜原件 D:/AI/my_project/dist/aws-support-plans/
status: growing
---

# AWS 支持计划能力基线与实测证据

**结论：AWS 支持计划已于 re:Invent 2025 重构为四档（Basic / Business Support+ / Enterprise / Unified Operations），旧三级 2027-01-01 全线停售；本账号从「全量 `SubscriptionRequiredException`」变为「全部 `support.*` / `health.*` / Trusted Advisor 可调用」，最硬证据是 `support refresh-trusted-advisor-check` 返回 `status: enqueued` —— 该接口仅 Business 级及以上开放。**

## 一、现行四档（2026 版）

| 计划 | 最低月费 | 定位 |
|---|---|---|
| Basic | 免费（账号自带） | 账单与配额问答、论坛、健康检查、文档 |
| **Business Support+** | **$29 / 账号 / 月** | 生产负载最低推荐档；24×7 工程师 + AI 上下文诊断 |
| Enterprise | **$5,000 / 月** | TAM、15 分钟响应、含 Security Incident Response |
| Unified Operations | **$50,000 / 月** | DSE 团队、Countdown Premium、供应商侧主动运营 |

- **计费口径**：取「最低月费」与「按 AWS 消费百分比」中的**较高者**；BS+ 首段 **9%**（旧 Business 是 10%，这是区分两者的关键数字）。
- **公开定价 API 实测**（`AWSSupportEssential` = BS+）：$0–10K **9%** / 10K–80K 7% / 80K–250K 5% / >250K 3%；`AWSSupportEnterprise` 首段 10%。
- ⚠️ **Unified Operations 未出现在公开价格 API 中**（需 Contact sales 议价）；`AWSSupportEssential` 与「Business Support+」的名称映射是**按 $29 + 9% 首段吻合的强推断**，非官方文档明示。
- **传承关系**：`Enterprise ⊇ Business Support+ ⊇ Basic`；Unified 是**独立顶层**，不是 Enterprise 的超集。

## 二、BS+ 买到了什么（官方原文口径）

- 生成式 AI 实时上下文响应、**24×7** 电话/Web/聊天接入 Cloud Support Engineer
- 业务关键系统宕机 **< 30 分钟**人工介入
- Trusted Advisor **500+ 项检查**（实测返回 **639** 项）
- **AWS Support API**（可编程管理 Support Center 与 Trusted Advisor）、**AWS Health API**
- 第三方软件支持、不限数量 Case、SAW 支持自动化工作流（实测 **112** 个 `AWSSupport-*` runbook）
- DevOps Agent 额度 = AWS Support 费用的 **30%**（Enterprise 75% / Unified 100%）

## 三、本账号事实底座

账号 `2064****4625`（N1noooo）｜区域 `us-east-1`｜计划 `PAID`/ACTIVE｜创建 2026-09-24｜**未加入 Organizations**
AWS Config **未启用**｜Compute Optimizer **Inactive**｜Security Hub **未订阅**

## 四、能力实测判据（升级前后对照）

| 能力 | 升级前 | 现在 |
|---|---|---|
| `support describe-cases` / `describe-services` | `SubscriptionRequiredException` | ✅ 可用（**324** 个可开单服务） |
| `describe-severity-levels` / `-supported-languages` | 同上 | ✅ 5 级 / 7 种语言 |
| `describe-create-case-options` | 同上 | ✅ 渠道 web/call/chat，时段 05:00–04:59:59（全天候） |
| `describe-trusted-advisor-checks` | 同上 | ✅ **639** 项 |
| **`refresh-trusted-advisor-check`** | 不可达 | ✅ **`{"status":"enqueued"}`** ← 决定性证据 |
| 全部 `health.*` | 同上 | ✅ 可用 |

> **判据价值**：同一账号、同一区域、同一身份（root），从全量拒绝变为全量通过 ⇒ **「root 绕不过订阅墙」在旧计划下成立，在新计划下已被推翻**。

## 五、两个易误判的坑

1. **Trusted Advisor 517/639 项 `not_available` ≠ 被计划挡住**。真因是 AWS Config 未启用 / Compute Optimizer 未激活 / Security Hub 未订阅 / 账号仅创建 2 天。**对照实验**：`MFA on Root Account` 刷新一次即从 `not_available` 变为 `error`（已评估）⇒ **`not_available` = 「尚未评估」**。
2. **Health 组织级视图 `AccessDenied` 不是权限问题**，错误文本明示 `not part of an organization`。

## 六、顺带发现的真实风险

| 检查项 | ID | 状态 | 含义 |
|---|---|---|---|
| **MFA on Root Account** | `7DAFEmoDos` | `error`（flagged 1） | 🔴 **root 账号未启用 MFA**，建议尽快开启 |
| Amazon RDS Public Snapshots | `rSs93HQwa1` | `ok` | 无 RDS 资源 |

## 七、证据文件索引（同目录 `dist/aws-support-plans/`）

| 文件 | 内容 |
|---|---|
| `console/plans_page_content.md`（39.6 KB） | 控制台页面总存档：当前计划 + 45 行矩阵 + 5 视图原文 + 95 条链接 |
| `console/compare_matrix_parsed.json` | 45 行功能矩阵（机器可读，含每格 ✓/✗） |
| `support_describe-services.json` / `-trusted-advisor-checks.json` | 324 个服务 / 639 项检查定义 |
| `account_capability_probe.json` / `ta_availability_scan.json` | 22 项能力探测原始结果 / 639 项 TA 逐项状态 |
| `_price_AWSSupport{Essential,Enterprise,Business}.json` | 三组定价档位原始数据 |
| `AWS支持计划_交付主体阶梯热力图.svg` | BA 交付主体阶梯可视化 |

**复现前提（本机）**：`export AWS_LOGIN_CACHE_DIRECTORY="D:\AI\my_project\_aws_cache"` —— `~/.aws/` 被 WorkBuddy 文件策略层锁死（见 [[github-knowledge-base-options]] 同源环境说明）。

## 相关

- [[aws-support-plans-33-capabilities]] — 33 项能力 × 四档逐项取值与三个断崖
- [[aws-support-plans-ba-architecture]] — BA 业务架构六视图逆向
- [[aws-support-plans-ba-cards]] — 33 张单能力 BA 卡片
- [[华为云支持服务立项-AWS竞品对标]] — 立项用的 AWS 竞品对标（定价与计划变动）
- [[AWS支持服务工具-手册总览]] — AWS 支持配套工具实测集
