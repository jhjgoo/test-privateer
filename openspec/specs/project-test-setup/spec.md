# project-test-setup Specification

## Purpose
规定 Test Privateer 如何为一个项目建立可重复读取的测试配置，保存项目已有权威来源和必要补充，同时避免复制测试文档、秘密信息或未经验证的环境结论。

## Requirements

### Requirement: Explore project facts before asking for configuration

`setup-test-privateer` SHALL 先调查项目规则、产品与架构资料、构建和 CI、测试框架与目录、运行入口、环境与数据准备、测试资产位置、缺陷平台、质量门槛、责任角色和既有验证器。调查 SHALL 覆盖项目实际使用的单元、接口、E2E、UI、Agent 评测或其他测试表面，但不得为不存在的表面强制选择框架。Agent SHALL 区分仓库事实、用户确认、推断、未知和临时运行状态。

仓库材料已经明确的配置 SHALL 直接沿用并记录来源。只有无法从材料确定且会改变测试范围、执行安全、证据位置、质量门槛或责任归属的决定，Agent 才 SHALL 询问用户。Agent MUST NOT 编造命令、凭据、环境或负责人。

#### Scenario: Existing project rules answer the question

- **WHEN** 项目文档已经明确测试环境、测试命令和发布前检查
- **THEN** Setup SHALL 沿用并引用这些来源，不重复询问相同问题

#### Scenario: Environment choice changes execution safety

- **WHEN** 仓库存在多个环境，但无法确认哪个环境允许自动创建测试数据
- **THEN** Setup SHALL 说明发现、推荐和影响，并等待用户确认后再保存该决定

### Requirement: Confirm and write one project test profile

Setup SHALL 在写入前展示项目配置草稿，并将确认后的配置保存到目标项目的 `.test-privateer/project.md`。项目配置 SHALL 至少覆盖适用范围、权威来源、测试入口、测试框架与驱动约定、环境与安全边界、身份与数据准备、质量门槛、证据策略、缺陷平台、责任角色、测试资产位置和验证器入口。

项目配置 SHALL 优先保存来源指针和项目尚未记录的已确认补充。仓库内来源指针 SHALL 相对项目根目录书写，不得相对 `.test-privateer/project.md` 使用 `../`。已有脚本、CI 或项目文档是命令和规则的权威来源时，配置 SHALL 引用来源而不是复制易失效的快照。没有正式来源的用户确认决定可以保存在配置中，并注明确认范围。

每个已使用测试表面的框架约定 SHALL 来自当前项目权威来源或用户明确确认。没有项目约定且选择会改变实现或执行时，Setup SHALL 说明候选方案和影响并等待确认；MUST NOT 因某个框架存在专项 Skill 而自动选择、安装或替换项目框架。框架专项 Skill 只有在当前项目或用户明确选择对应框架时才适用。

#### Scenario: Project has authoritative commands

- **WHEN** 测试命令已经由项目脚本和 CI 定义
- **THEN** 项目配置 SHALL 引用相应文件和适用阶段，不复制一份可能漂移的命令清单

#### Scenario: User confirms an undocumented safety boundary

- **WHEN** 用户确认 Agent 只能在隔离测试环境创建数据，但项目没有记录该限制
- **THEN** Setup SHALL 将该限制、适用范围和确认来源写入项目配置

#### Scenario: Project already uses its own agent evaluation framework

- **WHEN** 项目依赖、配置或权威文档已经指定一个 Agent 评测框架
- **THEN** Setup SHALL 记录其来源和适用范围，后续流程 SHALL 沿用该框架，不加载其他 Agent 评测框架的专项 Skill

#### Scenario: Agent evaluation framework is undecided

- **WHEN** 项目需要建立 Agent 评测，但仓库没有框架约定，且不同选择会改变测试资产和运行方式
- **THEN** Setup SHALL 提供最少候选及影响并等待用户确认，不得仅因 DeepEval 或其他框架有现成 Skill 而自动选择

### Requirement: Keep project configuration separate from testing assets

`.test-privateer/project.md` SHALL 描述项目如何开展测试，不得替代 `testing/TCO.md`、需求测试分析、测试依据、测试用例、执行记录或测试信心报告。Setup SHALL NOT 为完成初始化自动生成这些资产，也 SHALL NOT 把一次运行结果写成长期项目配置。

测试资源、证据位置或验证器可以由项目配置指向权威资产。产品和测试空间认知继续由 TCO 维护；单需求认识继续由需求资产维护；每轮执行继续由 Run ID 和执行记录维护。

#### Scenario: Project has no TCO

- **WHEN** Setup 完成时目标项目还没有 `testing/TCO.md`
- **THEN** Setup SHALL 记录 TCO 缺口或后续入口，但不得生成空 TCO 并声称项目地图已经建立

#### Scenario: Setup observes a temporary outage

- **WHEN** 调查期间测试环境暂时不可访问
- **THEN** Setup SHALL 将其作为本次未验证状态报告，不把临时故障写成长期项目规则

### Requirement: Rerun setup idempotently and preserve human content

重复运行时，Setup SHALL 读取现有项目配置，更新已变化的受管内容，保留仍有效的确认决定和非受管人工内容，并避免追加重复章节。失效来源或退役配置 SHALL 被修正、删除或标明替代位置。

写入工具 SHALL 要求目标项目根目录已经存在，只接收受管标记之间的非空正文，并拒绝覆盖无标记旧文件、标记异常文件、符号链接配置目录或符号链接目标文件。更新已有配置时 SHALL 保留受管区外内容、原始换行和文件权限。

项目规则要求写后运行格式化器、同步器或生成器时，Setup SHALL 将该动作包含在写入与最终回读的同一事务中；MUST NOT 在写入工具返回成功后单独运行写后工具并保留变形文件。用于传递受管区内容的草稿 SHALL 使用临时文件或内存，完成后不得作为第二份配置保留在项目中。

写入、写后动作、权限恢复和回读 SHALL 作为同一事务处理。写后动作抛错、目标消失、内容或权限不一致时，Setup SHALL 恢复原文件或删除初次创建的无效配置，并清理临时草稿和原子写入文件。Setup SHALL 报告未完成部分，MUST NOT 宣称 Setup 完成。

#### Scenario: Setup reruns after a CI path change

- **WHEN** 项目的 CI 文件已经迁移，配置仍引用旧路径
- **THEN** Setup SHALL 更新来源指针，保留无关人工说明，并确保配置中只保留一个有效入口

#### Scenario: Readback differs from the draft

- **WHEN** 写入后的文件缺少已确认字段或覆盖了人工内容
- **THEN** Setup SHALL 恢复原文件或删除无效的新文件，报告配置未完成，不把写入命令成功当作完成

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
