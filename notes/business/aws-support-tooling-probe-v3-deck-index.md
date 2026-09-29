---
title: AWS 支持工具能力普查 v3 · 交付包与支撑件索引
tags: [AWS, 支持服务, 交付包索引, 证据链, 本地原件, 华为云支持服务立项]
created: 2026-09-30
updated: 2026-09-30
source: D:/AI/my_project/deliverables/product-strategy/aws-support-tooling-inventory-v3-2026-09-29.{md,html} + _multiagent/workspace/aws-support-tools-v2/（2026-09-29）
status: growing
---

# AWS 支持工具能力普查 v3 · 交付包与支撑件索引

**一句话结论：v3 真实调用轮交付件 = 1 份 HTML 报告（48.5 KB）+ 1 份同名 Markdown（24.1 KB），支撑件为工作区 `aws-support-tools-v2/` 内的 5 份分析文档 + 209 条调用记录 + 422 个原始响应文件；全部为本地原件，大二进制与原始响应**不进 Git**。**

## 一、交付件（本地绝对路径）

| 文件 | 体积 | 生成时间 |
|---|---:|---|
| `D:/AI/my_project/deliverables/product-strategy/aws-support-tooling-inventory-v3-2026-09-29.html` | 48,498 B | 2026-09-29 22:40 |
| `D:/AI/my_project/deliverables/product-strategy/aws-support-tooling-inventory-v3-2026-09-29.md` | 24,149 B | 2026-09-29 22:40 |

> `.html` 是渲染呈现版（人读），`.md` 是同源文本版（机读 / 归档）。
> **结论摘要已编译为** [[aws-support-tooling-probe-v3-realrun]]，本页只登记交付形态与原件位置。

## 二、被取代版本（不单独成页，只登记）

| 版本 | 文件 | 说明 |
|---|---|---|
| v2（09-28 离线版） | `aws-support-tooling-inventory-v2-2026-09-28.md`（70.6 KB）/ `.html`（119.2 KB） | ⛔ **已被 v3 取代** —— 因 AWS CLI 凭据失效，明确标注 6 项「本轮未做」 |
| v1（09-27） | 报告正文在 `dist/aws-support-plans/tooling-probe/` | 已被 v2/v3 取代；v1 报告正文有 4 处只读列转写错误，见下 |

> ⚠️ **v1 报告正文的转写错误**（不是原始数据错）：`wellarchitected` 43（实 44）、`service-quotas` 9（实 14）、
> `ssm-incidents` 12（实 13）、`freetier` 5（实 4）；加总 188 但报告自己写 194。
> ⇒ **v1 报告 §2.1 的"只读"列不要直接对外引用**；总数 396 / 194 是对的。

## 三、支撑件（工作区 `_multiagent/workspace/aws-support-tools-v2/`）

| 文件 | 内容 | 状态 |
|---|---|---|
| `probe_results.json` | 209 条真实调用记录（468 KB） | ✅ 本轮已入库 |
| `raw/` | 422 个原始文件（211 `.json` 响应 + 211 `.txt` 错误/skip） | ✅ 本轮已入库 |
| `op_inventory.json` | 工具面清单（CLI 侧，407 op） | ✅ 本轮已入库 |
| `independent_inventory.json` | 工具面清单（botocore 模型侧，409 op） | ✅ 本轮已入库 |
| `param_values.json` | 取值计划（200 只读 op） | 未单独入库 |
| `probe_audit.md` | A~F 六项审计（9.2 KB） | ✅ 本轮已入库 |
| `inventory_diff.md` | CLI vs 模型双向差异（11.1 KB） | ✅ 本轮已入库 |
| `v1_delta.md` | v1 逐项对账 11 个检查点（11.1 KB） | ✅ 本轮已入库 |
| `defects.md` | 缺陷报告 P0 0 / P1 3 / P2 5（11.1 KB） | ✅ 本轮已入库 |
| `t3_audit.py` | 审计脚本（可复现） | 脚本，不入库 |
| `_verify_tmp/` | B 项重跑原始输出（主 `probe_results.json` 未被覆盖） | 中间产物，不入库 |

> **上表 "本轮已入库" 表示该源件已由 `kb_scan.py` 记账到本索引页**；
> 其中 `inventory_diff.md` 另有一篇 v1 轮的既有结论笔记 [[aws-support-tooling-probe-inventory-diff]]、`probe_audit.md` 有 [[aws-support-tooling-probe-audit]]，
> 那两篇是 **09-27 v1 轮**的版本（内容与 v3 轮不同），按轮次分别保留。

## 四、⭐ 一句话复现

```powershell
$PY = "C:\Users\lichangzhao\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$WS = "D:\AI\my_project\_multiagent\workspace\aws-support-tools-v2"
& $PY "$WS\t3_audit.py"      # 重算 A~F 六项
& $PY "$WS\probe_runner.py" --only "health/describe-events" --out "$WS\_verify_tmp\one.json"   # 单条重跑
```

## 相关

- [[aws-support-tooling-probe-v3-realrun]] — 本交付包对应的结论正文（13 ns / 407 op / 真触达率 0.7656 / D-1…D-8）
- [[aws-support-tooling-probe-audit]] — v1 轮 A/B/C/D 审计（B 项首次补上）
- [[aws-support-tooling-probe-inventory-diff]] — v1 轮双真值源差异底稿
- [[华为云支持服务立项-AWS竞品对标]] — 该交付包在立项材料中的引用位置
