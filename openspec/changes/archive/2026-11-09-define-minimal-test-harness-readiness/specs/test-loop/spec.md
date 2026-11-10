# Spec Delta

## ADDED Requirements

### Requirement: Check Harness readiness for selected Run surfaces

完整 Test Loop 在全局项目就绪、Run 合同和冷启动盲测门槛通过后，SHALL 只对本轮选中的测试表面核对 Harness 状态、具体测试用例、目标版本和本轮证据要求。Loop SHALL 逐段确认 `Prepare`、`Start`、`Drive`、`Observe`、`Preserve` 和 `Restore` 是否由可定位入口、已有证据或本轮实际动作覆盖；不得把全项目所有表面都强制初始化。

#### Scenario: An API-only Run selects an API Harness

- **WHEN** 本轮只选择接口行为，且接口 Harness 能准备身份和数据、调用接口、观察业务效果、保存响应／日志并清理本轮资源
- **THEN** Loop SHALL 沿用该入口执行接口用例，不启动无关浏览器，并在 Run 中记录六段证据指针

#### Scenario: A selected surface lacks Drive or Observe

- **WHEN** 本轮选中的测试表面缺少实际刺激入口、独立预期或可核验观察
- **THEN** Loop SHALL 将依赖该表面的执行标为缺口或受阻，不得用源码、健康检查、页面打开或框架名称代替行为证据；不受影响的只读分析仍可继续

#### Scenario: An unrelated surface is not configured

- **WHEN** 本轮只测试 API，而项目 UI Harness 尚未配置
- **THEN** Loop SHALL 不因未选中的 UI 表面缺口阻塞本轮 API 工作，也不得在报告中宣称 UI 已验证

### Requirement: Reuse execution evidence and preserve six-stage boundaries

Loop SHALL 尽量用本轮首次适用执行同时证明 Harness 的相关段，不为获得“已验证”标签机械重复运行。每个选中表面 SHALL 在 Run 中记录实际用例、覆盖的六段、原始证据、清理结果及未覆盖边界。Harness 状态、单项测试判定、轮次状态和最终信心 SHALL 分开记录。

#### Scenario: The first API execution supplies Harness evidence

- **WHEN** 首条接口用例已经完成数据准备、请求驱动、业务观察、证据保存和资源恢复
- **THEN** Loop SHALL 复用该执行的证据更新本轮 Harness 指针，不再为状态标签重复同一检查

#### Scenario: Cleanup removes evidence

- **WHEN** 测试清理在证据保存前删除了日志、响应、截图或轨迹
- **THEN** Loop SHALL 报告 `Preserve` 缺口或环境阻塞，保留失败边界，不把退出码为零写成完整 Harness 证据

#### Scenario: Harness is verified but the product check fails

- **WHEN** 六段 Harness 均有实际证据，但产品断言失败
- **THEN** Loop SHALL 保留产品失败和 Harness 证据，分别进入 Finding／信心报告，不把 Harness `verified` 改写为产品通过

### Requirement: Respect the lightweight boundary

Loop SHALL 复用项目既有 Runner、驱动、验证器和专项 Skill，不新增 Harness 服务、框架或统一注册中心。只有缺口会影响当前选中表面的执行安全、判定依据或证据可信度时，Loop 才阻塞该表面；不得因完整性口号强制 API、UI、E2E、Agent、单元和集成全部运行。

#### Scenario: A direct single-stage request bypasses the full Harness gate

- **WHEN** 用户只要求一次接口检查、单个单元测试、用例编写或报告汇总
- **THEN** 请求 SHALL 继续直达对应专项，不强制创建完整 Run 或项目级六段 Harness

#### Scenario: The project runner is already authoritative

- **WHEN** 项目已有明确 Runner 和测试约定，且当前任务只需补充一个测试用例
- **THEN** Loop SHALL 沿用项目入口，不能因为六段模型而自动更换框架、安装依赖或创建平行资产

### Requirement: Gate detailed analysis with reconnaissance of selected surfaces

完整 Loop SHALL 先从项目地图、变化和规则形成足以选择必要测试表面、待判断主张及最便宜区分动作的最小认识。进入详细风险模型、完整测试分析或用例扩展前，Loop SHALL 复用当前 Run 中仍适用于目标版本、环境和入口的实际执行证据；没有适用证据且当前结论依赖真实执行时，SHALL 先建立最小 Run 合同和盲测任务包，由冷启动子代理执行一次有界侦察探针。

长期 Harness 标为 `verified`，但目标版本、入口、环境或失效条件已经变化时，MUST NOT 替代当前侦察。探针 SHALL 使用当前表面最便宜且能区分可执行性的真实动作，优先判断 `Start`、`Drive` 和 `Observe` 是否可达；能力成立后 SHALL 复用证据校准后续分析，不重复相同覆盖。

没有执行授权，或探针涉及新增环境、凭据、费用、共享数据破坏或生产访问时，Loop SHALL 只做静态侦察并将运行时能力保留为未验证；静态侦察 MUST NOT 计作盲测执行证据。探针证明当前授权和环境无法取得真实刺激或独立观察，且没有已获准替代入口时，Loop SHALL 立即封存原始输出并停止依赖该表面的推进。受阻交付 SHALL 限于当前 Run 状态、探针证据、未执行范围、恢复入口和有界信心报告；MUST NOT 为表现流程完整而生成不能改变恢复与结论的阶段资产。

#### Scenario: Historical API verification does not cover the current revision

- **WHEN** API Harness 长期状态为 `verified`，但证据来自旧版本，当前项目入口只输出固定结果且没有真实请求或独立业务状态
- **THEN** Loop SHALL 在详细接口分析和用例扩展前由冷启动子代理运行一次有界入口探针，将当前能力降为实际证据支持的边界，并在受阻时停止扩展

#### Scenario: Execution is not authorized

- **WHEN** 当前任务只授权分析，或侦察需要新增环境、凭据、费用、共享破坏或生产访问
- **THEN** Loop SHALL 只核对静态入口、合同和风险，保留运行时未验证，不得启动服务、调用产品或把静态结果计作盲测执行

#### Scenario: Browser execution fails before a real page starts

- **WHEN** UI 盲测探针在浏览器启动或真实页面驱动前失败，且源码检查、静态打开脚本或继续补写文档不能提供渲染与操作证据
- **THEN** Loop SHALL 封存失败、标记相关 UI 用例受阻并交付最小恢复入口，不再展开完整测试资产或后续调查／回归阶段

#### Scenario: The bounded probe reaches real UI execution

- **WHEN** UI 盲测探针能够启动真实目标、执行用户操作并取得独立观察
- **THEN** Loop SHALL 复用该证据继续当前 Run，并只补充实际执行所需的分析、用例和报告资产
