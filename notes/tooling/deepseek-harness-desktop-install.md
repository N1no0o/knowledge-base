---
title: DeepSeek Harness Desktop 安装记录 · v0.1.7-rc.2
tags: [Windows, DeepSeek, dsh, NSIS, 安装记录, 工具链, PowerShell]
created: 2026-09-28
updated: 2026-09-28
source: dist/deepseek-harness-desktop/安装记录.md（3.8 KB，2026-09-27 10:45）｜原件 D:/AI/my_project/dist/deepseek-harness-desktop/
status: growing
---

# DeepSeek Harness Desktop 安装记录 · v0.1.7-rc.2

**一句话结论：装成功了，但整个过程最值得记住的不是产品本身，而是那个**反直觉的坑** —— 在 Git Bash 里给 NSIS 安装器传 `/D=` 会被 MSYS 篡改路径，安装器**rc=2 静默退出、不产生任何日志或目录**；必须改用 PowerShell `Start-Process`。**

## 一、安装结果

| 项 | 值 |
|---|---|
| 产品 | DeepSeek Harness Desktop（Electron 桌面壳 + 内置 `dsh` 运行时） |
| 版本 | **0.1.7-rc.2**（Nightly 通道） |
| 安装路径 | **`D:\Deepseek-Harness`** |
| 体量 | 9,767 文件 / 1,009.8 MB |
| 启动入口 | `D:\Deepseek-Harness\DeepSeek Harness.exe` |
| 卸载器 / 命令 | `"D:\Deepseek-Harness\Uninstall DeepSeek Harness.exe" /currentuser` |
| 安装范围 | 仅当前用户（`perMachine=false`，**无需管理员**） |
| 内置 Electron | 44.0.0 |
| 默认端口 | 桌面端 **19387**（Web 版 3080） |

注册表卸载项：`HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\1bf39983-50d0-5fe0-9ef4-cece76f67c5e`

## 二、安装包来源与校验

**官方分发域名不是 GitHub Releases**（Releases 里全是无附件的 prerelease）：

```
https://download.deepseek.com/dsh-desk/feeds/win-x64/nightly.yml
→ https://download.deepseek.com/dsh-desk/bin/win-x64/deepseek-harness-0.1.7-rc.2-win-x64.exe
   size   : 288,245,480 B
   sha512 : AY7f45dYO7BFrfgaLmzXNWP0pavlxkSbsehPo/WF6PXcFdDK3fF1oHUPs/4f2bzROgQvm6wSgawZ/g7UzbPRmw==
```

**实测 sha512 与官方 feed 完全一致（MATCH=True）。** 数字签名（Authenticode）：

| 项 | 值 |
|---|---|
| Status | **Valid** |
| Subject | `CN=Hangzhou DeepSeek Artificial Intelligence Co., Ltd., C=CN` |
| Issuer | `CN=GlobalSign GCC R45 EV CodeSigning CA 2020, O=GlobalSign nv-sa` |
| 有效期至 | 2027-09-01 |
| Thumbprint | `84032578657219876E273E0D1BD303CFE1B82E6F` |

> 未签名测试版命名为 `...-win-x64-unsigned.exe`；本包**无 `unsigned` 后缀**，属正式签名产物。

## 三、⭐ 核心坑：Git Bash 会破坏 NSIS 的 `/D=`

**MSYS/Git Bash 会篡改 NSIS 的 `/D=` 参数**，导致安装器判定路径非法并**立即以 exit code 2 退出，且不产生任何日志或目录**。**`MSYS_NO_PATHCONV=1` 拦不住。**

| 命令 | 结果 |
|---|---|
| `installer.exe /S` | rc=0，装到默认 `%LOCALAPPDATA%\Programs\DeepSeek Harness` |
| `installer.exe /S /D=C:\Temp\dsh-probe`（Git Bash） | **rc=2**，拒绝 |
| `installer.exe /S /D=D:\Deepseek-Harness`（Git Bash） | **rc=2**，拒绝 |
| **PowerShell `Start-Process -ArgumentList '/S','/D=D:\Deepseek-Harness'`** | ✅ **成功** |

> **结论：Windows 上给 NSIS 安装器传 `/D=`，一律用 PowerShell `Start-Process`（或 cmd），不要经 Git Bash。**
> 其他可用参数：`/THEME=light|dark|auto`、`/KEEP_APP_DATA`、`--updated`（升级替换时保留用户数据）。

## 四、用户数据（安装/卸载都不碰）

- **Harness home：`~/.dsh`** —— 本次安装前**已存在**（2026-08-23 建立，含 `.credentials.yaml`、`settings.yaml`、`sessions`、`storages`、`profiles`），安装与卸载均**不会触碰**。
- 桌面端独占 profile：`~/.dsh/profiles/desktop`。
- 首次启动会做 profile 初始化与内置运行时准备（`$DSH_HOME/dsh-runtimes/dsh-primary-runtime`），**可能耗时，属正常**。

## 五、残留与备份

| 位置 | 内容 | 处理建议 |
|---|---|---|
| `D:\_quarantine\deepseek-harness-src-20260927-104106\deepseek-harness` | 原先占用 `D:\Deepseek-Harness` 的**源码克隆**（commit `47f9438`，2026-08-13，165.5 MB / 7,440 文件，git 状态干净） | 确认无需后自行删除；随时可重 `git clone` |
| `D:\AI\my_project\_dsh_probe\installer\deepseek-harness-0.1.7-rc.2-win-x64.exe` | 官方安装包原文件（275 MB） | 保留可离线重装/回滚 |

## 六、升级方式

桌面端内置自动更新（**Nightly 固定通道**，启动时异步检查，基频 10 分钟 ±20% 抖动），也可用界面菜单的 **Check for Updates** 手动检查。升级走同源 `download.deepseek.com`，**原地更新、用户数据保留**。

## 相关

- [[dsh-plugin-ecosystem]] — 装完之后：插件版本兼容闸门、可安装清单与「设置 → 插件」唯一通路
- [[raven-install-windows-native]] — 同为 Windows 工具链安装记录，两篇共通的教训是"**静默失败先怀疑参数传递/环境层，别先怀疑产品**"
- [[windows-shortcut-ghost-cleanup]] — 同批 Windows 环境治理笔记
