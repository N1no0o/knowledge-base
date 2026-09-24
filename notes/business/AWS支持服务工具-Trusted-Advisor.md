---
title: AWS 支持服务工具 · Trusted Advisor
tags: [AWS, TrustedAdvisor, 检查项, 最佳实践, Priority, API]
created: 2026-09-25
updated: 2026-09-25
source: _website/aws-trusted-advisor.md + aws-support-user-guide/ + aws-support-api-reference/（5个TA操作）｜2026-09-25
status: growing
---

# AWS 支持服务工具 · Trusted Advisor

> **定位**：对 AWS 环境做**持续的最佳实践评估**，对偏离最佳实践处给出补救建议。
> 覆盖**六大类别**，是 AWS 支持服务里「主动式服务」的核心载体。

## ⭐ 最关键的商业数字（官方原文）

> - 所有 AWS 账户计划均可访问 **56 个** Trusted Advisor 检查
> - **Business Support 及以上级别可解锁另外 426 项检查，总计 482 项**

| 层级 | 检查项数 | 比例 |
|---|---|---|
| **免费（所有计划）** | **56 项** | 11.6% |
| **Business+ 解锁** | **+426 项** | 88.4% |
| **总计** | **482 项** | 100% |

> ⭐ **这是「基础免费 + 能力付费」最干净的量化先例** ——
> **426 项（88%）检查被锁在付费墙后**，这就是分层溢价的产品化实现。

## 六大检查类别

| 类别 | 检查什么 | 典型场景 |
|---|---|---|
| **成本优化** | 未使用资源、降本机会 | 闲置 EC2 / 未挂载 EBS |
| **性能** | 使用方式与配置 | 提升应用速度与响应 |
| **韧性** | 缺少冗余、资源过度使用 | 单点故障识别 |
| **安全性** | 是否符合安全标准与最佳实践 | 开放端口 / IAM 配置 |
| **卓越运营** | 运营最佳实践 | 监控覆盖 |
| **服务限制** | 账户使用量接近或超限 | 配额预警 |

## Trusted Advisor Priority（Enterprise 专属）

| 层级 | 提供什么 |
|---|---|
| **Business+** | 全套 482 项检查 |
| **Enterprise / Unified Ops** | 全套 + **Priority** |

**Priority 是什么**：由**你的 AWS 账户团队**提供的**情境驱动、按优先级排序**的建议 ——
综合考虑业务优先级、关键应用、建议紧迫性。

> ⭐ **关键差异**：普通 TA 给的是**检查结果清单**；Priority 给的是**排好序的行动建议**。
> 差别在于**从「数据」到「判断」** —— 这正是「人 + 工具」的价值锚点。

## API 操作（5 个）

| 操作 | 用途 |
|---|---|
| `DescribeTrustedAdvisorChecks` | ⭐ 查全部检查项定义（含 id / name / category / description） |
| `DescribeTrustedAdvisorCheckResult` | ⭐ 查单个检查的**详细结果**（含受影响资源明细） |
| `DescribeTrustedAdvisorCheckSummaries` | 批量查检查摘要（轻量，适合做概览） |
| `DescribeTrustedAdvisorCheckRefreshStatuses` | 查刷新状态 |
| `RefreshTrustedAdvisorCheck` | ⭐ **触发刷新**（唯一非只读操作，但**不产生费用**） |

> ⚠️ **注意**：`RefreshTrustedAdvisorCheck` 是 TA API 里唯一的「写」操作 ——
> 它只是触发重新检查，**不改动任何资源**。

## 关键数据类型

| 类型 | 说明 |
|---|---|
| `TrustedAdvisorCheckDescription` | 检查项定义（id / name / category / description / metadata） |
| `TrustedAdvisorCheckResult` | 检查结果（status / resourcesSummary / flaggedResources） |
| `TrustedAdvisorResourceSummary` | 资源汇总统计 |
| `TrustedAdvisorCostOptimizingSummary` | **成本优化专项**（estimatedMonthlySavings / estimatedPercentMonthlySavings） |

> ⭐ **`TrustedAdvisorCostOptimizingSummary` 提供「预估月省金额」** ——
> 这让成本优化检查**直接产出可量化的 ROI 数字**，是很有说服力的设计。

## 使用门槛

| 能力 | 门槛 |
|---|---|
| 控制台查看 56 项 | 免费 |
| **控制台查看全部 482 项** | **Business+** |
| **API 编程访问** | **Business+** |
| **AWS CLI 访问** | **Business+** |
| **Priority 排序建议** | **Enterprise+** |
| 组织级汇总视图 | Business+ |

> **官方原文**：「注册 AWS Business Support 以解锁**全套 Trusted Advisor 检查、
> AWS Trusted Advisor API 和 AWS 命令行界面**。」
> ⇒ **API 和 CLI 访问与检查项数绑在同一道付费墙上。**

## 与华为立项的对照意义

| 维度 | AWS Trusted Advisor | 华为可借鉴点 |
|---|---|---|
| 免费/付费切分 | **56 / 482（11.6% / 88.4%）** | 权益分层可量化，非黑即白 |
| 付费墙位置 | **检查项数 + API + CLI 一起锁** | API 访问本身可作为付费点 |
| 升级动力 | Priority 提供**排序后的建议** | 「从数据到判断」是溢价来源 |
| 量化价值 | 成本优化检查给**预估省钱金额** | 效果度量要能给数字 |
| 组织级能力 | Business+ 才有汇总视图 | 大型客户的组织视图是差异化 |

> **⭐ 可直接引用的话术**：
> 「AWS 把 88% 的最佳实践检查放在付费墙后，并且**把 API 访问和 CLI 权限与检查项数绑在一起卖**。
> 这说明**「能力型 + 分层溢价」在国际主流云厂商是被验证过的商业模式**，
> 而不是我们独创的收费借口。」

## 文档出处

- `_website/aws-trusted-advisor.md` — 56/426/482 数字与六大类别
- `_website/aws-trusted-advisor-full.md` — 产品页全量
- `aws-support-api-reference/014~020` — 5 个 TA 操作定义
- `aws-support-user-guide/` — TA 用户指南章节

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 工具体系全貌
- [[AWS支持服务工具-Support-API与工单]] — TA API 同属 Support API
- [[AWS支持服务工具-SAW与Slack]] — SAW 有「管理和 TA 检查」的 Runbook
- [[华为云支持服务立项-AWS竞品对标]] — 定价与六维度
