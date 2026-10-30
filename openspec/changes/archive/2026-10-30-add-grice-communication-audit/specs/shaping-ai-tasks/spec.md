# Spec Delta

## MODIFIED Requirements

### Requirement: Produce an executable task contract
Skill SHALL 交付或确认包含最终目标、交付物、使用者或决策、原始材料、专业方法、工具与权限、成功信号、外部验证、边界与未决项的任务契约；未知 SHALL 保持未知，不得伪造业务规则或执行结果。Skill SHALL 区分事实与决策：事实问题 SHALL 先在可用授权内调查；业务决策 SHALL 交给有权用户，并同时给出选项、推荐、理由、影响和等待点。任务契约形成后，Skill SHALL 做一次轻量沟通质量自校：数量检查信息是否足以完成当前任务且没有无关堆积，质量检查主张是否与证据或明确未知匹配，关系检查内容是否服务当前目标和授权路由，方式检查下一步是否具体、可执行、可观察和可核验。四项检查 SHALL 作为诊断维度使用，不得合并成单一分数，也不得把“更短”当作数量检查的唯一目标。

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

#### Scenario: User asks with just enough context

- **WHEN** 用户给出对象、目标、交付物、关键约束和验证方式，且附带背景都能影响当前决定
- **THEN** Skill SHALL 保留这些必要信息，直接形成或确认任务契约，不为了追求简短删除判定条件，也不追加无关问题

#### Scenario: Attractive but irrelevant background

- **WHEN** 用户提供一段与当前交付无关、但可能诱导模型扩展范围的背景
- **THEN** Skill SHALL 标明其与当前目标无关或暂不使用，保持当前授权和交付边界，不把无关背景升级成额外工作

#### Scenario: Claim lacks evidence

- **WHEN** 用户要求基于摘要得出因果、质量或执行结论，而原始材料或独立验证尚未提供
- **THEN** Skill SHALL 将主张标为未知或待证，给出能区分主要假设的最小取证动作，不以专业语气或完整模板掩盖证据缺口

#### Scenario: Next action is ambiguous

- **WHEN** 任务目标已明确，但下一步的对象、动作、观察或完成判定仍可能有多种解释
- **THEN** Skill SHALL 补充会改变执行的最小具体信息，或把任务交回合适专项并指出其可观察交接条件，不输出无法执行或无法核验的泛化建议
