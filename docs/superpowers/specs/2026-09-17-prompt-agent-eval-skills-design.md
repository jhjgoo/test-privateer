# Prompt Eval 与 Agent Eval Skill 设计

## 目标

为 Test Privateer 增加两项独立质检能力：`prompt-eval` 评估 Prompt 在指定模型、宿主和任务中的适配性；`agent-eval` 评估完整 Agent 系统的任务质量、策略合规、证据、稳定性与评估可信度。

两项能力用于辅助、纠偏和质检。它们不建设评测平台，不默认生成评测代码，不用排行榜或单次 Judge 分数代替产品质量判断。

## 边界

### prompt-eval

适用于 System Prompt、Skill、工具描述、Agent 指令和请求模板的审查、失败诊断、前后对照及模型／宿主变化后的重新适配。

它读取实际进入模型的完整 Prompt 表面，明确目标模型与目标行为，追溯规则来源，识别冲突、错误位置、重复加权、过度约束、示例过拟合和缺失完成条件。候选修改必须对应真实失败或目标模型证据，并使用失败场景、邻近正常场景和边界场景验证。

它内化 `skill-eval` 的有效审计方法，但不把模型迁移作为独立流程。目标模型变化时，重新执行同一套当前适配评估。无法运行时交付候选差异与验证设计，不宣称改进成立。

### agent-eval

适用于 Agent 测试设计、现有评估审查、版本比较和失败诊断。被测对象包含模型、Prompt、工具、权限、记忆、编排和环境。

它围绕具体质量主张工作，先固定系统版本和边界，再按风险选择任务结果、业务规则、权限安全、证据可信、工具行为、对话协作、恢复能力、稳定性和资源效率。场景来自真实失败、高频或高后果任务，每个失败场景配邻近正常场景。

Oracle 优先使用环境状态、可执行测试、结构规则和关键轨迹；人工或校准后的 Judge 只补充开放语义。执行证据分为 `pass`、`agent_failure`、`environment_error`、`invalid_case`。Agent、环境、工具和评分器问题分别归因。

它不选择或搭建 LangSmith、Langfuse、OpenAI Evals 等平台。已有结果可读取；没有执行能力时输出工具无关的测试设计。实际执行由 `running-test-sessions` 承接，异常调查交给 `investigating-findings`，证据强度交给 `assessing-test-confidence`。定位为 Prompt 问题时，将失败场景、目标行为、直接证据和邻近场景交给 `prompt-eval`。

## 信息层级

```text
skills/prompt-eval/
├── SKILL.md
└── references/prompt-review-patterns.md

skills/agent-eval/
├── SKILL.md
└── references/
    ├── agent-quality-model.md
    └── evaluator-checks.md
```

每次都需要的目标、步骤、边界和完成条件留在 `SKILL.md`。Prompt 审查模式、Agent 质量维度及评估器／统计检查按需读取。

## 路由

`test-privateer` 增加两个入口：

- Prompt、Skill、工具描述或 Agent 指令需要审查、比较、失败诊断或模型适配时，使用 `prompt-eval`。
- Agent 整体质量、轨迹、稳定性、评估方案或版本比较需要审查时，使用 `agent-eval`。

README 和研发教程加入直接调用示例。Skill 总数由 20 调整为 22。

## 验收

静态检查验证 frontmatter、目录、引用与主入口路由。行为样例至少覆盖：

- Prompt 真实失败应提出最小修正和邻近场景；只有一份 Prompt、目标模型未知时不声称完成适配。
- Agent 评估审查能识别单次运行、环境失败混入、只看最终文案和未校准 Judge；不擅自搭建平台。
- Agent 失败被定位到 Prompt 时，交接内容足以进入 `prompt-eval`。
- 普通产品测试分析不会误路由到两个新 Skill。

完成后按 `skill-eval` 审查 GPT-6 Astra 目标提示面；没有目标模型证据支持的改动不写入运行时 Skill。
