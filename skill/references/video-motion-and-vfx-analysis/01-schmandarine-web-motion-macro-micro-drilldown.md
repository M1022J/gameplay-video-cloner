# Macro-to-Micro High-FPS Motion Drill-Down (`Schmandarine/web-motion-skill`)

Distilled from `Schmandarine/web-motion-skill` (Closing the Agentic Vision Loop for Animation & Game Motion).

## 1. Why Single Screenshots Fail on Motion & How to Close the Loop
An AI agent reading a single screenshot or 1fps frames is blind to **anticipation**, **easing curves**, **hit-stop freeze frames**, and **stagger direction**. Close the visual loop in two stages:

1. **Stage 1 - Macro Contact Sheet (`contact_sheet.png`)**:
   - Sample 16 to 24 evenly spaced frames across the full video, labeled with exact frame numbers and timestamps (`#01 | 0.00s` ... `#16 | 8.50s`).
   - Identify the exact time windows where key actions occur:
     - **Entrance / Spawn Window**: When entities appear or scale in.
     - **Active Combat / Merge / Jump Window**: When peak velocity, slashes, collisions, or combos fire.
     - **Exit / Death / Transition Window**: When particles scatter, UI modals pop, or screens shake.
2. **Stage 2 - Micro 30/60fps Burst Strip (`action_burst_strip_01.png` via `extract_motion_trails_and_vfx.py`)**:
   - Drill into the 0.4-second peak window at `30fps` (12 consecutive frames, `33ms` apart) so the agent can read:
     - **Anticipation Frames** (e.g., `f01-f03`: character squats `6px` or pulls weapon back `+65°`).
     - **Active Strike / Launch Frames** (e.g., `f04-f06`: fast swing arc + white slash trail).
     - **Hit-Stop & Impact Flash** (e.g., `f07-f08`: `d=0.4` zero-motion freeze frame + `+45` luminance spike).
     - **Follow-Through & Settle** (e.g., `f09-f12`: `easeOutBack` overshoot settle).

## 2. Disney's 12 Principles Adapted for Runtime Game Code
- **Slow In / Slow Out**: Real objects have mass. Never use linear `t` for UI, jumps, or knockbacks; use `cubic-bezier(0.4, 0, 0.2, 1)` or `power2.inOut`.
- **Anticipation**: Add a `60ms-100ms` preparatory counter-motion (`scale(0.92, 1.08)` or `-10px` pullback) before dashes, jumps, and boss attacks.
- **Follow-Through & Overlapping Action**: Offset child elements (`stagger: 0.08s` on UI cards; `0.10s` phase delay on character head/hat/cape relative to torso).
- **Arc**: Animate `x` and `y` with different easing functions (`x` linear, `y` parabolic gravity or sine) so projectiles, loot drops, and floating damage numbers travel along curved arcs rather than robotic straight lines.
