---
name: gameplay-video-cloner
description: Reverse-engineer and 1:1 replicate playable games from gameplay videos (including 30-60+ min long videos AND subtle 0.01px frame-by-frame micro-diff videos) OR static screenshots. Deduplicated 31-file core suite (12 all-in-one scripts + 18 deep reference modules across 41 open-source repos): 32x18 tile micro-diff & 0.01px sub-pixel oscilloscope, O(1) streaming & VideoRAG bidirectional ledger, SAHI micro-detail zoom & 6D visual-verdict (>=90) QA, image-to-gameplay recon, optical-flow trails, 2D/3D skeletal IK, and 5-subagent swarm.
allowed-tools: default_api google youtube image_gen
---
# Gameplay Video & Screenshot Cloner (Deduplicated 31-File Core Suite — 12 Scripts + 18 Reference Playbooks)

Reverse-engineer and 1:1 replicate playable games from **gameplay videos of any length (from 5s clips to 60-minute / 100,000+ frame playthroughs and subtle frame-by-frame micro-animations) OR static screenshots**. All redundant/overlapping scripts and tiny stub files have been consolidated into **12 non-overlapping executable Python scripts** (`scripts/`) and **18 deep reference playbooks** (`references/`):

## 1. Consolidated 12 Core Executable Scripts (`scripts/`)

| Script File | Consolidated Capabilities (Zero Overlap) | Primary Open-Source Sources |
| :--- | :--- | :--- |
| `1. stream_long_video_indexer.py` | **O(1) Memory Video Streamer + `32x18` Localized Tile-Grid Micro-Diff + Dual-Anchor Cumulative Drift**: Scans 10k–500k+ frames at `--stride 1` without OOM; detects both single-tile micro-changes (`LOCALIZED_MICRO_CHANGE`) and slow gradual creeps (`CUMULATIVE_SLOW_DRIFT`); outputs `packed_timeline.md`, `frame_by_frame_micro_energy.json`, and overlapping sliding-window chunks. *(Replaces `analyze_gameplay_video.py`, `extract_video_frames.py`, `sheet_contact.py`)* | `KumarSashank/motiscope`, `GAIR-NLP/VidaForge`, `mugnimaestra/video-frames-skill`, `browser-use/video-use` |
| `2. extract_micro_frame_deltas.py` | **`3x` Zoomed Micro-Delta Patch Strip & `10x` Residual Amplifier**: Crops only the changing bounding box `[x,y,w,h]` (`diff >= 3/255`) across consecutive frames into `delta_patch_strip_3x_zoom.png` + `amplified_10x_residual_strip.png`. | `Breakthrough/DVR-Scan`, Eulerian Residual Amplification |
| `3. subpixel_motion_oscilloscope.py` | **`0.01px` Sub-Pixel Anti-Aliasing Centroid Tracker & Loop/Bezier Oscilloscope**: Recovers `0.01px` trajectories from edge alpha weights across every frame, measuring autocorrelation loop periods and velocity-integrated `cubic-bezier` curves. | `snapcndev/snapcn` (`motion-quality`), `KumarSashank/motiscope` |
| `4. bidirectional_context_ledger.py` | **Bidirectional Causal Graph ("上下结合判断") & Economy Curve Fitter**: Maintains `rolling_state_ledger.json` across chunks (Forward state accumulation + Backward causal hypothesis backfill) and fits Linear/Exponential progression formulas ($R^2$). | `HKUDS/VideoRAG`, `HKUDS/VideoAgent`, `MovieChat` |
| `5. extract_motion_trails_and_vfx.py` | **30/60fps Action Burst Strips + Stroboscopic Onion-Skin Trails + Optical Flow**: Bakes 8-frame cyan/gold/magenta motion ghosts + Farneback optical flow arrows into 1 image and measures hit-stop (ms), camera shake (px), and hit-flash. | `Schmandarine/web-motion-skill`, `senior-computer-vision`, `LottieFiles` |
| `6. extract_audio_sfx_peaks.py` | **Audio Waveform Envelope & Transient SFX Peak Detector**: Extracts 16kHz RMS peaks to synchronize Web Audio synth cues (`hit`, `jump`, `boom`, `levelup`) with visual impacts. | `bsisduck/video-analyzer-skill` |
| `7. infer_gameplay_from_image.py` | **Image-to-Gameplay Reverse-Engineering & `features.csv` Generator**: Deduces 3-zone spatial layout, entity shape distribution, core loops, and `must/should/could` feature matrix from static screenshots or keyframes. | `Jakeschincariol/replica-skill`, `Yakoub-ai/phaser4-gamedev` |
| `8. slice_micro_detail_crops.py` | **SAHI `2x2` Overlapping Quadrant + `1:1` Zone + `2x` Micro-Widget Zoom Cropper**: Slices native-pixel HUD/Arena/Control zones + Top-8 high-edge-density `2x` zoomed badges and extracts rare `0.05%–2.5%` accent hex colors. | `uxkin/ui-from-screenshot`, `Huc91/pixel-perfect-skill` |
| `9. process_and_audit_sprites.py` | **Unified Sprite Cropper, `#FF00FF` Chroma-Key Cleaner & RGBA Alpha Auditor**: Crops sprites, removes backgrounds, and enforces `corner_alpha_max <= 12` (`transparent_bg_ok`). *(Replaces `extract_sprites.py`, `chroma_key_magenta.py`, `audit_png_assets.py`, `provider_stub.py`)* | `yuzhworkhard-wq/image-to-code`, `ybuild-ai/ai-game-art-pipeline-skill` |
| `10. spine_and_swarm_pipeline.py` | **Unified 2D Spine Rig/Atlas Builder & 5-Subagent Swarm Orchestrator**: Routes engines, initializes 5-subagent context briefs & DAG boards, and builds Spine 4.2 `skeleton.json` + atlases. *(Replaces 8 fragmented Spine/Swarm micro-scripts)* | `spine-animation-ai`, `obra/superpowers`, `orchestrating-swarms` |
| `11. visual_verdict_diff_loop.py` | **Headless Browser Live Renderer + 3-Panel Delta-E Diff Heatmap + 6D Scorer (`>= 90` Gate)**: Renders the built game, generates `Original | Built | Heatmap`, checks quadrant element parity & `features.csv`. *(Replaces `imgdiff_parity.py`)* | `vibeeval/visual-verdict`, `garrytan/gstack`, `harness-visual-regression` |
| `12. validate_architecture.py` | **Runtime Architecture & QA Hook Validator**: Audits `Constants`, `dt` normalization, dual input listeners, `trauma^2` shake, Web Audio synth, and `window.render_game_to_text()`. | `Donchitos/Claude-Code-Game-Studios`, `PlayableIntelligence/game-creator` |

## 2. Consolidated 18 Reference Playbooks (`references/` — 5 Clean Domain Folders)

1. **`references/long-video-and-subpixel-diff/` (3 Playbooks — Merged Long-Video + Sub-Pixel Micro-Diff)**:
   - `01-o1-streaming-and-32x18-tile-micro-diff.md`
   - `02-subpixel-001px-oscilloscope-and-delta-strips.md`
   - `03-videorag-moviechat-bidirectional-causal-ledger.md`
2. **`references/micro-detail-and-visual-qa/` (4 Playbooks — SAHI Zoom + 24-Point Checklist + 6D Visual Verdict)**:
   - `01-sahi-highres-quadrant-and-roi-zoom.md`
   - `02-visual-verdict-6d-scoring-and-delta-e.md`
   - `03-gstack-uxkin-side-by-side-fix-loop.md`
   - `04-rastian-24-point-game-micro-detail-checklist.md`
3. **`references/image-to-gameplay-recon/` (4 Playbooks — Visual Semiotics + Clean-Room Recon + Layer Alpha Table + 13-Section GDD)**:
   - `01-visual-affordance-to-mechanics-matrix.md`
   - `02-jakeschincariol-replica-recon-and-diff.md`
   - `03-image-to-code-layer-table-and-alpha-audit.md`
   - `04-phaser4-13-section-gdd-and-playtest-loop.md`
4. **`references/video-motion-and-vfx-analysis/` (4 Playbooks — Macro-to-Micro Burst + Onion-Skin Optical Flow + Audio/Video Subagents + Easing Tables)**:
   - `01-schmandarine-web-motion-macro-micro-drilldown.md`
   - `02-opencv-optical-flow-and-onion-skin-trails.md`
   - `03-bsisduck-parallel-video-audio-subagents.md`
   - `04-lottiefiles-frankx-timing-easing-and-vfx-curves.md`
5. **`references/engines-skeletal-and-swarm/` (3 Playbooks — Consolidated 2D/3D Skeletal IK + 5-Subagent Swarm + 74 Gamedev/Studio Skills)**:
   - `01-2d-3d-skeletal-animation-and-ik.md`
   - `02-multi-agent-swarm-and-sdd-workflow.md`
   - `03-74-gamedev-skills-studio-hooks-and-art.md`

## 3. Unified 4-Stage Execution Workflow

```bash
# STAGE 1: Stream & Index Video (O(1) RAM, 32x18 local tile micro-diff, dual-anchor drift) + Bidirectional Ledger
python3 skills/gameplay-video-cloner/scripts/stream_long_video_indexer.py <video.mp4> ./video_index --stride 1 --micro-tile-thresh 12.0
python3 skills/gameplay-video-cloner/scripts/bidirectional_context_ledger.py init ./video_index/rolling_state_ledger.json --title "<Game>"

# STAGE 2: Drill into Subtle Micro-Diffs (3x Delta Patch + 0.01px Oscilloscope) & Action VFX (30fps Onion-Skin + Audio)
python3 skills/gameplay-video-cloner/scripts/extract_micro_frame_deltas.py <video.mp4> ./video_index/micro_deltas --start 0.0 --duration 2.0
python3 skills/gameplay-video-cloner/scripts/subpixel_motion_oscilloscope.py <video.mp4> ./video_index/subpixel.json --start 0.0 --duration 4.0
python3 skills/gameplay-video-cloner/scripts/extract_motion_trails_and_vfx.py <video.mp4> ./video_index/motion_vfx --top-peaks 3 --fps 30
python3 skills/gameplay-video-cloner/scripts/extract_audio_sfx_peaks.py <video.mp4> ./video_index/audio_peaks.json

# STAGE 3: Image-to-Gameplay Recon + SAHI 2x2 Quadrant & 2x Micro-Widget Slicing + Swarm Init
python3 skills/gameplay-video-cloner/scripts/infer_gameplay_from_image.py <keyframe_or_screenshot.png> ./recon_out
python3 skills/gameplay-video-cloner/scripts/slice_micro_detail_crops.py <keyframe_or_screenshot.png> ./micro_crops
python3 skills/gameplay-video-cloner/scripts/spine_and_swarm_pipeline.py init-swarm --project-dir ./swarm_ws --game-title "<Game>"

# STAGE 4: Sprite Alpha Audit + Architecture Validation + Closed-Loop 6D Visual Verdict (>= 90/100 Gate)
python3 skills/gameplay-video-cloner/scripts/process_and_audit_sprites.py audit ./assets
python3 skills/gameplay-video-cloner/scripts/validate_architecture.py <built_game.html>
python3 skills/gameplay-video-cloner/scripts/visual_verdict_diff_loop.py <keyframe_or_screenshot.png> <built_game.html> ./verdict_out
```
