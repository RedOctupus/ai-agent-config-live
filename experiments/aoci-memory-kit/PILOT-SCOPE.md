# 首轮 Managed Scope（只供复现实验）

在独立沙盒执行 `aoci init` **之后、首次 `scan` 之前**确定规则，避免从默认约 220 个候选源码直接全量写条目。本页只记录试点边界，不授权在原 SSSS 项目上执行。

## 显式纳入的 12 个代码文件

```text
ssss_agent/main.py
ssss_agent/config.py
ssss_agent/controllers/chat.py
ssss_agent/controllers/reviews.py
ssss_agent/controllers/memory_cards.py
ssss_agent/services/desk_service.py
ssss_agent/services/event_router.py
ssss_agent/services/graph_projection.py
ssss_agent/services/memory_card_service.py
ssss_agent/services/review_contract.py
ssss_agent/repositories/mysql.py
ssss_agent/repositories/milvus.py
```

除此之外，根 `AGENTS.md` 由默认规则纳入；空的 `ssss_agent/__init__.py` 被机器列为 `code_skipped`，无需 Entry。最终 13 条 Entry 只是**有限切片**，不能代表整个 SSSS。

## 排除/观察

- 目录级 exclude：`docs/`、`.cursor/`、`scripts/`、`ssss_agent/adapters/`、`ssss_agent/views/`、`ssss_agent/web/`、`ssss_agent/data/`、`ssss_agent/models/`，以及 controllers/services/repositories 各目录先排除再由上述精确文件规则纳入。
- 文件级 exclude：`.env.example`、`.gitignore`、`.gitattributes`、`docker-compose.yml`、`pytest.ini`、`requirements.txt`、`requirements-eval.txt`；glob exclude：`AGENTS.md.backup.*`。
- 其余测试文件多数为 observe，仅参与变动感知，不写语义 Entry。首次扫描后 Scope 身份冻结；要扩大试点应依当前 AOCI Guide 的 Scope Change 流程，不直接改索引文件。
- 最终 Scope 计数 index 17／observe 106／exclude 223；计数涵盖机器识别对象/派生文件，不能等同实际 13 个已写语义对象。

本切片围绕聊天入口、事件路由、人审契约、图投影和记忆卡；其余服务没有完整索引，不能凭此索引推断端到端行为。详见 [VERIFY-20261006-sandbox.md](VERIFY-20261006-sandbox.md)。
