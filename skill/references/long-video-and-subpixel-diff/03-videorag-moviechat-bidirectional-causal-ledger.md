# 03 — VideoRAG & MovieChat Bidirectional Causal Graph ("上下结合判断" & Economy Curve Regression)

## Sources
- [`HKUDS/VideoRAG`](https://github.com/HKUDS/VideoRAG) & [`HKUDS/VideoAgent`](https://github.com/HKUDS/VideoAgent/blob/main/readme.md) (*Dual-Channel Temporal Knowledge Graph*)
- [`ttengwang/awesome_long_form_video_understanding`](https://github.com/ttengwang/awesome_long_form_video_understanding) (*MovieChat Short-Term Sliding Window + Long-Term Consolidation Memory*)
- [`browser-use/video-use` (`SKILL.md`)](https://github.com/browser-use/video-use/blob/main/SKILL.md) (*Packed Timeline View & On-Demand Drill-Down*)

## Two-Pass Bidirectional Reasoning (`scripts/bidirectional_context_ledger.py`)
1. **Forward Pass (上文推下文 — Rolling State Accumulation)**:
   - Each chunk (`chunk_001` .. `chunk_N`) carries `upstream_context_event_ids` (last 2 events of `chunk_{i-1}`) and `downstream_lookahead_event_ids` (first 2 events of `chunk_{i+1}`).
   - `append-chunk` logs discovered FSM states, active buffs/items, numerical samples, and `new_hypotheses` into `rolling_state_ledger.json`.
2. **Backward Pass (下文反推上文 — Retrospective Causal Backfill)**:
   - When a later chunk (`chunk_018` at `24:50`) reveals the effect of an earlier mystery bar or item (`chunk_003` at `02:10`), passing `resolved_hypotheses` automatically backfills the upstream node and links `[t_cause: 02:10] <==> [t_effect: 24:50]`.
3. **Longitudinal Economy Curve Fitting (`fit_curve_from_samples`)**:
   - Automatically fits Linear (`y = m*x + c`) vs. Exponential (`y = a * r^x`) formulas with $R^2$ verification across all level/wave data points collected over the 30–60 minute video.
