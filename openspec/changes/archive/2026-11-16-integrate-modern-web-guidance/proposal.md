# Proposal: Integrate Modern Web Guidance

## Why

用户希望将 Google Modern Web Guidance 用作 UI 测试的现代平台依据，并保留后续现代化审计能力。现有 UI 评审和自动化设计没有统一入口说明如何使用该指南和 `legacy-scan`，也缺少“静态候选不是测试证据”的边界。

## What Changes

- 在 `reviewing-ui-ux` 新增 Modern Web Guidance 共享参考，说明检索、读取指南、扫描候选、复核证据和记录审计结果的方法。
- `reviewing-ui-ux`、`designing-test-automation` 和 `test-privateer` 入口接入该参考，使 UI 测试和后续现代化审计可路由到同一用法。
- 新增契约测试，检查参考可达、证据边界存在且三个消费者均可发现。

## Impact

- `skills/reviewing-ui-ux/`
- `skills/designing-test-automation/SKILL.md`
- `skills/test-privateer/SKILL.md`
- `tests/test_modern_web_guidance_contract.py`

## Non-goals

- 不复制或改写 MWG 指南内容，不把外部 CLI 安装为本仓库运行时依赖。
- 不新增独立“现代化审计”Skill；先复用 UI 评审与自动化设计入口。
- 不把静态扫描结果当作 UI 测试通过、无障碍符合或浏览器兼容结论。
