---
title: AWS 支持工具能力普查 · v3 真实调用轮结论
tags: [AWS, 支持服务, 工具面普查, 真实调用, 真触达率, 证据链, 华为云支持服务立项]
created: 2026-09-30
updated: 2026-09-30
source: D:/AI/my_project/deliverables/product-strategy/aws-support-tooling-inventory-v3-2026-09-29.md（真实调用轮，2026-09-29）
status: growing
---

# AWS 支持工具能力普查 · v3 真实调用轮结论

**一句话结论：v3 把 09-28 离线版里 6 项「本轮未做」全部补上，首次拿到真实 API 调用数据 —— 工具面 13 个命名空间 / 407 op / 200 只读、双真值源只差 2 个 op 且**无真实缺漏**；但真触达率实测 **0.7656**，**未达 U1 的 ≥0.85 目标**，且 160 条「真触达」里有 **64 条用的是合成参数** ⇒ 这是本轮唯一负面项，不许美化。**

## 一、v3 相对 v2 的增量

| 项 | v2（09-28 离线版） | **v3（真实调用轮）** |
|---|---|---|
| 工具面清单 13 ns / 407 op / 只读 200 | ✅ | ✅ 不变 |
| 双真值源对账（CLI 407 vs 模型 409） | ✅ | ✅ 不变 |
| **真实 API 调用** | ❌ 明确未做 | ✅ **209 条，落盘 422 个原始文件** |
| **真触达率 `actually_invoked_rate`** | ❌ 未知 | ✅ **0.7656**（160/209） |
| **服务端错误码分布** | ❌ 未知 | ✅ **17 种，最高 `AccessDeniedException` 24** |
| **A~F 审计的 B（可复现）** | ❌ 无对象可审 | ✅ **真重跑 5 条，5/5 一致** |
| **v1 的 4 条运行期断言** | ⚪ 无法验证 | ✅ **首次真跑证实，0 条被推翻** |

运行基线：墙钟 402.8 s（≈6.7 min）｜子进程启动 161 次｜单命令超时 30 s｜代理 `proxies_overridden=true`（剥离宿主注入的沙箱代理）。

## 二、三条要记住的结论

1. **工具面是干净的**：13 个命名空间、407 个 CLI op、200 个只读 op。CLI 侧与 botocore 模型侧**只差 2 个 op**
   （`drs/retry-data-replication`、`devops-agent/send-message`），全库**无真实缺漏**。
2. **真可达率 76.56%，未达 85% 目标**：未触达的 49 条里 **48 条是 `cli_param_validation`**（本地参数校验失败，
   请求根本没发出），**绝大多数是需要组织级 `--organization-id` 的 op** —— 属**账号态限制**，不是脚本缺陷。
   另有 🔴 **64 条「真触达」其实用的是合成参数**（假 ARN / 假 UUID），口径本身不严谨。
3. **v1 对账：0 条被推翻，4 条首次被证实**：`ssm list-documents` 恰好 114 且无 NextToken ✅、
   新旧 TA 都 639 ✅（v1 当时只有一侧真跑过）、`support` 配额 `{"Quotas": []}` ✅ 逐字一致、
   `wellarchitected` 11 个 `get-/list-agent-*` 全部报 `400 Unknown Operation` ✅（含错误原文）。

## 三、⚠️ 唯一负面项

> **U1 目标「真触达率 ≥ 85%」未达成**：实测 **0.7656**。
> 按宽松口径（排除账号态阻塞）为 160/(209−45) = **0.976**，但**那不是 U1 的原始定义** ⇒ **按原定义判：未达标**。

改善幅度确实大（v1 ≈0.366 → v3 0.7656，`cli_param_validation` 从 128 降到 48，↓63%），但**不得宣称达标**。

## 四、运行规模与错误码（首次拿到）

| 口径 | 值 |
|---|---|
| 总条数 | **209**（`op` 200 / `extra` 5 / `chain` 4） |
| `status` | ok **67** ｜ error **94** ｜ skip **47** ｜ timeout **1** |
| `actually_invoked` | **160 / 209 = 0.7656** ❌ |
| `by_error_class` | `service_error` 92 ｜ `cli_param_validation` 48 ｜ `cli_usage_error` 1 ｜ `timeout` 1 ｜ `ok` 67 |
| 落盘原始文件 | **422**（`raw/*.json` 211 + `raw/*.txt` 211）；`raw_file` 引用缺失 **0** |

服务端错误码 top（**产品含义是重点**）：

| 错误码 | 条数 | 产品含义 |
|---|---:|---|
| `AccessDeniedException` | 24 | 即使 root 也被拒 ⇒ 有独立权限模型或不支持该账号形态 |
| `UninitializedAccountException` | 15 | 服务在本账号未初始化 ⇒ 需先在控制台启用 |
| `OptInRequiredException` | 11 | 区域级 opt-in 未开 ⇒ 属**配置项**而非能力缺失 |
| `400 Unknown Operation` | 11 | 服务端未部署该 API（`wellarchitected` 的 11 个 `get-/list-agent-*`） |
| `ResourceNotFoundException` | 6 | 多为**合成参数**导致 ⇒ **不可当"不支持"的证据** |
| `NoAvailableOrganizationException` / `AWSOrganizationsNotInUseException` | 2 / 1 | 账号未加入 Organization ⇒ 组织级能力天然不可用 |

⇒ **`AccessDenied` + `UninitializedAccount` + `OptInRequired` + `NoAvailable*` ≈ 53 条**，
反映的是**账号态 / 权限态 / 区域配置**，**不是"该能力不存在"**。
做能力矩阵时这批必须归入 `unknown` 或「账号态阻塞」，**绝不能算作 `unsupported`**。

## 五、A~F 六项审计结论

| 项 | 结论 | 关键证据 |
|---|---|---|
| **A 真伪** | ✅ 未发现造假 | 抽 5 条把 `response_summary` 与 `raw_file` 逐字段核对 ⇒ 不一致 0；`raw_file` 缺失 0；真触达 latency min 1485.9 / p50 1597.3 / max 60075.9（无"全相同"）；47 条 latency=0 全是 skip |
| **B 可复现** | ✅ 5/5 一致 | `support/describe-severity-levels`、`support/describe-trusted-advisor-checks`、`trustedadvisor/list-organization-recommendations`（均 AccessDenied）、`health/describe-events`、`devops-agent/list-agent-spaces` |
| **C 越界** | ✅ 未发现越界 | 写动词 0；计费 ns（`ce`/`cur`/`pricing`/`aws-marketplace`/`budgets`）0；`help`/`wait`/`paginate` 当 op 0；`exclude_ops` 未出现 |
| **D 面覆盖** | ✅ 无真实缺漏 | CLI 407 vs 模型 409；归一化差集**仅模型 2 个 / 仅 CLI 0 个** |
| **E 空壳** | ⚠️ 真空壳 1 + 空集合 31 | 见下 |
| **F 补参真实性** | ✅ 8✅ / 0 造假 / 2 无法核 | 抽 10 个 chain 参数核对上游原始响应 |

**E 项判读纪律（易误用）**：
- **E-1 真空壳 1 条**：`support-app/get-account-alias`（`raw_bytes=0`、`response_summary=null`）。
  `exit_code=0` 但无任何返回 ⇒ **不能**作为"该 op 可用"的证据。
- **E-2 含空集合的 ok 条目 31 条**：API 确实被调用且返回 200，只是**该账号在该维度没有数据**。
  ⇒ 既**不能**当"能力已具备"的正面证据（`support-app` 两个 Slack list 返回 0 条 ⇏ "Slack 集成已开通"），
  也**不能**当失败。全库 ok 共 67 条，其中真正"无实质数据"（E-1∪E-2）**32 条**。

## 六、v1 逐项对账（11 个检查点）

> 纪律：**v2/v3 与 v1 不一致时不默认 v1 错**，每条都给裸命令 / 原始文件级依据。

| 检查点 | v1 断言 | v3 实测 | 判定 |
|---|---|---|---|
| CHECK-1 `drs/retry-data-replication` | 模型有、CLI 无 | 模型独有 `retrydatareplication` | ✅ 复现 |
| CHECK-2 `devops-agent/send-message` | 模型有、CLI 无 | 模型独有 `sendmessage` | ✅ 复现 |
| CHECK-3 `ssm list-documents` | 恰好 114、无 NextToken | **114、无 NextToken** | ✅ **首次真跑复现** |
| CHECK-4 新旧 TA 同量 | 639 / 639 | **639 / 639**（928,668 B / 1,241,494 B） | ✅ **首次双侧齐** |
| CHECK-5 TA 刷新冷却 ≈3599994 | ≈3599994 | **观测值 = 0** | ⚠️ 不一致但非推翻 |
| CHECK-6 `get-recommendation` 只受 region 留空 ARN | — | **真跑成功**，argv 即 `arn:aws:trustedadvisor::206482634625:recommendation/…` | ✅ 首次真跑复现 |
| CHECK-7 `support` 配额 | `{"Quotas":[]}` | **`{"Quotas": []}`** | ✅ **逐字复现** |
| CHECK-8 11 个 `get-/list-agent-*` 报 400 | 400 Unknown Operation | **11/11 `error 400`**，含错误原文 | ✅ **完全复现（含文案）** |
| CHECK-9 命名空间规模 | 396 / 194（12 ns） | 407 / 200（13 ns） | ✅ 同口径一致（差额 = `supportauthz` +11/+6） |
| CHECK-10 负向 6 个 + `supportauthz` | 6 个不存在；`supportauthz` 存在 | **7 个不存在**；`supportauthz` 存在（11 op / 只读 6） | ✅ 一致（且更强） |
| CHECK-11 / U1 本地校验错 128 ⇒ 应降个位数 | 128 | **48** | ⚠️ 改进但未达标 |

**CHECK-5 为什么不是"推翻"**：该字段语义是「距下次可刷新的剩余毫秒」。本轮取到 `status="none"`（该 check 从未刷新）
⇒ `0` 合理。v1 的 3599994 应是在**刚刷新完**的 check 上取到的 ⇒ **两轮采样时点不同**。
严格验证"1 小时冷却"需先手动 `refresh`（**写操作，只读纪律下未做**）。

**CHECK-6 的一个坑**：返回体里 `checkArn = arn:aws:trustedadvisor:::check/7DAFEmoDos`（region 与账号都空，三冒号），
而请求用的 `recommendation` ARN 含账号 —— **两种 ARN 形态不同**（见 D-7）。

## 七、缺陷清单：P0 0 ｜ P1 3 ｜ P2 5

| 编号 | 级别 | 一句话 | 影响面 |
|---|---|---|---|
| **D-1** | **P1** | 「真触达」里 **64 条用的是合成参数**（`suffix_rule` 79 个全合成）⇒ 成功率虚高、U1 口径不严谨 | 指标口径 |
| **D-2** | **P1** | **21 条**参数带 `OFFLINE_PLACEHOLDER_REQUIRES_REVIEW` 未收敛（全部 `skip`、未发请求，这点是诚实的） | 覆盖面 |
| **D-3** | **P1** | **U1 目标（≥0.85）未达成**，实测 0.7656 | 目标达成 |
| D-4 | P2 | `support-app/get-account-alias` 是真空壳；另有 31 条空集合需同规则标注 | 数据质量 |
| D-5 | P2 | `probe_targets.json` 的 `supportauthz` chain 引用了**不存在的 op**（`get-support-permit-request` 应为 `get-support-permit`）—— **v1 已指出，v2/v3 输入文件未修** | 交接风险 |
| D-6 | P2 | `trustedadvisor/recommendation-detail` chain 的 `extract` 提示写错（`recommendations` → `recommendationSummaries`），靠**运行时自动纠正**才跑通 | 契约一致性 |
| D-7 | P2 | `check` 与 `recommendation` 两种 ARN 形态极易混用，需下轮统一 | 解析规则 |
| D-8 | P2 | **环境缺陷**：两个 worker 均无法执行 ⇒ 本轮降级为编排层亲做 | 独立性 |

**D-1 细节（本轮最值得重视）**：`actually_invoked=true` 且 `synthetic=true` 的条目 **64 条**（占 160 条真触达的 **40%**）。
触发参数按名计：`--profile-arn`×10、`--resource-arn`×9、`--case-id`×6、`--asset-id`×5、`--template-arn`×5、`--question-id`×4、
`--attachment-id`×3 …… 共 44 个参数名。合成值形态如
`{"--attachment-id": {"value": "00000000-0000-0000-0000-000000000001", "source": "suffix_rule", "synthetic": true}}`。
这 64 条的错误码：`AccessDeniedException` 20 / `400` 10 / `ResourceNotFoundException` 6 / `BadRequestException` 6 /
`UninitializedAccountException` 6 / 其它 16。
⇒ 请求确实发出去了，但**参数是假的**，拿到的错误**不能反映真实能力边界**。
**建议**：把指标拆成 `request_sent_rate`（现 0.7656）与 `meaningful_response_rate`（排除 `synthetic=true` 后重算）；
对 `suffix_rule` 合成值产生的 `AccessDenied`/`ResourceNotFound`，在矩阵里**一律降级为 `unknown`**。

**「未发现」类**：N-1 未发现越界（209 条 argv 逐条扫描，写动词 0 / 计费 ns 0 / 元命令 0）；
N-2 未发现响应造假（抽 5 条逐字段核对 0 处不符；B 项重跑 5/5 一致）。

## 八、🔴 独立性降级（先声明，不含糊）

`codex` 工具宿主本轮故障（`os error 231`「所有管道实例都在使用中」，穷尽排查未解决）、
`dsh` 宿主 shell 启动失败（`0xFFFF0000`）⇒ **两个 worker 都无法执行命令**。
本轮所有脚本与审计**均由编排层亲做** ⇒ **不是双 agent 交叉验证**，**不得声称有**。

补偿手段：① B 项**真重跑** 5 条抽样（5/5 复现，外部校验）；② D 项用 **botocore `service-2.json`** 作独立真值源交叉（差集仅 2 个）；
③ A/C 两线**两个独立进程**数值互证 6/6 命中。

## 九、明确不做的边界（诚实清单）

| 未做项 | 原因 |
|---|---|
| CHECK-5 的「1 小时冷却」严格验证 | 需先 `refresh-trusted-advisor-check`（**写语义，已被 `exclude_ops` 排除**）⇒ 只读纪律下记 `UNVERIFIABLE_READONLY` |
| CHECK-11 的 U1 补达成 | 组织级 op 需真实 `--organization-id`，本账号未加入 Organization |
| `meaningful_response_rate` 口径重算 | 建议项，待下轮按 D-1 拆分指标后产出 |
| 控制台能力矩阵 / BA 业务架构 | 见 C 线（`aws-support-plans-v2/`）与 D 线（未开工） |

## 相关

- [[aws-support-tooling-probe-v3-deck-index]] — 本报告的交付包与支撑件清单（原件路径 / 体积）
- [[aws-support-tooling-probe-audit]] — v1 轮 A/B/C/D 审计（B 项当时未执行，本轮首次补上）
- [[aws-support-tooling-probe-inventory-diff]] — 双真值源逐命名空间差异（D 项底稿）
- [[aws-support-tooling-probe-defects]] — v1/v2 两轮缺陷清单（与本轮 D-1…D-8 按轮次区分）
- [[aws-support-tooling-probe-param-fill]] — 补参可达性（F 项对应）
- [[华为云支持服务立项-AWS竞品对标]] — 上述结论在立项中的用途
