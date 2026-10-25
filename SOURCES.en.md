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
