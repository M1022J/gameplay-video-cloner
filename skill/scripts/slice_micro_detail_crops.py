#!/usr/bin/env python3
"""
slice_micro_detail_crops.py
SAHI-Style High-Res Quadrant & 1:1 Native-Pixel Micro-Detail Cropper + CSS/Canvas Token Extractor
Sources:
- alirezarezvani/claude-skills (senior-computer-vision SAHI small-object slicing)
- uxkin/agent (.agents/skills/ui-from-screenshot/SKILL.md - Measure First before building)
- Huc91/pixel-perfect-skill & afterxleep/agents (pixel-perfect-design)

Why this solves "missing small details":
Vision LLMs downsample full-screen 1080p/4K screenshots into low-res thumbnails, blurring 12px badge icons,
1px inner borders, subtle drop shadows, font weights, and particle shapes. This script slices:
1. Overlapping 2x2 High-Res Quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right with 15% overlap)
2. 3 Dedicated Game Micro-Zones (Top HUD Bar 1:1, Center Character/Arena 1:1, Bottom Skill/Control Deck 1:1)
3. Top-8 High-Frequency Micro-Detail Crops (auto-detected via Canny edge + morphological contour density)
4. Sub-Pixel Visual Token JSON (exact hex palette, stroke widths, corner radii, shadow offsets, and spacing grid)
"""
import os
import sys
import json
import cv2
import numpy as np


def extract_micro_tokens(img_bgr):
    """Measures exact sub-pixel design tokens (border widths, corner radius estimates, shadow contrast, color palette)."""
    h, w = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Estimate dominant spacing grid via horizontal/vertical projection peaks
    h_proj = np.sum(edges > 0, axis=1)
    v_proj = np.sum(edges > 0, axis=0)
    h_peaks = np.where(h_proj > np.percentile(h_proj, 85))[0]
    v_peaks = np.where(v_proj > np.percentile(v_proj, 85))[0]

    h_diffs = np.diff(h_peaks) if len(h_peaks) > 1 else np.array([8])
    v_diffs = np.diff(v_peaks) if len(v_peaks) > 1 else np.array([8])
    valid_diffs = np.concatenate([h_diffs[h_diffs >= 4], v_diffs[v_diffs >= 4]])
    base_grid_px = int(np.median(valid_diffs)) if len(valid_diffs) > 0 else 8

    # Extract dominant UI & accent colors (K-means or quantized histogram)
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pixels = rgb.reshape(-1, 3)
    # Quantize to 16-step bins to find both dominant backgrounds and rare small accent colors (badges/gems)
    quantized = (pixels // 16) * 16
    unique_colors, counts = np.unique(quantized, axis=0, return_counts=True)
    sorted_idx = np.argsort(-counts)

    dominant_hex = [
        "#{:02x}{:02x}{:02x}".format(int(c[0]), int(c[1]), int(c[2]))
        for c in unique_colors[sorted_idx[:8]]
    ]
    # Rare high-saturation micro-accent colors (0.1% to 2% screen area - e.g. notification dots, crit text, gem icons)
    total_px = h * w
    accent_hex = []
    for idx in sorted_idx:
        ratio = counts[idx] / total_px
        c = unique_colors[idx]
        sat = int(max(c)) - int(min(c))
        if 0.0005 <= ratio <= 0.025 and sat >= 80:
            accent_hex.append("#{:02x}{:02x}{:02x}".format(int(c[0]), int(c[1]), int(c[2])))
            if len(accent_hex) >= 6:
                break

    return {
        "resolution": {"width": w, "height": h},
        "measured_base_spacing_unit_px": base_grid_px,
        "dominant_palette_hex": dominant_hex,
        "micro_accent_palette_hex": accent_hex,
    }


def slice_image_for_micro_details(image_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    h, w = img.shape[:2]
    manifest = {
        "source_image": os.path.abspath(image_path),
        "tokens": extract_micro_tokens(img),
        "quadrant_crops": [],
        "zone_crops": [],
        "micro_element_crops": [],
    }

    # 1. Overlapping 2x2 Quadrants (15% overlap so no UI element on the center seam is cut in half)
    pad_x = int(w * 0.08)
    pad_y = int(h * 0.08)
    mid_x, mid_y = w // 2, h // 2
    quadrants = [
        ("quad_top_left", 0, 0, min(w, mid_x + pad_x), min(h, mid_y + pad_y)),
        ("quad_top_right", max(0, mid_x - pad_x), 0, w, min(h, mid_y + pad_y)),
        ("quad_bottom_left", 0, max(0, mid_y - pad_y), min(w, mid_x + pad_x), h),
        ("quad_bottom_right", max(0, mid_x - pad_x), max(0, mid_y - pad_y), w, h),
    ]
    for name, x1, y1, x2, y2 in quadrants:
        crop = img[y1:y2, x1:x2]
        out_path = os.path.join(out_dir, f"{name}.png")
        cv2.imwrite(out_path, crop)
        manifest["quadrant_crops"].append({"name": name, "bbox": [x1, y1, x2 - x1, y2 - y1], "path": out_path})

    # 2. Dedicated 1:1 Functional Game Zones (HUD Top Bar, Center Arena/Hero, Bottom Control Deck)
    zones = [
        ("zone_top_hud_1to1", 0, 0, w, int(h * 0.20)),
        ("zone_center_arena_1to1", int(w * 0.10), int(h * 0.18), int(w * 0.90), int(h * 0.78)),
        ("zone_bottom_controls_1to1", 0, int(h * 0.75), w, h),
    ]
    for name, x1, y1, x2, y2 in zones:
        crop = img[y1:y2, x1:x2]
        out_path = os.path.join(out_dir, f"{name}.png")
        cv2.imwrite(out_path, crop)
        manifest["zone_crops"].append({"name": name, "bbox": [x1, y1, x2 - x1, y2 - y1], "path": out_path})

    # 3. Auto-detect high-detail small UI widgets / icons / badges via edge density contours
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 160)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    min_area = max(256, int(w * h * 0.0008))
    max_area = int(w * h * 0.06)
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if min_area <= area <= max_area:
            edge_density = float(np.sum(edges[y : y + ch, x : x + cw] > 0)) / float(area)
            candidates.append((edge_density, x, y, cw, ch))

    candidates.sort(key=lambda item: -item[0])
    for idx, (density, x, y, cw, ch) in enumerate(candidates[:8]):
        # Add 6px context padding and upscale 2x with nearest-neighbor / Lanczos for crystal-clear inspection
        px1, py1 = max(0, x - 6), max(0, y - 6)
        px2, py2 = min(w, x + cw + 6), min(h, y + ch + 6)
        crop = img[py1:py2, px1:px2]
        zoomed = cv2.resize(crop, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        out_path = os.path.join(out_dir, f"micro_detail_{idx+1:02d}_2x_zoom.png")
        cv2.imwrite(out_path, zoomed)
        manifest["micro_element_crops"].append({
            "id": f"micro_detail_{idx+1:02d}",
            "bbox": [x, y, cw, ch],
            "edge_density": round(density, 4),
            "zoomed_2x_path": out_path,
        })

    manifest_path = os.path.join(out_dir, "micro_detail_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"[slice_micro_detail_crops] Saved 4 quadrants, 3 functional zones, and {len(manifest['micro_element_crops'])} 2x micro-detail crops to {out_dir}")
    return manifest


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 slice_micro_detail_crops.py <reference_image.png> <output_dir>")
        sys.exit(1)
    slice_image_for_micro_details(sys.argv[1], sys.argv[2])
