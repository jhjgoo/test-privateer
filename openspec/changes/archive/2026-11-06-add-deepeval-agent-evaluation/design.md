# Design

## Context

`agent-eval` 维护框架无关的质量主张、自然场景、Oracle、真实加载轨迹和四类结果状态。Confident AI 官方仓库已经提供完整的 `deepeval`、`deepeval-tracing` 和 `deepeval-otel` Skills，并随官方实现维护数据集、tracing、测试资产、指标、命令和迭代方法。

早期实现仍在 Test Privateer 内维护 DeepEval API 映射参考，真实模型评测也只验证文字判断，没有证明能建立和运行完整项目资产。这既重复官方能力，也会随版本漂移。纠偏后，本 change 只维护官方 Skill 的条件路由和 Test Privateer 的质量约束。

## Goals / Non-Goals

**Goals:**

- 只在项目或用户已经选择 DeepEval 时调用官方 Skill。
- 在调用前交接质量主张、场景、确定性 Oracle、原始证据和授权边界。
- 在调用后检查资产可复跑、证据保真、Oracle 优先级、隐私和失败分类。
- 官方 Skill 缺失时明确受阻，继续框架无关工作，不自造 DeepEval 实现。

**Non-Goals:**

- 不复制或改写官方 DeepEval Skill、references、templates 和 API 教程。
- 不把 DeepEval 设为默认 Agent 评测框架。
- 不把官方 Skills 或 DeepEval Python 包内置为本仓库强制依赖。
- 不让 Judge 或聚合分数替代确定性业务、权限和状态证据。

## Decisions

### 1. 官方 Skills 是唯一 DeepEval 实现入口

项目选择 DeepEval 后：

- `deepeval` 负责数据集、测试资产、指标、运行和迭代；
- `deepeval-tracing` 负责 DeepEval tracing；
- `deepeval-otel` 负责原始 OpenTelemetry／OTLP 接入。

Test Privateer 通过稳定 GitHub 来源引用这些 Skills，不复制其正文。宿主已安装时读取安装版本；未安装时返回 `environment_error: missing_official_skill` 和恢复条件。除非用户另行授权，不自动安装。

### 2. `evaluating-agents-with-deepeval` 是质量约束层

该 Skill 不描述 DeepEval 类名、参数、目录模板或运行命令，只做两次交接：

1. 实施前，把 `agent-eval` 的质量主张、自然场景、确定性 Oracle、原始证据位置和授权边界交给官方 Skill。
2. 实施后，检查官方 Skill 留下的项目资产和运行证据是否满足 Test Privateer 的质量门槛。

这样能让官方实现随上游演进，同时保留本项目在测试证据和质量判定上的差异化职责。

### 3. 质量门槛不因框架改变

验收继续检查：

- DeepEval 是否由项目或用户明确选择；
- 测试、数据集、配置和运行入口是否可复跑；
- 派生 trace 和报告是否保留原始宿主证据指针；
- 模型自述是否被错误升级为真实加载或动作；
- 确定性业务、权限、安全、文件和工具结果是否优先；
- 登录、上传、外部 Judge、费用、安装和产品修改是否获得授权；
- `pass`、`agent_failure`、`environment_error`、`invalid_case` 是否分开；
- 未运行项、冲突和有限样本边界是否保留。

不生成平均发布总分，不以单项指标通过扩大为完整 Agent 通过。

### 4. 行为评测验证协作，不再验证自建实现

纠偏后的真实模型行为评测至少覆盖：

- 官方 Skill 可用时，实际加载官方 `deepeval` 并由其承担实施；
- 需要 tracing 时，正确转交官方 `deepeval-tracing`；
- 官方 Skill 缺失时，返回 `missing_official_skill`，不凭记忆补写；
- 项目使用自有框架时，不加载 DeepEval 专项；
- 确定性失败与 Judge 通过冲突时，保留失败；
- 私有轨迹未授权时，不登录、不上传、不调用外部 Judge。

判读仍核对完整输出、实际 Skill 加载、工具轨迹、文件差异和运行结果，不能只看模型自述。

## Risks / Trade-offs

- [宿主没有安装官方 Skills] → 明确受阻和官方来源；通用 `agent-eval` 仍可继续。
- [官方 Skill 更新改变行为] → 记录实际来源版本或提交；质量门槛保持稳定。
- [官方流程与项目约定冲突] → 项目权威来源和当前授权优先，冲突动作停止。
- [质量约束再次膨胀成实现教程] → 契约测试禁止本地指标类、命令和映射参考。

## Migration Plan

1. 删除本地 `references/deepeval-mapping.md`。
2. 将专项改为官方 Skill 引用和质量门槛。
3. 更新 OpenSpec、用户文档和行为评测判据。
4. 按新协作边界复跑真实模型行为评测。
5. 保留活动 change，等待用户确认后再同步规格、归档和同步本地 Skill。

回滚时恢复上一版专项和映射参考；通用 `agent-eval` 与项目配置不受影响。

## Implementation Evidence

- 2026-11-06 核对 Confident AI 官方仓库，确认存在 `skills/deepeval`、`skills/deepeval-tracing` 和 `skills/deepeval-otel`。
- 契约测试先失败于本地专项没有引用官方 Skills；生产 Skill 改为官方实现依赖并删除本地 API 映射后通过。
- 使用官方提交 `696248fd7f8b4db1aa0d4f05cee22c3d2cc5857b`、Codex CLI 0.166.0、`gpt-6.1-sol`、high reasoning 和只读隔离目录复跑六个协作场景。官方实现、tracing 分流、Skill 缺失、自有框架绕过、确定性冲突和私有记录边界均通过；实际加载轨迹分别证明了官方 Skill 的读取或绕过。
- 早期七个文字场景和 DeepEval 4.3.3 API 冒烟记录保留为历史证据，但不再被解释为完整 DeepEval 项目实施能力。
