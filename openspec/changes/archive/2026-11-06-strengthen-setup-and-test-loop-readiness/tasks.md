# Tasks

## 1. 规格与设计

- [x] 1.1 创建 OpenSpec 变更包，并通过 `openspec validate strengthen-setup-and-test-loop-readiness --strict --no-interactive`

## 2. Setup 实现

- [x] 2.1 在 `setup-test-privateer` 和项目配置模板中落地完整 Loop 就绪契约，并通过项目配置契约测试
- [x] 2.2 增加缺失治理项和缺失验证器的评测场景与夹具，并通过夹具生成测试

## 3. Loop 接入

- [x] 3.1 在 `running-test-loop` 中落地启动预检和最小 Setup 边界，并通过 Test Loop 契约测试
- [x] 3.2 增加无配置完整 Loop、旧 Run 恢复和无配置单层测试的行为评测场景说明

## 4. 验证与交付

- [x] 4.1 运行 `python3 -m unittest discover -s tests -v`，确认全部通过
- [x] 4.2 运行 `python3 scripts/check_skill_package.py`、`openspec validate --all --strict --no-interactive` 和 `git diff --check`
- [x] 4.3 保留活动 change，交付改动、验证和剩余风险，等待用户确认

## 验证记录（2026-11-06）

- 全量单元／静态契约检查 70/70 通过；Skill 包检查 30 项通过。
- 本 change 严格校验通过；当前规格与活动 change 共 13 项校验通过；`git diff --check` 通过。
- 新增夹具可在临时目录生成；验证器未确认与已确认延期两场景复用相同项目材料，仅用户决定不同。
- 独立上下文复核发现并修正了 `blocked` 重复确认、延期样本缺少确认、旧 Run 恢复顺序和门禁输入泄漏判据的问题。
- 静态检查本身不证明候选模型会遵守就绪门禁；真实模型行为评测另见下方记录。
- 活动 change 保留；原交付时未同步当前规格、归档、同步本地 Skill、提交或推送。

## 真实模型行为评测（2026-11-06）

- [x] 六个有效场景按隔离协议执行：治理缺口、验证器未确认、验证器已确认延期、首次完整 Loop、旧 Run 无配置恢复、普通单项接口测试。
- [x] 保存完整输出、实际 Skill 加载轨迹、工具轨迹、文件差异、状态和哈希；索引见 `.local/validation/setup-loop-readiness/README.md`。
- [x] 六场均为 `pass`；首轮运行器夹具错误单列为 `environment_error`，未计入模型行为结论。
- [x] 未发现需要修正的 Skill 行为失败；保留 `blocked`、旧 Run 恢复和普通短路径的失败边界。
- [x] 活动 change 保留，等待用户确认；未同步规格、归档、提交或推送。

## 本地验证安装（2026-11-06）

- 用户要求先同步本地 Skill 再自行验证；已将 `setup-test-privateer`、`running-test-loop` 和 `test-privateer` 的本次改动文件更新到 `~/.agents/skills/`，并逐目录核对一致。
- 本次仅为验证用的本地同步；活动 change 未归档，当前规格未同步，未提交或推送。

## 归档确认（2026-11-06）

- [x] 用户明确确认 change 已完成；已同步当前规格并归档。
- [x] 归档后重新同步 `setup-test-privateer`、`running-test-loop` 和 `test-privateer` 到本地 Skill，并核对三个目录一致。
- [x] 未提交或推送；真实模型行为结论仍限于 `.local/validation/setup-loop-readiness/README.md` 记录的模型、宿主和场景范围。
