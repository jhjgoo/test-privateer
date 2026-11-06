# Proposal

## Why

Test Privateer 每次进入新项目都需要重新调查测试入口、环境边界、证据位置和质量门槛。缺少稳定的项目配置时，Agent 容易重复提问、猜测命令，或把“配置已保存”误报为“环境已验证”。

## What Changes

- 新增 `setup-test-privateer`，先调查项目事实，再确认无法从仓库确定且会改变测试方式的决定。
- 使用固定项目入口 `.test-privateer/project.md` 保存权威来源指针和项目未记录的已确认补充。
- 覆盖项目范围、测试入口、项目选定的测试框架、环境与安全边界、数据与身份、质量门槛、证据策略、缺陷平台、责任角色和验证器入口。
- 重复运行时更新已有配置，保留人工内容，避免追加重复章节或创建第二套项目测试上下文。
- 回读实际文件并区分配置保存、环境确认、环境验证、测试执行和质量门禁接入状态。
- 让项目测试任务在配置存在时读取该入口；配置不存在时继续沿用现有项目调查流程，不把 Setup 变成强制前置。
- 不安装或擅自选择测试框架，不配置模型，不运行产品测试，不生成完整 TCO、测试分析或用例，也不读取、复制、回显或保存秘密值。

## Capabilities

### New Capabilities

- `project-test-setup`: 定义 Test Privateer 如何调查、确认、保存和复核项目级测试配置。

### Modified Capabilities

- `testing-workflow`: 增加项目初始化的显式路由和可选项目配置入口。

## Impact

- 新增 `setup-test-privateer` Skill、项目配置模板、主入口路由、契约测试和行为评测。
- 项目配置使用方需要先落实 `establish-test-run-asset-lifecycle`，以便引用统一的轮次和证据契约。
- 本 change 不修改业务项目的构建、CI、凭据、测试代码或产品代码。
- 本 change 不替代 `testing/TCO.md`。TCO 继续维护产品与测试空间，项目配置只维护测试工作的项目约定和来源指针。
