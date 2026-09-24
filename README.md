# 知识库

个人知识库。**纯 Markdown + Git 版本管理 + AI 协作维护**。

- 内容源：`notes/<领域>/` 下一个知识点一个文件
- 全文搜索：直接用 GitHub 仓库内搜索（按 `/` 或 `s`）
- 历史版本：每篇笔记的每次修改都可回溯
- AI 协作：规则写在 [`AGENTS.md`](AGENTS.md)，AI 负责整理、链接、索引、体检

## 快速开始

```bash
git clone <你的仓库地址> knowledge-base
cd knowledge-base
python tools/build_index.py     # 重建索引
```

## 目录结构

| 路径 | 作用 |
|---|---|
| `_inbox/` | 原始落地区，未整理的东西先扔这里 |
| `notes/<领域>/` | 已编译的知识，**唯一的内容层** |
| `_templates/` | 4 类笔记模板 |
| `_docs/` | 架构与使用说明 |
| `tools/` | 自动化脚本 |
| `index.md` | 全量索引（自动生成，勿手改） |
| `log.md` | 操作日志（追加式） |
| `AGENTS.md` | AI 维护规则，**唯一 agent 入口** |

内容领域：`ai` · `business` · `infra` · `tooling` · `reading` · `life`

## 对 AI 说什么

| 你说 | AI 执行 |
|---|---|
| 「把这段存进知识库」 | ingest：去重 → 落盘 → 更索引 → 记日志 |
| 「整理一下」「compile」 | compile：补双向链接、合并重复、提升 status |
| 「从知识库找一下 X」 | query：查 index → 综合回答 → 有价值的答案回填成笔记 |
| 「体检」「lint」 | lint：孤儿、断链、过时、无来源，只报告不删除 |

## 写笔记的约定

三段式：**一句话结论 → 要点/原理 → 相关链接**。
文件名用英文连字符（`rag-chunking.md`），中文标题放 frontmatter 的 `title`。

## 自动化

- `.github/workflows/build-index.yml` — 每次 push 自动重建 `index.md` 并回提交
- `.github/workflows/pages.yml` — 自动发布到 GitHub Pages

---

_本仓库采用 TIL（Today I Learned）范式：GitHub 本身就是知识库，不额外套笔记软件。_
