# Video Scene, HUD OCR, and Audio Timeline Indexing (`video-db/skills`)

Use `analyze_gameplay_video.py` to detect scene transitions (`mean_pixel_delta > 42.0`), mask static HUD bands (`hud_variance_map.png`), and track OCR score/timer deltas.
