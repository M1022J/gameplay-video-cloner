# 02 — `0.01px` Sub-Pixel Centroid Oscilloscope & `3x` Delta-Patch / `10x` Residual Strips (`snapcn` + `DVR-Scan`)

## Sources
- [`snapcndev/snapcn` (`.claude/skills/motion-quality/SKILL.md`)](https://github.com/snapcndev/snapcn/blob/main/.claude/skills/motion-quality/SKILL.md) (*Rule 0: `0.01px` Anti-Aliasing Sub-Pixel Centroid Recovery*)
- [`Breakthrough/DVR-Scan`](https://github.com/Breakthrough/DVR-Scan) & [`NVIDIA/skills` (`tao-train-action-recognition`)](https://github.com/NVIDIA/skills/blob/main/skills/tao-train-action-recognition/SKILL.md) (*Connected-Component Micro-ROI Extraction & Residual Amplification*)

## 1. Visual Micro-Diff Extraction (`scripts/extract_micro_frame_deltas.py`)
Instead of feeding 24 full-screen `1080p` frames that look 99.9% identical, crop **only the changing bounding box `[x, y, w, h]`** (`diff >= 3/255`):
- **`delta_patch_strip_3x_zoom.png`**: Packs 24 consecutive `3x` zoomed micro-patches into one contact sheet so the vision model sees every pixel of a digit roll, eye blink, or button press.
- **`amplified_10x_residual_strip.png`**: Multiplies `|I_t - I_{t-1}|` by `10x` (`INFERNO` colormap) so even a `1%` opacity shimmer glows brightly.

## 2. `0.01px` Sub-Pixel Motion Oscilloscope (`scripts/subpixel_motion_oscilloscope.py`)
Recovers sub-pixel coordinates from anti-aliased edge intensities ($\alpha = |I_t - I_{\text{bg}}| / |I_{\text{fg}} - I_{\text{bg}}|$) across every consecutive frame (`stride = 1`), outputting:
- Sub-pixel trajectory `(cx_subpixel, cy_subpixel)` accurate to `0.01px`.
- Autocorrelation loop period (`detected_loop_period_sec`) and velocity-integrated `cubic-bezier` easing curves.
