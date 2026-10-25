# 01 — SAHI High-Res Quadrant & 1:1 Native-Pixel ROI Zoom (`senior-computer-vision` & `uxkin/ui-from-screenshot`)

## Why Small Details Get Lost in Standard Vision Prompts
When you feed a full `1920x1080` or `1280x720` gameplay frame into a multi-modal LLM, the vision encoder typically downsamples or patches the whole image. As a result:
- **12px–16px mini badges** (red notification dots, star tiers, elemental affinity icons, lock icons) blur into adjacent borders.
- **1px–2px inner strokes and bevel highlights** on game buttons disappear.
- **Subtle drop shadows, cooldown radial wedges, and buff stack numbers** (`x2`, `Lv.99`, `+15%`) become illegible.

## Mandatory 3-Stage High-Res Slicing Protocol (`scripts/slice_micro_detail_crops.py`)
Before writing any UI or rendering code, run:
```bash
python3 scripts/slice_micro_detail_crops.py <reference_frame.png> ./micro_crops/
```
1. **Overlapping `2x2` Quadrants (15% Center Overlap)**:
   - Inspect `quad_top_left.png`, `quad_top_right.png`, `quad_bottom_left.png`, and `quad_bottom_right.png` individually so no element near the screen center is bisected.
2. **Functional 1:1 Native-Pixel Game Zones**:
   - `zone_top_hud_1to1.png` (top 20% — avatars, HP/XP bars, currency counters, stage progress, pause/settings buttons).
   - `zone_center_arena_1to1.png` (center 60% — character sprites, enemy hitboxes, floating damage numbers, ground shadows, projectiles).
   - `zone_bottom_controls_1to1.png` (bottom 25% — skill cards, cooldown overlays, mana costs, upgrade buttons, joystick/tab bar).
3. **Top-8 High-Edge-Density `2x` Bicubic Zoom Crops**:
   - Inspect `micro_detail_01_2x_zoom.png` through `micro_detail_08_2x_zoom.png` alongside `micro_detail_manifest.json` (`dominant_palette_hex`, `micro_accent_palette_hex`, and `measured_base_spacing_unit_px`).
