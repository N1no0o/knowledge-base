---
title: 技能一致性体检 · 把技能里的「实测」断言逐条真跑（2026-09-27）
tags: [Skill, 技能体检, hook, WorkBuddy, codex, 多agent, 工具链]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/skill-audit/技能一致性体检-2026-09-27.md（2026-09-27）
status: growing
---

# 技能一致性体检 · 把技能里的「实测」断言逐条真跑

**一句话结论：体检方法是「把 SKILL.md 里每一条『实测』断言拆出来、逐条对本机真跑一次」；结果是自建的 `multi-agent-cli-orchestration` 本机可用（修了 3 处过期断言），
而 skillhub 装的 `self-improvement` **只能当参考**——它的 hook 机制在本机静默失效。**

## 一、体检结论总表（20 条断言，16 ✅ / 4 ❌ / 2 ⚠️）

| 技能 | 判定 | 关键差异 |
|---|---|---|
| `multi-agent-cli-orchestration`（自建） | ✅ 本机可用 | 3 处过期已修：codex 版本号、小节标题「三个坑」实为四条、codex 上游来源 |
| `self-improvement`（skillhub 装） | ⚠️ 只能当参考 | `assets/` 缺 2 个模板（悬空引用）；hook 全套 Claude Code 专属、**本机静默失效** |

**已修的 3 处**：① 「三坑」→「四坑」（正文本来就是 4 条，标题少一条会让后续会话漏读最难受的那条）；
② 更新 codex 版本号；③ 新增 codex 本地代理依赖并标注旧直连记录作废。

## 二、⭐ 本次最值钱的发现：WorkBuddy 的 hook 契约（从程序本体取证）

取证文件：`D:\WorkBuddy\resources\app.asar.unpacked\cli\dist\codebuddy-lite-wb.mjs`

- **事件名与 Claude Code 同名**：`SessionStart / UserPromptSubmit / PreToolUse / PostToolUse / SubagentStop / InstructionsLoaded`
- **输入走 stdin JSON（不是环境变量）**：`{ hook_event_name, session_id, transcript_path, cwd, hook_specific_output }`
- **输出**经 `parseHookOutput` 解析：`{ message, systemMessage, additionalContext, hookSpecificOutput:{...} }`
- 配置结构（范本 = 内置 sheetagent 的 `hooks/hooks.json`）：
  ```json
  { "hooks": { "SubagentStop": [ { "hooks": [
      { "type": "command", "command": "node \"${CODEBUDDY_PLUGIN_ROOT}/hooks/x.mjs\"", "timeout": 15 } ] } ] } }
  ```
- ⚠️ 本机 `~/.workbuddy/settings.json`（40,003 B）**没有 `hooks` 键** ⇒ **第三方 hook 一个都没启用**。

⇒ 据此判定 `self-improvement` 的失效形态：`activator.sh`（纯打印文本、不读环境变量）**理论上可改用**；
而 `error-detector.sh` 读 `CLAUDE_TOOL_OUTPUT`，本机**从不提供该变量** ⇒ **永远读到空串、永远不触发、且不报任何错**。
**这是最危险的一类失效：静默的。**

## 三、新查明的环境事实（此前记录有误，已更正）

| 项 | 旧记录 | 实测（2026-09-27） |
|---|---|---|
| `codex` 版本 | `0.155.0-alpha.2.6` | **`0.158.0-alpha.2`** |
| `codex` 上游 | 直连 `https://api.deepseek.com` | 🔴 **`http://127.0.0.1:15721/v1`（本地代理）**，端口实测在听 |
| `bin\` 下版本目录数 | 假设 1 个 | **2 个**：`d23520d1e41bfb24`（有 codex.exe）/ `48e0e7462d1adb63`（**只有 `rg.exe`**） |

**影响**：`codex` 多了一条技能里没写的硬依赖 —— **编排前必须先探 `127.0.0.1:15721`，端口不在听则必然失败**
（端口在听 ≠ 上游可用，但端口不在听一定不可用）。
现有 `find_codex()`（筛 `*/codex.exe` 后按 mtime 取最新）**恰好能避开**那个只含 `rg.exe` 的目录，实现正确、无需改。

## 四、报给作者、未修（skillhub 装的不可改）

`self-improvement` 带 `_skillhub_meta.json`（`source: skillhub`）⇒ **改它会被下次更新覆盖，且本地漂移不可见**。建议反馈 5 点：

1. `assets/` 缺 `ERRORS.md` 与 `FEATURE_REQUESTS.md` 模板（SKILL.md 明确让「从 assets 复制」）。
2. 技能包内自带 `.learnings/` 空壳 —— 会诱使 agent 误把学习日志写进技能目录（**更新即丢**）。
3. hook 全套为 Claude Code 专属（`.claude/settings.json` + `CLAUDE_TOOL_OUTPUT`），在 WorkBuddy 等 harness 上静默失效；
   建议改为「stdin JSON 解析 + 可配置事件名」。
4. `extract-skill.sh` 默认输出 `./skills`，与本机 `~/.workbuddy/skills` 不符。
5. `Quick Status Check` 的 `grep` 在 Windows / 受限 shell 下不可移植；frontmatter 另有一处悬空 `metadata:` 空键。

## 五、沉淀

- 新技能 `~/.workbuddy/skills/skill-env-consistency-audit/SKILL.md`（agent_created）：把本次方法固化为**五步法**
  —— 摸文件构成 → 抽断言 → 逐条实测 → **hook 可用性取证** → 区分「能改 / 不可改」。
  含本次的 hook 契约取证手法与「skillhub 技能不可改」判据。
- **通用判据**：装了第三方技能后，**「技能说它能做」不等于「本机它会做」**；
  凡涉及 hook / 环境变量 / 绝对路径的断言，必须真跑一次才算验证过。

## 相关

- [[raven-install-windows-native]] — 同批「本机工具链」实测，方法一致（逐条实测取代自述）
- [[github-knowledge-base-options]] — 同一环境下的通路选型记录
