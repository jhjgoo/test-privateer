# Spec Delta

## MODIFIED Requirements

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
