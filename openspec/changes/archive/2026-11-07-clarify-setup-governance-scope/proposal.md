# Proposal

## Why

用户选择“普通测试入口配置”时，真实输出把 TCO、责任分工、缺陷升级和 CI 门禁表述成完整 Test Loop 缺口，容易被理解为这些治理字段只属于 Loop；后续验证又暴露 Setup 可以只记录“TCO 后续建立”并宣称完成。TCO 是项目长期测试全景图，普通初始化也应建立有依据的项目基线，而不是把它降级为可长期缺失的可选资产。

## What Changes

- 在 Setup 中明确区分项目治理字段与 Loop 专用门槛。
- 说明选择普通配置不缩小调查范围；只影响是否评估完整 Loop 就绪状态。
- 普通 Setup 核对适用测试类型和框架约定；已有框架直接沿用，需要新增能力但没有约定时给出推荐并等待确认。
- 普通 Setup 通过现有 `mapping-project-test-space` 初始化或校准唯一 TCO；允许保留未知和取证任务，不允许空模板占位。
- 用户明确排除 TCO 时遵守授权边界，但 Setup 只能报告部分完成和恢复入口。
- 为项目配置增加可判定的 Setup 状态、新鲜度与失效条件，避免把文件保存误报为初始化就绪。
- 将测试表面从“已确认／未决”扩展为项目级就绪矩阵，并用统一资产索引记录 TCO、需求资产、Run、证据、报告和盲测输出的权威位置与边界。
- 补充普通配置治理缺口的行为评测场景。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `project-test-setup`：普通初始化核对适用测试表面和框架，确认项目治理缺口，建立或校准项目 TCO，并保存可判定的 Setup、测试面及资产状态。

## Impact

- `skills/setup-test-privateer/SKILL.md`
- `skills/setup-test-privateer/references/project-profile-template.md`
- `skills/mapping-project-test-space/SKILL.md`（复用，不修改方法）
- `openspec/specs/project-test-setup/spec.md`
- `evals/project-test-setup/`
- `tests/test_project_test_setup_contract.py`
