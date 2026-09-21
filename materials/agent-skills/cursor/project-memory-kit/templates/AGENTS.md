# Agent

日常只读 [docs/memory/MEMORY.md](docs/memory/MEMORY.md)。不要每个任务读完 `docs/memory/`，也不要打开 Skill `references/`。
技术选型硬阀门见 MEMORY 第 3 节与第 7 节：每一项技术栈须用户确认后才能当作已定。
大任务开始前先跑 `python scripts/check-memory-size.py`（体量超阈值先裁剪），并刷新 MEMORY §0 的 HEAD。
**改完就同步记忆，别等用户问。** 每轮交付后按 MEMORY §5 落到位：需求条目 → `REQUIREMENTS.md`；选型/模块 → `FRAMEWORK.md`；端到端链路 → `FLOW.md`；跨阶段必知事实 → `HANDOVER.md`（**行内改，可增删**，改完追加一行 `ITERATION.md`）；外部对标 / 外部系统地址 → `REFERENCES.md`（**行内改，可增删**，只放指针、研究正文进 `annex/` 的 NOTE）；代码交付 → `annex/` 一份 VERIFY（**一天做成多件事**再加一份 `INDEX-YYYYMMDD.md` 串起来，只放指针）；有实质变更 → 追加一行 `ITERATION.md`；某阶段一句话真变了才改 MEMORY，小改动不动。
（Cursor 每轮以 `.cursor/rules/project-memory.mdc` 为准；本文件给不读 mdc 的 Agent。）
