---
title: AWS 支持计划 33 张单能力 BA 卡片（交付主体视角）
tags: [AWS, 支持计划, BA业务架构, 单能力卡片, 交付主体, 竞品]
created: 2026-09-27
updated: 2026-09-27
source: dist/aws-support-plans/AWS支持计划_逐项能力BA逆向.md（84.1 KB，2026-09-27 00:56）｜原件 D:/AI/my_project/dist/aws-support-plans/
status: growing
---

# AWS 支持计划 33 张单能力 BA 卡片

**结论：把 BA 六视图下钻到每一项能力（33 张卡片），四档形态表填的是「由谁交付」而不是「有没有」；汇总结构数据显示 —— 33 项里有 **16 项**在 BS+ 与 Unified 之间**交付主体完全相同**（其中 **14 项取值也相同 = 真·升级零收益**），**30 项**带业务风险/口径提示。**

## 一、卡片结构与交付主体编码

每张卡片固定回答 11 个问题：①业务问题 ②业务价值 ③业务对象 ④对象动作 ⑤流程定位 ⑥触发条件 ⑦业务角色 ⑧业务规则 ⑨前置依赖与激活 ⑩度量口径 ⑪映射接口（BA → AA/DA/TA）。

**交付主体编码**（四档形态表的核心，填「谁交付」）：

| 码 | 含义 |
|:--:|---|
| `SS` | 客户自助 |
| `AI` | AI / 自动化代理 |
| `TP` | 池化人力（Pooled） |
| `NR` | 具名专人（Named Resource） |
| `DT` | 指定团队 / 供应商主动 |
| `PQ` | 仅取得采购资格（Purchase Qualification） |
| `--` | 本档不可得 |

## 二、33 项卡片索引（四档交付主体）

| ID | 域 | L2 能力组 | 能力项 | Basic | BS+ | Ent | Uni | 证据 | 风险 |
|:--:|:--:|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | D1 | 事件协调指挥 | Incident Management Engineers | NO | NO | NO | DT | ⚪ | ⚠️ |
| 2 | D1 | 响应时限承诺 | Business/Mission-critical system down | NO | TP | TP | DT | ⚪ | ⚠️ |
| 3 | D1 | 响应时限承诺 | Production system down | NO | TP | TP | TP | ⚪ | ⚠️ |
| 4 | D1 | 响应时限承诺 | Production system impaired | NO | TP | TP | TP | ⚪ | |
| 5 | D1 | 响应时限承诺 | System impaired | NO | TP | TP | TP | ⚪ | |
| 6 | D1 | 响应时限承诺 | General guidance | NO | TP | TP | TP | ⚪ | |
| 7 | D2 | 供应商侧主动监控 | 24/7 workload monitoring | NO | NO | NO | DT | ⚪ | ⚠️ |
| 8 | D2 | 健康可视化 | AWS Health Dashboard | SS | SS | SS | SS | ⚪ | ⚠️ |
| 9 | D2 | 健康数据集成 | AWS Health API | NO | AI | AI | AI | 🟢 | ⚠️ |
| 10 | D3 | 专属人力配置 | Designated TAM | NO | NO | NR | NR | ⚪ | ⚠️ |
| 11 | D3 | 专属人力配置 | Designated DSE | NO | NO | NO | DT | ⚪ | ⚠️ |
| 12 | D3 | 关键负载评审 | Critical Workload Review | NO | NO | NO | DT | ⚪ | ⚠️ |
| 13 | D3 | 变更与上线保障 | Planned events and launch | NO | NO | NR | NR | ⚪ | ⚠️ |
| 14 | D3 | 安全治理评审 | Proactive security review | NO | NO | NR | NR | ⚪ | ⚠️ |
| 15 | D3 | 定制主动服务 | Customized proactive services | NO | NO | NR | NR | ⚪ | ⚠️ |
| 16 | D3 | 战略规划 | Personalized strategic support plan | NO | NO | NR | NR | ⚪ | ⚠️ |
| 17 | D3 | 架构指导 | Architectural Guidance | NO | TP | NR | DT | ⚪ | ⚠️ |
| 18 | D3 | 架构治理评审 | AWS Well-Architected Reviews | NO | NO | NR | NR | 🟢 | ⚠️ |
| 19 | D4 | AI 代理 | AWS DevOps Agent with Support integration | NO | AI | AI | AI | 🟢 | ⚠️ |
| 20 | D4 | 接口与集成 | AWS Support API | NO | AI | AI | AI | 🟢 | ⚠️ |
| 21 | D4 | 智能辅助建议 | Unlimited 24/7 contextual recommendations | AI | AI | AI | AI | ⚪ | ⚠️ |
| 22 | D4 | 检查与推荐 | AWS Trusted Advisor | NO | AI | AI | AI | 🟢 | ⚠️ |
| 23 | D4 | 自动化执行 | Support Automation Workflows（SAW） | NO | AI | AI | AI | 🟢 | ⚠️ |
| 24 | D5 | 支持覆盖范围 | Third-party software support | NO | TP | TP | TP | ⚪ | ⚠️ |
| 25 | D5 | 服务通道 | 24/7 phone, web, chat, email | NO | TP | TP | TP | 🟢 | ⚠️ |
| 26 | D5 | 服务通道 | AWS Support App in Slack | NO | TP | TP | TP | 🟢 | ⚠️ |
| 27 | D5 | 服务配额 | Unlimited cases and contacts | NO | TP | TP | TP | 🟢 | ⚠️ |
| 28 | D5 | 社区知识 | AWS re:Post | SS | TP | TP | TP | ⚪ | ⚠️ |
| 29 | D6 | 账户与账单服务 | Account & billing support | SS | TP | NR | NR | 🟢 | ⚠️ |
| 30 | D7 | 安全事件响应 | AWS Security Incident Response（SIR） | NO | PQ | DT | DT | 🟢 | ⚠️ |
| 31 | D7 | 托管运维（代运维） | AWS Managed Services（AMS） | NO | NO | PQ | PQ | ⚪ | ⚠️ |
| 32 | D7 | 检测响应托管 | AWS Incident Detection and Response（IDR） | NO | NO | PQ | DT | ⚪ | ⚠️ |
| 33 | D7 | 重大项目护航 | AWS Countdown Premium | NO | PQ | PQ | DT | 🟢 | ⚠️ |

> **读法**：第 2 行「顶级故障响应」在 BS+ 与 Enterprise 都是 `TP`（池化人力），只有 Unified 变 `DT` —— 即**从「有人接」变「一支队接」**；而第 3–6 行四档全是 `TP`，说明**普通响应速度不是 AWS 的分档变量**。

## 三、自动汇总的结构数据

| 指标 | 值 |
|---|---|
| 卡片总数 / 覆盖业务域 | **33** / **7** |
| 交付主体编码**四档全不同** | **1 项** |
| 主体编码 3 值但四档**形态解读各异** | **4 项** |
| **BS+ 与 Unified 交付主体相同** | **16 项** |
| 其中**取值也相同**（真·升级零收益） | **14 项** |
| 主体未升级但**取值升级**（量为升级） | **2 项** |
| 带风险 / 口径提示的项 | **30 项** |
| 需额外激活动作才能用 | **5 项**（不含前置服务依赖） |

**证据等级分布（撰写侧）**：⚪ 21 项 ｜ 🟢 12 项 ⇒ **近 2/3 的权益无法用程序化探针验证**，全部集中在人工交付类。

## 四、与本套其它三件的关系

| 文件 | 粒度 | 角色 |
|---|---|---|
| `能力基线`（26.3 KB） | 事实与证据 | 本账号实测底座 |
| `能力逐项分析报告`（66.9 KB） | 产品视角 | 33 项 × 四档取值 + 三个断崖 |
| `BA业务架构设计`（43.0 KB） | 整体架构 | 7 业务域 / 六视图 |
| **`逐项能力BA逆向`（84.1 KB，本笔记）** | **单能力** | 33 张卡片，**下钻版** |

> 四件的术语与编号**严格对齐**（7 个 L1 域、R1–R10 规则、12 业务对象、10 业务角色、5 级交付主体）—— 同一能力在整体版与下钻版中编号与结论一致。

## 相关

- [[aws-support-plans-ba-architecture]] — 整体六视图（本文件的上层）
- [[aws-support-plans-33-capabilities]] — 逐项取值与三个断崖（产品视角）
- [[aws-support-plans-baseline]] — 事实底座与实测证据
- [[华为云支持服务立项-立项二三产品定义]] — 我方「尊享级 = 企业级之上新增一级」的对应判断
