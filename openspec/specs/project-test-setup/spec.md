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

Setup SHALL 在写入前展示项目配置草稿，并将已确认范围或用户明确选型委托内形成的配置保存到目标项目的 `.test-privateer/project.md`。项目配置 SHALL 至少覆盖适用范围、权威来源、测试入口、测试框架与驱动约定、环境与安全边界、身份与数据准备、质量门槛、证据策略、缺陷平台、责任角色、测试资产位置和验证器入口。

项目配置 SHALL 优先保存来源指针和项目尚未记录的已确认补充。仓库内来源指针 SHALL 相对项目根目录书写，不得相对 `.test-privateer/project.md` 使用 `../`。已有脚本、CI 或项目文档是命令和规则的权威来源时，配置 SHALL 引用来源而不是复制易失效的快照。没有正式来源的用户确认决定可以保存在配置中，并注明确认范围。

每个已使用测试表面的框架约定 SHALL 来自当前项目权威来源、用户指定或用户明确委托范围内的选型决定，并保留依据。没有项目约定及选型委托，且选择会实质改变长期依赖、维护方式、费用或执行边界时，Setup SHALL 说明候选方案和影响并等待确认；MUST NOT 因某个框架存在专项 Skill 而自动选择、安装或替换项目框架。框架专项 Skill 只有在当前任务框架选择有上述依据时才适用。选型委托 MUST NOT 自动扩大为安装、联网、付费、替换既有套件或执行产品测试的权限；已有有效决定 SHALL 直接沿用，不反复确认。

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

- **WHEN** 项目需要建立 Agent 评测，但仓库没有框架约定、用户未委托选型，且不同选择会改变测试资产和运行方式
- **THEN** Setup SHALL 提供最少候选及影响并等待用户确认，不得仅因 DeepEval 或其他框架有现成 Skill 而自动选择

#### Scenario: User delegates a bounded framework choice

- **WHEN** 用户明确委托在已说明的成本和依赖边界内选择测试框架
- **THEN** Setup SHALL 在该范围内选型并说明依据，不重复索取相同决定；安装及测试执行仍按各自授权判断

### Requirement: Keep project configuration separate from testing assets

`.test-privateer/project.md` SHALL 描述项目如何开展测试，不得替代 `testing/TCO.md`、需求测试分析、测试依据、测试用例、执行记录或测试信心报告。Setup SHALL 通过 `mapping-project-test-space` 初始化或校准 TCO，但 SHALL NOT 把 TCO 正文复制到项目配置，也 SHALL NOT 为完成初始化自动生成需求测试分析、用例、执行记录、报告或一次运行结果。

测试资源、证据位置或验证器可以由项目配置指向权威资产。产品和测试空间认知继续由唯一 TCO 维护；单需求认识继续由需求资产维护；每轮执行继续由 Run ID 和执行记录维护。

#### Scenario: Project has no TCO

- **WHEN** 用户要求初始化项目，目标项目还没有 `testing/TCO.md` 且未明确排除建图
- **THEN** Setup SHALL 调用项目建图专项建立有来源的 TCO 草案，并让项目配置只引用其路径和状态，不复制地图正文

#### Scenario: Setup observes a temporary outage

- **WHEN** 调查期间测试环境暂时不可访问
- **THEN** Setup SHALL 将其作为本次未验证状态报告，不把临时故障写成长期项目规则

### Requirement: Rerun setup idempotently and preserve human content

重复运行时，Setup SHALL 读取现有项目配置，更新已变化的受管内容，保留仍有效的确认决定和非受管人工内容，并避免追加重复章节。失效来源或退役配置 SHALL 被修正、删除或标明替代位置。

写入工具 SHALL 要求目标项目根目录已经存在，只接收受管标记之间的非空正文，并拒绝覆盖无标记旧文件、标记异常文件、符号链接配置目录或符号链接目标文件。更新已有配置时 SHALL 保留受管区外内容、原始换行和文件权限。

项目规则要求写后运行格式化器、同步器或生成器时，Setup SHALL 在正式发布前对暂存候选完成所需动作及内容、权限检查；不能安全处理暂存候选的动作 SHALL 保留为写入阻塞，MUST NOT 在写入工具返回成功后单独运行写后工具并保留变形文件。用于传递受管区内容的草稿 SHALL 使用临时文件或内存，完成后不得作为第二份配置保留在项目中。

候选准备、后处理和校验失败时，写入工具 SHALL 保持正式目标不变并清理本次暂存文件；正式发布前 SHALL 复核目标位置、存在性、内容、文件身份及权限是否仍与初始快照一致，发现其他写入者的变更时 SHALL 保留该变更并报告冲突。发布后仍 SHALL 回读；无法确认差异属于本次操作时，MUST NOT 无条件恢复旧快照、删除正式目标或宣称完成。写入工具 SHALL 报告未完成部分及核对入口，MUST NOT 将单文件原子替换或提交前比较表述为对未协调外部写入的完整事务隔离。

#### Scenario: Setup reruns after a CI path change

- **WHEN** 项目的 CI 文件已经迁移，配置仍引用旧路径
- **THEN** Setup SHALL 更新来源指针，保留无关人工说明，并确保配置中只保留一个有效入口

#### Scenario: Readback differs from the draft

- **WHEN** 暂存候选的回读缺少已确认字段或覆盖了人工内容
- **THEN** Setup SHALL 拒绝发布并清理本次候选，保持正式目标不变，报告配置未完成，不把写入命令成功当作完成

#### Scenario: Another writer changes the profile during candidate preparation

- **WHEN** 候选准备期间其他写入者修改正式文件、删除目标或在初次创建路径写入自己的文件
- **THEN** 写入工具 SHALL 检测快照冲突，保留他人当前内容或删除决定，不以原始快照覆盖，也不删除他人创建的文件

#### Scenario: Published content no longer matches the candidate

- **WHEN** 发布后回读不一致，且无法确认差异只来自本次操作
- **THEN** 写入工具 SHALL 报告未完成与核对入口，保留正式目标现状，不执行破坏性回滚，不声称全局并发安全

#### Scenario: Candidate postprocessing fails

- **WHEN** 候选回调抛错、删除候选、改变内容或产生无法恢复的权限差异
- **THEN** 工具 SHALL 在正式发布前失败，清理仅属于本次操作的临时文件，保留原正式文件或原本不存在的状态

### Requirement: Separate saved configuration from verified readiness

Setup 结论 SHALL 分别说明项目配置已保存、入口已确认、框架约定已确认、当前宿主框架实施能力已就绪、环境已实际验证、测试已实际运行和质量门禁已接入的状态。只完成调查或写入时，Agent MUST NOT 宣称框架已经安装可用，或环境、测试、门禁已经可用。

项目明确选择 DeepEval 时，Setup SHALL 检查当前宿主能否读取任务所需的 Confident AI 官方 Skills，并区分官方 Skill、项目 Python 依赖和项目评测入口的就绪状态。当前宿主状态 SHALL 只作为本轮观察报告，不得写成长期项目事实。

官方 Skill 缺失时，Setup SHALL 说明缺失对象、官方来源、安装范围和安装后复检动作，并询问用户是否安装。用户尚未决定且尚未运行评测时，当前宿主所需官方 Skill 的就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题；等待选择不是一次评测结果，MUST NOT 同时把这一待确认状态写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后，Agent 才 SHALL 使用宿主已有的 Skill 安装能力；拒绝、宿主不支持安装或安装后仍不可读时，Agent SHALL 保留 `missing_official_skill`。安装位置和作用域 SHALL 由宿主安装能力与用户选择决定；没有宿主安装入口时，Agent MUST NOT 自行创建项目内 Skill 目录、克隆、下载或复制官方 Skill。该确认 MUST NOT 被扩大为安装 Python 依赖、修改锁文件、登录、上传、调用外部 Judge、产生费用或执行产品测试的授权。

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

#### Scenario: Project configuration and host capability differ

- **WHEN** 项目配置本身符合 ready 条件，但当前宿主官方 Skill 尚待安装确认
- **THEN** Setup SHALL 分别说明项目配置状态和当前宿主官方 Skill 状态，不将 awaiting_install_confirmation 写入项目配置的长期状态枚举，也不将等待决定记为已执行评测的环境失败

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

普通 Setup SHALL 按项目功能、已有测试和当前目标核对单元、接口、E2E、UI、Agent 评测等适用测试表面；适用范围不清时 SHALL 提出建议并确认，不把没有入口推断为不需要。每个适用表面的框架或项目自有入口 SHALL 分别记录来源。已有权威约定 SHALL 直接沿用；需要新增能力但没有约定及选型委托，且选择会实质改变长期依赖、维护方式、费用或执行边界时，Setup SHALL 给出最少候选、推荐和影响并等待确认；用户已明确委托选型时 SHALL 在约定边界内决定并保留依据。Setup MUST NOT 把已有单元框架推断为其他表面已配置，也不得因对应专项 Skill 存在而自动选择框架。用户明确暂不开展的表面 SHALL 记录决定及适用范围，不为这些表面反复询问。

#### Scenario: Missing interface framework requires user choice

- **WHEN** 用户要求普通配置并说明需要接口测试，但项目只有单元框架且没有接口测试约定，用户未委托接口选型
- **THEN** Setup SHALL 给出最少候选和影响并等待确认，不把单元框架推断为接口框架，也不等待 Loop 初始化才处理

#### Scenario: Existing framework does not answer test scope

- **WHEN** 项目只有单元框架，用户没有明确配置哪些测试类型
- **THEN** Setup SHALL 按项目功能和目标给出适用测试类型建议，必要时确认范围，不把缺少其他框架写成其他测试类型不适用

#### Scenario: User excludes a surface

- **WHEN** 用户明确当前只开展单元和接口测试，暂不开展 UI 测试
- **THEN** Setup SHALL 记录该范围并沿用已有框架，对缺失且未委托选型的接口约定提出确认，不询问 UI 框架

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

项目配置 SHALL 为每个已调查的候选测试表面保留一行，记录适用性、选定框架或入口、选择来源、六段 Harness 入口或缺口、Harness 状态、最近长期证据和阻塞／恢复入口。六段 SHALL 覆盖 `Prepare`（目标、身份、输入和初始数据）、`Start`（启动或连接及就绪检查）、`Drive`（真实刺激）、`Observe`（独立预期与实际结果）、`Preserve`（原始证据保留）和 `Restore`（只清理本轮拥有的资源并保留证据）。这些能力可以由同一 Runner 覆盖，不要求六个独立脚本或新目录。

Harness 状态 SHALL 只使用 `not_configured`、`partial`、`declared_unverified`、`verified`、`blocked` 和 `not_applicable`。框架名称、测试目录、健康检查或一次退出码单独不能产生 `verified`；临时机器、账号、网络或服务状态 SHALL 只进入本轮报告，不固化为长期 Harness 状态。配置契约升级为 `test-privateer-project-profile/v2` 时，旧 v1 的“项目级 `ready`”在没有六段实际证据时 SHALL 迁移为 `declared_unverified`，不得自动迁移为 `verified`。

#### Scenario: Applicable surface has no driver

- **WHEN** 项目确认某测试表面适用并已选定框架，但可执行驱动、独立观察、证据保留或资源恢复至少一段缺失
- **THEN** Setup SHALL 将该表面标为 `partial` 并记录缺失段和补建入口，不把框架名称等同于可运行

#### Scenario: Current environment is temporarily unavailable

- **WHEN** 测试表面的项目入口和长期 Harness 证据可定位，但当前机器或服务暂时不可用
- **THEN** Setup SHALL 保持项目级状态基于长期来源，并在当轮结果单独报告环境未验证或故障

#### Scenario: A candidate surface has unknown applicability

- **WHEN** 项目材料不足以判断 Agent 评测、UI 或其他候选测试表面是否适用
- **THEN** Setup SHALL 在矩阵保留该表面、标为 `not_configured` 并记录取证动作，不省略该行或写成 `not_applicable`

#### Scenario: A framework exists but the API driver is missing

- **WHEN** 项目已声明接口测试框架，但没有可定位的请求驱动、业务观察或证据保留入口
- **THEN** Setup SHALL 记录该测试表面的 Harness 为 `partial` 或 `declared_unverified`，列出缺失段和恢复入口，不把框架存在写成 `verified`

#### Scenario: An existing harness covers a selected surface

- **WHEN** 项目已有入口能够准备隔离数据、启动或连接目标、执行真实刺激、观察独立结果、保存原始证据并清理本轮资源
- **THEN** Setup SHALL 记录六段来源和可复核证据，将该表面标为 `verified`，同时说明这不表示产品通过或全量覆盖

#### Scenario: An old v1 profile has project-level ready

- **WHEN** Setup 读取旧项目配置，发现测试表面只有 v1 的 `ready`，没有六段 Harness 证据
- **THEN** Setup SHALL 保留原来源并将 Harness 标为 `declared_unverified`，记录重校准入口，不把迁移本身当作运行验证

### Requirement: Maintain one authoritative test asset registry

项目配置 SHALL 用一个资产索引统一记录 TCO、需求测试资产、测试 Run、原始证据、测试报告和盲测隔离输出的权威位置、维护责任、访问边界、保留／失效条件及状态与恢复入口。相同信息 MUST NOT 分散复制为互相独立的项目决定。

尚不存在的资产 SHALL 记录为 `pending`、`blocked` 或 `not_applicable` 及恢复入口；Setup MUST NOT 为填满索引创建空目录、空文件或占位验证资产。

#### Scenario: Run assets are not initialized

- **WHEN** 普通 Setup 尚未执行任何测试 Run，项目也没有既有 Run 根目录
- **THEN** Setup SHALL 在资产索引记录未就绪状态和后续入口，不创建空 Run、证据目录或报告

#### Scenario: Evidence access differs from report access

- **WHEN** 原始证据包含敏感内容而测试报告面向更广的项目成员
- **THEN** Setup SHALL 在同一资产索引中分别记录两者的权威位置、访问边界和保留条件，不用一个默认目录掩盖访问差异

### Requirement: Keep Harness setup proportional and separate from authorization

Setup SHALL 只调查和记录 Harness 能力，不因六段模型自动运行产品测试、启动服务、安装框架、创建数据、修改 CI 或生成验证器。需要实际构造或修复 Harness 时，Setup SHALL 指向 `designing-test-automation` 或现有验证器交接；测试表面不适用时 SHALL 记录 `not_applicable` 及依据。普通单层任务不得因项目尚未建立完整 Loop Harness 而被 Setup 阻塞。

顶层 Setup `ready` MAY 与有明确项目选择和恢复入口的 `partial` 或 `declared_unverified` Harness 共存，但 MUST NOT 与因框架、入口或适用性仍待决定而产生的 `not_configured` 共存；这种未决选择 SHALL 使用 `awaiting_user_confirmation` 并停在一个具体问题。

#### Scenario: A simple unit task does not need a project Harness

- **WHEN** 用户只要求一个局部单元测试，项目级 Harness 尚未配置
- **THEN** Setup 或路由 SHALL 不强制初始化完整 Harness、浏览器、服务或额外框架，直接保留单层任务所需的最小边界

#### Scenario: Harness construction needs authorization

- **WHEN** Setup 发现某测试表面缺少可执行 Harness，且补建会修改测试资产或访问环境
- **THEN** Setup SHALL 报告缺口和影响，交接到自动化设计专项；不得把推荐方案当成已确认或已验证

#### Scenario: An unconfirmed generated runner is discovered

- **WHEN** 仓库存在未提交、临时、历史实验或 AI 生成的测试入口，但项目权威来源和用户都没有采纳它，且本轮没有额外授权进行试验执行
- **THEN** Setup SHALL 只把它视为候选，不运行、不写成项目入口或 `verified`；采纳会改变后续执行时停在一个明确确认问题

#### Scenario: Trial execution and permanent adoption are decided separately

- **WHEN** 用户在初始化任务中另行授权验证临时驱动，但明确尚不将其采纳为长期入口
- **THEN** Setup SHALL 按该执行范围交接自动化专项，分别报告试验结果与采纳决定，不以未采纳阻塞获准试验，也不因试验通过自动更新长期入口或 verified 状态
