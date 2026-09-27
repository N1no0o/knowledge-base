---
title: AWS 支持工具能力普查 · 两路真值源逐命名空间差异
tags: [AWS, 支持服务, 面覆盖, botocore, 命名空间, 计数陷阱, 华为云支持服务立项]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/aws-support-plans/tooling-probe/inventory_diff.md（独立验证方产出，2026-09-27）
status: growing
---

# AWS 支持工具能力普查 · 两路真值源逐命名空间差异

**一句话结论：CLI 侧（`aws <ns> help`）与模型侧（botocore `service-2.json`）逐命名空间比对，12 个正向命名空间里 9 个一致、2 个有真实缺漏（`devops-agent/send-message`、`drs/retry-data-replication`），第 12 个（`ssm-incidents`）的差异是 CLI 伪影；总数「只差 1」是假象。**

## 一、归一化规则

```
norm(name) = re.sub(r"-+", "", name).lower()     # DescribeCases ↔ describe-cases → describecases
```

服务目录名一并归一化。**本次 12 个正向命名空间全部命中「精确目录名」，没用到任何别名回退** ⇒
不存在「CLI 服务名与 botocore 目录名不同」的历史坑。

## 二、主表（对比结论）

| 命名空间 | CLI 侧 | 模型侧 | 归一化差集 | 判定 |
|---|---:|---:|---|---|
| support | 20 | 20 | ∅ | 一致 |
| trustedadvisor | 12 | 12 | ∅ | 一致 |
| support-app | 10 | 10 | ∅ | 一致 |
| health | 14 | 14 | ∅ | 一致 |
| **devops-agent** | **62** | **63** | 仅模型：`SendMessage` | **真实缺漏** |
| security-ir | 24 | 24 | ∅ | 一致 |
| compute-optimizer | 28 | 28 | ∅ | 一致 |
| wellarchitected | 95 | 95 | ∅ | 一致 |
| **drs** | **69** | **70** | 仅模型：`RetryDataReplication` | **真实缺漏** |
| ssm-incidents | 32（排除 `wait` 后 31） | 31 | 仅 CLI：`wait`（元命令伪影） | 一致 |
| freetier | 5 | 5 | ∅ | 一致 |
| service-quotas | 26 | 26 | ∅ | 一致 |
| 6 个负向命名空间 | 0 | 0 | ∅ | 一致（`trust` 例外） |
| **合计** | **397**（排除 `wait` 后 **396**） | **398** | 缺 2 / 多 1 | — |

- **「仅命名差异」= 0 对**：本次归一化规则没有被命名风格差异占用，差异都是实质的。
- CLI 侧有 `retry-recovery-plan-execution-step`，但**没有** `retry-data-replication` ⇒ `drs` 的缺漏**不是**命名/前缀问题。
- **无法进一步归因**（是 `aws <ns> help` 真没列，还是解析器丢条目）：本会话 shell 不可用，跑不了
  `aws drs help` / `aws devops-agent help`。

## 三、⭐ 计数陷阱：397 vs 398 是「缺 2 多 1」

```
CLI 侧缺 2 个（send-message, retry-data-replication）
CLI 侧多 1 个（wait 元命令）
净差 = −1     ← 两个真实缺漏被一个伪影互相抵消
```

⇒ **只看总数会漏报**。正确口径 = 排除元命令后 **CLI 396 vs 模型 398，差 2**，且必须逐命名空间列出。

## 四、`wait` 为什么必须排除（三条独立理由）

1. **结构上它就不是操作**：botocore 把 waiter 定义在 `waiters-2.json`，不在 `service-2.json` 的
   `operations` 里 ⇒ 它**必然**出现在差集中，但不是被漏掉的服务操作。
2. **参数结构为空且全库唯一**：`params_total/params_required/params` 三者全 `null`，
   全库 397 个条目里**只有这一条**是 null（没有 Synopsis）。
   **「唯一一个解析不出参数的命令」本身就是它不是普通操作的证据。**
3. **同一段列表里 `help` 已被显式排除、`wait` 被漏掉** ⇒ 实现侧清单不完整，不是数据真伪问题。

排除后 `ssm-incidents` = 31 = 模型侧 31 ⇒ 一致。影响面仅 1 个命名空间 +1 计数（`wait` 不匹配 `include_prefixes`，未污染探测结果）。

## 五、`trust` 行：唯一「文件不自洽」条目

- 文件写 `model_dir: null / operation_count: 0`，`note` 列候选名 `[trust, trustedadvisor, trusted-advisor]`；
- 但生成器的 `ALIASES["trust"] = ["trustedadvisor", "trusted-advisor"]`，而 `trustedadvisor/2022-09-15/service-2.json` **确实存在**（12 个操作）
  ⇒ 按算法 `resolve("trust")` **必然命中**、返回 12。
- **两种互斥判定**：按文件字面 = 一致；按生成器算法 = 模型侧未收录。
- **结论**：判为「文件不自洽（需修脚本或修文件）」，**不计入真实缺漏**（`trust` 是负向命名空间，
  且 `trustedadvisor` 已单列、两侧都是 12，无实际覆盖缺口）。
  ⚠️ 但**重跑会让 totals 从 12/398 变成 13/410**，直接冲击「编排层复算对得上」这条验收。

## 相关

- [[aws-support-tooling-probe-design]] — 两路真值源的契约出处
- [[aws-support-tooling-probe-audit]] — D 项审计的完整结论
- [[aws-support-tooling-probe-defects]] — 本次缺漏被登记为 P1 缺陷并追踪修复
