---
title: AWS 支持工具能力普查 · A/B/C/D 交叉审计结论
tags: [AWS, 支持服务, 交叉审计, 可证伪, 反造假, 多agent, 华为云支持服务立项]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/aws-support-plans/tooling-probe/probe_audit.md（独立验证方产出，2026-09-27）
status: growing
---

# AWS 支持工具能力普查 · A/B/C/D 交叉审计结论

**一句话结论：A（真伪）未发现伪造、C（越界）0 越界、D（面覆盖）抓出 2 个真实缺漏，但 B（可复现）因宿主 shell 崩溃而**根本没执行**——本轮验收的「可证伪」前提未完全成立，这一点被审计方自己披露而非掩盖。**

## 一、A 真伪审计：未发现造假（四项硬证据）

| 证据 | 数值 |
|---|---|
| `latency_ms` 分布 | 202 条中 **100 个不同取值**，min 495ms / max 90066ms，**0 条为 0 或缺失** |
| ⭐ 墙钟交叉验证 | 202 条 latency 之和 ≈ **413.8s**，两产出文件 `generated_at` 间隔 **430s** ⇒ **96.2% 被解释**（差额 ≈16s = 落盘 + 进程启动开销）。**要伪造就得让随机 latency 之和精确落进观测时间窗，极难。** |
| `raw_file` | 202/202 存在且非空，字节数与 `raw_bytes` **逐条吻合**；`error/timeout` 一律 `.err.txt`、`ok` 一律 `.json` |
| 逐字节复算 | `raw/support__describe-cases.json` = 23 B = `raw_bytes`；`...describe-attachment.err.txt` 123 + 2×CRLF = 127 B = `raw_bytes` |

**附加反造假信号**（伪造者容易露馅处）：

- **latency 双峰且符合语义**：`ParamValidation`（CLI 本地校验失败、未出网）集中在 **495–570ms**，
  真实 API 往返集中在 **1300–2900ms**。伪造者通常只会铺一个均匀分布。
- **非字母序的真实字段序**：`iam/account-summary` 的 `SummaryMap` key 顺序与 raw 一致（非字母序）。
- 统计自洽：`total 202 = ok 40 + error 159 + timeout 1 + skip 2`。

## 二、B 可复现审计：**未执行**（宿主限制，诚实披露）

- 计划：`--only` 随机抽 5 条重跑。**实际执行 0 条。**
- 原因：本会话（及派生 subagent）**无法执行任何外部命令** —— `pwsh` 在 CLR 初始化阶段即失败，
  `exit code 4294901760`（= `0xFFFF0000`），stderr 字节级相同可复现；沙箱升级被 fail-closed 拒绝：
  `sandbox escalation ... requires approval, but no approval channel is available`。
- ⇒ **不能声称「前后一致」**；任何声称跑过重跑的结论都是假的。
- 静态审查另发现真实缺陷：2 条 `status="ok"` 的 `latency_ms` 超过契约 45s 上限（46961 / 46581ms），
  唯一自洽解释 = **第 1 次 45s 超时被静默吞掉、第 2 次成功** ⇒ 计时语义失真（见 [[aws-support-tooling-probe-defects]]）。

⚠️ **不可复现 id 的三类**（复核时按 `skip_reason` 豁免，别误判造假）：
随账号状态变化的（`iam/account-summary`）、时间窗参数导致数据会变的（`support/describe-cases`）、
依赖上一步取值的 chain。

## 三、C 越界审计：未越界

- 计费 namespace **0 命中**、22 个写动词前缀 **0 命中**、`exclude_ops` **0 命中**。
- 202 条 `namespace` 全在允许集合内（12 个正向 + `extras` 的 `ssm/organizations/iam`）。
- 实现侧另有 `validate_argv()` 四重校验构成第二道闸。

## 四、D 面覆盖审计：真实缺漏 2 个 + 1 个伪影

| 判定 | 条目 |
|---|---|
| **真实缺漏** | `devops-agent/send-message`、`drs/retry-data-replication` |
| CLI 侧伪影 | `ssm-incidents/wait`（等待器元命令被当成操作） |
| 一致 | 其余 9 个正向命名空间 + 5 个负向命名空间 |
| 文件不自洽 | `trust` 行（文件写 0，按其生成器算法应为 12） |

⭐ **§5.3 的计数陷阱（最值钱的一条）**：总数 **CLI 397 vs 模型 398 只差 1**，看似「基本对得上」，
真实构成是 **CLI 缺 2 个（被漏的真实操作）+ 多 1 个（`wait` 伪影）⇒ 净 −1**。
**两个真实缺漏被一个伪影互相抵消了。** ⇒ **不要用总数做验收判据，必须逐命名空间比对。**
排除 `wait` 后正确口径：**CLI 396 vs 模型 398，差 2**。

**验证方的方法论亮点**：不采信 `independent_inventory.json` 的自述（它自述生成器没跑过），
而是**直接读它声明的 botocore 模型文件逐个数**复核，得 `devops-agent=63 / drs=70 / ssm-incidents=31`，与文件记录吻合
⇒ 判定「**内容准确，仅 provenance 不可机器复现**」。

## 五、门禁与纪律

- 只读、零费用：全程无写动词、无计费 API。
- `probe_audit.py` 在本会话**没有被执行过**；A/C/D 的数值证据系逐文件手算（报告中已声明）。
- **正确做法**：在能启动 shell 的宿主上跑
  `python probe_audit.py --mode all --samples 5 --seed 20260927` 补 B 项；
  并在验收流程加**前置 `echo` 探活自检**，失败则整轮标记「环境不可用」——避免把「跑不了」误判成「跑过了没问题」。

## 相关

- [[aws-support-tooling-probe-design]] — 本审计所依据的契约与审计项定义
- [[aws-support-tooling-probe-inventory-diff]] — D 项差异的完整逐命名空间表
- [[aws-support-tooling-probe-defects]] — 两轮缺陷清单与修复判定
- [[华为云支持服务立项-AWS竞品对标]] — 上述结论在立项中的用途
