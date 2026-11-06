# Spec Delta

## Purpose

规定 Test Privateer 如何在一个有界授权内编排现有测试专项，连续完成分析、用例、执行、调查、回归和报告，并在证据、预算或安全边界要求时停止。

## ADDED Requirements

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
