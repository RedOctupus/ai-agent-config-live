# Z-image 场景生图

> Cursor Skill — 维护 `/scene-image` 与 Z-image 集成的参考文档。

## 何时使用

- 调试 `/scene-image` 或 Z-image API 连接
- 修改 `data/zimage/config.json` 映射
- 调整侧车 prompt 或 `:::scene-visual` 格式

## Z-image API（本机）

| 端点 | 方法 | 用途 |
|---|---|---|
| `/api/status` | GET | ComfyUI 是否 ready |
| `/api/generate` | POST | 提交生图 |
| `/api/generate/{prompt_id}/result` | GET | 轮询结果 |
| `/api/presets` | GET | 列出可用 preset slug |

**GenerateRequest 参数：**

- `preset_id`（必填）— API slug，如 `mood-portrait`、`guofeng`（**不是**工作流文件名 `06-氛围摄影`）
- `prompt`（必填）— 英文 SD prompt
- `width`, `height`, `steps`, `cfg`, `seed`（-1 随机）
- 可选：`lora_weights`, `checkpoint_id`, `batch_count`

**GenerateRequest 返回的 `url` 字段**形如 `/api/images/{filename}`，拼完整地址时用 **`http://127.0.0.1:8000` + url**，不要拼在 `apiBase`（`/api`）后面，否则会 `/api/api/images/...` 404。

## 本项目配置

复制 `data/zimage/config.example.json` → `data/zimage/config.json`

```json
{
  "apiBase": "http://127.0.0.1:8000/api",
  "defaultPresetId": "mood-portrait",
  "characterPresets": { "test-scholar": "guofeng" },
  "generateDefaults": { "width": 832, "height": 1216, "steps": 10, "cfg": 1.0, "seed": -1 }
}
```

**Preset slug 对照：** `portrait` · `cinematic` · `guofeng` · `illustration` · `nsfw-body` · `mood-portrait` · `acg-cosplay` · `acg-jk` · `anime-novel` · `base-pure`  
旧中文文件名会通过 `PRESET_ALIASES` 自动映射。

## 命令

```text
/scene-image                 # 默认 mood-portrait
/scene-image nsfw-body       # 指定 preset slug
/scene-image --dry-run       # 预览 capsule + sd_prompt，不生图
```

## 场景帧 Prompt（2026-09-03）

`/scene-image` 使用 **SceneFrameExtractor**（叙境 LLM）从最后一条 Assistant 提取结构化场景帧 JSON：

- **英文**：`locked.sd_appearance` 外貌锚点（建模锁定）
- **中文**：`pose_mood`、`expression`、`camera`、`composition`、`environment`
- **禁止** 台词/长叙事直灌 prompt

流程：`buildSceneGeneratePromptFromFrame` → `POST /api/prompt/compose`（`mode: template`，仅 quality_suffix）→ `POST /generate`

Spec：`docs/superpowers/specs/2026-09-03-scene-frame-prompt-design.md`

## 场景胶囊格式

```text
:::scene-visual
summary: ...
appearance: ...
pose_mood: ...
environment: ...
preset: ...
tags: ...
:::
```

侧车 LLM 产出 SceneFrame JSON → 渲染为 capsule；ComfyUI prompt 经 compose 增强，长 prompt 不进 RP 主对话。

## 验收

1. `/character use test-scholar`
2. 聊几轮后 `/scene-image --dry-run` 看 capsule
3. 启动 ZIMAGE 后 `/scene-image` → Harness 会话出现图片 + capsule
4. 下一轮 RP 应含 `persona:scene-visual` 注入

## 插件

`plugins/dsh-zimage-bridge/` — 规格见 `docs/superpowers/specs/2026-09-02-zimage-scene-image-design.md`
