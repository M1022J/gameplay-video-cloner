#!/usr/bin/env python3
"""Extract and resize video frames for runtime texture sequences (ybuild-ai/ai-game-art-pipeline-skill)."""
import argparse, subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("output_dir")
    parser.add_argument("--fps", type=float, default=12.0)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float, default=5.0)
    parser.add_argument("--width", type=int, default=-1)
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    vf = [f"fps={args.fps}"] + ([f"scale={args.width}:-2:flags=lanczos"] if args.width > 0 else [])
    subprocess.run(["ffmpeg", "-y", "-ss", f"{args.start:.3f}", "-t", f"{args.duration:.3f}", "-i", args.video_path, "-vf", ",".join(vf), str(out_dir / "seq_%04d.png")], capture_output=True, check=True)

if __name__ == "__main__":
    main()
