# Stroboscopic Onion-Skin Trails & OpenCV Optical Flow (`alirezarezvani/senior-computer-vision`)

Distilled from `alirezarezvani/claude-skills/engineering-team/skills/senior-computer-vision/SKILL.md` and adapted for single-image motion comprehension.

## 1. Baking Continuous Video Motion into a Single Image (`onion_skin_trail_01.png`)
Even if an LLM interface only inspects static PNG images, `scripts/extract_motion_trails_and_vfx.py` converts temporal motion into spatial geometry on a single canvas:

- **Color-Coded Stroboscopic Ghosting (Onion-Skinning)**:
  - Samples 8 consecutive frames across an action beat and composites moving foreground pixels (`|I_t - I_{t-1}| > 18`) onto a dimmed background with progressive color tinting:
    - **Cyan Ghosts (`t_0 .. t_2`)**: Startup position & initial velocity direction.
    - **Gold Ghosts (`t_3 .. t_5`)**: Mid-action trajectory arc & peak speed (wider spacing between ghosts = higher velocity!).
    - **Magenta Ghosts (`t_6 .. t_7`)**: Impact point, overshoot, and recovery settle.
- **Farneback Dense Optical Flow Arrows (`cv2.calcOpticalFlowFarneback`)**:
  - Computes per-pixel velocity vectors `(vx, vy)` between consecutive frames and draws directional arrows where `hypot(vx, vy) > 3.5 px/frame`.
  - Allows the agent to immediately distinguish:
    - **Radial Outward Arrows**: Explosion shockwave or particle burst.
    - **Converging Inward Arrows**: Magnetic XP gem pickup or suction vortex.
    - **Parallel Background Arrows**: Camera scrolling speed or screen-shake direction.

## 2. Automated VFX Telemetry (`vfx_timing_report.json`)
- **Camera Shake Detection (`cv2.phaseCorrelate`)**: Measures sub-pixel global translation shift `(dx, dy)` between consecutive frames to extract exact `trauma` amplitude in pixels.
- **Hit-Stop Detection**: Flags frames inside an active combat window where `mean_pixel_delta` drops below `25%` of the window's average delta, outputting `estimated_hit_stop_duration_ms`.
- **Hit-Flash Detection**: Flags frames where mean luminance spikes `> +18` above window median, outputting exact flash frame indices.
