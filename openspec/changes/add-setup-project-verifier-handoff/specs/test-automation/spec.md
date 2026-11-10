# Spec Delta

## ADDED Requirements

### Requirement: Return a verifier result that setup can reconcile

验证器生成专项接收 Setup 交接时 SHALL 沿用项目权威来源、安全边界、资产位置和已确认授权，优先复用既有 harness。结果 SHALL 返回 `verified`、`draft` 或 `blocked`，并包含实际验证资产位置、覆盖的产品表面、执行证据、清理结果、未验证项及恢复条件。

`verified` SHALL 要求至少一条已映射真实用户路径完成启动或连接、只读 doctor、驱动、原始证据持久化、仅清理本次资源及清理后证据复检。无法完成其中任一必要环节时 SHALL 返回 `draft` 或 `blocked`，MUST NOT 只因脚本生成或命令退出成功而返回 `verified`。

#### Scenario: Existing harness becomes a verified verifier

- **WHEN** 项目已有可复用 harness，专项补齐缺失入口并成功驱动一条真实路径，证据在清理后仍可读取
- **THEN** 专项 SHALL 返回 `verified`、资产与证据指针、已覆盖表面和清理结果，供 Setup 回读

#### Scenario: Environment blocks live verification

- **WHEN** 验证资产已生成，但环境、凭据或隔离条件阻止真实路径验证
- **THEN** 专项 SHALL 返回 `draft` 或 `blocked`、已完成资产、失败证据和恢复条件，不扩大权限或宣称验证器可用
