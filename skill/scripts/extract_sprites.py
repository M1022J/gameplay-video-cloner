#!/usr/bin/env python3
"""Crop a sprite or UI element from an extracted video frame and optionally remove solid background."""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_frame")
    parser.add_argument("output_sprite")
    parser.add_argument("--crop", default=None)
    parser.add_argument("--remove-bg", action="store_true")
    parser.add_argument("--tolerance", type=int, default=32)
    args = parser.parse_args()
    img = Image.open(args.input_frame).convert("RGBA")
    if args.crop:
        x1, y1, x2, y2 = [int(v.strip()) for v in args.crop.split(",")]
        img = img.crop((x1, y1, x2, y2))
    if args.remove_bg:
        arr = np.asarray(img, dtype=np.int16)
        corners = np.array([arr[0, 0, :3], arr[0, -1, :3], arr[-1, 0, :3], arr[-1, -1, :3]])
        bg_color = np.median(corners, axis=0)
        dist = np.linalg.norm(arr[:, :, :3] - bg_color, axis=-1)
        out_arr = arr.astype(np.uint8).copy()
        out_arr[:, :, 3] = np.where(dist <= args.tolerance, 0, arr[:, :, 3]).astype(np.uint8)
        img = Image.fromarray(out_arr, mode="RGBA")
    out = Path(args.output_sprite)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)

if __name__ == "__main__":
    main()
