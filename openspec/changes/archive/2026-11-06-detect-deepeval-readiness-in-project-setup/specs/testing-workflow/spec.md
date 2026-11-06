# Spec Delta

## MODIFIED Requirements

### Requirement: Route DeepEval agent evaluation only when selected

当用户明确调用 DeepEval Agent 评测，或项目配置／当前权威来源选择 DeepEval 且任务需要建立、运行、审查或修正 Agent 评测时，主入口 SHALL 路由到 `evaluating-agents-with-deepeval`。该专项 SHALL 先继承 `agent-eval` 已固定的质量主张、场景、Oracle 和证据协议，再把 DeepEval 实施交给 Confident AI 官方 Skills；不得从框架指标重新定义业务目标，也不得在本包复制官方实现教程。

没有选择 DeepEval 时，普通 Agent 测试设计、评估审查、版本比较和失败归因 SHALL 继续使用 `agent-eval` 或项目自有框架。官方 DeepEval Skill 缺失时，Agent SHALL 说明官方来源、安装对象和影响并询问用户是否安装；用户尚未决定且尚未运行评测时，顶层就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题，不得同时写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后才可使用宿主已有安装能力，安装目标由该能力和用户选择决定。拒绝、宿主不支持安装或安装后仍不可读时，SHALL 报告具体缺口并降级到仍可执行的通用评测工作，不得凭记忆补写实现、静默安装、自行复制到项目目录、登录、上传或替换项目框架。

#### Scenario: Explicit DeepEval request

- **WHEN** 用户明确要求使用 DeepEval 为当前 Agent 建立或运行评测
- **THEN** 主入口 SHALL 路由到 DeepEval 质量约束，再由其调用官方 `deepeval` Skill；该请求只代表本轮框架选择，不要求项目永久迁移

#### Scenario: Generic agent evaluation request

- **WHEN** 用户只要求设计 Agent 测试或审查现有评估，项目没有选择 DeepEval
- **THEN** 主入口 SHALL 使用通用 `agent-eval`，不加载 DeepEval 专项

#### Scenario: Official DeepEval skill is unavailable

- **WHEN** 项目选择 DeepEval，但当前宿主缺少官方 `deepeval` Skill
- **THEN** Agent SHALL 先标为 `awaiting_install_confirmation` 并询问是否安装，在明确确认前不安装或自行选择项目内安装位置；若仍不可用，则保留可完成的场景、Oracle 和原始证据工作并标记 `missing_official_skill`
