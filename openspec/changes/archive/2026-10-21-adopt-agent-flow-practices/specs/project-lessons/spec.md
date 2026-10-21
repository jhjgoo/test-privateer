# Spec Delta

## MODIFIED Requirements

### Requirement: Promote scoped and checkable rules

规则提炼 SHALL 依据当前项目、独立复发证据、稳定适用范围和能捕获原错误的检查动作；项目晋升标准优先，未定义时明确采用的候选标准。高后果单次事件可依据已确认约束成为规则，不需为满足计数等待事故重演。教训 SHALL 优先导向可执行的环境改进：机械错误 SHALL 优先映射到检查器、钩子、CI 或测试；判断问题 SHALL 进入规则或标准；导航与信息缺口 SHALL 进入入口指针或取证动作。无法自动检查的规则 SHALL 保留人工检查方式与适用边界。

#### Scenario: Vendor-specific observation

- **WHEN** 只有一个供应商的错误样本，邻近供应商行为正常
- **THEN** 保留供应商范围及正常边界，不把限制升级为全项目通用规则

#### Scenario: Mature lesson with conflicting standard

- **WHEN** 独立事件支持晋升，但已有规则规定相反行为
- **THEN** 先查适用条件与有效依据，能消解的按证据修正，需业务选择的保留为候选，不并列写入矛盾规则

#### Scenario: Mechanical mistake can become a check

- **WHEN** 返工由可在命令输出或文件结构中确定的错误触发
- **THEN** 维护 SHALL 提出或落地最小确定性检查，并把该检查的运行方式与适用范围写入教训或规则；仅追加提醒不视为完整纠正

#### Scenario: Environment finding lacks authorization

- **WHEN** 复盘发现应修改 CI、钩子或全局配置，但本轮只授权整理文档
- **THEN** 维护 SHALL 交付具体修改建议、预期检查效果和未实施状态，不越权改配置
