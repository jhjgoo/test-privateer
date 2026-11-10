# Spec Delta

## ADDED Requirements

### Requirement: Define a lightweight six-stage Harness contract

自动化设计 SHALL 使用统一但按测试表面裁剪的六段式 Harness：`Prepare`、`Start`、`Drive`、`Observe`、`Preserve`、`Restore`。每段 SHALL 对应一个真实可执行入口、项目权威约定或明确缺口；不得把六段强制拆成六个脚本、六个目录或新的通用服务。

不同表面可以复用同一 Runner：接口测试可以在测试函数中准备身份和数据、发请求、检查业务状态、保存响应与日志并恢复数据；UI／E2E 可以复用浏览器和应用验证器；Agent 评测可以复用任务包、模型调用、轨迹与结果封存。只有与当前目标相关的段需要实现，纯函数或只读检查可以明确 `not_applicable`。

#### Scenario: The API Harness uses one existing runner

- **WHEN** 接口测试已有项目 Runner，且它能准备身份和数据、调用请求、观察业务效果、保存原始输出并清理测试资源
- **THEN** 自动化设计 SHALL 复用该 Runner，记录六段映射，不新增 API 专用 Harness 服务

#### Scenario: A UI check has source assertions but no rendered observation

- **WHEN** UI 测试能检查源码或 DOM 结构，但没有真实渲染、交互结果或清理后仍可读的截图／视频／日志
- **THEN** 自动化设计 SHALL 将对应 Harness 标为 `partial` 或 `declared_unverified`，不得把源码检查扩大为真实 UI 证据

#### Scenario: An Agent evaluation has self-reported success only

- **WHEN** Agent 声称任务成功，但没有可核验的工具轨迹、文件状态、产品状态或原始输出
- **THEN** 自动化设计 SHALL 不标为 `verified`，并列出 `Observe` 或 `Preserve` 的证据缺口

### Requirement: Return actionable Harness readiness without replacing project tools

当用户要求构造或修复 Harness 时，自动化设计 SHALL 优先复用项目现有框架、Runner、驱动和验证器，返回 `verified`、`draft` 或 `blocked` 的交接结果。`verified` 必须由至少一条实际目标路径、独立观察、原始证据和清理后证据可读性支持；`draft` 只能表示资产已形成但仍有未验证段；`blocked` 必须指出不可安全继续的原因和恢复入口。`draft` 不是新的长期 Harness 状态。

自动化设计 SHALL 只修改获准的测试代码、夹具、驱动、验证器或说明，不修改被测产品代码；真实产品违反规则时保留失败证据，不通过改变预期值或放宽断言制造 `verified`。

#### Scenario: A generated Harness is actually driven

- **WHEN** 生成的 Harness 已驱动一条已映射路径，并在清理前保存原始证据、清理后仍能读取证据
- **THEN** 自动化设计 SHALL 返回 `verified`，列出实际入口、证据指针和未覆盖范围

#### Scenario: A Harness is written but not run

- **WHEN** Harness 文件已经生成，但没有真实驱动、独立观察或证据回读
- **THEN** 自动化设计 SHALL 返回 `draft`，保留未验证清单，不称为项目 Harness 已就绪

#### Scenario: Product behavior fails under a useful Harness

- **WHEN** Harness 能真实准备、驱动、观察和留证，但产品行为违反已确认规则
- **THEN** 自动化设计 SHALL 保留失败证据并将结果交给 Finding／缺陷流程；不得修改产品或把 Harness 降级为未验证

### Requirement: Invalidate evidence without inventing a stale status

自动化设计 SHALL 在目标版本、项目规则、接口、数据、环境权限或 Harness 入口发生实质变化时标记相关旧证据失效，并将当前状态重新评估为 `declared_unverified`、`partial` 或 `blocked`。不得增加 `stale` 作为第七个长期状态，也不得以旧报告自动恢复 `verified`。

#### Scenario: The driver path changed after a verified run

- **WHEN** 项目入口或关键驱动发生变化，旧证据不再能证明当前 Harness
- **THEN** 自动化设计 SHALL 保留历史证据指针但撤销当前 `verified` 依据，说明重校准或重跑入口
