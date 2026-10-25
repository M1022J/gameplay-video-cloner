#!/usr/bin/env python3
"""Validate generated HTML5/JS game replica against PlayableIntelligence & Claude-Code-Game-Studios QA hooks."""
import argparse, json, re, sys
from pathlib import Path

def validate_html_game(file_path: Path) -> dict:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    checks = {
        "has_constants_or_config": bool(re.search(r"\b(Constants|CONFIG|PALETTE)\b", text)),
        "has_state_reset": bool(re.search(r"\b(reset|initGame|restartGame|GameState)\b", text)),
        "has_request_animation_frame": "requestAnimationFrame" in text,
        "has_delta_time_normalization": bool(re.search(r"\b(dt|deltaTime|delta)\b", text)),
        "has_dual_input_listeners": bool(re.search(r"(pointerdown|mousedown|touchstart)", text)) and bool(re.search(r"(keydown|ArrowLeft|KeyA)", text)),
        "has_trauma_or_screen_shake": bool(re.search(r"(trauma|shake|hitStop)", text, re.IGNORECASE)),
        "has_web_audio_synth": bool(re.search(r"(AudioContext|webkitAudioContext)", text)),
        "has_render_game_to_text": "render_game_to_text" in text,
    }
    passed = sum(1 for v in checks.values() if v)
    return {"file": str(file_path), "score": f"{passed}/{len(checks)}", "passed_all": passed >= len(checks) - 1, "checks": checks}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("game_file")
    args = parser.parse_args()
    p = Path(args.game_file)
    if not p.exists():
        print(json.dumps({"error": f"File not found: {p}"}))
        sys.exit(1)
    print(json.dumps(validate_html_game(p), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
