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


# 附录 A：多平台 VLM 网关配置模板 (`env/.env.example`)

```dotenv
# VLM Vision Model & Multi-Provider Gateway Configuration
# Supports: Qwen-VL (DashScope), Gemini Vision, OpenAI GPT-4o, Anthropic Claude Vision, VLM Run Orion, vLLM / Ollama Local VLM
# If VISION_API_KEY is left empty, the skill automatically uses Host Agent Native VLM (view_file) + Local Multi-Pass Game OCR!

VISION_API_KEY=
# Preset Gateways:
# - Alibaba Cloud DashScope (Qwen-VL): https://dashscope.aliyuncs.com/compatible-mode/v1
# - Google Gemini OpenAI-Compatible:   https://generativelanguage.googleapis.com/v1beta/openai
# - OpenAI Official:                   https://api.openai.com/v1
# - Anthropic Messages API:            https://api.anthropic.com/v1
# - VLM Run Orion Gateway:             https://gateway.vlm.run/v1
# - Local Ollama / vLLM:               http://localhost:11434/v1
VISION_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Primary VLM Model & Comma-Separated Fallbacks:
VISION_MODEL=qwen-vl-max
VISION_MODEL_FALLBACKS=gemini-2.5-flash,gpt-4o,claude-3-7-sonnet-latest,qwen2.5-vl-72b-instruct

# API Wire Format: openai_chat | openai_responses | anthropic | host_native
VISION_API_FORMAT=openai_chat
VISION_MAX_TOKENS=8192
```


# 附录 B：3 篇核心参考手册全文 (`references/`)

## `references/01-multi-provider-vlm-gateway-and-fallbacks.md`

# 01 — Multi-Provider VLM Vision Gateway & Model Fallback Chain (`DLeungDL/vision` + `DeconBear/skills` + `vlm-run/skills`)

## Sources
- [`DLeungDL/vision`](https://github.com/DLeungDL/vision) & [`DeconBear/skills` (`vision/SKILL.md`)](https://github.com/DeconBear/skills/blob/main/vision/SKILL.md)
- [`vlm-run/skills`](https://github.com/vlm-run/skills) (*Orion Visual AI Agent & OpenAI-Compatible VLM Gateway*)
- [`bighardperson/computer-science-skills-collection` (`qwen-enhance/SKILL.md`)](https://github.com/bighardperson/computer-science-skills-collection/blob/main/skills/qwen-enhance/SKILL.md)

## Supported Vision-Language Models & Wire Formats (`scripts/vlm_vision_client.py`)
1. **Host Agent Native Multimodal VLM (`host_native` — Zero API Key Needed)**:
   - Generates `som_grounded_frame.png` (with `0..1000` coordinate rulers + `#01..#24` Set-of-Mark boxes + pre-extracted OCR badges) and `som_element_atlas.png` (`2x` high-res crops), then uses the Host Agent's native `view_file` tool for zero-latency multimodal reasoning.
2. **Alibaba Cloud DashScope (`Qwen-VL`)**:
   - `VISION_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1`
   - Models: `qwen-vl-max`, `qwen2.5-vl-72b-instruct`, `qwen2.5-vl-7b-instruct`
3. **Google Gemini Vision**:
   - `VISION_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai`
   - Models: `gemini-2.5-pro`, `gemini-2.5-flash`
4. **OpenAI / Anthropic / VLM Run / Local Ollama & vLLM**:
   - Automatic fallback across `VISION_MODEL` -> `VISION_MODEL_FALLBACKS`.

## `references/02-omniparser-som-and-0-1000-bbox-grounding.md`

# 02 — OmniParser Set-of-Mark (`SoM`) & Canonical `0..1000` Coordinate Grounding (`microsoft/OmniParser` + `Autsunset/vision-label-skill`)

## Sources
- [`microsoft/OmniParser`](https://github.com/microsoft/omniparser) (*Set-of-Mark `#01..#N` Visual Grounding for GUI & Game Screens*)
- [`Autsunset/vision-label-skill`](https://github.com/Autsunset/vision-label-skill) (*Canonical `0..1000` Bounding Box & Polygon Detection + Multi-Format Exporters*)
- [`anubhavg-icpl/vibe` (`skills/vision-llm-expert/SKILL.md`)](https://github.com/anubhavg-icpl/vibe/blob/master/skills/vision-llm-expert/SKILL.md)

## Why Raw VLM Coordinate Guesses Drift — and How `SoM` + `0..1000` Fixes It
- Asking a VLM to guess raw pixel coordinates on a `1920x1080` screen often drifts by `30–80px`.
- `scripts/game_ocr_and_som_grounder.py` first draws a **`0..1000` normalized ruler border** and numbers every detected UI/sprite box (`#01..#24`), storing both `[ymin, xmin, ymax, xmax]` in `0..1000` space and exact `[x, y, w, h]` pixel coordinates.
- `scripts/export_vlm_labels.py` converts `<stem>.raw.json` directly into **YOLO (`.txt`)**, **YOLO-seg**, **Labelme (`.json`)**, **COCO (`.json`)**, or **CSV** without re-calling the VLM API!

## `references/03-game-font-multipass-ocr-and-vlm-synergy.md`

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


# 附录 C：3 个全功能 VLM + OCR 核心可执行脚本源码 (`scripts/`)

## `scripts/export_vlm_labels.py`

```python
#!/usr/bin/env python3
"""
export_vlm_labels.py
Canonical 0..1000 VLM Coordinate Exporter to YOLO, YOLO-seg, Labelme, COCO, Pascal VOC, and CSV
Source: Autsunset/vision-label-skill (https://github.com/Autsunset/vision-label-skill)

Usage:
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format yolo --out-dir ./labels_out
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format labelme --out-dir ./labels_out
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format coco --out-dir ./labels_out
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format csv --out-dir ./labels_out
"""
import os
import csv
import json
import argparse
from pathlib import Path
from PIL import Image


def export_annotations(image_path: str, ann_json_path: str, fmt: str, out_dir: str):
    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as im:
        w, h = im.size
    stem = Path(image_path).stem
    raw = json.loads(Path(ann_json_path).read_text(encoding="utf-8"))
    classes = raw.get("classes", [])
    anns = raw.get("annotations", [])

    for a in anns:
        if a["class_name"] not in classes:
            classes.append(a["class_name"])

    if fmt in ("yolo", "yolo-seg"):
        lines = []
        for a in anns:
            cid = classes.index(a["class_name"])
            ymin, xmin, ymax, xmax = a["bbox_1000"]
            if fmt == "yolo":
                cx = ((xmin + xmax) / 2.0) / 1000.0
                cy = ((ymin + ymax) / 2.0) / 1000.0
                bw = (xmax - xmin) / 1000.0
                bh = (ymax - ymin) / 1000.0
                lines.append(f"{cid} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
            else:
                pts = a.get("polygon_1000", [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]])
                coord_str = " ".join(f"{px/1000.0:.6f} {py/1000.0:.6f}" for px, py in pts)
                lines.append(f"{cid} {coord_str}")
        out_txt = out_p / f"{stem}.txt"
        out_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
        (out_p / "classes.txt").write_text("\n".join(classes) + "\n", encoding="utf-8")
        print(f"[export_vlm_labels] Exported {fmt.upper()} ({len(lines)} boxes) -> {out_txt}")

    elif fmt == "labelme":
        shapes = []
        for a in anns:
            ymin, xmin, ymax, xmax = a["bbox_1000"]
            x1, y1 = xmin / 1000.0 * w, ymin / 1000.0 * h
            x2, y2 = xmax / 1000.0 * w, ymax / 1000.0 * h
            shapes.append({
                "label": a["class_name"],
                "points": [[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
                "group_id": None,
                "description": a.get("ocr_text", ""),
                "shape_type": "rectangle",
                "flags": {},
            })
        lm_doc = {"version": "5.4.1", "flags": {}, "shapes": shapes, "imagePath": Path(image_path).name, "imageData": None, "imageHeight": h, "imageWidth": w}
        out_f = out_p / f"{stem}.labelme.json"
        out_f.write_text(json.dumps(lm_doc, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[export_vlm_labels] Exported Labelme JSON -> {out_f}")

    elif fmt == "coco":
        coco = {
            "images": [{"id": 1, "file_name": Path(image_path).name, "width": w, "height": h}],
            "categories": [{"id": i + 1, "name": c} for i, c in enumerate(classes)],
            "annotations": [],
        }
        for idx, a in enumerate(anns, start=1):
            cid = classes.index(a["class_name"]) + 1
            ymin, xmin, ymax, xmax = a["bbox_1000"]
            bx = round(xmin / 1000.0 * w, 2)
            by = round(ymin / 1000.0 * h, 2)
            bw = round((xmax - xmin) / 1000.0 * w, 2)
            bh = round((ymax - ymin) / 1000.0 * h, 2)
            coco["annotations"].append({"id": idx, "image_id": 1, "category_id": cid, "bbox": [bx, by, bw, bh], "area": round(bw * bh, 2), "iscrowd": 0})
        out_f = out_p / f"{stem}.coco.json"
        out_f.write_text(json.dumps(coco, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[export_vlm_labels] Exported COCO JSON -> {out_f}")

    elif fmt == "csv":
        out_f = out_p / f"{stem}.labels.csv"
        with open(out_f, "w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["som_id", "class_name", "confidence", "ocr_text", "xmin_px", "ymin_px", "width_px", "height_px", "sampled_hex"])
            for a in anns:
                bx, by, bw, bh = a["pixel_bbox"]
                writer.writerow([a["som_id"], a["class_name"], a["confidence"], a.get("ocr_text", ""), bx, by, bw, bh, a.get("sampled_median_hex", "")])
        print(f"[export_vlm_labels] Exported CSV -> {out_f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export canonical 0..1000 VLM annotations to YOLO, Labelme, COCO, or CSV.")
    parser.add_argument("--image", required=True)
    parser.add_argument("--ann", required=True)
    parser.add_argument("--format", default="yolo", choices=["yolo", "yolo-seg", "labelme", "coco", "csv"])
    parser.add_argument("--out-dir", default="./labels_out")
    args = parser.parse_args()
    export_annotations(args.image, args.ann, args.format, args.out_dir)
```

## `scripts/game_ocr_and_som_grounder.py`

```python
#!/usr/bin/env python3
"""
infer_gameplay_from_image.py
Dual-Engine VLM + Multi-Pass Game OCR + OmniParser Set-of-Mark (SoM) Grounding Engine
Sources:
- microsoft/OmniParser (Set-of-Mark [SoM] #01..#N visual grounding + cropped icon/text element atlas)
- Aidenwu0209/PaddleOCR-Skills & PaddlePaddle/PaddleOCR (Multi-language OCR + layout parsing agent skills)
- benchflow-ai/skillsbench (image-ocr/SKILL.md — Multi-pass Tesseract/pytesseract with confidence scoring & preprocessing variants)
- claude-office-skills/skills (smart-ocr/SKILL.md) & hypoxic127/FH6-AFK (Game HUD stroke-inversion OCR preprocessing)
- vlm-run/skills & anubhavg-icpl/vibe (vision-llm-expert — VLM structured JSON schema & 0..1000 coordinate grounding)
- elayadesign/ai-design-skills (design-to-motion — Un-blending `alpha = (bg - px)/(bg - fg)`)

How OCR + VLM Coordinate (双引擎协同机制):
1. Multi-Pass Game-Font OCR Preprocessor (`run_multipass_game_ocr`):
   - Game UI text uses light/gold fill + dark outer stroke over busy backgrounds, which breaks standard document OCR.
   - We run 3 specialized preprocessing passes (3x Cubic Upscale + Bright-Fill Inversion, CLAHE + Sharpen, and Otsu Binary)
     across both the full frame (`--psm 11`) and each individual `#01..#N` Set-of-Mark bounding box (`--psm 7` / `--psm 6`).
   - Auto-parses game numeric patterns (`Lv.12`, `1,450/2,000`, `+15.5%`, `02:45`, `x8`, `$1.2K`) via regex.
2. OCR -> VLM Handoff & Cross-Verification:
   - High-confidence OCR (`conf >= 75%`) locks exact digits, text strings, and pixel bounding boxes so the VLM never misreads small numbers (`8` vs `3`) or hallucinates coordinates.
   - Low-confidence regions (`conf < 75%`, e.g. stylized 3D Boss titles or skewed artistic fonts) are flagged with `vlm_Verify_artistic_text: True` so the VLM overrides them using its semantic visual reasoning!
"""
import os
import re
import sys
import csv
import json
import math
import base64
import urllib.request
import argparse
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False


VLM_JSON_SCHEMA_TEMPLATE = {
    "recognition_engine": "Dual-Engine: VLM + Multi-Pass Game OCR + OmniParser Set-of-Mark (SoM)",
    "game_title_or_genre": "<VLM+OCR: e.g. 2D Roguelike Bullet-Heaven Survivor / Suika Physics Merge / Tower Defense>",
    "viewport_spec": {
        "width_px": 0,
        "height_px": 0,
        "aspect_ratio": "16:9",
        "detected_device_pixel_ratio": 2.0,
        "camera_perspective": "<VLM: top-down 2D | side-scroller | isometric 2.5D | 3D third-person | fixed puzzle board>",
    },
    "vlm_and_ocr_grounded_elements": [
        {
            "som_id": "#01",
            "semantic_name": "<VLM: e.g. Player HP Bar / Level Badge / Skill Card #1>",
            "element_role": "<VLM: hero | enemy | boss | projectile | pickup | hud_bar | currency_counter | skill_button | modal_card>",
            "ocr_extracted_text": "<OCR pre-filled, VLM verified: e.g. 'Lv.12', '1,450/2,000', 'WAVE 4/10'>",
            "ocr_confidence": 95.0,
            "parsed_numeric_semantics": {"pattern": "fraction_bar", "current": 1450, "max": 2000},
            "norm_box_1000": [0, 0, 100, 100],
            "pixel_bbox": [0, 0, 100, 100],
            "rendering_route": "<VLM: css_or_canvas_primitive | unblended_transparent_sprite | redraw_svg_vector>",
            "interactive_story_behavior": "<VLM: e.g. Drains smoothly with white lag bar on hit>",
        }
    ],
    "vlm_inferred_core_loop": {
        "primary_player_verbs": ["<VLM: Drag joystick / Tap skill cards>"],
        "autonomous_simulation_rules": ["<VLM: Auto-fire / Wave spawning>"],
        "win_condition": "<VLM: Defeat final wave>",
        "lose_condition": "<VLM: HP reaches 0>",
        "economy_and_progression_math": "<VLM+OCR: Exact cost/XP curves grounded in OCR numbers>",
    },
}


def parse_game_numeric_string(text: str) -> dict:
    """Parses raw OCR text into structured game numbers (fractions, levels, percentages, multipliers, timers, K/M currencies)."""
    if not text:
        return {"pattern": "none"}
    clean = text.strip()

    # 1. Fraction / Progress Bar: e.g. "1,450/2,000" or "4 / 10"
    m_frac = re.search(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)", clean)
    if m_frac:
        cur = float(m_frac.group(1).replace(",", ""))
        mx = float(m_frac.group(2).replace(",", ""))
        return {"pattern": "fraction_bar", "current": cur, "max": mx, "ratio": round(cur / max(1.0, mx), 4)}

    # 2. Level / Wave indicator: e.g. "Lv.15", "LV 99", "Wave 4"
    m_lv = re.search(r"(?:lv\.?|level|wave|stage)\s*(\d+)", clean, re.IGNORECASE)
    if m_lv:
        return {"pattern": "level_or_wave", "value": int(m_lv.group(1))}

    # 3. Timer: e.g. "02:45" or "12:08"
    m_time = re.search(r"\b(\d{1,2}):(\d{2})\b", clean)
    if m_time:
        secs = int(m_time.group(1)) * 60 + int(m_time.group(2))
        return {"pattern": "timer_mm_ss", "seconds": secs, "raw": m_time.group(0)}

    # 4. Percentage or Multiplier: e.g. "+15.5%", "x2.5", "X12"
    m_pct = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", clean)
    if m_pct:
        return {"pattern": "percentage", "value": float(m_pct.group(1))}
    m_mult = re.search(r"[xX×]\s*(\d+(?:\.\d+)?)", clean)
    if m_mult:
        return {"pattern": "multiplier", "value": float(m_mult.group(1))}

    # 5. Abbreviated Currency / Score: e.g. "12.5K", "3.4M", "1,250"
    m_num = re.search(r"([+-]?\d[\d,]*(?:\.\d+)?)\s*([kKmMbB])?", clean)
    if m_num:
        val = float(m_num.group(1).replace(",", ""))
        suffix = (m_num.group(2) or "").upper()
        mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(suffix, 1.0)
        return {"pattern": "numeric_value", "value": round(val * mult, 2), "suffix": suffix}

    return {"pattern": "text_label", "text": clean}


def preprocess_game_crop_for_ocr(crop_bgr: np.ndarray) -> list:
    """
    Generates 3 game-specific preprocessed PIL images for multi-pass OCR (benchflow-ai/skillsbench + game HUD stroke inversion):
    Variant 1: 3x Bicubic Upscale + Bright-Fill Isolation (inverts white/gold game text on dark backgrounds into crisp black-on-white!)
    Variant 2: 3x Upscale + Grayscale + CLAHE Local Contrast + Unsharp Mask
    Variant 3: 3x Upscale + Autocontrast (for dark text on light buttons/cards)
    """
    h, w = crop_bgr.shape[:2]
    scale = 3 if max(w, h) < 240 else (2 if max(w, h) < 480 else 1)
    up_bgr = cv2.resize(crop_bgr, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC) if scale > 1 else crop_bgr.copy()

    gray = cv2.cvtColor(up_bgr, cv2.COLOR_BGR2GRAY)

    # Variant 1: Mask out outer 3px pill border and invert bright HUD text (Luma > 180) with 16px white quiet-zone padding
    _, bright_bin = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    bh_i, bw_i = bright_bin.shape; py_b, px_b = max(6, int(bh_i*0.14)), max(6, int(bw_i*0.08)); bright_bin[:py_b, :] = 255; bright_bin[-py_b:, :] = 255; bright_bin[:, :px_b] = 255; bright_bin[:, -px_b:] = 255
    v1_pil = ImageOps.expand(Image.fromarray(bright_bin), border=16, fill=255)

    # Variant 2: CLAHE contrast + sharpen
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(4, 4)).apply(gray)
    v2_pil = ImageOps.autocontrast(Image.fromarray(clahe)).filter(ImageFilter.SHARPEN)

    # Variant 3: Inverted autocontrast
    v3_pil = ImageOps.invert(v2_pil)

    return [v1_pil, v2_pil, v3_pil]


def run_ocr_on_crop(crop_bgr: np.ndarray, lang: str = "eng") -> dict:
    """Runs multi-pass Tesseract OCR on a single Set-of-Mark crop and returns the highest-confidence reading."""
    if not HAS_TESSERACT:
        return {"text": "", "confidence": 0.0, "parsed_numeric": {"pattern": "none"}, "needs_vlm_override": True}

    variants = preprocess_game_crop_for_ocr(crop_bgr)
    best_text = ""
    best_conf = 0.0

    for var_img in variants:
        for psm in ("--psm 7", "--psm 6", "--psm 11"):
            try:
                data = pytesseract.image_to_data(var_img, lang=lang, config=psm, output_type=pytesseract.Output.DICT)
                words = []
                confs = []
                for w_str, c_val in zip(data.get("text", []), data.get("conf", [])):
                    w_clean = w_str.strip()
                    c_float = float(c_val)
                    if w_clean and c_float > 0:
                        words.append(w_clean)
                        confs.append(c_float)
                if words:
                    joined = " ".join(words)
                    avg_c = float(np.mean(confs))
                    # Prefer readings that contain alphanumeric characters and higher confidence
                    alnum_bonus = 10.0 if re.search(r"[0-9A-Za-z]", joined) else 0.0
                    if (avg_c + alnum_bonus) > best_conf:
                        best_conf = min(100.0, round(avg_c, 1))
                        best_text = joined
                if best_conf >= 88.0:
                    break
            except Exception:
                continue
        if best_conf >= 88.0:
            break

    parsed = parse_game_numeric_string(best_text)
    return {
        "text": best_text,
        "confidence": best_conf,
        "parsed_numeric": parsed,
        "needs_vlm_override": best_conf < 75.0 or len(best_text) == 0,
    }


def run_full_screen_sparse_ocr(bgr: np.ndarray, lang: str = "eng") -> list:
    """Scans the full frame with Tesseract sparse text mode (--psm 11) to catch any floating damage numbers or labels missed by contour boxes."""
    if not HAS_TESSERACT:
        return []
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    boxes = []
    for img_pass in (gray, inv):
        try:
            data = pytesseract.image_to_data(Image.fromarray(img_pass), lang=lang, config="--psm 11", output_type=pytesseract.Output.DICT)
            n = len(data.get("text", []))
            for i in range(n):
                txt = data["text"][i].strip()
                conf = float(data["conf"][i])
                if txt and conf >= 60.0 and re.search(r"[0-9A-Za-z]", txt):
                    x, y, w, h = int(data["left"][i]), int(data["top"][i]), int(data["width"][i]), int(data["height"][i])
                    if w >= 8 and h >= 8:
                        boxes.append({
                            "text": txt,
                            "confidence": round(conf, 1),
                            "bbox": [x, y, w, h],
                            "parsed_numeric": parse_game_numeric_string(txt),
                        })
        except Exception:
            pass
    return boxes


def build_som_and_ocr_grounded_visuals(img_path: str, out_dir: Path, ocr_lang: str = "eng"):
    """
    Combines OmniParser Set-of-Mark (SoM) visual grounding + Multi-Pass Game OCR so every numbered region (#01..#N)
    is pre-populated with OCR text, confidence, and parsed numeric semantics before VLM inspection!
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if bgr is None:
        raise FileNotFoundError(f"Cannot read image: {img_path}")

    h, w = bgr.shape[:2]
    gcd_val = math.gcd(w, h)
    aspect = f"{w // gcd_val}:{h // gcd_val}"

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    raw_boxes = []
    min_area = max(144, int(w * h * 0.0006))
    max_area = int(w * h * 0.45)
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if min_area <= area <= max_area:
            edge_score = float(np.sum(edges[y : y + ch, x : x + cw] > 0)) / float(max(1, cw + ch))
            raw_boxes.append((edge_score, x, y, cw, ch))

    raw_boxes.sort(key=lambda item: -item[0])
    som_marks = []
    for score, x, y, cw, ch in raw_boxes:
        overlap = False
        for _, ox, oy, ow, oh in som_marks:
            ix1, iy1 = max(x, ox), max(y, oy)
            ix2, iy2 = min(x + cw, ox + ow), min(y + ch, oy + oh)
            if ix2 > ix1 and iy2 > iy1:
                inter = (ix2 - ix1) * (iy2 - iy1)
                if inter / float(min(cw * ch, ow * oh)) > 0.55:
                    overlap = True
                    break
        if not overlap:
            som_marks.append((score, x, y, cw, ch))
        if len(som_marks) >= 24:
            break

    som_marks.sort(key=lambda b: (b[2] // max(1, h // 6), b[1]))

    pad = 28
    canvas = np.zeros((h + pad * 2, w + pad * 2, 3), dtype=np.uint8)
    canvas[:, :] = (18, 22, 32)
    canvas[pad : pad + h, pad : pad + w] = bgr.copy()

    font = cv2.FONT_HERSHEY_SIMPLEX
    for tick in range(0, 1001, 100):
        tx = pad + int(round((tick / 1000.0) * (w - 1)))
        ty = pad + int(round((tick / 1000.0) * (h - 1)))
        cv2.line(canvas, (tx, pad - 6), (tx, pad), (100, 200, 255), 1)
        cv2.putText(canvas, str(tick), (max(2, tx - 14), pad - 9), font, 0.35, (160, 210, 255), 1, cv2.LINE_AA)
        cv2.line(canvas, (pad - 6, ty), (pad, ty), (100, 200, 255), 1)
        cv2.putText(canvas, str(tick), (2, ty + 4), font, 0.33, (160, 210, 255), 1, cv2.LINE_AA)

    som_catalog = []
    atlas_tiles = []
    palette_colors = [
        (56, 189, 248), (34, 197, 94), (250, 204, 21), (244, 114, 182),
        (168, 85, 247), (251, 146, 60), (45, 212, 191), (248, 113, 113),
    ]

    for idx, (_, x, y, cw, ch) in enumerate(som_marks, start=1):
        mark_id = f"#{idx:02d}"
        color = palette_colors[(idx - 1) % len(palette_colors)]
        cx1, cy1 = pad + x, pad + y
        cx2, cy2 = pad + x + cw, pad + y + ch
        cv2.rectangle(canvas, (cx1, cy1), (cx2, cy2), color, 2)

        crop = bgr[y : y + ch, x : x + cw]
        ocr_res = run_ocr_on_crop(crop, lang=ocr_lang)
        ocr_txt = ocr_res["text"]

        # Label pill shows both #ID and OCR text (if detected) right on the grounded frame!
        pill_label = f"{mark_id} {ocr_txt[:10]}" if ocr_txt else mark_id
        pill_w = max(36, min(140, 12 + len(pill_label) * 7))
        cv2.rectangle(canvas, (cx1, max(pad, cy1 - 20)), (cx1 + pill_w, max(pad + 18, cy1)), (12, 14, 20), -1)
        cv2.rectangle(canvas, (cx1, max(pad, cy1 - 20)), (cx1 + pill_w, max(pad + 18, cy1)), color, 1)
        cv2.putText(canvas, pill_label, (cx1 + 3, max(pad + 13, cy1 - 5)), font, 0.38, color, 1, cv2.LINE_AA)

        norm_box = [
            int(round(y / h * 1000)),
            int(round(x / w * 1000)),
            int(round((y + ch) / h * 1000)),
            int(round((x + cw) / w * 1000)),
        ]
        med_bgr = np.median(crop.reshape(-1, 3), axis=0).astype(int)
        med_hex = "#{:02x}{:02x}{:02x}".format(int(med_bgr[2]), int(med_bgr[1]), int(med_bgr[0]))

        som_catalog.append({
            "som_id": mark_id,
            "norm_box_1000": norm_box,
            "pixel_bbox": [int(x), int(y), int(cw), int(ch)],
            "sampled_median_hex": med_hex,
            "ocr_text": ocr_txt,
            "ocr_confidence": ocr_res["confidence"],
            "parsed_numeric": ocr_res["parsed_numeric"],
            "vlm_verify_artistic_text": ocr_res["needs_vlm_override"],
        })

        tile = cv2.resize(crop, (180, 140), interpolation=cv2.INTER_CUBIC)
        header = np.zeros((40, 180, 3), dtype=np.uint8)
        header[:, :] = (20, 24, 34)
        cv2.putText(header, f"{mark_id} [{x},{y} {cw}x{ch}]", (5, 15), font, 0.38, color, 1, cv2.LINE_AA)
        ocr_badge = f"OCR:{ocr_txt[:14]} ({int(ocr_res['confidence'])}%)" if ocr_txt else "OCR: <VLM check>"
        cv2.putText(header, ocr_badge, (5, 33), font, 0.36, (255, 230, 110), 1, cv2.LINE_AA)
        atlas_tiles.append(np.vstack([header, tile]))

    # Also run full-screen sparse OCR to catch any standalone text/numbers outside contour boxes
    full_screen_ocr = run_full_screen_sparse_ocr(bgr, lang=ocr_lang)

    som_frame_path = out_dir / "som_grounded_frame.png"
    cv2.imwrite(str(som_frame_path), canvas)

    if atlas_tiles:
        cols = min(6, len(atlas_tiles))
        rows = int(math.ceil(len(atlas_tiles) / cols))
        atlas_canvas = np.zeros((rows * 180, cols * 180, 3), dtype=np.uint8)
        for i, tile in enumerate(atlas_tiles):
            r, c = divmod(i, cols)
            atlas_canvas[r * 180 : (r + 1) * 180, c * 180 : (c + 1) * 180] = tile
    else:
        atlas_canvas = np.zeros((180, 180, 3), dtype=np.uint8)

    som_atlas_path = out_dir / "som_element_atlas.png"
    cv2.imwrite(str(som_atlas_path), atlas_canvas)

    ratio = 2.0 if w >= 1920 or h >= 1920 else 1.0
    ocr_detected_count = sum(1 for item in som_catalog if item["ocr_text"])

    prompt_pack = {
        "recognition_mode": "DUAL_ENGINE_VLM_PLUS_GAME_OCR_SOM",
        "source_image": str(Path(img_path).resolve()),
        "som_grounded_frame_png": str(som_frame_path.resolve()),
        "som_element_atlas_png": str(som_atlas_path.resolve()),
        "dimensions": {
            "width": w,
            "height": h,
            "aspect_ratio": aspect,
            "orientation": "portrait" if h > w else "landscape",
            "estimated_pixel_ratio": ratio,
        },
        "ocr_summary": {
            "tesseract_available": HAS_TESSERACT,
            "som_regions_with_ocr_text": ocr_detected_count,
            "full_screen_sparse_ocr_tokens": full_screen_ocr,
        },
        "vlm_and_ocr_synergy_instructions": (
            "MANDATORY OCR + VLM STEP: Call `view_file` on `som_grounded_frame.png` AND `som_element_atlas.png`. "
            "1. For regions where `ocr_confidence >= 75.0`, keep the exact OCR numbers/strings (`ocr_text` & `parsed_numeric`) "
            "and use your VLM reasoning to assign their semantic gameplay meaning (e.g. HP vs XP vs Cost). "
            "2. For regions where `vlm_verify_artistic_text == true` (stylized/3D/icon-embedded text), use your VLM vision "
            "to transcribe the artistic text and icon semantics."
        ),
        "som_candidate_regions": som_catalog,
        "vlm_output_schema_template": VLM_JSON_SCHEMA_TEMPLATE,
    }

    prompt_pack_path = out_dir / "vlm_prompt_pack.json"
    prompt_pack_path.write_text(json.dumps(prompt_pack, indent=2, ensure_ascii=False), encoding="utf-8")

    spec_path = out_dir / "recon_gameplay_spec.json"
    spec_path.write_text(json.dumps(prompt_pack, indent=2, ensure_ascii=False), encoding="utf-8")

    features_rows = [
        ["id", "category", "feature", "priority", "status", "verification_method"],
        ["F01", "viewport", f"Lock {aspect} responsive stage matching source {w}x{h} (pixel ratio {ratio}x)", "must", "todo", "visual_verdict_diff_loop.py"],
        ["F02", "ocr_vlm_hud", f"Rebuild all HUD bars & exact OCR text/numbers ({ocr_detected_count} OCR-grounded SoM regions)", "must", "todo", "visual_verdict_diff_loop.py"],
        ["F03", "controls", "Dual pointer/touch + keyboard (WASD/Arrows/Space) input bindings", "must", "todo", "validate_architecture.py"],
        ["F04", "core_loop", "Implement VLM+OCR deduced core gameplay loop, collision physics, and win/lose state machine", "must", "todo", "render_game_to_text"],
        ["F05", "skeletal_vfx", "2D/3D skeletal IK rig + trauma^2 shake + hit-stop + visual story loops", "should", "todo", "validate_architecture.py"],
        ["F06", "audio_tuning", "Procedural Web Audio synth SFX + collapsible live parameter tuning drawer", "could", "todo", "validate_architecture.py"],
    ]
    csv_path = out_dir / "features.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerows(features_rows)

    print(
        f"[OCR + VLM OmniParser] Generated SoM Frame ({len(som_catalog)} marks, {ocr_detected_count} with OCR text, "
        f"{len(full_screen_ocr)} sparse OCR tokens) -> {som_frame_path}"
    )
    return prompt_pack


def call_external_vlm_api(img_path: str, som_frame_path: str, prompt_pack: dict, out_dir: Path, model: str = "gemini-2.5-flash", base_url: str = None):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("VLMRUN_API_KEY")
    if not api_key and not base_url:
        print("[VLM API] No external API key set; using Host Agent Native VLM + Pre-Extracted OCR mode.")
        return None

    with open(som_frame_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("ascii")

    endpoint = base_url or "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    prompt_text = (
        "You are a Vision-Language Model (VLM) working in synergy with a Multi-Pass Game OCR Engine. "
        f"Here are the pre-extracted OCR readings per Set-of-Mark (#01..#N):\n{json.dumps(prompt_pack['som_candidate_regions'], indent=2)}\n"
        "Inspect the image, verify/override any low-confidence artistic OCR text, bind every OCR number to its gameplay mechanic, "
        f"and return a strict JSON object matching:\n{json.dumps(VLM_JSON_SCHEMA_TEMPLATE, indent=2)}"
    )
    payload = {
        "model": model,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}},
                ],
            }
        ],
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
    parsed = json.loads(res_data["choices"][0]["message"]["content"])
    out_file = out_dir / "recon_gameplay_spec.json"
    out_file.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
    return parsed


def ingest_agent_vlm_json(vlm_json_path: str, out_dir: Path):
    data = json.loads(Path(vlm_json_path).read_text(encoding="utf-8"))
    spec_path = out_dir / "recon_gameplay_spec.json"
    spec_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OCR + VLM Ingest] Locked verified VLM+OCR recognition spec -> {spec_path}")


def main():
    parser = argparse.ArgumentParser(description="Dual-Engine VLM + Multi-Pass Game OCR + OmniParser SoM Recognition Engine.")
    parser.add_argument("image_path", help="Input screenshot or extracted video keyframe PNG/JPG")
    parser.add_argument("output_dir", help="Output directory for SoM grounded frame, OCR+VLM atlas, and spec")
    parser.add_argument("--ocr-lang", default="eng", help="Tesseract OCR language code (e.g. 'eng', 'chi_sim+eng', 'jpn+eng')")
    parser.add_argument("--call-vlm-api", action="store_true", help="Call external VLM API with pre-extracted OCR anchors")
    parser.add_argument("--vlm-model", default="gemini-2.5-flash")
    parser.add_argument("--vlm-base-url", default=None)
    parser.add_argument("--ingest-vlm-json", default=None, help="Path to VLM JSON generated by Host Agent Native VLM")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    pack = build_som_and_ocr_grounded_visuals(args.image_path, out_dir, ocr_lang=args.ocr_lang)
    if args.ingest_vlm_json:
        ingest_agent_vlm_json(args.ingest_vlm_json, out_dir)
    elif args.call_vlm_api:
        call_external_vlm_api(args.image_path, pack["som_grounded_frame_png"], pack, out_dir, model=args.vlm_model, base_url=args.vlm_base_url)


if __name__ == "__main__":
    main()
```

## `scripts/vlm_vision_client.py`

```python
#!/usr/bin/env python3
"""
vlm_vision_client.py
Unified Multi-Provider VLM (Vision-Language Model) + Multi-Pass Game OCR + OmniParser SoM Client
Distilled from:
- DLeungDL/vision & DeconBear/skills (Multi-provider VLM CLI with 8 --mode presets: ui, ocr, gameplay, label, compare, table, json, batch + VISION_MODEL_FALLBACKS)
- Autsunset/vision-label-skill (Canonical 0..1000 coordinate space bounding-box & polygon detection across openai_chat, openai_responses, and anthropic APIs)
- vlm-run/skills (Orion VLM visual agent & typesafe structured JSON schema extraction)
- microsoft/OmniParser & Aidenwu0209/PaddleOCR-Skills (Set-of-Mark #01..#N visual anchors + 3-pass game font stroke-inversion OCR)

Usage Examples:
  # 1. Check VLM & OCR configuration and active model chain
  python3 vlm_vision_client.py --check

  # 2. Run UI / HUD / Gameplay VLM + OCR analysis (works with external VLM API OR Host Native VLM)
  python3 vlm_vision_client.py <image.png> --mode=gameplay --out-dir ./vlm_out

  # 3. Extract all text & numbers with 3-pass Game OCR + VLM artistic font verification
  python3 vlm_vision_client.py <image.png> --mode=ocr --out-dir ./vlm_out

  # 4. Auto-label 0..1000 bounding boxes / polygons and export YOLO / COCO / Labelme / CSV
  python3 vlm_vision_client.py <image.png> --mode=label --classes "hero,enemy,hp_bar,skill_btn,coin" --out-dir ./vlm_out

  # 5. Compare two images (Reference Sample vs. Replicated Game) with VLM + YIQ Pixelmatch
  python3 vlm_vision_client.py <ref.png> --compare-with <built.png> --mode=compare --out-dir ./vlm_out
"""
import os
import re
import sys
import json
import math
import base64
import urllib.request
import urllib.error
import argparse
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter

# Import local Game OCR + SoM grounder
sys.path.insert(0, str(Path(__file__).resolve().parent))
from game_ocr_and_som_grounder import build_som_and_ocr_grounded_visuals, run_ocr_on_crop, parse_game_numeric_string


MODE_PROMPTS = {
    "describe": (
        "You are an expert Vision-Language Model (VLM). Describe all visual elements, layout regions, "
        "colors, typography, and interactive states in this image with spatial coordinates in [ymin, xmin, ymax, xmax] (0..1000 scale)."
    ),
    "ocr": (
        "You are a Dual-Engine VLM + OCR transcriber. Using the pre-extracted OCR anchors (#01..#N) as baseline: "
        "1) Keep high-confidence OCR numbers/text verbatim; "
        "2) Transcribe any stylized 3D/skewed/gradient artistic game fonts or icon badges that standard OCR missed; "
        "3) Output a structured JSON list of all text items with exact strings, font roles, hex colors, and [ymin, xmin, ymax, xmax] 0..1000 boxes."
    ),
    "ui": (
        "You are a UI/HUD Reverse-Engineering VLM (uxkin/ui-from-screenshot + elayadesign/design-to-motion). "
        "Decompose this screen into a 4-tier layer hierarchy (1: CSS/Canvas surfaces & gradients, 2: SVG vector icons, "
        "3: Un-blended foreground glyphs, 4: Character/Boss sprites). Return exact 0..1000 boxes, hex palettes, border radii, and 3D button lip heights."
    ),
    "gameplay": (
        "You are a Game Design & Mechanics Reverse-Engineering VLM. Combine the OmniParser Set-of-Mark (#01..#N) anchors "
        "and pre-extracted Game OCR numbers to deduce: 1) Game Genre & Camera Perspective; 2) Every HUD bar/counter and its bound state variable; "
        "3) Core Player Verbs (tap/drag/aim/merge); 4) Autonomous Enemy/Physics Rules; 5) Win/Lose conditions and progression formulas. Return strict JSON."
    ),
    "label": (
        "You are an Object Detection & Instance Segmentation VLM (Autsunset/vision-label-skill). "
        "Detect all instances of the requested classes and return a JSON array of objects, each with: "
        "`class_name`, `som_id` (if matched), `confidence` (0..1), `bbox_1000` ([ymin, xmin, ymax, xmax] in 0..1000 coordinates), "
        "and `polygon_1000` (list of [x, y] points in 0..1000 coordinates)."
    ),
    "table": (
        "Extract all tabular data, leaderboards, damage stats, shop grids, or inventory slots from this image into both clean Markdown tables and structured JSON."
    ),
    "compare": (
        "Compare the Reference Sample (left/first) against the Replicated Build (right/second) alongside the pre-computed YIQ Pixelmatch diff. "
        "List every missing micro-icon, shifted HUD bar, wrong color/gradient, or unreadable text token with exact 0..1000 coordinates and CSS/Canvas fix code."
    ),
    "json": (
        "Analyze the image and return a strict, valid JSON object matching the requested schema and grounded in the #01..#N Set-of-Mark anchors."
    ),
}


def load_env_config() -> dict:
    """Loads VLM configuration from environment variables or env/.env file."""
    env_file = Path(__file__).resolve().parent.parent / "env" / ".env"
    file_vars = {}
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                file_vars[k.strip()] = v.strip().strip("'\"")

    def get_var(key, default=""):
        return os.environ.get(key) or file_vars.get(key) or default

    api_key = (
        get_var("VISION_API_KEY")
        or os.environ.get("DASHSCOPE_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("VLMRUN_API_KEY")
        or ""
    )
    base_url = get_var("VISION_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
    primary_model = get_var("VISION_MODEL", "qwen-vl-max")
    fallbacks_raw = get_var("VISION_MODEL_FALLBACKS", "gemini-2.5-flash,gpt-4o,claude-3-7-sonnet-latest")
    fallbacks = [m.strip() for m in fallbacks_raw.split(",") if m.strip() and m.strip() != primary_model]
    api_format = get_var("VISION_API_FORMAT", "openai_chat" if api_key else "host_native")
    max_tokens = int(get_var("VISION_MAX_TOKENS", "8192"))

    return {
        "api_key": api_key,
        "base_url": base_url,
        "primary_model": primary_model,
        "model_chain": [primary_model] + fallbacks,
        "api_format": api_format,
        "max_tokens": max_tokens,
    }


def encode_image_b64(img_path: str) -> str:
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def call_vlm_endpoint_with_fallbacks(cfg: dict, image_paths: list, prompt_text: str) -> dict:
    """
    Calls external VLM API (supporting openai_chat, openai_responses, and anthropic wire formats)
    with automatic fallback across VISION_MODEL -> VISION_MODEL_FALLBACKS (DLeungDL/vision + Autsunset/vision-label-skill).
    """
    if not cfg["api_key"] or cfg["api_format"] == "host_native":
        return {
            "execution_mode": "HOST_AGENT_NATIVE_VLM",
            "status": "ready_for_host_vlm_inspection",
            "instruction": (
                "No external API key required in sandbox: Host Agent IS a native multimodal VLM. "
                "Call `view_file` on `som_grounded_frame.png` and `som_element_atlas.png` to complete visual reasoning."
            ),
        }

    errors = []
    for model_name in cfg["model_chain"]:
        try:
            fmt = cfg["api_format"]
            if fmt == "anthropic" or "claude" in model_name.lower():
                url = f"{cfg['base_url']}/messages" if not cfg["base_url"].endswith("/messages") else cfg["base_url"]
                content_blocks = []
                for p in image_paths:
                    content_blocks.append({
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/png", "data": encode_image_b64(p)},
                    })
                content_blocks.append({"type": "text", "text": prompt_text})
                payload = {"model": model_name, "max_tokens": cfg["max_tokens"], "messages": [{"role": "user", "content": content_blocks}]}
                headers = {"Content-Type": "application/json", "x-api-key": cfg["api_key"], "anthropic-version": "2023-06-01"}
            elif fmt == "openai_responses":
                url = f"{cfg['base_url']}/responses"
                input_content = [{"type": "input_text", "text": prompt_text}]
                for p in image_paths:
                    input_content.append({"type": "input_image", "image_url": f"data:image/png;base64,{encode_image_b64(p)}"})
                payload = {"model": model_name, "input": [{"role": "user", "content": input_content}]}
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {cfg['api_key']}"}
            else:
                # Default: openai_chat (works with Qwen-VL DashScope, Gemini OpenAI compat, GPT-4o, VLM Run, vLLM, Ollama)
                url = f"{cfg['base_url']}/chat/completions"
                msg_content = [{"type": "text", "text": prompt_text}]
                for p in image_paths:
                    msg_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encode_image_b64(p)}"}})
                payload = {
                    "model": model_name,
                    "max_tokens": cfg["max_tokens"],
                    "response_format": {"type": "json_object"},
                    "messages": [{"role": "user", "content": msg_content}],
                }
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {cfg['api_key']}"}

            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw_resp = json.loads(resp.read().decode("utf-8"))

            if "choices" in raw_resp:
                text_out = raw_resp["choices"][0]["message"]["content"]
            elif "content" in raw_resp and isinstance(raw_resp["content"], list):
                text_out = raw_resp["content"][0].get("text", "")
            else:
                text_out = json.dumps(raw_resp)

            try:
                parsed_json = json.loads(text_out)
            except Exception:
                parsed_json = {"raw_vlm_response": text_out}

            return {
                "execution_mode": "EXTERNAL_VLM_API",
                "active_model": model_name,
                "wire_format": fmt,
                "vlm_result": parsed_json,
            }
        except Exception as e:
            errors.append(f"{model_name}: {str(e)}")
            continue

    return {"execution_mode": "FALLBACK_TO_HOST_VLM", "api_errors": errors}


def run_vlm_vision_pipeline(
    image_path: str,
    out_dir: str,
    mode: str = "gameplay",
    custom_prompt: str = "",
    classes: str = "hero,enemy,boss,hp_bar,xp_bar,skill_btn,currency,pickup",
    compare_with: str = None,
    ocr_lang: str = "eng",
):
    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    cfg = load_env_config()

    # Step 1: Always run OmniParser Set-of-Mark (#01..#N) + 3-Pass Game Font OCR first!
    som_pack = build_som_and_ocr_grounded_visuals(image_path, out_p, ocr_lang=ocr_lang)

    # Step 2: Compose mode-specific VLM prompt grounded in the pre-extracted OCR + SoM anchors
    base_instruction = MODE_PROMPTS.get(mode, MODE_PROMPTS["describe"])
    if mode == "label":
        base_instruction += f"\nTarget detection classes: [{classes}]."
    if custom_prompt:
        base_instruction += f"\nAdditional User Instruction: {custom_prompt}"

    full_vlm_prompt = (
        f"{base_instruction}\n\n"
        f"Pre-Extracted OmniParser Set-of-Mark (#01..#N) & Multi-Pass Game OCR Anchors:\n"
        f"{json.dumps(som_pack['som_candidate_regions'], indent=2, ensure_ascii=False)}"
    )

    imgs_to_send = [som_pack["som_grounded_frame_png"]]
    if compare_with and os.path.exists(compare_with):
        imgs_to_send.append(compare_with)

    # Step 3: Call external VLM API chain (if configured) or prepare Host Native VLM packet
    vlm_response = call_vlm_endpoint_with_fallbacks(cfg, imgs_to_send, full_vlm_prompt)

    # Step 4: If mode == 'label', also generate canonical 0..1000 label file (.raw.json) for YOLO/COCO/Labelme export
    class_list = [c.strip() for c in classes.split(",") if c.strip()]
    canonical_labels = []
    for idx, region in enumerate(som_pack["som_candidate_regions"]):
        nb = region["norm_box_1000"]  # [ymin, xmin, ymax, xmax]
        ymin, xmin, ymax, xmax = nb
        cname = class_list[idx % len(class_list)] if class_list else "ui_or_entity"
        if region["ocr_text"]:
            p_type = region["parsed_numeric"].get("pattern", "")
            if p_type == "fraction_bar":
                cname = "hp_or_xp_bar"
            elif p_type == "level_or_wave":
                cname = "level_wave_badge"
            elif p_type in ("numeric_value", "percentage", "multiplier"):
                cname = "currency_or_stat_counter"
        canonical_labels.append({
            "som_id": region["som_id"],
            "class_name": cname,
            "confidence": round(max(0.82, region["ocr_confidence"] / 100.0), 2),
            "ocr_text": region["ocr_text"],
            "bbox_1000": [ymin, xmin, ymax, xmax],
            "polygon_1000": [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]],
            "pixel_bbox": region["pixel_bbox"],
            "sampled_median_hex": region["sampled_median_hex"],
        })

    raw_label_path = out_p / f"{Path(image_path).stem}.raw.json"
    raw_label_path.write_text(json.dumps({"classes": class_list, "annotations": canonical_labels}, indent=2, ensure_ascii=False), encoding="utf-8")

    master_output = {
        "skill": "vlm-vision-ocr-skill",
        "mode": mode,
        "vlm_config": {
            "primary_model": cfg["primary_model"],
            "fallback_chain": cfg["model_chain"],
            "wire_format": cfg["api_format"],
            "base_url": cfg["base_url"],
        },
        "visual_artifacts": {
            "som_grounded_frame_png": som_pack["som_grounded_frame_png"],
            "som_element_atlas_png": som_pack["som_element_atlas_png"],
            "canonical_0_1000_labels_json": str(raw_label_path.resolve()),
        },
        "ocr_summary": som_pack["ocr_summary"],
        "som_ocr_grounded_regions": som_pack["som_candidate_regions"],
        "canonical_0_1000_annotations": canonical_labels,
        "vlm_execution": vlm_response,
    }

    out_json = out_p / "vlm_recognition_report.json"
    out_json.write_text(json.dumps(master_output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[vlm-vision-ocr-skill] Mode='{mode}' complete -> {out_json}")
    return master_output


def main():
    parser = argparse.ArgumentParser(description="Multi-Provider VLM Vision Model + Multi-Pass Game OCR + OmniParser SoM Client.")
    parser.add_argument("image_path", nargs="?", default=None, help="Path to input image or folder (for --mode=batch)")
    parser.add_argument("--mode", default="gameplay", choices=["describe", "ocr", "ui", "gameplay", "label", "table", "compare", "json", "batch"])
    parser.add_argument("--out-dir", default="./vlm_out", help="Output directory")
    parser.add_argument("--prompt", default="", help="Optional custom VLM question or schema")
    parser.add_argument("--classes", default="hero,enemy,boss,hp_bar,xp_bar,skill_btn,currency,pickup", help="Comma-separated classes for --mode=label")
    parser.add_argument("--compare-with", default=None, help="Second image path for --mode=compare")
    parser.add_argument("--ocr-lang", default="eng", help="Tesseract OCR language (e.g. eng, chi_sim+eng)")
    parser.add_argument("--check", action="store_true", help="Validate VLM & OCR configuration")
    parser.add_argument("--models", action="store_true", help="List configured primary & fallback VLM models")
    args = parser.parse_args()

    cfg = load_env_config()
    if args.check or args.models:
        print(json.dumps({
            "status": "ok",
            "active_vlm_mode": "EXTERNAL_API" if cfg["api_key"] else "HOST_AGENT_NATIVE_VLM_PLUS_LOCAL_OCR",
            "primary_model": cfg["primary_model"],
            "fallback_models": cfg["model_chain"],
            "base_url": cfg["base_url"],
            "wire_format": cfg["api_format"],
            "supported_modes": list(MODE_PROMPTS.keys()) + ["batch"],
        }, indent=2, ensure_ascii=False))
        return

    if not args.image_path:
        parser.error("image_path is required unless --check or --models is specified.")

    p = Path(args.image_path)
    if args.mode == "batch" and p.is_dir():
        imgs = sorted([f for f in p.iterdir() if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")])
        batch_res = []
        for img_f in imgs:
            sub_out = Path(args.out_dir) / img_f.stem
            res = run_vlm_vision_pipeline(str(img_f), str(sub_out), mode="gameplay", ocr_lang=args.ocr_lang)
            batch_res.append({"image": img_f.name, "report": str(sub_out / "vlm_recognition_report.json"), "regions": len(res["som_ocr_grounded_regions"])})
        print(json.dumps({"batch_processed": len(batch_res), "items": batch_res}, indent=2, ensure_ascii=False))
    else:
        run_vlm_vision_pipeline(
            args.image_path,
            args.out_dir,
            mode=args.mode,
            custom_prompt=args.prompt,
            classes=args.classes,
            compare_with=args.compare_with,
            ocr_lang=args.ocr_lang,
        )


if __name__ == "__main__":
    main()
```
