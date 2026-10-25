#!/usr/bin/env python3
"""Analyze a gameplay video using ffprobe/ffmpeg and PIL/numpy (video-db/skills & ybuild-ai)."""
import argparse, json, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

def get_video_metadata(video_path: str) -> dict:
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
           "-show_entries", "stream=width,height,r_frame_rate,duration,nb_frames",
           "-show_entries", "format=duration", "-of", "json", video_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    stream = data.get("streams", [{}])[0]
    fmt = data.get("format", {})
    width, height = int(stream.get("width", 1280)), int(stream.get("height", 720))
    fps_str = stream.get("r_frame_rate", "30/1")
    fps = round(float(fps_str.split("/")[0]) / max(1.0, float(fps_str.split("/")[1])), 2) if "/" in fps_str else round(float(fps_str), 2)
    duration = float(stream.get("duration") or fmt.get("duration") or 10.0)
    gcd_val = math.gcd(width, height)
    return {
        "width": width, "height": height, "fps": fps, "duration_sec": round(duration, 2),
        "aspect_ratio": f"{width // gcd_val}:{height // gcd_val}",
        "orientation": "portrait (mobile/mini-game)" if height > width else ("square" if height == width else "landscape (desktop/console)")
    }

def extract_frames(video_path: str, out_dir: Path, num_frames: int, duration: float) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    interval = max(0.2, duration / max(1, num_frames))
    extracted = []
    for i in range(num_frames):
        ts = min(max(0.0, i * interval), max(0.0, duration - 0.05))
        fname = f"frame_{i+1:02d}.png"
        fpath = out_dir / fname
        subprocess.run(["ffmpeg", "-y", "-ss", f"{ts:.3f}", "-i", video_path, "-frames:v", "1", "-q:v", "2", str(fpath)], capture_output=True, check=False)
        if fpath.exists():
            extracted.append({"index": i + 1, "timestamp_sec": round(ts, 2), "file": fname, "path": str(fpath)})
    return extracted

def extract_dominant_palette(img_path: str, num_colors: int = 6) -> list[str]:
    img = Image.open(img_path).convert("RGB").resize((120, 120))
    q = img.quantize(colors=num_colors)
    pal = q.getpalette()[: num_colors * 3]
    return [f"#{pal[i]:02x}{pal[i+1]:02x}{pal[i+2]:02x}" for i in range(0, len(pal), 3)]

def compute_motion_and_hud_zones(frames: list[dict], out_dir: Path) -> dict:
    if len(frames) < 2:
        return {"motion_peaks": [], "scene_transitions": [], "detected_static_hud_zones": []}
    arrays = [np.asarray(Image.open(f["path"]).convert("RGB").resize((320, 320)), dtype=np.float32) for f in frames]
    stack = np.stack(arrays, axis=0)
    temporal_std = np.std(stack, axis=0).mean(axis=-1)
    norm_std = (temporal_std / max(1.0, float(temporal_std.max())) * 255.0).astype(np.uint8)
    Image.fromarray(norm_std).save(out_dir / "hud_variance_map.png")
    motion_deltas, scene_transitions = [], []
    for i in range(1, len(arrays)):
        diff = float(np.abs(arrays[i] - arrays[i - 1]).mean())
        entry = {"from_frame": frames[i - 1]["index"], "to_frame": frames[i]["index"], "timestamp_sec": frames[i]["timestamp_sec"], "mean_pixel_delta": round(diff, 2)}
        motion_deltas.append(entry)
        if diff > 42.0:
            scene_transitions.append(entry)
    top_var, mid_var, bot_var = float(temporal_std[:48, :].mean()), float(temporal_std[96:224, :].mean()), float(temporal_std[272:, :].mean())
    hud_zones = []
    if top_var < mid_var * 0.65: hud_zones.append("top_bar_hud")
    if bot_var < mid_var * 0.65: hud_zones.append("bottom_deck_hud")
    return {
        "dominant_color_palette_hex": extract_dominant_palette(frames[len(frames) // 2]["path"]),
        "top_band_variance": round(top_var, 2), "center_playfield_variance": round(mid_var, 2), "bottom_band_variance": round(bot_var, 2),
        "detected_static_hud_zones": hud_zones, "scene_transitions": scene_transitions,
        "motion_peaks": sorted(motion_deltas, key=lambda x: x["mean_pixel_delta"], reverse=True)[:4]
    }

def build_contact_sheet(frames: list[dict], out_path: Path, cols: int = 4) -> None:
    if not frames: return
    w, h = Image.open(frames[0]["path"]).size
    tw, th = 360, max(180, int(h * (360 / max(1, w))))
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * th), (18, 20, 28))
    draw = ImageDraw.Draw(sheet)
    for idx, f in enumerate(frames):
        x0, y0 = (idx % cols) * tw, (idx // cols) * th
        sheet.paste(Image.open(f["path"]).convert("RGB").resize((tw - 8, th - 8)), (x0 + 4, y0 + 4))
        draw.rectangle([x0 + 8, y0 + 8, x0 + 145, y0 + 32], fill=(0, 0, 0))
        draw.text((x0 + 14, y0 + 12), f"#{f['index']:02d} | {f['timestamp_sec']:.2f}s", fill=(255, 230, 80))
    sheet.save(out_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("output_dir")
    parser.add_argument("--frames", type=int, default=16)
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    meta = get_video_metadata(args.video_path)
    frames = extract_frames(args.video_path, out_dir, args.frames, meta["duration_sec"])
    motion_info = compute_motion_and_hud_zones(frames, out_dir)
    build_contact_sheet(frames, out_dir / "contact_sheet.png")
    report = {"video_metadata": meta, "sampled_frames_count": len(frames), "contact_sheet": str(out_dir / "contact_sheet.png"), "hud_variance_map": str(out_dir / "hud_variance_map.png"), "motion_and_hud_analysis": motion_info, "frames": frames}
    (out_dir / "telemetry.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
