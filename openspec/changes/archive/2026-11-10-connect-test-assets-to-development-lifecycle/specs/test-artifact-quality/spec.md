## MODIFIED Requirements

### Requirement: Make human-facing testing communication proportional to the decision

Agent SHALL 围绕读者当前任务突出重点，并使用具体、易懂且一致的用语，写清必要的对象、条件、动作与结果。测试澄清、分析、用例和报告可以按复杂度选择篇幅与版式，但精简 MUST 保留判定信息、真实符号、来源和不确定性。不得统一规定字数或段数。包括直接 Setup 在内的确认 SHALL 使用共享表达，说明决定对象、作答所需事实、推荐及关键后果；选项 SHALL 回答同一个问题。可调查的技术事实 SHALL 由 Agent 查明，MUST NOT 让用户提供未知脚本或以内部状态码代替解释。

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

#### Scenario: Timing and implementation are mixed

- **WHEN** 未来交付需要某项验证，但是否纳入当前阶段尚未决定，且尚无测试入口
- **THEN** Agent SHALL 说明验证的实际目的、当前已知边界和各时点的影响，围绕当前范围询问；不得用“推迟或指定入口”混合时间与技术方式，也不得因尚无入口自动判为不适用

#### Scenario: User already chose the scope

- **WHEN** 项目来源或用户已经明确该验证本阶段不开展，并给出恢复条件
- **THEN** Agent SHALL 沿用决定，不重复询问，不强制扩写为完整决策模板

#### Scenario: Final confirmation follows a long configuration report

- **WHEN** 调查或草稿已较长，但最终仍有实质范围或时点决定
- **THEN** 最终问题 SHALL 保留业务目的、已知边界、同维选项及影响，不能回退为内部状态码或要求用户提供未知技术入口

## ADDED Requirements

### Requirement: Keep volatile progress in its authoritative record

项目配置 SHALL 保存测试方式、治理、入口及适用证据指针；TCO SHALL 保存项目关系、覆盖与长期风险。任务勾选数、单轮步骤和局部待办 SHALL 留在原任务／Run／报告，MUST NOT 复制为长期配置或 TCO 中需要平行同步的当前进度。项目级结论 SHALL 保留来源、适用范围与版本，历史证据 SHALL 保持原始语义。

#### Scenario: A local task progresses after setup

- **WHEN** 一个 change 的任务从部分完成推进为全部完成
- **THEN** 维护者 SHALL 在原账本记录进度，只在新证据改变项目覆盖或长期风险时更新相关 TCO 节点；不向配置和 TCO 同步任务数量，不把任务完成当作用户验收
