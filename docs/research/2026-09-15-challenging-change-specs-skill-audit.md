# `challenging-change-specs` Skill prompt audit

日期：2026-09-15
审计方法：按 `skill-eval/shared/prompt-audit.md` 执行；目标模型证据适配读取 `references/target-model-evidence.md` 与用户提供的 `openai-gpt-6-astra.md` 快照。

## Scope 与 target model

- Scope：
  - `skills/challenging-change-specs/SKILL.md`
  - `skills/challenging-change-specs/references/framework-map.md`
  - `skills/test-privateer/SKILL.md` 中新增的路由行
- Target model：仓库未指定唯一运行模型；按 GPT-6 Astra 类 Agent Skills 使用场景做审计，并避免任何模型专属 API 或行为断言。
- 证据限制：`openai-gpt-6-astra.md` 是用户提供的离线官方文档快照，未在本轮重新联网核验。本 skill 不包含 API 参数、输出 schema、采样或工具调用契约，因此无需依赖快照提出模型迁移修改。

## Prompt surface inventory

- `SKILL.md` frontmatter description：模型可触发，用于 SDD 变更包审查。
- `SKILL.md` 正文：证据边界、产物角色、契约链审查、评审深度、输出契约与完成条件。
- `references/framework-map.md`：按需披露的框架映射，不在主提示常驻。
- `test-privateer` 路由行：把“SDD 变更包质量关口”指向本 skill。
- README 变更不属于运行时 prompt surface，仅作为安装与索引文档。

## Provenance

新 skill 与研究文档均为本轮创建，尚无 git 历史。设计来源是官方 SDD 文档研究与 `writing-great-skills` 的 invocation、progressive disclosure、granularity、pruning 原则；没有从旧模型 workaround 复制行为。

## Findings

无。

审计检查过且无需修改的点：

- Description 只保留一个主触发分支：SDD 变更包质量关口；框架名作为兼容线索，不拆成多个流程。
- Model invocation 是必要的：`test-privateer` 主入口需要自动路由到该子技能；代价由唯一 description 承担。
- 正文使用结果、证据和完成条件，不要求 Chain of Thought、assistant prefill、固定 JSON schema 或模型专属 API。
- `references/framework-map.md` 通过“非通用形态或来源不明时读取”的条件指针披露，避免主 skill 常驻框架细节。
- 评审深度含“从简／标准／加深”，与 Astra 快照中按变更校准验证、避免过度测试的指导一致；同时保留高风险变更的证据门槛。
- 澄清边界只针对会改变结论的业务规则、范围或责任归属，避免无谓暂停。
- Severity 规则绑定下游影响，避免把风格问题升级为 blocker。
- 未发现重复来源、过时角色脚本、否定式 steering 或无操作语句。

## Proposed diff

空。审计未发现需要修改的 prompt surface；这是有效结果。

## Verification obligations

- 结构检查：确认 skill 目录、frontmatter、reference 路径和主入口路由存在。
- 后续若调整 description、输出契约或模型专属行为，应重新执行本审计。
- 行为验证建议使用脱敏 SDD 变更包样本分别覆盖实施前、实施后、归档前和文档-only 输入，观察 finding 定位、判定强度和 P1/P2 分级。
