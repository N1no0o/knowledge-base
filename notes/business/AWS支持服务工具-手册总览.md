---
title: AWS 支持服务配套工具体系 · 手册总览
tags: [AWS, 支持服务, 工具, Trusted Advisor, Health, Support API, SAW, 竞品]
created: 2026-09-25
updated: 2026-09-25
source: AWS 官方文档（cloud-support-docs/aws/ 957 篇）+ 官网产品页 28 篇 + 真实 API 探测 42 次｜2026-09-25
status: growing
---

# AWS 支持服务配套工具体系 · 手册总览

> 本手册覆盖 AWS 支持服务（Support）的**全部配套工具**，含 API 能力、权限要求、
> 支持计划门槛、以及 **2026-09-25 真实 API 探测结果**。
>
> 文档底座：`D:/AI/my_project/cloud-support-docs/aws/`（957 篇官方 md）+ `_website/`（28 篇产品页）

## 一句话

**AWS 的支持服务不是「一个工单系统」，而是「数据层 + 服务层 + AI 层」三层叠加的工具体系** ——
其中**大量能力被支持计划等级锁死**，这是华为立项最直接的对标参照。

## 工具体系全景

| 层 | 工具 | 定位 | 计划门槛 |
|---|---|---|---|
| **数据层** | **AWS Health**（Dashboard + API） | 事件权威数据源，200+ 服务集成 | Dashboard 免费；**API 需 Business+** |
| **数据层** | **AWS Trusted Advisor** | 最佳实践检查（482 项） | **56 项免费 / 426 项需 Business+** |
| **服务层** | **Support Center / 工单** | 案例全生命周期管理 | **Basic 免费（不能改严重级别）** |
| **服务层** | **Support API** | 工单自动化（21 个操作） | **需 Business+** |
| **服务层** | **SAW**（支持自动化工作流） | SSM Runbook 自助修复 | **需 Business+** |
| **服务层** | **Support App in Slack** | 在 Slack 内管理工单 | **需 Business+** |
| **服务层** | **TAM**（技术客户经理） | 指定专人 | **需 Enterprise+** |
| **AI / 增值层** | **DevOps Agent** | AI 自主调查事件、给根因 | 按量付费 + 抵扣金 |
| **AI / 增值层** | **IDR**（事件检测与响应） | IME 5 分钟响应 + Runbook | **Enterprise 需额外付费 / Unified Ops 已含** |
| **AI / 增值层** | **Countdown Premium** | 关键活动护航 | **需额外付费 / Unified Ops 已含** |
| **AI / 增值层** | **AWS Managed Services** | 托管运维 | 需额外付费 |

## 计划门槛矩阵（官方原文）

| 能力 | Basic | Business Support+ | Enterprise | Unified Ops |
|---|---|---|---|---|
| CPU 生产系统停机响应 | — | **< 30 分钟** | **< 15 分钟** | **IME < 5 分钟** |
| Health Dashboard | ✔ | ✔ | ✔ | ✔ |
| **Health API** | ✘ | **✔** | ✔ | ✔ |
| Trusted Advisor | 56 项 | **482 项（全套）** | 全套 + **Priority** | 全套 + Priority |
| Support API | ✘ | **✔** | ✔ | ✔ |
| SAW 自动化工作流 | ✘ | **✔** | ✔ | ✔ |
| Support App (Slack) | ✘ | **✔** | ✔ | ✔ |
| 改工单严重级别 | ✘ | ✔ | ✔ | ✔ |
| TAM（指定技术客户经理） | ✘ | ✘ | **✔** | ✘（有领域专家工程师） |
| **IDR** | ✘ | **需额外付费** | **需额外付费** | **✔ 已含** |
| **Countdown Premium** | ✘ | 需额外付费 | 需额外付费 | **✔ 已含** |
| 白手套账单礼宾 | ✘ | ✘ | **✔** | ✔ |

> ⭐ **对本立项最关键的三个数字**：
> 1. **Business+ 响应 < 30 分钟 / Enterprise < 15 分钟 / Unified Ops < 5 分钟（IME）**
>    → 华为「尊享级 <5 分钟」对标的是 **Unified Operations**，且对方是**专人（IME）响应**
> 2. **Trusted Advisor：56 免费 vs 482 全套**
>    → **426 项检查是付费墙** —— 这就是「能力型 + 分层溢价」的现成先例
> 3. **Health API / Support API / SAW 全部锁在 Business+ 以上**
>    → **API 访问本身就是付费门槛**，不是技术门槛

## 2026-09-25 真实探测结果（重要）

对测试账号 `206482634625`（IAM 用户 `WorkBuddy`）执行 **42 次只读 API 调用**：

| 结果 | 次数 | 原因 |
|---|---|---|
| ✔ 成功 | **0** | — |
| ✘ `SubscriptionRequiredException` | **13** | **无有效付费支持订阅** |
| ✘ `AccessDeniedException` | **17** | **IAM 用户几乎无策略** |
| ✘ 参数错误（我的问题） | 2 | 已修正 |

**核心结论**：
- **`SubscriptionRequiredException` 是订阅层拦截，在 IAM 之前** —— 光配 IAM 策略无效
- 跨 4 个区域（us-east-1 / us-west-2 / ap-southeast-1 / eu-west-1）验证一致，**排除区域因素**
- **支持服务类 API（Trusted Advisor / Support / Health）在无付费订阅时完全不可用**

详见 [[AWS支持服务工具-API实测报告]]。

## 子笔记导航

| 笔记 | 内容 |
|---|---|
| [[AWS支持服务工具-AWS-Health]] | Health Dashboard + API（15 个操作） |
| [[AWS支持服务工具-Trusted-Advisor]] | 482 项检查 + 5 个 API 操作 |
| [[AWS支持服务工具-Support-API与工单]] | 21 个操作 + 工单全生命周期 |
| [[AWS支持服务工具-SAW与Slack]] | 自动化工作流 + Slack 集成 |
| [[AWS支持服务工具-IDR与AI增强]] | IDR / DevOps Agent / Countdown |
| [[AWS支持服务工具-API实测报告]] | 42 次真实调用记录与失败分析 |
| [[AWS支持服务配套工具-体验报告]] | ⭐ 面向决策者的总结报告（结论先行 + 6 个立项发现） |

## 文档底座位置

```
D:/AI/my_project/cloud-support-docs/aws/
├── _website/                          28 篇官网产品页/定价页
├── aws-health-api-reference/          41 篇（Health API 参考）
├── aws-health-user-guide/             47 篇（Health 用户指南）
├── aws-incident-detection-response/   40 篇（IDR 完整文档）
├── aws-service-quotas/                31 篇
├── aws-support-api-reference/         52 篇（21 操作 + 30 数据类型）
├── aws-support-user-guide/            169 篇（Support 用户指南）
├── aws-well-architected-framework/    476 篇
├── aws-well-architected-tool/         109 篇
└── _pdf/                              9 份官方 PDF 整册
```

---

## 关联笔记

- [[华为云支持服务立项-AWS竞品对标]] — 竞品定价与六维度速查
- [[EDR立项-AWS竞品分析资料包索引]] — 语料库入口
- [[华为云支持服务立项-立项二三产品定义]] — IDR 是我们不该抄的那条（客户侧投入极重）
