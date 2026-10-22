# Spec Delta

## MODIFIED Requirements

### Requirement: Apply sourced methods proportionally
方法指导 SHALL 保留原始来源和适用条件，按当前风险选择输入分区、边界、状态迁移、故障或性质检查。Agent MUST 保留项目已知契约；未知权限、幂等语义、时限等不得由经验资料补造。不要求每项任务完成全套方法清单。

当风险超出普通确定性用例能力时，SHALL 按风险选择增强方法：并发、重试或顺序依赖优先考虑模型检查或可复现并发探针；有限状态转换优先考虑状态机遍历；受约束输入域优先考虑属性测试；存在独立业务规则时优先考虑参考模型；内存、边界或解析安全优先选择语言适用的验证器、sanitizer 或静态检查。普通用例已足够时 SHALL NOT 强制这些方法。

所选性质或模型 SHALL 映射到真实代码结构或已确认规则，说明边界、工具版本和覆盖范围；交付前 SHALL 在安全可逆条件下用已知失败变体、受控故障或历史反例证明检查能够失败，无法验证时明确探错能力未验证。通过结论 SHALL 限定为模型和边界的通过，不得宣称整个系统已被证明。

#### Scenario: A known invariant makes generated tests useful
- **WHEN** 广泛输入或动作序列需要保护，且已有独立依据支持不变量或参考模型
- **THEN** 可以采用属性或状态模型测试，保留反例及其复现条件；无可靠性质时不以随机次数代替判定依据

#### Scenario: Concurrency risk needs bounded exploration
- **WHEN** 目标风险是重试、并发写入或操作顺序导致的状态错误
- **THEN** 优先选择模型检查或可复现并发探针，记录模型假设、工具版本、可复现调度和失败边界

#### Scenario: Formal method lacks real mapping
- **WHEN** 模型或属性无法映射到真实代码结构，也没有已确认业务规则依据
- **THEN** 不引入模型检查或属性测试；先补齐规则或使用确定性检查覆盖可判定部分

#### Scenario: Property check never fails
- **WHEN** 属性或形式检查已生成，但没有历史反例、受控故障或失败变体证明其能发现目标错误
- **THEN** 交付时明确探错能力未验证，且通过结论只覆盖当前模型、输入域和执行边界

#### Scenario: The project lacks an idempotency rule
- **WHEN** 重复请求会影响预期，但产品尚未确定幂等语义
- **THEN** 先明确该规则缺口，继续不依赖它的设计，不擅自规定 token、保留期或响应码

## ADDED Requirements

### Requirement: Maintain an existing project product verifier
当用户要求维护、修复或复核既有项目产品验证器时，Agent SHALL 先确认验证器资产、权威说明和目标功能范围已存在；不存在时 SHALL 停止并说明需要先生成或确认目标，不虚构维护对象。

维护 SHALL 仅修改验证说明、脚本、夹具或测试资产，不改被测产品代码。每个受影响功能 SHALL 先对账源码／文档理解与真实驱动行为；首次驱动、冷启动会话和异常后 SHALL 先运行只读 doctor。驱动 SHALL 保留原始证据并确认清理后证据仍存在；清理只作用于本次创建的实例或数据，失败 SHALL 清理残留并保留失败证据。

结果 SHALL 报告为 `clean`、`changed` 或 `blocked`。发现 SHALL 分类为文档漂移、验证器缺口或产品缺陷；维护轮只修正前两类，产品缺陷记录复现证据、影响和交接目标后不得顺手修改产品。

#### Scenario: Verifier target does not exist
- **WHEN** 用户要求维护项目验证器，但找不到权威验证资产或目标范围
- **THEN** 报告 blocked 并说明需要确认或先生成验证器，不创建替身后宣称是在维护既有资产

#### Scenario: Doctor fails after a cold start
- **WHEN** 新会话准备复用验证器
- **THEN** 先运行只读 doctor；未通过时不启动用户路径驱动，先报告环境和阻塞证据

#### Scenario: Source and live behavior disagree
- **WHEN** 源码理解与实际驱动结果不一致
- **THEN** 记录差异并分类为文档漂移、验证器缺口或产品缺陷；只有前两类进入本轮验证资产修正

#### Scenario: Evidence survives cleanup
- **WHEN** 验证路径执行完成并进入清理
- **THEN** 证据被保存到非临时位置或项目指定位置后，才清理本次实例；清理失败保留残留说明和安全处理建议
