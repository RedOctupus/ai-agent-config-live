# Path A — 私人扮演

Read this file only after an explicit pick of `私人扮演` or `A`.

## Workshop (one block at a time; user chooses the voice)

1. Who are you (name, background, relationship to the other person)?
2. Where are you, what is happening now?
3. How do you speak? Ask for a sample line or adjectives they pick — do not invent a full voice.
4. Opening first line.
5. One exchange: they say X, you say Y.
6. Hard no's.

If they bring a card: extract only identity / relationship / scene / opening / examples / boundaries. Drop jailbreak / PHI.

Done when you can answer: who, how you speak, what you never do, plus with whom, where, first line.

Copy templates from `templates/private-rp/` into the use-root (default `./persona-memory/`).

| File | Role |
|---|---|
| `persona.md` | Identity, personality, scene, boundaries |
| `protagonist.md` | In-fiction user name + bio; may be empty; never put this in `user.md` |
| `user.md` | Cross-session prefs only |
| `voice-examples.md` | `## ACTIVE` one example; `## HISTORY` for older versions |
| `world-facts.md` | Retrievable lore snippets |

## Distill

No compaction hook → distill voice **only** when they hit 记住现在这个语气 / 以后都按现在这样说. With a compaction hook, sidecar-distill "how they speak" into HISTORY and swap ACTIVE. Do not invent plot. ACTIVE ≤ 400 Chinese characters.

## Thinking recipe (reasoning channel only)

Director, third person: read the scene → draft and reject cliché/OOC → lock the visible reply. At depth, ≥300 characters, name the protagonist. Never paste planning words into `spoken`.
