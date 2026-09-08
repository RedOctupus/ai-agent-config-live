---
name: persona-jailbreak-inject
description: >-
  维护 CCv2 post_history_instructions / jailbreak 字段与 DSH persona:jailbreak
  注入。调试 /jailbreak、导入社区卡 PHI、编辑 data/memory/jailbreak.md 时使用。
---

# 人物卡越狱 / PHI 注入

> Cursor Skill — 维护 CCv2 `post_history_instructions` 与 DSH 运行时 `persona:jailbreak` 注入。

## 何时使用

- 从 Chub / AICC / Tavern 导入人物卡，需要启用或调试 PHI（Post-History Instructions）
- 卡内有 `jailbreak` / `post_history_instructions` 但模型仍「出戏」
- 想全局追加一段历史后约束（不写进每张卡）
- 调试 LLM 每轮实际收到的 prompt 分层

## 概念

| 名词 | 本项目映射 |
|---|---|
| CCv2 `post_history_instructions` | 卡 JSON 字段，解析后注入 |
| 社区 `jailbreak` | 同上（字段别名） |
| SillyTavern PHI | 历史消息**之后**、生成**之前**的 system 段 |
| `persona:phi` (order 90) | Host 内置短提醒（换卡过渡、勿客服腔） |
| `persona:jailbreak` (order 88) | **卡内 + 全局**越狱/PHI 正文 |

注入顺序（高 order 更靠后）：`persona:discipline` → `identity` → `style` → `user-memory` → `lore` → `scene-visual` → `examples` → **`jailbreak`** → **`phi`**

## 卡字段

在 `data/characters/<id>.json` 任选其一（内容相同，别名兼容）：

```json
{
  "post_history_instructions": "（每轮提醒：保持角色，勿 OOC…）"
}
```

或

```json
{
  "jailbreak": "…"
}
```

`system_prompt` 仍在 `persona:style`（会话前段），**不要**与 PHI 混用：ST 语义上 PHI 应在历史之后。

## 全局补充

复制 `data/memory/jailbreak.md.example` → `data/memory/jailbreak.md`

与卡内字段合并：`global + card`，空段自动跳过。单段最多 120 行注入。

## Harness 命令

```text
/jailbreak              # 状态 + 合并预览
/jailbreak on           # 本会话开启注入
/jailbreak off          # 本会话关闭（不影响 persona:phi 短提醒）
/jailbreak reload       # 重读 jailbreak.md
```

典型流程：

1. `/character use test-scholar`
2. `/jailbreak` 确认预览含卡内 PHI
3. 聊一轮；若仍偏客服腔，加强卡内 `post_history_instructions` 或全局 `jailbreak.md`
4. 对比 `/jailbreak off` 与 `on` 的回复差异

## 导入社区卡

1. 导出 JSON，检查 `post_history_instructions` / `jailbreak` / `data` 嵌套
2. **勿盲信 PNG 内嵌 hidden prompt** — 解码后人工审阅再放进 `data/characters/`
3. 过长 PHI 可拆：身份放 `description`，边界放 `system_prompt`，每轮 reinforcement 放 PHI

## 代码位置

| 文件 | 职责 |
|---|---|
| `plugins/dsh-persona-card/src/model/CharacterCard.js` | 解析 CCv2 字段与别名 |
| `plugins/dsh-persona-card/src/model/PromptAssembler.js` | `resolveJailbreakText` |
| `plugins/dsh-persona-card/src/model/JailbreakRepository.js` | `data/memory/jailbreak.md` |
| `plugins/dsh-persona-card/src/controller/JailbreakController.js` | `persona:jailbreak` |
| `plugins/dsh-persona-card/src/controller/JailbreakCommandController.js` | `/jailbreak` |

规格：`docs/superpowers/specs/2026-09-02-persona-jailbreak-inject-design.md`

## 验收

1. `npm run verify` 通过
2. `/character use test-scholar` + `/jailbreak` 显示卡内 PHI 预览
3. `/jailbreak off` 后合并预览仍可见，但注入状态为关闭
4. dsh `--dump-config` 仍含 `persona-card` 插件
