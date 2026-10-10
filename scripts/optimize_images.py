#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压缩 content/ 下的 PNG/JPG 图片（保持文件名与格式不变，因此无需改动任何文章引用）。

策略：
  1. 超过 MAX_WIDTH 的图先等比缩放到 MAX_WIDTH（正文实际展示宽度远小于此）
  2. PNG 转为 8-bit 调色板量化（256 色）；带 alpha 的用 FASTOCTREE 保留透明通道
  3. JPEG 用 quality=82 重新编码
  4. 若压缩后反而更大（例如本来就是低色位图），则跳过并保留原图

用法：
    python3 scripts/optimize_images.py --dry     # 预览
    python3 scripts/optimize_images.py           # 实际写入
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip3 install Pillow")

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

MAX_WIDTH = 1600      # 正文/封面实际展示宽度上限
MIN_BYTES = 250 * 1024  # 小于 250 KB 的图不值得处理
PNG_COLORS = 256
JPEG_QUALITY = 82
EXTS = {".png", ".jpg", ".jpeg"}


def compress(src: Path) -> tuple[bytes, str]:
    """返回 (新字节, 说明)；失败时抛异常。"""
    with Image.open(src) as im:
        im.load()
        fmt = im.format
        out = im

        if max(out.size) > MAX_WIDTH:
            ratio = MAX_WIDTH / max(out.size)
            new_size = (max(1, round(out.width * ratio)), max(1, round(out.height * ratio)))
            out = out.resize(new_size, Image.LANCZOS)
            note = f"缩放 {im.width}x{im.height} -> {new_size[0]}x{new_size[1]}"
        else:
            note = "原尺寸"

        buf = __import__("io").BytesIO()
        if fmt == "PNG":
            has_alpha = out.mode in ("RGBA", "LA", "P") and "transparency" in out.info or out.mode in ("RGBA", "LA")
            if has_alpha:
                out = out.convert("RGBA").quantize(colors=PNG_COLORS - 1, method=Image.FASTOCTREE)
            else:
                out = out.convert("RGB").quantize(colors=PNG_COLORS, method=Image.MEDIANCUT)
            out.save(buf, format="PNG", optimize=True)
        else:
            if out.mode not in ("RGB",):
                out = out.convert("RGB")
            out.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            note += " / JPEG q82"

        return buf.getvalue(), note


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="只预览，不写文件")
    args = ap.parse_args()

    targets = [p for p in sorted(CONTENT.rglob("*")) if p.suffix.lower() in EXTS]
    before = after = skipped = failed = 0
    rows = []

    for p in targets:
        size = p.stat().st_size
        if size < MIN_BYTES:
            skipped += 1
            continue
        try:
            data, note = compress(p)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  [失败] {p.relative_to(ROOT)}: {e}")
            continue

        if len(data) >= size:
            rows.append((p, size, size, "跳过（压缩后无收益）"))
            skipped += 1
            continue

        before += size
        after += len(data)
        ratio = len(data) / size
        rows.append((p, size, len(data), f"{note} → 剩余 {ratio * 100:.0f}%"))
        if not args.dry:
            p.write_bytes(data)

    print(f"\n{'文件':<62} {'原大小':>9} {'新大小':>9}  说明")
    print("-" * 110)
    for p, s, n, note in rows:
        print(f"{str(p.relative_to(ROOT)):<62} {s / 1024:>8.0f}K {n / 1024:>8.0f}K  {note}")

    print("-" * 110)
    print(f"共 {len(targets)} 张图；处理 {before / 1024 / 1024:.1f} MB → {after / 1024 / 1024:.1f} MB "
          f"（节省 {(before - after) / 1024 / 1024:.1f} MB，降为 {after / max(before, 1) * 100:.0f}%）")
    print(f"跳过 {skipped} 张（体积小或无收益），失败 {failed} 张")
    if args.dry:
        print("\n这是预览，未写入任何文件。去掉 --dry 执行实际压缩。")


if __name__ == "__main__":
    main()
