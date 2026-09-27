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
├── _kb_state/       产出件同步账本（ingested.json 进 Git；pending.json 不进）
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

### 3.5 sync — 产出件增量同步

**触发**：定时任务「知识库每日同步」，或用户说"同步产出件""把今天的产出归档"

日复一日地把 `D:/AI/my_project` 下新产生的资料性文档编译进库。**幂等**：靠 `_kb_state/ingested.json` 账本去重，跑多少次结果一致。

```bash
python tools/kb_scan.py          # ① 输出待处理清单（--all 全量，--status 只看统计）
#                              # ② ← 这一步由 agent 做：编译成笔记
python tools/kb_scan.py --mark "<源文件绝对路径>" --note "notes/<领域>/<文件名>.md"  # ③ 逐件记账
python tools/build_index.py      # ④ 重建索引
#                              # ⑤ 追加 log.md
python tools/kb_push.py -F _commit_msg.txt   # ⑥ 推送 GitHub（无凭据时只本地）
```

**第 ② 步的判断规则：**

| 产出件类型 | 处理方式 |
|---|---|
| `.md` 报告 / 方案 / 纪要（< 40 KB） | 按 §2 格式编译成 `notes/<领域>/` 笔记：保留结论与要点，删过程性叙述 |
| `.md` 大报告（≥ 40 KB） | 拆：核心结论单独成篇，细节留在 `source:` 指向的原件，笔记里只写「结论 + 关键数据 + 指向」 |
| `.zip` / `.pptx` / `.pdf` / `.xlsx` | **不进 Git**。写一篇索引笔记，记清包里有什么、体积、本地绝对路径、生成时间 |
| `slidep` 工程的 `STORY.md` / `DESIGN.md` | 属 PPT 源材料，不是交付物 ⇒ 加进 `_kb_state/ignore.txt`，或只在既有笔记里补一行链接 |
| 分支版本（`-v2` `-v3` `-final`） | 只收最新版；旧版在 `_kb_state/ignore.txt` 里排除 |

**领域归属**（`notes/` 下的目录）：立项 / 方案 / 竞品 / 客户 → `business`；服务器 / 网络 / 云 / 代理 → `infra`；
脚本 / 工具链 / 自动化 → `tooling`；大模型 / agent / 提示词 → `ai`；读书笔记 → `reading`；其余 → `life`。

**硬规则：**

1. **先查重再新建** —— 在 `notes/` 里搜主题词，已有同主题笔记就**更新它**，别新建重复页
2. 单次执行**最多处理 8 件**，按 `mtime` 倒序（新的先归档），余量留给下一次
3. 每处理完一件立刻 `--mark` 记账；**没真正落成笔记的不许 mark**（账本是账，不是待办清单）
4. `_kb_state/ignore.txt` 是人工判定区 —— agent 可以**建议**新增排除项，但不要自行把该排除的文件 mark 掉
5. 大二进制永远不进 Git：`.gitignore` 与 `kb_push.py` 的 2 MiB 上限是双保险
6. 涉及未公开经营数据 / 客户信息的产出件，归档前先问人

## 4. 硬规则

1. `index.md` 由脚本生成 —— **禁止手改**，改了会在下次构建时被覆盖
2. 每次写操作后必须：跑索引脚本 + 追加 `log.md`
3. 不删除 `source` 字段，不删除原始剪藏（归档到 `_inbox/_archived/` 而非删除）
4. 一篇笔记只讲一件事。超过 300 行的笔记应拆
5. 日期一律用 `YYYY-MM-DD`
6. 不确定的内容标 `status: seedling` 并在正文写「待验证」，**不要伪装成结论**

## 5. 维护脚本

```bash
python tools/build_index.py                  # 重建 index.md 与 search-index.json
python tools/build_index.py --check          # 只检查不写入（lint 用）

python tools/kb_scan.py                      # 扫描 agent 产出件，输出待处理清单
python tools/kb_scan.py --status             # 账本 / 可扫描数 / 已消失源文件
python tools/kb_scan.py --mark <src> --note <rel>   # 记账

python tools/kb_push.py                      # 推送到 GitHub（自动 commit message）
python tools/kb_push.py --dry-run            # 只看会推哪些文件
python tools/kb_push.py --verify-only        # 比对远端与本地一致性
```

新增 `notes/` 下的领域目录时，在 `tools/build_index.py` 的 `AREAS` 字典里加一行，否则不会被计入索引。

**推送凭据**：`kb_push.py` 依次从 `GH_PAT` / `N1NO_PAT` 环境变量、`D:/AI/my_project/.secrets/gh_pat_n1no`
读取 token（见该目录 `README.md`）。**token 永远不写进脚本、日志、笔记、报告。**
退出码：`0` 成功 · `1` 推送失败 · `2` 校验不一致 · `3` 未配置凭据（此时本地整理仍然有效）。

> ⚠️ **返回 3 = 凭据不在位，不是网络被拦，也没有第二条推路径**（2026-09-27 实测，2026-09-28 复核）：
> 本机 `git ls-remote` / `git fetch` 全部 rc=0（网络正常）；`git push` 报 `could not read Username`（零凭据）；
> **GitHub 连接器是「只读 App」—— 所有写接口一律 `403 Resource not accessible by integration`，不能用它推送，也不要重复试。**
> ⇒ **推送只走 `kb_push.py`**。返回 3 时：本地整理照常完成，但**必须在结果开头显式标注「⚠️ 远端未推送」**
> 并给出修复动作 = 把 fine-grained PAT（需 `Contents: Read and write`）整行粘进 `.secrets/gh_pat_n1no`；
> **不要重试、不要换路子、不要试图改用连接器。**
> （历史注记：本节曾错误建议退回连接器推送，该结论已被 `403` 实测证伪，故删除。）

---

_本文件是仓库的唯一 agent 入口。`CLAUDE.md` 只是一行导入。_
