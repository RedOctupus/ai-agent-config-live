# 外部参考（地址簿）

> 指针文件。2026-09-21 从 README / kit SKILL / 本会话已知外部项搜集。

------

## GitHub 本仓（来源）

```text
- **去哪看：** https://github.com/RedOctupus/ai-agent-config-live （私仓）
- **本项目用途：** 备份与 kit 权威源
- **相关指针：** README.md
- **最近核实：** 2026-09-21
```

## project-memory-kit（本仓内权威副本）

```text
- **去哪看：** materials/agent-skills/cursor/project-memory-kit/ 与 materials/agent-skills/claude/project-memory-kit/
- **本项目用途：** kit 源；本机 ~/.cursor/skills/project-memory-kit 是安装位置不是源
- **相关指针：** 该 SKILL.md「改 kit 本身」；其它项目默认 docs/memory/，本仓特例 memory/kit/
- **最近核实：** 2026-09-21
```

## Hermes Agent（外部运行时）

```text
- **去哪看：** 本机 D:\09-其他\hermes-agent\ ；配置 ~/.hermes/
- **本项目用途：** materials/skills/ 与 materials/hermes/ 的备份对象
- **相关指针：** memory/hermes/machine.md · materials/hermes/config.yaml
- **最近核实：** 2026-05-24（路径来自导出，未在本次重跑 hermes doctor）
```

## Open Code Review（参考实现 / 已备份技能）

```text
- **去哪看：** https://github.com/alibaba/open-code-review ；NPM @alibaba-group/open-code-review
- **CI/CD：** https://open-codereview.ai/docs/cicd ；GitHub Actions 示例 https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md ；Action 定义 https://github.com/alibaba/open-code-review/blob/main/action.yml
- **本项目用途：** Cursor 平铺技能 materials/agent-skills/cursor/open-code-review/
- **相关指针：** 该目录 SKILL.md · install.md · cicd.md
- **最近核实：** 2026-09-21
```

## AOCI-CODE（Kit 可选源码地图接口）

```text
- **去哪看：** https://github.com/aoci-spec/aoci-code （README）；宿主接入 https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/docs/agent-integrations.md ；Overview 交付协议 https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/spec/public/aoci-overview-delivery-v1.txt ；发布包 https://github.com/aoci-spec/aoci-code/releases ；升级 https://github.com/aoci-spec/aoci-code/blob/main/docs/upgrading.md ；安装校验 https://github.com/aoci-spec/aoci-code/blob/main/docs/install.md ；回滚 https://github.com/aoci-spec/aoci-code/blob/main/docs/rollback.md
- **本项目用途：** Kit v1.7.1 的可选项目级 MCP 接口；rc18 官方包保存在 materials/tools/aoci/，用户授权部署本配置仓；业务项目不自动建图
- **相关指针：** materials/tools/aoci/README.md · annex/NOTE-20261006-aoci-code-memory-kit.md · annex/VERIFY-20261006-aoci-codex-session.md · annex/VERIFY-20261006-aoci-workspace-kit-v1.7.md · annex/VERIFY-20261006-aoci-upgrade-checklist.md · annex/VERIFY-20261006-memory-tools-deploy.md
- **最近核实：** 2026-10-06（三宿主真会话与两分支集成试验）
```

## Cursor Agent CLI（AOCI 第三宿主待验）

```text
- **去哪看：** https://cursor.com/docs/cli/overview ；Windows 安装 https://prod.cursor.com/docs/cli/installation
- **本项目用途：** 只为隔离试验安装并登录官方 CLI；工作区 MCP 真会话已验，不代表已把 Kit 安装进 Cursor
- **相关指针：** annex/VERIFY-20261006-aoci-workspace-kit-v1.7.md
- **最近核实：** 2026-10-06（CLI 已登录，隔离授权会话通过）
```

## ASD-STE100 Skill / SimpleEnglish（英文写作技能对标）

```text
- **去哪看：** https://github.com/danyuchn/asd-ste100-skill ；https://github.com/AminBlg/SimpleEnglish
- **Cursor 规则机制：** https://cursor.com/docs/context/rules
- **本项目用途：** Agent 英文指令消歧与面向人的英文文档写作规则候选
- **相关指针：** annex/NOTE-20261007-ste-skills-comparison.md
- **最近核实：** 2026-10-07（源码与文档研究）
```

## 建仓计划（来源）

```text
- **去哪看：** materials/plans/2026-05-24_192600-agent-config-repo.md
- **本项目用途：** 当初把私仓做成 living backup 的计划
- **相关指针：** README Structure
- **最近核实：** 2026-09-21
```
