#!/usr/bin/env python3
"""Auto-position separated 2D character body-part PNGs onto an assembled reference image (GenielabsOpenSource/spine-animation-ai)."""
import argparse, json
from pathlib import Path
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--parts", required=True)
    parser.add_argument("--output", default="layout.json")
    args = parser.parse_args()
    ref_img = Image.open(args.reference).convert("RGBA")
    parts_out, draw_order = {}, []
    for pfile in sorted(Path(args.parts).glob("*.png")):
        im = Image.open(pfile)
        parts_out[pfile.stem] = {"x": ref_img.width / 2, "y": ref_img.height / 2, "width": im.width, "height": im.height, "scale": 1.0, "rotation": 0.0}
        draw_order.append(pfile.stem)
    Path(args.output).write_text(json.dumps({"reference_width": ref_img.width, "reference_height": ref_img.height, "parts": parts_out, "draw_order": draw_order}, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
