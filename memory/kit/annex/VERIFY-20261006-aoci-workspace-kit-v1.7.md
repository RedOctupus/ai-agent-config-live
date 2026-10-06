# Kit v1.7.0 × AOCI 工作区隔离验收

- **范围：** 仅本仓两份权威 Kit Skill 与 `experiments/aoci-memory-kit/`；原 SSSS 不写，已有本机 Skill 不覆盖，全局 MCP 不注册，不 push。
- **需求：** 单人 clone 可直接 Kit-only；团队以 Git clone/worktree 隔离而非按人/模块；新人写源码前提醒；个人图仅供审查、源码先合再更新全局图；Kit/AOCI 各自升级；三宿主真实验收。
- **TDD：** 先写 W01–W10 计划和 RED，再候选 GREEN；最终 29/29 `unittest` PASS（含双副本一致性、README 部署契约回归）。两份权威 Skill 变更文件字节一致，技能校验各 PASS；`check-memory-size.py`、`git diff --check` PASS。
- **真实源码集成：** 隔离 Git 两分支各自 `verify` 报 stale 后独立维护对齐；集成分支只先提交合并后的源码，Verify 报两处 stale；重签全局基线后 Verify=0、Check=0、Guide complete=true/next_action=none，再单独提交基线。冲突测试停止源码补丁且未改正式地图。该样本仅改源码注释，不证明语义质量或自动语义冲突识别。
- **真实宿主：** Codex、Claude Code、Cursor Agent CLI 均在各自 worktree 真实调用 AOCI MCP，完整 Overview 13 Entry、Host delivery confirmed、Attestation 10/10、当前系统认知 reliable=true，并核对源码。Codex/Claude 首轮猜 receipt 版本只部分通过；新会话按返回版本重测通过。Cursor `ask` 模式未暴露项目 MCP，普通非交互调用被拒；隔离 worktree 中 `-p --trust --approve-mcps --force` 的新会话才通过。宽授权不作为正式项目默认配置。
- **原项目：** `snapshot.py verify-source`：原 SSSS 330 个选定文件及 Git 状态未变。Codex 用户配置临时 trust 标记已移除；文件 SHA 未恢复试前值，可能有其他变化，未整体覆盖。
- **限制：** 尚未做跨 Kit/AOCI 版本升级兼容、跨模型地图语义质量对照和多人远程竞写实测；不能将配置存在等同于宿主自动触发，也不能将隔离试验中的 `--force` 当作最小授权方案。
- **详细用例/原始证据：** [隔离试验 VERIFY](../../../experiments/aoci-memory-kit/VERIFY-20261006-workspace-hosts.md)；原始 JSON/日志在忽略的 `experiments/aoci-memory-kit/artifacts/raw/`。
