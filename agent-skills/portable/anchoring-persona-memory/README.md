# anchoring-persona-memory

给可挂钩、且模型带 thinking 的 Agent 用：先和使用者摆立体角色，再分层记喜好，可见回复按角色口吻渲染。不假设有角色卡。

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
