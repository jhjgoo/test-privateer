# Spec Delta

## ADDED Requirements

### Requirement: Maintain an append-only test decision audit trail
当测试执行连续推进、多轮证据会改变解释、无人值守执行或用户明确要求审计时，Agent SHALL 维护追加式决策日志。每条决策 SHALL 记录时间、测试阶段、决策、理由、证据指针和结果；证据指针 SHALL 使用路径、稳定 ID、版本或等价定位方式，不得用叙述替代。

新证据、用户决策或失败 SHALL 通过新增记录取代旧决策的当前适用性；Agent SHALL NOT 重写或删除历史决策行。恢复点 SHALL 引用决策日志的最新边界，但不复制全部记录；普通短任务 SHALL NOT 被强制生成审计表。

#### Scenario: Evidence changes an earlier interpretation
- **WHEN** 后续执行显示先前 finding 的解释不成立
- **THEN** 新增决策行说明修正、依据和影响范围，保留原决策及其当时证据指针

#### Scenario: Unattended execution changes route
- **WHEN** 无人值守测试到达预设转向条件
- **THEN** 记录触发条件、决策、证据指针和下一阶段，再继续或停止

#### Scenario: Short execution stays lightweight
- **WHEN** 单会话只执行一个明确测试且证据不改变方向
- **THEN** 沿用正常测试记录，不强制创建决策日志
