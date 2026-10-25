# 04 · Scripts Reference (skill/scripts/, 12 scripts)

The v4 edition (2026-10-25) consolidated everything into 12 all-in-one scripts with
zero overlap. Parentheses name the old scripts each one replaces.

## Long video & micro-diff (new in v4)
| Script | Purpose | Basic usage |
|---|---|---|
| `stream_long_video_indexer.py` | O(1)-memory streaming scan of 30–60+ min videos: 32x18 tile micro-diff + cumulative drift detection, packed_timeline.md + micro-energy JSON (replaces analyze_gameplay_video / extract_video_frames / sheet_contact) | `stream_long_video_indexer.py <video> <out_dir> [--stride 1]` |
| `extract_micro_frame_deltas.py` | 3x zoomed delta-patch strips of just the changing bounding box + 10x amplified residual strips | `extract_micro_frame_deltas.py <video> <out_dir> [--start S --duration S]` |
| `subpixel_motion_oscilloscope.py` | 0.01px sub-pixel centroid trajectories + loop-period / Bezier velocity-curve fitting | `subpixel_motion_oscilloscope.py <video> <out.json> [--roi x,y,w,h]` |
| `bidirectional_context_ledger.py` | Bidirectional causal ledger: rolling cross-chunk state + backward causal backfill + economy-curve fitting (init / append-chunk / export-brief) | `bidirectional_context_ledger.py init <ledger.json>` |

## Motion, audio & image recon (kept from earlier editions)
| Script | Purpose | Basic usage |
|---|---|---|
| `extract_motion_trails_and_vfx.py` | 30/60fps burst strips + optical-flow onion-skin trails + VFX timing JSON | `extract_motion_trails_and_vfx.py <video> <out_dir>` |
| `extract_audio_sfx_peaks.py` | 50ms RMS audio peaks → aligned SFX events | `extract_audio_sfx_peaks.py <video> <out.json>` |
| `infer_gameplay_from_image.py` | Reverse-engineer gameplay from one screenshot → recon_gameplay_spec.json + features.csv | `infer_gameplay_from_image.py <image> <out_dir>` |

## Micro-detail, sprites & skeletal swarm (consolidated in v4)
| Script | Purpose | Basic usage |
|---|---|---|
| `slice_micro_detail_crops.py` | SAHI 2x2 overlapping quadrants + 1:1 zones + Top-8 2x micro-widget crops + rare accent-color extraction | `slice_micro_detail_crops.py <image.png> <out_dir>` |
| `process_and_audit_sprites.py` | Sprite cropping / #FF00FF chroma-key cleaning / RGBA alpha audit in one (replaces extract_sprites / chroma_key_magenta / audit_png_assets / provider_stub) | `process_and_audit_sprites.py {crop,chroma,audit} ...` |
| `spine_and_swarm_pipeline.py` | Engine routing + 5-subagent swarm init/verify + Spine rig & atlas building (replaces 8 micro-scripts) | `spine_and_swarm_pipeline.py {route-engine,init-swarm,verify-swarm,build-spine-rig} ...` |

## Verification loop
| Script | Purpose | Basic usage |
|---|---|---|
| `visual_verdict_diff_loop.py` | Headless render + 3-panel Delta-E heatmap + 6D scoring (≥90 gate) (replaces imgdiff_parity) | `visual_verdict_diff_loop.py <ref.png> <built.png/html/url> <out_dir>` |
| `validate_architecture.py` | Runtime architecture audit (constants / dt / dual input / shake / audio synth / render_game_to_text) | `validate_architecture.py <game.html>` |

Motion & VFX: `docs/en/07-video-motion-and-vfx.md`. Image recon:
`docs/en/08-image-to-gameplay.md`. Long video / sub-pixel / micro-detail QA:
`docs/en/09-long-video-and-micro-detail-qa.md`.
