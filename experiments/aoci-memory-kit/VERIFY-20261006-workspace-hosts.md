# Kit × AOCI 工作区与真实宿主验证（2026-10-06）

## 结论与边界

Kit v1.7.0 的**可选** AOCI 接口和团队工作区准入已在隔离试验中验证；不把 Kit 变成第二个 MCP，不自动安装/升级 AOCI，也不把个人地图文本合并。Codex、Claude Code、Cursor Agent CLI 的**真实宿主会话**最终均完成 Overview 交付确认、10/10 Attestation 和源码核对；但都需要各自的信任/审批条件，不能推断“默认自动调用”。本试验没有证明不同模型的地图语义质量相同，也没有做真实多人远程协作或 Kit/AOCI 跨版本升级回归。

## TDD 与工作区矩阵

- 先有 [W01–W10 计划](WORKSPACE-TDD-PLAN.md)，再写契约/CLI 测试；初轮 RED 见忽略的 `artifacts/raw/tdd-red-workspace.txt`（缺 helper/入口等）。加入 receipt、版本一致性、README 部署指引测试后也分别保存 RED。最终 `python -m unittest discover -s experiments/aoci-memory-kit/tests -p 'test_*.py'`：**29/29 PASS**，含权威双副本一致性回归；原始输出 `artifacts/raw/tdd-green-full-workspace.txt`。
- W01：一次性 Git clone 加 Kit MEMORY 模板可直接工作；模板明确 AOCI 未启用，未产生 `.aoci` 或 `.codex/config.toml`；不强制二次工作区。W02–W04：真实 Git fixture 中团队集成分支返回 `needs_workspace`，功能分支 clone/worktree 为 `ready`，显式 `create` 拒绝脏源、已有目标/分支；不会复制本机 MCP 配置。
- W05：独立 `task-codex`、`task-claude`、`task-cursor` worktree 的 `--repo` 各指向自身；各自 AOCI Verify 对齐、运行时 ledger 分开。Cursor `aoci init --agent cursor` 仅输出参考配置，测试者在**该忽略工作区**人工写 `.cursor/mcp.json` 并 gitignore；不声称官方自动写入。
- W06：另建 `task-merge-a/b` 两分支，各自修改**不同受管源码**，各自 Verify 先报 1 个 stale，再通过本工作区 Maintain 签发和 `update-entry` 更新个人基线，Verify/Check 均 0。集成工作区仅取回两个源码文件，提交 `e3aeed1`；此刻全局 Verify 报两个 stale。只在**合并后的源码**重新 Maintain，签发两候选，重新更新全局基线；Verify=0、Check=0、Guide `complete=true, next_action=none`，之后单独提交全局基线 `6dc9049`。没有从个人分支合并 `.aoci/baseline.json`、`aoci.code.txt`、旧 candidate/batch。**本用例只是注释性源码改动，Entry 文本无需语义改写；不能用它证明冲突语义编译质量。** 原始结果在 `artifacts/raw/merge-*.json`。
- W07：`test_workspace_merge_conflict.py` 用两个分支改同一源码行并各写不同地图提案；源码补丁在集成端失败，集成源码和正式地图均保持原状，必须人工裁决。对“Git 可合但 AOCI 同对象语义不同”的检测仍依赖集成人审，未实现自动语义冲突判定。
- W08：Kit Skill 仅保留启用状态、工作区准入、源码任务触发与 Kit 槽位；AOCI 工具版本/状态机仍来自当前 MCP/Guide。未执行真实二进制升级，兼容性**设计通过、跨版本实测未通过**。
- W10：`snapshot.py verify-source` 显示原 SSSS **330 个选定文件与试前一致**；两份 Kit 权威 Skill 的 7 个变更文件逐字一致、`quick_validate.py` 各 PASS；`check-memory-size.py` 与 `git diff --check` PASS。没有 push、没有覆盖本机已安装 Skill。
- 终态复核：`integration`、两条 merge 分支与三宿主工作区共 **6/6** 个 `aoci verify` 退出 0、`governance_aligned=true`、`stale=[]`，见 `artifacts/raw/final-workspace-verify-summary.json`。

## W09：真实宿主，不以配置存在代替调用

| 宿主 / 独立工作区 | 真实结果 | 原始证据 |
| --- | --- | --- |
| Claude Code / `task-claude` | 首次模型猜错 receipt 版本，`model_attestation=pass` 但 host delivery incomplete；**新会话**严格按返回的 `delivery_receipt_version`，`host_delivery_confirmed`、10/10、`current_system_cognition_reliable=true`，读取两 Entry 与源码，无编辑 | `artifacts/raw/host-claude-worktree*.jsonl` |
| Codex / `task-codex` | 首次模型猜错 receipt 版本，部分通过；**新会话**用返回的 `overview-delivery-receipt/v1`，`host_delivery_confirmed`、10/10、`current_system_cognition_reliable=true`，读取两 Entry 与源码，无编辑 | `artifacts/raw/host-codex-worktree-retry.jsonl` 与 `-final.txt` |
| Cursor Agent CLI / `task-cursor` | 官方 Windows CLI `2026.10.01-e373342` 登录后，`mcp enable aoci`/`mcp list` 为 ready。`--mode ask` 会话未暴露本地 MCP；普通非交互会话能发现工具但调用被拒绝；在隔离 worktree 用 `-p --trust --approve-mcps --force` 的新会话才真正调用 Rules→完整 Overview→确认/Attestation→Entry→源码，`host_delivery_confirmed`、10/10、`current_system_cognition_reliable=true`。未编辑源码/配置，终态 Verify=0 | `artifacts/raw/host-cursor-worktree{,-default,-force}.jsonl`、`host-cursor-final-verify.json` |

三个通过的宿主都指出真实源码约束：`review_contract.py` 未显式填 `primary` 时默认 `true`，一个 eligible event 如有重复 primary，会让整个 proposal 降为 incomplete；不是看地图就代替源码核对。Codex 临时用户配置 trust 标记已移除；用户配置恢复 SHA 与试前记录不一致，可能有并发/行尾变动，**未擅自整体覆盖**。团队部署须项目受信任且明确授权 MCP；真实会话成功不等于以后每次自动触发。Cursor `--force` 具备更宽授权，仅用于本次隔离只读任务，不应直接作为真实项目默认开关。

## 后续验收条件

另需真实跨版本 Kit/AOCI 升级兼容回归、不同模型对同一源码的语义质量抽检及同对象提案人审样本，不能从本轮三宿主的协议 PASS 推断通过。特别要为 Cursor 找到不依赖 `--force` 的最小审批路径，再用于正式项目。
