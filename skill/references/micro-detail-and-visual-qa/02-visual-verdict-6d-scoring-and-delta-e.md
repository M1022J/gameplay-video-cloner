# 02 — 6-Dimension Visual Verdict Scoring & Delta-E Color Gate (`vibeeval/vibecosystem` & `Huc91/pixel-perfect-skill`)

## Sources
- [`vibeeval/vibecosystem` (`skills/visual-verdict/SKILL.md`)](https://github.com/vibeeval/vibecosystem/blob/main/skills/visual-verdict/SKILL.md)
- [`Huc91/pixel-perfect-skill`](https://github.com/Huc91/pixel-perfect-skill)
- [`afterxleep/agents` (`skills/pixel-perfect-design/SKILL.md`)](https://github.com/afterxleep/agents/blob/main/skills/pixel-perfect-design/SKILL.md)

## Weighted 6-Dimension Visual Verdict Formula
Run `python3 scripts/visual_verdict_diff_loop.py <reference.png> <built_game.html> ./verdict_out/` to compute:
$$\text{Composite Score} = 0.25 \cdot S_{\text{Layout}} + 0.15 \cdot S_{\text{Typography}} + 0.15 \cdot S_{\text{Color}} + 0.15 \cdot S_{\text{Viewport}} + 0.15 \cdot S_{\text{Polish}} + 0.15 \cdot S_{\text{Completeness}}$$

| Dimension | Weight | What It Audits | Pass Target |
| :--- | :--- | :--- | :--- |
| **1. Layout & Spatial Occupancy** | `25%` | Dilated Canny edge IoU & quadrant bounding-box alignment | `>= 88/100` |
| **2. Typography & HUD Hierarchy** | `15%` | Top/Bottom HUD text density, font weight, tabular numerals, stroke contrast | `>= 85/100` |
| **3. Color Palette & CIE LAB Delta-E** | `15%` | Perceptual color distance ($\Delta E_{ab}$) across backgrounds, bars, and micro-accents | `>= 88/100` |
| **4. Viewport & Aspect Integrity** | `15%` | Exact aspect ratio (`16:9` / `9:16`), zero scrollbars, zero text clipping | `>= 95/100` |
| **5. Micro-States & Surface Polish** | `15%` | Laplacian texture variance: inner borders, bevels, shadows, glow, particles | `>= 85/100` |
| **6. Element Completeness Parity** | `15%` | Per-quadrant contour/widget count (`built_micro_elements == reference_micro_elements`) | `>= 90/100` |

## Hard Gate Thresholds
- **PASS (`>= 90.0` and all dimensions `>= 75.0`)**: Ready for final delivery.
- **REVISE (`60.0 – 89.9`)**: Must execute another atomic fix iteration targeting the lowest-scoring quadrant.
- **FAIL (`< 60.0`)**: Architectural layout or missing-layer failure; rebuild scene hierarchy before fine-tuning.
