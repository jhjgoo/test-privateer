# Spec Delta

## MODIFIED Requirements

### Requirement: Delegate DeepEval implementation to official skills

DeepEval 的数据集、测试资产、tracing、指标、命令和迭代实现 SHALL 交给 Confident AI 官方 `deepeval` Skill。需要 DeepEval tracing 时 SHALL 使用官方 `deepeval-tracing` Skill；需要原始 OpenTelemetry／OTLP 接入时 SHALL 使用官方 `deepeval-otel` Skill。

Test Privateer MUST NOT 复制官方 Skill 的 API 映射、模板或运行教程。官方 Skill 不可用时，Agent SHALL 说明缺失对象、官方来源、安装范围和安装后复检动作，并询问用户是否安装。用户尚未决定且尚未运行评测时，顶层就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题；等待选择不是一次评测结果，MUST NOT 同时把本轮顶层状态写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后，Agent 才 SHALL 使用宿主已有的 Skill 安装能力；安装位置和作用域 SHALL 由宿主安装能力与用户选择决定。没有宿主安装入口时，Agent MUST NOT 自行创建项目内 Skill 目录、克隆、下载或复制官方 Skill。该确认 MUST NOT 扩大为安装项目依赖、修改锁文件、登录、上传、调用外部 Judge 或产生费用的授权。

用户拒绝、未确认、宿主不支持安装或安装后仍不可读时，Agent SHALL 返回 `environment_error: missing_official_skill` 和恢复条件；不得凭记忆补写实现、静默安装或用本地替代教程继续。Agent 仍可完成框架无关的质量主张、场景和确定性 Oracle。

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
