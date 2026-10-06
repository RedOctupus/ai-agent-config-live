# AOCI 升级清单入口验收

- **范围：** Kit Claude/Cursor 双权威 README 与静态契约测试；仅完善已启用 AOCI 项目的规范化升级入口。未安装新版本、替换二进制、改 MCP 配置或重建 `.aoci`。
- **依据：** AOCI 官方 `docs/upgrading.md`、`docs/install.md`、`docs/rollback.md`；具体升级仍须以用户确认的目标版本发布说明和相应 tag 为准。
- **TDD：** 先增 `test_human_readme_has_version_neutral_aoci_upgrade_gate`，RED 因清单缺失失败；再补目标版本确认、冻结、包校验、宿主实际版本/`--repo`、工作区 Verify/Check/Guide、放行/回滚和停止条件。定向 9/9、全量 30/30 PASS；Claude/Cursor README SHA-256 一致。原始 RED/GREEN 日志在忽略的 `experiments/aoci-memory-kit/artifacts/raw/`。
- **安全复核：** `check-memory-size.py` PASS；`git diff --check` PASS；`snapshot.py verify-source` 确认原 SSSS 330 个选定文件与预检一致。未 push、未同步到本机已装 Skill。
- **结论/边界：** 这证明清单入口和文档契约齐备，**不证明**任何未来 AOCI 版本的二进制兼容、持久化迁移可逆性或真实宿主升级成功。Kit v1.7.0 不因 README-only 更新升版；若未来接口契约变化，另按 Kit TDD/升版规则处理。
