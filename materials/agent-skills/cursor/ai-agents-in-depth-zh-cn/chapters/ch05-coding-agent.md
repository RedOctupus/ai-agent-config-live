# Chapter 5: Coding Agent 与代码生成

## Core Idea
Coding 不是少数专门化 Agent 的专利，而是每个通用 Agent 都应该具备的基础能力。一个能处理任意任务的通用 Agent，其核心架构是 **Coding Agent + 文件系统 + 少量通用工具**。代码是通用 Agent 的元能力：它让思考严谨、可执行、可验证，能在运行时动态创造新工具。

## Frameworks Introduced

- **通用 Agent 的核心范式**：Coding Agent 运行时（推理 + 执行）+ 文件系统（工作空间）+ 多平台消息网关（用户交互）。
- **从 Manus 到 OpenClaw**：工业界实践反复验证，开放任务型通用 Agent 都遵循这一范式。
- **Coding Agent 的七个核心工具**：
  1. Code Interpreter（代码解释器，带沙箱）
  2. Bash Shell（命令行终端）
  3. Read File（读取文件）
  4. Write File（创建/重写文件）
  5. Edit File（局部修改文件）
  6. Glob（搜索文件名）
  7. Grep（搜索文件内容）
- **代码作为元能力的六个方向**：
  - 思考工具：把模糊自然语言写成精确代码
  - 业务规则约束：代码比自然语言更无歧义
  - 多媒体生成：PPT/Word/PDF/可视化通过代码生成
  - 系统适配器：动态生成解析逻辑、API 封装
  - 生成式 UI：把界面需求转成可执行代码
  - Agent 自举：Agent 写代码扩展自己的能力
- **Sessionless 设计**：Agent 的状态保存在文件系统而非长对话 session 中，便于重启、审计、协作。
- **Coding Agent 安全**：沙箱执行、权限控制、人类确认、版本控制、回滚机制。
- **故障与错误恢复**：测试失败 → 诊断 → 修复 → 再测试的循环。
- **代码编辑工具**：文件编辑是代码维护和迭代的核心操作，比完全重写更经济。
- **搜索工具**：Glob + Grep 是 Coding Agent 在代码库中定位信息的基础。
- **代码作为自我验证**：能跑通的代码是逻辑自洽的证明，执行结果提供客观对错标准。
- **RPA 固化**：Computer Use 成功的操作序列可固化为可复用的 RPA 代码。

## Key Concepts

- **Coding Agent**：能自主编写、修改、执行代码的 Agent。
- **Code Interpreter**：带沙箱的代码执行环境。
- **Sandbox**：与主系统隔离的安全运行空间。
- **Bash / Shell**：命令行终端工具。
- **Read / Write / Edit File**：文件读写与编辑工具。
- **Glob / Grep**：文件与内容搜索工具。
- **Sessionless**：状态持久化在文件系统，不依赖长对话 session。
- **RPA（Robotic Process Automation）**：机器人流程自动化，把操作序列固化为可复用代码。
- **OOXML**：Office Open XML，Word/PPT 等文档的底层格式。
- **Self-bootstrapping**：Agent 写代码扩展自身能力。
- **Test-driven Loop**：测试失败 → 诊断 → 修复 → 再测试。

## Mental Models

- **Code is the universal glue**：代码能把思考、规则、数据、界面、工具统一起来。
- **Think in code when precision matters**：自然语言有歧义，代码没有。
- **Execution is the ultimate test**：能跑通且结果正确，就是最有力的验证。
- **File system is the Agent's workspace**：代码、数据、记忆、中间产物都应在文件系统中有序组织。
- **Sandbox is non-negotiable**：执行不可信代码必须隔离。
- **Seven tools cover most coding tasks**：不要过度设计工具箱，基础工具组合足够强大。

## Anti-patterns

- **无沙箱执行代码**：直接让 Agent 在宿主机运行任意代码。
- **没有版本控制**：Agent 修改代码后无法回滚或审计。
- **没有测试验证**：不运行测试就声称修复完成。
- **过度依赖一次性重写**：应该优先局部编辑，保留上下文和评论。
- **把 Coding Agent 限制为“写代码”**：代码是通用问题解决的元能力，不应只用于软件开发。
- **忽视人类确认**：在破坏性操作前不请求用户确认。
- **文件系统混乱**：没有固定工作空间，临时文件散落各处。

## Code Examples

```python
# Agent 用七个核心工具完成“整理所有 TODO 注释”任务
Agent(think): 需要找到所有包含 TODO 的代码行
Agent → Grep("TODO", glob="**/*.py")
# 返回：
# src/api.py:42: # TODO: add rate limiting
# src/db.py:15: # TODO: migrate to PostgreSQL
# tests/test_api.py:8: # TODO: add edge case tests

Agent(think): 找到3个TODO，整理成清单写入文件
Agent → Write("TODO_LIST.md", content="...")
# 返回：文件已创建

Agent: 已整理完毕，共发现 3 个 TODO 项，清单保存在 TODO_LIST.md。
```
- **What it demonstrates**：七个基础工具（Grep + Write）即可组合完成复杂仓库级任务，无需为每个任务设计专用工具。

## Worked Example

**场景：修复一个 bug 的 Coding Agent 工作流**

1. **理解需求**：用户说“登录接口在密码错误时返回 500 而不是 401”
2. **定位代码**：`Grep("500", glob="src/**/*.py")` + `Grep("login", glob="src/**/*.py")` → 找到 `src/auth.py`
3. **阅读上下文**：`Read("src/auth.py")` → 理解登录逻辑和异常处理
4. **编辑修复**：`Edit("src/auth.py", old="...", new="...")` → 把密码错误改为返回 401
5. **运行测试**：`Bash("pytest tests/test_auth.py")`
6. **测试失败**：发现测试期望 500，需要同步更新测试
7. **更新测试**：`Edit("tests/test_auth.py", ...)`
8. **重新测试**：`Bash("pytest tests/test_auth.py")` → 通过
9. **汇报结果**：总结修改的文件和原因

这个流程体现了 Coding Agent 的核心：用代码作为思考、执行、验证的统一语言。

## Key Takeaways

1. **Coding 是通用 Agent 的元能力**：不是少数 Agent 的专利，而是所有通用 Agent 的基础设施。
2. **七个基础工具足够构建 Coding Agent**：Code Interpreter、Bash、Read、Write、Edit、Glob、Grep。
3. **代码让思考精确、可执行、可验证**：形式化表达消除歧义，执行结果提供客观反馈。
4. **文件系统是通用 Agent 的工作空间**：Sessionless 设计让 Agent 状态可持久、可审计、可协作。
5. **安全是 Coding Agent 的底线**：沙箱、权限、版本控制、测试缺一不可。
6. **代码能动态创造新能力**：Agent 自举、RPA 固化、生成式 UI 都是代码元能力的延伸。
7. **Coding Agent 不是只写代码，而是解决一切可形式化问题**：数学、文档、数据、UI、自动化。

## Connects To

- **Ch 1 AI Agent 入门**：Coding Agent 是 Agent 三元公式在代码场景的具体实践。
- **Ch 2 上下文工程**：代码上下文、流程规范、环境信息是 Coding Agent 的关键上下文。
- **Ch 4 工具**：七个核心工具是通用工具设计的典范。
- **Ch 6 Agent 的评估**：如何通过评估数据集和指标衡量 Coding Agent 能力。
- **Ch 8 Agent 的持续进化**：Computer Use 操作序列如何固化为 RPA 代码。
- **Ch 9 多模态与实时交互**：代码驱动的 GUI 操作和多媒体生成。
