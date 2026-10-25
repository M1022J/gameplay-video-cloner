# Gameplay Video Cloner — 看游戏视频 1:1 复刻游戏（整合版）

把一段 gameplay 视频 / 录屏 / GIF 逆向还原成可玩的游戏：主控 Agent + 并行子 Agent 蜂群
（Lead-Agent + Parallel-Subagents Swarm）工作流，覆盖视频遥测分析、引擎路由、
2D/3D 骨骼动画、物理/控制器、HUD/音频合成与 QA 验收。

本仓库是**整合版**：把原 skill 包（`gameplay-video-cloner` zip）里只有摘要占位、
正文散落在开源来源的内容，全部下载并合并到一个项目里，打开即用。
2026-10-25 增补第二版（视频运动与特效分析）：新增 5 个来源、2 个脚本、4 篇参考，来源总数 14 → 19；新版手册见 `HANDBOOK-v2.md`。

## 组成

| 部分 | 位置 | 说明 |
|---|---|---|
| Skill 本体 | `SKILL.md` + `skill/` | 入口文件 + 17 个可执行 Python 脚本（`skill/scripts/`）+ 28 篇参考摘要（`skill/references/`） |
| 单文件手册 | `HANDBOOK.md` | 用户提供的 All-in-One 手册全文（870 行，内嵌 15 个脚本的完整版与全部 playbook） |
| 上游原文 | `upstream/` | 14 个来源中本 skill 实际引用的全部内容（见下表与 `SOURCES.md`） |
| 依赖 | `requirements.txt` | Python：Pillow、numpy；系统：ffmpeg / ffprobe |

## 分文档介绍（中英双语）

- 中文版 `docs/zh/`：01 总览 · 02 快速开始 · 03 工作流与蜂群架构 · 04 脚本参考 · 05 骨骼动画 · 06 上游与整合说明 · 07 实测复盘硬规矩
- English `docs/en/`：01 Overview · 02 Quick Start · 03 Workflow & Swarm · 04 Scripts Reference · 05 Skeletal Animation · 06 Upstream & Integration · 07 Field Lessons
- English README: [`README.en.md`](README.en.md) · English sources: [`SOURCES.en.md`](SOURCES.en.md)

## 上游一览（`upstream/`，共 19 个来源）

| 目录 | 来源 | 收录内容 |
|---|---|---|
| `superpowers/` | obra/superpowers | 全仓（并行子 Agent 派发 + 子 Agent 驱动开发） |
| `orchestrating-swarms/` | kieranklaassen（Gist） | Swarm 编排 SKILL.md 原文（原手册写作仓库，实为 Gist） |
| `antigravity-subagent-orchestrator/` | sickn33/antigravity-awesome-skills | 仅所引用的 `subagent-orchestrator` skill（原仓 466MB） |
| `qodex-multi-agent-orchestration/` | qodex-ai/ai-agent-skills | 仅所引用的 `multi-agent-orchestration` skill |
| `awesome-claude-code-subagents/` | VoltAgent/awesome-claude-code-subagents | 全仓（100+ 子 Agent 目录） |
| `spine-animation-ai/` | GenielabsOpenSource/spine-animation-ai | 全仓（Spine 4.2 2D 骨骼自动绑骨） |
| `rive-skills/` | BowTiedSwan/rive-skills | 全仓（Rive 骨骼/网格/状态机） |
| `opencode-blender-rigging-animation/` | composio-community/opencode-skills | 仅所引用的 `blender-rigging-animation` skill |
| `blender-skills/` | arjun988/blender-skills | 全仓（94 个 Blender 3D 技能） |
| `ai-game-art-pipeline-skill/` | ybuild-ai/ai-game-art-pipeline-skill | 全仓（游戏美术流水线） |
| `videodb-skills/` | video-db/skills | 全仓（视频场景/OCR/时间线索引） |
| `game-creator/` | PlayableIntelligence/game-creator | `skills/ agents/ templates/ scripts/ tests/` + 根文档（不含 140MB `assets/` 与 70MB `examples/` 媒体库，见 `SOURCES.md`） |
| `awesome-gamedev-agent-skills/` | gamedev-skills/awesome-gamedev-agent-skills | 全仓（74 个跨引擎技能） |
| `claude-code-game-studios/` | Donchitos/Claude-Code-Game-Studios | 全仓（49 个工作室 Agent + 钩子/规则） |
| `web-motion-skill/` | Schmandarine/web-motion-skill | 全仓（第二版新增：宏观-微观高帧率动作拆解） |
| `senior-computer-vision/` | alirezarezvani/claude-skills | 仅所引用的 `senior-computer-vision` skill（OpenCV 光流/洋葱皮轨迹） |
| `video-analyzer-skill/` | bsisduck/video-analyzer-skill | 全仓（自适应分档抽帧 + 音频峰值 + 并行子 Agent 分析） |
| `motion-design-skill/` | LottieFiles/motion-design-skill | 全仓（时序/缓动查表与曲线拟合） |
| `awesome-motion-design-agent-skills/` | frankxai/awesome-motion-design-agent-skills | 仅所引用的 `motion-director` + `web-motion-auditor` 两个 skill |

每个来源的 URL、固定 commit SHA、许可证与取舍细节见 [`SOURCES.md`](SOURCES.md)。
16 个二进制媒体文件（演示 GIF/MP4/横幅图等）未随 GitHub 上传，清单与上游直达路径见
[`docs/BINARY_FILES.md`](docs/BINARY_FILES.md)；本地整合包中它们都在原位。

## 快速开始

```bash
pip install -r requirements.txt   # 另需系统 ffmpeg / ffprobe

# 1) 视频遥测：抽 16 帧、拼接触表、HUD 方差图、主色板 -> telemetry.json
python3 skill/scripts/analyze_gameplay_video.py <video.mp4> ./video_analysis --frames 16

# 2) 引擎/品类路由
python3 skill/scripts/detect_engine_router.py --workspace . --prompt "<复刻需求>"

# 3) 初始化 5 子 Agent 任务包 + DAG 任务板
python3 skill/scripts/orchestrate_subagents.py --project-dir ./subagent_workspace --game-title "<游戏名>"
python3 skill/scripts/swarm_task_board.py --board ./subagent_workspace/swarm_board.json init

# 4) 交付前验收（3 点抽查 + 架构 8 项门禁）
python3 skill/scripts/merge_subagent_modules.py <game.html>
python3 skill/scripts/validate_architecture.py <game.html>
```

工作流（三轮蜂群：遥测与契约 → 并行专科子 Agent → 合并审查交付）的完整说明见
`SKILL.md` 与 `HANDBOOK.md`。

## 许可

本整合仓不改变各上游的原许可证：各 `upstream/<目录>` 内保留其原 LICENSE
（如 spine-animation-ai 为 PolyForm Noncommercial 1.0.0，多数为 MIT / Apache-2.0），
使用时请遵守对应条款。`skill/`、`SKILL.md`、`HANDBOOK.md` 来自用户提供的原始包。
