# 03 — Multi-Pass Game Font OCR & VLM Semantic Synergy (`PaddleOCR-Skills` + `skillsbench/image-ocr` + `smart-ocr`)

## Sources
- [`Aidenwu0209/PaddleOCR-Skills`](https://github.com/Aidenwu0209/PaddleOCR-Skills) & [`PaddlePaddle/PaddleOCR`](https://github.com/PADDLEPADDLE/PADDLEOCR)
- [`benchflow-ai/skillsbench` (`image-ocr/SKILL.md`)](https://github.com/benchflow-ai/skillsbench/blob/main/tasks/jpg-ocr-stat/environment/skills/image-ocr/SKILL.md)
- [`claude-office-skills/skills` (`smart-ocr/SKILL.md`)](https://github.com/claude-office-skills/skills/blob/main/smart-ocr/SKILL.md) & [`hypoxic127/FH6-AFK`](https://github.com/hypoxic127/FH6-AFK)

## 3-Pass Game HUD OCR Preprocessing + Confidence-Gated VLM Override
1. **Variant 1 (`3x` Bicubic Upscale + Pill-Border Mask + Bright-Fill Stroke Inversion + `16px` Quiet Zone)**:
   - Isolates bright white/gold game HUD text (`Luma > 180`), masks outer button borders, and inverts to crisp black-on-white, achieving `91%–96%` confidence on `Lv.15` and `1450/2000`.
2. **Variant 2 (`3x` Upscale + CLAHE + Unsharp Mask)**: Reads low-contrast card descriptions.
3. **Variant 3 (`3x` Upscale + Inverted Autocontrast)**: Reads dark text on bright buttons.
4. **Regex Game-Numeric Parser (`parse_game_numeric_string`)**:
   - Automatically parses `fraction_bar` (`1450/2000`), `level_or_wave` (`Lv.15`), `timer_mm_ss` (`02:45`), `percentage` (`+15.5%`), `multiplier` (`x2.5`), and `K/M/B` currencies (`12.5K`).
