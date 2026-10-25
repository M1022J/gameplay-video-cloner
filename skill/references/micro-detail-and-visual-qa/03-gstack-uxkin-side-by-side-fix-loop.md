# 03 — Side-by-Side Screenshot Diff & Atomic Fix Loop (`garrytan/gstack` & `uxkin/agent`)

## Sources
- [`garrytan/gstack` (`design-review` & `qa`)](https://github.com/garrytan/gstack)
- [`uxkin/agent` (`.agents/skills/ui-from-screenshot/SKILL.md`)](https://github.com/uxkin/agent/blob/main/.agents/skills/ui-from-screenshot/SKILL.md)
- [`Intense-Visions/harness-engineering` (`harness-visual-regression`)](https://github.com/Intense-Visions/harness-engineering/blob/main/agents/skills/claude-code/harness-visual-regression/SKILL.md)

## Closed-Loop "Measure -> Build -> Render -> Side-by-Side Diff -> Atomic Fix" Protocol
Never deliver a game after a single blind code-generation pass. Execute up to **5 closed-loop iterations**:
1. **Step 1 — Measure First (`uxkin/ui-from-screenshot`)**:
   - Run `slice_micro_detail_crops.py` and lock in exact pixel bounding boxes, `dominant_palette_hex`, `micro_accent_palette_hex`, and `measured_base_spacing_unit_px`.
2. **Step 2 — Render Live Game & Generate 3-Panel Comparison (`visual_verdict_diff_loop.py`)**:
   - Produces `visual_verdict_side_by_side.png` showing `1. ORIGINAL REFERENCE | 2. BUILT GAME CAPTURE | 3. DELTA-E DIFF HEATMAP` and `visual_verdict_report.json`.
3. **Step 3 — Inspect `visual_verdict_side_by_side.png` via `view_file`**:
   - Look directly at red/yellow hotspots in Panel 3 (the Delta-E diff heatmap) and read `actionable_fixes` in `visual_verdict_report.json`.
4. **Step 4 — Atomic Fix Pass (`garrytan/gstack`)**:
   - Fix every missing badge, misaligned HUD bar, wrong hex color, missing drop shadow, or unstyled font in a focused patch, then re-run `visual_verdict_diff_loop.py` until `composite_score >= 90.0`.
