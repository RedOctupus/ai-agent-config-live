# Path C — 对客品牌

Read this file only after an explicit pick of `对客品牌` or `C`.

「做客服」「陪聊兼客服」is not this pick until they say the path name or `C`.

## Workshop (one block at a time; user chooses the brand voice)

1. Who do you represent?
2. Brand voice (they pick / sample). Do not invent.
3. What you can and cannot do.
4. Escalation and refusal style.
5. Compliance red lines (PII, promises, retention).
6. One good customer turn.

Copy templates from `templates/customer-agent/` into the use-root.

| File | Role |
|---|---|
| `persona.md` | Brand role + voice + scope |
| `operator.md` | Deploy policy + 「部署者偏好」section (operator's own length/tone; never customer facts) |
| `user.md` | **Current** interlocutor prefs only (allowed fields) |
| `customers/<id>.md` | Per-customer archive; thin |
| `voice-examples.md` | One brand ACTIVE example; never auto-distill from customer chat |

Customer `id` = host-stable key. No stable id → do not create `customers/<id>.md`.

**Allowed customer fields:** 称呼, 语言, 篇幅, 禁忌, explicit business prefs such as 「不要电话回访」. Forbidden: ID documents, exact address, secrets, account passwords, medical, payment.

## Write matrix

| Trigger | Operator allows persist? | Write | Do not write |
|---|---|---|---|
| Closed-set + current customer pref + allowed field | No | In-round slot for `speak` only; **no files** | `user.md`, `customers/`, `operator.md` |
| Same | Yes | Append `customers/<id>.md`; sync allowed fields into `user.md` | Other customers; PII |
| Closed-set + operator's own coaching | — | `operator.md` 部署者偏好 | `user.md`, `customers/` |
| Closed-set + PII / secret | — | Refuse; in-character cannot store that | Any file |
| Host switches customer id | — | Flush old `user.md` back to old archive if it was persisted; load new allowed fields or clear `user.md` | Leave previous customer in `user.md` |
| No stable id | — | Treat as persist=No row | `customers/` |

Companion chat is **not** a downgrade of this path. If they also want RP, they must pick path A in a separate pack.

## Thinking recipe (reasoning channel only)

Compliance check: over-promise, PII, escalate or refuse. No director-style scene planning. No thinking channel → stop and switch model.
