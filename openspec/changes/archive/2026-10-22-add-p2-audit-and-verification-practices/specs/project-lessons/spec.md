# Spec Delta

## MODIFIED Requirements

### Requirement: Promote scoped and checkable rules
规则提炼 SHALL 依据当前项目、独立复发证据、稳定适用范围和能捕获原错误的检查动作；项目晋升标准优先，未定义时明确采用的候选标准。高后果单次事件可依据已确认约束成为规则，不需为满足计数等待事故重演。

候选晋升 SHALL 先判断五个条件：独立复发证据、错误可由命令输出或文件结构观察、误报范围可接受、存在权威目标位置、能接入既有测试／脚本／CI／入口检查体系。机械错误满足条件时 SHALL 优先落地最小确定性检查、契约测试、frontmatter／引用检查或检查脚本，而不是继续追加提醒文本；无法自动检查的判断问题 SHALL 进入规则或标准，并写明人工检查方式。导航与信息缺口 SHALL 进入入口指针或取证动作。

结构化检查 SHALL 记录运行方式、适用范围和验证结果；尚未获准或无法落地时保留建议与未实施状态。不得为容纳教训新建无人运行的孤立规则或检查资产。

#### Scenario: Vendor-specific observation

- **WHEN** 只有一个供应商的错误样本，邻近供应商行为正常
- **THEN** 保留供应商范围及正常边界，不把限制升级为全项目通用规则

#### Scenario: Mature lesson with conflicting standard

- **WHEN** 独立事件支持晋升，但已有规则规定相反行为
- **THEN** 先查适用条件与有效依据，能消解的按证据修正，需业务选择的保留为候选，不并列写入矛盾规则

#### Scenario: Mechanical mistake can become a check

- **WHEN** 返工由可在命令输出或文件结构中确定的错误触发，且五个晋升条件均满足
- **THEN** 维护 SHALL 提出或落地最小确定性检查，接入既有检查体系，并把运行方式、适用范围与验证结果写入教训或规则；仅追加提醒不视为完整纠正

#### Scenario: Judgment mistake cannot be fully automated

- **WHEN** 失败源于取舍或证据判断，无法由确定性输出观察
- **THEN** 保留为条件化规则或标准，写明人工检查动作、反例和边界，不伪装成机械检查

#### Scenario: Environment finding lacks authorization

- **WHEN** 复盘发现应修改 CI、钩子或全局配置，但本轮只授权整理文档
- **THEN** 维护 SHALL 交付具体修改建议、预期检查效果和未实施状态，不越权改配置
