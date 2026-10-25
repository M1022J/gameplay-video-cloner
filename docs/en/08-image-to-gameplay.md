# 08 · Image-to-Gameplay Reverse Engineering (v3 supplement)

## The problem it solves
The first two editions needed video. V3 makes a single screenshot a valid starting
point: reverse-engineer the rules from a static image, generate a verifiable spec
and feature matrix, then score the finished clone pixel-by-pixel for parity.

## Pipeline (bolted onto the start of Round 1 and the end of Round 3)
1. **Visual affordance matrix** (reference 01): map on-screen elements to mechanics
   semiotically — interactables, hazards, collectibles, HUD state.
2. **Clean-room recon** (Jakeschincariol/replica-skill's replica-recon/design):
   image only, no source code; outputs a feature inventory and spec (what
   `infer_gameplay_from_image.py` writes as recon_gameplay_spec.json + features.csv).
3. **Layer classification hard rules** (yuzhworkhard-wq/image-to-code): split
   background / entities / HUD / FX with pixel-coordinate measurement; sprites must
   be clean transparent-background PNGs (`audit_png_assets.py` enforces this).
4. **13-section GDD synthesis** (yakoub-ai/phaser4-gamedev's phaser-gdd +
   DY-2026/GameDesignOS design skills): turn recon output into a full game design
   document before building.
5. **Playtest parity loop** (kursku/develop-web-game + caucy2026/game-playtest):
   automated playtest screenshots → `imgdiff_parity.py` scores them against the
   original screen by screen (the replica-diff idea); below threshold means rework.

## Three new scripts (skill/scripts/)
| Script | Outputs |
|---|---|
| `infer_gameplay_from_image.py` (requires opencv) | `recon_gameplay_spec.json` + `features.csv` (must/should feature matrix with a verification-method column) |
| `imgdiff_parity.py` (requires opencv) | Parity JSON (feature_parity_score, shippable flag) + optional diff image and per-feature checks against features.csv |
| `audit_png_assets.py` | Per-PNG alpha channel, corner alpha, transparent-pixel ratio and a `transparent_bg_ok` verdict |

All three were executed on real screenshots during integration: spec + feature
matrix generated, parity scoring produced, and alpha-less screenshots correctly
flagged as failing the transparent-background rule.

Originals: `upstream/replica-skill/`, `upstream/image-to-code/`,
`upstream/phaser4-gamedev/`, `upstream/gamedesignos/`, `upstream/develop-web-game/`,
`upstream/game-playtest/`; summaries in `skill/references/image-to-gameplay-recon/`.
