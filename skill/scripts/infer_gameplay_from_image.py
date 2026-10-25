#!/usr/bin/env python3
"""
Reverse-engineer gameplay mechanics, spatial layout, entity distribution, and a machine-checkable
features.csv matrix directly from a single game screenshot or extracted video frame
(integrating Jakeschincariol/replica-skill /replica-recon, yuzhworkhard-wq/image-to-code, and Yakoub-ai/phaser4-gamedev).

Produces:
1. `recon_gameplay_spec.json`:
   - Exact image dimensions, aspect ratio, and 3-zone spatial layout (Top HUD, Center Playfield, Bottom Control/Tray)
   - Detected visual entities / connected components (count, bounding boxes, size distribution, grid vs radial vs vertical-stack pattern)
   - Inferred candidate genre archetypes & core loop rules
   - Layer Classification Table (code-rendered UI vs transparent PNG sprites)
2. `features.csv`:
   - Prioritized feature checklist (`must`, `should`, `could`) for `/replica-build` and `/replica-diff` parity scoring.

Usage:
  python3 infer_gameplay_from_image.py screenshot.png ./recon_output
"""
import argparse
import csv
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def analyze_screenshot(img_path: str, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    pil_img = Image.open(img_path).convert("RGB")
    w, h = pil_img.size
    gcd_val = math.gcd(w, h)
    aspect = f"{w // gcd_val}:{h // gcd_val}"
    is_portrait = h > w

    bgr = cv2.imread(img_path)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 160)

    # 1. Measure 3-Zone Edge Density (Top HUD vs Center Playfield vs Bottom Control/Tray)
    top_h = int(h * 0.16)
    bot_h = int(h * 0.80)
    top_density = round(float(edges[:top_h, :].mean()), 2)
    mid_density = round(float(edges[top_h:bot_h, :].mean()), 2)
    bot_density = round(float(edges[bot_h:, :].mean()), 2)

    # 2. Detect Candidate Gameplay Entities via Contours in Playfield
    playfield_edges = edges[top_h:bot_h, :]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(playfield_edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    entities = []
    circular_count = 0
    rect_grid_count = 0
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if area < (w * h * 0.0015) or area > (w * h * 0.35):
            continue
        peri = cv2.arcLength(cnt, True)
        circularity = 4 * math.pi * cv2.contourArea(cnt) / max(1.0, peri * peri)
        aspect_box = cw / max(1.0, float(ch))
        shape_type = "circle_or_orb" if circularity > 0.68 else ("square_tile" if 0.8 <= aspect_box <= 1.25 else "sprite_or_bar")
        if shape_type == "circle_or_orb":
            circular_count += 1
        elif shape_type == "square_tile":
            rect_grid_count += 1
        entities.append({
            "bbox_playfield": [int(x), int(y + top_h), int(cw), int(ch)],
            "shape_hint": shape_type,
            "circularity": round(circularity, 2)
        })

    # 3. Infer Candidate Gameplay Genre & Core Loop from Visual Affordances
    inferred_genres = []
    if circular_count >= 5 and is_portrait:
        inferred_genres.append({
            "genre": "Physics Drop-Merge / Suika OR Bullet-Heaven Survivor",
            "visual_evidence": f"Portrait viewport with {circular_count} circular/orb entities in playfield",
            "inferred_core_loop": "Aim/drag at top or center -> drop/spawn -> circle-circle collision & tier merge / wave dodge -> score & combo escalation"
        })
    if rect_grid_count >= 6:
        inferred_genres.append({
            "genre": "Grid Puzzle / Tile-Match / Block Blast / Tower Defense",
            "visual_evidence": f"Detected {rect_grid_count} regular square/tile cells in playfield + bottom tray density {bot_density}",
            "inferred_core_loop": "Select/drag tile or card from bottom deck -> snap to grid cell -> match/clear row/column or place tower -> cascade combo"
        })
    if not inferred_genres:
        inferred_genres.append({
            "genre": "2D Action Arcade / Platformer / Roguelike Arena",
            "visual_evidence": f"Playfield entity count={len(entities)}, top HUD density={top_density}, bottom control density={bot_density}",
            "inferred_core_loop": "Move/jump/aim via pointer or WASD -> collide with targets/pickups -> trigger Juice feedback & HUD score/HP update"
        })

    # 4. Extract Dominant Design Tokens (Colors)
    small_rgb = pil_img.resize((100, 100)).quantize(colors=6)
    pal = small_rgb.getpalette()[:18]
    hex_tokens = [f"#{pal[i]:02x}{pal[i+1]:02x}{pal[i+2]:02x}" for i in range(0, len(pal), 3)]

    spec = {
        "source_image": img_path,
        "dimensions": {"width": w, "height": h, "aspect_ratio": aspect, "orientation": "portrait" if is_portrait else "landscape"},
        "spatial_zones": {
            "top_hud_band_px": [0, top_h],
            "center_playfield_px": [top_h, bot_h],
            "bottom_control_or_tray_px": [bot_h, h],
            "edge_density": {"top_hud": top_density, "playfield": mid_density, "bottom_deck": bot_density}
        },
        "detected_entities_count": len(entities),
        "shape_distribution": {"circular_orbs": circular_count, "square_tiles": rect_grid_count},
        "inferred_gameplay_candidates": inferred_genres,
        "design_tokens_hex": hex_tokens,
        "layer_classification_rules": {
            "code_rendered": ["background gradient/grid", "HUD progress bars", "score/timer typography", "buttons & cards", "particle effects"],
            "transparent_png_sprites": ["hero character", "enemy/boss sprites", "custom item icons (require alpha=0 at corners)"]
        }
    }

    spec_path = out_dir / "recon_gameplay_spec.json"
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")

    # 5. Write replica-recon features.csv matrix
    features_rows = [
        ["id", "category", "feature", "priority", "status", "verification_method"],
        ["F01", "viewport", f"Lock {aspect} responsive canvas matching source {w}x{h} layout", "must", "todo", "imgdiff_parity.py"],
        ["F02", "hud", "Top HUD bar with live score, progress/HP meter, and state badges", "must", "todo", "render_game_to_text"],
        ["F03", "controls", "Dual pointer/touch + keyboard (WASD/Arrows/Space) input controller", "must", "todo", "validate_architecture.py"],
        ["F04", "core_loop", inferred_genres[0]["inferred_core_loop"], "must", "todo", "render_game_to_text"],
        ["F05", "skeletal_vfx", "Articulated 2D/3D character rig + trauma^2 shake + hit-stop + particles", "should", "todo", "validate_architecture.py"],
        ["F06", "audio_tuning", "Procedural Web Audio SFX + collapsible live parameter tuning drawer", "could", "todo", "validate_architecture.py"]
    ]
    csv_path = out_dir / "features.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerows(features_rows)

    print(f"Saved gameplay recon spec to {spec_path} and feature matrix to {csv_path}")
    return spec


def main():
    parser = argparse.ArgumentParser(description="Reverse-engineer gameplay mechanics and features.csv from a screenshot.")
    parser.add_argument("image_path", help="Path to input game screenshot PNG/JPG")
    parser.add_argument("output_dir", help="Output directory for recon_gameplay_spec.json and features.csv")
    args = parser.parse_args()
    analyze_screenshot(args.image_path, Path(args.output_dir))


if __name__ == "__main__":
    main()
