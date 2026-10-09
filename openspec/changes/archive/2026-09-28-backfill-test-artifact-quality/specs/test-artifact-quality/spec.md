# Spec Delta

## Purpose

规定测试用例与报告如何兼顾业务可读性、技术精确性、可执行条件和证据边界。功能测试与单元测试按各自测试表面表达；摘要突出决策信息，明细保持判定所需语义，脑图只是同一用例源的导出视图。

## ADDED Requirements

### Requirement: Use the selected test surface without losing precision
用例 SHALL 使用执行者在所选层级可准备、操作和观察的语言；保留公开接口契约与单元测试可替换边界上的精确符号及诊断信息，混合请求分别交付。

#### Scenario: Functional case with inaccessible internal state
- **WHEN** 功能用例依赖内部变量，但没有可用准备或观察入口
- **THEN** 改写为有依据的业务操作、标记条件缺口或改派层级，不以变量赋值冒充页面或公开接口操作

#### Scenario: TDD unit case
- **WHEN** 用户要求单元测试或 TDD 切片
- **THEN** 保留真实符号、类型、输入输出、fixture、替身、命令和实际 RED 原因；缺少源码或执行证据时保留缺口，不为通俗化删除诊断信息或编造已运行

### Requirement: Make cases discriminating and independently usable
用例设计 SHALL 保留独立前置、动作、观察与判定依据，并检查所选样本能否区别目标规则与合理错误实现；可执行状态依据已核实条件，不由文档完成推断。

#### Scenario: Missing condition is invisible in current samples
- **WHEN** 某实现漏掉关键条件仍会通过全部所选样本
- **THEN** 补足有区分力的最小对照，按有效约束排除不可达组合，不机械展开所有组合

#### Scenario: Missing environment or rule
- **WHEN** 用例已写完，但环境尚未核实或预期规则未定
- **THEN** 明示准备或规则缺口，不将其标为可执行、已执行或通过

### Requirement: Lead reports with a bounded conclusion and preserve source meaning
报告 SHALL 先交代当前结论及版本范围、关键未决影响和下一行动，再展开证据；观察明细保留已知原值、类型与所属对象的对应关系，不补造业务译名或路径。

#### Scenario: Correct rejection and unknown null semantics
- **WHEN** 业务拒绝符合已确认规则，而另一结果的空值语义尚未知
- **THEN** 前者可判测试符合预期，后者保留观察与待判定；缺失、null、空字符串、false 与空列表不因排版而合并

#### Scenario: Summary of another person's test records
- **WHEN** 只汇总已有记录，没有实际执行本轮产品测试
- **THEN** 标明来源和核验边界，未执行与未覆盖保持可见，不把汇总工作称为新执行证据

### Requirement: Export one authoritative set of cases
XMind 导出 SHALL 复用已定稿用例的编号、内容和来源，脑图作为导出视图，不成为另一套独立维护的用例定义。

#### Scenario: Shared preparation and case details
- **WHEN** 源文档使用共用准备与按编号展开的详情
- **THEN** 先按原编号整理完整可转换内容再导出，核对步骤、预期及准备缺口不丢失，不因格式转换改变测试含义
