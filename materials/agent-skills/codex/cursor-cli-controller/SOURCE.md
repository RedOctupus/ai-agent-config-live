# Source and version

- Skill/runtime release: **0.1.0**, authored for this repository on 2026-10-07.
- Authoritative source: `RedOctupus/ai-agent-config-live`, `materials/agent-skills/codex/cursor-cli-controller/`.
- Origin: original controller instructions/runtime developed from the user's approved task contract; this is not a redistributed Cursor product or a fork of Cursor CLI.
- Runtime interface dependency: official MCP Python SDK **mcp==2.3.0** (MIT); no SDK source/binaries or virtual environment are bundled in Git.
- Verified Windows environment: Python **3.13.9**, Cursor Agent CLI **2026.10.01-e373342**.
- Optional project-memory instructions: existing `project-memory-kit` **1.7.1** used for contract reference. Project memory schema is detected separately; Kit is not a mandatory runtime dependency.
- Cursor's subagents, modes and CLI protocol follow the installed CLI and current official documentation; unknown capabilities are reported rather than inferred from a file's presence.
- Package introduction, prerequisite checklist, install/configure commands, platform limits, source hashes and validation summary: `materials/tools/cursor-controller/` in the source repository.

Sources: [Cursor CLI](https://cursor.com/docs/cli/overview), [output schema](https://cursor.com/docs/cli/reference/output-format), [subagents](https://cursor.com/docs/subagents), [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), [Codex MCP configuration](https://developers.openai.com/codex/mcp).

Responsibility attribution and integrity hashes are local evidence records, not cryptographic signatures. Original source is retained under this private repository's terms; the SDK's MIT license does not automatically license this original controller.
