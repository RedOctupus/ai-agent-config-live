# VERIFY｜AOCI-CODE × Memory Kit：SSSS 隔离试点

日期：2026-10-06。结论：**受限范围的技术链路可行；是否赋能 Kit 尚未验收**。本次只操作本目录新建的 `sandbox/` 与 `artifacts/`，未改原 SSSS 项目、已安装技能、全局 MCP 或 Kit 默认 init；未提交/推送主仓。测试依据为先定稿的 [TEST-PLAN.md](TEST-PLAN.md)。

## 测试对象与安全边界

- 原项目：`D:\课程\9.18(工程化落地、就业课准备)\interview_guideline\就业材料\SSSS agent项目`，**只读**。
- 测试项目：`experiments/aoci-memory-kit/sandbox/ssss-agent/`，独立 Git 工作树，含快照自己的本地基线提交；原项目 `.git` 不复制。
- 快照按 Git 跟踪＋非忽略未跟踪文件纳入 **330 文件、3,659,292 字节**；显式拒绝 `.env*`（`.env.example` 例外）、凭据名、链接/junction、`.git`、`.venv`、缓存和宿主配置。清单在忽略目录 `artifacts/raw/snapshot-inventory.json`。
- `python experiments/aoci-memory-kit/snapshot.py verify-source` 在首轮、漂移试验后、最终均通过：原项目入选文件哈希和 Git 状态字节与预检相同。沙盒 `.env` 不存在，原 `AGENTS.md` 正文作为沙盒新增规则之前的前缀完整保留。
- 未运行 SSSS 应用、pytest、Docker、MySQL、Milvus、Neo4j、DeepEval 或真实 LLM。AOCI 治理结果 `network_accessed=false` 指 AOCI 校验/索引步骤；**不包括**此前从 GitHub 下载发布包的网络活动。

## 供应链与接入

- 使用 [官方 v0.1.0-rc18 发布](https://github.com/aoci-spec/aoci-code/releases/tag/v0.1.0-rc18) Windows AMD64 ZIP；下载文件、SHA256SUMS 与 Sigstore provenance 到忽略目录。ZIP SHA-256 实测与发布值同为 `012072baeead1d37062e431f3191d3338e2e67789baec79549a8e0fd12c4a09b`。
- `gh attestation verify` 对 ZIP 与 SHA256SUMS 均成功，约束官方仓库、`release.yml@refs/tags/v0.1.0-rc18` 证书身份/发行者、源码提交 `ffbdafac512d339aa87342d5b9d1a4f27a299aaf`、tag，并拒绝 self-hosted runner。ZIP 条目先检查路径穿越，再只解出 `aoci.exe`。本机 `aoci --version` 为 `0.1.0-rc18`／上述提交；`doctor` 初始化后全部检查通过。
- `aoci init --locale zh-CN --agent codex` **仅在沙盒运行**，追加沙盒 `AGENTS.md` AOCI 区块，生成索引与基线资产，并生成沙盒 `.codex/config.toml`。该配置 command/args 均指本试验目录绝对路径，且被沙盒 Git 忽略。未修改已运行 Codex 会话的 MCP 配置。通过本目录 [mcp_probe.py](mcp_probe.py) 启动独立 stdio 子进程，`initialize` 返回 server `aoci-code 0.1.0-rc18`，`tools/list`、`aoci_rules`、`aoci_header`、`aoci_maintain`、`aoci_update_entry` 均走真实 MCP 协议成功；这**不是** Codex UI 在新会话自动加载项目级 MCP 的实测。

## 先定范围、再首次扫描

为避免 220 文件的粗放全量索引，在首次 `scan` **之前**按官方 Managed Scope 设置目录排除与 12 个核心源码文件的显式 index 规则；另有根 `AGENTS.md` 与空 `ssss_agent/__init__.py` 由配置计入受管候选。docs、非试点服务/控制器/仓储等排除；测试多数仅 observe。最终机器 Scope 计数：index **17**、observe **106**、exclude **223**（包括初始化生成/派生对象，不能当作 17 条完整代码地图）。首次 `scan` 建立 **123 文件基线，约 491 ms**；Code 实际可读源 **14**，其中 `__init__.py` 为空而 `code_skipped`，应写 Entry **13**。

模型阅读了这 13 个目标的决定性源码，并通过当前 MCP 签发的一个批次写入 13 条 F/R/A/S，而非由 AST/文件名批量生成。首轮 `verify --json` exit 0、`check --json` exit 0、Guide `complete=true,next_action=none`；质量纠偏后最终仍为 **13 Entry、aligned=true、无 stale/missing、Whole-Index 约 2,643 tokens**。原始 JSON 均在被忽略的 `artifacts/raw/`；最终证据为 `verify-opt-final.json`、`check-opt-final.json`、`guide-opt-final.json`。

**可移植性提醒**：本试点 `aoci.code.txt` 的目录段包含沙盒的绝对路径；跨机器、迁移仓库或将索引提交到共享仓后的行为未测试，不应直接照搬当前索引。

## 测试矩阵结果

| ID | 结果 | 可核验事实与边界 |
| --- | --- | --- |
| T01 快照/零写入 | **PASS** | 330 文件清单、原仓状态/哈希始终不变；无 `.env`；独立 Git。 |
| T02 供应链/宿主 | **PASS（本机）** | SHA256＋官方 provenance 通过；二进制版本一致；`doctor` 通过；只指沙盒。未测第二宿主。 |
| T03 规则共存/MCP | **PASS（协议层）** | Kit 原 `AGENTS.md` 保留；沙盒项目级配置被 Git 忽略；真实 stdio MCP 握手和工具调用成功。Codex 新进程是否自动信任/加载未测。 |
| T04 首次索引 | **PASS（13 文件限定范围）** | 模型写 13 Entry；1 空文件跳过；`verify/check/Guide` 最终对齐；约 2,643 tokens。不代表全 SSSS 覆盖。 |
| T05 条目质量 | **PARTIAL** | 对 13 个入索引对象作源码核查，发现并纠正 1 处过度表述：记忆卡语义召回仅在向量行**带有**快照哈希/版本字段时核对这些字段。修订由 `cognition_optimization` 批次写入并重新对齐。原计划至少 20 对象且包括测试/配置的逐项证据评分未达到，不计算质量通过率。 |
| T06 Kit-only 对照 | **未执行** | 尚无同模型、同预算、新会话的五题 A/B 对照，不能声称定位收益。 |
| T07 漂移/增量 | **PASS（单文件）** | 沙盒 `event_router.py` 暂改 UWB 初始 `proposed_close`→`open`，`verify` exit 1 且只报该文件 stale；MCP Maintain 签发 1 候选并更新后 `verify/check/Guide` 对齐。按字节还原源码，再维护该条目，最终对齐且原文件 SHA-256 恢复为 `fcfa93c73a66c1b964404d649f2beff60c228adefecc29b4b2775e2c281f2e5f`。 |
| T08 冲突/降级 | **PARTIAL** | 在沙盒手改 AOCI 索引为与源码相反的 UWB 状态，`verify` exit 1、`result=blocked`、`code_volume_unbaselined`；按字节还原后 exit 0。未测试 Agent 拒绝引用冲突条目、MCP 故障时 Kit-only 降级。 |
| T09 新会话 Overview | **PARTIAL** | 新 stdio MCP 进程中读取 `aoci_rules` 后取得完整 Overview：`completed=true`、13 Entry、约 2,643 tokens、正文 8,995 字节且 SHA-256 与服务器元数据相同。未做真实 Codex 新会话的 Host delivery confirmation/模型 Attestation/压缩恢复；返回仍是 `host_delivery_unconfirmed`，不可声称完整认知已验证。 |
| T10 回滚/清理 | **PARTIAL** | 源码和手改索引两次模拟均按字节还原；最终 `verify` 对齐，原仓零写入，未留 `aoci` 进程。沙盒与取证**有意保留**以供复核，尚未执行完整卸载/删除测试。 |

质量核查的关键源码锚点：`AGENTS.md` 1–12 与 AOCI 区块；`config.py` 9–36；`controllers/chat.py` 13–37；`controllers/memory_cards.py` 30–62；`controllers/reviews.py` 11–70；`main.py` 62–85、144–216（`seed_service.py` 20–92 佐证演示种子清理）；`repositories/milvus.py` 81–155；`repositories/mysql.py` 46–104、320–466、600–638；`services/desk_service.py` 44–152；`services/event_router.py` 21–265；`services/graph_projection.py` 134–258；`services/memory_card_service.py` 38–309、322–507；`services/review_contract.py` 30–118。路径均相对于沙盒根；未经运行行为测试，不把源代码静态核查等同端到端验收。

## 结论与下一闸口

本次证明“**Kit 管决策/交接，AOCI 作为可选代码语义地图＋漂移门禁**”在单机、代码限定范围可运作，且能与沙盒 Kit 规则共存。它还不能证明新增索引的准确率、跨文件问题增益、跨宿主可移植性或维护成本划算；按既定硬/收益门槛，**不启用 Kit 默认 init，也不改原 SSSS**。

下一轮若继续，应先把受管范围扩到至少 20 个源码/测试/配置对象并做逐条证据评分，再做五题 Kit-only 与 Kit＋AOCI 的同模型新会话对照；补真实 Codex 项目 MCP 加载、Overview 确认/Attestation、压缩恢复和完整回滚。任何正式项目安装、模板改动或网络/数据库接入须再次按 Kit 技术选型硬阀门确认。
