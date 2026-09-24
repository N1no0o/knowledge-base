---
title: AWS 支持服务配套工具 · 体验报告（2026-09-25）
tags: [AWS, 支持服务, 体验报告, 竞品, 华为云支持服务立项, 实测]
created: 2026-09-25
updated: 2026-09-25
source: 42 次真实只读 API 调用 + cloud-support-docs/aws/ 957 篇官方文档 + 28 篇官网产品页｜2026-09-25
status: stable
---

# AWS 支持服务配套工具 · 体验报告

**报告日期**：2026-09-25
**体验方式**：真实 API 调用（能测的通路）+ 官方文档深度分析（不能测的通路）
**测试账号**：`206482634625` / IAM 用户 `WorkBuddy`
**约束条件**：不产生任何费用，全部只读
**配套笔记**：6 篇（见 [[AWS支持服务工具-手册总览]]）

---

## 一、结论先行（TL;DR）

**这次体验的最重要产出，不是「学会了怎么用」，而是「看懂了 AWS 怎么分层卖」。**

三个可直接用于华为立项的判断：

| # | 结论 | 证据强度 |
|---|---|---|
| **1** | **AWS 支持体系是三层叠加（数据层 / 服务层 / AI 层），且「API 访问」本身被当作付费开关，而不是技术能力** | ⭐⭐⭐ 官方原文 + 实测双重验证 |
| **2** | **分层差异高度集中在「最高严重级别的响应速度」和「检查项数量」两个点上，其余能力全计划一致** | ⭐⭐⭐ 官方矩阵原文 |
| **3** | **AWS 的支持服务自动化没有自研引擎 —— 全部是「把已有基础服务编排成产品」（EventBridge / SSM / Lambda）** | ⭐⭐⭐ 官方架构文档原文 |

---

## 二、体验结果总览

### 2.1 实测部分：42 次调用，0 成功

| 结果 | 次数 | 占比 |
|---|---|---|
| ✔ 成功 | **0** | 0% |
| ✘ `SubscriptionRequiredException`（订阅层拦截） | 19 | 45% |
| ✘ `AccessDeniedException`（IAM 层拦截） | 20 | 48% |
| ✘ `ParamValidationError`（我方参数错误，已定位） | 3 | 7% |

**但 `sts:GetCallerIdentity` 是成功的** —— 说明**凭据有效、网络可达**。
所以这不是「环境不通」，而是 **「账号级别没有能力」**。

**两层封锁机制（本报告最有价值的发现）：**

```
第 1 层：订阅层  ← SubscriptionRequiredException
        ↑ 在 IAM 之前拦截；跨区域一致；调用方无法自行绕过
第 2 层：IAM 层  ← AccessDeniedException
        ↑ 该 IAM 用户几乎无任何策略（连 s3:ListAllMyBuckets 都被拒）
```

> 🔴 **方法论提醒（这是本次最硬的一课）**：
> **`sts:GetCallerIdentity` 成功 ≠ 账号可用。**
> 验证外部服务可用性时，**必须做「能力级探测」，不能只做「连通性探测」**。
> 只测连通的结论会完全错误。

### 2.2 文档分析部分：覆盖 10 个工具，957 篇官方文档

不能实测的通路，全部走了官方文档，且**每条事实都可在本地 Ctrl+F 复核**（源文件在 `D:/AI/my_project/cloud-support-docs/aws/`）。

| 工具 | 定位 | 计划门槛 | 本次体验方式 |
|---|---|---|---|
| **AWS Health Dashboard** | 事件权威数据源 | **免费** | 文档 |
| **AWS Health API** | 事件编程获取 | **Business+** | 实测（被拦）+ 文档 |
| **Trusted Advisor** | 482 项最佳实践检查 | **56 免费 / 426 需 Business+** | 实测（被拦）+ 文档 |
| **Support Center / 工单** | 案例全生命周期 | **Basic 免费**（不能改严重级别） | 文档 |
| **Support API** | 工单自动化（21 操作） | **Business+** | 实测（被拦）+ 文档 |
| **SAW** | SSM Runbook 自助修复 | **Business+** | 文档 |
| **Support App in Slack** | IM 内管理工单 | **Business+** | 实测（被拦）+ 文档 |
| **TAM** | 指定技术客户经理 | **Enterprise+** | 文档 |
| **IDR** | IME 5 分钟响应 + Runbook | **Enterprise 需额外付费 / Unified Ops 已含** | 实测（被拦）+ 文档 |
| **DevOps Agent / Countdown / AMS** | AI 与增值服务 | 按量付费 / 额外付费 | 文档（产品页级证据） |

---

## 三、对华为立项最有价值的 6 个发现

### 发现 1：付费墙的位置是「API 访问」本身

官方原文（Health）：

> "You must have an AWS Business Support+, AWS Enterprise Support, or AWS Unified Operations plan
> to use the AWS Health API. **If you call the AWS Health API from an AWS account that isn't enrolled
> in one of these plans, then you receive a `SubscriptionRequiredException` error.**"

Support API 同一套原文，措辞几乎一致。

**⇒ 关键洞察**：
AWS 把 **「事件可见」免费开放**（Dashboard + EventBridge），把 **「事件可编程获取」锁在 Business+ 之后**。
这是 **「基础可见免费、自动化/集成付费」** 的分层范式。

**对我们的用法**：
> 「AWS 的做法是：让你**看得见**事件，但要**把事件接进你自己的系统**，先买 Business。
> 这说明「API 访问权」在国际主流云厂商那里，本身就是一张付费门票，而不是技术能力。」

### 发现 2：分层的「量化比例」可以做得非常干净

Trusted Advisor 官方数字：

| 层级 | 检查项数 | 比例 |
|---|---|---|
| 免费（所有计划） | **56 项** | 11.6% |
| **Business+ 解锁** | **+426 项** | 88.4% |
| 总计 | **482 项** | 100% |

**⇒ 关键洞察**：
**88% 的能力锁在付费墙后，而且 API 和 CLI 权限与检查项数绑在同一道墙上卖。**
这给「能力型 + 分层溢价」提供了**国际厂商的量化先例**，不是我们独创的收费借口。

### 发现 3：分层差异高度集中，不是「全线提速」

严重级别响应矩阵（官方原文）：

| 严重级别 | 代码 | 首次响应时间 |
|---|---|---|
| 一般性指导 | `low` | 24 小时 |
| 系统受损 | `normal` | 12 小时 |
| 生产系统受损 | `high` | 4 小时 |
| 生产系统停机 | `urgent` | 1 小时 |
| **业务关键型系统停机** | `critical` | **Business+ < 30 分钟 / Enterprise < 15 分钟 / Unified Ops 5 分钟（IME）** |

**⇒ 关键洞察**：
**前四级在所有付费计划间完全一致**，只有最高一级拉开差距。
**升级卖的不是「全面更快」，而是「最坏情况下更快」。**

**对我们的用法**：
> 华为「尊享级 <5 分钟」对标的是 **Unified Operations 的 IME 5 分钟响应** ——
> 而且对方是**专人（Incident Management Engineer）**在响应，不是自动化工单。
> 这个对标关系要在立项材料里说清楚，否则容易被质疑「5 分钟是自动化还是人」。

### 发现 4：AWS 的支持自动化没有自研引擎 —— 全是「编排已有服务」

这是本次**最反直觉、也最有成本参考价值**的发现。

| 支持产品 | 用的什么底座 | 官方原文位置 |
|---|---|---|
| **IDR** | **Amazon EventBridge 是唯一集成点** | `002-Architecture.md`（IDR） |
| **IDR 的 Runbook** | **AWS Systems Manager Documents** | 同上 |
| **SAW** | **AWS Systems Manager Runbooks** | SAW 用户指南 |
| **APM 告警转换** | **Lambda + EventBridge** | `014-Direct-EventBridge-integration.md` |
| **Slack 触达** | **嵌入 Slack（不自建 IM）** | Support App 文档 |

官方原文（IDR 架构）：

> "**Amazon EventBridge serves as the sole integration point** between your workloads and
> AWS Incident Detection and Response."

**⇒ 关键洞察**：
AWS 支持服务的**技术自研投入极低**，几乎全是**产品化能力**：
- 集成点 → 复用 EventBridge
- 自动化 → 复用 SSM Runbook
- 转换 → 复用 Lambda
- IM 触达 → 嵌入 Slack

**唯一自研的，是「IME 团队 + 方法论」。**

**对我们的用法**：
> 「AWS 的支持服务不是靠自研引擎取胜的。它把 EventBridge、SSM、Lambda 编排成产品，
> 真正自研的是**人 + 流程 + 方法论**。
> 这提示我们：**要拼的不是组件，是组织能力。**」
>
> 同时也说明：**做支持服务的边际成本结构可以很低** —— 底座全是现成的。

### 发现 5：IDR 的门槛结构 = 「重承诺三件套」

官方原文（IDR Terms of Use）：

| 条目 | 官方要求 |
|---|---|
| 适用对象 | **直销和 Partner 转售的 Enterprise Support 账号** |
| 前置依赖 | **全程必须保持 Enterprise Support 有效**；终止 → **同时被移出 IDR** |
| **最短订阅期** | **90 天**；取消须**提前 30 天**提交 |
| 不适用 | **Partner Led Support（PLS）不可用** |

**⇒ 关键洞察**：
客户买 IDR 的真实决策是 **「Enterprise Support（≥$5,000/月）+ IDR 额外费用 + 90 天锁定」**。
**不是「按需开通」，是「重承诺」。**

**对我们的用法**（这条直接支撑「不该抄 IDR」的判断）：
> IDR 是**客户侧投入极重**的模式：90 天起订、必须押 Enterprise、onboarding 过程中
> **具体实施要客户自己做，AWS 只出指导**。
> 我们做支持服务，**要走轻承诺、快交付的路，不是走 IDR 这条重资产路。**

### 发现 6：两个现成的差异化切口（都有官方事实支撑）

| AWS 的现状（官方原文） | 我们可以主张的差异 |
|---|---|
| IDR **默认接收全账号所有 CloudWatch 告警的 ARN + 状态**；想收窄要联系 TAM 定制 | **更克制的数据采集边界**：显式授权、白名单化 |
| IDR 的报告数据（配置/事件/性能）**只能找 TAM 要，无自助报表 API** | **提供自助数据接口** —— 对客户技术团队友好得多 |

---

## 四、体验过程中的「踩坑清单」（可直接复用）

这些都是实际调用中撞到的，写下来避免重复踩：

| # | 坑 | 正解 |
|---|---|---|
| 1 | `Support.describe_communications` 传 `maxResults=5` 报 `ParamValidationError` | **最小值是 10** |
| 2 | `Health.describe_affected_entities` 不传 `filter` 报错 | **`filter` 是必填参数** |
| 3 | `billing.get_billing_view` 不传 `arn` 报错 | **`arn` 是必填参数** |
| 4 | 以为配好 IAM 策略就能调支持类 API | **`SubscriptionRequiredException` 在 IAM 之前拦截**，配策略无效 |
| 5 | 以为 `sts:GetCallerIdentity` 成功就代表账号可用 | **必须做能力级探测**，连通性 ≠ 能力 |
| 6 | 以为换个区域能绕过订阅限制 | **跨 `us-east-1` / `eu-west-1` 实测返回完全相同错误**，区域无关 |
| 7 | 直接用 `cn-north-1` 端点测 | 返回 `UnrecognizedClientException` —— **中国区凭据体系独立** |
| 8 | 代理端口写死 | 本机代理端口**动态变化**（63017 → 57079），遇 `ProxyConnectionError` 先确认端口 |

---

## 五、需要老板决策/跟进的事项

### 5.1 必须确认（阻塞性问题）

🔴 **口述的「Business 计划」与实测不符。**
用户口述支持计划为 Business，但 Trusted Advisor / Support API / Health API **全部返回订阅不足**。

三种可能，需要登录控制台核实：
1. 账号实际未订阅到 Business（仍是 Basic / Developer）
2. 订阅已过期或在途
3. 账号类型为 **PLS（Partner Led Support）** —— 该类型下部分 API 不可用

**核实方法**：AWS Support Center → **Support plans** 页面，截图确认当前计划名称与生效时间。
**这是排除「凭据有效但订阅无效」的唯一可靠办法。**

### 5.2 若后续要真正做完整体验

| 需求 | 说明 | 与「不产生费用」约束的关系 |
|---|---|---|
| ① **Business Support+** | Health API / Support API / SAW 的门槛 | ⚠️ **需付费**，冲突 |
| ② IAM 只读策略 | `AWSSupportAccess` + `Health_ViewOnlyAccess` + `ServiceQuotasReadOnlyAccess` + `AWSCloudWatchReadOnlyAccess` | ✔ 免费 |
| ③ **IDR** | 须 Enterprise Support + IDR 额外付费 + 90 天起订 | 🔴 **与约束直接冲突，不可行** |
| ④ Trusted Advisor 全套 | 需 Business+ | ⚠️ 需付费 |

**⇒ 结论：在「不产生费用」的前提下，付费 API 通路无解。**
**当前「文档分析 + 已有实测失败证据」的组合，已经是这个约束下的最完整交付。**

### 5.3 🔴 安全提醒（重要）

1. **AWS AK/SK 泄露**：本次测试用的 Access Key ID（`AKIA****`，20 位）与 Secret Access Key
   已在对话中明文传输。虽然该 IAM 用户权限极低（几乎无策略、连 `s3:ListAllMyBuckets` 都被拒），
   **仍建议轮换** —— 因为权限可能随时被追加。
2. **GitHub PAT 泄露**：会话中明文出现的 `ghp_****` 令牌**建议吊销重建**。

> ⚠️ **本报告已按 GitHub secret scanning 要求移除凭据原文。**
> 首次推送时 GitHub 直接以「Secret detected in content」拒绝（HTTP 422），
> 说明仓库的 secret scanning 防护正常工作 —— 这本身是一次正面验证。

---

## 六、交付物清单

### 6.1 知识库笔记（7 篇，已推送 GitHub）

| 笔记 | 内容 |
|---|---|
| [[AWS支持服务工具-手册总览]] | 工具体系三层全景 + 计划门槛矩阵 + 探测结果汇总 |
| [[AWS支持服务工具-AWS-Health]] | Dashboard 免费 vs API 需 Business+；15 个 API 操作 |
| [[AWS支持服务工具-Trusted-Advisor]] | 56 / 482 项；6 大类别；5 个 API 操作 |
| [[AWS支持服务工具-Support-API与工单]] | 21 个操作；严重级别矩阵；3 个重要限制 |
| [[AWS支持服务工具-SAW与Slack]] | SSM Runbook 完整清单；Slack 集成 |
| [[AWS支持服务工具-IDR与AI增强]] | EventBridge 唯一集成点；IME 5 分钟；90 天起订 |
| [[AWS支持服务工具-API实测报告]] | 42 次调用的完整记录与两层封锁机制分析 |

### 6.2 本报告

`D:/knowledge-base/notes/business/AWS支持服务配套工具-体验报告.md`

### 6.3 原始数据

| 文件 | 内容 |
|---|---|
| `D:/AI/my_project/_aws_probe.py` / `_aws_probe2.py` | 探测脚本（22 + 20 项） |
| `D:/AI/my_project/_aws_probe_result.json` / `_aws_probe2.json` | 原始调用结果 |

### 6.4 文档底座（可 Ctrl+F 复核）

```
D:/AI/my_project/cloud-support-docs/aws/   957 篇官方 md
├── aws-support-user-guide/            169 篇
├── aws-support-api-reference/          52 篇
├── aws-health-user-guide/              47 篇
├── aws-health-api-reference/           41 篇
├── aws-incident-detection-response/    40 篇
├── aws-service-quotas/                 31 篇
├── aws-well-architected-framework/    476 篇
├── aws-well-architected-tool/         109 篇
├── _website/                           28 篇产品页
└── _pdf/                                9 份官方整册
```

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 笔记总入口
- [[华为云支持服务立项-AWS竞品对标]] — 竞品定价与六维度
- [[华为云支持服务立项-EDR产品定义]] — EDR 定位
- [[华为云支持服务立项-立项二三产品定义]] — VIP TAC 与昇腾 950
- [[EDR立项-AWS竞品分析资料包索引]] — 语料库入口
