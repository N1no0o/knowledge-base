---
title: 达芬奇 Resolve 免费版 · 脚本自动化能力边界（P0/P1/P2 实测）
tags: [达芬奇, DaVinci Resolve, 视频自动化, 渲染队列, ffmpeg, 调色, 码率控制]
created: 2026-11-09
updated: 2026-11-09
source: D:/AI/my_project/deliverables/video-pipeline/resolve-capability-analysis-2026-11-08.md（13.0 KB，2026-11-08 17:35）
status: growing
---

# 达芬奇 Resolve 免费版 · 脚本自动化能力边界

**一句话结论：达芬奇免费版的外部脚本接口（`scriptapp`）封死，但「工作区 → 脚本」内部脚本可用，能全自动渲染出片；代价是码率不可控、调色 API 不可用，因此它只做「剪辑 + 渲母版」，调色与交付规格交给 ffmpeg。**

## 一、版本与前置条件（本机实测）

| 项 | 实测 |
|---|---|
| 版本 | DaVinci Resolve **21.2.0.6**，装在 `D:\Davinci\`（非 Program Files） |
| 授权 | **免费版**（`ProductName` 无 Studio 后缀；`Support\License` 下无激活文件） |
| 脚本 SDK | 随装 `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`（含 `DaVinciResolveScript.py` / `.pyi` / 20 个示例） |
| 桥接库 | `D:\Davinci\fusionscript.dll` |
| 外部脚本 | `scriptapp("Resolve")` 返回 `None` ⇒ 偏好设置「外部脚本使用」仍为 `None`，需要人点一次改成 `本地` |

**关键分界：外部脚本封死 ≠ 不能自动化。** 走内部脚本（`工作区 → 脚本 → Utility → xxx`）即可，代价是每次必须人点一次脚本菜单，做不到零点击。

## 二、已跑通的渲染链路（P0，全程无人工干预除首点）

```
SaveProject → CreateProject → ImportMedia(2×4K) → CreateEmptyTimeline
→ AppendToTimeline → SetCurrentRenderFormatAndCodec(mp4/H264)
→ SetRenderSettings → AddRenderJob → StartRendering({job})
```

产物 `p0_test.mp4`：33.4 MB / **3.97 s** 渲完 / 1920×1080 60 fps / H.264 Main / yuv420p 8 bit bt709 / AAC 48 kHz / ≈67 Mbps。

## 三、四条硬约束（都有实测触发条件）

| 约束 | 证据 | 应对 |
|---|---|---|
| **`io` / `os` / `dofile` / `load` 全为 `nil`** | 内部脚本读不了 `shots.json`、打不了时间戳 | **生成阶段把数据内联进 Lua**（`_gen_resolve_p1.py` 做法） |
| **`AppendToTimeline` 的 `endFrame` 是排他语义** | 日志 `Finished recording 11752 frames`，期望 11780，正好每段少 1 帧（28 段）；成片 195.88 s vs 计划 196.33 s | `endFrame = startFrame + frames`；**官方示例 7 注释「endFrame=23 即 24 帧」是错的** |
| **不显式设 `VideoQuality` 会飙到 245 Mbps** | 196 s 成片 **6.02 GB**，不可交付；设 `"High"` 仍 67 Mbps | 数值型 `VideoQuality = 20000`（但见下条——实际被忽略） |
| **免费版 H.264 只能 8 bit yuv420p** | 10 bit / HDR / HEVC 主 10 属 Studio | 发布够用；10 bit 交付才需 Studio |

## 四、码率控制：确认无效，改两段式交付

同一 10 秒片段分别用 `VideoQuality = "Medium"` / `20000` / `8000` 渲染，**三个文件字节数完全相同（151,843,839 B ≈ 121 Mbps）** ⇒ 该参数被忽略，不是写错。

> ⚠️ 方法论教训：早前一次「三条样本一致」的**1 帧**测试是无效实验（1 帧物理上无法体现码率差异），不能当证据。**必须整条实渲**才能定性。

兜底方案（已实测）：Resolve 只出母版，ffmpeg 转交付规格。

```
ffmpeg -i p1b_landscape.mp4 -c:v h264_nvenc -b:v 20M -maxrate 25M -bufsize 50M \
       -c:a aac -b:a 192k final_20m.mp4
```

6 GB 母版 → **490 MB / 19.7 Mbps / 1080p60 / 196.35 s**，耗时 **33 秒**。

## 五、调色：Resolve 内三条路都不通，改 ffmpeg

| 尝试 | 结果 |
|---|---|
| `TimelineItem:ApplyAutoColor()` | 样片与原始**肉眼无差别**（免费版未生效或极弱） |
| `TimelineItem:SetCDL(Slope/Offset/Power/Saturation)` | **画面直接变红**，单位/作用空间与预期不符 |
| 自定义 3D LUT + `SetLUT` | 仅 ±3% 色温增益，R−B 从 **−18.7 漂到 +25**，天空变土黄 |
| **ffmpeg 滤镜链** | 6 点抽样：Y 87.2→96.9、R−B −15.2→−2.0、过曝 1.26%→0.81%、死黑 0.54%→0.37% ⇒ **采用** |

最终滤镜链：

```
colorchannelmixer=rr=1.08:bb=0.93,
curves=all='0/0 0.2/0.235 0.5/0.57 0.8/0.85 1/0.98',
eq=saturation=1.10
```

**为什么放 ffmpeg**：① 语义确定（显式通道增益 / 显式控制点，无单位歧义）；② 可离线迭代（先在 10 秒片段量化 + 目视，再跑全片；Resolve 内每次试错都要人点一次脚本、等一次渲染）；③ 与转码合并，无额外耗时（调色 + 转码 + 编码合计 41 秒）。

## 六、性能账（RTX 5070 Ti / 8 核 16 线程 / 47.2 GB）

| 阶段 | 耗时 |
|---|---|
| 导入 21 条 4K + 建时间线 | 1–2 分钟（一次性，随素材数线性增长） |
| Resolve 渲染 196 s 成片 | **65–71 秒（≈2.75–3× 实时）** |
| ffmpeg 转码到 20 Mbps | **33 秒**（NVENC） |
| **合计** | **约 100 秒出可交付文件** |

派生结论：**渲染不是瓶颈，导入 + 建时间线才是纯渲染外的主要开销**。

## 七、两个顺带踩到的坑

- **素材实际偏冷**（R−B ≈ −15 ~ −19，天空 R−B ≈ −52）。此前统计脚本把 BGR 通道写反，一度误判为「偏暖」，方向差点搞反。
- **NVENC 输出像素格式**：RGB 滤镜链之后不加 `-pix_fmt yuv420p`，会输出 `yuv444p / High 4:4:4 Predictive`，多数平台不可用。**必须固定加**。

## 八、路线判定

- **正片归达芬奇**：调色由 ffmpeg 承担、渲染免人工导出，边际价值成立。
- **竖屏优先归剪映**：达芬奇的 `SmartReframe` 疑似 Studio 限定，免费版调用通常返回 `False`，**未实测前不算能力**。
- 真痛点其实是竖屏主体裁切，两边都没解干净 —— 解法是自写「主体感知裁切」（OpenCV 跟踪人脸/运动重心做逐镜偏移），与选哪个 NLE 无关，属独立待办。

## 九、待验证清单

- [ ] 免费版 `SmartReframe` / `SmartReframeStatus` 是否可用（决定竖屏归属）
- [ ] 免费版 `VoiceIsolation` 是否可用（可用则音频后期可再升一档）
- [ ] `CreateSubtitlesFromAudio` 免费版是否可用、中文识别质量
- [ ] 外部脚本 `Local` 与 `Network` 差异（本机单机 → `Local` 足够）

## 相关

- [[video-pipeline-action5pro-douyin-automation]] — 整条徒步剪辑流水线与双引擎分工的当前态（本页是其达芬奇引擎的能力底账）
- [[vp-preaudit-material-inventory]] — 进 NLE 之前的素材盘点口径
- [[jianying-draft-automation-route]] — 另一引擎（剪映草稿自动化）的路线与踩坑
