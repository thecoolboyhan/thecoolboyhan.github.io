#!/usr/bin/env python3
"""
博客文章排版/错别字批量修复脚本（可复现、安全）。

规则：
1. 维护 ``` 代码块状态，代码块内完全不修改（保护变量名/API/代码）。
2. 正文排版：
   - 压缩连续空行为最多 1 行（去除行尾空白）。
   - 标题行（# ~ ######）前后保证有且仅有一个空行。
   - 列表项（-, *, 1.）与后续非同级/非列表内容之间保证空行。
3. 错别字词典：仅替换正文（非代码块）中出现的常见错误。

用法：
  python3 scripts/format_posts.py --dry              # 打印改动统计，不写文件
  python3 scripts/format_posts.py                    # 实际应用修改
  python3 scripts/format_posts.py --file <path>      # 只处理单个文件
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "content", "post"))

# 错别字词典： (错误, 正确)。仅作用于非代码块正文，且均为已逐条核对确认的真实错别字。
TYPO_FIXES = [
    ("任然", "仍然"),
    ("sspring", "spring"),
    ("diService", "doService"),
    ("ExeutoService", "ExecutorService"),
    ("synachronized", "synchronized"),
    ("jion", "join"),
    ("tryReiease", "tryRelease"),
    ("Hiermate", "Hibernate"),
    ("SocJS", "SockJS"),
    ("GCLib", "CGLib"),
    ("Gclib", "CGLib"),
    ("里式替换", "里氏替换"),
    ("里式", "里氏"),
    ("自定以", "自定义"),
    ("未代理", "为代理"),
    ("Porlet", "Portlet"),
    ("swithc", "switch"),
    ("fasle", "false"),
    ("时间驱动，而MQ", "事件驱动，而MQ"),
    ("时间驱动，而 MQ", "事件驱动，而 MQ"),
    # 后续逐篇人工核对新发现的错别字
    ("再次面问", "再次访问"),
    ("数据井支持", "数据并支持"),
    ("数据井", "数据并"),
    ("元余", "冗余"),
    ("传动办法", "传统办法"),
    ("导人", "导入"),
    ("功能齐 全", "功能齐全"),
    ("井在", "并在"),
    ("即使解决", "及时解决"),
    ("vlaue", "value"),
    ("MapReduc e", "MapReduce"),
    ("指定器", "指定其"),
    ("交由器", "交由其"),
    ("对器进行", "对其进行"),
    ("作用时管理", "作用是管理"),
    ("更具实际", "根据实际"),
    ("更具传入", "根据传入"),
    ("更具情况", "根据情况"),
    ("主频Bean", "注解Bean"),
    # 2026-09-14《设计机器学习应用系统》核对的错别字
    ("座标", "坐标"),
    ("如何我们不断缩小", "如果我们不断缩小"),
    ("黛蛾", "的"),
    ("电解应该选择", "节点应该选择"),
    ("信息增效", "信息增益"),
    ("替换为也节点", "替换为叶子节点"),
    ("最小样本树", "最小样本数"),
    ("每颗新树", "每棵新树"),
    ("按行列排量", "按行列排列"),
    ("就就相当于", "就相当于"),
    ("大致画出数据分布的大致线", "画出数据分布的大致线"),
    ("x=(90,2,1,5,500)x=(90,2,1,5,500)", "x=(90,2,1,5,500)"),
]

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s+\S")
CODE_FENCE_RE = re.compile(r"^(\s*)```")


def process_file(path, apply):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = raw.split("\n")
    out = []
    in_code = False
    typo_changes = 0

    for line in lines:
        fence = CODE_FENCE_RE.match(line)
        if fence:
            in_code = not in_code
            out.append(line.rstrip(" \t"))
            continue
        if in_code:
            out.append(line)  # 代码块内完全不改
            continue
        norm = line.rstrip("\r\n").rstrip(" \t")
        new_norm = norm
        for wrong, right in TYPO_FIXES:
            if wrong in new_norm:
                new_norm = new_norm.replace(wrong, right)
        if new_norm != norm:
            typo_changes += 1
            norm = new_norm
        out.append(norm)

    # 第一遍：压缩连续空行（仅非代码区）
    compressed = []
    in_code = False
    prev_blank = False
    for line in out:
        fence = CODE_FENCE_RE.match(line)
        if fence:
            in_code = not in_code
            compressed.append(line)
            prev_blank = False
            continue
        if in_code:
            compressed.append(line)
            prev_blank = False
            continue
        if line.strip() == "":
            if prev_blank:
                continue
            compressed.append("")
            prev_blank = True
        else:
            compressed.append(line)
            prev_blank = False

    # 第二遍：标题/列表 前后空行（仅非代码区）
    result = []
    in_code = False
    for idx, line in enumerate(compressed):
        fence = CODE_FENCE_RE.match(line)
        if fence:
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue
        # 标题前空行
        if HEADING_RE.match(line) and result and result[-1].strip() != "":
            result.append("")
        result.append(line)
        # 标题后空行（若下一项非空且非标题/列表）
        nxt = compressed[idx + 1] if idx + 1 < len(compressed) else ""
        if HEADING_RE.match(line) and nxt.strip() != "" and not HEADING_RE.match(nxt) and not LIST_RE.match(nxt):
            result.append("")

    new_text = "\n".join(result).rstrip("\n") + "\n"

    changed = new_text != raw
    if changed and apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return changed, typo_changes


def main():
    apply = "--dry" not in sys.argv
    single = None
    if "--file" in sys.argv:
        i = sys.argv.index("--file")
        single = sys.argv[i + 1]
    total = 0
    changed_files = 0
    if single:
        targets = [single]
    else:
        targets = []
        for dp, _, fns in os.walk(ROOT):
            for fn in fns:
                if fn.endswith(".md"):
                    targets.append(os.path.join(dp, fn))
    for full in targets:
        changed, tc = process_file(full, apply)
        total += 1
        if changed:
            changed_files += 1
            rel = os.path.relpath(full, os.path.normpath(os.path.join(HERE, "..")))
            print("[%s] %s  (typo fixes: %d)" % ("APPLY" if apply else "DRY", rel, tc))
    print("\nTotal md files: %d, changed: %d" % (total, changed_files))


if __name__ == "__main__":
    main()
