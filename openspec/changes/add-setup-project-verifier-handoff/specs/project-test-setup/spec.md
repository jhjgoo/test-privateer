# Spec Delta

## ADDED Requirements

### Requirement: Offer a confirmed project verifier handoff

当完整 Test Loop 是当前 Setup 目标，且项目缺少覆盖启动、就绪检查、真实用户路径、证据保留、隔离、清理或恢复的验证器时，Setup SHALL 说明缺失能力、对 Loop 的影响、拟生成资产和预计验证动作，并询问用户是否现在生成。用户未确认时，Setup MUST NOT 生成验证器、启动服务或运行产品路径。

用户确认后，Setup SHALL 将已调查的项目表面、权威来源、安全边界、资产位置和授权范围交给验证器生成专项。生成结束后，Setup SHALL 回读实际验证资产及其证据，并将结果区分为 `verified`、`draft` 或 `blocked`；只有 `verified` 才 MAY 解除对应验证器阻塞。Setup SHALL 更新项目配置中的验证器入口、测试表面状态、资产状态和完整 Loop 状态，不得用专项自述代替文件与运行证据。

#### Scenario: User confirms verifier generation

- **WHEN** 完整 Loop 缺少验证器，Setup 已说明拟生成资产、项目内写入和验证动作，用户明确同意现在生成
- **THEN** Setup SHALL 交给验证器生成专项连续实施，并在专项返回后回读实际资产与证据，再更新项目配置状态

#### Scenario: User declines or defers generation

- **WHEN** 用户拒绝本轮生成，或明确由后续任务补建
- **THEN** Setup SHALL 保留完整 Loop `blocked`、缺失能力、责任角色和恢复入口，不创建占位验证器

#### Scenario: Generated verifier remains a draft

- **WHEN** 验证资产已经生成，但没有完成真实路径驱动、证据保留或清理复检
- **THEN** Setup SHALL 将验证器记录为 `draft` 并保持完整 Loop `blocked`，不得把文件存在报告为验证器可用
