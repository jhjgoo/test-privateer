## ADDED Requirements

### Requirement: Maintain test assets at development and verification handoff

接入项目规则后，当前任务合成者 SHALL 在开发交付、验证交付及归档后核对变化影响：测试方式、治理或入口变化更新项目配置；业务／系统关系、覆盖或长期风险变化更新 TCO；局部结果留在原 change／Run。无相关影响 SHALL 不改文件或校准时间，不强制重跑 Setup、重建地图或补跑测试。

维护 SHALL 先读权威来源与受影响资产，保留历史证据和仍有效决定，只修改受影响字段并回读。配置路径 SHALL 保持相对项目根目录，其他文档链接 SHALL 按各自位置核验，不因维护跨文件资产而破坏原有引用约定。来源冲突、并发修改或超出权限时 SHALL 保留可定位的差异和恢复动作，不覆盖他人变更。缺少证据 MUST NOT 自动提升 Harness 状态、测试判定或风险接受状态。共享资产 SHALL 由唯一合成者维护，分支交回证据，不并发改写。

本轮重新声明或保留 Harness `verified` SHALL 核对其历史证据的对象、版本、实际观察与限制；已读证据不足时 SHALL 按既有状态定义修正，无法访问时保留未核实范围。历史已验证、当前未核实与本轮执行 MUST NOT 混写；任务勾选数和目录存在 MUST NOT 代替原始证据，也不因没有本轮执行而将有效历史证据一律降级。

#### Scenario: A developer changes a test entry

- **WHEN** 一个未继承 Setup 聊天的新开发会话通过项目规则完成测试入口迁移及相关验证
- **THEN** 该会话 SHALL 能沿实际项目入口读取共享维护规则，更新配置中的受影响入口与证据；只有覆盖认知改变才更新 TCO，不需用户再次调用 Setup

#### Scenario: A completed change is archived

- **WHEN** 用户已授权归档，活动 change 的实际来源位置发生迁移
- **THEN** 维护者 SHALL 按真实归档结果修正当前配置及 TCO 的受影响指针，保持历史证据与验收边界；未发生迁移时不得预填归档路径

#### Scenario: An unrelated edit is delivered

- **WHEN** 本次只改无关文案，未改变测试方式、项目覆盖或长期风险
- **THEN** 维护者 SHALL 保持 project.md、TCO 和历史证据不变，不为了完成检查制造资产变更

#### Scenario: Only a source revision pointer has expired

- **WHEN** 重跑校准仅发现来源提交不可定位，其他来源及证据仍支持原结论
- **THEN** 维护者 SHALL 只修正必要指针及来源说明，不借机改写正确正文、重排章节或增加无关细节

#### Scenario: A required update cannot be written

- **WHEN** 新证据影响长期测试资产，但当前任务禁止写入该资产或发现来源冲突
- **THEN** 维护者 SHALL 保留局部任务实际结果，交回受影响字段、证据和恢复动作，不声称资产同步完成，也不自动扩展授权
