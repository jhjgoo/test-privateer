## ADDED Requirements

本 delta 对应已实施的表达契约。验收依据是本次 A/B、定向复测与人工反馈，不是每次生成均遵循、跨宿主稳定或真实产品执行的保证；安装及发布状态另行确认。

### Requirement: Make human-facing testing communication proportional to the decision

Agent SHALL 围绕读者当前任务突出重点，并使用具体、易懂且一致的用语，写清必要的对象、条件、动作与结果。测试澄清、分析、用例和报告可以按复杂度选择篇幅与版式，但精简 MUST 保留判定信息、真实符号、来源和不确定性。不得统一规定字数或段数。

#### Scenario: A small clarification with a real business choice

- **WHEN** 一个业务选择会改变预期，且问题与依据足以用短段落说明
- **THEN** 完整展示问题、有证据支持的推荐及理由，以及答案对测试的影响
- **AND** 不强制标签或分隔线，不将未作答视为同意

#### Scenario: A report is handed to the next reader

- **WHEN** 读者需要根据报告判断本轮结果或安排后续工作
- **THEN** 让本轮重点、结论及限制容易找到，下一步指向有依据的具体对象和动作
- **AND** 必要技术术语保持准确，需要时就近解释，不用内部结构名替代业务目的

#### Scenario: Concision would change a rule

- **WHEN** 待改写材料包含影响判定的信息
- **THEN** 保留否定、且／或关系、阈值与单位、状态与时序、字段所属对象及例外
- **AND** 规则不明确时保留未知，不补造阈值、操作或观察入口、业务译名或实际观察
- **AND** 不改变原要求的强制程度

#### Scenario: A sentence combines several operations

- **WHEN** 测试文档的操作或说明把多项信息挤在一个长句中，读者需要自行拆解才能执行或核对
- **THEN** 拆开操作与判断，优先用主动语态明确执行主体，保持名称一致
- **AND** 结论与理由分句；证据、缺口或限制需要逐项核对时列成清单，已简短的内容不强拆
- **AND** 条件紧邻对应动作，拆句不丢失判据或例外，也不把每个动作另建任务
- **AND** 句长建议不作为硬性字数门槛；主体未知时不编造负责人

#### Scenario: Technical detail is needed for the selected test level

- **WHEN** 所选测试层级依赖精确技术信息
- **THEN** 保留执行和判定所需的请求字段、响应码、单元测试符号或诊断信息
- **AND** 只精简无关解释，不仅因出现技术名词就判为阅读缺陷

#### Scenario: Existing output is already sufficient

- **WHEN** 简短输出已准确回答当前问题，且没有影响后续工作的隐藏缺口
- **THEN** 不为套模板增加多余背景、重复摘要、虚构待办或完整审查流程

### Requirement: Choose representations for the relationship being explained

Agent SHALL 根据待解释的关系选择最小有效表示。文字已经清楚时，不强制生成图或 HTML。概览与详情 MUST 使用同一来源、编号和预期，不得为简化展示遗漏已识别范围。

#### Scenario: Complex scope does not require a second overview

- **WHEN** 分组和表格已清楚表达测试范围
- **THEN** 不仅因范围复杂而再画重复脑图
- **AND** 保留全部已识别测试点及其安排

#### Scenario: A long report needs navigable sections

- **WHEN** 报告或其他测试交付包含多个主题，需要扫描章节或通过目录定位
- **THEN** 使用与内容从属关系一致的语义标题；独立 Markdown 文档区分文档标题、主要章节及必要的子章节
- **AND** 在对话中交付完整分析、用例或报告时同样保留标题层级
- **AND** 局部加粗突出影响判断或操作的重点，如当前结论、关键预期或停止条件；不整段加粗，不代替章节标题
- **AND** 标题名称和章节数量按内容确定，长说明不因使用表格而压进单元格
- **AND** 短答复不为套用层级增加空章节

#### Scenario: Ordering and exceptions matter

- **WHEN** 时序或状态分支会改变预期，且线性文字不易解释这些关系
- **THEN** 选择能清楚表达顺序和分支的列表、表格或图，不强制某一种图形
- **AND** 保留精确规则与例外，不在图中另建一套预期

#### Scenario: One complete case does not need a duplicate index

- **WHEN** 单条用例的详情已能清楚展示操作、预期及准备条件
- **THEN** 可以直接交付详情，不强制添加重复索引
- **AND** 保留编号、来源和独立执行信息；批量交付仍能找到各项安排

### Requirement: Preserve document purpose when applying shared writing guidance

Agent SHALL 按读者需要完成的理解、决策、执行或验收任务应用共享写作方法，不仅按文件名选择模板。精简 MUST 保留专项交付要求和执行关键上下文；不得以短句、少字或固定版式替代内容完整性。

#### Scenario: An execution plan is made easier to read

- **WHEN** 精简测试相关 tasks、测试计划或操作交接
- **THEN** 保留必要前置条件、依赖、改动或操作对象、关键步骤、验证方法、完成条件与失败处理
- **AND** 围绕可验收结果组织任务，不把每个动作机械拆成独立任务
- **AND** 执行关键条件放在任务附近，共享背景可以引用权威定义
- **AND** 不把互斥结果写成必须依次执行的步骤

#### Scenario: A document supports more than one reader task

- **WHEN** 同一文档同时用于决策和执行，或交接给人和 Agent
- **THEN** 保留各用途所需的信息，不因套用单一短句模板删除依据或执行细节
- **AND** 同样的方法适用于非 OpenSpec 的测试交付，不依赖特定文件名

#### Scenario: Necessary execution information is not in the source

- **WHEN** 来源缺少验证命令、前置依赖、判据或失败处理依据
- **THEN** 标出实际缺口及其影响，不编造项目事实
- **AND** 区分已确认安排与待确认建议，不把文案改写声称为执行或验收完成
