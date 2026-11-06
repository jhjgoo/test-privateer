# Spec Delta

## ADDED Requirements

### Requirement: Gate full loops on project readiness

在创建或推进完整 Test Loop 前，Loop SHALL 读取项目规则和 `.test-privateer/project.md`，并核对完整 Loop 就绪契约中的资产位置、验证器入口、共享资源策略、质量责任、缺陷升级和风险接受边界。恢复旧 Run 时 SHALL 先只读核对原 Run ID、已有决定和证据，保留原轮次；尚未就绪时不得推进产品执行。

项目配置不存在、状态为 `not_configured`／`awaiting_user_confirmation`，或关键架构决定未关闭时，Loop SHALL 先进入最小 `setup-test-privateer` 确认流程；每轮只询问一个会改变架构或执行安全的决定。状态为 `blocked` 时，Loop SHALL 沿已确认的恢复入口报告阻塞，不重复询问已确认决定；只有权威来源变化或用户要求改变决定时才重进 Setup。Loop MUST NOT 把默认路径、推断、项目名或未回答的推荐当成项目决定。

配置声明 `ready` 只解除项目架构预检，不替代当前轮次契约、执行授权、环境验证或宿主子代理能力检查。配置与当前权威来源冲突时，Loop SHALL 停止使用冲突字段并进入 Setup 或当前任务澄清。

普通单层测试、单次执行或报告汇总 SHALL 继续直达对应专项，不因缺少完整 Loop 就绪配置而被阻塞。

#### Scenario: Full loop starts without a profile

- **WHEN** 用户要求完整 Test Loop，但项目没有 `.test-privateer/project.md`
- **THEN** Loop SHALL 先进入最小 Setup 确认 Loop 架构，不创建轮次或边执行边猜测资产与责任边界

#### Scenario: Profile is awaiting confirmation

- **WHEN** 项目配置记录完整 Loop 状态为 `awaiting_user_confirmation`
- **THEN** Loop SHALL 停在对应确认问题，不推进产品执行或盲测调度

#### Scenario: Deferred verifier blocks a full loop

- **WHEN** 项目配置为 `blocked` 且记录了已确认的验证器补建入口
- **THEN** Loop SHALL 报告该入口和受阻范围，不重复请求同一确认，不创建新 Run 或推进盲测

#### Scenario: Resume an older run without a profile

- **WHEN** 用户要求恢复已有 Run，但项目没有完整 Loop 就绪配置
- **THEN** Loop SHALL 只读核对原 Run ID、授权和证据，进入最小 Setup 补齐缺失架构；恢复后沿用原 Run ID，不重做已有效的检查

#### Scenario: Single API test has no profile

- **WHEN** 用户只要求编写并运行一条接口测试，项目没有完整 Loop 配置
- **THEN** Agent SHALL 直达接口测试专项，不强制先完成 Setup
