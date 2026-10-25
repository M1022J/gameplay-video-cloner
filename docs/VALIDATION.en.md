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

## V2 supplement validation (2026-10-25)
| Check | Result |
|---|---|
| `extract_motion_trails_and_vfx.py` on a real video (OpenCV) | Pass: 3 burst strips + 3 onion-skin trail images + `vfx_timing_report.json` |
| `extract_audio_sfx_peaks.py` on the same video | Pass: `audio_peaks.json` with multiple medium-tier SFX peaks (e.g. 2.9s / 3.2s / 3.5s) |
| File-by-file diff of the v2 pack (46 files) against v1 | Only SKILL.md updated + 6 new files (2 scripts + 4 references); the other 39 files are byte-identical to v1 |
| 5 new upstream sources | All cloned with commits recorded (SOURCES #15–19) |

## V3 supplement validation (2026-10-25)
| Check | Result |
|---|---|
| `infer_gameplay_from_image.py` on a real screenshot | Pass: `recon_gameplay_spec.json` + `features.csv` (F01 viewport / F02 HUD / … feature matrix) |
| `imgdiff_parity.py` on two adjacent frames | Pass: parity JSON (feature_parity_score / shippable) + diff image |
| `audit_png_assets.py` on ordinary screenshots | Pass: correctly flags alpha-less screenshots as `transparent_bg_ok: false` |
| File-by-file diff of the v3 pack (53 files) against the current version | Only SKILL.md updated + 7 new files (3 scripts + 4 references); the other 45 files are byte-identical |
| 6 new upstream sources | All cloned with commits recorded (SOURCES #20–25) |
