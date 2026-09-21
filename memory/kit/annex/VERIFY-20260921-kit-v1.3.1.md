# VERIFY：project-memory-kit v1.3.1（设计文文首 + §3 裁成指针）

- 日期：2026-09-21
- 关联 TODO：无（用户同意两刀：文首进度戳、§3 改指针）
- 风险等级：LOW（只改设计记录与版本号；JinRong §4–§5 未动）

## 改了什么

| 动作 | 文件 |
| --- | --- |
| 文首进度戳改为：Part 1 已落地（版本见 `SKILL.md`）；Part 2 未开始 | `references/design-20260921-dated-log-index.md` |
| §3 改成现网指针表；删过时的「新建 `INDEX.md`」实施清单 | 同上 |
| 版本 `1.3.0` → `1.3.1`（补句） | `SKILL.md`、`README.md`、`templates/MEMORY.md` |
| 本仓跟版 | `memory/kit/{MEMORY.md,HANDOVER.md,ITERATION.md,annex/INDEX-20260921.md}` |

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | 设计文行数 | PASS：222 行（裁前 Get-Content 约 262）；§3 现为指针表；§4 仍从 JinRong 11 步起 |
| 手工 | `git diff --no-index` 两份 kit | PASS：退出码 0 |
| 手工 | `python scaffold/scripts/check-memory-size.py` | PASS：退出码 0；213 行 / §0 517 字符 |
| 手工 | `kit-version: 1.3.1` | PASS：cursor SKILL 顶部 |

## 未执行

- 未 commit / 未 push
- 未并当天多份 VERIFY
- 未动 JinRong §4–§5

## 结论

- 设计文不再当 changelog；Part 2 映射表仍在
