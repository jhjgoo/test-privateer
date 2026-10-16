# Proposal

## Why

用户常以局部动作或宽泛动词描述测试请求，导致任务在进入测试路由前缺少最终目标、成功信号、专业方法、原始材料和外部验证。现有 Skill 已能严谨执行明确的测试任务，但缺少一个上游能力把模糊请求升级为值得执行、可验证且不过度扩张的任务契约。

## What Changes

- 新增 `shaping-ai-tasks` Skill：识别表面任务与最终目标，补齐交付物、原始材料、专业方法、工具权限、成功信号和外部验证。
- 在 `test-privateer` 主入口增加任务升级路由，并明确它与 `setting-test-mission`、`clarifying-test-basis` 的边界。
- 增加“高度、深度、范围、验证”检查，要求专家方法产生实际认知增量，不以角色扮演或更长输出代替专业工作。
- 增加最小行为评测，覆盖需要升级、应直接放行和目标已清楚但测试依据不清的相邻场景。
- 更新 Skill 索引和使用教程中的 Skill 数量与入口说明。

## Capabilities

### New Capabilities

- `shaping-ai-tasks`: 将用户模糊或低层级请求升级为明确、有深度、可验证的 AI 工作任务。

### Modified Capabilities

- `testing-workflow`: 主入口在任务目标、交付物或成功标准会改变工作方向时，先进入任务升级；目标明确但测试依据不清时继续进入既有澄清流程。

## Impact

影响 `skills/shaping-ai-tasks/SKILL.md`、`skills/test-privateer/SKILL.md`、README 与开发教程，以及新增的评测输入和契约测试。无新增依赖、工具、运行时配置或安装方式变化；默认不修改用户项目、不执行产品测试。
