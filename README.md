# Clay Themed Stop-Motion

一个可复用的 Codex skill，用来生成主题驱动的黏土定格短视频。

它不绑定某个城市、角色或故事，适用于旅行、日常生活、厨房、节日、品牌世界观、城市漫游和其他主题视频。核心流程是：先分析参考风格，再生成统一的本地栅格素材，用 HTML/GSAP/HyperFrames 编排分层画面、定格式运动、字幕和声音，最后导出横屏或竖屏 MP4 并抽帧验收。

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

把这个目录作为 Codex skill 安装或复制到 `$CODEX_HOME/skills/`，然后让 Codex 按当前 brief 生成视频工程。主题内容来自用户当前需求；仓库中的规则不会预设城市、日期、职业、交通线或固定角色。

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
