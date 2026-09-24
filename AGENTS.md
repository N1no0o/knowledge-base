# AGENTS.md — 知识库维护规则

> 这是本仓库**唯一的 agent 入口**。任何 AI(WorkBuddy / Claude Code / Codex / Cursor)在本仓库工作时，必须先读本文件。

## 0. 角色分工

**人负责策展，AI 负责记账。**

- 人：决定什么值得记录、判断对错、提出好问题
- AI：整理、归类、交叉链接、更新索引、查重、体检

**编译优先于检索（compilation over retrieval）。** 不要每次提问都临时翻文件；要把知识持续"编译"成互链的结构，让下一次提问直接可用。

## 1. 仓库结构

```
.
├── _inbox/          原始落地区：未整理的剪藏、随手记、待处理素材
├── notes/           已编译的知识（唯一的内容层）
│   ├── ai/          大模型、agent、提示词
│   ├── business/    业务、立项、方案、客户、竞品
│   ├── infra/       服务器、网络、云、代理节点
│   ├── tooling/     工具链、脚本、自动化
│   ├── reading/     阅读摘录、文章笔记
│   └── life/        生活、资料、备忘
├── _templates/      笔记模板（4 类）
├── _docs/           架构与使用说明
├── tools/           自动化脚本
├── index.md         全量索引（AI 自动生成，不要手改）
├── log.md           操作日志（追加式）
└── AGENTS.md        本文件
```

**框架与内容分离**：根目录只放框架文件，所有内容一律进 `notes/<领域>/`。
新增领域目录时，必须同时在 `tools/build_index.py` 的 `AREAS` 里登记（见 §5）。

## 2. 笔记格式（强制）

每个 `.md` 必须有 frontmatter：

```yaml
---
title: 人类可读的标题
tags: [标签1, 标签2]
created: 2026-09-25
updated: 2026-09-25
source: 来源链接或说明（原创就写 "original"）
status: seedling        # seedling 幼苗 / growing 成长 / evergreen 常青
---
```

正文用**三段式**：

1. **一句话结论** — 第一行就必须是结论，不要铺垫
2. **要点 / 原理** — 支撑结论的证据、步骤、代码
3. **相关** — `[[双向链接]]` 到其他笔记

文件名规则：小写英文 + 连字符（`rag-chunking.md`），中文标题放 frontmatter 的 `title`。
理由：wikilink 按**文件名**解析（与路径无关，可以放心重组目录），英文文件名跨平台最稳。

## 3. 四个工作流

### 3.1 ingest — 摄取

**触发**：用户说"存入知识库""记一下""process inbox""收进库"

1. 读取 `_inbox/` 或用户给定的原始内容
2. 判断：属于哪个领域？是否与已有笔记重复？
3. **去重检查先做** —— 在 `notes/` 里搜关键词，若已有同主题笔记，**更新旧笔记**而不是新建
4. 按 §2 格式写成 `notes/<领域>/<文件名>.md`，`status: seedling`
5. 原始来源保留在 `source:` 字段，**不要删掉出处**
6. 跑 `python tools/build_index.py`
7. 向 `log.md` 追加一行

### 3.2 compile — 编译

**触发**："compile""整理一下""re-ingest"

1. 扫描 `status: seedling` 的笔记
2. 对每篇：补 `[[双向链接]]`、合并重复、标注矛盾
3. 若某主题累计 ≥5 篇，考虑写一篇**综合页**（synthesis）引用它们
4. 提升 `status` 到 `growing` / `evergreen`
5. 更新 `index.md` 与 `log.md`

### 3.3 query — 查询

**触发**：用户提问，或"从知识库找""answer from the wiki"

1. **先查 `index.md`** 定位候选，不要盲目遍历全部目录
2. 读候选笔记，综合回答
3. 回答里用 `[[文件名]]` 标注依据
4. **如果这个回答有价值 → 回填成新笔记**（这是本仓库增值的关键动作）
5. 追加 `log.md`

### 3.4 lint — 体检

**触发**："lint""体检""检查知识库"

检查并报告：

- **孤儿笔记**：没有任何入链
- **断链**：`[[xxx]]` 指向不存在的文件
- **过时内容**：`updated` 超过 180 天且 `status` 仍是 `seedling`
- **无来源**：`source` 为空
- **索引漂移**：`index.md` 与实际文件不符

**只报告，不擅自删除。** 删除必须经人工确认。

## 4. 硬规则

1. `index.md` 由脚本生成 —— **禁止手改**，改了会在下次构建时被覆盖
2. 每次写操作后必须：跑索引脚本 + 追加 `log.md`
3. 不删除 `source` 字段，不删除原始剪藏（归档到 `_inbox/_archived/` 而非删除）
4. 一篇笔记只讲一件事。超过 300 行的笔记应拆
5. 日期一律用 `YYYY-MM-DD`
6. 不确定的内容标 `status: seedling` 并在正文写「待验证」，**不要伪装成结论**

## 5. 维护脚本

```bash
python tools/build_index.py          # 重建 index.md 与 search-index.json
python tools/build_index.py --check  # 只检查不写入（lint 用）
```

新增 `notes/` 下的领域目录时，在 `tools/build_index.py` 的 `AREAS` 字典里加一行，否则不会被计入索引。

---

_本文件是仓库的唯一 agent 入口。`CLAUDE.md` 只是一行导入。_
