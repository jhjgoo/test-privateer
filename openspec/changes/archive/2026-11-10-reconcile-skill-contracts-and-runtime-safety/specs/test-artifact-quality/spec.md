## MODIFIED Requirements

### Requirement: Use the selected test surface without losing precision
用例 SHALL 使用执行者在所选层级可准备、操作和观察的语言；保留公开接口契约与单元测试可替换边界上的精确符号及诊断信息，混合请求分别交付。

#### Scenario: Functional case with inaccessible internal state
- **WHEN** 功能用例依赖内部变量，但没有可用准备或观察入口
- **THEN** 改写为有依据的业务操作、标记条件缺口或改派层级，不以变量赋值冒充页面或公开接口操作

#### Scenario: TDD unit case
- **WHEN** 用户要求单元测试或 TDD 切片
- **THEN** 保留真实符号、类型、输入输出、fixture、替身和执行入口；已运行时记录实际结果，适用 TDD 分支有实际 RED 时保留其原因。设计或只编写任务明确未执行，既有行为的真实首轮 GREEN 不强制转成 RED；缺少源码或执行证据时保留缺口，不为通俗化删除诊断信息或编造已运行

### Requirement: Export one authoritative set of cases
XMind 导出 SHALL 复用已定稿用例的编号、内容和来源，脑图作为导出视图，不成为另一套独立维护的用例定义。转换 SHALL 保留编号、层级、准备、步骤、预期、来源以及路径、正则等精确符号；只处理已声明格式中的明确转义，不吞掉普通反斜杠。跳过章节 SHALL 同时排除其正文和表格。不能无损解释的正文或异常 Case 行 SHALL 定位并报告，不静默忽略后宣称完整导出。源文档 SHALL 保持不变，必要归一化只形成导出中间视图。

#### Scenario: Shared preparation and case details
- **WHEN** 源文档使用共用准备与按编号展开的详情
- **THEN** 先按原编号整理完整可转换内容再导出，核对步骤、预期及准备缺口不丢失，不因格式转换改变测试含义

#### Scenario: Literal paths and patterns are exported

- **WHEN** 用例包含 `C:\temp\file.txt`、`\d+`、字面 `\n` 或转义表格竖线
- **THEN** 转换 SHALL 在对应脑图节点保留这些内容的原意与精确符号，不把路径或正则中的反斜杠当作通用转义删除

#### Scenario: Heading-based details require normalization

- **WHEN** 源文档按 tc-P0、tc-P1、tc-P2 层级标题及列表正文描述用例
- **THEN** 导出 SHALL 保留编号、层级及完整详情；无法归一化时报告具体缺口，不生成只有标题的成功交付

#### Scenario: An excluded appendix contains a case table

- **WHEN** 应跳过的附录章节内含历史 Case 表格
- **THEN** 导出 SHALL 排除该章节的表格及正文，并在后续同级或更高级有效章节恢复处理

#### Scenario: A case row cannot be parsed losslessly

- **WHEN** Case 行缺列或包含当前转换子集无法解释的内容
- **THEN** 导出 SHALL 报告具体位置并阻止不完整结果被宣称成功，权威源文档保持不变


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

#### Scenario: MFQ summary preserves the specialist definition

- **WHEN** 共享术语解释 MFQ 的 M
- **THEN** 摘要 SHALL 沿用专项对单个有界功能的定义并提供指针，不改写成多数功能、常用功能或频率优先策略


## ADDED Requirements

### Requirement: Label method output with the actual evidence basis

方法扫描 SHALL 依据实际读取的材料说明视角、来源和未知；输入可以是 PRD、原型、访谈、代码或运行证据，MUST NOT 将方法名或固定模板当作实际来源。推断与未观察行为 SHALL 保持可区分。

#### Scenario: SFDIPOT uses a prototype and interview

- **WHEN** SFDIPOT 扫描只有原型和访谈材料，没有 PRD 或运行证据
- **THEN** Agent SHALL 标注原型／访谈来源及对应观察边界，不自称当前为 PRD 视角，也不声称运行已验证
