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
