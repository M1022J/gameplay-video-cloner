#!/usr/bin/env python3
"""
Extract audio waveform RMS envelope and detect transient SFX impact timestamps (hits, jumps, explosions, BGM beats)
to synchronize visual VFX and Web Audio synthesizer cues (from bsisduck/video-analyzer-skill).

Usage:
  python3 extract_audio_sfx_peaks.py input.mp4 ./video_analysis/audio_peaks.json
"""
import argparse
import json
import subprocess
import wave
from pathlib import Path
import numpy as np


def extract_audio_peaks(video_path: str, output_json: str) -> None:
    out_path = Path(output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_wav = out_path.parent / "_tmp_audio_16k.wav"

    cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", str(tmp_wav)]
    subprocess.run(cmd, capture_output=True, check=False)

    if not tmp_wav.exists():
        out_path.write_text(json.dumps({"has_audio": False, "sfx_impact_peaks_sec": []}, indent=2), encoding="utf-8")
        return

    try:
        with wave.open(str(tmp_wav), "rb") as wf:
            n_frames = wf.getnframes()
            sr = wf.getframerate()
            raw = wf.readframes(n_frames)
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        hop = int(sr * 0.05)  # 50ms windows
        rms = [float(np.sqrt(np.mean(samples[i:i+hop] ** 2))) for i in range(0, len(samples) - hop, hop)]
        if not rms:
            raise ValueError("Empty audio track")
        threshold = float(np.mean(rms) + 1.35 * np.std(rms))
        peaks = []
        for idx in range(1, len(rms) - 1):
            if rms[idx] > threshold and rms[idx] >= rms[idx - 1] and rms[idx] >= rms[idx + 1]:
                ts = round(idx * 0.05, 2)
                if not peaks or ts - peaks[-1]["timestamp_sec"] >= 0.15:
                    peaks.append({"timestamp_sec": ts, "rms_intensity": round(rms[idx], 3), "tier": "large" if rms[idx] > threshold * 1.3 else "medium"})
        report = {"has_audio": True, "sample_rate": sr, "detected_sfx_impact_peaks": peaks[:24]}
    except Exception:
        report = {"has_audio": False, "detected_sfx_impact_peaks": []}
    finally:
        tmp_wav.unlink(missing_ok=True)

    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Audio SFX peak analysis saved to {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("output_json")
    args = parser.parse_args()
    extract_audio_peaks(args.video_path, args.output_json)


if __name__ == "__main__":
    main()
