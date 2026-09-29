---
title: dsh 插件体系 · 版本兼容闸门与可安装清单
tags: [dsh, DeepSeek Harness, 插件, semver, peerDependencies, 工具链]
created: 2026-09-30
updated: 2026-09-30
source: deliverables/dsh-plugins/dsh-plugin-install-verified-2026-09-29.md + dsh-plugin-recommendations-2026-09-29.md（2026-09-29）｜原件 D:/AI/my_project/deliverables/dsh-plugins/
status: growing
---

# dsh 插件体系 · 版本兼容闸门与可安装清单

**一句话结论：桌面版 dsh（`0.2.0-rc.2`）装插件**只能走「设置 → 插件」**（Electron 进程级独占 profile，CLI 会被回滚）；插件锚定的是 dsh 的**内部包版本**（`@deepseek-ai/dsh-*`）而非 dsh 自身版本号，因此「看着像能过」的区间常被 semver 预发布规则拒之门外。**

## 一、本机现状（实测）

| 项 | 值 |
|---|---|
| 桌面版安装目录 | `D:\deepseek-harness` |
| dsh 运行时版本 | `0.2.0-rc.2` |
| 随附 node / pnpm | `24.18.1` / `11.7.0` |
| `DSH_HOME` | `~/.dsh` |
| 当前 profile | `desktop` |
| 已装第三方插件 | `dsh-plugin-whale-pet@0.2.8` |
| profile bundles | `dsh-base` `dsh-web-app` + 3 个官方实验包 + whale-pet |

`desktop` profile 已启用的**官方实验包**（不用另装）：`dsh-experimental-agent-team-profile`（多智能体团队）、
`dsh-experimental-auto-review`（自动复核）、`dsh-experimental-voice-input-bundle`（语音输入）。

## 二、🔴 安装通路：只能走「设置 → 插件」

```
插件来源（npm 包名 / github:owner/repo / 本地目录）
        ↓
桌面版：设置 → 插件          ← 唯一能写 desktop profile 的入口
        ↓
写入 profile 的 dependencies + dsh.profile.bundles
        ↓
重启 dsh 生效
```

CLI 的 `dsh plugin --profile desktop add ...` **走不通**：Electron 进程级独占 `$DSH_HOME/profiles/desktop`
及其 package-manager state，CLI 执行后会打印
`dsh: restored package.json, pnpm-lock.yaml, and node_modules`（即回滚）。要用 CLI 必须换 profile（`web` / `headless`）。

**agent 无法代点安装**（实测证据，非推脱）：桌面版进程在跑（5 个 `DeepSeek Harness.exe`，Host PID 监听 `127.0.0.1:19387`），
但 `/`、`/api`、`/api/plugin`、`/api/plugins` **全部 HTTP 401**，`/pluginInventory/list` 404；
凭据只发给 `dsh-app://app` 窗口，走**私有 Node IPC**，渲染进程也拿不到 token。
官方 README 原文：Electron **「exclusively owns `$DSH_HOME/profiles/desktop` plus its package-manager state」**。

## 三、⭐ 闸门原理（可复用，下次自己就能判）

1. 从桌面版 `resources/app.asar` 抽出全部 `@deepseek-ai/*` 的**真实版本**：
   - `cordis=4.0.4`、`schemastery=3.18.4`、`cosmokit=1.8.5`
   - **其余 284 个 `dsh-*` 全是 `0.2.0-rc.2`**
   - 脚本：`_dsh_probe/internal_versions.py` → `_dsh_probe/dsh_internal_versions.json`
2. 取插件的 `peerDependencies`，对每个 `@deepseek-ai/*` 键用 `semver.satisfies(已装版本, 区间)` 判定。
3. 脚本：`_dsh_probe/final_check.js`（清单式批检，改数组即可复用）。

⭐ **易错点**：`cordis` / `schemastery` / `cosmokit` **不是 `0.2.0-rc.2`**，它们有独立版本线。

**为什么"看着像能过"其实过不了** —— semver 预发布规则：
`0.2.0-rc.2` 是**预发布版**，只有**写了预发布号的区间**才匹配它。
`^0.1.5-rc.3`、`>=0.1.0-rc.5 <0.2.0`、`>=0.1.5-rc.1` 都**不覆盖** `0.2.0-rc.2`。

> **关键认知**：插件锚定的是 dsh 的**内部包**版本（`@deepseek-ai/dsh-settings` 等），**不是 dsh 自身的版本号**。
> ⇒ 「我的 dsh 是 0.2.0-rc.2，插件要求 0.1.x，所以不兼容」——**不能这样推**，要看 peerDependencies 原文。

## 四、✅ 现在就能装（8 项，精确安装标识）

按建议顺序，**在「设置 → 插件」的自定义安装框里逐个粘贴**：

| # | 粘贴这个 | 版本 | 闸门 | 是什么 |
|---|---|---|---|---|
| 1 | `dshmarket` | 1.66.5 | **PASS** | 可视化插件市场（装完就有界面挑插件） |
| 2 | `@wxg-prc-cpg/dsh-weknora` | 0.1.0 | 无 peerDeps | 腾讯 WeKnora：语义检索 + 文档读取 + RAG 工具 |
| 3 | `@tt-a1i/archify-dsh` | 0.1.0 | 无 peerDeps | archify：架构图 / 时序图 / 数据流图 skill 包 |
| 4 | `dsh-cost-meter` | 1.7.45 | **PASS** | 会话成本 + 当日费用 + 11 家 Coding Plan 额度 |
| 5 | `dsh-tokenledger` | 0.1.0 | **PASS** | token 用量按中转站归属记账 |
| 6 | `dsh-better-sidebar` | 0.24.1 | **PASS** | 侧栏：文件树 / 编辑器 / 变更 / 任务 / 侧聊 |
| 7 | `github:0xsline/dsh-spotlight` | — | 无 peerDeps | 命令面板 |
| 8 | `github:MeteorNOX/DeepSeek-Balance-Whale-Widget` | — | 无 peerDeps | 鲸鱼形余额挂件 |

**闸门原文佐证**（`dsh-cost-meter` 作者显式支持 0.2.x，是生态里最规范的写法）：
```
peerDependencies: @deepseek-ai/dsh-home-paths "^0.1.0-rc.6 || ^0.1.1-0 || ... || >=0.2.0-rc.1 <0.3.0-0"
→ 对 0.2.0-rc.2 判定 PASS
```

> ⭐ **最重要的一条**：`dshmarket` **已经修好了** —— 09-27 装的是 1.66.3，现在 **1.66.5 在 peerDeps 里补了 `^0.2.0-rc.1`**，闸门通过。

## 五、⛔ 被版本闸门拦下的 4 项（不是安装姿势问题）

| 插件 | 最新版 | 报错原文（截取） |
|---|---|---|
| `dsh-context` | 0.60.0 | `@deepseek-ai/dsh-session@0.2.0-rc.2 不满足 ">=0.1.5-rc.1"` |
| `dsh-genui` | 0.2.1 | `@deepseek-ai/dsh-client-ui-slots@0.2.0-rc.2 不满足 ">=0.0.1-rc.1 <0.1.0 \|\| >=0.1.0-rc.1 <0.2.0-0"` |
| `@memtensor/memos-local-plugin` | 2.0.20 | `@deepseek-ai/dsh-agent@0.2.0-rc.2 不满足 ">=0.1.0-rc.5 <0.2.0"` |
| `@wxg-prc-cpg/browser-skill-dsh-plugin` | 0.3.1 | `@deepseek-ai/dsh-llm@0.2.0-rc.2 不满足 "^0.1.5-rc.3"` |

**处置建议**：等作者更新 > 用 dsh 的**精确版本豁免**强装。
⚠️ 强装不是走过场 —— 产品原文写着「**Running it may cause crashes or data loss**」。
`dsh-genui` 和 `memos` 是**明确把上界封在 0.2.0 之前**，说明作者已知不兼容，不是忘了改。

## 六、❌ 这 3 项不是 dsh 插件（目录站标错了）

| 你要的 | 实情 | 证据 |
|---|---|---|
| **open-design** | **不能作为 dsh 插件安装** | 根 `package.json` 是 `"private": true` 的 monorepo，**无 `dsh.bundle`**；官方 README 只给 `od agent setup deepseek-harness`，方向是**它来驱动 dsh**，不是反向 |
| **Hindsight** | 该仓库没有 dsh 插件 | `vectorize-io/hindsight` 无 `dsh-plugin` topic，根目录无插件包 |
| **EverOS** | 仓库内无 dsh 相关路径 | 全仓扫描 `1122` 个文件，`dsh` 匹配 0 条 |

> **09-27 那次 `open-design` 安装失败的根因就在这**：第三方教程给的
> `github:nexu-io/open-design` 命令本身就错（会把整个 monorepo 当插件包拉下来，
> 然后 `postinstall` 去构建 `packages/release` → `MODULE_NOT_FOUND` → 回滚）。

## 七、⚙️ 两个已踩的坑

1. **版本兼容闸门**（`dshmarket@1.66.3` 实测被拒）—— 见 §三。
   绕过：`dsh plugin allow-version`（显式承担崩溃/数据丢失风险），或等作者更新。
2. **GitHub 源插件常缺构建产物**（`open-design` 实测失败）：
   第一次 `ERR_PNPM_IGNORED_BUILDS`（pnpm 默认拒绝执行陌生包的构建脚本）→ 加 `allowBuilds` 后重试 →
   `postinstall: packages/release failed with exit code 1`（`MODULE_NOT_FOUND`）→ 回滚。
   ⚠️ 回滚**没有清掉** `pnpm-workspace.yaml` 里那条 `allowBuilds`，属残留。
   ⇒ **优先用 npm 预构建版，GitHub 源只作备选。**

修复动作：若报 `ERR_PNPM_IGNORED_BUILDS`，在 `~/.dsh/profiles/desktop/pnpm-workspace.yaml` 的 `allowBuilds` 下加该包并重试。

## 八、🔍 排障入口（最重要的一条）

```
~/.dsh/profiles/desktop/.plugin-manager/logs/<operation-*>/pnpm.log
```
—— 界面上只显示一句错，**真正的原因（pnpm 输出 + dsh 的拒绝理由）全在这个文件里**。

## 九、按用途分档推荐（生态 100+ 个，本机目前只装了 1 个）

**第一档 · 与日常工作直接对口**：`open-design`（98.6k，原型/落地页/仪表盘/幻灯片，导出 HTML·PDF·PPTX·MP4）｜
`archify`（74k，架构图/时序图/数据流图）｜Tencent `WeKnora`（31.2k，文档 → RAG + 自维护 Wiki）｜
`dsh-univer-office`（208，表格/文档/演示/数据库）｜Tencent `BrowserSkill`（1.2k，命令行 → 原生 `browser_*` 工具）

**第二档 · 长任务与成本可控**：`dsh-context`（600，上下文面板）｜`dsh-cost-meter`（133）｜`TokenLedger`（123）

**第三档 · 界面与操作效率**：`dsh-better-sidebar`（2.4k）｜`dsh-spotlight`｜`dsh-at-file`（438）｜
`dsh-genui` / `dsh-visualize`（265 / 191）｜`dsh-TUI` / `dsh-tianshu-tui`（2.2k / 224）

**第四档 · 记忆（生态第二大主题）**：`Hindsight`（20.4k）｜`EverOS`（13.3k）｜`MemOS`（11.6k）｜
`memsearch`（2.5k）｜`dsh-memory-evolve`（205）

**第五档 · 多 agent 与自动化**：`dsh-agent-teams`（682）｜`dsh-agent-team-gui`（111）｜
`app-wework（Wegent）`（760）｜`dsh-super-injector`（127）｜`dsh-answer-reviewer`

**第六档 · 好玩（含鲸鱼周边）**：`dsh-ads`（519）｜`openpets`（1.1k）｜`whale-girl`（252）｜
`DeepSeek-Balance-Whale-Widget`（208）｜`dsh-plugin-whale-pet`（**已装**）

> 星标为 2026-09-29 抓取值，**会漂移**；安装前请复核。

## 相关

- [[deepseek-harness-desktop-install]] — 桌面版 dsh 的安装与卸载记录
- [[skill-env-consistency-audit-20260927]] — 技能与环境一致性体检方法
- [[raven-install-windows-native]] — 同属本机工具链装/卸记录的姊妹篇
- [[proxy-node-rotation-bundle]] — 同为本机资产登记（基础设施侧）
