# 索引

> 本文件由 `tools/build_index.py` 自动生成，**请勿手改**。
> 最后更新:2026-09-28 · 共 31 篇

## 业务与立项(`business`) · 28 篇

- [AWS Agent Toolkit · 安装与验证记录（2026-09-26）](notes/business/AWS-Agent-Toolkit-安装记录.md) — --- `stable`
- [AWS 支持工具能力普查 · A/B/C/D 交叉审计结论](notes/business/aws-support-tooling-probe-audit.md) — 一句话结论：A（真伪）未发现伪造、C（越界）0 越界、D（面覆盖）抓出 2 个真实缺漏，但 B（可复现）因宿主 shell 崩溃而根本没执行——本轮验收的「可证… `growing`
- [AWS 支持工具能力普查 · 两路真值源逐命名空间差异](notes/business/aws-support-tooling-probe-inventory-diff.md) — 一句话结论：CLI 侧（aws <ns> help）与模型侧（botocore service-2.json）逐命名空间比对，12 个正向命名空间里 9 个一致… `growing`
- [AWS 支持工具能力普查 · 两轮缺陷审计与修复判定（D-1…D-22）](notes/business/aws-support-tooling-probe-defects.md) — 一句话结论：独立验证方两轮共登记 22 条缺陷（第一轮 D-1…D-12，第二轮 D-13…D-22），第二轮对第一轮逐项复审、撤回 1 条误判、确认 4 项修… `growing`
- [AWS 支持工具能力普查 · 探测设计与契约（2026-09-27）](notes/business/aws-support-tooling-probe-design.md) — 一句话结论：这次探测把「某云厂商支持工具能不能用」做成了可证伪的工程题——办法是「一份契约 + 两路互相独立的服务清单真值源 + 每个操作原始响应全量落盘 + … `growing`
- [AWS 支持工具能力普查 · 补参重跑与真实可达性](notes/business/aws-support-tooling-probe-param-fill.md) — 一句话结论：对 130 条「只读且必填参数 >0」的操作自动补参后重跑，「实际被调用」从 3 条跃升到 124 条、service_error 从 2 条增到 … `growing`
- [AWS 支持服务工具 · API 实测报告（两轮：2026-09-25 / 09-26）](notes/business/AWS支持服务工具-API实测报告.md) — --- `stable`
- [AWS 支持服务工具 · AWS Health](notes/business/AWS支持服务工具-AWS-Health.md) — AWS Health 的事件（Event）用于告知服务与资源变更如何影响你的应用。 `growing`
- [AWS 支持服务工具 · IDR 与 AI 增强层](notes/business/AWS支持服务工具-IDR与AI增强.md) — --- `growing`
- [AWS 支持服务工具 · SAW 与 Slack](notes/business/AWS支持服务工具-SAW与Slack.md) `growing`
- [AWS 支持服务工具 · Support API 与工单](notes/business/AWS支持服务工具-Support-API与工单.md) — 见 AWS支持服务工具-Trusted-Advisor。 `growing`
- [AWS 支持服务工具 · Trusted Advisor](notes/business/AWS支持服务工具-Trusted-Advisor.md) — Priority 是什么：由你的 AWS 账户团队提供的情境驱动、按优先级排序的建议 —— `growing`
- [AWS 支持服务配套工具 · 体验报告（2026-09-25）](notes/business/AWS支持服务配套工具-体验报告.md) — 报告日期：2026-09-25 `stable`
- [AWS 支持服务配套工具体系 · 手册总览](notes/business/AWS支持服务工具-手册总览.md) — AWS 的支持服务不是「一个工单系统」，而是「数据层 + 服务层 + AI 层」三层叠加的工具体系 —— `stable`
- [AWS 支持计划 33 张单能力 BA 卡片（交付主体视角）](notes/business/aws-support-plans-ba-cards.md) — 结论：把 BA 六视图下钻到每一项能力（33 张卡片），四档形态表填的是「由谁交付」而不是「有没有」；汇总结构数据显示 —— 33 项里有 16 项在 BS+ … `growing`
- [AWS 支持计划 33 项能力 × 四档逐项取值](notes/business/aws-support-plans-33-capabilities.md) — 结论：四档的分档轴不是「支持量大小」而是「工作负载的失效后果等级」（Default → Production → Business-critical → Mis… `growing`
- [AWS 支持计划 BA 业务架构逆向（六视图）](notes/business/aws-support-plans-ba-architecture.md) — 结论：用华为 4A 的 BA（业务架构）视角对 AWS 支持计划做逆向工程，得到一条可迁移的核心范式 —— 「档位 = 交付主体等级的封装包」，价格差异不是按「… `growing`
- [AWS 支持计划能力基线与实测证据（Business Support+）](notes/business/aws-support-plans-baseline.md) — 结论：AWS 支持计划已于 re:Invent 2025 重构为四档（Basic / Business Support+ / Enterprise / Unif… `growing`
- [EDR 立项汇报 PPT 索引（33 页 deck）](notes/business/edr-proposal-deck-index.md) — 结论：EDR（事件检测与响应）立项汇报 deck 已成稿，33 页，用 slidep DSL 生产，源为 slides/01–33.slide；大二进制不进 G… `growing`
- [EDR立项 · 云厂商支持服务文档库索引](notes/business/EDR立项-AWS竞品分析资料包索引.md) — 本地 Markdown 合计 6.4 MB，PDF 存档合计 39.4 MB。 `growing`
- [华为云支持服务「三级梯度 × 四项立项」汇报交付包索引](notes/business/huawei-support-four-proposals-deck.md) — 结论：本批立项汇报的战略视野从「单产品 EDR」提升到「三级梯度 × 四项立项」，deck 定稿 27 页（正文 26 + 备份 1）、汇报 30–35 分钟；… `growing`
- [华为云支持服务立项 · AWS 竞品对标](notes/business/华为云支持服务立项-AWS竞品对标.md) — 不是一个产品，是三层叠起来的体系： `growing`
- [华为云支持服务立项 · EDR 产品定义](notes/business/华为云支持服务立项-EDR产品定义.md) — 管理面（平台运维事件、计划内变更、群障/区域故障）数据链路已验证连通（2026-09-21 确认）。 `growing`
- [华为云支持服务立项 · 产品序列与收入路径](notes/business/华为云支持服务立项-产品序列与收入路径.md) — ⇒ 官网最高等级「企业级」SLA 是 ＜10 分钟；内部规划的「尊享级」要求 ＜5 分钟。 `growing`
- [华为云支持服务立项 · 总览](notes/business/华为云支持服务立项-总览.md) — 一套支持服务（Support Service）产品的立项组合，核心是把华为公有云的 `growing`
- [华为云支持服务立项 · 材料清单与路线图](notes/business/华为云支持服务立项-材料清单与路线图.md) — 理由：12 号给出全貌（三级梯度 × 四项立项），先立框架，再填内容， `growing`
- [华为云支持服务立项 · 立项二三（VIP TAC 与 昇腾950）](notes/business/华为云支持服务立项-立项二三产品定义.md) — AWS Unified Operations（$50,000/月起）/ AWS IDR（$7,000/月起） `growing`
- [昇腾950立项 · 官方语料索引](notes/business/昇腾950立项-官方语料索引.md) — 已归档位置：D:/AI/my_project/cloud-support-docs/huawei/ `growing`

## 工具链与自动化(`tooling`) · 3 篇

- [GitHub 初始化知识库的方案对比](notes/tooling/github-knowledge-base-options.md) — 最值得抄的不是某个笔记软件，而是 TIL（Today I Learned）范式——直接把 GitHub 仓库当知识库，因为 GitHub 已免费提供文件系统、M… `growing`
- [Raven（Windows 原生）安装与卸载记录 · v0.2.3](notes/tooling/raven-install-windows-native.md) — 一句话结论：Raven v0.2.3 在 Windows 上用 uv tool install 装成功、四个内置插件全部 activated；真正的坑不在 Ra… `growing`
- [技能一致性体检 · 把技能里的「实测」断言逐条真跑（2026-09-27）](notes/tooling/skill-env-consistency-audit-20260927.md) — 一句话结论：体检方法是「把 SKILL.md 里每一条『实测』断言拆出来、逐条对本机真跑一次」；结果是自建的 multi-agent-cli-orchestra… `growing`

> 空领域(待填充):`ai`, `infra`, `reading`, `life`
