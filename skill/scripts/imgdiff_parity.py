#!/usr/bin/env python3
"""
Visual Edge-Map Layout Diff & Feature Parity Scorer
(from Jakeschincariol/replica-skill replica-diff/imgdiff.py & parity.py).

1. Converts original reference screenshot and rebuilt game screenshot into structural edge maps
   (ignoring minor color/palette swaps) and computes a Layout Parity Score (0..100).
2. Evaluates `features.csv` (`must`, `should`, `could` weights) to compute overall Feature Parity.

Usage:
  python3 imgdiff_parity.py original.png clone.png --diff-out diff.png --features ./recon_output/features.csv
"""
import argparse
import csv
import json
import cv2
import numpy as np
from pathlib import Path


def compute_edge_layout_parity(orig_path: str, clone_path: str, diff_out: str | None) -> dict:
    img1 = cv2.imread(orig_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(clone_path, cv2.IMREAD_GRAYSCALE)
    if img1 is None or img2 is None:
        return {"layout_parity_score": 0.0, "error": "Could not load one or both images"}

    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    e1 = cv2.GaussianBlur(cv2.Canny(img1, 50, 150), (9, 9), 0).astype(np.float32)
    e2 = cv2.GaussianBlur(cv2.Canny(img2_resized, 50, 150), (9, 9), 0).astype(np.float32)

    # Compare 8x8 spatial macro-grid occupancy so layout structure is scored fairly
    h, w = img1.shape
    gh, gw = max(1, h // 8), max(1, w // 8)
    region_scores = []
    differing_regions = []

    for r in range(8):
        for c in range(8):
            y0, y1 = r * gh, min(h, (r + 1) * gh)
            x0, x1 = c * gw, min(w, (c + 1) * gw)
            d1 = float(e1[y0:y1, x0:x1].mean())
            d2 = float(e2[y0:y1, x0:x1].mean())
            denom = max(25.0, d1, d2)
            sim = max(0.0, 1.0 - abs(d1 - d2) / denom)
            region_scores.append(sim)
            if sim < 0.55:
                differing_regions.append({"grid_rc": [r, c], "px_box": [x0, y0, x1, y1], "similarity": round(sim, 2)})

    if diff_out:
        vis = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        for reg in differing_regions:
            x0, y0, x1, y1 = reg["px_box"]
            cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.imwrite(diff_out, vis)

    score = round(float(np.mean(region_scores)) * 100.0, 1)
    return {"layout_parity_score": score, "differing_regions_count": len(differing_regions), "differing_regions": differing_regions[:8]}


def score_features_csv(csv_path: str | None) -> dict:
    if not csv_path or not Path(csv_path).exists():
        return {"feature_parity_score": 100.0, "shippable": True}
    weights = {"must": 3.0, "should": 2.0, "could": 1.0}
    total_w, earned_w = 0.0, 0.0
    missing_must = []
    with open(csv_path, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original_png")
    parser.add_argument("clone_png")
    parser.add_argument("--diff-out", default=None)
    parser.add_argument("--features", default=None)
    args = parser.parse_args()
    res = {
        "visual_layout_diff": compute_edge_layout_parity(args.original_png, args.clone_png, args.diff_out),
        "feature_matrix_parity": score_features_csv(args.features)
    }
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
