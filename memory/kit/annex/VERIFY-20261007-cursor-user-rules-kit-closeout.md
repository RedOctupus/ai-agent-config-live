# User Rules：Kit/AOCI 交付收尾

日期：2026-10-07。用户要求在技能条款补充结束后的记录 / 源码地图更新，参考 project-memory-kit，规则要自然、明确。

本记录覆盖详则新增时的版本；后续用户要求压缩，收尾改为调用入口，详则交由 Kit / Guide 管理，见 `VERIFY-20261007-cursor-user-rules-compact.md`。

## 改动

- `materials/cursor-user-rules/RULES.md` 的技能条款新增一项“验证结束、最终交付前”。
- 已使用 Kit 的项目：同轮回写交付记录与受影响的记忆文件；实质变更记入 ITERATION，代码战报进 VERIFY，当天多项交付用 INDEX，MEMORY 只改变化的快照。
- 已启用 AOCI 且修改受管源码：按当前 Guide 更新并核验源码地图；同时使用 Kit 时，先核验地图，再回写 Kit。纯文档和只读任务不调用地图维护。
- 工具不可用或核验未完成：记录已完成工作与缺口，不宣称闭环；不会因为地图未核验而省略失败记录。
- README、R20、HANDOVER、ITERATION 与当日 INDEX 同步；本轮不修改账号、不维护地图、不修改 Kit Skill。

依据：`materials/agent-skills/cursor/project-memory-kit/SKILL.md` 的“源码任务与 AOCI”“日常维护”与交付 / annex 约定；没有打开 Skill references。

## 验证结果

- 修改前 / 后对 13 个二级章节正文做 SHA-256 比较（标准化换行）：仅“技能”变化，其他 12 个章节相同；另有文档修订标识更新。
- 已核对新增一条收尾规则，原有 Superpowers 条款保留；Kit 与 AOCI 各按项目已采用的能力触发，同时采用时按地图核验 → Kit 回写的顺序收尾。
- 文本边界核对：只用 Kit 的项目可单独回写；AOCI 必须已启用且存在受管源码变更；文档 / 只读不维护地图；失败仍记录缺口；本条不要求自动初始化 Kit 或启用 AOCI。
- `git diff --check` 退出 0；当日索引链接 3/3 可解析。
- `python scaffold/scripts/check-memory-size.py` 退出 0，MEMORY 217 行、§0 实义 7 行 / 624 字符，体量达标。

只验证规则文档的一致性，不代表已经在 Cursor 账号执行 Kit/AOCI 收尾。
