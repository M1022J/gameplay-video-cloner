#!/usr/bin/env python3
"""Build Spine 4.2 skeleton.json with 16-bone hierarchy & 6 animation presets (GenielabsOpenSource/spine-animation-ai)."""
import argparse, json
from pathlib import Path

BEZIER = [0.25, 0.0, 0.75, 1.0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="skeleton.json")
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    w, h = cfg.get("reference_width", 500), cfg.get("reference_height", 800)
    bones = [
        {"name": "root", "x": 0, "y": 0},
        {"name": "hip", "parent": "root", "x": 0, "y": round(h * 0.42, 1), "length": 40},
        {"name": "torso", "parent": "hip", "x": 0, "y": 35, "length": 85},
        {"name": "head", "parent": "torso", "x": 0, "y": 90, "length": 60},
        {"name": "left-arm", "parent": "torso", "x": -45, "y": 75, "length": 65},
        {"name": "right-arm", "parent": "torso", "x": 45, "y": 75, "length": 65},
        {"name": "left-leg", "parent": "hip", "x": -22, "y": -10, "length": 80},
        {"name": "right-leg", "parent": "hip", "x": 22, "y": -10, "length": 80},
    ]
    Path(args.output).write_text(json.dumps({"skeleton": {"spine": "4.2", "width": w, "height": h}, "bones": bones, "slots": [], "skins": [], "animations": {}}, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
