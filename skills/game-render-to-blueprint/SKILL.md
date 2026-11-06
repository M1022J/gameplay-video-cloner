---
name: game-render-to-blueprint
description: Replicate game UI from an approved render/mockup （效果图） by treating it as a construction blueprint: measure every element's coordinates on the original image, place elements by absolute coordinates in a reference-resolution view scaled proportionally to the screen, pre-form component art offline instead of runtime nine-slicing, and verify against the mockup element by element. Use whenever a game page must match an approved mockup/render 1:1 （复刻 UI、按效果图还原页面）.
---

# 效果图即施工图（Game Render to Blueprint）

复刻 UI 时，**效果图是施工图，不是风格参考**。1:1 还原是按图施工出来的，不是靠流式布局一点点凑出来的。

来源：《变废为宝》（竖屏垃圾桶寻宝）2026-11-07 复盘定版——远端实现用本法一次对齐；旧法（流式布局 + 公式参数追赶效果图）连追五轮未收敛。

## 流程

1. **先量测，后开发**：开发前先产出分析文档（如 `docs/ui-analysis.md`），逐页逐元素记录在原图上的坐标、尺寸、颜色、边框与内缩（原图分辨率即参考坐标系，如 1152×2048）。图上没有的东西不编造。
2. **坐标摆位**：建参考坐标视图层（如 `reference_view.lua`），每个元素按量测坐标绝对定位，整幅按参考分辨率等比缩放落屏。不用流式布局/内容撑高/百分比公式去「凑近」效果图。
3. **组件离线预成型**：纸面、按钮（含常态/按下/禁用三态）、缎带、徽章等组件，先在图上裁好成型为成品素材再进游戏；运行时**不做九宫格切片**，不与边厚、漏角、DPR 缠斗。
4. **内缩按量测值**：棋盘、面板等容器的边框内缩直接取量测数（如棋盘内缩 14.5%→5.5% 的教训：公式默认值会吃掉格面），不凭手感设。
5. **对图验收**：引擎内截图与效果图逐元素对照（坐标/尺寸/颜色/边框/内缩逐项打勾），差一项修一项；没亲眼对过图不许下「一样」的结论。

## 硬规矩

- **旧裁决与原图冲突先上报**：已定的行为/版式口径（如「点卡即领」「弹窗按内容定高」）与效果图原图打架时，把冲突摆给用户裁，不许默默守旧、也不许默默推翻。
- **无专属效果图的页面标「风格推及」**：只能按已有页面的风格语言（纸面卡、描边、色板）推及，并在分析文档里写明标准来源；不许假装有图、更不许虚构图上没有的元素。
- **三态齐全**：可点组件的常态/按下/禁用三态都要离线成型，缺态不许用运行时变色凑。
- **等比缩放单源**：全页共用一套参考坐标→屏幕的缩放与触点映射，禁止逐元素各算各的。

## 反例（勿重蹈）

- 把效果图当风格参考，用流式布局引擎凑版式，再靠预览截图逐轮往回追——每轮都差一点，永不收敛。
- 在九宫格切片上死磕参数（查格式、裁角、加内边距、回退），而不肯把组件改成离线成型。
- 守着旧裁决跟原图打架，既不推翻也不上报。
