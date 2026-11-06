# Spec Delta

## ADDED Requirements

### Requirement: Route an explicitly requested complete test loop

当用户明确要求 Agent 连续完成测试分析、用例、执行和报告，或直接调用 `running-test-loop` 时，主入口 SHALL 路由到 Test Loop。普通分析、单层自动化、单次执行或报告汇总 SHALL 继续直达现有专项，不因存在 Loop 而强制进入完整流程。

Loop SHALL 依赖当前测试轮次和项目配置契约。前置 change 尚未落实或对应资产不存在时，Agent SHALL 停在可定位边界并说明缺少的契约，不在 Loop 内创建另一套临时格式。

#### Scenario: User requests the whole testing chain

- **WHEN** 用户要求从当前变化分析开始，自动生成用例、执行适用测试并输出测试报告
- **THEN** 主入口 SHALL 路由到 `running-test-loop`，由 Loop 复用各专项推进

#### Scenario: User requests one API test

- **WHEN** 用户只要求编写并运行一条明确接口测试
- **THEN** 主入口 SHALL 直达 `writing-api-tests` 或 `running-test-sessions`，不创建完整 Loop

### Requirement: Keep analysis and product execution authorization separate

测试分析 SHALL 可以读取项目材料、现有测试和历史结果，但 SHALL NOT 因分析任务本身运行产品测试、启动服务、安装依赖、创建数据或访问外部环境。只有用户明确要求执行，或 Test Loop 已记录相应授权时，Agent 才 SHALL 进入产品执行。

获得执行授权后，Agent SHALL 在授权范围内连续完成正常测试步骤。新增环境、凭据、费用、共享数据修改或其他超出原授权的动作 SHALL 触发澄清、人工检查点或停止。

#### Scenario: Change analysis has no execution authorization

- **WHEN** 用户只要求分析一项变化的测试影响
- **THEN** Agent SHALL 核对已有测试和历史证据，提出建议执行范围，但不得运行测试并把结果写入分析

#### Scenario: Test loop includes execution authorization

- **WHEN** 用户明确授权 Test Loop 在指定本地或测试环境运行测试
- **THEN** Agent SHALL 在记录的边界内连续执行，无需为每条正常测试重复请求许可

#### Scenario: Execution needs a new destructive action

- **WHEN** 已授权 Loop 后发现必须清理共享数据或访问生产环境才能继续
- **THEN** Agent SHALL 停止该分支并说明影响，不把原测试授权扩大到新的破坏性动作
