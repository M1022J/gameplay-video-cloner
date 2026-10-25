# SOURCES — Upstream Provenance (Download & Integration Record)

Downloaded: 2026-10-25, via `git clone --depth 1` (same for the Gist). Integration strips
`.git` only; no upstream content is rewritten (only the scope selections noted below).

| # | Source (GitHub) | Commit | Integrated at | Scope & notes |
|---|---|---|---|---|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | `upstream/superpowers/` | Whole repo. This skill uses its `skills/dispatching-parallel-agents` and `skills/subagent-driven-development` |
| 2 | [kieranklaassen — Gist 4f2aba89](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea) | `f9926ad244b48abc93f6d6a7352d61c9a7a4b8d2` | `upstream/orchestrating-swarms/SKILL.md` | The handbook names a repo `kieranklaassen/orchestrating-swarms`; no such repo exists — the content is this Gist, "Claude Code Swarm Orchestration Skill", included verbatim |
| 3 | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | `e8d346bcb691225fb6ae51a49c353bcedb2ef61d` | `upstream/antigravity-subagent-orchestrator/` | Origin repo is 466MB (thousands of unrelated skills); only the cited `skills/subagent-orchestrator/` + origin LICENSE/README are included |
| 4 | [qodex-ai/ai-agent-skills](https://github.com/qodex-ai/ai-agent-skills) | `6ea9f00885c5dc5e6d9435d443dbf7d9ce865e29` | `upstream/qodex-multi-agent-orchestration/` | The handbook's `qodex-ai/multi-agent-orchestration` repo does not exist; the correct repo is ai-agent-skills. Only its `skills/multi-agent-orchestration/` + LICENSE/README are included |
| 5 | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | `408d3c9eee2d0c75c12a3abb5de29e53c2ca6b9e` | `upstream/awesome-claude-code-subagents/` | Whole repo |
| 6 | [GenielabsOpenSource/spine-animation-ai](https://github.com/GenielabsOpenSource/spine-animation-ai) | `702b71689cac826efee942ee4564fef9560d6ef8` | `upstream/spine-animation-ai/` | Whole repo (demo media are binary; see `docs/BINARY_FILES.en.md`). License: PolyForm Noncommercial 1.0.0 |
| 7 | [BowTiedSwan/rive-skills](https://github.com/BowTiedSwan/rive-skills) | `e64aa14cfdc4c3d0a92a8a0b14be4aa2bb911bdb` | `upstream/rive-skills/` | Whole repo |
| 8 | [composio-community/opencode-skills](https://github.com/composio-community/opencode-skills) | `5076f6673e5bf8b1f46dc5e934d1e3dd37250e10` | `upstream/opencode-blender-rigging-animation/` | Only the cited `skills/blender-rigging-animation/` + origin README |
| 9 | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | `8f778d2405a214b508d4c7d80742be8e43acdd52` | `upstream/blender-skills/` | Whole repo |
| 10 | [ybuild-ai/ai-game-art-pipeline-skill](https://github.com/ybuild-ai/ai-game-art-pipeline-skill) | `ed4a2ce1a94370d5962c7d079cd9404a863e02c7` | `upstream/ai-game-art-pipeline-skill/` | Whole repo (media images are binary; see `docs/BINARY_FILES.en.md`) |
| 11 | [video-db/skills](https://github.com/video-db/skills) | `b47b587e282bc95a0ec4e8a25fc72a8600941341` | `upstream/videodb-skills/` | Whole repo |
| 12 | [PlayableIntelligence/game-creator](https://github.com/PlayableIntelligence/game-creator) | `4e64b83b5fe400b34ad3a484d9b4a6090b26d512` | `upstream/game-creator/` | Includes `skills/ agents/ templates/ scripts/ tests/` and root docs. **Not included**: `assets/` (140MB media library), `examples/` (70MB sample games), `site/` (website), and `submodules/` (`skills/playdotfun`, `skills/unity-mcp` were symlinks into uninitialized submodules) — none are cited by this skill; fetch them upstream at the pinned commit if needed |
| 13 | [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | `184b72be02884f782a0058f2eeae2ce4277453e4` | `upstream/awesome-gamedev-agent-skills/` | Whole repo (banner image is binary; see `docs/BINARY_FILES.en.md`). License: Apache-2.0 |
| 14 | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418` | `upstream/claude-code-game-studios/` | Whole repo. License: MIT |

## Local dependencies (verified present on the build machine)

- Python 3 + `Pillow`, `numpy` (see `requirements.txt`)
- System tools `ffmpeg` / `ffprobe` (required by the frame-extraction and telemetry scripts)
- Node.js (optional toolchains of some upstream skills; not required by this skill's scripts)

## V2 supplement (2026-10-25, video motion & VFX analysis)

Added in the user's Gemini conversation to fix "static single-image blindness" (continuous
action and hit effects not visible). The updated pack (46 files: updated SKILL.md + 2 new
scripts + 4 new references) and the v2 handbook are integrated as well (`HANDBOOK-v2.md`).

| # | Source (GitHub) | Commit | Integrated at | Scope & notes |
|---|---|---|---|---|
| 15 | [Schmandarine/web-motion-skill](https://github.com/Schmandarine/web-motion-skill) | `74b7359277140f518cd33be224e6f86c158b629a` | `upstream/web-motion-skill/` | Whole repo. Macro (16/24-tile contact sheets) → micro (30/60fps burst strips) drill-down + Disney 12 principles of motion |
| 16 | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | `6d2f02ea077eead1bee5411a31bcc6db5a11a70c` | `upstream/senior-computer-vision/` | Monorepo; only `engineering-team/skills/senior-computer-vision/` + origin LICENSE/README. OpenCV Farneback dense optical flow, onion-skin trail synthesis |
| 17 | [bsisduck/video-analyzer-skill](https://github.com/bsisduck/video-analyzer-skill) | `1dd7e8172ba6ebb216e46df5cfdc3bdc10062600` | `upstream/video-analyzer-skill/` | Whole repo. Adaptive FPS tiering, scene cuts, audio transient peaks, parallel visual/motion/audio subagents |
| 18 | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | `f9a8a041b85185ee4881b3471d3415e939aac772` | `upstream/motion-design-skill/` | Whole repo. Timing/easing lookup tables, displacement-to-Bezier fitting, multi-element stagger choreography |
| 19 | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) | `b45d60fa5b0f7b7d07331572416b80e17dcfd203` | `upstream/awesome-motion-design-agent-skills/` | Only the cited `skills/motion-director` and `skills/web-motion-auditor` (5-point motion quality gate) + origin README/LICENSE |

New v2 script dependency: `opencv-python-headless` (added to `requirements.txt`).

## V3 supplement (2026-10-25, image-to-gameplay reverse engineering)

Added in the user's Gemini conversation ("how do you reverse-engineer gameplay from an
image?"). The updated pack (53 files: updated SKILL.md + 3 new scripts + 4 new references)
and the v3 handbook are integrated as well (`HANDBOOK-v3.md`).

| # | Source (GitHub) | Commit | Integrated at | Scope & notes |
|---|---|---|---|---|
| 20 | [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) | `77c9436fb3d18c3d58169efb8caf4fe906b0dc51` | `upstream/replica-skill/` | Whole repo. Clean-room reverse engineering: replica-recon → replica-design → replica-diff per-screen parity scoring |
| 21 | [yuzhworkhard-wq/image-to-code](https://github.com/yuzhworkhard-wq/image-to-code) | `886c882a05b3c44b27e1ac277d740eb3dc0b1a5b` | `upstream/image-to-code/` | Whole repo. Screenshot → layer classification (background/entities/HUD/FX), pixel-coordinate measurement, transparent-sprite PNG hard rules |
| 22 | [yakoub-ai/phaser4-gamedev](https://github.com/yakoub-ai/phaser4-gamedev) | `1c1bf45dec3f0acbe8b2a963cc6dab93be31253a` | `upstream/phaser4-gamedev/` | Whole repo. phaser-gdd synthesizes recon output into a 13-section game design document (GDD), etc. |
| 23 | [DY-2026/GameDesignOS](https://github.com/DY-2026/GameDesignOS) | `ada4bf9e60c2c90a4c84866e4bfd191e3767d164` | `upstream/gamedesignos/` | Monorepo (85MB); extract: root docs + 7 game-design skills (concept-architect / proposal-writer / experience-analyzer, …) + adapters/contracts/docs/scripts; the 36MB assets/ and examples were not included |
| 24 | [kursku/skills](https://github.com/kursku/skills) | `346c313fd2ec241a088c68274da26c538422568b` | `upstream/develop-web-game/` | Monorepo; only `frontend/develop-web-game/`. Playwright playtest loop: action scripts → screenshots → state checks |
| 25 | [caucy2026/skills](https://github.com/caucy2026/skills) | `c4a46da319c83ff0ad3d383c7aed096def8db7ad` | `upstream/game-playtest/` | Only `game-playtest/`. Screenshot-driven playtest auditing |
