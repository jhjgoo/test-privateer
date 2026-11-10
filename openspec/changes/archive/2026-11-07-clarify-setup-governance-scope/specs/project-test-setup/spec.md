# Spec Delta

## ADDED Requirements

### Requirement: Initialize the project test map during setup

普通项目 Setup SHALL 建立或校准唯一 `testing/TCO.md`。Setup SHALL 调用项目建图专项维护产品目标与使用者、关键业务和系统链、证据索引、覆盖节点与已有保护、长期风险与未知、测试资源入口及下一步取证；MUST NOT 在 Setup 中复制第二套建图方法。初始 TCO MAY 保持草案状态，但 SHALL 包含实际项目来源和可用于后续影响判断的项目关系，未知 SHALL 记录影响、负责人类型和取证动作；空模板、空标题或仅记录“后续建立”MUST NOT 作为初始化完成。

用户明确只要预览、禁止创建 TCO 或当前没有写入权限时，Setup SHALL 遵守边界并报告 `partial: tco_not_initialized` 与恢复入口，MUST NOT 宣称项目初始化完成。用户未明确排除时，普通配置或完整 Loop 的选择 SHALL NOT 使 Setup 跳过 TCO。已有 TCO SHALL 原地校准，不得创建第二份项目地图。

#### Scenario: Ordinary setup bootstraps a missing TCO

- **WHEN** 用户要求初始化项目，项目有足够的产品、架构、接口或测试资料但没有 `testing/TCO.md`
- **THEN** Setup SHALL 通过项目建图专项建立有来源的 TCO 草案并回读，配置引用该实际文件，不把 TCO 延期到未来任务

#### Scenario: Existing TCO is recalibrated

- **WHEN** 项目已有 TCO，但来源、业务链或测试入口与当前项目资料不一致
- **THEN** Setup SHALL 原地核对和修正受影响内容，保留有效认知和证据链，不创建第二份 TCO

#### Scenario: User explicitly excludes TCO creation

- **WHEN** 用户明确要求本轮只保存配置且禁止创建项目地图
- **THEN** Setup SHALL 不创建 TCO，并将结果报告为 `partial: tco_not_initialized` 及恢复入口，不宣称 Setup 完成

### Requirement: Determine applicable test surfaces in ordinary setup

普通 Setup SHALL 按项目功能、已有测试和当前目标核对单元、接口、E2E、UI、Agent 评测等适用测试表面；适用范围不清时 SHALL 提出建议并确认，不把没有入口推断为不需要。每个适用表面的框架或项目自有入口 SHALL 分别记录来源。已有权威约定 SHALL 直接沿用；需要新增能力但没有约定，且选择会改变实现或执行时，Setup SHALL 给出最少候选、推荐和影响并等待确认。Setup MUST NOT 把已有单元框架推断为其他表面已配置，也不得因对应专项 Skill 存在而自动选择框架。用户明确暂不开展的表面 SHALL 记录决定及适用范围，不为这些表面反复询问。

#### Scenario: Missing interface framework requires user choice

- **WHEN** 用户要求普通配置并说明需要接口测试，但项目只有单元框架且没有接口测试约定
- **THEN** Setup SHALL 给出最少候选和影响并等待确认，不把单元框架推断为接口框架，也不等待 Loop 初始化才处理

#### Scenario: Existing framework does not answer test scope

- **WHEN** 项目只有单元框架，用户没有明确配置哪些测试类型
- **THEN** Setup SHALL 按项目功能和目标给出适用测试类型建议，必要时确认范围，不把缺少其他框架写成其他测试类型不适用

#### Scenario: User excludes a surface

- **WHEN** 用户明确当前只开展单元和接口测试，暂不开展 UI 测试
- **THEN** Setup SHALL 记录该范围并沿用已有框架，对缺失的接口约定提出确认，不询问 UI 框架

### Requirement: Persist setup state and freshness

`.test-privateer/project.md` SHALL 记录配置契约版本、顶层 Setup 状态、最近校准时间、依据版本或来源快照、失效条件、当前阻塞及恢复入口。顶层状态 SHALL 区分 `ready`、`awaiting_user_confirmation`、`partial` 和 `blocked`；`ready` 只表示项目配置、TCO、关键治理决定、适用测试表面和权威资产在项目层面可定位，MUST NOT 表示当前环境、测试、CI 或宿主能力已验证。

Setup SHALL 在可定位时记录 Git 提交，否则记录实际读取的来源集合和日期，MUST NOT 编造版本。失效条件 SHALL 覆盖会改变项目测试方式的规则、产品／架构、构建／CI、测试框架或入口、TCO、治理责任及资产位置变化。

#### Scenario: Saved profile still awaits a decision

- **WHEN** 配置草稿可以保存，但仍有会改变测试范围、责任或安全边界的用户决定
- **THEN** Setup SHALL 将顶层状态标为 `awaiting_user_confirmation` 并记录问题和恢复入口，MUST NOT 因文件已保存而报告 `ready`

#### Scenario: Source snapshot cannot use a commit

- **WHEN** 目标项目没有可定位的版本提交
- **THEN** Setup SHALL 记录本轮实际读取的来源集合和校准日期，不编造提交、标签或版本号

### Requirement: Record project test surface readiness

项目配置 SHALL 为每个已调查的候选测试表面保留一行，记录适用性、选定框架或入口、选择来源、项目级就绪状态、最近长期证据和阻塞／恢复入口。适用性未知的表面 SHALL 记录取证动作和 `pending_choice`，MUST NOT 移出矩阵或因缺少材料写成不适用。项目级就绪状态 SHALL 只使用 `ready`、`declared_unverified`、`driver_missing`、`pending_choice`、`blocked` 或 `not_applicable`，并 SHALL 区分框架已声明、可执行驱动缺失、适用性或选择未定及权威来源冲突。

当前机器、账号、网络或服务的临时状态 MUST NOT 固化为测试表面的长期项目状态，除非项目权威来源明确将其定义为长期约束。

#### Scenario: Applicable surface has no driver

- **WHEN** 项目确认某测试表面适用并已选定框架，但仓库和权威入口中没有可执行驱动
- **THEN** Setup SHALL 将该表面标为 `driver_missing` 并记录补建入口，不把框架名称等同于可运行

#### Scenario: Current environment is temporarily unavailable

- **WHEN** 测试表面的项目入口可定位，但当前机器或服务暂时不可用
- **THEN** Setup SHALL 保持项目级状态基于长期来源，并在当轮结果单独报告环境未验证或故障

#### Scenario: A candidate surface has unknown applicability

- **WHEN** 项目材料不足以判断 Agent 评测、UI 或其他候选测试表面是否适用
- **THEN** Setup SHALL 在矩阵保留该表面、标为 `pending_choice` 并记录取证动作，不省略该行或写成 `not_applicable`

### Requirement: Maintain one authoritative test asset registry

项目配置 SHALL 用一个资产索引统一记录 TCO、需求测试资产、测试 Run、原始证据、测试报告和盲测隔离输出的权威位置、维护责任、访问边界、保留／失效条件及状态与恢复入口。相同信息 MUST NOT 分散复制为互相独立的项目决定。

尚不存在的资产 SHALL 记录为 `pending`、`blocked` 或 `not_applicable` 及恢复入口；Setup MUST NOT 为填满索引创建空目录、空文件或占位验证资产。

#### Scenario: Run assets are not initialized

- **WHEN** 普通 Setup 尚未执行任何测试 Run，项目也没有既有 Run 根目录
- **THEN** Setup SHALL 在资产索引记录未就绪状态和后续入口，不创建空 Run、证据目录或报告

#### Scenario: Evidence access differs from report access

- **WHEN** 原始证据包含敏感内容而测试报告面向更广的项目成员
- **THEN** Setup SHALL 在同一资产索引中分别记录两者的权威位置、访问边界和保留条件，不用一个默认目录掩盖访问差异

## MODIFIED Requirements

### Requirement: Keep project configuration separate from testing assets

`.test-privateer/project.md` SHALL 描述项目如何开展测试，不得替代 `testing/TCO.md`、需求测试分析、测试依据、测试用例、执行记录或测试信心报告。Setup SHALL 通过 `mapping-project-test-space` 初始化或校准 TCO，但 SHALL NOT 把 TCO 正文复制到项目配置，也 SHALL NOT 为完成初始化自动生成需求测试分析、用例、执行记录、报告或一次运行结果。

测试资源、证据位置或验证器可以由项目配置指向权威资产。产品和测试空间认知继续由唯一 TCO 维护；单需求认识继续由需求资产维护；每轮执行继续由 Run ID 和执行记录维护。

#### Scenario: Project has no TCO

- **WHEN** 用户要求初始化项目，目标项目还没有 `testing/TCO.md` 且未明确排除建图
- **THEN** Setup SHALL 调用项目建图专项建立有来源的 TCO 草案，并让项目配置只引用其路径和状态，不复制地图正文

#### Scenario: Setup observes a temporary outage

- **WHEN** 调查期间测试环境暂时不可访问
- **THEN** Setup SHALL 将其作为本次未验证状态报告，不把临时故障写成长期项目规则

### Requirement: Confirm material governance gaps during setup

项目初始化时，TCO、缺陷入口、测试责任、风险接受或 CI 门禁属于项目测试治理信息，不是完整 Test Loop 专属字段。Setup SHALL 在普通配置和完整 Loop 配置中调查这些信息；其中未知决定会影响后续交接、执行安全、证据位置或判定时，Setup SHALL 先给出依据、推荐、影响和应答角色，等待确认或明确记录当前不接入。用户选择普通测试入口配置 SHALL NOT 缩小调查范围，只表示本轮不评估完整 Loop 就绪状态。Setup MUST NOT 仅以“未记录”代替项目决定并宣称相关配置完成。TCO 的内容未知 SHALL 进入草案和取证任务，不得把 TCO 本身默认为可缺失。

#### Scenario: Ordinary setup has governance gaps

- **WHEN** 用户只要求普通测试入口配置，但项目没有可定位的 TCO、缺陷入口、测试责任或 CI 门禁决定，且这些缺口会影响后续测试交接或判定
- **THEN** Setup SHALL 继续调查并逐项确认关键缺口，不得把普通配置选择解释为忽略治理字段

#### Scenario: Defect and quality responsibility are unknown

- **WHEN** 项目没有可定位的缺陷入口和风险接受责任，且这些决定会影响测试交接
- **THEN** Setup SHALL 提出当前最重要的一个确认问题，不把缺口列表当作已完成的治理配置

#### Scenario: User selects ordinary setup after scope clarification

- **WHEN** Setup 询问配置范围，用户选择普通测试入口配置
- **THEN** Setup SHALL 继续核对普通配置的治理与框架决定，将完整 Loop 状态记为 `not_configured`；仍有会改变测试方式的未决项时停在草稿和确认问题，不提前写入或宣称配置完成

### Requirement: Establish full test loop readiness

当项目预期使用完整 Test Loop 时，Setup SHALL 建立可判定的 Loop 就绪契约，覆盖测试资产根目录、盲测隔离输出位置、共享资源与并行策略、真实验证器入口、质量责任、缺陷升级和风险接受边界。TCO 作为普通 Setup 的核心资产先由 `mapping-project-test-space` 建立或校准，不作为 Loop 专属决定重复维护。

每项 Loop 架构决定 SHALL 处于以下状态之一：项目权威来源已确认、用户已确认、明确不适用、或用户明确确认的后续补建入口。尚未取得这些状态的关键决定 SHALL 记录在配置草稿的未决项并逐项询问用户；Setup MUST NOT 把“未记录”或推荐方案当成已确认决定，也 MUST NOT 在关键决定未关闭时宣称完整 Loop 已就绪。

完整 Loop 就绪状态 SHALL 至少区分 `ready`、`awaiting_user_confirmation` 和 `blocked`。`ready` 仅表示项目级架构决定可定位；不证明环境已验证、测试已运行、质量门禁已接入或当前宿主可创建子代理。当前宿主能力 SHALL 只在当轮运行观察中报告，不写入长期项目配置。

Setup SHALL 调查已有验证器是否覆盖启动、就绪检查、驱动、证据、清理和并行隔离。没有可定位验证器时，Setup SHALL 推荐建立或补建验证器，并经用户确认后记录后续入口；Setup MUST NOT 为完成初始化自动生成验证器、需求测试资产或 CI。

#### Scenario: Governance fields are missing

- **WHEN** Setup 发现项目没有缺陷平台、测试责任角色和风险接受边界，且用户要求支持完整 Test Loop
- **THEN** Setup SHALL 逐项给出推荐、影响和应答角色，并将完整 Loop 状态报告为 `awaiting_user_confirmation`，不宣称初始化已完成

#### Scenario: User confirms a deferred verifier

- **WHEN** 项目没有真实验证器，用户确认先记录后续补建入口而不在本轮生成
- **THEN** Setup SHALL 保存该确认和恢复入口，并将完整 Loop 执行就绪状态报告为 `blocked`，不把配置保存冒充验证器可用

#### Scenario: Existing verifier is authoritative

- **WHEN** 项目文档和脚本已经定义启动、就绪检查、驱动、证据、清理和隔离方式
- **THEN** Setup SHALL 引用这些来源并将项目级 Loop 架构标为 `ready`，同时保留环境和宿主能力未验证状态
