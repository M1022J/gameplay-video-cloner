---
name: gameplay-video-cloner
description: Reverse-engineer and 1:1 replicate playable games directly from gameplay videos (看游戏视频直接复刻游戏), screen recordings, GIFs, or video URLs using a Lead-Agent + Parallel-Subagents Swarm workflow. Self-contained single-file edition bundling 14 open-source repositories: multi-agent orchestration suites (obra/superpowers dispatching-parallel-agents & subagent-driven-development, kieranklaassen/orchestrating-swarms, sickn33/subagent-orchestrator, qodex-ai/multi-agent-orchestration, VoltAgent/awesome-claude-code-subagents), 2D/3D skeletal animation suites (GenielabsOpenSource/spine-animation-ai, BowTiedSwan/rive-skills, composio-community/opencode-skills blender-rigging-animation, arjun988/blender-skills), and game pipelines (ybuild-ai/ai-game-art-pipeline-skill, video-db/skills, PlayableIntelligence/game-creator, gamedev-skills/awesome-gamedev-agent-skills, Donchitos/Claude-Code-Game-Studios). Use whenever the user shares a gameplay video or asks to clone, replicate, rig, animate, or multi-agent build a 2D/3D game.
allowed-tools: default_api google youtube image_gen
---
# Gameplay Video Cloner (All-in-One Single-File `SKILL.md` Edition)

This single `SKILL.md` file is **100% self-contained** (following the `GenielabsOpenSource/spine-animation-ai` inline-embedding standard). All **14 open-source skill repositories**, **24 reference playbooks**, and **15 executable Python scripts** are embedded directly inside this one file so you can copy, upload, or drop this single file into any AI agent environment without needing external folders or ZIP archives.

## When to Use

- The user provides a gameplay video (`.mp4`, `.mov`, `.webm`, `.gif`), screen recording, or video URL and asks to 1:1 clone, replicate, or rebuild the game.
- The user wants a **Lead Agent + Parallel Specialist Subagents Swarm** (`obra/superpowers`, `orchestrating-swarms`, `subagent-orchestrator`) to divide and conquer game development (Telemetry Architect, Physics/AI Engineer, 2D/3D Skeletal Animator, HUD/Audio Designer, QA Verifier).
- The user wants **2D skeletal animation** (Spine 4.2, Rive mesh skinning, 2-bone analytic IK) or **3D skeletal animation** (Three.js `SkinnedMesh` / articulated joint hierarchies, Blender rigging, glTF animation crossfading, Unity/Godot IK).

## Master Execution Workflow (3-Round Swarm Pipeline)

### Step 0: Self-Extract Required Inline Scripts (For Single-File Environments)

If `./scripts/` does not yet exist on disk, extract the needed Python script(s) from **Section 7 (Embedded Python Scripts)** of this file to `/tmp/cloner_scripts/` and run them via `execute_bash`.

### Step 1 — Round 1 (Foundation): Video Telemetry, Engine Routing & Swarm Mission Brief

1. **Extract Video Telemetry & Contact Sheets (`analyze_gameplay_video.py` + `extract_video_frames.py` + `sheet_contact.py`)**:
   - Sample 16 keyframes, build a numbered `contact_sheet.png`, compute the temporal pixel-variance `hud_variance_map.png` (isolating static HUD bars from the active playfield), detect scene-cut transitions (`mean_pixel_delta > 42.0`), and extract the 6-color dominant hex palette into `telemetry.json`.
   - Call `view_file` on `contact_sheet.png` and `telemetry.json`.
2. **Lock the Shared Interface Contract (`PlayableIntelligence/game-creator` + `obra/superpowers`)**:
   - Define `Constants` (aspect ratio `9:16` vs `16:9`, hex palette, physics speeds, safe zones), `EventBus` (`on_hit`, `on_merge`, `on_pickup`, `on_land`, `on_level_up`, `on_death`), and `GameState` (with deterministic `reset()` and `window.render_game_to_text()`).
3. **Initialize the 5-Subagent Mission Brief & DAG Task Board (`orchestrate_subagents.py` + `swarm_task_board.py`)**:
   - Complete DAG Task `#1 (Telemetry & EventBus Contract)`, automatically unblocking parallel Tasks `#2`, `#3`, and `#4`.

### Step 2 — Round 2 (Parallel Specialist Fan-Out): Execute Isolated Domain Subagents

Run the three unblocked specialist modules in parallel with strict context isolation (each subagent reads only the `Constants` + `EventBus` contract and writes only to its own namespace):

- **`subagent-02-physics-controller` (`PlayerController` + `PhysicsSystem` + `WaveDirector`)**:
  - Implement delta-time normalized movement (`dt = Math.min(0.05, (now - lastTime) / 1000)`), dual touch/pointer + keyboard (`WASD`/Arrows/`Space`) controls, sub-stepped circle/AABB collision resolution (`4-6` relaxation sub-steps for stacked objects), and enemy steering/wave spawning.
- **`subagent-03-skeletal-art` (`SkeletalRig` + `solveTwoBoneIK` + `Juice` + `ParticleSystem`)**:
  - **2D Games**: Use the 16-bone Spine 4.2 hierarchy (`root -> hip -> torso -> neck/head/hat + arms + legs`), cubic bezier `[0.25, 0, 0.75, 1]` interpolation, `0.1s` head/cape follow-through phase delay, Rive-style multi-layer state blending, and the analytic 2-bone IK solver (`solveTwoBoneIK`).
  - **3D Games**: Use `createProcedural3DRig` (articulated Three.js `Group` joint hierarchy) or `GlbAnimationController` (`THREE.AnimationMixer` with `0.18s` crossfades).
  - **Game-Feel Juice**: Attach 3-tier feedback bundles (`small`, `medium`, `large`) combining decaying `trauma^2` sinusoidal camera offset shake (applied to `ctx.translate`, never physics coordinates), real-time unscaled `hit_stop` (`performance.now()`), and volume-conserving `easeOutBack` squash-and-stretch.
- **`subagent-04-hud-audio` (`HUDRenderer` + `AudioSynth` + `TuningDrawer`)**:
  - Render score counters, health/XP bars with damage lag-trails, floating delta popups (`+100`, `CRIT!`), a collapsible `⚙️ 参数微调` live parameter tuning drawer, and gesture-unlocked Web Audio synthesizer BGM/SFX.

### Step 3 — Round 3 (Fan-In Review & Assembly): Two-Stage Review, 3-Point Spot Check & Canvas Delivery

1. **Run the 3-Point Spot Check & Architecture Validator (`merge_subagent_modules.py` + `validate_architecture.py`)**:
   - Verify every subagent stayed in scope, exported all required contract symbols, left **zero `TODO`/`FIXME` placeholders**, and passed all 8 architecture gates.
2. **Run Consensus Balancing (`qodex-ai` 3-Perspective Audit)**:
   - Verify fair hitboxes (`75%-80%` visual size), `80ms` coyote time, `0%` softlock rate, and visual contrast against the source video.
3. **Deliver Playable Game in Canvas**:
   - Save the final playable HTML5/Three.js/Phaser game to `/working_dir/<conversation_id>/artifacts/file_generation/ttl=63d/output/<game_name>.html`, present it via `google:show_file`, and output the **Multi-Agent Division-of-Labor Table** and **Video-to-Game Replication Matrix**.

---

## Section 1: Multi-Agent Division-of-Labor & Swarm Playbooks (5 Repositories)

### 1.1 `obra/superpowers`: `dispatching-parallel-agents` & `subagent-driven-development`

- **Isolated Context Packets (Never Dump Session History)**:
  - Each subagent receives a focused brief specifying:
    1. **Scope**: Exact module/namespace it owns.
    2. **Inputs**: Exact `Constants`, `EventBus` events, and `telemetry.json` values.
    3. **Constraints**: Do not mutate other modules' state directly; communicate strictly via `EventBus.emit(event, payload)`.
    4. **No Nested Subagents**: Worker subagents never spawn child subagents or duplicate reviewers.
- **Two-Stage Review Gate**:
  - **Stage 1 (Spec Compliance)**: Verify every mechanic, bone animation state, and HUD element from the video blueprint is implemented with zero placeholders.
  - **Stage 2 (Code Quality)**: Verify `dt` frame-rate independence, object pooling (swap-and-pop active arrays, zero `new` in 60fps hot paths), and clean `GameState.reset()`.
- **Persistent Recovery Ledger (`sdd_ledger.md`)**:
  - Log every completed round and architectural ruling (`Ruling: <decision> - <why> - <impact>`) so progress survives context compaction.

### 1.2 `kieranklaassen/orchestrating-swarms`: Leader + Teammates + DAG Task Queue

- **Swarm DAG Auto-Unblocking (`blockedBy`)**:
  - `Task #1`: Video Telemetry & `EventBus` Schema (`blockedBy: []`)
  - `Task #2`: Physics, Controller & Wave Spawner (`blockedBy: ["1"]`)
  - `Task #3`: 2D/3D Skeletal Rig, Analytic IK & Juice VFX (`blockedBy: ["1"]`)
  - `Task #4`: HUD Safe-Zones, Web Audio Synth & Tuning Drawer (`blockedBy: ["1"]`)
  - `Task #5`: Two-Stage Review & Single-File Assembly (`blockedBy: ["2", "3", "4"]`)
- **6 Canonical Swarm Patterns**:
  1. **Parallel Specialists (Leader Fan-Out / Fan-In)**
  2. **Sequential Pipeline with Auto-Unblocking**
  3. **Self-Organizing Worker Pool**
  4. **Research (Video Telemetry) -> Implementation**
  5. **Plan Approval Gate before Code Generation**
  6. **Coordinated Multi-Namespace Module Assembly**

### 1.3 `sickn33/antigravity-awesome-skills`: 6-Phase `subagent-orchestrator`

1. **Phase 1 - DECOMPOSE**: Emit the structured Mission Brief (`Goal`, `Total Agents`, `Round-by-Round Dependencies`, `Contract Exports`).
2. **Phase 2 - COMPLEXITY ROUTING**: Route frame extraction, sprite slicing, and contact sheets to deterministic Python scripts; route physics, skeletal IK, and shaders to specialist synthesis.
3. **Phase 3 - CONTEXT ISOLATION**: Enforce strict `Files to read`, `Files to write`, and `Do NOT read` boundaries per subagent.
4. **Phase 4 - PARALLEL EXECUTION & 3-POINT SPOT CHECK**:
   - Check 1: Did the subagent stay within its assigned namespace?
   - Check 2: Do all imports/exports match the shared `EventBus` and `Constants` contract?
   - Check 3: Are there zero `TODO` / `FIXME` / `implement later` strings?
5. **Phase 5 - SURGICAL ERROR RECOVERY**: If one subagent module fails a check, re-run only a targeted repair on that single module rather than restarting the whole mission.
6. **Phase 6 - FINAL INTEGRATION SWEEP**: Verify zero duplicate identifiers, clean `GameState.reset()`, working touch + keyboard inputs, and `window.render_game_to_text()`.

### 1.4 `qodex-ai/multi-agent-orchestration` & `VoltAgent/awesome-claude-code-subagents`: Specialist Contract Matrix

| Subagent ID | Role (`VoltAgent` + `Game Studios`) | Owned Namespace | Subscribed `EventBus` Events | Exported Symbols / Emitted Events |
| :--- | :--- | :--- | :--- | :--- |
| **`lead-orchestrator`** | `multi-agent-coordinator` / `producer` | `Constants`, `EventBus`, `GameState`, `main` | `task_completed`, `on_game_over` | `initGame()`, `GameState.reset()`, `window.render_game_to_text()` |
| **`subagent-01-telemetry`** | `video-analyst` / `systems-designer` | `TelemetrySpec`, `Constants.PALETTE` | `on_video_loaded` | `Constants`, `STAGE_CONFIG`, `HUD_SAFE_ZONES` |
| **`subagent-02-physics`** | `gameplay-programmer` / `ai-programmer` | `PlayerController`, `PhysicsSystem`, `WaveDirector` | `input:move`, `input:action` | `on_hit`, `on_merge`, `on_pickup`, `on_land`, `on_death` |
| **`subagent-03-skeletal`** | `technical-artist` / `spine-rive-animator` | `SkeletalRig`, `solveTwoBoneIK`, `Juice`, `ParticleSystem` | `on_hit`, `on_land`, `on_attack`, `on_merge` | `renderRig(ctx, dt)`, `Juice.feedback(x, y, tier)` |
| **`subagent-04-hud-audio`** | `ui-programmer` / `sound-designer` | `HUDRenderer`, `AudioSynth`, `TuningDrawer` | `on_score`, `on_hit`, `on_level_up`, `on_death` | `renderHUD(ctx)`, `playSfx(type)`, `bindTuningUI()` |

---

## Section 2: 2D & 3D Skeletal Animation Playbooks (4 Repositories)

### 2.1 `GenielabsOpenSource/spine-animation-ai`: Spine 4.2 2D Skeletal Hierarchy & Analytic 2-Bone IK

- **Standard 16-Bone Humanoid Hierarchy (`Y-up` in Spine JSON, `Y-down` in HTML5 Canvas)**:
  - `root (0,0)` at feet ground center -> `hip` -> `torso` -> `neck` -> `head` -> `hat/hair`
  - `torso` -> `left-shoulder` -> `left-upper-arm` -> `left-lower-arm` -> `left-hand`
  - `torso` -> `right-shoulder` -> `right-upper-arm` -> `right-lower-arm` -> `right-hand / weapon`
  - `hip` -> `left-upper-leg` -> `left-lower-leg` -> `left-foot`
  - `hip` -> `right-upper-leg` -> `right-lower-leg` -> `right-foot`
- **6 Procedural Animation Presets (Cubic Bezier `[0.25, 0, 0.75, 1]`)**:
  - **`idle` (2.0s loop)**: Hip `±3.5px` breathing bob, torso `±1.4°` rotate, head `±1.8°` delayed counter-sway (`0.1s` phase lag for follow-through).
  - **`walk` (0.8s loop)**: Opposing arm-leg sine swing (`±24°`), hip double-frequency bob (`±5px` at `0.2s` and `0.6s`), torso `±2.5°` lean.
  - **`run` (0.5s loop)**: Exaggerated limb swing (`±42°`), `-6°` forward torso lean, `±8px` vertical flight bounce.
  - **`attack` (0.6s)**: 3-phase anticipation windup (`0.0-0.2s`, torso `+12°`, arm `+65°`) -> strike (`0.2-0.35s`, torso `-18°`, arm `-75°`) -> recovery (`0.35-0.6s`).
  - **`jump` (1.0s)**: Squat anticipation -> launch stretch -> apex hang -> landing squash.
  - **`wave` (1.2s)**: Raise shoulder `-45°`, oscillate forearm `±15°`.
- **Zero-Dependency Canvas 2D Hierarchical Bone & 2-Bone Analytic IK Solver**:

```javascript
// 1. Two-Bone Analytic Inverse Kinematics (for aiming arms or planting feet)
function solveTwoBoneIK(rootX, rootY, targetX, targetY, len1, len2, flipKnee = 1) {
  const dx = targetX - rootX;
  const dy = targetY - rootY;
  const dist = Math.min(len1 + len2 - 0.001, Math.max(Math.abs(len1 - len2) + 0.001, Math.hypot(dx, dy)));
  const baseAngle = Math.atan2(dy, dx);
  const cosAngle1 = (len1 * len1 + dist * dist - len2 * len2) / (2 * len1 * dist);
  const angle1 = baseAngle + flipKnee * Math.acos(Math.max(-1, Math.min(1, cosAngle1)));
  const jointX = rootX + Math.cos(angle1) * len1;
  const jointY = rootY + Math.sin(angle1) * len1;
  const angle2 = Math.atan2(targetY - jointY, targetX - jointX);
  return { angle1, angle2, jointX, jointY };
}

// 2. Procedural 2D Articulated Character Renderer (Idle / Walk / Run / Attack / Hit)
function drawArticulated2DCharacter(ctx, x, y, facing, time, moveSpeedNorm, attackPhase, hitFlash, palette) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(facing, 1);

  const walkFreq = 11.0;
  const stride = Math.sin(time * walkFreq) * moveSpeedNorm;
  const bob = Math.abs(Math.cos(time * walkFreq)) * 5 * moveSpeedNorm + Math.sin(time * 3.0) * 2.5;
  const lean = moveSpeedNorm * 0.14 + Math.sin(attackPhase * Math.PI) * 0.35;

  // Shadow
  ctx.fillStyle = 'rgba(0,0,0,0.32)';
  ctx.beginPath();
  ctx.ellipse(0, 0, 18 - bob * 0.3, 6, 0, 0, Math.PI * 2);
  ctx.fill();

  // Hip & Torso Pivot
  ctx.translate(0, -26 - bob);
  ctx.rotate(lean);

  // Back Leg & Back Arm
  const drawLimb = (ox, oy, ang, len, w, color) => {
    ctx.save();
    ctx.translate(ox, oy);
    ctx.rotate(ang);
    ctx.fillStyle = hitFlash > 0 ? '#ffffff' : color;
    ctx.beginPath();
    ctx.roundRect(-w / 2, 0, w, len, w / 2);
    ctx.fill();
    ctx.restore();
  };

  drawLimb(-5, 6, -stride * 0.65, 20, 7, palette.dark);
  drawLimb(-8, -14, stride * 0.55, 18, 6, palette.dark);

  // Torso
  ctx.fillStyle = hitFlash > 0 ? '#ffffff' : palette.primary;
  ctx.beginPath();
  ctx.roundRect(-12, -18, 24, 26, 7);
  ctx.fill();

  // Head (with 0.1s delayed follow-through sway)
  ctx.save();
  ctx.translate(0, -22);
  ctx.rotate(Math.sin((time - 0.1) * 3.0) * 0.06 - lean * 0.4);
  ctx.fillStyle = hitFlash > 0 ? '#ffffff' : palette.accent;
  ctx.beginPath();
  ctx.arc(0, -8, 12, 0, Math.PI * 2);
  ctx.fill();
  // Visor / Eyes
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(3, -11, 7, 4);
  ctx.restore();

  // Front Leg & Front Weapon Arm
  drawLimb(5, 6, stride * 0.65, 20, 7, palette.secondary);
  const armAngle = -stride * 0.55 - Math.sin(attackPhase * Math.PI) * 1.9;
  drawLimb(8, -14, armAngle, 19, 6, palette.accent);

  ctx.restore();
}
```

### 2.2 `BowTiedSwan/rive-skills`: 2D Mesh Skinning, Constraints & Multi-Layer State Machines

- **Mesh Vertex Skinning**: Bind 2D contour and internal grid vertices to 2-4 bones with normalized weights (`w1 + w2 + w3 + w4 = 1.0`) for smooth cape, hair, and soft-body deformation.
- **3-Layer Animation State Machine**:
  - `Layer 0 (Locomotion)`: `Idle <-> Walk <-> Run` blended continuously by `moveSpeed`, plus `Jump -> Fall -> Land` driven by `isGrounded`.
  - `Layer 1 (Upper-Body Action Override)`: Masked to `torso/arms/head` so attacks and aiming blend cleanly while legs keep running.
  - `Layer 2 (Additive Hit-React)`: `150ms` additive knockback recoil and white flash triggered on `on_hit`.

### 2.3 `composio-community/opencode-skills` (`blender-rigging-animation`) & `arjun988/blender-skills` (94 3D Skills)

- **Production 3D Bone Hierarchy**: `root (0,0,0) -> pelvis -> spine_01 -> spine_02 -> chest -> neck -> head`, plus `clavicle_L/R -> upperarm (+twist) -> forearm (+twist) -> hand` and `thigh_L/R (+twist) -> calf -> foot -> toe`.
- **GPU Skinning & Export Rules**: Apply all transforms (`Ctrl+A`), cap vertex weights at **4 bones per vertex**, add pole-target 2-bone IK on arms/legs with rotation limits, bake NLA actions, and export `.glb` with `+Y Up`.

### 2.4 Runtime 3D `SkinnedMesh`, `AnimationMixer` & Procedural 3D Rigging (`Three.js`, `Unity 6.3`, `Godot 4.7`)

```javascript
// Procedural Articulated 3D Character Rig for Three.js Browser Games (Zero external .glb needed!)
function createProcedural3DRig(THREE, palette) {
  const root = new THREE.Group();
  const hips = new THREE.Group();
  hips.position.y = 1.0;
  root.add(hips);

  const matBody = new THREE.MeshStandardMaterial({ color: palette.primary, roughness: 0.35 });
  const matAccent = new THREE.MeshStandardMaterial({ color: palette.accent, roughness: 0.25 });

  const torsoPivot = new THREE.Group();
  hips.add(torsoPivot);
  const torsoMesh = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.75, 0.38), matBody);
  torsoMesh.position.y = 0.38;
  torsoMesh.castShadow = true;
  torsoPivot.add(torsoMesh);

  const headPivot = new THREE.Group();
  headPivot.position.y = 0.82;
  torsoPivot.add(headPivot);
  const headMesh = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.46, 0.46), matAccent);
  headMesh.position.y = 0.23;
  headMesh.castShadow = true;
  headPivot.add(headMesh);

  function makeLimb(x, y, w, len, mat) {
    const pivot = new THREE.Group();
    pivot.position.set(x, y, 0);
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, len, w), mat);
    mesh.position.y = -len / 2;
    mesh.castShadow = true;
    pivot.add(mesh);
    return pivot;
  }

  const armL = makeLimb(-0.46, 0.70, 0.20, 0.62, matAccent);
  const armR = makeLimb( 0.46, 0.70, 0.20, 0.62, matAccent);
  torsoPivot.add(armL, armR);
  const legL = makeLimb(-0.18, 0.0, 0.22, 0.75, matBody);
  const legR = makeLimb( 0.18, 0.0, 0.22, 0.75, matBody);
  hips.add(legL, legR);

  return {
    root, hips, torsoPivot, headPivot, armL, armR, legL, legR,
    updateLocomotion(time, moveSpeedNormalized, attackPhase = 0) {
      const freq = 10.0;
      const swing = moveSpeedNormalized * 0.85;
      hips.position.y = 1.0 + Math.abs(Math.sin(time * freq)) * 0.12 * moveSpeedNormalized + Math.sin(time * 2.5) * 0.03;
      torsoPivot.rotation.x = moveSpeedNormalized * 0.18 + Math.sin(attackPhase * Math.PI) * 0.45;
      armL.rotation.x =  Math.sin(time * freq) * swing;
      armR.rotation.x = -Math.sin(time * freq) * swing - Math.sin(attackPhase * Math.PI) * 2.1;
      legL.rotation.x = -Math.sin(time * freq) * swing;
      legR.rotation.x =  Math.sin(time * freq) * swing;
    }
  };
}
```

---

## Section 3: Cross-Engine 74 Skills & Game-Feel Juice (`gamedev-skills/awesome-gamedev-agent-skills`)

### 3.1 Master Router & All 74 Skills across 8 Categories
- **Web Engines (6)**: `phaser-core`, `phaser-arcade-physics`, `pixijs-rendering`, `threejs-scene-setup`, `threejs-gltf-loading`, `threejs-materials-lighting`
- **Godot 4.7 (16)**: `godot-gdscript`, `godot-nodes-scenes`, `godot-signals-groups`, `godot-2d-movement`, `godot-tilemap`, `godot-physics`, `godot-ui-control`, `godot-animation`, `godot-shaders`, `godot-3d-essentials`, `godot-resources`, `godot-audio`, `godot-multiplayer`, `godot-export`, `godot-csharp`, `godot-gdscript-headless-testing`
- **Unity 6.3 LTS (8)**: `unity-csharp-scripting`, `unity-input-system`, `unity-physics`, `unity-animation`, `unity-scriptableobjects`, `unity-tilemap-2d`, `unity-navmesh`, `unity-build-pipeline`
- **Unreal Engine 5.8 (6)**: `unreal-blueprints`, `unreal-cpp-gameplay`, `unreal-enhanced-input`, `unreal-behavior-trees`, `unreal-niagara`, `unreal-packaging`
- **Other Engines (10)**: `bevy-ecs`, `pygame-core`, `love2d-core`, `roblox-luau`, `roblox-datastores`, `roblox-ui`, `roblox-networking`, `roblox-characters`, `roblox-physics`, `roblox-studio-workflow`
- **Cross-Engine Disciplines (15)**: `create-game-assets`, `game-ai`, `ai-behavior-trees-utility-ai`, `procedural-gen`, `dialogue-systems`, `save-systems`, `audio-design`, `shader-programming`, `physics-tuning`, `level-design`, `input-systems`, `game-feel`, `game-ui-ux`, `camera-systems`, `performance-optimization`
- **Genres (9)**: `platformer`, `roguelike`, `rpg`, `fps-shooter`, `tower-defense`, `card-game`, `visual-novel`, `survival-crafting`, `puzzle`
- **Workflows (4)**: `game-jam`, `prototype-fast`, `steam-publish`, `itch-publish`

### 3.2 `game-feel` Standard Juice Engine (Decaying Trauma Shake + Real-Time Hit-Stop + Squash & Stretch)

```javascript
const Juice = {
  trauma: 0,
  decay: 1.4,
  maxOffset: { x: 14, y: 10 },
  maxRoll: 0.035,
  time: 0,
  hitStopUntil: 0,
  flashAlpha: 0,

  addTrauma(amount) { this.trauma = Math.min(1.0, this.trauma + amount); },
  hitStop(durationMs = 65) { this.hitStopUntil = Math.max(this.hitStopUntil, performance.now() + durationMs); },
  isFrozen() { return performance.now() < this.hitStopUntil; },

  feedback(x, y, tier, spawnParticlesFn, playSfxFn) {
    if (tier === 'small') {
      playSfxFn?.('tick'); this.addTrauma(0.18); spawnParticlesFn?.(x, y, 5, 120);
    } else if (tier === 'medium') {
      playSfxFn?.('hit'); this.addTrauma(0.42); this.hitStop(45); spawnParticlesFn?.(x, y, 12, 220);
    } else if (tier === 'large') {
      playSfxFn?.('boom'); this.addTrauma(0.85); this.hitStop(95); this.flashAlpha = 0.35; spawnParticlesFn?.(x, y, 28, 340);
    }
  },

  updateAndGetCameraOffset(dt) {
    this.time += dt * 32.0;
    this.trauma = Math.max(0, this.trauma - this.decay * dt);
    this.flashAlpha = Math.max(0, this.flashAlpha - dt * 2.5);
    const shake = this.trauma * this.trauma;
    return {
      offsetX: this.maxOffset.x * shake * Math.sin(this.time * 1.7),
      offsetY: this.maxOffset.y * shake * Math.sin(this.time * 2.3),
      rotation: this.maxRoll * shake * Math.sin(this.time * 1.1)
    };
  }
};

function easeOutBack(t) {
  const c1 = 1.70158, c3 = c1 + 1;
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
}
```

### 3.3 Genre Physics & Numerical Baselines
- **Physics Merge / Suika (`puzzle`)**: Gravity `G = 980 px/s^2`, restitution `0.25`, friction `0.92`, `4-6` positional relaxation sub-steps per frame, midpoint tier $T \to T+1$ fusion with `1.3x -> 1.0x` `easeOutBack` pop and `2^(T+1)` score.
- **2D Survivor / Bullet-Heaven (`roguelike`)**: Infinite camera-follow world with modulo-tiled background grid, soft-separation enemy steering, magnetic XP gems (`120px` radius), and 3-card weighted upgrade draft (`Common 60% / Rare 30% / Epic 10%`).
- **Arcade Platformer / Runner (`platformer`)**: Gravity `G = 1800 px/s^2`, `1.4x` fall gravity multiplier, variable jump cut (`vy *= 0.5`), `80ms` coyote time, `100ms` jump buffer, and 3-layer parallax (`0.15x`, `0.45x`, `1.0x`).
- **3D / 2.5D Gate Runner**: Perspective lane tapering (`80%` bottom width to `28%` horizon width), dual choice gates (`+20` vs `x2`), and instant crowd/fire-rate multiplication.

---

## Section 4: `PlayableIntelligence/game-creator` (11 Reference Skills & 11 Slash Commands)

- **11 Reference Skills**: `phaser`, `threejs-game`, `game-assets` (`renderPixelArt` 2D palette matrix renderer), `game-designer` (mandatory Spectacle Events), `game-audio` (Web Audio / Strudel procedural synthesizer), `game-qa` (`window.render_game_to_text()` & `window.advanceTime(ms)`), `game-architecture` (`Constants` + `EventBus` + `GameState.reset()`), `game-deploy`, `playdotfun`, `unity-mcp`, `fetch-tweet`.
- **11 Slash Commands**: `/viral-game`, `/make-game`, `/improve-game`, `/design-game`, `/add-feature`, `/add-assets`, `/retrodiffusion`, `/add-audio`, `/monetize-game`, `/qa-game`, `/review-game`.

---

## Section 5: `Donchitos/Claude-Code-Game-Studios` (49 Studio Agents, 74 Slash Commands, 15 Hooks & 14 Path Rules)

- **Tier 1 Directors (3)**: `creative-director`, `technical-director`, `producer`
- **Tier 2 Department Leads (8)**: `game-designer`, `lead-programmer`, `art-director`, `audio-director`, `narrative-director`, `qa-lead`, `release-manager`, `localization-lead`
- **Tier 3 Specialists (38)**: `gameplay-programmer`, `engine-programmer`, `ai-programmer`, `network-programmer`, `tools-programmer`, `ui-programmer`, `systems-designer`, `level-designer`, `economy-designer`, `ux-designer`, `live-ops-designer`, `technical-artist`, `sound-designer`, `writer`, `world-builder`, `prototyper`, `performance-analyst`, `devops-engineer`, `analytics-engineer`, `security-engineer`, `qa-tester`, `accessibility-specialist`, `community-manager`, plus 14 Godot/Unity/Unreal Engine Sub-Specialists.
- **9 Multi-Agent Team Workflows**: `/team-combat`, `/team-narrative`, `/team-ui`, `/team-polish`, `/team-audio`, `/team-level`, `/team-live-ops`, `/team-qa`, `/team-release`.
- **15 Hooks & 14 Path-Scoped Rules**: Enforce zero magic numbers (`Constants`), mandatory `dt` scaling, zero 60fps hot-loop allocations, UI/physics decoupling, `44x44px` minimum touch targets, and MDA/SDT/Flow alignment.

---

## Section 6: `ybuild-ai/ai-game-art-pipeline-skill` & `video-db/skills`

- **5 Art Pipeline Reference Rules (`ybuild-ai`)**:
  1. `static-assets`: Crop or generate at `2x` display size on `#FF00FF` magenta; strip and trim alpha via `chroma_key_magenta.py`.
  2. `battle-sprites`: Lock canonical idle frame first; normalize bottom-center foot anchor to `(0.5, 1.0)`.
  3. `motion-video`: Extract `startup`, `active`, and `recovery` frame counts from video; keep hitboxes owned by code.
  4. `backgrounds`: Separate into 3 contrast value bands; keep textures `< 2048x2048`.
  5. `runtime-shipping`: Verify zero alpha fringe halos and responsive `9:16` / `16:9` framing.
- **Video Timeline & HUD Masking (`video-db/skills`)**:
  - Segment scenes where `mean_pixel_delta > 42.0`; isolate static HUD bars where temporal variance `< 0.65 * center_playfield_variance`; track OCR score/timer deltas across keyframes.

---

## Section 7: All 15 Embedded Executable Python Scripts

### 7.1 `scripts/analyze_gameplay_video.py` (`video-db/skills` + `ybuild-ai`)

```python
#!/usr/bin/env python3
"""
Analyze a gameplay video using ffprobe/ffmpeg and PIL/numpy.
Produces sampled keyframes, contact_sheet.png, hud_variance_map.png, and telemetry.json.
"""
import argparse, json, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

def get_video_metadata(video_path: str) -> dict:
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
           "-show_entries", "stream=width,height,r_frame_rate,duration,nb_frames",
           "-show_entries", "format=duration", "-of", "json", video_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    stream = data.get("streams", [{}])[0]
    fmt = data.get("format", {})
    width, height = int(stream.get("width", 1280)), int(stream.get("height", 720))
    fps_str = stream.get("r_frame_rate", "30/1")
    fps = round(float(fps_str.split("/")[0]) / max(1.0, float(fps_str.split("/")[1])), 2) if "/" in fps_str else round(float(fps_str), 2)
    duration = float(stream.get("duration") or fmt.get("duration") or 10.0)
    gcd_val = math.gcd(width, height)
    return {
        "width": width, "height": height, "fps": fps, "duration_sec": round(duration, 2),
        "aspect_ratio": f"{width // gcd_val}:{height // gcd_val}",
        "orientation": "portrait (mobile/mini-game)" if height > width else ("square" if height == width else "landscape (desktop/console)")
    }

def extract_frames(video_path: str, out_dir: Path, num_frames: int, duration: float) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    interval = max(0.2, duration / max(1, num_frames))
    extracted = []
    for i in range(num_frames):
        ts = min(max(0.0, i * interval), max(0.0, duration - 0.05))
        fname = f"frame_{i+1:02d}.png"
        fpath = out_dir / fname
        subprocess.run(["ffmpeg", "-y", "-ss", f"{ts:.3f}", "-i", video_path, "-frames:v", "1", "-q:v", "2", str(fpath)], capture_output=True, check=False)
        if fpath.exists():
            extracted.append({"index": i + 1, "timestamp_sec": round(ts, 2), "file": fname, "path": str(fpath)})
    return extracted

def extract_dominant_palette(img_path: str, num_colors: int = 6) -> list[str]:
    img = Image.open(img_path).convert("RGB").resize((120, 120))
    q = img.quantize(colors=num_colors)
    pal = q.getpalette()[: num_colors * 3]
    return [f"#{pal[i]:02x}{pal[i+1]:02x}{pal[i+2]:02x}" for i in range(0, len(pal), 3)]

def compute_motion_and_hud_zones(frames: list[dict], out_dir: Path) -> dict:
    if len(frames) < 2:
        return {"motion_peaks": [], "scene_transitions": [], "detected_static_hud_zones": []}
    arrays = [np.asarray(Image.open(f["path"]).convert("RGB").resize((320, 320)), dtype=np.float32) for f in frames]
    stack = np.stack(arrays, axis=0)
    temporal_std = np.std(stack, axis=0).mean(axis=-1)
    norm_std = (temporal_std / max(1.0, float(temporal_std.max())) * 255.0).astype(np.uint8)
    Image.fromarray(norm_std).save(out_dir / "hud_variance_map.png")
    motion_deltas, scene_transitions = [], []
    for i in range(1, len(arrays)):
        diff = float(np.abs(arrays[i] - arrays[i - 1]).mean())
        entry = {"from_frame": frames[i - 1]["index"], "to_frame": frames[i]["index"], "timestamp_sec": frames[i]["timestamp_sec"], "mean_pixel_delta": round(diff, 2)}
        motion_deltas.append(entry)
        if diff > 42.0:
            scene_transitions.append(entry)
    top_var, mid_var, bot_var = float(temporal_std[:48, :].mean()), float(temporal_std[96:224, :].mean()), float(temporal_std[272:, :].mean())
    hud_zones = []
    if top_var < mid_var * 0.65: hud_zones.append("top_bar_hud")
    if bot_var < mid_var * 0.65: hud_zones.append("bottom_deck_hud")
    return {
        "dominant_color_palette_hex": extract_dominant_palette(frames[len(frames) // 2]["path"]),
        "top_band_variance": round(top_var, 2), "center_playfield_variance": round(mid_var, 2), "bottom_band_variance": round(bot_var, 2),
        "detected_static_hud_zones": hud_zones, "scene_transitions": scene_transitions,
        "motion_peaks": sorted(motion_deltas, key=lambda x: x["mean_pixel_delta"], reverse=True)[:4]
    }

def build_contact_sheet(frames: list[dict], out_path: Path, cols: int = 4) -> None:
    if not frames: return
    w, h = Image.open(frames[0]["path"]).size
    tw, th = 360, max(180, int(h * (360 / max(1, w))))
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * th), (18, 20, 28))
    draw = ImageDraw.Draw(sheet)
    for idx, f in enumerate(frames):
        x0, y0 = (idx % cols) * tw, (idx // cols) * th
        sheet.paste(Image.open(f["path"]).convert("RGB").resize((tw - 8, th - 8)), (x0 + 4, y0 + 4))
        draw.rectangle([x0 + 8, y0 + 8, x0 + 145, y0 + 32], fill=(0, 0, 0))
        draw.text((x0 + 14, y0 + 12), f"#{f['index']:02d} | {f['timestamp_sec']:.2f}s", fill=(255, 230, 80))
    sheet.save(out_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("output_dir")
    parser.add_argument("--frames", type=int, default=16)
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    meta = get_video_metadata(args.video_path)
    frames = extract_frames(args.video_path, out_dir, args.frames, meta["duration_sec"])
    motion_info = compute_motion_and_hud_zones(frames, out_dir)
    build_contact_sheet(frames, out_dir / "contact_sheet.png")
    report = {"video_metadata": meta, "sampled_frames_count": len(frames), "contact_sheet": str(out_dir / "contact_sheet.png"), "hud_variance_map": str(out_dir / "hud_variance_map.png"), "motion_and_hud_analysis": motion_info, "frames": frames}
    (out_dir / "telemetry.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
```

### 7.2 `scripts/orchestrate_subagents.py` (`obra/superpowers` + `sickn33/subagent-orchestrator`)

```python
#!/usr/bin/env python3
"""
Lead-Agent to Parallel-Subagents Mission Orchestrator.
Decomposes a video-to-game replication project into 5 isolated Subagent Context Packets,
creates the SDD recovery ledger (sdd_ledger.md), and executes parallel worker tasks.
"""
import argparse, concurrent.futures, json, time
from pathlib import Path

SUBAGENT_ROSTER = [
    {
        "id": "subagent-01-telemetry-architect",
        "role": "Lead Telemetry & Architecture Specifier",
        "round": 1,
        "depends_on": [],
        "scope_write": ["modules/01_constants_and_bus.js"],
        "scope_read": ["video_analysis/telemetry.json", "video_analysis/contact_sheet.png"],
        "do_not_read": ["node_modules", "dist"],
        "contract_exports": ["Constants", "EventBus", "GameState"],
        "description": "Extract video aspect ratio, color palette, state machine, and emit Constants + EventBus + GameState.reset()."
    },
    {
        "id": "subagent-02-physics-controller",
        "role": "Physics, Controller & Collision Subagent",
        "round": 2,
        "depends_on": ["subagent-01-telemetry-architect"],
        "scope_write": ["modules/02_physics_and_entities.js"],
        "scope_read": ["modules/01_constants_and_bus.js"],
        "do_not_read": ["modules/03_skeletal_and_art.js", "modules/04_hud_and_audio.js"],
        "contract_exports": ["PlayerController", "PhysicsSystem", "EntitySpawner"],
        "description": "Implement delta-time normalized movement, sub-stepped hitboxes (circle/AABB), and enemy/obstacle wave steering."
    },
    {
        "id": "subagent-03-skeletal-art",
        "role": "2D/3D Skeletal Rig, Shaders & VFX Subagent",
        "round": 2,
        "depends_on": ["subagent-01-telemetry-architect"],
        "scope_write": ["modules/03_skeletal_and_art.js"],
        "scope_read": ["modules/01_constants_and_bus.js"],
        "do_not_read": ["modules/02_physics_and_entities.js", "modules/04_hud_and_audio.js"],
        "contract_exports": ["SkeletalRig", "solveTwoBoneIK", "ParticleSystem", "Juice"],
        "description": "Build hierarchical 2D Spine/Rive or 3D joint rigs, 2-bone analytic IK, trauma^2 shake, hit-stop, and squash-stretch."
    },
    {
        "id": "subagent-04-hud-audio",
        "role": "HUD Safe-Zone UI & Procedural Web Audio Subagent",
        "round": 2,
        "depends_on": ["subagent-01-telemetry-architect"],
        "scope_write": ["modules/04_hud_and_audio.js"],
        "scope_read": ["modules/01_constants_and_bus.js"],
        "do_not_read": ["modules/02_physics_and_entities.js", "modules/03_skeletal_and_art.js"],
        "contract_exports": ["HUDRenderer", "AudioSynth", "TuningDrawer"],
        "description": "Build responsive HUD bars, floating damage numbers, live parameter tuning drawer, and Web Audio synthesizer SFX."
    },
    {
        "id": "subagent-05-qa-integrator",
        "role": "Two-Stage Spec & Code Quality Reviewer + Assembler",
        "round": 3,
        "depends_on": ["subagent-02-physics-controller", "subagent-03-skeletal-art", "subagent-04-hud-audio"],
        "scope_write": ["modules/05_integration_report.json"],
        "scope_read": ["modules/01_constants_and_bus.js", "modules/02_physics_and_entities.js", "modules/03_skeletal_and_art.js", "modules/04_hud_and_audio.js"],
        "do_not_read": [],
        "contract_exports": ["window.render_game_to_text", "window.advanceTime"],
        "description": "Run 3-point spot checks (scope, contract exports, zero TODO placeholders) and verify whole-branch integration."
    }
]

def write_context_packet(project_dir: Path, agent: dict, game_title: str) -> Path:
    packet_dir = project_dir / "context_packets"
    packet_dir.mkdir(parents=True, exist_ok=True)
    packet_file = packet_dir / f"{agent['id']}-brief.md"
    content = (
        f"# AGENT CONTEXT PACKET - {agent['id']}\n"
        f"- **Game Project**: {game_title}\n"
        f"- **Role**: {agent['role']}\n"
        f"- **Execution Round**: Round {agent['round']}\n"
        f"- **Files to Read**: {', '.join(agent['scope_read']) or 'None'}\n"
        f"- **Files to Write**: {', '.join(agent['scope_write'])}\n"
        f"- **Do NOT Read**: {', '.join(agent['do_not_read']) or 'None'}\n"
        f"- **Required Contract Exports**: {', '.join(agent['contract_exports'])}\n"
        f"- **Task Specification**: {agent['description']}\n"
    )
    packet_file.write_text(content, encoding="utf-8")
    return packet_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default="./subagent_workspace")
    parser.add_argument("--game-title", default="Replicated Game")
    args = parser.parse_args()
    proj = Path(args.project_dir)
    proj.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(write_context_packet, proj, ag, args.game_title): ag for ag in SUBAGENT_ROSTER}
        packets = {futures[f]["id"]: str(f.result()) for f in concurrent.futures.as_completed(futures)}
    (proj / "mission_brief.json").write_text(json.dumps({"goal": args.game_title, "agents": SUBAGENT_ROSTER, "context_packets": packets}, indent=2, ensure_ascii=False), encoding="utf-8")
    (proj / "sdd_ledger.md").write_text(f"# SDD Ledger - {args.game_title}\n- Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n", encoding="utf-8")

if __name__ == "__main__":
    main()
```

### 7.3 `scripts/swarm_task_board.py` (`kieranklaassen/orchestrating-swarms`)

```python
#!/usr/bin/env python3
"""Swarm DAG Task Board & Teammate Inbox Coordinator with blockedBy auto-unblocking."""
import argparse, json, time
from pathlib import Path

DEFAULT_TASKS = [
    {"id": "1", "subject": "Telemetry & EventBus Contract", "owner": "subagent-01-telemetry-architect", "status": "pending", "blockedBy": []},
    {"id": "2", "subject": "Physics, Controller & Hitbox Loop", "owner": "subagent-02-physics-controller", "status": "pending", "blockedBy": ["1"]},
    {"id": "3", "subject": "2D/3D Skeletal Rig, IK & Juice VFX", "owner": "subagent-03-skeletal-art", "status": "pending", "blockedBy": ["1"]},
    {"id": "4", "subject": "HUD Safe-Zones, Audio Synth & Tuning Drawer", "owner": "subagent-04-hud-audio", "status": "pending", "blockedBy": ["1"]},
    {"id": "5", "subject": "Two-Stage Review & Single-File HTML Assembly", "owner": "subagent-05-qa-integrator", "status": "pending", "blockedBy": ["2", "3", "4"]},
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board", default="./subagent_workspace/swarm_board.json")
    parser.add_argument("action", choices=["init", "complete", "status"])
    parser.add_argument("--task-id", default="1")
    parser.add_argument("--agent", default="subagent-01")
    parser.add_argument("--summary", default="Completed module specification.")
    args = parser.parse_args()
    bpath = Path(args.board)
    bpath.parent.mkdir(parents=True, exist_ok=True)
    if args.action == "init":
        bpath.write_text(json.dumps({"team_name": "gameplay-cloner-swarm", "tasks": DEFAULT_TASKS, "messages": []}, indent=2, ensure_ascii=False), encoding="utf-8")
    elif args.action == "complete":
        data = json.loads(bpath.read_text(encoding="utf-8"))
        unblocked = []
        for t in data["tasks"]:
            if t["id"] == args.task_id:
                t["status"] = "completed"
        for t in data["tasks"]:
            if args.task_id in t.get("blockedBy", []):
                t["blockedBy"].remove(args.task_id)
                if not t["blockedBy"] and t["status"] == "pending":
                    unblocked.append(t["id"])
        data["messages"].append({"type": "task_completed", "from": args.agent, "taskId": args.task_id, "unblockedTasks": unblocked, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")})
        bpath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"completed": args.task_id, "auto_unblocked": unblocked}, ensure_ascii=False))
    elif args.action == "status":
        print(bpath.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
```

### 7.4 `scripts/merge_subagent_modules.py` (`sickn33/subagent-orchestrator`)

```python
#!/usr/bin/env python3
"""3-Point Spot-Check & Parallel Subagent Module Assembler."""
import argparse, json, re, sys
from pathlib import Path

FORBIDDEN_PLACEHOLDERS = [r"\bTODO\b", r"\bFIXME\b", r"implement later", r"placeholder only"]

def audit_module(path: Path) -> dict:
    if not path.exists():
        return {"file": str(path), "exists": False, "clean": False, "issues": ["File missing"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    issues = [f"Forbidden placeholder: {pat}" for pat in FORBIDDEN_PLACEHOLDERS if re.search(pat, text, re.IGNORECASE)]
    return {"file": str(path), "exists": True, "bytes": len(text), "clean": len(issues) == 0, "issues": issues}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    results = [audit_module(Path(f)) for f in args.files]
    all_clean = all(r["clean"] for r in results)
    print(json.dumps({"all_subagents_clean": all_clean, "results": results}, indent=2, ensure_ascii=False))
    if not all_clean:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 7.5 `scripts/position_parts.py` (`GenielabsOpenSource/spine-animation-ai`)

```python
#!/usr/bin/env python3
"""Auto-position separated 2D character body-part PNGs onto an assembled reference image."""
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image

def find_part_position(ref_arr: np.ndarray, part_arr: np.ndarray) -> dict:
    ref_h, ref_w = ref_arr.shape[:2]
    ph, pw = part_arr.shape[:2]
    mask = (part_arr[:, :, 3] > 24).astype(np.float32)
    if mask.sum() < 10 or ph > ref_h or pw > ref_w:
        return {"x": ref_w / 2.0, "y": ref_h / 2.0, "width": pw, "height": ph, "scale": 1.0, "rotation": 0.0}
    best_score, best_x, best_y = -1e9, (ref_w - pw) // 2, (ref_h - ph) // 2
    part_rgb, ref_rgb = part_arr[:, :, :3].astype(np.float32), ref_arr[:, :, :3].astype(np.float32)
    denom = float(mask.sum() * 3.0)
    for y in range(0, max(1, ref_h - ph), 4):
        for x in range(0, max(1, ref_w - pw), 4):
            diff = np.abs(ref_rgb[y:y+ph, x:x+pw] - part_rgb) * mask[:, :, None]
            score = -float(diff.sum()) / denom
            if score > best_score:
                best_score, best_x, best_y = score, x, y
    return {"x": round(best_x + pw / 2.0, 2), "y": round(best_y + ph / 2.0, 2), "width": pw, "height": ph, "scale": 1.0, "rotation": 0.0}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--parts", required=True)
    parser.add_argument("--output", default="layout.json")
    args = parser.parse_args()
    ref_img = Image.open(args.reference).convert("RGBA")
    ref_arr = np.asarray(ref_img)
    parts_out, draw_order = {}, []
    for pfile in sorted(Path(args.parts).glob("*.png")):
        parts_out[pfile.stem] = find_part_position(ref_arr, np.asarray(Image.open(pfile).convert("RGBA")))
        draw_order.append(pfile.stem)
    Path(args.output).write_text(json.dumps({"reference_width": ref_img.width, "reference_height": ref_img.height, "parts": parts_out, "draw_order": draw_order}, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
```

### 7.6 `scripts/build_spine_json.py` (`GenielabsOpenSource/spine-animation-ai`)

```python
#!/usr/bin/env python3
"""Build Spine 4.2 skeleton.json with 16-bone humanoid hierarchy and 6 animation presets."""
import argparse, json
from pathlib import Path

BEZIER = [0.25, 0.0, 0.75, 1.0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="skeleton.json")
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    w, h = cfg.get("reference_width", 500), cfg.get("reference_height", 800)
    bones = [
        {"name": "root", "x": 0, "y": 0},
        {"name": "hip", "parent": "root", "x": 0, "y": round(h * 0.42, 1), "length": 40},
        {"name": "torso", "parent": "hip", "x": 0, "y": 35, "length": 85},
        {"name": "head", "parent": "torso", "x": 0, "y": 90, "length": 60},
        {"name": "left-arm", "parent": "torso", "x": -45, "y": 75, "length": 65},
        {"name": "right-arm", "parent": "torso", "x": 45, "y": 75, "length": 65},
        {"name": "left-leg", "parent": "hip", "x": -22, "y": -10, "length": 80},
        {"name": "right-leg", "parent": "hip", "x": 22, "y": -10, "length": 80},
    ]
    animations = {
        "idle": {"bones": {"hip": {"translate": [{"time": 0.0, "y": 0, "curve": BEZIER}, {"time": 1.0, "y": 3.5, "curve": BEZIER}, {"time": 2.0, "y": 0}]}, "torso": {"rotate": [{"time": 0.0, "value": 0}, {"time": 1.0, "value": 1.4}, {"time": 2.0, "value": 0}]}, "head": {"rotate": [{"time": 0.0, "value": 0}, {"time": 0.6, "value": -1.8}, {"time": 1.5, "value": 1.8}, {"time": 2.0, "value": 0}]}}},
        "walk": {"bones": {"hip": {"translate": [{"time": 0.0, "y": 0}, {"time": 0.2, "y": 5.0}, {"time": 0.4, "y": 0}, {"time": 0.6, "y": 5.0}, {"time": 0.8, "y": 0}]}, "left-leg": {"rotate": [{"time": 0.0, "value": 24}, {"time": 0.4, "value": -24}, {"time": 0.8, "value": 24}]}, "right-leg": {"rotate": [{"time": 0.0, "value": -24}, {"time": 0.4, "value": 24}, {"time": 0.8, "value": -24}]}}},
        "run": {"bones": {"hip": {"translate": [{"time": 0.0, "y": -3}, {"time": 0.125, "y": 8}, {"time": 0.25, "y": -3}, {"time": 0.375, "y": 8}, {"time": 0.5, "y": -3}]}, "left-leg": {"rotate": [{"time": 0.0, "value": 42}, {"time": 0.25, "value": -42}, {"time": 0.5, "value": 42}]}, "right-leg": {"rotate": [{"time": 0.0, "value": -42}, {"time": 0.25, "value": 42}, {"time": 0.5, "value": -42}]}}},
        "attack": {"bones": {"torso": {"rotate": [{"time": 0.0, "value": 0}, {"time": 0.2, "value": 12}, {"time": 0.35, "value": -18}, {"time": 0.6, "value": 0}]}, "right-arm": {"rotate": [{"time": 0.0, "value": 0}, {"time": 0.2, "value": 65}, {"time": 0.35, "value": -75}, {"time": 0.6, "value": 0}]}}},
        "jump": {"bones": {"hip": {"translate": [{"time": 0.0, "y": 0}, {"time": 0.2, "y": -14}, {"time": 0.5, "y": 48}, {"time": 0.8, "y": -10}, {"time": 1.0, "y": 0}]}}},
        "wave": {"bones": {"right-arm": {"rotate": [{"time": 0.0, "value": 0}, {"time": 0.25, "value": -125}, {"time": 0.5, "value": -95}, {"time": 0.75, "value": -125}, {"time": 1.2, "value": 0}]}}}
    }
    Path(args.output).write_text(json.dumps({"skeleton": {"spine": "4.2", "width": w, "height": h}, "bones": bones, "slots": [], "skins": [], "animations": animations}, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
```

### 7.7 `scripts/make_atlas.py` & `scripts/generate_spine_player.py` (`GenielabsOpenSource/spine-animation-ai`)

```python
#!/usr/bin/env python3
"""Pack separated body-part PNGs into a Spine .atlas + .png spritesheet."""
import argparse
from pathlib import Path
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts", required=True)
    parser.add_argument("--output", default=".")
    parser.add_argument("--name", default="skeleton")
    args = parser.parse_args()
    pfiles = sorted(Path(args.parts).glob("*.png"))
    if not pfiles: return
    imgs = [(p.stem, Image.open(p).convert("RGBA")) for p in pfiles]
    pad = 4
    total_w, total_h = max(im.width for _, im in imgs) + pad * 2, sum(im.height + pad for _, im in imgs) + pad
    atlas_img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    lines = [f"{args.name}.png", f"size: {total_w},{total_h}", "format: RGBA8888", "filter: Linear,Linear", "repeat: none"]
    y_cursor = pad
    for name, im in imgs:
        atlas_img.paste(im, (pad, y_cursor))
        lines.extend([name, "  rotate: false", f"  xy: {pad}, {y_cursor}", f"  size: {im.width}, {im.height}", f"  orig: {im.width}, {im.height}", "  offset: 0, 0", "  index: -1"])
        y_cursor += im.height + pad
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    atlas_img.save(out_dir / f"{args.name}.png")
    (out_dir / f"{args.name}.atlas").write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
```

### 7.8 `scripts/extract_video_frames.py`, `scripts/chroma_key_magenta.py`, `scripts/sheet_contact.py`, `scripts/extract_sprites.py` (`ybuild-ai`)

```python
#!/usr/bin/env python3
"""Remove solid magenta (#FF00FF) or custom chroma key backgrounds and auto-trim transparent borders."""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--key", default="255,0,255")
    parser.add_argument("--tolerance", type=int, default=45)
    parser.add_argument("--trim", action="store_true")
    args = parser.parse_args()
    img = Image.open(args.input).convert("RGBA")
    arr = np.asarray(img, dtype=np.float32)
    key = np.array([int(x.strip()) for x in args.key.split(",")], dtype=np.float32)
    dist = np.linalg.norm(arr[:, :, :3] - key, axis=-1)
    inner = max(0.0, float(args.tolerance) * 0.75)
    alpha_factor = np.clip((dist - inner) / max(1.0, float(args.tolerance) - inner), 0.0, 1.0)
    arr[:, :, 3] *= alpha_factor
    out_img = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    if args.trim and out_img.getbbox():
        out_img = out_img.crop(out_img.getbbox())
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out)

if __name__ == "__main__":
    main()
```

### 7.9 `scripts/validate_architecture.py` (`PlayableIntelligence/game-creator` + `Claude-Code-Game-Studios`)

```python
#!/usr/bin/env python3
"""Validate generated HTML5/JS game replica against PlayableIntelligence & Claude-Code-Game-Studios QA hooks."""
import argparse, json, re, sys
from pathlib import Path

def validate_html_game(file_path: Path) -> dict:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    checks = {
        "has_constants_or_config": bool(re.search(r"\b(Constants|CONFIG|PALETTE)\b", text)),
        "has_state_reset": bool(re.search(r"\b(reset|initGame|restartGame|GameState)\b", text)),
        "has_request_animation_frame": "requestAnimationFrame" in text,
        "has_delta_time_normalization": bool(re.search(r"\b(dt|deltaTime|delta)\b", text)),
        "has_dual_input_listeners": bool(re.search(r"(pointerdown|mousedown|touchstart)", text)) and bool(re.search(r"(keydown|ArrowLeft|KeyA)", text)),
        "has_trauma_or_screen_shake": bool(re.search(r"(trauma|shake|hitStop)", text, re.IGNORECASE)),
        "has_web_audio_synth": bool(re.search(r"(AudioContext|webkitAudioContext)", text)),
        "has_render_game_to_text": "render_game_to_text" in text,
    }
    passed = sum(1 for v in checks.values() if v)
    return {"file": str(file_path), "score": f"{passed}/{len(checks)}", "passed_all": passed >= len(checks) - 1, "checks": checks}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("game_file")
    args = parser.parse_args()
    p = Path(args.game_file)
    if not p.exists():
        print(json.dumps({"error": f"File not found: {p}"}))
        sys.exit(1)
    print(json.dumps(validate_html_game(p), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```
