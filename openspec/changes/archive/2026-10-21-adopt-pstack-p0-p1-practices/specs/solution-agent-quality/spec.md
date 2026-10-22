# Spec Delta

## MODIFIED Requirements

### Requirement: Select SDD and agent evaluation depth by scope
质检 SHALL 在确认 SDD 框架或变更产物链后才加深规格、设计、任务、实现及归档检查；Prompt 与完整 Agent 分别使用对应评估方法，声明限于实际配置与证据。完整 Agent 评估 SHALL 核验候选提示、判据隔离、匿名比较、实际加载轨迹和运行配置；输出质量、Skill 加载和配置有效性 SHALL 分别报告，不得合并成一个分数。

#### Scenario: Ordinary preimplementation check
- **WHEN** 用户要求普通方案的实施前质检，但无 SDD 框架或产物链
- **THEN** 使用核心对症检查，不要求补齐框架文档

#### Scenario: SDD archive or agent result claim
- **WHEN** 正在归档 SDD 变更或依据评测声称 Agent 已改善
- **THEN** 前者核对当前规格与实际完成范围，后者区分输出、轨迹及配置证据；两者均不以文件齐全或一次通过替代相应行为证明
