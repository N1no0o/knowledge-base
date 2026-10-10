---
title: A 股量化回测框架 · 交付包与产物索引
tags: [A股, 量化, 回测框架, 交付包索引, 产物清单, python]
created: 2026-10-11
updated: 2026-10-11
source: quant/README.md ＋ quant/output/*（原件 D:/AI/my_project/quant/，2026-10-10 23:11）
status: growing
---

# A 股量化回测框架 · 交付包与产物索引

**一句话结论：这是一套约 700 行、不依赖重量级框架的 A 股日频多因子回测系统（4 个源码模块 + 自检探针 + 4 张图 + HTML 报告）；结论见 [[ashare-quant-backtest-findings]]，本篇只做「包里有什么、在哪、多大」的索引登记，**产物不进 Git**。**

## 一、产物清单（本次入库登记的 4 件）

| 文件 | 类型 | 体积 | 进 Git |
|---|---|---|---|
| `quant/output/backtest_report.html` | 回测报告（净值/回撤/分布/换手成本/IC 四图 + 指标表） | 210.7 KB | ❌ |
| `quant/output/weights.csv` | 逐期持仓权重 | 110.1 KB | ❌ |
| `quant/output/nav.csv` | 净值序列 | 41.9 KB | ❌ |
| `quant/output/trades.csv` | 成交流水 | 18.8 KB | ❌ |

**生成时间**：2026-10-10 23:11 · **本地绝对路径**：`D:/AI/my_project/quant/output/`

## 二、包内其他构成（未逐件入库，登记备查）

- **源码**（`quant/src/`）：`data.py` 数据层（腾讯/新浪/akshare 多源降级 + parquet 缓存）· `factors.py` 因子层（动量/反转/波动/趋势/回撤 + IC 检验）· `backtest.py` 引擎（信号滞后、成本扣减、风控、绩效）· `report.py` 输出
- **入口**：`run_backtest.py`（约 7.1 KB，一条命令跑完）· `selfcheck.py`（约 4.4 KB，作弊信号探针）
- **数据缓存**（`quant/data/`）：12 只标的日线前复权 parquet，单只约 48–59 KB，合计约 **0.65 MB**（自动生成，可重跑重建）
- **图表**（`quant/output/*.png`）：01 净值与回撤 / 02 收益分布与持仓只数 / 03 换手与成本 / 04 IC 分析，合计约 **0.36 MB**
- `quant/requirements.txt`（394 B）：pandas / numpy / matplotlib / pyarrow（akshare 可选）

> 说明：`quant/README.md` 因文件名在扫描器 `EXCLUDE_FILES` 内、`.parquet`/`.png` 不在成品扩展名内，故未单独入账 —— 其内容已由本索引篇与结论篇完整覆盖。

## 三、关键参数默认值

| 参数 | 默认 | 说明 |
|---|---|---|
| `--codes` | 12 只蓝筹 | 平安银行/茅台/招行/平安/美的/长江电力等 |
| `--top-n` | 3 | 持股数量 |
| `--holding` | 20 | 调仓周期（交易日） |
| `--no-timing` | 关 | 默认开 60 日均线择时 |
| `--start`/`--end` | 2021-01-01 ~ 2026-09-30 | 回测区间 |

成本模型：佣金 0.00025 · 印花税 0.001（仅卖出）· 滑点 0.0005 · 总仓位 0.95。

## 四、复现方式

```bash
pip install pandas numpy matplotlib pyarrow
python selfcheck.py        # 必须：先确认引擎计算正确（不需网络）
python run_backtest.py     # 真实 A 股回测
# 打开 output/backtest_report.html
```

首次运行后数据缓存到 `data/`，重跑秒级、不再联网。

## 相关

- [[ashare-quant-backtest-findings]] — 本交付包的**实测结论篇**（三档配置对照、换手成本归因、ICIR 0.036、七条踩坑）
- [[sh600519-fundamentals-2026-09-30]] — 同批金融主题产出件
