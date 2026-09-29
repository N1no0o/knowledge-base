---
title: AWS 支持服务全套重做 · 09-28 总览（凭据卡死轮次）
tags: [AWS, 支持服务, 多agent, 新模型对照, aws-login, 进度总览, 华为云支持服务立项]
created: 2026-09-30
updated: 2026-09-30
source: deliverables/product-strategy/aws-support-full-rerun-overview-2026-09-28.md（4.7 KB）｜原件 D:/AI/my_project/deliverables/product-strategy/
status: growing
---

# AWS 支持服务全套重做 · 09-28 总览（凭据卡死轮次）

**一句话结论：用新模型（gpt-6-astra）把 AWS 支持服务全套 4 条线重做，**2 条跑通、2 条被 AWS 凭据卡死**；跑通的两条各抓到 v1 一个真实错误 —— 而卡死不是方法问题，是凭据彻底失效 + 交互式登录撞上 AWS 风控（CAPTCHA / Bad request），且**明确拒绝自动破解 CAPTCHA**。**

## 一、交付现状

| 线 | 内容 | 状态 | 交付件 |
|---|---|---|---|
| **A** | 工具面普查 | 🟡 **部分**（离线子集 ✅ / 真实调用 ❌ 被凭据卡死） | `aws-support-tooling-inventory-v2-2026-09-28.md` / `.html` |
| **B** | Countdown / IDR / AMS 深挖 | ✅ **完成** | `aws-countdown-idr-ams-deep-dive-v2-2026-09-28.md` / `.html` |
| **C** | 支持计划 33 项能力矩阵 | ❌ 未做（需控制台登录态 + 真实调用） | 沿用 09-26 存档 |
| **D** | BA 业务架构 + 33 张能力卡片 | ❌ 未做（派生自 C） | 沿用 09-26 存档 |

> 后续发展：A / C 两条线在 **09-29** 凭据恢复后真跑补齐，见 [[aws-support-real-run-overview]]。

## 二、本轮抓到的两个 v1 真实错误（"对比旧版"的核心产出）

### 1. B 线：三份报告里 **t3（AMS）保留了 v1 的绝对化表述**，另两份已撤回

同一份负向证据（S5 的负向观察），`t1` 与 `t2` 都明确写「『没有任何公开 API』**超出该负向证据的穷尽能力**，
本轮撤回 v1 的绝对化表达」，**只有 t3 保留并给了 `●`**。
⇒ **对外引用一律采信收窄版**：「在本轮检查范围内未发现专属公开 API/CLI 面」。

### 2. A 线：**v1 已发布报告的"只读"列有 4 处错值，且该列加总 188 ≠ 报告自己写的合计 194**

| 命名空间 | v1 报告正文 | 实际（v1 原始 json） |
|---|---:|---:|
| `wellarchitected` | 43 | **44** |
| `service-quotas` | 9 | **14** |
| `ssm-incidents` | 12 | **13** |
| `freetier` | 5 | **4** |
| 加总 | **188（≠194）** | **194 ✅** |

⇒ **错在 v1 报告的正文转写，原始数据一直是对的**。v1 报告 §2.1 该列不要直接对外引用；总数 396 / 194 没错。

## 三、质量对照：新模型带来了什么

| | v1（旧模型） | **v2（新模型）** |
|---|---|---|
| 三份报告评级 | B / B / **C** | **A / A / B** |
| 缺陷总数 | 21（**P0 3** / P1 6 / P2 12） | 18（**P0 0** / P1 4 / P2 14） |
| 最显著的行为变化 | — | **主动降低断言强度**：撤回绝对化表述、同页重复引用从 `●` 降 `◐`、不再给官方口径补造适用条件 |
| 差异标注可对质性 | — | 逐条把「与 v1 的差异清单」拿去 v1 原文对质，**未发现一处伪造差异** |

⚠️ **但 v2 也不是没问题**：18 条缺陷里 4 条 P1，其中 `t3` 的**置信点失控（单来源给 `●` 共 29 处）**是系统性问题。
⇒ **采信 v2 的结论，但要采信"收窄版"，并且不要引用 t3 的 `●`。** 详见 [[aws-countdown-idr-ams-deep-dive-v2]]。

## 四、工程侧产出

- **工作区**：`_multiagent/workspace/aws-cdp-idr-ams-v2/`、`_multiagent/workspace/aws-support-tools-v2/`
- **运行记录**：`_multiagent/runs/aws-cdp-idr-ams-v2-01/`（4 任务全 `ok`，19 分钟）、
  `_multiagent/runs/aws-support-tools-v2-offline-01/`（3 任务全 `ok`，15m54s）
- **新技能**：`aws-cli-login-automation`（本轮排障沉淀：新 AWS 体验 `aws login` 自动化、域名硬闸、
  四个必踩的坑、`--remote` 兜底）
- **新脚本**：`_browser/aws_login3.js`（状态机版登录驱动）、`_multiagent/build_*_v2_report.py`（交付件汇编）

## 五、🔴 被卡死的部分与解除条件

**症状**：`aws sts get-caller-identity` → `Your session has expired`（两个路径都试过）；
登录缓存里的 `refreshToken` 已失效 ⇒ 必须交互式 `aws login`；
自动化已能走到「经典 root 邮箱页」（`#resolving_input` 已填好邮箱），但：
- 触发 **CAPTCHA**（"Type the characters as shown above"）
- 换全新 profile 后转成 **`Bad request — Clear your cookies`**

**明确不做的事**：**不自动识别/破解 CAPTCHA** —— 那是绕过 AWS 明确部署的机器人防护。

**解除条件（二选一，约 30 秒人工动作）**：

1. 人工解一次 CAPTCHA（自动化已备好、浏览器停在那一页）；
2. `aws login --remote` —— 生成授权链接 + 配对码，手机打开批准。

**解除后可直接执行**：`_multiagent/workspace/aws-support-tools-v2/probe_plan.md`（已写死到命令级）+
`manifests/aws-support-tools-v2-01.json`（A 线真实调用两轮）。

## 相关

- [[aws-support-real-run-overview]] — 下一轮（09-29）真实调用总览，A / C 已补齐
- [[aws-countdown-idr-ams-deep-dive-v2]] — B 线 v2 深挖正文
- [[aws-support-tooling-probe-v3-deck-index]] — A 线交付包索引（含 v2 离线版登记）
- [[AWS支持服务工具-API实测报告]] — 09-25/26 最早两轮实测
