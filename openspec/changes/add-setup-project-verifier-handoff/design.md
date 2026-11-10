# Design

## Context

当前 Setup 能发现验证器缺口并记录后续入口，`designing-test-automation` 已能生成和验证项目产品驱动器；缺少的是两者之间需确认、可复检的交接。该 change 在 `clarify-setup-governance-scope` 同步后实施，复用其 Setup 状态、测试表面矩阵和资产索引。

## Goals / Non-Goals

**Goals:** 让用户可以在 Setup 中一次确认验证器补建，并让 Setup 根据真实资产和运行证据更新项目就绪状态。

**Non-Goals:** 不新增验证器 Skill，不要求普通 Setup 自动生成验证器，不静默安装框架，不将验证器生成授权扩大为外部环境、凭据、费用、CI 或产品代码修改。

## Decisions

- 复用 `designing-test-automation` 的“生成项目产品验证器”，Setup 只负责调查、确认、交接和结果对账，避免复制启动、doctor、驱动、采证与清理方法。
- 只在完整 Test Loop 是当前目标且验证器能力缺失时提供生成确认；普通 Setup 只记录验证器状态，避免初始化过重。
- 确认问题一次说明项目内拟写资产和预计验证动作。用户同意后，已说明范围内的项目本地生成与验证连续推进；遇到未说明的外部环境、凭据、费用、共享数据或安装动作时再停下确认。
- 交接上下文保持最小：目标产品表面、权威来源、已有 harness、允许环境、资产位置、隔离／清理边界和本轮权限。未知业务规则继续作为阻塞，不在生成专项中补造。
- 专项返回 `verified`、`draft` 或 `blocked`。Setup 通过实际文件、工具轨迹和证据指针复检，不接受“已完成”自述；只有 `verified` 可以解除验证器阻塞。
- 结果写回现有项目配置的验证器段、测试表面矩阵和资产索引，不新增状态文件。验证器脚本、说明和证据仍由项目约定的位置维护。

## Risks / Trade-offs

- [Setup 变成长任务] → 仅完整 Loop 且用户明确确认时进入生成；拒绝或延期立即记录恢复入口。
- [一次确认被过度解释] → 确认前列明写入和验证动作，外部副作用仍单独确认。
- [专项自述造成假就绪] → Setup 必须回读资产、运行证据和清理结果后再更新状态。
- [两个活动 change 修改同一 Skill] → 本 change 明确依赖 `clarify-setup-governance-scope` 先归档同步，实施时基于同步后的模板追加最小交接。

## Migration Plan

先完成并归档 `clarify-setup-governance-scope`。随后实施本 change，旧配置重跑 Setup 后按缺失验证器状态获得一次生成选择；用户不选择时保持现有 `blocked` 行为。
