# 05 · 2D / 3D Skeletal Animation

## 2D: Spine 4.2 standard humanoid (16 bones)
`root → hip → torso → neck/head/hat`, arms `shoulder→upper-arm→lower-arm→hand`,
legs `upper-leg→lower-leg→foot`. Six procedural animation presets (cubic bezier
[0.25, 0, 0.75, 1]): idle 2.0s breathing bob (head follows with a 0.1s phase delay),
walk 0.8s opposing swing, run 0.5s forward lean + flight bounce, attack 0.6s
windup → strike → recovery, jump 1.0s, wave 1.2s.
Tool chain: `position_parts.py → build_spine_json.py → make_atlas.py → generate_spine_player.py`.
Originals and examples: `upstream/spine-animation-ai/`.

## Analytic two-bone IK (solveTwoBoneIK)
Given a root point, a target, and two bone lengths, solve the joint angles directly with
the law of cosines — for aiming arms and planting feet. Zero dependencies, runs as-is in
Canvas. Formula and JS implementation: `HANDBOOK.md` §2.1.

## 2D supplement: Rive meshes & state machines
Multi-bone weighted vertex skinning (w1+w2+w3+w4=1) for capes/hair/soft bodies; a 3-layer
state machine: layer 0 locomotion (Idle/Walk/Run blended by speed + jump/fall/land),
layer 1 upper-body action override (attack/aim), layer 2 additive hit-react
(150ms recoil + white flash). Originals: `upstream/rive-skills/`.

## 3D: Blender rigging & runtime
Production bone chain `root→pelvis→spine×3→chest→neck→head` plus limb twist bones;
≤4 bone influences per vertex, pole-target two-bone IK, bake NLA actions, export .glb
(+Y Up). At runtime use either a procedural Three.js rig (`createProcedural3DRig`, a
Group joint hierarchy) or `GlbAnimationController` (AnimationMixer with 0.18s crossfades).
Originals: `upstream/opencode-blender-rigging-animation/` and `upstream/blender-skills/`
(94 Blender skills).

## Game feel (Juice) trio
- Camera shake: decaying trauma² sinusoidal offset, applied only to the render
  transform (`ctx.translate`), never to physics coordinates
- Hit-stop: real-time based (performance.now), three tiers (small/medium/large, 45–95ms)
- Squash & stretch: volume-conserving easeOutBack; merge-style pop 1.3x → 1.0x
Per-genre numeric baselines (gravity / restitution / friction / coyote time):
`HANDBOOK.md` §3.3.
