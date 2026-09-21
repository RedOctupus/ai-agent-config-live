# anchoring-persona-memory

给可挂钩、且模型带 thinking 的 Agent 用：先和使用者摆立体角色，再分层记喜好，可见回复按角色口吻渲染。不假设有角色卡。

## 产出是什么

用完这个技能，得到的是 **两样东西**，不是一个已部署的 HTTP API：

1. **记忆包**（默认 `./persona-memory/`）：人设、喜好、口吻范例、可选设定。这是渲染时用的参数，不是聊天记录全文。
2. **渲染合同**（见 `references/render-contract.md`）：宿主每轮要走的函数形状。

```text
maybe_remember(用户这句话)     → 只有命中「记住」闭集才静默追加喜好
配方注入 thinking 通道         → 内心戏仍是模型自带 reasoning（不二次代写）
模型产出 { inner, draft }
spoken = speak(draft, 记忆包, facts, inner)
使用者只看到 spoken
```

`speak` 的输入是模型可见草稿（一段话），输出是改过口吻、带上喜好摘要、织进检索事实、且不泄漏导演词的一段话。你可以在自建框架里把它包成 API（`POST /render` 之类），但本技能只定义合同和文件，不生成服务。

## 怎么影响输出

| 阶段 | 对 LLM / Agent 的影响 |
|---|---|
| 生成前 | 把薄参数（身份、纪律、喜好摘要、一条范例、短提醒）和路径内心戏配方喂进本轮；配方进 reasoning，不进可见稿 |
| 生成中 | 模型自己写 thinking；可见草稿仍可能出戏或带客服腔 |
| 生成后 | 宿主必须调用 `speak`，把草稿渲成角色说话；tool JSON、thinking 原文不渲染 |

没有「调用即渲染」的现成服务。少了输出拦截或 thinking 通道，技能会停，而不是降级成普通聊天。

## 安装

把本目录整夹拷到 Cursor 个人技能目录，文件夹名保持 `anchoring-persona-memory`：

- Windows: `%USERPROFILE%\.cursor\skills\anchoring-persona-memory\`
- macOS / Linux: `~/.cursor/skills/anchoring-persona-memory/`

或在自己的仓库里放一份 `skills/anchoring-persona-memory/`。

## 宿主

必须同时满足：

1. 能在使用者看见之前拦截模型的可见输出
2. 模型有 thinking / reasoning 通道

缺一就换框架或换模型。不要用二次生成「内心戏」或静默路由凑数。

## 使用

Agent 读到本技能后会先问宿主门，再让使用者显式选：

- A 私人扮演
- B 个人助手
- C 对客品牌

记忆默认写在当前项目的 `./persona-memory/`，不写进本技能包。口吻、闭集、路径文件都可以自己改。

## 不要读

`references/map-to-ccv2.md` 只有明确要对接 SillyTavern / 叙境时才打开。
