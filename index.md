# 索引

> 本文件由 `tools/build_index.py` 自动生成，**请勿手改**。
> 最后更新:2026-10-01 · 共 52 篇

## 业务与立项(`business`) · 44 篇

- [AWS Agent Toolkit · 安装与验证记录（2026-09-26）](notes/business/AWS-Agent-Toolkit-安装记录.md) — --- `evergreen`
- [AWS Countdown / IDR / AMS 深度分析 v2 · 新旧模型质量对照与三条实质结论](notes/business/aws-countdown-idr-ams-deep-dive-v2.md) — 一句话结论：用新模型把 09-27（v1 旧模型）对同一批冻结语料的深度分析完整重做，三份报告评级 B/B/C → A/A/B、缺陷总数 21（P0 3）→ 1… `growing`
- [AWS 支持工具能力普查 v3 · 交付包与支撑件索引](notes/business/aws-support-tooling-probe-v3-deck-index.md) — 一句话结论：v3 真实调用轮交付件 = 1 份 HTML 报告（48.5 KB）+ 1 份同名 Markdown（24.1 KB），支撑件为工作区 aws-su… `growing`
- [AWS 支持工具能力普查 · A/B/C/D 交叉审计结论](notes/business/aws-support-tooling-probe-audit.md) — 一句话结论：A（真伪）未发现伪造、C（越界）0 越界、D（面覆盖）抓出 2 个真实缺漏，但 B（可复现）因宿主 shell 崩溃而根本没执行——本轮验收的「可证… `growing`
- [AWS 支持工具能力普查 · v3 真实调用轮结论](notes/business/aws-support-tooling-probe-v3-realrun.md) — 一句话结论：v3 把 09-28 离线版里 6 项「本轮未做」全部补上，首次拿到真实 API 调用数据 —— 工具面 13 个命名空间 / 407 op / 2… `growing`
- [AWS 支持工具能力普查 · 两路真值源逐命名空间差异](notes/business/aws-support-tooling-probe-inventory-diff.md) — 一句话结论：CLI 侧（aws <ns> help）与模型侧（botocore service-2.json）逐命名空间比对，12 个正向命名空间里 9 个一致… `growing`
- [AWS 支持工具能力普查 · 两轮缺陷审计与修复判定（D-1…D-22）](notes/business/aws-support-tooling-probe-defects.md) — 一句话结论：独立验证方两轮共登记 22 条缺陷（第一轮 D-1…D-12，第二轮 D-13…D-22），第二轮对第一轮逐项复审、撤回 1 条误判、确认 4 项修… `growing`
- [AWS 支持工具能力普查 · 探测设计与契约（2026-09-27）](notes/business/aws-support-tooling-probe-design.md) — 一句话结论：这次探测把「某云厂商支持工具能不能用」做成了可证伪的工程题——办法是「一份契约 + 两路互相独立的服务清单真值源 + 每个操作原始响应全量落盘 + … `growing`
- [AWS 支持工具能力普查 · 补参重跑与真实可达性](notes/business/aws-support-tooling-probe-param-fill.md) — 一句话结论：对 130 条「只读且必填参数 >0」的操作自动补参后重跑，「实际被调用」从 3 条跃升到 124 条、service_error 从 2 条增到 … `growing`
- [AWS 支持工具面实测与竞品分析 · 三堵墙与六家工具面全景](notes/business/competitive-analysis-aws-support-tooling.md) — 一句话结论：AWS 支持工具面的真实边界不在「有没有 API」，而在三堵墙 —— ①档位墙（核心工具卡 Business+ 起）②组织墙（14+ 条 Acces… `growing`
- [AWS 支持服务全套重做 · 09-28 总览（凭据卡死轮次）](notes/business/aws-support-full-rerun-overview.md) — 一句话结论：用新模型（gpt-6-astra）把 AWS 支持服务全套 4 条线重做，2 条跑通、2 条被 AWS 凭据卡死；跑通的两条各抓到 v1 一个真实错… `growing`
- [AWS 支持服务全套重做 · 09-29 真实调用轮总览](notes/business/aws-support-real-run-overview.md) — 一句话结论：凭据恢复后把 09-28 被卡死的 A / C 两条线真跑通了 —— v1 的 4 条运行期结论首次被真跑证实、0 条被推翻；唯一负面项是 A 线 … `growing`
- [AWS 支持服务工具 · API 实测报告（两轮：2026-09-25 / 09-26）](notes/business/AWS支持服务工具-API实测报告.md) — --- `evergreen`
- [AWS 支持服务工具 · AWS Health](notes/business/AWS支持服务工具-AWS-Health.md) — AWS Health 的事件（Event）用于告知服务与资源变更如何影响你的应用。 `growing`
- [AWS 支持服务工具 · IDR 与 AI 增强层](notes/business/AWS支持服务工具-IDR与AI增强.md) — --- `growing`
- [AWS 支持服务工具 · SAW 与 Slack](notes/business/AWS支持服务工具-SAW与Slack.md) `growing`
- [AWS 支持服务工具 · Support API 与工单](notes/business/AWS支持服务工具-Support-API与工单.md) — 见 AWS支持服务工具-Trusted-Advisor。 `growing`
- [AWS 支持服务工具 · Trusted Advisor](notes/business/AWS支持服务工具-Trusted-Advisor.md) — Priority 是什么：由你的 AWS 账户团队提供的情境驱动、按优先级排序的建议 —— `growing`
- [AWS 支持服务配套工具 · 体验报告（2026-09-25）](notes/business/AWS支持服务配套工具-体验报告.md) — 报告日期：2026-09-25 `evergreen`
- [AWS 支持服务配套工具体系 · 手册总览](notes/business/AWS支持服务工具-手册总览.md) — AWS 的支持服务不是「一个工单系统」，而是「数据层 + 服务层 + AI 层」三层叠加的工具体系 —— `evergreen`
- [AWS 支持计划 33 张单能力 BA 卡片（交付主体视角）](notes/business/aws-support-plans-ba-cards.md) — 结论：把 BA 六视图下钻到每一项能力（33 张卡片），四档形态表填的是「由谁交付」而不是「有没有」；汇总结构数据显示 —— 33 项里有 16 项在 BS+ … `growing`
- [AWS 支持计划 33 项能力 × 四档逐项取值](notes/business/aws-support-plans-33-capabilities.md) — 结论：四档的分档轴不是「支持量大小」而是「工作负载的失效后果等级」（Default → Production → Business-critical → Mis… `growing`
- [AWS 支持计划 BA 业务架构逆向（六视图）](notes/business/aws-support-plans-ba-architecture.md) — 结论：用华为 4A 的 BA（业务架构）视角对 AWS 支持计划做逆向工程，得到一条可迁移的核心范式 —— 「档位 = 交付主体等级的封装包」，价格差异不是按「… `growing`
- [AWS 支持计划能力基线与实测证据（Business Support+）](notes/business/aws-support-plans-baseline.md) — 结论：AWS 支持计划已于 re:Invent 2025 重构为四档（Basic / Business Support+ / Enterprise / Unif… `growing`
- [EDR 立项汇报 PPT 索引（33 页 deck）](notes/business/edr-proposal-deck-index.md) — 结论：EDR（事件检测与响应）立项汇报 deck 已成稿，33 页，用 slidep DSL 生产，源为 slides/01–33.slide；大二进制不进 G… `growing`
- [EDR 立项资料包 / 汇报 PPT 包 · 打包索引（6 个 zip）](notes/business/edr-proposal-bundles-index.md) — 一句话结论：EDR 立项在 2026-09-21 一天内打了 6 个 zip，属于两个家族（材料/资料全包 与 汇报 PPT 包），每个家族只有最新一版是有效版… `growing`
- [EDR立项 · 云厂商支持服务文档库索引](notes/business/EDR立项-AWS竞品分析资料包索引.md) — 本地 Markdown 合计 6.4 MB，PDF 存档合计 39.4 MB。 `growing`
- [华为云支持服务「三级梯度 × 四项立项」汇报交付包索引](notes/business/huawei-support-four-proposals-deck.md) — 结论：本批立项汇报的战略视野从「单产品 EDR」提升到「三级梯度 × 四项立项」，deck 定稿 27 页（正文 26 + 备份 1）、汇报 30–35 分钟；… `growing`
- [华为云支持服务立项 · AWS 竞品对标](notes/business/华为云支持服务立项-AWS竞品对标.md) — 不是一个产品，是三层叠起来的体系： `growing`
- [华为云支持服务立项 · EDR 产品定义](notes/business/华为云支持服务立项-EDR产品定义.md) — 管理面（平台运维事件、计划内变更、群障/区域故障）数据链路已验证连通（2026-09-21 确认）。 `growing`
- [华为云支持服务立项 · 与企业优护计划的关系](notes/business/huawei-support-enterprise-care-plan.md) — 一句话结论：答案不是"增强它 / 调整它 / 取代它"三选一，而是给它做「能力注入 + 从人力模式升级为平台化模式」——因为官网资料显示，企业优护计划已经就是"… `growing`
- [华为云支持服务立项 · 与公司内部实际方案的衔接](notes/business/huawei-support-internal-alignment.md) — 一句话结论：立项评审上最尴尬的场景是"你这套和 XX 团队在推的方案什么关系？"——答不上来就变成「信息不同步、闭门造车」；解法是在技术方案里预留衔接章节 + … `growing`
- [华为云支持服务立项 · 产品序列与收入路径](notes/business/华为云支持服务立项-产品序列与收入路径.md) — ⇒ 官网最高等级「企业级」SLA 是 ＜10 分钟；内部规划的「尊享级」要求 ＜5 分钟。 `growing`
- [华为云支持服务立项 · 合规、数据与风险](notes/business/huawei-support-compliance-risk.md) — 一句话结论：这个产品的"一票否决区"是数据合规与技术差可改不同 —— 合规出问题直接毙；而风险的头号位置在立项期内已两次转移：从"数据拿不到"→"数据质量不足"… `growing`
- [华为云支持服务立项 · 商业计划与成本模型](notes/business/huawei-support-business-case.md) — 一句话结论：收入侧不需要发明新收费机制 —— 只须在既有「云服务收入 × 拆分比例」的三级梯度计费之上，决定哪些能力进哪个梯度、哪些做成梯度内加购；真正的风险全… `growing`
- [华为云支持服务立项 · 总览](notes/business/华为云支持服务立项-总览.md) — 一套支持服务（Support Service）产品的立项组合，核心是把华为公有云的 `growing`
- [华为云支持服务立项 · 技术方案与架构](notes/business/huawei-support-tech-architecture.md) — 一句话结论：技术论证的目标不是"我们会造轮子"，而是"能做、成本可控、不重复造轮子"——所以核心自研只保留三处（统一事件模型 / 聚合与路由引擎 / AI 场景… `growing`
- [华为云支持服务立项 · 材料清单与路线图](notes/business/华为云支持服务立项-材料清单与路线图.md) — 理由：12 号给出全貌（三级梯度 × 四项立项），先立框架，再填内容， `growing`
- [华为云支持服务立项 · 立项二三（VIP TAC 与 昇腾950）](notes/business/华为云支持服务立项-立项二三产品定义.md) — AWS Unified Operations（$50,000/月起）/ AWS IDR（$7,000/月起） `growing`
- [华为云支持服务立项 · 试点成效与证据（美团/顺丰）](notes/business/huawei-support-pilot-evidence.md) — 一句话结论：04 号材料是整套立项里说服力最强的一份，但截至 2026-09-21 美团/顺丰双方数据全部为待补（⬜）——能立即拿出的唯一硬证据是《管理面数据链… `growing`
- [华为云支持计划三产品 BA 汇报 PPT 索引（32 页 deck）](notes/business/huawei-support-three-product-ba-deck-index.md) — 结论：三产品 BA 差距分析与 TO BE 高阶方案设计 deck 已成稿，正文 31 页 + 备份 1 页 = 32 页，用 slidep DSL 生产（源为… `growing`
- [华为云支持计划三产品 · BA 差距分析与 TO BE 高阶方案设计](notes/business/huawei-support-three-product-ba-gap-tobe.md) — 一句话结论：三个产品不是三个独立产品，而是同一套底座的三个切面 —— EDR 负责「让事找到人」、通知能力负责「把话送到」、智算支持服务负责「在算力场景里把事办… `growing`
- [昇腾950立项 · 官方语料索引](notes/business/昇腾950立项-官方语料索引.md) — 已归档位置：D:/AI/my_project/cloud-support-docs/huawei/ `growing`
- [竞品语料库 cloud-support-docs（打包快照索引）](notes/business/cloud-support-docs-corpus.md) — 一句话结论：cloud-support-docs/ 是立项竞品分析的一手语料库（AWS + 阿里云官方文档与产品页的全量抓取），因体量大而明确排除在知识库 Gi… `growing`

## 基础设施与网络(`infra`) · 1 篇

- [代理节点轮换技能（proxy-node-rotation）打包索引](notes/infra/proxy-node-rotation-bundle.md) — 一句话结论：这是一份可复用的 WorkBuddy 技能包——把「阿里云 ECS 上 v2rayN/xray 节点轮换」的整套流程（SKILL.md + 配置样例… `growing`

## 工具链与自动化(`tooling`) · 6 篇

- [DeepSeek Harness Desktop 安装记录 · v0.1.7-rc.2](notes/tooling/deepseek-harness-desktop-install.md) — 一句话结论：装成功了，但整个过程最值得记住的不是产品本身，而是那个反直觉的坑 —— 在 Git Bash 里给 NSIS 安装器传 /D= 会被 MSYS 篡改… `growing`
- [GitHub 初始化知识库的方案对比](notes/tooling/github-knowledge-base-options.md) — 最值得抄的不是某个笔记软件，而是 TIL（Today I Learned）范式——直接把 GitHub 仓库当知识库，因为 GitHub 已免费提供文件系统、M… `growing`
- [Raven（Windows 原生）安装与卸载记录 · v0.2.3](notes/tooling/raven-install-windows-native.md) — 一句话结论：Raven v0.2.3 在 Windows 上用 uv tool install 装成功、四个内置插件全部 activated；真正的坑不在 Ra… `growing`
- [Windows 断链快捷方式与「应用栏鬼影」清理指南](notes/tooling/windows-shortcut-ghost-cleanup.md) — 一句话结论：点图标没反应 / 报"找不到文件"、以及"设置→应用里卸不掉"，根因都不是"隐藏属性"，而是两类残留——快捷方式指着已不存在的路径、卸载器删了文件却… `growing`
- [dsh 插件体系 · 版本兼容闸门与可安装清单](notes/tooling/dsh-plugin-ecosystem.md) — 一句话结论：桌面版 dsh（0.2.0-rc.2）装插件只能走「设置 → 插件」（Electron 进程级独占 profile，CLI 会被回滚）；插件锚定的是… `growing`
- [技能一致性体检 · 把技能里的「实测」断言逐条真跑（2026-09-27）](notes/tooling/skill-env-consistency-audit-20260927.md) — 一句话结论：体检方法是「把 SKILL.md 里每一条『实测』断言拆出来、逐条对本机真跑一次」；结果是自建的 multi-agent-cli-orchestra… `growing`

## 生活与资料(`life`) · 1 篇

- [贵州茅台 600519 · 基本面与估值单维度分析（2026-09-30）](notes/life/sh600519-fundamentals-2026-09-30.md) — 一句话结论：质地优质 · 估值低估 —— 属"高质量、低增长型的类债券资产"，但低估是对成长性转负的合理定价，修复需基本面企稳确认；成长性是唯一显著短板（五维评… `seedling`

> 空领域(待填充):`ai`, `reading`
