# Motion Timing, Easing Lookup Tables & VFX Choreography (`LottieFiles` + `frankxai`)

Distilled from `LottieFiles/motion-design-skill` and `frankxai/awesome-motion-design-agent-skills` (`motion-director` & `web-motion-auditor`).

## 1. Universal Game & UI Timing Lookup Table (`timing-easing-tables.md`)

| Action / VFX Event | Recommended Duration | Easing Function / Math Curve | Visual Purpose |
| :--- | :--- | :--- | :--- |
| **Hit-Flash (Sprite White Overlay)** | `50ms - 70ms` (`3-4 frames`) | Step / Instant Hold -> Linear Fade | Registers instant damage impact |
| **Hit-Stop (Simulation Freeze)** | `40ms - 95ms` (`2-6 frames`) | Real-time unscaled hold (`performance.now()`) | Sells heavy melee/explosion weight |
| **Button Press / Pickup Pop** | `120ms - 180ms` | `easeOutBack` (`c1 = 1.70158` overshoot) | Tactile responsiveness & dopamine |
| **Attack Slash / Dash Active** | `150ms - 250ms` | `cubic-bezier(0.16, 1, 0.3, 1)` (`expo.out`) | Explosive burst velocity with smooth stop |
| **Floating Damage / Score Number** | `550ms - 750ms` | `x`: sine drift, `y`: initial `-180px/s` + gravity `420px/s^2` | Readable arc that clears the hitbox zone |
| **Modal / Level-Up Card Entrance** | `280ms - 420ms` (`stagger: 60ms`) | `easeOutBack` scale `0.8 -> 1.0` + opacity | Directs player attention across 3 choices |
| **Health Bar Damage Lag-Trail** | `350ms - 500ms` (after `120ms` delay) | `easeOutCubic` (`1 - Math.pow(1 - t, 3)`) | Clearly shows how much HP was lost on hit |

## 2. `web-motion-auditor` 5-Point Motion Quality Gate (`frankxai`)
Before delivering any replicated game, verify:
- [ ] **No Linear Mechanical Movement**: Every UI popup, jump, knockback, and merge uses an explicit easing function or physics velocity/gravity integrator.
- [ ] **Anticipation + Follow-Through Present**: Attacks and jumps have visible squash/windup (`0.08s`) and recovery overshoot (`0.15s`).
- [ ] **Proportional Trauma Scaling**: Small pickups trigger `trauma += 0.15` (no hit-stop); crits/boss hits trigger `trauma += 0.80` + `80ms` hit-stop + `28` radial particles.
- [ ] **Staggered Multi-Element Choreography**: Upgrade cards, wave banners, and reward chests animate with `60ms-80ms` stagger rather than popping on the exact same frame.
- [ ] **60Hz / 120Hz Delta-Time Parity**: All easing timers advance by `dt` seconds, never by raw frame count.
