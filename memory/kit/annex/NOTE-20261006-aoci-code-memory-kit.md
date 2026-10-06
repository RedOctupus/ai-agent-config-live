# NOTE：AOCI-CODE 与 project-memory-kit 的互补性

- 日期：2026-10-06
- 对应 `REFERENCES.md` 条目：AOCI-CODE
- 最近核实：2026-10-06（下文研究写于只读 README 时；沙盒宿主会话见同日 VERIFY）

## 来源

- README：https://github.com/aoci-spec/aoci-code
- 发布包：https://github.com/aoci-spec/aoci-code/releases

## 摘录 / 规格（转述）

- AOCI-CODE 是项目级 CLI + stdio MCP；模型阅读源码后为受管文件写 F/R/A/S 条目（职责、强关系、接口、非显然约束），索引文件与项目一起由 Git 版本化。
- `init` 会写项目规则、空索引和宿主 MCP 配置；`scan` 建立受管基线。MCP 有读取和维护工具，变更后需使索引恢复 aligned。它不是仅靠连接 MCP 就自动理解代码的只读服务。
- 官方 README 称当前候选版为 v0.1.0-rc18，许可证为 FSL-1.1-MIT。结构/治理校验通过不代表模型写出的语义一定正确。完整 Overview 的读取有会话上下文成本。

## 对本项目意味着什么（尚未拍板）

- 推荐研究方向：Kit 管目的、需求、拍板、交接和验收；AOCI 管当前代码对象的职责、接口、强依赖和工程约束；源码与测试仍是最终证据。不要把 AOCI 条目复制进 `MEMORY.md`，也不要让 AOCI 覆盖 Kit 的技术选型门闸。
- 集成位置宜是**目标代码仓的可选外挂**，而非 Kit init 默认步骤。本仓主要是备份和技能树，不适合作为首个大型代码语义地图试验场。
- 关键冲突：Kit 的“日常只读 MEMORY”与 AOCI 的“新会话完整 Overview”会增加阅读负担；两者都写 `AGENTS.md`。若试点，需要明确启用条件、入口顺序、规则合并方式、Scope、双机本地 MCP 路径、降级路径。
- 第一阶段只在独立的实际代码项目做隔离试点：对照若干跨文件改动，测定位正确率、遗漏关系、过时索引告警、首读 token/耗时及维护成本；先确认许可证、二进制来源和宿主兼容性。未获得用户逐项选型确认前，不安装、不写入 FRAMEWORK 的“已定”。
- 候选集成契约和测试矩阵在 `experiments/aoci-memory-kit/`。隔离试验已经执行。真实 Codex 新会话的 Overview 与严格 Attestation 见 `annex/VERIFY-20261006-aoci-codex-session.md`。正式 Kit 仍未启用 AOCI，本文不构成选型。
