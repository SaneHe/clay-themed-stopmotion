# Clay Themed Stop-Motion

一个可复用的 Codex skill，用来生成主题驱动的黏土定格短视频。

它不绑定某个城市、角色或故事，适用于旅行、日常生活、厨房、节日、品牌世界观、城市漫游和其他主题视频。核心流程是：先分析参考风格，再生成统一的本地栅格素材，用 HTML/GSAP/HyperFrames 编排分层画面、定格式运动、字幕和声音，最后导出横屏或竖屏 MP4 并抽帧验收。

## 安装

这是一个给 Codex 读取的 skill，不是需要用户手动复制目录的独立剪辑器。安装后，在 Codex 中提出视频需求，Codex 会按 `SKILL.md` 的规则建立项目、生成素材、编排时间线并导出视频。

### 通过 Codex Skill Installer 安装

直接在 Codex 中告诉它：

```text
请使用 Skill Installer，从 GitHub 仓库 SaneHe/clay-themed-stopmotion 安装根目录的 skill，
并将安装名称设为 clay-themed-stopmotion。
```

也可以直接把仓库链接交给 Codex：

```text
请安装这个 Codex skill：https://github.com/SaneHe/clay-themed-stopmotion
```

Codex 会负责获取、校验并安装，用户不需要手动操作命令行或配置 skill 目录。安装完成后，从下一轮对话开始即可使用，也可以在请求中显式写 `$clay-themed-stopmotion`。

如果已经安装过旧版本，直接告诉 Codex：

```text
请从 GitHub 更新 clay-themed-stopmotion skill 到最新版本。
```

Codex 会先检查现有安装，再按需要更新；不要手动复制 skill 目录。

## 怎么使用

把主题、参考视频或参考图、时长、画幅、平台、字幕和音效要求一起告诉 Codex。例如：

```text
使用 clay-themed-stopmotion skill，制作一个 36 秒、9:16 的黏土定格主题视频。
主题：游客从海岛城市的老街出发，乘船到岛外水岸，傍晚回到海湾。
要求：先写 DESIGN.md、STORYBOARD.md 和 ASSET_MANIFEST.md；生成统一的角色和背景素材；
保留定格动画的 stepped motion；添加主题音乐、环境声、动作声和字幕；
最后输出 MP4、contact sheet，并检查 H.264/AAC、尺寸、时长、字幕和重复道具。
```

需求越具体，生成结果越稳定。建议至少提供：

- 主题故事和角色目标；
- 地点、时代、地标或世界观；
- 角色服装、道具和动作；
- 16:9 或 9:16、目标平台和时长；
- 字幕语言、音乐气质和需要的事件音效。

这个 skill 不会把城市、日期、职业、交通线或角色写死；每次视频都会从当前 brief 读取主题变量。

## 生成项目后的运行方式

skill 会在你指定的项目目录中生成 HTML/GSAP/HyperFrames 工程。进入项目目录后，通常使用：

```bash
npm install
npx hyperframes lint
npx hyperframes lint compositions/vertical.html  # 需要竖屏时
npx hyperframes validate --no-contrast
npm run render
npm run render:vertical                              # 需要竖屏时
```

渲染脚本和输出文件名由具体项目决定。横屏通常使用 1920×1080，竖屏使用 1080×1920；最终以项目的 `DESIGN.md` 和用户 brief 为准。

## 音频和素材注意事项

- `scripts/generate_theme_audio.py` 只生成确定性的本地占位音频，用于开发和时间线测试，不应未经试听直接作为成片音效。
- 正式环境音应使用合适的本地录音、已授权音效或经过处理并实际试听的素材。
- 如果角色 PNG 已经带有背包、杯子、相机、卡片等道具，不能再添加同语义的 CSS/HTML 层。
- 交付前要单独试听 BGM、环境声和事件音效，再试听成片开头、主要转场和片尾。

## 内容

- `SKILL.md`：Codex 使用入口和完整工作流
- `references/workflow.md`：brief、素材清单、镜头结构和验收清单
- `references/compositing-audit.md`：角色 PNG 内嵌道具与重复图层检查
- `references/audio-layout.md`：BGM、环境声、动作声和混音验收
- `references/vertical-export.md`：9:16 重新构图和安全区规则
- `scripts/check_render.py`：用 ffprobe 检查画幅、时长、编码和音轨
- `scripts/generate_theme_audio.py`：生成确定性的本地占位音频，仅用于草稿和开发
- `agents/openai.yaml`：Codex skill UI 元数据

## 使用方式

安装完成后，让 Codex 按当前 brief 生成视频工程。主题内容来自用户当前需求；仓库中的规则不会预设城市、日期、职业、交通线或固定角色。

开发阶段建议运行：

```bash
python3 /path/to/skill/scripts/check_render.py outputs/final.mp4 \
  --ffprobe /path/to/ffprobe \
  --width 1920 --height 1080 --max-duration 60
```

交付前必须实际检查片头、主要转场和片尾的声音。`ffprobe`、电平和频谱读数只能证明技术状态，不能代替听感验收；未经处理的白噪声不能直接冒充海浪、风、雨或其他自然环境音。

## 校验

```bash
python3 /Users/sane/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

如果你的环境没有这条系统路径，可以把仓库交给 Codex 校验，或直接检查 `SKILL.md` 的 YAML frontmatter、支持文档链接和脚本可执行性。
