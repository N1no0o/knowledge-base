---
title: AWS 支持工具能力普查 · 探测设计与契约（2026-09-27）
tags: [AWS, 支持服务, 能力探测, 多agent, 可证伪, 契约设计, 华为云支持服务立项]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/aws-support-plans/tooling-probe/INTERFACE.md（编排层写死的任务契约，2026-09-27）
status: growing
---

# AWS 支持工具能力普查 · 探测设计与契约

**一句话结论：这次探测把「某云厂商支持工具能不能用」做成了**可证伪**的工程题——办法是「一份契约 + 两路互相独立的服务清单真值源 + 每个操作原始响应全量落盘 + 支持单条重跑复核」，而不是让 agent 自报结果。**

## 一、目标：要「功能清单」，更要「真实调用结果」

- 既要 surface（有哪些操作），也要真实往返（能不能用、报什么错、返回什么结构、限流/配额特性）。
- 硬要求：**结论必须可证伪** —— 有原始响应落盘、可单条重跑、抽检不一致即判不合格。

## 二、环境与纪律（这部分是可复用的写法）

- **只读铁律**：禁写动词前缀（`create-/update-/delete-/put-/add-/remove-/register-/associate-/start-/stop-/cancel-/resolve-/enroll-/export-/request-/upgrade-/tag-/untag-/import-/subscribe-/refresh-`）；
- **禁计费 API**：`ce / cur / pricing / aws-marketplace / budgets`（**「只读」不等于「免费」**）；
- 单条命令超时 45s、整轮脚本墙钟 25 分钟；超时记 `status="timeout"`，重试不超过 1 次；
- **不得 mock / 硬编码**，`response_summary` 必须由真实 stdout 计算；
- 敏感凭据路径 `~/.aws/` 被文件策略层锁死 ⇒ 用 `AWS_CONFIG_FILE` + `AWS_LOGIN_CACHE_DIRECTORY` **重定向 I/O，不硬闯**。

## 三、核心设计：两路独立真值源 + 三份产出

| 产出 | 谁产出 | 真值来源 |
|---|---|---|
| `op_inventory.json` | 实现方 | `aws <ns> help` 的命令列表（CLI 自带，离线） |
| `probe_results.json` | 实现方 | 真实 `aws` 调用，**每个 op 的原始 stdout 全量落盘** `raw/<ns>__<op>.json`（error 落 `.err.txt`） |
| `independent_inventory.json` | 验证方 | **CLI 自带 botocore 服务模型** `...\awscli\botocore\data\<svc>\<ver>\service-2.json` |
| `defects.md` / `inventory_diff.md` | 验证方 | 按 A/B/C/D 四项审计 + 逐命名空间双向差异 |

⭐ **关键设计**：两路真值源**路径完全不同**（`aws help` 文本解析 vs botocore JSON 模型），
互为独立才能发现「解析层丢条目」这类实现缺陷。比对时统一小写去连字符
（`DescribeCases` ↔ `describe-cases`）。

**四项审计的定义（可复用的审计清单）**

| 项 | 判据 |
|---|---|
| A 真伪 | `latency_ms` 是否可疑地全同/为 0；`raw_file` 是否存在且非空；`response_summary` 与 raw 是否逐字段一致（抽 5 条） |
| B 可复现 | 用 `--only` 随机抽 5 条重跑，比对 `error_code` + `response_summary` |
| C 越界 | `argv` 里是否出现写动词或计费 namespace；`exclude_ops` 是否被违反 |
| D 面覆盖 | 两路清单**逐命名空间**比对 op 数，真实缺漏单列 |

⭐ **「没发现问题」也必须写**并附验证过的样本清单 —— **空报告和不报告无法区分**。

## 四、验收标准交由编排层独立执行

1. 五份产出齐全且可 `json.load`；
2. `stats.total` = 计划执行条数，`raw/` 文件数与 `results` 条数吻合；
3. **编排层自己**从 botocore 模型复算一遍 op 数（不采信验证方自述）；
4. 编排层随机抽 3 条重跑。

## 相关

- [[aws-support-tooling-probe-audit]] — 按本契约执行的 A/B/C/D 审计结果
- [[aws-support-tooling-probe-inventory-diff]] — 两路真值源的逐命名空间差异
- [[aws-support-tooling-probe-defects]] — 本次暴露的 21 条缺陷与修复判定
- [[aws-support-tooling-probe-param-fill]] — 补参重跑与真实可达性结论
- [[AWS支持服务工具-API实测报告]] — 同一账号更早的两轮直接 API 实测（2026-09-25/26）
