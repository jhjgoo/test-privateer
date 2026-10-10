# Proposal

## Why

现有自动化入口能选择单元、接口和页面测试，但接口／页面只交付设计，方法也不够细。用户希望以有来源、有适用边界的方法指导自动化，并在项目缺少 E2E 框架时，按需接入官方 e2e Skill 和框架，完成可复跑的业务测试。

## What Changes

- 将 `designing-test-automation` 调整为原则、方法与路由入口。区分测试范围、操作入口和开发流程，不规定套件比例。
- 新增 `writing-api-tests` 和 `writing-e2e-tests`，借鉴 `writing-unit-tests` 的输入、执行、失败判定与证据交付契约；两个专项支持直接调用。单元测试文件及 TDD 职责保持不变。
- 集成／契约和组件方法保留按需参考，但写清准备、刺激、观察、判定和交付；框架专属接入参考归到 E2E 专项，不重复维护同一执行契约。
- 用户只要求设计时仍交付设计；要求实现时，沿用合适的项目框架。无 E2E 框架且需求适合时，接入官方 e2e Skill，而非维护其副本。
- 接入包含环境核查、测试代码和实际运行证据；缺少条件时交付具体阻塞，不把脚本生成称为接入成功。
- 同步主入口、自校规则和用户文档。用行为样本及受控项目试跑验证选择、接入和证据边界。

**非目标：** 不新增通用执行平台、安装器或一套近义 Skill；不全量迁移已有测试；不把 e2e 设为所有自动化任务的默认工具。不在本次实现性能、完整安全、可访问性和移动端专项方法，也不承诺这些能力已由功能测试覆盖。

## Capabilities

### New Capabilities

- `test-automation`：按所需证据选择自动化方法，复用或接入执行框架，并交付与实际范围一致的结果。

### Modified Capabilities

无。沿用 `testing-workflow` 的阶段授权、`test-artifact-quality` 的表达与证据要求；本 change 在新 capability 中补充自动化专项行为，不重复修改通用契约。

## Impact

- 运行时：自动化方法入口、两个新实施专项、必要参考、`test-privateer` 路由和 `challenging-test-designs` 自校。
- 复用：`writing-unit-tests`、`running-test-sessions`、`assessing-test-confidence` 与回归选择，不接管其职责。
- 文档：README、两份使用指南、项目背景及 OpenSpec 配置中的能力声明和 Skill 数量。
- 验证：既有测试表面契约、自动化行为样本、一个受控本地 Web 夹具。
- 依赖：本 Skill 仓库不新增 e2e npm 运行依赖。使用方项目按授权安装，记录框架与官方 Skill 的版本／来源；已有框架与宿主配置不自动替换。

2026-10-10 第一阶段获准实施并完成技术验证；用户随后要求参考 writing-unit-tests 深化并拆出实施契约。第二阶段已获准实施，并增加 prompt-eval／skill-eval 审计。完成状态以 tasks 为准，旧验证不升级为新结构已验证。
