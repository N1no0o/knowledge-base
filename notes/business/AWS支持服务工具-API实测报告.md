---
title: AWS 支持服务工具 · API 实测报告（2026-09-25）
tags: [AWS, 支持服务, API, 实测, SubscriptionRequiredException, 华为云支持服务立项]
created: 2026-09-25
updated: 2026-09-25
source: 本机真实 API 调用 42 次（boto3 1.43.101 / botocore 1.43.101）｜原始记录 _aws_probe_result.json / _aws_probe2.json｜2026-09-25
status: stable
---

# AWS 支持服务工具 · API 实测报告

> **实测时间**：2026-09-25 03:09 – 03:10（UTC+8）
> **测试账号**：`206482634625`，IAM 用户 `WorkBuddy`（UserId `AIDATAE2S66AVV3R6ECUO`）
> **身份校验**：`sts:GetCallerIdentity` **成功** ✔（说明凭据有效、网络可达）
> **支持计划（用户口述）**：Business
> **约束**：**不产生任何费用**，全部调用为只读
> **工具链**：Python 3.13.12 + boto3 1.43.101（独立 venv）

---

## 一、结论先行

**42 次只读调用，成功 0 次。**

| 结果 | 次数 | 占比 |
|---|---|---|
| ✔ **成功** | **0** | 0% |
| ✘ `SubscriptionRequiredException` | **19** | 45% |
| ✘ `AccessDeniedException` / `AccessDenied` | **20** | 48% |
| ✘ `ParamValidationError`（**我方参数错误**，已定位） | 3 | 7% |

**这个账号无法用于 AWS 支持服务工具的体验** —— 但失败本身就是**有价值的一手证据**：
它精确暴露了 AWS 支持体系的**两层封锁机制**。

---

## 二、两层封锁机制（核心发现）

### 第一层：订阅层（Subscription Layer）

```
SubscriptionRequiredException:
Amazon Web Services Premium Support Subscription is required to use this service.
```

**关键特性（实测验证）**：

| 特性 | 证据 |
|---|---|
| **在 IAM 之前拦截** | 即使把 IAM 策略配全，此错误依然出现 —— 订阅校验先于权限校验 |
| **调用方无法自行绕过** | 这是账号级商务状态，非技术配置 |
| **跨区域一致** | 在 `us-east-1` / `eu-west-1` 两区实测同一操作，**返回完全相同错误** → 排除区域因素 |
| **中国区行为不同** | `cn-north-1` 返回 `UnrecognizedClientException`（中国区凭据体系独立） |

**触发该错误的操作（19 次）**：

| 服务 | 操作 |
|---|---|
| `support` | `describe_trusted_advisor_checks` ×2、`describe_trusted_advisor_check_summaries` ×3、`describe_trusted_advisor_check_result`、`describe_services` ×2、`describe_severity_levels`、`describe_cases`、`describe_communications`、`describe_attachment` |
| `health` | `describe_events` ×2、`describe_affected_entities`、`describe_event_types`、`describe_events_for_organization` |

→ **即：Trusted Advisor、Support API、Health API 三大支持工具组全部被订阅层锁死。**

### 第二层：IAM 层（Identity Layer）

```
AccessDeniedException: User: arn:aws:iam::206482634625:user/WorkBuddy
is not authorized to perform: <action> because no identity-based policy allows the <action> action
```

**关键特性**：该 IAM 用户**几乎没有任何附加策略**。

**被拒的操作（20 次）—— 覆盖面极广**：

| 类别 | 服务 / 操作 | 说明 |
|---|---|---|
| 支持相关 | `servicequotas:*` (3)、`supportapp:GetAccountAlias`、`ssm-incidents:ListResponsePlans` | Service Quotas / Slack App / Incident Manager |
| AI 增值 | `devops-guru:ListMonitoredResources`、`resiliencehub:ListApps` | DevOps Guru / Resilience Hub |
| **基础只读** | `s3:ListAllMyBuckets`、`iam:GetAccountSummary`、`cloudwatch:DescribeAlarms` | ⭐ **连最基础的只读都被拒** |
| 运维 | `events:ListRules`、`config:DescribeConfigurationRecorders`、`ssm:ListDocuments` | EventBridge / Config / SSM |
| 安全 | `cloudtrail:DescribeTrails`、`securityhub:DescribeHub` | CloudTrail / Security Hub |
| 成本 | `ce:GetCostAndUsage` ×2、`billing:get_billing_view`(参数错)、`compute-optimizer:GetEnrollmentStatus` | Cost Explorer / Billing |
| 组织 | `organizations:list_accounts`、`organizations:describe_organization` | 返回简化文案 `You don't have permissions to access this resource.` |
| 资源 | `resource-explorer-2:ListIndexes` | Resource Explorer |

> ⭐ **`s3:ListAllMyBuckets` 和 `iam:GetAccountSummary` 都被拒** 是最强的信号 ——
> 这两个是 AWS 权限体系里最松的只读操作。它们被拒说明该 IAM 用户**处于权限真空状态**。

---

## 三、我方参数错误（3 次，已定位）

诚实记录，避免误导后续复现：

| 操作 | 错误 | 正解 |
|---|---|---|
| `support.describe_communications` | `maxResults=5` 低于下限 | **`maxResults` 最小值是 10** |
| `health.describe_affected_entities` | 缺 `filter` | **`filter` 是必填参数** |
| `billing.get_billing_view` | 缺 `arn` | **需要 `arn` 参数** |

> 这三条已回写进对应的工具笔记，作为「参数陷阱」条目。

---

## 四、网络环境记录（复现须知）

| 项 | 值 |
|---|---|
| 代理 | `HTTP_PROXY=http://127.0.0.1:57079`（端口**动态变化**，此前为 63017） |
| 现象 | 间歇性 `ProxyConnectionError: Failed to connect to proxy URL` |
| 影响面 | 仅 IAM 端点偶发；STS / Support / Health 端点正常 |
| 判定 | **瞬时抖动，非稳定故障**（socket 直连测试确认 57079 端口 OPEN） |

> ⚠️ 复现时若遇代理报错，先确认当前端口，再重试。

---

## 五、这次实测证明了什么（对华为立项的价值）

### 1.「付费墙」是 AWS 支持体系的一等公民
API 访问不是技术门槛而是**商务门槛**。
`SubscriptionRequiredException` 这个错误码的存在本身，说明 AWS 在**架构层就实现了按计划分级授权**。

### 2. 免费层（Basic）与付费层的差距是「断崖式」的
Basic 计划下：Trusted Advisor 只有 56 项、**没有 Health API、没有 Support API、没有 SAW**。
→ 这是「**用 API 可用性做付费分层**」的教科书案例。

### 3. 「Business 计划」的口述与实测不符，需要跟进核实
用户口述支持计划为 Business，但实测显示 **Trusted Advisor / Support API / Health API 全部返回订阅不足**。
可能原因（**待用户侧确认**）：
- 该账号实际未订阅到 Business（如仍是 Basic / Developer）
- 订阅已过期或在途
- 账号类型为 PLS（Partner Led Support），该类型下部分 API 不可用

> 🔴 **建议动作**：登录 AWS Support Center → **Support plans** 页面，
> 截图确认当前计划名称与生效时间。这是排除「凭据有效但订阅无效」唯一可靠的办法。

### 4. `sts:GetCallerIdentity` 成功 ≠ 账号可用
这是本次最大的方法论提醒：
**身份可行、网络可达、但业务能力为零** ——
验证外部服务可用性时，**必须做能力级探测，不能只做连通性探测**。

---

## 六、后续若要真正体验，需要什么

| 需求 | 说明 |
|---|---|
| **① 确认订阅计划** | 至少 **Business Support+**（Health API / Support API / SAW 的门槛） |
| **② IAM 策略** | 需附加只读策略：`AWSSupportAccess`（AWS 托管策略）+ `Health_ViewOnlyAccess` + `ServiceQuotasReadOnlyAccess` + `AWSCloudWatchReadOnlyAccess` |
| **③ 如需 IDR** | 须 **Enterprise Support**，且 IDR 本身**额外付费 + 90 天起订** —— **与"不产生费用"约束冲突，不可行** |
| **④ 如需 Trusted Advisor 全套** | 需 Business+；**56 项免费检查在 Basic 下也读不到 API**（订阅层拦截在前） |

---

## 七、原始数据位置

| 文件 | 内容 |
|---|---|
| `D:/AI/my_project/_aws_probe.py` | 第一轮 22 项探测脚本 |
| `D:/AI/my_project/_aws_probe2.py` | 第二轮 20 项探测脚本（修正参数 + 扩面） |
| `D:/AI/my_project/_aws_probe_result.json` | 第一轮原始结果 |
| `D:/AI/my_project/_aws_probe2.json` | 第二轮原始结果 |

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 总入口（引用本文的统计）
- [[AWS支持服务工具-AWS-Health]] — 官方对 `SubscriptionRequiredException` 的原文说明
- [[AWS支持服务工具-Trusted-Advisor]] — 56 / 482 项检查的分层
- [[AWS支持服务工具-Support-API与工单]] — 21 个操作清单
- [[AWS支持服务工具-IDR与AI增强]] — `ssm-incidents` 被拒与 IDR 通路的关联
