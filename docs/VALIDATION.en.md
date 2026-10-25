# VALIDATION — Integration Test Record (2026-10-25)

Executed locally against the integrated project (not just build logs):

| Check | Result |
|---|---|
| `py_compile` on all 15 scripts in `skill/scripts/` | All pass |
| `analyze_gameplay_video.py` on a real video (1280×720 / 24fps / 6.04s) | Pass: 8 frames + `contact_sheet.png` + `hud_variance_map.png` + `telemetry.json` (16:9 landscape correctly detected) |
| `orchestrate_subagents.py` + `swarm_task_board.py init` | Pass: generated `mission_brief.json`, `sdd_ledger.md`, `swarm_board.json`, and 5 subagent context packets |
| `validate_architecture.py` on a sample HTML game | 8/8 (Constants / reset / rAF / dt / dual input / trauma shake / WebAudio / render_game_to_text) |
| `detect_engine_router.py` (portrait merge-puzzle request) | Pass: outputs engine routing + skeletal / multi-agent / discipline skill lists as JSON |
| Dependencies | Python 3.12 + Pillow + numpy installed; ffmpeg/ffprobe installed |

Structure check: 2,300+ text files in the repo; the 40 files of `skill/` match the
original zip one-to-one; the 14 directories under `upstream/` correspond exactly to the
commit list in `SOURCES.md` / `SOURCES.en.md`.
