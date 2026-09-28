# VERIFY：project-memory-kit few-shot 模板示例

- 日期：2026-09-28
- 关联 TODO：无（模板增强）
- 风险等级：LOW

## 改了什么

- 文件：`materials/agent-skills/{claude,cursor}/project-memory-kit/{SKILL.md,README.md,templates/**}`
- 行为变化：init 复制出的主要 memory 槽位带有精简的“最小示例（可删）”；示例只演示填写形状，不提供真实项目事实。
- 版本：kit 从 v1.5.0 升为 v1.6.0。

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `python scaffold/scripts/check-memory-size.py` | PASS：体量达标 |
| 手工 | `git diff --check` | PASS：无空白错误 |
| 手工 | Claude / Cursor templates 逐字 diff | PASS：两份模板一致 |
| 手工 | 检查 TODO、版本号与示例标记 | PASS：具体 DSH 示例改为通用可删示例；版本均为 v1.6.0 |

## 未执行

- 项：在全新临时仓库实际运行 init 流程
- 原因：本次只改模板内容，未改 init 脚本；静态模板与双副本一致性已核对

## 结论

- 需求是否覆盖：已覆盖；主要 memory 槽位和 annex 模板均有精简 few-shot 打样。
- 旧功能是否破坏：未改 init 拷贝逻辑；仅增加模板注释 / 示例并按规则升版。
- 剩余风险：示例仍需由使用者在 init 后删除或替换；模板之外的本地安装副本尚未同步。
- 建议人工再验：用 kit 在一个临时目录 init，确认示例可见且不会被误当成项目事实。
