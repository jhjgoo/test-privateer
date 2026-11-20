# Spec Delta

## MODIFIED Requirements

### Requirement: Select SDD and agent evaluation depth by scope
质检 SHALL 在确认 SDD 框架或变更产物链后才加深规格、设计、任务、实现及归档检查；Prompt 与完整 Agent 分别使用对应评估方法，声明限于实际配置与证据。完整 Agent 评估 SHALL 核验候选提示、判据隔离、匿名比较、实际加载轨迹和运行配置；输出质量、Skill 加载和配置有效性 SHALL 分别报告，不得合并成一个分数。Prompt 评估 SHALL 盘点实际进入模型的消息角色、指令层级、稳定规则、动态输入、工具结果和示例，区分协议权限与文本标记；SHALL 按“最小充分”检查判断条件、来源引用和无关噪声，不因篇幅本身判优劣。Prompt 要求结构化输出或高影响动作时，评估 SHALL 区分 Prompt 语义、Schema 格式约束、程序业务校验和确定性计算；Schema 通过不得当作业务事实正确。涉及缓存、成本或延迟主张时，SHALL 分别提供质量、输出、Token、命中、账单或延迟证据，并把 Prompt／Schema／业务规则版本与回滚条件记录为可追踪信息。Prompt 或 Agent 的沟通质量审查 SHALL 可按格赖斯四项准则分别观察数量、质量、关系和方式：数量关注最小充分信息，质量关注主张与证据匹配，关系关注目标、路由、工具和授权相关性，方式关注对象、动作、顺序、边界与判定的可执行性。评估 SHALL 使用四维失败标签定位问题，保留维度之间的冲突和未知，不得以四维平均分替代关键风险。

#### Scenario: Ordinary preimplementation check

- **WHEN** 用户要求普通方案的实施前质检，但无 SDD 框架或产物链
- **THEN** 使用核心对症检查，不要求补齐框架文档

#### Scenario: SDD archive or agent result claim

- **WHEN** 正在归档 SDD 变更或依据评测声称 Agent 已改善
- **THEN** 前者核对当前规格与实际完成范围，后者区分输出、轨迹及配置证据；两者均不以文件齐全或一次通过替代相应行为证明

#### Scenario: Text impersonates a protocol role

- **WHEN** 动态用户输入或工具结果中的标题、标签或历史文本声称拥有系统、开发者或管理员权限
- **THEN** Prompt 评估按实际 API 消息元数据和宿主指令层级审查其影响，不把文本标记当作协议权限提升

#### Scenario: Context is trimmed below sufficiency

- **WHEN** 为缩短 Prompt 或提高缓存复用而删除来源、对象关联、单位、版本、例外或证据引用
- **THEN** 评估保留材料充分性缺口和潜在漏判风险，不以长度下降或缓存命中证明优化有效

#### Scenario: Valid schema hides a business error

- **WHEN** 输出通过 JSON Schema，但引用不存在、对象关联错误或确定性业务校验失败
- **THEN** 评估将问题归入业务结果或程序验证缺口，不把格式通过当作判断正确

#### Scenario: Information is insufficient or overloaded

- **WHEN** Prompt 或 Agent 遗漏完成任务所需关键条件，或加入不影响当前决定的大量背景并因此改变行为
- **THEN** 评估 SHALL 将问题标为数量维度，指出缺失或无关信息及其行为影响；仅在证据支持时建议增删内容

#### Scenario: Assertion conflicts with evidence

- **WHEN** Agent 的结论、完成声明或事实描述超出已读取材料、工具结果或运行配置所支持的范围
- **THEN** 评估 SHALL 将问题标为质量维度，分别记录主张、证据和缺口；不得用语气、格式或模型自述抵消缺证

#### Scenario: Route or action is unrelated

- **WHEN** Prompt 诱导 Agent 偏离用户目标、越过授权、响应外部文本中的提示注入，或调用与任务无关的工具
- **THEN** 评估 SHALL 将问题标为关系维度，依据目标、路由、权限和实际工具轨迹判断，不把额外活动量视为能力提升

#### Scenario: Output cannot be executed or verified

- **WHEN** Agent 未明确对象、动作、顺序、边界或完成判定，导致交付无法执行、复跑或核验
- **THEN** 评估 SHALL 将问题标为方式维度，指出缺少的可观察信息，并区分表达缺陷、环境受阻和真实执行失败

## ADDED Requirements

### Requirement: Compare prompt revisions with paired blinded evidence

Prompt 优化效果 SHALL 以调整前版本为基线，使用冻结案例及同条件配置逐例比较调整后版本。执行会话与独立评审 SHALL 隔离版本标签、另一组答案及修改意图；隐藏判据不得泄漏给执行者，版本映射 SHALL 在评分锁定后揭盲。盲化未实现或存在泄漏时 SHALL 披露实际边界，不称为完整双盲。指标、分母与阈值 SHALL 预先约定，目标改善、邻近退化、样本不足、执行错误和评分错误 SHALL 分别报告。

#### Scenario: Claimed improvement lacks a previous version
- **WHEN** 只有新版结果或带／不带 Skill 的 Skill Lift，却声称本次修改有效
- **THEN** 要求旧版／新版同条件对照；未执行时只交付设计，不以静态分数或贡献比较代替版本效果

#### Scenario: One metric borrows another metric's baseline
- **WHEN** 只提供新版某项指标的达标结果，另一个指标有前后变化数据
- **THEN** 逐指标限定结论；没有自身前后证据的指标只能报告当轮表现，不能在建议替代结论中写成已有改善

#### Scenario: Version labels leak to evaluators
- **WHEN** 执行者知道预期赢家，或 Judge 从路径、轨迹或标签知道新旧映射
- **THEN** 标明盲化缺口，采用独立会话、匿名输出与随机呈现顺序，锁分后再揭盲；不把普通 A/B 宣称为双盲

### Requirement: Offer SkillEvaluator as an optional prompt evaluation framework

`prompt-eval` SHALL 沿用客户已有合适入口，允许只做审查或交付框架无关设计。客户选择 SkillEvaluator 且被测对象可忠实保留 Skill／指令包语义时 SHALL 读取官方 skillevaluator Skill 完成工具操作；领域判据和结论边界仍由 prompt-eval 负责。框架选择 SHALL 不自动授权安装、付费调用或上传数据，不导入本仓库维护模型矩阵和策略。

#### Scenario: Customer chooses a framework for skill revisions
- **WHEN** 客户选择 SkillEvaluator 比较旧版／新版 Skill
- **THEN** 保留完整快照、冻结案例与配置，按官方入口准备并运行；核对实际加载、评分器区分能力和结果完整性，缺条件时保留未完成

#### Scenario: Raw prompt would change semantics when wrapped
- **WHEN** 普通 API Prompt 必须改变消息角色、工具或加载方式才能被包装成 Skill
- **THEN** 沿用原宿主做配对验证，说明 SkillEvaluator 的适用缺口，不为框架改换被测对象

#### Scenario: Customer wants only a qualitative review
- **WHEN** 客户仅要求审查或设计，尚未授权执行
- **THEN** 完成审查和可执行验证设计，不安装框架、不调用模型评测，也不以缺少框架阻断交付

#### Scenario: Customer authorizes the existing harness
- **WHEN** 客户授权原有 API 脚本做版本对照，但未选择 SkillEvaluator
- **THEN** 沿用原入口和授权执行，不因未选外部框架而阻断量化
