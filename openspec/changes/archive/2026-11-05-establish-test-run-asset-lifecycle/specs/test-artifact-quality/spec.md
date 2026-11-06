# Spec Delta

## ADDED Requirements

### Requirement: Preserve evidence identity and applicability

存在轮次资产时，测试证据 SHALL 能定位到对应 Run ID、测试或 Finding ID、目标版本或快照、环境、生成时间和实际来源。合法的单会话、单项短任务没有轮次资产时，证据 SHALL 记录“无 Run ID（单项短任务）”，并用测试或 Finding ID、目标版本或快照、环境、生成时间和实际来源保持身份。报告中的摘要 SHALL 指向原始证据或说明原始证据不可访问，MUST NOT 让摘要替代原始观察。

证据适用范围 SHALL 与实际执行条件一致。历史结果、不同环境结果或已过期证据可以作为背景，但 MUST NOT 冒充当前轮次的直接证据。

#### Scenario: Evidence belongs to one run and case

- **WHEN** 一个接口检查保存了请求、响应和业务状态观察
- **THEN** 证据 SHALL 标明 Run ID、关联 Case、目标版本、环境和时间，使后续报告可以定位其来源

#### Scenario: Short test has no run record

- **WHEN** 一个单会话、单项且方向不变的检查没有建立轮次资产
- **THEN** 证据 SHALL 记录“无 Run ID（单项短任务）”，并用测试 ID、目标版本、环境、时间和来源定位，不得为满足字段虚构 Run ID

#### Scenario: Old report remains on disk

- **WHEN** 本轮执行在生成新报告前失败，磁盘仍存在旧报告
- **THEN** Agent SHALL 依据本轮 Run ID 和执行轨迹报告受阻，不把旧报告作为本轮结果

### Requirement: Record evidence sensitivity and retention boundaries

Agent SHALL 沿用项目已确认的证据位置、访问规则和保留策略。没有项目约定时，Agent SHALL 记录实际保存位置、敏感性、可访问范围和已知失效条件，并避免把秘密值、真实凭据或不必要的客户数据写入测试资产。

临时链接、短期 CI Artifact 或本地文件 SHALL 标明其保留限制。清理测试实例、临时数据或运行目录前，Agent SHALL 先确认完成判定所需的证据已保存到清理后仍可访问的位置。无法持久保存时，最终报告 SHALL 明确可复核性限制。

#### Scenario: CI artifact will expire

- **WHEN** 原始视频和日志只保存在会自动过期的 CI Artifact
- **THEN** Agent SHALL 记录 Artifact 地址、保留期限和必要摘要，并在报告中说明过期后的复核限制

#### Scenario: Evidence contains credentials

- **WHEN** 请求、日志或截图包含令牌、密码或等价秘密值
- **THEN** Agent SHALL 脱敏或限制证据位置，不把秘密原文写入可共享测试文档

#### Scenario: Cleanup would remove evidence

- **WHEN** 测试实例的临时目录同时保存完成判定所需的日志
- **THEN** Agent SHALL 先转移并核对必要日志，再清理本次实例；无法转移时保留实例或报告证据保存受阻

### Requirement: Mark invalidated assets without rewriting history

规则、目标版本、接口合同、夹具、环境权限或验证器发生会改变判定的变化时，Agent SHALL 将相关当前资产标记为需要复核或已被替代，并记录触发变化和影响范围。有效资产可以保持当前有效。

失效处理 SHALL 保留历史执行记录及其当时适用条件。Agent MUST NOT 修改旧预期或旧结果，使历史运行看起来符合新规则。新资产取代旧资产时 SHALL 保留稳定引用或替代指针。

#### Scenario: Business rule changes after a successful run

- **WHEN** 新规则改变了既有 Case 的预期
- **THEN** Agent SHALL 将该 Case 标记为需要复核或创建替代定义，保留旧运行的原预期、结果和版本

#### Scenario: UI driver changes without product change

- **WHEN** 页面驱动或选择器变化导致旧 E2E 证据无法证明当前路径
- **THEN** Agent SHALL 标记验证资产需要复核，区分验证器漂移和产品行为变化，不删除旧证据
