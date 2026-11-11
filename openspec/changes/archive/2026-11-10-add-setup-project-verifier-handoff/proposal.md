# Proposal

## Why

完整 Test Loop 所选范围缺少必要运行支撑时，Setup 仍主要建议另行补建。当前 `designing-test-automation` 已具备六段 Harness 的构造、验证和维护能力；剩余缺口是 Setup 获得授权后直接交接、核对结果并回填配置。

2026-11-10 对照当前契约校准：旧方案重复定义了已有生成状态，把草案写成长期状态，并把实际执行与 Loop 项目架构就绪混为一谈。本 change 保留，缩为现有能力之间的交接，不再建设验证器框架。

## What Changes

- 仅针对当前完整 Loop 所选范围的必要缺口建议最小补建／修复；现有 Runner 可满足时直接复用，不要求独立验证器或所有测试表面齐备。
- 沿用已有授权；尚未授权时说明拟改资产、验证动作和影响，确认后交给现有专项。写入、执行和长期采纳分别判断。
- 复用生成、维护及长期 Harness 的状态定义。资产完整但未实测可为 `declared_unverified`；项目级 Loop `ready` 不等于当前执行可用或产品通过。
- 回读资产、原始证据、清理结果和采纳依据后，按既有安全写入约定更新受影响配置；仅长期覆盖或风险改变时维护 TCO。
- 补有界交接及相邻边界的行为评测；构造自测不得替代后续 Loop 的独立盲测侦察。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `project-test-setup`：将必要缺口交给现有专项，核实回填正确层级的状态。
- `test-automation`：承接 Setup 范围与授权，交回实际资产、观察和恢复证据，复用现有方法。

## Impact

- 实施作用点：`skills/setup-test-privateer/SKILL.md`、`skills/designing-test-automation/SKILL.md`。
- 消费者核对：配置模板、主路由、Loop 侦察门禁和 `docs/guide.md`；只改实际冲突。保持 profile/v2，不增加状态文件，继续复用共享六段参考和安全写入脚本。
- 验收：`evals/project-test-setup/`、`tests/test_project_test_setup_contract.py` 及受影响自动化契约；复用已有夹具和评测记录器。
- 规格：`project-test-setup`、`test-automation`。

实施与验证已完成，保持活动 change 等待用户确认；验收结果和适用边界见 tasks.md。
