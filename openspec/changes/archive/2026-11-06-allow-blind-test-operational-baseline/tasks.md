# Tasks

## 1. 固定操作基线边界

- [x] 1.1 更新 `tests/test_test_loop_contract.py`，断言稳定的全局／项目规则、Skill 和 CLI 不构成污染，同时保留开发会话与既有结果隔离要求，并运行目标测试
- [x] 1.2 在 `evals/test-loop/` 增加稳定操作基线场景和判据，确认读取全局 RTK、项目规则、Skill 与 CLI 不被错误判为环境失败

## 2. 修正 Skill 与模板

- [x] 2.1 更新 `skills/running-test-loop/SKILL.md`，按内容区分稳定操作基线与任务特定开发上下文，并运行目标契约测试
- [x] 2.2 更新 `skills/test-privateer/references/test-run-template.md`，记录稳定操作基线和被隔离的开发材料，且不要求复制完整系统提示词

## 3. 纠正判读并验证

- [x] 3.1 复核首轮真实轨迹，纠正“读取全局 RTK／项目规则即环境错误”的判读并保留真正失败边界
- [x] 3.2 运行全量单元测试、Skill 包检查、OpenSpec 严格验证和 `git diff --check`

## 4. 交付与确认

- [x] 4.1 交付修正范围和证据，保留活动 change，等待用户确认后再同步规格、归档和同步本地 Skill
