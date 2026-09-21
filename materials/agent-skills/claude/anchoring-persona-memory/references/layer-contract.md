# Layer contract

Use-root default: `./persona-memory/`. Skill pack stays empty of real people.

## `persona.md`

```markdown
# 身份
# 口吻
# 边界
```

No jailbreak text. No user prefs. No plot diary.

## `user.md`

Bullets only. Durable prefs (address, length, taboos). No secrets. No in-fiction protagonist bio (that is `protagonist.md` on path A). Append one line per legal remember. Cap 8 KB; archive old bullets first.

## `protagonist.md` (path A only)

Name + in-fiction bio. May be empty.

## `operator.md` (path C only)

Deploy policy, retention, whether customer persist is allowed, section `## 部署者偏好`.

## `voice-examples.md`

```markdown
## ACTIVE
(one example only)

## HISTORY
(path A versions; other paths may omit)
```

`speak` and the thin pack read ACTIVE only.

## Fact files (`world-facts.md` / `knowledge.md` / customer extras)

```text
id: wf-012
keys: [name, alias]
content: standalone snippet
source: workshop | user-remember | import
updated: ISO-8601
```

## Forbidden writes

- This skill's `templates/`
- `data/memory/` or `data/characters/` unless user asked for `map-to-ccv2.md`
- Whole-file overwrite of `user.md` (append only)
