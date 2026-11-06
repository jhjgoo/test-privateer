# Spec Delta

## ADDED Requirements

### Requirement: Maintain one authoritative test run record when coordination requires it

当测试跨多个阶段或会话、包含并行执行、需要暂停恢复，或用户明确要求审计时，Agent SHALL 建立一个稳定 Run ID 和唯一轮次记录。轮次记录 SHALL 保存测试对象与版本、触发来源、范围、授权、禁止动作、预算、退出条件、当前阶段、轮次状态、资产指针、阻塞和下一动作。

轮次记录 SHALL 只索引 TCO、需求分析、测试依据、用例、原始证据和报告。各资产的正文与状态仍由原权威位置维护。单会话、单项测试且方向不变时，Agent SHALL NOT 强制创建轮次记录。

#### Scenario: Multi-stage test creates one run record

- **WHEN** 用户要求从变化分析连续推进到用例、执行和报告
- **THEN** Agent SHALL 创建一个 Run ID，并让后续阶段更新同一轮次记录中的阶段、状态和资产指针

#### Scenario: Short execution stays lightweight

- **WHEN** 用户只要求执行一个明确测试，且任务不会跨会话或改变测试方向
- **THEN** Agent SHALL 使用现有用例与执行记录，不为满足格式创建独立轮次资产

#### Scenario: Resumed work uses the existing run

- **WHEN** 一个已暂停或受阻的测试轮次在新会话继续
- **THEN** Agent SHALL 先恢复原 Run ID、授权、退出条件和资产指针，再推进剩余工作

### Requirement: Separate run state from test verdict and confidence

轮次记录 SHALL 将流程状态维护为准备中、可执行、执行中、已暂停、受阻、已完成或已取消。单项测试的通过、失败、跳过、受阻和待判定 SHALL 留在执行记录；综合信心 SHALL 留在测试信心报告。

轮次“已完成”只表示已到达退出条件并完成交付，MUST NOT 表示所有测试通过、风险消失或负责人批准发布。轮次“受阻” SHALL 保留已取得的有效证据和未证实范围。

#### Scenario: Completed run contains failed tests

- **WHEN** 所有计划内检查均已取得结果，但其中存在符合证据的失败
- **THEN** 轮次可以标记为已完成，同时执行记录保留失败，信心报告说明影响和残余风险

#### Scenario: Blocked run has partial evidence

- **WHEN** 一部分测试已经执行，但后续步骤因凭据或环境缺失而无法继续
- **THEN** 轮次 SHALL 标记为受阻，并保留已执行证据、阻塞原因和恢复动作，不将整轮写成未开始或通过

### Requirement: Use one synthesizer for authoritative run assets

当多个 Agent 或执行分支参与同一轮测试时，调用方 SHALL 指定一个合成者维护轮次记录和共享测试资产。执行分支 SHALL 返回自己的范围、Run ID、测试 ID、原始证据和状态，MUST NOT 并发改写同一权威文件。

共享账号、数据、端口或会话无法隔离时，Agent SHALL 串行执行相关分支，或停在明确阻塞边界。并行数量 SHALL NOT 以牺牲证据身份或环境隔离为代价。

#### Scenario: Parallel API and UI checks return to one writer

- **WHEN** API 和 UI 检查可以使用隔离数据并行执行
- **THEN** 两个分支 SHALL 分别保留证据并交回同一合成者，由合成者更新轮次记录和综合结论

#### Scenario: Shared account cannot be isolated

- **WHEN** 两个执行分支会修改同一账号的共享状态
- **THEN** Agent SHALL 改为串行执行或报告受阻，不让两个分支并发写入后再猜测结果归属

### Requirement: Preserve completed run history

已暂停或受阻的轮次可以沿用原 Run ID 恢复。已完成或已取消的轮次 SHALL 保持历史身份；后续发生新的产品执行时 SHALL 创建新的 Run ID，并引用先前轮次，而不是把旧轮次改回执行中。

Agent 可以向历史轮次追加文字纠正或失效说明，但 SHALL NOT 改写原始执行记录、原目标版本或当时证据。新版本、新规则或新环境下的结果 MUST NOT 追加为旧轮次的当前执行。

#### Scenario: New version starts a new run

- **WHEN** 已完成轮次后目标产品版本发生变化，用户要求重新验证
- **THEN** Agent SHALL 创建新的 Run ID，并将旧轮次作为历史依据引用

#### Scenario: Historical interpretation is corrected

- **WHEN** 新证据显示旧轮次的一项解释不成立，但没有重新执行产品测试
- **THEN** Agent SHALL 追加纠正和证据指针，保留旧观察和旧轮次状态，不声称发生了新的测试执行
