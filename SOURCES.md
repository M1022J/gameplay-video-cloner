# SOURCES — 上游来源清单（下载与整合记录）

下载日期：2026-10-25。方式：`git clone --depth 1`（Gist 同），整合时去掉 `.git`，
每个来源固定在下列 commit。原始克隆保存在本地构建目录，未做内容改写（仅按注明的范围取舍）。

| # | 来源（GitHub） | Commit | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | `upstream/superpowers/` | 全仓。本 skill 用其 `skills/dispatching-parallel-agents` 与 `skills/subagent-driven-development` |
| 2 | [kieranklaassen — Gist 4f2aba89](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea) | `f9926ad244b48abc93f6d6a7352d61c9a7a4b8d2` | `upstream/orchestrating-swarms/SKILL.md` | 手册写作仓库 `kieranklaassen/orchestrating-swarms`，该仓库不存在；其内容实为这篇 Gist《Claude Code Swarm Orchestration Skill》，按 Gist 原文收录 |
| 3 | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | `828257c3037dc7c3c3ec987decc5a603025a0ce5` | `upstream/antigravity-subagent-orchestrator/` | 原仓 466MB（数千个无关 skill），仅收录本 skill 引用的 `skills/subagent-orchestrator/` + 原仓 LICENSE/README |
| 4 | [qodex-ai/ai-agent-skills](https://github.com/qodex-ai/ai-agent-skills) | `6ea9f00885c5dc5e6d9435d443dbf7d9ce865e29` | `upstream/qodex-multi-agent-orchestration/` | 手册写作 `qodex-ai/multi-agent-orchestration`（仓库不存在），正确仓库为 ai-agent-skills；仅收录其 `skills/multi-agent-orchestration/` + 原仓 LICENSE/README |
| 5 | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | `ed74d115b7fb7026a22a4f816a8e3250f425e3b4` | `upstream/awesome-claude-code-subagents/` | 全仓 |
| 6 | [GenielabsOpenSource/spine-animation-ai](https://github.com/GenielabsOpenSource/spine-animation-ai) | `702b71689cac826efee942ee4564fef9560d6ef8` | `upstream/spine-animation-ai/` | 全仓（演示媒体为二进制，见 `docs/BINARY_FILES.md`）。许可证：PolyForm Noncommercial 1.0.0 |
| 7 | [BowTiedSwan/rive-skills](https://github.com/BowTiedSwan/rive-skills) | `e64aa14cfdc4c3d0a92a8a0b14be4aa2bb911bdb` | `upstream/rive-skills/` | 全仓 |
| 8 | [composio-community/opencode-skills](https://github.com/composio-community/opencode-skills) | `5076f6673e5bf8b1f46dc5e934d1e3dd37250e10` | `upstream/opencode-blender-rigging-animation/` | 仅收录本 skill 引用的 `skills/blender-rigging-animation/` + 原仓 README |
| 9 | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | `904f095d8f36a6e72adaebb08d07f884a074743d` | `upstream/blender-skills/` | 全仓 |
| 10 | [ybuild-ai/ai-game-art-pipeline-skill](https://github.com/ybuild-ai/ai-game-art-pipeline-skill) | `ed4a2ce1a94370d5962c7d079cd9404a863e02c7` | `upstream/ai-game-art-pipeline-skill/` | 全仓（media 图片为二进制，见 `docs/BINARY_FILES.md`） |
| 11 | [video-db/skills](https://github.com/video-db/skills) | `f985577fba97705ed937cc707c3a67e35f23faf5` | `upstream/videodb-skills/` | 全仓 |
| 12 | [PlayableIntelligence/game-creator](https://github.com/PlayableIntelligence/game-creator) | `53676bd2a524989745ce7cbd4128c17e8a20dd3d` | `upstream/game-creator/` | 收录 `skills/ agents/ templates/ scripts/ tests/` 与根文档；**未收录** `assets/`（140MB 媒体库）、`examples/`（70MB 示例游戏）、`site/`（官网）与 `submodules/`（`skills/playdotfun`、`skills/unity-mcp` 原为指向 submodules 的符号链接，未初始化，故一并略过）——均为本 skill 未引用的部分，需要时按 commit 从上游取 |
| 13 | [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | `19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9` | `upstream/awesome-gamedev-agent-skills/` | 全仓（横幅图为二进制，见 `docs/BINARY_FILES.md`）。许可证：Apache-2.0 |
| 14 | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418` | `upstream/claude-code-game-studios/` | 全仓。许可证：MIT |

## 本地依赖（已在本机验证齐全）

- Python 3 + `Pillow`、`numpy`（见 `requirements.txt`）
- 系统工具 `ffmpeg` / `ffprobe`（视频抽帧与遥测脚本必需）
- Node.js（部分上游 skill 的可选工具链，非本 skill 脚本必需）

## 第二版增补（2026-10-25，视频运动与特效分析）

来源：用户在 Gemini 对话中为解决「只能看单张静态图、看不出连续动作与打击特效」追加的 5 个仓库；
新版包（46 文件：SKILL.md 更新 + 新脚本 2 + 新参考 4）与新版手册已一并整合（`HANDBOOK-v2.md`）。

| # | 来源（GitHub） | Commit | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 15 | [Schmandarine/web-motion-skill](https://github.com/Schmandarine/web-motion-skill) | `74b7359277140f518cd33be224e6f86c158b629a` | `upstream/web-motion-skill/` | 全仓。宏观（16/24 格接触表）→微观（30/60fps 连续动作条）下钻 + 迪士尼运动 12 原则 |
| 16 | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | `8f082544116fc0d014188e521ca40304cdfc86b0` | `upstream/senior-computer-vision/` | 大仓，仅收录 `engineering-team/skills/senior-computer-vision/` + 原仓 LICENSE/README。OpenCV Farneback 稠密光流、洋葱皮轨迹合成 |
| 17 | [bsisduck/video-analyzer-skill](https://github.com/bsisduck/video-analyzer-skill) | `1dd7e8172ba6ebb216e46df5cfdc3bdc10062600` | `upstream/video-analyzer-skill/` | 全仓。自适应 FPS 分档、场景切分、音频瞬态峰值、视觉/运动/音频并行子 Agent |
| 18 | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | `f9a8a041b85185ee4881b3471d3415e939aac772` | `upstream/motion-design-skill/` | 全仓。时序/缓动查表、位移→贝塞尔曲线拟合、多元素 stagger 编排 |
| 19 | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) | `56d9a77baf143b604d9735bc23f6589b05056a53` | `upstream/awesome-motion-design-agent-skills/` | 仅收录所引用的 `skills/motion-director` 与 `skills/web-motion-auditor`（5 点运动质量门禁）+ 原仓 README/LICENSE |

第二版新增脚本依赖：`opencv-python-headless`（已加入 `requirements.txt`）。

## 第三版增补（2026-10-25，图片反推玩法）

来源：用户在 Gemini 对话中问「怎么根据图片反推游戏玩法」追加的 6 个仓库；新版包（53 文件：
SKILL.md 更新 + 新脚本 3 + 新参考 4）与新版手册已一并整合（`HANDBOOK-v3.md`）。

| # | 来源（GitHub） | Commit | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 20 | [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) | `77c9436fb3d18c3d58169efb8caf4fe906b0dc51` | `upstream/replica-skill/` | 全仓。净室逆向：replica-recon 侦察 → replica-design 规格 → replica-diff 逐屏差异审计与还原度打分 |
| 21 | [yuzhworkhard-wq/image-to-code](https://github.com/yuzhworkhard-wq/image-to-code) | `886c882a05b3c44b27e1ac277d740eb3dc0b1a5b` | `upstream/image-to-code/` | 全仓。截图→图层分类表（背景/实体/HUD/特效）、像素坐标量测、透明精灵 PNG 硬规则 |
| 22 | [yakoub-ai/phaser4-gamedev](https://github.com/yakoub-ai/phaser4-gamedev) | `1c1bf45dec3f0acbe8b2a963cc6dab93be31253a` | `upstream/phaser4-gamedev/` | 全仓。phaser-gdd 把侦察结果合成 13 节游戏设计文档（GDD）等 |
| 23 | [DY-2026/GameDesignOS](https://github.com/DY-2026/GameDesignOS) | `ada4bf9e60c2c90a4c84866e4bfd191e3767d164` | `upstream/gamedesignos/` | 大仓（85M），摘录：根文档 + 7 个游戏设计 skill（concept-architect / proposal-writer / experience-analyzer 等）+ adapters/contracts/docs/scripts；未收 36M 的 assets/ 与 examples |
| 24 | [kursku/skills](https://github.com/kursku/skills) | `346c313fd2ec241a088c68274da26c538422568b` | `upstream/develop-web-game/` | 大仓，仅收录 `frontend/develop-web-game/`。Playwright 试玩循环：动作脚本→截图→状态校验 |
| 25 | [caucy2026/skills](https://github.com/caucy2026/skills) | `2e5d45075b4adb95f7735827840bcf3e5e7f5a9a` | `upstream/game-playtest/` | 仅收录 `game-playtest/`。截图驱动的试玩审计 |

## 第四版增补（2026-10-25，去重核心版 + 长视频/亚像素/微细节）

用户上传第四版包（31 文件）并要求「去掉重复的、增加个别新的」：脚本 20 → 12（合并删除 16 个）、
参考 32 → 18（合并为 5 个主题文件夹、删除 24 篇旧摘要），同时新增以下 16 个来源（总数 25 → 41）。
注：`GenielabsOpenSource/spine-animation-ai` 与已收录的 #7 为同一仓库同一 commit（仅组织名不同），不重复计数。

| # | 来源（GitHub） | Commit | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 26 | [KumarSashank/motiscope](https://github.com/KumarSashank/motiscope) | `c0ce3ddedfbe59f445b74372a064e908587a648a` | `upstream/motiscope/` | 全仓。逐帧微差与亚像素运动分析（流式索引器/示波器来源） |
| 27 | [GAIR-NLP/VidaForge](https://github.com/GAIR-NLP/VidaForge) | `fbbc745f6f74025a1c8c18e9ef610c0efccb0a4c` | `upstream/vidaforge/` | 全仓。长视频理解 |
| 28 | [mugnimaestra/video-frames-skill](https://github.com/mugnimaestra/video-frames-skill) | `f0d30f9dc8274aa664ba68b528cd3b6d13dd3509` | `upstream/video-frames-skill/` | 全仓。抽帧 skill |
| 29 | [browser-use/video-use](https://github.com/browser-use/video-use) | `43cfc566833548093455c9d4a46bd69913b7e552` | `upstream/video-use/` | 全仓。视频操作 |
| 30 | [Breakthrough/DVR-Scan](https://github.com/Breakthrough/DVR-Scan) | `5dd53b3750c4544e66d66b09d9b468490d5514cb` | `upstream/dvr-scan/` | 摘录：源码 + 文档（未收 dist/ 安装包、tests/ 样例视频）。运动事件检测（微差条来源） |
| 31 | [snapcndev/snapcn](https://github.com/snapcndev/snapcn) | `9c57e1b6196d7c895d74ec52934298120b22ffb6` | `upstream/snapcn/` | 摘录：根文档（含 MOTION.md）+ `.claude/skills/motion-quality` + skills/rules（未收网站应用本体 app/registry/components 等）。motion-quality：0.01px 亚像素轨迹 |
| 32 | [HKUDS/VideoRAG](https://github.com/HKUDS/VideoRAG) | `c412a093a820ef7a0e0dda31076ed871136198b3` | `upstream/videorag/` | 全仓。长视频 RAG（双向因果账本来源，含 MovieChat 思路） |
| 33 | [HKUDS/VideoAgent](https://github.com/HKUDS/VideoAgent) | `f207987e3cffb554aaa6ffdbe733efb30f4b51ed` | `upstream/videoagent/` | 摘录：本体代码 + VideoEdit + 文档（未收 76M 的 assets/ 媒体与 tools/ 内嵌的第三方 TTS/ASR 项目群） |
| 34 | [Huc91/pixel-perfect-skill](https://github.com/Huc91/pixel-perfect-skill) | `2c677882743ebf0fcdc0bedebf055283182a04ce` | `upstream/pixel-perfect-skill/` | 全仓。像素级还原 |
| 35 | [garrytan/gstack](https://github.com/garrytan/gstack) | `a7585d0e74db25e861a92263fcae7e73a2e4d4ad` | `upstream/gstack/` | 摘录：未收 test/（41M 测试夹具）与 lib/diagram-render 构建产物。并排对比修复循环来源 |
| 36 | [rastian/interaction-design-skills](https://github.com/rastian/interaction-design-skills) | `a3f092f9bd183eef8c25ec5ea7f0bb97505b94d3` | `upstream/interaction-design-skills/` | 全仓。24 点游戏微细节清单来源 |
| 37 | [ttengwang/awesome_long_form_video_understanding](https://github.com/ttengwang/awesome_long_form_video_understanding) | `0e25a035559d9e7d420a2a7f0a4724d4723ac2be` | `upstream/awesome-long-form-video-understanding/` | 全仓。长视频理解论文/资源清单 |
| 38 | [afterxleep/agents](https://github.com/afterxleep/agents) | `ec4c354ad8f26690941353cf4f7516f804f78e91` | `upstream/afterxleep-agents/` | 全仓 |
| 39 | [Intense-Visions/harness-engineering](https://github.com/Intense-Visions/harness-engineering) | `19bec0c651790fb7ca134224d1384500f2162194` | `upstream/harness-engineering/` | 摘录：根文档 + docs（未收 changes/ 变更档案 28M）+ templates/examples/fixtures/.claude-plugin（未收 agents/ 多平台镜像与 packages/ 产品源码）。视觉回归 harness 来源 |
| 40 | [vibeeval/vibecosystem](https://github.com/vibeeval/vibecosystem) | `16a4a0e543c75a945e177e94779e07199b0d054f` | `upstream/vibecosystem/` | 全仓。visual-verdict 6 维打分（≥90 门禁）来源 |
| 41 | [uxkin/agent](https://github.com/uxkin/agent) | `c9425694cbf77ca13c067ae100a34eeec5a2856e` | `upstream/uxkin-agent/` | 全仓。ui-from-screenshot（SAHI 象限切片）来源 |

## 2026-11-06 增补（Roblox Game Remaker 全量融入）

用户指令将 Roblox-Game-Remaker 全部融入本仓：skill 本体收于 `skills/roblox-game-remaker/`，上游仓库其余文件（根文档、docs、tests、tools、插件清单等）收于 `skills/roblox-game-remaker/upstream-repo/`，上游内容未做改写；融入说明见 `skills/roblox-game-remaker/INTEGRATION.md`。

| # | 来源（GitHub） | Commit | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 42 | [InfiniteMindData/Roblox-Game-Remaker](https://github.com/InfiniteMindData/Roblox-Game-Remaker) | `fa5213de5852a7ed23473240ad1e381f9d7d7f0a` | `skills/roblox-game-remaker/`（仓库其余文件在其 `upstream-repo/`） | 全仓（125 文件）。许可证：MIT。闸门式复刻流程（研究→逐帧测量→证据化拆解→建造→测量比对修复）+ 24 个实测脚本（motion_track 跳跃重力拟合、visual_compare SSIM/色差等）+ 16 篇参考；Roblox 专属部分（翻译层/Rojo 模板/Studio MCP/VR）仅目标为 Roblox 时用，测量与验证层与引擎无关 |

## 2026-11-07 增补（自研技能 game-render-to-blueprint）

| # | 来源 | 日期 | 整合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 43 | 本仓自研（《变废为宝》UI 重构复盘蒸馏，用户 2026-11-07 令沉淀为技能并融入本仓） | 2026-11-07 | `skills/game-render-to-blueprint/` | 效果图即施工图方法：逐元素量测原图坐标→参考坐标系绝对摆位+整幅等比缩放；组件离线预成型（三态齐全、运行时不做九宫格）；内缩取量测值；旧裁决与原图冲突先上报；无专属图的页面标「风格推及」；对图逐元素验收。源于远端实现（reference_view 坐标摆位）一次对齐、而流式布局追赶五轮未收敛的对照教训 |

## 2026-11-07 增补二（game-render-to-blueprint 融合三项外部方法）

用户提供清单并令「把这几个也融进去」：以下三项的方法已转述融合进 `skills/game-render-to-blueprint/SKILL.md`（分块还原 / 层级树拆解 / 反廉价感约束三节），只吸收方法、未搬运代码与原文。

| # | 来源（GitHub） | 许可证（2026-11-07 API 核实） | 融合位置 | 收录范围与说明 |
|---|---|---|---|---|
| 44 | [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) | MIT | `skills/game-render-to-blueprint/`（融合方法一） | 截图/效果图转前端代码工具（81k star）；吸收其分块还原与「生成→截图→对照→修块」迭代收敛策略、原图素材优先提取复用 |
| 45 | [NoviScl/Design2Code](https://github.com/NoviScl/Design2Code)（斯坦福 SALT-Lab，论文 arXiv:2403.03163）+ [YaoMarkMu/UI2Code](https://github.com/YaoMarkMu/UI2Code) | Design2Code 为 MIT；UI2Code 仓库 API 未返回许可证信息（待核） | `skills/game-render-to-blueprint/`（融合方法二） | 吸收节点层级树拆解（容器嵌套/对齐约束/层叠）、文字先行提取、块级四维评测（块匹配/文字/位置/颜色）驱动的自修正回路 |
| 46 | [anthropics/skills · frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)（Anthropic 官方技能，其目录自带 LICENSE.txt）；索引：[travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)、[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 见其目录 LICENSE.txt；合集为索引引用 | `skills/game-render-to-blueprint/`（融合方法三） | 吸收「AI 默认脸」清单（奶油底+衬线+陶土、近黑+酸绿、报纸细线、SaaS 卡片套件、模板眉题/中点串/箭头尾巴等）与克制原则，适配到风格推及页与文案；有定版效果图时效果图优先于本节 |
