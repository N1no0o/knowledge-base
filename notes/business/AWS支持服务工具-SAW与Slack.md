---
title: AWS 支持服务工具 · SAW 与 Slack
tags: [AWS, SAW, 自动化工作流, SystemsManager, Slack, Runbook]
created: 2026-09-25
updated: 2026-09-25
source: _website/aws-support-automation-workflows.md + _website/aws-support-app-slack.md + aws-support-user-guide/｜2026-09-25
status: growing
---

# AWS 支持服务工具 · SAW 与 Slack

## 一、SAW（AWS Support 自动化工作流）

> **定位**：由 **AWS Support 工程团队**打造的**精选 SSM 自助式自动化运行手册（Runbook）**。
>
> **本质**：把「AWS Support 在解决客户问题中沉淀的最佳实践」**产品化**为可自助执行的 Runbook。

### 工作原理（5 步）

```
① AWS Systems Manager   ← 统一界面，执行自动化的基础
② SAW Runbook           ← AWS Support Engineering 提供
③ 运行 SAW Runbook      ← 浏览器界面选择并执行
④ 自动化工作流          ← 按 Runbook 规范执行诊断/修复
⑤ 修复指导              ← 记录验证与后续步骤
```

> ⭐ **关键洞察**：SAW 不是新引擎，而是**复用 SSM + 灌入官方最佳实践**。
> 这是「**把人工经验转化为产品能力**」的低成本路径 —— 边际成本几乎为零。
>
> **⇒ 这对华为立项有直接启发**：我们的支持服务经验同样可以沉淀为 Runbook，
> **用现成的自动化平台承载，不需要自研引擎。**

### Runbook 清单（官方，⭐ 实证数据）

#### 类别一：故障排除、修复和诊断

| 服务 | Runbook |
|---|---|
| **CodeDeploy** | CodeDeploy 故障排除 |
| **CloudFormation** | `TroubleshootCFNCustomResource` |
| **Directory Service** | `TroubleshootDirectoryTrust`、`TroubleshootADConnectorConnectivity` |
| **EBS** | `CalculateEBSPerformanceMetrics` |
| **EC2** | `ExecuteEC2Rescue`、`TroubleshootEC2DiskUsage`、`StartEC2RescueWorkflow`、`RunEC2RescueForWindowsTool` |
| **ECS** | `TroubleshootECSContainerInstance`、`CollectECSInstanceLogs`、`TroubleshootECSTasksFailedToStart` |
| **EFS** | `CheckAndMountEFS` |
| **EKS** | `TroubleshootEKSWorkerNode`、`TroubleshootEKSCluster`、`CollectEKSInstanceLogs` |
| **EMR** | `AnalyzeEMRLogs` |
| **Elastic Beanstalk** | `CollectElasticBeanstalkLogs`、`TroubleshootElasticBeanStalk` |
| **Lambda** | `TroubleshootLambdaS3Event`、`TroubleshootLambdaInternetAccess`、`RemediateLambdaS3Event` |
| **RDS** | `TroubleshootConnectivityToRDS` |
| **S3** | `TroubleshootS3AccessSameAccount`、`TroubleshootS3PublicRead` |
| **Systems Manager** | `TroubleshootManagedInstance` |
| **VPC** | `ConnectivityTroubleshooter`、`ConfigureTrafficMirroring` |
| **WorkSpaces** | `RecoverWorkSpace` |

#### 类别二：管理和 Trusted Advisor（TA）检查

| 服务 | Runbook |
|---|---|
| **Config** | `SetupConfig` |
| **EBS** | `ModifyEBSSnapshotPermission` |
| **EC2** | `CopyEC2Instance`、`ListEC2Resources`、`MigrateEC2ClassicToVPC`、`RestoreEC2InstanceFromSnapshot`、`ConfigureEC2Metadata` |
| **RDS** | `ModifyRDSSnapshotPermission`、`ShareRDSSnapshot` |
| **VPC** | `MigrateEC2ClassicToVPC`、`EnableVPCFlowLogs`、`SetupIPMonitoringFromVPC`、`TerminateIPMonitoringFromVPC`、`ConfigureDNSQueryLogging` |

#### 类别三：成本优化和运营审查（Cost Optimization and Operational Review）

| 服务 | Runbook |
|---|---|
| **EC2** | `CloneXenEC2InstanceAndMigrateToNitro` |
| **RDS** | `PostgreSQLWorkloadReview` |

> **统计**：三大类别，**覆盖 17 个服务，约 40 个 Runbook**。

### 门槛

| 能力 | 门槛 |
|---|---|
| SAW | **Business+** |

## 二、Support App in Slack

> **定位**：在 **Slack 内直接管理 AWS 工单**，不用离开聊天窗口。

### 功能清单（官方）

| 功能 | 说明 |
|---|---|
| 创建工单 | 在 Slack 频道内创建支持案例 |
| 更新工单 | 更新案例状态 |
| 搜索工单 | 在 Slack 内搜索 |
| 解决工单 | 关闭案例 |
| 重新打开工单 | 重开案例 |
| **分享工单详情给团队** | ⭐ **不用离开 Slack 频道** |
| 在 Support Center 查看 Slack 对话 | 双向可见 |

### 配置流程

```
① 前置条件（prerequisites）
② 授权 Slack 工作区（authorize-slack-workspace）
③ 配置 Slack 频道（add-your-slack-channel）
④ 使用（创建/回复/搜索/解决/重开工单）
```

**支持资源可通过 CloudFormation 创建**（`creating-resources-with-cloudformation`）。

### 门槛

| 能力 | 门槛 |
|---|---|
| Support App in Slack | **Business+** |

> ⭐ **设计价值**：把**工单能力投送到客户已有的协作工具里**，
> 而不是要求客户来 AWS 控制台。这是**「把服务嵌入客户工作流」**的思路 ——
> 与华为 EDR 立项里的「多通道触达（钉钉/企微/飞书）」**完全同构**。

## 与华为立项的对照意义

| 维度 | AWS SAW | AWS Slack App | 华为可借鉴 |
|---|---|---|---|
| **经验产品化** | 最佳实践 → SSM Runbook | — | 支持经验可沉淀为 Runbook |
| **复用现成平台** | 用 SSM，不自研引擎 | 用 Slack，不自建 IM | **降低研发成本的关键** |
| **嵌入客户工作流** | — | 工单进 Slack | 触达进钉钉/企微/飞书 |
| **覆盖面** | 17 服务 / ~40 Runbook | 全工单能力 | 我们的覆盖广度需明确 |

> **⭐ 可直接引用的话术**：
> 「AWS 的自动化能力（SAW）**没有自研引擎，而是复用 SSM 并灌入官方最佳实践**；
> 它的 IM 触达**没有自建协作工具，而是嵌入 Slack**。
> ⇒ 这说明**支持服务的差异化不来自自研基础设施，而来自经验沉淀与场景选择**。」

## 文档出处

- `_website/aws-support-automation-workflows.md` — SAW 完整 Runbook 清单
- `_website/aws-support-app-slack.md` — Slack App 功能与配置流程
- `aws-support-user-guide/` — 相关配置章节

---

## 关联笔记

- [[AWS支持服务工具-手册总览]] — 工具体系全貌
- [[AWS支持服务工具-Trusted-Advisor]] — SAW 有「管理 TA 检查」类别
- [[AWS支持服务工具-Support-API与工单]] — Slack App 管理的是同一套工单
- [[华为云支持服务立项-EDR产品定义]] — 多通道触达同构
