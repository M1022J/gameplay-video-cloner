# 03 · Workflow & Swarm Architecture

## The 3-round pipeline

### Round 1 (Foundation): video telemetry + contract lock + decomposition
- `analyze_gameplay_video.py` samples keyframes: a 16-frame contact sheet, a temporal
  variance map (static HUD bands vs. the active playfield), scene cuts
  (mean pixel delta > 42.0), and a 6-color dominant palette, summarized in `telemetry.json`
- Lock the shared contract: `Constants` (aspect, palette, speeds, safe zones), `EventBus`
  (on_hit / on_merge / on_pickup / on_land / on_level_up / on_death), and `GameState`
  (with a deterministic `reset()` and a `window.render_game_to_text()` self-check hook)
- `orchestrate_subagents.py` writes 5 isolated subagent context packets;
  `swarm_task_board.py` builds the DAG board: finishing Task 1 auto-unblocks Tasks 2/3/4,
  and finishing those unblocks Task 5

### Round 2 (Parallel fan-out): three specialists at once
| Subagent | Owns | Key rules |
|---|---|---|
| subagent-02 physics/controller | movement, collision (circle/AABB, 4–6 relaxation sub-steps), wave director | dt-normalized; 80ms coyote time, 100ms jump buffer (platformers) |
| subagent-03 skeletal/art | 2D Spine/Rive rigs or 3D procedural rigs, two-bone IK, Juice, particles | EventBus only; camera shake touches render transform, never physics coords |
| subagent-04 HUD/audio | score/health bars inside HUD safe zones, popups, tuning drawer, Web Audio synth | touch targets ≥44×44px; audio unlocks on gesture |

### Round 3 (Fan-in): two-stage review + assembly
- Stage 1, spec compliance: every mechanic / bone state / HUD element from the video is
  implemented; zero TODO/FIXME placeholders
- Stage 2, code quality: frame-rate independence, zero hot-loop allocation (object pools), clean reset
- 3-point spot check (`merge_subagent_modules.py`): stayed in namespace, exports match the
  contract, no placeholders
- Architecture gate (`validate_architecture.py`): 8 checks, ≥7 must pass (integration sample scored 8/8)
- Consensus balancing audit: hitboxes at 75–80% of visual size, 0% softlock rate, contrast vs. source video

## The 5-subagent contract matrix

| ID | Role | Owned namespace | Exports |
|---|---|---|---|
| lead-orchestrator | coordinator / producer | Constants, EventBus, GameState, main | initGame(), render_game_to_text() |
| subagent-01-telemetry | video analyst / systems designer | TelemetrySpec | Constants, STAGE_CONFIG, HUD_SAFE_ZONES |
| subagent-02-physics | gameplay / AI programmer | PlayerController, PhysicsSystem, WaveDirector | on_hit and other events |
| subagent-03-skeletal | technical artist / animator | SkeletalRig, Juice, ParticleSystem | renderRig(), Juice.feedback() |
| subagent-04-hud-audio | UI / sound designer | HUDRenderer, AudioSynth, TuningDrawer | renderHUD(), playSfx() |

## Upstream basis

obra/superpowers (isolated packets + two-stage review + SDD recovery ledger), Kieran
Klaassen's swarm Gist (Leader + Teammates + blockedBy DAG), sickn33's subagent-orchestrator
(6 phases + 3-point spot check), qodex-ai multi-agent-orchestration and the VoltAgent
subagent catalog (topologies and role matrix). Full texts live under `upstream/`.
