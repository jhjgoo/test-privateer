# Tasks

## 1. 建立失败基线与评测材料

- [x] 1.1 新增 `evals/deepeval-agent-evaluation/` 的自然输入、相邻正常输入和评审判据，覆盖显式选择 DeepEval、自有框架绕过、工具失败与 Judge 冲突、无计划轨迹、私有轨迹、缺少依赖和 Judge 不可用，并验证候选可见材料不泄漏评测意图
- [x] 1.2 在不提供 DeepEval 专项 Skill 的隔离候选目录运行基线场景，记录完整输出、实际 Skill／文件加载、工具轨迹和具体失败理由到 `.local/validation/deepeval-agent-evaluation/baseline/`，确认至少一个目标问题真实出现后再编写 Skill

## 2. 新增 DeepEval 质量约束并接入官方 Skill

- [x] 2.1 新增 `skills/evaluating-agents-with-deepeval/SKILL.md`，只解决框架触发、官方 Skill 交接、证据、Oracle、授权和失败分类，并用契约测试验证未选择 DeepEval 时不会触发
- [x] 2.2 引用 Confident AI 官方 `deepeval`、`deepeval-tracing` 和 `deepeval-otel` Skills，删除本地 API 映射参考；验证专项不复制指标类、命令、模板或数据集教程，官方 Skill 缺失时返回 `missing_official_skill`
- [x] 2.3 更新 `skills/agent-eval/SKILL.md` 和 `skills/test-privateer/SKILL.md` 的最小 handoff／路由，验证显式 DeepEval 请求和项目已选 DeepEval 会进入专项，自有框架和普通 Agent 评测继续走原路径
- [x] 2.4 更新 Skill 包计数、用户入口或开发文档中受新增 Skill 影响的内容，并运行包完整性测试确认 frontmatter、引用、路由和目标平台检查仍通过

## 3. 验证真实框架和模型行为

- [x] 3.1 在隔离临时项目中锁定并记录一个实际 DeepEval 版本，按该版本官方文档运行已知正例、已知反例、工具失败、Judge 不可用和无上传授权场景；验证原始证据未被派生结果覆盖，原始记录保存到 `.local/validation/deepeval-agent-evaluation/framework/`
- [x] 3.2 按现有 Agent 行为协议运行真实模型评测，记录完整输出、Skill 加载轨迹、工具与文件操作、模型和配置、DeepEval 指标结果及 `pass`／`agent_failure`／`environment_error`／`invalid_case` 边界，并保存到 `.local/validation/deepeval-agent-evaluation/model/`
- [x] 3.3 按纠偏后的官方 Skill 协作边界，复跑官方 Skill 可用、官方 Skill 缺失、自有框架绕过、确定性冲突和私有轨迹场景；根据实际失败最小修正质量约束，并确认本包没有接管 DeepEval 实施

## 4. 集成验收与用户确认

- [x] 4.1 运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_skill_package.py`、`openspec validate add-deepeval-agent-evaluation --strict --no-interactive`、`openspec validate --all --strict --no-interactive` 和 `git diff --check`，记录实际通过项和未运行项
- [x] 4.2 交付实现、框架版本、评测范围、失败边界和剩余风险，保留活动 change，等待用户明确确认后再同步规格、归档和同步本地 Skill
