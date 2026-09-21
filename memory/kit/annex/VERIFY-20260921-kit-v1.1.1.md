# VERIFY：project-memory-kit v1.1.1（`_INDEX.md` 改名 + 版本双写）

> **补记（同日）：** 本文的 `1.1.1` 已纠正为 **`1.2.0`**——该改名动了 init 拷贝目标，按升版规则属「改维护口令」，应中位 +1。理由与复核见 `VERIFY-20260921-kit-v1.2.0.md`。**下文出现的 `1.1.1` 均为当时标记，不是当前版本。**

- 日期：2026-09-21
- 关联 TODO：无（用户：「优化，有让我决定的地方就问我」）
- 风险等级：MEDIUM（改本仓权威源；两份副本必须逐字一致）

## 改了什么

用户拍板三项：Init 拷贝当日索引模板为 `_INDEX.md`；JinRong 设计文留在 kit 不动；kit 版本号 YAML `kit-version` 与正文 `kit v…` 都写。

| 动作 | 文件 |
| --- | --- |
| 新增瘦模板；init 拷 `_INDEX.md`（真下发才是 `INDEX-YYYYMMDD.md`） | `templates/annex/_INDEX.md` |
| 删误拷的无日期 `INDEX.md`；删残留 `templates/tests/_TEMPLATE.md` | 两处 kit 副本 |
| 版本升到 `1.1.1`；拷贝表 / 路径树 / 升版示例跟上 | `SKILL.md`、`README.md`、`templates/MEMORY.md` |
| 存量跟版：缺文件举例与误拷改名写成 `_INDEX.md` | `references/migration.md` |
| 设计文进度戳补 v1.1.1 改名（正文与 JinRong 映射不改） | `references/design-20260921-dated-log-index.md` |
| 本仓记忆跟版 | `memory/kit/{MEMORY.md,HANDOVER.md,ITERATION.md,annex/_INDEX.md,annex/INDEX-20260921.md}` |

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `python scaffold/scripts/check-memory-size.py` | PASS：退出码 0；213 行 / §0 实义 6 行·529 字符 / 最长行 179 |
| 手工 | `git diff --no-index claude/project-memory-kit cursor/project-memory-kit` | PASS：退出码 0（仅 CRLF warning，无内容 diff） |
| 手工 | 残留 `templates/annex/INDEX.md`、`templates/tests/` | PASS：两份副本均为空（不存在） |
| 手工 | `SKILL.md` 顶部 `kit-version: 1.1.1` + 正文 `kit v1.1.1` | PASS：cursor 与 claude 均命中 |
| 手工 | 本仓 `memory/kit/annex/_INDEX.md` 存在、无日期 `INDEX.md` 已删 | PASS：True / False |
| 手工 | 本机 `~/.cursor/skills` 与 `~/.claude/skills` 的 kit 对 cursor 副本 `git diff --no-index` | PASS：无内容 diff；`_INDEX.md` 在、旧 `INDEX.md`/`tests/` 不在 |

## 未执行

- 未 commit / 未 push（用户未要求）
- 未迁 JinRong（用户拍板先不管）

## 结论

- 需求覆盖：三项拍板已落地
- 旧功能：带日期的 `INDEX-YYYYMMDD.md` 规则未改，只改 init 模板文件名
- 剩余风险：改动未入库；新开 Cursor 窗口才一定加载本机已同步的 skill
- 建议人工再验：打开 kit `SKILL.md` 顶部确认 `1.1.1`；说一声才 commit/push
