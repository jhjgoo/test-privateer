## ADDED Requirements

### Requirement: Filter lesson candidates by future action value
错题本候选 SHALL 先判断未来同类任务是否仍成立、是否会改变后续 Agent 或人的行动、以及是否不是一次性偏好、偶发环境或已修复单例；三者不同时成立时 SHALL NOT 晋升为规则。

#### Scenario: One-off incident is not promoted
- **WHEN** 一条候选教训只对已修复的一次性环境状态有效
- **THEN** 保留为事件记录、待查证据或不收录，不晋升为项目规则
