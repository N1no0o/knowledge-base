#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb_scan.py — 扫描 agent 产出件，输出「待入库清单」

配合 AGENTS.md 的 ingest 工作流使用。本脚本只做机械识别与状态记账，
「编译成笔记」这一判断动作由 agent 完成。

用法:
    python tools/kb_scan.py                     # 增量扫描（对比 _kb_state/ingested.json）
    python tools/kb_scan.py --all               # 忽略状态，全量列出
    python tools/kb_scan.py --only-new          # 只列新增（排除 changed）
    python tools/kb_scan.py --mark <源文件路径> [--note <笔记相对路径>]
    python tools/kb_scan.py --status            # 只打印状态统计
    python tools/kb_scan.py --json <输出路径>   # 指定 pending.json 输出位置

产出:
    _kb_state/ingested.json   已入库账本（会进 Git，跨设备一致）
    _kb_state/pending.json    本次待处理清单（不进 Git 也无妨）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT, "_kb_state")
LEDGER = os.path.join(STATE_DIR, "ingested.json")
PENDING = os.path.join(STATE_DIR, "pending.json")

# ---------------------------------------------------------------- 扫描配置

# 源：agent/工作区的产出目录。depth=1 表示只看该目录下一层，不递归。
# ⚠️ 新增产出区目录时必须在此登记，否则整棵子树不会被扫描
#    （2026-09-30 教训：deliverables/ 漏登记 ⇒ 18 件交付物长期落在扫描视野外）。
SOURCE_ROOTS = [
    {"path": "D:/AI/my_project", "depth": 1, "label": "工作区根目录"},
    {"path": "D:/AI/my_project/dist", "depth": 99, "label": "dist 产出区"},
    {"path": "D:/AI/my_project/deliverables", "depth": 99, "label": "deliverables 交付区"},
]

# 目录名精确排除
EXCLUDE_DIRS = {
    ".git", ".workbuddy", ".obsidian", ".cache", ".slidep", ".secrets",
    "node_modules", "__pycache__", "_site",
    "aliyun-well-architected", "cloud-support-docs",  # 语料库，体量大且不进 Git
    "assets", "preview", "console",                    # 渲染中间产物
    "tencent-upload", "tencent-upload-v2",             # 腾讯文档分卷包，只留索引
}
# 目录名模式排除（备份/轮转/暂存）
EXCLUDE_DIR_RE = re.compile(r"^(_|\.|slides_bak|.*_bak|.*backup|automation-|\d{4}-\d{2}-\d{2})")

# 视为「成品资料」的扩展名
ARTIFACT_EXT = {".md", ".docx", ".doc", ".pptx", ".ppt", ".pdf", ".xlsx", ".csv", ".zip", ".html"}
# 二进制大件（只写索引笔记，不进 Git）
BINARY_EXT = {".zip", ".docx", ".doc", ".pptx", ".ppt", ".pdf", ".xlsx"}
# 文件名模式排除
EXCLUDE_FILE_RE = re.compile(
    r"(^_|^\.|~$|\.bak|\.old|\.tmp$|\.log$|\.jsonl?$|\.svg$|\.png$|\.jpg$|"
    r"_bak|bak-\d|before\d+|^00-.*说明|下载清单|^welcome_tmp)"
)
# 明确不是产出件的固定文件名
EXCLUDE_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "SKILL.md", ".gitkeep", ".gitignore"}

# 大文件阈值：超过则笔记里只记路径（不进 Git）
BIG_BYTES = 1 * 1024 * 1024


def load_ignore() -> list:
    """读取 _kb_state/ignore.txt —— 每行一个相对路径或 glob，`#` 开头为注释。

    用于把人工判定为「非产出件」的噪声文件排除在扫描之外。
    """
    p = os.path.join(STATE_DIR, "ignore.txt")
    if not os.path.exists(p):
        return []
    pats = []
    with open(p, encoding="utf-8-sig") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                pats.append(s.replace("\\", "/"))
    return pats


def is_ignored(key: str, pats: list) -> bool:
    import fnmatch
    for p in pats:
        if key == p or fnmatch.fnmatch(key, p) or fnmatch.fnmatch(os.path.basename(key), p):
            return True
        if p.endswith("/") and key.startswith(p):
            return True
    return False


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_ledger() -> dict:
    if os.path.exists(LEDGER):
        try:
            with open(LEDGER, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_ledger(d: dict) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2, sort_keys=True)


def collect() -> list:
    """按 SOURCE_ROOTS 收集候选产出件。"""
    found = []
    seen = set()
    ignore = load_ignore()
    for src in SOURCE_ROOTS:
        base = src["path"]
        if not os.path.isdir(base):
            continue
        depth_max = src["depth"]
        base_depth = base.rstrip("/\\").count(os.sep)
        for root, dirs, files in os.walk(base):
            cur_depth = root.rstrip("/\\").count(os.sep) - base_depth
            if cur_depth >= depth_max:
                dirs[:] = []
            else:
                dirs[:] = [d for d in dirs
                           if d not in EXCLUDE_DIRS and not EXCLUDE_DIR_RE.match(d)]
            for fn in files:
                if fn in EXCLUDE_FILES:
                    continue
                ext = os.path.splitext(fn)[1].lower()
                if ext not in ARTIFACT_EXT:
                    continue
                if EXCLUDE_FILE_RE.search(fn):
                    continue
                full = os.path.join(root, fn)
                key = os.path.relpath(full, "D:/AI/my_project").replace("\\", "/")
                if key in seen or is_ignored(key, ignore):
                    continue
                seen.add(key)
                try:
                    st = os.stat(full)
                except OSError:
                    continue
                found.append({
                    "key": key,
                    "path": full.replace("\\", "/"),
                    "name": fn,
                    "ext": ext,
                    "size": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "source_label": src["label"],
                    "is_binary": ext in BINARY_EXT,
                    "is_big": st.st_size > BIG_BYTES,
                })
    return sorted(found, key=lambda x: x["key"])


def diff(found: list, ledger: dict, all_mode: bool) -> tuple:
    new, changed, unchanged = [], [], []
    for it in found:
        rec = ledger.get(it["key"])
        if all_mode or rec is None:
            (new if rec is None else unchanged).append(it)
            continue
        digest = sha256_of(it["path"])
        it["sha256"] = digest
        if rec.get("sha256") != digest:
            changed.append(it)
        else:
            unchanged.append(it)
    for it in new:
        it["sha256"] = sha256_of(it["path"])
    return new, changed, unchanged


def render_text(new, changed, unchanged, ledger) -> str:
    lines = []
    lines.append("=" * 66)
    lines.append("agent 产出件扫描结果")
    lines.append("=" * 66)
    lines.append(f"账本已记录 : {len(ledger)} 件")
    lines.append(f"本次待处理 : {len(new) + len(changed)} 件  (新增 {len(new)} / 变更 {len(changed)})")
    lines.append(f"已入库跳过 : {len(unchanged)} 件")
    for tag, group in (("新增 NEW", new), ("变更 CHANGED", changed)):
        if not group:
            continue
        lines.append("")
        lines.append(f"--- {tag} ({len(group)}) ---")
        for it in group:
            flag = "BIN" if it["is_binary"] else ("BIG" if it["is_big"] else "MD ")
            lines.append(f"  [{flag}] {it['key']}  ({it['size'] / 1024:.1f} KB, {it['mtime']})")
    if not new and not changed:
        lines.append("")
        lines.append("=> 无待处理项，知识库已是最新。")
    return "\n".join(lines)


def cmd_mark(src: str, note: str) -> int:
    ledger = load_ledger()
    key = os.path.relpath(os.path.abspath(src), "D:/AI/my_project").replace("\\", "/")
    if not os.path.exists(src):
        print(f"[mark] 源文件不存在: {src}")
        return 1
    ledger[key] = {
        "sha256": sha256_of(src),
        "size": os.path.getsize(src),
        "ingested_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "note": note or "",
    }
    save_ledger(ledger)
    print(f"[mark] OK {key} -> {note or '(未指定笔记)'}  (账本 {len(ledger)} 件)")
    return 0


def cmd_status() -> int:
    ledger = load_ledger()
    found = collect()
    keys = {it["key"] for it in found}
    dropped = [k for k in ledger if k not in keys]
    print(f"账本条目   : {len(ledger)}")
    print(f"当前可扫描 : {len(found)}")
    print(f"账本中已消失(源文件被移动/删除): {len(dropped)}")
    for d in sorted(dropped)[:20]:
        print("  -", d)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--all", action="store_true", help="忽略账本，全量列出")
    ap.add_argument("--only-new", action="store_true", help="只列新增，不列变更")
    ap.add_argument("--mark", metavar="SRC", help="标记某产出件已入库")
    ap.add_argument("--note", metavar="REL", default="", help="配合 --mark，记录生成的笔记路径")
    ap.add_argument("--status", action="store_true", help="只打印状态统计")
    ap.add_argument("--json", metavar="PATH", help="pending.json 输出路径")
    args = ap.parse_args()

    if args.mark:
        return cmd_mark(args.mark, args.note)
    if args.status:
        return cmd_status()

    ledger = load_ledger()
    found = collect()
    new, changed, unchanged = diff(found, ledger, args.all)
    if args.only_new:
        changed = []
    pending = new + changed

    print(render_text(new, changed, unchanged, ledger))

    out = args.json or PENDING
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "summary": {"new": len(new), "changed": len(changed), "unchanged": len(unchanged),
                        "ledger": len(ledger)},
            "pending": pending,
        }, f, ensure_ascii=False, indent=2)
    print()
    print(f"[scan] 清单已写入 {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
