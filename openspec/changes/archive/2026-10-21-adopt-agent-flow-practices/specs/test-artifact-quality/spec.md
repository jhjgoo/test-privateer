# Spec Delta

## MODIFIED Requirements

### Requirement: Lead reports with a bounded conclusion and preserve source meaning

报告 SHALL 先交代当前结论及版本范围、关键未决影响和下一行动，再展开证据；观察明细保留已知原值、类型与所属对象的对应关系，不补造业务译名或路径。完整测试信心报告 SHALL 在结论后提供最小证据摘要，包含测试目标、能表达实际变化的最小示意或对照、前基线、后结果、证据限制和风险判断；最小示意 SHALL 只在比文字更清楚时使用，且不得替代证据明细。

#### Scenario: Correct rejection and unknown null semantics

- **WHEN** 业务拒绝符合已确认规则，而另一结果的空值语义尚未知
- **THEN** 前者可判测试符合预期，后者保留观察与待判定；缺失、null、空字符串、false 与空列表不因排版而合并

#### Scenario: Summary of another person's test records

- **WHEN** 只汇总已有记录，没有实际执行本轮产品测试
- **THEN** 标明来源和核验边界，未执行与未覆盖保持可见，不把汇总工作称为新执行证据

#### Scenario: Reader needs a quick risk decision

- **WHEN** 报告读者需要决定继续、停止、补证或升级处理
- **THEN** 报告 SHALL 用最小摘要呈现目标、前后结果、证据限制和风险，并链接或定位对应明细；不得只给通过率或冗长流水账

#### Scenario: No visual is clearer than prose

- **WHEN** 前后结果可以用一句话或小型表格清楚表达
- **THEN** 报告 SHALL 不强制生成图或 Mermaid，不为了模板增加重复视觉
