# Spec Delta

## Purpose

规定已形成的解决方案、Prompt 与完整 Agent 的质检边界：沿原问题、作用点、行为及证据检查真实缺口，识别样例耦合和不当完成声明。框架专属检查按产物关系启用，不将普通分析升级成审批。

## ADDED Requirements

### Requirement: Check the solution against its actual causal target
方案质检 SHALL 沿问题、依据、作用点、预期行为及验证证据检查样例耦合、共享路径遗漏和范围夸大；合法业务常量与有边界的止损不因外形而被误报。

#### Scenario: Sample-specific fix with no shared basis
- **WHEN** 补丁只识别当前样例字符串，而需求约束同类路径
- **THEN** 指出断开的依据与作用点，提出有区分力的最小探查，不把该样例通过当作共同问题解决

#### Scenario: Legitimate local rule
- **WHEN** 有效规则明确要求局部常量或分支
- **THEN** 按其依据和范围质检，不仅因存在常量就报告硬编码问题

### Requirement: Preserve the original completion boundary
勾选任务或宣称完成前 SHALL 按原请求与有效需求核对执行链、断言及未实现项；排除原承诺须有既有获准依据，执行者自行限缩或披露局限不构成排除授权。

#### Scenario: Status interface without the promised action
- **WHEN** 原任务要求实际执行某动作，但交付只新增状态、分类或提示且子项测试全绿
- **THEN** 保留原行为未完成，单列已完成子项及缺口，不关闭原任务

#### Scenario: Explicitly authorized phase
- **WHEN** 用户已明确本阶段只交付接口，后续执行属于获准的下一阶段
- **THEN** 按本阶段承诺验收，同时保留后续安排，不强迫本轮补齐全部能力

### Requirement: Select SDD and agent evaluation depth by scope
质检 SHALL 在确认 SDD 框架或变更产物链后才加深规格、设计、任务、实现及归档检查；Prompt 与完整 Agent 分别使用对应评估方法，声明限于实际配置与证据。

#### Scenario: Ordinary preimplementation check
- **WHEN** 用户要求普通方案的实施前质检，但无 SDD 框架或产物链
- **THEN** 使用核心对症检查，不要求补齐框架文档

#### Scenario: SDD archive or agent result claim
- **WHEN** 正在归档 SDD 变更或依据评测声称 Agent 已改善
- **THEN** 前者核对当前规格与实际完成范围，后者区分输出、轨迹及配置证据；两者均不以文件齐全或一次通过替代相应行为证明
