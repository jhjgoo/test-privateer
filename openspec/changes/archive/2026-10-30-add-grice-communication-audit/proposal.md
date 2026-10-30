# Proposal

## Why

现有 Skill 已要求任务目标、证据、路由和执行边界清楚，但缺少一个轻量、跨入口的沟通质量审查框架，导致“信息不足／过量、无证据断言、偏离目标、表达不可执行”等问题容易分散在不同规则中。将格赖斯四项准则转译为可观察的行为维度，可以帮助模型在不增加固定模板和无关篇幅的情况下，稳定检查任务契约、Prompt 和 Agent 轨迹是否真正支持下一步工作。

## What Changes

- 为 `shaping-ai-tasks` 增加数量、质量、关系、方式四维的轻量自校，并要求保留完成任务所需信息，不把简洁等同于越短越好。
- 为 Prompt 与 Agent 评估增加四类失败标签，分别检查信息充分性、证据匹配、目标／路由相关性和可执行／可核验性。
- 要求评测报告分别呈现四维观察、实际轨迹和最终结果，不将四维合并为单一总分。
- 增加成对行为评测样本和静态契约检查，覆盖信息刚好足够、关键条件缺失、诱人无关背景、证据冲突、工具失败、提示注入和歧义交付。
- 不新增全局人格提示词，不改变明确请求的直达路由，不把模型自述或文字风格替代真实工具与文件证据。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `shaping-ai-tasks`: 任务升级增加四维沟通质量自校，并保持最小充分、事实证据、目标相关和可验证交接。
- `solution-agent-quality`: Prompt 与完整 Agent 评估增加四维失败分类、轨迹观察和不合并总分的报告约束。

## Impact

影响 `skills/shaping-ai-tasks/SKILL.md`、`skills/prompt-eval/SKILL.md`、`skills/agent-eval/SKILL.md`，以及 `tests/test_eval_skills_contract.py` 和相关 `evals/` 可复用场景。无需新增依赖、工具权限或安装格式；现有主入口和专项路由保持不变。
