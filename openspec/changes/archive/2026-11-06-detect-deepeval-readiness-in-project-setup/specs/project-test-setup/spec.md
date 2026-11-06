# Spec Delta

## MODIFIED Requirements

### Requirement: Separate saved configuration from verified readiness

Setup 结论 SHALL 分别说明项目配置已保存、入口已确认、框架约定已确认、当前宿主框架实施能力已就绪、环境已实际验证、测试已实际运行和质量门禁已接入的状态。只完成调查或写入时，Agent MUST NOT 宣称框架已经安装可用，或环境、测试、门禁已经可用。

项目明确选择 DeepEval 时，Setup SHALL 检查当前宿主能否读取任务所需的 Confident AI 官方 Skills，并区分官方 Skill、项目 Python 依赖和项目评测入口的就绪状态。当前宿主状态 SHALL 只作为本轮观察报告，不得写成长期项目事实。

官方 Skill 缺失时，Setup SHALL 说明缺失对象、官方来源、安装范围和安装后复检动作，并询问用户是否安装。用户尚未决定且尚未运行评测时，顶层就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题；等待选择不是一次评测结果，MUST NOT 同时把本轮顶层状态写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后，Agent 才 SHALL 使用宿主已有的 Skill 安装能力；拒绝、宿主不支持安装或安装后仍不可读时，Agent SHALL 保留 `missing_official_skill`。安装位置和作用域 SHALL 由宿主安装能力与用户选择决定；没有宿主安装入口时，Agent MUST NOT 自行创建项目内 Skill 目录、克隆、下载或复制官方 Skill。该确认 MUST NOT 被扩大为安装 Python 依赖、修改锁文件、登录、上传、调用外部 Judge、产生费用或执行产品测试的授权。

除上述已确认的官方 Skill 安装外，Setup SHALL NOT 安装或升级测试框架、安装项目依赖、启动服务、创建测试数据、修改 CI、运行产品测试或配置模型，除非用户在同一任务中另外明确授权对应动作。额外授权产生的执行证据 SHALL 进入相应测试资产，而不是被 Setup 状态吸收。

Setup MUST NOT 读取、复制或回显秘密值到配置、草稿、回复、工具摘要或评测记录。需要描述凭据时 SHALL 只记录字段名、安全入口和提供方式。

#### Scenario: Configuration is saved without running tests

- **WHEN** 项目配置已写入并回读，但没有启动环境或执行测试
- **THEN** Setup SHALL 报告配置已保存，同时明确环境和测试未验证

#### Scenario: DeepEval is selected but the official skill is missing

- **WHEN** 项目已选择 DeepEval，但当前宿主无法读取所需官方 Skill
- **THEN** Setup SHALL 标为 `awaiting_install_confirmation`，展示官方来源和安装影响并只询问是否安装，在用户明确确认前不得执行安装或自行选择项目内安装位置

#### Scenario: User confirms official skill installation

- **WHEN** 用户明确同意安装缺失的官方 DeepEval Skill
- **THEN** Agent SHALL 只通过宿主已有安装能力安装已说明的官方 Skill，随后复检；该确认不得授权项目依赖、登录、上传、费用或测试执行

#### Scenario: User declines official skill installation

- **WHEN** 用户拒绝安装或宿主不支持安装
- **THEN** Setup SHALL 保留 `missing_official_skill` 和恢复条件，不改用其他框架、不自行复制官方 Skill，也不把当前宿主状态固化到项目配置

#### Scenario: User provides a secret during setup

- **WHEN** 用户提供用于调查的真实令牌或密码
- **THEN** Setup SHALL 要求改用安全入口，不读取、复制、回显或保存秘密值
