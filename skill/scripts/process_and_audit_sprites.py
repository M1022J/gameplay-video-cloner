#!/usr/bin/env python3
"""
process_and_audit_sprites.py
Unified Sprite Cropper, Chroma-Key Background Remover & RGBA Corner-Alpha Auditor
(Consolidates and replaces extract_sprites.py, chroma_key_magenta.py, audit_png_assets.py, and provider_stub.py)
Sources:
- yuzhworkhard-wq/image-to-code (Hard RGBA corner-alpha audit rule: corner_alpha_max <= 12)
- ybuild-ai/ai-game-art-pipeline-skill (Magenta #FF00FF chroma key & bounding-box alpha trim)

Subcommands:
  crop      Crop a sprite region from a frame and remove solid background
  chroma    Remove solid #FF00FF (or custom RGB) chroma background with soft ramp & trim
  audit     Audit a PNG or directory of PNGs for true RGBA transparency and zero rectangular border artifacts
"""
import os
import sys
import json
import argparse
from pathlib import Path
import numpy as np
from PIL import Image


def crop_and_clean(input_frame: str, output_sprite: str, crop_box: str = None, remove_bg: bool = True, tolerance: int = 32):
    img = Image.open(input_frame).convert("RGBA")
    if crop_box:
        x1, y1, x2, y2 = [int(v.strip()) for v in crop_box.split(",")]
        img = img.crop((x1, y1, x2, y2))
    if remove_bg:
        arr = np.asarray(img, dtype=np.int16)
        corners = np.array([arr[0, 0, :3], arr[0, -1, :3], arr[-1, 0, :3], arr[-1, -1, :3]])
        bg_color = np.median(corners, axis=0)
        dist = np.linalg.norm(arr[:, :, :3] - bg_color, axis=-1)
        out_arr = arr.astype(np.uint8).copy()
        out_arr[:, :, 3] = np.where(dist <= tolerance, 0, arr[:, :, 3]).astype(np.uint8)
        img = Image.fromarray(out_arr, mode="RGBA")
        if img.getbbox():
            img = img.crop(img.getbbox())
    out = Path(output_sprite)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"[process_and_audit_sprites] Saved sprite -> {out}")


def chroma_key_clean(input_path: str, output_path: str, key_rgb: str = "255,0,255", tolerance: int = 45, trim: bool = True):
    img = Image.open(input_path).convert("RGBA")
    arr = np.asarray(img, dtype=np.float32)
    key = np.array([int(x.strip()) for x in key_rgb.split(",")], dtype=np.float32)
    dist = np.linalg.norm(arr[:, :, :3] - key, axis=-1)
    inner = max(0.0, float(tolerance) * 0.75)
    alpha_factor = np.clip((dist - inner) / max(1.0, float(tolerance) - inner), 0.0, 1.0)
    arr[:, :, 3] *= alpha_factor
    out_img = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    if trim and out_img.getbbox():
        out_img = out_img.crop(out_img.getbbox())
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out)
    print(f"[process_and_audit_sprites] Chroma-keyed sprite -> {out}")


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
        "transparent_bg_ok": ok,
    }


def main():
    parser = argparse.ArgumentParser(description="Unified Sprite Cropper, Chroma-Key Cleaner & RGBA Alpha Auditor.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_crop = sub.add_parser("crop")
    p_crop.add_argument("input_frame")
    p_crop.add_argument("output_sprite")
    p_crop.add_argument("--crop", default=None, help="x1,y1,x2,y2")
    p_crop.add_argument("--tolerance", type=int, default=32)

    p_chroma = sub.add_parser("chroma")
    p_chroma.add_argument("input")
    p_chroma.add_argument("output")
    p_chroma.add_argument("--key", default="255,0,255")
    p_chroma.add_argument("--tolerance", type=int, default=45)

    p_audit = sub.add_parser("audit")
    p_audit.add_argument("target", help="PNG file or directory of PNGs")

    args = parser.parse_args()
    if args.cmd == "crop":
        crop_and_clean(args.input_frame, args.output_sprite, args.crop, True, args.tolerance)
    elif args.cmd == "chroma":
        chroma_key_clean(args.input, args.output, args.key, args.tolerance, True)
    elif args.cmd == "audit":
        p = Path(args.target)
        files = [p] if p.is_file() else sorted(p.glob("*.png"))
        results = [audit_png(f) for f in files]
        all_ok = all(r["transparent_bg_ok"] for r in results)
        print(json.dumps({"all_transparent_bg_ok": all_ok, "assets": results}, indent=2, ensure_ascii=False))
        if not all_ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
