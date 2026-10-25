#!/usr/bin/env python3
"""
Solve the 'single static image blindness' problem for AI agents analyzing gameplay videos
(integrating Schmandarine/web-motion-skill, alirezarezvani/senior-computer-vision, and LottieFiles/motion-design-skill).

For each top motion peak window in the video, this script generates:
1. `action_burst_strip_<N>.png`: Consecutive high-FPS (e.g. 30fps) frame strip showing exact startup -> active -> hit-stop -> recovery frames.
2. `onion_skin_trail_<N>.png`: A SINGLE composite image combining 8 consecutive frames with stroboscopic alpha ghosting (cyan -> gold -> magenta) AND OpenCV Farneback Dense Optical Flow velocity arrows (vx, vy) so an image-reading LLM can see continuous motion arcs and speed easing in 1 image!
3. `vfx_timing_report.json`: Quantifies transient action effects:
   - Screen shake amplitude (px) via global phase correlation
   - Hit-stop freeze frame count & duration (ms)
   - Hit-flash / explosion luminance spikes
   - Motion easing classification (linear, easeIn, easeOut, easeOutBack)

Usage:
  python3 extract_motion_trails_and_vfx.py input.mp4 ./video_analysis/motion_vfx --top-peaks 3 --fps 30
"""
import argparse
import json
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


def get_duration(video_path: str) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    try:
        return float(json.loads(res.stdout).get("format", {}).get("duration", 6.0))
    except Exception:
        return 6.0


def find_action_windows(video_path: str, duration: float, top_k: int = 3) -> list[float]:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    prev = None
    scores = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % max(1, int(fps // 10)) == 0:
            small = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (160, 160)).astype(np.float32)
            if prev is not None:
                diff = float(np.abs(small - prev).mean())
                scores.append((idx / fps, diff))
            prev = small
        idx += 1
    cap.release()

    if not scores:
        return [min(1.0, duration * 0.25), min(2.5, duration * 0.5), min(4.0, duration * 0.75)][:top_k]

    scores.sort(key=lambda x: x[1], reverse=True)
    chosen = []
    for ts, _ in scores:
        if all(abs(ts - c) > 0.8 for c in chosen):
            chosen.append(round(max(0.0, ts - 0.15), 2))
        if len(chosen) >= top_k:
            break
    return sorted(chosen)


def analyze_window_and_render(video_path: str, start_sec: float, fps: int, window_idx: int, out_dir: Path) -> dict:
    num_frames = 12
    dur = num_frames / float(fps)
    tmp_dir = out_dir / f"win_{window_idx:02d}_frames"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start_sec:.3f}",
        "-t", f"{dur:.3f}",
        "-i", video_path,
        "-vf", f"fps={fps},scale=480:-2",
        str(tmp_dir / "f_%02d.png")
    ]
    subprocess.run(cmd, capture_output=True, check=False)
    frame_files = sorted(tmp_dir.glob("f_*.png"))
    if len(frame_files) < 2:
        return {}

    bgr_frames = [cv2.imread(str(p)) for p in frame_files]
    gray_frames = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in bgr_frames]
    h, w = gray_frames[0].shape

    # 1. Build High-FPS Action Burst Strip (4x3 grid of consecutive frames)
    cols = 4
    rows = math.ceil(len(frame_files) / cols)
    strip_img = Image.new("RGB", (cols * w, rows * h), (15, 23, 42))
    draw_strip = ImageDraw.Draw(strip_img)

    frame_deltas = [0.0]
    luma_means = [float(gray_frames[0].mean())]
    shake_shifts = []

    for i in range(1, len(gray_frames)):
        diff = float(np.abs(gray_frames[i].astype(np.float32) - gray_frames[i - 1].astype(np.float32)).mean())
        frame_deltas.append(round(diff, 2))
        luma_means.append(round(float(gray_frames[i].mean()), 2))
        shift, _ = cv2.phaseCorrelate(np.float32(gray_frames[i - 1]), np.float32(gray_frames[i]))
        shake_shifts.append((round(float(shift[0]), 2), round(float(shift[1]), 2)))

    for i, fpath in enumerate(frame_files):
        r, c = i // cols, i % cols
        x0, y0 = c * w, r * h
        pil_f = Image.open(fpath).convert("RGB")
        strip_img.paste(pil_f, (x0, y0))
        ms = int((start_sec + i / float(fps)) * 1000)
        badge = f"f{i+1:02d} ({ms}ms) d={frame_deltas[i]:.1f}"
        draw_strip.rectangle([x0 + 6, y0 + 6, x0 + 215, y0 + 28], fill=(0, 0, 0))
        draw_strip.text((x0 + 10, y0 + 9), badge, fill=(56, 189, 248))

    burst_strip_path = out_dir / f"action_burst_strip_{window_idx:02d}.png"
    strip_img.save(burst_strip_path)

    # 2. Build Single-Image Stroboscopic Onion-Skin Motion Trail + Optical Flow Vector Map
    base_canvas = bgr_frames[0].astype(np.float32) * 0.35
    sample_indices = np.linspace(0, len(bgr_frames) - 1, min(8, len(bgr_frames)), dtype=int)
    tint_colors = [
        np.array([255, 200, 50], dtype=np.float32),   # BGR Cyan-ish startup
        np.array([240, 220, 80], dtype=np.float32),
        np.array([80, 220, 255], dtype=np.float32),   # Gold active
        np.array([50, 180, 255], dtype=np.float32),
        np.array([120, 100, 255], dtype=np.float32),  # Magenta impact/recovery
        np.array([180, 80, 255], dtype=np.float32),
        np.array([220, 100, 255], dtype=np.float32),
        np.array([255, 255, 255], dtype=np.float32),
    ]

    flow_vectors = []
    for rank, idx in enumerate(sample_indices):
        if idx == 0:
            continue
        prev_idx = sample_indices[rank - 1]
        diff_mask = np.abs(gray_frames[idx].astype(np.float32) - gray_frames[prev_idx].astype(np.float32))
        motion_mask = np.clip((diff_mask - 18.0) / 40.0, 0.0, 1.0)[:, :, None]
        weight = 0.22 + 0.55 * (rank / max(1, len(sample_indices) - 1))
        tinted = bgr_frames[idx].astype(np.float32) * 0.65 + tint_colors[min(rank, len(tint_colors) - 1)] * 0.35
        base_canvas = base_canvas * (1.0 - motion_mask * weight) + tinted * (motion_mask * weight)

        # Compute Farneback Dense Optical Flow between prev_idx and idx
        flow = cv2.calcOpticalFlowFarneback(gray_frames[prev_idx], gray_frames[idx], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        step = 32
        for y in range(step // 2, h, step):
            for x in range(step // 2, w, step):
                fx, fy = float(flow[y, x, 0]), float(flow[y, x, 1])
                mag = math.hypot(fx, fy)
                if mag > 3.5:
                    flow_vectors.append((x, y, int(x + fx * 2.2), int(y + fy * 2.2), round(mag, 2)))

    onion_bgr = np.clip(base_canvas, 0, 255).astype(np.uint8)
    for (x1, y1, x2, y2, _) in flow_vectors[:80]:
        cv2.arrowedLine(onion_bgr, (x1, y1), (x2, y2), (0, 230, 255), 2, tipLength=0.3)

    onion_pil = Image.fromarray(cv2.cvtColor(onion_bgr, cv2.COLOR_BGR2RGB))
    draw_onion = ImageDraw.Draw(onion_pil)
    draw_onion.rectangle([8, 8, 460, 34], fill=(0, 0, 0))
    draw_onion.text((14, 13), f"Onion-Skin Trail + Optical Flow | Window #{window_idx} ({start_sec:.2f}s)", fill=(250, 204, 21))
    onion_path = out_dir / f"onion_skin_trail_{window_idx:02d}.png"
    onion_pil.save(onion_path)

    # 3. Quantify Hit-Stop, Screen-Shake, Hit-Flash, and Easing Curve
    mean_delta = float(np.mean(frame_deltas[1:])) if len(frame_deltas) > 1 else 0.0
    hit_stop_frames = [i + 1 for i in range(1, len(frame_deltas) - 1) if frame_deltas[i] < max(1.8, mean_delta * 0.25) and frame_deltas[i - 1] > mean_delta * 0.8]
    base_luma = float(np.median(luma_means))
    hit_flash_frames = [i + 1 for i, lm in enumerate(luma_means) if lm - base_luma > 18.0]
    max_shake_px = round(max([math.hypot(dx, dy) for dx, dy in shake_shifts] or [0.0]), 2)

    first_half = np.mean(frame_deltas[1 : max(2, len(frame_deltas) // 2)])
    second_half = np.mean(frame_deltas[max(1, len(frame_deltas) // 2) :])
    if second_half > first_half * 1.25:
        easing_type = "easeInQuad / gravity-acceleration"
    elif first_half > second_half * 1.25:
        easing_type = "easeOutCubic / dash-deceleration"
    else:
        easing_type = "cubic-bezier(0.25, 0, 0.75, 1) / easeOutBack"

    return {
        "window_index": window_idx,
        "start_sec": start_sec,
        "fps_sampled": fps,
        "action_burst_strip_png": str(burst_strip_path),
        "onion_skin_trail_png": str(onion_path),
        "detected_hit_stop_frames": hit_stop_frames,
        "estimated_hit_stop_duration_ms": round(len(hit_stop_frames) * (1000.0 / fps), 1),
        "detected_hit_flash_frames": hit_flash_frames,
        "estimated_camera_shake_amplitude_px": max_shake_px,
        "fitted_motion_easing_curve": easing_type,
        "frame_by_frame_pixel_deltas": frame_deltas,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract 30/60fps action burst strips, onion-skin optical flow trails, and VFX timing JSON.")
    parser.add_argument("video_path", help="Input gameplay video file")
    parser.add_argument("output_dir", help="Output directory for strips, trails, and JSON")
    parser.add_argument("--top-peaks", type=int, default=3, help="Number of peak action windows to drill into")
    parser.add_argument("--fps", type=int, default=30, help="Sampling FPS for micro action strips (default: 30)")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dur = get_duration(args.video_path)
    windows = find_action_windows(args.video_path, dur, args.top_peaks)

    reports = []
    for idx, start_ts in enumerate(windows, start=1):
        rep = analyze_window_and_render(args.video_path, start_ts, args.fps, idx, out_dir)
        if rep:
            reports.append(rep)

    summary = {
        "video_path": args.video_path,
        "duration_sec": round(dur, 2),
        "micro_sampling_fps": args.fps,
        "analyzed_action_windows": reports
    }
    report_path = out_dir / "vfx_timing_report.json"
    report_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(reports)} high-FPS action burst strips, onion-skin optical flow trails, and {report_path}")


if __name__ == "__main__":
    main()
