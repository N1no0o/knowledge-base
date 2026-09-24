---
title: AWS 支持服务工具 · AWS Health
tags: [AWS, Health, HealthAPI, PHD, 事件, 组织视图, EventBridge]
created: 2026-09-25
updated: 2026-09-25
source: aws-health-user-guide/ (47篇) + aws-health-api-reference/ (41篇) + _website/aws-health-product.md｜2026-09-25
status: growing
---

# AWS 支持服务工具 · AWS Health

> **定位**：AWS 的**事件权威数据源** —— 提供「AWS 服务运行状况的个性化视图」，
> 200+ 服务集成，在资源受影响时发出警报。
>
> 它是 EDR 立项最直接的**数据层对标对象**。

## 两个东西必须分清（官方原文）

| 形态 | 可用性 | 说明 |
|---|---|---|
| **AWS Health Dashboard** | **所有客户免费** | 控制台视图，无需付费订阅、无需写代码 |
| **AWS Health API** | **仅 Business Support+ / Enterprise / Unified Operations** | 用于与内部及第三方系统集成 |

> ⭐ **官方原文**：
> "You must have an AWS Business Support+, AWS Enterprise Support, or AWS Unified Operations plan
> to use the AWS Health API. **If you call the AWS Health API from an AWS account that isn't enrolled
> in one of these plans, then you receive a `SubscriptionRequiredException` error.**"
>
> **⇒ 这一条已被实测验证**（见 [[AWS支持服务工具-API实测报告]]）。

## 事件模型（核心概念）

AWS Health 的**事件（Event）**用于告知服务与资源变更如何影响你的应用。

| 事件特征 | 说明 |
|---|---|
| **eventTypeCode** | 事件类型编码（如 `AWS_EC2_INSTANCE_STOP_SCHEDULED`） |
| **service** | 受影响服务（如 EC2 / RDS / S3） |
| **region** | 受影响区域 |
| **eventTypeCategory** | 分类：`issue`（问题）/ `accountNotification`（账户通知）/ `scheduledChange`（计划变更）/ `investigation`（调查中） |
| **statusCode** | `open` / `upcoming` / `closed` |
| **affectedEntities** | 受影响的具体资源（entityValue = 资源 ID） |

### 两类事件

| 类型 | 说明 |
|---|---|
| **账户特定事件** | 只影响你的账户（如某个实例的维护） |
| **公共事件** | 影响某区域内所有客户（如区域性故障） |

## API 操作清单（15 个）

### 账户级（8 个）

| 操作 | 用途 |
|---|---|
| `DescribeEvents` | ⭐ 查事件列表（核心入口，支持 filter） |
| `DescribeEventDetails` | 查事件详情（含最新描述） |
| `DescribeAffectedEntities` | 查受影响资源实体（**filter 必填**） |
| `DescribeEntityAggregates` | 按实体聚合统计 |
| `DescribeEventAggregates` | 按事件聚合统计（适合做趋势图） |
| `DescribeEventTypes` | 查事件类型目录 |
| `DescribeEventDetailsForOrganization` | 组织级事件详情 |
| `DescribeAffectedAccountsForOrganization` | 组织级受影响账户 |

### 组织级（7 个，需 Organizations）

| 操作 | 用途 |
|---|---|
| `DescribeEventsForOrganization` | 组织级事件列表（需主账号/委派管理员） |
| `DescribeAffectedEntitiesForOrganization` | 组织级受影响实体 |
| `DescribeEntityAggregatesForOrganization` | 组织级实体聚合 |
| `DescribeEventDetailsForOrganization` | 组织级事件详情 |
| `EnableHealthServiceAccessForOrganization` | 开启组织视图 |
| `DisableHealthServiceAccessForOrganization` | 关闭组织视图 |
| `DescribeHealthServiceStatusForOrganization` | 查组织视图状态 |

> ⚠️ **组织级操作需显式开启**（`EnableHealthServiceAccessForOrganization`），
> 且调用方必须是**管理账户或委派管理员**。

## 关键参数陷阱（实测踩过）

| 操作 | 陷阱 |
|---|---|
| `DescribeAffectedEntities` | **`filter` 是必填参数**，不传直接 `ParamValidationError` |
| `DescribeEvents` | `maxResults` 有范围限制；分页用 `nextToken` |
| `DescribeEventDetails` | `eventArns` 为必填，格式 `arn:aws:health:<region>::event/<service>/<type>/<id>` |

## 集成方式（三条路）

| 方式 | 说明 | 成本 |
|---|---|---|
| **EventBridge** | ⭐ 推荐。**所有客户免费**，可路由到 Lambda / SNS / SQS | **免费** |
| **Health API** | 主动拉取，适合自建系统 | **需 Business+** |
| **User Notifications** | 控制台通知配置 | 免费 |

> ⭐ **重要**：**All AWS customers can receive AWS Health events through Amazon EventBridge at no additional cost.**
> ⇒ **免费的 EventBridge 通道 + 付费的 API 通道**，这个设计本身就是分层策略。

## 与华为立项的对照意义

| 维度 | AWS Health | 华为 EDR 立项 |
|---|---|---|
| 数据源 | 200+ 服务集成，EventBridge 为唯一集成点 | 管理面 + 租户面 |
| 免费能力 | Dashboard + EventBridge 通知 | — |
| 付费能力 | **API 访问本身就要钱**（Business+ 起） | 我们主张 Basic 普惠（含基础通知） |
| 组织视图 | 支持（需 Organizations + 显式开启） | — |
| 北极星指标 | 事件触达 | 有效告警触达率 + MTTR 缩短比 |

> **⭐ 可引用结论**：AWS 把「**事件数据可编程获取**」这张门票放在 Business+ 之后，
> 而把「看见事件」免费开放。这是**「基础可见免费、自动化/集成付费」**的典型分层。

## 文档出处

- `aws-health-user-guide/000-What-is-AWS-Health.md` — 免费/付费分界
- `aws-health-user-guide/008-Integrating-with-other-systems-using-the-AWS-Health-API.md` — API 门槛与错误码
- `aws-health-api-reference/` — 15 个操作完整定义
- `_website/aws-health-product.md` / `aws-health-phd.md` — 产品页

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 工具体系全貌
- [[AWS支持服务工具-API实测报告]] — 本工具实测失败记录
- [[华为云支持服务立项-AWS竞品对标]] — AWS 三层体系
