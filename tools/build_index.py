#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_index.py — 重建知识库索引

用法:
    python tools/build_index.py           # 重建 index.md 与 search-index.json
    python tools/build_index.py --check   # 只检查不写入(lint 用)

做三件事:
    1. 扫描 notes/<领域>/*.md 并解析 frontmatter
    2. 生成 index.md(按领域分组的全量索引,含一行摘要)
    3. 生成 search-index.json(供前端或 AI 检索)
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_DIR = os.path.join(ROOT, "notes")
INDEX_MD = os.path.join(ROOT, "index.md")
SEARCH_JSON = os.path.join(ROOT, "search-index.json")

# 新增领域目录时,在这里登记中文名 —— 否则不会被计入索引
AREAS = {
    "ai": "大模型与 Agent",
    "business": "业务与立项",
    "infra": "基础设施与网络",
    "tooling": "工具链与自动化",
    "reading": "阅读摘录",
    "life": "生活与资料",
}

STALE_DAYS = 180
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")


def parse_frontmatter(text: str):
    """极简 frontmatter 解析(不依赖 pyyaml)。"""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
        fm[key] = val
    return fm, text[m.end():]


def summary_of(body: str, limit: int = 80) -> str:
    """取正文第一行实质性内容作为摘要。"""
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("|"):
            continue
        s = re.sub(r"[*`\[\]]", "", s)
        return s[:limit] + ("…" if len(s) > limit else "")
    return ""


def scan():
    items = []
    if not os.path.isdir(NOTES_DIR):
        return items
    for area in sorted(os.listdir(NOTES_DIR)):
        adir = os.path.join(NOTES_DIR, area)
        if not os.path.isdir(adir):
            continue
        for fn in sorted(os.listdir(adir)):
            if not fn.endswith(".md") or fn == ".gitkeep":
                continue
            path = os.path.join(adir, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            fm, body = parse_frontmatter(text)
            items.append({
                "area": area,
                "rel": os.path.relpath(path, ROOT).replace("\\", "/"),
                "stem": fn[:-3],
                "title": fm.get("title") or fn[:-3],
                "tags": fm.get("tags") or [],
                "created": str(fm.get("created", "")),
                "updated": str(fm.get("updated", "")),
                "source": str(fm.get("source", "")),
                "status": str(fm.get("status", "")),
                "summary": summary_of(body),
                "body": body,
            })
    return items


def build_index_md(items):
    today = date.today().isoformat()
    out = [
        "# 索引",
        "",
        "> 本文件由 `tools/build_index.py` 自动生成，**请勿手改**。",
        f"> 最后更新:{today} · 共 {len(items)} 篇",
        "",
    ]
    by_area = {}
    for it in items:
        by_area.setdefault(it["area"], []).append(it)

    order = list(AREAS.keys()) + [a for a in sorted(by_area) if a not in AREAS]
    for area in order:
        group = by_area.get(area)
        if not group:
            continue
        label = AREAS.get(area, area)
        out.append(f"## {label}(`{area}`) · {len(group)} 篇")
        out.append("")
        for it in sorted(group, key=lambda x: str(x["title"])):
            tail = f" `{it['status']}`" if it["status"] else ""
            summ = f" — {it['summary']}" if it["summary"] else ""
            out.append(f"- [{it['title']}]({it['rel']}){summ}{tail}")
        out.append("")

    empty = [a for a, lab in AREAS.items() if a not in by_area]
    if empty:
        out.append(f"> 空领域(待填充):{', '.join('`%s`' % a for a in empty)}")
        out.append("")
    return "\n".join(out)


def build_search_json(items):
    return [
        {
            "title": it["title"],
            "path": it["rel"],
            "area": it["area"],
            "areaLabel": AREAS.get(it["area"], it["area"]),
            "tags": it["tags"],
            "status": it["status"],
            "updated": it["updated"],
            "summary": it["summary"],
        }
        for it in items
    ]


def run_check(items):
    print(f"总笔记数:{len(items)}")
    if not items:
        print("(notes/ 下还没有笔记)")
        return 0

    print("\n按领域:")
    counts = {}
    for it in items:
        counts[it["area"]] = counts.get(it["area"], 0) + 1
    for a in sorted(counts):
        print(f"  {AREAS.get(a, a):<10} {counts[a]}")

    print("\n按状态:")
    st = {}
    for it in items:
        st[it["status"] or "(未标)"] = st.get(it["status"] or "(未标)", 0) + 1
    for k in sorted(st):
        print(f"  {k:<10} {st[k]}")

    # 断链 / 入链
    stems = {it["stem"] for it in items}
    inbound = {}
    broken = []
    for it in items:
        for m in WIKILINK_RE.finditer(it["body"]):
            target = os.path.basename(m.group(1).strip())
            if target.endswith(".md"):
                target = target[:-3]
            if target in stems:
                inbound[target] = inbound.get(target, 0) + 1
            else:
                broken.append((it["rel"], target))

    orphans = [it for it in items if inbound.get(it["stem"], 0) == 0]
    no_source = [it for it in items if not it["source"]]
    today = date.today()
    stale = []
    for it in items:
        if it["status"] != "seedling" or not it["updated"]:
            continue
        try:
            d = datetime.strptime(it["updated"][:10], "%Y-%m-%d").date()
            if (today - d).days > STALE_DAYS:
                stale.append((it["rel"], (today - d).days))
        except ValueError:
            pass

    def report(title, rows, fmt):
        print(f"\n{title}({len(rows)}):")
        if not rows:
            print("  无")
        for r in rows:
            print("  " + fmt(r))

    report("断链 [[...]] 指向不存在的笔记", broken, lambda r: f"{r[0]} → [[{r[1]}]]")
    report("孤儿笔记(无任何入链)", orphans, lambda r: r["rel"])
    report(f"过时(seedling 且 {STALE_DAYS} 天未更新)", stale, lambda r: f"{r[0]}({r[1]} 天)")
    report("缺 source 字段", no_source, lambda r: r["rel"])

    print("\n提示:孤儿/断链在初期属正常现象;删除笔记前必须人工确认。")
    return 0


def main():
    check_only = "--check" in sys.argv
    items = scan()

    if check_only:
        sys.exit(run_check(items))

    # 索引漂移检测
    old = ""
    if os.path.exists(INDEX_MD):
        with open(INDEX_MD, encoding="utf-8") as f:
            old = f.read()
    new = build_index_md(items)

    with open(INDEX_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    with open(SEARCH_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(build_search_json(items), f, ensure_ascii=False, indent=2)

    print(f"已扫描 {len(items)} 篇笔记")
    print(f"  index.md         {'已更新' if old != new else '无变化'}")
    print(f"  search-index.json 已写入")


if __name__ == "__main__":
    main()
