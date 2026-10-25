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

## V4 supplement (2026-10-25, deduplicated core + long-video / sub-pixel / micro-detail)

The user uploaded the v4 pack (31 files) asking to "remove the duplicates and add the
few new ones": scripts 20 → 12 (16 merged away and deleted), references 32 → 18
(consolidated into 5 domain folders; 24 old summaries deleted), plus these 16 new
sources (25 → 41 total). Note: `GenielabsOpenSource/spine-animation-ai` is the same
repo at the same commit as #7 under a different org name — not double-counted.

| # | Source (GitHub) | Commit | Integrated at | Scope & notes |
|---|---|---|---|---|
| 26 | [KumarSashank/motiscope](https://github.com/KumarSashank/motiscope) | `c0ce3ddedfbe59f445b74372a064e908587a648a` | `upstream/motiscope/` | Whole repo. Frame micro-diff & sub-pixel motion (streamer/oscilloscope source) |
| 27 | [GAIR-NLP/VidaForge](https://github.com/GAIR-NLP/VidaForge) | `fbbc745f6f74025a1c8c18e9ef610c0efccb0a4c` | `upstream/vidaforge/` | Whole repo. Long-video understanding |
| 28 | [mugnimaestra/video-frames-skill](https://github.com/mugnimaestra/video-frames-skill) | `f0d30f9dc8274aa664ba68b528cd3b6d13dd3509` | `upstream/video-frames-skill/` | Whole repo. Frame-extraction skill |
| 29 | [browser-use/video-use](https://github.com/browser-use/video-use) | `43cfc566833548093455c9d4a46bd69913b7e552` | `upstream/video-use/` | Whole repo. Video operations |
| 30 | [Breakthrough/DVR-Scan](https://github.com/Breakthrough/DVR-Scan) | `52aa2288dd45e7d607eb7b6356b1e84e270e63e5` | `upstream/dvr-scan/` | Extract: source + docs (excludes dist/ installers, tests/ sample videos). Motion-event detection |
| 31 | [snapcndev/snapcn](https://github.com/snapcndev/snapcn) | `ebbe43f388779c51b3e5465b95e03466c2c96267` | `upstream/snapcn/` | Extract: root docs (incl. MOTION.md) + `.claude/skills/motion-quality` + skills/rules (excludes the web app itself: app/registry/components/…). motion-quality: 0.01px sub-pixel trajectories |
| 32 | [HKUDS/VideoRAG](https://github.com/HKUDS/VideoRAG) | `c412a093a820ef7a0e0dda31076ed871136198b3` | `upstream/videorag/` | Whole repo. Long-video RAG (bidirectional causal ledger source, incl. MovieChat ideas) |
| 33 | [HKUDS/VideoAgent](https://github.com/HKUDS/VideoAgent) | `f207987e3cffb554aaa6ffdbe733efb30f4b51ed` | `upstream/videoagent/` | Extract: own code + VideoEdit + docs (excludes the 76MB assets/ media and the vendored third-party TTS/ASR projects under tools/) |
| 34 | [Huc91/pixel-perfect-skill](https://github.com/Huc91/pixel-perfect-skill) | `2c677882743ebf0fcdc0bedebf055283182a04ce` | `upstream/pixel-perfect-skill/` | Whole repo. Pixel-perfect replication |
| 35 | [garrytan/gstack](https://github.com/garrytan/gstack) | `669e59d65b48081547de9a3ae202122af5bbe065` | `upstream/gstack/` | Extract: excludes test/ (41MB fixtures) and the lib/diagram-render build artifact. Side-by-side fix-loop source |
| 36 | [rastian/interaction-design-skills](https://github.com/rastian/interaction-design-skills) | `a3f092f9bd183eef8c25ec5ea7f0bb97505b94d3` | `upstream/interaction-design-skills/` | Whole repo. 24-point game micro-detail checklist source |
| 37 | [ttengwang/awesome_long_form_video_understanding](https://github.com/ttengwang/awesome_long_form_video_understanding) | `0e25a035559d9e7d420a2a7f0a4724d4723ac2be` | `upstream/awesome-long-form-video-understanding/` | Whole repo. Long-video paper/resource list |
| 38 | [afterxleep/agents](https://github.com/afterxleep/agents) | `ec4c354ad8f26690941353cf4f7516f804f78e91` | `upstream/afterxleep-agents/` | Whole repo |
| 39 | [Intense-Visions/harness-engineering](https://github.com/Intense-Visions/harness-engineering) | `b691642acbe66968c571c93675318841287b7b9f` | `upstream/harness-engineering/` | Extract: root docs + docs (excludes the 28MB changes/ archive) + templates/examples/fixtures/.claude-plugin (excludes the agents/ platform mirrors and packages/ product source). Visual-regression harness source |
| 40 | [vibeeval/vibecosystem](https://github.com/vibeeval/vibecosystem) | `3b763b1fb288f57bfa3cce76ef18184b96461a78` | `upstream/vibecosystem/` | Whole repo. visual-verdict 6D scoring (≥90 gate) source |
| 41 | [uxkin/agent](https://github.com/uxkin/agent) | `6bb351e95de5ddce79bb6bbc5ccd4631eee49eb9` | `upstream/uxkin-agent/` | Whole repo. ui-from-screenshot (SAHI quadrant slicing) source |
