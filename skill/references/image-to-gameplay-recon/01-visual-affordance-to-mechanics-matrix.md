# How to Reverse-Engineer Gameplay Mechanics from Static Images (`Visual Affordance & Semiotics Matrix`)

When the user provides only 1 to 3 screenshots (or when inspecting static keyframes extracted from a video), deduce the complete playable rule set using this **6-Dimension Visual Semiotics Inference Matrix**:

## 1. HUD Numerals, Bars & Badges -> Core Economy & Win/Lose Rules

| Visual Cue in Screenshot | Inferred Underlying System & Mathematical Rule |
| :--- | :--- |
| **Top Progress Bar with Stage/Skull Nodes (`Wave 4/10`, `Boss`)** | Wave Director state machine: spawn `N` enemies per wave; filling bar triggers Boss phase or 3-card roguelike draft modal |
| **`Lv.X` + Horizontal Cyan/Green Bar at Top** | XP Gem Magnet + Auto-Leveling loop: enemies drop gems; `XP_req(L) = round(10 * 1.35^L)` triggers `LEVEL_UP_CHOICE` |
| **Fraction Counter (`14/20`, `Moves: 12`, `7-Slot Dock`)** | Capacity or Turn-Limited Puzzle constraint: exceeding dock capacity (`7/7` unmatched) or reaching `Moves == 0` triggers `GAME_OVER` |
| **Danger Dashed Line Near Top (`15%-20%` Y)** | Physics Overflow Timer (`Suika` / Drop-Merge / Tetris): any body resting above `dangerY` for `> 2.0s` triggers `GAME_OVER` |
| **`Combo x12` / `FEVER!` / Multiplier Ring** | Decay Timer Multiplier: each match/hit resets a `2.5s` decay bar and increments score multiplier `M = min(10, 1 + floor(combo/3))` |
| **Currency Badges (`Coins`, `Gems`, `+150/s`)** | Tycoon / Idle / Shop Upgrade sink: bind to upgrade buttons with exponential cost `Cost(L) = Base * 1.18^L` |

## 2. Playfield Spatial Geometry -> Physics & Movement Engine

| Playfield Layout in Screenshot | Inferred Physics & Collision Engine |
| :--- | :--- |
| **Center Hero Surrounded by Radial Hordes + Floating Weapons** | **2D Survivor / Bullet-Heaven**: Infinite camera-follow arena (`cam = player - screen/2`), radial auto-targeting cooldowns, flocking separation steering |
| **Walled Container + Assorted Sized Circles/Fruits** | **2D Sub-Stepped Physics Merge (`Suika`)**: Gravity `G = 980`, `4-6` relaxation sub-steps, circle-circle collision (`dist < r1 + r2`), identical tier `T + T -> T+1` midpoint fusion |
| **Orthogonal `N x M` Board + Bottom 3-Piece / 7-Slot Tray** | **Grid Puzzle (`Block Blast` / `Match-3` / `Triple-Match`)**: Pointer drag with `0.25` lerp snap to `(col, row)`, row/col or 3-of-a-kind clear, cascade gravity |
| **Side-View Ledges, Spikes, Coins & Parallax Horizon** | **2D Arcade Platformer / Runner**: Gravity `1800`, fall multiplier `1.4x`, variable jump cut, `80ms` coyote time, `100ms` jump buffer |
| **Tapering 3D/2.5D Road + Dual Colored Math Gates (`+15` vs `x2`)** | **Hyper-Casual Gate/Crowd Runner**: Horizontal drag steering `x in [-laneW, +laneW]`, forward Z-scroll, gate collision mutating entity count or fire rate |
| **Winding Path + Turret Sockets + Enemy HP Bars** | **Tower Defense**: Waypoint polyline pathing, socket click-to-build/upgrade, range circle targeting (`First`/`Strongest`) |

## 3. Control Overlays & Cursors -> Input Binding Spec

- **Bottom-Left Virtual Joystick Ring + Bottom-Right Action Buttons**: Bind both pointer-drag virtual joystick AND `WASD`/Arrow keys + `Space`/`J`/`K` hotkeys.
- **Dotted Trajectory Arc / Slingshot Pull Line**: Bind `pointerdown` anchor -> `pointermove` vector `(dx, dy)` with parabolic preview dots `(x0 + vx*t, y0 + vy*t + 0.5*g*t^2)` -> `pointerup` projectile launch.
- **Draggable Cards / Hand Fan at Bottom**: Bind hover elevation tween (`y - 18px`, `scale 1.08`) + drag-to-playfield release threshold.
