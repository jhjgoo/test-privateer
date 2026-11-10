# Proposal

## Why

完整 Test Loop 缺少真实产品验证器时，Setup 目前只能记录缺口和后续入口，用户仍需另起任务才能补齐。需要建立一个明确、需确认且可复检的交接，让初始化能把“发现缺口”推进到“生成并验证资产”，同时不扩大 Setup 自身权限。

## What Changes

- Setup 在完整 Test Loop 目标下发现验证器缺失时，说明影响并询问用户是否现在生成。
- 用户确认后，Setup 将已调查的产品表面、启动、证据、隔离和安全边界交给 `designing-test-automation`，不在 Setup 中复制验证器生成方法。
- 验证器生成结果区分 `verified`、`draft` 和 `blocked`；只有真实驱动、采证、清理和回读通过后，才可解除相应 Loop 阻塞。
- Setup 回读实际验证资产并更新 `.test-privateer/project.md` 的验证器入口、测试表面和资产状态；拒绝或延期时保留 `blocked` 和恢复入口。
- 增加确认、成功、草案和受阻边界的契约测试与真实模型行为评测。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `project-test-setup`：在完整 Loop 缺少验证器时提供需确认的专项生成交接，并根据实际结果回写就绪状态。
- `test-automation`：接收 Setup 的结构化上下文，生成、验证并返回可供项目配置复检的验证器结果。

## Impact

- `skills/setup-test-privateer/SKILL.md`
- `skills/designing-test-automation/SKILL.md`
- `skills/setup-test-privateer/references/project-profile-template.md`
- `openspec/specs/project-test-setup/spec.md`
- `openspec/specs/test-automation/spec.md`
- `evals/project-test-setup/`
- `tests/test_project_test_setup_contract.py`
