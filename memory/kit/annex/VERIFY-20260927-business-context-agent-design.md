# 验证记录：业务上下文优先 Agent 设计 Skill 与 Kit 接入

- 日期：2026-09-27
- 关联需求：R9、R10、R11
- 风险等级：MEDIUM

## 改了什么

- 新增 `business-context-first-agent-design`，同步到 `portable`、`claude`、`cursor`。
- project-memory-kit 升级到 v1.4.0。
- 新增可选 `templates/BUSINESS-CONTEXT.md`，并在 Kit 的 SKILL、AGENTS、Cursor 规则、README 中加入路由说明。
- 本仓 `memory/kit/` 增加对应的业务上下文、需求、流程、框架和迭代记录。
- 新 Skill 使用 L0–L3 分级、Kit-aware / standalone 两种落点，以及 GREEN / YELLOW / RED 门闸。

## 已执行

| 类型 | 命令或步骤 | 结果 |
|---|---|---|
| RED 基线 | `materials/_local/business-context-skill-sandbox/run_baseline.py` | PASS：6 个 DeepSeek 场景均完成；无 Skill 时角色/Agent/UI 请求直接进入实现设计 |
| RED 评分 | `score_baseline.py` | PASS：基线普遍缺少业务域、生命周期、角色任务或视图定位 |
| GREEN 复测 | `run_guided.py`（同一 6 场景 + 新 Skill） | PASS：L2/L3 场景先进入业务上下文门闸；L0 小修复保持局部范围 |
| 提示词优化 | 加入 `Response discipline` 后再次运行 `run_guided.py` | PASS：关键场景保持短响应；本次复跑 role-agent-first 3473→1201 字符，memory-first 2089→977 字符（模型输出有自然波动） |
| 结构检查 | `test_artifacts.py` | PASS：三份 Skill、两份 Kit、模板、路由、版本和清单一致 |
| 记忆体量 | `python scaffold/scripts/check-memory-size.py` | PASS：体量门闸通过 |
| Git 检查 | `git diff --check` | PASS，无 whitespace error（Windows 仅提示换行风格转换） |

## 结果判断

- 业务上下文门闸有效：模型不再直接接受“给主管做一个 Agent”并输出接口/工具清单，而是先判定 RED/L2 并询问最小解锁问题。
- 任务分级有效：明确的日期显示 bug 被判为 L0，不要求重新建模完整业务域。
- Kit 联动清晰：Kit 负责路由和存储契约，设计 Skill 负责分析流程；没有复制平行 `agent-design/` 记忆树。
- DeepEval 未使用：本轮已有可复现的模型调用、固定压力场景和结构化评分；引入 DeepEval 不会增加当前结论的可信度，反而会增加依赖和运行成本。

## 提示词优化结论

- 保留：L0–L3、Kit-aware / standalone、GREEN/YELLOW/RED、角色/工具反模式、上下文类别和人工边界。
- 新增并保留：首次响应纪律；RED 最多五个解锁问题；YELLOW 只给受控原型；L0 不问无关业务域问题；不重复打印整套 Skill。
- 当前剩余风险：不同宿主对 Skill description 和项目常驻规则的优先级不同，因此 Kit 路由和 Skill 自发现仍采用双重触发。
- 复跑结果：六个基线场景与六个引导场景均完成；引导评分为 9/9、9/9、9/9、9/9、8/9、6/9。后两项是通用关键词评分未覆盖全部语义，不代表行为失败；人工复核确认记忆场景仍先阻塞，L0 场景未启动完整建模。

## 未执行

- 未安装或注册本机 Skill；本仓只完成备份和可复用文档。
- 未运行完整应用测试；本仓没有应用运行时。
- 已推送到远程 `origin/main`；最终设计提交为 `6e15230`。
