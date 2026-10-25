# 01 — 2D Spine/Rive & 3D Blender/Three.js Skeletal Animation & Analytic IK

## Sources
- [`GenielabsOpenSource/spine-animation-ai`](https://github.com/GenielabsOpenSource/spine-animation-ai) & [`BowTiedSwan/rive-skills`](https://github.com/BowTiedSwan/rive-skills)
- [`composio-community/opencode-skills` (`blender-rigging-animation`)](https://github.com/composio-community/opencode-skills) & [`arjun988/blender-skills`](https://github.com/arjun988/blender-skills)

## 1. 2D Skeletal Hierarchy, Mesh Weights & Two-Bone Analytic IK (`scripts/spine_and_swarm_pipeline.py`)
- **16-Bone Humanoid Hierarchy**: `root -> hip -> torso -> neck/head/hat + L/R upper-arm/lower-arm/hand + L/R upper-leg/lower-leg/foot`.
- **6 Procedural Animation States**: `idle` (`2.5Hz` breathing + `0.1s` head overlap), `walk`, `run`, `attack` (windup -> active slash -> follow-through), `jump`, and `hit/death`.
- **Runtime Two-Bone Analytic IK (`solveTwoBoneIK`)**: Exact law-of-cosines elbow/knee solver so feet plant on uneven terrain and hands aim toward targets.

## 2. 3D Articulated Joints & SkinnedMesh Crossfading (`Three.js r186` / `Godot 4.7` / `Unity 6.3`)
- Build hierarchical `THREE.Group` pivots (`hips`, `torsoPivot`, `headPivot`, `armL/R`, `legL/R`) or `THREE.AnimationMixer` state machines with `0.18s` crossfade blending and max 4 bone weights per vertex.
