# Spec Delta

## ADDED Requirements

### Requirement: Preserve human-in-the-loop checkpoints
当测试推进依赖只有人能完成的步骤时，Agent SHALL 建立或恢复可交接的人工检查点。检查点 SHALL 包含负责人、目标、操作入口、前置状态、操作、成功观察、失败证据、回填位置和恢复下一动作；需要时 SHALL 写明超时或放弃条件。检查点状态 SHALL 区分待确认、待执行、执行中、已完成、失败和取消。

人工返回的截图、值、错误或结论 SHALL 作为该负责人提供的原始观察记录，注明回填人和时间；不得写成 Agent 亲自执行。结果未回填前，Agent SHALL 不推进依赖该步骤的测试结论；新会话或阶段交接后 SHALL 先恢复未完成检查点状态。

#### Scenario: Agent lacks environment access
- **WHEN** 测试已获授权但目标环境只能由用户访问
- **THEN** Agent SHALL 生成包含目标、入口、操作、观察值、失败保留证据和回填位置的检查点，并停在该检查点；不把指导步骤写成已执行

#### Scenario: Human result is returned
- **WHEN** 用户回填截图、接口值或操作结论
- **THEN** SHALL 记录回填人、时间、原始证据和适用范围，再更新测试记录与下一步；不把口述概括改写为 Agent 观察

#### Scenario: Checkpoint resumes in a new session
- **WHEN** 新会话继续包含未完成人工检查点的测试
- **THEN** SHALL 先恢复检查点状态和依赖关系；未回填结果不推进后续测试结论，失败或取消保留原因和剩余动作

#### Scenario: Short request does not need a checkpoint artifact
- **WHEN** 用户只需一句操作指导，且该步骤不阻塞当前测试链
- **THEN** 直接说明操作和观察方式，不强制生成检查点模板或状态表
