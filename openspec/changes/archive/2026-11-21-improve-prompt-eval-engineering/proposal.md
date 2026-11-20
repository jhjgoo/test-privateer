# Proposal: Improve prompt-eval engineering

## Why

`prompt-eval` 已覆盖模型适配、证据边界和前后对照，但对企业 Prompt 的消息层级、最小充分上下文、结构化输出分工、缓存与版本可观测性检查还不够明确。NVIDIA SkillEvaluator 强调可观察行为与固定条件比较，附件指南强调 Prompt 是接口契约而不是长文本；两者可以合成少量可判定的审查维度。

## What Changes

- 在 `prompt-eval` 中补消息角色与指令层级检查：区分协议角色、文本标题、动态输入和工具结果的权限。
- 补最小充分上下文审查：按稳定规则、动态任务、证据和程序观测分层，防止误删判断条件或注入无关噪声。
- 补结构化输出与验证分工：Schema 只证明格式，业务事实、引用和确定性计算需另设可观察校验。
- 补缓存与版本评估边界：缓存命中、质量、成本、延迟分开测量；Prompt／Schema／规则版本可追踪、可回归、可回滚。
- 明确调整前／后同条件配对、执行与评审两侧盲化、评分后揭盲及指标／错误分报。
- 客户可选 SkillEvaluator 量化 Skill 或语义可忠实保留的指令包；普通 Prompt 沿用原宿主，不强制包装、安装或继承维护配置。
- 保持 30 个 Skill 的包结构和主路由不变，仅优化 `prompt-eval` 及其参考。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `solution-agent-quality`: Prompt 评估须覆盖消息层级、上下文充分性、程序分工、运行证据、盲测配对与可选框架接入。
- `repository-workflow`: 区分仓库维护验证配置与客户主动选择的外部框架引用。

## Impact

- `skills/prompt-eval/SKILL.md`
- `skills/prompt-eval/references/prompt-review-patterns.md`
- `tests/test_eval_skills_contract.py`
- `evals/skillevaluator/prompt-eval/`
- `AGENTS.md`、`openspec/project.md` 与项目验证协议：消解“仅维护工具”与新增可选引用的范围冲突。
