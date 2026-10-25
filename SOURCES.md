# SOURCES — 上游来源清单（下载与整合记录）

下载日期：2026-10-25。方式：`git clone --depth 1`（Gist 同），整合时去掉 `.git`，
每个来源固定在下列 commit。原始克隆保存在本地构建目录，未做内容改写（仅按注明的范围取舍）。

| # | 来源（GitHub） | Commit | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | `upstream/superpowers/` | 全仓。本 skill 用其 `skills/dispatching-parallel-agents` 与 `skills/subagent-driven-development` |
| 2 | [kieranklaassen — Gist 4f2aba89](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea) | `f9926ad244b48abc93f6d6a7352d61c9a7a4b8d2` | `upstream/orchestrating-swarms/SKILL.md` | 手册写作仓库 `kieranklaassen/orchestrating-swarms`，该仓库不存在；其内容实为这篇 Gist《Claude Code Swarm Orchestration Skill》，按 Gist 原文收录 |
| 3 | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | `e8d346bcb691225fb6ae51a49c353bcedb2ef61d` | `upstream/antigravity-subagent-orchestrator/` | 原仓 466MB（数千个无关 skill），仅收录本 skill 引用的 `skills/subagent-orchestrator/` + 原仓 LICENSE/README |
| 4 | [qodex-ai/ai-agent-skills](https://github.com/qodex-ai/ai-agent-skills) | `6ea9f00885c5dc5e6d9435d443dbf7d9ce865e29` | `upstream/qodex-multi-agent-orchestration/` | 手册写作 `qodex-ai/multi-agent-orchestration`（仓库不存在），正确仓库为 ai-agent-skills；仅收录其 `skills/multi-agent-orchestration/` + 原仓 LICENSE/README |
| 5 | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | `408d3c9eee2d0c75c12a3abb5de29e53c2ca6b9e` | `upstream/awesome-claude-code-subagents/` | 全仓 |
| 6 | [GenielabsOpenSource/spine-animation-ai](https://github.com/GenielabsOpenSource/spine-animation-ai) | `702b71689cac826efee942ee4564fef9560d6ef8` | `upstream/spine-animation-ai/` | 全仓（演示媒体为二进制，见 `docs/BINARY_FILES.md`）。许可证：PolyForm Noncommercial 1.0.0 |
| 7 | [BowTiedSwan/rive-skills](https://github.com/BowTiedSwan/rive-skills) | `e64aa14cfdc4c3d0a92a8a0b14be4aa2bb911bdb` | `upstream/rive-skills/` | 全仓 |
| 8 | [composio-community/opencode-skills](https://github.com/composio-community/opencode-skills) | `5076f6673e5bf8b1f46dc5e934d1e3dd37250e10` | `upstream/opencode-blender-rigging-animation/` | 仅收录本 skill 引用的 `skills/blender-rigging-animation/` + 原仓 README |
| 9 | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | `8f778d2405a214b508d4c7d80742be8e43acdd52` | `upstream/blender-skills/` | 全仓 |
| 10 | [ybuild-ai/ai-game-art-pipeline-skill](https://github.com/ybuild-ai/ai-game-art-pipeline-skill) | `ed4a2ce1a94370d5962c7d079cd9404a863e02c7` | `upstream/ai-game-art-pipeline-skill/` | 全仓（media 图片为二进制，见 `docs/BINARY_FILES.md`） |
| 11 | [video-db/skills](https://github.com/video-db/skills) | `b47b587e282bc95a0ec4e8a25fc72a8600941341` | `upstream/videodb-skills/` | 全仓 |
| 12 | [PlayableIntelligence/game-creator](https://github.com/PlayableIntelligence/game-creator) | `4e64b83b5fe400b34ad3a484d9b4a6090b26d512` | `upstream/game-creator/` | 收录 `skills/ agents/ templates/ scripts/ tests/` 与根文档；**未收录** `assets/`（140MB 媒体库）、`examples/`（70MB 示例游戏）、`site/`（官网）与 `submodules/`（`skills/playdotfun`、`skills/unity-mcp` 原为指向 submodules 的符号链接，未初始化，故一并略过）——均为本 skill 未引用的部分，需要时按 commit 从上游取 |
| 13 | [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | `184b72be02884f782a0058f2eeae2ce4277453e4` | `upstream/awesome-gamedev-agent-skills/` | 全仓（横幅图为二进制，见 `docs/BINARY_FILES.md`）。许可证：Apache-2.0 |
| 14 | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418` | `upstream/claude-code-game-studios/` | 全仓。许可证：MIT |

## 本地依赖（已在本机验证齐全）

- Python 3 + `Pillow`、`numpy`（见 `requirements.txt`）
- 系统工具 `ffmpeg` / `ffprobe`（视频抽帧与遥测脚本必需）
- Node.js（部分上游 skill 的可选工具链，非本 skill 脚本必需）
