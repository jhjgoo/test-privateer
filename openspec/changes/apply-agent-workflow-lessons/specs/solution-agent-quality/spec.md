## ADDED Requirements

### Requirement: Investigate repeated special cases before adding branches
方案质检发现同一判断边界或断言反复出现特判、旁路或格式适配时 SHALL 先检查测试范围、数据模型或 oracle 是否错位；缺少明确差异化规则依据时 MUST NOT 继续堆叠特殊分支。

#### Scenario: Repeated format adapters reveal a boundary error
- **WHEN** 多个调用点分别携带相似的格式特判而目标规则并未要求差异
- **THEN** 质检 SHALL 将共同边界或模型错位列为断点，并要求最小修正而非继续复制特判
