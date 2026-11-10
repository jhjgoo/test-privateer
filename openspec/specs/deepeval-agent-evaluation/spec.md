# deepeval-agent-evaluation Specification

## Purpose
规定项目明确采用 DeepEval 时，如何将框架实施交给 Confident AI 官方 Skills，并由 Test Privateer 约束证据、Oracle、授权和结论质量。

## Requirements

### Requirement: Activate DeepEval only for an explicit framework choice

DeepEval 专项 SHALL 只在项目配置、当前权威项目来源或用户明确指令选择 DeepEval 时启用。仅因任务涉及 Agent、Judge、轨迹或评测，Agent MUST NOT 推断项目采用 DeepEval。

项目选择其他或自有 Agent 评测框架时，Agent SHALL 使用通用 `agent-eval` 和项目自身入口。项目尚未决定框架且选择会改变测试资产或运行方式时，Agent SHALL 交回项目 Setup 确认，不得擅自安装或替换框架。

#### Scenario: Project selects DeepEval

- **WHEN** 项目配置明确记录 Agent 评测框架为 DeepEval，且用户要求建立或运行 Agent 评测
- **THEN** 主入口 SHALL 加载 DeepEval 质量约束，并继续遵守通用 `agent-eval` 的质量主张和证据边界

#### Scenario: Project uses another framework

- **WHEN** 项目配置指定自有 Agent 评测框架
- **THEN** Agent SHALL 沿用该框架，不加载 DeepEval 专项，也不建议为复用 Skill 而迁移框架

### Requirement: Delegate DeepEval implementation to official skills

DeepEval 的数据集、测试资产、tracing、指标、命令和迭代实现 SHALL 交给 Confident AI 官方 `deepeval` Skill。需要 DeepEval tracing 时 SHALL 使用官方 `deepeval-tracing` Skill；需要原始 OpenTelemetry／OTLP 接入时 SHALL 使用官方 `deepeval-otel` Skill。

Test Privateer MUST NOT 复制官方 Skill 的 API 映射、模板或运行教程。官方 Skill 不可用时，Agent SHALL 说明缺失对象、官方来源、安装范围和安装后复检动作，并询问用户是否安装。用户尚未决定且尚未运行评测时，当前宿主所需官方 Skill 的就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题；等待选择不是一次评测结果，MUST NOT 同时把这一待确认状态写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后，Agent 才 SHALL 使用宿主已有的 Skill 安装能力；安装位置和作用域 SHALL 由宿主安装能力与用户选择决定。没有宿主安装入口时，Agent MUST NOT 自行创建项目内 Skill 目录、克隆、下载或复制官方 Skill。该确认 MUST NOT 扩大为安装项目依赖、修改锁文件、登录、上传、调用外部 Judge 或产生费用的授权。

用户拒绝、宿主不支持安装或安装后仍不可读而无法继续框架实施时，Agent SHALL 返回 `environment_error: missing_official_skill` 和恢复条件；不得凭记忆补写实现、静默安装或用本地替代教程继续。这一能力受阻分类 MUST NOT 被表述为已实际运行评测的失败结果，也不得写入项目配置的长期状态。用户尚未确认时 SHALL 继续保持 awaiting_install_confirmation，不与拒绝混同。Agent 仍可完成框架无关的质量主张、场景和确定性 Oracle。

#### Scenario: Official DeepEval skill is available

- **WHEN** 项目已选择 DeepEval，宿主可以读取官方 `deepeval` Skill
- **THEN** Agent SHALL 将具体框架实施交给官方 Skill，并由 Test Privateer 检查实施前后的质量门槛

#### Scenario: Official DeepEval skill is missing and installation is undecided

- **WHEN** 项目已选择 DeepEval，但宿主没有官方 `deepeval` Skill，且用户尚未决定是否安装
- **THEN** Agent SHALL 标为 `awaiting_install_confirmation`，说明官方来源、安装对象和影响，只询问用户是否安装，在明确确认前不得安装或自行选择项目内安装位置

#### Scenario: Official DeepEval skill installation is confirmed

- **WHEN** 用户明确同意安装已说明的官方 DeepEval Skill
- **THEN** Agent SHALL 使用宿主已有安装能力按用户选择的作用域安装并复检，只在实际可读后进入官方实施

#### Scenario: Official DeepEval skill is missing

- **WHEN** 用户拒绝安装、宿主不支持安装或安装后仍不可读
- **THEN** Agent SHALL 标记 `missing_official_skill`，继续框架无关的质量设计，不自造 DeepEval API、模板、命令或项目内 Skill 副本

#### Scenario: No reply has arrived to the installation question

- **WHEN** 安装确认已提出，用户尚未答复，且没有实际执行评测
- **THEN** Agent SHALL 保持当前宿主官方 Skill 的 awaiting_install_confirmation，不安装、不判为拒绝，不同时报告本轮环境失败或把该值写成项目配置状态

### Requirement: Pass a quality contract into the official workflow

调用官方 Skill 前，Agent SHALL 固定被测系统、自然任务、质量主张、目标失败与邻近正常场景、确定性 Oracle、原始证据位置和授权边界。

原始证据 SHALL 包括适用的完整输出、实际 Skill／文件加载、工具调用与结果、文件变化、运行配置和环境状态。模型自述、摘要轨迹或人工补写计划 MUST NOT 被升级为实际动作证据。

#### Scenario: Official workflow starts implementation

- **WHEN** 官方 Skill 准备建立或修改 DeepEval 资产
- **THEN** 它 SHALL 已收到质量主张、场景、确定性 Oracle、原始证据位置和网络／费用／上传边界

#### Scenario: Candidate claims a skill was loaded

- **WHEN** 最终回答声称读取了某个 Skill，但原始事件没有相应访问记录
- **THEN** 质量检查 SHALL 将该加载状态保留为未确认，不让框架结果把自述升级为真实证据

### Requirement: Apply Test Privateer quality gates after official implementation

官方 Skill 完成后，Test Privateer SHALL 检查：

- 测试、数据集、配置和运行入口是否位于项目约定位置并可独立复跑；
- 派生用例、trace 和报告是否保留原始记录指针；
- 已知错误是否能够失败，邻近正常路径是否不会被误拒；
- 业务状态、权限、安全、文件差异和工具结果等确定性 Oracle 是否优先；
- 登录、上传、外部 Judge、费用、安装、升级和产品修改是否在授权内；
- 未运行项、指标冲突和有限样本边界是否保留。

确定性失败 MUST NOT 被 Judge 或指标通过覆盖。结果 SHALL 分别保留 `pass`、`agent_failure`、`environment_error` 和 `invalid_case`，不得生成掩盖关键失败的平均总分。

#### Scenario: Deterministic result conflicts with a judge score

- **WHEN** 实际工具退出失败或业务状态未达成，但 Judge 或任务完成指标给出通过
- **THEN** 顶层结果 SHALL 保留确定性失败和指标冲突，不得判为完整通过

#### Scenario: Private traces have no upload authorization

- **WHEN** 评测包含私有 Prompt、工具参数或文件路径，且没有托管上传授权
- **THEN** Agent SHALL 采用本地、最小披露的运行与证据保存，不登录或上传

#### Scenario: Judge model is unavailable

- **WHEN** 需要 Judge 的指标因模型、凭据、费用或网络不可用而未运行
- **THEN** 结果 SHALL 标记环境受阻并保留已完成检查，不把未运行项计为通过或 Agent 失败

### Requirement: Preserve a bounded correction loop

质量门槛失败时，Agent SHALL 保留官方 Skill 的原始产物、首次失败和运行输出，定位失败属于 Agent、官方框架、环境、案例或质量检查中的哪一层。修正 SHALL 只针对已证实的最小对象，并只重跑受影响场景。

Agent MUST NOT 为取得分数而放宽确定性 Oracle、删除失败记录、补写不存在的轨迹或把框架错误改写为产品通过。

#### Scenario: One evaluation asset is wrong

- **WHEN** 失败证据表明问题只在一个数据集样本、指标配置或测试资产
- **THEN** Agent SHALL 修正该资产并重跑受影响场景，保留首次失败和修正证据
