# repository-workflow Specification

## Purpose
规定 Test Privateer 仓库如何以 OpenSpec 管理当前契约、活动变更和历史迁移，以及如何区分可复用验证源码与本地过程记录。该流程只约束本仓库维护，不改变分发的 Skill 行为或强制使用方项目采用同一框架。

## Requirements

### Requirement: Maintain one change chain for repository behavior

本仓库行为或流程变更 SHALL 在同一 OpenSpec change 中追溯意图、可观察要求、设计、任务与实际完成范围；实施与验证结束后保留活动 change，只有用户明确确认本次 change 已完成后才同步当前规格并归档。普通错字或失效链接修正可不新建 change。

#### Scenario: Resume implementation with failed evidence
- **WHEN** 继续已有变更时出现失败反证或未实现的原承诺
- **THEN** 更新原 change 的决定与剩余任务，不新建平行账本，不以缩小声明关闭原承诺

#### Scenario: Implementation verified without user confirmation
- **WHEN** 已完成授权范围并核对相应验证与限制，但用户尚未明确确认本次 change 已完成
- **THEN** 交付结果与剩余项，保留活动 change，不把测试通过、任务勾选或 Agent 总结当成用户确认，不同步当前规格或执行归档

#### Scenario: Completed change ready to archive
- **WHEN** 已完成授权范围、核对相应验证与限制，且用户明确确认本次 change 已完成
- **THEN** 记录简短验收结论，经严格校验将 delta 同步到当前规格后归档，不将原始运行日志作为 change 附件

### Requirement: Label retrospective migration honestly

历史回填 SHALL 记录迁移日期、来源提交和范围，仅登记已合并契约；未交付方案和未重跑的行为评测保持明确边界。

#### Scenario: Import pre-OpenSpec development
- **WHEN** 将采用 OpenSpec 之前的已合并能力补录为 archive
- **THEN** 按能力归组并标明回填，不伪造原开发时的 OpenSpec 审批、任务执行和验收记录

### Requirement: Ignore local records without hiding reusable assets

Git 规则 SHALL 排除本地评测输出、日志、审计及旧计划，保留 Skill、测试源码、可复用输入与夹具、判据、用户文档和 OpenSpec；对已跟踪纯记录仅停止跟踪，保留本地内容及 Git 历史。

#### Scenario: Generated output versus fixture evidence
- **WHEN** 同时存在评测 runs 中的输出及 fixture/evidence 中的固定输入
- **THEN** 前者被忽略，后者仍可跟踪；图像夹具和其校验清单也不因扩展名被隐藏

#### Scenario: Previously tracked audit document
- **WHEN** 某纯审计记录已被 Git 跟踪
- **THEN** 将其移出索引并验证本地内容未变；被生产 Skill 引用的长期资料继续跟踪，受影响的共享链接同步整理

### Requirement: Maintain evidence-backed project lessons and rules

本仓库 SHALL 在根 LESSONS.md 维护真实错误、验证缺口与纠正经验，在 AGENTS.md 维护当前协作规则；修改前读取与任务相关的教训。条目区分直接观察与历史记录回填，保持可定位来源、独立事件口径、适用范围与真实状态；有限材料整理不得声明连续历史审查完成。

#### Scenario: Initialize project lessons from bounded evidence
- **WHEN** 用户授权建立本项目错题本与规则，仅有当前 change 和部分历史归档资料
- **THEN** 基于已读资料建立条目和规则指针，保留既有项目要求，标明历史未重跑和未覆盖范围，不虚构复发次数或自动防复发效果

#### Scenario: Consume and update related lessons
- **WHEN** 修改涉及已记录的共享规则、验证或完成声明问题
- **THEN** 读取相关教训并按 AGENTS.md 的动作与检查约束工作，出现新事件时更新原条目及执行机制，保留原始证据而非另造同义规范
