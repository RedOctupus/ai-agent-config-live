# Cursor 用户全局规则（可复用资产）

机主 Cursor 账号里的 User Rules 快照。其他 Agent 读这里借鉴写法。本配置仓干活时不注入这份规则。

## 文件

| 中文职责 | 路径 |
| --- | --- |
| 规则全文快照 | `RULES.md` |
| 借鉴方式与维护约定 | `README.md`（本文件） |

## 其他 Agent 怎么借鉴

1. 先读 `RULES.md`。按目标项目取需要的条目。
2. 人类明确说在某个项目启用时，才把选中的条目写进那个项目自己的规则，或那个账号的 User Rules。
3. 人类点名要整份启用时，才把全文放进目标项目的规则。默认整份只作参考。
4. 在本配置仓干活的 Agent 以 `.cursor/rules/project-memory.mdc` 和根 `AGENTS.md` 为准。

## 怎么维护

- 账号里的 User Rules 变了：人说明变更后，改 `RULES.md`，并改下面的快照日期。
- 本目录改了，不会回写 Cursor Settings。账号里改了，也不会自动改本目录。
- 不放 API key、token。当前快照没有密钥。
- `scaffold/scripts/sync-skills.sh` 与 `restore.sh` 不碰本目录。更新靠人点名后改文件再提交。

## 快照

- 日期：2026-10-06
- 来源：当时注入会话的 Cursor Settings → Rules → User Rules（账号云端，不在 Git 里）
- 条目：提交、拉取请求、网页验收、表述、冲突裁决、规则 1–5、技能、简体中文
