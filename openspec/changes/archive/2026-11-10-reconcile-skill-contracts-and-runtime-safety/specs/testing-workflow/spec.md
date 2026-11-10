## MODIFIED Requirements

### Requirement: Verify agent behavior from actual load traces
Agent 行为评测 SHALL 使用自然任务提示，将隐藏判据、答案、预期缺陷、候选身份及比较标签与候选可见材料隔离。是否污染 SHALL 按内容是否泄漏评测意图或标准答案判断，MUST NOT 仅因真实任务、目录、字段或 Skill 原名含 test、eval、score 等词就判为泄漏或强制改名。判据 SHALL 只提供给评审；版本比较 SHALL 使用匿名标签，评审 SHALL 在同一尺度下判读。

结论 SHALL 区分最终输出、实际读取的 Skill／文件、工具轨迹和运行配置；SHALL NOT 以候选自述替代加载轨迹，也 SHALL NOT 跨项目扫描私有会话记录。失败 SHALL 保留为可诊断结果，不得为汇总方便改成通过。

#### Scenario: Candidate sees an organic task
- **WHEN** 评测候选收到任务提示
- **THEN** 提示、目录和文件名 SHALL 表现自然任务语境，不提示这是评测或比较

#### Scenario: Skill load is claimed
- **WHEN** 候选自称读取了某 Skill 或参考
- **THEN** SHALL 以当前授权内轨迹或可观察文件访问证据核验；无证据时按未确认加载处理

#### Scenario: Judge compares variants
- **WHEN** 评审比较多个版本输出
- **THEN** SHALL 只见匿名标签并使用同一判据；候选身份不进入评审上下文

#### Scenario: Natural testing vocabulary remains visible

- **WHEN** 任务需要读取 test-privateer、项目 tests 目录或真实业务 score 字段
- **THEN** 评测 SHALL 保留自然名称和执行所需信息，不因词面命中而删改任务或认定污染

#### Scenario: Innocently named input leaks hidden expectations

- **WHEN** 候选输入虽没有评测关键词，却含隐藏判据、预期缺陷或哪一版本应获胜的提示
- **THEN** 评测 SHALL 将该信息移出候选可见范围；已受污染的尝试记录为无效或受限证据，不作为盲测通过结果


### Requirement: Route DeepEval agent evaluation only when selected

当用户明确调用 DeepEval Agent 评测，或项目配置／当前权威来源选择 DeepEval 且任务需要建立、运行、审查或修正 Agent 评测时，主入口 SHALL 路由到 `evaluating-agents-with-deepeval`。该专项 SHALL 先继承 `agent-eval` 已固定的质量主张、场景、Oracle 和证据协议，再把 DeepEval 实施交给 Confident AI 官方 Skills；不得从框架指标重新定义业务目标，也不得在本包复制官方实现教程。

没有选择 DeepEval 时，普通 Agent 测试设计、评估审查、版本比较和失败归因 SHALL 继续使用 `agent-eval` 或项目自有框架。官方 DeepEval Skill 缺失时，Agent SHALL 说明官方来源、安装对象和影响并询问用户是否安装；用户尚未决定且尚未运行评测时，当前宿主所需官方 Skill 的就绪状态 SHALL 标为 `awaiting_install_confirmation` 并停在一个安装确认问题；该状态不得写入项目配置长期状态，也不得作为已执行评测的结果或同时写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后才可使用宿主已有安装能力，安装目标由该能力和用户选择决定。拒绝、宿主不支持安装或安装后仍不可读时，SHALL 报告具体缺口并降级到仍可执行的通用评测工作，不得凭记忆补写实现、静默安装、自行复制到项目目录、登录、上传或替换项目框架。

#### Scenario: Explicit DeepEval request

- **WHEN** 用户明确要求使用 DeepEval 为当前 Agent 建立或运行评测
- **THEN** 主入口 SHALL 路由到 DeepEval 质量约束，再由其调用官方 `deepeval` Skill；该请求只代表本轮框架选择，不要求项目永久迁移

#### Scenario: Generic agent evaluation request

- **WHEN** 用户只要求设计 Agent 测试或审查现有评估，项目没有选择 DeepEval
- **THEN** 主入口 SHALL 使用通用 `agent-eval`，不加载 DeepEval 专项

#### Scenario: Official DeepEval skill is unavailable

- **WHEN** 项目选择 DeepEval，但当前宿主缺少官方 `deepeval` Skill
- **THEN** Agent SHALL 先标为 `awaiting_install_confirmation` 并询问是否安装，在明确确认前不安装或自行选择项目内安装位置；若仍不可用，则保留可完成的场景、Oracle 和原始证据工作并标记 `missing_official_skill`

## ADDED Requirements

### Requirement: Separate handoff authorization from execution progress

阶段交接 SHALL 分别记录获准动作、权限边界及可定位来源，以及实际完成和未完成工作。执行中或已完成只 SHALL 描述进度，MUST NOT 作为执行授权的依据；SHALL 复用已有交接字段，不新增平行状态账本。

读取旧交接时 SHALL 将执行许可字段中的未开始、执行中、已完成等进度值还原为进度信息，并从用户指令、项目授权或其他有效来源核对动作范围。不能恢复授权依据且动作需授权时 SHALL 保留相应阻塞，同时继续不依赖该许可的工作。

#### Scenario: Old handoff says completed without an authorization source

- **WHEN** 旧交接的执行许可仅写已完成，当前任务未授权启动服务或再次运行产品测试
- **THEN** Agent SHALL 将已完成理解为历史进度，核对原始授权，不以该字段为由重新执行

#### Scenario: Valid authorization survives a cold handoff

- **WHEN** 交接保留了仍有效的执行授权、范围、限制及来源，任务尚未完成
- **THEN** 新会话 SHALL 沿授权继续相应动作，不因换会话重复请求相同许可，也不扩大原有边界


### Requirement: Discover automation capabilities through skill metadata

自动化专项的名称和 description SHALL 准确覆盖既有方法选择、Harness／项目验证器生成及维护能力，并与主入口路由、正文触发和实际交付一致。发现性验证 SHALL 先提供自然需求及可用名称／描述，再核对实际选择和加载路径，MUST NOT 通过直接提供目标 Skill 全文来替代入口发现验证。

#### Scenario: User asks to create a project verifier

- **WHEN** 用户描述需要可持续驱动真实产品并保留证据的验证资产，当前仅可见 Skill 名称和描述
- **THEN** Agent SHALL 能识别 designing-test-automation 为适用入口，随后按实际任务加载生成方法，不自行创建重复专项

#### Scenario: User asks to maintain an existing verifier

- **WHEN** 用户描述已有验证器与当前产品不一致，需要维护其驱动和证据能力
- **THEN** Agent SHALL 从元数据识别同一专项并加载维护方法，不误路由为仅选择测试框架
