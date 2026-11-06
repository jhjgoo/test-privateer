# Proposal

## Why

当前 `running-test-loop` 允许同一个 Agent 带着开发过程、修复理由和既有测试结论继续执行测试，容易形成确认偏差，并在多轮 Loop 中重复相同验证。完整测试闭环需要像 pstack 的独立 worker／adversary 一样，由冷启动子代理从质量与测试角度独立发现问题，且只有真实运行证明的 Finding 才进入结论。

## What Changes

- 完整 Test Loop 进入测试发现与执行阶段时，强制启动新的盲测子代理；开发上下文、实现理由、既有 Finding 结果、预期缺陷和评分规则不得传入。
- 为子代理建立最小盲测任务包，只提供测试目标、目标版本、用户可观察契约、项目入口、环境与授权、分配的质量视角，以及不含结果的覆盖排除项。
- 盲测结果封存后，才允许主 Agent 使用实现 diff、开发自测和历史 Finding 做定向回归；盲测阶段与知情阶段不复用同一子代理上下文。
- 子代理只写隔离证据和 handoff，由单一合成者复核真实运行、去重并更新当前 Run ID 和共享资产。
- 为每轮检查增加覆盖指纹与新颖性门槛；没有新风险、状态、路径、Oracle、故障或明确复验目的时，不重复执行相同检查。
- 宿主不能创建冷启动子代理或无法隔离输入时，完整 Loop 标记受阻；只有用户明确接受降级后才能继续，且不得声称完成盲测。
- 增加上下文污染、真实子代理加载、重复验证、证据不足、宿主不支持子代理和高风险扩展等契约测试与行为评测。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `test-loop`: 增加完整 Loop 的盲测子代理、上下文隔离、证据复核、防重复和降级边界。

## Impact

- 更新 `skills/running-test-loop/SKILL.md` 和测试轮次模板，不改变普通单层测试请求的路由。
- 更新 `openspec/specs/test-loop/spec.md` 的行为契约、`tests/test_test_loop_contract.py` 和 `evals/test-loop/`。
- 不引入固定模型、平台或编排框架；使用宿主已有子代理能力，同一模型的新会话也可满足冷启动要求。
- 不把子代理自述当作隔离或执行证据，必须保留实际调度、输入清单、加载轨迹、工具轨迹和产物指针。
- 当前 `add-deepeval-agent-evaluation` change 保持独立，不与本 change 合并。
