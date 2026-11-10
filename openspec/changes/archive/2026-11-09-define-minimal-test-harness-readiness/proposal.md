# Proposal

## Why

项目现在能记录测试框架和入口，但“入口存在”仍容易被误读成“这类测试已经具备可执行、可观察、可留证和可恢复能力”。这会让 Test Loop 跳过接口实际驱动、UI 真实渲染或 Agent 轨迹取证；现在需要一套跨测试表面的轻量 Harness 契约，明确能力缺口而不引入重型平台。

## What Changes

- 定义通用六段式 Harness：`Prepare`、`Start`、`Drive`、`Observe`、`Preserve`、`Restore`。
- 统一测试表面的 Harness 就绪状态：`not_configured`、`partial`、`declared_unverified`、`verified`、`blocked`、`not_applicable`。
- 将 Setup 的测试表面矩阵从“框架／入口存在”升级为“六段能力、证据和恢复入口可判定”，并保留 TCO、治理和资产索引边界。
- 让自动化设计复用既有项目 Runner、驱动和验证器，按测试表面给出最小 Harness 缺口，不新增通用 Harness 服务或框架。
- 让 Test Loop 在详细分析和用例扩展前，对本轮选中的测试表面执行最小侦察门禁；复用当前有效证据或运行一条有界探针，再由结果决定后续分析深度。
- 在 Run 模板中增加本轮测试面与 Harness 证据指针，不复制 Harness 或原始证据正文。
- 增加最小契约测试和代表性行为评测，覆盖分析阶段 API 侦察、UI、Agent、未确认候选、旧状态迁移和轻量任务旁路。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `project-test-setup`：测试表面矩阵 SHALL 记录六段式 Harness 能力和可核验状态，而不是把框架或入口存在等同于可用。
- `test-automation`：自动化设计 SHALL 提供可复用的轻量 Harness 就绪判断和最小构造／修复交接。
- `test-loop`：完整 Loop SHALL 在全局项目门禁通过、详细分析和用例扩展前，对本轮选中的测试表面执行侦察门禁，并以当前实际证据控制推进。

## Impact

- 修改 `skills/setup-test-privateer/SKILL.md` 及项目配置模板。
- 修改 `skills/designing-test-automation/SKILL.md`，新增共享参考 `references/harness-readiness.md`。
- 修改 `skills/running-test-loop/SKILL.md`、`skills/test-privateer/references/test-run-template.md`、共享产物路由和必要的变化分析交接。
- 修改 `openspec/specs/project-test-setup/spec.md`、`test-automation/spec.md`、`test-loop/spec.md` 的增量规格。
- 增加契约测试、最小评测输入和评测说明；不新增运行时依赖，不修改被测产品代码。
