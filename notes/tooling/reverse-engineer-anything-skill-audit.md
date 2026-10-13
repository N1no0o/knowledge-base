---
title: REA（Reverse Engineer Anything）技能调研与安全审计（2026-10-13）
tags: [skill安全审计, 逆向工程, MCP, 供应链安全, 热度造假, rea, 工具选型]
created: 2026-10-13
updated: 2026-10-14
source: _rea_audit/REA-skill-audit-2026-10-13.md（原件 D:/AI/my_project/_rea_audit/，2026-10-13 09:27）
status: growing
---

# REA（Reverse Engineer Anything）技能调研与安全审计（2026-10-13）

**一句话结论：`morluto/rea`（npm `rea-agents` 6.4.0，MIT）技术侧是真货、热度侧是造假 ⇒ 评级 CAUTION 而非 DANGER；已在可回滚前提下完成本机安装，风险的真实位置不在「安装瞬间」而在「使用期间」。**

## 一、它是什么

给 AI Agent 用的逆向工程工具箱，三件套 = **CLI（`rea`）+ MCP server（stdio，170 个工具）+ Agent skill 指令包**。能力面：原生二进制（Ghidra / Hopper / IDA）、JS·Electron（ASAR / source map / IPC）、.NET 程序集、Android APK、固件、HAR / mitmproxy 抓包、SQLite 快照、WASM·EVM 字节码、进程 PTY 观测。

## 二、技术侧「真货」的证据

3514 个文件 · 187 个 npm script · 完整测试与 CI · 17 种语言 README；已发布 npm tarball **不含任何 pre/postinstall 生命周期钩子**（复核 hooks = NONE）；`DISCLAIMER.md` 明确禁止 DRM 绕过 / 抄专有代码 / 绕过鉴权。第三方独立测量（senn-tech）原话：**「软件是真的，热度是假的」**。

## 三、热度造假证据（2026-10-13 实测原始数据）

| 指标 | 实测值 | 正常应有 | 判读 |
|---|---|---|---|
| stars | 158,460 | — | 10-04 仅 1.5K，9 天涨 15 万 |
| **watchers** | **506** | star 的 1–2% | 仅 **0.32%** ⚠️ 反常 |
| forks | 36,765 | star 的 5–10% | **23%** ⚠️ 反常 |
| fork 速率 | newest 页 100 条 fork 仅跨 **6.25 分钟**（≈960 forks/h） | 应随昼夜起伏 | 机器节奏 ⚠️ |
| 仓库创建 | 2026-04-14 | — | 前 5 个月基本无人问津 |

npm 下载曲线（`api.npmjs.org`）：09-29 起 12 → 14 → 18 → 16（基线），**10-03 起引爆** 418 → 798 → 4048 → 5032 → 9000 → 19983 → 34790 → **10-11 达 59,665**，一周合计 **132,518**。

第三方测算：fork 列表分页推算 16,500 次 fork 集中在 3.69 天内 ≈ **4,470 次/天 = 仓库自身历史基线（约 16 次/天）的 280 倍**；且 03:00 / 06:00 / 09:00 UTC 三点读数为 310 / 302 / 367 次/小时，**曲线整夜平坦不掉 ⇒ 机器而非人**。旁证：仓库 topics 里塞了 `dsh`、`dsh-plugin`、`cordis` 等与逆向无关的关键词（蹭热）。

> **性质界定：这是「流量运营事件」，不是「供应链投毒事件」—— 两者处置方式不同，不要混为一谈。**

## 四、安全审计五轴（结论）

| 轴 | 结果 |
|---|---|
| Frontmatter 完整性 | 🟢 与目录一致；无零宽字符 / RTL 覆写 / 隐藏指令 |
| 恶意模式（ClawHavoc） | 🟢 全文无反弹 shell / 凭据窃取 / 数据外发 / 混淆执行 / 提示注入；`install.sh` 反带「截断守卫」（加分项）；已发布 tarball 无 install 钩子 |
| 权限-用途匹配 | 🟢 工具面宽但与「逆向分析」声明用途一致；未越权申请凭据环境变量 |
| 指令质量与范围 | 🟡 SKILL.md 写得克制（强制区分「观测 / 推断 / 未知」、要求引用 Evidence ID），但 3 个月 31 个版本、一周 5 个版本，工程节奏激进 |
| 信任信号 | 🔴 匿名个人维护者（package.json 无 author / funding）；热度指标集体造假 |

**Overall：CAUTION ⚠️**。风险真实位置 = 使用期 —— 一个能读任意本地文件、spawn PTY、驱动浏览器、解析网络抓包的本机服务，**工具面高达 170 个**。

依赖树：35 个直接依赖全为主流包（`@modelcontextprotocol/*`、`ws`、`zod`、`ajv`、`plist`、`isomorphic-git`、`playwright-core`、`@electron/asar`、`@lydell/node-pty` 等）；5 个 git submodule 中 4 个为知名上游（binwalk / unblob / ghidra-nativeaot / wakaru），**`1013503897/jadx-headless-mcp` 来源不明（作者个人仓库）**。

## 五、本机可用性打折与本次安装内容

官方 `install.sh` **源码第 111 行硬拒 Windows**；`npx rea-agents setup` 支持 Claude Code / Codex / Cursor / Gemini CLI 等、**不含 WorkBuddy** ⇒ 改走「本地固定目录安装 + 手工注册 MCP + 手工放 skill」。

| # | 变更 | 路径 |
|---|---|---|
| 1 | Skill 指令包（纯 Markdown，7 文件） | `C:\Users\lichangzhao\.workbuddy\skills\reverse-engineer-anything\` |
| 2 | 本地 CLI + MCP server 实体（144 包，约 **100 MB**） | `D:\AI\_tools\rea-cli\node_modules\rea-agents\` |
| 3 | MCP 注册（stdio，绝对路径直调、版本钉死 6.4.0，不经 npx） | `C:\Users\lichangzhao\.workbuddy\mcp.json` → `mcpServers.rea` |
| 4 | 配置备份 | `mcp.json.bak-20261013-rea`（561 B，diff 一致） |

**验收证据（实测非推断）**：`rea --version` → `6.4.0` rc=0 · MCP `initialize` 握手 → `serverInfo = {name: rea, version: 6.4.0}`、`protocolVersion = 2024-11-05` · `tools/list` → **170 个工具** · 用配置中的真实绝对路径复跑握手 rc=0（端到端复核）。

**⚠️ 还需人工做一步**：MCP 配置写完不自动生效 —— ① 打开 WorkBuddy 连接器管理页，在右上角「自定义连接器」入口对 `rea` 点「信任」；② **重启 WorkBuddy**（MCP 配置变更需重启才加载）。

## 六、回滚 / 使用建议与红线

- **回滚（三步全撤）**：`python D:\AI\my_project\_rea_audit\uninstall_rea.py` —— 还原 `mcp.json`（优先用备份）→ 删 skill 目录 → 删 `D:\AI\_tools\rea-cli`。
- ✅ **建议用法**：理解闭源依赖行为、排查老旧二进制、CTF / 恶意样本分析、研究竞品**实现思路**后自研。
- 🚫 **红线**：不要用它拆 DRM / 授权校验 / 反作弊；不要把拆出来的专有代码搬进自己的产品（MIT 与作者 DISCLAIMER 都不授予你对**目标程序**的权利）。
- ⚠️ **Windows 侧能力边界**：原生二进制逆向依赖 Hopper（付费，仅 macOS）/ Ghidra / IDA。Windows 上实际可用的是 **JS·Electron、.NET 程序集、APK（需 JADX+JDK）、HAR 抓包、SQLite、Go 二进制元数据**这一半；固件类（Binwalk / Unblob）、PTY、mitmproxy 原生抓包断言为 **Linux/macOS**。
- ⚠️ **170 个工具**会让 Agent 工具索引明显变长；若影响日常推理效率，可把 `mcp.json` 里 `disabled` 改 `true` 按需启停。
- ⚠️ **抓包类工具**：解析 HAR 可能含 cookie / 凭据，作者声明已做凭据排除，仍建议只对自有且已脱敏的抓包使用。

## 相关

- [[skill-env-consistency-audit-20260927]] — 同类「技能体检」方法论（悬空引用 / 过期版本 / 静默失效 hook）
- [[dsh-plugin-ecosystem]] — 同为第三方插件/工具生态的准入判断（那里是 semver 预发布闸门）
- [[deepseek-harness-desktop-install]] — 同为「第三方工具本机安装 + 回滚」类记录
