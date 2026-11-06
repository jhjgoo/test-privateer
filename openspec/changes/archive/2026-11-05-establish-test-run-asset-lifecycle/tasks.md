# Tasks

## 1. 建立轮次资产契约

- [x] 1.1 新增 `skills/test-privateer/references/test-run-template.md`，定义 Run ID、轮次状态、授权、退出条件和资产指针，并用契约测试验证字段完整且不复制分析或用例正文
- [x] 1.2 更新 `skills/test-privateer/references/artifact-routing.md`，写明轮次记录的创建门槛、默认位置、状态分工和历史保留规则，并用短任务样本验证不会强制建档
- [x] 1.3 新增或扩展 `tests/test_test_run_lifecycle_contract.py`，验证 Run ID、单一合成者、状态集合、恢复和新版本新轮次等契约

## 2. 接入执行、回归和报告

- [x] 2.1 更新 `skills/running-test-sessions/SKILL.md`，让人工检查点、恢复点和决策日志引用当前 Run ID，并通过契约测试验证已完成轮次不会被改回执行中
- [x] 2.2 更新 `skills/selecting-regression-tests/SKILL.md` 和 `skills/assessing-test-confidence/SKILL.md`，让选择与报告绑定当前轮次、版本和证据适用性，并验证旧报告不能冒充本轮结果
- [x] 2.3 更新 `skills/designing-test-experiments/references/test-cases-template.md`，让执行批次记录 Run ID 和目标版本，同时保留每次运行的历史结果，并用模板契约测试验证
- [x] 2.4 在共享规则中补充证据敏感性、保留期限、清理前保存和资产失效状态，并用凭据、临时 CI Artifact 和规则变化样本验证边界

## 3. 验证真实行为

- [x] 3.1 新增 `evals/test-run-lifecycle/` 的自然输入和判据，覆盖长任务建档、短任务不建档、暂停恢复、旧报告残留、敏感证据和并行归并
- [x] 3.2 按现有协议运行真实模型行为评测，记录完整输出、Skill 加载轨迹、文件操作和失败边界，并将原始记录保存到 `.local/validation/test-run-lifecycle/`
- [x] 3.3 根据评测修正 Skill 和模板后，运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_skill_package.py`、`openspec validate establish-test-run-asset-lifecycle --strict --no-interactive`、`openspec validate --all --strict --no-interactive` 和 `git diff --check`
- [x] 3.4 用户已确认完成；同步当前规格并归档，再同步更新本地 Skill
