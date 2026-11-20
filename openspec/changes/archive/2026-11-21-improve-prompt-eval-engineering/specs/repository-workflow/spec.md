## MODIFIED Requirements

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
