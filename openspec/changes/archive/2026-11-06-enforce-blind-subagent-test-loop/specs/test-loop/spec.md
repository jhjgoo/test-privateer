# Spec Delta

## ADDED Requirements

### Requirement: Run a cold-start blind testing wave

完整 Test Loop 进入测试发现或执行阶段时，Loop SHALL 创建至少一个新的冷启动测试子代理。子代理 SHALL 使用独立会话，从当前项目和盲测任务包独立形成质量判断；MUST NOT 继承开发 Agent 的聊天上下文、实现理由、修复假设、开发自测结论、既有 Finding 结果、预期缺陷或评审 rubric。

盲测任务包 SHALL 只包含目标版本、用户可观察契约、项目规则与测试入口、环境与授权、分配的质量视角和不含结果的覆盖排除项。盲测结果封存后，Loop 才能使用实现 diff、开发记录和历史 Finding 做知情回归。盲测阶段与知情阶段 MUST NOT 复用同一子代理上下文。

知情回归 handoff SHALL 显式携带并核对原 Run ID、封存 wave ID、目标版本和封存证据哈希或指针。新的子代理会话 MUST NOT 创建新的 Run ID 或第二套 `run.md`；知情回归子代理 SHALL 只返回隔离输出，由单一合成者更新共享轮次。

#### Scenario: Development change enters a full test loop

- **WHEN** 一个开发 Agent 完成项目变更，用户要求运行完整 Test Loop
- **THEN** Loop SHALL 启动新的盲测子代理，且该子代理的输入不包含开发过程、实现 diff、开发自测结论或既有 Finding 结果

#### Scenario: Blind result is sealed before informed regression

- **WHEN** 盲测子代理完成独立发现并提交证据
- **THEN** Loop SHALL 先保存其原始结果和输入边界，再由另一个上下文使用 diff 和历史证据开展定向回归

#### Scenario: Informed regression starts in a new subagent session

- **WHEN** 封存盲测结果交给新的知情回归子代理
- **THEN** handoff SHALL 保持原 Run ID 并引用封存 wave 与证据；子代理 SHALL 只写隔离输出，不得创建新的 `run.md`

### Requirement: Keep blind testing inputs and outputs auditable

每个盲测 wave SHALL 记录 Run ID、wave ID、目标版本、质量视角、子代理会话或任务 ID、模型与宿主、允许读取的输入指针、宿主自动注入输入、明确未披露的开发材料、任务包哈希、输出路径和证据路径。候选实际收到的系统／开发者输入、父目录项目规则和可用记忆 SHALL 纳入输入审计。宿主不能导出完整基线时，SHALL 记录宿主与版本、全新会话机制、是否 fork、记忆策略和父级规则隔离保证；这些证据足以排除开发上下文继承时可以继续判读。

出现未声明的父级规则、记忆或其他额外输入时，该 wave SHALL 视为无效并在干净工作区重跑；宿主不透明且隔离保证仍不能成立时 SHALL 标记受阻。

子代理 SHALL 只写隔离输出，不得更新共享 `run.md`、权威测试资产、公共报告或产品代码。单一合成者 SHALL 核对实际调度、输入清单、Skill 加载、工具轨迹、文件变化和原始证据后，才更新共享轮次和结论。

#### Scenario: Subagent reports a defect without a run

- **WHEN** 子代理只描述潜在问题，但没有实际操作、命令、输出或产品状态证据
- **THEN** 合成者 SHALL 将其保留为待验证假设或丢弃，不得作为已证实 Finding 写入最终报告

#### Scenario: Parallel blind testers return results

- **WHEN** 高风险 Loop 分派多个独立测试子代理
- **THEN** 每个子代理 SHALL 使用隔离输出，只有单一合成者可以去重、复核并更新当前 Run ID 的共享资产

#### Scenario: Blind workspace inherits parent repository rules

- **WHEN** 冷启动会话实际加载了任务包未声明的父目录 `AGENTS.md`、开发仓库规则或宿主记忆
- **THEN** 该 wave SHALL 不计入盲测完成，并在不继承这些输入的干净工作区重跑；无法消除或审计时 SHALL 标记受阻

### Requirement: Prevent repetitive test waves

Loop SHALL 为已执行检查维护覆盖指纹，至少包含测试表面、身份／数据／初始状态、动作／路径、Oracle 和故障或质量视角。新的测试 wave SHALL 改变至少一个指纹维度，或声明修复回归、稳定性调查、环境恢复或新版本对照等明确复验目的。

完全相同且没有复验目的的执行 MUST NOT 重复。后续盲测子代理可以收到中性的覆盖排除项和分配视角，但 MUST NOT 收到上一轮结果、原因解释或推理正文。

#### Scenario: Loop proposes the same check again

- **WHEN** 新 wave 的覆盖指纹与已完成检查相同，且没有修复、稳定性、环境或版本复验目的
- **THEN** Loop SHALL 跳过该执行并选择新的风险切片，或在没有新增证据价值时停止

#### Scenario: Retry has a distinguishing purpose

- **WHEN** 首次失败后需要相同操作区分不稳定性或确认环境恢复
- **THEN** Loop SHALL 记录复验目的并保留两次证据，不把该重跑当作新的独立覆盖

### Requirement: Scale independent testers by risk

普通完整 Loop SHALL 至少使用一个盲测子代理。高影响、未知面大或发布关键的 Loop 在预算允许时 SHALL 按互不重叠的质量视角分派多个独立子代理；每个 brief SHALL 自包含并指定独立输出。子代理缺席或未返回有效证据 SHALL 形成覆盖缺口，不得计为通过。

#### Scenario: High-risk change has several independent concerns

- **WHEN** 变更同时涉及高影响业务、权限和异常恢复风险，且预算允许并行取证
- **THEN** Loop SHALL 将风险切成独立视角分派给多个子代理，而不是让一个 Agent 顺序重复同一验证

### Requirement: Block or disclose when blind subagents are unavailable

宿主不能创建新的子代理会话、不能证明输入隔离，或只能在同一上下文中模拟角色时，完整 Loop SHALL 在盲测门槛标记 `blocked`。只有用户明确接受降级后，Loop 才能继续同上下文测试，并 MUST 记录降级授权、原因和“独立盲测未完成”的残余风险。

普通单层测试请求 SHALL 继续沿对应专项运行，不因完整 Loop 的子代理门槛受阻。

#### Scenario: Host has no subagent capability

- **WHEN** 用户要求完整 Test Loop，但当前宿主无法创建或审计新的测试子代理
- **THEN** Loop SHALL 停在盲测门槛并报告恢复条件，不得由同一 Agent 伪装为新的盲测代理

#### Scenario: User explicitly accepts degraded testing

- **WHEN** 用户明确接受在没有独立子代理的情况下继续
- **THEN** Loop SHALL 记录降级并继续获准测试，但最终报告 MUST NOT 声称独立盲测已经完成

#### Scenario: User asks for one direct API check

- **WHEN** 用户只要求一次接口检查而不是完整 Test Loop
- **THEN** 请求 SHALL 继续直达接口测试专项，不强制创建盲测子代理
