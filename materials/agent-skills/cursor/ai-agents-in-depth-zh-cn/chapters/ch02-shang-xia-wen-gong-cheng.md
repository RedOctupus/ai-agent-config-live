# Chapter 2: 上下文工程

## Core Idea
上下文不是“提示词里塞更多信息”的技术细节，而是决定 Agent 能力上限的核心工程。Agent 在每个决策点能“看到”的全部信息——系统提示词、工具定义、对话历史、工具结果、环境信息——共同构成其观察空间。上下文工程（Context Engineering）就是系统性地设计、组织和提供这些信息，让中等模型在充分信息下胜过顶级模型的盲目摸索。

## Frameworks Introduced

- **上下文决定 Agent 能力上限**：模型智力只是基础，上下文质量才是 Agent 能否在真实业务中发挥作用的关键。
- **上下文 = 系统提示词 + 工具定义 + 对话历史 + 工具结果 + 环境信息**：一切模型在当前决策点能看到的信息。
- **消息四角色模型**：system（开发者规则）、user（用户输入）、assistant（模型历史回复/工具调用）、tool（工具执行结果）。理解每种角色的语义和优先级是上下文工程的基础。
- **API 调用无状态化**：每次调用必须包含模型所需的全部上下文，模型不会“记住”之前对话。
- **Chat Template**：从 API 消息到模型 Token 的转换模板，决定消息如何被序列化、角色如何被编码。
- **KV Cache 友好的上下文设计**：上下文不仅是长度问题，更是缓存复用问题。合理组织消息顺序和可复用片段可显著降低成本和延迟。
- **Prompt Cache 与 KV Cache 双层级缓存**：KV Cache 在模型层，Prompt Cache 在 API 层，两者设计目标不同但互补。
- **系统提示词四维设计**：语气与风格（人格）、结构化格式、流程驱动 vs 规则堆砌、业务规则细化。
- **Few-shot 示例设计**：在何时给模型看例子、给多少、给什么，以提升复杂任务稳定性。
- **工具定义设计**：工具名称、描述、参数schema 直接决定模型调用质量；描述要精确、可验证、避免歧义。
- **提示注入（Prompt Injection）**：上下文安全的核心威胁，需要通过输入隔离、输出过滤、权限控制等手段防御。
- **动态提示词与 Agent Skills**：Skills 是领域能力的可组合单元，可作为上下文的模块化注入。
- **Agent 状态栏（Status Bar）**：通过元信息增强 Agent 轨迹管理，让 Agent 在上下文中感知时间、任务进度、自身状态。
- **上下文压缩策略**：分层压缩、检索而非推理、隔离优于压缩（子 Agent 上下文隔离）。

## Key Concepts

- **Context Engineering**：上下文工程，设计和管理 Agent 在每个决策点能看到的全部信息。
- **System Prompt**：系统提示词，定义 Agent 身份、行为规则、约束条件，最高优先级指令。
- **Chat Completions API**：以消息列表为核心的 API 调用模式。
- **KV Cache（Key-Value Cache）**：Transformer 推理缓存，避免重复计算前缀。
- **Prompt Cache**：API 层面对重复前缀的缓存机制。
- **Tool Definition / Tool Schema**：工具的名称、描述、参数结构定义。
- **Prompt Injection**：恶意输入劫持模型行为的攻击方式。
- **Agent Skills**：可组合的领域能力模块，可动态注入上下文。
- **Agent Status Bar**：承载 Agent 状态、进度、时间感知的元信息结构。
- **Context Compression**：在保留关键信息的前提下减少上下文长度的策略。
- **Sub-agent Isolation**：通过子 Agent 隔离上下文，避免信息膨胀和冲突。

## Mental Models

- **Think of Agent  as 永远的新员工**：给足背景信息就干得好，什么都不告诉再聪明也白搭。
- **Context is the true bottleneck**：决定 Agent 能力上限的不是模型参数量，而是每个决策点能获得的精准上下文。
- **Prefer structured context over long context**：结构清晰、信息密度高比单纯长度长更重要。
- **Cache is an architecture constraint**：上下文设计要考虑 KV Cache 和 Prompt Cache 的复用模式，而非只看 token 数。
- **Isolation beats compression**：与其压缩海量信息，不如用子 Agent 隔离不同职责的上下文。
- **Treat context as a product**：上下文工程是产品工程，不是提示工程。

## Anti-patterns

- **把上下文当垃圾桶**：什么都塞进系统提示词，导致关键信息被稀释。
- **忽视工具定义质量**：描述模糊、参数不精确，导致模型乱调用工具。
- **假设模型有记忆**：不在每次请求中提供完整上下文，导致多轮对话断裂。
- **轻视提示注入风险**：把不可信用户输入直接拼接到系统提示词中。
- **过度压缩丢失关键信息**：为了省 token 把业务规则、约束条件压没了。
- **混合多个角色的职责**：system/user/assistant/tool 消息混用，导致模型对信息来源和优先级产生误解。

## Code Examples

```json
// 上下文窗口的构成：system + tools + user + assistant + tool + reasoning
{
  "model": "Qwen3",
  "messages": [
    { "role": "system", "content": "You are a helpful coding assistant." },
    { "role": "user", "content": "北京今天天气怎么样？" },
    { "role": "assistant", "content": "", "tool_calls": [{ "function": "get_weather", "arguments": { "city": "北京" } }] },
    { "role": "tool", "tool_call_id": "call_1", "content": "{\"temp\":\"23°C\",\"conditions\":\"晴\"}" }
  ],
  "tools": [{ "name": "get_weather", "description": "Search weather", "parameters": { "city": "string" } }]
}
```
- **What it demonstrates**：API 调用的无状态性要求所有上下文必须在每次请求中完整构造，包括系统规则、用户输入、历史 assistant 消息、工具结果和工具定义。

## Worked Example

**场景：Coding Agent 的上下文最小集合**

要让 Agent 修复“帮我修复这个 bug”，至少需要三类信息：
1. **代码上下文**：代码库目录结构、模块职责、核心数据结构、代码规范
2. **流程规范**：Git 分支策略、提交规范、代码审查流程、CI/CD 要求
3. **环境信息**：开发环境配置、测试数据库地址、staging 部署方式、API 密钥管理

缺少任何一类，Agent 都可能写出“语法正确但风格冲突”或“本地能跑测试环境崩溃”的代码。上下文工程就是把这三类信息系统化地组织到 Agent 的每次调用中。

## Key Takeaways

1. **上下文质量 > 模型能力**：中等模型 + 好上下文 > 顶级模型 + 坏上下文。
2. **系统提示词是最高优先级指令**：定义身份、规则、约束、输出格式，必须精心设计。
3. **工具定义是调用质量的闸门**：清晰的 schema 和描述直接减少错误调用。
4. **缓存设计是工程成本的核心**：利用好 KV Cache 和 Prompt Cache 能大幅降低长上下文成本。
5. **上下文安全不可忽视**：提示注入、权限控制、输入隔离是生产级 Agent 的必修课。
6. **Skills 和动态提示词让上下文可组合**：把领域能力模块化，按需注入，避免一次性加载所有知识。

## Connects To

- **Ch 1 AI Agent 入门**：上下文是 Agent 三元公式中的“眼睛”。
- **Ch 3 用户记忆和知识库**：用户记忆和 RAG 是上下文中“长期知识”的扩展。
- **Ch 4 工具**：工具定义作为上下文的一部分，直接影响模型调用行为。
- **Ch 5 Coding Agent**：代码上下文、流程规范、环境信息是 Coding Agent 的关键。
- **Ch 10 多 Agent 协作**：子 Agent 上下文隔离是协作系统的核心设计维度。
