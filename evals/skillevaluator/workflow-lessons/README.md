# 工作流教训收尾回归

用于 `apply-agent-workflow-lessons`，不添加产品 Skill。`cases.json` 按受影响 Skill 保存一个组合案例；暂存为各 Skill 的 `evals/evals.json` 时包成 `{"skill_name": "...", "evals": [case]}`，复用[现有配置](../prompt-eval/config.yml)。

来源与判据：

| Skill | 来源 | 目标与相邻保护 |
| --- | --- | --- |
| running-test-loop | 原 change 的共享任务包场景；`evals/test-loop/inputs/high-risk-fanout.md`、`single-stage-bypass.md` | 实际写两份 brief，首行共用可访问契约、差异信息完整；单层请求不进入 Loop |
| maintaining-project-lessons | 原 change 的偶发环境场景；`evals/project-lessons/cases.md` 的高后果单次例外；Skill 原有坏 JSON 教学示例 | 偶发状态不晋升；有已确认约束和证据的高后果单次事件不被机械排除 |
| checking-solutions | `evals/checking-solutions/inputs/shared-seam-patch.md`、`legitimate-local-rule.md` | 重复特判回到共同边界；合法局部分支保持 |
| designing-test-experiments | `evals/test-surface-language/input.md` | 明确准备、动作、观察与 oracle；缺状态入口不虚构可执行 |
| challenging-test-designs | 同上及原 change 的隐式经验判定场景 | 识别脑补与条件缺口；充分的短 Case 不扩写 |

本轮将已维护场景组合成最小回归，不宣称覆盖全部能力。方案、教训建议和用例审查按文字交付判定；Loop 案例按真实写入文件和读取轨迹判定，只覆盖任务包准备，不证明子代理调度、产品测试或整轮闭环通过。

旧版为 `b03fe30^`，新版为当前受测快照。两版保留完整 `skills/` 布局、引用和相同冻结案例，在独立暂存目录运行。使用官方 SkillEvaluator 0.9.0、Codex local、默认两模型、固定 Judge、每案例一次；首轮每个 Skill × 两版本 × 两模型，共 20 次执行，另有 Judge 调用。失败修正只对受影响 Skill 另行比较，保存版本与预算，不混作同一轮。不设无 Skill 组，不计算贡献。公开的案例与判据不放入执行者可读的产品输入。

审阅后冻结输入，再执行；核对官方分数、实际读取、最终回答和文件动作。缺失评分不记零分，业务失败不以平均分抵消。输出路径、旧新映射及轨迹可能暴露版本，不能称完整双盲；一次代表案例只能支持有限回归或方向性观察。

Loop 的临时工作区可能在运行结束后清理，应在清理前保留真实任务文件及共同引用可达性，或保留包含完整正文的原始工具响应。Judge 看到的截断轨迹不能代替这些产物；`not_checked`、评分超时及独立复核分别记录，不改写官方分数。

Loop 的生成器另由 `tests/test_blind_brief_generator.py` 在临时目录验证引用解析、不运行测试入口、既有文件保持、重复执行、非命令入口与专有条件，以及路径规范化的工作区边界。这些确定性检查不替代受测 Agent 实际加载、调用与产物审查。
