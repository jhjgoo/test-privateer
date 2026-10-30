# Tasks

## 1. 评测夹具与红灯基线

- [x] 1.1 增加 shaping-ai-tasks 的自然成对输入和评审判据，覆盖信息刚好足够、关键条件缺失和诱人无关背景，并验证输入不泄漏评测意图
- [x] 1.2 增加 agent-eval／prompt-eval 的自然边界输入，覆盖证据冲突、工具失败后禁止声称成功、外部提示注入和不可执行交付，并验证判据与受测提示隔离
- [x] 1.3 在 `tests/test_eval_skills_contract.py` 先加入四维契约断言并运行，确认基线因目标约束尚不存在而失败

## 2. Skill 最小实现

- [x] 2.1 在 `skills/shaping-ai-tasks/SKILL.md` 增加数量、质量、关系、方式的轻量自校，验证明确请求仍可直达且不删除执行关键条件
- [x] 2.2 在 `skills/prompt-eval/SKILL.md` 增加四类失败标签及“不合并总分”约束，验证每项修正仍要求目标场景、邻近正常场景和配置边界
- [x] 2.3 在 `skills/agent-eval/SKILL.md` 增加轨迹层四维观察和提示注入／工具失败／未执行却声称完成等边界，验证实际加载轨迹仍优先于模型自述
- [x] 2.4 更新契约测试和评测 README 的判据，验证入口、引用、自然任务和证据边界保持一致

## 3. 集成验证与交付

- [x] 3.1 运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_skill_package.py`、`git diff --check`，记录失败与修正结果
- [x] 3.2 运行 `openspec validate 2026-10-30-add-grice-communication-audit --strict --no-interactive`，验证 delta、设计和任务格式完整
- [x] 3.3 按现有协议执行最小真实模型行为评测，记录模型、宿主、读取轨迹、完整输出和失败边界到 `.local/validation/grice-communication-20261030/`；基线与候选的 4 组场景均完成判读，首轮 `gpt-6-astra` 容量超时单独保留
- [x] 3.4 对照原请求核对文件、行为范围、未完成项和活动 change 状态；用户已于 2026-10-30 明确确认本次 change 完成
