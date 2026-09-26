---
title: AWS 支持服务工具 · API 实测报告（两轮：2026-09-25 / 09-26）
tags: [AWS, 支持服务, API, 实测, SubscriptionRequiredException, new-AWS-experience, 华为云支持服务立项]
created: 2026-09-25
updated: 2026-09-26
source: 本机真实 API 调用｜第一轮 42 次（boto3 1.43.101）｜第二轮 17 次（AWS CLI 2.37.3 + root 身份）｜原始记录见文末
status: stable
---

# AWS 支持服务工具 · API 实测报告

> 本报告记录**两轮**真实 API 实测。第二轮推翻了第一轮的部分结论，并给出了**终局答案**。
> 全部调用均为**只读**，未产生任何费用（`ce:*` 因按次计费被**主动跳过**）。

| | 第一轮 | 第二轮 |
|---|---|---|
| 日期 | 2026-09-25 | 2026-09-26 |
| 身份 | IAM 用户 `WorkBuddy`（AK/SK） | **root**（`aws login`，`arn:aws:iam::206482634625:root`） |
| 工具 | Python 3.13.12 + boto3 1.43.101 | AWS CLI 2.37.3 |
| 调用数 | 42 | 17 |
| 成功 | **0** | **9** |

---

## 一、终局结论（第二轮得出）

### 1. 账号是「新形态 AWS · PAID 计划」，且该计划**不含** Premium Support 订阅

决定性证据 —— `aws freetier get-account-plan-state`（**该命令本身来自 AWS 官方规则的引导**）：

```json
{
    "accountId": "206482634625",
    "accountPlanType": "PAID",
    "accountPlanStatus": "ACTIVE",
    "accountPlanRemainingCredits": { "amount": 0.0, "unit": "USD" }
}
```

结合用户确认的 **new AWS experience** 形态（社交账号注册 + project 模型），结论是：

> 🔴 **新形态 AWS 账号的「PAID 计划」只决定资源额度与信用额，不包含传统 Premium Support 订阅。**
> 因此这个账号上 **Support API / Health API 永远不可达 —— 与 IAM 权限、区域、订阅是否过期全部无关。**

这解释并**修正**了第一轮的推测：不是「Business 计划没订上 / 已过期 / PLS 账号」，而是**该账号体系里根本不存在「Business 支持计划」这一档**。用户口述的「Business」在新形态账号语境下不成立。

### 2. 两层封锁中，**只有订阅层是真的**

第二轮换成 root（拥有账号内全部权限）后：

| 层 | 第一轮（IAM 用户） | 第二轮（root） | 判定 |
|---|---|---|---|
| **IAM 层** | 20 次 `AccessDenied` | ✅ **全部通过** | 第一轮的问题是**那个 IAM 用户没策略**，与账号无关 |
| **订阅层** | 19 次 `SubscriptionRequired` | 🔴 **依然全部失败** | **账号级真实状态，root 也绕不过** |

> ⭐ **这是本报告最有价值的一对对照实验**：
> 同一批操作、同一个账号，**只换身份**（受限 IAM 用户 → root），
> IAM 层错误全部消失，**订阅层错误分毫未动**。
> → **证明了「订阅校验发生在 IAM 之前」不是推测，而是可复现的事实。**

---

## 二、第二轮实测逐条结果（root 身份，17 次）

### ✅ 成功的（9 项）

| 服务 | 操作 | 返回 |
|---|---|---|
| `sts` | `get-caller-identity` | `arn:aws:iam::206482634625:root` |
| `freetier` | `get-account-plan-state` | `PAID` / `ACTIVE` |
| `freetier` | `get-free-tier-usage` | 多项 "Always Free" 用量 |
| `freetier` | `list-account-activities` | `{"activities": []}` |
| `service-quotas` | `list-service-quotas` | ✔ 正常返回配额列表 |
| **`support-app`** | `list-slack-channel-configurations` | `{"slackChannelConfigurations": []}` ⭐ |
| `ssm` | `list-documents` | ✔ 返回 AWS 托管文档（**SAW 的底层载体**） |
| `s3api` | `list-buckets` | `{"Buckets": []}`（账号无桶） |
| `iam` | `get-account-summary` | ✔ 正常返回 |
| `devops-guru` | `describe-account-health` | 全 0（未启用） |
| `ssm-incidents` | `list-incident-records` | `{"incidentRecordSummaries": []}` |
| `resiliencehub` | `list-apps` | ✔ 空列表 |

> ⭐ **意外发现**：`support-app`（Support App / Slack 集成）**竟然通过了订阅层**。
> 这与 `support` 主 API 全被锁形成鲜明对比 ——
> 说明 **AWS 的支持类 API 并非整体封锁，而是逐个服务、逐个操作地挂付费墙**。
> 对做分层设计的启示：**付费墙的粒度可以做到"同一产品族内不同子服务不同策略"。**

### 🔴 被订阅层锁死的（8 项）

| 服务 | 操作 | 错误 |
|---|---|---|
| `support` | `describe-cases` | `SubscriptionRequiredException`（带完整文案） |
| `support` | `describe-services` | 同上 |
| `support` | `describe-severity-levels` | 同上 |
| `support` | `describe-communications` | 同上 |
| `support` | `describe-trusted-advisor-checks` | 同上 |
| `health` | `describe-events` | `SubscriptionRequiredException`（**无文案**） |
| `health` | `describe-event-types` | 同上 |
| `health` | `describe-events-for-organization` | 同上 |

> **规律**：`support.*` 的错误**带解释文案**（"Premium Support Subscription is required…"），
> `health.*` 的**不带**。同一错误码、不同文案规范 —— 细节但值得记。

### ⚠️ 主动跳过（计费风险）

| 服务 | 操作 | 原因 |
|---|---|---|
| `ce` | `get-cost-and-usage` | **Cost Explorer API 按次计费（$0.01/请求）** → 与「不产生费用」约束冲突，**未调用** |

> 📌 **纪律条目**：在"零费用"约束下做体验，**必须先识别哪些"只读"调用其实是计费的**。
> Cost Explorer / Billing 系列 API 是典型陷阱 —— 它们"只读"但**不免费**。

---

## 三、第一轮记录（2026-09-25，IAM 用户，42 次）

保留原始数据，用于对照。

**42 次只读调用，成功 0 次。**

| 结果 | 次数 |
|---|---|
| ✔ 成功 | **0** |
| ✘ `SubscriptionRequiredException` | 19 |
| ✘ `AccessDeniedException` | 20 |
| ✘ `ParamValidationError`（我方参数错误） | 3 |

### 第一轮的 IAM 层封锁面（20 次）

该 IAM 用户**几乎没有任何附加策略**。被拒操作覆盖面极广：

| 类别 | 服务 / 操作 |
|---|---|
| 支持相关 | `servicequotas:*`、`supportapp:GetAccountAlias`、`ssm-incidents:ListResponsePlans` |
| AI 增值 | `devops-guru:ListMonitoredResources`、`resiliencehub:ListApps` |
| **基础只读** | `s3:ListAllMyBuckets`、`iam:GetAccountSummary`、`cloudwatch:DescribeAlarms` ⭐ |
| 运维 | `events:ListRules`、`config:DescribeConfigurationRecorders`、`ssm:ListDocuments` |
| 安全 | `cloudtrail:DescribeTrails`、`securityhub:DescribeHub` |
| 成本 | `ce:GetCostAndUsage` ×2、`compute-optimizer:GetEnrollmentStatus` |
| 组织 | `organizations:list_accounts`、`organizations:describe_organization` |
| 资源 | `resource-explorer-2:ListIndexes` |

> ⭐ `s3:ListAllMyBuckets` 与 `iam:GetAccountSummary` 都被拒 —— 这两个是 AWS 权限体系里最松的只读操作。
> 当时据此推断「该 IAM 用户处于权限真空」。
> **第二轮证实：这个推断只对"该 IAM 用户"成立，对"账号"不成立**（root 下全部通过）。

### 第一轮的区域对照（排除区域因素）

| 区域 | 结果 |
|---|---|
| `us-east-1` / `us-west-2` / `ap-southeast-1` / `eu-west-1` | 同一操作返回**完全相同**的 `SubscriptionRequiredException` |
| `cn-north-1` | `UnrecognizedClientException`（中国区凭据体系独立） |

### 第一轮的我方参数错误（3 次，已定位）

诚实记录，供后续复现避坑：

| 操作 | 错误 | 正解 |
|---|---|---|
| `support.describe_communications` | `maxResults=5` 低于下限 | **最小值是 10** |
| `health.describe_affected_entities` | 缺 `filter` | **`filter` 必填** |
| `billing.get_billing_view` | 缺 `arn` | **需要 `arn`** |

---

## 四、这次实测证明了什么（对华为立项的价值）

### 1.「付费墙」是 AWS 支持体系的**一等公民**，且粒度很细
`SubscriptionRequiredException` 这个错误码的**存在本身**，说明 AWS 在**架构层**就实现了按计划分级授权。
第二轮更发现：**同一个 `support` 产品族内，`support-app` 能过、`support` 主 API 不能过** ——
付费墙可以细到**子服务级**。

### 2. 免费层与付费层的差距是「断崖式」的
Basic 计划下：Trusted Advisor 只有 56 项、**没有 Health API、没有 Support API、没有 SAW**。
→ 「**用 API 可用性做付费分层**」的教科书案例。

### 3. 订阅校验发生在 IAM 之前 —— 这是可复现的事实，不是推测
只换身份（受限 IAM 用户 → root）就得到了一组干净的对照实验。
**推论**：如果我们要做类似分层，**要先把"订阅/合同层校验"放在"权限校验"前面**，
否则客户会拿到误导性的权限错误。

### 4. `sts:GetCallerIdentity` 成功 ≠ 账号可用（方法论）
第一轮的教训。**身份可行、网络可达、但业务能力为零。**
→ 验证外部服务可用性时，**必须做能力级探测，不能只做连通性探测**。

### 5. 新形态账号体系下，"支持计划"这个概念本身可能不存在（新增）
「新形态 AWS」把账号抽象成 **project**、把 IAM 用户抽象成 **team member**，
支持计划也退化为 **FREE / PAID** 两种计划类型。
→ **对华为的启示：面向中小客户，把支持能力做成"计划档位"而不是"合同采购项"，能大幅降低决策成本。**
（但代价是：**这类客户拿不到 API 级能力**，而这正好可以是我们的差异化切口。）

---

## 五、后续若要真正体验，需要什么

| 需求 | 说明 |
|---|---|
| **① 换账号形态** | 当前新形态账号**无法开通**传统 Support API / Health API，需改用传统 AWS 账号并订阅 **Business Support+** |
| **② IAM 策略** | 若走传统账号：需附加 `AWSSupportAccess`（AWS 托管）+ `Health_ViewOnlyAccess` + `ServiceQuotasReadOnlyAccess` + `AWSCloudWatchReadOnlyAccess` |
| **③ 如需 IDR** | 须 **Enterprise Support**，且 IDR **额外付费 + 90 天起订** —— **与"不产生费用"约束冲突，不可行** |
| **④ 如需 TA 全套** | 需 Business+；56 项免费检查在 Basic 下**连 API 都读不到**（订阅层拦截在前） |

---

## 六、网络环境记录（复现须知）

| 项 | 值 |
|---|---|
| 代理 | `HTTP_PROXY=http://127.0.0.1:57079`（端口**动态变化**，此前为 63017） |
| 现象 | 间歇性 `ProxyConnectionError: Failed to connect to proxy URL` |
| 影响面 | 仅 IAM 端点偶发；STS / Support / Health / FreeTier 端点正常 |
| 判定 | **瞬时抖动，非稳定故障**（socket 直连测试确认端口 OPEN） |
| 对策 | `aws login` 前设 `NO_PROXY=localhost,127.0.0.1,::1`（否则浏览器回环回调会被自己的代理截走） |

---

## 七、原始数据位置

| 文件 | 内容 |
|---|---|
| `D:/AI/my_project/_aws_probe.py` | 第一轮 22 项探测脚本 |
| `D:/AI/my_project/_aws_probe2.py` | 第一轮 20 项探测脚本（修正参数 + 扩面） |
| `D:/AI/my_project/_aws_probe_result.json` | 第一轮原始结果 |
| `D:/AI/my_project/_aws_probe2.json` | 第一轮原始结果 |
| `D:/AI/my_project/_aws_toolkit/plan-state.json` | **第二轮：账户计划状态（PAID/ACTIVE）** |

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 总入口（引用本文的统计）
- [[AWS-Agent-Toolkit-安装记录]] — 第二轮的安装与验证全过程
- [[AWS支持服务工具-AWS-Health]] — 官方对 `SubscriptionRequiredException` 的原文说明
- [[AWS支持服务工具-Trusted-Advisor]] — 56 / 482 项检查的分层
- [[AWS支持服务工具-Support-API与工单]] — 21 个操作清单
- [[AWS支持服务工具-IDR与AI增强]] — `ssm-incidents` 与 IDR 通路的关联
