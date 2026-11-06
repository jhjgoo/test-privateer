# Spec Delta

## ADDED Requirements

### Requirement: Confirm material governance gaps during setup

项目初始化时，缺陷入口、测试责任、风险接受或 CI 门禁的未知决定若会影响后续交接或判定，Setup SHALL 先给出依据、推荐、影响和应答角色，等待确认或明确记录当前不接入；MUST NOT 仅以“未记录”代替项目决定并宣称相关配置完成。TCO 不存在时仍按资产缺口处理，不生成空 TCO 或宣称项目地图完成。

#### Scenario: Defect and quality responsibility are unknown

- **WHEN** 项目没有可定位的缺陷入口和风险接受责任，且这些决定会影响测试交接
- **THEN** Setup SHALL 提出当前最重要的一个确认问题，不把缺口列表当作已完成的治理配置

### Requirement: Establish full test loop readiness

当项目预期使用完整 Test Loop 时，Setup SHALL 建立可判定的 Loop 就绪契约，覆盖测试资产根目录、盲测隔离输出位置、共享资源与并行策略、真实验证器入口、质量责任、缺陷升级和风险接受边界。

每项 Loop 架构决定 SHALL 处于以下状态之一：项目权威来源已确认、用户已确认、明确不适用、或用户明确确认的后续补建入口。尚未取得这些状态的关键决定 SHALL 记录在配置草稿的未决项并逐项询问用户；Setup MUST NOT 把“未记录”或推荐方案当成已确认决定，也 MUST NOT 在关键决定未关闭时宣称完整 Loop 已就绪。

完整 Loop 就绪状态 SHALL 至少区分 `ready`、`awaiting_user_confirmation` 和 `blocked`。`ready` 仅表示项目级架构决定可定位；不证明环境已验证、测试已运行、质量门禁已接入或当前宿主可创建子代理。当前宿主能力 SHALL 只在当轮运行观察中报告，不写入长期项目配置。

Setup SHALL 调查已有验证器是否覆盖启动、就绪检查、驱动、证据、清理和并行隔离。没有可定位验证器时，Setup SHALL 推荐建立或补建验证器，并经用户确认后记录后续入口；Setup MUST NOT 为完成初始化自动生成验证器、TCO、测试资产或 CI。

#### Scenario: Governance fields are missing

- **WHEN** Setup 发现项目没有缺陷平台、测试责任角色和风险接受边界，且用户要求支持完整 Test Loop
- **THEN** Setup SHALL 逐项给出推荐、影响和应答角色，并将完整 Loop 状态报告为 `awaiting_user_confirmation`，不宣称初始化已完成

#### Scenario: User confirms a deferred verifier

- **WHEN** 项目没有真实验证器，用户确认先记录后续补建入口而不在本轮生成
- **THEN** Setup SHALL 保存该确认和恢复入口，并将完整 Loop 执行就绪状态报告为 `blocked`，不把配置保存冒充验证器可用

#### Scenario: Existing verifier is authoritative

- **WHEN** 项目文档和脚本已经定义启动、就绪检查、驱动、证据、清理和隔离方式
- **THEN** Setup SHALL 引用这些来源并将项目级 Loop 架构标为 `ready`，同时保留环境和宿主能力未验证状态
