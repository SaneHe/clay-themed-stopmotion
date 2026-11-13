---
name: clay-themed-stopmotion
description: "Build short theme-driven clay stop-motion videos in HTML/GSAP/HyperFrames with generated raster assets, deterministic stepped motion, layered local audio, compositing audits, and verified landscape or portrait exports. Use when a user wants a handcrafted clay animation in a particular story, place, era, character world, or visual palette."
---

# 通用黏土定格主题视频

这个 skill 用于生成一类视觉风格稳定、主题可替换的短视频。它描述的是“黏土材质 + 分层素材 + 定格式运动 + 字幕和声音”的通用生产方法；城市、日期、角色、地标、交通工具、情节和音效都必须从用户当前 brief 读取，不能写死成某一个项目。

最终交付应包含可重复运行的 HyperFrames 源工程、真实本地素材、音频、MP4 导出和最终抽帧检查图。未渲染的 HTML 预览不是成片。

## 先明确主题变量

在写代码前，从用户需求提取并记录：

- 主题一句话：谁在什么世界里完成什么目标；
- 时间、地点、时代、地标或世界观；
- 角色数量、外观、服装、道具和动作；
- 视觉材料：黏土、纸板、布料、木头、金属或其他手工质感；
- 色彩来源和片头/片尾语言；
- 时长、画幅、平台、字幕和声音要求。

如果用户只给了一个参考视频，先分析它的材质、镜头节奏、构图、字幕和声音，再把主题变量写入 `DESIGN.md`。参考视频提供方法和气质，不会自动决定新视频的故事。

## 标准工作流

1. **分析参考并写假设。** 记录时长、比例、镜头节奏、定格停顿、材质、字幕位置、音乐和事件音效。无法确认的内容写成假设，不要伪装成事实。
2. **先写设计文档。** 创建 `DESIGN.md`、`STORYBOARD.md` 和素材清单。定义主题色、材质、字体、镜头时间、字幕、音频 cue 和片尾文案。
3. **生成分层素材。** 背景、角色、道具、地标、纹理和局部效果保存为本地 PNG/JPG/WAV。角色和前景道具优先使用透明 PNG，并保持机位、光线、比例和材质一致。导入前检查透明边缘和低 alpha 背景污染，清理残留的半透明黑底、白雾、渐变晕边和生成模型抠图残片。
4. **做素材归属审计。** 打开每一张角色/道具 PNG，列出其中已经包含的背包、杯子、卡片、帽子、阴影等物体。每个可见物体只能有一个来源：角色 PNG、独立素材层或 HTML/CSS。不能给已经画进角色 PNG 的物体再加一层简化 CSS 版本。详见 `references/compositing-audit.md`。
5. **先完成静态画面。** 根入口使用 `index.html`；需要竖屏时，在 `compositions/` 放独立 composition。先让每个镜头在静态状态下成立，再加运动。
6. **添加确定性定格运动。** 使用 GSAP 的暂停时间线、场景起止时间和有限次数的 `steps(n)`。步行、奔跑或骑行角色要把身体重心、左右腿和脚部动作拆成可独立控制的层或姿态帧，至少让摆腿、落脚和身体上下起伏相互配合；单张整身 PNG 只做有限位移，不要用整身平移伪装连续行走。角色动作可以按约 10–15fps 的有限帧节奏更新；持续数秒的背景推拉和镜头移动使用 `power1.inOut` 等连续缓动，不能用过低的 `steps(8)`、`steps(10)` 造成明显跳帧。用轻微平移、缩放、旋转、抖动和停顿表现手工定格感。禁止 `Math.random()`、`Date.now()`、`repeat: -1` 和互相覆盖的 CSS/GSAP transform。
7. **添加字幕与片尾。** 字幕是 HTML 图层，保证在不同画幅下可读。片尾只放用户需要的正式文案，禁止 `preview`、`draft`、`test`、`Codex` 或内部提示词。
8. **添加分层声音。** 音乐和事件音效分别作为本地音频。每个 `<audio>` 写清 `data-start`、`data-duration`、`data-track-index`、`data-volume` 和淡入淡出；嵌套竖屏 composition 的非零起始 cue 增加 `data-hf-media-start-basis="local"`。占位音频只能用于草稿，不能混进成品时间线。不要用白噪声直接冒充海浪、风、火焰等自然环境音；没有合适素材时留空或降低声音密度。交付前按 `references/audio-layout.md` 分别检查各音轨和混音。
9. **为平台重新构图。** 竖屏不能只裁切横屏。设置 `data-width="1080" data-height="1920"`，保留主题主体、关键地标和字幕，把文字放在中央安全区，并重新定位角色和道具。详见 `references/vertical-export.md`。
10. **渲染、抽帧和复核。** 运行 lint、validate、渲染、ffprobe 和 contact sheet。检查画幅、时长、字幕、素材层级、重复物体、漂移方块、结尾内部标记、H.264 视频和 AAC 音频；实际试听单独音轨和成片混音的开头 0–5 秒、主要转场及结尾。ffprobe 和电平检查不能代替听感检查。详见 `references/workflow.md` 和 `references/audio-layout.md`。

## 通用项目约定

- 保持一个根 `index.html`；备用画幅放在 `compositions/`，避免 HyperFrames 发现多个根入口。
- 真实地标或主题主体使用真实栅格素材；CSS 几何图只能用于临时布局，不作为最终视觉资产。
- 地点型视频的片头 1–3 秒必须出现至少一个真实的地点识别元素（地标栅格图、建筑轮廓、街景或交通设施）；地图线条和抽象标题只能作为辅助层，不能替代片头地标。片尾优先沿用片头已经出现的同一地标资产或其明确的夜景/远景版本，保持地点识别的首尾一致。
- 透明素材进入 composition 前必须在浅色和深色背景各检查一次；低 alpha 的背景色块、黑边、白边、雾状矩形和抠图残片要在素材层清理，不能靠混合模式或字幕遮住。
- 主题内容由 brief 决定，不能在 skill 中预设城市、线路、日期、职业或固定角色。
- 每个道具都要在素材清单中标明“内嵌在 PNG”或“独立图层”。如果是内嵌道具，就不要再绘制同语义 CSS 层。
- 需要环境道具时使用明确的 ID 和注释，例如闸机、炉子、门、列车或雨丝，避免让环境物体看起来像粘在角色身上的标记。
- 不使用真实公司 logo、个人信息或无授权音乐；通用标牌、生成纹理和本地确定性音频优先。

## 验证命令

```bash
npm install
npx hyperframes lint
npx hyperframes lint compositions/vertical.html
npx hyperframes validate --no-contrast
npm run render
npm run render:vertical
```

竖屏导出后，用实际项目的 `ffprobe-static` 检查：

```bash
FFPROBE=$(node --input-type=module -e "import p from 'ffprobe-static'; console.log(typeof p === 'string' ? p : p.path)")
python3 scripts/check_render.py outputs/final-vertical.mp4 \
  --ffprobe "$FFPROBE" --width 1080 --height 1920 --max-duration 60
```

最终 contact sheet 至少要包含片头、主体动作、转场、高潮/结果和片尾。渲染成功不等于视觉正确：只要出现无法解释的白色、棕色、蓝色或灰色方块，重复地标、重复道具、漂移物体或内部预览字样，就必须回到素材归属审计重新处理。

## 支持文档

- `references/workflow.md`：通用 brief、素材清单、镜头结构和验收标准。
- `references/compositing-audit.md`：内嵌道具归属、重复图层和视觉伪影检查。
- `references/vertical-export.md`：9:16 安全区和重新构图规则。
- `references/audio-layout.md`：通用音乐/音效布局和响度检查。
