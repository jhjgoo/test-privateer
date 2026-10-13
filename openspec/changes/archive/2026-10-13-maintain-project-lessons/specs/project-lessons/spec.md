# Spec Delta

## Purpose

规定如何从真实失败与返工维护可追溯的项目错题本，再将证据支持且边界稳定的教训提炼为项目规则。区分历史观察、原因假设、当前规范与验证证据，控制规则膨胀并保持资料可以被后续 Agent 找到。

## ADDED Requirements

### Requirement: Preserve evidence and review coverage

教训维护 SHALL 读取已有项目约定与材料，记录实际审查范围、可定位证据、失败机制或未知、纠正动作与验证状态；未读取或未覆盖的区间不得宣称已审查。

#### Scenario: Partial history review
- **WHEN** 上次记录审查到 A，本轮只读取 C，B 的材料不可访问
- **THEN** 记录 C 已审查及 B 的缺口，连续审查标记保持在 A，不把 C 写成连续完成的新水位

#### Scenario: Unproven cause after a passing retry
- **WHEN** 重试通过但没有失败机制或原因验证证据
- **THEN** 保留观察、原因未知和取证动作，不把重试成功记成根因已修复

### Requirement: Count recurrence by independent evidence

维护 SHALL 按失败机制与适用范围归并教训，以可识别的独立事件或项目定义的不同审查日统计复发；同一事件的多个提交、重试、转述或重复审查不能机械增加发生次数。

#### Scenario: Three records of one incident
- **WHEN** 一个事故有两次补丁与三次审查引用
- **THEN** 合并证据并保留返工信息，按一个事件计数，不因三条记录自动晋升

#### Scenario: New recurrence after promotion
- **WHEN** 已晋升规则后发生同类错误
- **THEN** 更新原教训的证据并检查规则入口、表达和执行机制，不另写重复规范或声称既有规范已防止复发

### Requirement: Promote scoped and checkable rules

规则提炼 SHALL 依据当前项目、独立复发证据、稳定适用范围和能捕获原错误的检查动作；项目晋升标准优先，未定义时明确采用的候选标准。高后果单次事件可依据已确认约束成为规则，不需为满足计数等待事故重演。

#### Scenario: Vendor-specific observation
- **WHEN** 只有一个供应商的错误样本，邻近供应商行为正常
- **THEN** 保留供应商范围及正常边界，不把限制升级为全项目通用规则

#### Scenario: Mature lesson with conflicting standard
- **WHEN** 独立事件支持晋升，但已有规则规定相反行为
- **THEN** 先查适用条件与有效依据，能消解的按证据修正，需业务选择的保留为候选，不并列写入矛盾规则

### Requirement: Maintain one discoverable authority within scope

维护 SHALL 复用已有错题本与规则权威位置；没有特殊约定时，错题本默认使用项目根目录 LESSONS.md，长期规则直接写入根目录 AGENTS.md 并保留其他项目要求。晋升后留下证据和目标指针；已有独立规范时，Agent 入口用有触发条件的短指针连接相关资料。只审查时交付建议，已授权维护时完成可确定的文件修改；全局 Skill、外部 Issue、定时任务等不因调用而获得写入授权。

#### Scenario: Default rule location without project convention
- **WHEN** 用户授权提炼规则，项目没有特殊规则位置约定或既有独立规范
- **THEN** 在根目录 AGENTS.md 写入简短的条件、动作与检查方法，保留原项目指令，教训及详细证据留在 LESSONS.md，不另造规则文件

#### Scenario: Authorized local maintenance
- **WHEN** 用户要求整理错题本并提炼项目规则，且现有文件与证据足够
- **THEN** 更新对应文件和入口、去重与关联，报告实际修改及未决项，不在每个可逆编辑前要求批准

#### Scenario: Ordinary diagnosis without lesson request
- **WHEN** 用户仅要求解释当前失败或质检补丁
- **THEN** 沿用调查或质检入口，不强制创建错题本和项目规范
