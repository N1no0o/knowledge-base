---
title: AWS 支持工具能力普查 · 两轮缺陷审计与修复判定（D-1…D-22）
tags: [AWS, 支持服务, 缺陷审计, 交叉审计, 多agent, 复盘, 华为云支持服务立项]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/aws-support-plans/tooling-probe/defects.md + defects2.md（独立验证方两轮产出，2026-09-27）
status: growing
---

# AWS 支持工具能力普查 · 两轮缺陷审计与修复判定

**一句话结论：独立验证方两轮共登记 22 条缺陷（第一轮 D-1…D-12，第二轮 D-13…D-22），第二轮对第一轮逐项复审、**撤回 1 条误判**、确认 4 项修好；真正卡住验收的是 P0 的「宿主无法执行任何命令」，而最容易被下游误用的是「20 条可用 op 里有 10 条没有实质数据」。**

## 一、第二轮修复判定（F1–F8）

| 项 | 判定 | 依据 |
|---|---|---|
| F1 `ssm-incidents`=31、`wait` 消失、totals 重算 | ✅ 已修好 | 计数逐项相加自洽（396 / 只读 194），旧 `wait` 条目已 0 命中；解析器死循环已删 |
| F2 4 条零信息量 op | ⚠️ **3/4 有证据** | 3 条已转 `service_error`；`health/describe-entity-aggregates` 因 `params_required=0` **根本不在重跑集合里** ⇒ 无新产物 |
| F3 两条 chain 不再是 skip | ⚠️ 代码正确、**运行时证据缺失** | 兼容映射逻辑正确且上游 raw 确有目标键，但**工作区找不到任何重跑产物** |
| F4 `error_class` 全覆盖 + 取值域封闭 | ✅ 已修好 | `by_error_class` 5 项合计 = 130 = total（越域值会被静默丢弃 ⇒ 反证全覆盖）；`actually_invoked` 与分类**逐类精确相等** |
| F5 `attempts` / `exceeded_timeout_budget` | ✅ 已修好 | 130 条全覆盖，10 条 true 全部 `attempts=2` 且状态如实（含 1 条 `ok` 仍显式标注），**无粉饰** |
| F6 `--only` 落原始输出 | ⚠️ 静态正确、产物不存在 | 代码有防覆盖守卫；但声称的验证产物**磁盘上不存在** ⇒ 断言无凭据（D-14） |
| F7 `stats2` 自洽 / `raw2` 计数 | ✅ 通过 | 状态/分类/调用/尝试/超时/错误码六组分解全部加总吻合；`raw2/` 20 json + 110 err = 130 与状态严格对应 |
| F8 `independent_inventory` totals + `trust` | ✅ 已修好 | totals = 12/398；`trust` 候选名只剩 `[trust]` ⇒ NOT FOUND；游离的 `provenance_caveat` 键已消失 |

**未修**：`drs/retry-data-replication`、`devops-agent/send-message` 两个真实缺漏本轮不在修复范围，仍然存在。

## 二、按主题归类（比按编号读更有用）

### ① 执行环境（P0，唯一一条）—— D-1
本宿主**无法执行任何外部命令**：`pwsh` CLR 初始化失败（`exit 0xFFFF0000`），沙箱升级 fail-closed 拒绝。
⇒ B 项复现审计、`probe_audit.py` 实跑、`independent_inventory.py` 重跑**全部不可执行**，
    整套「可证伪」设计里最关键的一环失效。**建议加前置 `echo` 探活自检**，避免把「跑不了」误判成「跑过了没问题」。

### ② 清单解析（已修）—— D-2 / D-11
`wait` 元命令未被过滤 + `parse_available_commands()` 有一段**死代码**（第一个循环从不 append）、
实际按全文本逐行匹配 ⇒ 范围过宽可致假阳性。修法：`META_COMMANDS = {"help","wait","paginate"}` + 限定在 `Available Commands` 段内。
（注：`paginate` 并非 CLI 元命令，属**对建议清单的过度照抄**，无害但说明黑名单没跟真实 help 校对过。）

### ③ 真实缺漏（未修）—— D-3 / D-4
`drs` 缺 `retry-data-replication`、`devops-agent` 缺 `send-message`；
与 `wait` 伪影抵消成「总数只差 1」，**只看 totals 会漏报**（详见 [[aws-support-tooling-probe-inventory-diff]]）。

### ④ 计时语义（只修了一半）—— D-5 → D-18
`latency_ms` 的计时器**在重试循环之前**起算 ⇒ 成功条目也可能 >45s（46961/46581ms），
即**首次超时被静默吞掉**、字段变成「两次尝试之和」。
第二轮已算出 `attempt_latencies_ms` 却**从未拷贝进结果** ⇒ 字段本身依旧失真。

### ⑤ chain 补参的「真值」没打中 —— D-15 / D-16 / D-17
- **取错字段**：`--recommendation-identifier` 的 `path:"AUTO"` 启发式选了 `id`，
  而上游同一对象里就有服务端要求的 `arn` ⇒ 直接被正则拒绝，「补参」零收获。
- **规格未实现**：`param_values.json` 里为 `--quota-code` 声明的 `service_code`、为
  `--recommendation-identifier` 声明的 `max_results`，**实现从未读取** ⇒ 4 条 quota op 全落 fallback。
- **标签不可证伪**：11 条 `--lens-alias` 标 `source:"chain"`，但填入值与 fallback **字面完全相同**，
  且声明 `path` 指向不存在的键、靠未声明的模糊 BFS 兜住 ⇒ 审计者无法区分真 chain 与降级。
- ⭐ 反面证据（说明降级路径是活的）：`--profile-arn` 与 `--quota-code` 在取不到值时**如实标 fallback**，
  35 条 chain 里 22 条可用「值不同于 fallback 且逐字命中上游 raw」独立证实为真值 ⇒ **未发现用 fallback 冒充 chain 的造假**。

### ⑥ 结论口径被高估 —— D-19 / D-21
- `param_fill_report` 的「真正可用 op 共 20 条」里，**8 条纯空壳 + 2 条半空/伪成功**（其中
  `health/describe-event-details` 是 CLI exit 0 但 API 逐项返回 `EventNotFoundError` 的**伪成功**）
  ⇒ 真正拿到实质数据的只有约 **10 条**，高估约一倍。
- timeout 条目落了一个 **0 字节 raw 文件**：「存在但为空」恰好卡在真伪判据边界
  （机械查 exists 通过、人工查非空失败）。

### ⑦ 交付物与 schema 治理 —— D-13（P1）/ D-14 / D-20 / D-22
- **主交付物分叉**：`probe_results.json` 未随本轮修复重跑，仍是旧时间戳、无
  `error_class/attempts/param_fill`、仍含 4 条 `ExitCode252` 与 2 条 chain skip；
  而验收口径认的就是这份文件 ⇒ **修复在验收口径下等于全部未生效**。二选一：重跑覆盖，或显式声明由 `probe_results2.json` 取代。
- `--only` 产物不在工作区 ⇒ F3/F6 的「已验证」**无凭据**。
- `status="skip"` 的 `error_class` 有 **三种写法并存且自相矛盾**（`ok` / `None` / `cli_usage_error`）。
- `--only` 的 `raw_file` 可能写成绝对路径、且不清理上次残留。

## 三、最值钱的两条方法论教训

1. **「我无法复现」≠「它是伪造的」** —— 第一轮 D-7 断言 `independent_inventory.json` 不是其声明生成器产出，
   第二轮**主动撤回**：根因是审计方自己跑不了脚本，就把无法复现升级成了伪造指控。
   编排层实跑证明该脚本 rc=0 正常产出。**审计报告必须区分「我验证为假」与「我无法验证」。**
2. **契约要防的是「字段齐全 ≠ 可信」** —— 本次多处缺陷的共同形态是：
   字段都在、schema 都合法，但语义失真（latency 跨尝试累加、chain 标签不可证伪、`ok` 却是伪成功）。
   ⇒ 验收集应加入**语义级**判据（如「ok 条目的载荷是否有实质条目」「45s 上限是否被遵守」），而不是只查字段存在性。

## 相关

- [[aws-support-tooling-probe-design]] — 契约原文与审计项定义
- [[aws-support-tooling-probe-audit]] — A/B/C/D 审计结论
- [[aws-support-tooling-probe-inventory-diff]] — 真实缺漏的逐命名空间证据
- [[aws-support-tooling-probe-param-fill]] — F7 补参重跑的完整数据
