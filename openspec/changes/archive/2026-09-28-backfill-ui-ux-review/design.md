# Design

## Context

UI/UX 专项评审已通过 `b99564d` 进入仓库。以当前已合并内容归纳规格，不恢复已被替换的中间 Skill 名称或旧方案。

## Goals / Non-Goals

保留可观察契约、正常边界及原始来源；不复制完整 Skill，不新增模型规则，不补造历史审批和验证。

## Decisions

采用一个能力规格和一份回填 change。方法、模板继续维护在 `skills/reviewing-ui-ux/` 及 `skills/test-privateer/` 中的专项路由。当前规格表示应遵循的契约，不等于模型行为保证。

## Risks / Trade-offs

源码合并可核对，历史样本的完整行为证据未在本次重跑。迁移检查限于来源、条款与场景一致性及 OpenSpec 校验；原始评测记录留本地或原 Git 历史，不作为归档附件。
