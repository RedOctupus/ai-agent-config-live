# ASD-STE100 Skill 与 SimpleEnglish 对比

核实日期：2026-10-07（Asia/Shanghai）。本次为源码与文档的只读研究，没有运行模型改写实验；结论是使用建议，不代表用户已确认安装或技术选型。

## 来源快照

| 项目 | 核实分支 / commit | Skill 版本 | 最近提交（UTC） |
| --- | --- | --- | --- |
| [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) | master / `32511c6992ecb5f1971e46a2943f2e6adceedafe` | 0.4.0 | 2026-10-04 06:18:56 |
| [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) | main / `a6fcb4fde098b33617cc1578d151ebf58774b883` | 2.1.1 | 2026-10-05 15:38:37 |

GitHub API 中两者的 `fork` 均为 false；这只能说明不是 GitHub 标记的 fork，不能证明没有借鉴关系。两者仓库许可证均为 MIT，核心材料是写作规则与检查脚本。

## 主要区别

| 维度 | asd-ste100-skill | SimpleEnglish |
| --- | --- | --- |
| 核心目标 | 减少 Agent / 下游系统理解英文时的歧义 | 让领域外读者理解英文文档，并约束 AI 聊天回复的风格 |
| 常见输入 | 工具说明、系统提示、Agent 间指令、错误消息、状态报告 | README、runbook、API 指南、发布说明、事件报告、说明文与日常回复 |
| 模式 | Strict 与 STE-flavored，按文本类型推断 | 默认 Plain；明确提及 STE / ASD-STE100 / compliance 时用 Strict，聊天回复仍为 Plain |
| 意义保留 | 明确保留事实、数字、条件、范围和 may/could 等不确定性；必要时保留复合时态或长句并标记 | 明确保护代码、标识符、命令、路径、引用错误和事实，但又禁用 should/would/may/might/could；必需的 should 改为 must，任选的删除 |
| 聊天输出 | 默认只给改写正文，按请求给规则与前后对比；有必要时加 Kept as-is | 对所有聊天回复要求连续正文，不用标题、项目符号、粗体或表格；文档本身可保留必要结构 |
| 检查工具 | 标准库 Python 结构检查器，支持 JSON、baseline、禁用规则和自测；不检查语义等价或官方词典合规 | 正则结构检查器、回复格式评分、可复算评测与 CI；另有官方 PDF 词表提取器和词汇检查器 |
| 集成形态 | 仓库根 SKILL.md，README 主打 Claude Code 与通用 skills CLI | 通用 Skill、独立系统提示词、Claude Code 插件 / output style、Codex 插件 |

核心来源：[前者 SKILL.md](https://github.com/danyuchn/asd-ste100-skill/blob/32511c6992ecb5f1971e46a2943f2e6adceedafe/SKILL.md)、[后者 SKILL.md](https://github.com/AminBlg/SimpleEnglish/blob/a6fcb4fde098b33617cc1578d151ebf58774b883/skills/simple-english/SKILL.md)、[前者检查器](https://github.com/danyuchn/asd-ste100-skill/blob/32511c6992ecb5f1971e46a2943f2e6adceedafe/scripts/ste-lint.py)、[后者检查器](https://github.com/AminBlg/SimpleEnglish/blob/a6fcb4fde098b33617cc1578d151ebf58774b883/evals/ste_lint.py)。本次没有打开两个项目的 Skill `references/`。

## 对使用结果有影响的差别

1. **语义与风格冲突：** 前者把作者置信度当作内容，明确禁止把“可能失败”改成“失败”。后者虽然要求保留事实，却把 may/might/could 作为禁用词，其结构检查器也会计为违规。由这些规则推断，改写故障判断、权限说明或需求时，后者更需要额外检查不确定性和义务强度；这不是本次模型实测结果。
2. **会话级影响：** SimpleEnglish 的 SessionStart hook 会在开始、恢复、清空或压缩会话时注入规则。Claude Code 另有 Markdown 写入后的检查和 Stop 回复检查，均为提示性，不阻断。Codex 只有 SessionStart hook。纯 Skill 安装不包含这些 hook 或 Claude output style。见 [hooks README](https://github.com/AminBlg/SimpleEnglish/blob/a6fcb4fde098b33617cc1578d151ebf58774b883/src/hooks/README.md)。
3. **依赖要按安装形态看：** 两者的 Skill 内容都可由支持 Agent Skills 的宿主读取；运行 Python 检查器需要 Python。SimpleEnglish 插件 hook 需要 Node.js，词表提取还需用户自有标准 PDF 与 pdftotext，不能把“Skill 无依赖”理解为全部附加功能无依赖。
4. **官方词典边界：** 两者都未随仓库分发完整官方词典。SimpleEnglish 额外提供从用户自有 Issue 9 PDF 提取词表的工具；词汇检查采用基本词形与简单变形匹配，不做词性消歧，不能作为合规裁定。见 [词表工具说明](https://github.com/AminBlg/SimpleEnglish/blob/a6fcb4fde098b33617cc1578d151ebf58774b883/tools/ste-dictionary/README.md)。

## 评测证据与局限

SimpleEnglish 提交了多组模型输出、评分工具和 CI；前者在本次核实目录树中主要提供示例与检查器自测，没有对应的多模型结果目录。但这不证明 SimpleEnglish 的消歧或事实保留能力更强。

注意文档存在时间差：README / CHANGELOG 仍称没有 2.1.0 及之后的复测；[2026-10-05 复测报告](https://github.com/AminBlg/SimpleEnglish/blob/a6fcb4fde098b33617cc1578d151ebf58774b883/evals/results/rerun-2026-10-05/RESULTS.md) 已包含 2.1.1，应以该较新证据补正。

该复测用一个模型、八个问题、两轮生成。2.1.1 相对基线减少 90.8% 的“可见缺陷”，但此指标只数破折号、粗体、标题和列表，不检测事实增加或丢失。2.0.1 的规则块带页面标题后，缺陷减少率从 97.1% 降到 73.5%，说明注入文本的包装也影响结果。没有发现两项目在相同数据、模型和语义指标上的直接对比实验。

## 结合本仓的建议（待选）

- 改 Agent 工具描述、系统提示或跨 Agent 指令：优先参考 asd-ste100-skill 的语义保护规则。
- 改面向人的英文 README、操作手册或说明文，减少套话与术语：参考 SimpleEnglish；是否采用会话级插件须另行决定。
- 同时借鉴时按用途分别调用；两者对情态词和输出格式的规则存在冲突，不宜全局叠加。
- 两者主要面向英文，英文词数限制不直接适用于中文；本次没有中文效果证据。

## 本次落点

初次研究轮只更新外部地址簿、本 NOTE 与 ITERATION；当时项目的需求、框架、链路和阶段快照没有变化。随后用户授权的规则文档修订见下文与 VERIFY。

## 后续：能否整合到 Cursor User Rules

接入评估轮核实前者长度，并参照本仓记忆找到已有全局规则。已读 `materials/cursor-user-rules/{README.md,RULES.md}`；评估基线是 2026-10-06 的账号快照，不是实时读取的 Cursor Settings。该评估轮只提供候选；后续用户授权的仓内修订已在下方标明，账号仍未写回。

### 实测体量

Python 读取上述固定 commit 的原始 UTF-8 SKILL.md，与本仓 RULES.md 比较；token 数由本机已有 tiktoken 的 `o200k_base` 编码计算，不等于所有 Cursor 模型的实际计数。

| 文件 | 原始行数 | 字符数（含换行） | o200k_base tokens |
| --- | --- | --- | --- |
| asd-ste100 SKILL.md 0.4.0 | 139 | 16,334 | 3,598 |
| 本仓 User Rules 快照 | 163 | 4,181 | 2,555 |

网页提取工具会压缩空白行，显示的 114 行不是源文件行数。全量粘贴粗合计约 6,153 tokens，是当前快照的约 2.4 倍；精确合并分词会略有差异。

### 与当前规则的对应关系

| 前者原则 | 已有规则 | 如何处理 |
| --- | --- | --- |
| 同一概念用同一名称，术语有必要时解释 | 规则 1、规则 2 | 不重复添加 |
| 保留数字、条件、范围与例外，精度优先 | 规则 3 | 只补确定性、义务强度与禁止补造事实 |
| 明确指代与逻辑关系，拆分长句、段落 | 规则 4 | 只补动作表达、宣传词与分步指令检查 |
| 默认只返回改写正文 | 规则 2 的实体介绍、规则 5 的交付提示 | 不全局移植；只可限定在用户要求纯文本改写的任务 |
| 英文指令 20 词、说明 25 词，时态与短语动词规则 | 语言要求是简体中文 | 限定到生成或改写的英文技术文本，不把英文语法约束套到中文 |
| 脚本、词典背景、references 路径 | 用户规则是常驻上下文 | 不粘贴；完整检查能力仍需独立 Skill / 文件 |

### 评估时的三种方案（推荐方案已在仓内落地）

- 推荐：把少量缺口合并到现有规则 3 / 4，再补一个英文技术文本的适用范围说明。保留现有结构与精度优先级。
- 完整 Skill 按需调用：适合需要逐条规则报告或结构检查时；省去全局常驻正文，但需要显式安装 / 加载。
- 全文塞入 User Rules：文本层面可行，但重复、常驻体量与输出格式冲突最多，不推荐。

下面保留评估阶段的增补草案。2026-10-07 用户随后授权修改 MD，已在 `materials/cursor-user-rules/RULES.md` 完成融合与去重；最终正文和影响范围见 `VERIFY-20261007-cursor-user-rules-ste.md`，账号未同步：

```markdown
规则 3 · 精度，补充：
保留原文的确定性与义务强度，不把“可能”改成“确定”、把“建议”改成“必须”。改写不得补出原文没有的原因、机制、频率或事实。

规则 4 · 可读性自查，补充：
4. 动作藏在抽象名词里：改成明确的“谁做什么”。
5. 宣传词没有事实支撑：删除，或换成证据和具体行为。
6. 多个操作挤在一句里：每句一个操作，条件写清楚；三步及以上用编号列表。

英文技术文本：
写英文工具说明、提示词、操作步骤或错误消息时，优先主动语态、明确主语、常见词和完整句。指令尽量不超过 20 词，说明尽量不超过 25 词；完整含义优先于词数。只调整自然语言，保留代码、标识符、命令、路径与引用文本。这些英文限制不套用中文，也不覆盖现有实体介绍、交付提示或用户指定的输出格式。
```

平台边界依据：[Cursor 官方 Rules 文档](https://cursor.com/docs/context/rules)。User Rules 是跨项目的 Agent Chat 偏好；规则内容进入模型上下文。官方建议规则聚焦、可执行、有范围，避免整份复制风格指南。账号实际加载效果没有在本轮运行会话验证。
