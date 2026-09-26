#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb_push.py — 把知识库推送到 GitHub（PAT + REST API，不依赖 gh / git 凭据）

为什么不用 git push:
    本机无 gh、无凭据管理器记录、无 SSH 私钥 ⇒ git push 直接报
    "could not read Username for 'https://github.com': terminal prompts disabled"。

    ⚠️ 2026-09-27 实测更正：这**不是**网络问题 —— 本机 `git ls-remote` 与 `git fetch` 均
    正常返回，唯一的卡点是「缺凭据」。REST API 这条路只需要一个 PAT，故仍为首选。

PAT 读取顺序（绝不打进日志/报告）:
    1. 环境变量 GH_PAT
    2. 环境变量 N1NO_PAT
    3. 受限文件 D:/AI/my_project/.secrets/gh_pat_n1no  （第一行，可带 "Bearer "/"token " 前缀）
    ⇒ 文件不存在时给出明确指引并返回码 3（"未配置凭据"），本地整理仍然有效。

用法:
    python tools/kb_push.py                      # 自动 commit message
    python tools/kb_push.py -m "notes(x): ..."   # 指定 message
    python tools/kb_push.py -F _commit_msg.txt   # 从文件读 message
    python tools/kb_push.py --dry-run            # 只列出待推送文件，不写远端
    python tools/kb_push.py --verify-only        # 只做远端/本地一致性校验

退出码: 0 成功/无事可做 · 1 推送失败 · 2 校验失败 · 3 未配置凭据
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER, REPO, BRANCH = "N1no0o", "knowledge-base", "main"
PAT_FILES = [
    "D:/AI/my_project/.secrets/gh_pat_n1no",
    os.path.expanduser("~/.workbuddy/.secrets/gh_pat_n1no"),
]
STATE_DIR = os.path.join(ROOT, "_kb_state")
REPORT = os.path.join(STATE_DIR, "push_report.json")

# 不进仓库的路径（前缀匹配）
SKIP_DIRS = {".git", "_extract", "_tdoc_dl", "_corpus", "_junk-quarantine", "__pycache__", ".obsidian"}
SKIP_FILES = {"_push.py", "_commit_msg.txt", ".DS_Store", "Thumbs.db", "_kb_state/pending.json",
              "_kb_state/pending_push.md", "_kb_state/push_report.json"}
SKIP_PREFIX = ("_tdoc_",)
MAX_BLOB = 2 * 1024 * 1024   # 单文件 2 MiB 上限，超了只告警不推

T0 = time.time()


def log(*a):
    print("[%6.1fs]" % (time.time() - T0), *a, flush=True)


def read_pat():
    for k in ("GH_PAT", "N1NO_PAT"):
        v = os.environ.get(k, "").strip()
        if v:
            return v, "env:" + k
    for p in PAT_FILES:
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8-sig") as f:
                    for line in f:
                        s = line.strip()
                        if not s or s.startswith("#"):
                            continue
                        for pre in ("Bearer ", "bearer ", "token "):
                            if s.startswith(pre):
                                s = s[len(pre):]
                        return s.strip(), "file:" + p
            except OSError:
                continue
    return None, None


def make_req(pat):
    def req(method, path, body=None, timeout=30):
        url = "https://api.github.com" + path
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(url, data=data, method=method)
        r.add_header("Authorization", "Bearer " + pat)
        r.add_header("Accept", "application/vnd.github+json")
        r.add_header("X-GitHub-Api-Version", "2022-11-28")
        r.add_header("User-Agent", "n1no-kb-sync")
        if data:
            r.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(r, timeout=timeout) as resp:
                raw = resp.read()
                return resp.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")[:400]
        except Exception as e:
            return -1, str(e)[:200]
    return req


def git_blob_sha(content: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(content))
    h.update(content)
    return h.hexdigest()


def local_files():
    out = {}
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn in SKIP_FILES or fn.startswith(SKIP_PREFIX):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            if rel in SKIP_FILES:
                continue
            try:
                with open(p, "rb") as fh:
                    out[rel] = fh.read()
            except OSError:
                continue
    return out


def cmd_verify(req, local, remote=None):
    """比对远端 tree 的 blob sha 与本地计算的 git blob sha。"""
    failures = []
    if remote is None:
        st, ref = req("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}")
        if st != 200:
            log("取远端 ref 失败", st, ref)
            return 1, []
        st, cm = req("GET", f"/repos/{OWNER}/{REPO}/git/commits/{ref['object']['sha']}")
        st, rt = req("GET", f"/repos/{OWNER}/{REPO}/git/trees/{cm['tree']['sha']}?recursive=1")
        if st != 200:
            log("取远端 tree 失败", st, rt)
            return 1, []
        remote = {i["path"]: i["sha"] for i in rt["tree"] if i["type"] == "blob"}
    checked = 0
    for rel, content in sorted(local.items()):
        if len(content) > MAX_BLOB:
            continue
        rs = remote.get(rel)
        if rs is None:
            failures.append((rel, "远端缺失"))
            continue
        if rs != git_blob_sha(content):
            failures.append((rel, "内容不一致"))
        checked += 1
    return (1 if failures else 0), failures, checked, len(remote)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--message")
    ap.add_argument("-F", "--message-file")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    pat, pat_src = read_pat()
    os.makedirs(STATE_DIR, exist_ok=True)

    local = local_files()
    log("本地文件:", len(local))

    if not pat and not args.verify_only:
        log("未配置凭据 —— 跳过推送")
        print()
        print("=" * 66)
        print("⚠️  未找到 GitHub PAT，本次只完成本地整理，未推送远端。")
        print("   配置方式（一次性）：")
        print(f"     1) 新建文件 {PAT_FILES[0]}")
        print("     2) 第一行粘贴 fine-grained PAT（需 Contents: Read and write；")
        print("        若含 .github/workflows/ 改动还需 workflow 权限）")
        print("     3) 收紧权限：icacls 只保留当前用户")
        print("=" * 66)
        return 3

    req = make_req(pat) if pat else None

    if args.verify_only:
        if req is None:
            log("未配置凭据 —— 无法校验远端")
            return 3
        code, failures, checked, total = cmd_verify(req, local)
        log(f"校验: 检查 {checked} 个文件, 远端共 {total} 个")
        for rel, why in failures[:30]:
            print("   ✗", rel, "|", why)
        log("校验通过" if code == 0 else f"校验失败 {len(failures)} 项")
        return 0 if code == 0 else 2

    # 身份核对：token 必须属于目标 owner
    st, me = req("GET", "/user")
    if st != 200:
        log("token 校验失败", st, me)
        return 3
    login = (me or {}).get("login", "")
    if login.lower() != OWNER.lower():
        log(f"token 属于 {login}，与目标 owner {OWNER} 不符 —— 中止")
        return 3
    log(f"凭据来源 {pat_src} · 身份 {login}")

    st, ref = req("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}")
    if st != 200:
        log("取分支 ref 失败", st, ref)
        return 1
    base_commit = ref["object"]["sha"]
    st, cm = req("GET", f"/repos/{OWNER}/{REPO}/git/commits/{base_commit}")
    base_tree = cm["tree"]["sha"]
    st, rt = req("GET", f"/repos/{OWNER}/{REPO}/git/trees/{base_tree}?recursive=1")
    if st != 200:
        log("取远端 tree 失败", st, rt)
        return 1
    remote = {i["path"]: i["sha"] for i in rt["tree"] if i["type"] == "blob"}
    log("远端 blob:", len(remote), "| base", base_commit[:8])

    todo, skipped_big = [], []
    for rel, content in sorted(local.items()):
        if len(content) > MAX_BLOB:
            skipped_big.append((rel, len(content)))
            continue
        if remote.get(rel) != git_blob_sha(content):
            todo.append((rel, content))
    log("待推送:", len(todo))
    for rel, _ in todo:
        print("   +", rel)
    for rel, n in skipped_big:
        print("   !  跳过(>%.0fMB): %s" % (MAX_BLOB / 1048576, rel))

    if not todo:
        log("远端已是最新，无需推送")
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(REPORT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"at": datetime.now().isoformat(timespec="seconds"),
                       "result": "up-to-date", "login": login, "pushed": []}, f,
                      ensure_ascii=False, indent=2)
        return 0
    if args.dry_run:
        log("dry-run，不写远端")
        return 0

    # message
    msg = args.message
    if not msg and args.message_file and os.path.exists(args.message_file):
        msg = open(args.message_file, encoding="utf-8").read().strip()
    if not msg:
        msg = f"chore(kb): 自动同步 {len(todo)} 个文件 ({date.today().isoformat()})"
    # 保留多行正文（首行为 title）；仅当首行过短时才回退到自动 message
    msg = msg.strip()
    if len(msg.split("\n")[0].strip()) < 5:
        msg = f"chore(kb): 自动同步 {len(todo)} 个文件 ({date.today().isoformat()})"

    tree_items = []
    for rel, content in todo:
        st, r = req("POST", f"/repos/{OWNER}/{REPO}/git/blobs",
                    {"content": base64.b64encode(content).decode(), "encoding": "base64"})
        if st not in (200, 201):
            log("blob 上传失败", rel, st, r)
            return 1
        tree_items.append({"path": rel, "mode": "100644", "type": "blob", "sha": r["sha"]})
    log("blobs 完成:", len(tree_items))

    st, tree = req("POST", f"/repos/{OWNER}/{REPO}/git/trees",
                   {"base_tree": base_tree, "tree": tree_items})
    if st not in (200, 201):
        log("tree 构建失败", st, tree)
        return 1
    st, nc = req("POST", f"/repos/{OWNER}/{REPO}/git/commits",
                 {"message": msg, "tree": tree["sha"], "parents": [base_commit]})
    if st not in (200, 201):
        log("commit 失败", st, nc)
        return 1
    st, ur = req("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}", {"sha": nc["sha"]})
    if st not in (200, 201):
        log("ref 更新失败", st, ur)
        return 1
    log("PUSHED OK ->", nc["sha"][:8])

    # 独立校验：重新拉远端 tree 比对
    code, failures, checked, total = cmd_verify(req, local)
    log(f"校验: {checked} 个文件, 远端 {total} 个, 失败 {len(failures)}")
    for rel, why in failures[:30]:
        print("   ✗", rel, "|", why)

    with open(REPORT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "at": datetime.now().isoformat(timespec="seconds"),
            "result": "pushed" if code == 0 else "pushed-verify-failed",
            "login": login, "commit": nc["sha"], "message": msg,
            "pushed": [r for r, _ in todo], "skipped_big": [r for r, _ in skipped_big],
            "verify": {"checked": checked, "remote_total": total,
                       "failures": [{"path": p, "why": w} for p, w in failures]},
        }, f, ensure_ascii=False, indent=2)
    log("报告:", REPORT)
    return 0 if code == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
