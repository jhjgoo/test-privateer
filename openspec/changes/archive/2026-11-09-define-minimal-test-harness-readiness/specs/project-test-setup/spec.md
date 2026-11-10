# Spec Delta

## MODIFIED Requirements

### Requirement: Record project test surface readiness

项目配置 SHALL 为每个已调查的候选测试表面保留一行，记录适用性、选定框架或入口、选择来源、六段 Harness 入口或缺口、Harness 状态、最近长期证据和阻塞／恢复入口。六段 SHALL 覆盖 `Prepare`（目标、身份、输入和初始数据）、`Start`（启动或连接及就绪检查）、`Drive`（真实刺激）、`Observe`（独立预期与实际结果）、`Preserve`（原始证据保留）和 `Restore`（只清理本轮拥有的资源并保留证据）。这些能力可以由同一 Runner 覆盖，不要求六个独立脚本或新目录。

Harness 状态 SHALL 只使用 `not_configured`、`partial`、`declared_unverified`、`verified`、`blocked` 和 `not_applicable`。框架名称、测试目录、健康检查或一次退出码单独不能产生 `verified`；临时机器、账号、网络或服务状态 SHALL 只进入本轮报告，不固化为长期 Harness 状态。配置契约升级为 `test-privateer-project-profile/v2` 时，旧 v1 的“项目级 `ready`”在没有六段实际证据时 SHALL 迁移为 `declared_unverified`，不得自动迁移为 `verified`。

#### Scenario: Applicable surface has no driver

- **WHEN** 项目确认某测试表面适用并已选定框架，但可执行驱动、独立观察、证据保留或资源恢复至少一段缺失
- **THEN** Setup SHALL 将该表面标为 `partial` 并记录缺失段和补建入口，不把框架名称等同于可运行

#### Scenario: Current environment is temporarily unavailable

- **WHEN** 测试表面的项目入口和长期 Harness 证据可定位，但当前机器或服务暂时不可用
- **THEN** Setup SHALL 保持项目级状态基于长期来源，并在当轮结果单独报告环境未验证或故障

#### Scenario: A candidate surface has unknown applicability

- **WHEN** 项目材料不足以判断 Agent 评测、UI 或其他候选测试表面是否适用
- **THEN** Setup SHALL 在矩阵保留该表面、标为 `not_configured` 并记录取证动作，不省略该行或写成 `not_applicable`

#### Scenario: A framework exists but the API driver is missing

- **WHEN** 项目已声明接口测试框架，但没有可定位的请求驱动、业务观察或证据保留入口
- **THEN** Setup SHALL 记录该测试表面的 Harness 为 `partial` 或 `declared_unverified`，列出缺失段和恢复入口，不把框架存在写成 `verified`

#### Scenario: An existing harness covers a selected surface

- **WHEN** 项目已有入口能够准备隔离数据、启动或连接目标、执行真实刺激、观察独立结果、保存原始证据并清理本轮资源
- **THEN** Setup SHALL 记录六段来源和可复核证据，将该表面标为 `verified`，同时说明这不表示产品通过或全量覆盖

#### Scenario: An old v1 profile has project-level ready

- **WHEN** Setup 读取旧项目配置，发现测试表面只有 v1 的 `ready`，没有六段 Harness 证据
- **THEN** Setup SHALL 保留原来源并将 Harness 标为 `declared_unverified`，记录重校准入口，不把迁移本身当作运行验证

## ADDED Requirements

### Requirement: Keep Harness setup proportional and separate from authorization

Setup SHALL 只调查和记录 Harness 能力，不因六段模型自动运行产品测试、启动服务、安装框架、创建数据、修改 CI 或生成验证器。需要实际构造或修复 Harness 时，Setup SHALL 指向 `designing-test-automation` 或现有验证器交接；测试表面不适用时 SHALL 记录 `not_applicable` 及依据。普通单层任务不得因项目尚未建立完整 Loop Harness 而被 Setup 阻塞。

顶层 Setup `ready` MAY 与有明确项目选择和恢复入口的 `partial` 或 `declared_unverified` Harness 共存，但 MUST NOT 与因框架、入口或适用性仍待决定而产生的 `not_configured` 共存；这种未决选择 SHALL 使用 `awaiting_user_confirmation` 并停在一个具体问题。

#### Scenario: A simple unit task does not need a project Harness

- **WHEN** 用户只要求一个局部单元测试，项目级 Harness 尚未配置
- **THEN** Setup 或路由 SHALL 不强制初始化完整 Harness、浏览器、服务或额外框架，直接保留单层任务所需的最小边界

#### Scenario: Harness construction needs authorization

- **WHEN** Setup 发现某测试表面缺少可执行 Harness，且补建会修改测试资产或访问环境
- **THEN** Setup SHALL 报告缺口和影响，交接到自动化设计专项；不得把推荐方案当成已确认或已验证

#### Scenario: An unconfirmed generated runner is discovered

- **WHEN** 仓库存在未提交、临时、历史实验或 AI 生成的测试入口，但项目权威来源和用户都没有采纳它
- **THEN** Setup SHALL 只把它视为候选，不运行、不写成项目入口或 `verified`；采纳会改变后续执行时停在一个明确确认问题
