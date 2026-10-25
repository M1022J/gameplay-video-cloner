# 09 · Long Video, Sub-Pixel Micro-Diff & Micro-Detail QA (v4 supplement)

## Three blind spots it closes
1. **Long videos can't be watched end to end**: 30–60 minute, 100k-frame recordings —
   sparse sampling misses events, loading everything runs out of memory.
2. **Micro-motion is invisible**: 0.01–0.5px breathing scales, easing tails and
   sub-pixel drift don't show up in frame-by-frame eyeballing.
3. **Small print and widgets blur out**: HUD text, badges and button states vanish
   when a full frame is downscaled — exactly what gets lost in a clone.

## The toolchain
- **O(1) streaming indexer** (`stream_long_video_indexer.py`; motiscope / VidaForge /
  video-frames-skill / video-use): scans frame by frame without loading the video;
  a 32x18 tile grid localizes single-tile micro-changes (LOCALIZED_MICRO_CHANGE) and
  dual anchors catch slow cumulative drift (CUMULATIVE_SLOW_DRIFT).
- **Bidirectional causal ledger** (`bidirectional_context_ledger.py`; HKUDS/VideoRAG /
  VideoAgent / MovieChat): forward rolling state + backward causal backfill across
  chunks, plus economy/progression curve fitting (linear/exponential with R²).
- **Micro-delta strips & sub-pixel oscilloscope** (`extract_micro_frame_deltas.py` +
  `subpixel_motion_oscilloscope.py`; DVR-Scan / snapcn motion-quality): 3x zoomed
  strips of just the changing box + 10x amplified residuals; edge-alpha weights
  recover 0.01px trajectories, fitted for loop periods and cubic-bezier velocity.
- **SAHI micro-detail slicing** (`slice_micro_detail_crops.py`; uxkin/ui-from-screenshot
  / pixel-perfect-skill): 2x2 overlapping quadrants + native-pixel HUD/Arena/Control
  zones + Top-8 high-edge-density 2x widget crops, plus rare accent colors (0.05%–2.5%).
- **Visual-verdict loop** (`visual_verdict_diff_loop.py`; vibeeval/visual-verdict /
  garrytan/gstack / harness-engineering): Original | Built | Delta-E heatmap panels,
  6D scoring with a ≥90 gate; failures go back with the heatmap as the locator.
  Rastian's 24-point micro-detail checklist is the human backstop.

## Verified during integration
The streamer produced packed_timeline.md + micro-energy JSON on a real video; the
delta script cut 24 patch strips; the oscilloscope fitted a sharp_cubic_bezier_burst
over 73 frames; the verdict loop scored two genuinely different frames 67.86/100
(REVISE) — the number tracks what the eye sees.

Originals: `upstream/motiscope/`, `upstream/vidaforge/`, `upstream/video-frames-skill/`,
`upstream/video-use/`, `upstream/dvr-scan/`, `upstream/snapcn/`, `upstream/videorag/`,
`upstream/videoagent/`, `upstream/pixel-perfect-skill/`, `upstream/gstack/`,
`upstream/interaction-design-skills/`, `upstream/awesome-long-form-video-understanding/`,
`upstream/afterxleep-agents/`, `upstream/harness-engineering/`, `upstream/vibecosystem/`,
`upstream/uxkin-agent/`; summaries in `skill/references/long-video-and-subpixel-diff/`
and `skill/references/micro-detail-and-visual-qa/`.
