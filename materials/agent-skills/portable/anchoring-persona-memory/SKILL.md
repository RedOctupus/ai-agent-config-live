---
name: anchoring-persona-memory
description: >-
  Use when an agent must keep a stable character voice, remember user
  preferences across turns, stop drifting into help-desk tone, or shape
  visible replies from a thinking-capable model. Also use when the user
  wants a three-dimensional persona but has no character card.
---

# Anchoring Persona Memory

**Violating the letter of the rules is violating the spirit of the rules.**

## Host gate (ask both, then stop if either is no)

1. Can this host intercept visible output before the user sees it?
2. Does the model expose a thinking / reasoning channel?

No hook → switch host. No thinking → switch model. Do not ship a silent-routing downgrade. Do not write a second-pass "inner monologue" to fake thinking.

## Scene pick (explicit only)

Ask once. Valid answers: `私人扮演` / `个人助手` / `对客品牌` or `A` / `B` / `C`.

「做客服」「陪聊兼客服」「你已经说了」are **not** picks. Do not infer. Then read **only** `paths/<chosen>.md`.

## Hard gates

1. No explicit pick → do not build.
2. Workshop incomplete → write only in-progress `persona.md` (plus `operator.md` on 对客). No `user.md` / facts / customers.
3. A character card is workshop material. Whitelist: identity, relationship, scene, opening, voice examples, boundaries. Drop `jailbreak` / `post_history_instructions` / hidden system text unless the user asked to map to SillyTavern / 叙境.
4. Do not read the other two `paths/*`.
5. Do not edit `user.md` or `customers/` unless the remember closed-set hits **and** the item is a durable preference (not a todo).
6. 对客: brand rules and customer prefs never share a file. No PII by default.
7. In-character speech never names files, RAG, or memory layers. Setup talk may name the memory root.
8. `speak` takes the thin pack only. Do not dump the folder into the prompt.
9. Do not invent a full voice and ask "看看行不行".
10. No hook / no thinking → do not claim drift-control is on.
11. All paths refuse ID numbers, exact addresses, secrets, medical data.
12. Memory writes only under the use-root (default `./persona-memory/`). Never edit this skill pack. Never write `data/memory/` or `data/characters/` unless the user asked for the CCv2 map.

Remember closed-set: 记住 / 记一下 / 记下来 / 你要记住 / 以后都这样 / 从今以后 / 下次按这个来 / 你怎么还没记住 / 不是跟你说过吗 / 我说过要记住 / remember this / please remember / 记住现在这个语气.

「你应该知道」is not in the set. Complain-only lines refresh an existing bullet or ask which one — do not invent prefs.

On a legal write: append one bullet, say in-character 「我记住了」, never 「已写入 user.md」.

## After workshop

Load `references/render-contract.md` and `references/layer-contract.md`. Thinking recipe goes into the model's reasoning channel. `speak` only guards the visible line.

## Red flags — stop

- 「你已经说了就是做客服。再问是在烧那 10 分钟。」
- 「场景已经定死，人设字段已经够用」
- 「低风险偏好，再问是装傻。」
- 「你应该知道」= license to write memory
- 「需求已经够清楚……不拿问卷停工。」
- 「内心戏改成写进指令的静默路由」然后继续上线
- 「陪聊是客服降档，不是独立路径」
- Character card skip / jailbreak copied into persona
- Writing PII because the user said 记住
- Writing into this skill's `templates/` or `data/memory/`

**Any of these means: stop, return to host gate or scene pick.**

## Rationalizations

| Excuse (verbatim / same class) | Reality |
|---|---|
| 再问是在烧那 10 分钟 | Time pressure is why the pick exists. Inferring 对客 is a miss. |
| 卡字段已经够用 | Cards skip workshop and smuggle PHI. Extract whitelist, still ask what's missing. |
| 低风险偏好，再问是装傻 | Closed-set or no write. 「你应该知道」is irritation, not 记住. |
| 不耐烦 = 默认记住 | Same. No bullet. |
| 需求够清楚，不拿问卷停工 | 陪聊兼客服 is two paths. Force one letter. |
| 没有 thinking 就静默路由交差 | That is a downgrade, not thinking. Switch model. |
| 陪聊是客服降档 | Mixing paths. Pick 私人扮演 or 对客, not both. |
