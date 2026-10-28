---
name: vlm-vision-ocr-skill
description: Standalone Multi-Provider VLM (Vision-Language Model: Qwen-VL, Gemini Vision, GPT-4o, Claude Vision, VLM Run Orion, or Host Native VLM) + Multi-Pass Game OCR + OmniParser Set-of-Mark (SoM) & 0..1000 Coordinate Auto-Labeling Skill. Use whenever the user asks to recognize images, screenshots, game UI/HUD, or video keyframes with a VLM vision model, combine VLM with OCR text/number extraction, infer game mechanics from screenshots, or auto-label bounding boxes (YOLO/COCO/Labelme/CSV).
allowed-tools: default_api google image_gen
---
# VLM Vision Model + Multi-Pass Game OCR + OmniParser SoM Skill (`vlm-vision-ocr-skill`)

Give any AI workflow **Dual-Engine Vision Recognition** combining **Vision-Language Models (VLM)** (`Qwen-VL`, `Gemini 2.5 Pro/Flash`, `GPT-4o`, `Claude 3.7 Sonnet`, `VLM Run Orion`, or **Host Agent Native VLM**) with **3-Pass Game/UI OCR (`pytesseract` + stroke-inversion)** and **OmniParser Set-of-Mark (`#01..#N`) `0..1000` Coordinate Grounding**.

## When to Use

- The user wants a **VLM vision model skill** (`vlm识图skill` / `vlm视觉模型skill`) to inspect screenshots, game frames, UI mockups, charts, or documents.
- The user wants **OCR + VLM working together** so small HUD numbers (`1,450/2,000`, `Lv.15`, `+15%`, `02:45`) are locked with pixel-exact OCR while artistic 3D/gradient titles and gameplay rules are interpreted by the VLM.
- The user wants **`0..1000` bounding-box / polygon object detection** exported to `YOLO`, `Labelme`, `COCO`, or `CSV`.

## Directory Structure (8 Core Files)

- `SKILL.md` - Complete instructions and 8-mode workflow
- `env/.env.example` - Multi-provider VLM gateway config (`VISION_MODEL=qwen-vl-max`, `VISION_MODEL_FALLBACKS`, `VISION_BASE_URL`)
- `scripts/vlm_vision_client.py` - Multi-provider VLM + OCR CLI with 8 built-in modes (`gameplay`, `ui`, `ocr`, `label`, `compare`, `table`, `json`, `batch`)
- `scripts/game_ocr_and_som_grounder.py` - OmniParser Set-of-Mark (`#01..#24`) + `0..1000` ruler + 3-pass game HUD OCR preprocessor & regex numeric parser
- `scripts/export_vlm_labels.py` - Canonical `0..1000` annotation exporter to `YOLO`, `YOLO-seg`, `Labelme`, `COCO`, and `CSV`
- `references/01-multi-provider-vlm-gateway-and-fallbacks.md`
- `references/02-omniparser-som-and-0-1000-bbox-grounding.md`
- `references/03-game-font-multipass-ocr-and-vlm-synergy.md`

## Core 3-Step Workflow

### Step 1: Run VLM + Multi-Pass Game OCR + Set-of-Mark Grounding

```bash
# Check active VLM model chain & OCR readiness
python3 skills/vlm-vision-ocr-skill/scripts/vlm_vision_client.py --check

# Mode A: Reverse-engineer Game UI, HUD numbers, and Core Gameplay Mechanics
python3 skills/vlm-vision-ocr-skill/scripts/vlm_vision_client.py <screenshot.png> --mode=gameplay --out-dir ./vlm_out

# Mode B: Pure OCR + VLM Artistic Font Cross-Verification
python3 skills/vlm-vision-ocr-skill/scripts/vlm_vision_client.py <screenshot.png> --mode=ocr --out-dir ./vlm_out

# Mode C: Auto-Label 0..1000 Bounding Boxes & Polygons
python3 skills/vlm-vision-ocr-skill/scripts/vlm_vision_client.py <screenshot.png> --mode=label --classes "hero,enemy,hp_bar,skill_btn,coin" --out-dir ./vlm_out
```

### Step 2: Inspect Grounded Visuals with Host Native VLM (`view_file`)

Always call `view_file` on the two generated visual grounding sheets in `./vlm_out/`:
1. `som_grounded_frame.png` - Original frame framed with a `0..1000` coordinate ruler and `#01..#24` Set-of-Mark bounding boxes labeled with pre-extracted OCR strings.
2. `som_element_atlas.png` - `2x` zoomed gallery of every detected `#ID` element with pixel coordinates `[x, y, w, h]`, median hex color, and `OCR: <text> (<conf>%)`.

### Step 3: Export Annotations (Optional — YOLO / Labelme / COCO / CSV)

```bash
python3 skills/vlm-vision-ocr-skill/scripts/export_vlm_labels.py --image <screenshot.png> --ann ./vlm_out/<stem>.raw.json --format yolo --out-dir ./vlm_out/labels
python3 skills/vlm-vision-ocr-skill/scripts/export_vlm_labels.py --image <screenshot.png> --ann ./vlm_out/<stem>.raw.json --format csv --out-dir ./vlm_out/labels
```
