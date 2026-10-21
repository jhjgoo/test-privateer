# Spec Delta

## MODIFIED Requirements

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
