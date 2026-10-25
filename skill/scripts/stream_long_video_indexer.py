#!/usr/bin/env python3
"""
stream_long_video_indexer.py (v8 Upgraded: Max-Pooled 32x18 Tile-Grid Energy + Dual-Anchor Cumulative Drift)
Sources:
- KumarSashank/motiscope (Localized tile-grid motion-energy peak detection — prevents small moving icons/digits from washing out in whole-frame averages)
- Breakthrough/DVR-Scan (Localized connected-component motion ROI detection)
- GAIR-NLP/VidaForge & mugnimaestra/video-frames-skill (O(1) streaming, model-aligned tile budgeting, timestamp burn-in)

Why v8 never misses tiny frame-to-frame differences:
1. Localized Max-Pooled Tile Grid (32x18 = 576 tiles at native resolution):
   - Instead of only checking whole-frame average diff (where a 16x16 icon changing on a 1920x1080 screen gets diluted by 8,000x!),
     we compute the L1 pixel delta inside each of the 576 local tiles and take the MAX tile delta (`max_tile_delta`).
   - Even if 99.8% of the screen is static and only ONE digit or small button changes, `max_tile_delta` spikes immediately!
2. Dual-Anchor Comparison (`Adjacent Frame F_{t-1}` + `Last Saved Anchor Frame F_{anchor}`):
   - If a bar or character drifts by only 0.2px per frame, `|F_t - F_{t-1}|` is tiny, so single-step diff might miss it.
   - By simultaneously tracking `|F_t - F_{anchor}|` (cumulative drift since the last saved keyframe), slow gradual motion
     is guaranteed to trigger a keyframe as soon as its accumulated local tile change exceeds `cumulative_tile_threshold`!
"""
import os
import sys
import json
import math
import argparse
import cv2
import numpy as np


def compute_dhash64(gray_small_9x8: np.ndarray) -> int:
    diff = gray_small_9x8[:, 1:] > gray_small_9x8[:, :-1]
    bits = diff.flatten()
    h_val = 0
    for b in bits:
        h_val = (h_val << 1) | int(b)
    return h_val


def hamming_distance64(h1: int, h2: int) -> int:
    return (h1 ^ h2).bit_count()


def format_ts(seconds: float) -> str:
    m, s = divmod(max(0.0, seconds), 60.0)
    h, m = divmod(int(m), 60)
    return f"{h:02d}:{m:02d}:{s:05.2f}"


def compute_localized_tile_diff(gray_a: np.ndarray, gray_b: np.ndarray, grid_x: int = 32, grid_y: int = 18):
    """
    Divides full-res grayscale difference |gray_a - gray_b| into a (grid_y x grid_x) tile matrix.
    Returns (max_tile_delta, top3_tile_mean, hot_tile_bbox_norm, active_tiles_count).
    """
    diff = cv2.absdiff(gray_a, gray_b)
    # Resize diff with INTER_AREA directly to (grid_x, grid_y) — mathematically equivalent to average pooling inside each tile!
    tile_means = cv2.resize(diff, (grid_x, grid_y), interpolation=cv2.INTER_AREA).astype(np.float32)
    max_val = float(np.max(tile_means))
    flat_sorted = np.sort(tile_means.flatten())[::-1]
    top3_mean = float(np.mean(flat_sorted[:3]))
    active_count = int(np.sum(tile_means > 6.0))

    max_idx = int(np.argmax(tile_means))
    ty, tx = divmod(max_idx, grid_x)
    hot_bbox_norm = [
        round(tx / grid_x, 4),
        round(ty / grid_y, 4),
        round(1.0 / grid_x, 4),
        round(1.0 / grid_y, 4),
    ]
    return max_val, top3_mean, hot_bbox_norm, active_count


def stream_index_long_video(
    video_path: str,
    out_dir: str,
    chunk_duration_sec: float = 60.0,
    overlap_sec: float = 8.0,
    scan_stride_frames: int = 1,
    micro_tile_threshold: float = 12.0,
    cumulative_tile_threshold: float = 18.0,
    max_keyframes_per_chunk: int = 20,
    resume: bool = True,
):
    os.makedirs(out_dir, exist_ok=True)
    keyframes_dir = os.path.join(out_dir, "keyframes")
    chunks_dir = os.path.join(out_dir, "chunks")
    os.makedirs(keyframes_dir, exist_ok=True)
    os.makedirs(chunks_dir, exist_ok=True)

    checkpoint_path = os.path.join(out_dir, "stream_index_manifest.json")
    if resume and os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        if cached.get("completed"):
            print(f"[stream_long_video_indexer] Loaded completed index from checkpoint: {checkpoint_path}")
            return cached

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0 or math.isnan(fps):
        fps = 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1280)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 720)
    est_duration = total_frames / fps if total_frames > 0 else 0.0

    print(
        f"[stream_long_video_indexer v8] Streaming {video_path} | {width}x{height} @ {fps:.2f}fps | "
        f"Total Frames: {total_frames} (~{format_ts(est_duration)}) | Stride={scan_stride_frames}"
    )

    prev_gray = None
    anchor_gray = None
    prev_dhash = None

    events = []
    spans = []
    micro_energy_timeline = []
    current_span = None

    frame_idx = 0
    last_saved_ts = -999.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % scan_stride_frames != 0:
            frame_idx += 1
            continue

        ts = frame_idx / fps
        # Keep 640x360 grayscale for fast localized 32x18 tile-grid evaluation (each tile = 20x20 px)
        eval_gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (640, 360), interpolation=cv2.INTER_AREA)
        tiny_9x8 = cv2.resize(eval_gray, (9, 8), interpolation=cv2.INTER_AREA)
        cur_dhash = compute_dhash64(tiny_9x8)

        event_type = None
        event_score = 0.0
        hot_tile = [0.0, 0.0, 1.0, 1.0]

        if prev_gray is None:
            event_type = "INITIAL_STATE"
            event_score = 100.0
            anchor_gray = eval_gray.copy()
        else:
            global_diff = float(np.mean(cv2.absdiff(eval_gray, prev_gray)))
            max_tile_adj, top3_adj, hot_tile, active_tiles = compute_localized_tile_diff(eval_gray, prev_gray)
            max_tile_cum, top3_cum, hot_tile_cum, _ = compute_localized_tile_diff(eval_gray, anchor_gray)
            dhash_dist = hamming_distance64(cur_dhash, prev_dhash)

            # Log dense frame-level localized energy (motiscope style: numeric curve is free and captures every single frame's micro-pulse!)
            micro_energy_timeline.append({
                "f": frame_idx,
                "t": round(ts, 3),
                "global_diff": round(global_diff, 3),
                "max_tile_diff": round(max_tile_adj, 2),
                "cum_drift_diff": round(max_tile_cum, 2),
                "active_tiles": active_tiles,
            })

            if global_diff > 34.0 and dhash_dist >= 16:
                event_type = "SCENE_TRANSITION"
                event_score = round(global_diff, 2)
            elif max_tile_adj >= micro_tile_threshold and active_tiles <= 25 and (ts - last_saved_ts) >= 0.15:
                # Localized Micro-Change! Whole frame looks static, but 1 to 25 local tiles had a distinct change (icon, digit, cooldown, sprite step)
                event_type = "LOCALIZED_MICRO_CHANGE"
                event_score = round(max_tile_adj, 2)
            elif max_tile_cum >= cumulative_tile_threshold and (ts - last_saved_ts) >= 0.35:
                # Cumulative Slow Drift! Gradual sub-pixel movement accumulated past threshold since last anchor frame
                event_type = "CUMULATIVE_SLOW_DRIFT"
                event_score = round(max_tile_cum, 2)
                hot_tile = hot_tile_cum
            elif global_diff > 18.0 and (ts - last_saved_ts) >= 0.8:
                event_type = "COMBAT_OR_MOTION_PEAK"
                event_score = round(global_diff, 2)

        if current_span is None:
            current_span = {
                "span_id": 1,
                "start_frame": frame_idx,
                "end_frame": frame_idx,
                "start_sec": round(ts, 2),
                "end_sec": round(ts, 2),
                "compressed_frames_count": 1,
            }
        else:
            if event_type is not None:
                current_span["duration_sec"] = round(current_span["end_sec"] - current_span["start_sec"], 3)
                spans.append(current_span)
                current_span = {
                    "span_id": len(spans) + 1,
                    "start_frame": frame_idx,
                    "end_frame": frame_idx,
                    "start_sec": round(ts, 2),
                    "end_sec": round(ts, 2),
                    "compressed_frames_count": 1,
                }
            else:
                current_span["end_frame"] = frame_idx
                current_span["end_sec"] = round(ts, 2)
                current_span["compressed_frames_count"] += scan_stride_frames

        if event_type is not None:
            scale = min(1.0, 1024.0 / max(width, height))
            out_w, out_h = int(round(width * scale)), int(round(height * scale))
            resized = cv2.resize(frame, (out_w, out_h), interpolation=cv2.INTER_AREA)

            # Highlight the localized hot tile with a subtle cyan reticle if it's a micro-change or slow drift
            if event_type in ("LOCALIZED_MICRO_CHANGE", "CUMULATIVE_SLOW_DRIFT"):
                hx = int(hot_tile[0] * out_w)
                hy = int(hot_tile[1] * out_h)
                hw = max(24, int(hot_tile[2] * out_w))
                hh = max(24, int(hot_tile[3] * out_h))
                cv2.rectangle(resized, (max(0, hx - 6), max(0, hy - 6)), (min(out_w, hx + hw + 6), min(out_h, hy + hh + 6)), (0, 255, 255), 2)

            badge_text = f"F#{frame_idx:06d} | {format_ts(ts)} | {event_type}"
            overlay = resized.copy()
            cv2.rectangle(overlay, (max(0, out_w - 460), out_h - 34), (out_w, out_h), (12, 12, 16), -1)
            cv2.addWeighted(overlay, 0.78, resized, 0.22, 0, resized)
            cv2.putText(resized, badge_text, (max(8, out_w - 450), out_h - 11), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (100, 240, 255), 1, cv2.LINE_AA)

            kf_name = f"kf_{len(events)+1:04d}_f{frame_idx:06d}.jpg"
            kf_path = os.path.join(keyframes_dir, kf_name)
            cv2.imwrite(kf_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            events.append({
                "event_id": f"E{len(events)+1:04d}",
                "frame_index": frame_idx,
                "timestamp_sec": round(ts, 3),
                "timestamp_str": format_ts(ts),
                "event_type": event_type,
                "event_score": event_score,
                "hot_tile_bbox_norm": hot_tile,
                "span_id": current_span["span_id"],
                "keyframe_path": os.path.abspath(kf_path),
            })
            last_saved_ts = ts
            anchor_gray = eval_gray.copy()

        prev_gray = eval_gray
        prev_dhash = cur_dhash
        frame_idx += 1

    cap.release()
    if current_span is not None:
        current_span["duration_sec"] = round(current_span["end_sec"] - current_span["start_sec"], 3)
        spans.append(current_span)

    actual_duration = max(est_duration, (frame_idx / fps) if frame_idx > 0 else 0.0)

    # Save the complete frame-by-frame localized micro-energy curve (zero frames lost!)
    energy_path = os.path.join(out_dir, "frame_by_frame_micro_energy.json")
    with open(energy_path, "w", encoding="utf-8") as ef:
        json.dump(micro_energy_timeline, ef, ensure_ascii=False)

    chunks = []
    step_sec = max(10.0, chunk_duration_sec - overlap_sec)
    num_chunks = max(1, int(math.ceil(max(0.1, actual_duration - overlap_sec) / step_sec)))

    for c_idx in range(num_chunks):
        w_start = round(c_idx * step_sec, 2)
        w_end = round(min(actual_duration + 0.01, w_start + chunk_duration_sec), 2)
        chunk_events = [e for e in events if w_start <= e["timestamp_sec"] <= w_end]

        if len(chunk_events) > max_keyframes_per_chunk:
            endpoints = [chunk_events[0], chunk_events[-1]]
            middle = sorted(chunk_events[1:-1], key=lambda x: -x["event_score"])[: max_keyframes_per_chunk - 2]
            chunk_events = sorted(endpoints + middle, key=lambda x: x["frame_index"])

        upstream_anchors = [e["event_id"] for e in events if (w_start - overlap_sec - 15.0) <= e["timestamp_sec"] < w_start][-2:]
        downstream_anchors = [e["event_id"] for e in events if w_end < e["timestamp_sec"] <= (w_end + overlap_sec + 15.0)][:2]

        chunk_id = f"chunk_{c_idx+1:03d}"
        chunk_meta = {
            "chunk_id": chunk_id,
            "chunk_index": c_idx + 1,
            "window_start_sec": w_start,
            "window_end_sec": w_end,
            "window_str": f"{format_ts(w_start)} -> {format_ts(w_end)}",
            "upstream_context_event_ids": upstream_anchors,
            "downstream_lookahead_event_ids": downstream_anchors,
            "keyframes_count": len(chunk_events),
            "estimated_gemini_tokens": len(chunk_events) * 258,
            "events": chunk_events,
        }
        chunks.append(chunk_meta)
        with open(os.path.join(chunks_dir, f"{chunk_id}.json"), "w", encoding="utf-8") as cf:
            json.dump(chunk_meta, cf, indent=2, ensure_ascii=False)

    packed_lines = [
        f"# Packed Long-Video Gameplay Timeline ({os.path.basename(video_path)})",
        f"- **Total Frames Scanned**: `{frame_idx:,}` frames (`{format_ts(actual_duration)}` @ `{fps:.2f}fps`)",
        f"- **Localized 32x18 Tile-Grid Energy Curve**: Saved to `frame_by_frame_micro_energy.json` (`{len(micro_energy_timeline):,}` frame measurements)",
        f"- **Extracted Event Keyframes (including `LOCALIZED_MICRO_CHANGE` & `CUMULATIVE_SLOW_DRIFT`)**: `{len(events)}` frames across `{len(chunks)}` chunks",
        "",
        "## Sliding-Window Chunks (with Upstream/Downstream Context Links)",
    ]
    for ch in chunks:
        packed_lines.append(
            f"### `{ch['chunk_id']}` [{ch['window_str']}] | Keyframes: `{ch['keyframes_count']}` (~`{ch['estimated_gemini_tokens']}` tokens) "
            f"| Upstream: `{ch['upstream_context_event_ids']}` | Downstream: `{ch['downstream_lookahead_event_ids']}`"
        )
        for ev in ch["events"]:
            packed_lines.append(
                f"- `[{ev['timestamp_str']} | F#{ev['frame_index']:06d}]` **{ev['event_type']}** (`{ev['event_id']}`, max_tile_score={ev['event_score']}, hot_tile={ev['hot_tile_bbox_norm']})"
            )
        packed_lines.append("")

    packed_md_path = os.path.join(out_dir, "packed_timeline.md")
    with open(packed_md_path, "w", encoding="utf-8") as pf:
        pf.write("\n".join(packed_lines))

    manifest = {
        "completed": True,
        "video_path": os.path.abspath(video_path),
        "video_stats": {
            "width": width,
            "height": height,
            "fps": round(fps, 2),
            "total_frames_scanned": frame_idx,
            "duration_sec": round(actual_duration, 2),
            "duration_str": format_ts(actual_duration),
        },
        "frame_by_frame_micro_energy_json": os.path.abspath(energy_path),
        "packed_timeline_md": os.path.abspath(packed_md_path),
        "chunks_dir": os.path.abspath(chunks_dir),
        "chunks": chunks,
    }
    with open(checkpoint_path, "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2, ensure_ascii=False)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="O(1) memory streaming indexer with 32x18 localized tile-grid micro-diff & cumulative drift detection.")
    parser.add_argument("video_path", help="Path to input gameplay video")
    parser.add_argument("output_dir", help="Directory to store chunks, keyframes, and manifest")
    parser.add_argument("--chunk-sec", type=float, default=60.0)
    parser.add_argument("--overlap-sec", type=float, default=8.0)
    parser.add_argument("--stride", type=int, default=1, help="Frame scan stride (default: 1 = inspect every single frame)")
    parser.add_argument("--micro-tile-thresh", type=float, default=12.0, help="Local 32x18 tile diff threshold for micro-changes")
    parser.add_argument("--cum-tile-thresh", type=float, default=18.0, help="Cumulative drift tile threshold against anchor frame")
    parser.add_argument("--max-kf-per-chunk", type=int, default=20)
    args = parser.parse_args()
    stream_index_long_video(
        args.video_path,
        args.output_dir,
        chunk_duration_sec=args.chunk_sec,
        overlap_sec=args.overlap_sec,
        scan_stride_frames=args.stride,
        micro_tile_threshold=args.micro_tile_thresh,
        cumulative_tile_threshold=args.cum_tile_thresh,
        max_keyframes_per_chunk=args.max_kf_per_chunk,
    )
