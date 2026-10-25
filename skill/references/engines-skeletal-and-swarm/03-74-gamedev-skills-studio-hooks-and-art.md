# 03 — 74 Game-Dev Skills, 49 Studio Agents & Art Pipeline Standards (`awesome-gamedev` + `Claude-Code-Game-Studios` + `PlayableIntelligence` + `ybuild-ai`)

## Sources
- [`gamedev-skills/awesome-gamedev-agent-skills`](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) (74 Engine, Discipline & Genre Skills)
- [`Donchitos/Claude-Code-Game-Studios`](https://github.com/Donchitos/Claude-Code-Game-Studios) (49 Studio Agents, 15 Safety Hooks & 14 Path-Scoped Rules)
- [`PlayableIntelligence/game-creator`](https://github.com/PlayableIntelligence/game-creator) & [`ybuild-ai/ai-game-art-pipeline-skill`](https://github.com/ybuild-ai/ai-game-art-pipeline-skill)

## Core Production Rules Consolidated Across All 4 Suites
1. **Exclusive Engine Routing**: Load only the active engine stack (`HTML5 Canvas / Phaser 4.2 / PixiJS 8 / Three.js r186`, `Godot 4.7`, `Unity 6.3`, or `Unreal 5.8`).
2. **15 Studio Safety Hooks**: Centralize all magic numbers in `Constants`; normalize all physics/animations by `dt` seconds (`60Hz/120Hz` parity); zero object allocations inside the `requestAnimationFrame` hot loop; decouple UI from physics via `EventBus`.
3. **Art & Sprite Hygiene (`scripts/process_and_audit_sprites.py`)**: Separate background into 3 contrast bands; anchor character sprites at bottom-center `(0.5, 1.0)`; clean `#FF00FF` chroma backgrounds and enforce `corner_alpha_max <= 12` (`transparent_bg_ok == True`).
4. **Machine-Checkable Playtest Hook**: Expose `window.render_game_to_text()` returning live JSON state (`state`, `score`, `level`, `player`, `entities_count`) and support instant in-place restart (`GameState.reset()`).
