# Chapter 4: 工具

## Core Idea
工具是连接 Agent 大脑（LLM）与真实世界的“手脚和感官”。构建实用 Agent 需要解决两大挑战：一是工具成百上千时如何准确高效地发现和选择工具；二是 Agent 如何响应邮件、日历、系统告警等外部事件而不陷入同步等待。工具设计的质量直接决定 Agent 能走多远。

## Frameworks Introduced

- **五类工具分类**：
  - 感知工具：Agent 主动获取信息（搜索、读取文件、数据库查询）
  - 执行工具：Agent 改变外部世界（写文件、执行命令、调用 API）
  - 协作工具：Agent 与其他 Agent 或人类协作（子 Agent、人类确认）
  - 用户沟通工具：Agent 主动向用户传递信息（回复、通知、卡片）
  - 事件触发工具：外部世界驱动 Agent 执行（定时器、Webhook、邮件、告警）
- **工具的两个设计维度**：调用方向（谁发起）与作用对象（作用于什么）。
- **能力表达形式的权衡**：专用工具（结构化 schema、确定性高） vs Skill + 通用执行器（自然语言描述、易维护、可组合）。
- **选择依据**：参数复杂度、变更频率、模型能力。参数复杂且稳定 → 专用工具；变化频繁且模型强 → Skill + 通用执行器。
- **工具粒度权衡**：整合与分离。功能相似、参数重叠 → 整合（如 read_document 统一 PDF/DOCX/PPTX）；差异大、使用频率极高 → 分离。
- **工具通用性原则**：通用工具优于专用工具，除非安全、权限或性能有明确理由。
- **MCP（Model Context Protocol）**：模型上下文协议，统一工具生态，让工具接入像安装插件。
- **工具描述的艺术**：名称、描述、参数 schema 必须精确、可验证、无歧义，引导模型正确调用。
- **参数传递保真性**：参数类型、校验、错误处理直接影响工具调用成功率。
- **感知工具设计**：粒度与输出信息量的控制；避免过载或信息不足。
- **执行工具设计**：安全是核心；沙箱、权限、确认、错误恢复缺一不可。
- **协作工具设计**：子 Agent 的委托、消息、取消、发现。
- **事件驱动的异步 Agent**：注册事件源 → 事件触发 → Agent 唤醒执行；适合耗时任务、中断管理、外部事件响应。
- **用户沟通工具设计**：从单 session 问答扩展到多渠道异步消息。
- **主动工具发现**：当工具数量庞大时，Agent 需要能发现可用工具而非死记硬背。

## Key Concepts

- **Tool / 工具**：Agent 与外部世界交互的能力单元。
- **Tool Calling / Function Calling**：LLM 通过结构化方式调用外部工具的机制。
- **MCP（Model Context Protocol）**：统一工具描述、发现和调用协议。
- **Perception Tool**：感知工具，获取信息。
- **Execution Tool**：执行工具，改变世界。
- **Collaboration Tool**：协作工具，驱动其他 Agent 或人类。
- **User Communication Tool**：用户沟通工具，向用户传递信息。
- **Event-Triggered Tool**：事件触发工具，由外部事件唤醒 Agent。
- **Tool Schema**：工具的名称、描述、参数结构定义。
- **Sandbox**：沙箱，隔离执行环境。
- **Tool Discovery**：主动工具发现机制。
- **Async Agent**：异步 Agent，事件驱动而非同步轮询。
- **Webhook / Timer / Channel**：常见事件触发源。

## Mental Models

- **Tools = Action Space**：工具的种类、质量、定义精度决定 Agent 能做什么。
- **Prefer generic + powerful tools**：七个基础工具（Code Interpreter, Bash, Read/Write/Edit, Glob, Grep）能组合出大量能力。
- **Tool description is the UI for the model**：模型通过描述理解工具，描述就是接口设计。
- **Execution tools demand safety first**：执行工具的代价是真实的，必须沙箱、权限、确认、回滚。
- **Event-driven beats polling**：让外部世界通知 Agent，而不是 Agent 不断询问。
- **Skill + executor = dynamic tool creation**：当能力变化快时，用 Skill 描述流程比新增专用工具更灵活。

## Anti-patterns

- **工具接口模糊**：描述不清、参数无校验，导致模型乱调用。
- **工具过多过细**：数量爆炸增加模型选择负担，破坏 KV Cache。
- **忽视执行工具安全**：无沙箱、无权限控制、无确认机制。
- **同步-only 设计**：无法处理耗时任务和外部事件。
- **错误处理缺失**：工具失败导致 Agent 死锁或无限重试。
- **把用户沟通当作副作用**：不设计显式用户沟通工具，导致异步场景混乱。
- **工具生态碎片化**：每个工具一套协议，缺乏 MCP 等统一标准。

## Code Examples

```json
// 工具定义示例：感知工具
{
  "name": "web_search",
  "description": "Search the web for real-time information",
  "parameters": { "query": { "type": "string" } }
}

// 执行工具
{
  "name": "write_file",
  "description": "Create or overwrite a file. Use with caution.",
  "parameters": {
    "path": { "type": "string" },
    "content": { "type": "string" }
  }
}

// 事件触发工具
{
  "name": "set_timer",
  "description": "Register a timer that triggers the agent at a specific time",
  "parameters": { "when": { "type": "string", "format": "date-time" } }
}
```
- **What it demonstrates**：工具定义必须清晰、有明确参数 schema、说明使用场景和约束，模型才能正确选择和调用。

## Worked Example

**场景：工具粒度整合——read_document vs 多个 extract_* 工具**

初始设计：
- `extract_pdf_text(file)`
- `extract_docx_content(file)`
- `extract_pptx_content(file)`

问题：工具数量膨胀，模型每次都要判断文件类型再选工具，增加认知负担，破坏缓存。

整合设计：
- `read_document(file, file_type: "pdf" | "docx" | "pptx")`

优势：模型只需记住“读取文档用 read_document”，统一入口便于扩展新格式，减少 KV Cache 占用。差异大的场景（如 OCR vs 视频解析）仍保持独立。

## Key Takeaways

1. **工具是 Agent 的“手脚和感官”**：没有工具，LLM 只能纸上谈兵。
2. **通用工具优于专用工具**：通过组合少量通用工具解决大量问题，减少生态碎片化。
3. **MCP 是统一工具生态的关键标准**：让工具接入像安装插件。
4. **工具描述就是接口设计**：精确的名称、描述、schema 直接决定调用质量。
5. **执行工具安全是底线**：沙箱、最小权限、错误处理、确认机制缺一不可。
6. **事件驱动让 Agent 从被动变主动**：响应外部事件、管理耗时任务、支持异步中断。
7. **工具数量大时需要主动发现机制**：不要假设模型能记住成百上千个工具。

## Connects To

- **Ch 1 AI Agent 入门**：工具是 Agent 三元公式的“手脚”。
- **Ch 2 上下文工程**：工具定义作为上下文的一部分，直接影响模型行为。
- **Ch 5 Coding Agent**：Coding Agent 的七个核心工具是通用工具设计的典范。
- **Ch 8 Agent 的持续进化**：Agent 根据使用经验沉淀新工具/Skill 的能力。
- **Ch 10 多 Agent 协作**：协作工具与多 Agent 系统的协调机制。
