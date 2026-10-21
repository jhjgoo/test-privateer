# Spec Delta

## ADDED Requirements

### Requirement: Maintain one testing vocabulary layer
测试领域语言 SHALL 在共享参考中维护唯一权威定义；专项 Skill SHALL 沿用这些术语并只保留各自使用规则、方法和例外。核心术语至少 SHALL 区分测试项、测试条件、测试用例、探索章程、探查、判定依据、测试发现、缺陷和原因判断。`SFDIPOT`、`MFQ`、`PPDCS`、`TCO` 等缩写 SHALL 保留原名，首次面向用户出现时按需提供中文含义和方法入口指针。

同一对象 SHALL 使用同一稳定名称；同义词变化 SHALL 归并到权威术语或说明其语义差异。领域语言层 SHALL 保持轻量，不复制完整方法理论，不把短答复变成术语表。

#### Scenario: Method abbreviation appears
- **WHEN** 产物中首次出现 SFDIPOT、MFQ、PPDCS 或 TCO
- **THEN** 保留原名并按需给出一句中文含义、适用对象和方法 Skill 指针；详细方法不在共享术语层重复展开

#### Scenario: Synonym drift appears
- **WHEN** 同一产物把测试点、测试项和测试条件混用而未说明差异
- **THEN** 归并到权威术语或按编号和定义区分对象成熟度；不因换词造成重复编号或状态漂移

#### Scenario: Short answer already clear
- **WHEN** 一次短答复无需引入新术语
- **THEN** 不强制解释术语表；仅在术语影响理解或判定时就近解释
