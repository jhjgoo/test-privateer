# Spec Delta

## ADDED Requirements

### Requirement: Generate a verified project product driver
当项目需要可持续验证真实产品行为且用户授权生成验证资产时，`designing-test-automation` SHALL 先从仓库、现有测试、运行文档和环境配置调查用户可触达表面、启动方式、可编程驱动方式、可观察证据、隔离能力和清理方式。生成物 SHALL 复用既有 harness；缺少时 SHALL 选择项目技术栈的最小可行驱动，不默认引入新框架。

生成的项目验证器 SHALL 至少说明启动与就绪判定、健康检查、真实用户路径、证据与保存位置、实例隔离、失败保留证据和清理方式；SHALL 标明授权与不可自动化边界。交付前 SHALL 实际驱动一条已映射用户路径并保留证据、确认清理后证据仍存在；未实测的生成物 SHALL 标注为草案，不得称为可用验证器。

#### Scenario: Existing harness is available
- **WHEN** 项目已有 Playwright、API、CLI 或组件 harness
- **THEN** SHALL 复用其启动、驱动和证据方式，只补齐缺口，不另建平行框架

#### Scenario: Generated driver is not run
- **WHEN** 验证器生成后未真实驱动任何用户路径
- **THEN** SHALL 交付为草案并列出启动、驱动、采证和清理的未验证项

#### Scenario: Shared environment cannot be isolated
- **WHEN** 两个验证实例可能写入同一共享数据或会话
- **THEN** SHALL 明确隔离方式或拒绝双实例驱动，不破坏用户现有会话
