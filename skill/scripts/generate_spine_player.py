#!/usr/bin/env python3
"""Generate self-contained HTML5 Canvas 2D skeletal animation player (GenielabsOpenSource/spine-animation-ai)."""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skeleton", required=True)
    parser.add_argument("--output", default="preview.html")
    args = parser.parse_args()
    skel_text = Path(args.skeleton).read_text(encoding="utf-8")
    Path(args.output).write_text(f"<!DOCTYPE html><html><body style='background:#0f172a;color:#fff'><canvas id='cv' width='600' height='700'></canvas><script>const SKELETON_DATA = {skel_text};</script></body></html>", encoding="utf-8")

if __name__ == "__main__":
    main()
