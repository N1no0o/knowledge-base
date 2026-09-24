---
title: AWS 支持服务工具 · Support API 与工单
tags: [AWS, SupportAPI, 工单, Case, 严重级别, 附件]
created: 2026-09-25
updated: 2026-09-25
source: aws-support-api-reference/ (52篇) + aws-support-user-guide/ (169篇)｜2026-09-25
status: growing
---

# AWS 支持服务工具 · Support API 与工单

> **定位**：Support Center（工单系统）的**编程接口**，覆盖案例全生命周期。
> **21 个操作**，分两组：**案例管理** + **Trusted Advisor**。

## ⚠️ 门槛（官方原文）

> "You must have an AWS Business Support+, AWS Enterprise Support, or AWS Unified Operations plan
> to use the AWS Support API. ... the **`SubscriptionRequiredException`** error message appears."
>
> **⇒ 已实测验证**（见 [[AWS支持服务工具-API实测报告]]）

| 能力 | 门槛 |
|---|---|
| 控制台提交/查看工单 | **Basic 免费** |
| **修改工单严重级别** | **Business+**（Basic 不能改） |
| **Support API** | **Business+** |
| Slack 集成 | Business+ |

## 严重级别矩阵（官方原文，⭐ 核心数据）

| 严重级别 | 代码 | 首次响应时间 | 说明 |
|---|---|---|---|
| **一般性指导** General guidance | `low` | **24 小时** | 开发问题或功能请求 |
| **系统受损** System impaired | `normal` | **12 小时** | 非关键功能异常 |
| **生产系统受损** Production system impaired | `high` | **4 小时** | 重要功能受损或降级 |
| **生产系统停机** Production system down | `urgent` | **1 小时** | 业务显著受影响 |
| **业务关键型系统停机** Business-critical system down | `critical` | **Business+：< 30 分钟**<br>**Enterprise：< 15 分钟**<br>**Unified Ops：IME 5 分钟** | 业务处于风险中 |

> ⭐ **这是我们立项最该记住的一张表**：
> - 前四级**所有付费计划完全一样**（24h / 12h / 4h / 1h）
> - **只有最高一级（critical）才拉开差距**：30 / 15 / 5 分钟
>
> **⇒ 分层差异集中在「最高严重级别的响应速度」上，而非全线提速。**

## API 操作清单（21 个）

### 案例管理（15 个）

| 操作 | 类型 | 用途 |
|---|---|---|
| `CreateCase` | 写 | ⭐ 创建工单（**返回 case number**） |
| `AddCommunicationToCase` | 写 | 追加通讯记录 |
| `DescribeCases` | 读 | ⭐ 查工单列表 |
| `DescribeCommunications` | 读 | 查工单通讯（`maxResults` **最小 10**） |
| `ResolveCase` | 写 | 关闭工单 |
| `DescribeCreateCaseOptions` | 读 | 查创建工单的可选参数（hours/language 可用性） |
| `DescribeServices` | 读 | 查服务目录（有哪些服务可开工单） |
| `DescribeSeverityLevels` | 读 | 查严重级别定义 |
| `DescribeSupportedLanguages` | 读 | 查支持语言 |
| `AddAttachmentsToSet` | 写 | 添加附件集 |
| `CompleteAttachmentUpload` | 写 | 完成附件上传 |
| `DescribeAttachment` | 读 | 查附件信息 |
| `DescribeAttachmentUploadStatus` | 读 | 查上传状态 |
| `GetAttachmentDownloadLink` | 读 | 获取下载链接 |
| `GetAttachmentUploadLinks` | 读 | 获取上传链接 |

### Trusted Advisor（5 个）

见 [[AWS支持服务工具-Trusted-Advisor]]。

### 已废弃（1 个）

| 操作 | 说明 |
|---|---|
| `DescribeCaseAttributes` | 已废弃 |

## ⚠️ 三个重要限制（官方原文）

### ① 不支持服务限额提升请求

> "**The Support API doesn't support requesting service limit increases.**"
>
> 替代方式：
> - 控制台 Create Case 页面提交
> - **Service Quotas API 的 `RequestServiceQuotaIncrease`**

**⇒ 意味着「配额提升」走的是另一条 API 通道（Service Quotas），不在 Support API 里。**

### ② 敏感信息自动脱敏

> AWS Support 自动对工单中的敏感信息脱敏，替换为 `[REDACTED_BY_AWS]`：
> - **AWS 密钥**（完整替换）
> - **私钥**（完整替换）
> - **信用卡号**（保留后 4 位）

**⇒ AWS Support 永不需要这些信息；这是自动的，不需要开发者处理。**

### ③ 附件需分步上传

上传流程是**三步**（不是一次调用）：
```
GetAttachmentUploadLinks → [客户端 PUT 上传] → CompleteAttachmentUpload
```

## 消息查询参数陷阱（实测踩过）

| 参数 | 陷阱 |
|---|---|
| `DescribeCommunications.maxResults` | **最小值是 10**，传 5 会 `ParamValidationError` |
| `DescribeCases` | 默认不返回已关闭工单，需 `includeResolvedCases: true` |
| `CreateCase` | 首次创建后需用 `AddCommunicationToCase` 追加沟通 |

## 与华为立项的对照意义

| 维度 | AWS | 华为立项可借鉴 |
|---|---|---|
| 响应分级 | **5 级**，前 4 级付费计划间无差异 | 分级差异聚焦在「最高级别」是行业惯例 |
| 最高级响应 | 30 / 15 / **5 分钟** | 我们的尊享级 <5 分钟对标 Unified Ops |
| 改严重级别 | **Basic 不能改**，Business+ 能改 | 「可控性」本身可以作为付费点 |
| API 访问 | Business+ 门槛 | API 是付费能力，不是技术能力 |
| 工单上限 | **任意数量的案例和联系方式**（无配额） | 我们不设工单数上限是合理的 |

## 文档出处

- `aws-support-api-reference/` — 21 个操作完整定义（含请求/响应/错误）
- `aws-support-user-guide/020-Case-management.md` — **严重级别矩阵官方原文**
- `aws-support-user-guide/036-About-the-AWS-Support-API.md` — API 门槛
- `aws-support-user-guide/021-Request-a-service-quota-increase.md` — 配额提升路径

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 工具体系全貌
- [[AWS支持服务工具-Trusted-Advisor]] — 同属 Support API 的 5 个操作
- [[AWS支持服务工具-SAW与Slack]] — 工单的自动化与 IM 触达
- [[华为云支持服务立项-AWS竞品对标]] — 定价与六维度
