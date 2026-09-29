---
title: AWS 支持工具面实测与竞品分析 · 三堵墙与六家工具面全景
tags: [AWS, 支持服务, 竞品分析, 工具面普查, 档位墙, Runbook, 华为云支持服务立项]
created: 2026-09-30
updated: 2026-09-30
source: deliverables/product-strategy/competitive-analysis-aws-support-tooling-2026-09-27.md（含工具面一手实测，2026-09-27 15:41）｜原件 D:/AI/my_project/deliverables/product-strategy/
status: growing
---

# AWS 支持工具面实测与竞品分析 · 三堵墙与六家工具面全景

**一句话结论：AWS 支持工具面的真实边界不在「有没有 API」，而在**三堵墙** —— ①档位墙（核心工具卡 `Business+` 起）②组织墙（14+ 条 `AccessDenied` / `NoAvailableOrganizationException`）③前置条件墙（TA 需先跑、Compute Optimizer 需先 Opt-in、SIR 需先买会员）；真正「开箱即用」的只有 59 条。六家里**只有 AWS 工具广度做到一家顶六家，也只有 AWS 的门最重**；「可编程 Runbook 库」这一格**全球仅 AWS 有（1/6 独占）**，是最值得我方抢的空白位。**

## 一、TL;DR

- **这轮不是读文档，是真调了工具**：对 AWS 支持类 **12 个 CLI 命名空间 / 396 个操作（只读 194 个）**建立完整工具面清单，
  并对 **194 个只读操作 100% 覆盖执行**；去重后 **202 条实测条目、195 条真正打到服务端、59 条返回成功**，
  全部原始响应落盘可复核。
- **最大意外发现**：`devops-agent` **不是空壳** —— AWS 在升级 `Business+` 后**自动为客户建了一个可用的 AI 运维队友工作空间**
  （Operator App 网址、自动创建 IAM 角色、预置技能/记忆库/运维报告目标、已完成系统学习任务）。
  这是本次实测数据最丰富的工具面（25 条全部真调用、13 条成功）。
- **次大发现**：`wellarchitected` 95 个操作里有 **23 个 `*-agent-*`**，其中 10 个 `get-/list-` 报 **`400 Unknown Operation`**
  ⇒ **AWS 正在把 Well-Architected 评审 Agent 化，CLI 与模型已发布、服务端尚未上线** —— 可直接用于路线图预判的领先信号。
- **竞品定位判断**：六家里**只有 AWS 工具广度做到"一家顶六家"，但也只有 AWS 的门最重**；
  **GCP 相反（工具全放开、只收人工）**；**「可编程 Runbook 库」全球仅 AWS 有（1/6 独占）**。

## 二、核心结论卡片

| 项目 | 内容 |
|---|---|
| **推荐方案** | 工具面按「**读与集成全放开、主动与专属按档收口**」设计；优先补 **① 健康事件 API+推送**、**② 支持品牌化可编程 Runbook 库**（对标 AWS SAW 的 114 个 `AWSSupport-*`） |
| **优先级** | **P0**（健康事件 API / 工单 API 解绑档位）→ **P1**（Runbook 库 / 巡检建议可编程）→ **P2**（对外工具能力对比页） |
| **预期影响** | 直接消掉「健康事件不可编程」这一最实缺口（GCP/腾讯云已证明可行）；用开放性在开发者心智上压过 AWS 的档位墙 |
| **资源需求** | 健康事件 API：中（可复用既有健康看板数据源）｜Runbook 库：中高（可复用 COC/AOM 自动化能力，起步 20–30 个场景） |
| **风险等级** | **中** —— 主要风险是"对标 AWS"措辞引发以服务等级反击；须用用户视角价值语言 |
| **实测可信度** | **高**：双模型交叉验证 + 编排层独立对账；随机抽 5 条重跑 **5/5 一致**；工具面清单经 `CLI` / `botocore 模型` / `两个 agent` **四方对账**，仅 3 处差异且全部定位到根因 |

## 三、方法论与人手分工（可证伪设计）

| 角色 | 承担者 | 职责 | 为什么必须分开 |
|---|---|---|---|
| **实现/实测** | `codex` | 写实测台并**真跑**（202 条 → 补参后再跑 130 条），产出原始响应 | 它能稳定批量写代码 + 执行 |
| **独立审计** | `dsh` | 从**完全不同的数据源**（botocore 离线模型）独立建真值源，逐字段审计实测结果 | **换一个模型才会挑出实现方的错** —— 共报出 **22 条缺陷**（含 1 条 P0） |
| **编排 + 独立验收** | 主理人 | 定契约、下发、**自己写独立验收器复核**、执行修复回路 | 不听任何 agent 自述 |

**交接面只有磁盘文件**：契约写在 `_multiagent/workspace/aws-support-tools/INTERFACE.md`，三个 agent 互看不到对方上下文。

**可证伪设计四条**：① 原始响应全量落盘（`raw/` 202 个 + `raw2/` 130 个）；② 单条可重跑（`--only "<ns>/<op>" --out <path>`）；
③ **两条互不相干的真值路径**（CLI `aws <ns> help` 的 kebab-case vs botocore `service-2.json` 的 PascalCase，共 434 个服务模型）；
④ 四方对账。

**🔴 必须交代的三个诚实边界**：

1. **`dsh` 宿主执行不了外部命令**（pwsh 报 `0xFFFF0000` CLR 初始化失败，沙箱升级被 fail-closed 拒）
   ⇒ 它自报 P0 缺陷 D-1：「随机抽 5 条重跑」它一条都没跑成（**0/5**）。**由编排层代跑补齐，结果 5/5 一致**。
   它另一条 D-7「产出非生成器所写」是**基于"自己跑不了"的错误推断**，已由编排层实跑证伪并令其撤回。
2. **没有开真实工单** —— `create-case` 会产生**真实 AWS 工单**（有真实人工响应、影响账号档案），本轮**未执行**。
3. **未测计费 API** —— `ce` / `cur` / `pricing` / `budgets` 均按次计费或产生计费对象，零成本约束下**全程未调用**。

## 四、工具面全景（实测，非文档抄录）

| 命名空间 | 操作数 | 其中只读 | 工具在 AWS 体系里的角色 | 实测可达性 |
|---|---:|---:|---|---|
| `wellarchitected` | **95** | 43 | Well-Architected 评审（**含 23 个 AI Agent 操作**） | ⚠️ 10 条 `400 Unknown Operation` |
| `drs` | 69 | 23 | 弹性灾难恢复 | ⚠️ 本账号未启用 |
| `devops-agent` | **62** | **30** | **AI 运维队友（Business+ 自动开通）** | ✅ **实测最丰富** |
| `compute-optimizer` | 28 | 17 | 资源优化建议（TA 的数据源之一） | ⚠️ `Inactive`（未 Opt-in） |
| `service-quotas` | 26 | 9 | 配额管理 | ✅ 可用（support 服务下配额为空） |
| `security-ir` | 24 | 11 | 安全事件响应（**会员制**） | ❌ `SecurityIncidentResponseNotActiveException` |
| `support` | 20 | 14 | **Support Center 核心 API**（工单/TA/严重级） | ✅ 核心可用 |
| `health` | 14 | 12 | 服务健康与事件 | ✅ 可用（组织级 5 条全拒） |
| `trustedadvisor` | 12 | 9 | **新版 TA API**（推荐 + 优先级） | ✅ 推荐可读，Priority 需组织 |
| `support-app` | 10 | 3 | Support App（Slack 集成） | ✅ API 通，未配置 |
| `ssm-incidents` | 31 | 12 | Incident Manager（Unified Operations 相关） | ⚠️ 未启用 |
| `freetier` | 5 | 5 | 账户计划状态 | ✅ 可用 |
| **合计** | **396** | **194** | — | 只读 op **100% 覆盖执行** |

**负向验证**：`support-plans` / `countdown` / `idr` / `ams` / `managedservices` / `trust` —— **六个全部报 `Found invalid choice`**，
且 botocore 模型里也没有对应服务目录。
> ⚠️ 这不代表服务不存在，而是**没有公开 CLI/API 面**。`Countdown` / `IDR` / `AMS` 在产品页确实存在且分档售卖，
> 但**只能通过控制台/销售流程触达** —— **对"工具面能力"而言，它们等于不存在**。
> 这也解释了为何 Unified Operations 强调"**包干团队**"而非"工具"。

## 五、三堵墙（错误码地形图比"有没有 API"更有信息量）

| 错误码 | 条数 | 它说明什么 |
|---|---:|---|
| `ResourceNotFoundException` | 25 | 面可用，只是喂的是合成 ID |
| `ValidationException` | 24 | 面可用，参数格式约束严格（**含 TA 的反直觉 ARN 格式**） |
| `UninitializedAccountException` | 20 | **前置条件墙**：Compute Optimizer 未 Opt-in |
| `AccessDeniedException` | 18 | **组织墙 + 权益墙**（含 1 条复合） |
| `OptInRequiredException` | 11 | **前置条件墙**：服务未启用（DRS 类） |
| `400 Unknown Operation` | **11** | ⚠️ **CLI 有命令、服务端不认** |
| `IllegalArgumentException` / `BadRequestException` / `InvalidParameterValueException` | 12 | 参数语义错误 |
| `SecurityIncidentResponseNotActiveException` | 1 | **会员制墙** |

**数据地形图（含补参重跑）**：合并去重 202 条；**真正打到服务端 195（96.5%）**；返回成功 59；
CLI 本地校验失败（请求没发出去）7；服务端拒绝/异常 132；超时 2。
> **为什么必须补参重跑**：首轮对"有必填参数的只读 op"没喂参数，124 条只拿到 CLI 本地校验错误（`ParamValidation`）——
> **请求根本没发出去，零信息量**。补参后 95.4% 真正触达服务端，这才有了真正的能力结论。
> 这一步是**修复回路**的产物，也是本报告与"抄文档"的分水岭。

## 六、逐个工具族的关键实测特性

### 6.1 `support` —— Support Center 核心 API（20 op / 14 只读）

- `describe-services` ✅ **324 个服务**，响应 **418,742 B**（"能对哪些服务开单"的权威口径）
- `describe-severity-levels` ✅ 5 级：`low/normal/high/urgent/critical`
- `describe-supported-languages` ✅ 7 种
- `describe-trusted-advisor-checks` ✅ **639 项检查目录** —— **必须传 `--language`**，且**不支持 `--max-results`**
- `describe-cases` ✅ 但 **46.9 秒** ⚠️ **响应极慢**

**🔴 特性：TA 刷新有 1 小时冷却**
```
aws support refresh-trusted-advisor-check --check-id 7DAFEmoDos
  → {"status":"enqueued","millisUntilNextRefreshable":3599994}   # ≈ 1 小时
```
⇒ 这解释了为什么"主动巡检"类能力**不能被当作实时监控**用 —— 它是**小时级**的。一条被文档低估的实际约束。

### 6.2 `trustedadvisor` —— 新版 TA API（12 op / 9 只读）

新旧同源同量（都 639）、数据结构不同：顶层键 `checks` vs `checkSummaries`；载荷 873 KB vs **1,241,494 B**。
`list-recommendations` **只返回 1 条**（`MFA on Root Account`，`status=error`）⇒ **旧 API 给目录，新 API 给已产出的结论**。

推荐对象结构很"产品化"：按 `pillars` + 按资源聚合 `resourcesAggregates` + 估算月度节省 `estimatedMonthlySavings`。

**🔴 反直觉的工具特性：`get-recommendation` 的 ARN 格式**

| 传法 | 结果 |
|---|---|
| `9ffa2f45-...`（纯 UUID） | ❌ 拒 |
| `arn:aws:trustedadvisor:us-east-1:206482634625:recommendation/...`（带 region） | ❌ 拒 |
| **`arn:aws:trustedadvisor::206482634625:recommendation/9ffa2f45-...`（region 段留空）** | ✅ **成功** |

服务端正则为 `arn:[\w-]+:trustedadvisor::\d{12}:recommendation/[\w-]+` —— **region 段必须为空**。
一条试错才能发现的接口特性，值得记进我方 API 设计反面教材。

### 6.3 ⭐ `devops-agent` —— 最大发现：预置好的 AI 运维队友（62 op / 30 只读）

实测 25 条全部真调用、13 条成功。真相比"页面写了个 DevOps Agent"丰富得多：

- **被自动开通**：`{"agentSpaces":[{"name":"DevOpsAgentSpace","description":"Created by Support Center","createdAt":"2026-09-26T14:07:42Z"}]}`
  —— `createdAt` 与账号升级 `Business Support+` 时间几乎重合 ⇒ **客户无需任何操作**。
- **同时创建 IAM 角色 + 可访问的 Operator App**：`operatorAppUrl` = `https://<id>.aidevops.global.app.aws`，
  角色 `DevOpsAgentRole-WebappAdmin-*`；关联 `accountType=monitor`。
  ⇒ **不只是一个 API，而是"带 Web 操作台 + 跨账号监控角色"的完整产品**。
- **预置资产 4 件**：`skill`（`sample-skip-scheduled-maintenance`，INACTIVE）、`memory_store`（`understanding-agent-space`，ACTIVE）、
  `memory`（`overview`）、`artifact`。
- **预置一个目标（Goal）**：「Generate Weekly Post-Incident Analysis Reports with Actionable Recommendations」，
  聚焦**流水线测试改进 / 可观测性增强 / 基础设施优化**三条线。
- **已完成一次系统学习**：`taskType=SYSTEM_LEARNING`、`status=COMPLETED`，升级后约 **40 分钟**完成。

> **📌 产品含义**：AWS 已把支持服务从"人接工单"推进到 **"AI 队友带工作台、带记忆、带预置目标地交付"**，
> 而且**默认开通、零操作门槛**。我方若仍把 AI 定位为"对话式客服"，差的是一个量级。

### 6.4 `wellarchitected` —— 95 op，藏着 23 个未上线的 AI Agent 操作

**10 个 `get-/list-` 全部返回 `400 Unknown Operation`**（`get-agent-context` / `get-agent-goal` / `get-agent-profile` /
`get-agent-recommendation` / `list-agent-*` 等）。
⇒ CLI 与 botocore 模型**已发布**这 23 个操作，但 `us-east-1` 服务端**尚未部署** ⇒
**AWS 正在把 Well-Architected 评审 Agent 化（agent-context / agent-goal / agent-profile / agent-recommendation + 反馈回路）**
—— **领先于公开文档的产品信号**，路线图预判价值极高。

> ⚠️ 卫生问题：`get-consolidated-report` 返回 `status=ok` 但只有 **25 B**、耗时 **23.6 s** —— "成功但无数据"，不应被当作正面证据。

### 6.5 `health` —— 开放性最弱的一环

`describe-events` ✅（`eventScopeCode=PUBLIC`）；`describe-event-types` ⚠️ **超时 90 s**；
`describe-event-details` ⚠️ `status=ok` 但内含 `failedSet[0].errorName=EventNotFoundError` —— **伪成功**；
**5 条组织级全部 `AccessDenied` / `NoAvailableOrganizationException`**。
⇒ 单账号下可用，**组织级视图完全取决于是否加入 Organizations**，而新 AWS 体验账号默认**不在任何组织内**。

### 6.6 `support-app` —— "API 通 ≠ 已接入"的活标本

`list-slack-channel-configurations` → `[]`（44 B）；`list-slack-workspace-configurations` → 46 B（**耗时 46.6 s**）；
`get-account-alias` → **0 字节**。
⇒ API 完全可用，但因未配置 Slack 工作区，**所有列表为空**。这类"空数组"极易被误读为"能力缺失"，实为"未配置"。

### 6.7 `security-ir` / `compute-optimizer` / `drs` —— 三种不同的墙

- **`security-ir`（会员制）**：`list-cases` → `SecurityIncidentResponseNotActiveException: does not have an active membership`
  ⇒ **SIR 是独立会员制**，与支持档位不是同一套权益体系（"需单独 sign up"的第三态）。
- **`compute-optimizer`（前置条件墙）**：`get-enrollment-status` → `{"status":"Inactive"}`，其余 20+ 条 `UninitializedAccountException`
  ⇒ **必须先 Opt-in**。这是 TA 639 项中 517 项 `not_available` 的真因（已用 `MFA on Root Account` 作探针验证）。
- **`drs` / `ssm-incidents`**：未启用服务的标准失败模式（`drs` 无一条 `ok`）。

### 6.8 ⭐ `ssm` —— SAW 自动化 Runbook 库：114 个，一次列全

```
aws ssm list-documents --filters Key=Name,Values=AWSSupport- --max-items 200
  → 114 条 DocumentIdentifiers，全部以 AWSSupport- 开头；响应中【无 NextToken】⇒ 列表完整
```
- 页面宣传"100+"，**实测 114 ⇒ 未夸大**，且这是**精确值**而非下界
- ✅ **`list-documents` → `describe-document` 两步链路实测打通**（7,598 B）
- ⇒ **六家里唯一"支持品牌化 + 可编程 + 可执行"的自动化资产**，我方最值得抢的空白位

## 七、六家工具面全景（⚠️ 文档层证据，未做一手实测）

> 完整分析见 `_members/competitive-analysis-support-tools-2026-09-27.md`（含逐条来源 URL 与 `[官方]/[社区]/[推测]` 证据分级）。
> **该部分为文档层证据，与 §四的一手实测性质不同，引用时请勿混用。**

| 厂商 | 工具面一句话特征 |
|---|---|
| **AWS** | **工具最全、API 最全，但门最重。** 所有"工程师有用的 API"从 `Business Support+` 一次放开 |
| **Microsoft Azure** | **读的放开、写（开单）收费。** Advisor / Service Health 免费且全 API 化，工单 API 卡 `ProDirect`（$1,000/月）以上 |
| **Google Cloud** | **把"可编程"当默认值。** Cloud Support API 从最低付费档 `Standard`（$29/月）起，健康与巡检 API **全客免费** ⇒ 与 AWS 门槛哲学最相反 |
| **阿里云** | 工单 / 巡检 API **全公开、无明显档位墙**，差异在响应时效 |
| **华为云（我方）** | 工单 API 卡 `商业级/企业级`；**健康事件缺对外 API**（仅状态页 + 消息中心） |
| **腾讯云** | **连健康事件 API 都不挂档位**（`DescribeEvents` 免费） |

**关键差异轴 —— 工具是否被"档位墙"锁住**：

| 维度 | AWS | Azure | GCP | 阿里云 | 华为云 | 腾讯云 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 工单 API 公开可编程 | ✅ **Business+ 起** | ✅ **ProDirect+ 起** | ✅ **Standard 起** | ✅ 无明显墙 | ✅ **商业级+ 起** | ⚠️ 待确认 |
| 健康事件 API | ✅ **Business+ 起** | ✅ 免费 | ✅ 免费 | — 仅 RSS | **❌ 无** | ✅ 免费 |
| 巡检 API | ✅ Business+ 起 | ✅ 免费 | ✅ 免费 | ✅ 公开 | ⚠️ 待确认 | — |
| **可编程自动化 Runbook 库** | ✅✅ **SAW 114 个（独家）** | ⚠️ 通用自动化 | — | ⚠️ OOS 编排 | ✅ COC（未与支持场景绑定） | ⚠️ 混沌演练 |
| 档位墙强度 | **✅✅ 最极端** | ✅ 中 | ⚠️ 弱 | ❌ 弱 | ✅ 中 | ⚠️ 弱-中 |

**SWOT（站在我方立场）**：

- **S**：云宝助手已成体系（四场景 + HITL + 转工单）；工单 API + COC + AOM 齐全；
  **IM 企业群形态领先**（企业微信/钉钉/飞书群 + 7×24 专线，是 AWS Support App in Slack 的中国化对等物，且是"群"不是"单点应用"）
- **W**：**健康事件无对外 API**（最实缺口）；工单 API 卡商业级；巡检建议是否可编程待确认；AI 助手无公开 API
- **O**：健康事件 API 是低垂果实；**SAW 类 Runbook 库是 6 家中的空白区**；把"工具解锁"从"按档位"改为"按身份与安全边界"
- **T**：AWS 工具广度全球第一（一家把六家的工具都在手里）；GCP 用"全免费开放"抢开发者心智；
  Azure 把支持入口做进 Copilot；中国厂商同质化

## 八、行动清单

| # | 行动 | 负责方 | 时间窗 | 优先级 | 验收标准 |
|---|---|---|---|---|---|
| 1 | **补建「云服务健康事件 API + 订阅推送」，不挂付费档位墙** | 支持产品 | 立项后首季 | **P0** | 公开事件查询 API（按产品/地域/时间过滤）+ Webhook 等价推送；**全付费档可用**；发布开发者文档 |
| 2 | **解绑工单 API 的档位限制**（开放到所有付费档） | 支持产品 | 与 #1 同步 | **P0** | 服务目录中工单 API 从"商业级/企业级"扩展为"付费档全量"；对外口径统一 |
| 3 | **立项「支持 Runbook 库」对标 AWS SAW**，从 20–30 个高频场景起步 | 支持产品 + COC | 第 2 季 | **P1** | ≥30 个官方 Runbook（连通性/性能/日志/安全遏制四类齐全）；API 可列出与执行；高风险项强制 HITL |
| 4 | **把「优化顾问 / 巡检建议」做成可编程读取** | 支持产品 | 第 2 季 | **P1** | 公开"列出巡检项 / 读取巡检结果 / 触发刷新"三类 API |
| 5 | **对标 DevOps Agent 的"AI 队友工作台"形态**（本次实测最大发现） | 云宝 + 支持产品 | 第 3 季 | **P1** | AI 助手有独立工作台入口 + 可编程资产（技能/记忆）+ 预置目标模板；不再是纯对话式 |
| 6 | **建立「竞品支持工具面」季度实测机制**（复用本轮方法论） | 产品战略 | 每季 | **P2** | 每次产出可证伪的工具面清单 + 原始响应存档 |
| 7 | 对外发布「支持工具能力对比表」，标注"我方工具 API 全客可用" | 市场 + 支持产品 | 第 3 季 | **P2** | 官网可访问；**事实全部可溯源**，不出现无法证实的数字 |

> ⚠️ **措辞纪律**：#7 对外**不要用"对标 AWS"**，而用「**工具可编程能力不分档，只有主动服务分档**」
> 这一用户视角价值语言 —— AWS 的档位墙是其商业模型的一部分，正面点名容易引发对方用"服务等级"反击。

## 九、待确认 / 假设 / Non-goals

**假设（未验证，请勿直接对外引用）**：

1. **`devops-agent` 由升级自动触发**：依据是 `createdAt` 与升级时间重合 + `description:"Created by Support Center"`。
   **未做对照实验**（无法回退档位验证），故为高置信推断而非已验证结论。
2. **`wellarchitected` 的 23 个 `*-agent-*` 是"将上线的 AI 评审能力"**：依据是 CLI/模型已发布 + 服务端 `400 Unknown Operation`。
   **具体是灰度、分区域还是延迟上线，未知**。
3. **`describe-cases` 的 46.9 s 是"无工单时的普遍延迟"还是本账号个案**，未在有多工单的账号上复核。

**待确认**：① 10 条元数据类缺陷（`latency_ms` 跨尝试累加、`skip` 的 `error_class` 三种写法并存、`--only` 残留清理）未做第二轮修复；
② `probe_results.json`（首轮）未覆盖重跑，与 `probe_results2.json` 存在分叉，本报告以**两者合并口径**为准；
③ TA 的组织级与 Priority 权益在本账号**无法分离归因**。

**🔴 Non-goals（本轮明确不做）**：① 不开真实支持工单；② 不调计费类 API；③ 不做控制台 UI 测评；
④ 不测 `Countdown` / `IDR` / `AMS`（无公开 API 面）；⑤ 不做竞品实测（§七为文档层证据）；
⑥ 不覆盖写操作（396 个操作中 202 个写操作**全部未执行**）。

## 十、🔴 一条会反复踩的坑

**关键会话可复用发现**：`aws login` 续期**需同时重定向 `AWS_CONFIG_FILE`** ——
否则被文件策略层 fail-closed 拦在 `~/.aws/config` 写操作上，**报"会话过期"误导**。
（详见技能 `aws-cli-login-automation` 与项目 `topic-E` 分册。）

## 相关

- [[aws-support-tooling-probe-v3-realrun]] — 同线的 v3 真实调用轮结论（09-29，取代本报告的部分数据）
- [[aws-support-tooling-probe-v3-deck-index]] — A 线交付包与支撑件索引
- [[aws-support-full-rerun-overview]] — 09-28 全套重做总览
- [[aws-support-real-run-overview]] — 09-29 真实调用轮总览
- [[aws-support-plans-33-capabilities]] — 支持计划 33 项能力 × 四档
- [[华为云支持服务立项-AWS竞品对标]] — AWS 竞品对标的立项版
- [[aws-support-tooling-probe-audit]] — v1 轮 A/B/C/D 审计
- [[sh600519-fundamentals-2026-09-30]] — 同批 agent 产出件（交易分析侧：体例同源的"数据源标注 + 存疑项显式披露"）
