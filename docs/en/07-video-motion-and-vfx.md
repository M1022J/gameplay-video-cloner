# 07 · Video Motion & VFX Analysis (v2 supplement)

## The problem it solves
V1 sampling was sparse (~1fps) plus static-image reading: swing arcs, easing curves,
hit-stop frames, screen-shake amplitude, and hit-flash — all the *between-frame*
information — were lost. The v2 (19-source) edition adds a dedicated motion layer.

## Four techniques
1. **Macro → micro drill-down** (Schmandarine/web-motion-skill): a 16/24-tile macro
   contact sheet locates the action segment, then a 30/60fps consecutive burst strip
   examines it frame by frame.
2. **Optical flow + onion-skin trails** (alirezarezvani/senior-computer-vision): OpenCV
   Farneback dense optical flow gives per-pixel motion vectors; 8 frames are composited
   into an onion-skin trail (cyan = startup, gold = active, magenta = recovery).
3. **Adaptive tiering + parallel audio/visual** (bsisduck/video-analyzer-skill):
   motion-adaptive FPS tiers, scene cuts, audio transient peaks, and parallel
   visual/motion/audio subagents.
4. **Timing–easing quantification** (LottieFiles/motion-design-skill + frankxai):
   displacement is fitted to Bezier easing curves and checked against lookup tables
   (hit-flash 50–70ms, hit-stop 40–95ms, pickup pop 120–180ms easeOutBack,
   slash/dash 150–250ms cubic-bezier(0.16, 1, 0.3, 1)), then passed through the
   web-motion-auditor 5-point quality gate.

## Two new scripts (skill/scripts/)
| Script | Outputs |
|---|---|
| `extract_motion_trails_and_vfx.py` | `action_burst_strip_*.png` (high-FPS consecutive action strips), `onion_skin_trail_*.png` (onion-skin trails with flow arrows), `vfx_timing_report.json` (phaseCorrelate shake offsets, hit-stop frames, flash spikes, fitted easing type) |
| `extract_audio_sfx_peaks.py` | `audio_peaks.json` (50ms RMS envelope peaks → SFX events aligned to time/frames, tiered small/medium/large) |

New dependency: `opencv-python-headless` (see requirements.txt). Both scripts were
executed on a real video during integration: 3 burst strips + 3 trail images + VFX
timing JSON produced; multiple medium-tier audio peaks detected.

Originals: `upstream/web-motion-skill/`, `upstream/senior-computer-vision/`,
`upstream/video-analyzer-skill/`, `upstream/motion-design-skill/`,
`upstream/awesome-motion-design-agent-skills/`; summaries in
`skill/references/video-motion-and-vfx-analysis/`.
