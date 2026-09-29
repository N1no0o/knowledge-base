---
title: 代理节点轮换技能（proxy-node-rotation）打包索引
tags: [代理节点, 轮换, v2rayN, xray, 阿里云, ECS, 技能, 索引]
created: 2026-09-28
updated: 2026-09-28
source: dist/proxy-node-rotation.zip（46.2 KB，2026-09-16 22:37）｜原件 D:/AI/my_project/dist/proxy-node-rotation.zip
status: growing
---

# 代理节点轮换技能（proxy-node-rotation）打包索引

**一句话结论：这是一份可复用的 **WorkBuddy 技能包**——把「阿里云 ECS 上 v2rayN/xray 节点轮换」的整套流程（SKILL.md + 配置样例 + 环境/坑位/配置格式三份参考 + 一个 Python CLI）打成了一个 46 KB 的 zip；大二进制不进 Git，本页只登记包内构成与本地位置。**

## 一、包内构成（17 个条目 / 解压后 113.7 KB）

| 路径 | 作用 |
|---|---|
| `proxy-node-rotation/SKILL.md` | 技能入口（触发词、流程、约束） |
| `assets/rotation.config.example.json` | **配置样例**（实际配置不含在包内，需自行派生） |
| `references/environment.md` | 环境说明 |
| `references/pitfalls.md` | ⭐ **坑位清单**（价值最高的一份） |
| `references/v2rayn-schema.md` | v2rayN 配置格式说明 |
| `scripts/run.py` | 脚本入口 |
| `scripts/ecsproxy/` | Python 包，11 个模块：`cli` / `config` / `ecs` / `errors` / `node` / `rotate` / `tasks` / `v2rayn` / `xraycore` / `__init__` / `__main__` |

> 模块划分显示它是一条完整链路：**ECS 侧操作（`ecs`）→ 节点管理（`node`）→ 轮换编排（`rotate`）→ xray 核心与 v2rayN 配置改写（`xraycore`/`v2rayn`）→ 任务调度（`tasks`）**。

## 二、与运行时环境的关系

- 后端：**阿里云 ECS**（`ap-southeast-1`，详见 `references/environment.md`）；
- 客户端：**v2rayN / xray**（配置格式见 `references/v2rayn-schema.md`）；
- ⚠️ **实际配置文件不在包内** —— 包内只有 `rotation.config.example.json`，真实配置与凭据需另行落地（**不要提交进任何公开仓库**）。

## 三、本地绝对路径

```
D:/AI/my_project/dist/proxy-node-rotation.zip          ← 打包件（权威快照）
```

> 工作副本/已解包目录若存在，通常是同名目录；本页以 zip 快照为准。

## 四、为什么只写索引笔记

`.zip` 属二进制大件，按 `AGENTS.md` §3.5 **不进 Git、只写索引笔记**（记清包里有什么、体积、本地绝对路径、生成时间）；
本页即为该索引，原包**只读不删**。

## 相关

- [[华为云支持服务立项-总览]] — 同一工作区产出，但属不同主题（本页为基础设施侧）
- [[dsh-plugin-ecosystem]] — 同为本机工具链侧的资产登记；两页共同构成"本机自建能力"索引
- [[github-knowledge-base-options]] — 知识库自身的搭建方案（本页所依据的归档规则的来源）
