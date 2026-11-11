# Spec Delta

## ADDED Requirements

### Requirement: Preserve setup scope in Harness handoff results

自动化专项接收 Setup 交接时 SHALL 沿用目标、预期来源、选定表面、项目入口、允许环境、证据位置、隔离恢复边界、写入／执行／采纳授权及预算。已有入口满足目标时 SHALL 复用，只补必要缺口，不新建平行框架；已有适用证据直接交回，不因交接重复执行。

构造／补建及维护 SHALL 分别沿用既有结果契约，不重新定义状态。返回 SHALL 提供实际资产和变化、六段入口／缺口、已执行与未执行动作、目标版本、原始观察及证据、清理／残留和恢复条件，分别说明 Harness 能力、产品结果和采纳依据，不自行改写 Setup 配置。

专项 SHALL 以足够验证已授权缺口的最小路径为界，遵守项目或执行前声明的时间／尝试预算。无法安全恢复的环境、权限或隔离故障 SHALL 留证返回；无新事实 MUST NOT 重复同一失败动作、扩展为完整 Loop 或靠改产品／预期获得通过。临时故障只报告本次结果，项目长期约束须有独立依据。

#### Scenario: Existing evidence satisfies the handoff

- **WHEN** 现有入口和适用版本证据已覆盖所选目标，没有需补能力
- **THEN** 专项 SHALL 交回可回读入口及证据，不为取得相同标签新增资产或重跑

#### Scenario: Environment blocks live verification

- **WHEN** 资产已形成，但只读就绪检查发现环境不可用且本轮无获准恢复路径
- **THEN** 专项 SHALL 在预算内停止相关驱动，返回失败证据、未验证项及恢复条件，不无限重试或固化临时故障为长期状态

#### Scenario: Product behavior fails under the repaired Harness

- **WHEN** Harness 能真实驱动、独立观察、留证和恢复，但产品违反已确认规则
- **THEN** 专项 SHALL 分别返回支撑证据和产品缺陷，不改产品或断言，不因产品失败把有证据的 Harness 降为草案

#### Scenario: An existing verifier is maintained

- **WHEN** Setup 交接已有权威验证资产的修复
- **THEN** 专项 SHALL 沿用维护分支的 `clean / changed / blocked` 并附实际证据，不把动作标签直接等同长期 Harness 状态
