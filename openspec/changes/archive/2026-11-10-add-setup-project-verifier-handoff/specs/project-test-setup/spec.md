# Spec Delta

## MODIFIED Requirements

### Requirement: Establish full test loop readiness

当项目预期使用完整 Test Loop 时，Setup SHALL 建立可判定的 Loop 就绪契约，覆盖测试资产根目录、盲测隔离输出位置、共享资源与并行策略、真实验证器入口、质量责任、缺陷升级和风险接受边界。TCO 作为普通 Setup 的核心资产先由 `mapping-project-test-space` 建立或校准，不作为 Loop 专属决定重复维护。

每项 Loop 架构决定 SHALL 处于以下状态之一：项目权威来源已确认、用户已确认、明确不适用、或用户明确确认的后续补建入口。尚未取得这些状态的关键决定 SHALL 记录在配置草稿的未决项并逐项询问用户；Setup MUST NOT 把“未记录”或推荐方案当成已确认决定，也 MUST NOT 在关键决定未关闭时宣称完整 Loop 已就绪。

完整 Loop 就绪状态 SHALL 至少区分 `ready`、`awaiting_user_confirmation` 和 `blocked`。`ready` 仅表示项目级架构决定可定位；不证明环境已验证、测试已运行、质量门禁已接入或当前宿主可创建子代理。当前宿主能力 SHALL 只在当轮运行观察中报告，不写入长期项目配置。

Setup SHALL 针对已选 Loop 范围调查六段 Harness 及并行隔离，复用已有 Runner 或验证资产组合，不要求独立验证器或未选表面同时完备。必需能力缺失时 SHALL 说明影响并提供按授权进行的专项补建交接；未取得相应授权时 MUST NOT 生成资产、执行产品测试或修改 CI。用户已确认后续补建时 SHALL 沿用决定与恢复入口；配置保存 MUST NOT 掩盖仍缺失的必需能力。

#### Scenario: Governance fields are missing

- **WHEN** Setup 发现项目没有缺陷平台、测试责任角色和风险接受边界，且用户要求支持完整 Test Loop
- **THEN** Setup SHALL 逐项给出推荐、影响和应答角色，并将完整 Loop 状态报告为 `awaiting_user_confirmation`，不宣称初始化已完成

#### Scenario: User confirms a deferred verifier

- **WHEN** 项目没有真实验证器，用户确认先记录后续补建入口而不在本轮生成
- **THEN** Setup SHALL 保存该确认和恢复入口，并将完整 Loop 执行就绪状态报告为 `blocked`，不把配置保存冒充验证器可用

#### Scenario: Existing verifier is authoritative

- **WHEN** 项目文档和脚本已经定义启动、就绪检查、驱动、证据、清理和隔离方式
- **THEN** Setup SHALL 引用这些来源并将项目级 Loop 架构标为 `ready`，同时保留环境和宿主能力未验证状态

#### Scenario: A nonselected surface lacks a driver

- **WHEN** 本次完整 Loop 已确认范围为接口，权威入口覆盖所需能力，但 UI 缺少驱动
- **THEN** Setup SHALL 分别记录范围及缺口，不要求补 UI 才配置接口 Loop，也不自动排除尚未决定的范围

## ADDED Requirements

### Requirement: Offer an authorized Harness handoff and reconcile its result

完整 Loop Setup 发现所选范围必要 Harness 能力缺失时，Setup SHALL 复用已有授权或提出一个具体补建问题，说明验证目的、已知缺口、拟改资产、执行动作及影响。已授权动作 SHALL 连续交给 `designing-test-automation`，不重复询问；必要决定未确认时 SHALL 保持待确认。明确拒绝或延期时 SHALL 记录当前缺口与恢复入口，不创建占位资产或反复追问。普通 Setup MUST NOT 因该交接自动扩展为完整 Loop。

交接 SHALL 区分写入、执行及长期采纳授权；只要求代码或临时试验时沿其范围交付。Setup SHALL 回读实际资产、适用原始证据、清理／残留和采纳依据，再按既有 Setup、Harness、资产索引与 Loop 状态定向更新。生成 `draft` 或维护 `changed` 等本次结果 MUST NOT 写为新的长期状态或机械提升为长期 `verified`。

项目已采纳、适用六段可定位且其他架构决定关闭时，未实测 Harness SHALL 为 `declared_unverified`，不单因缺少本轮实测否定 Loop 项目级 `ready`；仍缺必需段时 SHALL 保留真实缺口及 Loop `blocked`。临时环境故障 MUST NOT 覆盖有依据的长期事实。产品结果、Harness 能力与 Loop 独立盲测 SHALL 分开，构造自测 MUST NOT 替代后续独立侦察门禁。

专项 SHALL 交回证据，由 Setup 唯一合成配置；写入遵循既有受管区、冲突保护及回读契约。只有长期覆盖或风险改变时 SHALL 维护 TCO；无关人工内容、历史证据及有效决定 SHALL 保持，写入失败不得声称同步成功。

#### Scenario: Authorized API construction completes in the same task

- **WHEN** 用户已授权在指定本地范围补齐接口支撑、执行验证并采纳长期入口
- **THEN** Setup SHALL 读取并交接专项，在真实请求、独立观察、持久证据和清理复核后更新受影响入口及状态；不重复确认、不强制浏览器、不修改产品

#### Scenario: Only code is authorized

- **WHEN** 用户只授权生成资产而禁止运行
- **THEN** Setup SHALL 接收草案且不执行产品；六段可定位但未实测为 `declared_unverified`，仍缺能力则保留真实缺口，不将 `draft` 写为长期状态

#### Scenario: A temporary trial succeeds without adoption

- **WHEN** 用户允许临时驱动试验但尚未采纳长期入口，试验有完整实际证据
- **THEN** Setup SHALL 保留试验结果，不自动写入长期入口或提升长期 Harness 状态，也不以未采纳阻止获准试验

#### Scenario: A claimed success lacks evidence

- **WHEN** 专项声称 verified，但缺少可回读的真实观察、持久证据或资源恢复结果
- **THEN** Setup SHALL 保留对应未验证项与恢复入口，不根据自述或零退出码提升状态

#### Scenario: Self-validation is followed by a test loop request

- **WHEN** 构造自测完成后，用户另行要求启动完整 Loop
- **THEN** Agent SHALL 按现有 Loop 契约核对当前条件并执行独立侦察，不把构造自测写为独立测试结果；满足既有门禁且仍有效的证据按原规则复用
