# test-loop Specification

## Purpose
规定 Test Privateer 如何在一个有界授权内编排现有测试专项，连续完成分析、用例、执行、调查、回归和报告，并在证据、预算或安全边界要求时停止。

## Requirements

### Requirement: Start each test loop with a bounded contract

`running-test-loop` SHALL 在推进产品执行前固定测试对象、目标版本或快照、目标、范围、授权、禁止动作、环境影响、时间或成本预算和可判定退出条件。完整 Loop SHALL 使用当前测试轮次契约的 Run ID；已有可恢复轮次时 SHALL 先恢复，不得创建重复轮次。

缺少会改变测试对象、执行安全或完成判定的信息时，Loop SHALL 先调查可取得事实，再提出最小问题。缺口只影响部分阶段时，Loop SHALL 继续不依赖该信息的工作，并明确受阻范围。

#### Scenario: User authorizes an end-to-end test loop

- **WHEN** 用户要求分析当前变化、生成用例、运行获准测试并输出报告，同时给出目标项目和环境边界
- **THEN** Loop SHALL 建立或恢复 Run ID，记录授权、预算和退出条件，并在该范围内连续推进

#### Scenario: Target version is ambiguous

- **WHEN** 仓库和环境包含多个候选版本，选择不同版本会改变测试结论
- **THEN** Loop SHALL 先核实或询问目标版本，不在多个版本之间混合执行证据

### Requirement: Orchestrate existing skills through stage handoffs

Loop SHALL 复用现有专项 Skill 处理任务升级、使命、依据、项目地图、变化分析、风险、建模、用例、自校、自动化选择、执行、调查、回归和信心评估。Loop SHALL 使用各专项的 handoff 更新轮次状态和下一动作，MUST NOT 复制或改写专项方法。

Loop SHALL 按当前阶段即时加载专项 Skill。只有当前 handoff 或新证据使下一阶段成为当前动作时，才 SHALL 读取下一专项；MUST NOT 为预演完整流程一次性加载所有候选方法、框架或参考。已复用、跳过或尚未进入的阶段 SHALL NOT 预读其专项。

每个当前阶段 SHALL 固定输入指针、当前缺口、预期权威产物、完成证据和证据成立后的下一动作。只有权威产物实际存在、适用于当前版本，且完成证据支持当前阶段目标时才能推进。Skill 加载、计划、标题或 Agent 自述 MUST NOT 被当作阶段完成证据。

继续或恢复时，Loop SHALL 从 `run.md`、资产指针和实际项目状态重建当前状态，不得用旧聊天总结替代核对。已有资产足以支持当前阶段时，Loop SHALL 复用并核对其适用性。与当前目标无关或已经完成的阶段 SHALL 被跳过，并记录跳过依据。

局部阶段失败 SHALL NOT 让 Loop 重做所有已完成工作。新证据指出分析、用例、测试资产、执行证据或报告归纳存在问题时，Loop SHALL 回到拥有问题的最近责任阶段，只把受影响资产标为需要复核，保留未受影响的完成产物、证据和 Run ID，并在修正后重新验证受影响路径。

#### Scenario: Existing cases are current and executable

- **WHEN** 当前版本已有适用测试分析和经过复核的用例
- **THEN** Loop SHALL 跳过重复分析与用例生成，不加载这些已完成阶段的专项，核对执行条件后进入相应执行阶段

#### Scenario: New evidence changes the risk focus

- **WHEN** 执行发现新的高影响业务链或反驳原风险判断
- **THEN** Loop SHALL 记录转向依据，回到必要的分析或用例阶段，只更新受影响范围

#### Scenario: Stage claims completion but its artifact is missing

- **WHEN** 轮次记录声称用例阶段已完成，但指向的权威用例资产不存在或不适用于当前版本
- **THEN** Loop SHALL 将该阶段视为未完成或需要复核，先补齐并验证权威产物，不得依据阶段自述直接进入执行

#### Scenario: A late failure belongs to the test driver

- **WHEN** 有效分析和用例仍适用，但执行证据表明测试驱动使用了失效入口
- **THEN** Loop SHALL 回到测试资产责任阶段修正并复验驱动，保留既有分析、用例、证据和 Run ID，不重启整条测试链

### Requirement: Select the minimum sufficient test surfaces

Loop SHALL 根据风险、可观察结果、真实系统边界和项目测试框架约定选择测试方法。Agent SHALL NOT 为展示完整性强制运行 API、E2E、UI、Agent、单元或集成测试的全部组合。

纯接口行为 SHALL 使用适合的接口入口。跨页面或服务的用户旅程 SHALL 使用 E2E。视觉、交互、无障碍或任务可用性主张需要实际渲染和操作证据。局部模拟、组件检查和浏览器操作 SHALL 按实际边界报告，不得扩大为完整业务链证据。

框架专用 Skill SHALL 只在项目配置、当前权威来源或用户明确指令选择对应框架时加载。项目选择自有框架时，Loop SHALL 使用通用专项和项目入口；项目尚未选择且框架决定会改变资产或执行方式时，Loop SHALL 进入 Setup 确认，不得擅自安装、替换或选择框架。

#### Scenario: API-only service does not need a browser

- **WHEN** 目标是无页面产品的接口业务效果
- **THEN** Loop SHALL 使用接口和必要真实依赖取得证据，不安装或运行无关浏览器测试

#### Scenario: UI change requires rendered evidence

- **WHEN** 目标变化涉及布局、反馈、键盘操作或可访问性
- **THEN** Loop SHALL 实际查看并操作适用界面，记录视口、状态和证据，不以源码或 DOM 检查替代渲染结果

#### Scenario: Project uses its own agent evaluation framework

- **WHEN** 项目配置已经指定自有 Agent 评测框架
- **THEN** Loop SHALL 通过项目入口和通用 `agent-eval` 执行，不加载 DeepEval 或其他未选框架的专项 Skill

#### Scenario: Selected framework skill is unavailable

- **WHEN** 项目明确选择一个框架，但当前 Skill 包没有对应专项
- **THEN** Loop SHALL 沿用项目文档和通用测试能力，或报告具体能力缺口，不得静默安装依赖或改用其他框架

### Requirement: Let evidence control iteration and stopping

Loop SHALL 先执行最便宜且最能区分当前风险的检查。新证据只在改变范围、风险、模型、用例、执行路径或结论时触发下一轮；重复运行 MUST 有明确目的，不得用无界重试代替调查。

Loop SHALL 在满足退出条件、耗尽预算、到达人工检查点、遇到安全或授权边界、或剩余工作无法改变当前结论时停止。暂停、受阻和完成 SHALL 使用测试轮次契约的状态，并保留未完成项和恢复动作。

#### Scenario: Retry passes after an unexplained failure

- **WHEN** 首次执行失败而相同重试通过，但失败原因仍未知
- **THEN** Loop SHALL 保留两次结果和稳定性风险，选择调查或按预算停止，不把重试通过写成稳定通过

#### Scenario: Budget is exhausted

- **WHEN** 仍有低价值候选测试，但本轮时间或费用预算已经达到上限
- **THEN** Loop SHALL 停止新执行，完成现有原子步骤，并在报告中说明未覆盖范围和下一项高价值补证

### Requirement: Keep the loop testing-only

Loop SHALL 将被测产品代码视为只读。获得相应授权时，Loop 可以创建或修改测试代码、测试夹具、驱动、验证器和测试文档，并 SHALL 记录这些测试资产的变化和验证结果。

产品行为违反已确认规则时，Loop SHALL 保留复现证据、影响、可信度和交接目标，不得顺手修改产品实现。测试工具、夹具或验证器问题可以在测试资产范围内修正并复验；无法区分产品缺陷和测试资产问题时 SHALL 保留未知并调查。

#### Scenario: Product defect is reproduced

- **WHEN** 真实产品行为稳定违反已确认规则
- **THEN** Loop SHALL 记录产品缺陷证据并继续获准的相关测试，不修改产品代码

#### Scenario: Test driver is stale

- **WHEN** 产品行为符合规则，但测试驱动使用了失效入口
- **THEN** Loop 可以在授权范围内修正驱动并复验，记录验证器变化，不将该问题报告为产品缺陷

### Requirement: Finish with a bounded confidence report

Loop 结束时 SHALL 使用 `assessing-test-confidence` 汇总当前 Run ID 的直接证据、间接证据、矛盾证据、未知、残余风险和下一项选择。报告 SHALL 说明适用版本、环境、实际执行范围、未执行范围、测试资产变化和证据限制。

Loop 完成、工具退出码为零、用例通过率或报告生成成功 MUST NOT 单独支持“产品质量良好”“可以发布”或等价结论。发布和风险接受决定 SHALL 留给有权负责人。

#### Scenario: All executed checks pass but coverage is partial

- **WHEN** 已执行检查全部通过，但关键第三方链路因环境限制未运行
- **THEN** 报告 SHALL 说明已支持的主张和未证实链路，不把局部通过扩大为整体通过

#### Scenario: Loop stops at a human checkpoint

- **WHEN** 最终关键证据需要用户在受限后台完成操作
- **THEN** Loop SHALL 交付当前信心、人工检查点和恢复动作，轮次保持已暂停或受阻，不生成虚假的最终通过结论

### Requirement: Run a cold-start blind testing wave

完整 Test Loop 进入测试发现或执行阶段时，Loop SHALL 创建至少一个新的冷启动测试子代理。子代理 SHALL 使用独立会话，从当前项目和盲测任务包独立形成质量判断；MUST NOT 继承开发 Agent 的聊天上下文、实现理由、修复假设、开发自测结论、既有 Finding 结果、预期缺陷或评审 rubric。

盲测任务包 SHALL 只包含目标版本、用户可观察契约、项目规则与测试入口、环境与授权、分配的质量视角和不含结果的覆盖排除项。盲测结果封存后，Loop 才能使用实现 diff、开发记录和历史 Finding 做知情回归。盲测阶段与知情阶段 MUST NOT 复用同一子代理上下文。

知情回归 handoff SHALL 显式携带并核对原 Run ID、封存 wave ID、目标版本和封存证据哈希或指针。新的子代理会话 MUST NOT 创建新的 Run ID 或第二套 `run.md`；知情回归子代理 SHALL 只返回隔离输出，由单一合成者更新共享轮次。

#### Scenario: Development change enters a full test loop

- **WHEN** 一个开发 Agent 完成项目变更，用户要求运行完整 Test Loop
- **THEN** Loop SHALL 启动新的盲测子代理，且该子代理的输入不包含开发过程、实现 diff、开发自测结论或既有 Finding 结果

#### Scenario: Blind result is sealed before informed regression

- **WHEN** 盲测子代理完成独立发现并提交证据
- **THEN** Loop SHALL 先保存其原始结果和输入边界，再由另一个上下文使用 diff 和历史证据开展定向回归

#### Scenario: Informed regression starts in a new subagent session

- **WHEN** 封存盲测结果交给新的知情回归子代理
- **THEN** handoff SHALL 保持原 Run ID 并引用封存 wave 与证据；子代理 SHALL 只写隔离输出，不得创建新的 `run.md`

### Requirement: Keep blind testing inputs and outputs auditable

每个盲测 wave SHALL 记录 Run ID、wave ID、目标版本、质量视角、子代理会话或任务 ID、模型与宿主、稳定操作基线、允许读取的项目输入、明确未披露的开发材料、任务包哈希、输出路径和证据路径。

稳定操作基线 MAY 包含宿主固定规则、全局 RTK、全局／项目级 Skill、项目 `AGENTS.md`／`CLAUDE.md`、项目测试配置和获准 CLI；这些能力不因全局安装、自动注入或父级继承而构成开发上下文污染。子代理 SHALL 按任务需要使用这些能力。发现未预先列出的稳定操作基线时，Loop SHALL 补记其名称、来源和可取得的版本或哈希，并检查是否包含任务特定开发材料。

开发 Agent 的聊天上下文、实现理由、修复假设、实现 diff、开发自测结论、既有 Finding 结果、预期缺陷、评审 rubric，以及携带这些内容的会话记忆 MUST NOT 进入盲测会话。只有发现这类材料且无法剥离或审计时，该 wave 才 SHALL 视为无效或标记受阻。

子代理 SHALL 只写隔离输出，不得更新共享 `run.md`、权威测试资产、公共报告或产品代码。单一合成者 SHALL 核对实际调度、任务特定输入、Skill 加载、工具轨迹、文件变化和原始证据后，才更新共享轮次和结论。

#### Scenario: Test agent uses project and global capabilities

- **WHEN** 冷启动子代理读取全局 RTK、全局或项目级 Skill、项目规则及获准 CLI，且这些输入不包含本次开发叙事或既有结果
- **THEN** Loop SHALL 将它们记录为稳定操作基线并继续判读，不得仅因继承或未预先枚举而使 wave 无效

#### Scenario: Project rule contains development-specific results

- **WHEN** 项目规则、记忆或自动注入内容包含本次实现理由、diff、开发自测结论、既有 Finding 结果或 rubric
- **THEN** Loop SHALL 隔离该内容；无法隔离时该 wave SHALL 不计入盲测完成

#### Scenario: Blind workspace inherits parent repository rules

- **WHEN** 冷启动会话加载父目录或当前项目的 `AGENTS.md`、项目规则、全局 RTK、Skill 或 CLI
- **THEN** Loop SHALL 按内容判断并记录稳定操作基线；只有其中包含任务特定开发材料且无法隔离时，该 wave 才 SHALL 无效或受阻

#### Scenario: Subagent reports a defect without a run

- **WHEN** 子代理只描述潜在问题，但没有实际操作、命令、输出或产品状态证据
- **THEN** 合成者 SHALL 将其保留为待验证假设或丢弃，不得作为已证实 Finding 写入最终报告

#### Scenario: Parallel blind testers return results

- **WHEN** 高风险 Loop 分派多个独立测试子代理
- **THEN** 每个子代理 SHALL 使用隔离输出，只有单一合成者可以去重、复核并更新当前 Run ID 的共享资产

### Requirement: Prevent repetitive test waves

Loop SHALL 为已执行检查维护覆盖指纹，至少包含测试表面、身份／数据／初始状态、动作／路径、Oracle 和故障或质量视角。新的测试 wave SHALL 改变至少一个指纹维度，或声明修复回归、稳定性调查、环境恢复或新版本对照等明确复验目的。

完全相同且没有复验目的的执行 MUST NOT 重复。后续盲测子代理可以收到中性的覆盖排除项和分配视角，但 MUST NOT 收到上一轮结果、原因解释或推理正文。

#### Scenario: Loop proposes the same check again

- **WHEN** 新 wave 的覆盖指纹与已完成检查相同，且没有修复、稳定性、环境或版本复验目的
- **THEN** Loop SHALL 跳过该执行并选择新的风险切片，或在没有新增证据价值时停止

#### Scenario: Retry has a distinguishing purpose

- **WHEN** 首次失败后需要相同操作区分不稳定性或确认环境恢复
- **THEN** Loop SHALL 记录复验目的并保留两次证据，不把该重跑当作新的独立覆盖

### Requirement: Scale independent testers by risk

普通完整 Loop SHALL 至少使用一个盲测子代理。高影响、未知面大或发布关键的 Loop 在预算允许时 SHALL 按互不重叠的质量视角分派多个独立子代理；每个 brief SHALL 自包含并指定独立输出。子代理缺席或未返回有效证据 SHALL 形成覆盖缺口，不得计为通过。

#### Scenario: High-risk change has several independent concerns

- **WHEN** 变更同时涉及高影响业务、权限和异常恢复风险，且预算允许并行取证
- **THEN** Loop SHALL 将风险切成独立视角分派给多个子代理，而不是让一个 Agent 顺序重复同一验证

### Requirement: Block or disclose when blind subagents are unavailable

宿主不能创建新的子代理会话、不能排除开发会话或任务特定开发材料，或只能在同一上下文中模拟角色时，完整 Loop SHALL 在盲测门槛标记 `blocked`。无法导出完整系统基线，或子代理使用稳定的全局／项目规则、Skill 与 CLI，本身 MUST NOT 成为受阻理由。

只有用户明确接受降级后，Loop 才能继续同上下文测试，并 MUST 记录降级授权、原因和“独立盲测未完成”的残余风险。普通单层测试请求 SHALL 继续沿对应专项运行，不因完整 Loop 的子代理门槛受阻。

#### Scenario: Host has no subagent capability

- **WHEN** 用户要求完整 Test Loop，但当前宿主无法创建新的测试子代理，或无法排除开发会话与任务特定开发材料
- **THEN** Loop SHALL 停在盲测门槛并报告恢复条件，不得由同一 Agent 伪装为新的盲测代理

#### Scenario: Host exposes normal operational capabilities

- **WHEN** 新子代理会话自动获得宿主固定规则、全局／项目 Skill 和获准 CLI，但不继承开发会话或任务特定结果
- **THEN** Loop SHALL 正常执行盲测，并记录可观察到的操作基线，不得要求用户接受降级

#### Scenario: User explicitly accepts degraded testing

- **WHEN** 用户明确接受在没有独立子代理的情况下继续
- **THEN** Loop SHALL 记录降级并继续获准测试，但最终报告 MUST NOT 声称独立盲测已经完成

#### Scenario: User asks for one direct API check

- **WHEN** 用户只要求一次接口检查而不是完整 Test Loop
- **THEN** 请求 SHALL 继续直达接口测试专项，不强制创建盲测子代理

### Requirement: Gate full loops on project readiness

在创建或推进完整 Test Loop 前，Loop SHALL 读取项目规则和 `.test-privateer/project.md`，并核对完整 Loop 就绪契约中的资产位置、验证器入口、共享资源策略、质量责任、缺陷升级和风险接受边界。恢复旧 Run 时 SHALL 先只读核对原 Run ID、已有决定和证据，保留原轮次；尚未就绪时不得推进产品执行。

项目配置不存在、状态为 `not_configured`／`awaiting_user_confirmation`，或关键架构决定未关闭时，Loop SHALL 先进入最小 `setup-test-privateer` 确认流程；每轮只询问一个会改变架构或执行安全的决定。状态为 `blocked` 时，Loop SHALL 沿已确认的恢复入口报告阻塞，不重复询问已确认决定；只有权威来源变化或用户要求改变决定时才重进 Setup。Loop MUST NOT 把默认路径、推断、项目名或未回答的推荐当成项目决定。

配置声明 `ready` 只解除项目架构预检，不替代当前轮次契约、执行授权、环境验证或宿主子代理能力检查。配置与当前权威来源冲突时，Loop SHALL 停止使用冲突字段并进入 Setup 或当前任务澄清。

普通单层测试、单次执行或报告汇总 SHALL 继续直达对应专项，不因缺少完整 Loop 就绪配置而被阻塞。

#### Scenario: Full loop starts without a profile

- **WHEN** 用户要求完整 Test Loop，但项目没有 `.test-privateer/project.md`
- **THEN** Loop SHALL 先进入最小 Setup 确认 Loop 架构，不创建轮次或边执行边猜测资产与责任边界

#### Scenario: Profile is awaiting confirmation

- **WHEN** 项目配置记录完整 Loop 状态为 `awaiting_user_confirmation`
- **THEN** Loop SHALL 停在对应确认问题，不推进产品执行或盲测调度

#### Scenario: Deferred verifier blocks a full loop

- **WHEN** 项目配置为 `blocked` 且记录了已确认的验证器补建入口
- **THEN** Loop SHALL 报告该入口和受阻范围，不重复请求同一确认，不创建新 Run 或推进盲测

#### Scenario: Resume an older run without a profile

- **WHEN** 用户要求恢复已有 Run，但项目没有完整 Loop 就绪配置
- **THEN** Loop SHALL 只读核对原 Run ID、授权和证据，进入最小 Setup 补齐缺失架构；恢复后沿用原 Run ID，不重做已有效的检查

#### Scenario: Single API test has no profile

- **WHEN** 用户只要求编写并运行一条接口测试，项目没有完整 Loop 配置
- **THEN** Agent SHALL 直达接口测试专项，不强制先完成 Setup
