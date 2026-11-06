# Spec Delta

## MODIFIED Requirements

### Requirement: Keep blind testing inputs and outputs auditable

每个盲测 wave SHALL 记录 Run ID、wave ID、目标版本、质量视角、子代理会话或任务 ID、模型与宿主、稳定操作基线、允许读取的项目输入、明确未披露的开发材料、任务包哈希、输出路径和证据路径。

稳定操作基线 MAY 包含宿主固定规则、全局 RTK、全局／项目级 Skill、项目 `AGENTS.md`／`CLAUDE.md`、项目测试配置和获准 CLI；这些能力不因全局安装、自动注入或父级继承而构成开发上下文污染。子代理 SHALL 按任务需要使用这些能力。发现未预先列出的稳定操作基线时，Loop SHALL 补记其名称、来源和可取得的版本或哈希，并检查是否包含任务特定开发材料。

开发 Agent 的聊天上下文、实现理由、修复假设、实现 diff、开发自测结论、既有 Finding 结果、预期缺陷、评审 rubric，以及携带这些内容的会话记忆 MUST NOT 进入盲测会话。只有发现这类材料且无法剥离或审计时，该 wave 才 SHALL 视为无效或标记受阻。

子代理 SHALL 只写隔离输出，不得更新共享 `run.md`、权威测试资产、公共报告或产品代码。单一合成者 SHALL 核对实际调度、任务特定输入、Skill 加载、工具轨迹、文件变化和原始证据后，才更新共享轮次和结论。

#### Scenario: Test agent uses project and global capabilities

- **WHEN** 冷启动子代理读取全局 RTK、全局或项目级 Skill、项目规则及获准 CLI，且这些输入不包含本次开发叙事或既有结果
- **THEN** Loop SHALL 将它们记录为稳定操作基线并继续判读，不得仅因继承或未预先枚举而使 wave 无效

#### Scenario: Project rule contains development-specific results

- **WHEN** 项目规则、记忆或自动注入内容包含本次实现理由、diff、开发自测结论、既有 Finding 结果或 rubric
- **THEN** Loop SHALL 隔离该内容；无法隔离时该 wave SHALL 不计入盲测完成

#### Scenario: Blind workspace inherits parent repository rules

- **WHEN** 冷启动会话加载父目录或当前项目的 `AGENTS.md`、项目规则、全局 RTK、Skill 或 CLI
- **THEN** Loop SHALL 按内容判断并记录稳定操作基线；只有其中包含任务特定开发材料且无法隔离时，该 wave 才 SHALL 无效或受阻

#### Scenario: Subagent reports a defect without a run

- **WHEN** 子代理只描述潜在问题，但没有实际操作、命令、输出或产品状态证据
- **THEN** 合成者 SHALL 将其保留为待验证假设或丢弃，不得作为已证实 Finding 写入最终报告

#### Scenario: Parallel blind testers return results

- **WHEN** 高风险 Loop 分派多个独立测试子代理
- **THEN** 每个子代理 SHALL 使用隔离输出，只有单一合成者可以去重、复核并更新当前 Run ID 的共享资产

### Requirement: Block or disclose when blind subagents are unavailable

宿主不能创建新的子代理会话、不能排除开发会话或任务特定开发材料，或只能在同一上下文中模拟角色时，完整 Loop SHALL 在盲测门槛标记 `blocked`。无法导出完整系统基线，或子代理使用稳定的全局／项目规则、Skill 与 CLI，本身 MUST NOT 成为受阻理由。

只有用户明确接受降级后，Loop 才能继续同上下文测试，并 MUST 记录降级授权、原因和“独立盲测未完成”的残余风险。普通单层测试请求 SHALL 继续沿对应专项运行，不因完整 Loop 的子代理门槛受阻。

#### Scenario: Host has no subagent capability

- **WHEN** 用户要求完整 Test Loop，但当前宿主无法创建新的测试子代理，或无法排除开发会话与任务特定开发材料
- **THEN** Loop SHALL 停在盲测门槛并报告恢复条件，不得由同一 Agent 伪装为新的盲测代理

#### Scenario: Host exposes normal operational capabilities

- **WHEN** 新子代理会话自动获得宿主固定规则、全局／项目 Skill 和获准 CLI，但不继承开发会话或任务特定结果
- **THEN** Loop SHALL 正常执行盲测，并记录可观察到的操作基线，不得要求用户接受降级

#### Scenario: User explicitly accepts degraded testing

- **WHEN** 用户明确接受在没有独立子代理的情况下继续
- **THEN** Loop SHALL 记录降级并继续获准测试，但最终报告 MUST NOT 声称独立盲测已经完成

#### Scenario: User asks for one direct API check

- **WHEN** 用户只要求一次接口检查而不是完整 Test Loop
- **THEN** 请求 SHALL 继续直达接口测试专项，不强制创建盲测子代理
