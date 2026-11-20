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

### Requirement: Validate repository skills with SkillEvaluator

本仓库 SHALL 使用官方 skillevaluator Skill 与固定版本 CLI 作为维护验证器。新增或实质修改 Skill／共享参考时 SHALL 对实际受影响 Skill 运行完整无 LLM Tier 1 及既有契约检查；行为变化 SHALL 补实际行为回归，优化效果 SHALL 以同条件旧版／新版比较支持，Skill 贡献主张 SHALL 补无 Skill 基线。验证资产留在仓库 evals 中，原始记录保留在忽略目录；本验证器不向发布包新增 Skill 或自动接入消费方项目。prompt-eval 可提供客户主动选择的外部框架引用，但 SHALL 不将仓库维护配置作为客户依赖。

#### Scenario: Static score without behavior evidence
- **WHEN** quality-check 得分通过，但没有完整静态门禁或所需行为评测
- **THEN** 只报告快速静态检查，保留相应验证未完成，不声明优化有效

#### Scenario: Compare an optimization
- **WHEN** 维护者需要判断候选 Skill 是否优于旧版
- **THEN** 使用冻结的同一任务、输入、模型、宿主与判据比较旧版／新版，并分离激活、结果和运行错误，不以单独的带／不带 Skill 比较替代版本比较

#### Scenario: Runtime prerequisites unavailable
- **WHEN** 缺少凭据、沙箱、经审阅的数据集或实际轨迹
- **THEN** 保存受阻证据与解除动作，所需 Tier 3 验收保持未完成，不降级为静态通过

#### Scenario: Keep verification outside the product package
- **WHEN** 为仓库接入或更新 SkillEvaluator
- **THEN** 官方 Skill 由维护者宿主读取，项目规则指向验证协议，发布包 Skill 数量和自动安装行为保持不变；客户选择外部框架时按 prompt-eval 接入参考执行，不继承维护模型矩阵、策略或网关配置

#### Scenario: Adapt optional metadata without bypassing checks
- **WHEN** 默认策略要求现有 Skill 未提供的可选作者元数据
- **THEN** 项目策略只将 author_missing 保留为非阻断提示，报告所用策略及 digest；必填字段、目录名称、安全和许可证检查保持原判定，反例验证错误元数据仍会失败

#### Scenario: Execute official Tier 3 with an existing gateway
- **WHEN** 使用已有兼容网关运行官方 Tier 3
- **THEN** 显式记录 provider、Agent/Judge 模型、执行后端及隔离边界，验证真实推理和执行环境连通后执行双组案例；local 仅用于可信 Skill，密钥不进入项目配置，所需轨迹缺失、任务失败和判读错误保留真实状态，不视为默认通过

#### Scenario: Run the default Codex behavior matrix
- **WHEN** Codex CLI 执行行为评测且维护者未追加其他模型
- **THEN** 默认同时运行 GPT-5.6-SOL 与 GLM-5.3 的完整双组；维护者追加模型时新增模型与默认组一并运行，不得用追加模型替换默认矩阵

#### Scenario: Aggregate score masks a failed task
- **WHEN** 已标注反例或实际任务的关键结果失败，但评分器总分或命令退出码通过
- **THEN** 保留原始评分与反例，将汇总门禁视为尚未通过校准；项目验收不得用总分抵消关键结果、必需断言或安全失败
