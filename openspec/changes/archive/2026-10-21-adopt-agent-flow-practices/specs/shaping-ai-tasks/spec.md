# Spec Delta

## MODIFIED Requirements

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
