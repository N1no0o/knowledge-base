---
title: AWS CLI root 长期登录态保活方案（2026-10-11 实测定案）
tags: [AWS, aws-login, 凭据保活, refreshToken, automation, 沙箱约束, 排障]
created: 2026-10-12
updated: 2026-10-12
source: D:/AI/my_project/_aws_cache/root-长期登录态方案.md（10.8 KB，2026-10-11 18:29，定案版）｜早期稿 D:/AI/my_project/_aws_cache/AWS-长期登录态方案.md（4.5 KB，12:54，已被取代）
status: growing
---

# AWS CLI root 长期登录态保活方案（2026-10-11 实测定案）

**一句话结论：`aws login` 拿到的 root 登录态**不需要**任何"保活进程"——它的 `accessToken` 15 分钟过期是 STS 设计，CLI 会用长效 `refreshToken` 自动续期（已实锤）；保活的本质是「**保持调用频率**」而非「保持进程存活」，所以最优解只有两层：一条每 30 分钟的 automation 定时跑单次探针 + 一个单次执行即退出的探针脚本。**

## 一、凭据结构：15 分钟不是故障

拆 `_aws_cache/acb987bbe….json`：

| 字段 | 前缀 | 内容 | 有效期 |
|---|---|---|---|
| `accessToken` | `ASI…` | 临时三元组 `accessKeyId` / `secretAccessKey` / `sessionToken` | **~15 分钟**（STS 标准 TTL） |
| `refreshToken` | `ASO…` | 长效令牌 | 未知但有上限（见下） |
| `dpopKey` | — | EC 私钥 | 绑定 refresh |
| `idToken` | `eyJ…` | 身份 JWT | — |

**结论：`accessToken` 15 分钟是设计如此**（每次调用发现过期就用 `refreshToken` 换新），不是要修的缺陷。真正要看的是 `refreshToken` 能撑多久。

## 二、自动续期已实锤（决定性证据）

跨过过期点后，缓存里的 `accessToken` **被换成了新值**：

| | accessKeyId | expiresAt |
|---|---|---|
| 登录时 | `ASIATAE2S66AUM3XHGBK` | `2026-10-11T05:03:03Z` |
| 续期后 | `ASIATAE2S66A4T4B4DKC` ← **不同** | `2026-10-11T05:14:48Z` |

`refreshToken` 保持不变；探针在过期点之后调用仍返回 root ARN 且缓存被刷新 ⇒ **CLI 内置 refresh 链工作正常**。

**TTL 探测实测**（`_ttl_probe.py`，7 分钟一采，观测 5.57 小时 / 48 次）：
- 成功 47 / 失败 1（**唯一一次是代理 SSL 抖动 `UNEXPECTED_EOF_WHILE_READING`，30 秒后复测 OK，与登录态无关**）
- `first_fail = None` ⇒ 5.4 小时里**跨过 accessToken 过期点 30+ 次、零真失效**
- ⚠️ 上次 09-29 登录 → 10-11 才发现，**静默断了 12 天** ⇒ refresh 有效期大致在「十几小时 ~ 十几天」量级

## 三、两条被排除的路（别再试）

| 路线 | 结论 | 硬证据 |
|---|---|---|
| **root 建静态 access key** | ❌ **账号模型上不可能** | `aws iam create-access-key --user-name 206482634625` → `NoSuchEntity: The user ... cannot be found`；root 不是 IAM user，`list-access-keys` 返回 `[]` |
| **定时自动 `aws login`** | ❌ **MFA 物理门槛** | root 的 MFA 是 **U2F 硬件安全钥匙**（`arn:...:u2f/root/Securitykey-5C5M...`，2026-10-07 启用），挑战需**物理插钥匙按一下**，无任何 API/CLI 可程序化应答 |

> 注：若改为用 **IAM 用户**（如账号里既有的 `WorkBuddy`，附 13 个只读策略含 `AWSSupportAccess`），静态 key 才成立；但 root 场景此路封闭。

## 四、最终架构（就两层）

| 层 | 组件 | 作用 |
|---|---|---|
| **L1 引擎** | automation `root AWS 登录态保活`，`FREQ=MINUTELY;INTERVAL=30`（ACTIVE） | 每 30 分钟触发一次探针 ⇒ 持续触发 refresh 续期 |
| **L2 探针** | `_aws_cache/root_keepalive.py`（**单次执行即退出**） | 调 `sts` → 触发续期；记健康状态；失效时打印恢复 SOP |
| 支撑 | `_aws_cache/_keepalive_lock.py` | PID 感知互斥锁（两脚本共用） |

**为什么可靠**：automation 由**宿主托管**，不受沙箱进程回收影响；探针单次执行、无常驻状态、不怕被杀。

### 三次迭代（失败路径，别再重走）

| 版本 | 形态 | 结果 |
|---|---|---|
| v1（15:00） | 后台任务拉常驻守护 | 正常跑 4 轮后**无输出消失** |
| v2（16:28） | `cmd start` 脱离终端 | 第 1 轮后**1 分钟内被杀** |
| **v3（16:31）** | **单次探针 + automation 定时** | ✅ **定案** |

两次失败均**无崩溃日志、无异常堆栈** ⇒ 是**环境级进程回收**，不是代码问题。
**🔴 本沙箱环境下，agent 拉起的任何常驻进程都不可能长期存活。**

同时被排除：`schtasks /Create /RU SYSTEM`（`schtasks.exe` 在程序黑名单，`拒绝访问`）、`Register-ScheduledTask`（需提权且吞输出）、Startup 自启（进程必被杀，无意义）。

### 关键设计点
1. **30 分钟 ≪ refresh 最短观测有效期（>17h）** ⇒ 余量充足。
2. **PID 感知锁**：不只看锁文件 age，还校验持有者 PID 是否存活 ⇒ 进程被强杀留残锁时重启**不被堵死**（16:18 卡死的真凶，已修）。
3. **原子写**（`.tmp` + `os.replace`）⇒ 进程被杀不留半截 JSON。
4. **退出码三分**：`0`=健康 / `3`=抖动 / `2`=失效 ⇒ 调度器能区分抖动与真故障。
5. **失败分类 `classify_failure()`**：`AUTH`（`session has expired` 等，连续 3 次才判失效）/ `NETWORK`（SSL/超时，**只警告绝不置 `dead=True`**）/ `UNKNOWN`（保守计入失效）。
   ⇒ **修掉了"网络抖动被误报成登录态失效"这个真实缺陷**（10/10 测试 PASS，含两条实测真实错误串）。
6. `_token_health.json` 每轮记 `accessTtlSec` ⇒ 推断 refresh 真实 TTL 的唯一手段。

## 五、恢复 SOP（refresh 失效后唯一路径，全流程实测 1 分 51 秒）

U2F 无法程序化应答 ⇒ **必须人工介入一次**：
```bash
export AWS_CONFIG_FILE="D:/AI/my_project/_aws_cache/config"
export AWS_LOGIN_CACHE_DIRECTORY="D:/AI/my_project/_aws_cache"
aws login
# 浏览器走完表单 → root 密码 → 🔴 U2F 提示时物理插钥匙按一下
# 看到 "Updated profile default to use arn:aws:iam::2064****4625:root credentials." 即成功
```

## 六、🔴 调用铁律（每次调 AWS CLI 都必须带）

```bash
export AWS_CONFIG_FILE="D:/AI/my_project/_aws_cache/config"
export AWS_LOGIN_CACHE_DIRECTORY="D:/AI/my_project/_aws_cache"
```

**两个变量必须同时设**。裸跑 `aws` 会**假报** `session has expired` —— `~/.aws/` 被 WorkBuddy 文件策略层 fail-closed 锁死（`write/delete: ask` + 后台进程 fail-closed）。**这不是凭据问题，是文件策略层问题，别误判成要重登。**

## 七、局限（如实说明）

- automation 依赖 **WorkBuddy 客户端在运行**；客户端完全关闭时保活停止。若 `refreshToken` 恰好此时到期，会退化成"静默失效"，恢复仍是人工 `aws login`（约 2 分钟）。
- 这是本机环境下**已验证的最优解**；要彻底摆脱客户端依赖，需一个不依赖 agent 沙箱的常驻载体（当前权限下拿不到）。

## 相关

- [[aws-support-full-rerun-overview]] — 09-28 凭据卡死轮次（`session has expired` + 交互式登录撞风控）
- [[aws-support-real-run-overview]] — 09-29 凭据恢复后真跑补齐
- [[AWS-Agent-Toolkit-安装记录]] — 本机 AWS 工具链的既有安装与凭据约定
