# Gameplay Video Cloner — Replicate Games 1:1 from Gameplay Videos (Integrated Edition)

Reverse-engineer a gameplay video, screen recording, GIF, or video URL into a playable
1:1 replica, using a **Lead Agent + Parallel Subagents Swarm** workflow: video telemetry,
engine routing, 2D/3D skeletal animation, physics/controllers, HUD/audio synthesis, and QA gates.

This is the **integrated edition**: in the original skill package (zip) the body text was
mostly summaries, with the substance scattered across 14 open-source repositories.
Everything cited has been downloaded and merged here into a single ready-to-use project.

## Contents

| Part | Location | Description |
|---|---|---|
| The skill | `SKILL.md` + `skill/` | Entry point + 15 executable Python scripts (`skill/scripts/`) + 24 reference summaries (`skill/references/`) |
| Single-file handbook | `HANDBOOK.md` | The user-provided all-in-one handbook (870 lines, full embedded scripts + all playbooks) |
| Upstream originals | `upstream/` | Everything this skill cites from its 14 sources (table below, details in `SOURCES.en.md`) |
| Requirements | `requirements.txt` | Python: Pillow, numpy; system: ffmpeg / ffprobe |

## Documentation (split by topic, Chinese + English)

- Chinese: `docs/zh/` — 01 总览 · 02 快速开始 · 03 工作流与蜂群架构 · 04 脚本参考 · 05 骨骼动画 · 06 上游与整合说明
- English: `docs/en/` — 01 Overview · 02 Quick Start · 03 Workflow & Swarm · 04 Scripts Reference · 05 Skeletal Animation · 06 Upstream & Integration

## Upstream at a glance (`upstream/`)

| Directory | Source | Included |
|---|---|---|
| `superpowers/` | obra/superpowers | Whole repo (parallel subagent dispatch + subagent-driven development) |
| `orchestrating-swarms/` | kieranklaassen (Gist) | The swarm-orchestration SKILL.md (the handbook calls it a repo; it is a Gist) |
| `antigravity-subagent-orchestrator/` | sickn33/antigravity-awesome-skills | Only the cited `subagent-orchestrator` skill (origin repo is 466MB) |
| `qodex-multi-agent-orchestration/` | qodex-ai/ai-agent-skills | Only the cited `multi-agent-orchestration` skill |
| `awesome-claude-code-subagents/` | VoltAgent/awesome-claude-code-subagents | Whole repo (100+ subagent catalog) |
| `spine-animation-ai/` | GenielabsOpenSource/spine-animation-ai | Whole repo (Spine 4.2 2D skeletal auto-rigging) |
| `rive-skills/` | BowTiedSwan/rive-skills | Whole repo (Rive bones / meshes / state machines) |
| `opencode-blender-rigging-animation/` | composio-community/opencode-skills | Only the cited `blender-rigging-animation` skill |
| `blender-skills/` | arjun988/blender-skills | Whole repo (94 Blender 3D skills) |
| `ai-game-art-pipeline-skill/` | ybuild-ai/ai-game-art-pipeline-skill | Whole repo (game art pipeline) |
| `videodb-skills/` | video-db/skills | Whole repo (video scene / OCR / timeline indexing) |
| `game-creator/` | PlayableIntelligence/game-creator | `skills/ agents/ templates/ scripts/ tests/` + root docs (excludes the 140MB `assets/` and 70MB `examples/` media libraries; see `SOURCES.en.md`) |
| `awesome-gamedev-agent-skills/` | gamedev-skills/awesome-gamedev-agent-skills | Whole repo (74 cross-engine skills) |
| `claude-code-game-studios/` | Donchitos/Claude-Code-Game-Studios | Whole repo (49 studio agents + hooks/rules) |

URLs, pinned commit SHAs, licenses, and inclusion details: [`SOURCES.en.md`](SOURCES.en.md).
16 binary media files (demo GIFs/MP4, banner images) are not in the GitHub upload;
see [`docs/BINARY_FILES.en.md`](docs/BINARY_FILES.en.md). They are present in the local copy.

## Quick start

```bash
pip install -r requirements.txt   # plus system ffmpeg / ffprobe

# 1) Video telemetry: 16 frames, contact sheet, HUD variance map, palette -> telemetry.json
python3 skill/scripts/analyze_gameplay_video.py <video.mp4> ./video_analysis --frames 16

# 2) Engine / genre routing
python3 skill/scripts/detect_engine_router.py --workspace . --prompt "<replication request>"

# 3) Initialize the 5-subagent packets + DAG task board
python3 skill/scripts/orchestrate_subagents.py --project-dir ./subagent_workspace --game-title "<title>"
python3 skill/scripts/swarm_task_board.py --board ./subagent_workspace/swarm_board.json init

# 4) Acceptance: 3-point spot check + 8-gate architecture validation
python3 skill/scripts/merge_subagent_modules.py <game.html>
python3 skill/scripts/validate_architecture.py <game.html>
```

The full workflow (3-round swarm: telemetry & contract → parallel specialists → review &
assembly) is specified in `SKILL.md` and `HANDBOOK.md`.

## License

This integration does not alter any upstream license: each `upstream/<dir>` keeps its own
LICENSE (spine-animation-ai is PolyForm Noncommercial 1.0.0; most others are MIT /
Apache-2.0). `skill/`, `SKILL.md`, and `HANDBOOK.md` come from the user-provided package.
