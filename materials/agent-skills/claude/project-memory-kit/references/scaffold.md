# 工程脚手架（仅用户点名时）

默认 init **只**创建 `docs/memory/` + `AGENTS.md` + `.cursor/rules/project-memory.mdc`。
用户明确说「工程脚手架 / 生成 gitignore / README / env 示例」时才按本节做。

**不要**默认生成：RBAC、JWT、Docker、前端、许可证、完整 MVC 代码。

## MVC 分层（后端常见）

```text
允许：API/Controller → Service → Repository → Database
禁止：API 直连数据库；Repository 写业务流程
```

按语言改名，原则不变：入口薄、业务在中间、持久化单独一层。

## 可生成的骨架文件（点名再做）

**最小集（点名「工程脚手架」时必须有）：** `README.md`、`.gitignore`、`.env.example`。

**按需（用户提到依赖/语言时才加）：** `requirements.txt` 或该生态的锁文件。未点名则不要编造依赖列表。

| 文件 | 作用 |
| --- | --- |
| `README.md` | 项目是什么、如何运行 |
| `.gitignore` | 含 `.env`、`__pycache__`、`node_modules`、密钥文件 |
| `.env.example` | 配置项名，无真实密钥 |
| `requirements.txt` 或锁文件 | 依赖名与版本；仅当用户要或项目已有该生态 |

约定：禁止硬编码密钥和连库串；真实值只在 `.env`。

## 模块开发节奏（如 RBAC，须用户点名）

1. 思路（角色/权限模型）
2. 开发计划
3. 写入 `docs/memory/TODO.md`
4. 逐步开发，每步打钩并测试后再下一步

## 日志

应用日志用于跟操作路径、定位 bug；与 `docs/memory/annex/` annex 交付记录不是同一件事。
