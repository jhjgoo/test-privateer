# Proposal

## Why

当前盲测规则把未预先声明的全局 RTK、全局／项目级 Skill、项目规则和 CLI 误当成开发上下文污染，可能让测试子代理失去正常项目能力，或把有效盲测错误判为无效。盲测应隔离本次开发叙事与既有结论，而不是隔离稳定的操作基线。

## What Changes

- 明确全局／项目规则、Skill、项目测试配置和常规 CLI 属于允许的稳定操作基线，子代理可以并应按任务需要使用。
- 将污染边界收窄为开发会话、实现理由、diff、修复假设、开发自测、既有 Finding 结果、评分规则及携带这些内容的记忆。
- 未预先列出的稳定操作基线只需补记身份或版本；只有它包含任务特定开发材料时，wave 才无效或受阻。
- 修正评测协议和既有评测判读，不再把读取全局 RTK 或项目 `AGENTS.md` 本身归类为环境错误。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `test-loop`: 修正盲测输入隔离和无子代理受阻条件，允许测试 Agent 使用稳定的全局／项目操作基线。

## Impact

- 更新 `skills/running-test-loop/SKILL.md`、测试轮次模板、`openspec/specs/test-loop/spec.md`、契约测试和 `evals/test-loop/`。
- 不放宽开发叙事、既有 Finding、diff 或评分规则的隔离要求。
- 不要求宿主导出不可取得的完整系统提示词，也不新增模型、CLI 或 Skill 依赖。
