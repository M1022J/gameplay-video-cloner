# 02 · Quick Start

## Requirements

- Python 3.10+ with `pip install -r requirements.txt` (Pillow, numpy)
- System tools `ffmpeg` / `ffprobe` (required for frame extraction and telemetry)
- Optional: Node.js (only some upstream toolchains need it; the core scripts do not)

## Four steps

```bash
# 1) Video telemetry: 16 frames, contact sheet, HUD variance map, palette -> telemetry.json
python3 skill/scripts/analyze_gameplay_video.py <video.mp4> ./video_analysis --frames 16

# 2) Engine routing: which engine / skeletal suite / genre baselines to use
python3 skill/scripts/detect_engine_router.py --workspace . --prompt "<one-line replication request>"

# 3) Initialize the swarm: 5 subagent context packets + recovery ledger + DAG task board
python3 skill/scripts/orchestrate_subagents.py --project-dir ./subagent_workspace --game-title "<game title>"
python3 skill/scripts/swarm_task_board.py --board ./subagent_workspace/swarm_board.json init

# 4) Acceptance: 3-point spot check (scope / contract / zero placeholders) + 8-gate architecture check
python3 skill/scripts/merge_subagent_modules.py <game.html>
python3 skill/scripts/validate_architecture.py <game.html>
```

## Feeding it to an AI agent

Give the root `SKILL.md` to your agent environment (Claude Code / Cursor / Codex all work),
then hand it a gameplay video and say "replicate this per the skill". The agent follows the
3-round workflow in `SKILL.md` and consults `skill/references/`, `HANDBOOK.md`, and the
upstream originals under `upstream/` for detail.

## Validation

The scripts above were executed during integration (real-video telemetry, task-board init,
architecture check 8/8). See `docs/VALIDATION.md` (English: `docs/VALIDATION.en.md`).
