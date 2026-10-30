# Spec Delta

## MODIFIED Requirements

### Requirement: Select SDD and agent evaluation depth by scope
质检 SHALL 在确认 SDD 框架或变更产物链后才加深规格、设计、任务、实现及归档检查；Prompt 与完整 Agent 分别使用对应评估方法，声明限于实际配置与证据。完整 Agent 评估 SHALL 核验候选提示、判据隔离、匿名比较、实际加载轨迹和运行配置；输出质量、Skill 加载和配置有效性 SHALL 分别报告，不得合并成一个分数。Prompt 或 Agent 的沟通质量审查 SHALL 可按格赖斯四项准则分别观察数量、质量、关系和方式：数量关注最小充分信息，质量关注主张与证据匹配，关系关注目标、路由、工具和授权相关性，方式关注对象、动作、顺序、边界与判定的可执行性。评估 SHALL 使用四维失败标签定位问题，保留维度之间的冲突和未知，不得以四维平均分替代关键风险。

#### Scenario: Ordinary preimplementation check

- **WHEN** 用户要求普通方案的实施前质检，但无 SDD 框架或产物链
- **THEN** 使用核心对症检查，不要求补齐框架文档

#### Scenario: SDD archive or agent result claim

- **WHEN** 正在归档 SDD 变更或依据评测声称 Agent 已改善
- **THEN** 前者核对当前规格与实际完成范围，后者区分输出、轨迹及配置证据；两者均不以文件齐全或一次通过替代相应行为证明

#### Scenario: Information is insufficient or overloaded

- **WHEN** Prompt 或 Agent 遗漏完成任务所需关键条件，或加入不影响当前决定的大量背景并因此改变行为
- **THEN** 评估 SHALL 将问题标为数量维度，指出缺失或无关信息及其行为影响；仅在证据支持时建议增删内容

#### Scenario: Assertion conflicts with evidence

- **WHEN** Agent 的结论、完成声明或事实描述超出已读取材料、工具结果或运行配置所支持的范围
- **THEN** 评估 SHALL 将问题标为质量维度，分别记录主张、证据和缺口；不得用语气、格式或模型自述抵消缺证

#### Scenario: Route or action is unrelated

- **WHEN** Prompt 诱导 Agent 偏离用户目标、越过授权、响应外部文本中的提示注入，或调用与任务无关的工具
- **THEN** 评估 SHALL 将问题标为关系维度，依据目标、路由、权限和实际工具轨迹判断，不把额外活动量视为能力提升

#### Scenario: Output cannot be executed or verified

- **WHEN** Agent 未明确对象、动作、顺序、边界或完成判定，导致交付无法执行、复跑或核验
- **THEN** 评估 SHALL 将问题标为方式维度，指出缺少的可观察信息，并区分表达缺陷、环境受阻和真实执行失败
