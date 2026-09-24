---
title: EDR立项 · 云厂商支持服务文档库索引
tags: [AWS, 阿里云, 竞品, 语料库, 索引, 支持服务]
created: 2026-09-25
updated: 2026-09-25
source: 「AWS竞品分析资料包-20260921.zip」(380篇) + 「03-华为支持计划+阿里云Markdown.zip」等｜归档 2026-09-25
status: growing
---

# EDR立项 · 云厂商支持服务文档库索引

> **这是索引笔记，不是正文。** 原始 PDF / HTML 快照 / 逐页 Markdown 均为大体量二进制与语料，
> 存放在**语料库**而非本知识库仓库。

## 语料在哪

| 语料库 | 路径 | 规模 | 自带索引 |
|---|---|---|---|
| **云厂商支持服务文档库** | `D:/AI/my_project/cloud-support-docs/` | **3996 文件 / 108.5 MB** | ✅ `README.md` + `_fetch_report.json` + `index.html` |
| **阿里云卓越架构** | `D:/AI/my_project/aliyun-well-architected/` | **1168 文件 / 11.6 MB** | ✅ `README.md` + `官方目录清单.md`（81KB） |

## cloud-support-docs 内容构成

> 面向华为云「支持服务」产品**竞品对标**的官方文档归档。全部抓取自官方站点，
> 逐页转 Markdown 便于全文检索，同时保留官方 PDF 整册作为原始存档。

### 总览

| 厂商 | 文档集 | Markdown 页数 | 官方 PDF |
|---|---|---|---|
| AWS | 8 个指南 | 957 | 8 份整册 |
| 阿里云 | 2 个文档集 | 172 | — |
| **合计** | **10** | **1129** | **8** |

本地 Markdown 合计 **6.4 MB**，PDF 存档合计 **39.4 MB**。

### AWS 文档集（8 个）

| 指南 | 页数 |
|---|---|
| **AWS Support 用户指南** | 168 |
| **AWS Well-Architected Framework** | 475 |
| **AWS Well-Architected Tool** | 108 |
| **AWS Support API 参考** | 51 |
| **AWS Health 用户指南** | 46 |
| **AWS Health API 参考** | 40 |
| **AWS Incident Detection and Response** | 39 |
| **AWS Service Quotas 用户指南** | 30 |

> ⭐ **竞品对标核心**：`aws-incident-detection-response/` = AWS IDR 的官方文档，
> 是 EDR 立项的**直接对标对象**（见 [[华为云支持服务立项-AWS竞品对标]]）。

### 目录结构

```
cloud-support-docs/
├── README.md              # 总索引
├── _fetch_report.json     # 抓取报告（页数/失败项）
├── _raw/                  # 原始 HTML 快照（1143 项，可重跑可核对）
├── aws/                   # 1002 项
│   ├── NNN-*.md           # 逐页 Markdown
│   ├── _pdf/              # 官方 PDF 整册（8 份）
│   └── _website/          # 官网产品页/定价页
└── aliyun/                # 177 项
    ├── aliyun-support-plans/
    └── _website/
```

## AWS 竞品分析资料包（380 篇，独立来源）

腾讯文档另有一份 `AWS竞品分析资料包-20260921.zip`（380 篇 md，2.6 MB）。
这份是**针对本立项的分析产出**（非原始抓取），与 `cloud-support-docs` 互补：

- `cloud-support-docs` = 官方文档原样抓取（**原始证据**）
- `AWS竞品分析资料包` = 已加工的分析结论（**可直接引用**）

**分析结论的精华已提炼进** [[华为云支持服务立项-AWS竞品对标]]。

## 怎么用

1. **查官方原文** → 进 `cloud-support-docs/<厂商>/<指南>/NNN-*.md`
2. **查本立项的分析结论** → 看 [[华为云支持服务立项-AWS竞品对标]]
3. **核对抓取完整性** → 看 `_fetch_report.json`（含失败项）
4. **重跑抓取** → `_raw/` 保留原始 HTML 快照，可重新转换

> ⚠️ **引用纪律**：这些是**竞品官方事实**，可直接引用于立项材料与答辩。
> 但注意区分「官方承诺」与「厂商自报」（如 AWS 的 MTTR 降低 75% 属自报数据，见竞品笔记）。

---

## 关联笔记

- [[华为云支持服务立项-AWS竞品对标]] — 六维度速查（从本语料提炼）
- [[华为云支持服务立项-总览]] — 立项纲领
- [[华为云支持服务立项-EDR产品定义]] — IDR 是直接对标
- [[昇腾950立项-官方语料索引]] — 华为侧语料
