# shaping-ai-tasks Specification

## Purpose
在进入具体专项 Skill 前，把用户模糊、局部或低层级的请求转换为目标明确、方法适当、边界清楚且可验证的 AI 工作任务。

## Requirements

### Requirement: Upgrade only when the request can change the work direction

`shaping-ai-tasks` SHALL 仅在用户最终目标、交付物、成功信号、任务抽象层级或验证方式的缺口会改变工作方向时介入；目标和交付物已经足够明确时 SHALL 直接放行到合适专项。

#### Scenario: Vague action with multiple possible outcomes

- **WHEN** 用户只说“帮我测试一下这个功能”，且没有说明要支持的决定或成功标准
- **THEN** Skill SHALL 区分表面动作与可能的最终结果，提出一个最高价值的澄清点或给出带边界的推荐，并说明答案会改变的后续工作

#### Scenario: Explicit implementation request

- **WHEN** 用户已指定对象、行为、交付物、命令或执行边界
- **THEN** Skill SHALL 不重复进行完整任务升级，直接交回对应专项或执行路径，并只补充会阻塞该路径的缺口

### Requirement: Produce an executable task contract

Skill SHALL 交付或确认包含最终目标、交付物、使用者或决策、原始材料、专业方法、工具与权限、成功信号、外部验证、边界与未决项的任务契约；未知 SHALL 保持未知，不得伪造业务规则或执行结果。Skill SHALL 区分事实与决策：事实问题 SHALL 先在可用授权内调查；业务决策 SHALL 交给有权用户，并同时给出选项、推荐、理由、影响和等待点。

#### Scenario: User does not know how to ask

- **WHEN** 用户明确表示不知道如何提问或只能描述一个症状
- **THEN** Skill SHALL 将症状转换为候选最终目标和最小下一步，标明假设、需要的材料和可验证结果，不要求用户先写出专业术语

#### Scenario: Missing evidence source

- **WHEN** 任务结论需要原始数据、代码、环境或独立判定，但当前请求只提供了摘要
- **THEN** Skill SHALL 指出原始材料和验证缺口，并将其转化为调查、实验或后续取证动作

#### Scenario: Fact can be investigated

- **WHEN** 目标或材料中的未知可以通过仓库、文档、代码、日志或已有配置查清
- **THEN** Skill SHALL 先执行授权内调查并记录来源，不把该事实作为用户问题

#### Scenario: Business decision changes direction

- **WHEN** 交付物用途或成功标准存在多个合理业务选项
- **THEN** Skill SHALL 提出完整问题、推荐、理由和影响，并等待用户选择；不得把推荐写成已确认目标

### Requirement: Increase ambition through methods rather than wording

Skill SHALL 检查任务的高度、深度、范围和验证；涉及专家能力时 SHALL 要求具体原始材料、方法、工具或独立验证，不能以角色扮演、词汇变化或更长回答代替专家工作。

#### Scenario: Surface artifact hides a decision

- **WHEN** 用户请求制作报告、用例、Prompt 或方案，但结果实际用于业务判断或风险控制
- **THEN** Skill SHALL 将表面产物改写为需要支持的动作或决定，并保留该产物作为交付形式

#### Scenario: Cross-disciplinary method may change the result

- **WHEN** 任务的最终结果可能需要测试之外的产品、数据、用户研究、安全、运营或其他领域方法
- **THEN** Skill SHALL 识别相关领域和具体动作，只有在能改变范围、方法、风险或验证时才推荐引入

### Requirement: Route without taking over downstream responsibilities

Skill SHALL 根据任务契约选择下一专项，并区分任务升级、测试使命、测试依据澄清、方案质检和实际执行；不得把任务契约、方法建议或方案草案冒充实际测试结果。

#### Scenario: Clear goal but unclear testing oracle

- **WHEN** 用户目标和交付物已明确，但产品规则、系统边界或判断依据不清
- **THEN** Skill SHALL 跳过任务升级，交回 `clarifying-test-basis`，并保留当前已知目标与受影响的未知

### Requirement: Define a checkable exit condition before long or comparative work
当任务会连续执行、批量维护资产、比较版本、运行行为评测或跨阶段推进时，`shaping-ai-tasks` SHALL 在进入执行前建立可判定退出条件。退出条件 SHALL 描述可观察对象、判定方式、复跑或核验位置、停止／失败边界和必要的截止条件；SHALL 区分目标完成、环境受阻、案例无效和放弃推进。

执行中新证据或用户决策 SHALL 只能显式修改退出条件并记录原因；Agent SHALL NOT 为宣称完成而临时放宽原条件，也不 SHALL 把活动量、输出长度或阶段自述当作完成证据。

#### Scenario: Continuous test execution
- **WHEN** 用户要求持续执行测试直到达到某目标但未说明何时停止
- **THEN** Skill SHALL 先给出可观察退出条件、失败边界和记录位置，再进入执行路径

#### Scenario: Version comparison
- **WHEN** 任务会比较 Prompt、Skill、模型或工具版本
- **THEN** Skill SHALL 先固定比较对象、任务、指标、失败判定和结果状态，再启动候选运行

#### Scenario: Exit condition changes
- **WHEN** 执行中发现原退出条件测错对象或用户改变目标
- **THEN** SHALL 显式记录新旧条件、修改原因和已产生结果的适用范围；不得静默放宽原条件
