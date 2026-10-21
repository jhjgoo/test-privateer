# testing-workflow Specification

## Purpose
规定黑帆测试官如何沿当前任务选择测试活动、保持授权与阶段边界，并维护可追溯的测试资产。此规格抽取已合并的工作流约定，不要求独立任务建立完整项目档案，也不把测试设计当成产品执行。

## Requirements

### Requirement: Route by current task and authorized stage
主入口 SHALL 沿已确认任务、已有材料和信息缺口选择当前活动，分别交代完成、未完成、依据、下一动作及执行状态；专项直接调用只完成其当前请求。主入口 SHALL 先判断用户最终目标、交付物、成功信号和任务抽象层级是否足以选择工作路径；当缺口会改变工作方向时 SHALL 先使用 `shaping-ai-tasks`。目标明确但产品事实、业务规则、系统关系或 oracle 不清时 SHALL 继续使用 `clarifying-test-basis`，不得把任务升级重复成测试依据澄清。

主入口 SHALL 用稳定导航层组织路由：项目主线、入口场景、独立能力和词汇／资产层；路由表 SHALL 保持当前处境与专项入口的短映射，详细能力与例外 SHALL 由对应专项维护。主入口在陈述某专项能力、比较入口或建议跳过前，SHALL 读取该专项的 `SKILL.md`；摘要不得替代目标入口。可自行核实的事实 SHALL 先在授权内调查；业务决策、发布决定和跨授权执行 SHALL 留给有权用户。

主入口 SHALL 支持明确请求直达对应专项，不强制重走任务升级或项目建图。长项目 SHALL 保留路线状态；在阶段交接、新会话或上下文压缩后继续前，SHALL 先恢复项目规则、TCO、路线状态和最近产物，不得在缺失上下文时宣称延续既有结论。

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

#### Scenario: Router must not rely on stale summaries
- **WHEN** 主入口需要说明某专项不能覆盖当前请求，或建议跳过该专项
- **THEN** SHALL 先读取该专项 `SKILL.md`，再基于实际入口给出判断和替代路由

#### Scenario: New session continues a project test
- **WHEN** 项目测试在新会话或上下文压缩后继续
- **THEN** SHALL 先恢复项目规则、TCO、路线状态和最近产物；确认仍适用后再推进，不把旧结论冒充当前上下文结论

#### Scenario: Standalone request bypasses the project main line
- **WHEN** 用户明确请求报告汇总、方案质检、错题本维护或单层测试编写
- **THEN** SHALL 直达对应专项并停止在其交付边界，不强制补项目地图或产品执行

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
