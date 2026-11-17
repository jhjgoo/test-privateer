## ADDED Requirements

### Requirement: Reuse one blind test worker contract
完整 Loop 的每个冷启动盲测 wave SHALL 在任务包首行指向同一份盲测子代理共同契约；brief SHALL 只补充目标版本、质量视角、获准入口、覆盖排除项和输出要求，MUST NOT 重复共同隔离、授权、证据、handoff 或写入规则。

#### Scenario: Multiple blind waves share baseline rules
- **WHEN** 一轮 Loop 分派多个盲测子代理
- **THEN** 每个任务包首行都指向同一共同契约，差异信息保留在各 brief 中
