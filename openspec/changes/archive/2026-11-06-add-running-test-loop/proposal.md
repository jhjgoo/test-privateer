# Proposal

## Why

现有主入口能按阶段路由测试分析、用例、执行、调查和信心评估，但用户仍需多次推动各阶段。需要一个受授权、可停止、可恢复的编排入口，将现有专项连接成完整测试闭环，同时保持产品代码只读和证据边界。

## What Changes

- 新增 `running-test-loop`，在一次明确的测试授权内连续推进分析、用例、执行、调查、回归和报告。
- 启动时固定测试对象、目标版本、授权、禁止动作、预算和退出条件，并复用统一 Run ID。
- 复用现有专项 Skill 和阶段 handoff，不在 Loop 中复制测试方法、模板或判定规则。
- 按风险选择最小充分的 API、E2E、UI、Agent、单元、集成或其他检查，并沿用项目 Setup 选定的框架，不要求每轮运行全部测试层级。
- 根据新证据扩展、收缩或停止测试，并记录转向依据；到达退出条件、预算、人工检查点或安全边界时停止。
- 允许在授权范围内创建或修正测试代码、夹具、驱动和测试文档，但禁止修改被测产品代码。
- 修正变化分析中的执行授权冲突。未获得执行授权时只核对已有证据，获得 Loop 授权后才运行测试。
- 最终使用 `assessing-test-confidence` 输出有范围的测试报告，不把 Loop 完成、工具成功或通过率写成发布批准。

## Capabilities

### New Capabilities

- `test-loop`: 定义完整测试闭环的启动契约、阶段编排、证据驱动转向、停止条件和只测试边界。

### Modified Capabilities

- `testing-workflow`: 增加完整 Test Loop 的显式路由，并分离分析活动与产品执行授权。

## Impact

- 新增 `running-test-loop` Skill，并更新 `test-privateer` 和 `analyzing-change-for-testing` 的路由与授权表达。
- 本 change 依赖 `establish-test-run-asset-lifecycle` 和 `add-test-privateer-project-setup` 的契约与产物，不重复定义项目配置、Run ID、证据字段或资产失效规则。
- 新增真实模型行为评测，覆盖 API-only、UI、人工检查点、工具失败、暂停恢复、预算停止和错误完成声明。
- 本 change 不自动修复产品缺陷，不批准发布，不自动创建或关闭外部缺陷。
