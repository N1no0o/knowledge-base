---
title: GitHub 初始化知识库的方案对比
tags: [github, knowledge-base, til, pkm]
created: 2026-09-25
updated: 2026-09-25
source: https://github.com/jbranchaud/til
status: growing
---

最值得抄的不是某个笔记软件，而是 **TIL（Today I Learned）范式**——直接把 GitHub 仓库当知识库，因为 GitHub 已免费提供文件系统、Markdown 渲染、全文搜索、历史版本、权限控制与 AI 接口。

## 五条路线（★ 为 2026-09-25 实测）

| 路线 | 代表仓库 | ★ | 增量成本 | 适合 |
|---|---|---|---|---|
| TIL 极简 | jbranchaud/til | 14154 | 建 repo + 目录 + 索引 | 零依赖，日常够用 |
| 加自动化 | simonw/til | 1458 | 加 Actions 重建索引并发布 | 笔记上百篇后 |
| 加 AI 维护 | tieubao/til | 75 | 加 AGENTS.md 四工作流 | 长期积累 |
| 换前端 | Obsidian + obsidian-git | 12035 | 装软件 + 插件 | 要双链与图谱 |
| 只做发布 | Quartz | 13281 | 加构建配置 | 要公开站点 |

## 关键判据

- **GitHub 自带全文搜索** → 数千篇规模内不需要自建搜索引擎
- **下划线开头的目录会被 Jekyll 自动忽略** → 用 `_inbox` / `_templates` / `_docs` 天然隔离框架与内容
- **Obsidian wikilink 按文件名解析、与路径无关** → 领域目录可以随时重构而不破坏链接
- **`AGENTS.md` 作唯一 agent 入口**，`CLAUDE.md` 只写一行 `@AGENTS.md`，规则只有一份、兼容多 agent
- **编辑优先于检索**（compilation over retrieval）——平时就把知识编译成互链结构，而不是提问时临时翻找

## 避坑

- `obsidian-dataview`（9358★）最后更新停在 2025-11，**已停更约 10 个月**，新项目别重度依赖
- 自托管系统（Trilium 37965★ / Outline 40694★ / 思源 46489★）功能强，但要常驻服务、数据进私有数据库，与"GitHub 原生"目标相反

## 相关

- 本仓库的落地规范见 `AGENTS.md`
- 设计理由见 `_docs/architecture.md`
