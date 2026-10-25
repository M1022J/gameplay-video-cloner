# Pixel-Coordinate Layer Classification & Transparent Sprite Hard Rules (`yuzhworkhard-wq/image-to-code`)

Distilled from `yuzhworkhard-wq/image-to-code/blob/main/SKILL.md`.

## 1. Mandatory Layer Classification Table (图层分类表)
Before writing rendering code from a reference image, classify every visual element into one of two rendering routes:

- **Route A - Code-Rendered Primitives (Canvas 2D / CSS / Shaders)**:
  - Background gradients, grid lines, arena borders, HUD progress bars, pill badges, score/timer text, floating damage numbers, and particle bursts.
  - **Rule**: Never slice a whole screenshot as a static background image if it contains dynamic HUD numbers or moving entities.
- **Route B - Cropped Transparent PNG Sprites (`transparent_required: true`)**:
  - Character sprites, boss/enemy illustrations, custom item/fruit/weapon icons, and decorative badges cropped from the source frame.
  - **Hard Transparency Rule**: Every cropped sprite MUST have a true RGBA alpha channel with `corner_alpha_max == 0` (zero rectangular white, gray, or card-colored background boxes!).
  - **Mandatory Audit**: Run `python3 scripts/audit_png_assets.py ./assets/` after extracting or generating sprites. If any sprite fails (`transparent_bg_ok: false`), re-clean with `chroma_key_magenta.py` or `extract_sprites.py --remove-bg` or render crisp procedural vector/pixel art instead of pasting a rectangular patch!
