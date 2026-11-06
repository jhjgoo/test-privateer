# Proposal

## Why

当前 Setup 能记录项目事实，但关键治理项缺失时仍可能宣称“配置已完成”；完整 Test Loop 则在运行中临时补问资产、责任、验证器和并发边界，导致晚阻塞和不可信的初始化结论。完整闭环需要项目级架构先行确认，而普通单项测试仍不应被 Setup 前置化。

## What Changes

- 项目初始化的缺陷入口、测试责任、风险接受和 CI 门禁若影响后续交接与判定，必须取得决定；不能把未知仅写成缺口后宣称相关配置完成。
- 为 Setup 增加完整 Test Loop 就绪契约：关键架构项必须处于“权威来源已确认、用户已确认、明确不适用或明确后续补建”的可判定状态。
- 扩展项目配置模板，记录测试资产根目录、验证器入口、共享资源与并行策略、盲测隔离输出位置、质量责任和风险接受边界。
- Setup 只调查、推荐和确认，不生成 TCO、验证器、测试资产或 CI；缺少真实验证器时明确完整 Loop 执行受阻及恢复路径。
- 完整 Test Loop 启动前执行就绪预检；配置缺失或关键架构未关闭时先进入最小 Setup 确认，不边跑边猜。
- 保留兼容边界：无配置的普通单层测试不强制 Setup；当前宿主子代理能力仍按运行时状态判断，不写入长期项目配置。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `project-test-setup`: 新增完整 Test Loop 就绪契约和初始化完成门禁。
- `test-loop`: 新增完整 Loop 启动前项目就绪预检与进入最小 Setup 的边界。
- `testing-workflow`: 主入口对无配置项目明确区分普通任务与完整 Loop。

## Impact

- `skills/setup-test-privateer/SKILL.md`
- `skills/setup-test-privateer/references/project-profile-template.md`
- `skills/running-test-loop/SKILL.md`
- `skills/test-privateer/SKILL.md`
- `skills/test-privateer/references/artifact-routing.md`
- `tests/test_project_test_setup_contract.py`
- `tests/test_test_loop_contract.py`
- `evals/project-test-setup/README.md`
- `evals/project-test-setup/inputs/`
- `evals/project-test-setup/prepare_fixture.py`
- `evals/test-loop/README.md`
- `evals/test-loop/inputs/`
