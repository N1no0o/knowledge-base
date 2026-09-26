---
title: AWS 支持计划 33 项能力 × 四档逐项取值
tags: [AWS, 支持计划, 能力矩阵, 差距分析, 竞品]
created: 2026-09-27
updated: 2026-09-27
source: dist/aws-support-plans/AWS支持计划能力逐项分析报告.md（66.9 KB，2026-09-27 00:05）｜原件 D:/AI/my_project/dist/aws-support-plans/
status: growing
---

# AWS 支持计划 33 项能力 × 四档逐项取值

**结论：四档的分档轴不是「支持量大小」而是「工作负载的失效后果等级」（Default → Production → Business-critical → Mission-critical）；权益差距只有三个断崖，且**所有档位溢价只买三件事 —— 顶级故障的 25 分钟时间差、一支指定团队、供应商侧主动监控**。**

## 一、定位与定价（控制台页面实读）

| 档位 | 页面 `Recommended for` | 最低月费 | 百分比阶梯 |
|---|---|---|---|
| Basic | Default Support Plan | 无 | — |
| **Business Support+** | Minimum recommended plan for production workloads | **$29/月·每账号** | 9% ≤$10K ／ 7% 10–80K ／ 5% 80–250K ／ 3% >$250K |
| **Enterprise** | business-critical workloads | **$5,000/月·含所有账号** | 10% ≤$150K ／ 7% 150–500K ／ 5% 500K–1M ／ 3% >$1M |
| **Unified Operations** | mission-critical + enhanced resilience | **$50,000/月·含所有账号** | 10% ≤$1M ／ 6% 1–5M ／ 5% >$5M |

> ⚠️ **「每账号」vs「含所有账号」是结构性差异**：BS+ 最低月费按账号逐个计，多账号环境下成本线性增长；Enterprise/Unified 整组织包干。这就是矩阵里 `Multi-account Support` 从 Enterprise 才出现的原因。

## 二、33 项能力压缩表（取值 = 交付形态，不只是有无）

| # | 能力 | Basic | BS+ | Enterprise | Unified |
|---|---|:--:|:--:|:--:|:--:|
| 1 | Unlimited 24/7 contextual recommendations | ✓⚠️ | ✓ | ✓ | ✓ |
| 2 | DevOps Agent 抵扣额度 | ✗ | 30% | 75% | 100% |
| 3 | Business/Mission-critical down 响应 | ✗ | <30m | <15m | **<5m** |
| 4–7 | 其余四类响应时间 | ✗ | <1h/<4h/<12h/<24h | 同 BS+ | 同 BS+ |
| 8 | Account & billing support | ✓ | 24×7 | 白手套礼宾 | **指定专家** |
| 9 | Designated TAM | ✗ | **✗** | ✓ | ✓ |
| 10 | Designated DSE | ✗ | ✗ | **✗** | **全球覆盖** |
| 11 | Incident Management Engineers | ✗ | ✗ | **✗** | ✓ |
| 12 | Architectural Guidance | ✗ | 语境化 | 咨询式评审 | 持续评审 |
| 13 | Well-Architected Reviews | ✗ | **✗** | ✓ | ✓ |
| 14 | Proactive security review | ✗ | **✗** | ✓ | ✓ |
| 15 | Planned events and launch | ✗ | ✗ | ✓ | ✓ |
| 16 | Personalized strategic support plan | ✗ | ✗ | ✓ | ✓ |
| 17 | Customized proactive services | ✗ | ✗ | ✓ | ✓ |
| 18 | Critical Workload Review | ✗ | ✗ | **✗** | **持续** |
| 19 | Health Dashboard | ✓ | ✓ | ✓ | ✓ |
| 20 | Health API | ✗ | **✓** | ✓ | ✓ |
| 21 | 24/7 workload monitoring | ✗ | **✗** | **✗** | **✓** |
| 22 | 24×7 phone/web/chat/email | ✗ | ✓ | ✓ | ✓ |
| 23 | Support App in Slack | ✗ | ✓ | ✓ | ✓ |
| 24 | Unlimited cases and contacts | ✗ | ✓ | ✓ | ✓ |
| 25 | Third-party software support | ✗ | ✓ | ✓ | ✓ |
| 26 | Support API | ✗ | **✓** | ✓ | ✓ |
| 27 | Trusted Advisor | ✗ | 全部检查 | ＋Priority | ＋Priority |
| 28 | Support Automation Workflows | ✗ | ✓（112+） | ✓ | ✓ |
| 29 | re:Post | ✓ | 优先响应 | 优先响应 | 优先响应 |
| 30 | Security Incident Response | ✗ | 另付费 | **✓ 内含** | ✓ |
| 31 | Countdown Premium | ✗ | 另付费 | 另付费 | **✓ 内含** |
| 32 | Incident Detection and Response | ✗ | **✗** | 另付费 | **✓ 内含** |
| 33 | AWS Managed Services | ✗ | **✗** | 另付费 | **另付费** |

## 三、三个断崖（逐行核对结果）

| 断崖 | 增量 | 本质 |
|---|---|---|
| **Basic → BS+** | **15 项**由 ✗ 变可用（5 类响应时间 + Health API/Support API/TA 全量/SAW + 24×7 四渠道 + Slack + 无限工单 + 第三方支持 + 语境化架构指导 + Agent 30%），另 2 项由「不可得」变「可购」 | **唯一一次能力面的整体跃迁**，也是门槛最低的一次（$29/月起）。**BS+ 才是这套体系的真正起点** |
| **BS+ → Enterprise** | **6 项**由 ✗ 变内含（TAM + Well-Architected 评审 + 主动安全评审 + 计划事件与上线 + 个性化战略支持计划 + 定制化主动服务），另 2 项变可购 | 6 项**全部是「必须由专属人力交付」**的能力 ⇒ **这份清单本身就是「TAM 的附加值列表」** |
| **Enterprise → Unified** | **4 项**由 ✗ 变内含（DSE / Incident Management Engineers / Critical Workload Review / 24-7 workload monitoring），另 3 项由「可购」变内含 | **质变而非量变**：监控主体从「你」变「AWS」，责任主体从「某个人」变「一支队」 |

> ⚠️ **Unified 不是 Enterprise 的超集**：Enterprise 有 4 项是 ✗。

## 四、14 项「全档无差异」项（升级零收益）

响应时间 4 项（`<1h`/`<4h`/`<12h`/`<24h`）· 通道与工单 4 项（24×7 渠道、Slack、无限工单、第三方支持）· 工具与 API 4 项（Health API、Support API、SAW、Health Dashboard）· 其它 2 项（24/7 contextual recommendations、re:Post）。

> **采购法则**：诉求若落在上述 14 项内，**BS+ 已是终点，升级是浪费**。

## 五、页面自身的数据问题（诚实记录，不替 AWS 圆场）

| # | 问题 | 处置 |
|---|---|---|
| 1 | `Unlimited 24/7 contextual recommendations` 在 **Basic 列也打 ✓**，与 Basic 其他权益自相矛盾；已回原始 DOM 复核 `columnId=basic` 确为对勾路径，**非解析错误** | 该行 Basic/BS+ 取值**不可信** |
| 2 | 矩阵写 `phone/web/chat/email`，而 `describe-create-case-options` 只返回 web/call/chat | 以控制台开单页为准 |
| 3 | DevOps Agent 抵扣基数措辞不一（`gross Support spend` vs `prior month's spend`） | 采购前须向 AWS 确认 |
| 4 | 45 行矩阵无 `Multi-account Support` 行，定价计算器描述里有 | 两处视图不一致，以合同为准 |
| 5 | `#/pricingcalculator` 不是有效路由（重定向回 `#/compare`） | 计算器是页内 button，需点击展开 |

## 6. 证据等级纪律（本报告口径）

🟢 实读/实测（可复现）｜🟡 推演（按公开规则推导，未官方确认）｜⚪ 未验证（页面声称但无探针 —— **全部人工服务类权益一律 ⚪，不替 AWS 背书**）。
另注意：**矩阵取值 ≠ 权益已激活**；响应时间是「目标」而非 SLA（页面脚注原文为 *every reasonable effort*）。

## 相关

- [[aws-support-plans-baseline]] — 事实底座与本账号实测证据
- [[aws-support-plans-ba-architecture]] — 把 33 项压成 7 业务域的 BA 六视图
- [[aws-support-plans-ba-cards]] — 33 张单能力卡片（下钻版）
- [[华为云支持服务立项-AWS竞品对标]] — 立项引用版（含 IDR / DevOps Agent 定价）
