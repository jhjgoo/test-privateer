# Tasks

## 1. 固定失败行为与契约

- [x] 1.1 在 `tests/test_test_loop_contract.py` 增加盲测子代理、上下文排除、覆盖指纹、单一合成者和无子代理受阻的失败断言，并运行目标测试确认当前 Skill 因缺少规则而失败
- [x] 1.2 在 `evals/test-loop/inputs/` 增加开发上下文污染、重复 wave、无子代理宿主和高风险 fan-out 自然场景，在 `evals/test-loop/README.md` 固定必须观察的调度、输入、轨迹和证据判据

## 2. 实施盲测子代理 Loop

- [x] 2.1 更新 `skills/running-test-loop/SKILL.md`，加入盲测发现、知情回归、冷启动输入排除、风险分级 fan-out、证据复核和严格降级边界，并运行目标契约测试确认通过
- [x] 2.2 更新 `skills/test-privateer/references/test-run-template.md`，增加盲测 wave 索引、输入披露边界、任务包哈希、覆盖指纹和隔离证据指针，并用模板契约测试确认不复制原始 prompt 或证据正文
- [x] 2.3 核对主入口和相邻专项，确认普通单层请求不强制子代理、开发 Loop 必须进入盲测门槛、自有框架和现有授权边界保持不变

## 3. 验证真实行为

- [x] 3.1 按现有协议运行开发上下文污染、重复 wave、无子代理宿主、高风险 fan-out 和单层绕过场景，记录完整输出、子代理调度、候选输入、Skill 加载、工具轨迹、文件差异和失败边界到 `.local/validation/test-loop/`
- [x] 3.2 根据真实失败最小修正 Skill、模板和判据，只重跑受影响场景及相邻正常场景
- [x] 3.3 运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_skill_package.py`、`openspec validate enforce-blind-subagent-test-loop --strict --no-interactive`、`openspec validate --all --strict --no-interactive` 和 `git diff --check`

## 4. 交付与确认

- [x] 4.1 交付实现、真实子代理评测范围、失败边界和剩余风险，保留活动 change，等待用户明确确认后再同步规格、归档和同步本地 Skill
