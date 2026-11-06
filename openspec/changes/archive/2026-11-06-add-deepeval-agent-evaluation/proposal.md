# Proposal

## Why

`agent-eval` 已定义 Agent 质量主张、场景、Oracle、真实加载轨迹和失败分类。Confident AI 官方仓库已经提供完整的 `deepeval`、`deepeval-tracing` 和 `deepeval-otel` Skills；本项目若再维护 API 映射、模板和运行步骤，会形成较浅且容易漂移的重复实现。Test Privateer 只需补齐框架选择、证据、授权、Oracle 优先级和失败分类等质量门槛。

## What Changes

- 新增 `evaluating-agents-with-deepeval` 质量约束层，仅在项目配置、权威项目来源或用户明确指令选择 DeepEval 时启用。
- 将 DeepEval 的数据集、tracing、指标、测试资产、运行和迭代实现交给 Confident AI 官方 Skills，不在本包复制其 API、模板和教程。
- 在调用官方 Skill 前交接质量主张、自然场景、确定性 Oracle、原始证据位置和授权边界；调用后检查资产可复跑、证据保真和结论边界。
- 让确定性业务／权限／状态判据优先于 LLM Judge；指标冲突、Judge 错误、环境错误和无效案例分别保留，不合并为单一总分。
- 默认采用本地、最小披露的运行方式；上传轨迹、登录托管平台或调用外部 Judge 必须符合项目配置和当前授权。
- 官方 Skill 缺失时标记 `missing_official_skill`，保留通用 `agent-eval` 工作，不凭记忆补写 DeepEval 实现。
- 增加官方 Skill 交接、框架触发、证据保真、已知正反例校准、隐私边界和失败降级的契约测试与真实模型行为评测。

## Capabilities

### New Capabilities

- `deepeval-agent-evaluation`: 定义项目选择 DeepEval 后，如何把实现交给官方 Skills，并用 Test Privateer 的质量门槛约束和验收结果。

### Modified Capabilities

- `testing-workflow`: 增加 DeepEval 专项的条件路由，确保未选择 DeepEval 的项目继续使用通用 Agent 评测或项目自有框架。

## Impact

- 新增 `evaluating-agents-with-deepeval` 质量约束 Skill、契约测试和行为评测材料；不新增本地 DeepEval API 参考或模板。
- 更新 `test-privateer` 与 `agent-eval` 的最小路由／handoff，使 DeepEval 专项可达但不成为默认路径。
- 本 change 依赖 `add-test-privateer-project-setup` 提供项目框架选择；实施顺序位于该 change 之后。用户显式调用 DeepEval 专项时，该调用本身可作为本轮框架选择。
- 官方 DeepEval Skills 和 Python 包保持使用方项目的可选依赖，本仓库只保存来源引用，不复制或内置。
- 本 change 不替代现有 `.local/validation/` 原始记录协议，不建设托管评测平台，不配置模型或凭据，也不改变非 DeepEval 项目的测试框架。
