---
name: gameplay-video-cloner
description: Reverse-engineer and 1:1 replicate playable games directly from gameplay videos (看游戏视频直接复刻游戏), screen recordings, GIFs, or video URLs using a Lead-Agent + Parallel-Subagents Swarm workflow. Bundles 14 open-source repositories (40 files): multi-agent orchestration suites (obra/superpowers dispatching-parallel-agents & subagent-driven-development, kieranklaassen/orchestrating-swarms, sickn33/subagent-orchestrator, qodex-ai/multi-agent-orchestration, VoltAgent/awesome-claude-code-subagents), 2D/3D skeletal animation suites (GenielabsOpenSource/spine-animation-ai, BowTiedSwan/rive-skills, composio-community/opencode-skills blender-rigging-animation, arjun988/blender-skills), and game pipelines (ybuild-ai/ai-game-art-pipeline-skill, video-db/skills, PlayableIntelligence/game-creator, gamedev-skills/awesome-gamedev-agent-skills, Donchitos/Claude-Code-Game-Studios). Use whenever the user shares a gameplay video or asks to clone, replicate, rig, animate, or multi-agent build a 2D/3D game.
allowed-tools: default_api google youtube image_gen
---
# Gameplay Video Cloner (14-Repository Multi-Agent Swarm, 2D/3D Skeletal & Game Engine Suite)

Reverse-engineer gameplay videos, screen recordings, GIFs, or video URLs into playable 1:1 game replicas using a **Lead Orchestrator + Parallel Specialist Subagents Swarm** architecture. This skill packages **15 executable scripts** and **24 reference modules** (40 files total) across 14 open-source repositories:

## 1. Bundled Open-Source Skill Repositories

### Part A: Multi-Agent Division-of-Labor & Swarm Orchestration (5 Repositories)
1. **obra/superpowers (`dispatching-parallel-agents` & `subagent-driven-development`)**:
   - Script & Reference: `scripts/orchestrate_subagents.py` + `references/multi-agent-orchestration/01-obra-superpowers-parallel-and-sdd.md` (isolated Context Briefs per subagent, zero context pollution, persistent `sdd_ledger.md` recovery ledger, and Two-Stage Review Gate: Spec Compliance + Code Quality).
2. **kieranklaassen/orchestrating-swarms (Claude Code Swarm Orchestration)**:
   - Script & Reference: `scripts/swarm_task_board.py` + `references/multi-agent-orchestration/02-swarm-teammate-and-dag-taskboard.md` (Leader + Teammates, 6 Swarm patterns, `blockedBy` DAG task queue with automatic downstream task unblocking, and JSON inbox messaging).
3. **sickn33/antigravity-awesome-skills (`subagent-orchestrator`)**:
   - Script & Reference: `scripts/merge_subagent_modules.py` + `references/multi-agent-orchestration/03-antigravity-subagent-orchestrator-6-phases.md` (6-Phase Mission Brief, Context Packet isolation, Round-by-Round parallel execution, 3-Point Spot Check for scope/contract/zero-TODOs, surgical single-agent repair, and final integration sweep).
4. **qodex-ai/ai-agent-skills (`multi-agent-orchestration`) & VoltAgent/awesome-claude-code-subagents (100+ Subagents)**:
   - Reference: `references/multi-agent-orchestration/04-qodex-voltagent-topologies-and-roles.md` (5 orchestration topologies, shared-memory `EventBus` contract table for the 5 Game-Cloner Specialist Subagents, and 3-Agent Consensus Balancing).

### Part B: 2D & 3D Skeletal Animation Suites (4 Repositories)
5. **GenielabsOpenSource/spine-animation-ai (Spine 4.2 2D Skeletal Auto-Rigging)**:
   - Scripts & Reference: `scripts/position_parts.py`, `scripts/build_spine_json.py`, `scripts/make_atlas.py`, `scripts/generate_spine_player.py` + `references/skeletal-animation-2d-3d/01-spine-2d-skeletal-animation-ai.md` (16-bone humanoid hierarchy, 6 animation presets, and analytic 2-bone IK solver `solveTwoBoneIK`).
6. **BowTiedSwan/rive-skills (Rive 2D Bones, Weighted Meshes, IK & State Machines)**:
   - Reference: `references/skeletal-animation-2d-3d/02-rive-2d-bones-ik-state-machines.md`.
7. **composio-community/opencode-skills (`blender-rigging-animation`) & arjun988/blender-skills (94 3D Skills)**:
   - Reference: `references/skeletal-animation-2d-3d/03-blender-3d-rigging-and-animation.md` + `04-runtime-3d-skinnedmesh-ik-threejs-unity-godot.md` (`createProcedural3DRig` & `GlbAnimationController`).

### Part C: Video Understanding, Art Pipeline & Cross-Engine Game Studios (5 Repositories)
8. **ybuild-ai/ai-game-art-pipeline-skill**: 5 scripts (`extract_video_frames.py`, `sheet_contact.py`, `chroma_key_magenta.py`, `provider_stub.py`, `extract_sprites.py`) + 5 reference guides under `references/ybuild-art-pipeline/`.
9. **video-db/skills**: `scripts/analyze_gameplay_video.py` + `references/videodb-workflows/video-scene-ocr-audio-indexing.md`.
10. **PlayableIntelligence/game-creator**: `scripts/validate_architecture.py` + `references/playable-game-creator/11-skills-and-11-commands.md` (11 skills + 11 commands).
11. **gamedev-skills/awesome-gamedev-agent-skills**: `scripts/detect_engine_router.py` + 6 catalog modules under `references/awesome-gamedev-74-skills/` (all 74 skills).
12. **Donchitos/Claude-Code-Game-Studios**: 3 modules under `references/claude-code-game-studios/` (49 studio agents + 74 slash commands + 15 hooks + 14 path rules).

## When to Use

- The user shares a gameplay video, screen recording, GIF, or link and asks to clone, replicate, or rebuild the game.
- The user wants a Lead Agent to coordinate multiple specialized Subagents in parallel (Telemetry Architect, Physics/AI Engineer, 2D/3D Skeletal Animator, HUD/Audio Designer, QA Verifier) to build, rig, or polish a game.

## Steps

### 1. Round 1 (Foundation): Video Telemetry, Engine Routing & Multi-Agent Mission Brief

Run the parallel discovery and mission-decomposition scripts:

```bash
# 1) Extract video keyframes, contact sheet, HUD variance map, scene cuts & dominant hex palette
python3 skills/gameplay-video-cloner/scripts/analyze_gameplay_video.py <video_path> ./video_analysis --frames 16

# 2) Route engine, 2D/3D skeletal suite, genre & multi-agent swarm configuration
python3 skills/gameplay-video-cloner/scripts/detect_engine_router.py --workspace . --prompt "<user_request_summary>"

# 3) Initialize the 5-Subagent Mission Brief, isolated Context Packets, SDD Ledger & DAG Task Board
python3 skills/gameplay-video-cloner/scripts/orchestrate_subagents.py --project-dir ./subagent_workspace --game-title "<game_title>"
python3 skills/gameplay-video-cloner/scripts/swarm_task_board.py --board ./subagent_workspace/swarm_board.json init
```

### 2. Round 2 (Parallel Specialist Fan-Out): Execute Isolated Domain Subagents

- **`subagent-02-physics-controller` (`PhysicsSystem` + `PlayerController` + `WaveDirector`)**:
  - Implement delta-time normalized movement (`dt`), coyote time/jump buffer or pointer drag lerp, sub-stepped circle/AABB collision detection, and enemy steering/wave spawning. Emit `on_hit`, `on_merge`, `on_pickup`, `on_land`, `on_death` via `EventBus`.
- **`subagent-03-skeletal-art` (`SkeletalRig` + `solveTwoBoneIK` + `Juice` + `ParticleSystem`)**:
  - For 2D games, run `position_parts.py` + `build_spine_json.py` or build a Canvas 2D hierarchical bone rig (`root -> hip -> torso -> head / arms / legs`) with cubic bezier `[0.25, 0, 0.75, 1]` interpolation, `0.1s` head/cape follow-through, and analytic 2-bone IK (`solveTwoBoneIK`).
  - For 3D games, use `createProcedural3DRig` or `GlbAnimationController` (`THREE.AnimationMixer` crossfades).
  - Attach 3-tier `Juice.feedback(x, y, 'small'|'medium'|'large')` with decaying `trauma^2` camera offset shake, real-time unscaled `hit_stop`, and `easeOutBack` squash-and-stretch.
- **`subagent-04-hud-audio` (`HUDRenderer` + `AudioSynth` + `TuningDrawer`)**:
  - Render score/health/XP bars inside the static HUD safe-zones detected in `telemetry.json`, add floating damage/score numbers, build the collapsible `⚙️ 参数微调` live tuning drawer, and wire procedural Web Audio synthesizer SFX/BGM to `EventBus`.

### 3. Round 3 (Fan-In Review & Assembly): 3-Point Spot Check, QA Gate & Delivery

```bash
python3 skills/gameplay-video-cloner/scripts/merge_subagent_modules.py <output_html>
python3 skills/gameplay-video-cloner/scripts/validate_architecture.py <output_html>
```

## Gotchas

- **Dumping Full Session History into Subagents**: Always isolate each subagent to its `AGENT CONTEXT PACKET` and shared `EventBus` contract (`obra/superpowers` rule).
- **Skipping the 3-Point Spot Check Between Rounds**: Never merge a subagent module that contains `TODO` placeholders or mutates another subagent's private state directly instead of emitting `EventBus` events.
- **Shaking Physics Coordinates**: Apply `trauma^2` camera shake strictly to the visual render transform (`ctx.translate`), never to physics collision bodies.
