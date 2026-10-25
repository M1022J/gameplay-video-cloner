#!/usr/bin/env python3
"""
visual_verdict_diff_loop.py
Automated 3-Panel Side-by-Side Comparison (`Reference | Built | Delta-E Heatmap`) & 6-Dimension Visual Verdict Scorer
Sources:
- vibeeval/vibecosystem (skills/visual-verdict/SKILL.md - 6-Dimension Weighted Scoring Rubric & PASS >= 90 Gate)
- Huc91/pixel-perfect-skill & afterxleep/agents (pixel-perfect-design)
- garrytan/gstack (design-review & qa - Measure -> Compare -> Atomic Fix Loop)
- Intense-Visions/harness-engineering (harness-visual-regression)

Dimensions & Weights (vibeeval/visual-verdict formula):
1. Layout & Spatial Occupancy (Weight: 0.25) - Quadrant structural SSIM & edge alignment
2. Typography & HUD Hierarchy (Weight: 0.15) - High-frequency text/number region sharpness & placement
3. Color Palette & Delta-E Fidelity (Weight: 0.15) - CIE76 / LAB perceptual color distance
4. Aspect Ratio & Viewport Integrity (Weight: 0.15) - Zero clipping/overflow, exact aspect ratio match
5. Micro-States & Polish Details (Weight: 0.15) - Presence of borders, shadows, gradients, and micro-accents
6. Content & Element Completeness (Weight: 0.15) - Contour/component count parity across all 4 quadrants

Verdict Thresholds:
- PASS: Composite Score >= 90.0 (and no dimension < 75.0)
- REVISE: Composite Score 60.0 - 89.9 (outputs actionable per-quadrant fix list)
- FAIL: Composite Score < 60.0 (major architectural or visual mismatch)
"""
import os
import sys
import json
import subprocess
import cv2
import numpy as np


def render_url_or_html_to_png(target: str, output_png: str, width: int = 1280, height: int = 720):
    """Uses headless chromium if target is a URL or .html file; otherwise copies existing image."""
    if os.path.exists(target) and target.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        img = cv2.imread(target)
        cv2.imwrite(output_png, img)
        return output_png

    url = target if target.startswith("http") else f"file://{os.path.abspath(target)}"
    cmd = [
        "chromium",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={width},{height}",
        f"--screenshot={output_png}",
        url,
    ]
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_png


def compute_visual_verdict(ref_path: str, built_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    ref = cv2.imread(ref_path, cv2.IMREAD_COLOR)
    if ref is None:
        raise FileNotFoundError(f"Reference image not found: {ref_path}")

    h, w = ref.shape[:2]
    built_png = os.path.join(out_dir, "built_capture.png")
    render_url_or_html_to_png(built_path, built_png, width=w, height=h)

    built = cv2.imread(built_png, cv2.IMREAD_COLOR)
    if built is None:
        raise RuntimeError(f"Failed to load or render built target: {built_path}")

    # Aspect ratio & viewport check before resizing for pixel comparison
    bh, bw = built.shape[:2]
    aspect_diff = abs((w / max(1, h)) - (bw / max(1, bh)))
    responsive_score = max(0.0, min(100.0, 100.0 - aspect_diff * 150.0))

    if (bh, bw) != (h, w):
        built_resized = cv2.resize(built, (w, h), interpolation=cv2.INTER_AREA)
    else:
        built_resized = built.copy()

    # 1. CIE LAB Delta-E Perceptual Color Distance
    ref_lab = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).astype(np.float32)
    built_lab = cv2.cvtColor(built_resized, cv2.COLOR_BGR2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - built_lab) ** 2, axis=2))
    mean_delta_e = float(np.mean(delta_e))
    color_score = max(0.0, min(100.0, 100.0 - (mean_delta_e * 1.6)))

    # 2. Layout & Spatial Occupancy (Edge & Luminance Structural Alignment across 4 Quadrants)
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    built_gray = cv2.cvtColor(built_resized, cv2.COLOR_BGR2GRAY)
    ref_edges = cv2.Canny(ref_gray, 50, 150)
    built_edges = cv2.Canny(built_gray, 50, 150)

    # Dilate edges by 4px to forgive minor 2-3px jitter while penalizing missing/misplaced layout blocks
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    ref_dil = cv2.dilate(ref_edges, kernel)
    built_dil = cv2.dilate(built_edges, kernel)

    overlap = np.logical_and(ref_dil > 0, built_dil > 0).sum()
    union = np.logical_or(ref_dil > 0, built_dil > 0).sum()
    edge_iou = float(overlap) / float(max(1, union))
    layout_score = max(0.0, min(100.0, edge_iou * 115.0))

    # 3. Typography & HUD Hierarchy (Top 20% + Bottom 20% High-Frequency Detail Ratio)
    hud_mask = np.zeros((h, w), dtype=np.uint8)
    hud_mask[: int(h * 0.22), :] = 1
    hud_mask[int(h * 0.78) :, :] = 1
    ref_hud_edges = max(1, int(np.sum((ref_edges > 0) & (hud_mask > 0))))
    built_hud_edges = int(np.sum((built_edges > 0) & (hud_mask > 0)))
    hud_ratio = min(ref_hud_edges, built_hud_edges) / float(max(ref_hud_edges, built_hud_edges))
    typography_score = max(0.0, min(100.0, hud_ratio * 100.0))

    # 4. Micro-States & Polish Details (Gradient smoothness, shadow/border contrast variance)
    ref_lap = float(cv2.Laplacian(ref_gray, cv2.CV_64F).var())
    built_lap = float(cv2.Laplacian(built_gray, cv2.CV_64F).var())
    polish_ratio = min(ref_lap, built_lap) / float(max(1.0, max(ref_lap, built_lap)))
    micro_polish_score = max(0.0, min(100.0, (polish_ratio ** 0.5) * 100.0))

    # 5. Content & Element Completeness (Per-Quadrant Component Count Parity)
    quads = [
        ("Top-Left (HUD/Avatar)", 0, 0, w // 2, h // 2),
        ("Top-Right (Currency/Settings)", w // 2, 0, w, h // 2),
        ("Bottom-Left (Controls/Skills)", 0, h // 2, w // 2, h),
        ("Bottom-Right (Action/Buttons)", w // 2, h // 2, w, h),
    ]
    quad_reports = []
    completeness_scores = []
    actionable_fixes = []

    for qname, x1, y1, x2, y2 in quads:
        rq = ref_edges[y1:y2, x1:x2]
        bq = built_edges[y1:y2, x1:x2]
        rc_cnt, _ = cv2.findContours(cv2.dilate(rq, np.ones((5, 5), np.uint8)), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bc_cnt, _ = cv2.findContours(cv2.dilate(bq, np.ones((5, 5), np.uint8)), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        r_num = len([c for c in rc_cnt if cv2.contourArea(c) >= 36])
        b_num = len([c for c in bc_cnt if cv2.contourArea(c) >= 36])
        q_delta_e = float(np.mean(delta_e[y1:y2, x1:x2]))
        parity = min(r_num, b_num) / float(max(1, max(r_num, b_num))) if max(r_num, b_num) > 0 else 1.0
        q_score = round(parity * 100.0, 1)
        completeness_scores.append(q_score)
        quad_reports.append({
            "quadrant": qname,
            "reference_micro_elements": r_num,
            "built_micro_elements": b_num,
            "quadrant_delta_e": round(q_delta_e, 2),
            "completeness_score": q_score,
        })
        if b_num < r_num:
            actionable_fixes.append(
                f"[{qname}] Missing ~{r_num - b_num} micro-elements (reference has {r_num}, built has {b_num}). Inspect 1:1 quadrant crop for omitted icons, badges, or borders."
            )
        if q_delta_e > 18.0:
            actionable_fixes.append(
                f"[{qname}] High color/contrast mismatch (Delta-E={q_delta_e:.1f}). Check background panel opacity, gradient stops, or shadow fill."
            )

    completeness_score = float(np.mean(completeness_scores))

    # Weighted Composite Score (vibeeval/visual-verdict formula)
    composite = (
        layout_score * 0.25
        + typography_score * 0.15
        + color_score * 0.15
        + responsive_score * 0.15
        + micro_polish_score * 0.15
        + completeness_score * 0.15
    )
    composite = round(float(composite), 2)

    min_dim = min(layout_score, typography_score, color_score, responsive_score, micro_polish_score, completeness_score)
    if composite >= 90.0 and min_dim >= 75.0:
        verdict = "PASS"
    elif composite >= 60.0:
        verdict = "REVISE"
    else:
        verdict = "FAIL"

    # Generate 3-Panel Side-by-Side Comparison Image (Original | Built | Delta-E Heatmap)
    norm_de = np.clip(delta_e * 2.5, 0, 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(norm_de, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(built_resized, 0.45, heatmap, 0.55, 0)

    banner_h = 44
    panel_w = w * 3
    canvas = np.zeros((h + banner_h, panel_w, 3), dtype=np.uint8)
    canvas[:banner_h, :] = (24, 24, 28)
    canvas[banner_h:, 0:w] = ref
    canvas[banner_h:, w : w * 2] = built_resized
    canvas[banner_h:, w * 2 : w * 3] = overlay

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(canvas, "1. ORIGINAL REFERENCE", (16, 29), font, 0.7, (255, 255, 255), 2)
    cv2.putText(canvas, "2. BUILT GAME CAPTURE", (w + 16, 29), font, 0.7, (120, 255, 160), 2)
    cv2.putText(
        canvas,
        f"3. DELTA-E DIFF HEATMAP | {verdict} ({composite}/100)",
        (w * 2 + 16, 29),
        font,
        0.7,
        (80, 200, 255) if verdict == "PASS" else (80, 120, 255),
        2,
    )

    side_by_side_path = os.path.join(out_dir, "visual_verdict_side_by_side.png")
    cv2.imwrite(side_by_side_path, canvas)

    report = {
        "verdict": verdict,
        "composite_score": composite,
        "pass_threshold": 90.0,
        "dimensions": {
            "layout_spatial_occupancy_25pct": round(layout_score, 1),
            "typography_hud_hierarchy_15pct": round(typography_score, 1),
            "color_delta_e_fidelity_15pct": round(color_score, 1),
            "viewport_aspect_integrity_15pct": round(responsive_score, 1),
            "micro_states_and_polish_15pct": round(micro_polish_score, 1),
            "element_completeness_parity_15pct": round(completeness_score, 1),
        },
        "quadrant_breakdown": quad_reports,
        "actionable_fixes": actionable_fixes,
        "side_by_side_comparison_image": os.path.abspath(side_by_side_path),
    }

    report_path = os.path.join(out_dir, "visual_verdict_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"[visual_verdict_diff_loop] Verdict: {verdict} ({composite}/100) -> {side_by_side_path}")
    return report




def score_features_csv(csv_path: str):
    """Merged from imgdiff_parity.py: evaluates must/should/could feature completion parity."""
    import csv
    if not csv_path or not os.path.exists(csv_path):
        return {"feature_parity_score": 100.0, "shippable": True, "missing_must_haves": []}
    weights = {"must": 3.0, "should": 2.0, "could": 1.0}
    total_w, earned_w = 0.0, 0.0
    missing_must = []
    with open(csv_path, "r", encoding="utf-8") as fp:
        for row in csv.DictReader(fp):
            p = row.get("priority", "should").lower()
            st = row.get("status", "done").lower()
            w = weights.get(p, 1.0)
            total_w += w
            if st in ("done", "complete", "completed", "pass"):
                earned_w += w
            elif st == "partial":
                earned_w += w * 0.5
            elif p == "must":
                missing_must.append(row.get("id", "unknown"))
    pct = round((earned_w / max(1.0, total_w)) * 100.0, 1)
    return {"feature_parity_score": pct, "shippable": len(missing_must) == 0, "missing_must_haves": missing_must}


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 visual_verdict_diff_loop.py <reference.png> <built.png_or_html_or_url> <output_dir>")
        sys.exit(1)
    compute_visual_verdict(sys.argv[1], sys.argv[2], sys.argv[3])
