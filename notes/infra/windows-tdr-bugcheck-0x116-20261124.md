---
title: 意外重启定案：NVIDIA 621.24 驱动 TDR 恢复失败（BugCheck 0x116）现场诊断法
tags: [Windows, 崩溃诊断, BugCheck, 0x116, TDR, 显卡驱动, WER, RTX5070Ti, 排障]
created: 2026-11-25
updated: 2026-11-25
source: deliverables/diagnostics/2026-11-24-windows-crash-bugcheck-0x116.md（6.0 KB，2026-11-24 23:34）｜原件 D:/AI/my_project/deliverables/diagnostics/2026-11-24-windows-crash-bugcheck-0x116.md
status: growing
---

# 意外重启定案：NVIDIA 621.24 驱动 TDR 恢复失败（BugCheck 0x116）

**一句话结论：无蓝屏界面的"自动重启"不是电源故障、也不是 Windows Update，本次直接原因是显卡驱动 TDR 恢复失败触发内核 BugCheck 0x116（VIDEO_TDR_ERROR，参数 3 = `0xC000009A` STATUS_INSUFFICIENT_RESOURCES）；深层原因是 NVIDIA 621.24 在 RTX 5070 Ti + 双 2K 高刷链路上的持续性不稳 —— 该版驱动 11-07 生效后 17 天内 3 次致命崩溃，且 11-19 重装同版本无效，因此处置方向是「回退驱动」而非「重装驱动」。**

## 一、判据链：怎么把"意外重启"定到显卡驱动

诊断的关键不是读蓝屏，而是**先证明"没有蓝屏界面"这件事本身是证据**：0x116 在 TDR 恢复失败时直接重启，用户看不到蓝屏。

| 环节 | 判据 | 本次实测值 |
|---|---|---|
| 排除"正常关机/更新重启" | 无 Event **1074**；Event **6008** = "上一次关机是意外的" | 6008 存在、1074 缺失 |
| 确认内核级崩溃 | Event **1001**(WER) 带 BugCheck 码 + minidump 路径 | `0x00000116`，`C:\WINDOWS\Minidump\112426-10218-01.dmp` |
| 定位到图形栈 | BugCheck 参数 3 的 NTSTATUS | `0xC000009A` = STATUS_INSUFFICIENT_RESOURCES ⇒ TDR **恢复**阶段资源不足 |
| 排除硬件随机性 | **WHEA-Logger 近 30 天 0 条** | 无 CPU/内存/总线机器检查异常 |

> 0x116 的参数 3 是分水岭：`0xC000009A` 说明 GPU 已超时、驱动尝试重置失败，属"软件栈恢复不动"；若伴随 WHEA 记录或 0x124，才轮到硬件方向。

## 二、核心证据：WER ReportQueue 的内核报告分布

`C:\ProgramData\Microsoft\Windows\WER\ReportQueue` 里按 `Kernel_` 前缀目录统计 BugCheck 码，比只看 System 日志更能反映"长期病根"：

| BugCheck | 含义 | 次数 |
|---|---|---|
| 0x1B8 | VIDEO_MINIPORT_BLACK_SCREEN_LIVEDUMP | **34** |
| 0x141 | VIDEO_ENGINE_TIMEOUT_DETECTED | 11 |
| 0x116 | VIDEO_TDR_ERROR（致命） | 2 |
| 0x133 | DPC_WATCHDOG_VIOLATION | 1 |
| 0x1A8 | VIDEO_DXGKRNL_BLACK_SCREEN_LIVEDUMP | 1 |
| 0x193 | VIDEO_DXGKRNL_LIVEDUMP | 1 |

**合计 50 条全部落在图形栈**，无一条指向存储、网络、USB 或内存控制器。

**这是本条最可迁移的判断方法**：0x1B8/0x141 属 **live dump（不致命）**，日常只表现为瞬时黑屏/显示恢复、不打断使用，极易被忽略；0x116 是同一病根的致命终端。⇒ **"偶尔闪一下黑屏"与"某天突然自动重启"是同一件事的两个严重度**，排障时应当把 live dump 计数当预警指标。

## 三、时间线（相关性定因）

| 时间 | 事件 |
|---|---|
| 2026-08-08 12:05 | BugCheck 0x3B（孤立，基线偶发） |
| **2026-11-07 08:00** | NVIDIA **621.24** 生效（oem105.inf `DriverVer = 11/07/2026, 32.0.16.2124`） |
| 2026-11-07 14:03 | BugCheck 0xD1（DRIVER_IRQL_NOT_LESS_OR_EQUAL，装完 6 小时内首崩） |
| 2026-11-19 21:42 / 21:57 | 0x116 首次致命崩溃 / 0x133 DPC_WATCHDOG_VIOLATION |
| 2026-11-19 22:17–22:22 | **重装同版本 621.24**（Installer2 / nvmdi.inf 目录创建于该时段） |
| **2026-11-24 23:28:29** | 系统意外关闭 → 23:29:06 启动 → Kernel-Power 41 → WER 1001 记 0x116 |

⇒ **"重装同版本无效"是排除"安装损坏"、锁定"版本缺陷"的决定性一步**。同样的推理：若重装有效，则问题在安装完整性；重装无效而时间相关性仍在，则问题在版本本身。

## 四、已排除项（含一处自我纠错）

| 怀疑方向 | 核查结果 |
|---|---|
| Windows Update 自动重启 | 11-23/11-24 仅 Defender 病毒库 + Store 应用更新，无驱动/累积更新；无 1074 |
| 用户/程序发起重启 | 无 1074，6008 明确"意外关闭" |
| 断电 / 电源故障 | 除 Kernel-Power 41 无其他断电特征，重启后 BIOS 时间正常 |
| CPU/内存硬件错误 | WHEA-Logger 30 天 **0 条** |
| 驱动文件缺失/损坏 | `nvlddmkm.sys` 在 `DriverStore\FileRepository\nvmdi.inf_amd64_6792e5c6f4ec2d9d\`（102 MB），服务 Running。**早期"文件缺失"判断为误判，已纠正** |
| Event 219 驱动加载失败 | 全部指向 HP HID 外设（VID_03F0），与显卡无关 |
| 系统文件损坏 | 未做 SFC/DISM，无证据，非首要方向 |

> 教训：**DCH 驱动由服务从 DriverStore 直接加载，`System32\drivers` 里查不到 `nvlddmkm.sys` 属正常形态** —— 不能用"文件不在 System32"推断驱动缺失。

## 五、剩余嫌疑（按置信度）

1. **NVIDIA 621.24 版本缺陷（高）** — 时间相关性最强：生效当日首崩、17 天 3 崩、重装无效。
2. **双 2K 高刷显示链路（中）** — 主屏 2560×1440@**299Hz** + 异构第二屏，DSC 链路压力大，是 0x1B8 黑屏转储的常见诱因。
3. **DDR5 EXPO 6000 超频（中低）** — 2×24GB 双面颗粒在 B850 双 DIMM 跑 6000 属边界工况，可解释 0xD1/0x3B，**不解释 34 次黑屏转储**。
4. **BIOS 偏旧（中低）** — 1065 为 2025-06 版本，此后 AGESA 对 RTX 50 系列兼容性多次修订。
5. **GPU 供电/硬件（低，不可排除）** — 无 WHEA，软件层排除后再交叉验证。

## 六、处置顺序（性价比排序，每步都可当对照实验）

1. **DDU 安全模式干净卸载 + 回退到 621.24 之前的 WHQL 分支**，并关闭 NVIDIA App 自动更新驱动。（最高优先；"干净卸载"与"普通卸载"的区别就在这里 —— 后者会留下旧栈残片，导致重装等于没装。）
2. **降显示链路压力做对照**：主屏 299Hz → 240Hz，或临时单屏 1–2 天。黑屏转储停止 ⇒ 链路嫌疑确认。
3. **内存回归 JEDEC**：BIOS 关 EXPO 跑 5600 + `mdsched.exe` 满 4 轮。无改善 ⇒ 排除内存。
4. **升级主板 BIOS**（TUF B850M-PLUS WIFI，含 AGESA 修订），升级前记录当前设置。
5. **硬件交叉验证**（前三步无效时）：查 12V-2×6 供电插接/换线，有条件换卡或换电源。

## 七、取证命令（可直接复用）

```powershell
# 崩溃清单（90 天）
Get-WinEvent -FilterHashtable @{LogName='System'; ID=1001; StartTime=(Get-Date).AddDays(-90)}

# WER 内核报告按 BugCheck 码聚合 —— 找"长期病根"最有效的一招
Get-ChildItem 'C:\ProgramData\Microsoft\Windows\WER\ReportQueue' -Directory |
  Where-Object Name -match '^Kernel_' | Group-Object { ($_.Name -split '_')[1] } |
  Select-Object Count, Name

# 显示驱动重置（TDR）事件
Get-WinEvent -FilterHashtable @{LogName='System'; ID=4101} -MaxEvents 20
```

## 八、局限

- `C:\Windows\Minidump` 与 `C:\Windows\LiveKernelReports` **需管理员权限**；本次在非提权会话完成，**转储内部模块栈未解析**。事件层证据已足以定因，但若要确认具体出错的驱动模块（`nvlddmkm+0x...`），仍需提权跑一次 `!analyze -v`。
- 本次为单机样本（ASUS TUF B850M-PLUS WIFI / RTX 5070 Ti / 48GB DDR5-6000 / BIOS 1065），**"621.24 有缺陷"是这台机器的强相关结论，不是该版本的普适定论**。

## 相关

- [[windows-shortcut-ghost-cleanup]] — 同属 Windows 本机排障，判据同样是"看实际状态而不是猜测方向"
- [[raven-install-windows-native]] — Windows 本机安装/驱动栈操作的同类踩坑记录
