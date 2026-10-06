# Kit × AOCI TDD 联动验证（2026-10-06）

## 结论

**协议级联动跑通，正式宿主闭环尚未验证。** 候选 Kit 明确将单人/多人和 AOCI 启用/不启用作为两个独立 init 选择；未启用项目在负责槽位提示 Kit-only。启用的沙盒里，Kit MEMORY 指向 AOCI 入口；一次真实源码修改引发索引漂移，MCP 维护后对齐，并在同轮完成 Kit VERIFY/ITERATION。未比较 AOCI 与 Kit 的效果高低。

## TDD 与用例结果

先写 [测试计划](KIT-INTEGRATION-TEST-PLAN.md)，再写契约/端态测试，跑 RED，最后仅改实验候选和独立沙盒、跑 GREEN。

| 范围 | RED | GREEN |
| --- | --- | --- |
| Kit 候选契约 | 初轮 6 项未通过（`artifacts/raw/tdd-red.txt`）；追加多人模块状态回归测试 1 FAIL（`artifacts/raw/tdd-red-team-status.txt`） | 初轮 6/6 通过（`artifacts/raw/tdd-green-contract.txt`）；最终候选 7/7 通过 |
| 沙盒端态 | 2 FAIL、1 ERROR、3 PASS（`artifacts/raw/tdd-red-sandbox.txt`） | 与契约合跑 13/13 通过（`artifacts/raw/tdd-green-all.txt`） |

| ID | 结果 | 证据/边界 |
| --- | --- | --- |
| K01 | 通过 | 沙盒 MEMORY 唯一 `kit:aoci-status` 指针可达根 AGENTS；`check-memory-size.py` 通过。 |
| K02 | 部分 | 真实 stdio MCP 返回 `aoci_rules`、完整 `aoci_overview`（13 Entry，`completed=true`）和目标 Entry；但 Host 交付仍 `host_delivery_unconfirmed`，严格 Attestation 未完成。不能声称完整系统认知可靠。 |
| K03 | 通过 | 沙盒 `review_contract.py` 仅改有限数判断一行；离线向量测试与既有 `tests/unit/test_review_llm.py` 9 passed。 |
| K04 | 通过 | 改后 `verify` 退出 1，stale 仅该源码；一次 MCP Maintain 签发一个候选，模型基于源码提交绑定 SHA/candidate/batch 的完整 Entry；Update `applied/aligned/remaining=0`；依次 Verify/Check/Guide 均退出 0，Guide `complete=true, next_action=none`。 |
| K05 | 通过 | 沙盒同轮新建 `docs/memory/annex/VERIFY-20261006-kit-aoci-source-task.md`，ITERATION 追加一行；MEMORY 不记战报。 |
| K06 | 通过 | `snapshot.py verify-source` 显示原 SSSS 330 个选定文件及 Git 状态与试前相同；未改主仓 Kit 权威副本/全局配置；无业务服务或数据库操作。 |
| K07 | 静态契约通过 | 候选 Skill 规定已启用但 MCP 不可用/索引不对齐时继续 Kit＋源码/测试受限工作，显式标待维护、不得宣称闭环；未做真实宿主故障注入。 |

## 部署结论与待验

- 架构是**一个 Kit Skill＋每 Git 仓一个 AOCI 项目级 stdio MCP 配置**，不是两个 MCP；各机器各自注册绝对路径。详见 [DEPLOYMENT.md](DEPLOYMENT.md)。
- 本轮只改 `experiments/aoci-memory-kit/kit-candidate/` 和忽略的 `sandbox/ssss-agent/`，没有把候选合入正式 Kit。官方宿主接入细节见 [AOCI v0.1.0-rc18 文档](https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/docs/agent-integrations.md)。
- 2026-10-06 补验：沙盒受信任后，真实 Codex 新会话可见 AOCI MCP；`codex exec --approve-for-me` 完成 Overview 与严格 Attestation。详见 `memory/kit/annex/VERIFY-20261006-aoci-codex-session.md`。默认 exec 不审批会挡住 MCP，不能写成「打开会话就自动调用」。
- 仍未验：多人多机部署、故障注入、长期质量。用户若决定采用，下一步应先审候选 diff，再获授权改 Kit 权威模板；不能把沙盒宿主会话当成正式 Kit 安装。
