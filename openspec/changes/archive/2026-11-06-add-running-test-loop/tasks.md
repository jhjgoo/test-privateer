# Tasks

## 1. 建立 Loop 编排入口

- [x] 1.1 新增 `skills/running-test-loop/SKILL.md`，实现启动契约、阶段状态机、单一合成者、handoff 合成、回边条件和停止条件，并用契约测试验证不复制专项方法
- [x] 1.2 更新 `skills/test-privateer/SKILL.md`，将完整测试链请求路由到 `running-test-loop`，并验证单项 API、E2E、UI、执行和报告请求继续直达专项
- [x] 1.3 增加前置契约检查，使 Loop 复用 `.test-privateer/project.md` 和当前 Run ID；缺少前置 change 时明确受阻，不生成临时替代格式

## 2. 收紧授权和执行边界

- [x] 2.1 更新 `skills/analyzing-change-for-testing/SKILL.md`，将无授权时的行为改为核对已有测试和建议执行范围，并用契约测试验证分析请求不会运行产品测试
- [x] 2.2 在 Loop 中接入 API、E2E、UI、Agent 评测、自动化设计、执行、调查、回归和信心评估 handoff，并用路由测试验证只选择当前风险需要且符合项目框架约定的测试方法、框架专项只在匹配时加载，且最终报告绑定当前 Run ID
- [x] 2.3 落实产品代码只读边界，允许获准的测试资产修正，并用产品缺陷和验证器漂移两个场景验证行为不同
- [x] 2.4 接入人工检查点、暂停恢复、决策日志、预算和退出条件，并验证重试、受阻和完成状态不会被写成通过

## 3. 验证真实行为

- [x] 3.1 新增 `evals/test-loop/` 的自然输入和判据，覆盖 API-only、UI、项目选定的 Agent 评测框架、框架专项缺失、已有用例复用、人工检查点、工具失败、重试、预算停止、暂停恢复、产品代码只读和单层请求绕过
- [x] 3.2 按现有协议运行真实模型行为评测，记录完整输出、Skill 加载轨迹、工具轨迹、文件操作和失败边界，并将原始记录保存到 `.local/validation/test-loop/`
- [x] 3.3 根据评测修正 Loop 和相关入口后，运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_skill_package.py`、`openspec validate add-running-test-loop --strict --no-interactive`、`openspec validate --all --strict --no-interactive` 和 `git diff --check`
- [x] 3.4 交付实现、评测范围和剩余风险，保留活动 change，等待用户明确确认后再同步规格和归档

## 4. 收紧阶段推进与定向返工

- [x] 4.1 参考公司 dev skills 的真实状态恢复、产物门禁和定向返工，给当前阶段增加输入指针、当前缺口、预期权威产物、完成证据和下一动作，不引入第二套状态机
- [x] 4.2 增加“阶段自述完成但权威产物缺失”和“后期失败只回最近责任阶段”两个自然场景，并更新契约测试
- [x] 4.3 按相同模型与记录协议运行两个新增场景及已有用例复用、暂停恢复、人工检查点、预算停止、单层绕过五个邻近回归；保留完整输出、加载轨迹、工具轨迹、文件差异和失败边界
- [x] 4.4 根据结果核对是否需要继续修正；本轮 7 个有效场景均通过，没有观察到需要新增规则的 Agent 失败，随后完成全量静态验证
