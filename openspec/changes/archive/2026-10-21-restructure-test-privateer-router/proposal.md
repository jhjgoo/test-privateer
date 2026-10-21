# Proposal

## Why

基于 `ask-matt` 的写法审计发现：`test-privateer` 的方法论覆盖完整，但主入口以高密度规则呈现，缺少 Matt 式的“处境地图”。用户和模型需要先读大量操作规则才能判断请求属于主线、入口场景、独立能力还是词汇层；路由表也承载过多解释，容易与专项 Skill 边界重复漂移。

近期实际使用还暴露三类风险：凭摘要判断专项能力而不读取目标 Skill；长任务缺少上下文恢复纪律；明确请求可能被拉入完整项目流程。应优化主入口的信息架构，而不是新增通用路由或复制 Matt 的工程流程。

## What Changes

- 重构 `skills/test-privateer/SKILL.md` 的信息架构为稳定层次：
  - 主线：明确请求 → 必要澄清／建图 → 风险与建模 → 用例与自校 → 授权执行 → 证据结论；
  - 入口场景：异常、回归、方案／Prompt／Agent／UI 质检、错题本；
  - 独立能力：不强制进入完整项目主线；
  - 词汇与资产层：TCO、TCON、oracle、artifact-routing。
- 路由表降维为“当前处境 → 专项入口”，详细能力和例外下沉到专项 Skill 或既有共享参考。
- 增加硬规则：宣布某专项能做、不能做或建议跳过前，先读取该 `skills/<name>/SKILL.md`；主入口摘要只用于定位。
- 将“事实归 Agent、业务决策归用户”提升为显眼路由原则。
- 补充上下文纪律：项目建图、变化分析与风险排序优先保持同一上下文；阶段交接、新会话或上下文压缩后先恢复 TCO、路线状态和最近产物，不在认知降级时强行展开完整模型。
- 增加捷径与反例：明确 API／单元／报告请求直达；已有 TCON 不重复建图；只汇总报告不补跑测试；只质检方案不自动进入产品测试；只维护错题本不重走需求建图。
- 增加最小行为评测输入与判据，覆盖直达、宽泛请求、项目续会话和路由前读取目标 Skill 四类风险。

## Capabilities

### Modified Capabilities

- `testing-workflow`: 主入口按稳定主线、入口场景、独立能力和词汇层组织路由；路由判断前读取目标专项；长任务遵守上下文恢复与捷径边界。

## Impact

- 修改 `skills/test-privateer/SKILL.md`。
- 增加或更新 `evals/test-communication/` 的代表性输入与判据。
- 如静态契约需要，更新相关测试。
- 修改 `openspec/specs/testing-workflow/spec.md`（归档时同步）。
- 不新增 Skill；不引入 `ask-matt`、grilling、wayfinder、phase-boundaries 等外部流程名；不实现多 Agent 编排；不改变各专项 Skill 的权威职责。
