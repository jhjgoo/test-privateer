# Proposal

## Why

项目选择 DeepEval 后，当前流程只能在官方 Skill 缺失时返回 `missing_official_skill`，用户还需要自行判断如何恢复。需要把官方 Skill 可用性变成可见的就绪检查，并在任何安装发生前取得用户明确确认。

## What Changes

- `setup-test-privateer` 在项目选定 DeepEval 时检查官方 Skill、项目运行依赖和评测入口是否就绪，但不把宿主临时状态固化为项目事实。
- 官方 DeepEval Skill 缺失时，先说明来源、安装对象和影响，再询问用户是否安装；只有明确确认后才使用宿主现有安装能力。
- 实际进入 DeepEval 评测时重复核对官方 Skill，避免 Setup 与执行发生在不同宿主后误判。
- 用户拒绝、未确认或安装失败时继续保留 `missing_official_skill`，只完成框架无关的质量设计，不自造实现或切换框架。
- Python 依赖、登录、上传、外部 Judge 和费用继续使用各自的授权边界，不随 Skill 安装确认一并放行。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `project-test-setup`：在 DeepEval 被选定时增加就绪检查和官方 Skill 安装确认。
- `deepeval-agent-evaluation`：官方 Skill 缺失时先提供可授权的恢复入口，再决定是否保持受阻。
- `testing-workflow`：主流程允许用户明确确认安装官方 Skill，同时继续禁止静默安装和框架替换。

## Impact

影响 `setup-test-privateer`、`evaluating-agents-with-deepeval`、主路由的 DeepEval 边界、相关契约测试和项目 Setup 行为评测材料。不新增运行时依赖，不自动安装官方 Skill 或 Python 包。
