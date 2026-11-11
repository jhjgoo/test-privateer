## ADDED Requirements

### Requirement: Connect setup to the project completion workflow

Setup SHALL 核对项目实际读取的协作入口及其引用链，在已有等效规则时复用；缺失时在初始化授权和项目流程允许的范围内合并最小测试资产收尾约定。约定 SHALL 覆盖开发交付、验证交付和归档后的影响检查，并指向可定位的共享维护方法。Setup MUST NOT 为此修改第三方 Skill、安装钩子、强制使用 OpenSpec 或把指令保存在仅供事实索引的 project.md 中。

写前 SHALL 展示实际入口及必要变更，保留无关人工内容、已有有效决定、换行和权限；重复运行 SHALL 不产生重复约定。写后 SHALL 回读规则及引用，配置只索引其位置。明确禁止规则修改、只允许预览、缺少权限或无法确定实际入口时 SHALL 报告联动尚未接通，保留 `partial` 与恢复动作；规则冲突 SHALL 保留 `blocked`，不得声称 Setup 或自动同步已完成。

目标方法 SHALL 沿未来会话的实际加载优先级读取，核对必要维护内容，MUST NOT 只检查文件存在或用全局副本代替项目副本验证。缺少方法时 SHALL 保留联动缺口，按已有授权更新或请求对应作用域的更新决定，不静默覆盖项目 Skill。新增交付、维护或验收义务 SHALL 按使用方协作流程变更处理；没有产品代码变化 MUST NOT 单独成为规格豁免理由。

#### Scenario: Ordinary setup connects future development sessions

- **WHEN** 项目已有可读取的协作入口，但缺少测试资产收尾要求，用户要求完整初始化且未排除规则维护
- **THEN** Setup SHALL 最小补充该入口并回读，保留既有项目规则，让新开发会话能沿规则定位维护方法

#### Scenario: Equivalent policy already exists

- **WHEN** 项目入口已经引用等效的维护约定
- **THEN** Setup SHALL 核对并沿用，不追加第二份规则，不为统一措辞重写人工内容

#### Scenario: User excludes changes to project rules

- **WHEN** 用户允许配置和 TCO 写入，但禁止修改协作规则，且项目尚无维护约定
- **THEN** Setup SHALL 保持规则不变，完成获准部分并报告 `partial` 及联动缺口，不把配置保存等同于持续维护接入

#### Scenario: Project copy lacks the method loaded from the host copy

- **WHEN** 用户调用宿主新版 Setup，未来会话优先项目 Skill，但项目同名参考缺少维护方法
- **THEN** Setup SHALL 识别目标内容缺失，不写入失效引用或声称接通；没有包更新授权时保留部分完成，说明作用域与恢复动作

#### Scenario: New completion duties require a behavior change record

- **WHEN** 接入新增开发收尾义务，使用方要求协作流程变化走完整规格流程
- **THEN** Setup SHALL 按该流程记录行为变化，不以 `skip_specs` 的语法校验通过代替适用性判断；已有等效义务且仅校准事实指针时仍可按项目规定豁免

#### Scenario: Existing profile and TCO disagree with current sources

- **WHEN** 校准发现长期资产中的局部待办、进度副本或 Harness 验证声明与当前来源冲突
- **THEN** Setup SHALL 定向核对来源及必要原始证据，移除平行进度账本并修正受影响结论；无法核验时保留具体未知，不得声称已完成校准或全部 verified

#### Scenario: A pending scope choice coexists with confirmed profile errors

- **WHEN** 用户已授权更新已有配置，部分选择待确认，但其他状态已独立证实错误
- **THEN** Setup SHALL 修正并回读不依赖该选择的失实字段，未决范围保持待确认，顶层使用 awaiting_user_confirmation；不只改回复中的草稿而保留失实文件，也不擅自关闭用户决定
- **AND** 只要求预览或禁止写入时仍不得修改文件

## MODIFIED Requirements

### Requirement: Persist setup state and freshness

`.test-privateer/project.md` SHALL 记录配置契约版本、顶层 Setup 状态、最近校准时间、依据版本或来源快照、失效条件、当前阻塞及恢复入口。顶层状态 SHALL 区分 `ready`、`awaiting_user_confirmation`、`partial` 和 `blocked`；`ready` 只表示项目配置、TCO、关键治理决定、适用测试表面和权威资产在项目层面可定位，且开发收尾约定已接入实际协作入口，MUST NOT 表示当前环境、测试、CI 或宿主能力已验证。

Setup SHALL 在可定位时记录 Git 提交，否则记录实际读取的来源集合和日期，MUST NOT 编造版本。失效条件 SHALL 覆盖会改变项目测试方式的规则、产品／架构、构建／CI、测试框架或入口、TCO、治理责任及资产位置变化。

#### Scenario: Saved profile still awaits a decision

- **WHEN** 配置草稿可以保存，但仍有会改变测试范围、责任或安全边界的用户决定
- **THEN** Setup SHALL 将顶层状态标为 `awaiting_user_confirmation` 并记录问题和恢复入口，MUST NOT 因文件已保存而报告 `ready`

#### Scenario: Source snapshot cannot use a commit

- **WHEN** 目标项目没有可定位的版本提交
- **THEN** Setup SHALL 记录本轮实际读取的来源集合和校准日期，不编造提交、标签或版本号
