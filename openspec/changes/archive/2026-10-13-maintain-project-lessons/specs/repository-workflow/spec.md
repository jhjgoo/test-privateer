# Spec Delta

## ADDED Requirements

### Requirement: Maintain evidence-backed project lessons and rules

本仓库 SHALL 在根 LESSONS.md 维护真实错误、验证缺口与纠正经验，在 AGENTS.md 维护当前协作规则；修改前读取与任务相关的教训。条目区分直接观察与历史记录回填，保持可定位来源、独立事件口径、适用范围与真实状态；有限材料整理不得声明连续历史审查完成。

#### Scenario: Initialize project lessons from bounded evidence
- **WHEN** 用户授权建立本项目错题本与规则，仅有当前 change 和部分历史归档资料
- **THEN** 基于已读资料建立条目和规则指针，保留既有项目要求，标明历史未重跑和未覆盖范围，不虚构复发次数或自动防复发效果

#### Scenario: Consume and update related lessons
- **WHEN** 修改涉及已记录的共享规则、验证或完成声明问题
- **THEN** 读取相关教训并按 AGENTS.md 的动作与检查约束工作，出现新事件时更新原条目及执行机制，保留原始证据而非另造同义规范

## MODIFIED Requirements

### Requirement: Maintain one change chain for repository behavior

本仓库行为或流程变更 SHALL 在同一 OpenSpec change 中追溯意图、可观察要求、设计、任务与实际完成范围；实施与验证结束后保留活动 change，只有用户明确确认本次 change 已完成后才同步当前规格并归档。普通错字或失效链接修正可不新建 change。

#### Scenario: Resume implementation with failed evidence
- **WHEN** 继续已有变更时出现失败反证或未实现的原承诺
- **THEN** 更新原 change 的决定与剩余任务，不新建平行账本，不以缩小声明关闭原承诺

#### Scenario: Implementation verified without user confirmation
- **WHEN** 已完成授权范围并核对相应验证与限制，但用户尚未明确确认本次 change 已完成
- **THEN** 交付结果与剩余项，保留活动 change，不把测试通过、任务勾选或 Agent 总结当成用户确认，不同步当前规格或执行归档

#### Scenario: Completed change ready to archive
- **WHEN** 已完成授权范围、核对相应验证与限制，且用户明确确认本次 change 已完成
- **THEN** 记录简短验收结论，经严格校验将 delta 同步到当前规格后归档，不将原始运行日志作为 change 附件
