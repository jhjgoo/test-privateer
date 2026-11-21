## ADDED Requirements

### Requirement: Reuse one blind test worker contract
完整 Loop 的每个冷启动盲测 wave SHALL 在任务包首行指向同一份盲测子代理共同契约；brief SHALL 只补充目标版本、质量视角、获准入口、覆盖排除项和输出要求，MUST NOT 重复共同隔离、授权、证据、handoff 或写入规则。

#### Scenario: Multiple blind waves share baseline rules
- **WHEN** 一轮 Loop 分派多个盲测子代理
- **THEN** 每个任务包首行都指向同一共同契约，差异信息保留在各 brief 中

#### Scenario: Prepare task packages without executing a loop
- **WHEN** 用户只要求准备盲测任务包，尚未要求执行产品测试或启动子代理
- **THEN** 编排者先读取共同契约，通过任务包生成入口填写已确认差异并核对引用可达；不创建或推进 Run，也不将准备完成写成测试完成
