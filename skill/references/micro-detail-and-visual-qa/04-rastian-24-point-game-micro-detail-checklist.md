# 04 — 24-Point Game Micro-Detail & Micro-Interaction Checklist (`rastian/interaction-design-skills`)

## Sources
- [`rastian/interaction-design-skills`](https://github.com/rastian/interaction-design-skills/blob/main/SKILL.md)
- [`Huc91/pixel-perfect-skill`](https://github.com/Huc91/pixel-perfect-skill)

## The 24 Micro-Details Most Frequently Missed in Game Clones (Audit Before Delivery)

### A. HUD & Icon Micro-Details (1–6)
1. **Notification Red Dots & Count Badges**: Small corner badges (`1`, `!`, `NEW`) on shop/skill/backpack icons.
2. **Currency Icon Inner Highlights**: Gold coin bevels, gem facets, and energy lightning glow (never flat single-color circles).
3. **Bar Sub-Layers**: HP/XP bars must include **4 layers**: dark trough background, delayed white/yellow damage-drain ghost bar, main gradient fill, and top specular highlight strip.
4. **Segmented Bar Ticks**: Vertical tick dividers every `25%` or `100 HP` inside health/shield bars.
5. **Avatar Frame Ornaments**: Level pill badge overlapping the avatar bottom border + VIP/elemental corner emblem.
6. **Tabular Numerals & Text Outlines**: Game numbers (`font-variant-numeric: tabular-nums`) with `1.5px–2px` dark outer stroke (`-webkit-text-stroke` or Canvas `strokeText`) + `0 2px 0 #000` hard drop shadow so numbers stay crisp over busy arenas.

### B. Button & Card Surface Polish (7–12)
7. **3-Layer Game Button Depth**: Top 1px inner highlight (`rgba(255,255,255,0.45)`), main gradient body, and bottom `3px–4px` 3D lip (`border-bottom` or box-shadow) that compresses on press (`translateY(2px)`).
8. **Rarity Card Frames**: Distinct border color + corner glow for Common (Gray), Rare (Blue), Epic (Purple), and Legendary (Gold).
9. **Cost & Requirement Sub-Labels**: Mana drop / coin icon + cost number tucked inside the bottom edge of skill/upgrade buttons.
10. **Cooldown Radial Sweep & Countdown**: Semi-transparent dark radial fan (`conic-gradient`) + live `0.1s` countdown number on active skills.
11. **Locked / Disabled State**: Desaturated grayscale filter (`filter: grayscale(0.85)`) + padlock micro-icon + unlock condition label (`Lv.5`).
12. **Active / Selected Breathing Glow**: Pulsing outer border or rotating dashed ring on the currently selected tower/hero/card.

### C. Arena, Character & Environment Micro-Details (13–18)
13. **Contact Ground Shadows**: Soft dark ellipse (`rgba(0,0,0,0.35)`) directly underneath every character, enemy, and drop item (scales smaller when jumping).
14. **Sprite Idle Breathing & Bobbing**: Continuous sinusoidal scale/Y-offset (`scaleY(1.03)` at `2.5Hz`) so idle entities never look like frozen statues.
15. **Directional Facing & Flip**: Smooth horizontal flip (`scaleX(-1)`) with brief turn squash when changing movement or attack direction.
16. **Ground Prop & Tile Variety**: Subtle cracks, grass tufts, grid lines, or ambient dust motes so the arena floor isn't a flat `#hex` rectangle.
17. **Range & Target Indicators**: Translucent ground circle showing attack/placement radius + target reticle under locked enemies.
18. **Collectible Magnet Arc**: Coins/gems pop upward with gravity bounce, pause `120ms`, then curve along a Bezier trajectory into the top HUD counter.

### D. Combat Juice & Micro-Interactions (19–24)
19. **1-Frame White Hit-Flash**: Target sprite flashes pure white (`globalCompositeOperation = 'source-atop'` or brightness filter) for `50ms–70ms` on impact.
20. **Hit-Stop (Frame Freeze)**: `30ms–50ms` micro-pause on heavy/critical hits before knockback velocity applies.
21. **Tiered Floating Damage Text**: Normal hits (white, small upward float) vs. Critical hits (`1.5x` scale burst, gold/red gradient, `!` suffix, slight horizontal scatter).
22. **Muzzle Flash & Impact Ring**: Expanding 3-frame shockwave ring + 6–10 directional spark particles at the exact collision point.
23. **HUD Counter Bounce**: When a collected coin/gem reaches the HUD counter, the icon and text scale to `1.25x` for `100ms` (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
24. **Audio-Visual Sync**: Subtle low-pass filter or pitch randomization (`0.92x–1.08x`) on rapid repeated hit/coin SFX so micro-events never sound robotic.
