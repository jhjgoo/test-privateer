# Spec Delta

## ADDED Requirements

### Requirement: Define a checkable exit condition before long or comparative work
当任务会连续执行、批量维护资产、比较版本、运行行为评测或跨阶段推进时，`shaping-ai-tasks` SHALL 在进入执行前建立可判定退出条件。退出条件 SHALL 描述可观察对象、判定方式、复跑或核验位置、停止／失败边界和必要的截止条件；SHALL 区分目标完成、环境受阻、案例无效和放弃推进。

执行中新证据或用户决策 SHALL 只能显式修改退出条件并记录原因；Agent SHALL NOT 为宣称完成而临时放宽原条件，也不 SHALL 把活动量、输出长度或阶段自述当作完成证据。

#### Scenario: Continuous test execution
- **WHEN** 用户要求持续执行测试直到达到某目标但未说明何时停止
- **THEN** Skill SHALL 先给出可观察退出条件、失败边界和记录位置，再进入执行路径

#### Scenario: Version comparison
- **WHEN** 任务会比较 Prompt、Skill、模型或工具版本
- **THEN** Skill SHALL 先固定比较对象、任务、指标、失败判定和结果状态，再启动候选运行

#### Scenario: Exit condition changes
- **WHEN** 执行中发现原退出条件测错对象或用户改变目标
- **THEN** SHALL 显式记录新旧条件、修改原因和已产生结果的适用范围；不得静默放宽原条件
