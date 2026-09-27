# 实现流程

> 从 README Maintenance / Quick Recovery 与 `agent-skills` 同步规则归纳的 to-be（也是现在正在走的路）。

------

## 1. 链路总览（与 MEMORY 快照同一句话）

```text
本机改技能 → 拷进 materials/ 对应夹 → commit/push；灾难恢复走 restore.sh。
```

## 2. 主链路

```text
本机运行时技能目录（~/.cursor/skills 或 ~/.hermes/skills 等）
↓ 有变化才拷贝（Cursor：只往远程）
本仓 materials/agent-skills/<runtime>/ 或 materials/skills/<category>/
↓ git add / commit / push
GitHub 私仓 RedOctupus/ai-agent-config-live
```

## 3. 分支

```text
日常备份：scaffold/scripts/sync-skills.sh / 手工拷目录 → commit「sync: YYYY-MM-DD」或 feat 说明
Hermes 记忆导出：scaffold/scripts/sync-memory.sh → memory/hermes/
灾难恢复：clone → scaffold/scripts/restore.sh → 复制 materials/hermes/.env.template 到 ~/.hermes/.env 并手工填 key → hermes doctor
从远端「取回某个技能来用」：仅当用户明确说；拷到 ~/.cursor/skills/<name>/ 或 ~/.claude/skills/<name>/
Superpowers：备份插件缓存到 materials/agent-skills/cursor/plugins/superpowers/；恢复靠重装 Cursor 插件，不是拷 skills 目录
本仓 kit 记忆：只写 memory/kit/；体量门闸 python scaffold/scripts/check-memory-size.py
```

## 4. 每步输入 / 输出

| 步骤 | 输入 | 输出 | 约定 |
| --- | --- | --- | --- |
| 发现本机技能变更 | 本机 skill 目录 | 要拷的文件夹列表 | 有变化才提交 |
| 拷入仓库 | 本机目录 | `materials/agent-skills/` 或 `materials/skills/` 下同名树 | 平铺 vs `suites/` 见 agent-skills README |
| 提交推送 | 工作区 diff | GitHub `main` | 私仓 |
| 恢复 | 空本机 / 新机器 | 本机 Hermes 配置 + 技能 | 密钥不在仓内，须手填 |
| 本仓记忆维护 | 任务结果 | `memory/kit/` 源文件 + 必要时 MEMORY 一句 | 改完就同步，别等用户问 |

## 5. Agent / 复杂业务设计路由

```text
用户提出 Agent / 能力模块 / 角色视图 / 多 Agent / 记忆或跨域需求
↓
项目入口规则读取 MEMORY 并判断 L0–L3
↓
L2/L3 加载 business-context-first-agent-design
↓
有 Kit：使用 memory/kit/BUSINESS-CONTEXT.md 并回写 REQUIREMENTS / FLOW / FRAMEWORK / TODO / ITERATION
无 Kit：按 Skill 兼容模式使用 docs/agent-context/
↓
GREEN 可实现；YELLOW 只能做受控原型；RED 先补业务上下文
↓
实现后更新 VERIFY 和项目记忆
```

## 6. 关键数据约定

```text
技能身份 = 目录名；入口文件必须是 SKILL.md
Cursor 成套技能放 materials/agent-skills/cursor/suites/<suite>/
memory/hermes/ ≠ memory/kit/
其它项目的 kit 默认路径仍是 docs/memory/（不要改 kit 模板副本）
```
