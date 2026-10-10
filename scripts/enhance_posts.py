#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文章排版结构优化（通用、保守、可复现）

处理两类纯机械问题，规则保守，改动前可 dry 预览：

1. 松散列表合并：「列表项是词条 + 说明另起一段」→ 合并为「列表项：说明」

       - 堆初始大小
       （空行）
       -Xms

   改为：

       - **堆初始大小**：-Xms

2. 标题层级跳级修正：h2 之后直接出现 h4 时降为 h3（只降不升）

用法:
    python3 scripts/enhance_posts.py --dry                # 预览全部精选文章
    python3 scripts/enhance_posts.py                      # 实际写入
    python3 scripts/enhance_posts.py --file path/index.md # 只处理单篇
    python3 scripts/enhance_posts.py --all                # 含非精选
    python3 scripts/enhance_posts.py --dry --verbose      # 打印每处改动
"""
import argparse
import os
import re

CONTENT = 'content/post'
MAX_ITEM_LEN = 28      # 列表项超过此长度不当作「词条」
MAX_DESC = 3           # 最多合并几个说明段落
MAX_MERGED = 220       # 合并后单行长度上限

# 说明段落出现这些特征就放弃合并（说明它不是对词条的简短说明）
BLOCK_PAT = re.compile(r'^(```|~~~|!\[|#{1,6}\s|\||>|<[a-zA-Z/]|\{\{<|\*\*[^*]+\*\*\s*$|[-*+]\s|\d+\.\s)')
ITEM_RE = re.compile(r'^(\s*)([-*+]|\d+[.)])\s+(\S.*)$')
FENCE_RE = re.compile(r'^\s*(```|~~~)')


TAGS = ('span', 'mark', 'code', 'a', 'em', 'strong', 'b', 'i', 'u', 'sub', 'sup', 'font')


def tags_balanced(text):
    low = text.lower()
    for tg in TAGS:
        if low.count('<%s' % tg) != low.count('</%s>' % tg):
            return False
    if low.count('<span') != low.count('</span>'):
        return False
    return True



def split_fm(text):
    m = re.match(r'^(---\n.*?\n---\n)', text, re.S)
    return (m.group(1), text[m.end():]) if m else ('', text)


def merge_loose_lists(body, report):
    lines, out, i, n = body.split('\n'), [], 0, len(body.split('\n'))
    while i < n:
        line = lines[i]
        out.append(line)
        m = ITEM_RE.match(line)
        if not m or FENCE_RE.match(line):
            i += 1
            continue
        indent, marker, item = m.group(1), m.group(2), m.group(3)
        if item.startswith('**') or len(item) > MAX_ITEM_LEN:
            i += 1
            continue
        # 收集紧随其后的「空行 + 说明段落」序列
        descs, j, blank = [], i + 1, False
        while j < n:
            cur = lines[j]
            if not cur.strip():
                blank = True
                j += 1
                continue
            s = cur.strip()
            if not blank or BLOCK_PAT.match(s) or re.match(r'^\[.+\]\(.+\)$', s):
                break
            # 说明段落本身是「**词条**：说明」结构 → 它是另一个列表项，不该被吞进来
            if re.match(r'^\*\*[^*]+\*\*\s*[：:]', s):
                break
            # 说明段落以列表项标记开头却没被 BLOCK_PAT 拦住的兜底
            if re.match(r'^([-*+]\s|\d+[.)]\s)', s):
                break
            if indent and not cur.startswith(indent):
                break
            descs.append(s)
            blank = False
            j += 1
        if not descs or len(descs) > MAX_DESC or len(item) + len(' '.join(descs)) > MAX_MERGED:
            i += 1
            continue
        body_txt = ' '.join(descs)
        # 合并后 Markdown 结构必须仍然自洽，否则放弃
        if body_txt.count('**') % 2:            # 产生悬空加粗
            i += 1
            continue
        if body_txt.count('<') != body_txt.count('>'):   # 标签不配对
            i += 1
            continue
        if re.match(r'^[，。、；：！？）】」』%s,.;:!?]', body_txt):  # 说明以标点开头=切错了
            i += 1
            continue
        if body_txt.rstrip().endswith(('**', '<', '`')):  # 跨段强调/标签/代码，闭合在后面
            i += 1
            continue
        if not tags_balanced(item + body_txt):                # 标签必须成对
            i += 1
            continue
        merged = '%s%s **%s**：%s' % (indent, marker, item, body_txt)
        out[-1] = merged
        report.append('列表合并 | ' + merged.strip()[:88])
        i = j
    return '\n'.join(out)


def fix_heading_jumps(body, report):
    out, prev, fence = [], 0, False
    for line in body.split('\n'):
        if FENCE_RE.match(line):
            fence = not fence
        if not fence:
            m = re.match(r'^(#{1,6})\s+(\S.*)$', line)
            if m:
                lvl = len(m.group(1))
                if prev and lvl > prev + 1:
                    line = '%s %s' % ('#' * (prev + 1), m.group(2))
                    report.append('标题降级 | %s %s' % (line[:20], m.group(2)[:60]))
                    lvl = prev + 1
                prev = lvl
        out.append(line)
    return '\n'.join(out)


def collect(only_featured, explicit):
    if explicit:
        return [explicit]
    hits = []
    for root, _d, files in os.walk(CONTENT):
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            if only_featured and '精选' not in split_fm(open(p, encoding='utf-8').read())[0]:
                continue
            hits.append(p)
    return sorted(hits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--file')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()
    files = collect(not a.all and not a.file, a.file)
    print('待处理 %d 篇\n' % len(files))
    total = 0
    for p in files:
        raw = open(p, encoding='utf-8').read()
        fm, body = split_fm(raw)
        r = []
        b2 = merge_loose_lists(fix_heading_jumps(body, r), r)
        if r:
            print('%s  (%d 处)' % (p, len(r)))
            if a.verbose:
                for x in r:
                    print('    ' + x)
            total += len(r)
        if not a.dry and b2 != body:
            open(p, 'w', encoding='utf-8').write(fm + b2)
    print('\n合计 %d 处%s' % (total, '（预览，未写入）' if a.dry else '（已写入）'))


if __name__ == '__main__':
    main()
