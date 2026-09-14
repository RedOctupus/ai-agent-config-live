# 存量项目收敛（按需读）

不拷进业务项目。目标项目已有 `docs/memory/` 但**不符合本骨架**（缺源文件、MEMORY 超长、战报堆在 MEMORY 里）时，按本 playbook 收敛。**只外移，不删除**。

## 什么时候走这里

- Init 时发现 `docs/memory/MEMORY.md` 已存在且体量/结构不合骨架。
- 已有 memory 系统（含旧名 `MANUAL.md`、或战报 / 仓库地图堆在 MEMORY 正文里）。

## 收敛步骤

1. **盘点现状**：列出 `docs/memory/` 下所有文件与各自行数；标记哪些是「快照/约束」、哪些是「源文件正文」、哪些是「战报/逐轮结果」。
2. **建 tests/ 外移战报**：把 MEMORY 里的逐轮结果、逐缺陷状态、E2E 明细、复跑取证 → 新建 `tests/YYYYMMDD-任务名.md`（用 `_TEMPLATE.md`）；MEMORY 只留一行 `见 [TEST-LOG](tests/…)` 指针。
3. **按骨架重建源文件**：缺哪个补哪个；把已有正文按性质归位：
   - 对方现在怎么办事 → `ENVIRONMENT.md`
   - 拆解条目 / 验收 → `REQUIREMENTS.md`
   - 选型 / 能力模块 / 分层 / 仓库地图 → `FRAMEWORK.md`
   - 端到端怎么走 → `FLOW.md`
   - 变更史 → `ITERATION.md`
4. **MEMORY 裁回 ≤200 行**：只留各阶段一句话 + 约束/入口 + §0 指针；跑 `python scripts/check-memory-size.py` 确认达标。
5. **不可丢内容用指针保留**：任何舍不得删的正文，都放回对应源文件，MEMORY 里留「见 X.md」指针，而不是留在 MEMORY 里。

## 注意

- 重命名旧 `MANUAL.md` → `ENVIRONMENT.md`，不要两份并存。
- 先查 git / 对话里是否还有旧内容，能恢复就恢复，不要用空模板盖掉进度。
- 收敛过程本身记一条 `ITERATION.md`（影响：MEMORY 体量）。
