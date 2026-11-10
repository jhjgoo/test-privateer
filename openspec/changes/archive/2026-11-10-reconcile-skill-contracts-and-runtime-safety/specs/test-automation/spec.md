## MODIFIED Requirements

### Requirement: Route implementation without replacing working tools

用户要求实现时，自动化入口 SHALL 沿用合适的项目测试框架、目录和命令，并将方法指导交给可用实施工具。没有合适框架时 SHALL 根据目标、技术环境及用户选型委托判断接入路径；没有委托且选择会实质改变长期依赖、维护方式、费用或执行边界时 SHALL 先说明影响并确认。用户已指定或明确委托选型时 SHALL 在边界内选择；既有栈内客户端或标准库临时探针不自动构成长期框架决策。MUST NOT 把所有无框架任务导向浏览器 E2E，也不得把选型委托当作安装、联网、付费、替换既有套件或产品执行授权。该规则 SHALL 在 Setup、API、E2E 和自动化入口保持一致，不强制单层任务先执行完整 Setup。

#### Scenario: Existing API or browser automation fits the task
- **WHEN** 已有框架能够取得本次所需证据
- **THEN** 沿用它补测试和验证，不另装 e2e、不自动迁移既有套件

#### Scenario: An API-only project has no browser need
- **WHEN** 任务只需要接口行为证据
- **THEN** 使用或选择项目技术栈合适的接口执行方式；缺少实施能力时明确交接缺口，不引入无关浏览器基础设施

#### Scenario: A suitable project has no E2E framework
- **WHEN** 用户要求接入并运行 E2E，项目条件适合官方 e2e 框架且没有合适的既有框架，对应选型及所需安装／执行已有授权
- **THEN** 按需获取与实际框架版本匹配的官方 e2e Skill，完成最小配置、首条业务测试及运行验证
- **AND** 不维护伪称官方的改写副本，不把仅下载 Skill 或初始化配置称为接入完成

#### Scenario: Material framework choice has no delegation

- **WHEN** 用户需要补接口或 E2E 能力，项目没有约定，且未委托会新增长期依赖的选型
- **THEN** 对应入口 SHALL 给出最少候选及影响并询问，不因从专项进入而绕过同一选择边界

#### Scenario: Authorized probe uses the existing stack

- **WHEN** 用户授权一次有限接口探针，现有运行器或标准库已能获取所需证据，且未引入新的外部边界
- **THEN** 专项 SHALL 在当前授权内完成探针，不要求为此初始化完整 Setup 或另选长期框架，也不把探针自动登记为项目正式入口


## ADDED Requirements

### Requirement: Separate trial execution from project adoption

自动化实施 SHALL 分别核对当前执行授权、实际能力证据与长期项目采纳。用户已授权的临时或 AI 生成驱动 SHALL 可在本轮范围内试验和验证；MUST NOT 仅因未提交或未长期采纳而阻塞。历史或来源不明脚本仍 SHALL 核对执行授权及安全边界，不因存在即可运行。

本轮试验通过 SHALL 保留真实驱动、证据和恢复结果；未取得权威采纳依据时 MUST NOT 自动把临时入口及结果升级为项目长期 Harness 入口或 verified 状态。既有六种长期 Harness 状态 SHALL 保持不变。

#### Scenario: Temporary driver is authorized but not adopted

- **WHEN** 用户要求生成并验证临时驱动，同时明确不将其设为项目长期入口
- **THEN** Agent SHALL 执行获准试验并报告实际结果，保持长期入口和采纳状态不变

#### Scenario: Historical script has no current execution authority

- **WHEN** Agent 发现来源不明的历史脚本，任务尚未授权运行
- **THEN** Agent SHALL 保留待核对项，不自动执行，不把脚本存在记为能力已验证

#### Scenario: Only driver code is requested

- **WHEN** 用户只要求编写测试驱动而未授权运行
- **THEN** Agent SHALL 交付代码及运行入口并明确未运行，不以需要证明 Harness 可用为由启动产品


### Requirement: Complete unit testing according to the authorized branch

单元测试 SHALL 同时按请求的设计、只编写、编写并验证范围，以及新行为／缺陷保护或既有行为保护目标决定完成条件。实际 RED 仅 SHALL 作为相应 TDD 阶段的证据要求，MUST NOT 成为所有单元任务的统一交付前提。

设计和只编写任务 SHALL 按授权交付判据或代码，说明未运行；编写并验证任务 SHALL 运行获准目标并报告真实状态。新行为／缺陷保护测试首轮通过时 SHALL 核对行为是否已存在及断言能否区分目标缺陷；既有行为测试首轮通过 SHALL 可作为该次观察，不强制破坏产品来制造 RED。执行失败或条件不足 SHALL 保留真实原因。该 Skill MUST NOT 因验证要求取得产品修改权限，或把有效 RED 宣称为整个开发任务已完成。

#### Scenario: Design-only or code-only unit request

- **WHEN** 用户只要求设计或编写单元测试，明确不运行
- **THEN** Agent SHALL 完成对应交付并说明未执行，不索要或伪造实际 RED，不运行测试或启动产品；读取源码和既有约定仍可按任务范围进行

#### Scenario: Characterization test passes on the first run

- **WHEN** 用户要求为既有行为补保护测试，目标测试首轮通过
- **THEN** Agent SHALL 核对目标与断言并报告真实 GREEN 和证据边界，不为满足模板修改产品或制造失败

#### Scenario: A defect protection test produces a valid RED

- **WHEN** 获准执行的缺陷保护测试因目标业务缺陷失败
- **THEN** Agent SHALL 保留命令、实际失败原因及证据，交接后续实现；不把依赖、语法或环境失败算作有效业务 RED

#### Scenario: A new behavior test is unexpectedly green

- **WHEN** 新行为保护测试首轮通过而原先预期失败
- **THEN** Agent SHALL 调查目标行为与断言适用性，报告真实发现，不伪造失败记录或跳过验证直接声称有效 RED
