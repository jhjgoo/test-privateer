# testing-workflow Specification

## Purpose
规定黑帆测试官如何沿当前任务选择测试活动、保持授权与阶段边界，并维护可追溯的测试资产。此规格抽取已合并的工作流约定，不要求独立任务建立完整项目档案，也不把测试设计当成产品执行。

## Requirements

### Requirement: Route by current task and authorized stage
主入口 SHALL 沿已确认任务、已有材料和信息缺口选择当前活动，分别交代完成、未完成、依据、下一动作及执行状态；专项直接调用只完成其当前请求。主入口 SHALL 先判断用户最终目标、交付物、成功信号和任务抽象层级是否足以选择工作路径；当缺口会改变工作方向时 SHALL 先使用 `shaping-ai-tasks`。目标明确但产品事实、业务规则、系统关系或 oracle 不清时 SHALL 继续使用 `clarifying-test-basis`，不得把任务升级重复成测试依据澄清。

#### Scenario: Independent analysis without product execution
- **WHEN** 用户只要求分析一份规则明确的材料
- **THEN** 直接完成有关分析，不强制建项目地图、不重复确认已知规则，也不执行产品测试或把分析写成已测试

#### Scenario: Project task requires context
- **WHEN** 已选择项目测试且系统关系不足以支持变化判断
- **THEN** 补齐唯一项目 TCO 所需上下文后推进相关分析，无关未知作为待办，不要求写完项目百科

#### Scenario: Vague testing request needs task shaping
- **WHEN** 用户只提出“测试一下”或“帮我看看有没有问题”，且不同最终结果会导致不同测试活动
- **THEN** 主入口 SHALL 先交给 `shaping-ai-tasks`，在任务契约确认或带边界推荐后再进入测试使命或其他专项

#### Scenario: Clear testing goal keeps the existing route
- **WHEN** 用户已明确测试对象、目的和交付物，只缺产品规则或 oracle
- **THEN** 主入口 SHALL 跳过任务升级并调用 `clarifying-test-basis`

### Requirement: Preserve uncertainty and causal evidence
澄清与调查 SHALL 区分规则未知、观察、缺陷、原因假设与已支持的解释，保留影响判断的未知及具体取证动作。

#### Scenario: Missing business rule
- **WHEN** 缺失的配置时点会改变预期结果
- **THEN** 给出具体问题、推荐及测试影响，继续不依赖答案的部分，不把未决选项写成既定预期

#### Scenario: Local guard explains only amplification
- **WHEN** 现有证据只能解释异常如何被放大，不能解释最初为何发生
- **THEN** 分开说明已解释与未解释部分，不以止损或修复后通过替代完整原因证据

### Requirement: Maintain one traceable test asset chain
测试资产 SHALL 保持需求、测试项、用例、风险及回归证据的可追溯关系；同一对象复用权威编号，当前规则与历史观察分开维护。

#### Scenario: Rule changes after an earlier successful run
- **WHEN** 已确认新规则，需要更新分析与用例
- **THEN** 同步有效规则、关联和安排，保留历史执行记录及其版本，不将旧通过升级为新规则已验证

#### Scenario: Partial design handoff
- **WHEN** 本轮只完成部分已识别测试内容
- **THEN** 交接保留未设计、阻塞或排除项及依据，不把局部用例完成称为整体测试完成
