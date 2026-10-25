# 13-Section GDD Synthesis & Visual Playtest Loop (`Yakoub-ai/phaser4-gamedev` + `kursku` + `caucy2026`)

Distilled from `Yakoub-ai/phaser4-gamedev` (`/phaser-gdd`), `kursku/skills/blob/master/frontend/develop-web-game/SKILL.md`, and `caucy2026/skills/blob/main/game-playtest/SKILL.md`.

## 1. Rapid 13-Point Game Design Spec from Visuals (`/phaser-gdd`)
When reverse-engineering a game from image(s) or video frames, synthesize these 13 parameters before coding:
1. **Viewport & Aspect Ratio** (`9:16` portrait vs `16:9` landscape)
2. **Core Player Verb** (Drag-and-drop, Aim-and-shoot, Tap-to-jump, Twin-stick dodge, Tile-match)
3. **Primary Core Loop** (Action -> Immediate Feedback -> Resource/Score Gain -> Upgrade/Escalation)
4. **Win & Lose Conditions** (HP == 0, Overflow line crossed for 2s, Timer == 0, Wave 10 Boss defeated)
5. **Entity Roster & Hitboxes** (Player, 3+ Enemy/Obstacle tiers, Projectiles, Pickups)
6. **Physics & Easing Math** (Gravity, restitution, drag, `easeOutBack` pop)
7. **Progression & Economy Formula** (XP curve, combo multiplier, shop costs)
8. **State Machine Transitions** (`READY -> PLAYING -> LEVEL_UP / PAUSE -> GAME_OVER`)
9. **HUD Wireframe & Safe Zones** (Top bar, bottom tray, floating popups)
10. **2D/3D Skeletal Animation States** (`idle`, `move`, `attack`, `hit`, `death`)
11. **Game-Feel Juice Spec** (`trauma^2` shake, `hit_stop_ms`, `hit_flash`, particle bursts)
12. **Procedural Web Audio Cues** (`hit`, `pickup`, `merge`, `levelup`, `gameover`)
13. **Machine-Checkable Acceptance Criteria** (`window.render_game_to_text()` state assertions)

## 2. Exhaustive Control & Visual Playtest Loop (`kursku/develop-web-game` + `caucy2026/game-playtest`)
- Verify the UI layer independently from the canvas render layer so HUD buttons never block playfield pointer events unnecessarily.
- Exercise every main verb (`move`, `action`, `upgrade`, `restart`) and verify that `window.render_game_to_text()` reflects live coordinates, scores, and active entity counts accurately.
