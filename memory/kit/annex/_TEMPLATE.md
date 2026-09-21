# annex 选哪种（不是 pytest / 评测集）

本目录是 MEMORY 外移夹。按内容选前缀，不要一律叫测试日志。

| 前缀 | 何时写 | 文件名 | 模板 |
| --- | --- | --- | --- |
| **VERIFY** | 交付后：改了什么、跑过什么、PASS/FAIL/未执行、结论 | `VERIFY-YYYYMMDD-短名.md` | [VERIFY.md](VERIFY.md) |
| **NOTE** | 外部研究正文：摘录、提示词、阈值、规格。地址仍只放 `REFERENCES.md` | `NOTE-YYYYMMDD-短名.md` | [NOTE.md](NOTE.md) |
| **CHECKLIST** | 给人逐步点的手工步骤（灌数、点哪、看什么） | `CHECKLIST-YYYYMMDD-短名.md` | [CHECKLIST.md](CHECKLIST.md) |

**不是日志、仍放 annex：**

- `_raw/` — stdout / JSON / SQL 快照 / 截图（不入库；`.gitignore` 已忽略）
- `_archive/` — 过期 VERIFY 归档
- 任务很大（一线一包）可建 `YYYYMMDD-短名/` 子目录，日志仍用上面三个前缀；包内可另有 `README.md` 当目录

复制对应模板到本目录（或子目录）后改名填写。不要改模板文件本身。
