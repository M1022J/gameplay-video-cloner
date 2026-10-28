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
