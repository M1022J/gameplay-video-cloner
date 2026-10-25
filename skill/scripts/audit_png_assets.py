#!/usr/bin/env python3
"""
Transparent PNG Sprite Asset Auditor
(from yuzhworkhard-wq/image-to-code SKILL.md hard rules).

Checks every extracted sprite/icon PNG to verify:
1. `has_alpha_channel == True` (RGBA mode)
2. `corner_alpha_max == 0` (no un-removed rectangular white/gray/card background at the 4 corners!)
3. `transparent_bg_ok == True`

Usage:
  python3 audit_png_assets.py ./assets/
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image


def audit_png(path: Path) -> dict:
    im = Image.open(path)
    has_alpha = im.mode == "RGBA" or "transparency" in im.info
    rgba = im.convert("RGBA")
    arr = np.asarray(rgba)
    alpha = arr[:, :, 3]
    corners = [int(alpha[0, 0]), int(alpha[0, -1]), int(alpha[-1, 0]), int(alpha[-1, -1])]
    corner_max = max(corners)
    transparent_ratio = round(float((alpha <= 10).mean()), 3)
    ok = has_alpha and corner_max <= 12 and transparent_ratio >= 0.05
    return {
        "file": path.name,
        "size": [im.width, im.height],
        "has_alpha_channel": has_alpha,
        "corner_alpha_max": corner_max,
        "transparent_pixel_ratio": transparent_ratio,
        "transparent_bg_ok": ok
    }


def main():
    parser = argparse.ArgumentParser(description="Audit extracted sprite PNGs for clean transparent backgrounds.")
    parser.add_argument("target", help="PNG file or directory of PNGs")
    args = parser.parse_args()

    p = Path(args.target)
    files = [p] if p.is_file() else sorted(p.glob("*.png"))
    results = [audit_png(f) for f in files]
    all_ok = all(r["transparent_bg_ok"] for r in results)
    print(json.dumps({"all_transparent_bg_ok": all_ok, "assets": results}, indent=2, ensure_ascii=False))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
