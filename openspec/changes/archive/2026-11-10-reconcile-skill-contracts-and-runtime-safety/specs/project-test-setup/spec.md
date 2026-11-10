## MODIFIED Requirements

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
