---
title: Raven（Windows 原生）安装与卸载记录 · v0.2.3
tags: [Windows, uv, 工具链, 沙箱, Playwright, 批量删除守卫, 安装记录]
created: 2026-09-28
updated: 2026-09-28
source: D:/AI/my_project/dist/raven-install/raven-install-report-2026-09-27.md（本机实测，2026-09-27）
status: growing
---

# Raven（Windows 原生）安装与卸载记录 · v0.2.3

**一句话结论：Raven v0.2.3 在 Windows 上用 `uv tool install` 装成功、四个内置插件全部 activated；真正的坑不在 Raven 本身，而在「uv 缓存 / PowerShell 脚本缺陷 / 沙箱代理」三处环境障碍——装完当天即卸载，回收约 1.03 GB。**

## 一、安装结果（成功面）

| 项 | 值 |
|---|---|
| 版本 | v0.2.3 |
| 可执行文件 | `~/.local/bin/raven.exe`（用户 PATH 已含，无需改） |
| 安装方式 | `uv tool install`（独立 venv，`%APPDATA%\uv\tools\raven`，179 个依赖包） |
| 插件 | `design-engine` / `everos-memory` / `playbook` / `ppt-engine` 全部 `activated`；默认 memory backend = `everos` |
| 浏览器运行时 | `%LOCALAPPDATA%\ms-playwright\chromium-1234`（playwright 1.62） |
| 配置目录 | `~/.raven`（`config.json` 需跑 `raven onboard` 才生成） |

`raven doctor` 在未 onboard 时报 `Raven is not configured` —— **属预期状态，不是安装失败**。
`raven onboard` 是七步交互向导（provider→sandbox→channel→memory→web→sub-agents→import），**非交互环境跑不了**，必须人工执行。

## 二、三个真实障碍与修法（本记录的核心价值）

### 障碍 A：uv 缓存路径踩「批量删除守卫」→ 依赖编译被掐死

- **现象**：`jieba==0.42.1` 编译失败，构建后端 `rc=1`，但 **stderr 只有警告、没有报错**，紧随
  `[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED] {"count":98,"threshold":50,"scope":"turn"}`。
- **经验修法**：安装/升级前重定向 uv 缓存，
  `$env:UV_CACHE_DIR = Join-Path $env:LOCALAPPDATA "Temp\uv-cache"` → 同包一次构建成功。
  `raven upgrade` 走同一条链路，**同样必须设**。
- ⚠️ **归因要如实**：初版报告写的「uv 缓存不在 `delete: allow` 白名单」已被证伪——
  `~/appdata/local/uv/` 与 `~/appdata/roaming/uv/` 两条规则都是 `delete: allow`，
  且 `uv tool uninstall raven` 在 allowlisted 路径下一次删 16471 文件**完全没触发守卫**。
  ⇒ **精确触发条件未定**，重定向是「经验有效」而非「已证根因」。

### 障碍 B：官方 `install.ps1` 的三处缺陷

| 缺陷 | 表现 | 规避 |
|---|---|---|
| `Invoke-WebRequest` 取插件清单**未设超时** | 卡在 `github.com` TLS 上**永久挂起**（实测 PID 挂 17 分钟、CPU 仅 0.6s） | 自行带 `-TimeoutSec` 下载 `raven-plugins.txt` / `raven-constraints.txt` |
| 结尾默认 `raven web --foreground` | 前台起服务**占住会话、永不返回** | `RAVEN_NO_LAUNCH=1` |
| LibreOffice 走 `Read-Host` | 非交互环境可能挂起 | `RAVEN_MINIMAL=1`，事后单独装 |

另：`$ErrorActionPreference="Stop"` + PowerShell 的 `*>` 重定向会把 uv 打到 stderr 的进度信息
包装成终止性错误 `NativeCommandError` ⇒ **不要用 `*>` 重定向安装脚本输出**，改用 OS 级重定向或看后台任务 stdout/stderr。

### 障碍 C：沙箱代理与镜像选型

- 沙箱内 **`github.com`（含 `/releases/download/`）与 `codeload.github.com` 连不上**；
  `api.github.com`、`raw.githubusercontent.com` 正常 ⇒ Raven 的 wheel 全托管在 release 页，**安装必须在沙箱外执行**。
- `cdn.playwright.dev` 仅 ~123–146 KB/s（201 MB 要 ~27 分钟）；换
  `$env:PLAYWRIGHT_DOWNLOAD_HOST = "https://cdn.npmmirror.com/binaries/playwright"`
  可达 **12–15 MB/s（快约 100 倍，同一文件同一长度）**。

## 三、卸载记录（官方文档未覆盖）

```powershell
uv tool uninstall raven      # 实测 rc=0，一次删掉 3 样
```

- 一次清除：工具 venv（16471 文件 / 603 MB，**三个插件因同 venv 一并消失**）、`~/.local/bin/raven.exe`、uv tool receipt。
- ⏱️ **耗时约 9.5 分钟且全程无输出**（Windows 删 1.6 万小文件 + 杀软扫描）——**看着像卡死其实在正常删**。
  判据：目录文件数持续下降（实测 45 秒 −2512 文件 / −44.9 MB）。
- **需单独处理的残留**：`~/.raven`（712 文件 / 6.2 MB）、`%LOCALAPPDATA%\Temp\uv-cache`（28652 文件 / 980 MB）、
  `ms-playwright\chromium-1234` + `chromium_headless_shell-1234`（697 MB，**同目录的 `chromium-1217` 等属其他工具，别一起删**）。
- 合计回收约 **1.03 GB**（不含 chromium）。

## 四、可复现命令（沙箱外执行）

```powershell
$env:UV_CACHE_DIR             = Join-Path $env:LOCALAPPDATA "Temp\uv-cache"
$env:RAVEN_NO_LAUNCH          = "1"
$env:RAVEN_MINIMAL            = "1"
$env:PLAYWRIGHT_DOWNLOAD_HOST = "https://cdn.npmmirror.com/binaries/playwright"
irm https://raw.githubusercontent.com/EverMind-AI/Raven/refs/heads/main/install.ps1 | iex
```

## 相关

- [[skill-env-consistency-audit-20260927]] — 同批「本机工具链体检」，同样以「逐条实测取代技能自述」为方法
- [[github-knowledge-base-options]] — 同一环境下的 GitHub 通路选择
