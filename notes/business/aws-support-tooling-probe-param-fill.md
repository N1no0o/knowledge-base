---
title: AWS 支持工具能力普查 · 补参重跑与真实可达性
tags: [AWS, 支持服务, 补参, error_class, 真实可达性, 华为云支持服务立项]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/aws-support-plans/tooling-probe/param_fill_report.md（2026-09-27）
status: growing
---

# AWS 支持工具能力普查 · 补参重跑与真实可达性

**一句话结论：对 130 条「只读且必填参数 >0」的操作自动补参后重跑，「实际被调用」从 3 条跃升到 **124 条**、`service_error` 从 2 条增到 103 条——说明上一轮 61% 的记录只是 CLI 本地参数校验失败、**根本没到 AWS**；但 `status=ok` 的 20 条里只有约 10 条真的拿到了数据。**

## 一、为什么必须补参

第一轮 202 条里 **124 条（61%）**是 `ParamValidation`（CLI 本地参数校验失败），
**没有产生任何 AWS API 应答** ⇒ 标称「真实调用结果的能力普查」，对 124/202 个操作**零信息量**。
（latency 双峰也因此而来：本地校验 495–570ms，真实往返 1300–2900ms。）

## 二、130 条补参前后的 `error_class` 对比（分母一致）

| `error_class` | 补参前 | 补参后 | 变化 |
|---|---:|---:|---:|
| `cli_usage_error` | 3 | 0 | −3 |
| `cli_param_validation` | 124 | 6 | **−118** |
| `service_error` | 2 | 103 | **+101** |
| `timeout` | 0 | 1 | +1 |
| `ok` | 1 | 20 | +19 |
| **合计** | **130** | **130** | — |
| `actually_invoked=true` | **3** | **124** | **+121** |

补参路径：`op_inventory.json` 里 `is_readonly=true` 且 `params_required>0` 的 130 条；
参数来源 `chain / static / suffix_rule / fallback`，每条参数都写进结果的 `param_fill`（便于审计真值 vs 合成值）。

## 三、真正可用（`actually_invoked=true` 且 `status=ok`）共 20 条

集中在 **`devops-agent`（13 条）**、`support`（3 条）、`wellarchitected`（2 条）、`trustedadvisor`、`health`。

⚠️ **但这 20 条里 8 条是纯空壳**（唯一载荷为空集合，如 `{"items": []}`）、**2 条半空/伪成功**
（含 `health/describe-event-details`：CLI exit 0 但 API 逐项 `EventNotFoundError`）
⇒ **真正拿到实质数据的只有约 10 条（≈7.7%），按现口径 20/130≈15.4% 会把可用性高估约一倍。**

## 四、诚实降级的证据（`fallback` 共 16 条）

- `wellarchitected` 的 `--profile-arn`：上游 `list-profiles` 返回**空数组** ⇒ 取不到值 ⇒ 如实落 fallback；
- `service-quotas` 的 `--quota-code`：上游 raw **只有 `.err.txt` 没有 `.json`** ⇒ 如实落 fallback。

⭐ **降级路径是活的、没被掩盖** —— 这是「35 条 chain 参数不是造假」的关键反证。
但其中 2 条 chain 的「真值」其实没打中（取错字段 / 规格未实现 / 标签不可证伪），见 [[aws-support-tooling-probe-defects]] 主题⑤。

## 五、本轮新触达的服务端结论（此前未拿到）

| # | 操作 | 服务端返回 |
|---|---|---|
| 1 | `devops-agent/describe-private-connection` | `ResourceNotFoundException`（`Private connection 'probe' not found`） |
| 2 | `devops-agent/list-tags-for-resource` | `BadRequestException`（`expected vendor aidevops`） |
| 3 | `service-quotas/get-requested-service-quota-change` | `NoSuchResourceException` |
| 4 | `wellarchitected/list-tags-for-resource` | `NotFoundException` |
| 5 | `support/describe-attachment-upload-status` | `UploadIdNotFound` |
| 6 | `service-quotas/get-service-quota` | `IllegalArgumentException`（ServiceCode 不满足服务端正则） |
| 7 | `wellarchitected/get-agent-context` | `400 Unknown Operation` |
| 8 | `security-ir/list-tags-for-resource` | `AccessDeniedException, UnauthorizedException` |

## 六、验收侧的两条提醒

1. `stats2`：`ok=20 / error=109 / timeout=1 / skip=0`；`attempts={"1":120,"2":10}`；
   10 条 `exceeded_timeout_budget` **如实标注**（含 1 条重试后成功仍保留 `attempts=2`，未粉饰）。
2. **主交付物未重跑** ⇒ 本轮修复在「读 `probe_results.json`」的验收口径下看不到（见 [[aws-support-tooling-probe-defects]] 主题⑦）。

## 相关

- [[aws-support-tooling-probe-design]] — 契约与产出定义
- [[aws-support-tooling-probe-defects]] — 补参链路的 4 条相关缺陷
- [[AWS支持服务工具-API实测报告]] — 同账号更早的直接实测，可对照「哪些操作本来就被订阅层锁死」
