---
title: 竞品语料库 cloud-support-docs（打包快照索引）
tags: [语料库, 竞品, AWS, 阿里云, 索引, 离库归档]
created: 2026-09-28
updated: 2026-09-28
source: dist/cloud-support-docs.zip（33,619.9 KB，2026-09-17 00:57）+ dist/AWS与阿里云支持服务文档.zip（2,507.4 KB，2026-09-17 00:59）｜原件 D:/AI/my_project/dist/
status: growing
---

# 竞品语料库 cloud-support-docs（打包快照索引）

**一句话结论：`cloud-support-docs/` 是立项竞品分析的**一手语料库**（AWS + 阿里云官方文档与产品页的全量抓取），因体量大而**明确排除在知识库 Git 之外**（`kb_scan.py` 的 `EXCLUDE_DIRS` 已含 `cloud-support-docs`）；本页只登记它的**两个 zip 快照位置与体量**，供需要时定位。**

## 一、两个 zip 的关系（一个是大全集、一个是子集）

| zip | 压缩后 | 解压后 | 条目 | 判定 |
|---|---|---|---|---|
| **`cloud-support-docs.zip`** | **33.6 MB** | **47.2 MB** | **1159** | ✅ **全集（权威快照）** |
| `AWS与阿里云支持服务文档.zip` | 2.5 MB | 6.8 MB | 1150 | ❌ **已取代**（同一 `cloud-support-docs/` 树，但内容量只有约 1/7） |

> 两者内部路径前缀相同（均解压出 `cloud-support-docs/`），**后者是大全集裁掉大部内容后的精简包**，不是不同语料。
> ⇒ 取用时**一律用 `cloud-support-docs.zip`**。

## 二、语料库结构（以全集为准）

```
cloud-support-docs/
├── README.md
├── _fetch_report.json        ← 抓取报告（来源与数量）
├── index.html
├── aliyun/
│   ├── aliyun-advisor/       000-产品概述 … 034-分页获取最新巡检结果（智能顾问全量文档）
│   ├── aliyun-support-plans/ 阿里云支持计划（含产品计费、服务条款）
│   └── …（其余阿里云产品）
└── aws/                      见下
```

**AWS 侧的分区**（立项材料 03/11 号的直接素材来源）：

| 分区 | 内容 |
|---|---|
| `aws/aws-incident-detection-response/` | IDR 官方文档 **38 篇**（含 002-Architecture、003-Roles-and-responsibilities、007-Onboard-with-the-IDR-CLI、031-Monitoring、032-Incident-management、036-Reporting） |
| `aws/aws-health-user-guide/`、`aws-health-api-reference/` | AWS Health |
| `aws/aws-support-user-guide/`、`aws-support-api-reference/` | AWS Support |
| `aws/aws-well-architected-framework/`、`aws-well-architected-tool/` | Well-Architected |
| `aws/_website/` | **23 篇官网产品页/定价页**（含 `aws-support-pricing.md`、`aws-devops-agent*.md` 四件套） |
| `aws/_pdf/` | **9 本官方 PDF 全文** |

> 📌 **在线工作副本**：`D:/AI/my_project/cloud-support-docs/`（未打包的目录形态，体量大、不进 Git）。
> 另有同目录 `aliyun-well-architected/` 也属语料库，同样被排除。

## 三、本地绝对路径

```
D:/AI/my_project/dist/cloud-support-docs.zip              ← 全集快照（权威）
D:/AI/my_project/dist/AWS与阿里云支持服务文档.zip          ← 子集快照（已取代，保留备用）
D:/AI/my_project/cloud-support-docs/                      ← 未打包的工作副本目录
```

## 四、为什么它不进 Git

- 全集解压后 **47 MB / 1159 文件**，远超索引仓库的合理体量；
- `kb_scan.py` 的 `EXCLUDE_DIRS` 里显式列了 `cloud-support-docs` 与 `aliyun-well-architected`（注释：*语料库，体量大且不进 Git*）；
- 知识库里**只建指向它的索引笔记**（本页 + [[华为云支持服务立项-AWS竞品对标]] 的"数据出处"），语料本身留在本地。

## 相关

- [[华为云支持服务立项-AWS竞品对标]] — 从本语料库提炼的 AWS 三层体系与定价结论
- [[EDR立项-AWS竞品分析资料包索引]] — 另一份 AWS 竞品资料包（380 篇）的索引
- [[华为云支持服务立项-总览]] — 立项纲领（语料库服务的上游目标）
