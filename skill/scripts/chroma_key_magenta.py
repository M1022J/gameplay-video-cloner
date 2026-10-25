#!/usr/bin/env python3
"""Remove solid magenta (#FF00FF) or custom chroma key backgrounds (ybuild-ai/ai-game-art-pipeline-skill)."""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--key", default="255,0,255")
    parser.add_argument("--tolerance", type=int, default=45)
    parser.add_argument("--trim", action="store_true")
    args = parser.parse_args()
    img = Image.open(args.input).convert("RGBA")
    arr = np.asarray(img, dtype=np.float32)
    key = np.array([int(x.strip()) for x in args.key.split(",")], dtype=np.float32)
    dist = np.linalg.norm(arr[:, :, :3] - key, axis=-1)
    inner = max(0.0, float(args.tolerance) * 0.75)
    alpha_factor = np.clip((dist - inner) / max(1.0, float(args.tolerance) - inner), 0.0, 1.0)
    arr[:, :, 3] *= alpha_factor
    out_img = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    if args.trim and out_img.getbbox():
        out_img = out_img.crop(out_img.getbbox())
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out)

if __name__ == "__main__":
    main()
