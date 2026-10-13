<!-- reviewed-through: A -->
# 错题本

## L-2 解析失败当空值导致覆盖

发生三次：INC-11、INC-24、INC-31；机制与验证见 evidence/events.md。
用户自定义值被删除。纠正做法是在读取失败时停止覆盖，合法空值保留其有效业务语义。
状态：教训，未晋升。

## L-9 失败读取应停止覆盖

Seen 1：10-09 审查再次引用 INC-31。证据见 evidence/events.md。与 L-2 相同机制。

## L-5 North 模型统一限制到 96K

旧协议 v1 规定 North 的模型上限为 96K，见 evidence/events.md。Beta 不属于 North。
状态：规则候选。尚未形成通用规范。

## L-8 缺失字段要保留未知

该教训不在本轮维护范围，原有引用 L-2 与 L-9 仍供历史阅读。请保留本段。
