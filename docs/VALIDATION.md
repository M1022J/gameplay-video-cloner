# VALIDATION — 整合验收记录（2026-10-25）

在本机对整合后的项目实测（非仅看构建日志）：

| 检查 | 结果 |
|---|---|
| `skill/scripts/` 15 个 Python 脚本 `py_compile` | 全部通过 |
| `analyze_gameplay_video.py` 跑真实视频（1280×720 / 24fps / 6.04s） | 成功：抽 8 帧 + `contact_sheet.png` + `hud_variance_map.png` + `telemetry.json`（画幅 16:9 横屏判定正确） |
| `orchestrate_subagents.py` + `swarm_task_board.py init` | 成功：生成 `mission_brief.json`、`sdd_ledger.md`、`swarm_board.json` 与 5 个子 Agent 任务包 |
| `validate_architecture.py` 跑样例 HTML 游戏 | 8/8 全过（Constants / reset / rAF / dt / 双输入 / trauma 震屏 / WebAudio / render_game_to_text） |
| `detect_engine_router.py`（竖屏合成消除需求） | 正常输出引擎路由 + 骨骼动画/多 Agent/学科技能清单 JSON |
| 依赖 | Python 3.12 + Pillow + numpy 已装；ffmpeg/ffprobe 已装 |

结构核对：仓库内文本文件 2,362 个；`skill/` 本体 40 文件与原始 zip 逐一对齐；
`upstream/` 14 个来源目录与 `SOURCES.md` 的 commit 清单一一对应。

## 第二版增补验收（2026-10-25）
| 检查 | 结果 |
|---|---|
| `extract_motion_trails_and_vfx.py` 跑真实视频（OpenCV） | 成功：3 组动作条 + 3 张洋葱皮轨迹图 + `vfx_timing_report.json` |
| `extract_audio_sfx_peaks.py` 跑同一视频 | 成功：`audio_peaks.json`，检出多处 medium 档音效峰值（如 2.9s / 3.2s / 3.5s） |
| v2 包 46 文件与 v1 逐项 diff | 仅 SKILL.md 更新 + 新增 6 文件（2 脚本 + 4 参考），其余 39 文件与 v1 逐字节一致 |
| 新增 5 个上游来源 | 全部克隆成功并记录 commit（SOURCES #15–19） |

## 第三版增补验收（2026-10-25）
| 检查 | 结果 |
|---|---|
| `infer_gameplay_from_image.py` 跑真实截图 | 成功：`recon_gameplay_spec.json` + `features.csv`（F01 视口/F02 HUD/… 特性矩阵） |
| `imgdiff_parity.py` 跑两张相邻帧 | 成功：输出还原度 JSON（feature_parity_score / shippable）+ 差异图 |
| `audit_png_assets.py` 跑普通截图 | 成功：正确判定无 alpha 的截图 `transparent_bg_ok: false` |
| v3 包 53 文件与当前版逐项 diff | 仅 SKILL.md 更新 + 新增 7 文件（3 脚本 + 4 参考），其余 45 文件逐字节一致 |
| 新增 6 个上游来源 | 全部克隆成功并记录 commit（SOURCES #20–25） |

## 第四版验收（2026-10-25，去重核心版）
| 检查 | 结果 |
|---|---|
| 12 个脚本 py_compile | 全部通过 |
| `stream_long_video_indexer.py` 跑真实视频 | 成功：packed_timeline.md + frame_by_frame_micro_energy.json + 关键帧 |
| `extract_micro_frame_deltas.py` | 成功：24 个 3x 微差补丁 + 10x 残差放大条 + 热力图 + 报告 |
| `subpixel_motion_oscilloscope.py` | 成功：73 帧 0.01px 分析，拟合出 sharp_cubic_bezier_burst 曲线类型 |
| `bidirectional_context_ledger.py` | init + export-brief 均成功 |
| `slice_micro_detail_crops.py` | 成功：4 象限 + 3 功能区 + 8 张 2x 微细节裁剪 |
| `process_and_audit_sprites.py audit` / `spine_and_swarm_pipeline.py route-engine` | 均成功输出 |
| `visual_verdict_diff_loop.py` 两张不同帧对比 | 成功：67.86/100 判 REVISE + 三联图（原图/构建/热力图） |
| 去重核对 | 保留的 4 脚本 + 8 参考与旧版逐字节一致；删除的 16 脚本/24 参考均已被新合并脚本/手册覆盖（对照 SKILL.md 合并表） |
| 新增 16 个上游来源 | 全部克隆成功并记录 commit（SOURCES #26–41） |
