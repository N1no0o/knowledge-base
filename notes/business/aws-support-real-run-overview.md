---
title: AWS 支持服务全套重做 · 09-29 真实调用轮总览
tags: [AWS, 支持服务, 多agent, 编排, 真实调用, 进度总览, 华为云支持服务立项]
created: 2026-09-30
updated: 2026-09-30
source: deliverables/product-strategy/aws-support-real-run-overview-2026-09-29.md（7.7 KB）｜原件 D:/AI/my_project/deliverables/product-strategy/
status: growing
---

# AWS 支持服务全套重做 · 09-29 真实调用轮总览

**一句话结论：凭据恢复后把 09-28 被卡死的 A / C 两条线真跑通了 —— v1 的 4 条运行期结论首次被真跑证实、0 条被推翻；唯一负面项是 A 线 U1 真触达率未达标（76.56%）；但两个 worker（codex / dsh）的执行能力本轮都不可用，**跨 agent 独立性降级**，全部由编排层亲做。**

## 一、4 条线状态

| 线 | 内容 | 09-28 | **09-29 真实调用轮** | 交付件 |
|---|---|---|---|---|
| **A** | 工具面普查（209 条真实调用） | 🟡 离线子集 | ✅ **真实调用完成 + A~F 六项审计** | `_multiagent/workspace/aws-support-tools-v2/` |
| **B** | Countdown / IDR / AMS 深挖 | ✅ 完成 | ⏸ **无需重跑**（纯语料分析，不依赖凭据） | `aws-countdown-idr-ams-deep-dive-v2-2026-09-28.md` |
| **C** | 支持计划能力矩阵 | ❌ 未做（被登录卡死） | ✅ **首次真跑 + 14 维矩阵** | `_multiagent/workspace/aws-support-plans-v2/` |
| **D** | BA 业务架构（派生自 C） | ❌ 未做 | ⏳ **未开工**（C 已就绪，可派生） | — |

## 二、A 线核心结果（209 条）

工具面：**13 命名空间 / 407 op / 只读 200 / 元命令排除 14**；
`status` = ok 67 ｜ error 94 ｜ skip 47 ｜ timeout 1；**真触达 160/209 = 0.7656** ❌（U1 目标 ≥0.85）。

> 结论正文与完整缺陷清单见 [[aws-support-tooling-probe-v3-realrun]]，交付形态见 [[aws-support-tooling-probe-v3-deck-index]]。

## 三、C 线能力矩阵核心结果（首次真跑）

- **19 条 CLI 调用**（15 ok / 4 error），14 个维度判定：**supported 9 ｜ partial 3 ｜ unknown 2**。
- **22 条账号可观测事实**（`account_facts.md`）关键值：

| 事实 | 值 |
|---|---|
| 账户计划态 | `PAID` / `ACTIVE` |
| 支持服务目录 | **324** 个 |
| 支持语言 | **7** 种 |
| TA 检查项（新旧两条路径） | **639 / 639** |
| Health 事件 / 事件类型 | **13 / 2702** |
| Health 可见范围 | `eventScopeCode` 全部 `PUBLIC` |
| Service Quotas | 服务 **318**；EC2 配额 **1770**（可提升 **242**） |
| 历史案例 | **0** 条 |
| 支持渠道（CLI 侧） | web / chat / call **三种**（近 24h） |

- **5 条 gap**（无法用现有手段证实）：severity 可用级别、TA 摘要被 `UNKNOWN_CHECK_ID_ERROR` 挡住、
  Slack 集成是否已配置、**计划名（CHECK-C1）缺 CONSOLE 证据**、组织级能力（账号未加入 Organization）。
- **5 条缺陷**，其中 **P1 两条**：`cli_evidence/*.json` 在失败条目里被写入 stderr 文本（破坏「json=stdout」契约）、
  `raw_bytes=0` 与磁盘文件非空自相矛盾。

## 四、与 v1 逐项对账（11 个检查点）

| 结果 | 检查点 |
|---|---|
| ✅ **复现** | CHECK-1 / 2（`drs` / `devops-agent` 的「模型有、CLI 无」） |
| ✅ **首次真跑复现** | CHECK-3（`ssm list-documents` 恰好 114、无 NextToken）、CHECK-6（TA ARN region 段留空） |
| ✅ **首次双侧齐** | CHECK-4（新旧 TA 都 639；v1 当时只有一侧真跑） |
| ✅ **逐字复现** | CHECK-7（support 配额 `{"Quotas":[]}`） |
| ✅ **完全复现（含原文）** | CHECK-8（`wellarchitected` 11 个 `get-/list-agent-*` 报 400 `Unknown Operation`） |
| ✅ 同口径一致 | CHECK-9（命名空间规模 +11/+6 = `supportauthz`）、CHECK-10（负向 7 个） |
| ⚠️ **非推翻** | CHECK-5（TA 刷新冷却观测值 0，采样时点不同） |
| ❌ **未达标** | CHECK-11 / **U1**：0.366 → **0.7656**（目标 0.85） |

**总括**：**0 条 v1 断言被推翻**；4 条此前无法验证的运行期结论**首次被真跑证实**。

## 五、🔴 环境故障与独立性降级

| 项 | 状态 |
|---|---|
| `codex` 工具宿主 | ❌ `TOOL_HOST_BROKEN`（`os error 231`「所有管道实例都在使用中」），穷尽排查**未解决** |
| `dsh` 宿主 | ❌ 任何命令返回 `0xFFFF0000`（shell 启动失败） |
| 后果 | 编排层**既实现又审计**，**非**双 agent 交叉验证 |
| 补偿 | ① 真重跑 5 条抽样（B 项）② 用 **botocore 模型**作独立真值源交叉（D 项）③ A/C 两线两个独立进程数值互证（6/6 命中） |

## 六、下一步（当初列的三项，现状）

1. **A 线正式报告 v3** —— ✅ **已完成**（`aws-support-tooling-inventory-v3-2026-09-29.md`）。
2. **D 线（BA 业务架构 + 能力卡片）** —— ⏳ 仍未开工。
3. **U1 补达成** —— ⏳ 未做；对标做法是「把组织级 op 标注为账号态阻塞 + 另出排除阻塞后 0.976 的对照口径」。

## 相关

- [[aws-support-tooling-probe-v3-realrun]] — A 线 v3 结论正文
- [[aws-support-tooling-probe-v3-deck-index]] — A 线交付包索引
- [[aws-support-full-rerun-overview]] — 上一轮（09-28）总览
- [[aws-countdown-idr-ams-deep-dive-v2]] — B 线 v2 深挖
- [[competitive-analysis-aws-support-tooling]] — 同批的竞品分析（含六家工具面全景）
- [[aws-support-plans-33-capabilities]] — C 线的前身（33 项 × 四档，09-27 存档）
