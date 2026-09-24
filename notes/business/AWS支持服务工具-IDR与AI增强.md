---
title: AWS 支持服务工具 · IDR 与 AI 增强层
tags: [AWS, 支持服务, IDR, EventBridge, IME, 竞品, 华为云支持服务立项]
created: 2026-09-25
updated: 2026-09-25
source: AWS 官方文档 aws-incident-detection-response/（40 篇，docs.aws.amazon.com/IDR/latest/userguide/）｜2026-09-25
status: growing
---

# AWS 支持服务工具 · IDR 与 AI 增强层

> 本篇覆盖 AWS 支持体系里**最贵、也最难抄**的一层：IDR（Incident Detection and Response）、
> DevOps Agent、Countdown Premium、AWS Managed Services。
>
> 全部事实来自官方文档 `aws-incident-detection-response/`（40 篇），可本地 Ctrl+F 复核。

---

## 一、IDR 是什么（官方定义）

> "AWS Incident Detection and Response offers eligible AWS Enterprise Support customers
> **proactive incident engagement** to reduce the potential for failure and accelerate recovery
> of critical workloads from disruption."
> —— `000-What-is-AWS-Incident-Detection-and-Response.md`

**四个官方卖点**（官方原词，可直接引用）：

| 卖点 | 官方表述 |
|---|---|
| **Improved observability** | AWS 专家指导你定义并**关联应用层与基础设施层**的指标与告警，以提早发现中断 |
| **5-minute response time** | IME（Incident Management Engineer）在你的工作负载告警后**5 分钟内**主动介入；或响应你提交的 critical case |
| **Faster resolution** | IME 使用为你的工作负载**预定义和定制的 runbook**，**代你创建 Support case**，并以**单线程所有权（single-threaded ownership）**负责到底 |
| **Reduced potential for failure** | 事后提供 Post-Incident Review（按需）、共同改进 runbook、可用 Resilience Hub 做持续韧性追踪 |

> ⭐ **「single-threaded ownership」这个提法值得注意** ——
> 它精准描述了「客户不用自己拉通 AWS 内部团队」这个痛点。
> 华为立项时若谈「专人负责到底」，这是 AWS 的现成话术参照。

---

## 二、准入门槛（Terms of Use，官方原文）

来源：`001-Terms-of-use.md`

| 条目 | 官方要求 |
|---|---|
| **适用对象** | 面向**直销和 Partner 转售的 Enterprise Support 账号** |
| **不适用** | **Partner Led Support（PLS）账号不可用** |
| **前置依赖** | **全程必须保持 AWS Enterprise Support 有效**；Enterprise Support 终止 → **同时被移出 IDR** |
| **工作负载** | 所有纳入 IDR 的工作负载**必须走 onboarding 流程** |
| **最短订阅期** | **90 天**；取消须**提前 30 天**提交 |

> 🔴 **对本立项最关键的一条**：IDR 的**订阅期是 90 天起，且必须先买 Enterprise Support**。
> 即：客户要买 IDR，实际门槛是「Enterprise Support（最低 $5,000/月）+ IDR 额外费用 + 90 天锁定」。
> 这不是一个「按需开通」的产品，而是**重承诺型服务**。

---

## 三、架构：EventBridge 是唯一集成点

来源：`002-Architecture.md`

官方原文：

> "**Amazon EventBridge serves as the sole integration point** between your workloads and
> AWS Incident Detection and Response."

架构涉及四个组件：

| 组件 | 作用 |
|---|---|
| **Amazon EventBridge** | **唯一集成点**。告警从 CloudWatch 等监控工具经 EventBridge 摄入，使用 **AWS 托管预定义规则**。需安装 **service-linked role（SLR）** |
| **AWS Health** | 追踪你工作负载所用 AWS 服务上的事件，并在收到告警时通知你 |
| **AWS Systems Manager** | **存放工作负载信息**（架构细节、告警详情、对应的 runbook）—— 以 **SSM Documents** 形式承载 |
| **你的专属 Runbook** | 定义 IDR 在事件管理期间执行什么动作：**联系谁、怎么联系、分享什么信息** |

> ⭐ **架构洞察**：AWS 没有为 IDR 自研事件总线，而是**复用 EventBridge**；
> runbook 也不是自研引擎，而是**复用 SSM Documents**。
> 与我们此前在 SAW 里发现的结论一致 ——
> **AWS 的支持服务自动化，本质是「把已有基础服务编排成支持产品」**，而非重新造轮子。
> 这是「产品化能力 > 技术自研」的典型样本，对华为立项的成本结构估算有直接参考价值。

---

## 四、值班与响应流程（IME 到底做什么）

来源：`032-Incident-management.md`

```
告警产生 → EventBridge → IDR 自动调出对应 runbook
        → 通知 IME → IME 在 5 分钟内响应
        → 会议桥（conference call）/ 按 runbook 指定方式联系你
        → IME 核验 AWS 服务健康度
        → 需要时【代你创建 case】并拉通 AWS 专家
        → 事件缓解/解决
        → 事后 Post-Incident Review（按需）
```

**几个重要的细节（官方原文支持）**：

1. **7×24 主动监控**，由「指定的事件经理团队（a designated team of incident managers）」交付。
2. **IME 可能早于 AWS 服务事件正式宣告就识别出问题** ——
   官方原文："Incident Detection and Response might determine that the incident is related to an
   AWS service issue **before an AWS service event is declared**."
   → 这给客户**提前执行恢复方案或 workaround 的机会**。
3. **告警抖动处理规则（重要）**：
   - 告警触发后快速恢复 → IME **只发 case 通信说明已恢复，不拉会议桥**
   - **但若同一告警在 15 分钟内触发超过一次 → 即使已恢复，IME 仍按 runbook 联系你**
4. **Post Incident Report ≠ RCA**（官方明确）：
   > "The Post Incident Report **isn't a Root Cause Analysis (RCA)**. You can request a RCA
   > **in addition to** the Post Incident Report."
   → PIR 包含：问题描述、影响、拉通了哪些团队、采取了什么缓解动作。

---

## 五、主动请求 Incident Response 的三条路径

来源：`034-Request-an-Incident-Response.md`

适用场景：**工作负载发生了告警未覆盖的严重事件**（含 onboarding 中的工作负载）。
三条路径任选：

### 路径 1：Support Center 控制台
关键分类字段（**必须这样填才会被 IDR 接单**）：

| 字段 | 值 |
|---|---|
| **Case type** | `Technical` |
| **Service** | `Incident Detection and Response` |
| **Category** | `Active Incident` |
| **Severity** | `Business-critical system down` |

建议在 Description 里提供：受影响资源 ARN、工作负载名及用途、业务影响描述、（可选）你偏好的会议桥 URL。
→ **提交后 5 分钟内 IDR 响应并拉会议桥。**

### 路径 2：AWS Support API
官方仅指向 `About the AWS Support API`，即**用标准 Support API 建 case**，
按上面的分类字段填即可（**无专用 IDR API**）。

> 🔴 **这也解释了为什么实测时 Support API 报 `SubscriptionRequiredException`** ——
> IDR 的 API 通路就是 Support API 本身，同样受订阅层拦截。

### 路径 3：Slack
```
/awssupport create
```
按提示填 Subject / 技术信息 / 业务信息，然后选 Issue Type=`Technical support`、
Service=`Incident Detection and Response`、Category=`Active Incident`、
Severity=`Business-critical system down`；可**额外填最多 10 个通知联系人**（逗号分隔）。

---

## 六、Slack 集成的两个注意事项

来源：`035-Manage-...-with-the-AWS-Support-App-in-Slack.md`

1. **必须在工作负载的【所有】账号上都配置 Support App in Slack**，否则收不全通知。
   （因为 **Support case 建在告警来源的那个账号上**）
2. **Slack 通知不能替代 IDR 的电话/邮件紧急联系人** ——
   官方原文："Notifications that you receive through the AWS Support App in Slack **don't replace**
   your workload's initial and escalation contacts that are engaged via email or phone call."

---

## 七、可观测性：两阶段方法论

来源：`031-Monitoring-and-observabililty.md`

AWS 把可观测性拆成**两个层次 + 两个阶段**，这个方法论本身可以直接借鉴：

**两个层次：**
- **业务结果指标（Business Outcome metrics）** —— 从终端用户体验出发。
  官方举例：移动通话 App 的 **Call Setup Success Rate**；网站的 **page speed**。
  ⭐ **"Incident engagement is triggered based on business outcome metrics."**
  → 事件介入由**业务指标**触发，不是由 CPU 告警触发。
- **基础设施层指标（Infrastructure level metrics）** ——
  如 ALB 的 `ApplicationLoadBalancerErrorCount`。

**两个阶段：**
| 阶段 | 重点 |
|---|---|
| **Onboarding phase** | 聚焦**应用层业务结果指标**，让 AWS 能及时响应中断 |
| **Post-onboarding phase** | 主动服务：基础设施层指标定义、指标调优、trace/log 搭建（**视客户成熟度而定**）；**可能横跨数月、涉及多个团队**；**具体实施由客户自己做**，AWS 只出指导 |

同时提到官方 CLI 工具：
[`awslabs/CLI-for-AWS-Incident-Detection-and-Response`](https://github.com/awslabs/CLI-for-AWS-Incident-Detection-and-Response)
（用于自动化 onboarding 步骤）

> ⭐ **「客户自己实施、AWS 只出指导」这句很重要** ——
> 这印证了 [[华为云支持服务立项-立项二三产品定义]] 里的判断：
> **IDR 是重客户侧投入的模式，不是我们该抄的那条路。**

---

## 八、告警摄入的三种集成方式

来源：`014-Direct-EventBridge-integration.md`、`015-Webhook-integration.md`、`016-Amazon-SNS-integration.md`

| 方式 | 适用 | 关键点 |
|---|---|---|
| **APM 直连 EventBridge** | New Relic / Datadog / Splunk 等 | 提供 CloudFormation 模板一键部署；**会产生额外费用（Lambda + EventBridge）**；每个账号每个区域都要部署 |
| **Webhook** | 无原生 EventBridge 集成的监控工具 | 见 `015` |
| **Amazon SNS** | 已有 SNS 通知链路 | 见 `016` |
| **CloudWatch 告警** | 原生 | 最标准路径 |
| **APM 告警** | 第三方 APM | 见 `012` |

**APM 集成的两个硬性前提（易踩坑）：**
1. 必须先在账号里创建 SLR `AWSServiceRoleForHealth_EventProcessor`
2. 必须自行修改模板里的 `TransformLambdaFunction`，把
   `event["detail"]["incident-detection-response-identifier"]`
   指向**你这套 APM 的告警名 JSON 路径**（每个 APM 都不同）：
   - New Relic → `event["detail"]["workflowName"]`
   - Datadog → `event["detail"]["meta"]["monitor"]["name"]`
   - Splunk → `event["detail"]["ruleName"]`

AWS 会安装一条**托管规则** `AWSHealthEventProcessorEventSource-DO-NOT-DELETE`
（名字里带 DO-NOT-DELETE，顾名思义不能删）。

---

## 九、IDR 报告能力

来源：`036-Reporting.md`

| 数据类型 | 内容 |
|---|---|
| **配置数据** | 所有已 onboard 账号；所有应用名；每个应用关联的**告警、runbook、支持档案** |
| **事件数据** | 每个应用的**日期/数量/时长**；特定告警关联的事件；**Post Incident Report** |
| **性能数据** | **SLO 性能** |

获取方式：**联系你的 TAM**。
→ 注意：**没有自助报表 API**，数据要靠 TAM 给。这又是一个「专人依赖」。

---

## 十、安全与数据边界（客户最关心的两条）

来源：`037-Security-and-resiliency.md`

1. **默认接收范围**（官方原文）：
   > "By default, Incident Detection and Response **receives the ARN and state of every CloudWatch
   > alarm in your account**"
   → **默认是全账号所有 CloudWatch 告警的 ARN + 状态**。想收窄要**联系 TAM 定制**。
   → ⭐ 这是客户安全评审必问的一条，可以作为「我们比它更克制」的差异化切入点。

2. **区域可用性**（`004-Region-availability.md`）：
   覆盖 27+ 区域，支持**英语、日语、中文（Mandarin）、韩语**四种语言。
   → **中文是官方支持语言**，说明 AWS 在中国客户出海场景上是认真做的。

---

## 十一、AI 增强层：DevOps Agent 与其他增值服务

> ⚠️ **证据等级说明**：以下内容基于 `_website/` 产品页与支持计划总览，
> **未见独立的官方用户指南目录**，故标注为「产品页级证据」，引用时需谨慎。

| 服务 | 定位 | 计费 | 证据等级 |
|---|---|---|---|
| **AWS DevOps Agent** | AI 自主调查事件、给出根因分析 | **按量付费 + 抵扣金** | 产品页级 |
| **Countdown Premium** | 关键活动（大促/迁移/上线）护航 | **Enterprise 需额外付费 / Unified Ops 已含** | 支持计划总览 |
| **AWS Managed Services (AMS)** | 托管运维（人 + 自动化代运营） | 需额外付费 | 支持计划总览 |
| **AWS Resilience Hub** | 持续韧性追踪（IDR 官方文档中提及可配合使用） | — | IDR 官方文档引用 |

> ⚠️ 上一轮探测中，`devops-guru` 与 `resiliencehub` 的 API 调用均返回 `AccessDeniedException`，
> **无法验证**其真实能力边界。若后续需要，建议走「申请试用账号」或「查官方产品页 + re:Invent 演讲」补齐。

---

## 十二、对华为立项的三条可直接用结论

### 结论 1：IDR 的门槛结构 = 「重承诺三件套」
**Enterprise Support（≥$5,000/月）+ IDR 额外费用 + 90 天锁定期**
→ 客户真正要决策的不是「买不买 IDR」，而是「**要不要整个押到 Enterprise**」。

### 结论 2：IDR 的本质是「流程产品化」，不是「技术产品」
- 集成点用 EventBridge（现成）
- Runbook 用 SSM Documents（现成）
- 自动化用 Lambda（现成）
- 唯一「自研」的是 **IME 团队 + 方法论（两层次两阶段可观测性）**

→ 对我们的启示：**要拼的不是技术组件，是「人 + 流程 + 方法论」的组织能力**。
这也是为什么 [[华为云支持服务立项-立项二三产品定义]] 判断 IDR「客户侧投入极重、不该照抄」。

### 结论 3：两个可用的差异化切口（均有官方事实支撑）
| AWS 的做法 | 我们可以主张的差异 |
|---|---|
| 默认采集**全账号所有 CloudWatch 告警 ARN + 状态** | 更克制的数据采集边界（可显式授权、白名单化） |
| 报告数据**只能找 TAM 要**，无自助 API | 提供**自助数据接口**（这对客户的技术团队友好得多） |

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 工具体系总入口
- [[AWS支持服务工具-API实测报告]] — 42 次真实调用记录（含 IDR 通路 = Support API 的验证）
- [[AWS支持服务工具-SAW与Slack]] — 同为「复用基础服务做产品」的样本
- [[华为云支持服务立项-立项二三产品定义]] — 为什么不抄 IDR
- [[华为云支持服务立项-AWS竞品对标]] — 竞品定价与分层
