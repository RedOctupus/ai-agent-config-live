# VERIFY：沙盒真实 Codex 新会话

- 日期：2026-10-06
- 关联：`experiments/aoci-memory-kit/` 隔离试验；不改正式 Kit，不测原 SSSS
- 风险等级：MEDIUM（本机 Codex 信任表与可写审批）

## 改了什么

- 本机 `~/.codex/config.toml` 只为沙盒路径增加 `trust_level = "trusted"`。
- 沙盒源码、`aoci.txt`、`.aoci/baseline.json`、`.aoci/config.json` 相对会话前快照未变。
- `.aoci/ledger.jsonl` 追加三条审计：`rules`、完整 `overview`、`attestation`。索引 SHA-256 仍是 `99b5f3a01efffe2faecdf85839b99efc880183ac4d04d270f1ffdae74c67c98b`。

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 宿主 | 沙盒为根的 `codex exec`，线程 `01a10f4a-d771-73d0-9b3d-60ac24564efc` | PASS：项目受信任后 MCP 服务器 `aoci` 可见 |
| 宿主 | 只读且默认不审批的前一次 exec | FAIL：`aoci_rules` 返回 approval policy is never。`--approve-for-me` 与 `--sandbox read-only` 不能同用 |
| MCP | `aoci_rules` 后完整 `aoci_overview` | PASS：`0.1.0-rc18`，13 条，约 2645 tokens，正文 9001 字节，`completed=true`。此时 `host_delivery_unconfirmed`，`model_full_cognition_reliable=false` |
| MCP | 同一 Challenge 再交 Attestation | 第一次因多了 `path`/`f` 被 schema 拒绝。只改字段名为 `object_identity`/`core_f` 后 `model_attestation=pass`，`host_delivery_confirmed`，`cognition_level=4` |
| 源码 | 对照 `review_contract.py`、`reviews.py`、`risk_triage_service.py` | 调用链是路由 → `RiskTriageService.start` → `validate_proposal`。两文件之间没有 import。形状错误整包 `incomplete`。决策哈希与链版本在服务的决策路径，不在提议校验器 |
| 对照 | 会话前沙盒 zip 与结束后逐文件比对 | 仅 `ledger.jsonl` 变长。未调用 Maintain / Update |

## 未执行

- 项：会话自称的 12 个不落盘边界样例
- 原因：本轮只核对了关键源码行，没有重跑那些样例
- 项：多人多机、故障注入、把候选合入正式 Kit
- 原因：不在这次宿主验收范围

## 结论

- 需求是否覆盖：补上了「真实 Codex 新会话按 Kit 指针完成认知确认」。索引对齐和 Attestation 通过不等于源码理解正确。
- 旧功能是否破坏：正式 Kit、原 SSSS、全局 MCP 未改。成功的会话具备工作区写入能力，但源码索引未改。
- 剩余风险：`codex exec` 默认不审批；未受信任项目看不到项目级 MCP。回滚包在 `experiments/aoci-memory-kit/artifacts/raw/sandbox-pre-approved-session.zip`（不入库）。
