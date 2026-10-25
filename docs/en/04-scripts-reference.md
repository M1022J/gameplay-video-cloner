# 04 · Scripts Reference (skill/scripts/, 17 scripts)

## Video analysis
| Script | Purpose | Basic usage |
|---|---|---|
| `analyze_gameplay_video.py` | All-in-one telemetry: frames + contact sheet + HUD variance map + scene cuts + palette → telemetry.json | `analyze_gameplay_video.py <video> <out_dir> [--frames 16]` |
| `extract_video_frames.py` | Extract frames by fps/range, resized as runtime texture sequences | `extract_video_frames.py <video> <out_dir> [--fps N --width W]` |
| `sheet_contact.py` | Build a numbered contact sheet from a frames directory | `sheet_contact.py <frames_dir> <out.png> [--cols 4]` |

## Art & skeleton (Spine chain)
| Script | Purpose | Basic usage |
|---|---|---|
| `extract_sprites.py` | Crop a sprite/UI element from a frame, optionally remove solid background | `extract_sprites.py <frame> <out> [--crop x,y,w,h --remove-bg]` |
| `chroma_key_magenta.py` | Remove #FF00FF magenta (or custom) chroma key and auto-trim | `chroma_key_magenta.py <in> <out> [--tolerance 45 --trim]` |
| `provider_stub.py` | Provider-neutral adapter interface for image/video generation models | Import as a library; no standalone CLI |
| `position_parts.py` | Auto-position separated body-part PNGs onto the assembled reference → layout.json | `position_parts.py --reference <img> --parts <dir>` |
| `build_spine_json.py` | Build Spine 4.2 skeleton.json (bone hierarchy + 6 animation presets) from a layout | `build_spine_json.py --config layout.json [--output skeleton.json]` |
| `make_atlas.py` | Pack part PNGs into a Spine .atlas + spritesheet PNG | `make_atlas.py --parts <dir> [--name skeleton]` |
| `generate_spine_player.py` | Generate a standalone HTML5 Canvas skeletal-animation player | `generate_spine_player.py --skeleton skeleton.json` |

## Orchestration & QA
| Script | Purpose | Basic usage |
|---|---|---|
| `orchestrate_subagents.py` | Generate 5 isolated subagent packets, mission_brief.json, sdd_ledger.md | `orchestrate_subagents.py --project-dir <dir> --game-title <title>` |
| `swarm_task_board.py` | DAG task board: init / complete (auto-unblocks downstream) / status | `swarm_task_board.py --board <file> init\|complete\|status` |
| `detect_engine_router.py` | Route engine / skeletal suite / genre / skill set from a request, outputs JSON | `detect_engine_router.py --workspace . --prompt "<request>"` |
| `merge_subagent_modules.py` | 3-point spot check: files exist, zero TODO/FIXME/placeholders | `merge_subagent_modules.py <file...>` |
| `validate_architecture.py` | 8-gate architecture validation of a finished game (Constants/reset/rAF/dt/dual input/shake/audio/render_game_to_text) | `validate_architecture.py <game.html>` |

## Video motion & VFX (v2 additions, require opencv)
| Script | Purpose | Basic usage |
|---|---|---|
| `extract_motion_trails_and_vfx.py` | High-FPS burst strips + optical-flow onion-skin trails + VFX timing JSON (shake / hit-stop / flash / easing fit) | `extract_motion_trails_and_vfx.py <video> <out_dir> [--top-peaks N --fps N]` |
| `extract_audio_sfx_peaks.py` | 50ms RMS audio peaks → aligned SFX events (audio_peaks.json) | `extract_audio_sfx_peaks.py <video> <out.json>` |

See `docs/en/07-video-motion-and-vfx.md`.

Note: Section 7 of `HANDBOOK.md` embeds full-length versions of these scripts (minor
detail differences vs. the zip versions) — the two copies are worth cross-reading. The v2 handbook is `HANDBOOK-v2.md`.
