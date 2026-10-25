#!/usr/bin/env python3
"""Build numbered contact sheets for sprite curation (ybuild-ai/ai-game-art-pipeline-skill)."""
import argparse, math
from pathlib import Path
from PIL import Image, ImageDraw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_dir")
    parser.add_argument("output_path")
    parser.add_argument("--cols", type=int, default=6)
    parser.add_argument("--thumb-width", type=int, default=240)
    args = parser.parse_args()
    files = sorted([p for p in Path(args.frames_dir).iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")])
    if not files: return
    w, h = Image.open(files[0]).size
    tw, th = args.thumb_width, max(120, int(h * (args.thumb_width / max(1, w))))
    rows = math.ceil(len(files) / max(1, args.cols))
    sheet = Image.new("RGBA", (args.cols * tw, rows * th), (20, 22, 30, 255))
    draw = ImageDraw.Draw(sheet)
    for idx, fpath in enumerate(files):
        x0, y0 = (idx % args.cols) * tw, (idx // args.cols) * th
        img = Image.open(fpath).convert("RGBA").resize((tw - 8, th - 8))
        sheet.paste(img, (x0 + 4, y0 + 4), img)
        draw.rectangle([x0 + 6, y0 + 6, x0 + min(tw - 10, 150), y0 + 28], fill=(0, 0, 0, 200))
        draw.text((x0 + 10, y0 + 10), f"#{idx+1:02d} {fpath.stem}"[:18], fill=(255, 230, 90, 255))
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)

if __name__ == "__main__":
    main()
