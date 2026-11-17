## ADDED Requirements

### Requirement: Remove execution nuance from test cases
测试实验设计 SHALL 将可固化的准备、驱动、观察和判定信息放入 Case 字段、脚本、测试标识或断言；终稿自校 SHALL 将需要执行者凭经验解释目标、观察方式或判定规则、但能够固化的 Case 判为设计缺陷。

#### Scenario: A case requires tribal knowledge to judge
- **WHEN** 执行者只能根据未写出的经验判断某结果是否通过
- **THEN** 终稿自校 SHALL 要求补清 oracle、观察位置或判定规则，或标明该判断为未固化的人工检查边界
