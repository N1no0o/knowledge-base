---
title: 《徒步中国》50 条路线轨迹包 · 交付包与产物索引
tags: [徒步, GPX, 交付包索引, 产物清单, 开放数据, 户外]
created: 2026-10-13
updated: 2026-10-14
source: D:/AI/my_project/hiking-50/（index.html / index.md / README.md / *.zip，2026-10-13 12:21）
status: growing
---

# 《徒步中国》50 条路线轨迹包 · 交付包与产物索引

**一句话结论：这是一个「路线索引页 + 轨迹文件 + 打包 zip」三件式交付包（合计约 7.7 MB，zip 1.0 MB / 52 条目）；结论见 [[hiking-china-50-routes-gpx-pack]]，本篇只做「包里有什么、在哪、多大」的索引登记，**4 件产物均不进 Git**。**

## 一、入库登记的 4 件产物

| 文件 | 类型 | 体积 | 进 Git |
|---|---|---|---|
| `hiking-50/index.html` | 总览页（可离线打开） | 27.4 KB | ❌ |
| `hiking-50/index.md` | 同内容 Markdown 版（周表 + 许可 + 用法） | 9.8 KB | ❌ |
| `hiking-50/徒步中国50条路线-公开轨迹包.zip` | 打包交付件（**52 条目**，含 index.html/md/README.md + 全部 gpx/kml） | 1,002.3 KB | ❌ |
| `hiking-50/README.md` | 包说明（扫描器 `EXCLUDE_FILES` 内，**未单独入账**，内容已由本索引篇与结论篇覆盖） | 3.4 KB | — |

**生成 / 取数时间**：2026-10-13 12:21–12:22 · **本地绝对路径**：`D:/AI/my_project/hiking-50/`

## 二、包内构成（未逐件入库，登记备查）

```
hiking-50/
├── index.html / index.md      ← 总览（同一内容的两种版式）
├── 徒步中国50条路线-公开轨迹包.zip
├── gpx/hongkong/   19 个文件（4.67 MB）  ← 中国香港四径，CC0-1.0
└── gpx/osm/        30 个文件（2.97 MB）  ← OpenStreetMap 匹配路线，ODbL-1.0
```

- `gpx/` 合计 **49 个文件 / 7.64 MB**（另含 `_LICENSE-CC0.txt` 许可原文）。
- `_work/`（**中间件，不入库**）：17 个文件 / 6.97 MB —— 含 OSM 拉取与匹配脚本（`fetch_osm_regions.py` / `match_and_fetch.py` / `fix_missing.py` / `probe_route.py` / `check_links.py` 等）、`hk.zip`（6.48 MB 上游原始包）、若干 manifest/names json。中间件目录名以 `_` 开头，被扫描器规则排除。

## 三、数据来源与许可

| 来源 | 许可 | 要求 |
|---|---|---|
| OpenStreetMap（`gpx/osm/`） | **ODbL 1.0** | 署名 © OpenStreetMap 贡献者 + 保持同一许可 |
| `nicholas-fong/Hong-Kong-Trails-GPX-KML`（`gpx/hongkong/`） | **CC0 1.0** | 无附加限制 |

OSM 数据快照 **2026-05-06**；取数时间 2026-10-13。

## 四、复现方式（要点）

1. 取图书公开书目中的 50 条路线名；
2. 到 OSM 按名称匹配 + 坐标落区校验，命中后导出 GPX/KML；
3. 里程按「相邻点跳变 > 2 km 不计入」过滤后重算（校验样本见结论篇）；
4. 未配到的 30 条给出两步路检索词，由使用者自行下载（`.htm` 改名 `.kml`）。

## 相关

- [[hiking-china-50-routes-gpx-pack]] — 本交付包的**结论篇**（覆盖情况、匹配等级三档、里程口径、许可铁律、用法）
- [[howtolivebetter-kit-index]] — 同属「公开资料整理成交付包」类（三件套形态）
