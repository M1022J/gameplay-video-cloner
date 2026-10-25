# Clean-Room App/Game Reverse Engineering & Parity Scoring (`Jakeschincariol/replica-skill`)

Distilled from `Jakeschincariol/replica-skill` (11 Claude Skills: `/replica-recon`, `/replica-architect`, `/replica-design`, `/replica-build`, `/replica-test`, `/replica-diff`).

## 1. The 5-Step Screenshot-to-Replica Pipeline
1. **`/replica-recon` (`scripts/infer_gameplay_from_image.py`)**:
   - Inspect every provided screenshot or video keyframe to inventory:
     - **Screens & States**: Title, Main Playfield, Upgrade/Shop Modal, Pause, Victory/Defeat Summary.
     - **Interactive Flows**: What happens when the player taps, drags, releases, or waits 3 seconds?
     - **Inferred Data Model (`GameState`)**: Entities, inventory slots, currencies, wave counters, and cooldown timers.
     - **Feature Matrix (`features.csv`)**: Every visible mechanic logged with `must` / `should` / `could` priority.
2. **`/replica-design`**:
   - Extract exact pixel proportions, container aspect ratio, hex color tokens (`design_tokens_hex`), font hierarchy, and UI card border radii directly from the image.
3. **`/replica-build`**:
   - Implement the core playable loop end-to-end first, ticking off `features.csv` rows so zero `must` features are left unbuilt or mocked.
4. **`/replica-test`**:
   - Test both happy paths (scoring, merging, leveling up) and edge cases (rapid clicking, window resize, Game Over -> instant Restart).
5. **`/replica-diff` (`scripts/imgdiff_parity.py`)**:
   - Compare the reference screenshot against the running replica using edge-map structural similarity (`layout_parity_score`) and `features.csv` completion (`feature_parity_score`). A build is only shippable when `missing_must_haves` is empty!
