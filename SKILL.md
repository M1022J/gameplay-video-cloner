---
name: gameplay-video-cloner
description: Reverse-engineer and 1:1 replicate playable games directly from gameplay videos (看游戏视频直接复刻游戏及动作特效), screen recordings, GIFs, or video URLs using a Lead-Agent + Parallel-Subagents Swarm workflow. Bundles 19 open-source repositories (46 files): continuous video motion & VFX analysis suites (Schmandarine/web-motion-skill 60fps burst drill-down, alirezarezvani/senior-computer-vision OpenCV optical flow & stroboscopic onion-skin trails, bsisduck/video-analyzer-skill parallel video/audio subagents, LottieFiles/motion-design-skill & frankxai/awesome-motion-design-agent-skills easing/choreography), multi-agent orchestration suites (obra/superpowers, kieranklaassen/orchestrating-swarms, sickn33/subagent-orchestrator, qodex-ai, VoltAgent), 2D/3D skeletal animation suites (GenielabsOpenSource/spine-animation-ai, BowTiedSwan/rive-skills, blender-rigging-animation, arjun988/blender-skills), and game pipelines (ybuild-ai, video-db, PlayableIntelligence/game-creator, awesome-gamedev-agent-skills, Claude-Code-Game-Studios). Use whenever the user shares a gameplay video or asks to clone a game with accurate motion, physics, VFX, and animations.
allowed-tools: default_api google youtube image_gen
---
# Gameplay Video Cloner (19-Repository Video Motion, Multi-Agent Swarm, 2D/3D Skeletal & Game Suite)

Reverse-engineer gameplay videos, screen recordings, GIFs, or video URLs into playable 1:1 game replicas without losing continuous motion trajectories, action frame timings, easing curves, or transient VFX effects. This skill packages **17 executable Python scripts** and **28 reference playbooks** (46 files total) across 19 open-source repositories.

## How This Skill Solves the "Single Static Image Blindness" Problem

Standard image-only skills fail on gameplay videos because a single screenshot cannot show movement arcs, speed easing, hit-stop freeze frames, screen shake, or particle burst timing. This skill solves that with a **4-Layer Video-to-Motion-Vision Pipeline**:

1. **Stroboscopic Onion-Skin Motion Trail Images (`extract_motion_trails_and_vfx.py` — `senior-computer-vision`)**:
   - Bakes 8 consecutive high-FPS frames of each action window into **one single composite image** (`onion_skin_trail_01.png`) with decaying alpha ghosts (cyan = startup anticipation, gold = active trajectory arc, magenta = recovery) and **OpenCV Farneback Dense Optical Flow velocity arrows `(vx, vy)`**. Even when viewing a single image, the agent directly sees the exact jump parabola, sword swing arc, acceleration/deceleration spacing, and knockback vector.
2. **Macro-to-Micro 30/60fps Action Window Drill-Down (`Schmandarine/web-motion-skill` + `bsisduck/video-analyzer-skill`)**:
   - First builds a 16-tile macro `contact_sheet.png` across the whole video to spot action timestamps, then automatically zooms into the top motion peaks and extracts **consecutive 30fps/60fps burst strips** (`action_burst_strip_01.png`) labeled with millisecond deltas so startup, active, hit-stop, and recovery frame counts are visible frame-by-frame.
3. **Automated Micro-VFX & Easing Telemetry (`vfx_timing_report.json` — `LottieFiles/motion-design-skill` + `frankxai`)**:
   - Quantifies invisible-in-stills effects directly into JSON:
     - **Camera Screen Shake**: Global background phase-correlation translation `(dx, dy)` in pixels and decay duration.
     - **Hit-Stop Freeze Frames**: Sudden 1-to-5 frame velocity drops (`mean_delta < 1.5`) inside a high-motion combat window (`40ms-90ms`).
     - **Hit-Flash & Burst VFX**: 1-to-3 frame localized luminance spikes (`+45` brightness jump) on impact.
     - **Fitted Easing Curve**: Computes displacement ratios across consecutive frames to classify motion as `linear`, `easeInQuad` (gravity fall), `easeOutCubic` (dash deceleration), or `easeOutBack` (overshoot pop).
4. **Audio Waveform SFX & Beat Correlation (`extract_audio_sfx_peaks.py` — `bsisduck/video-analyzer-skill`)**:
   - Extracts audio RMS transient spikes (impacts, jumps, gunshots, merge pops) and correlates them with visual frame numbers.

## 1. Bundled Open-Source Skill Repositories (19 Repositories)

### Part A: Video Motion, Optical Flow, VFX & Easing Analysis (5 Repositories - NEW)
1. **Schmandarine/web-motion-skill**: Macro 24-tile overview contact sheet -> Micro 25-60fps consecutive action burst strip drill-down + Disney 12 Principles of Web/Game Motion (`references/video-motion-and-vfx-analysis/01-schmandarine-web-motion-macro-micro-drilldown.md`).
2. **alirezarezvani/claude-skills (`senior-computer-vision`)**: OpenCV Farneback dense optical flow, stroboscopic onion-skin trail synthesis, and motion vector arrows (`scripts/extract_motion_trails_and_vfx.py` + `02-opencv-optical-flow-and-onion-skin-trails.md`).
3. **bsisduck/video-analyzer-skill**: Adaptive FPS tiering, scene-cut detection, audio transient peak extraction (`scripts/extract_audio_sfx_peaks.py`), and parallel visual/motion/audio subagents (`03-bsisduck-parallel-video-audio-subagents.md`).
4. **LottieFiles/motion-design-skill & frankxai/awesome-motion-design-agent-skills**: Timing and easing lookup tables (`timing-easing-tables`), displacement-to-Bezier curve fitting, multi-element stagger choreography, and `web-motion-auditor` QA rubric (`04-lottiefiles-frankx-timing-easing-and-vfx-curves.md`).

### Part B: Multi-Agent Division-of-Labor & Swarm Orchestration (5 Repositories)
5. **obra/superpowers (`dispatching-parallel-agents` & `subagent-driven-development`)**: `scripts/orchestrate_subagents.py` + `references/multi-agent-orchestration/01-obra-superpowers-parallel-and-sdd.md`.
6. **kieranklaassen/orchestrating-swarms**: `scripts/swarm_task_board.py` + `02-swarm-teammate-and-dag-taskboard.md`.
7. **sickn33/antigravity-awesome-skills (`subagent-orchestrator`)**: `scripts/merge_subagent_modules.py` + `03-antigravity-subagent-orchestrator-6-phases.md`.
8. **qodex-ai/ai-agent-skills & VoltAgent/awesome-claude-code-subagents**: `04-qodex-voltagent-topologies-and-roles.md`.

### Part C: 2D & 3D Skeletal Animation Suites (4 Repositories)
9. **GenielabsOpenSource/spine-animation-ai**: `scripts/position_parts.py`, `scripts/build_spine_json.py`, `scripts/make_atlas.py`, `scripts/generate_spine_player.py` + `references/skeletal-animation-2d-3d/01-spine-2d-skeletal-animation-ai.md`.
10. **BowTiedSwan/rive-skills**: `02-rive-2d-bones-ik-state-machines.md`.
11. **composio-community/opencode-skills (`blender-rigging-animation`) & arjun988/blender-skills**: `03-blender-3d-rigging-and-animation.md` + `04-runtime-3d-skinnedmesh-ik-threejs-unity-godot.md`.

### Part D: Game Art Pipeline, VideoDB & Cross-Engine Game Studios (5 Repositories)
12. **ybuild-ai/ai-game-art-pipeline-skill**: `extract_video_frames.py`, `sheet_contact.py`, `chroma_key_magenta.py`, `provider_stub.py`, `extract_sprites.py` + 5 art guides under `references/ybuild-art-pipeline/`.
13. **video-db/skills**: `scripts/analyze_gameplay_video.py` + `references/videodb-workflows/video-scene-ocr-audio-indexing.md`.
14. **PlayableIntelligence/game-creator**: `scripts/validate_architecture.py` + `references/playable-game-creator/11-skills-and-11-commands.md`.
15. **gamedev-skills/awesome-gamedev-agent-skills**: `scripts/detect_engine_router.py` + 6 modules under `references/awesome-gamedev-74-skills/` (all 74 skills).
16. **Donchitos/Claude-Code-Game-Studios**: 3 modules under `references/claude-code-game-studios/` (49 agents + 74 skills + 15 hooks + 14 rules).

## Steps

### 1. Round 1 (Foundation): Macro Telemetry + Micro High-FPS Burst Strips + Onion-Skin Optical Flow

Run the video motion & VFX analysis suite via `execute_bash` before writing any code:

```bash
# 1) Macro timeline analysis: 16 keyframes, contact sheet, HUD variance map, scene cuts & hex palette
python3 skills/gameplay-video-cloner/scripts/analyze_gameplay_video.py <video_path> ./video_analysis --frames 16

# 2) Micro 30fps Action Burst Strips + Stroboscopic Onion-Skin Motion Trails + Optical Flow + VFX Telemetry
python3 skills/gameplay-video-cloner/scripts/extract_motion_trails_and_vfx.py <video_path> ./video_analysis/motion_vfx --top-peaks 3 --fps 30

# 3) Audio waveform transient SFX & impact beat synchronization
python3 skills/gameplay-video-cloner/scripts/extract_audio_sfx_peaks.py <video_path> ./video_analysis/audio_peaks.json

# 4) Route engine, 2D/3D skeletal suite & initialize 5-Subagent Swarm Board
python3 skills/gameplay-video-cloner/scripts/detect_engine_router.py --workspace . --prompt "<user_request_summary>"
python3 skills/gameplay-video-cloner/scripts/orchestrate_subagents.py --project-dir ./subagent_workspace --game-title "<game_title>"
python3 skills/gameplay-video-cloner/scripts/swarm_task_board.py --board ./subagent_workspace/swarm_board.json init
```

- **Inspect Both Macro and Motion-Trail Visuals**: Call `view_file` in parallel on:
  - `./video_analysis/contact_sheet.png` (overall state flow & UI layout)
  - `./video_analysis/motion_vfx/action_burst_strip_01.png` (frame-by-frame 30fps action sequence)
  - `./video_analysis/motion_vfx/onion_skin_trail_01.png` (single-image stroboscopic motion trajectory + optical flow arrows)
  - `./video_analysis/motion_vfx/vfx_timing_report.json` (quantified screen shake, hit-stop frames, hit-flash spikes, and fitted easing curves)

### 2. Round 2 (Parallel Specialist Fan-Out): Execute Isolated Domain Subagents

- **`subagent-02-physics-controller` (`PhysicsSystem` + `PlayerController` + `WaveDirector`)**:
  - Implement exact velocity, gravity, and fitted easing curves from `vfx_timing_report.json` with delta-time normalization (`dt`).
- **`subagent-03-skeletal-art` (`SkeletalRig` + `solveTwoBoneIK` + `Juice` + `ParticleSystem`)**:
  - Replicate the exact startup/active/recovery frame counts and motion arcs visible in `action_burst_strip_01.png` and `onion_skin_trail_01.png` using 2D Spine/Rive bones (`solveTwoBoneIK`) or 3D articulated joints (`createProcedural3DRig`).
  - Configure `Juice.feedback()` with the exact `hit_stop_ms`, `camera_shake_px`, `hit_flash_ms`, and particle burst vectors measured in `vfx_timing_report.json`.
- **`subagent-04-hud-audio` (`HUDRenderer` + `AudioSynth` + `TuningDrawer`)**:
  - Build HUD elements inside the static HUD zones, wire Web Audio synth SFX to match `audio_peaks.json`, and include the `⚙️ 参数微调` live tuning drawer.

### 3. Round 3 (Fan-In Review & Assembly): 3-Point Spot Check, QA Gate & Canvas Delivery

```bash
python3 skills/gameplay-video-cloner/scripts/merge_subagent_modules.py /working_dir/<conversation_id>/artifacts/file_generation/ttl=63d/output/<game_name>.html
python3 skills/gameplay-video-cloner/scripts/validate_architecture.py /working_dir/<conversation_id>/artifacts/file_generation/ttl=63d/output/<game_name>.html
```

- Call `google:show_file` on the verified game file and present the **Motion & VFX Telemetry Table**, **Multi-Agent Division-of-Labor Table**, and **Video-to-Game Replication Matrix**.

## Gotchas

- **Relying Only on 1fps Sparse Keyframes**: Fast attacks (`0.25s`), hit-stop freezes (`0.06s`), and hit-flashes (`0.05s`) vanish between 1fps keyframes. Always inspect `action_burst_strip_01.png` (30fps) and `onion_skin_trail_01.png` so fast motion and transient VFX are captured.
- **Linear Motion Instead of Fitted Easing**: Never move UI popups, knockbacks, or jumps with constant linear speed when `vfx_timing_report.json` shows `easeOutBack` or parabolic gravity acceleration.
- **Shaking Physics Coordinates**: Apply `trauma^2` camera shake strictly to `ctx.translate`, never to entity collision coordinates.
