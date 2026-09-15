# SDD 框架映射

按产物角色识别材料；不要要求项目改变既有框架文件名。

| 通用角色 | GitHub Spec Kit | AWS Kiro | OpenSpec | BMad Method | BDD / Specification by Example |
| --- | --- | --- | --- | --- | --- |
| 意图与边界 | `spec.md` 用户故事、优先级、非目标、假设 | `requirements.md` / `bugfix.md` | `proposal.md` | `SPEC.md` Why、Capabilities、Non-goals | user story |
| 治理约束 | constitution | design/testing strategy | project config 与 review 规则 | architecture spine、constraints | 团队共同理解 |
| 当前事实与 delta | spec 状态与既有规格 | requirements / bugfix baseline | `openspec/specs/` 与 `ADDED/MODIFIED/REMOVED` | project context 与 canonical contract | living documentation |
| 行为与 oracle | acceptance scenario、success criteria | EARS、acceptance criteria、property | `MUST/SHALL` + scenario | capability success、success signal | rule + concrete example |
| 技术决策 | `plan.md` | `design.md` | `design.md` | architecture/companions | formulation 边界 |
| 工作切分 | `tasks.md` by story/phase | `tasks.md` + dependencies | `tasks.md` | `stories.yaml`、build units | story/example slices |
| 执行证据 | converge 结果 | task status、PBT、测试结果 | verify、sync、archive | implementation record、review | automated examples |
| 归档事实 | 更新后的 specs | 实施后的规格状态 | archive 后的 `openspec/specs/` | story/spec record | living documentation |

## 官方来源

- GitHub Spec Kit: https://github.com/github/spec-kit
- Kiro Specs: https://kiro.dev/docs/specs.md
- OpenSpec: https://github.com/Fission-AI/OpenSpec
- BMad Method: https://github.com/bmad-code-org/BMAD-METHOD
- Cucumber BDD: https://cucumber.io/docs/bdd/
- Example Mapping: https://cucumber.io/docs/bdd/example-mapping/

详细研究记录见 `docs/research/2026-09-15-sdd-frameworks-and-spec-gate.md`。
