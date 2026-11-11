# testing-workflow Specification

## Purpose
规定黑帆测试官如何沿当前任务选择测试活动、保持授权与阶段边界，并维护可追溯的测试资产。此规格抽取已合并的工作流约定，不要求独立任务建立完整项目档案，也不把测试设计当成产品执行。

## Requirements

### Requirement: Route by current task and authorized stage
主入口 SHALL 沿已确认任务、已有材料和信息缺口选择当前活动，分别交代完成、未完成、依据、下一动作及执行状态；专项直接调用只完成其当前请求。主入口 SHALL 先判断用户最终目标、交付物、成功信号和任务抽象层级是否足以选择工作路径；当缺口会改变工作方向时 SHALL 先使用 `shaping-ai-tasks`。目标明确但产品事实、业务规则、系统关系或 oracle 不清时 SHALL 继续使用 `clarifying-test-basis`，不得把任务升级重复成测试依据澄清。

主入口 SHALL 用稳定导航层组织路由：项目主线、入口场景、独立能力和词汇／资产层；路由表 SHALL 保持当前处境与专项入口的短映射，详细能力与例外 SHALL 由对应专项维护。主入口在陈述某专项能力、比较入口或建议跳过前，SHALL 读取该专项的 `SKILL.md`；摘要不得替代目标入口。可自行核实的事实 SHALL 先在授权内调查；业务决策、发布决定和跨授权执行 SHALL 留给有权用户。

主入口 SHALL 支持明确请求直达对应专项，不强制重走任务升级或项目建图。长项目 SHALL 保留路线状态；在阶段交接、新会话或上下文压缩后继续前，SHALL 先恢复项目规则、TCO、路线状态和最近产物，不得在缺失上下文时宣称延续既有结论。

#### Scenario: Independent analysis without product execution
- **WHEN** 用户只要求分析一份规则明确的材料
- **THEN** 直接完成有关分析，不强制建项目地图、不重复确认已知规则，也不执行产品测试或把分析写成已测试

#### Scenario: Project task requires context
- **WHEN** 已选择项目测试且系统关系不足以支持变化判断
- **THEN** 补齐唯一项目 TCO 所需上下文后推进相关分析，无关未知作为待办，不要求写完项目百科

#### Scenario: Vague testing request needs task shaping
- **WHEN** 用户只提出“测试一下”或“帮我看看有没有问题”，且不同最终结果会导致不同测试活动
- **THEN** 主入口 SHALL 先交给 `shaping-ai-tasks`，在任务契约确认或带边界推荐后再进入测试使命或其他专项

#### Scenario: Clear testing goal keeps the existing route
- **WHEN** 用户已明确测试对象、目的和交付物，只缺产品规则或 oracle
- **THEN** 主入口 SHALL 跳过任务升级并调用 `clarifying-test-basis`

#### Scenario: Router must not rely on stale summaries
- **WHEN** 主入口需要说明某专项不能覆盖当前请求，或建议跳过该专项
- **THEN** SHALL 先读取该专项 `SKILL.md`，再基于实际入口给出判断和替代路由

#### Scenario: New session continues a project test
- **WHEN** 项目测试在新会话或上下文压缩后继续
- **THEN** SHALL 先恢复项目规则、TCO、路线状态和最近产物；确认仍适用后再推进，不把旧结论冒充当前上下文结论

#### Scenario: Standalone request bypasses the project main line
- **WHEN** 用户明确请求报告汇总、方案质检、错题本维护或单层测试编写
- **THEN** SHALL 直达对应专项并停止在其交付边界，不强制补项目地图或产品执行

### Requirement: Preserve uncertainty and causal evidence
澄清与调查 SHALL 区分规则未知、观察、缺陷、原因假设与已支持的解释，保留影响判断的未知及具体取证动作。

#### Scenario: Missing business rule
- **WHEN** 缺失的配置时点会改变预期结果
- **THEN** 给出具体问题、推荐及测试影响，继续不依赖答案的部分，不把未决选项写成既定预期

#### Scenario: Local guard explains only amplification
- **WHEN** 现有证据只能解释异常如何被放大，不能解释最初为何发生
- **THEN** 分开说明已解释与未解释部分，不以止损或修复后通过替代完整原因证据

### Requirement: Maintain one traceable test asset chain
测试资产 SHALL 保持需求、测试项、用例、风险及回归证据的可追溯关系；同一对象复用权威编号，当前规则与历史观察分开维护。

#### Scenario: Rule changes after an earlier successful run
- **WHEN** 已确认新规则，需要更新分析与用例
- **THEN** 同步有效规则、关联和安排，保留历史执行记录及其版本，不将旧通过升级为新规则已验证

#### Scenario: Partial design handoff
- **WHEN** 本轮只完成部分已识别测试内容
- **THEN** 交接保留未设计、阻塞或排除项及依据，不把局部用例完成称为整体测试完成

### Requirement: Preserve human-in-the-loop checkpoints
当测试推进依赖只有人能完成的步骤时，Agent SHALL 建立或恢复可交接的人工检查点。检查点 SHALL 包含负责人、目标、操作入口、前置状态、操作、成功观察、失败证据、回填位置和恢复下一动作；需要时 SHALL 写明超时或放弃条件。检查点状态 SHALL 区分待确认、待执行、执行中、已完成、失败和取消。

人工返回的截图、值、错误或结论 SHALL 作为该负责人提供的原始观察记录，注明回填人和时间；不得写成 Agent 亲自执行。结果未回填前，Agent SHALL 不推进依赖该步骤的测试结论；新会话或阶段交接后 SHALL 先恢复未完成检查点状态。

#### Scenario: Agent lacks environment access
- **WHEN** 测试已获授权但目标环境只能由用户访问
- **THEN** Agent SHALL 生成包含目标、入口、操作、观察值、失败保留证据和回填位置的检查点，并停在该检查点；不把指导步骤写成已执行

#### Scenario: Human result is returned
- **WHEN** 用户回填截图、接口值或操作结论
- **THEN** SHALL 记录回填人、时间、原始证据和适用范围，再更新测试记录与下一步；不把口述概括改写为 Agent 观察

#### Scenario: Checkpoint resumes in a new session
- **WHEN** 新会话继续包含未完成人工检查点的测试
- **THEN** SHALL 先恢复检查点状态和依赖关系；未回填结果不推进后续测试结论，失败或取消保留原因和剩余动作

#### Scenario: Short request does not need a checkpoint artifact
- **WHEN** 用户只需一句操作指导，且该步骤不阻塞当前测试链
- **THEN** 直接说明操作和观察方式，不强制生成检查点模板或状态表

### Requirement: Preserve auditable pause and resume state
当测试执行需要跨会话暂停、上下文可能降级或用户明确要求暂停时，Agent SHALL 交付冷启动恢复点。恢复点 SHALL 记录原始目标与授权、可判定退出条件、已完成及已验证事实、未验证结论、产物与原始证据路径、未完成项、阻塞、下一动作和恢复判据。

恢复时 Agent SHALL 先读取项目规则、权威测试资产、恢复点和最近产物，继承已完成工作；仅对仍影响当前判断的关键断言做抽查，SHALL NOT 重做已完成工作或把旧结论重新冒充本轮观察。恢复点缺失或相互冲突时，Agent SHALL 停在可定位边界并说明需要补证的范围。

#### Scenario: User pauses a session
- **WHEN** 用户要求暂停或即将跨会话恢复
- **THEN** Agent SHALL 在当前原子步骤边界停止并交付恢复点，不开启新的测试分支

#### Scenario: Session resumes
- **WHEN** 新会话继续一个已暂停的测试任务
- **THEN** Agent SHALL 先恢复目标和状态，继承权威轨迹，只推进剩余工作

#### Scenario: Resume evidence conflicts
- **WHEN** 恢复点、测试资产或项目规则描述不一致
- **THEN** Agent SHALL 停在冲突点并说明差异和最小补证动作，不选择性忽略冲突

### Requirement: Verify agent behavior from actual load traces
Agent 行为评测 SHALL 使用自然任务提示，将隐藏判据、答案、预期缺陷、候选身份及比较标签与候选可见材料隔离。是否污染 SHALL 按内容是否泄漏评测意图或标准答案判断，MUST NOT 仅因真实任务、目录、字段或 Skill 原名含 test、eval、score 等词就判为泄漏或强制改名。判据 SHALL 只提供给评审；版本比较 SHALL 使用匿名标签，评审 SHALL 在同一尺度下判读。

结论 SHALL 区分最终输出、实际读取的 Skill／文件、工具轨迹和运行配置；SHALL NOT 以候选自述替代加载轨迹，也 SHALL NOT 跨项目扫描私有会话记录。失败 SHALL 保留为可诊断结果，不得为汇总方便改成通过。

#### Scenario: Candidate sees an organic task
- **WHEN** 评测候选收到任务提示
- **THEN** 提示、目录和文件名 SHALL 表现自然任务语境，不提示这是评测或比较

#### Scenario: Skill load is claimed
- **WHEN** 候选自称读取了某 Skill 或参考
- **THEN** SHALL 以当前授权内轨迹或可观察文件访问证据核验；无证据时按未确认加载处理

#### Scenario: Judge compares variants
- **WHEN** 评审比较多个版本输出
- **THEN** SHALL 只见匿名标签并使用同一判据；候选身份不进入评审上下文

#### Scenario: Natural testing vocabulary remains visible

- **WHEN** 任务需要读取 test-privateer、项目 tests 目录或真实业务 score 字段
- **THEN** 评测 SHALL 保留自然名称和执行所需信息，不因词面命中而删改任务或认定污染

#### Scenario: Innocently named input leaks hidden expectations

- **WHEN** 候选输入虽没有评测关键词，却含隐藏判据、预期缺陷或哪一版本应获胜的提示
- **THEN** 评测 SHALL 将该信息移出候选可见范围；已受污染的尝试记录为无效或受限证据，不作为盲测通过结果

### Requirement: Maintain an append-only test decision audit trail
当测试执行连续推进、多轮证据会改变解释、无人值守执行或用户明确要求审计时，Agent SHALL 维护追加式决策日志。每条决策 SHALL 记录时间、测试阶段、决策、理由、证据指针和结果；证据指针 SHALL 使用路径、稳定 ID、版本或等价定位方式，不得用叙述替代。

新证据、用户决策或失败 SHALL 通过新增记录取代旧决策的当前适用性；Agent SHALL NOT 重写或删除历史决策行。恢复点 SHALL 引用决策日志的最新边界，但不复制全部记录；普通短任务 SHALL NOT 被强制生成审计表。

#### Scenario: Evidence changes an earlier interpretation
- **WHEN** 后续执行显示先前 finding 的解释不成立
- **THEN** 新增决策行说明修正、依据和影响范围，保留原决策及其当时证据指针

#### Scenario: Unattended execution changes route
- **WHEN** 无人值守测试到达预设转向条件
- **THEN** 记录触发条件、决策、证据指针和下一阶段，再继续或停止

#### Scenario: Short execution stays lightweight
- **WHEN** 单会话只执行一个明确测试且证据不改变方向
- **THEN** 沿用正常测试记录，不强制创建决策日志

### Requirement: Maintain one authoritative test run record when coordination requires it

当测试跨多个阶段或会话、包含并行执行、需要暂停恢复，或用户明确要求审计时，Agent SHALL 建立一个稳定 Run ID 和唯一轮次记录。轮次记录 SHALL 保存测试对象与版本、触发来源、范围、授权、禁止动作、预算、退出条件、当前阶段、轮次状态、资产指针、阻塞和下一动作。

轮次记录 SHALL 只索引 TCO、需求分析、测试依据、用例、原始证据和报告。各资产的正文与状态仍由原权威位置维护。单会话、单项测试且方向不变时，Agent SHALL NOT 强制创建轮次记录。

#### Scenario: Multi-stage test creates one run record

- **WHEN** 用户要求从变化分析连续推进到用例、执行和报告
- **THEN** Agent SHALL 创建一个 Run ID，并让后续阶段更新同一轮次记录中的阶段、状态和资产指针

#### Scenario: Short execution stays lightweight

- **WHEN** 用户只要求执行一个明确测试，且任务不会跨会话或改变测试方向
- **THEN** Agent SHALL 使用现有用例与执行记录，不为满足格式创建独立轮次资产

#### Scenario: Resumed work uses the existing run

- **WHEN** 一个已暂停或受阻的测试轮次在新会话继续
- **THEN** Agent SHALL 先恢复原 Run ID、授权、退出条件和资产指针，再推进剩余工作

### Requirement: Separate run state from test verdict and confidence

轮次记录 SHALL 将流程状态维护为准备中、可执行、执行中、已暂停、受阻、已完成或已取消。单项测试的通过、失败、跳过、受阻和待判定 SHALL 留在执行记录；综合信心 SHALL 留在测试信心报告。

轮次“已完成”只表示已到达退出条件并完成交付，MUST NOT 表示所有测试通过、风险消失或负责人批准发布。轮次“受阻” SHALL 保留已取得的有效证据和未证实范围。

#### Scenario: Completed run contains failed tests

- **WHEN** 所有计划内检查均已取得结果，但其中存在符合证据的失败
- **THEN** 轮次可以标记为已完成，同时执行记录保留失败，信心报告说明影响和残余风险

#### Scenario: Blocked run has partial evidence

- **WHEN** 一部分测试已经执行，但后续步骤因凭据或环境缺失而无法继续
- **THEN** 轮次 SHALL 标记为受阻，并保留已执行证据、阻塞原因和恢复动作，不将整轮写成未开始或通过

### Requirement: Use one synthesizer for authoritative run assets

当多个 Agent 或执行分支参与同一轮测试时，调用方 SHALL 指定一个合成者维护轮次记录和共享测试资产。执行分支 SHALL 返回自己的范围、Run ID、测试 ID、原始证据和状态，MUST NOT 并发改写同一权威文件。

共享账号、数据、端口或会话无法隔离时，Agent SHALL 串行执行相关分支，或停在明确阻塞边界。并行数量 SHALL NOT 以牺牲证据身份或环境隔离为代价。

#### Scenario: Parallel API and UI checks return to one writer

- **WHEN** API 和 UI 检查可以使用隔离数据并行执行
- **THEN** 两个分支 SHALL 分别保留证据并交回同一合成者，由合成者更新轮次记录和综合结论

#### Scenario: Shared account cannot be isolated

- **WHEN** 两个执行分支会修改同一账号的共享状态
- **THEN** Agent SHALL 改为串行执行或报告受阻，不让两个分支并发写入后再猜测结果归属

### Requirement: Preserve completed run history

已暂停或受阻的轮次可以沿用原 Run ID 恢复。已完成或已取消的轮次 SHALL 保持历史身份；后续发生新的产品执行时 SHALL 创建新的 Run ID，并引用先前轮次，而不是把旧轮次改回执行中。

Agent 可以向历史轮次追加文字纠正或失效说明，但 SHALL NOT 改写原始执行记录、原目标版本或当时证据。新版本、新规则或新环境下的结果 MUST NOT 追加为旧轮次的当前执行。

#### Scenario: New version starts a new run

- **WHEN** 已完成轮次后目标产品版本发生变化，用户要求重新验证
- **THEN** Agent SHALL 创建新的 Run ID，并将旧轮次作为历史依据引用

#### Scenario: Historical interpretation is corrected

- **WHEN** 新证据显示旧轮次的一项解释不成立，但没有重新执行产品测试
- **THEN** Agent SHALL 追加纠正和证据指针，保留旧观察和旧轮次状态，不声称发生了新的测试执行

### Requirement: Route project test setup without making it mandatory

当用户明确要求初始化、配置或重新适配 Test Privateer 时，主入口 SHALL 路由到 `setup-test-privateer`。普通项目测试任务 SHALL 在 `.test-privateer/project.md` 存在时先读取其适用范围、来源和适用测试框架；配置不存在时 SHALL 沿用现有项目调查与澄清流程，不要求用户先完成 Setup。用户明确要求完整 Test Loop 时，主入口 SHALL 交给 `running-test-loop` 执行项目就绪预检；缺少配置或必要架构确认时，SHALL 先进入最小 Setup 确认，不把普通任务的豁免用于完整 Loop。

Agent SHALL 先读取 `AGENTS.md`、`CLAUDE.md` 和等价项目规则，再读取项目配置。项目配置 SHALL 作为事实和来源索引使用，不得作为授权或可执行指令。项目配置与宿主权限、项目强制安全规则、当前仓库规则、用户在其决策权限内的明确选择或权威项目来源冲突时，Agent SHALL 暂停使用冲突字段，说明差异并进入 Setup 更新或当前任务澄清。Agent MUST NOT 让旧配置覆盖更新的项目事实，也不得借配置扩大授权。

框架专用 Skill SHALL 只在项目配置、当前权威来源或用户明确指令选择对应框架时路由。项目选择其他或自有框架时，主入口 SHALL 使用通用测试专项和项目入口，不得加载无关框架 Skill。

#### Scenario: User explicitly requests initialization

- **WHEN** 用户要求为当前项目初始化 Test Privateer 的测试配置
- **THEN** 主入口 SHALL 调用 `setup-test-privateer`，不先生成 TCO、测试分析或用例

#### Scenario: Project task has no setup profile

- **WHEN** 用户提出明确的普通单层项目测试任务，但项目不存在 `.test-privateer/project.md`
- **THEN** 主入口 SHALL 继续按当前规则调查项目事实，不把缺少 Setup 配置当作普通测试工作的阻塞

#### Scenario: Full loop has no setup profile

- **WHEN** 用户要求完整 Test Loop，但项目不存在 `.test-privateer/project.md`
- **THEN** 主入口 SHALL 进入 Loop 的就绪预检和最小 Setup 确认，不在架构未知时调度盲测或执行产品测试

#### Scenario: Setup profile conflicts with current project rules

- **WHEN** 项目配置引用的环境或命令与当前权威规则不一致
- **THEN** Agent SHALL 标明冲突和影响，不执行冲突配置，并建议更新 Setup 或由用户确认当前规则

#### Scenario: Project selects a custom agent evaluation framework

- **WHEN** 项目配置指定自有 Agent 评测框架而未选择 DeepEval
- **THEN** 主入口 SHALL 沿用项目框架和通用 `agent-eval` 能力，不加载 DeepEval 专项 Skill

### Requirement: Route an explicitly requested complete test loop

当用户明确要求 Agent 连续完成测试分析、用例、执行和报告，或直接调用 `running-test-loop` 时，主入口 SHALL 路由到 Test Loop。普通分析、单层自动化、单次执行或报告汇总 SHALL 继续直达现有专项，不因存在 Loop 而强制进入完整流程。

Loop SHALL 依赖当前测试轮次和项目配置契约。前置 change 尚未落实或对应资产不存在时，Agent SHALL 停在可定位边界并说明缺少的契约，不在 Loop 内创建另一套临时格式。

#### Scenario: User requests the whole testing chain

- **WHEN** 用户要求从当前变化分析开始，自动生成用例、执行适用测试并输出测试报告
- **THEN** 主入口 SHALL 路由到 `running-test-loop`，由 Loop 复用各专项推进

#### Scenario: User requests one API test

- **WHEN** 用户只要求编写并运行一条明确接口测试
- **THEN** 主入口 SHALL 直达 `writing-api-tests` 或 `running-test-sessions`，不创建完整 Loop

### Requirement: Keep analysis and product execution authorization separate

测试分析 SHALL 可以读取项目材料、现有测试和历史结果，但 SHALL NOT 因分析任务本身运行产品测试、启动服务、安装依赖、创建数据或访问外部环境。只有用户明确要求执行，或 Test Loop 已记录相应授权时，Agent 才 SHALL 进入产品执行。

获得执行授权后，Agent SHALL 在授权范围内连续完成正常测试步骤。新增环境、凭据、费用、共享数据修改或其他超出原授权的动作 SHALL 触发澄清、人工检查点或停止。

#### Scenario: Change analysis has no execution authorization

- **WHEN** 用户只要求分析一项变化的测试影响
- **THEN** Agent SHALL 核对已有测试和历史证据，提出建议执行范围，但不得运行测试并把结果写入分析

#### Scenario: Test loop includes execution authorization

- **WHEN** 用户明确授权 Test Loop 在指定本地或测试环境运行测试
- **THEN** Agent SHALL 在记录的边界内连续执行，无需为每条正常测试重复请求许可

#### Scenario: Execution needs a new destructive action

- **WHEN** 已授权 Loop 后发现必须清理共享数据或访问生产环境才能继续
- **THEN** Agent SHALL 停止该分支并说明影响，不把原测试授权扩大到新的破坏性动作

### Requirement: Route DeepEval agent evaluation only when selected

当用户明确调用 DeepEval Agent 评测，或项目配置／当前权威来源选择 DeepEval 且任务需要建立、运行、审查或修正 Agent 评测时，主入口 SHALL 路由到 `evaluating-agents-with-deepeval`。该专项 SHALL 先继承 `agent-eval` 已固定的质量主张、场景、Oracle 和证据协议，再把 DeepEval 实施交给 Confident AI 官方 Skills；不得从框架指标重新定义业务目标，也不得在本包复制官方实现教程。

没有选择 DeepEval 时，普通 Agent 测试设计、评估审查、版本比较和失败归因 SHALL 继续使用 `agent-eval` 或项目自有框架。官方 DeepEval Skill 缺失时，Agent SHALL 说明官方来源、安装对象和影响并询问用户是否安装；用户尚未决定且尚未运行评测时，当前宿主所需官方 Skill 的就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题；该状态不得写入项目配置长期状态，也不得作为已执行评测的结果或同时写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后才可使用宿主已有安装能力，安装目标由该能力和用户选择决定。拒绝、宿主不支持安装或安装后仍不可读时，SHALL 报告具体缺口并降级到仍可执行的通用评测工作，不得凭记忆补写实现、静默安装、自行复制到项目目录、登录、上传或替换项目框架。

#### Scenario: Explicit DeepEval request

- **WHEN** 用户明确要求使用 DeepEval 为当前 Agent 建立或运行评测
- **THEN** 主入口 SHALL 路由到 DeepEval 质量约束，再由其调用官方 `deepeval` Skill；该请求只代表本轮框架选择，不要求项目永久迁移

#### Scenario: Generic agent evaluation request

- **WHEN** 用户只要求设计 Agent 测试或审查现有评估，项目没有选择 DeepEval
- **THEN** 主入口 SHALL 使用通用 `agent-eval`，不加载 DeepEval 专项

#### Scenario: Official DeepEval skill is unavailable

- **WHEN** 项目选择 DeepEval，但当前宿主缺少官方 `deepeval` Skill
- **THEN** Agent SHALL 先标为 `awaiting_install_confirmation` 并询问是否安装，在明确确认前不安装或自行选择项目内安装位置；若仍不可用，则保留可完成的场景、Oracle 和原始证据工作并标记 `missing_official_skill`

### Requirement: Separate handoff authorization from execution progress

阶段交接 SHALL 分别记录获准动作、权限边界及可定位来源，以及实际完成和未完成工作。执行中或已完成只 SHALL 描述进度，MUST NOT 作为执行授权的依据；SHALL 复用已有交接字段，不新增平行状态账本。

读取旧交接时 SHALL 将执行许可字段中的未开始、执行中、已完成等进度值还原为进度信息，并从用户指令、项目授权或其他有效来源核对动作范围。不能恢复授权依据且动作需授权时 SHALL 保留相应阻塞，同时继续不依赖该许可的工作。

#### Scenario: Old handoff says completed without an authorization source

- **WHEN** 旧交接的执行许可仅写已完成，当前任务未授权启动服务或再次运行产品测试
- **THEN** Agent SHALL 将已完成理解为历史进度，核对原始授权，不以该字段为由重新执行

#### Scenario: Valid authorization survives a cold handoff

- **WHEN** 交接保留了仍有效的执行授权、范围、限制及来源，任务尚未完成
- **THEN** 新会话 SHALL 沿授权继续相应动作，不因换会话重复请求相同许可，也不扩大原有边界

### Requirement: Discover automation capabilities through skill metadata

自动化专项的名称和 description SHALL 准确覆盖既有方法选择、Harness／项目验证器生成及维护能力，并与主入口路由、正文触发和实际交付一致。发现性验证 SHALL 先提供自然需求及可用名称／描述，再核对实际选择和加载路径，MUST NOT 通过直接提供目标 Skill 全文来替代入口发现验证。

#### Scenario: User asks to create a project verifier

- **WHEN** 用户描述需要可持续驱动真实产品并保留证据的验证资产，当前仅可见 Skill 名称和描述
- **THEN** Agent SHALL 能识别 designing-test-automation 为适用入口，随后按实际任务加载生成方法，不自行创建重复专项

#### Scenario: User asks to maintain an existing verifier

- **WHEN** 用户描述已有验证器与当前产品不一致，需要维护其驱动和证据能力
- **THEN** Agent SHALL 从元数据识别同一专项并加载维护方法，不误路由为仅选择测试框架

### Requirement: Maintain test assets at development and verification handoff

接入项目规则后，当前任务合成者 SHALL 在开发交付、验证交付及归档后核对变化影响：测试方式、治理或入口变化更新项目配置；业务／系统关系、覆盖或长期风险变化更新 TCO；局部结果留在原 change／Run。无相关影响 SHALL 不改文件或校准时间，不强制重跑 Setup、重建地图或补跑测试。

维护 SHALL 先读权威来源与受影响资产，保留历史证据和仍有效决定，只修改受影响字段并回读。配置路径 SHALL 保持相对项目根目录，其他文档链接 SHALL 按各自位置核验，不因维护跨文件资产而破坏原有引用约定。来源冲突、并发修改或超出权限时 SHALL 保留可定位的差异和恢复动作，不覆盖他人变更。缺少证据 MUST NOT 自动提升 Harness 状态、测试判定或风险接受状态。共享资产 SHALL 由唯一合成者维护，分支交回证据，不并发改写。

本轮重新声明或保留 Harness `verified` SHALL 核对其历史证据的对象、版本、实际观察与限制；已读证据不足时 SHALL 按既有状态定义修正，无法访问时保留未核实范围。历史已验证、当前未核实与本轮执行 MUST NOT 混写；任务勾选数和目录存在 MUST NOT 代替原始证据，也不因没有本轮执行而将有效历史证据一律降级。

#### Scenario: A developer changes a test entry

- **WHEN** 一个未继承 Setup 聊天的新开发会话通过项目规则完成测试入口迁移及相关验证
- **THEN** 该会话 SHALL 能沿实际项目入口读取共享维护规则，更新配置中的受影响入口与证据；只有覆盖认知改变才更新 TCO，不需用户再次调用 Setup

#### Scenario: A completed change is archived

- **WHEN** 用户已授权归档，活动 change 的实际来源位置发生迁移
- **THEN** 维护者 SHALL 按真实归档结果修正当前配置及 TCO 的受影响指针，保持历史证据与验收边界；未发生迁移时不得预填归档路径

#### Scenario: An unrelated edit is delivered

- **WHEN** 本次只改无关文案，未改变测试方式、项目覆盖或长期风险
- **THEN** 维护者 SHALL 保持 project.md、TCO 和历史证据不变，不为了完成检查制造资产变更

#### Scenario: Only a source revision pointer has expired

- **WHEN** 重跑校准仅发现来源提交不可定位，其他来源及证据仍支持原结论
- **THEN** 维护者 SHALL 只修正必要指针及来源说明，不借机改写正确正文、重排章节或增加无关细节

#### Scenario: A required update cannot be written

- **WHEN** 新证据影响长期测试资产，但当前任务禁止写入该资产或发现来源冲突
- **THEN** 维护者 SHALL 保留局部任务实际结果，交回受影响字段、证据和恢复动作，不声称资产同步完成，也不自动扩展授权
