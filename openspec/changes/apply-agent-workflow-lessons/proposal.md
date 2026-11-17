# Proposal: Apply Agent Workflow Lessons

## Why

pstack 11 月 release 的有效方向是把子代理共同规则抽成固定入口、只保留能改变未来行动的教训、识别重复特殊分支背后的模型错位。Matt 的新调整也强调区分抽象任务与 CI 接线、让探索留下可复现 findings。现有能力已覆盖大半，但三处仍有最小补强空间。

## What Changes

- 新增盲测子代理共同契约：每个 wave 首行读取同一规则，brief 只写差异，不重复共同约束。
- 错题本候选增加持久性、行动价值和非单例筛选。
- 方案质检增加“反复特判先检查范围／模型／oracle 错位”的断点。
- 测试实验设计内化“减少执行 nuance”：Case 的复杂度由明确字段、入口、脚本或断言承载，质检识别需要经验脑补才能执行的设计缺陷。

## Impact

- `skills/running-test-loop/`
- `skills/maintaining-project-lessons/SKILL.md`
- `skills/checking-solutions/SKILL.md`
- `skills/designing-test-experiments/SKILL.md`
- `skills/challenging-test-designs/SKILL.md`
- `tests/test_agent_workflow_lessons_contract.py`

## Non-goals

- 不引入模型路由、默认模型、PR 流程或宿主专属子代理参数。
- 不精简现有证据、盲测、单一合成者或 OpenSpec 归档要求。
- 不把 CI workflow/job 词汇迁移到测试 Loop；现有 Run／wave 词汇保持不变。
