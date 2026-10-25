# 02 — Multi-Agent Swarm Orchestration & Two-Stage SDD Review (`superpowers` + `orchestrating-swarms` + `subagent-orchestrator`)

## Sources
- [`obra/superpowers`](https://github.com/obra/superpowers) (*Parallel Subagent Dispatch & Two-Stage SDD Review*)
- [`kieranklaassen/orchestrating-swarms`](https://github.com/kieranklaassen/orchestrating-swarms) & [`sickn33/antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills)
- [`qodex-ai/multi-agent-orchestration`](https://github.com/qodex-ai/multi-agent-orchestration) & [`VoltAgent/awesome-claude-code-subagents`](https://github.com/VoltAgent/awesome-claude-code-subagents)

## 3-Round Parallel Specialist Swarm (`scripts/spine_and_swarm_pipeline.py init-swarm`)
1. **Round 1 (Foundation & Contracts — `subagent-01-telemetry`)**:
   - Locks `Constants`, `EventBus`, `GameState` schema, and `rolling_state_ledger.json`.
2. **Round 2 (Parallel Specialist Fan-Out — DAG Unblocked)**:
   - **`subagent-02-physics-controller`**: Core loop, collision engine, `WaveDirector`, and fitted economy curves.
   - **`subagent-03-skeletal-art`**: 2D/3D skeletal IK rigs, `trauma^2` camera shake, real-time `hit_stop`, and particle emitters.
   - **`subagent-04-hud-audio`**: 4-layer HP/XP bars, 3D button lips, procedural Web Audio synth SFX, and `⚙️ 参数微调` live tuning drawer.
3. **Round 3 (Fan-In Spot-Check & Visual Verdict Gate — `subagent-05-qa-integrator`)**:
   - Verifies `window.render_game_to_text()`, runs `validate_architecture.py`, and executes `visual_verdict_diff_loop.py` until `Composite Score >= 90.0`.
