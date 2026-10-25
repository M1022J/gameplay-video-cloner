# Adaptive Multi-Tier Video Sampling & Parallel Audio/Visual Subagents (`bsisduck/video-analyzer-skill`)

Distilled from `bsisduck/video-analyzer-skill`.

## 1. Adaptive Frame-Rate Tiering by Video Duration
- **Micro Action Clip (`< 10s` or peak window)**: Sample at `30fps` via `extract_motion_trails_and_vfx.py` to capture exact combat/VFX frame data.
- **Short Gameplay Recording (`10s - 60s`)**: Sample macro overview at `2fps - 4fps` (`16-24` frames) + `30fps` burst strips on top 3 motion peaks.
- **Long Walkthrough (`1 - 3 min`)**: Sample macro overview at `1fps` + scene-change high-res frames + `30fps` burst strips on boss/upgrade moments.
- **Portrait-Aware Montage Grids**: Use `4x4` grid for `16:9` landscape videos and `4x3` / `3x5` high-aspect tiles for `9:16` mobile mini-games so vertical HUD details are never crushed.

## 2. Parallel Video Analysis Subagent Dispatch
When analyzing a complex gameplay video, fan out four analysis tasks simultaneously:
1. **Macro Grid Agent**: Reads `contact_sheet.png` to map the Finite State Machine (`Title -> Core Loop -> Upgrade Modal -> Boss -> GameOver`) and static HUD layout.
2. **Micro Burst & Onion-Skin Agent**: Reads `action_burst_strip_01.png` and `onion_skin_trail_01.png` to extract player jump/attack frame timings, trajectory arcs, and easing curves.
3. **VFX & Juice Telemetry Agent**: Reads `vfx_timing_report.json` to extract screen-shake pixels, hit-stop duration, hit-flash frames, and particle counts.
4. **Audio Envelope Agent**: Reads `audio_peaks.json` (from `extract_audio_sfx_peaks.py`) to map Web Audio synthesizer SFX triggers (`tick`, `hit`, `boom`, `levelup`) to exact gameplay events.
