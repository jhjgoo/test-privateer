# Tasks

## 1. DeepEval 就绪与授权边界

- [x] 1.1 更新 `setup-test-privateer`，在项目选择 DeepEval 时检查官方 Skill、项目依赖和评测入口，并通过契约测试验证缺失项不会被写成已就绪
- [x] 1.2 更新 `evaluating-agents-with-deepeval` 和主路由，在安装前请求明确确认，并通过契约测试验证拒绝或未确认时保留 `missing_official_skill`

## 2. 行为场景与集成验证

- [x] 2.1 增加一个官方 Skill 缺失的自然 Setup 场景，并由契约测试验证场景、夹具和判据已接入，供后续真实模型评测
- [x] 2.2 运行全量契约测试、Skill 包检查、OpenSpec 严格校验和 diff 检查，记录实际结果并保留活动 change 等待用户确认
- [x] 2.3 按现有协议执行 DeepEval 就绪确认的真实模型评测，保存完整输出、加载轨迹和失败边界；修正已证实问题并只重跑受影响场景

## 验收记录

- 真实模型：`gpt-6.1-sol`，Codex CLI `0.166.0`，high reasoning，独立临时项目，`workspace-write`。
- 首轮 5 场景中 3 场通过；2 个待确认场景暴露“自行规划项目内 Skill 副本”和等待态／环境错误混用。
- 修正后只重跑受影响场景和自有框架邻近场景；最终选定的 5 个场景均通过，原始失败和中间复测继续保留在 `.local/validation/deepeval-readiness/attempts/`。
