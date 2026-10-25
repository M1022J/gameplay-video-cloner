# 01 — O(1) Memory Streaming, `32x18` Localized Tile-Grid Micro-Diff & Dual-Anchor Drift (`VidaForge` + `motiscope` + `video-frames-skill`)

## Sources
- [`KumarSashank/motiscope`](https://github.com/KumarSashank/motiscope/blob/main/README.md) (*Localized Tile-Grid Motion-Energy Peak Detection — Zero Whole-Frame Washout*)
- [`GAIR-NLP/VidaForge`](https://github.com/GAIR-NLP/VidaForge) & [`mugnimaestra/video-frames-skill`](https://github.com/mugnimaestra/video-frames-skill) (*O(1) Streaming Segmentation, Resume Checkpoints & Model Tile Budgeting*)

## Solving Both "50,000+ Frames OOM" AND "Every Frame Only Has a Tiny Difference"
Naive global `dHash` (`9x8`) or whole-frame average diff washes out a `20x20` px icon/number change by `5,000x`. `scripts/stream_long_video_indexer.py` solves both scale and sensitivity in a single `O(1)` memory pass (`--stride 1`):

1. **`32x18` Max-Pooled Local Tile Grid (`576` Independent Micro-Zones)**:
   - Computes L1 pixel diff inside each of the `576` local tiles and takes `max_tile_delta = max(tile_means)`.
   - Even if `575` tiles are completely frozen and only `1` tile has a tiny icon/digit/cooldown tick (`max_tile_delta >= 12.0`), it immediately triggers `LOCALIZED_MICRO_CHANGE` and draws a cyan reticle around `hot_tile_bbox_norm`.
2. **Dual-Anchor Cumulative Drift (`Adjacent Frame F_{t-1}` + `Last Saved Anchor Frame F_{anchor}`)**:
   - Tracks both `|F_t - F_{t-1}|` (for sudden micro-events) and `|F_t - F_{anchor}|` (for slow `0.15px/frame` creeps like progress bars or camera pans). Once cumulative drift in any tile crosses `18.0`, it fires `CUMULATIVE_SLOW_DRIFT` and resets `F_{anchor} = F_t`.
3. **Zero-Loss Frame-by-Frame Numeric Curve (`frame_by_frame_micro_energy.json`)**:
   - Records `{f, t, global_diff, max_tile_diff, cum_drift_diff, active_tiles}` for every single frame at zero vision-token cost, while grouping visual keyframes into overlapping `60s` sliding-window chunks (`packed_timeline.md`).
