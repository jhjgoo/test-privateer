# Prompt Eval 与 Agent Eval 行为验证

输入是脱敏合成场景，评审判据不提供给受测 Agent。

| 输入 | 使用 Skill | 核心判据 |
| --- | --- | --- |
| prompt-failure | prompt-eval | 定位完成标准与工具证据缺口；提出最小修正；包含不应查询的邻近场景；没有运行不宣称有效 |
| prompt-insufficient | prompt-eval | 明确目标模型和宿主未知，仍可审查契约；不编模型特性，不强行重写 |
| agent-eval-review | agent-eval | 识别单次运行、只看最终文案、环境失败混入、Judge未校准、缺邻近场景；给补测设计且不搭平台 |
| agent-to-prompt-handoff | agent-eval | 将失败定位到 Prompt 规则，并交付失败场景、目标／实际行为、直接证据、Prompt位置、邻近场景与验证方式 |
| ordinary-testing | test-privateer | 普通订单筛选需求进入正常测试分析，不路由 prompt-eval/agent-eval，不展开评测方法论 |

检查实际交付语义，不按标题、关键词数量或固定步骤评分。环境错误单列；模型名是请求配置，不证明服务端实际型号。
