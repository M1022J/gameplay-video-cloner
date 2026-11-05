# INTEGRATION — Roblox Game Remaker 在本仓的位置

- **来源**：[InfiniteMindData/Roblox-Game-Remaker](https://github.com/InfiniteMindData/Roblox-Game-Remaker) @ `fa5213de5852a7ed23473240ad1e381f9d7d7f0a`，许可证 MIT（原文见 `upstream-repo/LICENSE`）。
- **融入日期**：2026-11-06，用户指令「全部融入」。上游内容**未做改写**：skill 本体（`SKILL.md` / `references/` / `scripts/` / `assets/` / `evals/` / `examples/` / `agents/`）原样收录；上游仓库的其余文件（根 README、CHANGELOG、docs、tests、tools、插件清单等）收在 `upstream-repo/`。本文件是融入时唯一新增的说明。

## 它给本仓补了什么

本仓核心套件（12 脚本 + 18 手册）强在长视频流式索引、微差/亚像素分析与 6D 视觉裁决；Remaker 强在**带闸门的完整复刻流程**与**可测量的物理/视觉参数拟合**，两者互补：

| Remaker 部件 | 在本仓流程中的位置 |
|---|---|
| `scripts/probe_video.py`、`extract_frames.py`、`contact_sheet.py`、`frame_zoom.py`、`find_mover.py`、`pose_track.py` | Stage 1/2 的录像取证补充：帧率/重复帧探针、精确抽帧清单、标注接触表、目标追踪 |
| `scripts/motion_track.py` + `remake_calc.py` | 核心套件的缺口：由录像**拟合**跳跃重力、加速度、弹簧参数、FOV/单位换算，给规格层提供实测数值而非估值 |
| `scripts/visual_compare.py`、`measure_compare.py` | Stage 4 裁决补充：SSIM / CIEDE2000 / Lab 色移 / 边缘 IoU / 热图，与 6D 打分（≥90 门禁）并行使用 |
| `scripts/ledger.py`、`breakdown_check.py`、`config_check.py`、`remake_status.py` | 证据台账与规格完整性检查，配合 `game_reverse_spec` 的证据先行口径；`remake_status.py` 提供跨会话续跑状态 |
| `scripts/audio_onsets.py` | Stage 2 音频补充：音效起始点检测 |
| `references/research-protocol.md`、`game-breakdown.md`、`verification-loop.md`、`rights-and-policy.md` | 流程闸门、拆解规格、验证闭环与权利政策；其「不声称分析过打不开的录像」与本仓证据纪律一致 |
| `assets/templates/`、`evals/` | 立项/拆解/证据/测量/交付模板与评测集，可直接套用 |

## 引擎范围（重要）

以下部件是 **Roblox Studio 专属**，仅当复刻目标就是 Roblox 时使用；目标为 TapTap Maker（Lua/UrhoX）或其他引擎时，只取上面的测量/验证层，翻译层按目标引擎自己的约定另行处理：

- `references/roblox-translation.md`、`luau-architecture.md`、`studio-mcp.md`、`vr-quest.md`
- `assets/rojo-template/`（Rojo 工程模板与 Luau 运行时）
- `scripts/blender_roblox_export.py`、`studio_snippets.py`、`preset.py` 中的 Roblox 专用部分

## 用法

当任务是「把某个已有游戏尽量 1:1 复刻出来」且有录像/截图证据时，先读本目录 `SKILL.md` 的闸门流程，再按上表调用脚本；核心套件的 Stage 1–4 仍是长视频与微差分析的主线。

## 融入时的一处省略

上游仓库内的便捷符号链接 `.claude/skills/roblox-game-remaker`（指向 `../../skills/roblox-game-remaker`）未收录：它不携带内容，且在 `upstream-repo/` 的收纳位置下该相对路径已失效；skill 本体内容完整收于本目录。
