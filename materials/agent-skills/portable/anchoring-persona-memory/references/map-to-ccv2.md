# Map to CCv2 / 叙境

Read this **only** when the user explicitly wants SillyTavern or this repo's DSH plugin. Do not open it to "be complete".

This table is a Harness field map. It is **not** the portable `pack` order and does not license a seven-layer prompt rebuild.

| This skill | 叙境 / CCv2 |
|---|---|
| `persona.md` | `description` + `personality` + `scenario` + `system_prompt` |
| `voice-examples.md` ACTIVE | `mes_example` / L4 active example |
| `user.md` short summary | `data/memory/user.md` (trimmed) |
| `protagonist.md` | `user-persona.json` |
| `world-facts.md` | lorebook / L5 |
| thinking recipe | `persona:director-thinking` → reasoning (`buildDirectorThinkingBlock`) |
| `speak` reminder | post-history channel (`post_history_instructions` / `persona:phi`) |

Do not replace `.cursor/skills/persona-jailbreak-inject`. That skill operates DSH jailbreak / PHI toggles.

If 叙境 already injects director thinking, still run `speak` on the visible exit so the draft cannot leak planning or drop the voice.
