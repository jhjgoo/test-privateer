## ADDED Requirements

### Requirement: Use Modern Web Guidance as implementation evidence
UI/UX 评审在需要现代平台实现、浏览器兼容性或旧 Web 写法依据时 SHALL 读取 Modern Web Guidance 参考，并在获准执行时使用其指南检索和 `legacy-scan`。MWG 指南 SHALL 作为实现依据，MUST NOT 替代产品承诺、适用标准或真实渲染／操作证据；扫描输出 SHALL 作为候选处理并逐项复核。

#### Scenario: Modern implementation needs guidance
- **WHEN** 界面问题的判断取决于现代平台用法或兼容性边界
- **THEN** 检索并引用具体 MWG 指南，同时保留产品任务、适用标准或设计承诺作为最终判定依据

#### Scenario: Legacy scan reports findings
- **WHEN** `legacy-scan` 输出候选旧写法
- **THEN** 逐项按指南验证规则和真实渲染／操作证据复核，报告区分候选、已证实、不适用、证据不足和未覆盖
