# 主流 SDD 框架的过程产物与质量把关共性

日期：2026-09-15
目的：为 Test Privateer 的 `challenging-change-specs` 子技能提供框架无关依据。本文只采信框架官方文档、源码仓库模板或官方文档站；不把社区评论当作框架事实。

## 结论先行

主流 Spec-Driven Development（SDD）框架的差异主要在**治理强度和文件形态**，不在核心思想。它们共同把一次变更拆成一条可追溯的契约链：

```text
意图与边界 -> 行为与判定依据 -> 技术决策 -> 工作切分 -> 实现证据 -> 归档后的当前事实
```

质量把关者不应检查某个框架“有没有某个固定文件名”，而应检查这条链是否能支持三个动作：

1. **人在实现前能否看懂并否决错误方向**；
2. **实施者能否不发明业务规则、边界和 oracle 地完成工作**；
3. **实现后的证据能否证明变更已收敛，并把新事实归档为可维护的当前规格**。

## 框架事实

### GitHub Spec Kit

官方定位是“先定义要构建什么，再构建”，强调意图驱动、多步精化、组织原则和 guardrails。核心流程为：

```text
constitution -> specify -> plan -> tasks -> implement -> converge
```

主要产物与动作：

- `constitution`：项目原则、质量门槛和治理约束。
- `spec.md`：用户故事、优先级、独立测试、验收场景、边界情况、功能需求、成功标准。
- `plan.md`：技术上下文、项目结构、constitution 检查、复杂度例外。
- `tasks.md`：按用户故事和阶段组织，含依赖、并行机会、测试任务和执行顺序。
- `analyze`：跨 `spec.md`、`plan.md`、`tasks.md` 检查重复、歧义、欠定义、原则冲突、覆盖缺口和不一致。
- `converge`：对照 spec、plan、tasks 和 constitution 评估代码，把剩余工作追加为新任务。

对质量门的启示：SDD 不是“生成文档”，而是让规格、计划、任务和实现围绕同一意图收敛；constitution 提供项目级 guardrails。

来源：

- https://github.com/github/spec-kit
- https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md
- https://raw.githubusercontent.com/github/spec-kit/main/templates/plan-template.md
- https://raw.githubusercontent.com/github/spec-kit/main/templates/tasks-template.md
- https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/analyze.md
- https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/converge.md

### AWS Kiro Specs

Kiro 将规格定义为结构化产物，用于把高层想法转成可执行实施计划。每个 Feature/Bugfix 规格通常生成：

- `requirements.md` 或 `bugfix.md`
- `design.md`
- `tasks.md`

Feature 流程支持 Requirements-First 与 Design-First 两种入口，但最终都要形成可审查、可执行的任务。需求使用 EARS 风格描述，例如 `WHEN ... THE SYSTEM SHALL ...`，以降低歧义并支持测试转化。`Analyze Requirements` 会跨需求检查逻辑不一致、歧义、冲突约束、未说明假设和缺失边界。任务执行会解析依赖并把独立任务分波并行。

Kiro 还把 Correctness / property-based testing 视为规格质量的一部分：先从需求提取可验证性质，再生成大量随机样例寻找反例；官方文档同时说明这是证据增强，不是形式化证明。

对质量门的启示：结构化语法不是目的；可测试陈述、跨需求一致性、任务依赖和性质/反例思维才是关键。

来源：

- https://kiro.dev/docs/specs.md
- https://kiro.dev/docs/specs/feature-specs.md
- https://kiro.dev/docs/specs/feature-specs/requirements-first.md
- https://kiro.dev/docs/specs/feature-specs/tech-design-first.md
- https://kiro.dev/docs/specs/analyze-requirements.md
- https://kiro.dev/docs/specs/correctness.md
- https://kiro.dev/docs/specs/best-practices.md

### OpenSpec

OpenSpec 的核心心智是“先同意，再自信构建”。它把仓库分成两类事实：

- `openspec/specs/`：当前系统行为的 source of truth。
- `openspec/changes/<name>/`：一次变更的提案、delta specs、技术设计、任务清单和后续证据。

典型产物链：

```text
proposal -> delta specs -> design -> tasks -> implement -> verify/sync/archive
```

delta spec 使用 `ADDED`、`MODIFIED`、`REMOVED` 描述相对当前规格的变化；archive 时把 delta 合并回主规格。官方文档强调“fluid not rigid”：产物顺序是依赖和可用上下文，不是不可回退的瀑布门。实现前建议按 proposal、delta specs、design、tasks 的顺序审查；实现后 `/opsx:verify` 从 completeness、correctness、coherence 检查实现与规格是否匹配。

OpenSpec 对好规格的定义很明确：行为而非代码；一个需求一个可观察的 `MUST/SHALL`；每个需求至少有一个真正行使该需求的 GIVEN/WHEN/THEN 场景；重要错误和边界不能只有 happy path；一次变更应能一句话说明意图。

对质量门的启示：brownfield 变更必须区分“当前事实”和“提议 delta”；归档不是移动文件，而是把已验证的新事实折叠回唯一 truth。

来源：

- https://github.com/Fission-AI/OpenSpec
- https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/overview.md
- https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/opsx.md
- https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/commands.md
- https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/writing-specs.md
- https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/reviewing-changes.md

### BMad Method

BMad 的核心是“选择能安全 fits 这次变更的最小规划路径”。官方文档把 well-defined intent 定义为：完成时什么必须为真、什么不能变、什么在范围外；足以让他人不猜测地构建，且不比这更长。

它把产品探索、PRD/PRFAQ、UX、架构和实施合同分层：

- PRD/PRFAQ/UX/Architecture：为多人、多 epic 或长期一致性保存决策。
- `SPEC.md`：实施读取的 canonical contract，包含 Why、Capabilities、success、Constraints、Non-goals、Success signal、Assumptions、Open Questions。
- `stories.yaml`：可把 epic 拆成有序 story，可声明 human checkpoint。
- `bmad-build`：先调查真实代码库，记录复用与不改动边界，实施并生成 implementation record。

对质量门的启示：规划深度要随风险右 sizing；`SPEC` 必须是下游唯一合同，来源文档只作追溯，不应让实施者重新考古；实现记录和 deferred work 是收敛证据的一部分。

来源：

- https://github.com/bmad-code-org/BMAD-METHOD
- https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/docs/plan/choose-a-planning-path.md
- https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/docs/plan/define-requirements-and-a-specification.md
- https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/docs/build/build-a-change.md
- https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-spec/assets/spec-template.md
- https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-spec/assets/stories-schema.md

### BDD / Specification by Example

Cucumber 官方文档把 BDD 定义为通过具体真实例子建立共同理解，并用自动检查的文档连接业务与技术。核心循环是：

```text
Discovery -> Formulation -> Automation
```

Example Mapping 在开发前把故事、规则/验收标准、具体例子和未答问题分开：例子揭示规则，未答问题显式保留，不伪装成结论。好的例子应具体、面向领域问题，可转化为自动验收测试；验证外部可观察结果，而不是默认验证内部实现。

对质量门的启示：SDD 的测试视角不是后置“写用例”，而是在需求形态中寻找规则、例子、反例和 open questions；没有 oracle 的叙述不能被称为验收标准。

来源：

- https://cucumber.io/docs/bdd/
- https://cucumber.io/docs/bdd/example-mapping/
- https://cucumber.io/docs/bdd/examples/
- https://cucumber.io/docs/gherkin/reference/

## 框架产物角色映射

| 通用角色 | Spec Kit | Kiro | OpenSpec | BMad | BDD |
| --- | --- | --- | --- | --- | --- |
| 意图与边界 | spec 用户故事、非目标/假设 | requirements / bugfix | proposal | SPEC Why、Non-goals | story |
| 当前事实与变更类型 | constitution、spec 状态 | requirements / bugfix | `specs/` 与 delta ADDED/MODIFIED/REMOVED | project context、SPEC | living documentation |
| 行为与 oracle | acceptance scenarios、success criteria | EARS、acceptance criteria | SHALL/MUST + scenarios | capabilities success、success signal | rules + examples |
| 技术决策 | plan.md | design.md | design.md | architecture/companions | formulation 技术边界 |
| 工作切分 | tasks by story/phase | tasks + dependencies | tasks.md | stories.yaml / build | example/story slices |
| 执行与收敛 | converge | task status、PBT | verify、sync、archive | implementation record、review | automated examples |
| 治理约束 | constitution | design/testing strategy | project config、review | architecture spine | team shared understanding |

## 常见断点

1. **Spec theater**：文档被生成，但人未审查，实施者仍从聊天或猜测补规则。
2. **意图漂移**：变更名、proposal、design、tasks 描述的不是同一个问题。
3. **边界真空**：只说要做什么，不说什么不能变、什么不做，实施者自行扩权。
4. **what/how 污染**：需求混入实现细节，或设计没有解释关键 seam 和迁移。
5. **无 oracle 的验收**：使用“快、稳健、友好、正确”等不可判定词。
6. **happy path only**：错误、并发、权限、数据边界、兼容、回滚没有场景或风险处置。
7. **任务覆盖缺口**：需求无任务、任务无需求来源、巨型任务隐藏真实决策。
8. **依赖不可执行**：任务顺序、并行文件边界、外部迁移或人工步骤不清。
9. **代码库失配**：设计忽视既有调用点、数据结构、架构规则或已有测试。
10. **证据漂移**：任务勾选、verify、review、commit、状态字段彼此不是同一快照。
11. **跳过无理由**：E2E、类型检查、迁移验证或回归被跳过，却没有替代证据。
12. **归档造假**：未验证 delta 被合并进 source of truth，当前规格从此错误。
13. **一次性大杂烩**：一个变更包含多个可独立交付意图，审查成本超过价值。
14. **文档过重**：低风险小改被套完整框架，导致无人阅读。

## 对 `challenging-change-specs` 的设计约束

1. **框架无关**：识别 artifact role，而不是强制 OpenSpec/Spec Kit 文件名。
2. **阶段相关**：实施前关注可实施性；实施后关注收敛证据；归档前关注 truth 更新。
3. **风险定深度**：核心契约链总是检查；安全、数据、并发、兼容、跨系统变更加深边界探针。
4. **测试视角**：每个验收主张都要有 oracle、可观察结果和合适测试层级，但不要求穷举所有用例。
5. **研发视角**：检查任务、调用点、迁移、回滚和并行可执行性，不替开发选择实现方案。
6. **证据优先**：未读代码时不判断实现质量；未执行测试时不宣布测试通过。
7. **少而准**：只报告会改变理解、实施、验证或放行决策的断点。
8. **不制造模板税**：缺角色只在阶段需要它时是 finding；不为格式补格式。
