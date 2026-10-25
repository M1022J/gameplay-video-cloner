---
name: gameplay-video-cloner
description: Reverse-engineer and 1:1 replicate playable games from gameplay videos OR static screenshots (看视频或单张图片反推并复刻游戏玩法与动作特效). Bundles 25 open-source repositories (53 files): image-to-gameplay reverse-engineering (Jakeschincariol/replica-skill recon & imgdiff, image-to-code layer table & alpha audit, phaser4-gdd), video motion & optical-flow onion-skin trails (Schmandarine/web-motion-skill, OpenCV optical flow, bsisduck/video-analyzer, LottieFiles/frankxai easing), multi-agent swarm (obra/superpowers, orchestrating-swarms, subagent-orchestrator), 2D/3D skeletal animation (spine-animation-ai, rive-skills, blender-skills), and 74 game-dev & studio skills.
allowed-tools: default_api google youtube image_gen
---
# Gameplay Video & Screenshot Cloner (25-Repository All-in-One Suite — 53 Files)

Reverse-engineer and 1:1 replicate playable games from **either gameplay videos OR static screenshots/images**. This skill packages **20 executable Python scripts** and **32 reference playbooks** (53 files total) across 25 open-source repositories:

1. **Image-to-Gameplay Reverse-Engineering Suite (6 Repositories - NEW)**:
   - **`Jakeschincariol/replica-skill`** (`/replica-recon`, `/replica-design`, `/replica-diff`): `scripts/infer_gameplay_from_image.py` & `scripts/imgdiff_parity.py` + `references/image-to-gameplay-recon/02-jakeschincariol-replica-recon-and-diff.md` (infers screens, flows, state machines, and `features.csv` from screenshots, and scores visual edge-map layout parity).
   - **`yuzhworkhard-wq/image-to-code`**: `scripts/audit_png_assets.py` + `03-image-to-code-layer-table-and-alpha-audit.md` (builds the Pixel-Coordinate Layer Classification Table and audits extracted transparent PNG sprites so zero rectangular white/gray boxes remain).
   - **Visual Affordance & Semiotics Matrix (`Yakoub-ai/phaser4-gamedev`, `DY-2026/GameDesignOS`, `kursku/develop-web-game`, `caucy2026/game-playtest`)**: `01-visual-affordance-to-mechanics-matrix.md` & `04-phaser4-13-section-gdd-and-playtest-loop.md` (deduces hidden core loops, win/lose rules, physics engines, and economy math from static HUD badges, playfield geometry, and control overlays).
2. **Video Motion, Optical Flow, Onion-Skin Trails & VFX Suite (5 Repositories)**:
   - **`Schmandarine/web-motion-skill`**, **`alirezarezvani/senior-computer-vision`**, **`bsisduck/video-analyzer-skill`**, **`LottieFiles/motion-design-skill`**, **`frankxai/awesome-motion-design-agent-skills`**: `scripts/extract_motion_trails_and_vfx.py` & `scripts/extract_audio_sfx_peaks.py` + 4 playbooks under `references/video-motion-and-vfx-analysis/` (bakes 8-frame stroboscopic onion-skin trails + OpenCV optical flow velocity arrows into a single image, extracts 30/60fps burst strips, and quantifies hit-stop, screen shake, hit-flash, and easing curves).
3. **Multi-Agent Division-of-Labor & Swarm Orchestration Suite (5 Repositories)**:
   - **`obra/superpowers`**, **`kieranklaassen/orchestrating-swarms`**, **`sickn33/subagent-orchestrator`**, **`qodex-ai/multi-agent-orchestration`**, **`VoltAgent/awesome-claude-code-subagents`**: `scripts/orchestrate_subagents.py`, `scripts/swarm_task_board.py`, `scripts/merge_subagent_modules.py` + 4 playbooks under `references/multi-agent-orchestration/`.
4. **2D & 3D Skeletal Animation Suite (4 Repositories)**:
   - **`GenielabsOpenSource/spine-animation-ai`**, **`BowTiedSwan/rive-skills`**, **`composio-community/opencode-skills` (`blender-rigging-animation`)**, **`arjun988/blender-skills`**: `position_parts.py`, `build_spine_json.py`, `make_atlas.py`, `generate_spine_player.py` + 4 playbooks under `references/skeletal-animation-2d-3d/`.
5. **Cross-Engine Game Development & Studio Suite (5 Repositories)**:
   - **`ybuild-ai/ai-game-art-pipeline-skill`**, **`video-db/skills`**, **`PlayableIntelligence/game-creator`**, **`gamedev-skills/awesome-gamedev-agent-skills` (74 skills)**, **`Donchitos/Claude-Code-Game-Studios` (49 agents + 74 skills)**.

## Steps

### 1. Round 1 (Foundation): Image-to-Gameplay Recon + Video Motion Trails + Swarm Mission Brief

Run the automated reconnaissance scripts via `execute_bash` on the input video or screenshot(s):

```bash
# If input is a video: extract macro keyframes, 30fps burst strips, onion-skin optical flow trails & audio peaks
python3 skills/gameplay-video-cloner/scripts/analyze_gameplay_video.py <video_path> ./video_analysis --frames 16
python3 skills/gameplay-video-cloner/scripts/extract_motion_trails_and_vfx.py <video_path> ./video_analysis/motion_vfx --top-peaks 3 --fps 30
python3 skills/gameplay-video-cloner/scripts/extract_audio_sfx_peaks.py <video_path> ./video_analysis/audio_peaks.json

# Run Image-to-Gameplay Reverse-Engineering on the primary screenshot or keyframe (generates recon_gameplay_spec.json & features.csv)
python3 skills/gameplay-video-cloner/scripts/infer_gameplay_from_image.py ./video_analysis/frame_08.png ./recon_output

# Initialize Engine Router, 5-Subagent Context Packets & Swarm DAG Board
python3 skills/gameplay-video-cloner/scripts/detect_engine_router.py --workspace . --prompt "<user_request_summary>"
python3 skills/gameplay-video-cloner/scripts/orchestrate_subagents.py --project-dir ./subagent_workspace --game-title "<game_title>"
python3 skills/gameplay-video-cloner/scripts/swarm_task_board.py --board ./subagent_workspace/swarm_board.json init
```

- **Apply the 6-Dimension Visual Semiotics Matrix (`references/image-to-gameplay-recon/01-visual-affordance-to-mechanics-matrix.md`)**:
  1. **HUD Numerals & Bars -> Economy & Win/Lose Rules**: Deduce wave directors, XP curves, move limits, overflow timers, and combo decay bars from top/corner UI badges.
  2. **Playfield Geometry -> Physics Engine**: Deduce Suika sub-stepped circle collision, Survivor radial flocking, Grid snap-and-clear, Platformer gravity/coyote-time, or 3D Gate Runner projection from entity shapes and layout.
  3. **Control Affordances -> Input Bindings**: Deduce virtual joystick, slingshot trajectory preview, or card drag-and-drop from bottom-deck UI elements.
  4. **Layer Classification (`image-to-code`)**: Separate code-rendered HUD/backgrounds from cropped transparent PNG sprites (`audit_png_assets.py`).

### 2. Round 2 (Parallel Specialist Fan-Out): Execute Isolated Domain Subagents

- **`subagent-02-physics-controller`**: Implement the core loop, physics equations, and win/lose conditions listed in `recon_gameplay_spec.json` and `features.csv`.
- **`subagent-03-skeletal-art`**: Build 2D Spine/Rive bones (`solveTwoBoneIK`) or 3D articulated joints (`createProcedural3DRig`), plus `Juice.feedback()` (`trauma^2` shake, real-time `hit_stop`, `easeOutBack` squash-and-stretch).
- **`subagent-04-hud-audio`**: Build the pixel-accurate HUD, floating score/damage popups, `⚙️ 参数微调` live tuning drawer, and procedural Web Audio synth SFX.

### 3. Round 3 (Fan-In Review, Parity Diff & Delivery)

```bash
# Audit extracted PNG sprites (if any), verify subagent modules, validate architecture, and score feature parity
python3 skills/gameplay-video-cloner/scripts/merge_subagent_modules.py /working_dir/<conversation_id>/artifacts/file_generation/ttl=63d/output/<game_name>.html
python3 skills/gameplay-video-cloner/scripts/validate_architecture.py /working_dir/<conversation_id>/artifacts/file_generation/ttl=63d/output/<game_name>.html
```

- Present the playable game in Canvas via `google:show_file` along with the **Image-to-Gameplay Recon Matrix**, **Motion & VFX Telemetry Table**, and **Multi-Agent Division-of-Labor Summary**.
