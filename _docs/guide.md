# 日常操作手册

## 每天怎么用

### 1. 随手记 → `_inbox/`

想到什么先扔 `_inbox/`，不用管格式。这一步刻意零门槛。

### 2. 让 AI 整理

对 AI 说：

> 把 `_inbox` 里的东西存进知识库

AI 会按 `AGENTS.md` 的 ingest 流程执行：判领域 → 查重 → 落盘到 `notes/` → 更索引 → 记日志。

### 3. 直接提问

> 从知识库找一下：代理节点轮换是怎么防止 IP 被封的？

AI 会先查 `index.md` 定位，再综合回答，并标注依据的笔记。**有价值的回答会被回填成新笔记**。

## 常用指令对照

| 你说 | AI 做什么 |
|---|---|
| 「存进知识库」「记一下」 | ingest |
| 「整理一下」「compile」 | compile：补链接、合并重复、提升 status |
| 「从知识库找 X」 | query |
| 「体检」「lint」 | 生成健康报告（只报告不删） |

## 手动操作

```bash
# 重建索引
python tools/build_index.py

# 只检查不写入（lint 用）
python tools/build_index.py --check
```

## 接入 Obsidian（可选）

1. 用 Obsidian 打开本仓库目录作为 vault
2. 设置 → 文件与链接 → 勾选「使用 [[Wikilinks]]」
3. 装 `obsidian-git` 插件，配置自动 commit + push
4. 之后本地写笔记会自动同步到 GitHub

> 注意：Obsidian 的配置（`.obsidian/`）会一并提交，但缓存和 workspace 状态已在 `.gitignore` 里排除。

## 搜笔记的几种方式

1. **GitHub 网页**：仓库内按 `/` 打开搜索框
2. **`index.md`**：所有笔记 + 一行摘要，AI 和人都先看这个
3. **本地**：`grep -r "关键词" notes/`（有 Git Bash 的话）
4. **AI**：直接问，AI 会先查 index

## 给笔记定 status

| status | 含义 | 什么时候用 |
|---|---|---|
| `seedling` | 幼苗 | 刚记下，还没验证或没链接 |
| `growing` | 成长 | 已验证，有入链，可能还会补充 |
| `evergreen` | 常青 | 结论稳定，可长期引用 |

`lint` 会提醒超过 180 天还停在 `seedling` 的笔记——要么提升，要么归档。

## 新增领域

1. 建目录 `notes/<新领域>/`
2. **同时**在 `tools/build_index.py` 的 `AREAS` 里登记中文名
3. 跑一次 `python tools/build_index.py`

漏了第 2 步的话，新目录的笔记不会出现在 `index.md` 里。
