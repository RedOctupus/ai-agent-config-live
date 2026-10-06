# TODO

> 只留项目级待办。模板里的 DSH 示例已删。

------

## 进行中

（无）

## 待办

- [ ] Cursor 正式项目的最小 MCP 审批路径 — 验收：不用 `--force`、不用全局放开权限，仍可在受信任隔离工作区真实调用 Rules/Overview/Attestation/Entry 并保持无源码写入
- [ ] Kit/AOCI 独立升级与团队语义冲突回归 — 验收：隔离工作区做至少一轮跨版本兼容检查和同对象分支提案人审，失败不覆写正式地图/本机配置
- [ ] 核对工具版本清单是否过期 — 验收：`README.md` 与 `tools/catalog.md` 的 Last sync / 版本号与本机 `git --version`、`node -v`、`hermes doctor`（若在 PATH）对齐，或文件头注明「仍以 YYYY-MM-DD 快照为准」
- [ ] ⛔ 等 核对工具版本清单是否过期 —— 若确认过期则改 README Installed Tools 表 — 验收：表内 git/node 与本机命令输出一致

## 已完成

- [x] 2026-10-06 Kit/AOCI 仓内分发与三宿主安装 — 11 项 TDD、真实包冷安装与 Codex/CC/Cursor 接入通过；见 `annex/VERIFY-20261006-memory-tools-deploy.md`。

- [x] 2026-10-06 Cursor CLI 独立工作区真实宿主验收 — `task-cursor` 新会话调用 AOCI Rules/Overview/Attestation/Entry 并核对源码；Host delivery confirmed、10/10；隔离试验需宽授权，见 `annex/VERIFY-20261006-aoci-workspace-kit-v1.7.md`
- [x] 2026-09-21 init 本仓 `docs/memory/`（后迁到 `memory/kit/`）— 见 `annex/VERIFY-20260921-init-memory-kit.md`
- [x] 2026-09-21 目录三分：脚手架 / 记忆 / 本地物料，并补 gitignore — 见 `annex/VERIFY-20260921-classify-repo-layout.md`
