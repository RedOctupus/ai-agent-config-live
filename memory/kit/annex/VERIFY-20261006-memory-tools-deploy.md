# Kit v1.7.1 / AOCI 仓内分发与本机三宿主部署

- **授权/范围：** 用户要求将 Kit、AOCI 发布包与配置入口放在本仓，明确更新 Codex / CC / Cursor 并同步远端；异步确认 MCP 绑定当前配置仓。当前仓只注册 MCP，建图仍另选；原 SSSS 不写。
- **分发：** `materials/tools/aoci/` 收录未改动的官方 rc18 Windows AMD64 ZIP、manifest、SHA256SUMS、Sigstore 签名/provenance、LICENSE / NOTICE / PATENTS / THIRD-PARTY-NOTICES / TRADEMARKS。ZIP SHA-256 与前次官方验证一致；本轮 `gh attestation verify` 约束官方 repo/workflow、tag/source commit 与非 self-hosted runner，再次退出 0。标准库安装器不联网下载。
- **Kit：** 双权威源及试验 candidate 同步到 v1.7.1。init 先定位本机 `memory-tools.json` 并复用仓内来源；没有定位先询问本仓 clone，不在 init 自动下载。Codex 安装在 `~/.agents/skills`，CC/Cursor 各为自己的用户技能目录；三份完整树与对应权威源一致，旧 v1.5.0 技能目录保存在本机 backups。
- **TDD：** RED 因安装器缺失而失败；GREEN 11/11（含 Windows junction 拒绝，无跳过）。覆盖默认预览零写入、坏包/路径拒绝、完整旧技能备份、两组件独立、配置保留/冲突/幂等、已跟踪配置拒绝、显式升级及旧二进制保留、自定义 env 保留。原试验 30/30 PASS；两份 Skill 的 `quick_validate.py` PASS。
- **冷安装：** 将真实仓内包和完整 Kit 安装到忽略的 `materials/_local/memory-tools-deploy/` 临时 home / 空 Git 根，三宿主配置生成、EXE 版本与技能镜像均通过；没有索引或 `.aoci`。结果指针为该目录的 `result.json`。
- **真实本机：** AOCI 安装在 `~/.local/share/ai-agent-config/aoci/0.1.0-rc18/`（含 notices）；三份项目 MCP 均绑定本配置仓，加入 Git 忽略。Codex 用户配置只添加本仓 trust，CC 本仓本机设置仅批准 aoci 并接受当前仓 trust，Cursor 执行 `agent mcp enable aoci`；被改用户配置先备份，其他 MCP/权限保留。
- **宿主验证：** Codex 新会话真实调用一次 `aoci_header`，收到 `not_initialized`（预期），没有初始化；该次仅允许 AOCI header 工具并使用 `--approve-for-me`。CC `claude mcp get aoci` 最终 Connected；Cursor ready / tools 9。这验收部署与连接，当前仓没有完整 Overview/Attestation，不能称地图认知已验收。
- **安全复核：** 原 SSSS 330 文件与预检一致；本仓机器路径配置、安装备份、临时 fixture 不提交。提交前运行体量、diff、包校验和暂存文件检查；远端结果以 HANDOVER 最后核实为准。
- **后续：** git pull 后显式 install 应用；Kit 单独更新不改 AOCI。更换 AOCI 版本需先走升级清单，再 `--component aoci --upgrade-aoci`，各工作区用 `configure --replace-aoci` 切换并复验。当前只捆绑 Windows AMD64；没有做跨 AOCI 版本或第二台机器实测。

- **远端放行：** 本轮实现与此前已确认的 Kit/AOCI 改动已推送私仓 `origin/main`；随后从远端全新 sparse clone，校验 ZIP / EXE 并在临时 home 安装，三份 Kit 完整镜像和 EXE 版本通过。机器路径/备份/试验原始资产未入库。
