#!/usr/bin/env python3
"""Pack separated body-part PNGs into a Spine .atlas + .png spritesheet (GenielabsOpenSource/spine-animation-ai)."""
import argparse
from pathlib import Path
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts", required=True)
    parser.add_argument("--output", default=".")
    parser.add_argument("--name", default="skeleton")
    args = parser.parse_args()
    pfiles = sorted(Path(args.parts).glob("*.png"))
    if not pfiles: return
    imgs = [(p.stem, Image.open(p).convert("RGBA")) for p in pfiles]
    pad = 4
    total_w, total_h = max(im.width for _, im in imgs) + pad * 2, sum(im.height + pad for _, im in imgs) + pad
    atlas_img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    atlas_img.save(out_dir / f"{args.name}.png")

if __name__ == "__main__":
    main()
