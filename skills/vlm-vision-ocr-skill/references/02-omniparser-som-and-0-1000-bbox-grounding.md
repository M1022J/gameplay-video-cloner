# 02 — OmniParser Set-of-Mark (`SoM`) & Canonical `0..1000` Coordinate Grounding (`microsoft/OmniParser` + `Autsunset/vision-label-skill`)

## Sources
- [`microsoft/OmniParser`](https://github.com/microsoft/omniparser) (*Set-of-Mark `#01..#N` Visual Grounding for GUI & Game Screens*)
- [`Autsunset/vision-label-skill`](https://github.com/Autsunset/vision-label-skill) (*Canonical `0..1000` Bounding Box & Polygon Detection + Multi-Format Exporters*)
- [`anubhavg-icpl/vibe` (`skills/vision-llm-expert/SKILL.md`)](https://github.com/anubhavg-icpl/vibe/blob/master/skills/vision-llm-expert/SKILL.md)

## Why Raw VLM Coordinate Guesses Drift — and How `SoM` + `0..1000` Fixes It
- Asking a VLM to guess raw pixel coordinates on a `1920x1080` screen often drifts by `30–80px`.
- `scripts/game_ocr_and_som_grounder.py` first draws a **`0..1000` normalized ruler border** and numbers every detected UI/sprite box (`#01..#24`), storing both `[ymin, xmin, ymax, xmax]` in `0..1000` space and exact `[x, y, w, h]` pixel coordinates.
- `scripts/export_vlm_labels.py` converts `<stem>.raw.json` directly into **YOLO (`.txt`)**, **YOLO-seg**, **Labelme (`.json`)**, **COCO (`.json`)**, or **CSV** without re-calling the VLM API!
