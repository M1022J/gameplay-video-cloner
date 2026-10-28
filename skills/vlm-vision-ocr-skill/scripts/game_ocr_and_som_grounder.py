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
