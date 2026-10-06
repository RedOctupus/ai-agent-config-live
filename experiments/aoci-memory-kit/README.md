# Project Memory Kit × AOCI-CODE：候选外挂

> 状态：**Kit v1.7.1 已同步两份权威 Skill；原 SSSS 不改，MCP 部署范围见下方**。日期：2026-10-06。所有 AOCI 运行仍只在本目录忽略的沙盒/工作区。

## 目的与边界

给已使用 project-memory-kit 的**代码项目**增加当前代码语义地图，不把每文件职责、接口和强关系塞进 `MEMORY.md`。Kit 继续管服务对象、需求、用户确认的技术选型、端到端流程、交接和验收；AOCI-CODE（候选）管受管源码对象的 F/R/A/S 地图和漂移。源码、测试与人工确认仍是最终证据。AOCI 的 MCP 是宿主连接的项目级服务，Kit 本身不内嵌或代执行 MCP。

Kit init 保持 AOCI **默认不启用**，只有用户明确选择时才为目标工作区单独配置；单人 clone 不强制另建 worktree。多人按 Git 工作区而非人员/模块隔离地图，新人先检查集成分支，功能工作区各自维护，集成时源码先于全局图。此次只在隔离沙盒验证 AOCI，不更改原 SSSS、不触碰业务数据库。

## 候选组成（逐项待用户确认）

| 项 | 候选 | 尚未确定的取舍 |
| --- | --- | --- |
| 语义地图 | AOCI-CODE 官方发布版 `v0.1.0-rc18` 的 CLI + stdio MCP | RC 稳定性、FSL-1.1-MIT 许可、二进制验证；若发布版不适用，是否允许源码构建 |
| 宿主 | 先用一个支持 stdio MCP 的本地编码 Agent 验证，再测 Cursor/Claude 等宿主 | 宿主配置与重启方式；不能假设所有宿主行为一致 |
| 模型写条目 | Agent-native，复用当前宿主模型 | 不配置额外模型 API；模型通道的数据政策仍由宿主决定 |
| 试验目标 | `D:\课程\9.18(工程化落地、就业课准备)\interview_guideline\就业材料\SSSS agent项目` | 此项目有 Kit、真实代码/测试；旁边 `ssss-ops-agent` 是较小伪代码演示，不作首选 |
| 沙盒 | 本目录 `sandbox/ssss-agent/`，独立 Git 快照，仅存测试副本 | 只复制 Git 跟踪与非忽略未跟踪文件，并显式排除 `.env`、凭据、`.venv`、缓存；不复制原 `.git`；快照在独立沙盒有本地基线提交，不推送 |
| 测试工具 | 原项目已有 Python/pytest；快照与静态断言优先用 Python 标准库 | 不默认安装新 Python 依赖，不默认启动 Docker/MySQL/Milvus/Neo4j |

## 文件

- [INTEGRATION-CONTRACT.md](INTEGRATION-CONTRACT.md)：两套记忆的权威边界、读写顺序与失败降级。
- [TEST-PLAN.md](TEST-PLAN.md)：先定测试项目、证据、停机条件，再允许沙盒执行。
- [PILOT-SCOPE.md](PILOT-SCOPE.md)：首次扫描前固定的 12 文件显式纳入范围及排除边界。
- [VERIFY-20261006-sandbox.md](VERIFY-20261006-sandbox.md)：已执行的矩阵、供应链校验、安全复核、未覆盖项和结论。
- [DEPLOYMENT.md](DEPLOYMENT.md)：一个 Kit Skill＋每工作区一个 AOCI stdio MCP、单人/多人与 AOCI 两项正交选择、每机配置及团队集成边界。
- [WORKSPACE-TDD-PLAN.md](WORKSPACE-TDD-PLAN.md)：W01–W10 的工作区、合并和三宿主验收矩阵。
- [VERIFY-20261006-workspace-hosts.md](VERIFY-20261006-workspace-hosts.md)：工作区 TDD、个人图→源码先行集成、三宿主真实会话与未覆盖项。
- [KIT-INTEGRATION-TEST-PLAN.md](KIT-INTEGRATION-TEST-PLAN.md)：先定的 K01–K07 Kit 同轮联动测试计划。
- [VERIFY-20261006-kit-integration.md](VERIFY-20261006-kit-integration.md)：RED→GREEN、源码漂移→MCP 维护→Kit 同轮收尾与未覆盖项。
- [kit-candidate/](kit-candidate/) 与 [tests/](tests/)：仅供审查的 Kit 改动候选及可执行契约/沙盒测试。
- [snapshot.py](snapshot.py)：只复制 Git 清单的封闭快照工具；`verify-source` 在沙盒变动后继续检查原项目。
- [mcp_probe.py](mcp_probe.py)：只连接沙盒二进制/仓库的最小 MCP stdio 探针，不安装全局 MCP。
- `sandbox/` 与 `artifacts/`：本地试验副本及原始证据，均被本目录 `.gitignore` 排除。

## 当前结论

在**受限的 13 个非空代码文件试点**中，AOCI 可对齐、检测漂移并拒绝未经基线认可的手改；原 SSSS 未变化。这证明外挂方式技术上可跑通，**不证明**比 Kit-only 更有效。工作区 TDD 30 项通过，两个个人工作区各自对齐、集成工作区先纳入源码后重签全局基线；三宿主真实 MCP 会话最终通过，但均有明确审批/信任前提。

更早的 Kit×AOCI 源码任务联动是 MCP 协议探针；随后另有真实 Codex、Claude Code 与 Cursor Agent CLI 宿主会话。Attestation 与源码理解的具体结果、Codex/Claude receipt 版本误填重试、Cursor 模式/审批边界见新增 VERIFY。真实宿主调用不等于自动触发：仍需项目受信任、授权 MCP、Agent 遵循入口规则。

来源：[AOCI-CODE 官方 README](https://github.com/aoci-spec/aoci-code)；本仓研究正文见 `memory/kit/annex/NOTE-20261006-aoci-code-memory-kit.md`。仅试验用版本/宿主经用户同意，不构成 Kit 正式技术选型确认。

## 仓内分发落地

2026-10-06 用户另行授权后，Kit v1.7.1 / AOCI rc18 已安装到三宿主，MCP 仅新增绑定当前配置仓，未初始化该仓地图。安装来源与显式更新命令见 [仓内安装入口](../../materials/tools/aoci/README.md)；安装器 11 项 TDD 与真实包离线冷安装、宿主连接见 [部署 VERIFY](../../memory/kit/annex/VERIFY-20261006-memory-tools-deploy.md)。此前报告中的“不改本机/不 push”是相应隔离试验当时的边界，不代表本次授权后的部署状态。
