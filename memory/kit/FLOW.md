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
有 Kit：使用 memory/kit/BUSINESS-CONTEXT.md；Agent-to-Agent 实现前先记录协作契约，再回写 REQUIREMENTS / FLOW / FRAMEWORK / TODO / ITERATION
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

## Cursor 控制器资产发布与使用

```text
用户批准设计与责任分工 → 安装副本真实/fixture 验证 → 独立审阅与修复
→ 单源码归档 codex/cursor-cli-controller → 来源/版本/哈希与前置说明
→ 安装器检查/预览、隔离冷安装 → 明确提交本轮路径并推送 main → 核对远端提交

显式安装：verify → install --apply（私有环境）→ configure --apply（只加本 MCP）
使用：doctor + capabilities/Kit/AOCI 检测 → Codex 定目标/责任 → Cursor 执行
→ 确认写者停止 → 必要记忆维护（各维护者各署名）→ 稳定文件 final verify
→ 新批次证据与署名拍板 → MCP 独立审计；有 Kit 才引用到既有 VERIFY/ITERATION
```

## 7. Kit 可选 AOCI 与团队集成（不改变本仓备份主链路）

```text
Kit init：单人 clone 默认可用；明确多人时根 MEMORY 记录用户确认的集成分支
  ├─ AOCI 未启用：负责槽位提示 Kit-only；源码/测试 + Kit 回写，不安装 MCP
  └─ 用户确认启用：目标工作区各自配置本机绝对 --repo / 项目级 MCP，按当前 AOCI Guide 建图

多人新任务：入口读根集成分支 → kit-workspace.py status
  ├─ 集成分支：源码写入前显式创建/切换功能工作区，禁止静默创建
  └─ 功能分支 clone/worktree：独立读写自己的源码与地图（同目录并发写仍需人协商）

集成：个人地图只供审查 → 冲突人审 → 先纳入源码并测试
  → 集成 Agent 对合并后的真实源码重新 Maintain/撰写全局 Entry
  → Verify → Check → Guide 对齐 → 单独交付全局图与 Kit VERIFY/ITERATION
失配：AOCI 待维护而非自动改“未启用”；Kit 与 AOCI 升级各自先验兼容，不自动覆盖配置。

AOCI 版本升级（仅已启用项目）：Kit README 清单 → 用户确认目标版本/工作区/宿主
  → 冻结旧二进制/配置/对齐状态并清理未完事务 → 按目标版本官方文档校验新包、并存试跑
  → 经确认逐宿主切换并核对实际运行版本/--repo → 各受影响工作区 Verify/Check/Guide 与真实宿主回归
  → 全部通过才记录交付；否则按官方说明回滚或因不可逆迁移停下。Kit 不随 AOCI 自动升版。

本仓分发：git pull → install-memory-tools.py verify → install（默认预览，--apply 写入）
  → 三宿主 Kit / 本机 AOCI 与旧资产备份；--component kit/aoci 可分别更新
  → configure --repo <目标根>（显式 --apply）合并三宿主本机配置、先忽略机器路径
  → 宿主批准/目标项目信任 → 真实工具发现 → 需要建图时才按 Kit/AOCI init 与 Guide 进行。
```
