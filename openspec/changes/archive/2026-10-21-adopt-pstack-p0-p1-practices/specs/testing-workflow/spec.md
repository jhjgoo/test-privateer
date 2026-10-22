# Spec Delta

## ADDED Requirements

### Requirement: Preserve auditable pause and resume state
当测试执行需要跨会话暂停、上下文可能降级或用户明确要求暂停时，Agent SHALL 交付冷启动恢复点。恢复点 SHALL 记录原始目标与授权、可判定退出条件、已完成及已验证事实、未验证结论、产物与原始证据路径、未完成项、阻塞、下一动作和恢复判据。

恢复时 Agent SHALL 先读取项目规则、权威测试资产、恢复点和最近产物，继承已完成工作；仅对仍影响当前判断的关键断言做抽查，SHALL NOT 重做已完成工作或把旧结论重新冒充本轮观察。恢复点缺失或相互冲突时，Agent SHALL 停在可定位边界并说明需要补证的范围。

#### Scenario: User pauses a session
- **WHEN** 用户要求暂停或即将跨会话恢复
- **THEN** Agent SHALL 在当前原子步骤边界停止并交付恢复点，不开启新的测试分支

#### Scenario: Session resumes
- **WHEN** 新会话继续一个已暂停的测试任务
- **THEN** Agent SHALL 先恢复目标和状态，继承权威轨迹，只推进剩余工作

#### Scenario: Resume evidence conflicts
- **WHEN** 恢复点、测试资产或项目规则描述不一致
- **THEN** Agent SHALL 停在冲突点并说明差异和最小补证动作，不选择性忽略冲突

## ADDED Requirements

### Requirement: Verify agent behavior from actual load traces
Agent 行为评测 SHALL 使用自然任务提示，不在候选可见的目录、文件名或提示中泄漏 `eval`、`test`、`judge`、`rubric`、`score`、`benchmark` 或其他会改变候选行为的评测意图。判据 SHALL 只提供给评审；版本比较 SHALL 使用匿名标签，评审 SHALL 在同一尺度下判读。

结论 SHALL 区分最终输出、实际读取的 Skill／文件、工具轨迹和运行配置；SHALL NOT 以候选自述替代加载轨迹，也 SHALL NOT 跨项目扫描私有会话记录。失败 SHALL 保留为可诊断结果，不得为汇总方便改成通过。

#### Scenario: Candidate sees an organic task
- **WHEN** 评测候选收到任务提示
- **THEN** 提示、目录和文件名 SHALL 表现自然任务语境，不提示这是评测或比较

#### Scenario: Skill load is claimed
- **WHEN** 候选自称读取了某 Skill 或参考
- **THEN** SHALL 以当前授权内轨迹或可观察文件访问证据核验；无证据时按未确认加载处理

#### Scenario: Judge compares variants
- **WHEN** 评审比较多个版本输出
- **THEN** SHALL 只见匿名标签并使用同一判据；候选身份不进入评审上下文
