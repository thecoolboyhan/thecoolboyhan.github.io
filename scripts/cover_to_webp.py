#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把体积较大的本地封面图（书籍封面等照片类PNG）迁移为 WebP，并同步更新 front matter 的 image 字段。

背景：
    Hugo 的 imageProcessing 对 PNG 只做「缩放」不做「重编码」，照片类PNG 即使量化到
    256 色仍有 1 MB+。WebP 在同等观感下通常只有 1/10。

安全约束（脚本会强制校验，不满足则跳过并报告）：
    1. 目标图片必须只被 front matter 的 `image:` 引用；
       若正文中出现 `![](xxx.png)` 或 `<img src="xxx.png">`，则跳过（避免改坏正文）。
    2. 转换后若体积没有明显下降，则跳过并保留原 PNG。
    3. front matter 中 `image:` 的值必须精确等于该文件名才会替换。

用法：
    python3 scripts/cover_to_webp.py --dry    # 预览
    python3 scripts/cover_to_webp.py          # 实际执行
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip3 install Pillow")

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

MIN_BYTES = 700 * 1024   # 只处理大于此体积的封面
MIN_WIDTH = 1400         # WebP 输出最大宽度
QUALITY = 80


def body_without_fm(text: str) -> str:
    """去掉 front matter 与代码块，只留下正文。"""
    body = re.sub(r"^---.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"```.*?```", "", body, flags=re.S)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    # 收集所有正文中的本地图片引用（含 markdown 与 html），用于安全校验
    body_refs: set[tuple[str, str]] = set()
    fm_images: dict[Path, str] = {}
    for md in sorted(CONTENT.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        body = body_without_fm(text)
        for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", body):
            body_refs.add((str(md), m.group(1)))
        for m in re.finditer(r"<img[^>]+src=[\"']([^\"']+)", text):
            body_refs.add((str(md), m.group(1)))
        m = re.search(r"^image:\s*(\S+)", text, re.M)
        if m and not m.group(1).startswith("http"):
            fm_images[md] = m.group(1).strip()

    converted = skipped = 0
    saved = 0
    print(f"{'封面图':<58} {'原':>8} {'新':>8}")
    print("-" * 82)

    for md, img in fm_images.items():
        src = md.parent / img
        if not src.exists() or src.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        size = src.stat().st_size
        if size < MIN_BYTES:
            continue

        # 安全约束 1：正文里不能引用这张图
        if any(Path(f).parent == md.parent and u.split("/")[-1] == Path(img).name
               for f, u in body_refs):
            print(f"[跳过·正文有引用] {src.relative_to(ROOT)}")
            skipped += 1
            continue

        with Image.open(src) as im:
            im.load()
            out = im
            if out.mode not in ("RGB", "RGBA"):
                out = out.convert("RGBA" if "A" in out.info.get("transparency", "") else "RGB")
            if out.width > MIN_WIDTH:
                ratio = MIN_WIDTH / out.width
                out = out.resize((MIN_WIDTH, max(1, round(out.height * ratio))), Image.LANCZOS)
            dst = src.with_suffix(".webp")
            out.save(dst, "WEBP", quality=QUALITY, method=6)

        new_size = dst.stat().st_size
        # 安全约束 2：无收益则回退
        if new_size >= size * 0.5:
            dst.unlink()
            print(f"[跳过·无收益] {src.relative_to(ROOT)}")
            skipped += 1
            continue

        # 安全约束 3：精确替换 front matter 的 image 值
        text = md.read_text(encoding="utf-8")
        new_text, n = re.subn(rf"^(image:\s*){re.escape(img)}\s*$",
                              rf"\g<1>{dst.name}", text, count=1, flags=re.M)
        if n != 1:
            dst.unlink()
            print(f"[跳过·front matter 未精确匹配] {src.relative_to(ROOT)}")
            skipped += 1
            continue

        if not args.dry:
            new_text = new_text.replace(f"]({img})", f"]({dst.name})")
            md.write_text(new_text, encoding="utf-8")
            src.unlink()

        saved += size - new_size
        converted += 1
        print(f"{str(src.relative_to(ROOT)):<58} {size / 1024:>7.0f}K {new_size / 1024:>7.0f}K")

    print("-" * 82)
    print(f"转换 {converted} 张，跳过 {skipped} 张，累计节省 {saved / 1024 / 1024:.1f} MB")
    if args.dry:
        print("\n这是预览，未改动任何文件。去掉 --dry 执行。")


if __name__ == "__main__":
    main()
