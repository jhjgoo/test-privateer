# test-automation Specification

## Purpose
规定自动化入口如何根据业务风险和所需证据选择方法，并在授权范围内将设计交给合适的实现工具。覆盖不同测试范围的判断、既有框架复用、无框架的 E2E 接入，以及可核查的执行交付，避免工具选择替代测试设计。

## Requirements

### Requirement: Provide directly usable implementation contracts

接口与 E2E 实施 SHALL 分别提供可直接调用的专项 Skill，明确任务分支、输入事实、真实观察边界、独立预期、首个有区分力的用例、运行结果处理及交付证据。专项 MUST 保留项目已有工具与授权边界，不要求先经过完整策略流程，也不强制套用单元测试的单次 Act 或 RED。

#### Scenario: An API implementation task is called directly
- **WHEN** 用户直接要求编写并验证接口测试，已有请求合同、数据准备与获准环境
- **THEN** 接口专项核实调用身份、初始状态、请求、独立结果观察和预期来源，沿用工具编写并运行目标保护
- **AND** 业务断言、准备或环境错误分别报告；源码不可读本身不阻止已具备条件的黑盒接口测试

#### Scenario: A journey needs multiple actions
- **WHEN** 一条已选旅程需要多个操作才能完成业务目标
- **THEN** E2E 专项保留必要操作、真实链路与关键结果断言，不为套单元测试模式拆断旅程
- **AND** 环境和数据隔离可核查，已有框架继续使用，组件模拟结果不冒充完整旅程证据

#### Scenario: A direct request is limited to design or code
- **WHEN** 用户仅要求设计，或允许编写代码但不允许运行
- **THEN** 专项交付对应产物与缺口，不安装或启动超出范围的工具，不填写未发生的运行结果

#### Scenario: An existing behavior passes on the first run
- **WHEN** 新增的是既有行为保护且首次通过
- **THEN** 不强制制造 RED；在安全可逆条件下验证目标错误能被发现，恢复后复跑，无法验证时明确限制

#### Scenario: A failed test leaves data behind
- **WHEN** 执行失败或清理本次资源失败
- **THEN** 先保留与失败关联的必要证据，只清理本次拥有的资源，并分别报告业务检查结果与环境遗留

### Requirement: Select automation by evidence and real boundaries

自动化入口 SHALL 根据目标行为、判定依据、必须保留的真实依赖及反馈成本选择测试范围。API／页面入口、测试范围、TDD 流程和质量目标 MUST 分别理解；不得用工具名称或固定测试比例替代选择理由。

#### Scenario: A narrow rule needs unit protection
- **WHEN** 目标是计算或状态规则，现有公开边界足以验证
- **THEN** 复用单元测试入口，保留其真实符号、预期和验证方式，不引入浏览器或把 TDD 当成另一层测试

#### Scenario: An API test crosses selected dependencies
- **WHEN** 请求经 API 发起，但可能经过真实或模拟依赖
- **THEN** 说明实际经过的边界及未验证部分，不仅因使用 HTTP 就宣称完成真实集成或 E2E

#### Scenario: Several levels protect the same behavior
- **WHEN** 候选测试涉及同一业务行为的多个范围
- **THEN** 根据各自能发现的错误选择互补检查，不机械重复全部组合，也不删去高层独有的装配证据

### Requirement: Apply sourced methods proportionally

方法指导 SHALL 保留原始来源和适用条件，按当前风险选择输入分区、边界、状态迁移、故障或性质检查。Agent MUST 保留项目已知契约；未知权限、幂等语义、时限等不得由经验资料补造。不要求每项任务完成全套方法清单。

#### Scenario: A known invariant makes generated tests useful
- **WHEN** 广泛输入或动作序列需要保护，且已有独立依据支持不变量或参考模型
- **THEN** 可以采用属性或状态模型测试，保留反例及其复现条件；无可靠性质时不以随机次数代替判定依据

#### Scenario: The project lacks an idempotency rule
- **WHEN** 重复请求会影响预期，但产品尚未确定幂等语义
- **THEN** 先明确该规则缺口，继续不依赖它的设计，不擅自规定 token、保留期或响应码

### Requirement: Distinguish business effects from compatibility checks

接口测试 SHALL 按选中风险检查请求／响应及业务效果，并区分认证、对象权限和操作权限。集成测试 MUST 保留承载目标风险的真实边界；消费者驱动契约结果不得替代提供者完整业务与副作用证据。

#### Scenario: A valid response hides a missing write
- **WHEN** 接口返回成功且符合格式，但目标行为承诺持久化或触发后续动作
- **THEN** 设计对应结果的观察和断言；只有响应证据时不宣称业务完成

#### Scenario: An authenticated actor targets another owner
- **WHEN** 已确认对象归属和权限规则，调用者可访问接口但无权操作目标对象
- **THEN** 验证拒绝及目标未被违规读取或修改，不把登录成功当权限覆盖

#### Scenario: A database behavior is replaced by a fake
- **WHEN** 目标风险是数据库约束或事务行为，但测试替换了数据库
- **THEN** 补真实边界的验证路径，或明确当前只覆盖替身上的行为

#### Scenario: Only the consumer side of a contract ran
- **WHEN** 消费者测试通过，但提供者验证尚未执行
- **THEN** 保留提供者验证缺口，不宣称双方兼容；双方验证通过也不据此宣称业务副作用正确

### Requirement: Distinguish component checks from end-to-end journeys

组件／页面／E2E 设计 SHALL 以选定用户任务或系统流程为对象，说明真实范围、前置数据、完成信号及结果断言。浏览器隔离不得冒充后端数据隔离，局部模拟不得冒充完整业务链验证。

#### Scenario: UI behavior uses simulated responses
- **WHEN** 页面测试用模拟响应检查提示、输入保留或恢复
- **THEN** 可以保留该测试，但明确它验证本方页面行为，不证明真实服务协作

#### Scenario: A successful click does not prove saved state
- **WHEN** 用户任务要求保存后重新打开仍可读取结果
- **THEN** 检查重新读取的业务状态，不仅核对按钮点击或瞬时成功提示

#### Scenario: Tests share a mutable backend
- **WHEN** 浏览器会话独立，但账号或后端数据可能互相影响
- **THEN** 准备可隔离的数据及恢复方式，按可观察条件等待完成，不靠任意休眠或执行顺序维持通过

### Requirement: Route implementation without replacing working tools

用户要求实现时，自动化入口 SHALL 沿用合适的项目测试框架、目录和命令，并将方法指导交给可用实施工具。没有合适框架时 MUST 根据测试目标和技术环境选择接入路径；不得把所有无框架任务导向浏览器 E2E。

#### Scenario: Existing API or browser automation fits the task
- **WHEN** 已有框架能够取得本次所需证据
- **THEN** 沿用它补测试和验证，不另装 e2e、不自动迁移既有套件

#### Scenario: An API-only project has no browser need
- **WHEN** 任务只需要接口行为证据
- **THEN** 使用或选择项目技术栈合适的接口执行方式；缺少实施能力时明确交接缺口，不引入无关浏览器基础设施

#### Scenario: A suitable project has no E2E framework
- **WHEN** 用户要求接入并运行 E2E，项目条件适合官方 e2e 框架且没有合适的既有框架
- **THEN** 按需获取与实际框架版本匹配的官方 e2e Skill，完成最小配置、首条业务测试及运行验证
- **AND** 不维护伪称官方的改写副本，不把仅下载 Skill 或初始化配置称为接入完成

### Requirement: Respect execution scope and external dependency limits

Agent SHALL 区分设计与获准实施；已授权的正常步骤连续完成，超出授权的环境、凭证、数据或费用变化才请求决定。第三方 Skill MUST 服从当前任务边界，不得据其默认步骤覆盖无关文件或扩大权限。

#### Scenario: The user requests design only
- **WHEN** 用户只要求方法、设计或计划
- **THEN** 不安装依赖、启动应用或执行产品测试，给出设计与实施条件

#### Scenario: Framework setup encounters an incompatible environment
- **WHEN** 包版本、运行环境、网络、凭证或宿主能力阻止实施
- **THEN** 报告已完成部分、具体失败和下一动作；不擅自升级全局环境、覆盖已有配置或伪造可运行状态

#### Scenario: Deterministic tests do not require a model
- **WHEN** 当前用例能以确定性操作和断言取得所需证据
- **THEN** 不强制配置模型；实际使用 AI 步骤时才核对模型和凭证条件

### Requirement: Deliver current evidence and meaningful failure detection

自动化交付 SHALL 区分设计、脚本生成、接入和实际运行，关联本轮版本、命令、范围与证据。Agent MUST 区分首次通过、重试后通过、失败、跳过和环境受阻；不能由旧报告或单一退出码放大结论。

#### Scenario: A run fails before writing a new report
- **WHEN** 本轮配置或启动失败，磁盘仍存在旧报告
- **THEN** 以本轮命令和失败证据报告受阻，不将旧报告作为本轮通过依据

#### Scenario: A retry passes after an initial failure
- **WHEN** 首次执行失败而重跑通过
- **THEN** 保留首次失败和重试结果，不称为稳定通过；区分业务重试、断言等待和测试重跑

#### Scenario: Newly implemented checks need sensitivity evidence
- **WHEN** 新自动化测试准备交付，且存在安全可逆的判错验证方式
- **THEN** 用目标 RED、已知失败变体或受控故障核实测试能够发现目标错误，恢复后再运行正常路径
- **AND** 无法核实时明确未验证的探错能力，不破坏生产环境或为制造 RED 改坏现有实现
